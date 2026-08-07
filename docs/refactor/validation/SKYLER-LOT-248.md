# SKYLER LOT 248 — Dossier de décision de purge de terminal.py (0 code touché)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-248` (base : lot 247 fusionné)

## Objet

La purge de terminal.py attend un accord humain depuis des dizaines de
lots. Ce lot prépare le DOSSIER DE DÉCISION — preuves mesurées + plan
par étapes sûres — pour que l'humain puisse trancher en connaissance.
**Aucun code touché.**

## Livré — `TERMINAL-PURGE-DECISION.md`

### La preuve décisive (mesurée ce lot, reproductible)

Croisement runtime `app.url_map` × fonctions retournant `PAGE_*` :

- **21 fonctions de rendu héritées → 0 routée, 21 ORPHELINES** —
  aucun utilisateur ne peut les atteindre (cohérent avec les 43
  commentaires « route migrée » et le constat du lot 246 : /journal
  sert performance_page, pas PAGE_JOURNAL).
- **32 constantes PAGE_*** : hors terminal.py, référencées UNIQUEMENT
  par les tests de caractérisation écrits POUR ce moment (lot 183 &
  épingles associées).
- **1 exception cartographiée** : PAGE_DAILY ↔ home_art.py/vault.py
  (modules hérités eux-mêmes) → étape dédiée.

### Le plan (3 étapes, une PR chacune, rollback = revert)

É1 : fonctions orphelines + PAGE_* qu'elles seules consomment + tests
de caractérisation devenus sans objet. É2 : blocs BODY/CSS/JS révélés
non référencés (chiffrage outillé après É1). É3 : dépendances
croisées PAGE_DAILY/home_art/vault (décision dédiée). Chaque étape :
pytest 100 % + navigateur 8 pages + 0 erreur console.

### La décision demandée

**GO / NO-GO Étape 1** — sans accord explicite, rien ne sera purgé.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : docs seulement.

## Preuves

- Mesure runtime dans le dossier (21/21 orphelines) ; grep des
  références externes par constante.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 249 : entretien ou directive. La purge ne démarre QUE sur
« GO purge étape 1 » de l'humain.
