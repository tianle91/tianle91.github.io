"""Smoke test the offline builders end-to-end in isolation (no r5py/Java/GTFS).

Rebuilds a minimal copy of the project layout (src/ + data/ + output/) in a temp
dir and runs the builders there, so it neither needs the routing stack nor
clobbers committed outputs. Without data/reachability.json, build_isochrones.py
falls back to the curated transit model.
"""
import json
import pathlib
import shutil
import subprocess
import sys

import pytest
from shapely.geometry import shape

ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture
def built(tmp_path):
    """Run both builders in a temp project tree; return its output/ directory."""
    for sub in ("src", "data", "output"):
        (tmp_path / sub).mkdir()
    shutil.copytree(ROOT / "src", tmp_path / "src", dirs_exist_ok=True)
    shutil.copy(ROOT / "data" / "transit_model.json", tmp_path / "data" / "transit_model.json")
    for script in ("build_isochrones.py", "build_map.py"):
        subprocess.run([sys.executable, f"src/{script}"], cwd=tmp_path, check=True)
    return tmp_path / "output"


def test_isochrones_geojson_is_valid(built):
    geo = json.loads((built / "isochrones.geojson").read_text())
    assert geo["type"] == "FeatureCollection"
    assert geo["features"], "no band polygons produced"
    minutes = {f["properties"]["minutes"] for f in geo["features"]}
    assert minutes == {15, 30, 45, 60, 75, 90, 120}
    for f in geo["features"]:
        assert f["geometry"]["type"] == "MultiPolygon"
        assert f["geometry"]["coordinates"], "band has no polygons"


def test_bands_are_nested(built):
    """A longer time budget must cover at least as much ground as a shorter one."""
    geo = json.loads((built / "isochrones.geojson").read_text())
    areas = {}
    for f in geo["features"]:
        rings = [ring for poly in f["geometry"]["coordinates"] for ring in poly]
        # Shoelace over exterior rings is a fine proxy at this scale.
        areas[f["properties"]["minutes"]] = sum(
            abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(r, r[1:]))) / 2 for r in rings
        )
    ordered = [areas[m] for m in sorted(areas)]
    assert ordered == sorted(ordered), f"bands not nested by area: {areas}"
    geometries = [shape(feature['geometry']) for feature in
                  sorted(geo['features'], key=lambda feature: feature['properties']['minutes'])]
    for smaller, larger in zip(geometries, geometries[1:]):
        assert smaller.difference(larger).area < 1e-12


def test_committed_grid_reproduces_routed_contours_without_large_cache(tmp_path):
    shutil.copytree(ROOT / 'src', tmp_path / 'src')
    (tmp_path / 'data').mkdir()
    shutil.copy(ROOT / 'data/transit_model.json', tmp_path / 'data/transit_model.json')
    grid = {'grid_spacing_m': 500, 'arrival': '2026-11-18T09:00:00', 'percentile': 1,
            'points': [[43.6453, -79.3806, 0], [43.65, -79.38, 20]]}
    (tmp_path / 'data/routing_grid.json').write_text(json.dumps(grid))
    command = [sys.executable, 'src/build_isochrones.py']
    subprocess.run(command, cwd=tmp_path, check=True)
    output = tmp_path / 'output/isochrones.geojson'
    first = output.read_bytes()
    geo = json.loads(first)
    assert geo['properties']['source'] == 'r5py travel-time grid'
    assert geo['properties']['grid_spacing_m'] == 500
    assert {f['properties']['minutes'] for f in geo['features']} == {15, 30, 45, 60, 75, 90, 120}
    subprocess.run(command, cwd=tmp_path, check=True)
    assert output.read_bytes() == first
    # Fresh routing output takes precedence over the committed contour snapshot.
    grid['grid_spacing_m'] = 1000
    (tmp_path / 'data/reachability.json').write_text(json.dumps(grid))
    subprocess.run(command, cwd=tmp_path, check=True)
    assert json.loads(output.read_text())['properties']['grid_spacing_m'] == 1000


def test_map_html_rendered(built):
    html = (built / "union-station-transit-isochrone.html").read_text()
    assert html.startswith("<!DOCTYPE html")
    assert "__PAYLOAD__" not in html          # payload was substituted
    assert "Morning commute to Union Station" in html
    assert "service_assumption" in html       # data wired through


def test_routed_station_snapshot_survives_without_large_grid(tmp_path):
    for sub in ('src','data','output'):
        (tmp_path/sub).mkdir()
    shutil.copytree(ROOT/'src',tmp_path/'src',dirs_exist_ok=True)
    for name in ('transit_model.json','station_itineraries.json','transit_lines.geojson'):
        shutil.copy(ROOT/'data'/name,tmp_path/'data'/name)
    (tmp_path/'output/isochrones.geojson').write_text(json.dumps({
        'type':'FeatureCollection','properties':{'source':'r5py travel-time grid'},'features':[]}))
    subprocess.run([sys.executable,'src/build_map.py'],cwd=tmp_path,check=True)
    html=(tmp_path/'output/union-station-transit-isochrone.html').read_text()
    payload=json.JSONDecoder().raw_decode(html.split('const DATA = ',1)[1])[0]
    cached=json.loads((ROOT/'data/station_itineraries.json').read_text())
    assert payload['stations'] == cached['stations']
    assert payload['lines'] == json.loads((ROOT/'data/transit_lines.geojson').read_text())
    assert payload['generated_at'] == cached['generated_at']
    model = json.loads((ROOT/'data/transit_model.json').read_text())
    locations = {(station['name'], station['mode']): station for station in cached['stations']}
    for original, displayed in zip(model['nodes'], payload['nodes'], strict=True):
        station = locations.get((original['name'], original['mode']), original)
        assert displayed == {**original, 'lat': station['lat'], 'lon': station['lon']}
    unionville = next(node for node in payload['nodes'] if node['name'] == 'Unionville GO')
    assert (unionville['lat'], unionville['lon']) == (43.85169, -79.31433)
    # A deliberate curated rebuild must not inherit routed station trip claims.
    subprocess.run([sys.executable,'src/build_isochrones.py'],cwd=tmp_path,check=True)
    subprocess.run([sys.executable,'src/build_map.py'],cwd=tmp_path,check=True)
    html=(tmp_path/'output/union-station-transit-isochrone.html').read_text()
    payload=json.JSONDecoder().raw_decode(html.split('const DATA = ',1)[1])[0]
    assert payload['stations'] == []
    assert payload['nodes'] == model['nodes']
