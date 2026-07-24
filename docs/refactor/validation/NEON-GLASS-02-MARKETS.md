# Validation — NEON GLASS 02 : Migration « Marchés »

> Issue #14, 2ᵉ espace. Marchés adopte le langage **Neon Glass** validé sur
> Aujourd'hui, en gardant son rôle : « **Le vent est-il dans le dos ou de face ?** »
> Branche `agent/vertex-neon-glass-graphs`. **Aucun moteur, aucune donnée, aucun
> calcul modifié. READONLY intact. Les 6 autres espaces ne sont PAS touchés.**

## 1. Fichiers modifiés

- `vertex/static/vertex/css/neon-glass.css` — **scope étendu** à Marchés
  (`.vx-content:is([data-space="briefing"],[data-space="markets"])`) + **polish
  Marchés** (onglet actif orange néon, conteneurs de graphes en verre, jauges sobres,
  point actif RRG = glow réservé, lisibilité heatmap, rails en verre, sparklines KPI).
- `vertex/ui/shell/__init__.py` — inchangé depuis NG-01 (le hook `data-space` existait
  déjà ; aucun code Marchés touché).
- `vertex/app/routes/system.py` — service worker `v51 → v52` (visuel Marchés modifié).
- `tests/test_neon_glass_01.py` — gardiens mis à jour (scope = briefing **+ markets** ;
  les 6 autres espaces restent hors scope) + gardiens SW v52.

**Aucune ligne de `markets_page.py` modifiée** : la migration est purement visuelle
(CSS scopé), les moteurs/données/graphes restent identiques.

## 2. Vues migrées (5)

Vue d'ensemble · Macro · Secteurs · Breadth (participation) · Volatilité — toutes
rendues en glass premium, chacune conservant sa **question principale**, sa
**conclusion**, sa **source/période/unité/fraîcheur** et ses **états honnêtes**
(contrat `C.card` intact). *(La vue « Cross-asset » n'existe pas comme onglet distinct
dans l'implémentation actuelle : taux/DXY/or/pétrole/BTC vivent dans Macro & Vue
d'ensemble — voir §Éléments différés.)*

## 3. Graphes avant / après

| Élément | Avant | Après | Note |
|---|---|---|---|
| Nombre de graphes Marchés | **13** | **13** | migration **visuelle** : aucun graphe supprimé ni ajouté (pas de big-bang) |
| Traitement visuel | thème obsidian copper | **glass premium neon** (fond bleuté, bord cuivre, identité orange) | |
| RRG (`vx-mk-rotation`) | scatter quadrants | **quadrants lisibles + point actif glow-on-select + tooltip verre** | conclusion conservée |
| Heatmap secteurs | table-heat | **texte renforcé (ombre) + piste sobre** | lisible à 390 px |
| Jauges (régime/breadth/VIX) | 3 jauges | **conteneurs sobres, bande sémantique conservée** | consolidation différée (cf. §9) |

> La convergence des **~41 graphes → ~15 primitives** (jauge unique, timeline unique,
> etc. — cf. `VERTEX_NEON_GLASS_GRAPH_AUDIT.md`) est un chantier **structurel** volontai-
> rement différé : il touche le JS des pages et sera fait après validation, espace par
> espace, avec tests. Ici on **habille** l'existant sans le recréer (règle « ne pas
> créer de nouveau graphe si un composant existant peut être migré »).

## 4. Composants réutilisés

`neon-glass.css` (tokens fond bleuté, surfaces glass, bordures cuivre, identité orange
néon, variantes de carte, états, motion) — **aucun nouveau composant**. Polish Marchés =
règles CSS scopées sur les ids/classes existants (`[id^="vx-mk-"]`, `[id$="-gauge"]`,
`.vx-mk-rotation`, `.vx-tab`, rails, sparkSvg). Onglet actif = accent orange néon.

## 5. Responsive (mesuré : 390 / 768 / 1440 / 1920)

Sweep Playwright sur **5 vues × 4 viewports = 20 combinaisons** :

| Viewport | Débordement réel | Erreurs console applicatives |
|---|---|---|
| 390 | **0 px** | 0 |
| 768 | **0 px** | 0 |
| 1440 | **0 px** | 0 |
| 1920 | **0 px** | 0 |

**20/20 propres.** Tableaux larges = scroll intentionnel ; RRG et heatmap lisibles à
390 px. Captures : `scratchpad/neon2shots/mk-{overview,sectors,volatility}.png`.

## 6. Console

**0 erreur applicative** sur les 20 combinaisons (hors `ERR_CONNECTION_RESET` Google
Fonts, non applicatif).

## 7. Tests

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **958 passed, 2 skipped**.
- Gardiens neon-glass (8) mis à jour : scope = briefing **+ markets** ; les 6 espaces
  non migrés (opportunities/analysis/portfolio/options/journal/system) **absents** du
  scope CSS (preuve anti-big-bang) ; identité orange néon **sans bleu** ; glass premium ;
  glow live/hover uniquement ; reduced-motion ; READONLY intact. SW v52 (vN présent,
  v(N-1) absent).

## 8. Captures

`mk-overview.png`, `mk-sectors.png` (RRG + leaders glass), `mk-volatility.png` — desktop
1440@2x. Vérifié : fond bleuté, cartes glass à bord cuivre, onglet actif orange néon,
RRG quadrants lisibles + dots sémantiques (corail = secteurs faibles), tickers orange,
DÉMO glass, sémantiques respectées (vert/rouge/ambre), **aucun bleu identitaire, aucun
glow permanent**.

## 9. Risques

- Migration **visuelle** (CSS scopé) : robuste et réversible, mais elle **ne réduit pas
  encore le nombre de graphes** ni ne consolide les 7 jauges / 3 timelines / 2 quadrants.
  Risque faible (aucun changement de données/JS), mais l'objectif « limiter les jauges »
  n'est que partiellement atteint (jauges sobrisées, pas supprimées).
- `backdrop-filter` : léger coût GPU sur very-low-end ; `--ng-blur` réduit à 10px ≤768.
- Validation Chromium **headless** (pas d'appareil physique).

## 10. Éléments différés (après validation, migration structurelle)

- **Consolidation des graphes** Marchés vers les primitives canoniques : jauge unique
  (régime/breadth/VIX), timeline unique (macro-cal), suppression des doublons
  inter-pages (funnel, quadrant) — nécessite du JS, fait espace par espace avec tests.
- **Cross-asset** dédié (taux/DXY/or/pétrole/BTC/corrélations) : à structurer en vue
  propre si souhaité (aujourd'hui réparti dans Macro/Vue d'ensemble).
- **Term structure / skew** volatilité : seulement si données réellement disponibles
  (sinon carte sobre — aucune donnée inventée).
- **Chart Shell V2 sur canvas** (tooltip verre natif Chart.js, légendes/axes V2) : la
  couche CSS pose le langage ; le thème Chart.js sera adapté à la migration structurelle.

## Verdict

**Marchés migré en Neon Glass** au niveau de qualité du prototype Aujourd'hui : glass
premium, identité orange néon, sémantiques et états honnêtes préservés, RRG/heatmap/
volatilité lisibles. **958 tests verts · 20/20 combinaisons sans débordement ni erreur
console · READONLY intact · aucun bleu identitaire · aucune donnée modifiée.** **Arrêt
pour validation humaine avant Opportunités.**
