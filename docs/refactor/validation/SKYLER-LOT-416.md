# SKYLER LOT 416 — Un titre qui n'a pas bougé affiche « RSI 100 », et le gardien qui dit « neutre » accepte l'extrême

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-416` (base : lot 415 fusionné,
cd37e4e)

**Changement de famille, comme annoncé.** Les lots 413-415 mesuraient la
couverture des gardiens sur les octets servis. Celui-ci descend dans les
**moteurs de calcul**. Le rendement n'est pas le même.

**Aucun code, aucun gardien, aucun test.**

## Le point de départ : une prémisse, et elle est fausse

Le RSI de Vertex porte sa justification dans son propre docstring
(`vertex/engines/indicators.py:13`) :

> *« dn==0 (aucune baisse) → 100, **jamais NaN (casserait le JSON)** »*

C'est la raison invoquée pour ne pas rendre « donnée absente ». Elle a été
mesurée :

```text
jsonify({'x': float('nan'), 'y': float('inf')})  →  {"x":null,"y":null}
```

**Flask assainit déjà.** Un `NaN` sort en `null` — du JSON parfaitement valide,
que le client sait déjà rendre en `—`/`n/d`. La prémisse qui justifie le choix
**ne tient pas dans cette pile**.

*Le témoin a fermé une question avant même de la poser* : la sonde prévue —
« un `NaN` peut-il casser `JSON.parse` côté navigateur ? » — s'est arrêtée sur
son propre contrôle. C'est le contrôle qui a produit le résultat.

## Ce que rend le moteur, mesuré en mémoire

```text
série NORMALE (marche aléatoire, 300 pts)   RSI  63.1
baisse MONOTONE                             RSI   0.0
hausse MONOTONE (aucune baisse)             RSI 100.0     ← convention de Wilder, CORRECTE
série PLATE (300 × 100.0, aucun mouvement)  RSI 100.0     ← 0/0, indéfini, rendu comme l'extrême
```

Les deux dernières lignes rendent **la même valeur** pour deux situations
opposées. Un titre halté, illiquide, ou dont le flux répète le dernier cours,
est présenté comme **aussi suracheté qu'une envolée sans un seul jour de repli**.

La seconde implémentation, `vertex/market/indicators.py:85` (Python pur, utilisée
par `backtest`), fait exactement le même choix : `out[i] = … if avg_l > 0 else
100.0`.

## Où la valeur arrive

`vertex/engines/analysis.py:40` calcule, ligne 304 place `'rsi': round(r)` dans
la charge servie, et `vertex/ui/pages/analysis_page.py:472` l'affiche :
`kv('RSI', d.rsi)`. **Le nombre 100 est montré au trader, tel quel.**

## Ce que j'ai failli surestimer — et que la mesure a corrigé

`vertex/engines/committee.py:97` produit une **phrase de verdict** :
`Timing défavorable : RSI 100 (suracheté). On patiente.` J'ai voulu vérifier si
un titre plat pouvait la déclencher. Mesuré :

```text
plateau après hausse   RSI     dernier   MM50     above50 (condition de la phrase)
   3 jours             100.0   159.00    137.38   True
  21 jours             100.0   159.00    150.88   True
  45 jours             100.0   159.00    158.80   True
  60 jours             100.0   159.00    159.00   False
```

La phrase **est** atteignable sur un titre immobile depuis 45 jours. Mais il faut
dire l'autre moitié : dans ces séries il n'y a **aucun jour de baisse depuis le
début** — et « aucune baisse ⇒ RSI 100 » est la **définition de Wilder**, pas une
faute. Ce cas est contre-intuitif, il n'est pas faux.

Vérifié par sonde : neutraliser le seul cas `up == 0 ET dn == 0` laisse le
plateau-après-hausse à 100, parce que la moyenne mobile des hausses garde la
mémoire de la montée. **Le défaut est donc plus étroit que je ne l'ai cru** :

```text
titre PLAT DEPUIS TOUJOURS      RSI indéfini (0/0) rendu 100   ← faux, affiché
plateau APRÈS une hausse        RSI 100 par convention          ← correct
```

Sur une série parfaitement plate, `dernier > MM50` est faux — la phrase de
`committee.py` dit alors « sous la MM50 », pas « suracheté ». **Le nombre est
faux à l'écran ; la phrase de verdict, elle, ne ment pas.**

## Le gardien dit « neutre » et accepte l'extrême

`tests/test_calculations_golden.py:193` :

```python
def test_rsi_flat_series_is_neutral_not_zero():
    """Série plate : pas de mouvement — le RSI ne doit pas retomber à 0…"""
    val = indicators.rsi(pd.Series([100.0] * 30)).iloc[-1]
    assert not math.isnan(val) and 30 <= val <= 100
```

Le **nom** promet la neutralité, l'**assertion** admet `100`. Le test protège
contre le `0` (signal baissier extrême) et laisse passer le `100` (signal
haussier extrême) — il ne garde qu'une moitié de ce que son nom annonce.

**Il ne bloque pas la correction non plus** : sonde posée pour rendre `50.0` sur
le cas sans mouvement → les **31 tests golden passent**. Le coût de la correction
n'est donc pas dans la suite.

## Classement

**Rang 1** — un chiffre affiché comme réel alors qu'il est indéfini, sur une page
de décision. Mais **nettement moins grave que le 407** : le HHI y était faux d'un
facteur 170 dans le cas *nominal*, ici la valeur est juste dans le cas dominant
et fausse dans un cas de bord. Correction pressentie : rendre `None` (donc
`null`, donc `—`) quand il n'y a **ni hausse ni baisse** sur la fenêtre — deux
lignes, deux moteurs, plus le nom du gardien à mettre en accord avec son
assertion. **Aucun GO, rien n'est engagé.**

## Portée

Un seul indicateur a été ouvert. Le recensement statique montre **641 divisions
dans `vertex/**` hors UI, dont 481 à dénominateur non constant et non protégé par
`max()`/`or`** — c'est un **vivier trié par la forme**, pas une liste de défauts,
et le lot 408 a déjà montré ce que valent ces viviers. Aucune campagne n'est
lancée. Rien n'a été mesuré sur les 480 autres.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier livré modifié.** La sonde sur `vertex/engines/indicators.py`
  **restaurée à l'octet** (`git status` vide, moteur ré-interrogé après
  restauration : série plate → 100.0, comportement d'origine). Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle — la note de cadence, tranchée

La consigne du 416 était explicite : si le lot rendait une quatrième fois « produit
sain, gardien à périmètre court », déclarer la veine épuisée. **Ce n'est pas le
cas.** Changer de famille a produit, en un lot : une prémisse de conception
fausse, une valeur indéfinie affichée, et un gardien dont le nom contredit
l'assertion.

La veine « couverture des gardiens sur les octets servis » reste **close en
rendement** ; celle des **moteurs de calcul** vient de s'ouvrir et paie mieux.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
