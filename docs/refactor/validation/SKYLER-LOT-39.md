# SKYLER V2 — LOT 39 : drill-down cellule de calibration

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-39-cell-drilldown`
(base : `integration/vertex-skyler-v2` @ `158831b`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) drill-down cellule, (b) RC courte étendue,
(c) autre. Choix : **(a)** — le dernier grand chantier du backlog mémoire.

- Un badge dit « niveau=A : 0,82 (25 mesures) » — mais QUELLES 25
  décisions ? Sans drill-down, la calibration reste une boîte noire :
  invérifiable par le trader, donc non auditable. Le lot rend chaque
  cellule TRAÇABLE jusqu'aux records immuables qui la composent.
- La limite connue (« pas de cellules mesurées en réel ») n'empêche pas
  de livrer l'API TESTÉE sur données construites — même méthode que les
  lots 26/28/30.

## 2. Périmètre livré

### 2.1 Moteur — règle d'appartenance en SOURCE UNIQUE

`vertex/engines/decision_memory.py` :

- `CONTEXT_GROUPS` (5 groupes) + **`_cell_key(group, record)`** : la
  règle d'appartenance d'un record à une cellule, extraite en UN SEUL
  endroit — consommée par `calibration_by_context` (recâblée dessus,
  comportement identique prouvé par la suite) ET par le nouveau
  `cell_decisions` (anti-divergence structurelle : le badge et le
  drill-down ne peuvent plus diverger) ;
- `_measured_records` factorisé (`_measured_hits` réexprimé dessus) ;
- **`cell_decisions(memory, version, group, key)`** : décisions MESURÉES
  de la cellule — id, titre, séance, contextes figés, hit/miss par
  record, comptes ; groupe inconnu ou clé dégénérée → None ; jamais de
  mélange de versions ; lecture seule.

### 2.2 Route — `GET /api/skyler/memory/cell/<group>/<key>`

404 STRUCTURÉS : `groupe_inconnu` (avec la liste des groupes valides),
`cellule_inconnue` (aucune décision mesurée ne la forme). Cellule
existante → payload drill-down + résumé `cell` (le même que le badge).
Jamais 500 (magasin corrompu toléré — gardes lot 34).

### 2.3 UI — badges cliquables

Les badges de calibration par contexte (carte Mémoire) deviennent des
liens vers leur cellule (`encodeURIComponent` sur groupe et clé, title
enrichi « clic : décisions mesurées de la cellule ») — même mécanique de
rendu, zéro second renderer. Shell visible → **SW v104 → v105** +
4 gardiens.

## 3. Méthode — rouge d'abord

`tests/test_calibration_drilldown_lot39.py` (10 tests) écrit AVANT ;
confirmé rouge : **9 failed / 1 passed**. Après : **10 passed**.

Couverture : comptes exacts de la cellule earnings (25 mesures / 20
hits — fixture lot 30) ; **anti-divergence prouvée sur TOUTES les
cellules publiées** (chaque cellule de `calibration_by_context` retrouve
exactement son `n_measured` par le drill-down) ; groupe/clé dégénérés
refusés ; séparation de versions ; route 200 avec résumé joint, 404
structurés × 2, magasin corrompu sans 500 ; badges liés ; SW ≥ v105.

## 4. Preuves

```text
python -m pytest tests/test_calibration_drilldown_lot39.py -q → 10 passed
python -m compileall -q terminal.py vertex                    → exit 0
python -m pytest tests/ -q → 1586 passed, 2 skipped           (1576 → +10)

tools/rc_short_audit.js : 8 pages HTTP 200 · console_err=0 · pageerror=0
  /api/client-log n=0 · sw.js td-shell-v105 · RC COURTE : GO — 0 défaut.

Live : GET /api/skyler/memory/cell/by_level/INEXISTANT → 404
       GET /api/skyler/memory/cell/by_magie/A          → 404
```

Moteur 0.9.0 inchangé : la refactorisation `_cell_key` ne change AUCUN
comportement de calibration (mêmes cellules, mêmes comptes — suite verte
inchangée sur les tests des lots 22/26/28/30) ; le drill-down lit, ne
décide rien.

## 5. Invariants tenus

- source unique de la règle d'appartenance (anti-divergence prouvée) ;
- records immuables, lecture seule, jamais de mélange de versions ;
- 404 structurés, jamais 500 ; données réelles uniquement (cellule
  inexistante → 404 dit, jamais une cellule vide inventée) ;
- SW bump v105 + 4 gardiens ; RC courte GO ; READONLY absolu ;
- fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 40)

1. RC courte étendue (`/memory/<id>` + un badge cellule dans le
   parcours de `tools/rc_short_audit.js`) ;
2. Vue HTML lisible de la cellule (aujourd'hui : JSON — suffisant pour
   l'audit, une vue mise en forme est un confort futur) ;
3. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
