# SKYLER LOT 299 — A11y : les 2 derniers champs sans étiquette accessible

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-299` (base : lot 298 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — balayage a11y des noms accessibles (26 vues)

Dernier balayage a11y : lot 73 — ANCIEN. Sondeur neuf sur 8 pages
racines + 18 vues profondes : boutons sans nom accessible, liens sans
nom, champs sans étiquette (aria-label / aria-labelledby /
label[for] / label parent).

**Résultat : 25 vues sur 26 parfaites** (0 bouton, 0 lien, 0 champ) —
l'hygiène des lots 73/209 a tenu. Deux défauts réels, tous deux sur la
fiche Analyse :

- `#an-cp-q` (question du copilote) et `#an-pt-amt` (montant du ticket
  pré-trade) n'avaient qu'un **placeholder** — qui n'est PAS une
  étiquette (il disparaît à la saisie, lecture inconstante par les
  lecteurs d'écran).

## Livré

`analysis_page.py` : `aria-label="Question sur ce titre"` et
`aria-label="Montant envisagé en dollars"` sur les deux champs.

## Gardien neuf — `tests/test_analysis_inputs_a11y_lot299.py` (2 tests)

Chaque champ garde son aria-label.

## Preuves (navigateur réel, DEMO)

- /analysis/AAPL : les 2 aria-labels lus dans le DOM, **0 champ sans
  étiquette restant**, 0 erreur console. Capture envoyée.
- Suite complète : **2514 passed / 2 skipped** (+2).

## Décision SW

**Bump v184 → v185** (HTML servi change) + les 5 gardiens.

## Suite

LOT 300 : purge É1 en PRIORITÉ dès déblocage ; sinon ÉCHÉANCE
PÉRIODIQUE (smoke-check protocole 251 + mini-bilan tranche 288-299).
