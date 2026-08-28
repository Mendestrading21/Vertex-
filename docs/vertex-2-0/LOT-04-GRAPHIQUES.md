# Lot 4 — Graphiques

Périmètre du lot : **thème, conteneur, rendu**. Aucune série, valeur, agrégation,
source ni période n'est touchée.

## Deux alias qui mentaient

Le thème conservait des clés historiques (`blue`, `cyan`, `teal`, `plum`, `sand`…)
pour ne pas casser leurs appelants. Deux d'entre elles ne rendaient pas ce que leur
nom annonçait — et l'écart n'était pas anodin.

### `blue` rendait `#84aa31` — le vert de marque abandonné

Une série demandée « bleue » sortait **verte**. C'est la couleur que la doctrine
réserve strictement au *positif réel*. Pire : `blue` était la **valeur par défaut de
`C.area()`**, donc la couleur de toute aire tracée sans couleur explicite.

### `cyan` rendait `#c0b79f` — un beige chaud

Et cet alias servait de couleur à la **courbe d'équité** (`equity-chart.js`) ainsi
qu'aux **niveaux de support** (`chart-core.js`).

Les deux retombent désormais sur l'argent. Le cyan analytique existe sous son propre
nom, **`crosshair` = `#65d8e8`**, et n'est atteignable que délibérément — ce qui est
exactement sa règle : crosshair et focus technique, rien d'autre.

## Deux appelants corrigés à la source

| Fichier | Avant | Après | Pourquoi |
|---|---|---|---|
| `equity-chart.js` | `C.colors.cyan` | `C.colors.brand` | Une courbe d'équité est la **série principale** : argent. Pas une teinte analytique. |
| `chart-core.js` | `support: C.colors.cyan` | `support: C.colors.brand` | Un support n'est ni positif ni analytique : c'est un **niveau**. La prudence reste réservée à la résistance. |

## Le thème réaligné

```
argent   série principale, structure, sélection      #c9ced8
gris     benchmark, séries neutres                   #8f96a2
vert     positif RÉEL uniquement                     #36c889
rouge    négatif, perte, risque                      #ed655c
ambre    prudence, incertitude, donnée dégradée      #dda23b
violet   OPTIONS exclusivement                       #9c79d0
cyan     crosshair et focus technique — rien d'autre #65d8e8
```

**Ordre des séries :** `argent · gris · gris pierre · violet · ambre · acier`.
Aucune série verte, rouge, bleue ni cyan : une couleur sémantique n'apparaît que
lorsqu'elle **porte** ce sens. Les séries neutres se distinguent d'abord par
luminance, épaisseur, tiret et marqueur — une teinte nouvelle est le dernier
recours, pas le premier.

`muted` passe de `#817d77` à `#9aa1ad`, au niveau AA, comme `--vx-smoke`.

Vérifié au **runtime**, pas dans le fichier :

```json
{"brand":"#c9ced8","blue":"#c9ced8","cyan":"#c9ced8","crosshair":"#65d8e8",
 "positive":"#36c889",
 "series":["#c9ced8","#8f96a2","#7f8794","#9c79d0","#dda23b","#9aa1ad"]}
séries conformes : True
```

Aucune des quatre teintes hors palette (`#84aa31`, `#53b9ad`, `#c0b79f`, `#8f698c`)
n'apparaît plus dans une série.

## Un nom de fichier laissé en place

`chart-theme-obsidian-copper.js` ne décrit plus rien : ni obsidienne cuivrée, ni
cuivre. Il est **conservé** parce que la coque et plusieurs bancs l'épinglent. Le
renommer appartient au lot de nettoyage, pas à un lot de contenu — et un renommage
n'apporterait aucune clarté à l'utilisateur.

## Outil ajouté

`tools/vertex_2_0_bump_sw.py` bumpe le service worker **et** les six gardiens qui
l'épinglent, plus l'empreinte `/static`, d'un seul geste. Le faire à la main en six
endroits, c'est en oublier un — ce qui est déjà arrivé une fois dans cette refonte.
L'outil purge aussi `tests/__pycache__`, dont un `.pyc` périmé fait mentir le
gardien d'empreinte.

Service worker `v222` → **`v223`**.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4246 passés**, 154 ignorés, 1 échec environnemental connu |
| Palette de séries au runtime | conforme, 0 teinte hors doctrine |

## Limites déclarées

- Les sources de marché étant injoignables dans cet environnement, **aucun
  graphique ne trace de série réelle** : le thème est vérifié sur ses valeurs
  effectives au runtime, et les conteneurs sur leurs états vides. Le rendu d'une
  série alimentée reste à vérifier sur une machine connectée.
- Le contrat complet de `ChartCard` (question · conclusion · source · unité ·
  période · résumé accessible · table équivalente) est **disponible** via
  `vx2.chart_card`, mais les graphiques existants n'y ont pas encore été migrés :
  ils gardent leur conteneur historique. La migration appartient aux lots de page.
