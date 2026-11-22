"""Source-specific parsers for listing events and registered transfers.

Keep these definitions separate: provider-classified MLS listings are not
land-registry transfers, and neither series can extend Valery's listing counts.
"""
import csv
from datetime import datetime
from io import StringIO
import json
import math
import re

from bs4 import BeautifulSoup

HOMELEADER = 'https://homeleaderrealty.com/power-of-sale-tracker/'
HOMELEADER_CSV = 'https://homeleaderrealty.com/api/hlr/v1/pos/csv'
TERANET = 'https://teraintelligence.teranet.ca/market_insights/market-insights-q1-2026/'


def count(value):
    if not re.fullmatch(r'\d+', str(value)):
        raise ValueError(f'Expected a nonnegative whole count: {value}')
    return int(value)


def parse_homeleader(content):
    lines = content.lstrip('\ufeff').splitlines()
    metadata = next((line for line in lines if line.startswith('# Power of sale tracker,')), '')
    stamp = re.search(r'Data as of (\d{4}-\d{2}-\d{2}T[\d:]+Z)\.', metadata)
    if not stamp or 'Counts are properties:' not in metadata:
        raise ValueError('Homeleader source timestamp or property-count definition missing')
    as_of = datetime.fromisoformat(stamp[1].replace('Z', '+00:00'))
    reader = csv.DictReader(StringIO('\n'.join(line for line in lines if not line.startswith('#'))))
    required = {'month', 'scope', 'region', 'city', 'property_type', 'new_listings', 'listed', 'active_listings'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Homeleader CSV columns changed')
    points = []
    for row in reader:
        if row['scope'] != 'gta':
            continue  # Regional, city and property-type aggregates overlap the GTA total.
        if any(row[key] for key in ('region', 'city', 'property_type')):
            raise ValueError('Ambiguous Homeleader GTA total')
        match = re.fullmatch(r'(\d{4}-(?:0[1-9]|1[0-2]))( \(to date\))?', row['month'])
        if not match:
            raise ValueError('Invalid Homeleader month')
        period, partial = match[1], bool(match[2])
        value = count(row['new_listings'])  # Not "listed", which includes relistings.
        if value > count(row['listed']):
            raise ValueError('Homeleader new homes exceed listed homes')
        count(row['active_listings'])
        item = {'period': period, 'value': value, 'status': 'observed'}
        if partial:
            item['partial'] = True
        points.append(item)
    points.sort(key=lambda point: point['period'])
    group = {'id': 'power_sale_homes', 'title': 'GTA newly listed power-of-sale homes',
             'unit': 'homes', 'frequency': 'Monthly', 'data_as_of': as_of.date().isoformat(),
             'source': 'Homeleader Realty, GTA Power of Sale Tracker (MLS-derived)',
             'source_url': HOMELEADER, 'download_url': HOMELEADER_CSV,
             'note': 'Residential homes in Toronto, Peel, York, Durham and Halton. Listings for the same home are consolidated; a return within 60 days is not counted as new. Detection uses listing remarks and can miss undisclosed lender sales. These counts use a different definition from Valery and are not spliced together. The current month is incomplete.',
             'series': [{'name': 'Newly listed power-of-sale homes', 'points': points}]}
    validate_distress_group(group)
    return group


def parse_teranet(html):
    soup = BeautifulSoup(html, 'html.parser')
    if 'Ontario power of sale transfer volumes, 2015 to 2025' not in soup.get_text(' ', strip=True):
        raise ValueError('Teranet report edition or Figure 4A changed')
    matches = [script.get_text() for script in soup.select('script')
               if re.search(r'title:\s*"Power of Sale Trends - Years"', script.get_text())]
    if len(matches) != 1:
        raise ValueError('Expected one Teranet annual power-of-sale chart')
    marker = re.search(r'\brender_data:\s*', matches[0])
    if not marker:
        raise ValueError('Teranet embedded chart data missing')
    payload, _ = json.JSONDecoder().raw_decode(matches[0][marker.end():])
    options = payload['options']
    years = options['xaxis']['categories']
    series = options['series']
    if years != list(range(2015, 2026)) or len(series) != 1 or series[0]['orig_header'] != 'count':
        raise ValueError('Teranet annual coverage or count series changed')
    values = series[0]['data']
    if len(values) != len(years):
        raise ValueError('Incomplete Teranet annual counts')
    group = {'id': 'power_sale_transfers', 'title': 'Ontario registered power-of-sale transfers',
             'unit': 'transfers', 'frequency': 'Annual',
             'source': 'Teranet, Q1 2026 Market Insights, Figure 4A', 'source_url': TERANET,
             'note': 'Registered Ontario power-of-sale transfers, 2015–2025. Annual completed transfers, not new MLS listings or active inventory. Extracted directly from the report’s embedded numerical chart data. This fixed report edition does not imply monthly or 2026 coverage.',
             'series': [{'name': 'Registered power-of-sale transfers', 'points': [
                 {'period': str(year), 'value': count(value), 'status': 'observed'}
                 for year, value in zip(years, values, strict=True)]}]}
    validate_distress_group(group)
    return group


def validate_distress_group(group):
    if len(group['series']) != 1:
        raise ValueError('Expected one distress count series')
    points = group['series'][0]['points']
    if any(not math.isfinite(p['value']) or p['value'] < 0 or p['value'] % 1 or
           p['status'] != 'observed' for p in points):
        raise ValueError('Distress counts must be nonnegative observed integers')
    if group['id'] == 'power_sale_homes':
        if group['unit'] != 'homes' or group['frequency'] != 'Monthly':
            raise ValueError('Homeleader count definition changed')
        as_of = datetime.strptime(group['data_as_of'], '%Y-%m-%d')
        end = as_of.strftime('%Y-%m')
        expected = [f'{year}-{month:02}' for year in range(2025, as_of.year + 1)
                    for month in range(1, 13) if f'{year}-{month:02}' <= end]
        if len(expected) < 12 or [p['period'] for p in points] != expected:
            raise ValueError('Homeleader must cover January 2025 through its source month')
        if [bool(p.get('partial')) for p in points] != [False] * (len(points) - 1) + [True]:
            raise ValueError('Only the current Homeleader month must be marked to date')
    else:
        if group['unit'] != 'transfers' or group['frequency'] != 'Annual':
            raise ValueError('Teranet count definition changed')
        if [p['period'] for p in points] != [str(year) for year in range(2015, 2026)]:
            raise ValueError('Teranet must cover 2015–2025')
        if [p['value'] for p in points[-2:]] != [2123, 2979] or any(p.get('partial') for p in points):
            raise ValueError('Teranet counts disagree with the report’s stated totals')
