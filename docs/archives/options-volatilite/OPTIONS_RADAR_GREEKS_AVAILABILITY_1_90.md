# Vertex — Disponibilité du radar grec options

Le radar de visualisation exige désormais que chaque grec soit réellement reporté. Il ne remplace plus gamma, thêta, vega ou IV par des valeurs de secours.

| Mesure | Entrée reportée requise | Valeur si absente |
|---|---|---|
| Delta, thêta | Contrat vedette | `null` |
| Gamma, vega | Jambe options associée | `null` |
| IV | Contrat vedette | `null` |

Le champ `radar_coverage` détaille la disponibilité de chaque mesure et renvoie `RADAR_GREEKS_PARTIAL` lorsqu’au moins une manque.

> Le radar est descriptif et en lecture seule. Il ne constitue ni une prévision, ni un ordre, ni une garantie de résultat.
