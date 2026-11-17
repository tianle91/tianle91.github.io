"""Offline GTFS shape extraction and deterministic snapshot publication."""
import csv
import io
import zipfile

import pytest
from shapely.geometry import Point, shape

from transit_lines import build_lines, save_lines


def feed(path, agency="GO Transit", route_type="2", missing_shape=False):
    tables = {
        "agency.txt": [["agency_id", "agency_name"], ["a", agency]],
        "routes.txt": [
            ["route_id", "agency_id", "route_type", "route_short_name", "route_long_name", "route_color"],
            ["rail", "a", route_type, "R", "Rail route", "123ABC"],
            ["unused", "a", route_type, "U", "Route without trips", "123ABC"],
            ["bus", "a", "3", "B", "Bus route", "FF0000"],
        ],
        "trips.txt": [
            ["route_id", "shape_id"], ["rail", "main"], ["rail", "reverse"],
            ["rail", "branch"], ["rail", ""], ["bus", "bus"],
        ],
        "shapes.txt": [
            ["shape_id", "shape_pt_sequence", "shape_pt_lat", "shape_pt_lon"],
            ["main", 2, 43.8, -79.2], ["main", 0, 43.8, -79.4], ["main", 1, 43.8, -79.3],
            ["reverse", 0, 43.8, -79.2], ["reverse", 1, 43.8, -79.4],
            ["branch", 0, 43.8, -79.3], ["branch", 1, 43.9, -79.3],
            ["bus", 0, "nan", -79.3],
        ],
    }
    if missing_shape:
        tables["shapes.txt"] = tables["shapes.txt"][:1]
    with zipfile.ZipFile(path, "w") as archive:
        for name, rows in tables.items():
            output = io.StringIO()
            csv.writer(output).writerows(rows)
            archive.writestr(name, output.getvalue())


def test_go_rail_and_ttc_subway_streetcar_with_all_branches(tmp_path):
    go, ttc, streetcar, up = [tmp_path / name for name in ("go.zip", "ttc.zip", "streetcar.zip", "up.zip")]
    feed(go)
    feed(ttc, agency="TTC", route_type="1")
    feed(streetcar, agency="TTC", route_type="0")
    feed(up, agency="UP Express")
    result = build_lines([go, ttc, streetcar, up])
    assert result == build_lines([up, streetcar, ttc, go])
    assert [f["properties"]["mode"] for f in result["features"]] == ["go", "streetcar", "subway"]
    for feature in result["features"]:
        assert feature["properties"]["color"] == "#123abc"
        assert feature["geometry"]["type"] == "MultiLineString"
        geometry = shape(feature["geometry"])
        for point in [(-79.4, 43.8), (-79.2, 43.8), (-79.3, 43.9)]:
            assert geometry.distance(Point(point)) < 1e-10
        assert geometry.length == pytest.approx(0.3)


def test_repeated_snapshot_preserves_bytes_date_and_mtime(tmp_path):
    source = tmp_path / "go.zip"
    destination = tmp_path / "lines.geojson"
    feed(source)
    payload = build_lines([source])
    save_lines(payload, destination)
    before = destination.read_bytes(), destination.stat().st_mtime_ns
    save_lines(build_lines([source]), destination)
    assert (destination.read_bytes(), destination.stat().st_mtime_ns) == before
    assert "generated_at" not in payload


def test_missing_selected_geometry_does_not_replace_snapshot(tmp_path):
    source = tmp_path / "go.zip"
    destination = tmp_path / "lines.geojson"
    feed(source)
    save_lines(build_lines([source]), destination)
    before = destination.read_bytes()
    feed(source, missing_shape=True)
    with pytest.raises(ValueError, match="missing or degenerate shape"):
        save_lines(build_lines([source]), destination)
    assert destination.read_bytes() == before
