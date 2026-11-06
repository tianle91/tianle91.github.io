"""Homepage integration with StaticSites tracked in the parent Git repository."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import sync_staticsites as sync


class ManifestTests(unittest.TestCase):
    def test_directory_groups_known_projects_and_preserves_unknown_ones(self):
        sites = [{"title": title, "description": "A project", "output": f"{slug}/output/{slug}.html"}
                 for title, slug in [("Yields", "us-canada-yield-curves"),
                                     ("Crime", "toronto-crime-map"), ("New", "new-project")]]
        block = sync.render(sites)
        for title in ["Maps", "Economics & Finance", "Other projects"]:
            self.assertIn(f"## {title}", block)
        for site in sites:
            self.assertEqual(block.count(f"](/StaticSites/{site['output']})"), 1)
        document = f"Intro\n{sync.STARTMARK}\nOld content\n{sync.ENDMARK}\nFooter"
        self.assertEqual(sync.splice(document, block),
                         f"Intro\n{sync.STARTMARK}\n{block}\n{sync.ENDMARK}\nFooter")

    def test_nested_tracked_outputs_match_manifest_and_report_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sites_root = root / "StaticSites"
            output = sites_root / "example/output/example.html"
            output.parent.mkdir(parents=True)
            output.write_text("<html></html>")
            sites = [{"title": "Example", "description": "A plot",
                      "output": "example/output/example.html"}]
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            with patch.object(sync, "STATIC_SITES", sites_root):
                self.assertEqual(sync.verify(sites), [])
                output.unlink()
                self.assertIn("file is missing", sync.verify(sites)[0])
                output.touch()
                self.assertIn("is not in sites.json", sync.verify([])[0])
            block = sync.render(sites)
            self.assertIn("(/StaticSites/example/output/example.html)", block)
            self.assertIn("tianle91.github.io/tree/master/StaticSites", block)


if __name__ == "__main__":
    unittest.main()
