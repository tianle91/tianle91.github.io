/* Aligned original-unit plots plus a separately labelled payment-equivalent price. */
(() => {
  const reference = $('reference-rate');
  let rows, index, plots = [];
  const money = value => '$' + Math.round(value).toLocaleString('en-CA');
  const month = period => new Date(period+'-01T00:00:00Z').toLocaleDateString('en-CA',
    {month:'short',year:'numeric',timeZone:'UTC'});
  function inspect(next) {
    index = Math.max(0, Math.min(rows.length-1,next));
    const row = rows[index];
    for (const plot of plots) {
      plot.cursor.setAttribute('x1',plot.xAt(index));
      plot.cursor.setAttribute('x2',plot.xAt(index));
    }
    $('benchmark-period').textContent = month(row.period);
    $('benchmark-price').textContent = money(row.price);
    $('benchmark-rate').textContent = row.rate.toFixed(2)+'%';
    $('cost-period').textContent = month(row.period);
    $('cost-actual').textContent = money(row.price);
    $('cost-equivalent').textContent = money(row.equivalent);
    $('cost-payment').textContent = money(row.payment)+'/month';
    $('cost-reference-label').textContent = `Same-payment price at ${Number(reference.value).toFixed(1)}%`;
    $('cost-explanation').textContent = `The ${money(row.price)} benchmark at ${row.rate.toFixed(2)}% costs about ${money(row.payment)}/month in principal and interest. `+
      `At ${Number(reference.value).toFixed(1)}%, a ${money(row.equivalent)} home would have the same payment, with the same 20% down and 25-year amortization.`;
  }
  function draw(id, panels) {
    const container = $(id);
    const width = container.clientWidth;
    const left = width < 480 ? 53 : 72, right = 18, top = 28;
    const panelHeight = panels.length === 2 ? (width < 480 ? 160 : 170) : (width < 480 ? 230 : 270);
    const gap = 38, bottom = 42;
    const height = top + panels.length*panelHeight + (panels.length-1)*gap + bottom;
    const xAt = i => left + i/(rows.length-1)*(width-left-right);
    const svg = svgNode('svg',{viewBox:`0 0 ${width} ${height}`,role:'img',tabindex:'0',
      'aria-label':(panels.length===2 ? 'Greater Toronto benchmark price and Canadian mortgage rate, in aligned panels with separate units.' :
        `Greater Toronto benchmark and same-payment price at ${reference.value} percent.`)+
        ' Use left and right arrows to inspect months. Home and End jump to the edges.'});
    container.replaceChildren(svg);
    panels.forEach((panel,panelIndex)=>{
      const panelTop = top+panelIndex*(panelHeight+gap);
      const maximum = Math.max(...rows.flatMap(row=>panel.lines.map(line=>row[line.key])));
      const step = panel.rate ? Math.max(1,Math.ceil(maximum/4)) : Math.max(100000,Math.ceil(maximum/400000)*100000);
      const high = Math.ceil(maximum/step)*step;
      const yAt = value => panelTop+panelHeight-value/high*panelHeight;
      svg.append(svgNode('text',{x:left,y:panelTop-10,class:'axis-title'},width < 480 ? panel.shortTitle : panel.title));
      for (let value=0;value<=high;value+=step) {
        const y = yAt(value);
        svg.append(svgNode('line',{x1:left,x2:width-right,y1:y,y2:y,class:'gridline'}));
        svg.append(svgNode('text',{x:left-8,y:y+4,'text-anchor':'end',class:'axis'},
          panel.rate ? value+'%' : '$'+(value/1000000).toFixed(1)+'m'));
      }
      for (const line of panel.lines) {
        const path = rows.map((row,i)=>(i?'L':'M')+xAt(i).toFixed(2)+','+yAt(row[line.key]).toFixed(2)).join(' ');
        svg.append(svgNode('path',{d:path,stroke:line.color,class:'series-line benchmark-line',
          'data-series':line.key,...(line.dashed?{'stroke-dasharray':'6 4'}:{})}));
      }
    });
    let previousRight = -Infinity;
    const spacing = width < 480 ? 36 : 24;
    rows.forEach((row,i)=>{
      const last = i===rows.length-1;
      if (i !== 0 && !last && i%spacing!==0) return;
      const x = xAt(i), label = row.period.slice(0,4);
      const start = i===0 ? x : last ? x-28 : x-14;
      if (!last && i!==0 && (start<previousRight+8 || start+36>width-right-28)) return;
      svg.append(svgNode('text',{x,y:height-18,'text-anchor':i===0?'start':last?'end':'middle',class:'axis benchmark-tick'},label));
      previousRight=start+28;
    });
    const cursor=svgNode('line',{x1:0,x2:0,y1:top,y2:height-bottom,stroke:'var(--ink)',
      'stroke-dasharray':'2 4',class:'benchmark-guide'});
    svg.append(cursor);
    const overlay=svgNode('rect',{x:left,y:top,width:width-left-right,height:height-top-bottom,fill:'transparent'});
    svg.append(overlay);
    const pointer=event=>{
      const bounds=svg.getBoundingClientRect();
      const x=(event.clientX-bounds.left)/bounds.width*width;
      inspect(Math.round((x-left)/(width-left-right)*(rows.length-1)));
    };
    overlay.addEventListener('pointermove',event=>{if(event.pointerType!=='touch')pointer(event);});
    overlay.addEventListener('pointerdown',pointer);
    svg.addEventListener('keydown',event=>{
      if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      event.preventDefault();
      inspect(event.key==='Home'?0:event.key==='End'?rows.length-1:index+(event.key==='ArrowLeft'?-1:1));
    });
    plots.push({cursor,xAt});
  }
  function render() {
    rows=MortgageCosts.observations(DATA,Number(reference.value));
    plots=[];
    const dates=`${month(rows[0].period)}–${month(rows.at(-1).period)} · Shared monthly observations only`;
    $('benchmark-window').textContent=dates;
    $('cost-window').textContent=dates;
    draw('benchmark-chart',[
      {title:'Composite benchmark · CAD',shortTitle:'Benchmark · CAD',lines:[{key:'price',color:'var(--price)'}]},
      {title:'Uninsured fixed mortgage rate · 5+ years',shortTitle:'Mortgage rate · %',rate:true,lines:[{key:'rate',color:'var(--bank)'}]},
    ]);
    draw('cost-chart',[{title:'Nominal price and same-payment equivalent · CAD',shortTitle:'Price · CAD',lines:[
      {key:'price',color:'var(--price)'},{key:'equivalent',color:'var(--adjusted)',dashed:true},
    ]}]);
    inspect(index ?? rows.length-1);
  }
  reference.addEventListener('change',render);
  let timer;
  window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(render,100);});
  render();
})();
