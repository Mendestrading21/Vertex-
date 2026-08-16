# Vertex — réponses d’erreur API sûres 1.11

## Principe

Les réponses d’erreur ne retournent plus les classes d’exception, messages, chemins locaux ou détails d’implémentation. Elles emploient des codes stables orientés produit, tandis que les calculs normaux et les états `empty` restent inchangés.

| Domaine | Code sûr | Statut |
|---|---|---:|
| Vue options | `options_overview_unavailable` | 500 |
| Environnement options | `options_environment_unavailable` | 500 |
| GEX / radar / graphiques | `options_gex_unavailable`, `options_gex_radar_unavailable`, `options_vol_charts_unavailable` | 500 |
| Simulation | `simulation_indisponible` | 200 avec `empty: true` |
| Laboratoire options | `options_lab_unavailable`, `options_analysis_unavailable` | 500 ou 200 selon le parcours historique |
| Erreur API non interceptée | `internal` | 500 |

Les codes représentent une indisponibilité de calcul, pas un signal de marché. Ils ne doivent pas être convertis en recommandation, ordre ou hypothèse sur les données sous-jacentes.
