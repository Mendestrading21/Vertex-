"""Détecte les BLOCS VIDES réellement servis par Vertex.

La doctrine visuelle interdit le rectangle vide : un conteneur visible, de
taille non négligeable, qui ne porte ni texte, ni graphique, ni contrôle. Un
squelette qui ne se résout jamais entre dans cette catégorie — il promet une
donnée qui n'arrivera pas.

Deux faux positifs ont dû être écartés, et c'est ce qui rend l'outil utilisable :

  · le contenu d'un `<details>` REPLIÉ garde une boîte de mise en page dans
    Chromium alors que `innerText` rend `''`. Ce n'est pas un bloc vide, c'est
    un bloc fermé ;
  · un conteneur transparent SANS bordure ne se voit pas : c'est de l'espace,
    pas un rectangle.

Usage :
    python tools/audit/etats_vides.py --base http://127.0.0.1:8099
"""
from __future__ import annotations

import argparse
import json
import sys

ROUTES = ('/', '/calendar', '/markets', '/opportunities', '/analysis', '/options',
          '/simulator', '/portfolio', '/follow-up', '/performance',
          '/intelligence', '/system', '/design-system')

_JS = """() => {
  const out = [];
  const ferme = el => el.closest('details:not([open])') !== null;
  document.querySelectorAll('#vx-content div, #vx-content section, #vx-content aside')
    .forEach(el => {
      const r = el.getBoundingClientRect();
      // 48 px et non 70 : un squelette de 60 px de haut est parfaitement
      // visible, et c'est exactement ce qui avait échappé à la première passe.
      if (r.width < 180 || r.height < 48) return;
      if (ferme(el)) return;                       // repli, pas vide
      if ((el.innerText || '').trim().length > 0) return;
      const squeletteSeul = el.querySelector('.vx-skeleton, .vx2-skeleton')
        && !(el.innerText || '').trim();
      if (!squeletteSeul && el.querySelector('canvas, svg, img, table, input, button, a')) return;
      const st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden' || st.opacity === '0') return;
      const bg = st.backgroundColor;
      const invisible = (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')
        && st.borderTopWidth === '0px' && st.borderLeftWidth === '0px';
      if (invisible) return;                       // espace, pas rectangle
      out.push({
        tag: el.tagName.toLowerCase(), id: el.id || null,
        cls: String(el.className).slice(0, 70),
        w: Math.round(r.width), h: Math.round(r.height),
      });
    });
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--routes', nargs='*', default=list(ROUTES))
    ap.add_argument('--json', default='')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    total, rapport = 0, {}
    with sync_playwright() as pw:
        kw = {}
        import os
        if os.path.exists(args.exe):
            kw['executable_path'] = args.exe
        b = pw.chromium.launch(**kw)
        ctx = b.new_context(viewport={'width': 1440, 'height': 1000}, locale='fr-FR')
        page = ctx.new_page()
        for route in args.routes:
            page.goto(args.base + route, wait_until='networkidle', timeout=45000)
            page.wait_for_timeout(2600)
            vides = page.evaluate(_JS)
            rapport[route] = vides
            total += len(vides)
            print(f'{route:<18} {len(vides)} bloc(s) vide(s)')
            for v in vides:
                print(f"    {v['tag']}#{v['id']} .{v['cls'][:48]} {v['w']}x{v['h']}")
        ctx.close(); b.close()

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
    print(f'\nTOTAL : {total} bloc(s) vide(s) sur {len(args.routes)} routes')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
