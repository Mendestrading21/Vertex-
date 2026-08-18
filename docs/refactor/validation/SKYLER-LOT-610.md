# SKYLER — LOT 610 · UN BANDEAU LARGE DE 22 PIXELS, DEPUIS SEPT LOTS

Le brief envoyait chercher un défaut **mobile**. La mesure en a trouvé un — mais
**il n'est pas mobile**, et il était à moi.

## Ce qui a été mesuré

Depuis le 602, huit lots ont ajouté des bandeaux d'état jamais vus ailleurs qu'en
1440×900. Ce lot les mesure **chacun contre son parent**, à **390 px** et à
**1440 px**.

**16 zones d'état** exercées en échec, sur six écrans. Une seule est fautive —
et elle l'est **aux deux largeurs** :

| | avant | après |
| --- | --- | --- |
| `/markets?view=macro`, `summary` en échec | bandeau **large de 22 px**, contenu **coupé de 102 px** | **366 px**, rien de coupé |

Les quinze autres tiennent : 332 à 366 px, aucun débordement, **page jamais
débordée** (0 px à 390 comme à 1440).

## Le défaut, et pourquoi ma preuve du 603 ne l'a pas vu

`#vx-mk-macro-regime` est une **grille** (`vx-grid`, 12 colonnes). Le rendu
nominal y pose ses enfants avec leurs classes de colonne (`vx-col-5`,
`vx-col-7`). **L'état d'échec que j'ai ajouté au lot 603 n'en avait aucune** : le
bandeau tombait dans une **colonne implicite** et s'écrasait à 22 pixels.

**Ma preuve du 603 vérifiait la PRÉSENCE du texte attendu.** Elle disait vrai :
« Appétit pour le risque indisponible » était bien là. Elle ne pouvait pas voir
qu'il était **illisible**. Sept lots ont passé au-dessus.

## Le correctif : la famille, pas le cas

Un `vx-col-12` posé sur le site fautif aurait réparé ce bandeau-là. La règle
couvre **les trois classes d'état**, présentes et futures (**606-C**) :

```css
.vx-grid > .vx-state,
.vx-grid > .vx-error-banner,
.vx-grid > .vx-stale-banner{grid-column:1 / -1}
```

## Le piège, écrit avant de mesurer — trois volets sur quatre réfutés

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « à 390 px, au moins un bandeau déborde » | **CONFIRMÉ**, un seul sur seize |
| **(b)** | « le débordement vient des boutons » | **RÉFUTÉ** — il vient de la **grille** ; les boutons n'y sont pour rien |
| **(c)** | « seuls mes ajouts récents peuvent déborder, le reste tient en mobile » | **RÉFUTÉ dans sa prémisse** — c'est bien mon ajout, mais **le défaut n'est pas mobile** : identique à 1440 px |
| **(d)** | « un bandeau qui déborde ferait déborder la page » | **RÉFUTÉ** — `document.scrollWidth` vaut **0 px de débordement** partout. La page allait bien ; le bandeau était écrasé **à l'intérieur de sa propre boîte** |

**(d) est le volet qui comptait**, et je l'avais nommé comme danger : *mesurer
`scrollWidth` seulement est un contrôle trop grossier*. S'il avait été mon seul
instrument, ce lot aurait conclu « tout va bien » — et le bandeau serait encore
large de 22 pixels.

## Le témoin, d'abord partiel — donc muet

Premier jet : le témoin 1440 px ne couvrait que **trois** des six cas, et
`/markets` n'en faisait pas partie. J'ai donc lu « fautif à 390, sain à 1440 » et
j'ai failli publier **« défaut mobile »**.

Témoin étendu aux six : `/markets` est fautif **à 1440 aussi**. Le diagnostic
change entièrement — ce n'est pas un défaut de responsive, c'est un défaut de
mise en page, à toutes les tailles.

**Un témoin partiel ne témoigne pas.** C'est **606-B** pris par son autre bout :
la passe qui ne doit pas bouger doit couvrir **tout** ce que la passe active
couvre.

**Arrêtés avant publication : 242 → 243 (+1).**

## Le second arrêt — mon gardien a cassé un test étranger

Mon test « la règle est-elle dans l'octet **servi** ? » détournait
`persist._BASE_DIR` vers un dossier temporaire — un **état global partagé par
toute la session pytest**. Il ne le rendait pas.

Résultat : `test_persist.py::test_cache_path_points_to_repo_root`, qui n'a rien à
voir avec ce lot, **tombait**. La suite affichait **2 échecs** dont un totalement
étranger au sujet.

Restauration en `finally`. **Arrêtés : 243 → 244 (+1).**

## Le gardien, rouge dans les deux sens

`tests/test_etats_dans_grille_lot610.py` — **4 tests** :

- **règle retirée** → 3 rouges ;
- **règle réduite à une seule classe** (sous-application) → 2 rouges.

Il vérifie la règle **dans la feuille SERVIE**, pas seulement sur disque : un
fichier CSS peut exister sans être servi. Plus un garde-fou de volume (591-C) :
si `#vx-mk-macro-regime` cessait d'être une grille, ou si l'état d'échec du 603
disparaissait, le fichier passerait en ne vérifiant plus rien de réel — le test
le refuse.

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure **les bandeaux en état d'échec**, provoqués par injection. Le
cas exclu : **le rendu NOMINAL à 390 px** — si la page débordait déjà sans
panne, accuser mes bandeaux serait faux.

Mesuré : **0 px de débordement de page** sur les six écrans, en échec comme au
repos. Le produit tient à 390 px ; le seul défaut est celui-ci, et il est **de
mise en page, pas de largeur**.

## Ce que le lot n'établit pas

- **Que les autres largeurs soient saines.** Deux points mesurés — 390 et 1440.
  Entre les deux, rien.
- Que les bandeaux soient **lisibles**, seulement qu'ils ne sont pas coupés. La
  taille de police, le contraste et l'ordre de lecture n'ont pas été jugés.
- Que d'autres hôtes-grilles n'attendent pas le même piège : mon inventaire
  statique n'a trouvé que deux autres hôtes déclarés `vx-grid` et remplis par un
  état, **tous deux corrects** — mais il ne détecte que la forme
  `$('id').innerHTML=`, et le cas fautif passait par une variable locale. **Il
  aurait raté le défaut de ce lot.** C'est pourquoi le correctif est une règle
  CSS de famille et non une liste de sites.
- Que les états **hors grille** soient corrects : ils sont sortis du périmètre.

## Règles neuves

- **610-A — UNE PREUVE DE PRÉSENCE N'EST PAS UNE PREUVE DE LISIBILITÉ.** Le
  lot 603 a vérifié que le texte attendu était là. Il y était — dans un bandeau
  de 22 pixels. Vérifier qu'une zone **dit** son état ne dit rien sur le fait
  qu'on puisse **la lire**.
- **610-B — UN TÉMOIN PARTIEL NE TÉMOIGNE PAS.** Le témoin 1440 px couvrait la
  moitié des cas ; il a failli faire publier « défaut mobile » sur un défaut de
  toutes largeurs. La passe qui ne doit pas bouger doit couvrir **tout** ce que
  la passe active couvre.
- **610-C — UN TEST QUI DÉTOURNE UN ÉTAT GLOBAL DOIT LE RENDRE.** Mon gardien a
  fait tomber un test étranger. Une suite qui échoue ailleurs que là où on
  travaille coûte plus cher que le test ne rapporte.

## Ce que le dépôt fait bien

- **Quinze bandeaux sur seize tiennent à 390 px**, sans que personne ne les y ait
  jamais mesurés : le système de cartes fait son travail par construction.
- **La page ne déborde jamais**, à aucune largeur, en échec comme au repos. Les
  lots mobiles antérieurs (289 à 295) tiennent.
- **Le rendu nominal de `/markets` portait bien ses colonnes** — l'auteur d'
  origine avait raison ; c'est l'état d'échec ajouté après coup qui les a
  oubliées.
- **Le témoin 1440 px, une fois complet, a renversé le diagnostic** : l'outil de
  vérification a servi à corriger la conclusion, pas seulement à la valider.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/static/vertex/css/layout.css` (règle de
  famille), `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (4 tests, rouge dans les deux sens) + **5 épingles**
  `td-shell-v193` → **`td-shell-v194`** + empreinte des assets et `_SW_VERSION`
  du gardien 361.
- MD5 des 8 pages : **8 / 8 identiques** — le correctif est une **règle CSS**,
  aucun HTML de page ne change.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2898 passed / 0 skipped** *(2894 + les 4 du gardien neuf)*.
- Navigateur : **24 mesures** (6 écrans × 2 largeurs, avant et après), chacune
  comparant **chaque bandeau à son parent**.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **244 (+2)**
- Publiés puis corrigés : **41 (+1)** *(l'état d'échec du lot 603, publié
  illisible, corrigé ici)*
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 8**
