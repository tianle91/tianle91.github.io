/* Separate count scale and published window; never rebase or forecast listings. */
(() => {
  const group = DATA.groups.find(group => group.id === 'power_sale');
  const points = group.series[0].points;
  const panel = $('power-sale-chart');
  const dateLabel = period => new Date(period + '-01T00:00:00Z').toLocaleDateString('en-CA',
    {month:'short', year:'numeric', timeZone:'UTC'});
  const total = start => points.slice(start, start + 12).reduce((sum, point) => sum + point.value, 0);
  const previous = total(0), latest = total(12);
  $('power-sale-summary').textContent = `${latest} new listings in Oct 2025–Sep 2026 · ` +
    `${((latest / previous - 1) * 100).toFixed(1)}% more than ${previous} the year before`;
  let inspected = points.length - 1;

  for (const point of points) {
    const row = document.createElement('tr');
    const heading = text('th', dateLabel(point.period));
    heading.scope = 'row';
    row.append(heading, text('td', String(point.value)));
    $('power-sale-values').append(row);
  }

  function inspect(index) {
    inspected = Math.max(0, Math.min(points.length - 1, index));
    panel.querySelectorAll('.power-sale-bar').forEach((bar, i) => {
      bar.classList.toggle('is-inspected', i === inspected);
    });
    const point = points[inspected];
    $('power-sale-period').textContent = dateLabel(point.period);
    $('power-sale-value').textContent = `${point.value} new listings`;
  }

  function render() {
    const width = panel.clientWidth;
    const height = width < 480 ? 260 : 300;
    const left = 36, right = 14, top = 30, bottom = height - 42;
    const step = (width - left - right) / points.length;
    const high = Math.ceil(Math.max(...points.map(point => point.value)) / 20) * 20;
    const yAt = value => bottom - value / high * (bottom - top);
    const svg = svgNode('svg', {viewBox:`0 0 ${width} ${height}`, role:'img', tabindex:'0',
      'aria-label':'GTA new power-of-sale listings, October 2024 to September 2026. Use Left and Right to inspect months; Home and End jump to the first and last month.',
      'aria-describedby':'power-sale-readout'});
    panel.replaceChildren(svg);
    svg.append(svgNode('text', {x:left, y:15, class:'axis-title'}, 'New listings / month'));
    for (let value = 0; value <= high; value += 20) {
      const y = yAt(value);
      svg.append(svgNode('line', {x1:left, x2:width-right, y1:y, y2:y, class:'gridline'}));
      svg.append(svgNode('text', {x:left-7, y:y+4, 'text-anchor':'end', class:'axis'}, value));
    }
    points.forEach((point, i) => {
      const x = left + i * step;
      const rect = svgNode('rect', {x:x+step*.15, y:yAt(point.value), width:step*.7,
        height:bottom-yAt(point.value), rx:2,
        class:'power-sale-bar ' + (i < 12 ? 'previous-year' : 'latest-year'),
        'data-period':point.period, 'data-value':point.value});
      rect.append(svgNode('title', {}, `${dateLabel(point.period)}: ${point.value} new listings`));
      svg.append(rect);
      if (i === 0 || i === 23 || i % (width < 480 ? 6 : 3) === 0) {
        const edge = i === 0 ? 'start' : i === 23 ? 'end' : 'middle';
        const label = dateLabel(point.period).replace('20', '’');
        svg.append(svgNode('text', {x:i === 23 ? width-right : x+step/2,
          y:height-18, 'text-anchor':edge, class:'axis'}, label));
      }
    });
    const overlay = svgNode('rect', {x:left, y:top, width:width-left-right,
      height:bottom-top, fill:'transparent'});
    svg.append(overlay);
    const pointer = event => {
      const bounds = svg.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width * width;
      inspect(Math.floor((x - left) / step));
    };
    overlay.addEventListener('pointermove', event => {
      if (event.pointerType !== 'touch') pointer(event);
    });
    overlay.addEventListener('pointerdown', pointer);
    svg.addEventListener('keydown', event => {
      if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
      event.preventDefault();
      inspect(event.key === 'Home' ? 0 : event.key === 'End' ? points.length-1 :
        inspected + (event.key === 'ArrowLeft' ? -1 : 1));
    });
    inspect(inspected);
  }
  let timer;
  window.addEventListener('resize', () => {clearTimeout(timer); timer = setTimeout(render, 100);});
  render();
})();
