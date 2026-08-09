# SKYLER LOT 419 — La forme du 418 bornée : 22 replis, 18 légitimes, 4 aveuglants — et un RSI de 0 effacé

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-419` (base : lot 418 fusionné,
f30e199)

Dernier lot de mesure de la tranche. Il **borne** au lieu d'ouvrir : le lot 418 a
trouvé qu'une condition de validation testait son propre repli
(`(p.get('multiplier') or 100) <= 0`). **Ce site est-il isolé ?**

**Aucun code, aucun gardien, aucun test.**

## Le recensement, par AST

Périmètre : `vertex/**/*.py` + `terminal.py`. On cherche les comparaisons de `if`
dont un opérande contient un repli `… or CONSTANTE`.

```text
comparaisons de `if` contenant un repli `or CONSTANTE`      25
   dont SANS garde `is None` dans la même condition         22
```

**Témoins de l'instrument** — les trois passent :

```text
+  le site du 418 (`multiplier`) est retrouvé                        oui
   la ligne `quantity` du même fichier est vue par le détecteur      oui
−  …et ÉCARTÉE, parce qu'elle porte son `is None`                    oui
```

Le détecteur distingue donc bien la forme fautive de la forme correcte écrite
deux lignes plus haut.

## Les 22 ouverts un par un — la majorité est saine

Le critère de tri n'est pas la forme, c'est **le rôle de la comparaison** :

```text
SÉLECTION / CLASSEMENT — le repli est honnête                      18
   « absent → 0 » veut dire « ne qualifie pas » :
   `(fund.get('score') or 0) >= 65` · `(ev.get('news_count_24h') or 0) >= 5`
   `(c.get('quality') or 0) > (best[s].get('quality') or 0)` · comparaisons
   de chaînes, de dates, d'en-têtes HTTP, `or 'UNKNOWN'` volontaire…

DÉTECTION / VALIDATION — le repli masque ce qu'on cherche            4
```

Un vivier trié par la forme n'est pas une liste de défauts : **18 sur 22 sont
des choix corrects**, et il faut le dire avant de parler des 4.

## Les 4 — dont un défaut réel, mesuré

**1. `vertex/positions/audit.py:30`** — le site du 418. Rappel seulement.

**2. `vertex/scanner/daily.py:62` — un RSI de 0 est effacé.** C'est la trouvaille
de ce lot.

```python
if float(d.get('rsi') or 50) < 45:
    bits.append('momentum faible')
```

`0.0` est *falsy* : la valeur la plus baissière qui existe est remplacée par le
neutre 50. Mesuré sur `_avoid_reason`, toutes autres entrées identiques :

```text
rsi = 40  (momentum faible)      → « … · momentum faible »
rsi = 1   (quasi extrême bas)    → « … · momentum faible »
rsi = 0   (extrême bas RÉEL)     → « … »            ← la raison DISPARAÎT
rsi ABSENT                       → « … »            ← même sortie que rsi = 0
```

Le trader reçoit **exactement la même explication** pour « je n'ai pas la donnée »
et pour « le momentum est au plus bas possible ». Et la raison est listée pour
`rsi = 1` mais pas pour `rsi = 0` : **la fonction est non monotone à sa propre
frontière.**

L'ironie avec le lot 416 mérite d'être écrite : le même indicateur y était
**fabriqué à 100** là où il est indéfini ; il est ici **effacé à 0** là où il est
réel. Deux fautes opposées, une seule cause — traiter une valeur extrême
légitime comme une donnée manquante.

**3. `vertex/positions/reconciler.py:82`** —
`(loc.get('multiplier') or 100) != (b.get('multiplier') or 100)`. Le lot 418 a
mesuré que le côté courtier **ne porte jamais** de multiplicateur
(`fetch_positions` n'en lit pas). Cette comparaison oppose donc toujours la
valeur locale à un **100 fabriqué** : elle ne peut signaler qu'un écart local,
jamais une divergence réelle du courtier. Cohérent avec le 418, pas un dossier
neuf.

Et le contraste est **quatre lignes plus haut, dans le même bloc** :

```python
if la is not None and ba is not None and ba and abs(la - ba) / abs(ba) > 0.02:
```

Le coût moyen, lui, est gardé par un `is not None` explicite **et** par un
dénominateur non nul.

**4. `vertex/portfolio/portfolio_guard.py:19`** —
`(opts.get('open_options') or 0) >= profile.max_simultaneous_options`. Une
exposition **inconnue** est comptée comme **zéro**, donc le garde-fou
`MAX_OPTIONS_REACHED` ne se déclenche pas. Un garde qui s'ouvre quand la donnée
manque. **Lu, pas mesuré** — je ne l'ai pas exécuté et je ne prétends pas
qu'il soit atteignable dans un état réel.

## Ce que ce lot établit

**La forme du 418 est rare et le plus souvent inoffensive : 4 sites de détection
sur 22 replis, dont 1 défaut réel nouveau, 1 déjà connu, 1 conséquence d'un
défaut connu, 1 signalé sans mesure.** Il n'y a pas de campagne à lancer — et
c'était la question.

Le nouveau défaut (`daily.py:62`) est **rang 2** : la conséquence est un texte
d'explication incomplet, pas un chiffre faux ; elle ne survient que sur un RSI
exactement nul, lequel — mesuré au 416 — demande une baisse sans un seul jour de
hausse. Rare, mais c'est précisément le cas où l'avertissement compte le plus.
**Aucun GO, rien n'est engagé.**

## Portée

Le détecteur ne voit que les replis **littéraux dans une comparaison de `if`** :
un repli passé par une variable intermédiaire (`v = x or 0` puis `if v < …`) lui
échappe, et je ne l'ai pas quantifié. Les 18 « légitimes » ont été classés par
lecture de leur rôle, pas par exécution.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde lit par
  AST et n'appelle que des fonctions pures. Pas de preuve MD5 requise, pas de
  bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-troisième lot court, **quatrième d'affilée dans la veine des moteurs**.
Celui-ci ferme proprement la tranche : il transforme la trouvaille du 418 en
**décision facile** — 4 sites, pas 22, et un seul défaut nouveau.

Le motif de la veine se vérifie une quatrième fois : la bonne pratique est écrite
**tout près du défaut** — ici, le `is not None` du coût moyen, quatre lignes
au-dessus du multiplicateur non gardé.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
