# /vertex-v4-redesign

## Rôle

Tu es l'orchestrateur unique de la refonte Vertex V4 **Obsidian Prism**.
Tu travailles sur `integration/vertex-v4-clean`, jamais directement sur `main`.

## Lecture obligatoire

Avant toute action, lire :

1. `CLAUDE.md`
2. `docs/README.md`
3. `docs/canonical/READONLY.md`
4. `docs/canonical/DATA_CONTRACT.md`
5. `docs/canonical/CHART_CONTRACT.md`
6. `docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`
7. `docs/vertex-v4/DECISIONS.md`
8. `docs/vertex-v4/STATUS.md`
9. `docs/vertex-v4/MIGRATION_MAP.md`
10. `docs/vertex-v4/reference/README.md`

Ouvrir la référence maître :
`docs/vertex-v4/reference/00-master-obsidian-prism.jpg`.

Les fichiers de `references/` complètent ces contrats. En cas de contradiction,
les documents canoniques et `DECISIONS.md` gagnent.

## Invariants absolus

- Refonte visuelle et ergonomique uniquement.
- Aucun moteur, calcul, score, verdict, contrat API ou donnée métier modifié.
- `READONLY=True` et `readonly=True` intacts ; aucun chemin d'ordre.
- Aucune donnée inventée ; absence et estimation explicitement étiquetées.
- Routes, IBKR, TradingView, sync, stockage et service worker préservés.
- Aucun secret, identifiant de compte ou nom personnel dans le dépôt/captures.
- Un seul lot actif et un commit atomique par sous-lot cohérent.
- Aucune suppression de legacy sans satisfaire `MIGRATION_MAP.md`.

## Modes

### `/vertex-v4-redesign audit`

Effectuer uniquement le lot 00 ou rafraîchir sa baseline :

1. vérifier branche et worktree ;
2. lire les contrats ;
3. inventorier pages, sous-vues, CSS, styles inline et thèmes graphiques ;
4. lancer tests et application en mode démo ;
5. capturer chaque espace en desktop, tablette et mobile ;
6. relever erreurs console, overflow, incohérences et composants dupliqués ;
7. produire un rapport ancré dans les fichiers ;
8. mettre à jour `STATUS.md` sans modifier l'interface.

### `/vertex-v4-redesign plan`

À partir de l'audit :

1. définir les fichiers exacts de chaque lot ;
2. cartographier producteur, consommateur et tests ;
3. séparer fondations, shell, composants, graphiques et pages ;
4. documenter les migrations legacy et risques de régression ;
5. définir les preuves de validation ;
6. ne pas commencer l'implémentation.

### `/vertex-v4-redesign execute <lot>`

1. vérifier les prérequis dans `STATUS.md` ;
2. annoncer périmètre, fichiers, risque et tests ;
3. créer `claude/v4-XX-description` si une branche temporaire est nécessaire ;
4. implémenter uniquement le lot demandé ;
5. compiler et exécuter tous les tests ;
6. démarrer en `DEMO=1 NO_IBKR=1` ;
7. vérifier desktop/tablette/mobile, console, overflow et états de données ;
8. comparer à la référence maître ;
9. mettre à jour `STATUS.md` et `MIGRATION_MAP.md` si nécessaire ;
10. commit/push, puis s'arrêter pour revue visuelle.

### `/vertex-v4-redesign review <lot>`

Lecture seule : comparer captures, référence, contrats, responsive, sémantique des
couleurs et cohérence inter-pages. Classer les écarts P0 à P3 et proposer une
correction ciblée sans l'appliquer.

### `/vertex-v4-redesign fix <lot>`

Appliquer uniquement les corrections validées, retester, recapturer, mettre à
jour le statut, commit/push et s'arrêter.

### `/vertex-v4-redesign final-qa`

Exécuter le lot 16 : neuf espaces, toutes sous-vues, trois viewports, tous états,
0 overflow, 0 erreur console, tests à 100 %, READONLY intact, aucune route cassée,
aucune donnée fabriquée et aucun legacy visuel actif non documenté.

## Ordre des lots

```text
00 consolidation-baseline
01 foundations
02 shell
03 components
04 charts
05 briefing
06 markets
07 opportunities
08 portfolio
09 analysis
10 options
11 performance
12 intelligence
13 system
14 tracking-mobile
15 cleanup
16 final-qa
17 final-pr
```

Ne jamais traiter plusieurs pages en une passe globale.

## Tests minimums

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
```

Puis :

- `GET /healthz` sain ;
- `GET /api/client-log` sans erreur réelle ;
- routes principales en HTTP 200 ;
- console navigateur vide ;
- 1536×960, 768×1024 et 390×844 ;
- loading, empty, partial, stale et error ;
- focus clavier, contraste et réduction du mouvement.

## Definition of Done

Un lot n'est terminé que si :

- son périmètre est isolé ;
- aucun contrat métier/donnée n'a changé ;
- tests complets verts ;
- application réellement démarrée ;
- captures aux trois viewports ;
- comparaison avec la référence ;
- 0 erreur console et 0 overflow ;
- états de données vérifiés ;
- accessibilité vérifiée ;
- `STATUS.md` à jour ;
- commit poussé ;
- revue utilisateur encore distincte de « code terminé ».

## Rapport de lot

```markdown
# Lot XX — Nom

## Résultat
- ...

## Fichiers
- ...

## Invariants
- READONLY : OK
- Métier / API / données : inchangés
- Routes : inchangées ou migration documentée

## Tests
- commande : ...
- résultat : ...

## Navigateur
- desktop : ...
- tablette : ...
- mobile : ...
- console / overflow / états : ...

## Captures
- ...

## Commit
- ...

## À valider visuellement
- ...
```

## Premier message d'une session

Toujours indiquer : branche active, lot courant, référence trouvée, tests de
baseline, action proposée et confirmation qu'aucun moteur ni chemin d'ordre ne
sera touché.
