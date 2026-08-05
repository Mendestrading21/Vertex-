# SKYLER V2 — LOT 36 : fuzz du cœur HTTP `/api/skyler/<sym>`

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-36-skyler-route-fuzz`
(base : `integration/vertex-skyler-v2` @ `fd752ab`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) fuzz de `/api/skyler/<sym>`, (b) fraîcheur
du ledger en UI, (c) drill-down cellule, (d) bilan consolidé. Choix :
**(a)**, premier par valeur.

- C'est la route la plus riche du programme (packet + red-team +
  calibration + décision + hooks journal/mémoire/séances/portefeuille) —
  le cœur décisionnel. Après les lots 31/34, c'était le dernier grand
  chemin HTTP sans batterie adversariale dédiée.
- (b)/(c)/(d) restent au backlog.

## 2. Méthode — batterie à liste FIXE (zéro aléatoire)

`tests/test_skyler_route_fuzz_lot36.py` (7 tests, magasins runtime
ISOLÉS par fixture — les vrais fichiers ne sont jamais touchés) :

- 14 symboles dégénérés (inconnu, minuscules, 500 chars, espaces,
  apostrophe, `<script>`, %00, unicode, '..', '-', '_', '0', 'NULL',
  'undefined') ;
- 6 corruptions de magasins runtime, un par un PUIS simultanées
  (mémoire × 3 formes, journal, séances, desk_data) — avec double appel
  (chemin dédupliqué) ;
- honnêteté du symbole inconnu (blocs INSUFFISANTS, décision jamais un
  achat, note « jamais un ordre ») ; déterminisme à état constant ;
  calibration fail-safe (0,50 global) sous mémoire corrompue.

## 3. Résultat — la route est DÉJÀ robuste (0 défaut)

**7/7 verts sans aucun correctif produit.** Les gardes des lots 31
(moteurs) et 34 (routes mémoire) plus les hooks fail-safe historiques de
la route (chaque hook sous try/except documenté « ne casse jamais la
décision ») couvrent l'intégralité de la batterie :

- symbole dégénéré → clamp `upper()[:12]`, décision structurée, jamais 500 ;
- titre hors scan → `insufficient_blocks` non vide, décision
  ATTENDRE/REFUSER (jamais un achat sans données), note READONLY servie ;
- magasins corrompus (un par un et tous ensemble, deux appels) → décision
  toujours servie, calibration retombée à 0,50 global honnête ;
- déterminisme confirmé à état constant.

Note de méthode : le premier passage de la batterie était rouge sur une
MAUVAISE hypothèse de contrat (lecture des champs au niveau racine alors
que la route enveloppe `{symbol, decision:{…}, packet, red_team_review,
demo}`) — la batterie a été alignée sur le contrat réel, qui se trouve
ainsi DOCUMENTÉ par les tests. Aucun défaut produit derrière ce rouge.

## 4. Preuves

```text
python -m pytest tests/test_skyler_route_fuzz_lot36.py -q → 7 passed
python -m compileall -q terminal.py vertex                → exit 0
python -m pytest tests/ -q → 1572 passed, 2 skipped       (baseline 1565 → +7)
```

Aucun changement moteur/route/UI → moteur 0.9.0 et SW v103 inchangés.
La couverture HTTP adversariale est désormais complète sur les chemins
Skyler : `/api/skyler/<sym>` (lot 36), `/api/skyler/memory*` et
`/memory/<id>` (lot 34), `/api/skyler/graph*` (lot 34), moteurs (lot 31),
export (lots 29/31).

## 5. Invariants tenus

- READONLY absolu (note servie vérifiée) ; jamais 500 ; données réelles
  uniquement (blocs INSUFFISANTS dits, jamais remplis) ;
- zéro aléatoire ; magasins runtime réels jamais touchés (fixture
  isolée) ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 37)

1. Fraîcheur du ledger dans la carte Mémoire (dernière décision figée :
   date/ancienneté honnête — bump SW v104) ;
2. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
3. Bilan consolidé des lots 29-36 dans STATUS ;
4. RC courte re-jouée après le prochain lot UI.

**Arrêt après ce lot — validation humaine requise.**
