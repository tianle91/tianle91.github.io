"""Project snapshot configuration; capture is a build-time shared component."""
from pathlib import Path
from staticsites.snapshots import Snapshotter

ROOT = Path(__file__).resolve().parent.parent


class MortgageSnapshotter(Snapshotter):
    def generate(self, browser, url, destination=None):
        # Capture every panel at both sizes; publish only after every capture succeeds.
        captures = {}
        for name, size in self.VIEWS.items():
            captures[name] = self.capture(browser, url, name, size)
            captures['power-sale-' + name] = self.capture(browser, url + '#power-sale-title', name, size)
            captures['transfers-' + name] = self.capture(browser, url + '#transfers-title', name, size)
            captures['benchmark-' + name] = self.capture(browser, url + '#benchmark-title', name, size)
            captures['borrowing-cost-' + name] = self.capture(browser, url + '#cost-title', name, size)
        self.publish(captures, self.SNAPSHOTS if destination is None else destination)


SNAPSHOT = MortgageSnapshotter(ROOT, kind='chart', expected_plots=1)
SNAPSHOT.READY = f"""() => ({SNAPSHOT.READY})() &&
  document.querySelectorAll('#power-sale-chart .count-bar').length ===
    DATA.groups.find(group => group.id === 'power_sale_homes').series[0].points.length &&
  document.querySelectorAll('#power-sale-values tr').length ===
    document.querySelectorAll('#power-sale-chart .count-bar').length &&
  document.getElementById('power-sale-value').textContent.trim() &&
  document.querySelectorAll('#transfers-chart .count-bar').length === 11 &&
  document.getElementById('transfers-value').textContent === '2,979 transfers' &&
  document.querySelectorAll('.benchmark-line').length === 4 &&
  document.getElementById('cost-payment').textContent.includes('/month') &&
  [...document.querySelectorAll('.benchmark-line')].every(path =>
    path.getAttribute('d') && !/NaN|Infinity/.test(path.getAttribute('d')) && path.getTotalLength() > 0) &&
  [...document.querySelectorAll('#benchmark-chart svg, #cost-chart svg')].every(svg => {{
    const labels = [...svg.querySelectorAll('.benchmark-tick')].map(label => label.getBoundingClientRect());
    return labels.every((box, i) => i === 0 || box.left >= labels[i-1].right + 2);
  }}) &&
  [...document.querySelectorAll('#power-sale-chart svg, #transfers-chart svg')].every(svg => {{
    const labels = [...svg.querySelectorAll('.count-tick')].map(label => label.getBoundingClientRect());
    return labels.every((box, i) => i === 0 || box.left >= labels[i-1].right + 2);
  }}) &&
  [...document.querySelectorAll('.count-bar')].every(bar =>
    Number(bar.getAttribute('height')) >= 0 && Number(bar.getAttribute('width')) > 0)
"""

if __name__ == '__main__':
    SNAPSHOT.main()
