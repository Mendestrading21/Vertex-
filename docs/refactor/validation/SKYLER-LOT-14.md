# SKYLER V2 — LOT 14 — PRODUCTEUR RED-TEAM DÉTERMINISTE (MOTEUR 0.4.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-14-red-team-producer`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `d63ca48`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Depuis le lot 12, la règle « S/S+ sans red-team complétée = invalide » est
appliquée par le moteur, mais rien ne PRODUISAIT de red-team : `complete`
restait `False` par défaut et le chemin S/S+ était structurellement fermé.

## 2. Problème

Sans producteur, la règle est un verrou sans clé : prudent, mais la revue
adversariale exigée par ADVERSARIAL_COMMITTEE §8 (10 questions minimum)
n'existait nulle part en tant qu'artefact vérifiable.

## 3. Décision

Nouveau moteur pur `vertex/engines/red_team.py` (`RED_TEAM_VERSION 1.0.0`) :
`review(packet, score)` évalue les 10 questions du comité DEPUIS LES DONNÉES
RÉELLES du packet — chaque question reçoit :

- une réponse FONDÉE citant les données (RSI/extrême de fenêtre pour « déjà
  dans le prix », blocs insuffisants + mode démo pour « chiffre trompeur »,
  répartition réelle des points pour « hypothèse dominante », catalyseur daté
  réel pour « retard 90 j », IV réelle pour « IV −10 pts », régime connu pour
  « risk-off », portefeuille réel (poids max, HHI) pour « exposition cachée »,
  candidat noté pour « option vs action », stop réel pour « chemin de perte »
  et « preuve d'invalidation »), avec niveau de preuve F1/F2 ;
- ou `UNANSWERED` avec la raison exacte — JAMAIS une réponse inventée.

`complete=True` UNIQUEMENT si 10/10 fondées. La revue est branchée dans
`/api/skyler/<sym>` (servie en clair dans `red_team_review`) et injectée dans
`decide()`/`build_packet()`. **`ENGINE_VERSION` 0.3.0 → 0.4.0** — la revue
produite entre dans la décision ; l'historique 0.3.0 reste séparé en mémoire.

Alternative rejetée : générer la red-team par agent linguistique — refusée,
un texte libre non fondé serait exactement la « formalité » que §8 interdit ;
le producteur déterministe cite ou se tait.

## 4. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/red_team.py` | producteur (nouveau) | faible |
| `vertex/engines/skyler_core.py` | ENGINE_VERSION 0.4.0 (commentaire versionné) | faible |
| `vertex/app/routes/analysis_api.py` | revue calculée sur le packet réel, injectée dans decide/packet, servie dans la réponse | faible |
| `tests/test_red_team_producer_lot14.py` | 12 tests rouges→verts | faible |
| `tests/test_operational_confidence_lot13.py` | gardiens de version rendus prospectifs (≥ 0.3.0, version dynamique) | faible |

## 5. Tests rouges avant correction

```text
python -m pytest tests/test_red_team_producer_lot14.py -q
ImportError — module vertex.engines.red_team inexistant
```

## 6. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_red_team_producer_lot14.py -q → 12 passed
python -m pytest tests/ -q → 1398 passed, 2 skipped in 8.87s
```

Couverture : contrat des 10 questions (ids, statuts, preuve ou raison),
`complete` seulement à 10/10, refus d'inventer sans OptionsContext (Q05/Q08),
régime UNKNOWN → Q06 ouverte, absence de stop → Q09/Q10 ouvertes, absence de
portefeuille → Q07 ouverte, réponses citant les données réelles, hypothèse
dominante détectée, déterminisme, version moteur, `decide` porte le statut,
route servant la revue.

## 7. Validation runtime (`DEMO=1 NO_IBKR=1`)

`/api/skyler/ACN` : moteur 0.4.0, revue **10/10 ANSWERED, complete=True** —
chaque réponse cite les données du moment (RSI 65 ; blocs insuffisants +
DÉMO étiquetée ; bloc technique 5/19 points ; NFP J-2 ; IV 34 % ; TREND_UP ;
2 positions, poids max 100 %, HHI 1,00 ; LEAPS qualité 60/100 ; stop 189,63 =
−4,2 % ; invalidation sous 189,63). `decision.red_team.complete=True`.
`/api/client-log` : 0 erreur.

Note d'honnêteté : la revue complète n'assouplit RIEN — le niveau reste plafonné
par les blocs insuffisants (fondamentaux non branchés), donc S/S+ demeure
inaccessible tant que le dossier est incomplet. La red-team retire le verrou
« sans clé », pas les autres garde-fous.

## 8. Invariants vérifiés

- [x] jamais une réponse inventée — donnée absente = question ouverte, raison dite ;
- [x] `complete` seulement à 10/10 fondées ;
- [x] version moteur bumpée, historique séparé ;
- [x] READONLY, aucun ordre, `main` intacte, Constitution intouchée ;
- [x] suite complète verte (1398/2 skipped) ; SW v94 inchangé (aucune UI).

## 9. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1386/2 | 1398/2 |
| ENGINE_VERSION | 0.3.0 | 0.4.0 |
| Red-team | règle sans producteur | revue déterministe 10 questions, servie et injectée |

## 10. Risques et limites restantes

1. Les réponses sont des constats orientés risque, pas des simulations
   chiffrées (l'impact exact d'une IV −10 pts exigerait le repricing spot×temps×IV
   du lot 6 branché ici — amélioration future).
2. Q08 (option vs action) répond sur la qualité du candidat, pas sur une
   matrice comparative complète — dit dans la réponse.
3. La revue complète ne crée pas de S/S+ tant que les fondamentaux ne sont pas
   branchés — voulu.

## 11. Rollback

`git revert` du commit du lot.

## 12. Verdict

`GO`

## 13. Prochaine étape autorisée

Bloc suivant du travail continu : LOT 15 — série datée par séance pour les
horizons réels de la mémoire.

**Arrêt après ce lot — validation humaine requise.**
