# SKYLER V2 — LOT RUNBOOK

## Règle centrale

Un lot est une unité de décision, de code, de validation et de revue.

Claude ne doit jamais exécuter deux lots en une seule passe, même si le premier semble simple.

## Préflight commun

Avant chaque lot :

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git fetch origin --prune
```

Puis :

1. confirmer que la branche n’est pas `main` ;
2. confirmer qu’aucun fichier étranger au lot n’est modifié ;
3. lire le rapport du lot précédent ;
4. vérifier que son verdict est `GO` ;
5. vérifier qu’une validation humaine explicite existe ;
6. lire tous les fichiers de référence du skill ;
7. annoncer le périmètre exact et les interdictions du lot.

Si une condition échoue : `NO-GO`, aucun code.

## AUDIT — Convergence des branches

### Entrées

- `main`
- `agent/vertex-total-rebuild`
- `agent/vertex-neon-glass-graphs`
- `integration/vertex-skyler-v2`
- branches V4 encore ouvertes

### Commandes indicatives

```bash
git log --left-right --cherry-pick --oneline A...B
git diff --stat A...B
git diff --name-status A...B
git merge-base A B
```

### Livrable

`docs/skyler/BRANCH_CONVERGENCE_AUDIT.md`

Inclure : SHA, ancêtre commun, commits uniques, fichiers/moteurs/pages/tests divergents, risques, source canonique par domaine et plan de récupération.

Aucune fusion automatique.

### Fin

Arrêt obligatoire.

## LOT 0 — Baseline

### But

Mesurer l’état exact avant changement métier.

### Validation

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
DEMO=1 NO_IBKR=1 python terminal.py
```

Contrôler `/healthz`, `/api/client-log`, routes, huit espaces, démo, sans IBKR, mobile 390, desktop 1440/1920 et READONLY.

### Livrables

- `docs/skyler/BASELINE.md`
- `docs/skyler/STATUS.md`
- captures baseline
- aucun changement moteur

## LOT 1 — Correctness options

### Audit ciblé

Inspecter moteurs options, routes, board, champs IV/primes/quantités/multiplicateurs, profils et tests mathématiques.

### Séquence

1. test rouge short call illimité ;
2. `max_loss_unbounded` ;
3. unités IV explicites ;
4. normalisation typée ;
5. migration des points de jonction ;
6. filtrage profil ;
7. refus structurés ;
8. alignement UI/API ;
9. suite complète ;
10. rapport ;
11. arrêt.

### Interdictions

Pas de scoring global, refonte visuelle, nouvelles sources ou Constitution V2.

## LOT 2 — Constitution V2

1. lire V1 ;
2. créer V2 via versioning ;
3. V1 immuable ;
4. intégrer 8–15 positions, niveaux et LEAPS ;
5. tests validation/diff/rollback ;
6. vérifier moteur exécutif ;
7. rapport ;
8. arrêt.

## LOT 3 — Market Intelligence

1. inventorier sources ;
2. schéma `MarketContext` ;
3. source/fraîcheur ;
4. données réelles uniquement ;
5. dimensions progressives ;
6. transitions de régime ;
7. diff session ;
8. tests missing/stale/conflicted ;
9. rapport ;
10. arrêt.

## LOT 4 — News, catalyseurs et anomalies

1. OHLCV canonique ;
2. retirer reconstructions artificielles des chemins décisionnels ;
3. événements normalisés ;
4. déduplication news ;
5. fait/interprétation/impact ;
6. révisions si source disponible ;
7. anomalies multi-domaines ;
8. confirmation/persistance/faux positifs ;
9. rapport ;
10. arrêt.

## LOT 5 — Skyler Core

1. contrats typés ;
2. builders purs ;
3. claims structurés ;
4. comité contradictoire ;
5. contradiction detector ;
6. hard gates ;
7. score /40 ;
8. scénarios ;
9. audit trail ;
10. réponse déterministe ;
11. Claude limité à la rédaction ;
12. tests déterminisme/non-invention ;
13. rapport ;
14. arrêt.

## LOT 6 — Options Intelligence

1. TACTICAL/SWING/LEAPS ;
2. calls/puts autorisés ;
3. liquidité ;
4. vol surface/term/skew ;
5. Greeks avancés ;
6. GEX/dealer et limites ;
7. spot × temps × IV ;
8. earnings/IV crush ;
9. PoP et doublement séparés ;
10. comparaison action/option ;
11. rapport ;
12. arrêt.

## LOT 7 — Portfolio Intelligence

1. positions canoniques ;
2. budget de risque ;
3. niveau/sizing ;
4. concentration/corrélation ;
5. impact marginal ;
6. remplacement ;
7. renforcement gagnant uniquement ;
8. sécurisation partielle ;
9. stress ;
10. Greeks portefeuille ;
11. tests garde-fous ;
12. rapport ;
13. arrêt.

## LOT 8 — Neon Glass

Une sous-PR par espace ou groupe validé.

Pour chaque page : capture avant, mission, source canonique, hiérarchie réponse/preuve/expertise, composants réutilisés, suppression doublons, implémentation, responsive, accessibilité, console, capture après, rapport et arrêt.

## LOT 9 — Scénarios et calibration

1. geler fonctionnalités ;
2. ledger de décisions ;
3. probabilités versionnées ;
4. Brier/log loss/calibration bins ;
5. MAE/MFE ;
6. résultats régime/niveau/instrument ;
7. faux positifs ;
8. benchmark ;
9. tests look-ahead ;
10. rapport ;
11. arrêt.

## LOT 10 — Mémoire et discipline décisionnelle

### But

Transformer le journal en mémoire institutionnelle sans auto-modification des règles.

### Séquence

1. figer les décisions historiques avec version moteur ;
2. capturer thèse, déclencheur, invalidation et scénarios ;
3. observer résultat aux horizons déclarés ;
4. séparer erreur de modèle, erreur de données, erreur de discipline et variance normale ;
5. détecter biais récurrents ;
6. produire recommandations d’amélioration ;
7. exiger validation humaine avant changement de règle ;
8. tests immutabilité/versioning ;
9. rapport ;
10. arrêt.

### Tests critiques

- aucune décision historique réécrite ;
- aucun résultat futur dans les données d’entrée ;
- aucun ajustement automatique de Constitution ;
- comparaison entre versions séparée.

## LOT 11 — Knowledge Graph et recherche institutionnelle

### But

Relier les entités importantes pour détecter dépendances, propagation de catalyseurs et risques cachés.

### Entités

- sociétés ;
- secteurs ;
- industries ;
- thèmes ;
- fournisseurs ;
- clients ;
- concurrents ;
- matières premières ;
- régions ;
- réglementations ;
- catalyseurs ;
- risques.

### Séquence

1. schéma relation typé ;
2. provenance par relation ;
3. date et confiance ;
4. ingestion uniquement depuis sources disponibles ;
5. interdiction d’inventer une relation ;
6. propagation d’impact explicable ;
7. questions de recherche ;
8. détection de concentration cachée portefeuille ;
9. tests cycles/doublons/provenance ;
10. rapport ;
11. arrêt.

## LOT 12 — Red-team et release candidate

### But

Chercher activement les erreurs avant toute promotion.

### Séquence

1. red-team de chaque S/S+ ;
2. chocs marché/secteur/volatilité/liquidité ;
3. retard ou échec catalyseur ;
4. IV crush et gap ;
5. audit mathématique options indépendant ;
6. audit données, sécurité et confidentialité ;
7. audit READONLY ;
8. audit déterminisme ;
9. audit accessibilité/performance/responsive ;
10. démo/sans IBKR/stale/offline ;
11. documentation release/rollback ;
12. validation appareil physique ;
13. RC brouillon ;
14. arrêt avant `main`.

## `decision-review <SYMBOL>`

Mission analytique sans changement de code :

1. construire `SkylerPacket` ;
2. exécuter analystes ;
3. qualité et hard gates ;
4. contradictions ;
5. scénarios ;
6. action/call/put/attendre ;
7. portefeuille ;
8. avocat du diable ;
9. décision déterministe ;
10. faits/estimations/interprétations séparés.

Ne jamais passer d’ordre ou modifier le journal historique.

## `red-team <SYMBOL|DECISION_ID>`

1. préserver décision initiale ;
2. meilleur dossier adverse ;
3. choc marché ;
4. retard catalyseur ;
5. IV crush ;
6. gap/liquidité ;
7. corrélation portefeuille ;
8. hypothèse fragile ;
9. conditions de baisse score/confiance ;
10. rapport séparé.

## Discipline de commit

- commits ciblés ;
- message `type(skyler): description` ;
- pas de `git add -A` avec changements étrangers ;
- pas d’amend/rebase partagé sans accord ;
- pas de captures temporaires mélangées au code ;
- diff relu avant push.

## Discipline de PR

Le corps précise lot, objectif, périmètre/hors périmètre, défaut, solution, fichiers, tests, invariants, captures, contradictions, risques, rollback et validation humaine manquante.

Toujours ouvrir en brouillon.
