#!/usr/bin/env python3
"""Explicit actual-artifact desktop/mobile URL sharing checks and review capture.

Run with the shared Python environment after offline builds. Uses an existing
browser; never installs tools or refreshes project data.
"""
import argparse
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import sync_playwright
from staticsites.snapshots import Snapshotter
ROOT=Path(__file__).resolve().parents[1]
PROJECTS={
 'ontario-physiotherapy-clinics-map':[],
 'toronto-vulnerable-services-map':[],
 'toronto-crime-map':[],
 'toronto-dinesafe-map':['near-toggle'],
 'toronto-building-permits-map':['status','type','year'],
 'trca-flood-plain-map':['watershed'],
 'union-station-transit-isochrone':[],
}

def run(browser, snapshots=False, projects=None):
 with Snapshotter(ROOT).serve(ROOT) as base:
  for slug in projects or PROJECTS:
   fields=PROJECTS[slug]
   snap=Snapshotter(ROOT/slug)
   url=f'{base}/{slug}/output/{slug}.html'
   if snapshots:snap.generate(browser,url)
   for mobile in (False,True):
    context=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile,color_scheme='light')
    context.route('**/api/3/action/**',lambda route:route.abort())
    context.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copiedView=text;}}});window.geoRequests=0;const original=navigator.geolocation.getCurrentPosition.bind(navigator.geolocation);navigator.geolocation.getCurrentPosition=(...args)=>{window.geoRequests++;return original(...args);};")
    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url+'?utm_source=share-regression#anchor',timeout=120000);page.wait_for_function(snap.READY,timeout=120000)
    assert page.locator('#copy-view').is_visible()
    assert page.locator('#copy-view').get_attribute('aria-label')=='Copy link to this view'
    assert page.locator('.search-row #search').count()==1 and page.locator('.search-row #copy-view svg').count()==1
    assert page.locator('.share-view').count()==0
    # One enabled category and a query yield a compact but nonempty/empty
    # result set deterministically, including chunked permit rendering.
    chosen=page.evaluate("document.querySelector('[data-layer]').dataset.layer")
    values=page.evaluate('''fields=>{
      const values={};
      for(const id of fields){const node=document.getElementById(id);values[id]=node.type==='checkbox'?'0':node.options.length>1?node.options[1].value:node.value;}
      return values;
    }''',fields)
    page.evaluate('''({chosen,values})=>{
      const search=document.getElementById('search');search.value='zzzz-share-regression';search.dispatchEvent(new Event('input',{bubbles:true}));
      for(const node of document.querySelectorAll('[data-layer]')){node.checked=node.dataset.layer===chosen;node.dispatchEvent(new Event('change',{bubbles:true}));}
      for(const [id,value] of Object.entries(values)){const node=document.getElementById(id);if(node.type==='checkbox')node.checked=value==='1';else node.value=value;node.dispatchEvent(new Event('change',{bubbles:true}));}
      Explorer.collapse();
    }''',{'chosen':chosen,'values':values})
    page.locator('#map').drag_to(page.locator('#map'),source_position={'x':220,'y':150},target_position={'x':270,'y':190})
    page.wait_for_timeout(600)
    page.locator('#copy-view').click()
    shared=page.evaluate('window.copiedView');assert shared
    expected=parse_qs(urlsplit(shared).query,keep_blank_values=True)
    assert expected['q']==['zzzz-share-regression'] and expected['layers']==[chosen]
    page.goto(shared,timeout=120000);page.wait_for_function(snap.READY,timeout=120000)
    assert page.locator('#search').input_value()=='zzzz-share-regression'
    assert page.locator('#stats strong').inner_text()=='0'
    assert urlsplit(page.url).fragment=='anchor'
    assert page.evaluate("[...document.querySelectorAll('[data-layer]')].filter(n=>n.checked).map(n=>n.dataset.layer)")==[chosen]
    for id,value in values.items():
     actual=page.locator('#'+id).is_checked() if id=='near-toggle' else page.locator('#'+id).input_value()
     assert actual==(False if id=='near-toggle' else value),(slug,id,actual,value)
    page.locator('#copy-view').click()
    restored=parse_qs(urlsplit(page.evaluate('window.copiedView')).query,keep_blank_values=True)
    # Pixel rounding varies by viewport: compare the projected camera centres.
    difference=page.evaluate('''([old,now])=>{
      const a=L.CRS.EPSG3857.latLngToPoint(L.latLng(+old.lat[0],+old.lng[0]),+old.z[0]);
      const b=L.CRS.EPSG3857.latLngToPoint(L.latLng(+now.lat[0],+now.lng[0]),+now.z[0]);return a.distanceTo(b);
    }''',[expected,restored])
    assert difference<=1,(slug,mobile,difference)
    assert expected['z']==restored['z']
    assert page.evaluate('window.geoRequests')==0
    # No categories selected is a real shareable state, not a missing default.
    page.evaluate("document.getElementById('clear-all').click()")
    page.locator('#copy-view').click();empty=page.evaluate('window.copiedView')
    assert parse_qs(urlsplit(empty).query,keep_blank_values=True)['layers']==['']
    page.goto(empty,timeout=120000);page.wait_for_function(snap.READY,timeout=120000)
    assert page.evaluate("[...document.querySelectorAll('[data-layer]')].every(n=>!n.checked)")
    page.evaluate("url=>{history.pushState({},'',url);window.dispatchEvent(new PopStateEvent('popstate'));}",shared)
    assert page.evaluate("[...document.querySelectorAll('[data-layer]')].filter(n=>n.checked).length")==1
    page.go_back();page.wait_for_function("[...document.querySelectorAll('[data-layer]')].every(n=>!n.checked)")
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert not errors,errors
    print(f'{slug} {"mobile" if mobile else "desktop"}: camera/search/layers/specific filters/copy/empty layers/no location passed',flush=True)
    context.close()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--browser-executable');parser.add_argument('--snapshots',action='store_true');parser.add_argument('--project',choices=list(PROJECTS),action='append');args=parser.parse_args()
 with sync_playwright() as p:
  # Large permit/inspection snapshots get a fresh browser per project so closed
  # contexts cannot accumulate memory across the entire matrix.
  for slug in args.project or PROJECTS:
   browser=p.chromium.launch(**({'executable_path':args.browser_executable} if args.browser_executable else {}))
   try:run(browser,args.snapshots,[slug])
   finally:browser.close()
if __name__=='__main__':main()
