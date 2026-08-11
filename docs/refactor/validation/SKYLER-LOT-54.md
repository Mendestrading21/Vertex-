# SKYLER V2 — LOT 54 : prix d'Analyse & chandeliers sur la signature 2026

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-54-candles-2026`
(base : `integration/vertex-skyler-v2` @ `edf95a0`, fraîchement fetchée) ·
Mode : développement, axe VISUEL — arc utilisateur « développe jusqu'au
lot 60 » (54 = graphiques satellites, 55 = connexions entre pages,
56-59 = polish détaillé, 60 = RC finale + arrêt).

## 1. Justification du choix de lot

Le tronc commun `chart-core.js` est entièrement 2026 depuis le lot 53,
mais deux modules satellites gardaient l'ancien rendu : `price-chart.js`
— le graphique PRINCIPAL de la fiche Analyse, la carte la plus regardée
du produit — et `candlestick-chart.js` (repli Chart.js honnête des
chandeliers). Inspection préalable : `equity-chart.js` et
`drawdown-chart.js` délèguent déjà à `C.area` (héritage automatique des
lots 51-52 — aucun changement nécessaire, dit) ; `candlestick-lwc.js`
reste sur son moteur TradingView Lightweight Charts pro (crosshair natif,
zoom/pan) — inchangé, dit.

## 2. Livré

**`price-chart.js`** — signature 2026 complète : lissage monotone (jamais
de faux extrêmes), ligne 2 px, dégradé 3 arrêts (`brand+'4D'` → `+'17'` →
transparent), glow (`C.glowPlugin`), visée au survol (`C.crosshairPlugin`),
pastille de dernier prix (`C.lastDotPlugin` + `VX.fmt.price`). Le plan
moteur (`C.levelLines`) et les marqueurs earnings (`C.eventMarkers`) sont
conservés tels quels.

**`candlestick-chart.js`** — chandeliers 2026 : mèches FINES 1 px (avant
1,5), corps ARRONDIS (`borderRadius 2`, `borderSkipped:false`), visée au
survol. **Défaut visuel RÉEL attrapé par la preuve navigateur** : l'axe Y
était forcé à 0 (défaut Chart.js pour les barres flottantes) — des bougies
à ~100 s'écrasaient sur une échelle 0-150, illisibles. Corrigé :
`beginAtZero:false` + `grace 5 %` — l'axe épouse la plage de prix réelle.
Test rouge ajouté après coup pour figer la correction.

Palette : aucun littéral hex nouveau dans les fichiers touchés
(`price-chart.js` garde son unique secours `#DBE1E8` pré-existant,
`candlestick-chart.js` n'en a aucun — gardien).

## 3. Tests (rouges d'abord — 7 nouveaux)

`tests/test_charts_2026_lot54.py` (rouge confirmé 4/6 avant l'édition —
les 2 verts étant des non-régressions plan/earnings et littéraux,
attendu ; 7e test ajouté rouge après le défaut navigateur) : signature
complète du prix · plan+earnings conservés · corps arrondis + mèches 1 px ·
crosshair chandeliers · échelle Y épousant les prix · littéraux inchangés ·
SW ≥ v111 et v110 absent.

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_charts_2026_lot54.py -q → 7 passed
python -m pytest tests/ -q → 1650 passed, 2 skipped   (1643 + 7)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v111 servi,
  cycle souverain inclus)
Preuve navigateur par HARNAIS (modules réellement servis, exécutés dans
la vraie page /analysis) : priceCard — courbe monotone + glow + dégradé +
pastille « 110,40 » + niveau Entrée rendus ; candlestickCard — bougies
arrondies lisibles sur échelle ajustée (95-115), mèches fines, visée +
tooltip OHLC au survol réel. 0 erreur console. Capture :
lot54_price_candles.png.
```

SW `td-shell-v110` → `td-shell-v111` + les 4 gardiens (« vN-1 absent »
inclus).

## 5. Invariants

READONLY intact · données réelles uniquement — le repli honnête « OHLC
indisponible → clôtures, aucune bougie inventée » est inchangé, l'échelle
ajustée n'invente rien (elle cadre) · moteur 0.9.0 inchangé · `main`
intacte · fichiers runtime non commités.

## 6. Suite (arc jusqu'au lot 60)

Lot 55 : CONNEXIONS ENTRE PAGES (demande utilisateur « simplifier les
connexions entre les pages ») — audit réel des liens croisés existants
puis simplification/complétion centrale. Puis 56-59 polish détaillé,
60 RC finale + bilan consolidé + ARRÊT.

**Arrêt après ce lot — validation humaine requise.**
