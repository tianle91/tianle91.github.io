/* Local metric distances for Toronto-area project geometry. No geocoding requests. */
const Nearby = (() => {
  function distance(geometry, lat, lng) {
    if (!geometry) return Infinity;
    const scaleX = 111320 * Math.cos(lat * Math.PI / 180), scaleY = 111320;
    const xy = c => [(c[0]-lng)*scaleX,(c[1]-lat)*scaleY];
    const point = c => Math.hypot(...xy(c));
    function segment(a,b) {
      a=xy(a);b=xy(b);const dx=b[0]-a[0],dy=b[1]-a[1],d=dx*dx+dy*dy;
      const t=d?Math.max(0,Math.min(1,-(a[0]*dx+a[1]*dy)/d)):0;
      return Math.hypot(a[0]+t*dx,a[1]+t*dy);
    }
    const line = cs => cs.length===1 ? point(cs[0]) : cs.slice(1).reduce((best,c,i)=>Math.min(best,segment(cs[i],c)),Infinity);
    function inside(ring) {
      let yes=false;
      for(let i=0,j=ring.length-1;i<ring.length;j=i++){
        const a=ring[i],b=ring[j];
        if((a[1]>lat)!==(b[1]>lat) && lng<(b[0]-a[0])*(lat-a[1])/(b[1]-a[1])+a[0]) yes=!yes;
      }
      return yes;
    }
    const polygon = rings => inside(rings[0]) && !rings.slice(1).some(inside) ? 0 : Math.min(...rings.map(line));
    switch(geometry.type){
      case 'Point':return point(geometry.coordinates);
      case 'MultiPoint':return Math.min(...geometry.coordinates.map(point));
      case 'LineString':return line(geometry.coordinates);
      case 'MultiLineString':return Math.min(...geometry.coordinates.map(line));
      case 'Polygon':return polygon(geometry.coordinates);
      case 'MultiPolygon':return Math.min(...geometry.coordinates.map(polygon));
      default:return Infinity;
    }
  }
  return {distance};
})();
if(typeof module!=='undefined') module.exports=Nearby;
