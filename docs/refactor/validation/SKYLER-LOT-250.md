# SKYLER LOT 250 — Mini-bilan de la tranche 246-250

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-250` (base : lot 249 fusionné)

## Caractère de la tranche : du « prouver » au « préparer la décision »

La tranche a fermé la campagne de preuve (214-246) puis a construit,
en trois lots, TOUT ce qu'il faut pour que l'humain tranche la purge de
terminal.py en connaissance de cause. **Zéro ligne de code produit
touchée sur les 5 lots** — c'est un fait, pas une paresse : le produit
est mesuré correct (0 défaut depuis le lot 232) et la règle « jamais de
changement gratuit » a tenu.

## Les 5 lots

| Lot | Livré | PR |
|---|---|---|
| 246 | 4e parcours métier : JOURNALISATION D'UNE DÉCISION d'un trait (formulaire réel « Ajouter une entrée » → `vxJournal` → serveur → persistance après reload) — 2 fausses pistes de sélecteurs documentées honnêtement | #279 |
| 247 | GRANDE SYNTHÈSE de la campagne 214-246 : 33 lots, +14 tests, 3 correctifs réels, 6 gardiens neufs, 8 invariants tenus, 4 parcours métier — le produit passe de « supposé correct » à « MESURÉ correct » | #280 |
| 248 | DOSSIER DE DÉCISION DE PURGE : preuve runtime **21 fonctions héritées / 0 routée / 21 orphelines**, 32 PAGE_* épinglées seulement par les tests de caractérisation, plan 3 étapes (une PR chacune, rollback = revert) | #281 |
| 249 | CHIFFRAGE OUTILLÉ É2 : outil commité `tools/purge_e2_sizing.py` — fourchette mesurée **31,4 % (borne basse certaine) → 48,7 % (borne haute)** de terminal.py mort ; 2 pièges gravés (12 PAGE_* référencées par CHAÎNE via `globals()[_pg]` ; dépendance `PAGE_ENTREPRISES` → `_OPP_BRIEF_JS` → `PAGE_DAILY`) ; 4 faux positifs corrigés avant publication | #282 |
| 250 | Ce mini-bilan | #283 |

## Les chiffres de la tranche

- Tests : **2486 passed / 2 skipped** — inchangé sur les 5 lots
  (aucun test ajouté : rien à garder de neuf, rien à corriger).
- SW : **td-shell-v173** — inchangé (aucun octet servi modifié).
- PR fusionnées : 5 (#279 → #283), toutes squash.
- Faux positifs d'outils attrapés AVANT conclusion : 3 (sélecteurs
  journal ×2 au lot 246, fonctions décorées au lot 249).

## État honnête de la boucle

Les pistes d'entretien autonome s'amincissent : le produit est prouvé
(8 invariants, 8 pages, responsive, shell, infra, 4 parcours), les
docs sont gardées par des tests d'intégrité, et le seul gros chantier
restant — la purge (~3 370 à 5 236 lignes mortes chiffrées) — est
**bloqué par conception** sur une décision humaine. La boucle continue
en entretien utile ou constats courts, sans fabriquer du travail.

## Ce qui attend l'humain (inchangé)

1. **« GO purge étape 1 »** — dossier complet : preuves (248) +
   chiffrage (249) dans `TERMINAL-PURGE-DECISION.md`.
2. Validation physique TWS réel + iPhone (vider le cache → SW v173).
3. Merge vers `main` — accord explicite uniquement.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs seulement.

## Suite

LOT 251 : entretien ou directive.
