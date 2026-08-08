"""Performance perçue (outillé au LOT 304) : DCL + temps avant contenu
utile, 8 pages racines.

Par page : DOMContentLoaded (Navigation Timing), puis échantillonnage
toutes les 250 ms du nombre de squelettes visibles et de la taille de
texte — le « temps avant contenu utile » = 1er échantillon où le texte
dépasse 60 % de sa valeur finale ET 0 squelette visible.

Usage : serveur DEMO lancé (attendre vertex_ready via /healthz), puis
    python docs/refactor/validation/tools/probe_perceived_perf.py
NOTE : la TOUTE première page mesurée paie le froid (serveur + premier
lancement navigateur) — re-mesurer isolément avant de conclure.

Baselines : DCL < 300 ms (lot 72) — mesuré lot 304 : 264-341 ms.
Contenu utile (lot 304, PREMIÈRE référence) : / 957 · /markets 1055 ·
/opportunities 625 · /analysis 363 · /portfolio 362 · /options 641 ·
/journal 597 · /system 682 ms ; 0 squelette visible à 1 s partout.
"""
import asyncio, json
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:5002'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
PAGES = ['/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']


async def main():
    out = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for path in PAGES:
            ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
            page = await ctx.new_page()
            await page.goto(BASE + path, wait_until='domcontentloaded')
            samples = []
            for i in range(28):  # 7 s
                s = await page.evaluate("""() => ({
                  t: Math.round(performance.now()),
                  skel: [...document.querySelectorAll('.vx-skeleton')].filter(e => e.getBoundingClientRect().width > 0).length,
                  txt: document.body.innerText.length,
                })""")
                samples.append(s)
                await page.wait_for_timeout(250)
            nav = await page.evaluate("""() => {
              const e = performance.getEntriesByType('navigation')[0];
              return {dcl: Math.round(e.domContentLoadedEventEnd), load: Math.round(e.loadEventEnd)};
            }""")
            final_txt = samples[-1]['txt']
            useful = next((s['t'] for s in samples if s['txt'] >= 0.6 * final_txt and s['skel'] == 0), None)
            out[path] = {'dcl_ms': nav['dcl'], 'load_ms': nav['load'],
                         'useful_ms': useful, 'final_txt': final_txt,
                         'skel_at_1s': next((s['skel'] for s in samples if s['t'] >= 1000), None)}
            await ctx.close()
        await b.close()
    print(json.dumps(out, indent=1, ensure_ascii=False))

asyncio.run(main())
