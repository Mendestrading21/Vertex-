# SKYLER LOT 486 — Le test du 485 appliqué à TOUS les barèmes : le score /40 est affiché sur DEUX pages, pas une — et la trouvaille vient du cas que mon recensement EXCLUAIT : la barre de poids de `/portfolio` est TOUJOURS VERTE

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-486` (base : lot 485 fusionné,
`9800e372`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 485 avait posé la règle : *un test appliqué à un objet de l'enquête doit
l'être à tous les objets de même genre*. Le test — **un barème affiché « x/max »
atteint-il son max ?** — n'avait servi qu'à **deux** objets. Ce lot le porte à
toute la population.

## L'instrument, et sa calibration

Population construite **depuis l'écran** (règle 456) : les **42 objets servis**,
**841 916 caractères** — 8 pages + `/analysis/AAPL` + 33 JS statiques non-vendor.
Six motifs de barème (`/100`, `/40`, `/10`, `/5`, `/max`, `score_max`, jauges
`v/max*100`, `Math.min(100, …)`).

**Calibration écrite dans le code, sur les DEUX réponses déjà connues** — le
barème LEAPS (sain, 484) et le score /40 (bridé à 29, 485) — avec sortie
programmée si l'un des deux manque : **les deux trouvés, instrument calibré**.

```text
66 relevés bruts sur 15 des 42 objets
   /opportunities 13 · /analysis/AAPL 12 · /portfolio 11 · options-structure.js 6
   /markets 5 · options-intel.js 4 · chart-core.js 3 · vx-entities.js 3 · …
```

## Ce que la LECTURE de la liste donne — un second site, pas un second défaut

**`/opportunities` sert une carte « Classement Skyler — score canonique /40 ».**
Tracé : `/api/skyler/sweep` (`analysis_api.py:209`) → `skyler_sweep.py:50`
`_sk.decide(...)` — **le moteur exact dont le 485 a mesuré le plafond à 29**.

Conséquences **nouvelles et mesurables**, sur une page dont ni le 484 ni le 485
n'avaient parlé :

```text
barre de verre   width = Math.max(4, Math.min(100, n/40*100))
                 n ≤ 29  →  la barre ne peut JAMAIS dépasser 72,5 % de son rail
seuil vert       n >= 28 positive · 16-27 warning · < 16 negative
                 →  la bande verte est une fenêtre de DEUX points (28-29) sur 40
colonne Niveau   ne peut afficher ni S ni S+ (0 sur 3 072, mesuré au 485)
```

**Ce n'est PAS un défaut neuf** — c'est le dossier 484/485, **retrouvé sur un
second écran**. Je compte donc **un SITE de plus, pas un dossier de plus**
(leçon 483 : la parenté de famille n'est pas une parenté de site, mais ici la
parenté est de **cause** — le même `score40`). **Le dossier passe de 1 à 2 pages
servies**, ce qui change son chiffrage, pas son rang.

## Le second contrôle — et c'est LUI qui trouve

Mon recensement exige **un maximum déclaré dans les octets servis**. Il exclut
donc **les jauges dont le dénominateur n'est pas écrit**. Contrôle sur un cas
exclu : `wgtBar`, la barre de poids de `/portfolio` (`:502-510`).

```javascript
const wgtBar=(w,cap)=>{ …
  const over = cap!=null && w>cap,  near = cap!=null && !over && w>=cap*0.8;
  const tok  = over?negative : near?warning : positive;
  const width= cap!=null ? Math.min(100, w/cap*60) : Math.min(100, w);
  …(cap!=null ? tick de plafond à 60 % : rien)…
  …(cap!=null ? ' / '+cap+' %' : rien)… };

appelée UNE seule fois — :524   wgtBar(wgt, tr ? tr.max : null)
                                 tr = tierOf(t)
```

Et `tierOf` (`:182-190`) lit **`t.entrySnap.score`**.

### `entrySnap.score` n'est écrit par personne

Mesuré **dans les octets servis** : `entrySnap` y apparaît **18 fois — 15
lectures et 3 écritures**, les trois dans `vx-entities.js` :

```text
entrySnap: {}                      création par défaut
entrySnap: { stop: n('f-stop') }   formulaire d'ajout — le STOP seul
entrySnap: snap                    snap = Object.assign({}, t.entrySnap||{})  (recopie)
```

**Aucune n'écrit `score`.** Le seul site du dépôt qui pourrait le faire est
`vx_kit.py:185` (`window.tSnapOf(s)`) — **fichier mort, qui n'atteint aucune des
8 pages** (mesuré au lot 381).

Donc `Number(undefined)` → `NaN` → `!isFinite` → **`tierOf` rend `null` pour
TOUTE position, toujours.** Et par conséquent, pour chaque ligne du portefeuille :

```text
tick du plafond à 60 %      jamais dessiné
suffixe « / cap % »         jamais écrit
over / near                 toujours faux
→ LA BARRE DE POIDS EST TOUJOURS VERTE, quel que soit le poids
classe vx-warn de la cellule (wgt > tr.max*1.5)  ne se déclenche jamais
```

**Les trois chemins sont bien dans les octets servis** — vérifié : la branche
`cap!=null?Math.max(4,Math.min(100,w/cap*60))`, le tick `left:60%` et le suffixe
`vx-meta"> / '+cap+' %` sont **tous PRÉSENTS**. Ils ne sont simplement **jamais
pris**. C'est la leçon 475 dans sa forme la plus nette : **exact, servi,
inatteignable.**

### Ce qui atténue, et que je dis

La page porte **ailleurs** une alerte de concentration réelle —
`dominantRisk` (`:221`) : `if(m.top1 && m.top1.w > 25)` → « Concentration
élevée : X = N % du portefeuille » — **présente dans les octets servis**. Le
risque de concentration **est** signalé au niveau du portefeuille ; c'est la
barre **par ligne** qui ne le signale pas.

### Classement — critères absolus (règle 480)

**486-A — la barre de poids ne peut jamais alerter : rang 2.**
(a) **servi** — vérifié dans les octets de `/portfolio` ; (b) c'est un **affichage
de RISQUE** qui ne peut pas exprimer le risque, sur une page de décision ;
(c) **une information co-visible existe** — l'alerte de concentration Top1 > 25 %.
C'est ce troisième point, et lui seul, qui l'empêche de monter au rang 1
(mécanique 456/484). Aucune comparaison à un autre dossier n'entre dans ce rang.

## Un défaut LATENT, que je nomme sans le classer

`tierOf` : `const n = sc<=40 ? sc : Math.round(sc/2.5); /* tolère un score /100 → /40 */`

```text
sc = 78  (/100, bon)   → 78 > 40 → n = 31 → tier S,  plafond 10 %
sc = 40  (/100, faible)→ 40 ≤ 40 → n = 40 → tier S+, plafond 15 %
```

**Un score /100 inférieur ou égal à 40 est lu comme un score /40 : plus il est
mauvais, meilleur est le palier.** Et la même page lit **le même champ à l'autre
échelle** 74 lignes plus haut — `roleOf` (`:111`) : `(snap.score||0) >= 78`, un
seuil qui n'a de sens que sur /100.

**Deux lectures d'un même champ, dans un même fichier.** Mais comme **rien
n'écrit jamais `score`**, ce défaut est **latent, pas actif** : je le nomme, je
ne lui donne **aucun rang**, et je ne le compte pas dans la feuille. Il
deviendrait actif le jour où un site remplirait le champ.

## Mutualisation — cherchée, et cette fois RÉELLE

**486-A et le défaut latent ont UNE seule cause** : `entrySnap.score` n'est
jamais écrit. Même champ, même fichier, **un seul correctif** les traite tous
les deux — soit en écrivant le champ, soit en retirant les lectures. C'est la
première fois depuis le 478 que la mutualisation est autre chose qu'une famille.

Et c'est la **famille** du dossier 406/407 (`myCapital`, `myTradesEquity` : des
clés du desk lues et écrites par personne) — **famille, pas site** : champ
différent, fichier différent. Je ne les fusionne pas.

## Les barèmes NOMMÉS mais NON TRACÉS (règle 448)

Ni comptés, ni conclus : `confiance conf/100` et `accord agreement/100`
(`/analysis`), `best.score /100` · `edge /100` · `r.score /100` (`/opportunities`,
échelle `opGrade`, **homonyme du niveau Skyler** — piège signalé au 484),
`count + ' / 10 max'` (Positions déclarées) et `stocks.length + ' / 10'` /
`opts.length + ' / 3'` (déjà de la famille du 471), `rating_mean/5`
(observation du 484).

## Deux faux résultats arrêtés avant publication

1. **Mon recensement allait conclure « rien de neuf hors des sites connus ».** Il
   n'aurait rien trouvé, parce que sa restriction — *un maximum déclaré* —
   **exclut précisément les jauges muettes**, et c'est là qu'était le défaut.
   La règle du 481 a payé pour la cinquième fois consécutive.
2. **Ma sonde sur les octets servis a rendu « ABSENT » pour le suffixe du
   plafond** — parce que j'avais recopié la chaîne avec les mauvaises
   apostrophes. Revérifiée avec la bonne sous-chaîne : **PRÉSENT**. J'allais
   écrire que le code n'était pas servi alors qu'il l'est, et affaiblir mon
   propre constat. *Matcher un motif approximatif n'est pas matcher la chose*
   (leçon 466), cette fois **contre moi**.

**Arrêtés avant publication : 49 → 51.**

## Portée

- **Aucune exécution de moteur ce lot** : `tierOf`, `roleOf` et `wgtBar` sont du
  **JS client**, non exécutable depuis un banc Python. L'inatteignabilité est
  établie par **recensement des écritures dans les octets servis** — 3 écritures,
  aucune ne portant `score` — pas par exécution navigateur. **C'est la dette de
  ce lot, et je la nomme** : un rendu navigateur la solderait.
- Le recensement porte sur **six motifs littéraux**. Une jauge construite par un
  helper, ou un maximum passé par déstructuration, **échapperait** — non
  quantifié.
- **7 barèmes nommés et non tracés** : ils ne sont comptés dans aucun total.
- Le verdict « `vx_kit.py` est mort » est **repris du lot 381**, non remesuré.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié**. Pages en **GET**. **`/api/skyler/`,
  `/api/analyst/`, `/api/correlations/`, `/options/` et `/desc/` NON appelées.**
  Aucun écrivain appelé.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Trois lots de suite ont porté le même geste : **prendre au sérieux ce qu'un lot
précédent avait écarté d'une phrase**. Le 484 a tracé trois « barèmes » que le
456 avait écartés ; le 485 a payé la dette que le 484 avait nommée ; le 486
applique à toute la population le test que le 485 avait posé.

Et à chaque fois, **le résultat est venu du bord de l'instrument, pas de son
centre** : le 484 dans une catégorie écartée, le 485 dans un bloc qui marquait
« quelque chose », le 486 dans une jauge sans dénominateur. **Le défaut se loge
là où la définition de la population s'arrête.**

Comptes séparés : résultats faux **arrêtés avant publication 51 (+2)** ; publiés
puis corrigés **9** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
