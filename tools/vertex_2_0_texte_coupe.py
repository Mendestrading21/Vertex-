"""Detecte le TEXTE COUPE : un contenu rendu plus large que sa boite.

Sur un ecran financier, un chiffre tronque n est pas un detail de mise en
page : c est une valeur FAUSSE. « 1 234 567 » coupe en « 1 234... » se lit,
et se lit mal. Un libelle coupe se devine ; un nombre coupe, non.

L outil compare, sur la page rendue, la largeur du CONTENU a celle de la
BOITE (`scrollWidth` contre `clientWidth`). Il separe deux cas, parce qu ils
ne se valent pas :

  · **GRAVE** -- l element porte un chiffre (classe monospace, `tabular-nums`,
    ou un texte majoritairement numerique). Une valeur amputee.
  · **A VOIR** -- du texte courant coupe. Genant, rarement mensonger.

Faux positifs ecartes, et c est ce qui rend le relevé utilisable :

  · un conteneur volontairement DEFILANT (`overflow-x:auto/scroll`) -- son
    contenu deborde par construction, l utilisateur peut le faire glisser ;
  · un element hors ecran ou replie (boite nulle) ;
  · un ecart d un pixel, qui vient de l arrondi sub-pixel et ne se voit pas.

Usage :
    python tools/vertex_2_0_texte_coupe.py --routes / /portfolio --largeur 1440
"""
from __future__ import annotations

import argparse

_JS = r"""() => {
  const out = [];
  const c = document.getElementById('vx-content') || document.body;
  const defilant = (e) => {
    let n = e;
    while (n && n !== document.body) {
      const s = getComputedStyle(n);
      if (['auto', 'scroll'].includes(s.overflowX)) return true;
      n = n.parentElement;
    }
    return false;
  };
  c.querySelectorAll('*').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width < 8 || r.height < 4) return;                 // replie ou hors vue
    if (e.children.length) return;                           // on juge les FEUILLES
    const texte = (e.textContent || '').trim();
    if (!texte) return;
    const trop = e.scrollWidth - e.clientWidth;
    if (trop <= 1) return;                                   // arrondi sub-pixel
    const s = getComputedStyle(e);
    if (s.overflow === 'visible' && s.overflowX === 'visible') return;  // ca deborde, ca ne coupe pas
    if (defilant(e)) return;                                 // l utilisateur peut faire glisser
    const cls = String(e.className || '');
    const chiffres = (texte.match(/[0-9]/g) || []).length;
    const numerique = /mono|num|kpi-value|stat-v|metric-v|price|-val/.test(cls)
      || s.fontVariantNumeric.includes('tabular')
      || (chiffres >= 2 && chiffres / texte.length > 0.3);
    out.push({ grave: numerique, texte: texte.slice(0, 38), trop: trop,
               cls: cls.slice(0, 34) || e.tagName.toLowerCase() });
  });
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--largeur', type=int, default=1440)
    ap.add_argument('--wait', type=int, default=2400)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    graves = autres = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(
            viewport={'width': args.largeur, 'height': 1000},
            is_mobile=args.largeur <= 430, has_touch=args.largeur <= 430).new_page()
        for route in args.routes:
            page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            trouve = page.evaluate(_JS)
            g = [t for t in trouve if t['grave']]
            a = [t for t in trouve if not t['grave']]
            graves += len(g); autres += len(a)
            etat = 'OK' if not trouve else '%d chiffre(s) coupe(s), %d texte(s)' % (len(g), len(a))
            print('%-40s %s' % (route, etat))
            for t in g[:5]:
                print('     GRAVE  « %s »  coupe de %d px  (%s)'
                      % (t['texte'], t['trop'], t['cls']))
            for t in a[:3]:
                print('     texte  « %s »  coupe de %d px  (%s)'
                      % (t['texte'], t['trop'], t['cls']))
        nav.close()
    print('\nTOTAL a %d px : %d chiffre(s) coupe(s) · %d texte(s) coupe(s)'
          % (args.largeur, graves, autres))
    return 1 if graves else 0


if __name__ == '__main__':
    raise SystemExit(main())
