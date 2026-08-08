"""Robustesse des états d'erreur (outillé au LOT 301) : API coupée en vol
→ état honnête ou squelette éternel ?

Par cas : on ABORT une API clé (interception réseau), on charge la page,
on attend 9 s, puis on mesure : squelettes restants, textes d'erreur/vide
honnêtes, textes cassés, erreurs console non liées à l'abort.

Usage : serveur DEMO lancé, puis
    python docs/refactor/validation/tools/probe_error_states.py
Verdict LOT 301 (référence) : 7 cas SAINS — état honnête (« indisponible »,
« ERREUR ») ou résilience par un autre endpoint réel ; 0 squelette éternel.
Fait mesuré : /markets n'appelle PAS /api/market/summary au chargement ;
/opportunities privé de /scan reste complet (le radar vit de /api/command).
"""
import asyncio, json
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:5002'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
CASES = [
    ('/', '**/api/briefing/editorial*'),
    ('/', '**/api/command*'),
    ('/markets', '**/api/market/summary*'),
    ('/opportunities', '**/scan*'),
    ('/system', '**/api/system-status*'),
]


async def main():
    out = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for path, blocked in CASES:
            ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
            page = await ctx.new_page()
            errors = []
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(f'PAGEERROR {e}'))
            await page.route(blocked, lambda route: asyncio.ensure_future(route.abort()))
            await page.goto(BASE + path, wait_until='domcontentloaded')
            await page.wait_for_timeout(9000)
            r = await page.evaluate("""() => {
              const txt = document.body.innerText;
              return {
                skeletons: document.querySelectorAll('.vx-skeleton').length,
                honest: (txt.match(/indisponible|impossible|erreur|Aucune donnée|réessayer|hors ligne/gi) || []).slice(0, 5),
                broken: (txt.match(/\\b(NaN|undefined|null)\\b/g) || []).slice(0, 5),
              };
            }""")
            r['case'] = f'{path} SANS {blocked}'
            # Erreurs console non liées à l'abort volontaire (fetch failed attendu)
            r['unexpectedErrors'] = [e for e in errors if 'Failed to fetch' not in e
                                     and 'ERR_FAILED' not in e and 'NetworkError' not in e][:5]
            out.append(r)
            await ctx.close()
        await b.close()
    print(json.dumps(out, indent=1, ensure_ascii=False))

asyncio.run(main())
