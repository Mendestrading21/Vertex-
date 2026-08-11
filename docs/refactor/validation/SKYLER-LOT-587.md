# SKYLER — LOT 587

## Ce que le lot établit

**Les seuils de produit sont majoritairement des DÉCISIONS, pas des bornes
techniques : 111 contre 81.** Mon attente disait l'inverse — je m'attendais à ce
que les bornes de rendu (`vx-core.js`, constructeurs de graphiques) dominent
largement. **Elles sont minoritaires.**

Et en le vérifiant, j'ai trouvé une **erreur dans le nombre publié par le 586** :
ses « 210 seuils nus » incluaient **23 sites d'une bibliothèque tierce**. Le
chiffre juste est **192**.

## Le choix (ggg)

Le 586 avait écrit noir sur blanc : « ils n'ont pas été lus, seulement comptés ».
C'était la plus grosse dette qu'un lot ait ouverte sur lui-même, et elle portait
sur la forme **dominante**.

## La correction du 586 — mesurée, pas devinée

Mon relevé rendait **192**, le 586 annonçait **210**. Un écart entre deux de mes
propres mesures est un arrêt : il faut savoir **laquelle est juste**, jamais
choisir la plus flatteuse. J'ai donc rejoué le banc du 586 **tel quel** (il est
conservé, c'est une preuve) et comparé les deux ensembles site par site.

| | sites |
| --- | --- |
| communs aux deux relevés | **187** |
| vus par le **586 seulement** | **23** |
| vus par le **587 seulement** | **5** |

- Les **23** sont **tous** dans `/static/vertex/js/vendor/lightweight-charts…` —
  une **bibliothèque tierce** (`t>255`, `i<650`, `this.Za.length>100`,
  `t<999999995`…). Le filtre du 586 excluait `chart.umd` **mais pas `/vendor/`**.
- Les **5** sont des `Math.abs(…) >= n` : mon relevé nomme désormais les appels
  de fonction, que celui du 586 laissait tomber faute de nom.

**Le chiffre juste est 192.** La conclusion du 586 — « le repli est l'exception »
— **n'est pas affectée** : 3 sur 195 au lieu de 3 sur 213, soit 1,5 % au lieu de
1,4 %.

**C'est ma propre règle 576-C** (isoler la part tierce **avant** tout total) que
le 586 a enfreinte — la troisième auto-violation en quatre lots, après 580-C au
584.

**Publiés puis corrigés : 38 → 39. Arrêtés : 213 → 214** — j'ai failli publier
« 192 » comme un simple résultat, en contredisant **silencieusement** un nombre
déjà publié.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

| piège | verdict |
| --- | --- |
| **Attente principale** — la famille BORNE TECHNIQUE domine largement | **RÉFUTÉE** : **DÉCISION 111 (58 %)** contre **BORNE 81 (42 %)** |
| **Contre-piège 1 (586-C)** — ne rien conclure de la fréquence avant d'avoir lu | **respecté** : histogramme complet des **89 noms** publié, classement par lecture, **couverture 192/192**, **0 non tranché** |
| **Contre-piège 2 (580-C)** — vérifier la déduplication, ne pas la supposer | **A PAYÉ** : c'est lui qui a trouvé les 23 sites tiers du 586 |

## Les 192, lus par famille

| famille | sites | part |
| --- | --- | --- |
| **DÉCISION** — choisit une catégorie, un verdict, un niveau, une couleur sémantique | **111** | **58 %** |
| **BORNE** — géométrie, cache, durée, unité, « assez de points pour dessiner ? », réessais | **81** | 42 % |
| non tranché | **0** | — |

**Les décisions, par page** : `options-structure.js` **36** · `/portfolio` 20 ·
`/markets` 17 · `/journal` 12 · `/opportunities` 9 · `vx-shell.js` 6 ·
`/analysis/AAPL` 5 · `chart-core.js` 4 · `catalyst-runway.js` 2.

**Le fichier des structures d'options porte à lui seul un tiers des décisions du
produit** — plus que `/portfolio` et `/markets` réunis.

### Le vocabulaire que ces seuils produisent — 25 libellés, lus

`Actionnable` · `Proche` · `À surveiller` · `Asymétrie excellente` ·
`Structure intéressante` · `Risque/temps médiocre` · `Excellente` ·
`Acceptable` · `Médiocre` · `excellente` · `acceptable` · `mediocre` ·
`Participation moyenne` · `Signal net — régime lisible` ·
`concentration modérée` · `très concentré` · `Concentration élevée :` ·
`Exposition options élevée :` · `Bêta pondéré élevé (` · `× la perte max` ·
`j) pour cette asymétrie` · `dans` · `muted` · `warn` · `risk`.

*(Noter, sans le corriger : `Excellente`/`excellente`, `Médiocre`/`mediocre` —
le même jugement écrit deux fois, avec et sans accent, avec et sans majuscule.)*

## Second contrôle (481) — le seuil dont la droite n'est pas un nombre

Le 586 excluait explicitement ces cas et déclarait son relevé « plancher ». De
combien ?

| forme | sites de produit |
| --- | --- |
| droite = littéral numérique (le relevé du 586) | **192** |
| **droite = variable ou expression** (`>= state.minScore`, `> n-1`, `> a.right`, `> sm.total*0.7`) | **108** |

**Le plancher était dépassé de 108 sites, soit 36 % de toutes les comparaisons
de seuil du produit.** Le 586 avait raison de le déclarer plancher ; il ne
pouvait pas savoir de combien.

## Ce que le lot n'établit pas

- **Que les 111 décisions soient justes.** Elles sont **nommées et comptées** ;
  aucun seuil n'a été confronté à ce que le moteur produit réellement.
- Que les 108 comparaisons à droite variable soient des décisions : **elles n'ont
  pas été lues**, seulement comptées. C'est la dette que ce lot ouvre à son tour.
- Que la classification soit la seule possible : `mins`/`day` (horloge de séance)
  et `a` (formatage k$/M$/Md$) sont les cas où j'ai hésité — le premier classé
  **décision** parce que « marché ouvert » est un énoncé produit, le second
  **borne** parce qu'il ne juge rien.

## Limites déclarées

- La classification est **par nom**, pas par site : les 89 noms ont été lus avec
  leur seuil, leur fichier et leur production, mais un nom réutilisé dans deux
  intentions différentes serait rangé une seule fois. Aucun cas de ce genre n'a
  été rencontré ; ce n'est pas une preuve qu'il n'y en a pas.
- L'extraction de « ce que produit la branche » est bornée à **4 littéraux, 4
  niveaux de profondeur** : une branche qui délègue à une fonction ne rend
  aucun libellé. **75 des 192** n'en produisent aucun (117 en produisent au
  moins un).
- Le corpus reste les 8 pages à leur URL de base + `/analysis/AAPL`.

## Règles neuves

- **587-A — UN NOMBRE QUI CONTREDIT SILENCIEUSEMENT UN NOMBRE DÉJÀ PUBLIÉ EST
  UNE FAUTE, MÊME S'IL EST JUSTE.** Rejouer l'ancien relevé, mesurer le
  recouvrement, publier la décomposition — jamais remplacer sans expliquer.
- **587-B — LES SEUILS DE PRODUIT SONT MAJORITAIREMENT DES DÉCISIONS.** 111
  contre 81 : le code de ce dépôt juge plus qu'il ne dessine.
- **587-C — UN FILTRE DE TIERS DOIT NOMMER TOUS LES CHEMINS TIERS.** `chart.umd`
  **et** `/vendor/` — un seul des deux laisse passer 23 sites.

## Ce que le dépôt fait bien

- **Les décisions sont concentrées et lisibles** : 111 seuils, 25 libellés, tous
  en français et tous compréhensibles hors contexte.
- **`bucketOf` reste le modèle** : trois seuils, trois catégories, aucune garde
  parasite, une production littérale par branche.
- **La bibliothèque tierce est physiquement isolée** dans `/vendor/` et
  `chart.umd.min.js` — c'est mon filtre qui était incomplet, pas le rangement du
  dépôt.
- **Les bornes techniques ne se déguisent pas en décisions** : les 81 relevées
  portent des noms qui disent ce qu'elles sont (`cache.size`, `attempt`,
  `bars.length`, `axes.length`).

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **214 (+1)**
- Publiés puis corrigés : **39 (+1 — les « 210 » du 586)**
- Interprétations retirées : **12**
