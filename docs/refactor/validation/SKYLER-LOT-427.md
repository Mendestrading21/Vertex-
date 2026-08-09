# SKYLER LOT 427 — La légende annonce quatre indices, le graphique en trace trois : les couleurs glissent d'un cran

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-427` (base : lot 426 fusionné,
6777e48)

Onzième lot de la veine, **troisième mené depuis l'écran**. Le 426 avait
constaté que le vivier `limits:`/`conclusion:` était quasi épuisé (9 non
ouvertes, surtout des conventions d'affichage). La consigne était de
**l'élargir**. C'est fait, et l'élargissement a immédiatement produit une
trouvaille.

**Aucun code, aucun gardien, aucun test.**

## L'élargissement du vivier : 17 → 118

Le recensement du 425 ne prenait que `limits:` et `conclusion:`, de 15 à 150
caractères → **17 affirmations**. Même corpus servi (52 pages et vues, 43
fichiers `/static`, **3 829 722 octets**), filtre élargi aux huit familles de
champs :

```text
question       32        limits          11
why            22        conclusion       8
confirm        15        note             1
invalidate     15        shows           14
                                 TOTAL  118 affirmations distinctes
```

**Le vivier était sept fois plus grand que ce qui avait été recensé.** Sur les
118, **17 portent un chiffre** — donc un compte, un seuil ou une identité
vérifiable. C'est dans celles-là que j'ai choisi.

## L'affirmation ouverte

Carte **« Indices — performance comparée »** (`/markets`, `vx-mk-multi`) :

> `explain:{shows:'Les mêmes séries d’indices que le bandeau, rebasées à 0 %`
> `pour comparer la force relative.'}`

C'est une **affirmation d'identité** entre deux objets de la même page : le
bandeau d'indices en haut, et le graphique comparé en dessous. Vérifiable.

## Ce que le code fait — mesuré en EXÉCUTANT les octets servis

Les fonctions ont été **extraites du marquage servi** de `/markets` (appariement
d'accolades), puis **exécutées sous Node 22** avec `VXCharts` stubé, contre des
payloads de scan fabriqués. Ce n'est ni une lecture ni une transcription : c'est
le code servi qui tourne.

```javascript
// loadMultiIndex — 1 432 octets extraits du marquage servi
const wanted = ['S&P 500','Nasdaq','Dow Jones','Russell 2000'];
const sets   = wanted.map(n => ({n, spark:(by[n]&&by[n].spark)||[]}))
                     .filter(x => x.spark.length > 5);        // ← DONNÉES FILTRÉES
…
legend: wanted.map((n,i) => ({label:n, color:VXCharts.colors.series[i%6]})),  // ← LISTE FIXE
render: (cv) => VXCharts.multiLine(cv, labels, sets.map(…))
```

Et dans `chart-core.js:526`, servi lui aussi :

```javascript
datasets.map((d, i) => Object.assign({ borderColor: C.colors.series[i % 6], … }, d))
```

**La couleur d'une courbe vient de son rang dans `sets` (filtré) ; la couleur de
sa pastille de légende vient de son rang dans `wanted` (fixe).** Dès qu'un
indice manque, les deux numérotations divergent.

### Mesure

```text
cas                            légende servie                              courbes tracées                       courbes mal nommées
4 indices (nominal)            S&P=C0 Nasdaq=C1 Dow=C2 Russell=C3          S&P=C0 Nasdaq=C1 Dow=C2 Russell=C3            0   ← témoin positif
Nasdaq absent du scan          S&P=C0 Nasdaq=C1 Dow=C2 Russell=C3          S&P=C0 Dow=C1 Russell=C2                      2
Dow Jones absent               id.                                         S&P=C0 Nasdaq=C1 Russell=C2                   1
S&P 500 absent                 id.                                         Nasdaq=C0 Dow=C1 Russell=C2                   3
S&P 500 seul                   id.                                         S&P=C0                                        0
Russell 2000 seul              id.                                         Russell=C0                                    1
```

Lecture du cas « Nasdaq absent » : la pastille C1 annonce **« Nasdaq »**, la
courbe C1 tracée est **Dow Jones** ; la pastille C2 annonce **« Dow Jones »**, la
courbe C2 est **Russell 2000**. Et la légende continue d'annoncer un
quatrième indice qui n'est **pas tracé du tout**.

Le témoin positif (cas nominal, 0 décalage) et les témoins négatifs (1 à 3
décalages) encadrent la mesure.

## Et l'affirmation de départ, elle ?

Même méthode, `loadStrip` et `crossAsset` extraits du marquage servi et
exécutés :

```text
cas                                    bandeau   graphique   « les mêmes séries que le bandeau »
4 indices, historiques longs              4          4                  VRAI
Russell : 4 clôtures seulement            4          3                  FAUX
Nasdaq + Russell historiques courts       4          2                  FAUX
```

Les deux objets n'appliquent **pas le même filtre** : le bandeau garde un indice
dès qu'il a un **dernier cours** (`last != null`), le graphique exige une **série
de plus de 5 points** (`spark.length > 5`). L'affirmation « les mêmes séries »
est donc conditionnelle, alors qu'elle est écrite comme un fait.

## Pourquoi c'est visible à l'écran, et pas seulement dans le code

`VXCharts.card` rend la légende à pastilles dans le corps de la carte — extrait
des **octets servis** de `chart-core.js` :

```javascript
const legend = (opts.legend || []).map(l =>
  `<span><span class="vx-swatch" style="background:${l.color}"></span>${l.label}</span>`).join('');
…
(legend ? `<div class="vx-chart-legend">${legend}</div>` : '')
```

et `charts.css`, servi également, la rend visible :

```css
.vx-chart-legend{display:flex;flex-wrap:wrap;gap:4px 14px;…}
.vx-chart-legend .vx-swatch{display:inline-block;width:10px;height:10px;…}
```

**Détail aggravant** : `multiLine` réactive par-dessus la légende native de
Chart.js (`plugins:{legend:{display:true,position:'bottom'}}`), qui est
construite, elle, **à partir des jeux de données**. La carte porte donc **deux
légendes** — l'une correcte, l'autre décalée — qui se contredisent sur le même
écran.

## Ce que je n'ai pas observé, et que je dis

Aucun payload de scan persisté ne contient de clé `indices`
(`market_context_last.json`, `daily_prev.json` vérifiés) et le scan est vide au
démarrage : **je n'ai pas constaté de graphique réellement décalé sur données
réelles.** Le décalage est démontré **par exécution du code servi sur des
payloads fabriqués**, et sa porte d'entrée est établie — `terminal.py:449-457`
construit `indices` dans un `try/except: pass` par ticker, donc **un indice dont
le téléchargement échoue est simplement omis**. C'est exactement le mécanisme
constaté au 425 pour les maturités.

## Bornage

Deux sites seulement construisent une `legend:` sur mesure dans `vertex/ui/**` :
celui-ci, et la courbe des taux (`markets_page.py:599`) dont les deux jeux
(`cur`, `prev`) sont bâtis sur le même `pts` — **toujours deux, jamais filtrés :
légende correcte**. **1 site défectueux sur 2.**

Aucun test du dépôt ne mentionne `vx-mk-multi`, `loadMultiIndex` ni
`vx-chart-legend` : **le point n'est couvert par aucun gardien.**

## Classement

**Rang 1**, famille des 422 et 425 : les **valeurs** tracées sont réelles —
aucune série n'est inventée, aucun point n'est fabriqué. C'est le **nom** attaché
à la couleur qui devient faux quand une source manque, sur une carte dont le rôle
est précisément de **comparer des indices entre eux**. Un trader qui lit « la
courbe Nasdaq mène » lit en réalité la courbe du Dow Jones.

Correction pressentie, minuscule : construire la légende depuis `sets` et non
depuis `wanted` (`sets.map((x,i)=>({label:x.n,color:series[i%6]}))`), ce qui
corrige **du même geste** le décalage de couleur et l'indice fantôme ; et rendre
l'affirmation `shows:` conditionnelle. **Aucun GO, rien n'est engagé.**

## Portée

**Une seule** affirmation ouverte sur les **118** recensées. Les 117 autres sont
**listées, non vérifiées**. Le recensement lui-même reste borné aux littéraux
entre guillemets simples de 10 à 200 caractères : **les phrases construites
dynamiquement lui échappent toujours** et n'ont pas été comptées — c'est la
limite qui reste à lever.

Le stub de `VXCharts` reproduit la règle de coloration lue dans `chart-core.js` ;
Chart.js lui-même n'a pas été exécuté.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; les sondes
  rendent les pages en mémoire et exécutent du JS extrait, sans rien écrire. Pas
  de preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot runtime avec contrôle d'apparition : **21 fichiers** à la racine (et
  non 22 — un `desk_backup_*` est sorti de la fenêtre de 7 jours, rotation de
  l'application, pas de mon fait). Aucun apparu, aucun disparu.
- Les trois fichiers habituels sont ré-horodatés par la suite. **Cette fois je
  l'ai caractérisé** au lieu de le supposer : suite lancée **deux fois** avec
  copie du contenu entre les deux, comparaison JSON normalisée →
  `ai_enrichment.json` change son seul `as_of`, `desk_data.json` son seul `ts`,
  `weekly_snapshot.json` son seul `generated_at`. **Aucune donnée utilisateur
  modifiée.**
- Suite : **2864 passed / 0 skipped**, deux fois de suite.

## Où en est la boucle

Trentième lot court. Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ ·
421 ✗ · 422 ✓ · 423 ✗ · 424 ~ · 425 ✓ · 426 ✗ (bornage) · 427 ✓ (affiché,
prouvé)**.

Le bornage du 426 avait conclu « exception, pas symptôme » sur les affirmations
de **méthode** — et c'était juste. Mais il avait aussi désigné la vraie limite :
le vivier était mal recensé. **En l'élargissant, la première affirmation ouverte
a mordu.** Le motif de la veine tient une huitième fois, sous une forme nouvelle :
ici la règle n'est pas oubliée dans une phrase, elle est **rompue par un
filtre** — une liste fixe et une liste filtrée qui se croient alignées.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
