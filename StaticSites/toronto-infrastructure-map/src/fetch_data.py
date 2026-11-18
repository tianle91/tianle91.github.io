"""Explicit network refresh; publish only after every required source validates."""
from datetime import datetime, timezone
from hashlib import sha256
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from staticsites.pipeline import write_if_changed
from staticsites.sources import get_response, arcgis_result

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/'
OWNERS = {'Transportation Services', 'Toronto Water', 'Parks, Forestry and Recreation',
          'Economic Development and Culture', 'City Planning', 'Toronto Transit Commission',
          'Toronto Hydro Electric System Ltd.', 'Toronto Community Housing Corporation'}
EXCLUDED = {'TS_Moratorium', 'TS_Moratorium_Future', 'TS_CIP_Study', 'CP_Avenue_Study',
            'TS_Lane_Restriction'}

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if not self.skip and tag in ('br', 'p', 'div', 'td', 'li', 'h1', 'h2', 'h3', 'h4'):
            self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
        if not self.skip: self.parts.append(' ')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def plain(value):
    parser = Text(); parser.feed(unescape(str(value or '')))
    return ' '.join(''.join(parser.parts).split())

def safe_url(value):
    value = unescape(str(value or '')).strip()
    if value.startswith('www.'): value = 'https://' + value
    parsed = urlsplit(value)
    return value if parsed.scheme in ('http', 'https') and parsed.hostname else ''

def category(owner, program):
    if owner == 'Toronto Water': return 'water'
    if owner == 'Toronto Transit Commission': return 'transit'
    if owner == 'Toronto Hydro Electric System Ltd.': return 'power'
    if owner in ('Parks, Forestry and Recreation', 'Toronto Community Housing Corporation', 'Economic Development and Culture', 'City Planning'): return 'places'
    return 'roads'

def contract_fields(value):
    # Parse table cells as text, never publish upstream HTML.
    cells = re.findall(r'<td\b[^>]*>(.*?)</td>', value or '', re.I | re.S)
    return {plain(cells[i]): plain(cells[i+1]) for i in range(0, len(cells)-1, 2)}

def normalize(feature, kind):
    p = feature['properties']; owner = plain(p.get('INV_OWNER'))
    program = plain(p.get('INV_DISPLAY_PROGRAM'))
    if owner not in OWNERS or program in EXCLUDED or 'Study' in program: return None
    contracts = contract_fields(p.get('CONTRACT_LIST'))
    state = contracts.get('Contract State', '')
    # Active includes design, procurement and stale schedules. Never infer construction from year alone.
    if p.get('INV_STATUS') == 'Completed' or state.lower() == 'complete': stage = 'Completed'
    elif state.lower() in ('post-construction', 'warranty'): stage = 'Post-construction'
    elif state.lower() in ('construction', 'under construction'): stage = 'Construction'
    elif state.lower() in ('design', 'detailed design'): stage = 'Design'
    elif state.lower() in ('pre-rf(x)', 'planning', 'tender', 'procurement'): stage = 'Planning'
    else: stage = 'Active — schedule unconfirmed'
    return {
        'type': 'Feature', 'geometry': feature.get('geometry'),
        'properties': {
            'id': f"register-{kind.lower()}-{p['OBJECTID']}", 'collection': 'register',
            'title': plain(p.get('INV_PROJECT')) or 'Infrastructure project',
            'location': plain(p.get('INV_LOCATION')), 'description': plain(p.get('INV_DETAIL')),
            'owner': owner, 'category': category(owner, program), 'stage': stage,
            'source_status': plain(p.get('INV_STATUS')), 'schedule': plain(p.get('INV_DURATION_PUBLIC')),
            'start_year': p.get('INV_START_YEAR'), 'end_year': p.get('INV_END_YEAR'),
            'project_number': plain(p.get('PROJ_NUM')), 'program': program,
            'contract_state': state, 'contract': contracts.get('Contract #', ''),
            'source_updated': datetime.fromtimestamp(p['LAST_UPDATED_DATE']/1000, timezone.utc).date().isoformat() if p.get('LAST_UPDATED_DATE') else '',
            'url': safe_url(p.get('INV_WEB_SITE')) or 'https://map.toronto.ca/toinview/',
            'geometry_note': 'City-published location geometry; may represent only part of a project.'
        }
    }

def fetch_layer(kind, get=get_response):
    url = BASE + f'COTGEO_TOINVIEW_PROGRAM_{kind}/FeatureServer/0/query'
    info = arcgis_result(get(url, params={'where':'1=1', 'returnIdsOnly':'true', 'f':'json'}).json())
    ids = sorted(info.get('objectIds') or [])
    if not ids or len(set(ids)) != len(ids): raise ValueError(f'{kind}: empty or duplicate object IDs')
    features = []
    for offset in range(0, len(ids), 150):
        batch = ids[offset:offset+150]
        payload = arcgis_result(get(url, params={'objectIds':','.join(map(str,batch)), 'outFields':'*', 'outSR':4326, 'f':'geojson'}).json())
        rows = payload.get('features', [])
        if payload.get('properties', {}).get('exceededTransferLimit') or {f['properties']['OBJECTID'] for f in rows} != set(batch) or len(rows) != len(batch):
            raise ValueError(f'{kind}: incomplete response')
        features.extend(rows)
    return features

def evidence(url, get=get_response):
    text = plain(get(url).text)
    if len(text) < 500 or 'City of Toronto' not in text: raise ValueError('Invalid project source: '+url)
    # Hash visible text; changes to scripts and styles do not generate review flags.
    return sha256(text.encode()).hexdigest()

def publish(payload, path):
    previous = json.loads(path.read_text()) if path.exists() else {}
    previous.pop('retrieved_at', None)
    if previous == payload: return False
    return write_if_changed(path, json.dumps({'retrieved_at': datetime.now(timezone.utc).isoformat(), **payload}, indent=2, ensure_ascii=False, allow_nan=False)+'\n')

def main():
    watchlist = json.loads((ROOT/'data/major-projects.json').read_text())
    sources = {url:evidence(url) for url in sorted({f['properties']['url'] for f in watchlist['features']})}
    features = []
    counts = {}
    for kind in ('POINT','LINE','POLYGON'):
        rows = fetch_layer(kind); counts[kind.lower()] = len(rows)
        features.extend(f for row in rows if (f := normalize(row, kind)))
    for f in watchlist['features']:
        p = f['properties']; p['needs_review'] = sources[p['url']] != p['reviewed_source_hash']
    features = sorted(watchlist['features']+features, key=lambda f:f['properties']['id'])
    if not any(f['properties']['collection']=='register' for f in features): raise ValueError('No City records')
    publish({'source_counts': counts, 'source_fingerprints': sources, 'features': features}, ROOT/'data/projects.json')
    print(f'Validated {sum(counts.values())} source records; published {len(features)} watchlist and City location records.')

if __name__ == '__main__': main()
