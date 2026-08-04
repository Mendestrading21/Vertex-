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

Inclure :

- SHA de chaque branche ;
- ancêtre commun ;
- commits uniques ;
- fichiers divergents ;
- moteurs divergents ;
- pages divergentes ;
- tests divergents ;
- risques ;
- source canonique par domaine ;
- plan de récupération ;
- aucune fusion automatique.

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

Contrôler :

- `/healthz`
- `/api/client-log`
- routes principales ;
- 8 espaces ;
- mode démo ;
- sans IBKR ;
- mobile 390 ;
- desktop 1440/1920 ;
- READONLY.

### Livrables

- `docs/skyler/BASELINE.md`
- `docs/skyler/STATUS.md`
- captures baseline ;
- aucun changement de moteur.

## LOT 1 — Correctness options

### Audit ciblé

Inspecter :

- `vertex/engines/multileg_lab.py`
- moteurs options ;
- routes d’analyse ;
- tests mathématiques ;
- format du board ;
- champs IV, prime, coût, quantité, multiplicateur ;
- profils stratégiques.

### Séquence

1. écrire un test rouge pour short call illimité ;
2. ajouter `max_loss_unbounded` sans casser les sorties existantes ;
3. écrire les tests d’unités IV explicites ;
4. créer la normalisation typée ;
5. migrer les points de jonction ;
6. filtrer les stratégies selon le profil ;
7. ajouter refus structurés ;
8. vérifier UI/API ;
9. exécuter suite complète ;
10. rapport `SKYLER-LOT-01.md` ;
11. arrêt.

### Interdictions

- pas de nouveau scoring global ;
- pas de refonte visuelle ;
- pas de nouvelles sources de marché ;
- pas de Constitution V2 dans la même PR.

## LOT 2 — Constitution V2

### Séquence

1. lire la V1 ;
2. créer V2 par mécanisme de versioning ;
3. ne jamais modifier V1 ;
4. intégrer 8–15 positions, niveaux et LEAPS ;
5. tests de validation ;
6. tests de diff ;
7. tests de rollback ;
8. vérifier le moteur exécutif ;
9. rapport ;
10. arrêt.

## LOT 3 — Market Intelligence

### Séquence

1. inventorier les sources actuelles ;
2. créer le schéma `MarketContext` ;
3. normaliser source/fraîcheur ;
4. connecter seulement les données réellement disponibles ;
5. ajouter dimensions progressivement ;
6. transition de régime ;
7. diff depuis session précédente ;
8. tests missing/stale/conflicted ;
9. rapport ;
10. arrêt.

Ne jamais remplir une dimension absente avec une approximation non étiquetée.

## LOT 4 — News, catalyseurs et anomalies

### Séquence

1. choisir la série OHLCV canonique ;
2. supprimer les reconstructions artificielles des chemins décisionnels ;
3. créer événements normalisés ;
4. dédupliquer les news ;
5. distinguer fait, interprétation et impact ;
6. ajouter révisions si source disponible ;
7. tester anomalies sur vraies barres et données manquantes ;
8. rapport ;
9. arrêt.

## LOT 5 — Skyler Core

### Séquence

1. contrats typés ;
2. builders purs ;
3. contradiction detector ;
4. hard gates ;
5. score /40 ;
6. scénarios ;
7. audit trail ;
8. réponse déterministe ;
9. couche Claude limitée à la rédaction ;
10. tests de déterminisme ;
11. tests de non-invention ;
12. rapport ;
13. arrêt.

## LOT 6 — Options Intelligence

### Séquence

1. séparer TACTICAL/SWING/LEAPS ;
2. scanner calls/puts autorisés ;
3. liquidité ;
4. vol surface/term/skew ;
5. Greeks avancés ;
6. GEX/dealer avec conventions ;
7. scénarios spot × temps × IV ;
8. earnings/IV crush ;
9. probabilité de doublement ;
10. calibration/labels ;
11. rapport ;
12. arrêt.

## LOT 7 — Portfolio Intelligence

### Séquence

1. contrat positions canonique ;
2. budget de risque ;
3. niveau et sizing ;
4. concentration/corrélation ;
5. impact marginal ;
6. replacement logic ;
7. renforcement gagnant seulement ;
8. sécurisation partielle ;
9. stress ;
10. tests de garde-fous ;
11. rapport ;
12. arrêt.

## LOT 8 — Neon Glass

Une sous-PR par espace ou groupe validé.

Pour chaque page :

1. capture avant ;
2. mission ;
3. source canonique ;
4. hiérarchie réponse/preuve/expertise ;
5. composants existants réutilisés ;
6. suppression des doublons ;
7. implémentation ;
8. desktop/tablette/mobile ;
9. clavier/reduced-motion ;
10. console ;
11. capture après ;
12. rapport ;
13. arrêt avant page suivante si la validation humaine l’exige.

## LOT 9 — Calibration et RC

### Séquence

1. geler les fonctionnalités ;
2. mesurer les probabilités ;
3. Brier/calibration ;
4. performance par régime/niveau ;
5. MAE/MFE ;
6. dérive ;
7. faux positifs ;
8. benchmark ;
9. sécurité ;
10. performance ;
11. accessibilité ;
12. responsive ;
13. docs release/rollback ;
14. RC brouillon ;
15. arrêt avant `main`.

## Discipline de commit

- commits courts et ciblés ;
- message `type(skyler): description` ;
- ne pas utiliser `git add -A` si le worktree contient des changements étrangers ;
- ne pas amender ou rebase une branche partagée sans accord ;
- ne pas mélanger captures temporaires et code produit ;
- vérifier le diff avant push.

## Discipline de PR

Le corps de PR doit préciser :

- lot ;
- objectif ;
- périmètre ;
- hors périmètre ;
- défaut reproduit ;
- solution ;
- fichiers ;
- tests exacts ;
- invariants ;
- captures ;
- risques ;
- rollback ;
- validation humaine manquante.

Toujours ouvrir en brouillon.
