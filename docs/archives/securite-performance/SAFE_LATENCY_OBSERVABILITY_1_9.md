# Vertex — observabilité de latence sûre 1.9

## Objectif

Vertex mesure désormais la latence des routes API pour guider les améliorations de performance sans enregistrer de données financières, de paramètres d’URL, de corps de requête, d’adresse IP ou d’identité utilisateur.

## Données conservées

Chaque échantillon contient uniquement le nom d’endpoint Flask, le statut HTTP et une durée en millisecondes. La mémoire est limitée aux 256 derniers échantillons, n’est pas persistée et se réinitialise au redémarrage.

| Champ exposé par endpoint | Usage |
|---|---|
| `count` | Nombre d’échantillons conservés. |
| `mean_ms`, `p50_ms`, `p95_ms`, `max_ms` | Diagnostic de latence, sans promesse de niveau de service. |
| `error_count` | Nombre de réponses HTTP 4xx/5xx sur les échantillons conservés. |

## Consultation

Les statistiques sont disponibles sous `request_metrics` dans `GET /api/skyler/health`. Elles sont strictement descriptives et ne changent ni le score, ni les gates, ni les conclusions de marché.

> La télémétrie utilise le nom interne d’endpoint, pas le chemin demandé. Un symbole, une chaîne d’options, un portefeuille ou un contenu de requête ne peut donc pas être reconstitué depuis les métriques.
