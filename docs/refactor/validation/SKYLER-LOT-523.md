# SKYLER LOT 523 — Le français que le produit PEINT, mesuré par exécution. **Zéro faute de langue sur 89 chargeurs et 37 vues servies — mais trois candidats spectaculaires étaient des artefacts de ma propre charge.** Et le 520 mesurait son propre balisage : ses octets sont recomptés

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-523` (base : lot 522 fusionné,
`14057c75`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)** — la dette du 516 : « le français construit en JavaScript », 336
occurrences mal discriminées, **jamais reprise depuis sept lots**. La raison est
maintenant nommable : le seul instrument disponible alors était un **grep**,
c'est-à-dire exactement la famille de mesure que le **522** vient de disqualifier.

Le harnais node du 520 change la donne. Il extrait une fonction du **JS servi**,
l'exécute, et **capture le texte réellement écrit dans le DOM**. Ce n'est plus un
motif : c'est une mesure de **sortie**.

## Ce que j'ai dû réparer d'abord : le harnais mesurait son propre appareil

Le 520 **stubait** `VX.states` et `Vf`. Or les deux sont **servis** :
`vx-core.js` L42 (`VX.fmt`) et L85 (`VX.states`). Le stub du 520 rendait
`<div class="vx-empty">…</div>` ; la fonction **réelle** rend un
`<div class="vx-state" data-state="empty">` avec une **silhouette SVG** et un
titre **« Aucune donnée »**.

Ici les deux objets sont **extraits du JS servi** (1 814 et 2 918 caractères) et
évalués ; `esc`, `emptyCard`, `loading` sont résolus automatiquement dans le code
servi. **C'est la leçon 522 appliquée à un harnais plutôt qu'à un chiffre.**

## Le crible, calibré avant tout le reste

Deux familles **non ambiguës** :

- **F1 · accord numérique brisé** — « 1 jours », « 1 positions ».
- **F2 · fuite technique dans le texte visible** — `undefined`, `NaN`,
  `[object Object]`, `Infinity`.

```text
CALIB CRIBLE · POSITIF   7 / 7 phrases bien formées passent            OK
   « 3 positions ouvertes » · « 1 position ouverte » · « 12 mois » · « 1 fois »
CALIB CRIBLE · NÉGATIF   6 / 6 phrases fautives signalées              OK
   « 1 jours » · « 1 positions » · « Score undefined » · « NaN % »
CALIB HARNAIS · POSITIF  `loadBreadth` (exécutée au 508) extraite      OK
CALIB HARNAIS · NÉGATIF  un nom FABRIQUÉ n'est pas extrait             OK
CALIB APPAREIL           VX.fmt et VX.states RÉELS extraits du servi   OK
```

## Le balayage

```text
105 fonctions candidates inventoriées sur les 8 pages
 89 ciblées (hors `loadStatus` / `renderPalette`, communes au shell)
267 exécutions = 89 × 3 régimes
    A · riche (3 éléments) · U · unitaire (1 élément) · V · vide {}
161 exécutions peignent · 55 fonctions sur 89 peignent au moins une fois
```

**Aucun réseau.** `VX.fetch` est un stub ; `globalThis.fetch` **lève « RESEAU
INTERDIT »**. Le code extrait est du code navigateur : il n'a aucun autre moyen
de sortir. Les URL demandées sont **capturées comme preuve**, jamais envoyées.

## F1 — zéro faute, sur cinq occasions seulement

```text
régime UNITAIRE, occurrences « 1 <mot> » réellement peintes :   4
   /opportunities  loadSkylerRank   « 1 titre »
   /portfolio      renderOptions    « 1 PUT »
   /options        loadPositions    « 1 PUT »
   /system         loadAutomations  « 1 erreur »
texte rendu par le SERVEUR, même motif :                        1
   /analysis                        « 1 Fondamental »
```

**Cinq occasions, cinq accords justes.** Je le dis comme c'est : **zéro défaut
sur cinq tirages est une preuve mince**, pas un quitus. Le crible a bien eu
l'occasion de se déclencher — c'est le minimum exigible — mais cinq fois
seulement.

## F2 — trois candidats, **trois réfutés**

Le balayage a signalé trois fonctions. C'étaient les seuls défauts visibles du
lot, donc précisément ceux qu'il fallait vérifier le plus durement (**520-B**).

| fonction | ce qui était peint | vérification | verdict |
|---|---|---|---|
| `/journal loadTrack` | `[object Object],… verdict(s) enregistré(s)` | `track_record.py:168` rend `'entries': len(entries)` — **un nombre** ; j'avais aliasé `entries` sur un **tableau** | **artefact** |
| `/journal loadPostmortem` | `Trades undefined` | `postmortem.py:59` et `:124` rendent **toujours** `trades_n` | **artefact** |
| `/portfolio renderDiscipline` | `undefined-undefined lignes cibles` | `/api/portfolio/context` **appelée** (route sûre) : rend `available: False` → la branche **honnête** ; et `portfolio_context.py:120-122` fournit **toujours** `bounds` et `n_positions` quand `available` est vrai | **artefact** |

**Les trois venaient de MA charge fabriquée, aucun du produit.**

**Arrêtés avant publication : 121 → 125** (+4 : les trois artefacts, plus les
slugs de vues écrits de mémoire — voir plus bas).

## Le chiffre du 520, recompté avec l'appareil réel

Le 520 publiait, pour `/system?view=automations`, des tailles de sortie. Elles
incluaient **mon propre balisage d'état vide**. Recomptées :

```text
                          520 publiait     appareil RÉEL      écart
A · charge riche          3 / 2208 o       3 / 2031 o          −177 o
B · charge VIDE {}        3 /  329 o       3 / 1987 o        +1 658 o
C · fetch en ÉCHEC        3 /  182 o       3 /  734 o          +552 o
```

**L'état vide réel est six fois plus gros que ce que le 520 a mesuré**, parce
qu'il porte un titre et une silhouette que mon stub n'avait pas.

**Les conclusions du 520 tiennent** : les **messages** (« Registre de jobs
vide. », « Registre indisponible : HTTP 500 ») sont bien des arguments écrits par
le produit, et les trois régimes se distinguent toujours. **Ce sont les octets
qui étaient à moi.**

**Publiés puis corrigés : 16 → 17.**

## Ce que le dépôt fait bien — et que le 520 ne pouvait pas voir

- L'état vide réel **nomme la situation** (« Aucune donnée ») **avant** d'en
  donner la raison, et affiche une silhouette plutôt qu'un rectangle vide.
- La bannière d'erreur réelle **offre une sortie** : un bouton **« Réessayer »**
  et un lien **« Ouvrir Système »**. Le 520 a conclu que le message était
  honnête ; il n'a pas pu voir que le produit **propose en plus une action de
  récupération**.
- **Zéro défaut sur les 37 URL servies** (25 454 caractères de texte rendu par le
  serveur) : le français rendu côté serveur ne porte aucune des deux fautes.
- Les registres de vues, **relus par AST**, donnent exactement **35 vues** —
  le chiffre du 518 se trouve confirmé par un chemin indépendant.

## Le second contrôle — ce que l'instrument EXCLUT (règle 481)

**A · le français rendu par le SERVEUR** ne passe par aucun chargeur. Balayé
séparément avec le même crible : **37 URL** (les 35 vues des registres + les 2
pages sans registre), **25 454 caractères**, **0 défaut**.

**Mes slugs étaient faux.** Mon premier jet les avait écrits **de mémoire** :
`regime`, `vix`, `discipline`, `memoire`, `app` n'existent pas. Une vue
inexistante **retombe sur la vue par défaut** — je mesurais donc la même page
plusieurs fois en croyant balayer le registre. Corrigé en **lisant les registres
par AST** (règle 519-C : un contrôle interne vaut mieux qu'un contrôle externe).
**Arrêt n° 125.**

**B · les chargeurs qui n'ont jamais peint** :

```text
89 fonctions exécutées · 55 ont peint · 34 MUETTES sous mon harnais
   19  constante de module absente (mon résolveur ne reprend que des FONCTIONS)
    4  aucune exception — sortie réellement vide
    4  `(rows || []).filter is not a function`   ← ma charge, pas le produit
    4  lecture d'une propriété d'un `undefined`
```

**34 chargeurs sur 89, soit 38 %, n'ont pas rendu leur français.** La cause
dominante est mienne : le résolveur automatique reprend les **fonctions**
voisines mais pas les **constantes de module** (`SCAN_ACTION`, `PARAMS`,
`IDX_MAIN`, `MACRO_NAMES`…). C'est une borne connue et chiffrée, pas une zone
ignorée.

## Portée — ce que ce lot NE dit PAS

- **Deux familles seulement.** Accords en genre, registre de langue, typographie
  française (espace avant les deux-points), anglicismes : **non mesurés**. Un
  anglicisme n'est d'ailleurs pas un défaut par principe en salle de marché
  (règle 515-C).
- **F1 n'a eu que cinq occasions.** Conclure « le produit accorde juste » serait
  extrapoler un tirage (**516-C**).
- **Les charges sont fabriquées.** Une phrase qui n'apparaît qu'avec des données
  réelles reste invisible ; et une fuite sous charge fabriquée ne prouve rien —
  c'est exactement ce que les trois réfutations démontrent.
- **38 % des chargeurs n'ont pas peint.** Leur français n'est pas mesuré.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.** Une seule
  route a été appelée, `/api/portfolio/context`, de la liste sûre.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les cinq bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0**.

Aucun dossier. Une dette de sept lots est **entamée et bornée** : sur la moitié
mesurable du français assemblé en JavaScript, **aucune faute des deux familles
cherchées** ; sur l'autre moitié, la raison de l'aveuglement est chiffrée.

Quatre règles neuves, toutes payées comptant :

- **523-A · NE PAS STUBER CE QUI EST SERVI** — un stub qui remplace une fonction
  réelle fait mesurer son propre appareil. Le 520 en est mort de six cents pour
  cent.
- **523-B · UN CRIBLE SANS OCCASION NE PROUVE RIEN** — compter les occasions
  avant d'annoncer « zéro défaut ».
- **523-C · LIRE LES SLUGS DANS LE REGISTRE, JAMAIS DE MÉMOIRE** — une vue
  inexistante retombe silencieusement sur la vue par défaut.
- **523-D · UNE FUITE SOUS CHARGE FABRIQUÉE N'EST PAS UN DÉFAUT** — remonter à la
  forme réellement rendue par le moteur avant de publier.

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **les 34 chargeurs muets** (dette neuve, chiffrée) ;
**le « 7 barèmes » du 491, non re-vérifiable sans instrument neuf** ; **mesurer
les 23 routes — outil prêt, en attente d'un GO** ; **l'assemblage entre
fonctions** ; **la condition `k ≤ 5` sur un scan réel** ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 125 (+4)** ;
**publiés puis corrigés 17 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
