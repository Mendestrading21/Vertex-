# Vertex — Disponibilité des contrôles portefeuille du briefing

La réponse `GET /api/command` expose désormais `controls_availability` pour ses contrôles portefeuille.

| Contrôle | Statut disponible | Statut indisponible |
|---|---|---|
| Risque portefeuille | `PORTFOLIO_RISK_AVAILABLE` | `PORTFOLIO_RISK_UNAVAILABLE` |
| Validation portefeuille | `PORTFOLIO_VALIDATION_AVAILABLE` | `PORTFOLIO_VALIDATION_UNAVAILABLE` |

Lorsqu’un moteur est indisponible, son résultat demeure `null` et un motif descriptif est exposé. Le champ `does_not_change_decision` garantit que ce statut n’altère pas la décision de marché du briefing.

> Ces contrôles sont informatifs, sans exécution d’ordre et sans garantie de résultat. Vertex demeure en lecture seule.
