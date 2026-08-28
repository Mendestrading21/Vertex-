# Lot 26 — Nettoyage GitHub : archives POUSSÉES, suppression prête (RAPPORT)

Date : 2026-08-28 · Autorisation utilisateur : donnée (exécution complète)

## Fait

1. **Classement vérifié** (748 refs) : 30 fusionnées dans main (tranche A,
   re-prouvées ancêtres), 636 `agent/skyler-v2-*` (tranche B), 77
   pré-consolidation (tranche C), 5 protégées — listes exactes dans
   `branches-tranche-{A,B,C}.txt`.
2. **Archives octopus POUSSÉES et vérifiées** (chaque tête archivée est un
   parent → chaque commit reste joignable, AUCUNE perte possible) :
   - `archive/skyler-v2-20260804` @ `4ab5a374` (636 têtes, 8 segments) ;
   - `archive/pre-vertex-2-0-20260828` @ `07d82011` (77 têtes) ;
   - contre-épreuve : `git merge-base --is-ancestor` vert sur échantillons
     + premières/dernières têtes de chaque liste.
3. **PR #840 fusionnée dans main** (`1d72bfe`) ; #838 et #839 fermées avec
   preuve de contenance (`682c2014` et `cfec7145` ancêtres de main).

## Bloqué — à exécuter par l'utilisateur (1 minute)

La politique de permissions de l'environnement d'exécution refuse
`git push --delete` (action distante destructive), indépendamment de
l'autorisation donnée. Tout est préparé ; depuis un clone local :

```bash
# Tranche A (30 fusionnées) puis B (636 archivées) puis C (77 archivées) :
for f in docs/vertex-2-0/lot-26/branches-tranche-A.txt \
         docs/vertex-2-0/lot-26/branches-tranche-B.txt \
         docs/vertex-2-0/lot-26/branches-tranche-C.txt; do
  xargs -a "$f" -n 25 git push origin --delete
done
```

Vérification après coup : `git ls-remote --heads origin | wc -l` doit
rendre ~10 (main, 2 archives, 2 branches ex-PR si conservées, intégration,
checkpoint, vy3h7s…). Rollback d'une suppression : recréer la branche
depuis son SHA listé dans `ARCHIVE.md` de l'archive correspondante.

## Jamais touché

`main` · les 2 archives · `agent/vertex-design-2-0-master-20260827` ·
`claude/vertex-2-0-visual-redesign-vy3h7s` ·
`checkpoint/vertex-2-0-graphique-20260828` ·
`agent/vertex-2-0-integration-20260828` · tag `vertex-premium-2026-07-07`.
Aucun force-push, aucune réécriture d'historique.
