const $ = id => document.getElementById(id), esc = Explorer.esc;
const map = L.map('map', {preferCanvas:true}).setView([43.69,-79.43],11);
const basemap=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19,opacity:0.4,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
map.createPane('major-projects').style.zIndex=450;
map.createPane('selected-project').style.zIndex=470;
map.getPane('selected-project').style.pointerEvents='none';
// Separate canvases intercept events across their entire rectangular surface,
// including blank pixels. SVG panes hit-test only their interactive paths, so
// major corridors and selection outlines cannot block register clicks below.
const majorRenderer=L.svg({pane:'major-projects'});
const selectionRenderer=L.svg({pane:'selected-project'});
const categories = [
  {id:'roads',label:'Roads & bridges',color:'#6546a4'},
  {id:'water',label:'Water & wastewater',color:'#0075aa'},
  {id:'transit',label:'TTC infrastructure',color:'#b3342b'},
  {id:'power',label:'City-owned electricity',color:'#a46400'},
  {id:'places',label:'Parks, housing & public places',color:'#08774c'}
];
const colors = Object.fromEntries(categories.map(x=>[x.id,x.color]));
const group = L.featureGroup().addTo(map);
const spotlight=L.featureGroup().addTo(map);
let visible = [], nearby = null, nearbyRadius=500, locationControl=null;
function clearHighlight() {
  spotlight.clearLayers();$('selection-key').hidden=true;
}
function highlight(f) {
  clearHighlight();if(!f.geometry)return;
  const color=f.properties.stage==='Completed'?'#58636c':colors[f.properties.category];
  for(const halo of [true,false]) {
    L.geoJSON(f,{pane:'selected-project',renderer:selectionRenderer,interactive:false,
      style:{pane:'selected-project',interactive:false,color:halo?'#fff':color,weight:halo?12:6,opacity:1,fillOpacity:halo?0:0.16},
      pointToLayer:(_,ll)=>L.circleMarker(ll,{pane:'selected-project',renderer:selectionRenderer,interactive:false,radius:halo?13:9,color:halo?'#fff':color,fillColor:color,fillOpacity:1,weight:halo?4:2})
    }).addTo(spotlight);
  }
  $('selection-name').textContent=f.properties.title;$('selection-key').hidden=false;
}
function projectStyle(f) {
  const p=f.properties, close=map.getZoom()>=14;
  return {color:p.stage==='Completed'?'#58636c':colors[p.category],
    weight:p.collection==='major'?6:close?4:2,
    opacity:p.collection==='major'?1:close?0.95:0.7,fillOpacity:0.12,
    dashArray:['Planning','Design'].includes(p.stage)?'7 6':null};
}
$('clear-selection').onclick=clearHighlight;
$('basemap').onchange=()=>basemap.setOpacity(Number($('basemap').value));
for (const owner of [...new Set(DATA.features.map(f=>f.properties.owner))].sort()) {
  const option = document.createElement('option'); option.value=owner;option.textContent=owner;$('owner').append(option);
}
function details(f) {
  const p=f.properties;
  let html=`<strong>${esc(p.title)}</strong><p>${esc(p.location)}</p><p><b>${esc(p.stage)}</b> · ${esc(p.owner)}</p><p>${esc(p.description)}</p><p><b>Schedule</b><br>${esc(p.schedule || 'Not published')}</p>`;
  if (p.collection==='major') {
    html+=`<p>Summary reviewed ${esc(p.reviewed_at)}. ${p.needs_review ? '<b>Source page changed since review. Check the official update before relying on this summary.</b>' : ''}</p>`;
    if(p.ownership_note) html+=`<p>${esc(p.ownership_note)} <a href="${esc(p.ownership_source)}" target="_blank" rel="noopener">Ownership announcement ↗</a></p>`;
  } else {
    html+=`<p>Source status: ${esc(p.source_status)}${p.contract_state ? ' · Contract: '+esc(p.contract_state):''}<br>Project ID: ${esc(p.project_number || 'Not published')}<br>Source updated: ${esc(p.source_updated || 'Not published')}</p>`;
    if(p.source_status==='Active' && p.end_year && p.end_year < Number(DATA.retrieved_at.slice(0,4))) html+='<p><b>Past scheduled end year.</b> The source still marks this record Active; current construction is unconfirmed.</p>';
    html+='<p>Year ranges and Active status do not prove work is underway today.</p>';
  }
  html+=`<p><small>${esc(p.geometry_note)}</small></p><p><a href="${esc(p.url)}" target="_blank" rel="noopener">Official project source ↗</a></p><p><a href="?project=${encodeURIComponent(p.id)}">Link to this record</a></p>`;
  return html;
}
function select(entry) {
  if(entry.layer) {Explorer.fit(map,entry.layer.getBounds(),15);highlight(entry.f);entry.layer.openPopup();}
  else Explorer.detail(entry.f.properties.title,details(entry.f));
}
function update() {
  const q=$('search').value.toLowerCase().trim(), scope=$('scope').value, stage=$('stage').value, owner=$('owner').value;
  group.clearLayers();clearHighlight();visible=[];const counts={};
  for(const f of DATA.features) {
    const p=f.properties;
    const distance = nearby ? Nearby.distance(f.geometry,nearby.lat,nearby.lng) : null;
    if(nearby && distance>nearbyRadius) continue;
    if(scope!=='all' && p.collection!==scope) continue;
    if(stage==='open' ? ['Completed','Post-construction'].includes(p.stage) : stage!=='all' && p.stage!==stage) continue;
    if(owner && p.owner!==owner) continue;
    if(q && ![p.title,p.location,p.description,p.project_number,p.owner,p.stage].join(' ').toLowerCase().includes(q)) continue;
    counts[p.category]=(counts[p.category]||0)+1;
    if(!Explorer.enabled(p.category)) continue;
    let layer=null;
    if(f.geometry) {
      const color=projectStyle(f).color, pane=p.collection==='major'?'major-projects':'overlayPane';
      layer=L.geoJSON(f,{
        pane,
        renderer:p.collection==='major'?majorRenderer:undefined,
        onEachFeature: (_,path)=>{path.options.bubblingMouseEvents=false;},
        style:()=>({...projectStyle(f),pane}),
        pointToLayer:(_,ll)=>L.circleMarker(ll,{pane,renderer:p.collection==='major'?majorRenderer:undefined,radius:p.collection==='major'?9:map.getZoom()>=14?7:4,color:'#fff',weight:2,fillColor:color,fillOpacity:1,bubblingMouseEvents:false})
      });
      layer.on('click',()=>highlight(f));
      layer.bindPopup(()=>details(f),{...Explorer.detailPopup(p.title),maxWidth:370});
      layer.bindTooltip(p.title);group.addLayer(layer);
    }
    visible.push({f,layer,distance});
  }
  if(nearby) visible.sort((a,b)=>a.distance-b.distance);
  Explorer.layerCounts(Object.fromEntries(categories.map(c=>[c.id,counts[c.id]||0])));
  Explorer.count(visible.length,'project locations',visible.filter(x=>x.layer).length,nearby?'within '+nearbyRadius.toLocaleString()+' metres':'','without geometry');
  Explorer.results(visible,e=>e.f.properties.title,e=>`${nearby?Math.round(e.distance)+' m · ':''}${e.f.properties.stage} · ${e.f.properties.location || e.f.properties.owner}`,select);
  if(!visible.length) $('result-note').textContent='No matching project records in this snapshot. Broaden the radius, clear filters or ask the City. This does not establish that no work is planned.';
}
Explorer.layers(categories,update);
map.on('zoomend',()=>{
  for(const entry of visible) if(entry.layer) entry.layer.eachLayer(path=>{
    if(path instanceof L.CircleMarker) path.setRadius(entry.f.properties.collection==='major'?9:map.getZoom()>=14?7:4);
    else path.setStyle(projectStyle(entry.f));
  });
});
for(const id of ['scope','stage','owner']) $(id).onchange=update;
$('search').addEventListener('input',update);
$('gardiner').onclick=()=>{
  locationControl.clear();
  $('scope').value='major';$('stage').value='all';$('owner').value='';$('search').value='Gardiner';
  $('select-all').click();update();$('fit').click();
  document.getElementById('results-tab').click();
};
Explorer.stamp(DATA.retrieved_at);
function clearNearby() {
  nearby=null;
  $('nearby-label').hidden=true;$('clear-nearby').hidden=true;
  update();
}
function setNearby(ll,radius) {
  const first=!nearby, changed=first || nearbyRadius!==radius || map.distance(nearby,ll)>5;
  nearby=ll;nearbyRadius=radius;
  let option=$('radius').querySelector('[data-custom]');
  if(![250,500,1000].includes(radius)) {
    if(!option){option=document.createElement('option');option.dataset.custom='true';$('radius').append(option);}
    option.value=radius;option.textContent=radius.toLocaleString()+' metres (dragged)';
  } else if(option)option.remove();
  $('radius').value=String(radius);
  $('nearby-label').textContent=`Within ${radius.toLocaleString()} metres of your reported location. Drag the circle edge or ↔ handle to resize. Distances are to project geometry.`;
  $('nearby-label').hidden=false;$('clear-nearby').hidden=false;
  if(changed)update();
  if(first)$('results-tab').click();
}
Explorer.connect(map,{bounds:()=>group.getBounds(),maxZoom:14});
locationControl=LocationCircle.connect(map,{change:setNearby,dismiss:clearNearby,status:Explorer.status});
$('clear-nearby').onclick=()=>locationControl.clear();
$('radius').onchange=()=>locationControl.resize(Number($('radius').value));

update();
const requested=new URLSearchParams(location.search).get('project');
if(requested) {
  const f=DATA.features.find(f=>f.properties.id===requested);
  if(f){$('scope').value=f.properties.collection;$('stage').value='all';update();const e=visible.find(e=>e.f===f);if(e)select(e);}
}
