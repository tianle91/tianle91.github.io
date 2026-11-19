"""Build the standalone map from committed inputs, offline."""
import json
from pathlib import Path
from staticsites.assets import read_template, source_text, script_json
from staticsites.pipeline import write_if_changed
ROOT = Path(__file__).resolve().parent.parent

def render(data):
    page = read_template(ROOT / "src/page.html")
    for token, asset in [("__EXPLORER_CSS__", "explorer.css"), ("__EXPLORER_JS__", "explorer.js"), ("__NEARBY_JS__", "nearby.js"), ("__LOCATION_JS__", "location.js"), ("__VIEW_STATE_JS__", "view_state.js"), ("__APP_JS__", "app.js")]:
        page = page.replace(token, source_text(ROOT, asset))
    return page.replace("__PAYLOAD__", script_json(data))

def main():
    data = json.loads((ROOT / "data/projects.json").read_text())
    write_if_changed(ROOT / "output/toronto-infrastructure-map.html", render(data))

if __name__ == "__main__":
    main()
