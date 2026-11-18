/* Location permission, marker and radius share one dismissible lifecycle. */
const LocationCircle = (() => {
  function connect(map, {change, dismiss, status}) {
    const button=document.getElementById('locate');
    const pane=map.createPane('location-radius');pane.style.zIndex=480;
    const renderer=L.svg({pane:'location-radius'});
    let generation=0, watch=null, center=null, radius=500, layers=[], ring=null, edge=null, handle=null;
    let pending=null, finishDrag=null;
    const limit=value=>Math.max(100,Math.min(5000,Math.round(value/25)*25));
    function reset() {
      generation++;
      if(watch!==null) navigator.geolocation.clearWatch(watch);
      watch=null;if(finishDrag)finishDrag();
      if(pending!==null)clearTimeout(pending);pending=null;
      for(const layer of layers)map.removeLayer(layer);
      layers=[];center=null;ring=edge=handle=null;
      button.removeAttribute('aria-busy');button.setAttribute('aria-pressed','false');
      button.classList.remove('location-active');
      button.title='Find projects near my location';button.setAttribute('aria-label',button.title);
    }
    function notify() {pending=null;if(center)change(center,radius);}
    function resize(value, immediate=false) {
      radius=limit(value);
      if(ring){ring.setRadius(radius);edge.setRadius(radius);handle.setLatLng(east());
        const node=handle.getElement().querySelector('button');node.setAttribute('aria-valuenow',radius);node.setAttribute('aria-valuetext',radius+' metres');}
      if(immediate){if(pending!==null)clearTimeout(pending);notify();}
      else if(pending===null)pending=setTimeout(notify,120);
    }
    function east() {return L.latLng(center.lat,center.lng+radius/(6371000*Math.cos(center.lat*Math.PI/180))*180/Math.PI);}
    function beginDrag(event) {
      if(event.button!==undefined && event.button!==0)return;
      event.preventDefault();event.stopPropagation();
      const target=event.currentTarget;target.setPointerCapture(event.pointerId);
      const dragging=map.dragging.enabled();map.dragging.disable();
      const move=e=>{e.preventDefault();if(center)resize(map.distance(center,map.mouseEventToLatLng(e)));};
      finishDrag=()=>{
        document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',end);document.removeEventListener('pointercancel',end);
        if(target.hasPointerCapture(event.pointerId))target.releasePointerCapture(event.pointerId);
        if(dragging)map.dragging.enable();finishDrag=null;
      };
      const end=()=>{finishDrag();resize(radius,true);};
      document.addEventListener('pointermove',move,{passive:false});document.addEventListener('pointerup',end);document.addEventListener('pointercancel',end);
    }
    function position(pos, first=false) {
      center=L.latLng(pos.coords.latitude,pos.coords.longitude);
      for(const layer of layers)layer.setLatLng(center);
      if(!ring) {
        const marker=L.marker(center,{title:'Your reported location',zIndexOffset:2000,icon:L.divIcon({className:'',html:'<div class="you-dot"></div>',iconSize:[18,18],iconAnchor:[9,9]})}).addTo(map);
        ring=L.circle(center,{pane:'location-radius',renderer,radius,color:'#182d37',weight:2,fillOpacity:0.04,interactive:false}).addTo(map);
        edge=L.circle(center,{pane:'location-radius',renderer,radius,color:'#182d37',weight:14,opacity:0,fill:false,className:'radius-edge',bubblingMouseEvents:false}).addTo(map);
        handle=L.marker(east(),{title:'Drag to resize nearby radius',icon:L.divIcon({className:'radius-handle',html:'<button type="button" role="slider" aria-label="Nearby search radius" aria-valuemin="100" aria-valuemax="5000" aria-valuenow="500" aria-valuetext="500 metres">↔</button>',iconSize:[44,44],iconAnchor:[22,22]})}).addTo(map);
        layers=[marker,ring,edge,handle];
        edge.getElement().addEventListener('pointerdown',beginDrag);
        const slider=handle.getElement().querySelector('button');slider.addEventListener('pointerdown',beginDrag);
        slider.addEventListener('keydown',event=>{
          const step=event.shiftKey?100:25;
          const value={ArrowRight:radius+step,ArrowUp:radius+step,ArrowLeft:radius-step,ArrowDown:radius-step,Home:100,End:5000}[event.key];
          if(value!==undefined){event.preventDefault();resize(value,true);}
        });
      }
      handle.setLatLng(east());
      const slider=handle.getElement().querySelector('button');
      slider.setAttribute('aria-valuenow',radius);slider.setAttribute('aria-valuetext',radius+' metres');
      button.removeAttribute('aria-busy');button.setAttribute('aria-pressed','true');button.classList.add('location-active');
      button.title='Refresh my location';button.setAttribute('aria-label',button.title);
      change(center,radius);
      const accuracy=Number.isFinite(pos.coords.accuracy)?` Reported accuracy: about ${Math.round(pos.coords.accuracy)} m.`:'';
      status('Circle centred on your reported location.'+accuracy);
      if(first)Explorer.focus(map,center,15);
    }
    function request() {
      reset();dismiss();
      if(!navigator.geolocation){status('Location is unavailable in this browser.');return;}
      const token=generation;button.setAttribute('aria-busy','true');status('Finding your location…');
      navigator.geolocation.getCurrentPosition(pos=>{
        if(token!==generation)return;position(pos,true);
        watch=navigator.geolocation.watchPosition(next=>{if(token===generation)position(next);},error=>{
          if(token!==generation)return;
          if(error.code===1){reset();dismiss();status('Location access was denied. Use ◎ to retry after allowing access.');}
          else status('Location updates are unavailable. Circle shows your last reported location.');
        },{enableHighAccuracy:true,maximumAge:0,timeout:15000});
      },error=>{
        if(token!==generation)return;reset();dismiss();
        status(error.code===1?'Location access was denied. Allow location access and use ◎ to retry.':'Your location could not be determined. Use ◎ to retry.');
      },{enableHighAccuracy:true,maximumAge:0,timeout:10000});
    }
    // This project owns the shared button's lifecycle so dismissal can remove
    // the marker and stop location updates together with its nearby circle.
    button.onclick=request;button.setAttribute('aria-pressed','false');
    button.title='Find projects near my location';button.setAttribute('aria-label',button.title);
    return {resize:value=>resize(value,true),clear:()=>{reset();dismiss();status('Location circle dismissed. Use ◎ to start again.');}};
  }
  return {connect};
})();
