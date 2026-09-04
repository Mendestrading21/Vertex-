"""Registre page → widget, et conformité des graphiques au contrat (060, 061).

Ni l'un ni l'autre n'est DÉCLARÉ : les deux sont MESURÉS sur l'application
réellement exécutée. L'outil ouvre chaque sous-vue dans un navigateur, relève
chaque carte de graphique effectivement rendue, et vérifie pour chacune les
cinq champs que le contrat exige.

  question   → `.vx-chart-question`
  conclusion → `.vx-chart-conclusion`
  source     → le pied de carte nomme sa source (jamais « n/d » seul)
  unité      → badge d'unité, ou titre d'axe lu dans l'instance Chart.js
  période    → badge de période / timeframe

L'unité et la période vivent parfois dans les OPTIONS du graphique plutôt que
dans un badge : on interroge alors l'instance Chart.js elle-même, sinon on
déclarerait non conforme une carte qui l'est.

Usage :
    python tools/audit/graphiques.py --base http://127.0.0.1:8099 \
        --out le registre des graphiques (archive, retiree du depot)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Sous-vues à parcourir. Une page dont on ne visite qu'un onglet donnerait un
# registre faussement court.
ROUTES = [
    ('Aujourd’hui', '/'),
    ('Calendrier', '/calendar'),
    ('Marchés · Synthèse', '/markets'),
    ('Marchés · Macro', '/markets?view=macro'),
    ('Marchés · Indices', '/markets?view=indices'),
    ('Marchés · Secteurs', '/markets?view=sectors'),
    ('Marchés · Participation', '/markets?view=breadth'),
    ('Marchés · Volatilité', '/markets?view=volatility'),
    ('Opportunités', '/opportunities'),
    ('Analyse', '/analysis'),
    ('Options · Structure', '/options'),
    ('Options · Volatilité', '/options?view=volatility'),
    ('Options · Positions', '/options?view=positions'),
    ('Simulateur', '/simulator'),
    ('Portefeuille · Synthèse', '/portfolio'),
    ('Portefeuille · Allocation', '/portfolio?view=allocation'),
    ('Portefeuille · Risque', '/portfolio?view=risk'),
    ('Portefeuille · Thèses', '/portfolio?view=theses'),
    ('Suivi', '/follow-up'),
    ('Performance · Synthèse', '/performance'),
    ('Performance · Progression', '/performance?view=progression'),
    ('Performance · Historique', '/performance?view=track-record'),
    ('Vertex IA', '/intelligence'),
    ('Système', '/system'),
]

RELEVE = r"""
() => {
  const out = [];
  document.querySelectorAll('.vx-chart-card').forEach(function (el) {
    const t = (s) => { const n = el.querySelector(s); return n ? n.innerText.trim() : ''; };
    const pied = el.querySelector('.vx-chart-foot');
    const maj = pied ? pied.querySelector('.vx-update') : null;
    const majTexte = maj ? maj.innerText.trim() : '';
    /*  « Source : n/d » et un pied sans source se valent : ni l'un ni l'autre
        ne nomme d'origine. On ne compte que ce qui en nomme une.  */
    const source = /·\s*[^·]+$/.test(majTexte) && !/n\/d/i.test(majTexte)
      ? majTexte.split('·').slice(1).join('·').trim() : '';
    const badges = [...el.querySelectorAll('.vx-chart-head .vx-badge')]
      .map(b => ({ texte: b.innerText.trim(), unite: b.classList.contains('vx-badge-unit') }));
    let unite = badges.filter(b => b.unite).map(b => b.texte).join(' ');
    let periode = badges.filter(b => !b.unite).map(b => b.texte).join(' ');
    /*  L'unité vit souvent dans le TITRE D'AXE plutôt que dans un badge : on
        interroge l'instance Chart.js, sinon une carte conforme serait déclarée
        fautive.  */
    const cv = el.querySelector('canvas');
    if (cv && window.Chart && Chart.getChart) {
      const ch = Chart.getChart(cv);
      const sc = ch && ch.options && ch.options.scales;
      if (sc) {
        const titres = Object.keys(sc)
          .map(k => sc[k] && sc[k].title && sc[k].title.display && sc[k].title.text)
          .filter(Boolean);
        if (!unite && titres.length) unite = 'axe : ' + titres.join(' / ');
      }
    }
    /*  Une table équivalente compte comme lecture alternative du même chiffre.  */
    const table = !!el.querySelector('.vx2-table-equivalente, .vx-chart-tbl');
    out.push({
      titre: t('.vx-chart-title'),
      question: t('.vx-chart-question'),
      conclusion: t('.vx-chart-conclusion'),
      source: source, unite: unite, periode: periode,
      table: table,
      etat: el.querySelector('canvas') ? 'rendu' : 'etat-vide',
    });
  });
  return out;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--out', required=True)
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ap.add_argument('--wait', type=int, default=3200)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    releve: list[tuple[str, str, list[dict]]] = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(viewport={'width': 1440, 'height': 1000}).new_page()
        for nom, route in ROUTES:
            try:
                page.goto(args.base + route, wait_until='domcontentloaded')
                page.wait_for_timeout(args.wait)
                # Déplier : un graphique replié est rendu mais invisible au relevé.
                page.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                page.wait_for_timeout(900)
                cartes = page.evaluate(RELEVE)
            except Exception as exc:  # noqa: BLE001
                cartes = [{'titre': 'RELEVÉ IMPOSSIBLE : %s' % exc, 'question': '',
                           'conclusion': '', 'source': '', 'unite': '', 'periode': '',
                           'table': False, 'etat': 'erreur'}]
            releve.append((nom, route, cartes))
            print('%-28s %2d carte(s)' % (nom, len(cartes)))
        nav.close()

    total = sum(len(c) for _, _, c in releve)
    champs = ('question', 'conclusion', 'source', 'unite', 'periode')
    manques = {f: 0 for f in champs}
    for _, _, cartes in releve:
        for c in cartes:
            for f in champs:
                if not c.get(f):
                    manques[f] += 1

    lignes = [
        '# Registre page → widget, et conformité des graphiques',
        '',
        'Contrôles **060** (registre) et **061** (contrat des graphiques).',
        '',
        'Ni l’un ni l’autre n’est déclaré : les deux sont **mesurés** sur',
        'l’application réellement exécutée, en ouvrant chaque sous-vue dans un',
        'navigateur et en relevant chaque carte effectivement rendue.',
        '',
        '> Un graphique qui ne se rend pas n’apparaît pas ici — et c’est le point :',
        '> un registre écrit à la main aurait listé des cartes mortes comme',
        '> vivantes. Quatre l’étaient encore au lot 14, trois au lot 16.',
        '',
        '## Conformité mesurée',
        '',
        '| Champ du contrat | Cartes qui le portent | Cartes qui ne le portent pas |',
        '|---|---:|---:|',
    ]
    for f in champs:
        lignes.append('| %s | %d | %d |' % (f.capitalize(), total - manques[f], manques[f]))
    lignes += ['', '**%d cartes relevées** sur %d sous-vues.' % (total, len(releve)), '',
               '## Registre par page', '']
    for nom, route, cartes in releve:
        lignes.append('### %s — `%s`' % (nom, route))
        lignes.append('')
        if not cartes:
            lignes += ['_Aucune carte de graphique sur cette sous-vue._', '']
            continue
        lignes.append('| Widget | Question | Source | Unité | Période | Table |')
        lignes.append('|---|---|---|---|---|:-:|')
        for c in cartes:
            def cel(v):
                v = (v or '').replace('|', '/').replace('\n', ' ')
                return (v[:58] + '…') if len(v) > 58 else (v or '—')
            lignes.append('| %s | %s | %s | %s | %s | %s |' % (
                cel(c['titre']), cel(c['question']), cel(c['source']),
                cel(c['unite']), cel(c['periode']), 'oui' if c['table'] else '—'))
        lignes.append('')

    Path(args.out).write_text('\n'.join(lignes) + '\n', encoding='utf-8')
    print('\n%d carte(s) relevée(s) — registre écrit dans %s' % (total, args.out))
    for f in champs:
        print('  %-11s manquant sur %d carte(s)' % (f, manques[f]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
