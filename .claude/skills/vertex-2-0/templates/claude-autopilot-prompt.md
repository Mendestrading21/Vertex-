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

Pour chaque page modifiée, produis automatiquement une capture avant puis une
capture après à 1600, 1024 et 390 px, avec mêmes données/route/état. Vérifie
interactions, clavier, focus, console, réseau, client-log, responsive et états
dégradés. Annexe les captures et résultats au rapport du lot avant de passer à
la page suivante.

Reste en français. Ouvre ou mets à jour une PR brouillon. Après chaque lot,
indique commit, fichiers, tests exacts, mesures avant/après, écarts, rollback et
prochain lot. Arrête-toi seulement pour une décision réellement destructive,
une migration ambiguë, une donnée privée, une permission nouvelle, une formule
financière non spécifiée ou la validation finale de fusion.
```
