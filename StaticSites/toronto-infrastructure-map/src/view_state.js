/* Validated, deterministic URL state; no geolocation or permission state. */
const ViewState = (() => {
  const core=MapURL;
  const keys=['v','lat','lng','z','q','scope','stage','owner','layers','basemap','radius','project'];
  function parse(url, options) {
    const p=new URL(url).searchParams;
    const number=(key,min,max)=>core.number(p,key,min,max);
    const choice=(key,values,fallback)=>core.choice(p,key,values,fallback);
    const layers=core.layers(p,options.layers);
    const radius=number('radius',100,5000);
    return {
      view:core.view(p),
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
    core.writeView(p,state.view);
    for(const [key,fallback] of [['q',''],['scope','all'],['stage','open'],['owner',''],['basemap','0.4'],['radius',500]]) {
      if(String(state[key])!==String(fallback))p.set(key,state[key]);
    }
    core.writeLayers(p,state.layers,options.layers);
    if(state.project)p.set('project',state.project);
    return target.href;
  }
  return {parse,write};
})();
if(typeof module!=='undefined')module.exports=ViewState;
