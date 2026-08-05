# SKYLER V2 — LOT 17 — CORRÉLATION PARTIELLE VS SPY + GROUPES DE DÉPENDANCES

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-17-partial-correlation`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `8050284`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Le co-mouvement du knowledge graph (lot 11) utilisait la corrélation BRUTE des
rendements : deux titres qui suivent simplement le marché paraissaient
« co-mouvants en propre » — limite n° 2 documentée du lot 11. Et les
dépendances cachées restaient des paires : un groupe de 3+ titres exposés
ensemble apparaissait comme plusieurs paires sans synthèse.

## 2. Décision

- **Corrélation partielle** : quand la série SPY est disponible, chaque titre
  est régressé (OLS) sur les rendements de SPY et la corrélation se calcule
  sur les RÉSIDUS — la part de marché est retirée. Arête étiquetée
  `method: residual_vs_SPY` avec `r2` par titre (part expliquée par le
  marché) et base explicite. SPY est exclu des paires (son co-mouvement avec
  le marché est trivial — dit dans `limits`).
- **Fallback étiqueté** : sans SPY, la corrélation brute reste mais l'arête
  porte `method: raw` et `limits` avertit que le marché n'est pas contrôlé —
  jamais un fallback silencieux.
- **Groupes ≥ 3** : composantes connexes des paires de dépendances cachées →
  `hidden_groups` (titres triés, nombre de liens, base) dans
  `/api/skyler/graph`, affichés sur Portefeuille → Risque quand non vides.
- Shell modifié (page_js) → **SW `td-shell-v95` → `td-shell-v96`** + gardiens.

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/knowledge_graph.py` | `_residual_vs_market` (OLS + R²), co-mouvement à deux méthodes étiquetées, `_hidden_groups` | faible |
| `vertex/ui/pages/portfolio_page.py` | rendu des groupes dans `renderHiddenDeps` | faible |
| `vertex/app/routes/system.py` | SW v96 | faible |
| 4 gardiens SW + `test_ui_memory_graph_lot16.py` | v96 / v95 absent ; gardien lot 16 rendu prospectif (≥ 95) | faible |
| `tests/test_partial_corr_lot17.py` | 11 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_partial_corr_lot17.py -q
10 failed, 1 passed
```

Le test clé prouvait le défaut : deux titres portés UNIQUEMENT par le marché
(composantes propres indépendantes, périodes 3 et 4) formaient une arête en
corrélation brute — le test exigeait sa disparition sous résidus.

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_partial_corr_lot17.py -q → 11 passed
python -m pytest tests/ -q → 1427 passed, 2 skipped in 9.25s
```

Couverture : faux co-mouvement de marché filtré, exposition propre partagée
conservée (`residual_vs_SPY`, R² borné, base citant les résidus), fallback
`raw` étiqueté + limite dite, SPY exclu des paires, méthode toujours
étiquetée, déterminisme, groupe de 3 synthétisé (3 paires × ≥ 2 liens → 1
groupe, ≥ 6 liens), pas de groupe sous 3, graphe vide → groupes vides, rendu
UI présent, SW v96.

## 6. Validation navigateur (Playwright, `DEMO=1 NO_IBKR=1`)

| Vue | Taille | Résultat |
|---|---:|---|
| /portfolio?view=risk | 1440×900 | section rendue, état vide honnête (une seule position desk), 0 overflow |
| /portfolio?view=risk | 390×844 | idem |

- erreurs console : **0** ; `/api/client-log` : 0 ;
- captures : `docs/skyler/baseline/lot17-portfolio-risk-{desktop,mobile}.png`.

## 7. Invariants vérifiés

- [x] méthode TOUJOURS étiquetée (`residual_vs_SPY`/`raw`) — jamais de
      fallback silencieux ; R² borné [0,1] ;
- [x] variance de marché nulle → résidus = bruts, R² = 0 (rien d'inventé) ;
- [x] groupes = synthèse de liens PROUVÉS existants — aucune relation créée ;
- [x] SW v96 + gardiens (dont lot 16 rendu prospectif) ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1427/2 skipped.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1416/2 | 1427/2 |
| Co-mouvement | corrélation brute non étiquetée | résidus vs SPY étiquetés (ou raw étiqueté) |
| Dépendances | paires seulement | paires + groupes ≥ 3 |
| SW | v95 | v96 |

## 9. Risques et limites restantes

1. La régression est mono-facteur (SPY) — les expositions sectorielles pures
   restent dans les résidus (voulu : c'est exactement le lien « propre »
   recherché), mais un modèle multi-facteurs serait plus discriminant.
2. En démo, SPY n'est pas dans l'univers scanné → mode `raw` étiqueté actif ;
   en réel, dès que SPY est scanné, les résidus prennent le relais.

## 10. Rollback

`git revert` du commit (SW revient à v95 dans le même revert).

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : analyse de perturbation pour le facteur
`robustness` de la confiance (moteur bumpé).

**Arrêt après ce lot — validation humaine requise.**
