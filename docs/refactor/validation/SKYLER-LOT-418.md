# SKYLER LOT 418 — Le multiplicateur d'option vaut 100 partout, et le seul contrôle qui le surveille ne peut pas mordre

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-418` (base : lot 417 fusionné,
a918c76)

Troisième lot dans la veine des moteurs. Cible :
`vertex/positions/calculator.py`, dont le docstring pose une règle nette :

> *« donnée absente → None (jamais 0) »*

C'est une affirmation testable. Elle a été testée.

**Aucun code, aucun gardien, aucun test.**

## La règle est tenue — sauf sur un champ

Moteur exécuté en mémoire, mêmes entrées, seul le multiplicateur change :

```text
multiplicateur          market_value   P&L      delta   theta   data_quality  issues
ABSENT (clé manquante)     1000.0     +100.0   110.0   -16.0        OK          []
= 100 (standard)           1000.0     +100.0   110.0   -16.0        OK          []
= 10  (mini-option)         100.0     -800.0    11.0    -1.6        OK          []
= 22  (ajusté après split)  220.0     -680.0    24.2    -3.52       OK          []
= 0   (valeur invalide)    1000.0     +100.0   110.0   -16.0        OK          []
```

Même position : **P&L +100 avec l'hypothèse 100, −800 avec le vrai
multiplicateur 10.** Un changement de signe sur l'argent, les Greeks divisés par
dix, et `data_quality` reste **OK** sans la moindre alerte.

**Témoins de la règle, dans le même fichier** : Greeks absents → `delta = None` ·
`cost_basis = 0` → `unrealized_pnl_pct = None` · `mark` absent →
`market_value = None` et `overall = MISSING_MARK`. **La règle est appliquée
partout, sauf sur le seul champ qui multiplie tout le reste.**

## Mais il faut suivre la chaîne — et elle resserre le diagnostic

Le repli du calculateur (`mult = p.get('multiplier') or 100.0`) est en réalité
un **second** repli. Mesuré en remontant :

```text
ibkr_positions.fetch_positions   ne lit QUE symbol, position, avgCost, secType, currency
                                 → `contract.multiplier` n'est JAMAIS demandé à IBKR
repository.load_positions        construit le dict IBKR sans clé `multiplier`
models.option_position           `mult = _f(trade.get('multiplier')) or 100.0`  ← le vrai défaut
calculator.enrich_option         `mult = p.get('multiplier') or 100.0`          ← repli sur un défaut
```

Donc **toute position arrivant au calculateur porte déjà 100**. Le 100 n'est pas
improvisé au dernier moment : c'est une **convention produit assumée** —
`option_position` l'écrit dans son docstring (*« cost = qty × prime × 100 »*).

Ce que la chaîne montre vraiment : **le multiplicateur réel n'est jamais demandé
au courtier.** Pour un contrat non standard — mini-option, contrat ajusté après
un split ou une fusion — `average_cost`, `market_value`, le P&L et les quatre
Greeks sont faux, sans aucun signal.

Et le système **connaît** ce risque : `data_sources/reconciliation.py:134` lève
`MULTIPLIER_MISMATCH` (sévérité 3) dès qu'un contrat annonce autre chose que 100.
Ce détecteur travaille sur les **contrats** ; il ne voit jamais les **positions**.

## Le contrôle qui existe, et qui ne peut pas mordre

`vertex/positions/audit.py:30` :

```python
if (p.get('multiplier') or 100) <= 0:
    errs.append('MULTIPLIER_INVALID')
```

Exécuté sur toutes les valeurs invalides :

```text
multiplicateur              erreurs relevées
ABSENT (clé manquante)      —
None                        —
0                           —          ← la valeur même que « <= 0 » vise
0.0                         —
-100 (négatif)              MULTIPLIER_INVALID     ← seul cas qui mord
```

Cause : `or 100` remplace `None` **et** `0` (tous deux falsy) **avant** la
comparaison. **Le contrôle teste son propre repli, pas la donnée.**

**Le témoin est deux lignes plus haut, dans le même fichier :**

```python
if p.get('quantity') is None or (p.get('quantity') or 0) <= 0:
    errs.append('QUANTITY_INVALID')
```

Le `is None` explicite y est. Vérifié par exécution : `quantity` absente ou nulle
→ `QUANTITY_INVALID` **mord**, comme `STRIKE_MISSING` et `COST_BASIS_INVALID`.
**Deux lignes d'écart, la même forme, une seule écrite correctement.**

Et `MULTIPLIER_INVALID` **n'apparaît dans aucun test** — recherche sur
`tests/**` : zéro occurrence. Le code d'erreur n'est exercé nulle part.

## Classement — calibré, pas gonflé

Ce lot est **moins grave que le 416 et le 417**, et il faut le dire :
l'hypothèse « multiplicateur = 100 » est **juste pour l'écrasante majorité des
contrats** américains, elle est **documentée**, et le mauvais chiffre n'apparaît
que sur un contrat non standard.

- **Rang 2** — le multiplicateur réel n'est jamais lu chez le courtier alors que
  le système sait déjà le contrôler ailleurs (`MULTIPLIER_MISMATCH`). Conséquence
  bornée aux contrats non standard, mais l'erreur y est **silencieuse et
  multiplicative**.
- **Rang 4** — `MULTIPLIER_INVALID` ne peut détecter ni l'absence ni le zéro ;
  il ne sert qu'aux multiplicateurs négatifs, qui ne peuvent pas se produire
  puisque la valeur est fixée à 100 en amont. **Contrôle mort, deux fois.**

**Aucun GO, rien n'est engagé.**

## Portée

Un seul moteur ouvert, plus la chaîne d'alimentation nécessaire pour savoir si le
défaut est atteignable — c'est ce parcours qui a **réduit** le diagnostic, pas
qui l'a gonflé. Je n'ai pas vérifié ce que devient une position d'option IBKR par
ce chemin au-delà du multiplicateur : `fetch_positions` ne transmet ni `right`,
ni `strike`, ni `exp`, et la question de savoir ce qui en résulte n'a **pas** été
mesurée ici — elle n'appartient pas à ce lot.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; les sondes vivent
  dans le scratchpad et n'importent que des fonctions pures. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-deuxième lot court, **troisième d'affilée dans la veine des moteurs, trois
trouvailles**. Le motif se confirme et se précise : dans les trois cas, la bonne
pratique est **écrite à quelques lignes du défaut** — 416 : `pos = 50.0` quand
`hi == lo` ; 417 : `tp1_resolved` dans le même dictionnaire ; 418 : le `is None`
explicite deux lignes au-dessus.

**Chercher la règle que le fichier respecte ailleurs, puis l'endroit où il
l'oublie** — c'est la méthode la plus rentable trouvée depuis le lot 398.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
