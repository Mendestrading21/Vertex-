# SKYLER LOT 436 — `/api/command` sert dix champs, le produit en lit deux : 95 % du payload ne va nulle part, et la suite en défend une partie

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-436` (base : lot 435 fusionné,
99c3550)

Dix-neuvième lot de la veine. Le 435 avait mesuré qu'un champ de `/api/command`
— la **décision du jour** — était calculé, sérialisé, envoyé et **jamais lu**. La
question évidente : **est-il le seul ?**

**Aucun code, aucun gardien, aucun test.**

## La leçon du 435, appliquée D'ABORD

Le 435 avait perdu du temps à qualifier un défaut avant de vérifier qu'il
atteignait quelqu'un. Ici l'ordre est inversé : **d'abord la consommation, ensuite
le contenu.** Et le comptage est **littéral** avant d'être régulier — le motif
sans `DOTALL` du 435 avait rendu « 0 appel » là où il y en avait 16.

## Mesure — qui lit quoi, dans les octets servis

```text
champ de /api/command   accès `X.champ` dans les 3 829 722 octets servis
alerts                    4     LU
top_stocks               12     LU
counts                    0     *** JAMAIS LU ***
decision                  0     *** JAMAIS LU ***   (confirmé au 435)
exposure                  0     *** JAMAIS LU ***
portfolio_score           0     *** JAMAIS LU ***
regime                    0     *** JAMAIS LU ***
risk                      0     *** JAMAIS LU ***
top_options               0     *** JAMAIS LU ***
validation                0     *** JAMAIS LU ***

→ 2 champs sur 10 sont lus. 8 sont calculés, sérialisés, envoyés — et jamais lus.
```

**Témoin positif** : l'instrument détecte bien les deux champs dont la lecture
était déjà établie au 435 (`top_stocks` 12 accès, `alerts` 4). Il mord là où il
doit.

**Durcissement** (leçon 434/435) — trois formes échapperaient au motif
`X.champ` :

```text
déstructuration `const {…} = cmd`      0
accès par crochet `cmd[…]` / `c[…]`    6 formes distinctes : c[0] c[1] c[d] c[h] c[k] c[l]
itération `Object.keys(cmd)`           2 → internes Chart.js + /api/system/config
```

Les six formes à crochets sont la carte d'échappement HTML et des internes
Chart.js ; les deux itérations ne portent pas sur ce payload. **Rien
n'échappe.**

## Le poids

```text
payload /api/command sur un scan VIDE      628 octets
   champs lus (top_stocks, alerts)          32 octets
   champs jamais lus                       596 octets   ← 95 %
```

Et ce ne sont pas des champs gratuits : `risk` déclenche
`portfolio_risk.build(...)` (`command.py:105`) et `validation` déclenche
`validator.build(...)` (`:117`). **Deux moteurs tournent à chaque appel pour un
résultat que personne ne lit**, avec un TTL client de 30 à 60 secondes.

## `exposure` : ce n'est même pas un calcul

Le champ que je venais chercher, `command.py:123` :

```python
'exposure': {'actions': '70-90%', 'options': '10-20%', 'etf': 'tampon / cash'}
```

**Un littéral inline dans le `jsonify`.** Il ne dépend ni du marché, ni du
régime, ni du portefeuille, ni du scan — il ne varie **jamais**. Ma présomption
d'entrée (« des fourchettes d'allocation affirmées sans données ») était juste sur
le fond et **trop généreuse sur la forme** : il n'y a pas de calcul discutable,
il y a une constante. Et elle n'est lue par personne.

**Rang 4** : si un jour un consommateur l'affichait, il présenterait une
allocation fixe comme une recommandation ; aujourd'hui, elle ne va nulle part.

## Le point qui mérite d'être signalé : la suite défend l'inutilisé

`tests/test_command_routes.py` :

```python
assert j['decision']['action'] == 'RÉDUIRE / DÉFENSIF'   # :39 et :47
assert j['counts'] == {'ACHETER': 1}                     # :68
```

**Trois assertions portent sur deux champs qu'aucun consommateur servi ne lit.**
Ce n'est pas un gardien faux — il vérifie exactement ce qu'il dit. C'est un
gardien qui **protège une sortie que le produit n'affiche pas** : il rendrait
toute suppression coûteuse, et il donne l'impression que le champ compte.

C'est l'inverse du motif habituel de la boucle (un gardien vert dont le périmètre
s'arrête avant le défaut, 381/414/415) : ici le périmètre est **au-delà** du
produit.

## Classement

**Rang 3.** Aucun mensonge à l'écran — c'est précisément le problème : rien de
tout cela n'atteint l'écran. Ce qui reste est du **poids mort servi** : 95 % d'un
payload, deux moteurs exécutés pour rien à chaque appel, et trois assertions qui
figent l'ensemble.

Correction pressentie — et elle demande une **décision de produit**, pas une
correction de deux lignes : soit ces huit champs ont un consommateur prévu et il
manque, soit ils n'en ont pas et l'endpoint doit maigrir. **Aucun GO, rien n'est
engagé.**

## Portée

Je n'ai mesuré que **les octets servis** : un consommateur externe (script,
client tiers, appel manuel) lirait ces champs sans que mon instrument le voie.
Le dépôt étant un terminal personnel en lecture seule, je considère la mesure
représentative — mais c'est une **appréciation**, pas une preuve, et je la marque
comme telle.

La mesure du poids est faite sur le **scan vide du démarrage** : avec un scan
réel, `top_stocks` et `risk` grossissent tous les deux et la proportion de 95 %
changerait. **Le rapport 2 champs sur 10, lui, ne dépend pas de l'état** — c'est
une propriété du code, pas des données.

Je n'ai pas chronométré `portfolio_risk.build` ni `validator.build` : leur coût
est **constaté par lecture du code**, pas mesuré.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure, et
  **re-vérifié après chaque `cd` dans le scratchpad** (incident du 435).
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. L'appel à `/api/command` est un GET, donc une lecture.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-neuvième lot court. Séquence : **433 ✓ · 434 ✓ · 435 ~ · 436 ~**.

Deux lots de suite qui **descendent** leur propre trouvaille : le 435 parce que la
phrase n'atteignait personne, celui-ci parce que rien du payload n'atteint
personne. C'est cohérent, et c'est un résultat en soi : **`/api/command` est une
route dont le produit a cessé de se servir sans que personne l'écrive.** Le seul
signe extérieur est un gardien qui continue de la défendre.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
