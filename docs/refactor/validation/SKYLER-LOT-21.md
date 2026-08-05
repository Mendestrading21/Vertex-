# SKYLER V2 — LOT 21 — REPRICING SPOT×IV POUR LA RED-TEAM (1.1.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-21-redteam-repricing`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `212f2bf`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat / audit du pricer

Les questions options de la red-team (Q05 « IV −10 pts », Q08 « option vs
action ») répondaient qualitativement. L'audit du moteur options (lot 6) a
confirmé qu'un pricer RÉEL et validé existe : `vertex/options/scenario_pricer.
bs_price` (Black-Scholes européen avec dividende continu, limites étiquetées
MODEL_ESTIMATE) — réutilisé tel quel, AUCUN pricer ad hoc écrit.

## 2. Décision

- **Q05 chiffrée** : candidat complet (spot, strike, DTE > 0, IV décimale
  validée) → valeur théorique repricée à IV −10 pts, spot et échéance
  inchangés — impact en %, étiqueté **F3** avec `model:
  black_scholes_european` et hypothèses listées (taux fixe 4,5 % documenté,
  dividende non modélisé, « ESTIMATION, jamais un prix broker »).
- **Q08 en grille** : niveaux RÉELS du plan (stop/TP2/TP3) × IV −10/0/+10 —
  9 cellules en % de variation du candidat (temps inchangé, theta non
  consommé — dit), plus la comparaison convexité option vs action au TP2
  (« bat / ne bat pas »). F3 + modèle.
- **Fallbacks intacts** : entrées incomplètes → réponse qualitative F2
  d'avant ; IV absente → UNANSWERED ; entrées invalides (NaN, IV négative,
  DTE nul, strike négatif, spot nul) → JAMAIS chiffré, aucun non-fini en
  sortie (testé).
- **`RED_TEAM_VERSION` 1.0.0 → 1.1.0** (contrat des réponses enrichi).
- **Garde-fou pricer** : cas manuel connu vérifié en test — ATM 1 an,
  vol 20 %, taux 0 ≈ 7,97 % du spot (`bs_price` ≈ 7,9656).

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/red_team.py` | `_reprice_inputs` (validation stricte), Q05/Q08 chiffrées + fallbacks, version 1.1.0 | faible |
| `tests/test_redteam_repricing_lot21.py` | 9 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_redteam_repricing_lot21.py -q
3 failed, 6 passed     (les 6 verts = chemins inchangés : fallbacks, UNANSWERED, pricer canonique)
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_redteam_repricing_lot21.py -q → 9 passed
python -m pytest tests/ -q → 1472 passed, 2 skipped in 33.89s
```

Couverture : cas manuel BS connu ; Q05 chiffrée (impact −27 % attendu pour
IV 30→20 sur call ATM 1 an, chiffre exact exigé dans la réponse) ; fallback F2
sans spot ; UNANSWERED sans IV inchangé ; grille Q08 avec convexité réelle
(TP2 : option +55 % vs action +12 %) ; fallback F2 sans niveaux de plan ;
5 familles d'entrées invalides refusées sans crash ni NaN ; déterminisme ;
`complete` 10/10 toujours atteignable ; version ≥ 1.1.0.

## 6. Validation runtime (`DEMO=1 NO_IBKR=1`)

`/api/skyler/ACN` : revue 1.1.0 complète — **Q05 : « IV 34 % → 24 % : valeur
théorique du candidat −30,6 % » (F3, black_scholes_european)** ; **Q08 :
grille réelle « stop/IV−10 −52 % · stop/IV0 −23 % · … · TP2/IV0 +55 % »** avec
comparaison action. `/api/client-log` : 0.

## 7. Invariants vérifiés

- [x] pricer canonique RÉUTILISÉ (aucun pricer ad hoc) + cas manuel gardé ;
- [x] unités IV explicites (décimales validées par iv_units en amont) ;
- [x] estimation F3 étiquetée avec modèle et hypothèses — jamais un prix broker ;
- [x] entrées invalides jamais chiffrées, aucun non-fini sérialisé ;
- [x] fallbacks honnêtes préservés ; version revue bumpée ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1472/2 skipped ; SW v97
      inchangé (aucune UI).

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1463/2 | 1472/2 |
| Q05 | qualitative (F2) | impact chiffré −X % (F3 + modèle) quand candidat complet |
| Q08 | qualité seule (F2) | grille 3×3 spot×IV + convexité vs action (F3) |
| RED_TEAM_VERSION | 1.0.0 | 1.1.0 |

## 9. Risques et limites restantes

1. Taux fixe 4,5 % documenté dans la revue (la courbe de taux réelle
   `RateCurve` n'est pas branchée ici pour garder la revue déterministe en
   toutes circonstances) — hypothèse listée dans chaque réponse chiffrée.
2. Grille à temps inchangé (theta non consommé) — la grille temporelle
   complète existe déjà dans `scenario_pricer.simulate` pour l'espace Options ;
   la revue red-team reste volontairement instantanée.
3. Dividende non modélisé dans la revue — dit dans la réponse.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : calibration par contexte (régime/niveau)
quand l'échantillon le permet + vue formatée du post-mortem.

**Arrêt après ce lot — validation humaine requise.**
