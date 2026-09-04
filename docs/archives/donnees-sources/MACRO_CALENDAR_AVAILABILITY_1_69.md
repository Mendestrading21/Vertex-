# Vertex — Disponibilité du calendrier macro

La timeline `GET /api/events/<sym>` distingue désormais un calendrier macro effectivement chargé, même vide, d’un calendrier macro indisponible.

| Situation | Statut | Garantie |
|---|---|---|
| Chargement réussi | `MACRO_CALENDAR_AVAILABLE` | `events_loaded` indique le nombre d’événements déclarés chargés |
| Repli technique | `MACRO_CALENDAR_UNAVAILABLE` | Aucun événement macro n’est créé et aucune absence d’événement n’est inférée |

Le statut figure dans `coverage.macro_calendar`. Lorsqu’il est indisponible, le constructeur de timeline reçoit `macro=None`, de sorte que `input_channels.macro_provided` reste `false`.

> Cette couverture est descriptive, sans prévision macroéconomique, score, gate, verdict ou exécution. Vertex demeure en lecture seule.
