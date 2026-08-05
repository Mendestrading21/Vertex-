# SKYLER V2 — LOT 16 — SURFAÇAGE UI : MÉMOIRE DÉCISIONNELLE ET DÉPENDANCES CACHÉES

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-16-ui-surfacing`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `ff31243`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

La mémoire décisionnelle (lot 10/13/15) et le knowledge graph (lot 11/16)
n'existaient qu'en API — aucun écran ne les montrait au trader.

## 2. Décision

Deux surfaçages, chacun dans son domicile canonique (une donnée = un seul
domicile ; Aujourd'hui résume, les espaces expliquent — vérifié par gardien) :

- **Performance (`/journal`, vue overview)** : carte « Mémoire décisionnelle »
  sous la carte Calibration existante — n décisions figées, résultats mesurés,
  tableau PAR VERSION DE MOTEUR (décisions, répartition, mesurées, erreurs
  classées), badges des 10 biais surveillés (DETECTE/ABSENT/INSUFFISANT avec
  base au survol), propositions `EN_ATTENTE_VALIDATION_HUMAINE`, badge DÉMO,
  état vide honnête (« Aucune décision figée pour le moment »).
- **Portefeuille → Risque** : section « Dépendances cachées (Knowledge
  Graph) » — paires ≥ 2 liens indépendants avec base par lien, état vide
  honnête, questions de recherche (relations non documentées, jamais
  inventées), fraîcheur + badge DÉMO.

Shell visible modifié → **service worker `td-shell-v94` → `td-shell-v95`** +
mise à jour des 4 gardiens (et assertions vN-1 absent).

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/ui/pages/performance_page.py` | carte + `loadMemory()` + orchestration | faible |
| `vertex/ui/pages/portfolio_page.py` | `renderHiddenDeps()` + dispatch vue risk | faible |
| `vertex/app/routes/system.py` | SW v95 | faible |
| `tests/test_production_guards_canonical.py`, `test_reconstruction_today.py`, `test_redesign_ui.py`, `test_ui_v3.py` | gardiens v95 / v94 absent | faible |
| `tests/test_ui_memory_graph_lot16.py` | 6 gardiens du lot (rouges→verts) | faible |

Aucune apostrophe française non échappée dans les chaînes JS ajoutées (les
libellés ont été formulés sans apostrophe — le piège connu des `_JS = r"""`).

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_ui_memory_graph_lot16.py -q
4 failed, 2 passed
(les 2 verts sont les invariants préexistants : calibration intacte, graphe
absent d'Aujourd'hui — voulus vrais avant ET après)
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_ui_memory_graph_lot16.py -q → 6 passed
python -m pytest tests/ -q → 1416 passed, 2 skipped in 9.25s
```

## 6. Validation navigateur (Playwright, `DEMO=1 NO_IBKR=1`)

| Vue | Taille | Résultat | Capture |
|---|---:|---|---|
| /journal (Performance) | 1440×900 | carte Mémoire rendue : « 1 décision figée · 0 résultat mesuré · DÉMO », tableau moteur 0.4.0, biais badges ; 0 overflow | `docs/skyler/baseline/lot16-performance-desktop.png` |
| /journal | 390×844 | idem, tableau responsive ; 0 overflow | `lot16-performance-mobile.png` |
| /portfolio?view=risk | 1440×900 | section Dépendances cachées rendue, état vide honnête + questions de recherche ; 0 overflow | `lot16-portfolio-risk-desktop.png` |
| /portfolio?view=risk | 390×844 | idem ; 0 overflow | `lot16-portfolio-risk-mobile.png` |

- erreurs console : **0** (les 4 pages, deux tailles) ;
- `/api/client-log` : `{"count":0,"errors":[]}` ;
- données affichées : réelles (la décision ACN figée sous 0.4.0 pendant la
  preuve), badge DÉMO présent car serveur démo — jamais présenté comme réel.

## 7. Invariants vérifiés

- [x] une donnée = un seul domicile (gardien : `/api/skyler/graph` absent
      d'Aujourd'hui) ; la carte Calibration existante reste intacte (gardien) ;
- [x] états vides/erreur honnêtes ; DÉMO étiquetée ; rien d'inventé côté client ;
- [x] SW bumpé v95 + 4 gardiens à jour + v94 absent du body ;
- [x] apostrophes JS échappées/évitées ; 0 erreur console ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1416/2 skipped.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1410/2 | 1416/2 |
| Service worker | v94 | v95 |
| Mémoire/graph visibles | API seulement | Performance + Portefeuille/Risque |

## 9. Risques et limites restantes

1. La carte Mémoire liste les erreurs classées agrégées — le détail par
   décision (drill-down) reste API-only (`/api/skyler/memory`).
2. Les dépendances cachées dépendent des positions desk : avec une seule
   position réelle, l'état vide honnête est l'affichage normal.

## 10. Rollback

`git revert` du commit + retour SW v94 automatique (même commit).

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : LOT 17 — corrélation partielle vs SPY dans
le knowledge graph + synthèse des groupes ≥ 3.

**Arrêt après ce lot — validation humaine requise.**
