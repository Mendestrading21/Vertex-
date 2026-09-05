"""Exécute les sondes de `boutons_morts` sur une page témoin. Sortie : JSON.

DANS UN SOUS-PROCESSUS, et c'est nécessaire : `ib_async` applique
`nest_asyncio`, ce qui fait croire à Playwright qu'une boucle asyncio
tourne — son API synchrone refuse alors de démarrer dans le processus de
test. Mesuré : le banc échouait sur « Playwright Sync API inside the
asyncio loop » avant même d'ouvrir un navigateur.
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
from playwright.sync_api import sync_playwright
from tools.audit import boutons_morts as bm

EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
PAGE = """
<!doctype html><html><head><meta charset="utf-8"></head><body>
  <input id="champ" value="depart">
  <button id="mort" type="button">Ne fait rien</button>
  <button id="remplit" type="button"
          onclick="document.getElementById('champ').value='rempli'">Remplit</button>
  <button id="coche" type="button"
          onclick="document.getElementById('case').checked=true">Coche</button>
  <input type="checkbox" id="case">
  <button id="mute" type="button"
          onclick="document.body.appendChild(document.createElement('span'))">Mute</button>
  <button id="va" type="button"
          onclick="location.href='/ailleurs'">Va</button>
</body></html>
"""
_LIRE = ('() => { const e = window.__vxEffet'
         ' || {dom:0,stockage:0,defile:0,champs:0,y0:0,x0:0};'
         ' if (window.scrollY !== e.y0 || window.scrollX !== e.x0) e.defile = 1;'
         ' if (window.__vxChamps && e.c0 !== undefined'
         '     && window.__vxChamps() !== e.c0) e.champs = 1;'
         ' return e; }')

#  La page temoin est SERVIE par un vrai serveur : `set_content` produit un
#  document a origine opaque, ou `localStorage` est refuse — et `_JS_ARMER`,
#  qui instrumente justement le stockage, y leve une SecurityError.
import http.server, socket, threading


class _Poste(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        #  Chrome refuse une navigation de premier niveau vers `data:` : le
        #  temoin de navigation doit viser une VRAIE page.
        corps = (b'<!doctype html><p>ailleurs</p>' if self.path.startswith('/ailleurs')
                 else PAGE.encode('utf-8'))
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def log_message(self, *a):
        pass


_prise = socket.socket(); _prise.bind(('127.0.0.1', 0))
_port = _prise.getsockname()[1]; _prise.close()
_serveur = http.server.HTTPServer(('127.0.0.1', _port), _Poste)
threading.Thread(target=_serveur.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:%d/' % _port

out = {}
kw = {'executable_path': EXE} if os.path.exists(EXE) else {}
with sync_playwright() as pw:
    nav = pw.chromium.launch(**kw)
    ctx = nav.new_context(viewport={'width': 900, 'height': 600})
    page = ctx.new_page()
    for ident in ('mort', 'remplit', 'coche', 'mute', 'va'):
        page.goto(BASE, wait_until='domcontentloaded')
        page.evaluate(bm._JS_ARMER)
        url_avant = page.url
        page.click('#' + ident)
        page.wait_for_timeout(150)
        e = page.evaluate(_LIRE)
        e['a_navigue'] = (page.url != url_avant)
        out[ident] = e
    ctx.close(); nav.close()
_serveur.shutdown()
print(json.dumps(out))
