"""Offline shared URL primitive and packaged-asset regressions."""
from pathlib import Path
import shutil
import subprocess
import pytest
from staticsites.assets import ASSETS, source_text

def test_map_url_primitives():
    if not shutil.which('node'):pytest.skip('Node unavailable')
    script=r'''
const assert=require('node:assert/strict'),U=require(process.argv[1]);
const ids=['Auto Theft','Assault'];
const p=new URLSearchParams('lat=43.65&lng=-79.38&z=15&layers=Auto%20Theft&status=Open');
assert.deepEqual(U.view(p),{lat:43.65,lng:-79.38,z:15});assert.deepEqual(U.layers(p,ids),['Auto Theft']);
assert.equal(U.choice(p,'status',['Open','Closed'],'Closed'),'Open');
assert.equal(U.choice(p,'unknown',['A'],'A'),'A');
for(const text of ['lat=NaN&lng=0&z=1','lat=0&lng=181&z=1','lat=0&lng=0&z=20','lat=&lng=0&z=1'])assert.equal(U.view(new URLSearchParams(text)),null);
assert.deepEqual(U.layers(new URLSearchParams('layers='),ids),[]);
assert.deepEqual(U.layers(new URLSearchParams('layers=not-real'),ids),ids);
assert.deepEqual(U.layers(new URLSearchParams('layers=Assault,Assault,not-real'),ids),['Assault']);
const out=new URLSearchParams('utm_source=example');U.writeView(out,{lat:43.65000012,lng:-79.38,z:15});U.writeLayers(out,[],ids);
assert.equal(out.get('layers'),'');assert.equal(out.get('lat'),'43.65');assert.equal(out.get('utm_source'),'example');
U.writeLayers(out,ids,ids);assert.equal(out.has('layers'),false);
'''
    subprocess.run(['node','-e',script,str(ASSETS/'maps/map_url.js')],check=True)

def test_explorer_includes_shared_url_primitives(tmp_path):
    text=source_text(tmp_path,'explorer.js')
    assert text.index('const MapURL')<text.index('const Explorer')
    assert 'function share(map' in text
