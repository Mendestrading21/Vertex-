# SKYLER LOT 383 — Trois invariants confrontés, trois réellement imposés

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-383` (base : lot 382 fusionné,
ef1fc4a)

## Piste

Troisième passe d'audit des gardiens par mutation. Les lots 381 et 382 avaient
trouvé un écart chacun, tous deux au même endroit : **un énoncé de `CLAUDE.md`
plus large que ce qui est réellement imposé**. Ce lot continue méthodiquement.

## Résultat de la passe

```text
apostrophes déséchappées dans un bloc JS SERVI       MORD
nom personnel injecté dans une page servie           MORD
scan_state réassigné dans un CONSOMMATEUR            MORD
ENGINE_VERSION : recul 0.9.0 → 0.8.0                 MORD
ENGINE_VERSION : bond   0.9.0 → 1.4.0                passe — plancher, voir plus bas
demo_mode masqué                                      mutation sans effet servi
[témoin] aucune modification                          ne mord pas — correct
```

**Aucun trou.** Contrairement aux deux lots précédents, les invariants confrontés
sont réellement tenus. C'est un résultat, pas une absence de résultat.

## Deux « AUCUN GARDIEN » qui accusaient à tort

**`scan_state`.** La première mutation réassignait `scan_state` **dans
`vertex/app/state.py`** — or ce fichier est le `HOME` déclaré du gardien
`test_scan_state_invariant_lot217`, **exclu du scan par conception** : c'est le
domicile légitime de l'affectation. Rejouée dans un **consommateur**
(`routes/system.py`), la violation tombe immédiatement.

**`demo_mode`.** Passer `demo_mode=DEMO_MODE` à `demo_mode=False` ne change
**aucun octet servi** : `/system` rend le même MD5 (`73e917c0f2d0`, 82 837 o)
avant et après, alors que `DEMO_MODE` vaut bien `True` au runtime. La mutation
était effective dans la source mais ce point d'appel n'atteint pas la page —
aucune conclusion sur un gardien n'est donc possible. Mutation invalide, pas un
trou.

Deux fois sur trois, le « AUCUN » initial était faux. La règle du lot 379 continue
de payer : **un cas qui ne mord pas accuse d'abord la mutation**, puis le
périmètre, et seulement ensuite le gardien.

## Le seul écart : un plancher, pas une égalité

« skyler_core 0.9.0 intact » suggère une égalité. Le gardien réel impose
`parts >= (0, 9, 0)` : un **recul** (0.8.0) fait tomber la suite, un **bond en
avant** (1.4.0) passe.

C'est la deuxième catégorie de la grille du lot 383 — **gardien plus étroit que
l'énoncé** — mais, contrairement au lot 382, **la règle réelle est la bonne** :
une montée de version est légitime, une régression ne l'est pas. Rien à corriger
dans le code ; c'est l'énoncé qui gagne à être dit précisément, et le gardien
ci-dessous le fixe.

**Verdict : sain, rien touché.**

## Un faux gardien écarté avant livraison

Ma première version testait la **parité des quotes simples** hors échappement
dans les blocs JS servis. Elle échouait sur **5 pages sur 8** — et le code est
sain : les quotes vivent aussi dans des chaînes à guillemets doubles, des regex
et des commentaires, où la parité ne signifie rien. Un gardien qui accuse du code
sain finit désactivé ; je l'ai **remplacé** par la vérification que le vrai
parseur (`node --check`, `test_js_syntax_sweep_lot182`) couvre encore les
8 pages servies. C'est le bon outil, il existait déjà.

## Gardien

`tests/test_invariants_reellement_imposes_lot383.py` (14 tests) :

- la version du cœur ne peut que **monter**, et un test **anti-dérive** signale
  si quelqu'un durcit un jour en égalité stricte ;
- **anti-vide** : ≥ 20 apostrophes échappées dans le JS inline servi (31
  mesurées) — si la surface disparaît, la règle n°2 n'a plus d'objet ;
- le balayage `node --check` couvre bien les 8 pages servies ;
- aucun marqueur d'auteur dans les **octets servis** (le gardien historique
  balaie l'arbre ; celui-ci vérifie ce que le navigateur reçoit) ;
- **anti-péremption** du gardien de noms personnels ;
- la sémantique de `scan_state` est fixée : `HOME` exclu, production scannée —
  si le domicile change de nom ou si le scan rétrécit, la protection deviendrait
  vide sans que rien ne le signale.

### Preuve ROUGE

```text
ROUGE OK  recul de version du cœur (0.9.0 → 0.8.0)          | restauration identique
ROUGE OK  plancher de version affaibli dans le gardien       | restauration identique
ROUGE OK  page servie retirée du balayage `node --check`     | restauration identique
après restauration : 14 passed
```

Le deuxième cas a d'abord répondu **NE MORD PAS** : j'avais muté **mon propre
fichier de test** au lieu du gardien historique — les deux contiennent la même
chaîne. Corrigé sur `test_catalyst_type_lot30.py`, il mord. Encore une fois, la
preuve était fautive avant le gardien.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 382, ef1fc4a) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Suite : **2779 → 2793 passed / 2 skipped** — verte (+14).
- SW : `td-shell-v187`.

## Portée — ce que ce lot ne prétend pas

Cinq mutations utiles de plus, soit dix-huit en trois lots sur 2 793 tests :
toujours un **sondage**. « MORD » signifie « attrape CETTE faute-là », pas
« couvre tout ». Le cas `demo_mode` reste **non conclu** : je n'ai pas cherché
quelle surface consomme ce point d'appel, seulement établi qu'il n'atteint pas
`/system`. Et je n'ai pas confronté les deux règles restantes de la liste :
`desk_data.json` jamais écrasé (déjà caractérisé au lot 362) et l'étiquetage
démo pris sous un autre angle.

## Suite

LOT 384 : la veine reste ouverte mais son rendement se précise — **deux écarts
sur trois lots**, et ce lot-ci n'en trouve aucun. Cibles restantes :
`desk_data.json` / `/api/desk/restore` (viser le gardien, pas la caractérisation
du 362) · l'étiquetage démo par une autre porte que `demo_mode` · les gardiens
de routes et de navigation · les gardiens de responsive. Si deux lots
consécutifs ne trouvent rien, le dire et changer de veine. Prochaine échéance
périodique : **~lot 390**.
