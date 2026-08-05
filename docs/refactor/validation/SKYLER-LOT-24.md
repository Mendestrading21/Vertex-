# SKYLER V2 — LOT 24 — EXPOSITION SECTORIELLE DU GRAPHE (SW v99)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-24-sector-exposure`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `14b1745`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Le knowledge graph reliait positions et secteurs mais n'agrégeait pas
l'EXPOSITION du portefeuille par secteur ; et un groupe caché entièrement
mono-secteur n'était pas distingué d'un groupe inter-sectoriel — alors que
c'est précisément la concentration la plus dangereuse.

## 2. Décision

- **`sector_exposure`** dans `knowledge_graph.build(..., quotes=)` : positions
  RÉELLES agrégées par secteur déclaré — titres, nombre de positions, poids en
  % SEULEMENT si TOUTES les positions ont une cote (un poids partiel serait un
  mensonge — sinon `None` avec raison « cote absente, jamais estimé ») ;
  titre hors watchlist → `HORS_WATCHLIST` étiqueté.
- **`sector_concentration`** sur les groupes cachés : un groupe ≥ 3 entièrement
  dans un même secteur déclaré porte `sector_concentration: true`, son
  `sector`, et la mention CONCENTRATION SECTORIELLE dans sa base.
- **Route** : les cotes réelles du scan sont passées au graphe.
- **UI** : bloc « Exposition sectorielle du portefeuille » dans la section
  Dépendances cachées (Portefeuille → Risque) — shell modifié →
  **SW `td-shell-v98` → `td-shell-v99`** + gardiens.

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/knowledge_graph.py` | `_sector_exposure`, flag de concentration des groupes, param `quotes` | faible |
| `vertex/app/routes/analysis_api.py` | cotes réelles passées au graphe | faible |
| `vertex/ui/pages/portfolio_page.py` | bloc exposition dans `renderHiddenDeps` | faible |
| SW + 4 gardiens | v99 | faible |
| `tests/test_sector_exposure_lot24.py` | 10 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_sector_exposure_lot24.py -q → 10 failed
```

Note honnête : le test « groupe multi-secteurs non étiqueté » a d'abord
révélé un comportement CORRECT du moteur (en secteurs mixtes, les paires
croisées perdent un lien et le groupe se dissout légitimement) — le FIXTURE a
été corrigé (catalyseur commun daté ajouté pour conserver 2 liens), pas le
moteur.

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_sector_exposure_lot24.py -q → 10 passed
python -m pytest tests/ -q → 1498 passed, 2 skipped in 12.57s
```

Couverture : poids exacts avec cotes complètes (66,7/33,3 %) ; sans cotes →
comptage seul avec raison ; hors watchlist étiqueté ; positions vides → {} ;
déterminisme ; groupe mono-secteur flaggé avec secteur ; groupe multi-secteurs
jamais flaggé ; route sert `sector_exposure` ; rendu UI ; SW ≥ 99.

## 6. Validation navigateur (Playwright, `DEMO=1 NO_IBKR=1`)

| Vue | Taille | Résultat |
|---|---:|---|
| /portfolio?view=risk | 1440×900 | bloc rendu : « HORS_WATCHLIST — ACN (1 position · poids n/d — cote absente, jamais estimé) » — honnêteté totale (la 2e position du desk n'a pas de cote) ; 0 overflow |
| idem | 390×844 | idem |

- erreurs console : **0** ; client-log : 0 ; captures `lot24-*.png`.

## 7. Invariants vérifiés

- [x] poids jamais partiel/estimé (tout coté ou None avec raison) ;
- [x] secteur = déclaration de la watchlist citée, jamais deviné ;
- [x] concentration = synthèse de liens PROUVÉS ;
- [x] SW v99 + gardiens ; READONLY, `main` intacte ; suite 1498/2.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1488/2 | 1498/2 |
| Exposition sectorielle | absente du graphe | agrégée, honnête, affichée |
| Groupes | non qualifiés | concentration sectorielle étiquetée |
| SW | v98 | v99 |

## 9. Risques et limites restantes

1. Le poids exige toutes les cotes — voulu ; en réel avec l'univers scanné
   complet, les poids s'afficheront.
2. Watchlist sectorielle statique (limite connue du lot 11) — `HORS_WATCHLIST`
   la rend au moins visible côté portefeuille.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant : revue /simplify des moteurs `decision_memory`/`skyler_core`
(sans changement de comportement) + découpes calibration supplémentaires.

**Arrêt après ce lot — validation humaine requise.**
