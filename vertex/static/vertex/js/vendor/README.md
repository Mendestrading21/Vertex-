# Vendored third-party JS

Auto-hébergé (aucun CDN, compatible CSP self-contained). Ne pas éditer ces fichiers.

## lightweight-charts.standalone.production.js
- **Projet** : TradingView Lightweight Charts™
- **Version** : 4.2.3
- **Source** : https://unpkg.com/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js
- **Licence** : Apache License 2.0 — https://github.com/tradingview/lightweight-charts/blob/master/LICENSE
- **Attribution** : requise par la licence. Affichée en deux endroits — le logo « TV »
  natif rendu par la lib sur chaque graphique **et** un lien « Charting by TradingView »
  dans le pied de la carte (voir `../charts/candlestick-lwc.js`).
- **Usage** : rendu des chandeliers PRO (crosshair/zoom) sur la page Analyse via le
  composant `VXCharts.lwCandlestickCard`. Pur frontend, aucune donnée/broker/ordre —
  compatible avec l'invariant READONLY de Vertex.
