# SKYLER V2 — LOT 25 — REVUE DE SIMPLIFICATION DES MOTEURS

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-25-simplify`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `a9a23f2`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Périmètre

Revue de dette ciblée sur les moteurs du travail continu :
`vertex/engines/decision_memory.py` (678 lignes), `vertex/engines/skyler_core.py`
(628 lignes) — et `vertex/engines/red_team.py` en voisin immédiat (duplication
évidente constatée en lisant). Règle absolue : AUCUN changement de
comportement — la suite complète (1498) est le filet et doit rester
exactement verte, sans aucun test modifié.

## 2. Trouvailles et corrections appliquées

1. **Docstring de `skyler_core` désynchronisée** : elle décrivait le pipeline
   du lot 5 (0.1.0) sans red-team, état opérationnel, confiance factorisée,
   perturbation ni calibration. Réécrite pour refléter 0.7.0 (pipeline complet,
   règle « changement de règle = bump de version »).
2. **Docstring de `decision_memory` désynchronisée** : mentionnait « le moteur
   0.1.0 » pour les horizons et ignorait le log de séances daté (lot 15).
   Mise à jour (« le moteur courant », séances réelles + empreinte en secours).
3. **Formule du facteur de calibration dupliquée** (`0,50 + 0,40 × hit rate`
   dans `calibration_factor` ET `_context_cell`) : extraite en `_hit_factor()`
   — une seule source de vérité pour la formule.
4. **Boucle de mesure dupliquée** : `calibration_factor` réimplémentait
   l'itération decisions→version→`_measured_class` déjà factorisée dans
   `_measured_hits` (lot 22) — réécrite pour la réutiliser (le booléen hit de
   `_measured_hits` est exactement `classe ∈ {DECISION_CORRECTE,
   VARIANCE_NORMALE}` : équivalence prouvée par la suite).
5. **Réponses qualitatives tripliquées dans `red_team`** : les fallbacks F2 de
   Q05 et Q08 étaient copiés-collés à 3 et 3 exemplaires — extraits en
   `_q05_qualitative()` / `_q08_qualitative()` (textes identiques au caractère
   près, vérifiés par les tests du lot 21 qui épinglent le contenu).

## 3. Examiné et volontairement NON modifié

- `_num`/`_fin` existent en 3 variantes locales (decision_memory,
  knowledge_graph, red_team) — les partager créerait un couplage inter-moteurs
  pour 5 lignes ; l'idiome local reste préférable (documenté ici).
- `operational_state`/`confidence`/`perturbation_analysis` : structure claire,
  aucune branche morte détectée (la branche REDUIRE morte avait déjà été
  supprimée au lot 13 sous gardien).
- Les sections de `decision_memory` suivent l'ordre historique des lots
  (20 avant 19 dans le fichier) — réordonner serait un churn sans gain
  (les définitions sont résolues à l'appel).

## 4. Validation

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1498 passed, 2 skipped in 12.59s
```

**Exactement** la baseline d'avant-lot — aucun test modifié, aucun test
ajouté : c'est la définition d'un lot de simplification réussi. Les tests des
lots 19/21/22 épinglent les textes de base et les valeurs des facteurs — ils
prouvent l'équivalence au caractère près.

## 5. Invariants vérifiés

- [x] zéro changement de comportement (suite identique) ;
- [x] aucune version bumpée (aucune règle changée — seules les docstrings et
      la factorisation interne ont bougé) ;
- [x] READONLY, aucun ordre, `main` intacte ; SW v99 inchangé.

## 6. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1498/2 | 1498/2 (identique — voulu) |
| Duplication formule calibration | 2 copies | 1 (`_hit_factor`) |
| Duplication boucle de mesure | 2 copies | 1 (`_measured_hits`) |
| Fallbacks red-team copiés | 6 blocs | 2 helpers |
| Docstrings à jour | 2 périmées | à jour (0.7.0, lot 15) |

## 7. Risques et limites restantes

1. Aucun risque introduit (pas de changement de comportement).
2. Dette restante assumée : ordre historique des sections de decision_memory ;
   helpers numériques locaux par moteur.

## 8. Rollback

`git revert` du commit du lot.

## 9. Verdict

`GO`

## 10. Prochaine étape autorisée

Bloc suivant : calibration par régime (figer le régime dans le record mémoire)
+ badge de portée de calibration dans la carte Mémoire.

**Arrêt après ce lot — validation humaine requise.**
