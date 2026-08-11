# Smoke-check santé (protocole LOT 251, outillé au LOT 301) : 8 pages
# racines, erreurs console/pageerror, /api/client-log, tailles de texte.
# Usage : serveur DEMO lancé (DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 python
# terminal.py, attendre la fin du premier scan via /healthz vertex_ready)
# puis : python docs/refactor/validation/tools/probe_smoke.py
# Références (LOT 300) : / 3371 · /markets 2794 · /opportunities 4679 ·
# /analysis 923 · /portfolio 1609 · /options 2960 · /journal 2676 ·
# /system 4124-4126 (bruit d'horodatage). Écart = à EXPLIQUER, jamais masquer.
import json, urllib.request
from playwright.sync_api import sync_playwright

PAGES = ['/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']
BASE = 'http://127.0.0.1:5002'
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

results = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    pg.on('console', lambda m: errors.append(f'{pg.url} :: {m.text}') if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errors.append(f'{pg.url} :: PAGEERROR {e}'))
    for path in PAGES:
        r = pg.goto(BASE + path, wait_until='domcontentloaded', timeout=30000)
        pg.wait_for_timeout(4500)
        title = pg.title()
        body_len = pg.evaluate('document.body.innerText.length')
        results.append((path, r.status, title[:40], body_len))
    b.close()

print('page | HTTP | titre | taille texte')
for row in results:
    print(' ', row)
print('erreurs console/page :', len(errors))
for e in errors[:10]:
    print('  !', e)

clog = json.load(urllib.request.urlopen(BASE + '/api/client-log'))
print('client-log:', clog)
