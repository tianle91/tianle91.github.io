/* Validated, deterministic URL state; no geolocation or permission state. */
const ViewState = (() => {
  const keys=['v','lat','lng','z','q','scope','stage','owner','layers','basemap','radius','project'];
  function parse(url, options) {
    const p=new URL(url).searchParams;
    const number=(key,min,max)=>{const text=p.get(key);if(text===null || !text.trim())return null;const n=Number(text);return Number.isFinite(n)&&n>=min&&n<=max?n:null;};
    const choice=(key,values,fallback)=>values.includes(p.get(key))?p.get(key):fallback;
    const lat=number('lat',-85.051129,85.051129),lng=number('lng',-180,180),z=number('z',0,19);
    const requested=p.get('layers');
    let layers=requested===null?[...options.layers]:options.layers.filter(id=>requested.split(',').includes(id));
    if(requested && !layers.length)layers=[...options.layers];
    const radius=number('radius',100,5000);
    return {
      view:lat!==null&&lng!==null&&z!==null?{lat,lng,z}:null,
      q:(p.get('q')||'').slice(0,300),
      scope:choice('scope',options.scopes,'all'),stage:choice('stage',options.stages,'open'),
      owner:choice('owner',options.owners,''),layers,
      basemap:choice('basemap',['0.4','1'],'0.4'),radius:radius===null?500:Math.round(radius/25)*25,
      project:p.get('project')||null,
      legacyProject:p.has('project')&&!keys.filter(k=>k!=='project').some(k=>p.has(k))
    };
  }
  function write(url,state,options) {
    const target=new URL(url),p=target.searchParams;
    for(const key of keys)p.delete(key);
    p.set('v','1');p.set('lat',Number(state.view.lat.toFixed(6)));p.set('lng',Number(state.view.lng.toFixed(6)));p.set('z',state.view.z);
    for(const [key,fallback] of [['q',''],['scope','all'],['stage','open'],['owner',''],['basemap','0.4'],['radius',500]]) {
      if(String(state[key])!==String(fallback))p.set(key,state[key]);
    }
    const layers=options.layers.filter(id=>state.layers.includes(id));
    if(layers.length!==options.layers.length)p.set('layers',layers.join(','));
    if(state.project)p.set('project',state.project);
    return target.href;
  }
  return {parse,write};
})();
if(typeof module!=='undefined')module.exports=ViewState;
