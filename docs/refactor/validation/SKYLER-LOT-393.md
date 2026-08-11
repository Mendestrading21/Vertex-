# SKYLER LOT 393 — Les promesses de retour imbriquées : pas besoin d'un analyseur

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-393` (base : lot 392 fusionné,
ea044cf)

## Piste

Dernier angle mort déclaré du lot 375, sur la seule des pistes fines restantes
qui portait encore une question vérifiable. Le 375 écrivait :

> *« Vérifier les formes IMBRIQUÉES demanderait un analyseur d'un autre ordre ;
> c'est déclaré ici plutôt que tu. »*

**Il n'en fallait pas un.** Une promesse de retour se vérifie en **appelant** la
fonction : l'exécution tranche ce que l'analyse statique ne sait pas suivre. Le
lot 375 cherchait la solution du mauvais côté — c'est la seule vraie trouvaille
de ce lot, et elle porte sur la méthode.

## Le dénominateur

```text
fonctions portant une promesse « Retourne {…} »            7
   dont au moins un `return {littéral}`  (couvert par 375)  5
   dont AUCUN littéral → forme déléguée   (angle mort)      2
```

Deux fonctions, pas une famille. Le trou déclaré était réel mais **étroit** — le
dire évite de faire passer un lot mince pour une percée.

## Verdict — les deux promesses sont exactes, prouvé par exécution

```text
grade_packet   promises {overall, warnings, actionable_allowed}
               rendues  {overall, warnings, actionable_allowed}   → 0 manquante
select_calls   promises {per_category, primary, rejected, notes}
               rendues  {per_category, primary, rejected, notes}  → 0 manquante
```

Les fixtures sont **celles de la suite** (`test_data_sources`,
`test_options_engine`), pas des entrées fabriquées pour l'occasion : le contrat
est vérifié sur les mêmes objets que le reste des tests.

## Le troisième cas, déjà connu, re-mesuré

`options_for_position` délègue à son `pack()` interne. Sa docstring énumère
**12 identifiants nus** — `role, role_label, sym, type, strike, exp, dte,
premium, pop, score, grade, why` — et `pack()` en renvoie **13**. Le
surnuméraire est `delta` : **sous-déclaration, pas promesse fausse**. Rien de ce
qui est annoncé ne manque. Mesure identique à celle du lot 375, confirmée.

Détail de méthode : ma première extraction cherchait des clés **entre quotes** et
n'en trouvait aucune — la docstring les écrit nues. Le détecteur, encore, avant
le code.

## Gardien

`tests/test_promesses_imbriquees_lot393.py` (6 tests). Ces trois fonctions
étaient **hors de portée** du gardien du 375, qui n'inspecte que les dicts
littéraux : une clé promise qui disparaîtrait aujourd'hui passerait la suite.

- **dénominateur** : 7 promesses, dont 2 déléguées — si une promesse cessait
  d'avoir un retour littéral, elle basculerait dans l'angle mort du 375 sans que
  rien ne le signale ;
- **les deux déléguées, par exécution** : toute clé annoncée doit être rendue ;
- **la troisième, statiquement** : tout identifiant cité dans la docstring doit
  figurer dans `pack()` ;
- **anti-péremption** de la sous-déclaration connue (13 clés rendues).

### Preuve ROUGE

```text
clé promise renommée dans grade_packet                ROUGE OK
clé promise renommée dans select_calls                ROUGE OK
clé annoncée absente de pack() (promesse FAUSSE)      ROUGE OK
[témoin] `delta` ENFIN déclaré — la correction légitime  ne mord pas — correct
après restauration : 6 passed
```

Le témoin vaut, ici encore, plus que les trois cas rouges : il simule **la
correction que quelqu'un ferait un jour** — déclarer `delta` dans la docstring —
et vérifie que le gardien tolère la sous-déclaration résolue au lieu de s'y
opposer. Un gardien qui punit la correction est pire qu'aucun gardien.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Copies de sûreté des 21 fichiers runtime ; contrôle d'**apparition** de
  nouveaux fichiers (leçon du 392) : aucun créé. Écart final : aucun.
- Suite : **2856 → 2862 passed / 2 skipped** (+6). SW : `td-shell-v187`.

## Portée

Ce lot est **mince, et c'est normal** : il ferme un angle mort de deux fonctions.
Il ne prouve rien sur les promesses formulées autrement que « Retourne {…} » —
le 375 avait déjà montré que les promesses en un seul mot majuscule ne sont pas
décidables ainsi. Et la vérification par exécution ne couvre qu'**un chemin par
fonction** : celui que les fixtures de la suite empruntent.

## Suite — il ne reste plus de piste fine porteuse

Les pistes fines sont désormais **épuisées** :

- refus API, littéraux (377) et construits en variable (392) — **closes** ;
- écritures runtime par la suite (389) — **close** ;
- promesses de retour, littérales (375) et imbriquées (393) — **closes** ;
- restent : trois sites de concaténation à constantes (374), question de forme
  sans enjeu d'honnêteté · le commentaire périmé de `vx-entities.js`, différé
  car il changerait un octet servi pour un gain nul.

**Aucune ne mérite un lot.** Le prochain sera court et le dira, à moins qu'un GO
n'arrive sur l'un des dossiers du rang 1 — où se trouve, elle, la matière utile.

Prochaine échéance périodique : bilan n°9 **~lot 400**.
