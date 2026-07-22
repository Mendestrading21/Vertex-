# /vertex-v4-redesign

## Rôle

Tu es l’orchestrateur de la refonte visuelle VERTEX V4.

Tu travailles dans le dépôt `Mendestrading21/Vertex-` sur la branche d’intégration :

```text
redesign/vertex-v4-master
```

Tu dois lire intégralement avant toute action :

```text
CLAUDE.md
docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md
docs/vertex-v4/STATUS.md
```

La référence visuelle officielle est l’image validée par l’utilisateur. Elle doit être jointe à la session Claude Code ou au ticket GitHub principal. Ne jamais remplacer cette référence par une tendance générique ou une autre maquette.

---

## Invariants absolus

- Refonte visuelle et ergonomique uniquement.
- Ne jamais modifier les moteurs financiers, scores, décisions, données ou règles métier.
- Ne jamais modifier la sécurité READONLY ni créer un chemin d’ordre.
- Ne jamais inventer de données.
- Ne jamais travailler directement sur `main`.
- Ne jamais fusionner vers `main` sans accord explicite.
- Ne jamais coder un nom personnel en dur.
- Préserver routes, APIs, IBKR, TradingView, Claude, sync et stockage.
- Un lot actif à la fois.
- Un commit clair par lot ou sous-lot cohérent.

---

## Modes de commande

### `/vertex-v4-redesign audit`

Effectuer uniquement le lot 00 :

1. vérifier la branche active ;
2. lire les documents V4 ;
3. cartographier toutes les pages et sous-vues ;
4. inventorier les CSS globaux, CSS locaux, styles inline et thèmes de graphiques ;
5. démarrer l’application sans IBKR si nécessaire ;
6. capturer l’état actuel de chaque page en desktop, tablette et mobile ;
7. relever overflow, erreurs console, incohérences visuelles et composants dupliqués ;
8. produire un rapport ;
9. mettre à jour `STATUS.md` ;
10. ne modifier aucun fichier d’interface pendant cet audit.

### `/vertex-v4-redesign plan`

À partir de l’audit :

1. produire le plan exact des fichiers à modifier pour chaque lot ;
2. distinguer fondations, shell, composants, graphiques et pages ;
3. identifier les risques de régression ;
4. préciser comment préserver les comportements existants ;
5. proposer les validations de chaque lot ;
6. ne pas commencer l’implémentation sans instruction d’exécution.

### `/vertex-v4-redesign execute <lot>`

Exécuter uniquement le lot demandé, par exemple :

```text
/vertex-v4-redesign execute 01
/vertex-v4-redesign execute 05
/vertex-v4-redesign execute 10
```

Processus obligatoire :

1. relire le périmètre dans la Master Spec ;
2. vérifier que les lots prérequis sont terminés ;
3. annoncer les fichiers ciblés ;
4. créer une branche temporaire `claude/v4-XX-nom` ou travailler sur la branche d’intégration avec un commit isolé ;
5. implémenter sans toucher au métier ;
6. exécuter les tests ;
7. démarrer l’application ;
8. vérifier dans un vrai navigateur ;
9. capturer desktop, tablette, mobile ;
10. contrôler loading, empty, stale, error ;
11. vérifier clavier, contraste et responsive ;
12. mettre à jour `STATUS.md` ;
13. commit et push ;
14. s’arrêter pour revue visuelle.

### `/vertex-v4-redesign review <lot>`

Ne pas modifier immédiatement.

1. comparer les captures du lot à la référence ;
2. contrôler cohérence avec les autres pages déjà migrées ;
3. vérifier que la sémantique des couleurs est respectée ;
4. relever les écarts par ordre de gravité ;
5. proposer une correction ciblée ;
6. attendre l’autorisation avant d’appliquer les corrections importantes.

### `/vertex-v4-redesign fix <lot>`

Appliquer uniquement les corrections validées à la revue, retester, recapturer, mettre à jour `STATUS.md`, commit et push.

### `/vertex-v4-redesign final-qa`

Exécuter le lot 16 :

- toutes pages ;
- toutes sous-vues ;
- desktop / tablette / mobile ;
- 0 overflow horizontal ;
- 0 erreur console réelle ;
- 100 % des tests existants verts ;
- READONLY intact ;
- aucune route cassée ;
- aucun style Copper / Signal Green incohérent restant ;
- aucun chiffre inventé ;
- rapport final avant PR.

---

## Ordre obligatoire

```text
00 audit
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

Ne jamais refaire toutes les pages en une seule passe.

---

## Tests minimums

Commencer par les commandes documentées dans `CLAUDE.md`.

Minimum :

```bash
python -m pytest tests/ -q
```

Après un changement visuel lourd :

- vérifier le démarrage Flask ;
- vérifier `/healthz` ;
- vérifier `/api/client-log` ;
- vérifier les pages en vrai navigateur ;
- vérifier la console ;
- si le shell visible change, appliquer la règle de version du service worker documentée dans `CLAUDE.md`.

---

## Definition of Done

Aucun lot ne peut être déclaré terminé sans :

- tests verts ;
- application fonctionnelle ;
- captures desktop/tablette/mobile ;
- comparaison avec la référence ;
- aucune donnée ou logique métier altérée ;
- aucune erreur console ;
- aucun overflow horizontal ;
- états de données vérifiés ;
- `STATUS.md` à jour ;
- commit poussé ;
- arrêt pour validation utilisateur.

---

## Format du compte rendu après chaque lot

```markdown
# Lot XX — Nom

## Résultat
- ...

## Fichiers modifiés
- ...

## Invariants vérifiés
- READONLY : OK
- APIs / données : inchangées
- Routes : inchangées

## Tests
- commande : ...
- résultat : ...

## Contrôle navigateur
- desktop : ...
- tablette : ...
- mobile : ...
- console : ...
- overflow : ...

## Captures
- chemins : ...

## Commit
- SHA : ...

## Points à valider visuellement
- ...
```

---

## Premier message à produire lors du lancement

Quand l’utilisateur lance `/vertex-v4-redesign`, répondre avec :

1. branche active ;
2. état des lots ;
3. référence visuelle trouvée ou manquante ;
4. tests de départ ;
5. action proposée : audit, plan ou exécution du prochain lot ;
6. confirmation explicite qu’aucune logique métier et aucun chemin d’ordre ne seront touchés.
