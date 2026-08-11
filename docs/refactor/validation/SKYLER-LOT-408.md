# SKYLER LOT 408 — Le `|| 0` du lot 407 est isolé, pas une famille

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-408` (base : lot 407 fusionné,
544b75b)

Le lot 407 a trouvé **un** `|| 0` qui convertit une absence en zéro déclaré réel,
et fausse un chiffre affiché. Question laissée ouverte : **est-ce un cas isolé ou
le premier d'une famille ?** La réponse change la taille du dossier de rang 1 —
et donc la décision.

**Aucun code, aucun gardien, aucun test.**

## Le recensement brut, et pourquoi il ne conclut rien

Périmètre **servi** uniquement : `vertex/**` (`.py` + `.js`) et `terminal.py`,
les six modules reliques exclus (`options_lab`, `journal`, `vault`, `signals`,
`strategy_os`, `vx_kit` — sans consommateur en production).

```text
lignes portant `|| 0` / `?? 0` / `or 0`      440   (dans 70 fichiers)
occurrences (plusieurs par ligne possible)   606
   dont terminal.py                          206
```

Instrument validé : le site connu du lot 407 (`portfolio_page.py:718`) est
retrouvé ; un fichier sans motif (`vertex/app/state.py`) ne rend rien.

**Ce chiffre ne prouve rien**, et il ne faut pas le présenter comme un problème :
`(r.get('change') or 0)` dans une somme, `Number(v) || 0` dans une moyenne — ce
sont des choix de modélisation, pas des mesures fausses. Un `|| 0` n'est un
défaut que si l'opérande peut être **absent** *et* que le zéro est ensuite
**présenté comme une mesure**.

## Le filtre décisif — les charges utiles envoyées aux moteurs

C'est exactement la forme du 407 : un `null` transformé en `0`, transmis à une
API et **déclaré réel**. Ce sous-périmètre est petit et vérifiable.

```text
appels POST sur chemin servi                          25
   dont un `|| 0` / `?? 0` dans la charge utile        1
```

**Un seul — celui du lot 407.** Aucune autre page n'envoie une absence maquillée
en zéro à un moteur.

**Le défaut du 407 est isolé.** Le dossier de rang 1 reste ce qu'il était : un
site, une page, une décision — pas une famille à traiter.

## Le filtre de forme, et ce qu'il vaut vraiment

Second filtre, plus large : un `|| 0` appliqué à un **appel de fonction** dont le
résultat est, **ailleurs dans le même fichier**, comparé à `null`/`None` —
autrement dit, l'auteur sait que la valeur peut manquer.

```text
occurrences totales                                       606
   dont l'opérande est un APPEL                           128
   dont ce même appel est ailleurs testé contre null       53
```

**Ces 53 ne sont pas des trouvailles : c'est un vivier d'hypothèses.** Pour le
montrer plutôt que de l'affirmer, le candidat le plus sensible a été ouvert —
celui qui toucherait le P&L d'une position IBKR :

```python
vertex/positions/repository.py:63
'cost': (raw.get('avgCost') or 0) * (qty or 0)
        if raw.get('avgCost') is not None and qty else None,
```

**Il est sain.** Le `or 0` est gardé par un `if … is not None … else None` : quand
`avgCost` manque, `cost` vaut **`None`**, pas zéro. La branche fautive n'existe
pas. Mon filtre l'a signalé parce que le test de nullité est *sur la même
construction* — un faux positif de forme, résolu en le lisant.

*Un vivier trié par la forme ne devient une liste de défauts qu'après lecture,
un par un. Publier les 53 comme des trouvailles aurait été malhonnête.*

## Ce que ce lot établit

1. **Sur le chemin qui compte — les charges utiles envoyées aux moteurs — le
   défaut du 407 est unique.** Le zéro est substantiel : 25 POST examinés, 1 seul
   fautif.
2. Le recensement large (606) et le vivier de forme (53) sont **des matériaux**,
   pas des conclusions ; ils sont consignés pour qu'un futur lot n'ait pas à les
   refaire, avec l'avertissement qu'ils demandent une lecture site par site.
3. **Conséquence pratique pour la décision** : corriger le dossier 406/407 ne
   demande pas une campagne. Un seul site à changer, une seule cause
   (`myCapital` jamais écrit).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve
  MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Le filtre décisif ne voit que les payloads construits **près** d'un
`method: 'POST'` (fenêtre de 12 lignes en amont). Une charge utile assemblée
loin de son envoi, ou passée par une variable intermédiaire, échapperait au
comptage — et le résultat « 1 sur 25 » vaut pour cette forme d'écriture, qui est
celle du dépôt. Le recensement large, lui, est purement textuel : il ne
distingue pas un opérande qui peut manquer d'un compteur qui vaut réellement
zéro. C'est dit, pas contourné.

## Où en est la boucle

Treizième lot court. Après deux lots qui ont trouvé (406, 407), celui-ci **borne**
ce qu'ils ont trouvé — un résultat négatif utile : il empêche de transformer une
correction d'un site en une campagne sur 606.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388.
