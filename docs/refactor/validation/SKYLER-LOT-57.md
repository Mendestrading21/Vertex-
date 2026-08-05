# SKYLER V2 — LOT 57 : polish Opportunités + Analyse (défauts prouvés uniquement)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-57-polish-opps-analysis`
(base : `integration/vertex-skyler-v2` @ `83e4a1f`, fraîchement fetchée) ·
Mode : arc « jusqu'au lot 60 » (4/7).

## 1. Inspection réelle d'abord — verdict honnête : pages saines

6 captures (Opportunités, Analyse, fiche `/analysis/AAPL` × desktop 1440
/ mobile 390) + audit automatique : **0 débordement de page, 0 erreur
console**. Points vérifiés et déclarés SAINS (non touchés) : la table de
comparaison mobile (519 px) défile dans `.vx-table-wrap`
(`overflow-x:auto` — motif conforme du dépôt) ; les pairs de la fiche
sont déjà cliquables (`data-open-analysis`) ; les états vides sont
honnêtes partout (« Aucune donnée », jamais de chiffre inventé).
Deux défauts RÉELS trouvés dans la fiche :

## 2. Défaut n°1 : information tronquée dans les lignes clé/valeur

`.vx-kv .k` était `white-space:nowrap` + `text-overflow:ellipsis` : le
libellé « Politique par défaut » se rendait « Politique … » dès que la
valeur est longue — perte d'information visible sur la capture AVANT.
Corrigé : le libellé passe à la ligne (`overflow-wrap:anywhere`), rien
n'est jamais tronqué. Vérifié APRÈS programmatiquement :
`scrollWidth ≤ clientWidth` et texte complet « Politique par défaut ».

## 3. Défaut n°2 : littéral couleur hors palette (étoile favori)

`analysis_page.py` colorait l'étoile favori en `#FFD27A` dur — hors
palette officielle (doctrine §3 : aucun littéral sauvage côté UI).
Remplacé par le token sémantique `var(--vx-warning)` (#D9BE3C). Le
littéral analogue de `vertex/engines/scorecard.py` est CÔTÉ MOTEUR
(mapping grade → couleur servie aux clients) — hors périmètre d'un lot
polish UI, dit ici et non touché.

## 4. Tests (rouges d'abord — 3 nouveaux)

`tests/test_polish_lot57.py` (rouge 3/3 confirmé) : plus d'ellipse ni de
nowrap sur `.vx-kv .k` · plus de `#FFD27A` côté page + token présent ·
SW ≥ v114 et v113 absent.

## 5. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1661 passed, 2 skipped   (1658 + 3)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v114 servi,
  cycle souverain inclus)
Preuve navigateur APRÈS : fiche AAPL — libellé « Politique par défaut »
  ENTIER (non tronqué, vérifié scrollWidth/clientWidth), 0 erreur
  console. Captures avant/après conservées.
```

SW `td-shell-v113` → `td-shell-v114` + 4 gardiens.

## 6. Invariants

READONLY intact · aucun moteur touché (scorecard.py laissé tel quel,
dit) · zéro littéral couleur nouveau (un littéral SUPPRIMÉ) · `main`
intacte · fichiers runtime non commités.

## 7. Suite (arc)

Lot 58 : polish Portefeuille + Options (même méthode). Puis 59, et 60 =
RC finale + bilan consolidé n°4 + ARRÊT.

**Arrêt après ce lot — validation humaine requise.**
