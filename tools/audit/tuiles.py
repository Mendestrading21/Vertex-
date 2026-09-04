"""Mesure que les familles de tuiles historiques rendent LA MÊME tuile.

Le contrôle 048 demande « une famille unique de cartes et MetricCard ». Le
dépôt en porte quatre noms — `vx-kpi`, `vx-stat`, `vx-metric`, `vx-stat-xl` —
et l'audit les a longtemps déclarées « déjà visuellement unifiées ». Elles ne
l'étaient pas : deux fonds, deux filets, deux rayons, et un pixel de
rembourrage d'écart entre `vx-stat` et `vx-metric`.

L'outil injecte le balisage réel des trois tuiles dans une page servie et
compare leurs styles CALCULÉS. Il ne lit pas le CSS : une feuille peut être
écrasée, chargée dans le désordre, ou porter un `!important` qu'on n'avait
pas vu — seul le navigateur dit la vérité.

`vx-stat-xl` est délibérément exclue : ce n'est pas une tuile mais un GRAND
NOMBRE (`-value` + `-label`), sans fond ni filet. La fusionner reviendrait à
inventer une équivalence qui n'existe pas.

Usage :
    python tools/audit/tuiles.py --route '/portfolio?view=positions'
"""
from __future__ import annotations

import argparse

_PROPS = ('backgroundColor', 'backgroundImage', 'borderTopWidth', 'borderTopColor',
          'borderRadius', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight',
          'boxShadow', 'display', 'gap')

_JS = r"""(props) => {
  const hote = document.getElementById('vx-content');
  const bac = document.createElement('div');
  bac.innerHTML =
    '<div class="vx-card vx-kpi"><div class="vx-kpi-label">Libelle</div>'
      + '<div class="vx-kpi-value">12,3</div></div>'
    + '<div class="vx-stat"><div class="vx-stat-k">Libelle</div>'
      + '<div class="vx-stat-v">12,3</div></div>'
    + '<div class="vx-metric"><span class="vx-metric-k">Libelle</span>'
      + '<span class="vx-metric-v">12,3</span></div>';
  hote.appendChild(bac);
  const lire = (sel) => { const e = bac.querySelector(sel); if (!e) return null;
    const s = getComputedStyle(e); const o = {}; props.forEach(p => o[p] = s[p]); return o; };
  const typo = (sel) => { const e = bac.querySelector(sel); if (!e) return null;
    const s = getComputedStyle(e);
    return { taille: s.fontSize, graisse: s.fontWeight, couleur: s.color,
             casse: s.textTransform, chiffres: s.fontVariantNumeric }; };
  const r = {
    surfaces: { kpi: lire('.vx-kpi'), stat: lire('.vx-stat'), metric: lire('.vx-metric') },
    libelles: { kpi: typo('.vx-kpi-label'), stat: typo('.vx-stat-k'),
                metric: typo('.vx-metric-k') },
    valeurs:  { kpi: typo('.vx-kpi-value'), stat: typo('.vx-stat-v'),
                metric: typo('.vx-metric-v') },
  };
  bac.remove();
  return r;
}"""


def _ecarts(bloc, ignorer=()):
    noms = list(bloc)
    ref = bloc[noms[0]] or {}
    out = []
    for cle in ref:
        if cle in ignorer:
            continue
        vals = {n: (bloc[n] or {}).get(cle) for n in noms}
        if len(set(vals.values())) > 1:
            out.append((cle, vals))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:8099')
    ap.add_argument('--route', default='/portfolio?view=positions')
    ap.add_argument('--exe', default='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=args.exe)
        page = nav.new_context(viewport={'width': 1440, 'height': 1000}).new_page()
        page.goto(args.base + args.route, wait_until='domcontentloaded')
        page.wait_for_timeout(2500)
        r = page.evaluate(_JS, list(_PROPS))
        nav.close()

    faute = 0
    for titre, bloc, ignorer in (
            ('Surface', r['surfaces'], ()),
            ('Libellé', r['libelles'], ()),
            # La taille du chiffre est le SEUL écart voulu : compacte, courante,
            # forte. Tout le reste de sa typographie doit concorder.
            ('Chiffre', r['valeurs'], ('taille',))):
        ecarts = _ecarts(bloc, ignorer)
        print('%-9s %s' % (titre, 'identique' if not ecarts else '%d écart(s)' % len(ecarts)))
        for cle, vals in ecarts:
            faute += 1
            print('     %-18s %s' % (cle, ' | '.join('%s=%s' % kv for kv in vals.items())))
    tailles = {n: (v or {}).get('taille') for n, v in r['valeurs'].items()}
    print('\nTailles de chiffre assumées : ' + ' · '.join('%s %s' % kv for kv in tailles.items()))
    print('TOTAL : %d écart(s) non voulu(s)' % faute)
    return 1 if faute else 0


if __name__ == '__main__':
    raise SystemExit(main())
