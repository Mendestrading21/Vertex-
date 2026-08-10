# SKYLER LOT 501 — L'espion d'exécution étendu aux HUIT sous-objets du détail : ZÉRO clé absente. Le bornage du 499 tient un niveau plus bas — et les deux « manques » apparents sont, l'un mon propre banc, l'autre un garde qui fonctionne

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-501` (base : lot 500 fusionné,
`a67049c0`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

## Le choix

**(b)**. L'espion du 499 est l'instrument le plus fiable construit ici — **zéro
faux positif par construction** — et son périmètre était **explicitement borné à
un seul niveau** : le rapport disait « les sous-objets (`plan`, `sub`, `series`)
ne sont pas espionnés ». L'étendre coûte peu et teste une frontière que j'ai
moi-même posée.

**(a)** — le coût de démarrage en millisecondes — et **(c)** — les huit rangs
relatifs jamais re-vérifiés — **restent des dettes nommées**. **(a) en est à son
troisième report**, et je le note plutôt que de le laisser filer.

## L'instrument et sa calibration à trois étages

Les **huit** sous-objets dict du détail sont espionnés, pas trois : `plan`,
`sub`, `series`, `signals`, `structure`, `vertex`, `physics`, `mtf` (règle 485 —
le même test sur tous les objets du même genre). Plus les objets du desk.

```text
1. CHARGE          20 titres · 160 sous-objets espionnés · 20 positions chargées   OK
2. POSITIF, MÊME GENRE   on RETIRE `plan['stop']` d'un détail témoin
                   → l'espion l'enregistre 8 fois                                  OK
3. NÉGATIF         `plan['entry']`, présent partout → enregistré 0 fois            OK
```

**Caveat nommé d'avance** pour le bras desk : une position utilisateur peut
légitimement omettre un champ optionnel — une absence n'y serait pas un défaut.
La position de banc est donc **maximalement remplie** avec les **30 clés** que
`vertex/positions/*.py` lit. Ce qui manque encore serait une clé que **personne
n'écrit jamais**.

## Le résultat : rien

```text
sous-objet    lectures réussies    clés absentes
plan            1 100  +  520            0
trade           1 520                    0     (position maximalement remplie)
sub               680  +   32            1  →  `options`, voir plus bas
signals           312  +  124            0
structure         216                    0
physics           136                    0
vertex             72                    0
mtf                68                    0
series             16                    0
entrySnap         200                    1  →  `thesis`, voir plus bas
```

**Le bornage du 499 tient un niveau plus bas.** La famille « clé lue sur un objet
qui ne la porte pas » est bien un phénomène du **premier niveau du détail**, et
de lui seul.

## Les deux « manques », tous deux refusés à la lecture

**`entrySnap['thesis']`, 40 fois — c'est MON BANC.** Le second bras de mon
exercice retire délibérément la thèse pour reproduire la configuration du 497.
L'espion enregistre donc une absence que j'ai créée. **Publier ça aurait été
publier mon propre montage.**

**`sub['options']`, 68 fois — le garde fonctionne.** Site unique, localisé par
capture de pile : `decision_stack.py:176`.

```python
subscores = [{'label': _SUB_LABELS[k], 'value': int(sub[k]), …}
             for k in ('technical', 'momentum', 'fundamental', 'risk', 'options')
             if isinstance(sub.get(k), (int, float))]        # ← le garde
```

Et la clé **n'existe légitimement pas** : `analysis.py:203` appelle
`scoring.compose(ind, fund=fund)` **sans `opt`**, donc `options_score(None)`
rend `None` et `parts` ne porte pas `'options'`. La note affichée avec le bloc
annonce d'ailleurs exactement **quatre** sous-scores. **Rien n'est promis qui ne
soit rendu.**

**Une clé morte suivie d'un garde qui marche n'est pas un défaut** — règle posée
au 499, **deuxième occurrence en trois lots**.

**Arrêtés avant publication : 77 → 79.**

## Le second contrôle — ce que l'espion NE PEUT PAS voir, et il est vide ici

L'espion intercepte `get`, `[]` et `in`. Il est **structurellement aveugle à
l'itération** : `for k, v in sub.items()` ne passe par aucun de ces trois, et une
clé qui devrait être là serait silencieusement sautée.

**Mesuré sur tout le code serveur : ZÉRO itération** (`.items()`, `.keys()`,
`.values()`) sur les huit sous-objets. **L'angle mort existe, et il est vide
ici** — ce n'est pas une supposition, c'est un comptage.

Second volet, plus embarrassant : au premier passage, **`series`, `structure` et
`vertex` affichaient 0 lecture**. Ce n'est pas « propre », c'est **« jamais
exercé »** — et les deux se lisent pareil dans un tableau de zéros. J'ai donc
ajouté des exercices ciblés (`committee.evaluate`, `quant_engine.evaluate` ×8,
`/api/strategy/decision` ×8, `/api/system/status`) : **16, 216 et 72 lectures**,
toujours **zéro absence**. **Un zéro de couverture et un zéro de propreté sont
indiscernables tant qu'on ne compte pas les lectures réussies.**

## Ce que le lot trouve sans le chercher

`decision_stack._decomposition` construit un bloc complet — sous-scores
étiquetés, ajustements physique et multi-horizons, note pédagogique.
**Mesuré dans les octets servis : `subscores` 0 · `decomposition` 0 ·
`is_proxy` 0.**

Le moteur dont la **confiance** et l'**accord** sont affichés sur `/analysis`
(492) calcule aussi une **traçabilité du score que personne ne peint**.
**Nommé, non classé** (règles 486, 491, 492) — et c'est une observation, pas un
dossier.

## Portée

- **Zéro absence** vaut pour les **chemins exécutés** : 32 exercices puis un
  second jeu ciblé. Les chemins non couverts échappent, comme au 499.
- Le bras **desk** est concluant **parce que la position est maximalement
  remplie** ; sur une position utilisateur réelle, une absence serait
  ininterprétable.
- Les sous-objets **de troisième niveau** (par exemple `vertex['mc']`,
  `vertex['rr_detail']`, `plan` imbriqué dans un paquet) **ne sont pas
  espionnés**. La frontière a bougé d'un cran, elle n'a pas disparu.
- Le site de `sub['options']` est établi **par capture de pile à l'exécution**,
  pas par recherche textuelle.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** ; positions **fabriquées en mémoire**,
  `desk_data.json` jamais ouvert en écriture ; **aucune route réseau sortante**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Résultat **négatif, et c'est ce qu'on lui demandait** : la frontière que le 499
avait posée par prudence tient à la mesure. Ce lot ne trouve pas de défaut ; il
retire une inconnue.

Le fait de méthode est neuf et il est chiffré : **un zéro de couverture ressemble
exactement à un zéro de propreté.** Trois sous-objets affichaient « 0 clé
absente » alors qu'ils n'avaient tout simplement **jamais été lus**. Sans la
colonne « lectures réussies » à côté, j'aurais publié une propreté que je n'avais
pas mesurée. **Un compteur d'absences ne veut rien dire sans son compteur de
présences.**

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
Dettes nommées qui restent : le **coût de démarrage en millisecondes**
(troisième report) et les **huit rangs relatifs jamais re-vérifiés**.

Comptes séparés : résultats faux **arrêtés avant publication 79 (+2)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
