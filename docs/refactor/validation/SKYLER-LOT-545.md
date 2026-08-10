# SKYLER LOT 545 — La page que personne n'avait jamais mesurée : **`/analysis/<symbole>` porte 15 conteneurs à squelette, ZÉRO muet — et 4 zones de contenu qui se remplissent après une attente sans rien annoncer.** Le témoin exigé par le brief était faux

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-545` (base : lot 544 fusionné,
`ceced604`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(m)** — le 544 a découvert que la surface la plus riche du produit, la page
d'analyse d'un **titre**, n'a jamais été dans aucun corpus. Les 43 URL des lots
530 à 544 contiennent `/analysis` **nu**. Ce lot refait pour `/analysis/AAPL` ce
que les 535 et 536 ont fait pour les 43 URL.

## L'arrêt du lot — **le témoin imposé par le brief était faux**

Le brief exigeait : « `an-chart` doit ressortir comme **conteneur à squelette**
de `/analysis/AAPL` (constaté au 544) ». La calibration a échoué. Lecture des
octets servis, position **12 731** :

```html
<div id="an-chart"></div>
```

**Vide, sans squelette.** Le 544 n'a jamais dit cela : il a écrit que `an-chart`
est **présent hors script**. Le brief a transformé *présent* en *porteur de
squelette*. **Présent n'est pas porteur** — et c'est le brief, écrit par la
boucle elle-même, qui a introduit le glissement.

Témoin remplacé par un témoin **lu dans le code** avant d'écrire l'instrument
(541) : `an-anomaly`, dont `analysis_page.py` porte
`const host=$('an-anomaly');…host.innerHTML=…`.

## Le second arrêt — **14 n'était pas la réponse**

Le crible a d'abord rendu **14 identifiants servis vides, sans squelette, et
dans lesquels le JavaScript écrit**. Publier 14 comme « zones aveugles » aurait
été faux : un menu contextuel est vide **par construction**, une sortie de
calculette se remplit **au clic**, un bandeau conditionnel reste vide **quand il
n'y a rien à dire**.

Un second instrument (`l545_attente.js`) a tranché sur le seul critère qui
compte — **le remplissage vient-il après une attente ?** (fonction `async`, ou
callback `.then`/`.catch`) : **14 → 6**. Puis la lecture du code a retiré
`an-fresh` et `an-stale`, deux indicateurs conditionnels dont le vide est l'état
normal : **6 → 4**.

**Arrêtés avant publication : 162 → 164.**

## (1) Les conteneurs à squelette — la question du 535, posée à cette page

```text
/analysis/AAPL        200 · 75 216 octets · 69 id servis · 15 `vx-skeleton`
   conteneurs à squelette                                15
      visés DIRECTEMENT (`$(id)` littéral)                5   dont écrits 4
      CONFIÉS à une fonction (littéral passé)            10
      INTROUVABLES dans le JS servi                       0
```

**Zéro muet.** Aucune barre de chargement éternelle sur cette page non plus.

`an-rail-decision` ressort « référencé sans écriture prouvée ». Lecture du
code : l'écriture passe par
`$('an-rail-decision').querySelector('[data-body]')` — **une limite de
l'instrument, pas un défaut** ; le conteneur est bien rempli.

## (2) L'inverse, que personne n'avait cherché : **écrit, mais rien d'annoncé**

```text
identifiants servis                                      69
   servis VIDES (ni balise ni texte)                     19
   servis dans lesquels le JS ÉCRIT (prouvé)             27
   ÉCRITS, servis VIDES et SANS squelette                14
      sous ATTENTE (async / .then)                        6
      hors attente (synchrone, clic, conditionnel)        8
      invisibles à l'analyseur                            0
```

Les 8 hors attente sont légitimes et nommés : `an-badges` (synchrone, depuis le
magasin local), `an-cp-out` et `an-pt-out` (sorties de calculettes, au clic),
et les cinq coquilles du shell — `vx-context-menu`, `vx-drawer-body`,
`vx-modal-body`, `vx-modal-footer`, `vx-palette-list`.

Restent, après lecture, **quatre zones de contenu qui se remplissent après une
attente réseau et n'annoncent rien** :

```text
an-chart        <- loadDossier         (await /api/ticker + /api/strategy/decision)
an-scores       <- loadDossier
an-committee    <- loadDecisionStack   (await /api/decision)
an-scenarios    <- loadDecisionStack
```

`an-fresh` et `an-stale` sont écartés : ce sont un bandeau d'avertissement
conditionnel et une pastille de fraîcheur, dont le vide est l'état normal.

## La preuve la plus nette — **la page se contredit à la même ligne**

`analysis_page.py`, ligne 736, dans `loadDecisionStack` :

```javascript
const V=$('an-verdict'),SC=$('an-scenarios'),CO=$('an-committee');
```

**Trois conteneurs, la même fonction, le même `await`.** Dans les octets servis,
`an-verdict` porte `<div class="vx-skeleton" style="height:48px">` ; `an-scenarios`
et `an-committee` sont servis vides. Ce n'est pas une page qui ignore la
convention : **c'est une page qui l'applique à un conteneur sur trois de la même
déclaration.**

**Ce constat n'est pas arbitré et n'entre pas dans le relevé.** Il est nommé
comme candidat, borné à **quatre conteneurs**, et **rien n'est corrigé** — cela
demande un GO.

## (3) L'angle mort du corpus, chiffré

```text
conteneurs à squelette de /analysis nu                    1   (`an-recent`)
conteneurs à squelette de /analysis/AAPL                 15
id servis par la page nue                                32
id servis par la page d'un titre                         69
id de la cible ABSENTS de la page nue                    43   (préfixe `an`, 43)
recouvrement avec les 63 conteneurs des 43 URL            0
```

**Les 15 sont entièrement neufs.** Aucun ne figurait dans les 63 du 535,
reconfirmés au 544.

## (4) La dette du 544, réduite et recomptée

```text
identifiants à squelette dans `vertex/ui/**.py`          150
   servis par les 43 URL (chemin 1 du 544)                63
   jamais servis par les 43 URL                           87
      dont servis par /analysis/AAPL                      15
      restent jamais servis par aucune URL mesurée        72
servis avec squelette mais absents de la source            0
```

**87 → 72.** La dette nommée au 544 est réduite d'un sixième, et ce qui reste
est dit.

## Second contrôle (481) — ce que le crible ne voit pas sur cette page

```text
(a) appels à argument CONSTRUIT                          17   4 formes distinctes
       document.getElementById(host) · (hostId) · (id) · (t)
(b) `querySelector` / `querySelectorAll`                 39   dont bibliothèque 0
(c) squelettes POSÉS PAR LE JAVASCRIPT (occurrences)      1   `vx-core.js`
(d) identifiants RÉFÉRENCÉS mais ABSENTS du HTML servi   23
       `an-order-ticket`, `ot-*`, `fc-*`, `fd-*`, `fe-*`, `vx-add-confirm`…
```

Les 23 de la catégorie (d) sont les champs de formulaires et de tickets **créés
à la demande** ; ils ne sont pas servis, donc pas comptés. **Ces quatre
catégories sont comptées à part et ne sont jamais ajoutées aux 15.**

## Ce que le dépôt fait bien, mesuré

- **Zéro conteneur à squelette muet** sur la page la plus riche du produit :
  les 15 ont un chargeur.
- **Dix conteneurs sur quinze sont confiés à une fonction** (`VXCharts.*`,
  builders) — l'idiome dominant, et l'analyseur le suit.
- **Zéro conteneur servi avec squelette qui ne vienne de la source.**
- **La page nue et la page d'un titre ne se recouvrent pas** : le produit sert
  bien deux surfaces distinctes, et non une page dégradée.

## Portée — ce que ce lot NE dit PAS

- **Un seul symbole a été mesuré** (`AAPL`). Une autre valeur pourrait servir
  d'autres conteneurs ; rien n'est extrapolé (**529-B**).
- **Aucun navigateur.** « Servi vide » est mesuré sur les **octets servis** ;
  ce qu'un utilisateur voit dépend aussi du CSS, qui n'est pas mesuré ici.
- Les commentaires HTML ne comptent pas comme contenu — c'est un choix, il est
  dit.
- La catégorie « sous attente » est décidée sur la **fonction englobante**
  (`async` ou `.then`), pas sur l'ordre réel d'exécution.
- **Les quatre zones ne sont pas arbitrées** : constat, pas dossier.
- **Aucune exécution de chargeur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; toutes
  les sorties en chemin **absolu**, y compris le diagnostic jetable (544).
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans chaque banc.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés pendant le lot** (`ai_enrichment.json`, `daily_prev.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Mais **le plus gros angle mort du produit est ouvert et mesuré** :
la page d'analyse d'un titre tient la promesse du 535 — quinze conteneurs, zéro
muet — et pose une question neuve que les 43 URL ne pouvaient pas poser.

Ce qu'il faut dire sans le maquiller : **le brief m'a donné un témoin faux, et
je l'ai suivi jusqu'à l'échec de calibration.** C'est exactement ce à quoi sert
la calibration — mais c'est aussi la deuxième fois que ce brief, que j'écris
moi-même, déforme un résultat antérieur (le 538 sur une cause, celui-ci sur une
propriété). **Une phrase recopiée d'un lot à l'autre se dégrade.**

Trois règles neuves :

- **545-A · PRÉSENT N'EST PAS PORTEUR** — le 544 disait « `an-chart` présent
  hors script » ; le brief en a fait « conteneur à squelette ». Les octets
  servis disent `<div id="an-chart"></div>`.
- **545-B · UN CONTENEUR VIDE N'EST UN DÉFAUT QUE S'IL Y A UNE ATTENTE** —
  14 → 6 par l'instrument, 6 → 4 par la lecture. Dix des quatorze sont vides
  par construction.
- **545-C · UNE PAGE PEUT SE CONTREDIRE À LA MÊME LIGNE** — `an-verdict`
  annonce, `an-scenarios` et `an-committee` non, dans la même déclaration et
  sous le même `await`.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 4 zones sous attente sans annonce de
`/analysis/<symbole>` — candidat, non arbitré** ; **les 72 identifiants à
squelette encore jamais servis** ; **les SEPT chiffres lourds encore NON
RECOMPTÉS** (112 atténuations, 103 états, 53 refus, 178 appels, 156 variables
serveur, 25 fonctions, 11 limites) ; **le contrat d'ÉCHEC serveur, jamais
observé** ; **les 4 noms de clé du 542** ; **les 15 messages d'erreur sans
pourquoi du 541** ; **les 95 atténuations non affichées** ; **`initSettings`** ;
**les 8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42
cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes —
outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 164 (+2)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
