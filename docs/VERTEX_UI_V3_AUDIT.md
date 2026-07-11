# Vertex UI V3 — Audit avant refonte Experience OS

Date : 2026-07-11 · Base auditée : interface Master Redesign (8 espaces,
shell unifié, 22 modules graphiques). Captures « avant » :
`docs/redesign/v3-before/{desktop,mobile}/` (8 pages × 1600 px et 390 px).

## 1. Inventaire

- **Pages** : 9 routes (8 espaces + fiche `/analysis/<sym>`), 21 sous-vues,
  3 398 lignes dans `vertex/ui/pages/*.py` + shell
  (`vertex/ui/shell/__init__.py`).
- **CSS** : 9 fichiers, 156 classes `vx-*`. Manquent au périmètre V3 :
  `buttons.css`, `states.css`, `animations.css` (boutons/états/transitions
  vivent dans `components.css`, à scinder).
- **JS** : `vx-core.js` (bus, fetch, états, contexte), `vx-entities.js`
  (entités + sync 17 clés), `vx-shell.js` (sidebar, topbar, palette,
  drawers) ; 22 modules graphiques sur Chart.js unique.
- **Boutons** : matrice complète dans `VERTEX_BUTTON_MATRIX.md` — 0 bouton
  mort (gardien `test_every_button_has_handler`).
- **États vides** : présents partout via `VX.states.*` ; aucun bloc vide
  > 240 px détecté au scan automatisé.

## 2. Constats V3 (ce que la refonte doit changer)

### Direction artistique
1. **Palette actuelle bleu froid** (#050811 / accent #3B82F6) — la V3
   passe en DARK FINANCIAL LUXURY orange/ambre (#f68a3c) avec surfaces
   plus chaudes et halos discrets. Aucune ambiance de fond aujourd'hui
   (fond plat).
2. **Un seul niveau de carte** (`.vx-card`) — pas de hiérarchie
   HERO / ANALYTICAL / COMPACT ; toutes les cartes ont le même poids
   visuel.
3. **Boutons** : 4 variantes seulement (primary/ghost/icon/sm) — pas de
   soft/danger/success/split/loading.
4. **Tabs** : soulignement bleu simple, pas d'indicateur de filtres
   actifs ni de compteur.

### Couleurs hors tokens (à centraliser)
- 7 hex codés en dur dans les pages (`opportunities_page.py` ×4,
  `analysis_page.py` #FFD27A, `performance_page.py` #22D3EE,
  shell #050811 theme-color).
- `chart-core.js` : palette graphique codée en dur (12 hex) — à déplacer
  dans un `chart-theme.js` alimenté par les tokens.

### Bugs de rendu trouvés (corrigés dans cette passe)
1. **`[object Object]` sur /markets** : `sector.leader` est un objet
   `{symbol,score,grade}` rendu tel quel dans deux boutons ticker
   (`markets_page.py:168,268`) → normalisé `leader.symbol`.

### Pages trop vides / disproportions
- **Marchés** : cartes Breadth/volatilité principalement en état vide en
  mode démo — combler avec ce que le scan fournit réellement (indices,
  VIX, secteurs) et réduire la hauteur des refus honnêtes.
- **Intelligence/Analyste** : formulaire seul au-dessus de la ligne de
  flottaison — manque exemples, tickers récents, décisions récentes.
- **Portefeuille** : pas de header synthèse (valeur, coût, P&L déclaré,
  nombre de positions) ; les options sont présentées dans le bloc
  « Gardien/réserve » — V3 exige la séparation Options tactiques.
- **Briefing** : la rangée cross-asset (DXY/pétrole/or/BTC) est un rang
  entier de « n/d » en mode démo — la compacter/regrouper.

### Incohérences
- Espacement vertical hétérogène entre pages (`vx-mb3`/styles inline —
  18 à 21 `style=` par page).
- KPI parfois en `font-size` inline au lieu d'une classe KPI.
- `updateIndicator` absent de quelques cartes secondaires.
- Typo : `tabular-nums` appliqué via `.vx-mono` seulement — pas
  systématique sur les cellules numériques.

### Performance front
- Chart.js chargé sur toutes les pages (OK, mutualisé) ; pas de
  lazy-loading des graphiques hors écran (IntersectionObserver absent) ;
  destruction des instances gérée par le registre `chart-core` (OK).
- Pas d'`AbortController` sur les fetchs de navigation interne (risque
  faible, pages full-reload).

## 3. Ce qui est conservé tel quel (fonctionne et testé)

Navigation 8 espaces + 42 redirections ; `VXEntities` (sync 17 clés,
last-writer-wins, beacon) ; palette ⌘K ; drawers/modales avec focus trap
et Échap ; `VX.states` (logique) ; contrat de carte graphique
(titre/question/conclusion/source/timestamp/« Comprendre ce graphique ») ;
télémétrie `/api/client-log` ; service worker network-first ; 516 tests.

## 4. Plan V3 (phases 2-24)

Tokens orange/ambre avec **alias legacy** (aucune page ne casse pendant la
migration) → base/ambiance → shell (sidebar 7+Système bas, topbar
breadcrumb/état marché/bouton Ajouter brand) → cards 3 niveaux + boutons +
tabs + états premium → thème graphique unifié → 8 pages enrichies →
responsive/accessibilité/perf → tests §39 → docs + rapport final.
