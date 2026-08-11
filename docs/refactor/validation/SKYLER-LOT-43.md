# SKYLER V2 — LOT 43 : fuzz clés encodées des routes cellule

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-43-cell-key-fuzz`
(base : `integration/vertex-skyler-v2` @ `7b87018`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) bilan consolidé n°2 (lots 38-42),
(b) fuzz clés encodées des routes cellule, (c) autre. Choix : **(b)**.

- La « couverture HTTP adversariale complète » affirmée au lot 36 avait
  un TROU réel : les routes cellule (lots 39/40) sont postérieures à la
  batterie du lot 34. Fermer un écart entre une affirmation de
  couverture et la réalité passe avant un rafraîchissement de bilan —
  le bilan n°1 (lot 38) date de 5 lots et reste exact.
- (a) reste le candidat naturel du prochain lot de consolidation.

## 2. Méthode — batterie à liste FIXE (zéro aléatoire)

`tests/test_cell_key_fuzz_lot43.py` (7 tests, magasins isolés) sur les
DEUX routes cellule — `/api/skyler/memory/cell/<g>/<k>` (JSON) et
`/memory/cell/<g>/<k>` (HTML) :

- 12 clés dégénérées : traversée percent-encodée (`%2e%2e`,
  `%2e%2e%2f%2e%2e`), 500 caractères, `<script>`, apostrophe, unicode
  NFD (é décomposé), CJK, espaces, `%20`, 'null', 'undefined', '-' ;
- 4 groupes dégénérés : inconnu, `%2e%2e`, 500 chars, `<script>` ;
- traversée brute `../../etc/passwd` sur les deux routes ;
- **non-interférence** : une cellule réelle (25 mesures, moteur courant)
  reste servie EXACTEMENT entre deux salves de clés hostiles ;
- **pas de normalisation cachée** : une clé NFD ne matche jamais une
  cellule NFC — la donnée figée est la seule vérité (404 dit).

## 3. Résultat — les routes étaient DÉJÀ robustes (0 défaut)

**7/7 verts sans aucun correctif produit.** Les gardes accumulées
couvrent l'intégralité : `cell_decisions` refuse les groupes/clés
dégénérés (lot 39), 404 structurés JSON et lisibles HTML (lots 39/40),
markupsafe sur tout contenu (lot 40), entrées de magasin non-dict
ignorées (lots 31/34). Aucun 500, aucun reflet brut, aucun fichier
système, aucune interférence, aucune normalisation silencieuse.

L'affirmation du lot 36 est désormais EXACTE : couverture adversariale
HTTP complète des chemins Skyler (lots 31/34/36/43).

## 4. Preuves

```text
python -m pytest tests/test_cell_key_fuzz_lot43.py -q → 7 passed
python -m compileall -q terminal.py vertex             → exit 0
python -m pytest tests/ -q → 1606 passed, 2 skipped    (baseline 1599 → +7)
```

Aucun changement produit → moteur 0.9.0 et SW v106 inchangés (tests
seulement).

## 5. Invariants tenus

- zéro aléatoire (listes figées) ; magasins réels jamais touchés ;
- jamais 500 ; 404 structurés/lisibles ; XSS jamais réfléchi ;
- pas de normalisation cachée des clés (la donnée figée est la vérité) ;
- READONLY absolu ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 44)

1. Bilan consolidé n°2 (section BILAN de STATUS étendue aux lots 38-43) ;
2. Pattern biais par type de catalyseur — QUAND des échantillons mesurés
   réels existeront ;
3. Toute amélioration constatée pendant le travail.

Rappel honnête (déjà posé au réveil précédent) : la valeur marginale des
lots code diminue — la validation humaine physique (réserve n°1, lot 27)
est l'étape la plus utile du programme à ce stade.

**Arrêt après ce lot — validation humaine requise.**
