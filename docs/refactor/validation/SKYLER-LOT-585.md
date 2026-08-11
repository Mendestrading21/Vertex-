# SKYLER — LOT 585

## Ce que le lot établit

**Un repli `|| 0` détruit les gardes situées en AVAL.** Mesuré deux fois, de
deux façons indépendantes :

- **par exécution** — `VX.fmt.num(null)` rend **« — »**, mais
  `VX.fmt.num(null || 0)` rend **« 0,00 »** ;
- **par lecture** — `VXCharts.waterfall` filtre déjà
  `it.value != null && !isNaN(it.value)` ; le `|| 0` écrit en amont fait passer
  la valeur absente à travers ce filtre, sous la forme d'une barre de hauteur
  nulle.

Le dépôt **a** des branches honnêtes. Le repli les rend inatteignables. C'est
exactement le mécanisme du dossier du 582 — et ce lot montre qu'il n'est pas
propre à `VX.freshness.assess`.

**Mon attente principale est réfutée** : je m'attendais à ce que la plupart des
52 replis « mesure » soient affichés directement comme des nombres. **Aucun ne
l'est.**

## Le choix (eee)

Le 584 a établi que l'origine ne tranche rien (584-A). Le 583 avait compté
**52 replis « mesure »**, dont aucun n'avait été lu au bout aval. Ce lot lit ce
bout.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

Écrits dans `l585_piege.md` **avant** toute mesure.

| piège | verdict |
| --- | --- |
| **Attente principale** — la classe « le consommateur affiche `0` comme une valeur du domaine » domine | **RÉFUTÉE** : **0 des 52** affiche `0` comme un nombre dans la même expression |
| **Contre-piège 1** — `VX.fmt.num` pourrait porter la même garde que `ago` | **RÉFUTÉ par exécution** : `num` garde `null`/`undefined`/non-fini, **pas `0`**. Et la prémisse « le dépôt n'a qu'une fonction de formatage » était fausse : il y en a **quatre** (`nd`, `num`, `pct`, `price`) |
| **Contre-piège 2** — le gabarit HTML sera le cas le plus fréquent | **RÉFUTÉ** : **1 seul** site atteint un gabarit, et ce n'est pas un affichage |

## Les 52, par issue mesurée

| issue | sites | part |
| --- | --- | --- |
| **échappe par une variable — INDÉCIS** | **39** | 75 % |
| aucune sortie dans la chaîne (comparaison, tri, itération) | **12** | 23 % |
| **atteint un gabarit HTML** | **1** | 2 % |

**Les premiers consommateurs, lus** : `Math.abs` ×16 · `.sort` ×8 ·
`Math.round` ×7 · `VXCharts.waterfall` ×4 · `rows.forEach` ×3 · `others.map` ×2 ·
`f.filter` · `pos.map` · `Math.min` · `h.forEach`. **Aucun formateur. Aucun
gabarit.**

### Le seul site « HTML », lu en entier

```javascript
const uid = 'ra' + Math.round((o.confidence || 0) + (o.regime || '').length * 7);
```

*(`vertex/static/vertex/js/charts/regime-aura.js`.)* Ce n'est pas un affichage :
c'est la fabrication d'un **identifiant DOM**. **Donc, en toute rigueur : aucun
des 52 replis « mesure » ne montre `0` comme un nombre dans son expression.**

### Les deux sites à chaîne vide, lus — les plus conséquents du lot

```javascript
if(b==='Actionnable'&&(r.score||0)>=80)return 'S+';      // /opportunities
if((snap.score||0)>=78||…)return'Offensive';             // /portfolio
```

Ce sont des **seuils de classement**. Un score absent y devient un **mauvais
score**, silencieusement : l'opportunité tombe de « S+ » à « S », la position
sort de « Offensive ». Le repli ne produit pas un « 0 » visible — il produit une
**catégorie** différente.

## Ce que les formateurs font de `0` — exécuté

`vx-core.js` chargé en bac à sable, fonctions appelées.
Calibration : `num(1234.5)` → `"1 234,50"`.

| entrée | `nd()` | `num()` | `pct()` | `price()` |
| --- | --- | --- | --- | --- |
| `null` | `"—"` | `"—"` | `"—"` | `"—"` |
| `undefined` | `"—"` | `"—"` | `"—"` | `"—"` |
| **`0`** | `0` | **`"0,00"`** | **`"0,00 %"`** | **`"0,00"`** |
| `''` | `"—"` | **`"0,00"`** | **`"0,00 %"`** | **`"0,00"`** |

Les quatre gardent `null`/`undefined`/non-fini — **mais pas `0`**, qui est fini
et passe. `ago`, lui, garde **tout ce qui est faux** (`if (!ts)`), `0` compris.
**C'est toute la différence, et elle est en une ligne de code.**

*Constat annexe, non corrigé* : sur la chaîne vide `''`, `nd` rend « — » et
`num` rend « 0,00 ». Les deux fonctions du même objet ne s'accordent pas.

## Second contrôle (481) — le `0` comme géométrie, pas comme texte

La restriction de l'instrument est « ce qui s'affiche **comme un nombre** ».
Le cas qu'elle exclut : un repli dont le consommateur est un **constructeur de
graphique**, où `0` devient une **forme**.

**24 des 52** passent par un constructeur ou une boucle de dessin :
`call_gex ×5 · put_gex ×5 · value ×3 · net_gex ×3 · score ×2 · strike ×2 ·
pct_a50 · pct_a200 · brNum · advpct`.

Les quatre sites `waterfall` de `/markets`, lus :

```javascript
items:[ {label:'>MM50',   value:0.30*(inter.pct_a50 ||0)},
        {label:'>MM200',  value:0.25*(inter.pct_a200||0)},
        {label:'Breadth', value:0.25*(inter.breadth!=null?inter.breadth:(brNum||0))},
        {label:'Adv/Déc', value:0.20*(inter.advpct ||0)},
        {label:'Santé',   value:inter.health, isTotal:true} ]
```

et le filtre que `waterfall` applique, lu dans `chart-core.js` :

```javascript
const items = (o.items || []).filter(it => it && it.value != null && !isNaN(it.value));
if (!items.length) { el.innerHTML = o.emptyHtml || ''; return null; }
```

**Le constructeur sait refuser une valeur absente. Le repli l'en empêche.** Une
composante manquante devient une contribution de `0` au total « Santé », visuellement
indistinguable d'une composante réellement nulle.

*(À noter, dans la même expression : la troisième ligne porte une garde
explicite `inter.breadth != null ? …` — puis un repli sur l'alternative. Les
deux écritures cohabitent à quatre lignes d'intervalle.)*

## Les arrêts du lot — deux calibrations échouées sur le même témoin

**Arrêt 1 (211 → 212).** Mon premier banc devait dire, pour le site du 582, que
le consommateur est `VX.freshness.assess`. Il a répondu **« CALCUL · opérateur
`*` »** — et il avait **raison** : le parent immédiat de `(man.age_s||0)` est la
multiplication `*1000`. C'est ma calibration qui nommait la mauvaise réponse.
**« Consommateur » était sous-défini.** J'ai écrit un **second banc** relevant
**deux faits distincts** — parent immédiat *et* premier appel englobant — sans
toucher au premier, qui reste la preuve de la faute.

**Arrêt 2 (212 → 213).** Le troisième banc devait montrer que la chaîne du
témoin **finit dans un gabarit**. Elle finit à `=> fr` :

```text
VX.freshness.assess -> VX.freshness.chip -> => fr
```

`fr` est une variable, interpolée **plus loin, dans une autre instruction**.
**Un parcours d'ancêtres ne traverse pas une affectation.** Ce n'est pas un
défaut de l'instrument, c'est sa **portée**. Elle est déclarée — et **comptée** :
**39 des 52** s'échappent ainsi, et sont classés **INDÉCIS**, jamais « sans
affichage ».

**Arrêtés avant publication : 211 → 213 (+2).**

## Ce que le lot n'établit pas

- **Que ces 52 replis mentent.** 39 sont **indécis** — la valeur sort par une
  variable que l'instrument ne suit pas. Dire « ils ne s'affichent pas » serait
  une déduction non mesurée.
- **Qu'un seul soit un défaut.** Aucun n'a été lu jusqu'au serveur (583-C) : le
  dossier du 582 reste **le seul** lu aux deux bouts.
- Que les deux seuils (`>=80`, `>=78`) produisent un mauvais classement en
  pratique : il faudrait savoir si `score` peut être absent côté serveur — **non
  mesuré ici**.

## Limites déclarées

- L'instrument **ne traverse pas une affectation** : 39 sites sur 52 finissent
  dans une variable. Portée déclarée et comptée.
- Le bac à sable de `l585_fmt.js` est un **remplacement**, pas un navigateur ;
  les quatre fonctions appelées ne touchent ni au DOM ni au réseau.
- Le classement « mesure » vient de la **lecture** du 583, recopiée telle
  quelle — c'est une lecture, pas une règle exécutable.
- Les 52 se retrouvent **exactement** (52 = 52), ce qui est un contrôle de
  cohérence entre deux lots, pas une preuve d'exhaustivité.

## Règles neuves

- **585-A — « CONSOMMATEUR » N'EST PAS UN FAIT UNIQUE.** Le parent immédiat et
  le premier appel englobant sont **deux mesures différentes**. Les publier
  séparément (546-A appliqué à la structure).
- **585-B — UN REPLI `|| 0` DÉTRUIT LES GARDES SITUÉES EN AVAL.** Avant de juger
  un repli, lire ce que son consommateur aurait fait de la valeur **absente**.
- **585-C — UNE CALIBRATION QUI ÉCHOUE DEUX FOIS SUR LE MÊME TÉMOIN MESURE LA
  PORTÉE DE L'INSTRUMENT, PAS SON EXACTITUDE.** Deux fois de suite ici,
  l'instrument avait raison et l'attente avait tort.

## Ce que le dépôt fait bien

- **Les quatre formateurs gardent `null` et `undefined`** — la branche honnête
  existe et est écrite.
- **`VXCharts.waterfall` refuse les valeurs absentes** et sait afficher un état
  vide (`o.emptyHtml`) : le constructeur est plus prudent que ses appelants.
- **Aucun des 52 ne va directement dans du HTML** : la couche d'affichage est
  systématiquement traversée par une fonction, jamais court-circuitée.
- La garde explicite `inter.breadth != null ? …` montre que **l'écriture prudente
  est connue du dépôt** — elle cohabite avec le repli, à quatre lignes d'écart.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **213 (+2)**
- Publiés puis corrigés : **38**
- Interprétations retirées : **11**
