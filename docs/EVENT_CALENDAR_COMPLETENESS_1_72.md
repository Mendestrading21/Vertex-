# Vertex — Complétude du calendrier événementiel options

Le risque ex-dividende ne traite plus une date absente comme une absence de risque. `dividend_risk(None, ...)` retourne désormais `INCONNU` avec un motif explicite.

| Situation | Niveau retourné | Interprétation |
|---|---|---|
| Date ex-dividende absente | `INCONNU` | Le calendrier est incomplet ; aucune absence de risque n’est inférée |
| Événement earnings élevé ou modéré connu | Niveau observé prioritaire | Une menace objectivement connue n’est pas masquée par le calendrier incomplet |
| Calendriers earnings et dividende connus | Niveau combiné observé | Synthèse déterministe des deux calendriers |

`combined()` expose `calendar_coverage` avec le statut `EVENT_CALENDAR_AVAILABLE` ou `EVENT_CALENDAR_INCOMPLETE`.

> Ce statut décrit la complétude des données de calendrier. Il ne prédit pas le prix, ne garantit aucun résultat et n’exécute aucun ordre. Vertex demeure en lecture seule.
