/* Small URL primitives shared by the map adapters; no geolocation state. */
const MapURL = (() => {
  function number(params,key,min,max) {
    const text=params.get(key);if(text===null || !text.trim())return null;
    const value=Number(text);return Number.isFinite(value)&&value>=min&&value<=max?value:null;
  }
  function view(params) {
    const lat=number(params,'lat',-85.051129,85.051129),lng=number(params,'lng',-180,180),z=number(params,'z',0,19);
    return lat!==null&&lng!==null&&z!==null?{lat,lng,z}:null;
  }
  function layers(params,ids) {
    const text=params.get('layers');if(text===null)return [...ids];
    const chosen=ids.filter(id=>text.split(',').includes(id));
    return text && !chosen.length?[...ids]:chosen;
  }
  const choice=(params,key,values,fallback)=>values.includes(params.get(key))?params.get(key):fallback;
  function writeView(params,camera) {
    params.set('v','1');params.set('lat',Number(camera.lat.toFixed(6)));params.set('lng',Number(camera.lng.toFixed(6)));params.set('z',camera.z);
  }
  function writeLayers(params,chosen,ids) {
    params.delete('layers');const ordered=ids.filter(id=>chosen.includes(id));
    if(ordered.length!==ids.length)params.set('layers',ordered.join(','));
  }
  return {number,view,layers,choice,writeView,writeLayers};
})();
if(typeof module!=='undefined')module.exports=MapURL;
