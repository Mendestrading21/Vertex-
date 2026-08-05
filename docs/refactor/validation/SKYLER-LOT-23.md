# SKYLER V2 — LOT 23 — VUE LISIBLE DU POST-MORTEM + INDEX DES LOTS

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-23-postmortem-view`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `c97975a`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Le lien « détail → » de la carte Mémoire ouvrait le JSON brut de l'API — le
contenu était complet mais illisible pour un humain. Et 14 rapports de lots
(10 → 23) n'avaient aucun index consolidé.

## 2. Décision

- **`GET /memory/<decision_id>`** : page HTML lecture seule dans le shell
  produit (`render_shell`, espace Journal) — trois cartes : « Décision
  figée » (15 champs clés du ledger), « Résultat mesuré » (horizons, séances,
  MFE/MAE), « Post-mortem » (scénario contenant, classification par horizon,
  résumé, note discipline) — états honnêtes (« Aucun résultat mesuré »),
  liens retour Performance + JSON brut.
- **XSS** : TOUT contenu issu de la mémoire est échappé serveur
  (`markupsafe.escape`) — testé avec un `<script>` hostile figé en mémoire
  (sort en `&lt;script&gt;`, jamais brut).
- **Lien de la carte** mis à jour vers la vue ; l'API JSON reste intacte.
  Shell modifié → **SW `td-shell-v97` → `td-shell-v98`** + gardiens.
- **`SKYLER-INDEX.md`** : tableau consolidé des lots 10 → 23 (objectif,
  version moteur, SW, tests, verdict) + schéma de l'architecture atteinte —
  lié depuis STATUS.

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/app/routes/analysis_api.py` | vue `/memory/<id>` (rendu serveur échappé, 404 lisible) | faible |
| `vertex/ui/pages/performance_page.py` | lien carte → vue lisible | faible |
| `vertex/app/routes/system.py` + 4 gardiens + gardien lot 20 | SW v98 ; lien attendu `/memory/` | faible |
| `docs/refactor/validation/SKYLER-INDEX.md` | index consolidé (nouveau) | faible |
| `tests/test_postmortem_view_lot23.py` | 7 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_postmortem_view_lot23.py -q
6 failed, 1 passed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_postmortem_view_lot23.py -q → 7 passed
python -m pytest tests/ -q → 1488 passed, 2 skipped in 12.62s
```

Couverture : vue mesurée complète (symbole, décision, PROBABLE, H20 +14 %,
classe, version moteur) ; non mesuré honnête ; 404 lisible ; **XSS échappé
prouvé** ; lien de carte ; SW ≥ 98 ; index couvrant les 14 rapports.

## 6. Validation navigateur (Playwright, `DEMO=1 NO_IBKR=1`)

| Parcours | Taille | Résultat |
|---|---:|---|
| carte Mémoire → clic « détail → » → `/memory/<id>` | 1440×900 | page rendue « DÉCISION FIGÉE — ACN », section Post-mortem présente, 0 overflow |
| idem | 390×844 | idem |

- erreurs console : **0** ; `/api/client-log` : 0 ;
- captures : `docs/skyler/baseline/lot23-memory-view-{desktop,mobile}.png`.

## 7. Invariants vérifiés

- [x] contenu mémoire ÉCHAPPÉ serveur (XSS testé) ; lecture seule ;
- [x] états honnêtes ; ledger jamais réécrit ;
- [x] SW v98 + gardiens prospectifs ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1488/2 skipped.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1481/2 | 1488/2 |
| Post-mortem | JSON brut | page lisible dans le shell produit |
| Index des lots | aucun | `SKYLER-INDEX.md` (10 → 23) |
| SW | v97 | v98 |

## 9. Risques et limites restantes

1. La vue rend les champs clés — les blocs bruts complets (score_blocks,
   scénarios détaillés) restent accessibles via le lien JSON.
2. L'index est manuel — le tenir à jour fait partie du rituel de chaque lot.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : agrégation sectorielle du portefeuille dans
le graphe + revue /simplify des moteurs récents.

**Arrêt après ce lot — validation humaine requise.**
