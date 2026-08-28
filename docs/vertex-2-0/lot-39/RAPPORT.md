# Lot 39 — Le bundle CSS servi est minifié (chaîne critique du LCP)

## Problème

Re-mesure Lighthouse post-lot 38 (accueil, émulation mobile) : **perf 63 —
sous le budget ≥ 65 du contrôle 131** — avec « unminified-css : 66 KiB »
directement sur la chaîne critique. Le bundle (lot 30) est une seule requête,
mais transporte commentaires et indentation de 19 feuilles.

## Changement

`_minifier_css()` dans vertex/app/routes/system.py, appliqué feuille par
feuille à l'assemblage mémoire du bundle. Minification CONSERVATRICE :
- chaînes préservées caractère à caractère (gardées hors des regex) ;
- `calc()` intact (jamais toucher `+`/`-`) ;
- combinateurs de sélecteurs (`a > b`, `a b`) : l'espace unique reste ;
- suppression : commentaires, blancs autour de `{` `}` `;` `,`, `;}` ;
- les 19 marqueurs `/* ═ bundle: nom ═ */` restent (sommaire + contrat
  lot 30). Les feuilles individuelles sur disque ne changent PAS
  (développement, bancs, rollback).

SW **v279** (le bundle est précaché).

## Preuves

- Bundle servi : **211 266 → 141 033 octets (−33 %)**.
- Lighthouse accueil (même banc, mêmes flags) : perf **63 → 65**, FCP
  **3,0 → 2,7 s**, LCP **7,7 → 7,3 s**, audit unminified-css soldé, CLS 0.
- Parité visuelle : styles calculés échantillonnés avant/après identiques
  (.vx-card, .vx-btn, .vx-badge sur 4 pages), débordement 0, console vide.
- Bancs nés rouges 6/6 (cas pièges unitaires du minifieur : chaînes avec
  `/*`, calc, combinateurs, media queries + bundle servi sans commentaire
  et < 75 % du brut). Suite : **4423 passés · 152 ignorés · 0 échec**.

## Rollback

git revert — l'assemblage retourne au brut, aucune donnée en jeu.
