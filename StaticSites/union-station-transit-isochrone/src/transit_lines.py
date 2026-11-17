"""Extract GO rail and TTC subway/streetcar shapes from local GTFS feeds."""
import csv
import datetime
import io
import json
import math
import re
import zipfile
from collections import defaultdict

from shapely.geometry import LineString, mapping
from shapely.ops import linemerge, unary_union

from staticsites.pipeline import write_if_changed

TTC_MODES = {"0": "streetcar", "1": "subway"}
MODE_COLORS = {"go": "1b7a3d", "subway": "1f78b4", "streetcar": "e31a1c"}


def feed_lines(path):
    with zipfile.ZipFile(path) as archive:
        def rows(name):
            with archive.open(name) as stream:
                yield from csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig"))

        agencies = {row.get("agency_id", ""): row["agency_name"].strip()
                    for row in rows("agency.txt")}
        routes = {}
        for route in rows("routes.txt"):
            agency = agencies.get(route.get("agency_id", ""))
            if agency is None and len(agencies) == 1:
                agency = next(iter(agencies.values()))
            if agency == "GO Transit" and route["route_type"] == "2":
                mode = "go"
            elif agency in ("TTC", "Toronto Transit Commission") and route["route_type"] in TTC_MODES:
                mode = TTC_MODES[route["route_type"]]
            else:
                continue
            color = route.get("route_color", "")
            if not re.fullmatch(r"[0-9a-fA-F]{6}", color):
                color = MODE_COLORS[mode]
            short_name = route.get("route_short_name", "") or route["route_id"]
            routes[route["route_id"]] = {
                "id": f"{mode}-{short_name}", "mode": mode,
                "name": route.get("route_long_name", "") or short_name,
                "short_name": short_name, "color": "#" + color.lower(),
            }
        if not routes:
            return []

        route_shapes = defaultdict(set)
        used_routes = set()
        for trip in rows("trips.txt"):
            if trip["route_id"] in routes:
                used_routes.add(trip["route_id"])
                shape_id = trip.get("shape_id")
                if shape_id:
                    route_shapes[trip["route_id"]].add(shape_id)
        wanted = set().union(*route_shapes.values())
        shapes = defaultdict(list)
        for point in rows("shapes.txt"):
            if point["shape_id"] not in wanted:
                continue
            lat, lon = float(point["shape_pt_lat"]), float(point["shape_pt_lon"])
            if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError(f"{path}: invalid shape coordinate")
            shapes[point["shape_id"]].append((int(point["shape_pt_sequence"]), (lon, lat)))

        features = []
        for route_id in sorted(used_routes):
            properties = routes[route_id]
            paths = []
            for shape_id in sorted(route_shapes[route_id]):
                points = [point for _, point in sorted(shapes[shape_id])]
                if len(set(points)) < 2:
                    raise ValueError(f"{path}: missing or degenerate shape {shape_id}")
                paths.append(LineString(points))
            if not paths:
                raise ValueError(f"{path}: route {route_id} has no shapes")
            # Merge overlapping trip variants and retain every published branch.
            geometry = unary_union(paths)
            if geometry.geom_type == "MultiLineString":
                geometry = linemerge(geometry)
            geometry = geometry.simplify(0.00003).normalize()
            if geometry.geom_type == "LineString":
                coordinates = [mapping(geometry)["coordinates"]]
            else:
                coordinates = mapping(geometry)["coordinates"]
            features.append({
                "type": "Feature", "properties": properties,
                "geometry": {"type": "MultiLineString", "coordinates": coordinates},
            })
        return features


def build_lines(feeds):
    features = [feature for path in sorted(feeds) for feature in feed_lines(path)]
    features.sort(key=lambda feature: feature["properties"]["id"])
    return {"type": "FeatureCollection", "features": features}


def save_lines(payload, destination):
    """Keep the observation date when the extracted geometry is identical."""
    payload = json.loads(json.dumps(payload))
    previous = json.loads(destination.read_text()) if destination.exists() else {}
    previous_date = previous.pop("generated_at", None)
    payload["generated_at"] = (previous_date if previous == payload and previous_date
                               else datetime.date.today().isoformat())
    write_if_changed(destination, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
