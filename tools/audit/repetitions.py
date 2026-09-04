"""Détecte les répétitions visibles sur une page (contrôle 039).

« EvidenceZone explique sans répéter. » La règle est facile à écrire et facile
à violer sans s'en apercevoir : un même libellé, une même valeur ou une même
question posée deux fois à trois centimètres d'écart passe inaperçue au relecteur
et saute aux yeux de l'utilisateur.

L'outil relève chaque nœud de texte VISIBLE, normalise, et signale ce qui
apparaît plus d'une fois. Il ignore ce qui se répète LÉGITIMEMENT :

  · les valeurs courtes (« — », « 0 », « n/d ») — l'absence se répète par nature ;
  · les cellules d'une même table, où la répétition est la donnée ;
  · la navigation, présente sur chaque page par construction ;
  · les PIEDS DE CARTE : les règles d'intégrité exigent que chaque valeur porte
    sa source et sa fraîcheur, donc « · scan Différé » sur trois cartes est la
    règle qui s'applique trois fois, pas une redite.

Un signalement n'est donc pas automatiquement une faute : c'est un endroit à
regarder. L'outil ne juge pas, il montre.

Usage :
    python tools/audit/repetitions.py --base http://127.0.0.1:8099 \
        --routes / /markets /portfolio
"""
from __future__ import annotations

import argparse
import re
import sys

RELEVE = r"""
() => {
  /*  Les PIEDS DE CARTE sont exclus a dessein. Les regles d'integrite du
      produit exigent que CHAQUE valeur affichee porte sa source et sa
      fraicheur : « · scan Différé » sur trois cartes n'est pas une redite,
      c'est la regle qui s'applique trois fois. Les compter ferait crier
      l'outil sur la seule chose qu'il faut surtout garder.  */
  const zonesIgnorees = ['nav', 'aside.vx-sidebar', '.vx-sidebar', '.vx2-tabs',
                         'header.vx-topbar', '.vx-topbar', 'table', '.vx2-table',
                         'script', 'style', '.vx-mobilebar',
                         '.vx-chart-foot', '.vx-card-footer', '.vx-update',
                         '.vx2-stamp', '.vx-primitive-foot'];
  const dansZoneIgnoree = (n) => zonesIgnorees.some(s => n.closest && n.closest(s));
  const vu = new Map();
  const marcheur = document.createTreeWalker(
    document.getElementById('vx-content') || document.body,
    NodeFilter.SHOW_TEXT, null);
  let n;
  while ((n = marcheur.nextNode())) {
    const t = (n.textContent || '').replace(/\s+/g, ' ').trim();
    if (t.length < 14) continue;                 // trop court pour conclure
    const p = n.parentElement;
    if (!p || dansZoneIgnoree(p)) continue;
    const r = p.getBoundingClientRect();
    if (!r.width || !r.height) continue;         // invisible
    const cle = t.toLowerCase();
    if (!vu.has(cle)) vu.set(cle, { texte: t, n: 0, ou: [] });
    const e = vu.get(cle);
    e.n += 1;
    e.action = e.action || !!(p.closest('button,a,.vx-btn,.vx2-btn,.vx-chip,.vx2-chip,'
      + '.vx2-badge,.vx-badge,.vx-freshness'));
    if (e.ou.length < 4) {
      /*  Un BOUTON et un BADGE se repetent par nature : chaque etat vide doit
          offrir sa sortie, chaque population porte son etiquette d'etat. La
          regle « expliquer sans repeter » vise le TEXTE EXPLICATIF. On classe
          plutot que d'exclure : le lecteur voit les deux comptes.  */
      const carte = p.closest('.vx2-surface,.vx-card,.vx2-section,section');
      const titre = carte ? (carte.querySelector(
        '.vx2-card-title,.vx-card-title,.vx-chart-title,.vx2-section-title') || {}).innerText : '';
      e.ou.push((titre || '(hors carte)').replace(/\s+/g, ' ').trim().slice(0, 44));
    }
  }
  return [...vu.values()].filter(e => e.n > 1).sort((a, b) => b.n - a.n);
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=3200)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    total = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(viewport={'width': 1440, 'height': 1000}).new_page()
        for route in args.routes:
            page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
            page.wait_for_timeout(700)
            reps = page.evaluate(RELEVE)
            textes = [r for r in reps if not r.get('action')]
            actions = [r for r in reps if r.get('action')]
            total += len(textes)
            print('%-34s %d texte(s) répété(s), %d action/badge (légitimes)'
                  % (route, len(textes), len(actions)))
            for r in textes:
                extrait = r['texte'][:76] + ('…' if len(r['texte']) > 76 else '')
                print('    ×%d  « %s »' % (r['n'], extrait))
                print('         %s' % ' | '.join(r['ou']))
        nav.close()

    print('\nTOTAL : %d texte(s) explicatif(s) répété(s) sur %d route(s)'
          % (total, len(args.routes)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
