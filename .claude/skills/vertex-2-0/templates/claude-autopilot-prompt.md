# Prompt Claude Code — Vertex 2.0 Autopilot

```text
/vertex-2-0 mode:audit

Tu es responsable de faire converger ce dépôt vers Vertex 2.0 en suivant
strictement le skill maître et son programme de livraison.

Commence par remesurer le dernier main, le runtime, les PR/CI, routes, moteurs,
sources, jobs, stores, pages, tests et documents. Exécute notamment
`scripts/audit_runtime.py` depuis le skill et compare le résultat à
`runtime-page-manifest.md`. Ne crois aucune ancienne affirmation sans preuve.
Publie la baseline et les P0, puis continue
automatiquement avec le premier lot non terminé, un seul lot cohérent à la
fois.

Avant le premier changement, produis un `WORK_MANIFEST` versionné contenant :
lot, objectif, non-objectifs, SHA, propriétaires, fichiers, routes, stores,
données à préserver, dépendances, tests rouges, budgets, captures, migration,
rollback et critères d'arrêt. Ne modifie aucun fichier absent de ce manifeste
sans l'actualiser et expliquer pourquoi.

Invariants : aucun ordre ou ticket broker ; IBKR données de marché uniquement ;
zéro compte/solde/position/P&L IBKR ; portefeuille saisi manuellement ; un seul
AdviceResult ; Claude explique et l'humain décide ; aucune donnée inventée ;
aucune fusion automatique.

Fais converger l'existant au lieu de tout réécrire. Avant de supprimer, prouve
consommateurs migrés, parité, données préservées et rollback. N'efface aucune
branche distante et ne réécris pas l'historique Git sans mon autorisation
explicite sur une liste précise.

Ne considère jamais une redirection ou une 404 comme une page livrée. Respecte
la matrice vérité → cible et son ordre de cutover. Ne supprime Journal,
Tracking, une ancienne route ou un Design System qu'après migration de ses
consommateurs, deep links, stores et tests.

Pour l'intelligence et les stratégies : utilise uniquement des snapshots
point-in-time ; sépare faits, calculs, estimations, simulations et
interprétations ; empêche look-ahead/survivorship ; inclue coûts, spread,
slippage, liquidité, benchmark, walk-forward, purge/embargo, stabilité des
paramètres/régimes et replay. Aucun backtest ne modifie AdviceResult ou une
règle active. Claude explique les preuves ; il ne choisit pas la stratégie.

Pour les connexions : consolide d'abord le runtime Flask, le scheduler et les
snapshots existants. N'ajoute ni Redis, PostgreSQL, Celery, Kafka, Temporal,
React ni plateforme financière complète sans manque reproduit, seuil mesuré,
ADR, licence, test de panne et plan de retrait. Toute source externe passe par
une enveloppe identité/unité/source/timestamps/mode/qualité/fallback et ne
partage jamais l'objet provider brut avec l'UI.

Pour chaque page, lis `page-widget-intelligence-blueprint.md`, puis produis la
fiche `PAGE_CONTRACT` : question en cinq secondes, widget dominant, preuves
secondaires, action primaire non financière, contrats de données, états,
desktop/mobile, accessibilité et budget. N'ajoute aucun widget dont les données
ou le moteur ne sont pas réels.

Pour chaque page modifiée, produis automatiquement une capture avant puis une
capture après à 1600, 1024 et 390 px, avec mêmes données/route/état. Vérifie
interactions, clavier, focus, console, réseau, client-log, responsive et états
dégradés. Annexe les captures et résultats au rapport du lot avant de passer à
la page suivante.

Chaque dépendance ou méthode GitHub est une candidature, pas une consigne
d'installation. Pour chacune, renseigne source exacte, version/SHA, licence,
maintenance, permissions, poids, compatibilité, données envoyées, tests,
alternative locale et retrait. Une adoption utilise une PR dédiée et ne peut
être mélangée à la refonte visuelle d'une page.

Reste en français. Ouvre ou mets à jour une PR brouillon. Après chaque lot,
indique commit, fichiers, tests exacts, mesures avant/après, écarts, rollback et
prochain lot. Arrête-toi seulement pour une décision réellement destructive,
une migration ambiguë, une donnée privée, une permission nouvelle, une formule
financière non spécifiée ou la validation finale de fusion.

À la fin de chaque lot, exécute une revue depuis le diff et le runtime :
intégrité des données, sécurité/READONLY, calculs/unités, navigateur,
accessibilité, performance, dépendances, migrations et rollback. Un test vert
qui ne prouve pas l'invariant demandé est insuffisant. Ne passe au lot suivant
que lorsque chaque critère reçoit `OK + preuve`, `N/A + justification` ou
`Écart + ticket`.
```
