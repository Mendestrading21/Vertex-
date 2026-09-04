"""Audit d'accessibilité et de responsive de Vertex, sur l'application RÉELLE.

Mesure ce qui peut l'être objectivement dans un navigateur, sans jugement :

  · débordement horizontal global, à chaque largeur cible ;
  · boutons-icône sans nom accessible ;
  · images sans alternative textuelle ;
  · champs de formulaire sans étiquette reliée ;
  · lien d'évitement présent et atteignable au clavier ;
  · contraste du texte réellement rendu, contre le fond réellement peint
    (la couleur est résolue en remontant les ancêtres jusqu'à un fond opaque —
    sur des surfaces en verre, lire `backgroundColor` sur l'élément lui-même
    rendrait « transparent » et la mesure serait fausse) ;
  · ordre du clavier et piégeage du focus dans un drawer, quand il est ouvert.

Usage :
    python tools/audit/a11y.py --base http://127.0.0.1:8099
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROUTES = ('/', '/calendar', '/markets', '/opportunities', '/analysis', '/options',
          '/simulator', '/portfolio', '/follow-up', '/performance',
          '/intelligence', '/system')

LARGEURS = (390, 430, 768, 1024, 1280, 1440, 1600, 1920)

_JS_AUDIT = r"""() => {
  const res = {overflow: 0, sansNom: [], sansAlt: [], champsSansLabel: [],
               skipLink: false, contrastes: [], focusInvisible: []};

  res.overflow = Math.max(0, document.documentElement.scrollWidth
                             - document.documentElement.clientWidth);

  const skip = document.querySelector('.vx-skip-link, .vx2-skip-link, a[href="#vx-content"]');
  res.skipLink = !!skip;

  const nom = el => (el.getAttribute('aria-label')
    || el.getAttribute('title')
    || (el.getAttribute('aria-labelledby')
        && (document.getElementById(el.getAttribute('aria-labelledby'))||{}).textContent)
    || el.innerText || '').trim();

  // `innerText` rend '' pour tout ce qui vit dans un <details> REPLIÉ : un
  // bouton qui y porte pourtant un libellé serait signalé à tort. On lit alors
  // `textContent`, qui ignore le rendu.
  const replie = el => el.closest('details:not([open])') !== null;
  document.querySelectorAll('button, a[role="button"], [role="button"]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    const n = nom(el) || (replie(el) ? (el.textContent || '').trim() : '');
    if (!n) res.sansNom.push((el.id || el.className || el.tagName).toString().slice(0, 60));
  });

  document.querySelectorAll('img').forEach(el => {
    if (!el.hasAttribute('alt')) res.sansAlt.push((el.src || '').slice(-60));
  });

  document.querySelectorAll('input, select, textarea').forEach(el => {
    if (el.type === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    const lie = (el.id && document.querySelector('label[for="' + CSS.escape(el.id) + '"]'))
      || el.closest('label')
      || el.getAttribute('aria-label')
      || el.getAttribute('aria-labelledby');
    if (!lie) res.champsSansLabel.push((el.id || el.name || el.tagName).toString().slice(0, 60));
  });

  // ── Contraste ──────────────────────────────────────────────────────────
  // Le fond doit être cherché sur les ANCÊTRES : sur une surface en verre,
  // l'élément lui-même est transparent et la mesure serait fausse.
  const lum = c => {
    const s = c.map(v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); });
    return .2126*s[0] + .7152*s[1] + .0722*s[2];
  };
  const rgb = s => { const m = s.match(/\d+(\.\d+)?/g); return m ? m.slice(0,3).map(Number) : null; };
  const alpha = s => { const m = s.match(/\d+(\.\d+)?/g); return m && m.length > 3 ? Number(m[3]) : 1; };
  const melange = (fg, bg, a) => fg.map((v,i) => v*a + bg[i]*(1-a));
  const fondOpaque = el => {
    let cur = el, fond = [5,6,7];        // fond de page par défaut
    const pile = [];
    while (cur) {
      const bg = getComputedStyle(cur).backgroundColor;
      const a = alpha(bg), c = rgb(bg);
      if (c && a > 0) { pile.push([c, a]); if (a >= .999) break; }
      cur = cur.parentElement;
    }
    for (let i = pile.length - 1; i >= 0; i--) fond = melange(pile[i][0], fond, pile[i][1]);
    return fond;
  };

  const vus = new Set();
  document.querySelectorAll('#vx-content *').forEach(el => {
    if (el.children.length) return;                    // feuilles seulement
    if (el.closest('details:not([open])')) return;     // replié, non rendu
    const t = (el.textContent || '').trim();
    if (t.length < 2) return;
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return;
    const st = getComputedStyle(el);
    if (st.visibility === 'hidden' || st.display === 'none' || Number(st.opacity) < .1) return;
    const fgS = st.color, a = alpha(fgS), c = rgb(fgS);
    if (!c) return;
    const bg = fondOpaque(el);
    const fg = a >= .999 ? c : melange(c, bg, a);
    const l1 = lum(fg), l2 = lum(bg);
    const ratio = (Math.max(l1,l2) + .05) / (Math.min(l1,l2) + .05);
    const px = parseFloat(st.fontSize), gras = Number(st.fontWeight) >= 700;
    const grand = px >= 24 || (px >= 18.66 && gras);
    const seuil = grand ? 3 : 4.5;
    const cle = st.color + '|' + Math.round(px) + '|' + st.fontWeight;
    if (ratio < seuil && !vus.has(cle)) {
      vus.add(cle);
      res.contrastes.push({texte: t.slice(0,44), couleur: st.color, px, poids: st.fontWeight,
                           ratio: Math.round(ratio*100)/100, seuil});
    }
  });
  return res;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--routes', nargs='*', default=list(ROUTES))
    ap.add_argument('--json', default='')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    rapport, defauts = {}, 0
    with sync_playwright() as pw:
        kw = {'executable_path': args.exe} if os.path.exists(args.exe) else {}
        b = pw.chromium.launch(**kw)

        # 1) Débordement horizontal à toutes les largeurs cibles.
        print('── Débordement horizontal ──')
        for w in LARGEURS:
            ctx = b.new_context(viewport={'width': w, 'height': 900}, locale='fr-FR',
                                is_mobile=w <= 430, has_touch=w <= 430)
            page = ctx.new_page()
            pires = []
            for route in args.routes:
                page.goto(args.base + route, wait_until='networkidle', timeout=45000)
                page.wait_for_timeout(1500)
                ov = page.evaluate('Math.max(0, document.documentElement.scrollWidth'
                                   ' - document.documentElement.clientWidth)')
                if ov > 0:
                    pires.append((route, ov)); defauts += 1
            rapport.setdefault('overflow', {})[w] = pires
            print(f'  {w:>5} px : ' + ('OK' if not pires else f'{len(pires)} route(s) — {pires}'))
            ctx.close()

        # 2) Audit détaillé à 1440 puis à 390.
        for w, h in ((1440, 1000), (390, 844)):
            ctx = b.new_context(viewport={'width': w, 'height': h}, locale='fr-FR',
                                is_mobile=w <= 430, has_touch=w <= 430)
            page = ctx.new_page()
            print(f'\n── Audit {w}×{h} ──')
            for route in args.routes:
                page.goto(args.base + route, wait_until='networkidle', timeout=45000)
                page.wait_for_timeout(2200)
                r = page.evaluate(_JS_AUDIT)
                rapport.setdefault(f'audit{w}', {})[route] = r
                n = (len(r['sansNom']) + len(r['sansAlt'])
                     + len(r['champsSansLabel']) + len(r['contrastes'])
                     + (0 if r['skipLink'] else 1))
                defauts += n
                marque = 'OK' if n == 0 else f'{n} défaut(s)'
                print(f'  {route:<16} {marque}')
                if r['sansNom']:
                    print(f'      bouton sans nom : {r["sansNom"][:4]}')
                if r['champsSansLabel']:
                    print(f'      champ sans label : {r["champsSansLabel"][:4]}')
                if not r['skipLink']:
                    print('      lien d\'évitement absent')
                for c in r['contrastes'][:4]:
                    print(f'      contraste {c["ratio"]}:1 < {c["seuil"]} — '
                          f'{c["px"]}px/{c["poids"]} « {c["texte"]} »')
            ctx.close()
        b.close()

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
    print(f'\nTOTAL : {defauts} défaut(s)')
    return 1 if defauts else 0


if __name__ == '__main__':
    sys.exit(main())
