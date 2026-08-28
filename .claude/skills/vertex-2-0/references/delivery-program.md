# Programme maître de livraison Vertex 2.0

Le programme fait converger l'existant par lots indépendants, réversibles et
mesurés. Un lot reste ouvert tant que ses consommateurs, tests, migrations et
preuves runtime ne sont pas terminés. Claude ne démarre jamais plusieurs lots
dépendants en parallèle et ne fusionne jamais automatiquement.

## Phase A — Autorité, confidentialité et vérité

### Lot 0 — Baseline reproductible

Figer SHA, branche, PR/CI, inventaire des routes, moteurs, jobs, stores,
sources, pages, tests, dépendances, données persistées et documents actifs.
Mesurer latences, payloads, erreurs, états de connexion et captures avant.
Exécuter `audit_runtime.py`, publier la matrice vérité → cible et interdire de
traiter une redirection ou une 404 comme une page déjà livrée.

### Lot 1 — Autorité Claude unique

Activer uniquement `/vertex-2-0`, intégrer les règles utiles des doctrines
historiques, retirer skills/agents concurrents prouvés et ajouter le test de
non-réapparition. Les archives restent explicitement historiques.

### Lot 2 — Frontière IBKR market-data-only

Créer un firewall de capacités typé, retirer comptes/positions/P&L/routes et
objets IB bruts, corriger les statuts de connexion, protéger caches/logs et
prouver par double hostile qu'aucun appel personnel n'est possible.

### Lot 3 — Portefeuille manuel souverain

Consolider enveloppes, cash déclaré, positions, thèses, transactions et
valorisations sans propriétaire double. Migrer idempotemment les stores
existants avec sauvegarde, aperçu, rollback et provenance champ par champ.

### Lot 4 — Sécurité privée et exposition

Faire échouer tout démarrage privé non-loopback sans authentification, rendre
la démo publique non persistante, ajouter CSRF/rate limit/headers no-store,
minimisation IA, scan secrets/PII et politique explicite de consentement.

## Phase B — Architecture de la machine

### Lot 5 — Contrats instrument, source et unité

Une identité d'instrument, une unité canonique par champ, enveloppes de
provenance, fraîcheur, qualité et lineage. `UNKNOWN` n'est jamais zéro ni
neutre. Migrer route par route sans casser les fixtures.

### Lot 6 — Market Data Gateway et snapshots

Un propriétaire de connexion, collectes asynchrones, timeouts, pacing,
circuit breakers, coalescence et snapshots immuables publiés atomiquement.
Aucun réseau fournisseur dans une requête UI.

### Lot 7 — Automatisations honnêtes

Relier chaque job à un exécuteur réel ou le marquer `NON_IMPLÉMENTÉ`. Ajouter
idempotence, retries bornés, heartbeats, freshness produite, reprise après
redémarrage, arrêt propre et tests de panne.

### Lot 8 — Observabilité et budgets

Logs structurés sans données privées, métriques/traces bornées, health/ready,
latence p50/p95/p99, budgets payload/cache/JS/CSS et charge reproductible.

### Lot 9 — Convergence du runtime

Réduire `terminal.py` par strangler pattern. Choisir un propriétaire par route,
store, service, composant et style ; migrer les consommateurs, mesurer la
parité puis retirer l'ancien chemin dans une PR dédiée.

## Phase C — Intelligence canonique

### Lot 10 — AdviceEngine unique

Une seule API `AdviceEngine.evaluate(snapshot) -> AdviceResult`. Les autres
moteurs deviennent producteurs de preuves/métriques. Compléter les hard gates,
unifier R:R et versions, rendre GET purs et supprimer les verdicts UI/JS après
parité.

### Lot 11 — Gateway IA unique

Faire passer analyste, copilote, briefs et enrichissement par schéma strict,
grounding numérique, citations, redaction, consentement, limites de coût/débit,
audit et fallback déterministe. Claude explique mais ne décide pas.

### Lot 12 — Pipeline opportunités et recherche

Un entonnoir point-in-time, budgets à chaque étage, preuves comparables,
déduplication, calendrier et statut explicable. Aucun candidat ne contourne les
gates canoniques.

### Lot 13 — Options et simulateur multi-actifs

Unifier chaîne, identité contrat, unités, filtres, Greeks, volatilité, GEX,
scénarios et recommandations. Consolider les trois simulateurs en un moteur
Actions/ETF/Options/Forex, séparer prévision, estimation et stress, sans ordre.

## Phase D — Produit Black Glass page par page

### Lot 14 — Fondations et shell

Tokens, Geist/Geist Mono, Black Glass Signal Light, composants, topbar,
`NavigationManifest` unique, sidebar groupée, barre mobile, recherche,
responsive, états et Design System interne. Résoudre la collision
`/options/<sym>`, rendre Journal accessible à 390 px et arbitrer le routeur
persistant avant la cosmétique. Fusionner les deux Design Systems seulement
après migration de leurs consommateurs. Aucune logique financière dans l'UI.

### Lot 15 — Aujourd'hui et Calendrier

Command center : attention, risques, revues, opportunités, événements et tâches
à partir de données réelles. Calendrier global sans dupliquer ses producteurs.

### Lot 16 — Marchés et Opportunités

Vue de marché, régimes, listes, heatmaps et entonnoir canonique ; une
visualisation dominante, sources/fraîcheur visibles et drill-down cohérent.

### Lot 17 — Analyse

Un seul dossier ticker et un seul `AdviceResult`, avec thèse, preuves,
contradictions, gates, scénarios, sources, annotations et historique.

### Lot 18 — Options et Simulateur

Vue options, chaîne, volatilité, scanner, stratégies et scénarios. Simulateur
multi-actifs compréhensible, hypothèses/limites visibles, aucun bouton d'ordre.

### Lot 19 — Portefeuille, Suivi et Performance

Patrimoine déclaré, allocations, exposition, risque, thèses, watchlists,
alertes, journal et performance avec populations et provenances séparées.

### Lot 20 — Vertex IA et Système

Assistant explicatif fondé sur le packet canonique ; connexions, données, jobs,
sécurité, archives, préférences et diagnostic sans fuite d'information.

### Lot 21 — Responsive, accessibilité et netteté

Vérifier 390/430/768/1024/1280/1440/1600, clavier, zoom 200 %, touch, focus,
reduced motion, contraste, HiDPI, tableaux/graphiques et budgets Lighthouse.

## Phase E — Nettoyage et acceptation

### Lot 22 — Nettoyage prouvé

Retirer seulement les adaptateurs, routes, moteurs, CSS, assets, tests et docs
dont l'absence de consommateur, la parité, la migration et le rollback sont
prouvés. Les branches distantes font l'objet d'une autorisation séparée.

### Lot 23 — Acceptation finale

Exécuter compile, tests ciblés/complets, no-orders, privacy firewall, tests de
charge/sécurité/navigateur, les 150 contrôles, captures avant/après et rollback.
La PR reste brouillon jusqu'à validation humaine.

## Commandes Claude

```text
/vertex-2-0 mode:audit
/vertex-2-0 lot:2
/vertex-2-0 page:Analyse
```

Sans lot explicite, Claude remesure la baseline et reprend le premier lot non
terminé. Il ne transforme jamais ce programme en promesse de capacité déjà
livrée.
