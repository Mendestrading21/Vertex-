# SKYLER V2 — LOT 31 : fuzz déterministe des chemins récents

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-31-deterministic-fuzz`
(base : `integration/vertex-skyler-v2` @ `6ff3729`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) fuzz déterministe ciblé, (b) RC courte
navigateur, (c) drill-down cellule de calibration, (d) surfaçage
by_catalyst_type. Choix : **(a)**, premier par valeur estimée.

- Les lots 26–30 ont livré vite plusieurs chemins neufs (propagation du
  graphe, sélection de calibration par contexte, kind figé, export) ; la
  batterie adversariale du lot 12 ne les couvrait pas.
- Les magasins runtime sont des fichiers disque : un contenu corrompu est
  un scénario RÉEL (édition manuelle, disque, sync partielle). Un moteur
  d'analyse ne doit jamais lever — il refuse honnêtement.
- Le choix s'est avéré payant : la batterie a trouvé **7 vrais crashs**
  (voir §3). (c) reste limité par l'absence de cellules mesurées en réel ;
  (b) et (d) restent au backlog.

## 2. Méthode — batterie à liste FIXE (zéro aléatoire)

`tests/test_deterministic_fuzz_lot31.py` (12 tests) : listes FIGÉES
d'entrées dégénérées (None, chaînes vides, nombres, booléens, dicts,
listes, tuples, magasins JSON corrompus) — même esprit que le lot 12,
déterminisme total, reproductible à l'identique.

Cibles : `knowledge_graph.propagate` (lot 28), `calibration_factor` /
`calibration_factor_for` / `calibration_by_context` (lots 19/22/26/28/30),
`freeze` + `catalyst_kind` (lot 30), `/api/skyler/memory/export` (lot 29).

## 3. Trouvailles RÉELLES (rouge confirmé : 7 failed / 5 passed)

| # | Crash trouvé | Entrée | Correctif (refus honnête) |
|---|--------------|--------|---------------------------|
| 1 | `TypeError: unhashable type` dans `propagate` | `node_id` dict/liste | nœud non-chaîne → `[]` |
| 2 | `TypeError` arithmétique dans `propagate` | `max_hops` None/'abc'/{} | inexploitable ou < 1 → `[]` (0 saut = 0 chemin) |
| 3 | `ValueError/TypeError` dans `propagate` | `max_paths` 'abc'/{} | inexploitable → garde MAX_PATHS par défaut, JAMAIS désactivée |
| 4 | `AttributeError` dans `_measured_hits`/`_measured_class` | magasin `decisions`/`outcomes` = chaîne ou entrées non-dict | entrées non-dict ignorées → facteur 0,50 honnête |
| 5 | `TypeError: unhashable` dans `calibration_factor_for` | `level`/`regime` dict/liste | contexte non-chaîne → jamais une clé de cellule → scope global |
| 6 | `TypeError: unhashable` dans `by_catalyst_type` | `catalyst_kind` dict (magasin corrompu) | kind non-chaîne → bucket `inconnu`, jamais deviné |
| 7 | `TypeError: unhashable` dans by_level/by_decision/by_regime | niveau/décision/régime non-chaîne | contexte non-chaîne ≠ cellule (comme un régime inconnu) |

Aussi vérifié SANS correctif nécessaire (déjà robuste) : graphes
dégénérés (None/{}/vides), `max_hops=99` (chemins simples bornés,
terminaison), déterminisme sous fuzz, `freeze` avec kinds dégénérés
(figés tels quels, l'aval survit), export avec magasins corrompus
(200 + JSON valide).

## 4. Correctifs — refus honnête, jamais d'invention

- `vertex/engines/knowledge_graph.py` (`propagate`) : validation stricte
  de `node_id`/`max_hops`/`max_paths` documentée dans la docstring —
  entrée dégénérée → `[]` ; garde de volume par défaut si `max_paths`
  inexploitable.
- `vertex/engines/decision_memory.py` : entrées non-dict des magasins
  ignorées (`_measured_hits`, `_measured_class`) ; contextes non-chaîne
  jamais des clés de cellule (`calibration_by_context`,
  `calibration_factor_for`) ; kind non-chaîne → bucket `inconnu`.

**Aucun bump de version** : aucune règle ne change sur données valides
(suite complète inchangée en est la preuve), aucun champ figé nouveau —
seules les entrées dégénérées passent du crash au refus honnête.
Aucun changement de shell → SW v101 inchangé.

## 5. Preuves

```text
python -m pytest tests/test_deterministic_fuzz_lot31.py -q
→ rouge avant correctifs : 7 failed / 5 passed
→ vert après :             12 passed in 1.97s

python -m compileall -q terminal.py vertex   → exit 0
python -m pytest tests/ -q
→ 1543 passed, 2 skipped in 9.36s            (baseline 1531 → +12)
```

## 6. Invariants tenus

- READONLY absolu ; données réelles uniquement (refus honnête : `[]`,
  0,50, `inconnu`, cellule absente — jamais une valeur inventée) ;
- zéro aléatoire (listes d'entrées FIGÉES, reproductibles) ;
- gardes de volume jamais désactivées (`MAX_PATHS`) ;
- fichiers runtime jamais commités ; gardiens prospectifs ; `main`
  intacte ; SW inchangé.

## 7. Backlog restant (candidats lot 32)

1. RC courte périodique (navigateur Playwright 8 pages +
   /api/client-log=0 + SW v101) ;
2. Surfaçage by_catalyst_type dans la carte Mémoire (badges contexte) ;
3. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
4. Étendre la batterie fuzz aux routes graphe (`/api/skyler/graph/<sym>`).

**Arrêt après ce lot — validation humaine requise.**
