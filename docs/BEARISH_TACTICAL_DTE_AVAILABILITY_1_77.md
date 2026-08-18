# Vertex — Disponibilité DTE du module tactique baissier

Le module d’achat de PUT tactique exclut désormais les contrats dont le DTE n’est pas numérique, entier, non négatif et réellement reporté.

| DTE du PUT | Effet |
|---|---|
| Valide et dans la constitution | Peut poursuivre les contrôles de liquidité, anomalies et simulation |
| Absent, illisible, négatif ou fractionnaire | Exclu avant sélection ; une note de disponibilité est ajoutée |

Le refus ne crée aucune position ni signal baissier. Il est distinct de l’absence de preuves baissières, de liquidité ou de R:R suffisant.

> Vertex n’achète ni ne vend d’options. Le module reste une analyse en lecture seule sans garantie de résultat.
