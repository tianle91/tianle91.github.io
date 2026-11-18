"""Explicit real-pointer regression. Run with the shared Python environment.

Serves a small fixture through the production renderer and app. No browser is
installed or launched by ordinary pytest/build/data commands.
"""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from staticsites.snapshots import Snapshotter
from build_site import render

ROOT = Path(__file__).resolve().parent.parent

def feature(id, title, geometry, collection='register'):
    return {'type':'Feature', 'geometry':geometry, 'properties':{
        'id':id, 'title':title, 'collection':collection, 'owner':'Transportation Services',
        'category':'roads', 'stage':'Construction', 'description':'Pointer regression fixture',
        'location':'Test street', 'schedule':'2026', 'source_status':'Active',
        'url':'https://map.toronto.ca/toinview/', 'geometry_note':'Test geometry'
    }}

def run(browser):
    data={'retrieved_at':'2026-11-18', 'features':[
        feature('line','Register line',{'type':'LineString','coordinates':[[-79.382,43.65],[-79.374,43.65]]}),
        feature('point','Register pin',{'type':'Point','coordinates':[-79.38,43.651]}),
        # Offscreen geometry still creates the higher renderer pane. Its blank
        # canvas must not intercept clicks on the register underneath it.
        feature('major','Major corridor',{'type':'LineString','coordinates':[[-79.49,43.7],[-79.48,43.7]]},'major')
    ]}
    with TemporaryDirectory() as temporary:
        root=Path(temporary);(root/'map.html').write_text(render(data))
        with Snapshotter(ROOT).serve(root) as base:
            for mobile in (False,True):
                context=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile,geolocation={'latitude':43.65,'longitude':-79.38},permissions=['geolocation'])
                page=context.new_page();errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(base+'/map.html')
                page.wait_for_function("typeof visible!=='undefined' && visible.length===3")
                page.evaluate("map.setView([43.65,-79.38],16,{animate:false})")
                page.wait_for_timeout(600)
                def click(lat,lng):
                    pt=page.evaluate('ll=>{const p=map.latLngToContainerPoint(ll),r=document.getElementById("map").getBoundingClientRect();return {x:r.left+p.x,y:r.top+p.y}}',[lat,lng])
                    if mobile: page.touchscreen.tap(pt['x'],pt['y'])
                    else: page.mouse.click(pt['x'],pt['y'])
                    page.wait_for_timeout(350)
                def close():
                    page.evaluate("if(document.getElementById('record-detail').open)document.getElementById('record-detail').close();map.closePopup()")
                    page.wait_for_timeout(350)
                # A register line and pin must remain selectable, including
                # after the selection overlay exists above both of them.
                for lat,lng,title in [(43.65,-79.378,'Register line'),(43.651,-79.38,'Register pin'),(43.65,-79.378,'Register line')]:
                    click(lat,lng)
                    assert page.locator('#selection-name').inner_text()==title, f'{mobile=}: click missed {title}'
                    assert page.evaluate('nearby===null'), 'Project click moved the nearby circle'
                    assert page.locator('#record-detail' if mobile else '.leaflet-popup').is_visible()
                    close()
                click(43.648,-79.384)
                assert page.evaluate('nearby===null'), 'Empty-map click unexpectedly started location search'
                assert page.locator('.radius-handle').count()==0
                page.locator('#locate').click()
                page.wait_for_function('nearby!==null')
                page.wait_for_timeout(400)
                assert page.locator('#locate').get_attribute('aria-pressed')=='true'
                assert page.locator('.you-dot').count()==1
                page.locator('.radius-handle button').press('ArrowRight')
                assert page.evaluate('nearbyRadius')==525
                assert page.locator('.radius-handle button').get_attribute('aria-valuenow')=='525'
                centre=page.evaluate('[nearby.lat,nearby.lng]')
                click(43.65,-79.378)
                assert page.locator('#selection-name').inner_text()=='Register line'
                assert page.evaluate('[nearby.lat,nearby.lng]')==centre
                close()
                # Drag the circumference itself, away from the east-side handle.
                coords=page.evaluate("""() => {
                  const c=nearby,r=nearbyRadius;
                  const p=map.latLngToContainerPoint([c.lat+r/111195,c.lng]);
                  const b=document.getElementById('map').getBoundingClientRect();
                  return {x:b.left+p.x,y:b.top+p.y};
                }""")
                x,y=coords['x'],coords['y']
                if mobile:
                    cdp=context.new_cdp_session(page)
                    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
                    for offset in range(10,61,10):
                        cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-offset}]})
                        page.wait_for_timeout(40)
                    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
                else:
                    page.mouse.move(x,y);page.mouse.down();page.mouse.move(x,y-60,steps=8);page.mouse.up()
                page.wait_for_timeout(400)
                assert page.evaluate('nearbyRadius')>550,'Circumference drag did not grow radius'
                assert page.evaluate('[nearby.lat,nearby.lng]')==centre,'Resize moved centre'
                assert page.evaluate('map.dragging.enabled()')
                # Location updates move the centre; dragging and ordinary map clicks cannot.
                context.set_geolocation({'latitude':43.6501,'longitude':-79.38})
                page.wait_for_function('Math.abs(nearby.lat-43.6501)<0.00001')
                page.evaluate("document.getElementById('clear-nearby').click()")
                assert page.evaluate('nearby===null')
                assert page.locator('.you-dot').count()==0
                assert page.locator('.radius-handle').count()==0
                assert page.locator('.radius-edge').count()==0
                assert page.locator('#locate').get_attribute('aria-pressed')=='false'
                context.set_geolocation({'latitude':43.651,'longitude':-79.38})
                page.wait_for_timeout(200)
                assert page.evaluate('nearby===null'),'Dismissed watch resurrected circle'
                page.locator('#locate').click()
                page.wait_for_function('nearby && Math.abs(nearby.lat-43.651)<0.00001')
                page.evaluate("document.getElementById('clear-nearby').click()")
                # Higher-pane major geometry must also remain interactive.
                page.evaluate("document.getElementById('clear-nearby').click();map.setView([43.7,-79.485],16,{animate:false});Explorer.collapse()")
                page.wait_for_timeout(600)
                click(43.7,-79.485)
                assert page.locator('#selection-name').inner_text()=='Major corridor'
                assert page.evaluate('nearby===null')
                assert not errors,errors
                print(f'{"Mobile touch" if mobile else "Desktop pointer"}: project clicks, location-only circle, circumference drag, location updates, dismissal and restart passed',flush=True)
                context.close()

            for mode in ('denied','pending'):
                context=browser.new_context()
                context.add_init_script("""Object.defineProperty(navigator,'geolocation',{value:{
                  getCurrentPosition(success,error){window.geoSuccess=success;window.geoError=error;},
                  watchPosition(){window.geoWatched=true;return 1;},clearWatch(){}
                }});""")
                page=context.new_page();page.goto(base+'/map.html')
                page.wait_for_function("typeof locationControl!=='undefined' && locationControl")
                assert page.evaluate('window.geoSuccess===undefined'),'Location requested before user action'
                page.locator('#locate').click()
                if mode=='denied':
                    page.evaluate('window.geoError({code:1})')
                    assert 'denied' in page.locator('#location-status').inner_text()
                else:
                    page.evaluate("locationControl.clear();window.geoSuccess({coords:{latitude:43.65,longitude:-79.38,accuracy:10}})")
                assert page.evaluate('nearby===null')
                assert page.locator('.you-dot').count()==0
                assert page.locator('.radius-handle').count()==0
                assert page.evaluate('!window.geoWatched')
                assert page.locator('#locate').get_attribute('aria-pressed')=='false'
                context.close()
            print('Permission denial and cancelled late location response passed',flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--browser-executable')
    args=parser.parse_args()
    with sync_playwright() as p:
        browser=p.chromium.launch(**({'executable_path':args.browser_executable} if args.browser_executable else {}))
        try:run(browser)
        finally:browser.close()

if __name__=='__main__':main()
