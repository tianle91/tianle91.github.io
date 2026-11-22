"""Project snapshot configuration; capture is a build-time shared component."""
from pathlib import Path
from staticsites.snapshots import Snapshotter

ROOT = Path(__file__).resolve().parent.parent


class MortgageSnapshotter(Snapshotter):
    def generate(self, browser, url, destination=None):
        # Capture both panels at both sizes; publish only after all four succeed.
        captures = {}
        for name, size in self.VIEWS.items():
            captures[name] = self.capture(browser, url, name, size)
            captures['power-sale-' + name] = self.capture(browser, url + '#power-sale-title', name, size)
        self.publish(captures, self.SNAPSHOTS if destination is None else destination)


SNAPSHOT = MortgageSnapshotter(ROOT, kind='chart', expected_plots=1)
SNAPSHOT.READY = f"""() => ({SNAPSHOT.READY})() &&
  document.querySelectorAll('#power-sale-chart .power-sale-bar').length === 24 &&
  document.querySelectorAll('#power-sale-values tr').length === 24 &&
  document.getElementById('power-sale-value').textContent === '87 new listings' &&
  [...document.querySelectorAll('#power-sale-chart .power-sale-bar')].every(bar =>
    Number(bar.getAttribute('height')) > 0 && Number(bar.getAttribute('width')) > 0)
"""

if __name__ == '__main__':
    SNAPSHOT.main()
