# Vertex — Disponibilité des scores directionnels du laboratoire options

Les lignes « Institutionnels », « Momentum » et « Greeks » ne transforment plus un score absent en état neutre ou en lecture de convexité. Chaque état indisponible est rapporté avec une couverture dédiée.

| Diagnostic | Intrant nécessaire | Statut si absent |
|---|---|---|
| Institutionnels | Anomalie de volume (`vol_z`) numérique | `INSTITUTIONAL_SIGNAL_UNAVAILABLE` |
| Momentum | Momentum numérique | `MOMENTUM_SIGNAL_UNAVAILABLE` |
| Greeks | Delta numérique | `GREEKS_DELTA_UNAVAILABLE` |

> Les diagnostics demeurent descriptifs et en lecture seule : aucun ordre, aucune garantie de performance et aucune donnée synthétique ne sont produits.
