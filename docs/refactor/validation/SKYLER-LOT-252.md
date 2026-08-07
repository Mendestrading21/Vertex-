# SKYLER LOT 252 — Robustesse de l'outil de décision (rejouable de partout)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-252` (base : lot 251 fusionné)

## Objet

`tools/purge_e2_sizing.py` (lot 249) est l'instrument officiel du
chiffrage de la purge : il sera rejoué à l'Étape 1 et à l'Étape 2 pour
produire les listes exactes. Un outil de décision doit être rejouable
par n'importe qui, depuis n'importe où — pas seulement depuis le cwd
qui se trouve être le bon.

## Défaut prouvé AVANT de toucher (calibrage)

Lancé depuis `docs/` : `FileNotFoundError: terminal.py` (l'outil
faisait `open('terminal.py')`, `sys.path.insert(0, '.')` et
`grep … .` relatifs au cwd, silencieusement).

## Correctif minimal

Ancrage sur `__file__` : la racine du dépôt est calculée depuis
l'emplacement de l'outil (4 niveaux au-dessus de
`docs/refactor/validation/tools/`) puis `os.chdir(_ROOT)` — tout le
reste du script est inchangé.

## Preuves

- Rejoué depuis `docs/` (ancien cas d'échec) ET depuis la racine :
  les DEUX invocations rendent des chiffres identiques entre eux **et
  identiques au lot 249** — mort total 5 236 lignes (48,7 %) /
  692 382 octets (56,6 %), 107 défs (30 fonctions, 77 constantes),
  bornes basse/haute inchangées. La mesure est stable et reproductible.
- Suite complète : **2486 passed / 2 skipped**.

## Décision SW

**Pas de bump** (`td-shell-v173`) : outil de docs seulement, aucun
octet servi ne change. Aucun code produit touché.

## Suite

LOT 253 : entretien ou directive. La purge attend « GO purge étape 1 ».
