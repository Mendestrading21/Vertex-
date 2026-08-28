"""Mesure les espacements et la mise en page (rythme vertical, alignements).

## Pourquoi cet outil

Les contrôles existants attrapent le grave — un débordement, un bloc vide, un
contraste insuffisant. Ils ne voient pas ce qui rend une page *fatigante* : un
rythme vertical incohérent, deux cartes voisines qui ne s'alignent pas, une
marge écrite en dur au lieu d'un jeton, un titre collé à son contenu.

L'outil relève, sur la page RÉELLEMENT rendue :

  1. **Rythme vertical** — les écarts entre sections consécutives. Un produit
     cohérent en utilise trois ou quatre, pas quinze.
  2. **Alignements rompus** — deux cartes de la même rangée dont les bords
     gauches ou droits diffèrent de plus d'un pixel.
  3. **Espacements en dur** — `margin`/`padding` posés en style *inline*, qui
     échappent aux jetons `--vx2-s*` et dérivent page après page.
  4. **Titres collés** — un titre de section à moins de 8 px de son contenu.
  5. **Rangées orphelines** — une grille dont la dernière rangée n'a qu'un
     élément très étiré, signe d'un `auto-fit` mal borné.

Aucun de ces relevés n'est une faute automatique : ce sont des endroits à
regarder. L'outil montre, il ne juge pas.
"""
from __future__ import annotations

import argparse
import json
import sys

RELEVE = r"""
() => {
  const R = { rythme: {}, alignements: [], durs: [], colles: [], orphelines: [] };
  const contenu = document.getElementById('vx-content') || document.body;
  const px = (v) => Math.round(parseFloat(v) || 0);

  /* 1. Rythme vertical : écarts entre frères de premier niveau. */
  const enfants = [...contenu.children].filter(e => e.getBoundingClientRect().height > 4);
  for (let i = 1; i < enfants.length; i++) {
    const a = enfants[i - 1].getBoundingClientRect(), b = enfants[i].getBoundingClientRect();
    const d = Math.round(b.top - a.bottom);
    if (d >= 0 && d < 200) R.rythme[d] = (R.rythme[d] || 0) + 1;
  }

  /* 2. Alignements : cartes d'une même rangée aux bords décalés. */
  const cartes = [...contenu.querySelectorAll('.vx2-surface,.vx-card,.vx2-these,.vx2-population')]
    .filter(e => e.getBoundingClientRect().height > 20);
  const rangees = new Map();
  cartes.forEach(e => {
    const r = e.getBoundingClientRect();
    const cle = Math.round(r.top / 8) * 8;
    (rangees.get(cle) || rangees.set(cle, []).get(cle)).push({ e, r });
  });
  rangees.forEach((liste) => {
    if (liste.length < 2) return;
    const tops = liste.map(x => Math.round(x.r.top));
    const bas = liste.map(x => Math.round(x.r.bottom));
    if (Math.max(...tops) - Math.min(...tops) > 1)
      R.alignements.push({ quoi: 'bords hauts', ecart: Math.max(...tops) - Math.min(...tops),
                           n: liste.length });
    if (Math.max(...bas) - Math.min(...bas) > 1)
      R.alignements.push({ quoi: 'bords bas', ecart: Math.max(...bas) - Math.min(...bas),
                           n: liste.length });
  });

  /* 3. Espacements en dur : style inline qui échappe aux jetons. */
  contenu.querySelectorAll('[style]').forEach(e => {
    if (!e.getBoundingClientRect().height) return;
    const s = e.getAttribute('style') || '';
    const m = s.match(/(?:^|;)\s*(margin|padding)(-top|-bottom|-left|-right)?\s*:\s*([^;]+)/g);
    if (!m) return;
    m.forEach(decl => {
      if (/var\(/.test(decl) || /:\s*0\b/.test(decl) || /auto/.test(decl)) return;
      R.durs.push({ ou: (e.className || e.tagName).toString().slice(0, 44),
                    decl: decl.replace(/^;/, '').trim().slice(0, 46) });
    });
  });

  /* 4. Titres collés à leur contenu.

     Un élément replié rend une boîte à zéro : `top` et `bottom` valent 0, et
     l'écart calculé vaut 0 lui aussi. Le mesurer reviendrait à reprocher un
     défaut de mise en page à un bloc que l'utilisateur a choisi de ne pas
     voir — le tableau de bord en replie quatre par défaut. On n'inspecte
     donc que ce qui occupe réellement de la place. */
  const visible = (e) => { const r = e.getBoundingClientRect();
                           return r.height > 0 && r.width > 0; };
  contenu.querySelectorAll('.vx2-section-title,.vx2-card-title,.vx-card-title,h2,h3')
    .forEach(t => {
      const suivant = t.parentElement && t.parentElement.nextElementSibling;
      if (!suivant || !visible(t) || !visible(suivant)) return;
      const a = t.getBoundingClientRect(), b = suivant.getBoundingClientRect();
      const d = Math.round(b.top - a.bottom);
      if (d >= 0 && d < 8)
        R.colles.push({ titre: (t.innerText || '').trim().slice(0, 40), ecart: d });
    });

  /* 5. Rangée orpheline : dernier élément d'une grille, très étiré. */
  contenu.querySelectorAll('.vx2-strip,.vx2-theses,.vx2-populations,.vx-grid').forEach(g => {
    const kids = [...g.children].filter(e => e.getBoundingClientRect().width > 10);
    if (kids.length < 3) return;
    const larg = kids.map(e => Math.round(e.getBoundingClientRect().width));
    const der = larg[larg.length - 1], typique = larg[0];
    if (der > typique * 1.9)
      R.orphelines.push({ grille: (g.className || '').toString().slice(0, 40),
                          n: kids.length, largeur: der, typique: typique });
  });
  return R;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--routes', nargs='+', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=3000)
    ap.add_argument('--largeur', type=int, default=1440)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    rythmes: dict[int, int] = {}
    total = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(viewport={'width': args.largeur, 'height': 1000}).new_page()
        for route in args.routes:
            page.goto(args.base + route, wait_until='domcontentloaded')
            page.wait_for_timeout(args.wait)
            r = page.evaluate(RELEVE)
            for k, v in (r['rythme'] or {}).items():
                rythmes[int(k)] = rythmes.get(int(k), 0) + v
            n = len(r['alignements']) + len(r['durs']) + len(r['colles']) + len(r['orphelines'])
            total += n
            print('%-38s %s' % (route, 'OK' if not n else '%d relevé(s)' % n))
            for a in r['alignements'][:3]:
                print('     alignement : %s, écart %d px sur %d cartes'
                      % (a['quoi'], a['ecart'], a['n']))
            for d in r['durs'][:4]:
                print('     espacement en dur : %-44s dans %s' % (d['decl'], d['ou']))
            for c in r['colles'][:3]:
                print('     titre collé : « %s » à %d px de son contenu' % (c['titre'], c['ecart']))
            for o in r['orphelines'][:2]:
                print('     rangée orpheline : %s — %d px contre %d typiques'
                      % (o['grille'], o['largeur'], o['typique']))
        nav.close()

    print('\n── Rythme vertical, toutes routes confondues ──')
    for ecart, n in sorted(rythmes.items(), key=lambda x: -x[1])[:12]:
        print('   %4d px  ×%d' % (ecart, n))
    distincts = len([e for e, n in rythmes.items() if n >= 2])
    print('   %d écart(s) distinct(s) utilisés au moins deux fois' % distincts)
    print('\nTOTAL : %d relevé(s) sur %d route(s)' % (total, len(args.routes)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
