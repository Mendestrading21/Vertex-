# Vertex — Contrat de preuves décisionnelles par symbole

Le module `decision_evidence` ne transforme jamais une source globale en preuve pour un titre. Les contrôles de qualité et de réconciliation sont sélectionnés uniquement depuis un `AnalyticsPacket` correspondant au symbole, un détail explicitement enrichi ou une table de réconciliation indexée par symbole.

| Situation | Statut exposé |
|---|---|
| Aucune qualité instrumentale | `available: false` avec motif explicite |
| Réconciliation instrumentale absente | `available: false` avec motif explicite |
| Source correspondante non actionnable | `actionable_allowed: false` conservé |
| Paquet d’un autre symbole | Ignoré |

> Cette garantie empêche qu’une disponibilité globale soit interprétée comme une preuve de qualité pour un instrument donné. Elle ne modifie ni score, ni gate, ni verdict, et Vertex demeure un système d’analyse en lecture seule.
