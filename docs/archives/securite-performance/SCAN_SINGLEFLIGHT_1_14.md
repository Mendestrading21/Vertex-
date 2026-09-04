# Vertex — exécution single-flight du scan

## Objectif

Le cycle de marché ne peut exécuter qu’un téléchargement global à la fois. Un déclencheur concurrent — rafraîchissement manuel ou signal de boucle — ne démarre pas un second téléchargement yfinance, Stooq, options ou fondamentaux pendant que le scan en cours possède le verrou.

| État | Signification | Données servies |
|---|---|---|
| `RUNNING` | Un scan est actif ou un second déclencheur a été ignoré. | Le dernier état complet de scan reste disponible. |
| `IDLE` | Le dernier scan s’est terminé sans code d’erreur. | Le dernier état complet de scan reste disponible. |
| `DEGRADED` | Le scan s’est terminé avec une indisponibilité de source ou une erreur sûre. | L’état précédent reste disponible avec les codes de santé descriptifs. |

`scan_skip_count` est un compteur non sensible de déclencheurs concurrents ignorés. Il ne contient ni identité de demandeur, ni paramètres, ni contenu de requête.

> Le verrou ne transforme pas un scan en opération de trading : il réduit seulement le travail réseau concurrent et protège la cohérence de l’état analytique en lecture seule.
