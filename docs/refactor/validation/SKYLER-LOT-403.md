# SKYLER LOT 403 — Les tests qui n'affirment rien : deux, et tous deux légitimes

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-403` (base : lot 402 fusionné,
80df97c)

Point de contrôle **peu coûteux**, choisi après les 35 minutes du lot 402 : un
balayage AST, quelques secondes. Question : **la suite contient-elle des tests
qui ne peuvent pas échouer ?**

**Aucun code, aucun gardien, aucun test ajouté.**

## Trois familles cherchées

| famille | ce que c'est |
|---|---|
| **A** | test sans **aucune** assertion — ni `assert`, ni `pytest.raises`, ni appel à une aide locale qui assère |
| **B** | `assert` sur un littéral toujours vrai — `assert True`, `assert 1`, `assert 'texte'` |
| **C** | `assert (cond, 'message')` — **le tuple**. Un tuple non vide est toujours vrai : la parenthèse de trop **annule l'assertion**, et le code a l'air correct |

La famille C est la plus dangereuse des trois : elle se lit comme une assertion
avec message, et n'en est pas une.

## L'instrument, validé avant emploi

Fichier de contrôle avec les quatre fautes plantées et **trois témoins
légitimes** : un `assert` normal, un test qui délègue à une aide qui assère, un
test à `pytest.raises`.

```text
plantées : sans assertion · assert True · assert 1 · assert (cond, 'msg')   → 4 détectées
témoins  : assert normal · délégation à une aide · pytest.raises            → 0 signalé
```

Le détecteur suit **un niveau d'indirection** — sans quoi tout test déléguant sa
vérification à une aide aurait été faussement accusé.

## Le résultat

```text
fonctions test_* analysées                    2 563
   A. sans AUCUNE assertion                       2
   B. assert sur un littéral toujours vrai        0
   C. assert sur un TUPLE                         0
```

**Zéro `assert True`, zéro assertion annulée par une parenthèse**, sur
2 563 fonctions. C'est un résultat négatif, mais le dénominateur est mesuré et
l'instrument prouvé.

*Note de dénominateur* : 2 563 fonctions pour **2 864** tests collectés. L'écart
vient des **55 fonctions paramétrées** (59 décorateurs `parametrize`, certaines
fonctions en portant deux) : 33 décorateurs énumèrent une liste littérale — 152
cas — et **26 construisent leurs cas par calcul**, non énumérables sans exécuter.
Je ne prétends donc pas reconstituer 2 864 par l'analyse statique ; je dis d'où
vient l'écart.

## Les deux tests sans assertion — et pourquoi ils restent

```text
tests/test_persist.py:37        test_save_failure_is_silent
tests/test_services_lot90.py:39 test_save_failure_is_silent_by_contract
```

Tous deux vérifient la même chose : `persist.save_json` **ne doit pas lever**
quand l'écriture échoue (cache best-effort). L'assertion est implicite — si la
fonction levait, le test échouerait. Leurs commentaires le disent :
`# ne doit PAS lever`.

**Mais ils ont un angle mort** : ils passeraient aussi si `save_json` devenait un
**no-op**, c'est-à-dire s'il cessait d'écrire quoi que ce soit. Un test qui ne
distingue pas « a échoué en silence » de « n'a rien tenté » est incomplet.

Plutôt que de l'affirmer, je l'ai **mesuré** — `save_json` remplacé par un
`return` nu :

```text
les 2 tests sans assertion                              2 passed   ← aveugles, confirmé
leurs voisins de fichier                                2 FAILED
   test_persist.py::test_round_trip
   test_services_lot90.py::test_save_load_roundtrip_faithful
```

**L'angle mort est réel, et il est couvert dans le même fichier.** Les deux
tests peuvent donc rester tels quels : les durcir n'ajouterait aucune protection
que la suite n'ait déjà. Production restaurée à l'octet (`git status` vide).

*Un test sans assertion n'est pas nécessairement un test creux — encore
faut-il vérifier qui couvre ce qu'il ne voit pas.*

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — ni production, ni test. La mutation de `persist.py`
  a été restaurée à l'octet avant toute autre étape. Pas de preuve MD5 requise,
  pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**,
  aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Le détecteur voit les assertions **écrites dans le fichier de test**, avec un
seul niveau d'indirection. Un test dont toute la vérification vivrait dans une
aide **importée d'un autre module** serait compté comme assérant s'il l'appelle,
mais une aide importée qui n'assère pas ne serait pas détectée comme telle. Et
« 0 littéral toujours vrai » ne dit rien des assertions **fausses mais non
littérales** — `assert x == x` passerait au travers.

## Où en est la boucle

Huitième lot court, huitième point de contrôle distinct — et le moins coûteux de
la série (quelques secondes d'analyse, contre 35 minutes au lot 402).

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388, tous les dossiers de rang 1 à l'arrêt.
