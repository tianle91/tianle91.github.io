const $ = id => document.getElementById(id), esc = Explorer.esc;
const map = L.map('map', {preferCanvas:true}).setView([43.69,-79.43],11);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
const categories = [
  {id:'roads',label:'Roads & bridges',color:'#806493'},
  {id:'water',label:'Water & wastewater',color:'#258ac2'},
  {id:'transit',label:'TTC infrastructure',color:'#b94b3f'},
  {id:'power',label:'City-owned electricity',color:'#aa7618'},
  {id:'places',label:'Parks, housing & public places',color:'#278365'}
];
const colors = Object.fromEntries(categories.map(x=>[x.id,x.color]));
const group = L.featureGroup().addTo(map);
let visible = [], nearby = null, searchCircle = null;
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
  if(entry.layer) {Explorer.fit(map,entry.layer.getBounds(),15);entry.layer.openPopup();}
  else Explorer.detail(entry.f.properties.title,details(entry.f));
}
function update() {
  const q=$('search').value.toLowerCase().trim(), scope=$('scope').value, stage=$('stage').value, owner=$('owner').value;
  group.clearLayers(); visible=[];const counts={};
  for(const f of DATA.features) {
    const p=f.properties;
    const distance = nearby ? Nearby.distance(f.geometry,nearby.lat,nearby.lng) : null;
    if(nearby && distance>Number($('radius').value)) continue;
    if(scope!=='all' && p.collection!==scope) continue;
    if(stage==='open' ? ['Completed','Post-construction'].includes(p.stage) : stage!=='all' && p.stage!==stage) continue;
    if(owner && p.owner!==owner) continue;
    if(q && ![p.title,p.location,p.description,p.project_number,p.owner,p.stage].join(' ').toLowerCase().includes(q)) continue;
    counts[p.category]=(counts[p.category]||0)+1;
    if(!Explorer.enabled(p.category)) continue;
    let layer=null;
    if(f.geometry) {
      const color=p.stage==='Completed' ? '#76818a' : colors[p.category];
      layer=L.geoJSON(f,{
        onEachFeature: (_,path)=>{path.options.bubblingMouseEvents=false;},
        style:{color,weight:p.collection==='major'?6:1.5,opacity:p.collection==='major'?0.9:0.6,fillOpacity:0.12,dashArray:['Planning','Design'].includes(p.stage)?'7 6':null},
        pointToLayer:(_,ll)=>L.circleMarker(ll,{radius:p.collection==='major'?9:4,color:'#fff',weight:1.5,fillColor:color,fillOpacity:0.9,bubblingMouseEvents:false})
      });
      layer.bindPopup(()=>details(f),{...Explorer.detailPopup(p.title),maxWidth:370});
      layer.bindTooltip(p.title);group.addLayer(layer);
    }
    visible.push({f,layer,distance});
  }
  if(nearby) visible.sort((a,b)=>a.distance-b.distance);
  Explorer.layerCounts(Object.fromEntries(categories.map(c=>[c.id,counts[c.id]||0])));
  Explorer.count(visible.length,'project locations',visible.filter(x=>x.layer).length,nearby?'within '+$('radius').selectedOptions[0].text:'','without geometry');
  Explorer.results(visible,e=>e.f.properties.title,e=>`${nearby?Math.round(e.distance)+' m · ':''}${e.f.properties.stage} · ${e.f.properties.location || e.f.properties.owner}`,select);
  if(!visible.length) $('result-note').textContent='No matching project records in this snapshot. Broaden the radius, clear filters or ask the City. This does not establish that no work is planned.';
}
Explorer.layers(categories,update);
for(const id of ['scope','stage','owner']) $(id).onchange=update;
$('search').addEventListener('input',update);
$('gardiner').onclick=()=>{
  clearNearby();
  $('scope').value='major';$('stage').value='all';$('owner').value='';$('search').value='Gardiner';
  $('select-all').click();update();$('fit').click();
  document.getElementById('results-tab').click();
};
Explorer.stamp(DATA.retrieved_at);
function clearNearby() {
  nearby=null;if(searchCircle) {map.removeLayer(searchCircle);searchCircle=null;}
  $('nearby-label').hidden=true;$('clear-nearby').hidden=true;
}
function setNearby(ll) {
  nearby=ll;if(searchCircle) map.removeLayer(searchCircle);
  searchCircle=L.circle(ll,{radius:Number($('radius').value),color:'#182d37',weight:2,fillOpacity:0.04,interactive:false}).addTo(map);
  $('nearby-label').textContent=`Within ${$('radius').selectedOptions[0].text} of ${ll.lat.toFixed(4)}, ${ll.lng.toFixed(4)}. Distances are to mapped geometry, not work boundaries.`;
  $('nearby-label').hidden=false;
  $('clear-nearby').hidden=false;update();$('results-tab').click();
}
$('clear-nearby').onclick=()=>{clearNearby();update();};
$('radius').onchange=()=>{if(nearby)setNearby(nearby);};
map.on('click',e=>setNearby(e.latlng));
Explorer.connect(map,{bounds:()=>group.getBounds(),maxZoom:14,located:pos=>setNearby(L.latLng(pos.coords.latitude,pos.coords.longitude))});
update();
const requested=new URLSearchParams(location.search).get('project');
if(requested) {
  const f=DATA.features.find(f=>f.properties.id===requested);
  if(f){$('scope').value=f.properties.collection;$('stage').value='all';update();const e=visible.find(e=>e.f===f);if(e)select(e);}
}
