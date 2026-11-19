"""Offline regressions for coverage, source safety and snapshot publication."""
import json
from pathlib import Path
import pytest
from build_site import render
from fetch_data import normalize, plain, safe_url, fetch_layer, publish

ROOT = Path(__file__).resolve().parent.parent

def record(**properties):
    p = {'OBJECTID':1, 'INV_OWNER':'Transportation Services', 'INV_PROJECT':'Bridge work',
         'INV_STATUS':'Active', 'INV_START_YEAR':2025, 'INV_END_YEAR':2026}
    p.update(properties)
    return {'properties':p, 'geometry':{'type':'Point','coordinates':[-79.4,43.7]}}

def test_active_is_not_assumed_under_construction():
    assert normalize(record(), 'POINT')['properties']['stage'] == 'Active — schedule unconfirmed'
    assert normalize(record(INV_STATUS='Completed'), 'POINT')['properties']['stage']=='Completed'
    p=normalize(record(CONTRACT_LIST='<table><td>Contract State</td><td>Construction</td></table>'),'POINT')['properties']
    assert p['stage']=='Construction'

def test_scope_excludes_non_city_work_and_moratoria():
    for p in [{'INV_OWNER':'Metrolinx'}, {'INV_OWNER':'Development Engineering'}, {'INV_DISPLAY_PROGRAM':'TS_Moratorium'}, {'INV_DISPLAY_PROGRAM':'TS_CIP_Study'}]:
        assert normalize(record(**p),'POINT') is None
    assert normalize(record(INV_OWNER='Parks, Forestry and Recreation '),'POINT')

def test_source_html_and_links_are_safe():
    assert plain('Street&lt;br&gt;From: A')=='Street From: A'
    assert safe_url('javascript:alert(1)')==''
    assert safe_url('www.toronto.ca/bridges')=='https://www.toronto.ca/bridges'
    assert '<script>alert(1)</script>' not in render({'features':[], 'text':'</script><script>alert(1)</script>'})

class Response:
    def __init__(self,payload): self.payload=payload
    def json(self): return self.payload

def test_all_id_batches_are_required():
    ids=list(range(1,302)); queries=[]
    def get(url,params):
        queries.append(params)
        if params.get('returnIdsOnly'): return Response({'objectIds':ids})
        return Response({'features':[record(OBJECTID=int(i)) for i in params['objectIds'].split(',')]})
    assert len(fetch_layer('POINT',get))==301
    assert len(queries)==4
    def incomplete(url,params):
        if params.get('returnIdsOnly'): return Response({'objectIds':[1,2]})
        return Response({'features':[record()]})
    with pytest.raises(ValueError,match='incomplete'): fetch_layer('POINT',incomplete)

def test_noop_refresh_preserves_bytes_and_timestamp(tmp_path):
    path=tmp_path/'snapshot.json'
    assert publish({'features':[1]},path)
    before=path.read_bytes(),path.stat().st_mtime_ns
    assert not publish({'features':[1]},path)
    assert (path.read_bytes(),path.stat().st_mtime_ns)==before

def test_committed_snapshot_and_shell():
    data=json.loads((ROOT/'data/projects.json').read_text())
    fs=data['features']; ids=[f['properties']['id'] for f in fs]
    assert len(ids)==len(set(ids))
    major=[f for f in fs if f['properties']['collection']=='major']
    assert len([f for f in major if f['properties']['id'].startswith('gardiner-')])==6
    assert len(fs)>500
    assert data['source_counts']['line']>2000
    html=render(data)
    assert html.startswith('<!DOCTYPE html') and '__PAYLOAD__' not in html
    assert '__EXPLORER' not in html and '__APP_JS__' not in html and '__LOCATION_JS__' not in html and '__VIEW_STATE_JS__' not in html
    assert 'Data sources' in html and 'Track the Gardiner' in html

def test_nearby_uses_full_line_and_polygon_geometry():
    import shutil
    import subprocess
    if not shutil.which('node'): pytest.skip('Node unavailable for geometry regression')
    script = r'''
const assert = require('node:assert/strict');
const {distance} = require(process.argv[1]);
const line={type:'LineString',coordinates:[[-79.5,43.7],[-79.3,43.7]]};
assert(distance(line,43.7,-79.4)<0.01); // midpoint is near, even with distant endpoints
assert(distance(line,43.71,-79.4)>1000);
const polygon={type:'Polygon',coordinates:[[
 [-79.5,43.6],[-79.3,43.6],[-79.3,43.8],[-79.5,43.8],[-79.5,43.6]
],[[ -79.41,43.69],[-79.39,43.69],[-79.39,43.71],[-79.41,43.71],[-79.41,43.69]]]};
assert.equal(distance(polygon,43.65,-79.4),0);
assert(distance(polygon,43.7,-79.4)>700); // a hole is not inside a work polygon
assert.equal(distance(null,43.7,-79.4),Infinity);
'''
    subprocess.run(['node','-e',script,str(ROOT/'src/nearby.js')],check=True)

def test_major_reviewed_geometry_matches_published_snapshot():
    editorial=json.loads((ROOT/'data/major-projects.json').read_text())['features']
    published={f['properties']['id']:f for f in json.loads((ROOT/'data/projects.json').read_text())['features']}
    for f in editorial:
        assert published[f['properties']['id']]['geometry']==f['geometry']
        assert published[f['properties']['id']]['properties']['reviewed_source_hash']==f['properties']['reviewed_source_hash']

def test_url_state_validation_and_roundtrip():
    import shutil
    import subprocess
    if not shutil.which('node'): pytest.skip('Node unavailable for URL-state regression')
    script=r'''
const assert=require('node:assert/strict');global.MapURL=require(process.argv[2]);const V=require(process.argv[1]);
const options={layers:['roads','water'],scopes:['all','major','register'],stages:['open','all','Construction'],owners:['','Toronto Water']};
const state=V.parse('https://example.com/map?lat=43.65&lng=-79.38&z=15&q=A%26B&layers=&radius=750&owner=Toronto+Water',options);
assert.deepEqual(state.view,{lat:43.65,lng:-79.38,z:15});assert.deepEqual(state.layers,[]);assert.equal(state.q,'A&B');assert.equal(state.radius,750);
const url=V.write('https://example.com/map?utm_source=test#anchor',state,options);
assert.equal(new URL(url).searchParams.get('utm_source'),'test');assert.equal(new URL(url).hash,'#anchor');
assert.deepEqual(V.parse(url,options),{...state,legacyProject:false});
const invalid=V.parse('https://example.com/map?lat=&lng=999&z=NaN&layers=unknown&scope=evil&owner=evil&radius=Infinity&basemap=evil',options);
assert.equal(invalid.view,null);assert.deepEqual(invalid.layers,options.layers);assert.equal(invalid.scope,'all');assert.equal(invalid.owner,'');assert.equal(invalid.radius,500);assert.equal(invalid.basemap,'0.4');
assert.equal(V.parse('https://example.com/map?project=gardiner-3',options).legacyProject,true);
assert.equal(V.parse('https://example.com/map?project=gardiner-3&scope=register',options).legacyProject,false);
assert.equal(new URL(url).searchParams.has('nearby'),false);
'''
    subprocess.run(['node','-e',script,str(ROOT/'src/view_state.js'),str(ROOT.parent/'src/staticsites/assets/maps/map_url.js')],check=True)
