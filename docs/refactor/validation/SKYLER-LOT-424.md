# SKYLER LOT 424 — « Thèse INTACT, confiance 0.0 » : le titre médian reçoit un verdict sans une seule preuve

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-424` (base : lot 423 fusionné,
34cef40)

Huitième lot dans la veine des moteurs. Cible :
`vertex/positions/thesis_health.py` — la **santé de thèse** de chaque position
déclarée par le trader. Choisi selon la consigne du lot précédent : **entrées
utilisateur, donc réellement variables**, et **chaîne vérifiée avant d'investir
dans la mesure**.

**Aucun code, aucun gardien, aucun test.**

## La règle que le fichier respecte — et il la respecte beaucoup

Ce module est l'un des plus honnêtes du dépôt. Il tient un compteur d'**inconnues**
dimension par dimension, il expose `confidence = connu / (connu + inconnues)`, et
son docstring porte même une correction du lot 365 (« PORTFOLIO_FIT n'est PAS
évalué ici … ne pas le supposer »). Le statut `UNKNOWN` existe dans son contrat
et il s'en sert :

```text
thèse absente                          UNKNOWN   conf 0.0   unk 1
thèse écrite, AUCUNE donnée            UNKNOWN   conf 0.0   unk 4
preuves positives (fond 70, rs 65)     STRENGTHENING   conf 1.0   pos 2
preuves négatives (fond 30, rs 20)     AT_RISK         conf 1.0   neg 2
```

Quatre témoins, deux de chaque côté. Le moteur **sait** dire qu'il ne sait pas.

## L'endroit où il ne la tient pas — et ce n'est pas un cas de bord

Chaque dimension n'émet une preuve qu'aux extrêmes : fondamental ≥ 60 ou < 45 ·
force relative ≥ 60 ou < 40 · R:R restant ≥ 2 ou < 1 · earnings dans 0-30 jours.
**Entre les deux, rien** — ni preuve, ni inconnue. Un titre entièrement médian
traverse donc les quatre dimensions sans laisser de trace, et tombe dans le
`else` final :

```python
elif len(unknowns) >= 3:
    overall = 'UNKNOWN'
else:
    overall = 'INTACT'        # ← le titre médian atterrit ici
```

Mesuré :

```text
fond 52 · rs 50 · R:R 1.4 · earnings J+60     statut = INTACT   conf = 0.0
                                              pos 0 · neg 0 · unk 0
```

**Zéro preuve positive, zéro preuve négative, zéro inconnue — et le verdict est
« thèse INTACTE ».** Le moteur a évalué ses quatre dimensions, n'a rien trouvé,
et conclut que la thèse tient.

La contradiction est dans le même dictionnaire : **statut `INTACT`, confiance
`0.0`**. Le premier affirme, le second dit qu'il n'y a rien derrière.

`UNKNOWN` est réservé aux données **manquantes**, jamais aux données
**non concluantes** — alors que c'est exactement le même aveu d'ignorance.

## Ce n'est pas un cas de bord

Les quatre conditions à réunir sont : fondamental entre 45 et 60, force relative
entre 40 et 60, R:R restant entre 1 et 2, résultats à plus de 30 jours. **C'est
le titre médian**, pas un cas construit. Contrairement aux lots 421 et 423, la
mesure porte ici sur des entrées **ordinaires et atteignables** : le `p` vient
des positions déclarées par le trader, le `d` du scan.

## Mais je dois m'appliquer la règle du 411 : est-ce AFFICHÉ ?

Chaîne mesurée :

```text
recalculator.py:76-78     p['thesis_health'] = assess(...)['overall_status']
positions_api.py:54-62    /api/positions/state  → jsonify(state)          ← SERVI
portfolio_page.py:478     posState = await VX.fetch('/api/positions/state')
portfolio_page.py:538     actionListHtml(posState)   → colonne « Statut »
recalculator.py:105       'thesis_invalidated': p.get('thesis_health') == 'INVALIDATED'
```

Le champ est **calculé et servi au client**. En revanche, la seule consommation
que j'aie tracée dans les moteurs est un **booléen `INVALIDATED`** — pour lequel
`INTACT` et `UNKNOWN` sont équivalents. Et je **n'ai pas établi** que la colonne
« Statut » de la liste d'actions rende `thesis_health` plutôt que le statut de
cycle de vie. Aucune recherche sur `vertex/ui/**` ni sur les fichiers servis ne
fait apparaître `thesis_health` ni les libellés `STRENGTHENING`/`WEAKENING` en
dehors de `markets_page.py`, où ils désignent autre chose.

**Donc : défaut réel, sur des entrées ordinaires, servi au client — mais son
affichage n'est pas prouvé.** Je l'écris ainsi plutôt que de supposer.

## Classement

**Rang 2.** Le verdict est faux au sens propre — « INTACTE » est une affirmation
que rien ne soutient — mais je n'ai pas prouvé qu'un œil humain le voie. Ce
n'est ni le 422 (affiché, rang 1) ni le 421/423 (inatteignable, rang 4) : c'est
entre les deux, et le dire est plus utile que de trancher au hasard.

Correction pressentie, dans l'esprit du fichier : quand `pos_ev` et `neg_ev` sont
**tous deux vides**, rendre `UNKNOWN` plutôt que `INTACT` — le statut existe déjà,
et `confidence` vaut déjà 0.0. **Aucun GO, rien n'est engagé.**

## La décision de veine, prise

La consigne était : *si ce lot rend une troisième fois « défaut réel mais
inatteignable », déclarer la veine épuisée.* **Le critère n'est pas rempli** — le
cas mesuré ici est parfaitement atteignable, et c'est le titre médian.

Mais il faut voir la pente :

```text
422   défaut réel · atteignable · AFFICHÉ (la carte montre ses limites, celle-là manque)
423   défaut réel · INATTEIGNABLE
424   défaut réel · atteignable · SERVI, affichage NON PROUVÉ
```

La conséquence s'amincit à chaque lot. **Critère durci pour le 425 : si le lot
suivant ne produit pas un défaut dont la valeur est PROUVÉE AFFICHÉE, la veine
des moteurs sera déclarée épuisée et la famille changera au 426.** Le compteur ne
porte plus sur « trouver », mais sur « atteindre l'écran ».

## Portée

Un seul moteur, une seule fonction (`assess`). Je n'ai pas suivi la colonne
« Statut » de `actionListHtml` jusqu'à sa source exacte — c'est précisément la
limite que je déclare. Le gardien `tests/test_thesis_health_dimensions_lot365.py`
existe (cité par le docstring) mais n'a pas été ouvert ici.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde importe
  une fonction pure et l'appelle avec des dicts fabriqués. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-septième lot court. Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ ·
421 ✗ · 422 ✓ · 423 ✗ · 424 ~**. Le motif — *la règle que le fichier respecte
ailleurs* — tient une sixième fois, et sur le module le plus scrupuleux ouvert
jusqu'ici : c'est justement parce qu'il compte ses inconnues qu'on voit qu'il en
oublie une catégorie.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
