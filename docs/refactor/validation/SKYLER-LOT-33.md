# SKYLER V2 — LOT 33 : by_catalyst_type dans la carte Mémoire

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-33-catalyst-type-ui`
(base : `integration/vertex-skyler-v2` @ `d1aafed`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) surfaçage by_catalyst_type en UI, (b) fuzz
des routes HTTP graphe/mémoire, (c) drill-down cellule. Choix : **(a)**,
premier par valeur.

- Les découpes `by_catalyst` (lot 28) et `by_catalyst_type` (lot 30)
  existent dans le payload servi mais restaient INVISIBLES : une mesure
  que le trader ne voit pas ne corrige aucun biais. Le coût est minimal
  (la mécanique de badges du lot 26 est déjà en place — zéro nouveau
  moteur de rendu) et la RC courte du lot 32 vient de valider le socle.
- (b) reste au backlog ; (c) toujours limité par l'absence de cellules
  mesurées en réel.

## 2. Périmètre livré

### 2.1 Carte Mémoire (`vertex/ui/pages/performance_page.py`)

La boucle de badges « calibration par contexte » gagne DEUX groupes :
`by_catalyst` (avec/sans catalyseur) et `by_catalyst_type` (earnings/
macro/…/inconnu) — MÊME mécanique que niveau/régime/décision (une seule
boucle, un seul littéral `calibration_by_context`, gardé par test) :
badge vert `MESURE` (valeur + n) ou neutre `insuffisant (n)`, `title` =
basis du moteur. Le libellé de la section dit désormais explicitement :
« catalyseur/type = observation, jamais consommés » — l'UI ne vend
jamais une découpe d'observation comme une règle de sélection.

### 2.2 Service worker

Shell visible modifié → bump `td-shell-v101` → `td-shell-v102`
(`vertex/app/routes/system.py` L211) + les 4 gardiens mis à jour
(v102, assertions vN-1 → v101 absent).

## 3. Méthode — rouge d'abord

`tests/test_catalyst_type_ui_lot33.py` (4 tests) écrit AVANT ; confirmé
rouge : **3 failed / 1 passed** (le passant : gardien « un seul moteur de
rendu », déjà vrai). Après : **4 passed**. Couverture : groupes
by_catalyst/by_catalyst_type présents dans la source servie ; libellé
« observation » ; unicité du littéral `calibration_by_context` (pas de
second renderer) ; SW ≥ v102 avec v101 absent.

## 4. Preuves

```text
python -m pytest tests/test_catalyst_type_ui_lot33.py -q → 4 passed
python -m compileall -q terminal.py vertex               → exit 0
python -m pytest tests/ -q → 1547 passed, 2 skipped      (baseline 1543 → +4)

tools/rc_short_audit.js (serveur DEMO=1 NO_IBKR=1) :
  8 pages HTTP 200 · console_err=0 · pageerror=0 · /healthz 200
  /api/client-log n=0 · sw.js td-shell-v102
  RC COURTE : GO — 0 défaut.
```

Preuve navigateur `/journal` : page rendue sans erreur sous v102 ;
en démo 0 cellule mesurée → aucun badge de contexte affiché — c'est le
comportement HONNÊTE documenté au lot 26 (les badges n'apparaissent que
quand des cellules existent), pas un défaut. Capture `lot33_journal.png`
(scratchpad de session).

## 5. Invariants tenus

- Données réelles uniquement : cellules absentes → rien d'affiché ;
  cellules insuffisantes → badge neutre « insuffisant (n) » ; découpes
  d'observation étiquetées comme telles dans l'UI ;
- XSS : basis/labels passent par `esc()` (mécanique existante) ;
- READONLY absolu ; moteur 0.9.0 inchangé (UI seulement) ;
- SW bump + 4 gardiens prospectifs ; fichiers runtime jamais commités ;
  `main` intacte.

## 6. Backlog restant (candidats lot 34)

1. Fuzz des routes HTTP graphe/mémoire (hops/ids dégénérés, liste fixe) ;
2. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
3. RC courte re-jouée après le prochain lot UI.

**Arrêt après ce lot — validation humaine requise.**
