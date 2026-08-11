# SKYLER — LOT 613 · UN PALIER DE TEXTE QUI NE POUVAIT ÊTRE LISIBLE NULLE PART

Le brief visait **les bandeaux d'état**. Ils sont **tous conformes**. Le défaut
était à côté — et il fallait mesurer les bandeaux pour le trouver.

## Ce que le brief demandait, et la réserve qu'il posait

> « Les bandeaux d'état portent `data-tone` / `vx-error-banner` sur fond de verre ;
> le rapport de contraste texte/fond n'a JAMAIS été mesuré. **ATTENTION —
> vérifier d'abord que le fond est OPAQUE** : un ratio calculé sur une couleur
> transparente serait un chiffre inventé. »

**La réserve était fondée** : `--vx-negative-soft` vaut `rgba(233,85,95,.17)`, et
le produit porte **11 règles `backdrop-filter`**. Un ratio calculé sur cette seule
valeur n'aurait mesuré rien.

## Les bandeaux : conformes, et c'est le premier résultat

**45 feuilles de texte**, 5 écrans **en état d'échec réel** (routes interceptées
en 500), deux méthodes indépendantes, **0 injoignable** :

| famille | px | pire ratio | seuil |
| --- | --- | --- | --- |
| `.vx-error-banner` (texte) | 12 | **4,79** | 4,5 |
| `.vx-state` (span) | 13 | 5,34 | 4,5 |
| `.vx-stale-banner` | 12 | 8,20 | 4,5 |
| boutons `.vx-btn-ghost` des bandeaux | 12 | 8,75 | 4,5 |
| `.vx-fresh-chip` | 10,5 | 9,79 | 4,5 |
| `.vx-demo-banner` / `.vx-badge-demo` | 12 / 10 | 15,81 | 4,5 |
| **témoin (481) — texte courant hors bandeau** | 12–32 | **5,22** | 4,5 / 3,0 |

**Marge la plus étroite : 4,79 contre 4,5 — 6 %.** Conforme, sans confort.

## Le mécanisme que le brief a mal nommé

Le brief soupçonnait **le verre**. Mesuré : sur les 45 feuilles, l'écart maximal
entre composition CSS et pixels peints est **0,21** — le flou n'a jamais été
décisif.

Ce qui casse réellement le calcul CSS est **le dégradé** :

```
/portfolio  button.vx-btn « + Position »   A = 18,54   B = 6,86   écart 11,68
```

`.vx-btn-primary{background:var(--vx-brand-gradient)}` est un `linear-gradient`,
et `getComputedStyle().backgroundColor` rend `rgba(0,0,0,0)` pour un fond en
dégradé : la méthode CSS ne le voit **pas du tout**. La réserve du brief visait
la transparence ; le vrai angle mort était l'**image** de fond.

## Ce que le balayage complet a trouvé — et c'est le lot

Les bandeaux étant propres, l'instrument a été élargi : **8 pages servies × 2
largeurs (1440 et 390), 2 700 feuilles de texte, 212 combinaisons distinctes**,
pseudo-éléments `::before`/`::after` compris — ils ne sont pas des nœuds du DOM
et aucun banc précédent ne pouvait les voir.

**`--vx-text-faint` valait `#655d5f` : 3,23:1 sur la surface la PLUS favorable du
produit.** Ce palier ne pouvait atteindre 4,5:1 **sur aucune surface déclarée** —
il était non conforme **par construction**, pas par contexte. Or il porte du
texte réel :

| ce qu'il écrit | px | avant | après |
| --- | --- | --- | --- |
| `.vx-help` — aide des formulaires, 4 pages | 11 | **3,10** | conforme |
| `.vx-mono` / `b` — noms de fichiers sur `/system` | 11 | **3,10** | conforme |
| `.vx-state-icon` — pictogramme d'état vide | 16 | **3,21** | **4,93** |
| `.vx-op-mom .b span` — étiquettes de momentum | 8 | **3,15** | 4,47 – 4,85 ⚠ |
| `.vx-table-cards td::before` — **l'étiquette qui nomme chaque valeur quand la table passe en cartes sous 768 px** | 9,5 | — | — |

La dernière ligne est la plus lourde : sous 768 px, c'est **le seul texte qui dit
de quelle colonne vient un chiffre**. Elle n'apparaît dans aucune mesure parce
qu'aucune table ne passait en mode cartes sur les écrans balayés — **recensée,
non mesurée**, et dite comme telle.

## Le correctif, et la contrainte qui l'a borné

`--vx-text-faint` : **`#655d5f` → `#847a7c`** (un seul point de définition, un
seul repli). Conforme sur les quatre surfaces où ce texte est **servi** :

| surface | ratio |
| --- | --- |
| `canvas` `#020305` | **4,97** |
| `shell` `#070709` | **4,85** |
| `surface` `#0c0c0e` | **4,71** |
| `surface-elevated` `#121214` | **4,50** |
| `surface-selected` `#1d1c1f` | 4,08 ✗ |
| `warm-depth` `#242327` | 3,76 ✗ |

**Pourquoi pas conforme partout ?** Viser `warm-depth` imposait `#92878a`, dont
la luminance **0,2527 dépasse celle de `--vx-text-muted` (0,2303)** : le palier
« le plus discret » serait devenu **le plus lumineux**. **Les deux paliers sont
couplés** — on ne peut pas rendre `faint` conforme partout sans déplacer `muted`
d'abord. C'est la découverte structurante du lot, et elle a borné le correctif.

**Défaut annexe corrigé** : `polish.css` portait `var(--vx-text-faint,#5f5a55)`,
un repli **plus sombre encore** que le token qu'il double — un second réglage,
jamais relu.

## Ce que le lot REFUSE de corriger, avec le chiffre pour décider

**`--vx-text-muted` `#8A8284` tombe à 4,04:1** sous `.vx-meta`, `.vx-kpi-label`,
`.vx-card-footer`, `.vx-muted` — **sous le seuil, sur 11 combinaisons page ×
largeur**, confirmé par les deux méthodes.

Le lot ne le déplace pas. Trois raisons, dans cet ordre :

1. **60 littéraux de repli** `var(--vx-text-muted,#8A8284)` dans `vertex/ui/**` —
   contre **1** pour `faint`. Le corriger est une campagne, pas un correctif.
2. Le déficit est **contextuel** (4,04 sur les fonds les plus clairs, 5,44 sur
   les plus sombres) : la correction pourrait viser **la surface** autant que
   le texte.
3. Il change le poids typographique de **tout le produit**. C'est une décision de
   design — **612-B**.

Valeur minimale calculée si l'humain décide de le faire : **`#938a8c`**
(× 1,062), qui donne 4,51 sur le pire fond mesuré. **Le chiffre est posé ; la
décision revient à l'humain.**

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « `--vx-negative-soft` est semi-transparent, un ratio sur cette seule valeur serait inventé » | **CONFIRMÉ** — `rgba(233,85,95,.17)` |
| **(b)** | « la composition des fonds ancêtres suffit » | **CONFIRMÉ pour le verre** (écart ≤ 0,21), **RÉFUTÉ pour les dégradés** (écart 11,68) |
| **(c)** | « au moins un bandeau est sous 4,5:1 » | **RÉFUTÉ** — 45 feuilles, la pire à 4,79 |
| **(d)** | « le témoin hors bandeau est au-dessus du seuil » | **CONFIRMÉ** — 30 feuilles, la pire à 5,22 |
| **global** | | **le dossier visé était sain ; le défaut était à côté, et seule la mesure du dossier sain l'a fait apparaître** |

## Ce que j'ai dû réviser sur mon propre instrument

J'avais posé la règle : **« si A et B divergent, c'est B (les pixels) qui fait
foi »**. Après correctif, deux éléments restaient signalés par B seule. **Je ne
pouvais pas annuler ma règle par confort** — j'ai sondé où B échantillonne :

| élément | boîte | dominante lue | verdict |
| --- | --- | --- | --- |
| `.vx-state-icon` | 42 × 42, **fond transparent**, coins arrondis | rangée haute **(66,66,67) à 45 %**, rangée basse **(17,17,18) à 50 %** — **les deux rangées se contredisent** | **B non fondée** ; A (4,93) fait foi |
| `.vx-op-mom .b span` | **8 × 12** → **3 pixels lus par rangée** | (10,10,12) à 67 % | **sous la résolution de l'instrument** ; 4,47–4,85, **indéterminé** |
| `.vx-op-grade[data-g="S"]` | encre `#0b0e14` sur `var(--vx-brand-gradient)` | A = 1,04 **et** B = 1,01 | **les deux méthodes fausses**, pour deux raisons différentes ; seule la lecture du CSS a tranché — le design est correct |

**La règle corrigée : B ne fait foi que là où la bande lue est *vérifiablement*
du fond.** Un critère objectif s'en dégage — **la part de la dominante** : ~100 %
sur un fond réel, 45–50 % quand l'échantillon sort de la forme.

Et pour l'étiquette de momentum, la conclusion honnête est **« indéterminé »** :
8 px de large ne donnent pas assez de pixels pour trancher un seuil à 0,03 près.
Le produit interdit d'afficher un chiffre absent ; il interdit aussi d'en
publier un que l'instrument ne peut pas porter.

## Ce que le lot n'établit pas

- **Que les 26 combinaisons signalées soient 26 défauts.** Après tri, **5**
  étaient réelles (les familles `#655d5f`), **8** relèvent de `--vx-text-muted`
  (mesurées, non corrigées, remises à l'humain), **le reste sont des artefacts**
  d'instrument (texte SVG, puces arrondies, dégradés). **208 feuilles sur 2 700
  restent injoignables en pixels** — bornées par la géométrie, pas par le thème.
- **L'étiquette `td::before` du mode cartes** : recensée dans le CSS, **jamais
  rendue** dans le balayage. Elle bénéficie du correctif par construction, mais
  ce n'est pas mesuré.
- **Les états de survol et de focus** — non mesurés ; ils remontent le contraste,
  donc le pire cas reste l'état au repos.
- **Que la lisibilité se réduise au contraste.** Taille, graisse, interlignage et
  ordre de lecture ne sont toujours pas jugés.

## Règles neuves

- **613-A — UN INSTRUMENT PLUS PROCHE DU RÉEL N'EST PAS UN INSTRUMENT PLUS
  FIABLE.** Lire les pixels peints bat le calcul CSS sur les dégradés, et perd
  sur les petites formes arrondies et le texte SVG. **La question n'est pas
  « quelle méthode est la meilleure » mais « où chaque méthode a-t-elle du
  signal ».** Une règle de préséance posée d'avance doit pouvoir être *bornée*
  par la mesure — pas annulée quand elle dérange.
- **613-B — MESURER UN DOSSIER SAIN N'EST PAS UN LOT PERDU.** Les bandeaux
  étaient conformes ; c'est l'instrument construit pour eux, élargi, qui a
  trouvé le palier non conforme par construction. **Le premier balayage ne
  couvrait que 45 feuilles sur 2 700.**
- **613-C — UN TOKEN QUI NE PEUT ATTEINDRE SON SEUIL SUR AUCUNE SURFACE DU
  PRODUIT N'EST PAS UN CHOIX DE STYLE, C'EST UN DÉFAUT.** La distinction avec
  612 (où l'exemption à 32 px était une décision assumée) tient à l'existence
  d'un **seuil objectif publié**. Là où il n'y en a pas, le loop décrit ; là où
  il y en a un et que le code est dessous **partout**, il corrige.
- **613-D — UN COMMENTAIRE PEUT CASSER UN PARSEUR.** Le commentaire posé dans
  `tokens.css` contenait `--vx-warm-depth : les…` ; `design_system_page.
  _load_tokens` lit `(--vx-...)\s*:\s*([^;]+);` et a **avalé la déclaration
  suivante comme valeur**. Le gardien du lot 187 l'a arrêté. **Une prose de
  documentation vit dans le même fichier que la donnée qu'elle documente.**

## Ce que le dépôt fait bien

- **Les bandeaux d'état sont conformes**, y compris leurs boutons (8,75 minimum)
  et leurs puces (9,79) — sur un thème quasi noir, ce n'est pas gratuit.
- **`--vx-text-faint` n'avait qu'un seul point de définition** : le correctif
  global tient en deux lignes. La discipline « une couleur = un token » a payé.
- **Le gardien d'empreinte du lot 361 a réclamé le bump deux fois** — une fois
  par changement d'octet servi, exactement ce pour quoi il a été écrit.
- **Le gardien du lot 187 a attrapé un commentaire**, pas un code. C'est le seul
  test du dépôt qui pouvait voir cette faute.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **3 fichiers de production** : `vertex/static/vertex/css/tokens.css`
  (`--vx-text-faint` + commentaire), `vertex/static/vertex/css/polish.css`
  (repli aligné), `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (5 tests, **5 mutations rouges chacune sur sa propre
  cause**) + **5 épingles** `td-shell-v195` → **`td-shell-v196`** + empreinte des
  assets et `_SW_VERSION` du gardien 361 (**ré-enregistrées deux fois**).
- MD5 des 8 pages : **8 / 8 identiques** — seuls des octets CSS ont changé.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2910 passed / 0 skipped** *(2905 + les 5 du gardien neuf)*.
- Navigateur : **26 chargements** — 5 écrans en échec (3 bancs successifs) puis
  **8 pages × 2 largeurs, avant ET après correctif**. **2 700 feuilles de texte
  examinées**, 212 combinaisons distinctes.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **248** *(+3 : « 7/9 bandeaux mesurés » alors que
  la capture était bornée au viewport ; « B fait foi » appliqué à un
  échantillon hors forme ; « 26 combinaisons sous le seuil » avant tri des
  artefacts)*
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 10** *(un palier de texte non conforme par
  construction, et son repli divergent)*
