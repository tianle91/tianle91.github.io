"""Explicit browser regression for sharing and restoring the production UI."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright
from staticsites.snapshots import Snapshotter
from build_site import render
from check_clicks import feature
ROOT=Path(__file__).resolve().parent.parent

def run(browser):
    bridge=feature('bridge','Bridge & road',{'type':'Point','coordinates':[-79.38,43.65]})
    water=feature('water','Water work',{'type':'Point','coordinates':[-79.37,43.65]})
    water['properties'].update(owner='Toronto Water',category='water')
    major=feature('gardiner-3','Gardiner 3',{'type':'Point','coordinates':[-79.49,43.7]},'major')
    data={'retrieved_at':'2026-11-18','features':[bridge,water,major]}
    with TemporaryDirectory() as temporary:
        root=Path(temporary);(root/'map.html').write_text(render(data))
        with Snapshotter(ROOT).serve(root) as base:
            for mobile in (False,True):
                context=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},is_mobile=mobile,has_touch=mobile)
                context.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copiedView=text;}}});")
                page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/map.html');page.wait_for_function('urlReady')
                page.evaluate("""() => {
                  $('search').value='Bridge & road';$('scope').value='register';$('stage').value='Construction';$('owner').value='Transportation Services';
                  document.querySelectorAll('[data-layer]').forEach(input=>{input.checked=input.dataset.layer==='roads';});
                  $('basemap').value='1';$('basemap').dispatchEvent(new Event('change'));
                  $('radius').value='1000';$('radius').dispatchEvent(new Event('change'));
                  update();map.setView([43.65,-79.38],15,{animate:false});
                }""")
                page.wait_for_function("new URL(location.href).searchParams.get('owner')==='Transportation Services'")
                page.locator('#copy-view').click()
                assert page.evaluate('window.copiedView')==page.url
                shared=page.url
                restored=context.new_page();restored.on('pageerror',lambda e:errors.append(str(e)))
                restored.goto(shared);restored.wait_for_function('urlReady')
                assert restored.evaluate("$('search').value")=='Bridge & road'
                assert restored.evaluate("[$('scope').value,$('stage').value,$('owner').value,$('basemap').value,$('radius').value]")==['register','Construction','Transportation Services','1','1000']
                assert restored.evaluate('categories.filter(c=>Explorer.enabled(c.id)).map(c=>c.id)')==['roads']
                assert restored.evaluate('visible.map(e=>e.f.properties.id)')==['bridge']
                assert restored.evaluate('map.getCenter().lat')==43.65
                assert restored.evaluate('map.getCenter().lng')==-79.38
                assert restored.evaluate('map.getZoom()')==15
                assert restored.evaluate('nearby===null')
                # Empty layer selection must survive a reload.
                restored.evaluate("$('clear-all').click()")
                restored.wait_for_function("new URL(location.href).searchParams.get('layers')===''")
                restored.reload();restored.wait_for_function('urlReady')
                assert restored.evaluate('visible.length')==0
                # Browser history restores a previous combo without adding pan/typing entries.
                page.evaluate("history.pushState({},'',location.pathname+'?lat=43.7&lng=-79.4&z=13&layers=water');window.dispatchEvent(new PopStateEvent('popstate'))")
                assert page.evaluate('categories.filter(c=>Explorer.enabled(c.id)).map(c=>c.id)')==['water']
                page.go_back();page.wait_for_function("$('search').value==='Bridge & road'")
                # Legacy record links remain valid; highlighted links preserve an explicit camera.
                restored.goto(base+'/map.html?project=gardiner-3');restored.wait_for_function("selectedProject==='gardiner-3'")
                restored.evaluate("if($('record-detail').open)$('record-detail').close();map.closePopup()")
                restored.goto(base+'/map.html?'+urlencode({'v':1,'project':'bridge','lat':43.64,'lng':-79.4,'z':12}))
                restored.wait_for_function("urlReady && selectedProject==='bridge'")
                assert restored.evaluate('map.project(map.getCenter(),12).distanceTo(map.project([43.64,-79.4],12))')<1
                assert restored.evaluate('map.getZoom()')==12
                restored.goto(base+'/map.html?lat=oops&lng=999&z=Infinity&scope=bad&stage=bad&owner=bad&layers=unknown&radius=999999&basemap=evil')
                restored.wait_for_function('urlReady')
                assert restored.evaluate('visible.length')==3
                assert restored.evaluate('nearby===null')
                assert restored.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert not errors,errors
                print(f'{"Mobile" if mobile else "Desktop"}: share/copy, fresh restore, empty layers, history, legacy projects and invalid parameters passed',flush=True)
                context.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--browser-executable');args=parser.parse_args()
    with sync_playwright() as p:
        browser=p.chromium.launch(**({'executable_path':args.browser_executable} if args.browser_executable else {}))
        try:run(browser)
        finally:browser.close()
if __name__=='__main__':main()
