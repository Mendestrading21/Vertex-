# Vertex — Transparence du repli de profil du scanner d’horizons

Le scanner d’horizons options continue à servir une analyse bornée lorsque le profil de stratégie ne peut pas être chargé. Il utilise alors uniquement ses fenêtres internes documentées et expose ce repli dans la sortie du scan.

| Chargement du profil | Fenêtres appliquées | `profile_coverage.status` |
|---|---|---|
| Réussi | Profil actif, complété si nécessaire par les limites internes | `PROFILE_AVAILABLE` |
| Échec non détaillé | Limites internes stables du scanner | `PROFILE_FALLBACK` |

Le détail de l’exception de chargement n’est jamais servi. Le statut est descriptif, sans ordre, sans données synthétiques et sans garantie de résultat.
