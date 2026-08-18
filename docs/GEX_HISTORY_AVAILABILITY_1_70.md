# Vertex — Disponibilité de l’historique GEX

La réponse `GET /api/options/gex/<sym>` expose `history_availability` en complément de `history`.

| Situation | Statut | Garantie |
|---|---|---|
| Journal et lecture réussis | `GEX_HISTORY_AVAILABLE` | `points_loaded` compte les observations réellement retournées, y compris zéro |
| Journal ou lecture indisponible | `GEX_HISTORY_UNAVAILABLE` | `history` reste vide sans être interprété comme absence d’historique |

Le statut est descriptif. Il ne modifie ni le calcul du profil GEX, ni le flux, ni la synthèse options.

> Un historique GEX est une mesure d’observations disponibles, pas une prévision ou un ordre. Vertex reste strictement en lecture seule.
