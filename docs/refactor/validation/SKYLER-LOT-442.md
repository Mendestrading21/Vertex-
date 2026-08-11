# SKYLER LOT 442 — « R:R structurel 3 » : le seul R:R affiché sur la page d'analyse vaut 3 sur tous les marchés, et celui qui varie — lu par huit moteurs — n'est affiché nulle part

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-442` (base : lot 441 fusionné,
d77eb23)

Vingt-quatrième lot de la veine. Le 441 avait ouvert la route `/analysis` à
paramètre et y avait **recensé cinq affirmations sans en ouvrir aucune**. Ce lot
en ouvre une — celle qui promet « moyennes mobiles 20/50/200 et niveaux du plan
moteur » — et en trouve une autre en chemin.

**Aucun code, aucun gardien, aucun test.**

## Ce que je cherchais : la promesse des trois moyennes mobiles

`analysis_page.py:414`, dans le tiroir « Comprendre ce graphique » :

```javascript
shows:'Chandeliers (ou clôtures) du titre, moyennes mobiles 20/50/200 et
       niveaux du plan moteur : entrée, stop (invalidation), objectifs.'
```

Trois moyennes annoncées. Vingt lignes plus haut, le code les **filtre** :

```javascript
].filter(o => o.data && o.data.some(x => x != null));   // analysis_page.py:389
```

Et le moteur le documente lui-même (`engines/analysis.py:266-268`) : *« Une
moyenne indisponible (fenêtre trop courte) → None. »*

**Mesuré sur le moteur réel**, en appelant `analyse()` sur des historiques de
longueurs croissantes et en appliquant le filtre exact de l'interface :

```text
barres d'historique   carte tracée ?   MM annoncées   MM réellement tracées
        11                 oui           20/50/200      1   (MM20)
        30                 oui           20/50/200      1   (MM20)
        60                 oui           20/50/200      2   (MM20, MM50)
       120                 oui           20/50/200      2   (MM20, MM50)
       199                 oui           20/50/200      2   (MM20, MM50)
       200                 oui           20/50/200      3   (MM20, MM50, MM200)
       400                 oui           20/50/200      3
```

Le seuil est **exactement 200 barres**, et la carte est tracée **dès 11**. C'est
la famille du 425 (« 4 maturités réelles » en dur, courbe tracée dès 2 points).

**Une atténuation réelle, mais qui ne couvre pas le tiroir** : la légende de la
carte est bâtie depuis `shownOverlays()` (`candlestick-lwc.js:69`), donc elle
n'affiche que les courbes tracées — le dépôt fait le bon geste **dans le même
fichier**. Mais la phrase fautive est dans le **tiroir**, et le tiroir
(`chart-core.js:167-175`) ne rend **ni la légende ni les limites de la carte** :
il rend `shows`, `why`, `confirm`, `invalidate` et une ligne de source. Le lecteur
qui ouvre « Comprendre ce graphique » lit « 20/50/200 » **sans** la légende sous
les yeux.

**Rang 2** : défaut affiché, atténué par une légende honnête **non co-visible**.

**Ce que je n'ai pas établi** : je n'ai **pas observé** de titre réel à moins de
200 barres. Le cas est prévu par le moteur (son commentaire, et une quinzaine de
gardes `if len(c) > N`) et la carte se trace dès 11 barres — mais la
**fréquence** du cas dans l'univers réel n'est pas mesurée, et je ne la
suppose pas.

## Ce que j'ai trouvé en chemin, et qui pèse plus lourd

Le même bloc rend la conclusion de la carte (`analysis_page.py:402`) :

```javascript
conclusion:(d.verdict ? ('Verdict technique moteur : '+d.verdict) : '—')
  + (plan.rr ? ` · R:R structurel ${plan.rr}` : '')
```

Et `plan.rr` a **un seul écrivain dans tout le dépôt** (`analysis.py:262`) :

```python
'tp3': round(last + 3 * risk, 2), 'rr': 3.0, 'atr': round(atr, 2),
```

**Un littéral.** Le R:R affiché n'est pas calculé : il est la **définition** de
`tp3` (`tp3 = entrée + 3 × risque`), relue à l'envers.

### Mesuré sur six marchés très différents

```text
cas                      entrée     stop      tp3   R:R structurel   rr_res (jamais affiché)
haussier calme           113.51   107.83   130.56             3.0                       0.4
haussier violent         110.25   100.85   138.44             3.0                       0.7
baissier                  71.89    67.86    84.01             3.0                       1.1
plat                     105.27   102.68   113.02             3.0                       3.5
très volatil              30.28     27.00    40.13            3.0                       1.1
court (120 barres)       101.86    98.84   110.90             3.0                       4.7

valeurs distinctes de « R:R structurel »  →  [3.0]
valeurs distinctes de rr_res              →  [0.4, 0.7, 1.1, 3.5, 4.7]
```

**Témoin positif intégré** : entrée, stop et TP3 varient fortement d'un cas à
l'autre — le moteur réagit bien aux données. **Seul `rr` ne bouge pas**, et il ne
peut pas bouger.

### Et le R:R qui varie, lui, n'est affiché nulle part

`rr_res` — le R:R vers la résistance, calculé **une ligne plus bas** — est lu par
**huit consommateurs** :

```text
engines/committee.py:42        engines/decision_stack.py:99 et :209
engines/decide.py:91           engines/evidence.py:108
engines/skyler_core.py:283     research/chart_read.py:135
app/routes/planning_api.py:33 → planning/order_ticket.py:122
```

Mesuré sur les octets servis de la page :

```text
« R:R structurel »   2 occurrences   (libellé affiché)
plan.rr              7 occurrences   (4 rendus distincts)
rr_res               0 occurrence    *** JAMAIS SERVI ***
```

**Le R:R qui décide n'est jamais montré ; le R:R montré ne peut pas varier.**

Les quatre rendus de `plan.rr` : la conclusion de la carte principale (`:402`),
l'`aria-label` de l'échelle risque/récompense (`:582`), la ligne
« R:R structurel » de la carte plan (`:591`), et le libellé d'horizon du cône de
projection (`:600`).

## Pourquoi c'est un rang 1, et ce qui l'atténue

**Ce qui l'atténue, et je le dis d'abord** : le mot « structurel » peut se lire
« par construction », et le chiffre n'est pas **faux** — le plan a bien un R:R de
3 face à TP3, puisque TP3 est défini comme trois fois le risque. Ce n'est pas la
famille du 407 (chiffre faux).

**Ce qui le rend grave quand même** : la ligne « R:R structurel » est **dans une
liste de cinq valeurs par titre** — Entrée, Stop, TP1, TP2, TP3 — qui, elles,
varient toutes. Rien ne signale que la sixième est une tautologie. Un lecteur qui
compare deux titres lit **3 pour les deux** et croit avoir comparé quelque chose ;
la vraie différence, entre un `rr_res` de 0,4 et un de 4,7, est **calculée, elle
sert à décider dans huit moteurs, et elle n'atteint pas l'écran**.

C'est le croisement de deux motifs déjà établis : **428** (un calcul constant par
construction, présenté comme une mesure) et **433** (l'information honnête est
déjà calculée, mais ne sert aucune phrase). Et, comme au 434 et au 439, le
**contre-exemple est dans le même fichier, une ligne plus bas**.

Correction pressentie : afficher `rr_res` à côté — il est déjà calculé, déjà
arrondi, déjà servi dans le payload. **Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne mentionne « R:R structurel » : **aucun gardien.**

## Une hypothèse que je ne retiens pas, et pourquoi

J'ai vérifié le repli du gabarit `invalidate` : si `plan.stop` manquait,
`VX.fmt.nd(undefined)` rend `'—'` (`vx-core.js:43`) et la phrase deviendrait
« Clôture sous le stop — — la thèse est invalidée ». **Le cas ne se produit pas** :
mesuré sur six longueurs d'historique de 11 à 250 barres, `plan.stop` est
**toujours** un nombre réel. Le repli `d.plan||{}` existe côté interface, mais le
moteur remplit le plan sans condition. **Résultat négatif, publié comme tel.**

## Classement

- **`R:R structurel` constant à 3, `rr_res` jamais affiché** → **rang 1**.
- **« moyennes mobiles 20/50/200 » annoncées, 1 à 3 tracées** → **rang 2**
  (atténué par une légende honnête, non co-visible dans le tiroir).
- **repli `—` du stop** → **écarté**, cas non atteignable.

Une affirmation sur cinq est ouverte, quatre restent recensées non vérifiées
(`question`, `why`, `confirm`, `invalidate`).

## Portée

Les deux mesures sont faites en appelant le **moteur réel** sur des séries
**synthétiques** : c'est un banc, pas le marché. Ce qu'il établit, c'est le
**comportement du code** face à des entrées — pas la fréquence des cas dans
l'univers suivi.

Je n'ai **pas ouvert de navigateur** : la chaîne du rang 1 est établie sur les
octets servis (`plan.rr` lu 7 fois, `rr_res` 0 fois) et sur l'unique écrivain du
champ. Le rendu SVG du cône et de l'échelle n'est pas exécuté.

Le seuil de 200 barres est mesuré sur le calcul `rolling(200)` du moteur ; la
**part des titres concernés dans l'univers réel n'est pas mesurée**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. La route `/analysis` à paramètre appelée en **GET**
  (lecture) ; `persist` redirigé vers un répertoire temporaire ; `analyse()`
  appelée sur des `DataFrame` en mémoire, sans écriture.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée — lancée **après** l'écriture des
  trois documents (leçon du 441).

## Où en est la boucle

Quarante-cinquième lot court. Séquence : **439 ✗ · 440 bilan · 441 ✗ (piste
refermée) · 442 ✓**.

Après trois lots sans défaut de produit nouveau, celui-ci en rend deux — et il
les rend là où le 441 avait dit qu'il fallait chercher : dans les cinq
affirmations d'une page que la boucle n'avait ouverte que la veille. La veine
n'était pas épuisée, elle n'était pas ouverte.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
