# Automatisations, rapidité et observabilité

## Vérité des jobs

Un job est `NON_IMPLÉMENTÉ` tant qu'un exécuteur réel n'émet pas son battement.
`EN_ATTENTE` signifie implémenté mais pas encore exécuté. `ACTIF`, `ERREUR`,
`STALE` et `DÉSACTIVÉ` exigent une preuve runtime. Le registre ne transforme
pas une intention en automatisation.

Chaque job expose : propriétaire, déclencheur, intervalle, dernière tentative,
dernière réussite, durée, prochain passage, résultat, erreur, dépendances,
freshness produite, coalescence, retry borné et idempotence.

## Chemin de données

Les requêtes UI lisent des snapshots rapides et datés. Les collectes lentes
s'exécutent hors requête, se coalescent par clé et publient atomiquement leur
résultat. Aucun thundering herd, appel fournisseur sans timeout ou retry infini.

```text
provider → timeout/circuit breaker → normalisation → validation
→ snapshot/cache → événement → moteurs → UI
```

## Budgets initiaux à mesurer

Ne pas imposer aveuglément des chiffres historiques. Établir p50/p95/p99 avant
le lot, puis fixer un budget par classe : shell, page chaude, API snapshot,
recherche, collecte, chaîne options et génération IA. Le budget de régression
fait partie de la CI.

Cible de conception : réponse initiale utile sans attendre une source lente ;
le rafraîchissement devient progressif et étiqueté. Réduire payload, appels
dupliqués, parsing et JS de page avant d'ajouter une nouvelle couche.

## Cache

Documenter clé, TTL, maximum, invalidation, scope utilisateur, source,
freshness, stale-while-revalidate et comportement en erreur. Ne jamais mettre
donnée de compte ou secret dans service worker, cache partagé ou logs.

## Observabilité

- logs structurés avec request/job/source IDs ;
- métriques latence, taux d'erreur, timeout, retry, circuit ouvert, cache hit,
  âge et couverture ;
- traces bornées pour routes et fournisseurs, avec suppression des données
  personnelles ;
- `/healthz` pour vie, `/readyz` pour capacité, statut système pour détails ;
- alertes actionnables, sans payload financier privé ;
- rétention et export explicitement documentés.

OpenTelemetry est un candidat, pas une obligation. L'instrumentation ne doit
pas devenir une fuite de portefeuille ou de prompt.

## Tests

- route chaude/froide, fournisseur lent, timeout et circuit ouvert ;
- plusieurs requêtes identiques coalescées ;
- cache stale et fallback honnêtes ;
- restart, replay et idempotence des jobs ;
- charge HTTP reproductible avec seuils ;
- absence de thread fantôme et fermeture propre ;
- budget JS/CSS/images et Lighthouse sur les pages principales ;
- preuve que l'UI reste utilisable sans IBKR, Claude ou réseau externe.
