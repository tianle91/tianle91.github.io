/* Project-local explorer UI. No source is loaded from another project. */
const Explorer = (() => {
  const byId = (id) => document.getElementById(id);
  const esc = (value) =>
    String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const choices = new Map();
  const mobile = () => matchMedia("(max-width:760px)").matches;
  function collapse() {
    byId("panel").classList.remove("expanded");
    byId("sheet-toggle").setAttribute("aria-expanded", "false");
    byId("sheet-toggle").setAttribute("aria-label", "Expand map controls");
    byId("sheet-toggle").textContent = "Show results & filters";
  }
  function sheetHeight() {
    return mobile() ? byId("panel").getBoundingClientRect().height : 0;
  }
  function tab(name) {
    // Programmatic navigation (diagnostics, trip results, provenance) must also
    // reveal its panel when the phone is showing the compact map view.
    if (name !== "layers") expandSearch();
    document.querySelectorAll(".explorer-tabs [role=tab]").forEach((button) => {
      button.setAttribute("aria-selected", String(button.dataset.tab === name));
      button.tabIndex = button.dataset.tab === name ? 0 : -1;
    });
    document
      .querySelectorAll(".explorer-panel")
      .forEach((panel) => (panel.hidden = panel.id !== name + "-panel"));
  }
  document.querySelectorAll(".explorer-tabs [role=tab]").forEach((button) => {
    button.onclick = () => tab(button.dataset.tab);
    button.onkeydown = (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key))
        return;
      event.preventDefault();
      const buttons = [
        ...document.querySelectorAll(".explorer-tabs [role=tab]"),
      ];
      const index = buttons.indexOf(button);
      const next =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? buttons.length - 1
            : (index + (event.key === "ArrowRight" ? 1 : buttons.length - 1)) %
              buttons.length;
      buttons[next].focus();
      tab(buttons[next].dataset.tab);
    };
  });
  tab("layers");
  byId("provenance").onclick = () => tab("sources");
  byId("sheet-toggle").onclick = () => {
    const expanded = byId("panel").classList.toggle("expanded");
    byId("sheet-toggle").setAttribute("aria-expanded", String(expanded));
    byId("sheet-toggle").setAttribute(
      "aria-label",
      expanded ? "Collapse map controls" : "Expand map controls",
    );
    byId("sheet-toggle").textContent = expanded ? "Show more map" : "Show results & filters";
  };
  function expandSearch() {
    if (!mobile()) return;
    byId("panel").classList.add("expanded");
    byId("sheet-toggle").setAttribute("aria-expanded", "true");
    byId("sheet-toggle").setAttribute("aria-label", "Collapse map controls");
    byId("sheet-toggle").textContent = "Show more map";
  }
  byId("search").addEventListener("focus", expandSearch);
  byId("search").addEventListener("keydown", (event) => {
    if (event.key === "Enter") byId("search").blur();
  });
  // iOS changes the visual viewport when its keyboard opens without changing
  // layout viewport units. Size the phone layout to the actually visible area.
  if (typeof window !== "undefined" && window.visualViewport) {
    const resize = () => document.documentElement.style.setProperty(
      "--visible-height", window.visualViewport.height + "px",
    );
    window.visualViewport.addEventListener("resize", resize);
    resize();
  }
  byId("search").addEventListener("input", () =>
    tab(byId("search").value.trim() ? "results" : "layers"),
  );
  const status = (message) => {
    byId("location-status").textContent = message;
  };
  function count(
    total,
    unit,
    mapped,
    note = "",
    missingLabel = "without a pin",
  ) {
    const stats = byId("stats");
    stats.replaceChildren();
    const number = document.createElement("strong");
    number.textContent = total.toLocaleString();
    stats.append(number, document.createTextNode(" " + unit));
    const secondary = document.createElement("div");
    secondary.className = "secondary";
    secondary.textContent =
      mapped == null
        ? note
        : mapped.toLocaleString() +
          " mapped · " +
          (total - mapped).toLocaleString() +
          " " +
          missingLabel +
          (note ? " · " + note : "");
    stats.append(secondary);
  }
  function layers(items, onChange) {
    const target = byId("layer-controls");
    target.replaceChildren();
    choices.clear();
    for (const item of items) {
      const label = document.createElement("label");
      label.className = "layer-row";
      const input = document.createElement("input");
      input.type = "checkbox";
      input.checked = item.checked !== false;
      input.dataset.layer = item.id;
      const name = document.createElement("span");
      name.className = "layer-label";
      const dot = document.createElement("span");
      dot.className = "swatch";
      dot.style.background = item.color;
      name.append(dot, document.createTextNode(item.label));
      const n = document.createElement("span");
      n.className = "layer-count";
      n.textContent =
        typeof item.count === "number"
          ? item.count.toLocaleString()
          : (item.count ?? "");
      label.append(input, name, n);
      target.append(label);
      choices.set(item.id, { input, n, item });
      input.onchange = () => {
        if (item.layer) {
          if (input.checked) item.layer.addTo(item.map);
          else item.map.removeLayer(item.layer);
        }
        onChange();
      };
    }
    for (const [id, value] of [
      ["select-all", true],
      ["clear-all", false],
    ])
      byId(id).onclick = () => {
        for (const { input, item } of choices.values()) {
          input.checked = value;
          if (item.layer) {
            if (value) item.layer.addTo(item.map);
            else item.map.removeLayer(item.layer);
          }
        }
        onChange();
      };
  }
  const enabled = (id) => choices.get(id)?.input.checked ?? false;
  function layerCounts(counts) {
    for (const [id, n] of Object.entries(counts)) {
      const choice = choices.get(id);
      if (choice) choice.n.textContent = Number(n).toLocaleString();
    }
  }
  function results(items, label, summary, onSelect, limit = 50) {
    const target = byId("results");
    target.replaceChildren();
    for (const item of items.slice(0, limit)) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "feature-result";
      const title = document.createElement("strong");
      title.textContent = label(item);
      const sub = document.createElement("small");
      sub.textContent = summary(item);
      button.append(title, sub);
      button.onclick = () => {
        byId("search").blur();
        onSelect(item);
      };
      target.append(button);
    }
    // The count above already covers a complete result list. Keep warnings
    // about empty or truncated lists visible even in the compact phone panel.
    byId("result-note").classList[items.length && items.length <= limit ? "add" : "remove"]("complete-list");
    byId("result-note").textContent = !items.length
      ? "No features match the selected layers and search."
      : items.length > limit
        ? "First " +
          limit +
          " of " +
          items.length.toLocaleString() +
          " matches listed. Narrow the search to find a specific feature."
        : items.length.toLocaleString() + " matching features.";
  }
  function stamp(value) {
    byId("snapshot-date").textContent = value
      ? "Snapshot " + String(value).slice(0, 10)
      : "Committed snapshot";
    byId("snapshot-provenance").textContent = byId("snapshot-date").textContent;
  }
  function fit(map, bounds, maxZoom = 16) {
    collapse();
    if (bounds?.isValid()) {
      map.fitBounds(bounds, {
        paddingTopLeft: [30, 30],
        paddingBottomRight: [30, sheetHeight() + 30],
        maxZoom,
      });
      status("");
    } else status("No mapped features match the selected layers and search.");
  }
  function focus(map, ll, zoom = 16) {
    collapse();
    map.setView(ll, zoom, { animate: false });
    if (mobile()) map.panBy([0, sheetHeight() / 2], { animate: false });
  }
  function detail(title, html) {
    const dialog = byId("record-detail");
    byId("record-title").textContent = title;
    byId("record-body").innerHTML = html;
    if (!dialog.open) dialog.showModal();
  }
  byId("record-close").onclick = () => byId("record-detail").close();
  function detailPopup(title) {
    return { detailTitle: title, autoPan: !mobile() };
  }
  function connect(map, config) {
    // Resolve lazy content only when selected. Desktop retains its anchored
    // popups; long phone details get a separate scroll area and fixed close.
    map.on("popupopen", ({ popup }) => {
      if (!mobile() || !popup.options.detailTitle) return;
      let content = popup.getContent();
      if (typeof content === "function") content = content();
      map.closePopup();
      detail(popup.options.detailTitle, typeof content === "string" ? content : content.innerHTML);
    });
    if (mobile()) map.panBy([0, sheetHeight() / 2], { animate: false });
    let userMarker = null,
      accuracyCircle = null;
    const Control = L.Control.extend({
      options: { position: "topleft" },
      onAdd() {
        const container = L.DomUtil.create(
          "div",
          "leaflet-bar explorer-control",
        );
        const button = L.DomUtil.create("button", "", container);
        button.type = "button";
        button.id = "locate";
        button.title = "Center on my location";
        button.setAttribute("aria-label", "Center on my location");
        button.textContent = "◎";
        L.DomEvent.disableClickPropagation(container);
        L.DomEvent.disableScrollPropagation(container);
        button.onclick = () => {
          if (!navigator.geolocation) {
            status(
              "Location is unavailable. Use a browser with location support on HTTPS or localhost.",
            );
            return;
          }
          button.disabled = true;
          button.setAttribute("aria-busy", "true");
          status("Finding your location…");
          const finish = (message) => {
            button.disabled = false;
            button.removeAttribute("aria-busy");
            status(message);
          };
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              const ll = [pos.coords.latitude, pos.coords.longitude],
                accuracy = pos.coords.accuracy;
              if (userMarker) userMarker.setLatLng(ll);
              else
                userMarker = L.marker(ll, {
                  icon: L.divIcon({
                    className: "",
                    html: '<div class="you-dot"></div>',
                    iconSize: [18, 18],
                    iconAnchor: [9, 9],
                  }),
                  zIndexOffset: 2000,
                  title: "You are here",
                })
                  .addTo(map)
                  .bindPopup("You are here");
              if (Number.isFinite(accuracy) && accuracy > 0) {
                if (accuracyCircle)
                  accuracyCircle.setLatLng(ll).setRadius(accuracy);
                else
                  accuracyCircle = L.circle(ll, {
                    radius: accuracy,
                    color: "#258fc1",
                    weight: 1,
                    fillOpacity: 0.08,
                    interactive: false,
                  }).addTo(map);
              } else if (accuracyCircle) {
                map.removeLayer(accuracyCircle);
                accuracyCircle = null;
              }
              focus(map, ll, 14);
              finish(
                "Centered on your location." +
                  (Number.isFinite(accuracy) && accuracy > 0
                    ? " Browser accuracy: about " +
                      Math.max(1, Math.round(accuracy)).toLocaleString() +
                      " m."
                    : ""),
              );
              if (config.located) config.located(pos);
            },
            (error) =>
              finish(
                {
                  1: "Location access was denied. Enable location for this site in your browser, then try again.",
                  2: "Your location could not be determined. Please try again.",
                  3: "Finding your location timed out. Please try again.",
                }[error.code] ||
                  "Your location could not be determined. Please try again.",
              ),
            { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 },
          );
        };
        return container;
      },
    });
    map.addControl(new Control());
    const Fit = L.Control.extend({
      options: { position: "topleft" },
      onAdd() {
        const container = L.DomUtil.create(
            "div",
            "leaflet-bar explorer-control",
          ),
          button = L.DomUtil.create("button", "", container);
        button.type = "button";
        button.id = "fit";
        button.title = "Fit matching features";
        button.setAttribute("aria-label", "Fit matching features");
        button.textContent = "⛶";
        L.DomEvent.disableClickPropagation(container);
        button.onclick = () => {
          fit(map, config.bounds(), config.maxZoom || 16);
        };
        return container;
      },
    });
    map.addControl(new Fit());
    // Location stays in memory only and is requested solely by the locate button.
  }
  function hasSharedView() {
    return typeof location!=='undefined' && !!location.href && typeof MapURL!=='undefined' && !!MapURL.view(new URL(location.href).searchParams);
  }
  // Project adapters opt in after their controls and initial view are ready.
  function share(map, {update, fields=[]} = {}) {
    if(typeof location==='undefined' || typeof history==='undefined')return;
    const ids=[...choices.keys()], defaults=new Map(), initialLayers=ids.filter(enabled);
    const inputs=fields.map(id=>byId(id));
    for(const input of inputs) defaults.set(input.id,input.type==='checkbox'?(input.checked?'1':'0'):input.value);
    const initialView={lat:map.getCenter().lat,lng:map.getCenter().lng,z:map.getZoom()};
    const keys=['v','lat','lng','z','q','layers',...fields];
    let timer=null, restoring=false;
    const holder=document.createElement('div');holder.className='share-view';
    const copy=document.createElement('button');copy.id='copy-view';copy.type='button';copy.textContent='Copy link to this view';
    const message=document.createElement('p');message.id='share-status';message.setAttribute('role','status');message.setAttribute('aria-live','polite');
    holder.append(copy,message);byId('stats').after(holder);
    byId('search').maxLength=300;
    function save() {
      clearTimeout(timer);if(restoring)return;
      const url=new URL(location.href),params=url.searchParams;
      for(const key of keys)params.delete(key);
      const center=map.getCenter().wrap();
      MapURL.writeView(params,{lat:Math.max(-85.051129,Math.min(85.051129,center.lat)),lng:center.lng,z:map.getZoom()});
      MapURL.writeLayers(params,ids.filter(enabled),ids);
      if(byId('search').value)params.set('q',byId('search').value);
      for(const input of inputs) {
        const value=input.type==='checkbox'?(input.checked?'1':'0'):input.value;
        if(value!==defaults.get(input.id))params.set(input.id,value);
      }
      if(url.href!==location.href)history.replaceState(history.state,'',url.href);
    }
    function schedule() {if(!restoring){clearTimeout(timer);timer=setTimeout(save,400);}}
    function restore(initial=false) {
      clearTimeout(timer);restoring=true;
      const params=new URL(location.href).searchParams;
      if(!initial || keys.some(key=>params.has(key))) {
        map.stop();map.closePopup();if(byId('record-detail')?.open)byId('record-detail').close();
        byId('search').value=(params.get('q')||'').slice(0,300);
        for(const input of inputs) {
          const values=input.type==='checkbox'?['0','1']:[...input.options].map(option=>option.value);
          const value=MapURL.choice(params,input.id,values,defaults.get(input.id));
          if(input.type==='checkbox')input.checked=value==='1';else input.value=value;
        }
        const selected=params.has('layers')?MapURL.layers(params,ids):initialLayers;
        for(const [id,{input,item}] of choices) {
          input.checked=selected.includes(id);
          if(item.layer){if(input.checked)item.layer.addTo(item.map);else item.map.removeLayer(item.layer);}
        }
        update();
        const view=MapURL.view(params)||initialView;
        map.setView([view.lat,view.lng],Math.min(view.z,map.getMaxZoom()),{animate:false});
      }
      restoring=false;schedule();
    }
    byId('panel').addEventListener('input',schedule);
    byId('panel').addEventListener('change',schedule);
    for(const id of ['select-all','clear-all'])byId(id).addEventListener('click',schedule);
    map.on('moveend',schedule);window.addEventListener('popstate',()=>restore());
    copy.onclick=async()=>{
      save();
      try {await navigator.clipboard.writeText(location.href);message.textContent='Link copied. Recipients enable their own location.';}
      catch {message.textContent='Copy the link from your browser’s address bar. Recipients enable their own location.';}
    };
    restore(true);
    return {save,restore};
  }

  return {
    share,
    hasSharedView,
    mobile,
    detailPopup,
    esc,
    tab,
    count,
    layers,
    enabled,
    layerCounts,
    results,
    stamp,
    fit,
    focus,
    detail,
    connect,
    collapse,
    status,
  };
})();
