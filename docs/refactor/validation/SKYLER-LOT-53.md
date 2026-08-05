# SKYLER V2 — LOT 53 : sparkline / bars / donut sur la signature 2026

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-53-charts-polish`
(base : `integration/vertex-skyler-v2` @ `a474878`, fraîchement fetchée) ·
Mode : développement, axe VISUEL (direction utilisateur « plus plus plus 2026 »).

## 1. Justification du choix de lot

Suite directe des lots 51 (aires) et 52 (crosshair + multiLine). Les trois
primitives restantes de `chart-core.js` gardaient l'ancien rendu et
créaient une rupture visuelle à côté des aires 2026. Même stratégie :
livraison **centrale**, zéro fork — tout consommateur des primitives est
upgradé d'un coup.

## 2. Livré (fichier unique `vertex/static/vertex/js/charts/chart-core.js`)

- **`C.sparkline`** : lissage `cubicInterpolationMode 'monotone'` (jamais
  de faux extrêmes), ligne 1,6 px, **mini-aire en dégradé** (`col+'33'` →
  transparent) — le rendu watchlist des apps de courtage ; reste MUETTE
  (aucune interaction, `events: []`, tooltip désactivé) ;
- **`C.bars`** : coins arrondis complets (`borderRadius 5`,
  `borderSkipped:false`), barres légèrement translucides (`+'D9'`) qui
  deviennent **pleines au survol** (`hoverBackgroundColor`) — l'alpha
  n'est appliqué qu'aux hex 6 digits via un garde regex (toute couleur
  non-hex passe inchangée, jamais corrompue) ;
- **`C.donut`** : arcs **arrondis** (`borderRadius 4`) **espacés**
  (`spacing 2`), léger décalage au survol (`hoverOffset 6`), `cutout 70%`
  — donut 2026 ; la règle §33 (≤ 5 catégories) est inchangée.

Palette : **aucun littéral couleur nouveau** — gardien à inventaire exact
identique aux lots 51-52.

## 3. Tests (rouges d'abord — 5 nouveaux)

`tests/test_charts_2026_lot53.py` (rouge confirmé avant l'édition — 4/5,
le gardien anti-littéral étant une non-régression déjà verte, attendu) :
sparkline monotone + `addColorStop` + tooltip muet · bars
`borderSkipped:false` + `hoverBackgroundColor` + garde hex-seulement ·
donut `borderRadius` + `spacing` + `hoverOffset` · aucun hex nouveau ·
SW ≥ v110 et v109 absent.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_charts_2026_lot53.py -q → 5 passed
python -m pytest tests/ -q → 1643 passed, 2 skipped   (1638 + 5)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut
  (8 pages 0 erreur console · client-log 0 · SW v110 servi · parcours
   mémoire · cycle souverain : altération refusée + restauration bouton)
Preuve navigateur visuelle : l'état DÉMO n'affiche ni donut ni bars sur
les pages (portefeuille vide) — dit honnêtement. Preuve directe par
HARNAIS : les trois primitives RÉELLEMENT SERVIES (Chart.js +
chart-core.js du serveur) exécutées sur des canvas de test dans la vraie
page /markets — barres arrondies translucides, donut arcs
arrondis/espacés, sparkline monotone + dégradé rendus, 0 erreur console.
Capture : lot53_primitives.png.
```

SW `td-shell-v109` → `td-shell-v110` (`vertex/app/routes/system.py`) + les
4 gardiens mis à jour (y compris les assertions « vN-1 absent »).

## 5. Invariants

READONLY intact · données réelles uniquement — le lissage monotone
n'invente jamais d'extrême, le harnais de preuve n'utilise aucune donnée
présentée comme réelle (canvas de test superposés, jamais commités) ·
moteur 0.9.0 inchangé · `main` intacte · fichiers runtime non commités.

## 6. Suite (axe visuel — « plus plus plus »)

Le tronc commun `chart-core.js` est maintenant ENTIÈREMENT sur la
signature 2026 (area, multiLine, sparkline, bars, donut + plugins vxGlow/
vxLastDot/vxCrosshair). Candidats lot 54 : chandeliers (candlestick-chart
.js — mèches 1 px, corps arrondis) et modules satellites (equity-chart,
drawdown-chart, price-chart) s'ils n'héritent pas déjà de C.area. La
validation humaine physique reste l'étape décisive.

**Arrêt après ce lot — validation humaine requise.**
