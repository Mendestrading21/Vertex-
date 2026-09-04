"""Détecte les CARTES CREUSES : un titre qui promet, un corps qui ne rend rien.

## Pourquoi un outil de plus

`vertex_2_0_etats_vides.py` cherche un **rectangle** vide : un conteneur assez
grand pour se voir, sans texte ni contrôle. Il ne peut pas voir le défaut
suivant, et c'est une limite de sa définition, pas un réglage :

    <section class="vx-card">
      <div class="vx-card-header">Meilleurs contrats (radar)  [Tout voir →]</div>
      <div id="…-body"></div>          ← vidé en silence
    </section>

La carte n'est pas vide — son `innerText` porte le titre. Son corps, lui, fait
0 px de haut, donc il passe sous le seuil de visibilité. Résultat : une carte
qui annonce un contenu, n'en donne aucun, et ne dit pas pourquoi. C'est
exactement ce que le contrat interdit : une absence doit être **nommée**.

L'outil relève donc les cartes dont **tout** le contenu hors en-tête est vide :
pas de texte, pas de graphique, pas de tableau, pas de contrôle.

Faux positifs écartés :

  · un `<details>` replié garde une boîte alors que son texte est masqué ;
  · une carte entièrement invisible (repliée par l'utilisateur, hors vue) —
    le tableau de bord en replie quatre par défaut, et le lui reprocher
    reviendrait à reprocher un défaut à un bloc que personne ne regarde.

Usage :
    python tools/audit/cartes_creuses.py --routes / /options?view=overview
"""
from __future__ import annotations

import argparse

_JS = r"""() => {
  const out = [];
  const c = document.getElementById('vx-content') || document.body;
  const TETE = '.vx-card-header,.vx-chart-head,.vx2-surface-head,.vx2-card-head';
  const PLEIN = 'canvas,svg,img,table,input,select,textarea,button';
  c.querySelectorAll('.vx-card,.vx2-surface').forEach(carte => {
    const r = carte.getBoundingClientRect();
    if (r.height < 24 || r.width < 120) return;          // repliée ou hors vue
    if (carte.closest('details:not([open])')) return;    // fermée, pas creuse
    const tete = carte.querySelector(':scope > ' + TETE);
    if (!tete) return;                                   // sans titre, rien de promis
    let texte = '', riche = false;
    [...carte.children].forEach(enfant => {
      if (enfant === tete) return;
      texte += (enfant.innerText || '').trim();
      if (enfant.matches(PLEIN) || enfant.querySelector(PLEIN)) riche = true;
    });
    if (texte.length || riche) return;
    const titre = (tete.innerText || '').trim().split('\n')[0].slice(0, 46);
    out.push({ titre: titre, id: carte.id || null, h: Math.round(r.height) });
  });
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=2500)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    total = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(viewport={'width': 1440, 'height': 1000}).new_page()
        for route in args.routes:
            page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            trouve = page.evaluate(_JS)
            total += len(trouve)
            print('%-40s %s' % (route, 'OK' if not trouve else '%d creuse(s)' % len(trouve)))
            for t in trouve:
                print('     « %s »  %s · %d px de haut'
                      % (t['titre'], t['id'] or 'sans id', t['h']))
        nav.close()
    print('\nTOTAL : %d carte(s) creuse(s) sur %d route(s)' % (total, len(args.routes)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
