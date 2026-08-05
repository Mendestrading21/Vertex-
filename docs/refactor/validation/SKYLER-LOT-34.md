# SKYLER V2 — LOT 34 : fuzz HTTP graphe/mémoire

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-34-http-fuzz`
(base : `integration/vertex-skyler-v2` @ `8033892`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) fuzz HTTP graphe/mémoire, (b) santé du
ledger multi-versions, (c) drill-down cellule. Choix : **(a)**, premier
par valeur.

- Le lot 31 a durci les MOTEURS contre les entrées dégénérées ; les
  ROUTES HTTP restaient la surface exposée non couverte (c'est par
  l'iPhone/le LAN que le trader les touche). Contrat : JAMAIS de 500 —
  clamp dit, 404 structuré, aucun reflet XSS.
- Le choix s'est encore avéré payant : **4 vrais crashs 500 trouvés**
  (voir §3). (b) est partiellement couvert au passage (la liste mémoire
  survit désormais à un magasin mêlant entrées valides et corrompues) ;
  (c) toujours limité par l'absence de cellules mesurées.

## 2. Méthode — batterie HTTP à liste FIXE (zéro aléatoire)

`tests/test_http_fuzz_lot34.py` (8 tests) : listes FIGÉES — hops
dégénérés ('abc', '', '-1', '0', '99', '1e9', '3.5', 'None'), symboles
dégénérés (500 chars, espaces, apostrophe, `<script>`, %00, unicode,
'..'), ids dégénérés (500 chars, XSS, traversée encodée `%2e%2e%2f`,
espaces, 'null'), traversée brute `../../etc/passwd`, magasin mémoire
corrompu (entrées non-dict mêlées à une entrée valide).

## 3. Trouvailles RÉELLES (rouge confirmé : 4 failed / 4 passed)

| # | Crash 500 trouvé | Chemin | Correctif (refus honnête) |
|---|------------------|--------|---------------------------|
| 1 | `AttributeError` passe de mesure | `GET /api/skyler/memory` avec magasin corrompu | entrées non-dict ignorées dans la boucle de mesure (route) |
| 2 | `AttributeError` `find_decision`/`find_outcome` | `GET /api/skyler/memory/<id>` et `/memory/<id>` avec magasin corrompu | garde isinstance — l'entrée valide reste servie |
| 3 | `AttributeError` `detect_patterns` (décisions + outcomes CATALYSEUR) | liste mémoire | entrées non-dict filtrées à l'entrée |
| 4 | `AttributeError` `aggregates` | liste mémoire | idem — agrégats par version sur entrées valides seules |

Déjà robuste (vérifié SANS correctif) : `?hops=` dégénérés → 200 avec
clamp 1..3 et `truncated` toujours dit ; symboles dégénérés → jamais
500 ; ids dégénérés → 404 STRUCTURÉ (forme route `ok:false` ou forme
applicative `error:not_found` — les deux structurées, jamais nues) ;
traversée → jamais un fichier système ; vue HTML : l'id hostile n'est
JAMAIS réfléchi sans échappement (`<script>` absent du corps).

## 4. Preuves

```text
python -m pytest tests/test_http_fuzz_lot34.py -q
→ rouge avant correctifs : 4 failed / 4 passed
→ vert après :             8 passed in 2.35s

python -m compileall -q terminal.py vertex   → exit 0
python -m pytest tests/ -q
→ 1555 passed, 2 skipped in 13.21s           (baseline 1547 → +8)
```

**Aucun bump de version** : aucune règle ne change sur données valides
(suite inchangée) — les entrées corrompues passent du 500 au refus
honnête. Aucun changement de shell → SW v102 inchangé.

## 5. Invariants tenus

- READONLY absolu ; jamais de 500 sur les routes fuzzées ; 404 toujours
  structuré ; clamp `hops` toujours appliqué et troncature toujours dite ;
- XSS : aucun reflet brut d'id hostile (markupsafe en place, prouvé) ;
- données réelles : entrées corrompues ignorées, entrées valides
  toujours servies — jamais de fabrication ;
- zéro aléatoire ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 35)

1. Santé du ledger multi-versions (rapport de cohérence 0.8.0/0.9.0
   dans la liste mémoire — compteurs par version déjà servis, à surfacer) ;
2. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
3. RC courte re-jouée après le prochain lot UI ;
4. Fuzz des routes restantes (/api/skyler/<sym> paramètres).

**Arrêt après ce lot — validation humaine requise.**
