/* Keep publisher definitions, time windows and count scales separate. */
(() => {
  const groups = Object.fromEntries(DATA.groups.map(group => [group.id, group]));
  const dateLabel = period => period.length === 4 ? period :
    new Date(period + '-01T00:00:00Z').toLocaleDateString('en-CA',
      {month:'short', year:'numeric', timeZone:'UTC'});
  const number = value => value.toLocaleString('en-CA');
  const change = (value, base) => base > 0 ?
    `${value >= base ? '+' : ''}${((value / base - 1) * 100).toFixed(1)}%` : 'no percentage comparison';
  const sourceChoice = $('power-sale-source');
  const inspected = {};

  function draw(group, prefix) {
    const points = group.series[0].points;
    const panel = $(prefix + '-chart');
    const unit = group.unit === 'homes' ? 'new homes' : group.unit === 'transfers' ? 'transfers' : 'new listings';
    const annual = group.frequency === 'Annual';
    const valery = group.id === 'power_sale';
    const complete = points.filter(point => !point.partial);
    const latest = complete.at(-1);
    const prior = complete.at(-2);
    const latestYear = points.at(-1).period.slice(0,4);
    const isLatest = (point, i) => valery ? i >= 12 : point.period.startsWith(latestYear);
    const priorYear = complete.find(point => point.period === `${Number(latest.period.slice(0,4))-1}${latest.period.slice(4)}`);
    let summary;
    if (valery) {
      const total = start => points.slice(start,start+12).reduce((sum, point) => sum + point.value, 0);
      summary = `${total(12)} new listings in Oct 2025–Sep 2026 · ${change(total(12),total(0))} versus the year before`;
    } else if (annual) {
      summary = `${latest.period}: ${number(latest.value)} transfers · ${change(latest.value,prior.value)} versus ${prior.period}`;
    } else {
      summary = `${dateLabel(latest.period)}: ${latest.value} new homes` +
        (priorYear ? ` · ${change(latest.value,priorYear.value)} versus ${dateLabel(priorYear.period)}` : ' · latest complete month');
    }
    $(prefix + '-summary').textContent = summary;
    $(prefix + '-description').textContent = `${annual ? 'Registered transfers by year' : valery ? 'New listing events by month' : 'Newly listed homes by month'} · ` +
      `${dateLabel(points[0].period)}–${dateLabel(points.at(-1).period)}${points.at(-1).partial ? ' (last month to date)' : ''}`;
    $(prefix + '-note').textContent = group.note;
    const source = text('a', group.source);
    source.href = group.source_url;
    source.target = '_blank';
    source.rel = 'noopener';
    $(prefix + '-source-note').replaceChildren('Source: ', source,
      group.data_as_of ? ` · Data as of ${group.data_as_of}.` : group.published_at ? ` · Published ${group.published_at}.` : '');
    const legend = $(prefix + '-legend');
    legend.replaceChildren();
    for (const [label, className] of [
      [valery ? 'Oct 2025–Sep 2026' : latestYear, 'latest-key'],
      [valery ? 'The 12 months before' : annual ? `${points[0].period}–${prior.period}` : points[0].period.slice(0,4), 'previous-key'],
      ...(points.at(-1).partial ? [['Month to date', 'partial-key']] : []),
    ]) {
      const key = text('span', '', className);
      key.append(document.createElement('i'), label);
      legend.append(key);
    }
    $(prefix + '-values').replaceChildren();
    for (const point of points) {
      const row = document.createElement('tr');
      const heading = text('th', dateLabel(point.period) + (point.partial ? ' (to date)' : ''));
      heading.scope = 'row';
      row.append(heading, text('td', number(point.value)));
      $(prefix + '-values').append(row);
    }
    function inspect(index) {
      inspected[group.id] = Math.max(0, Math.min(points.length - 1, index));
      panel.querySelectorAll('.count-bar').forEach((bar, i) => {
        bar.classList.toggle('is-inspected', i === inspected[group.id]);
      });
      const point = points[inspected[group.id]];
      $(prefix + '-period').textContent = dateLabel(point.period) + (point.partial ? ' (to date)' : '');
      $(prefix + '-value').textContent = `${number(point.value)} ${unit}`;
    }
    const width = panel.clientWidth;
    const height = width < 480 ? 260 : 300;
    const left = annual ? 46 : 36, right = 14, top = 30, bottom = height - 42;
    const step = (width - left - right) / points.length;
    const max = Math.max(...points.map(point => point.value));
    const interval = annual ? 1000 : 20;
    const high = Math.max(interval, Math.ceil(max / interval) * interval);
    const yAt = value => bottom - value / high * (bottom - top);
    const svg = svgNode('svg', {viewBox:`0 0 ${width} ${height}`, role:'img', tabindex:'0',
      'aria-label':`${group.title}, ${dateLabel(points[0].period)} to ${dateLabel(points.at(-1).period)}. Use Left and Right to inspect; Home and End jump to the first and last period.`,
      'aria-describedby':prefix + '-readout'});
    panel.replaceChildren(svg);
    const defs = svgNode('defs');
    const pattern = svgNode('pattern', {id:prefix+'-partial', width:6, height:6, patternUnits:'userSpaceOnUse', patternTransform:'rotate(45)'});
    pattern.append(svgNode('rect', {width:6, height:6, fill:'var(--latest)', opacity:.2}),
      svgNode('line', {x1:0,x2:0,y1:0,y2:6,stroke:'var(--latest)','stroke-width':3}));
    defs.append(pattern);
    svg.append(defs, svgNode('text', {x:left, y:15, class:'axis-title'},
      annual ? 'Registered transfers / year' : valery ? 'New listings / month' : 'New homes / month'));
    for (let value = 0; value <= high; value += interval) {
      const y = yAt(value);
      svg.append(svgNode('line', {x1:left, x2:width-right, y1:y, y2:y, class:'gridline'}));
      svg.append(svgNode('text', {x:left-7, y:y+4, 'text-anchor':'end', class:'axis'}, number(value)));
    }
    let lastTickRight = -Infinity;
    points.forEach((point, i) => {
      const x = left + i * step;
      const rect = svgNode('rect', {x:x+step*.15, y:yAt(point.value), width:step*.7,
        height:bottom-yAt(point.value), rx:2,
        class:'count-bar ' + (prefix === 'power-sale' ? 'power-sale-bar ' : '') +
          (isLatest(point, i) ? 'latest-year' : 'previous-year'),
        'data-period':point.period, 'data-value':point.value, 'data-partial':Boolean(point.partial)});
      if (point.partial) rect.style.fill = `url(#${prefix}-partial)`;
      rect.append(svgNode('title', {}, `${dateLabel(point.period)}${point.partial ? ' (to date)' : ''}: ${number(point.value)} ${unit}`));
      svg.append(rect);
      const spacing = annual ? (width < 480 ? 2 : 1) : (width < 480 ? 6 : 3);
      const last = i === points.length-1;
      const edge = i === 0 ? 'start' : last ? 'end' : 'middle';
      const labelX = i === 0 ? left : last ? width-right : x+step/2;
      const labelWidth = annual ? 28 : 44;
      const labelStart = labelX - (edge === 'end' ? labelWidth : edge === 'middle' ? labelWidth/2 : 0);
      const fits = labelStart >= lastTickRight+8 && labelStart+labelWidth+8 <= width-right-labelWidth;
      if (i === 0 || last || (i % spacing === 0 && fits)) {
        const label = annual ? point.period : dateLabel(point.period).replace('20', '’');
        svg.append(svgNode('text', {x:labelX,
          y:height-18, 'text-anchor':edge, class:'axis count-tick'}, label));
        lastTickRight = labelStart+labelWidth;
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
        inspected[group.id] + (event.key === 'ArrowLeft' ? -1 : 1));
    });
    inspect(inspected[group.id] ?? points.length-1);
  }
  function render() {
    draw(groups[sourceChoice.value], 'power-sale');
    draw(groups.power_sale_transfers, 'transfers');
  }
  sourceChoice.addEventListener('change', render);
  let timer;
  window.addEventListener('resize', () => {clearTimeout(timer); timer = setTimeout(render, 100);});
  render();
})();
