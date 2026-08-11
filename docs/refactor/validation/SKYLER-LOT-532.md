# SKYLER LOT 532 — **531-A double de taille : quatre chargeurs d'Opportunités sur cinq laissent un squelette perpétuel, pas deux.** Et le crible statique désignait six coupables — l'exécution en disculpe deux

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-532` (base : lot 531 fusionné,
`63841c02`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(r)** — le 531 a trouvé un défaut réel en lisant **cinq chargeurs d'une seule
page**. La question évidente : **sur tout le JS servi, combien de chargeurs
attaquent `VX.fetch` sans protection ?** Chacun est un squelette perpétuel
potentiel.

Mesuré **par comptage d'accolades**, pas par grep (**515-A**) : chaque
`VX.fetch(` vit-il **à l'intérieur d'un `try{`** de la même fonction, ou porte-t-il
un `.catch(` ?

## Le témoin a pris mon instrument en défaut — puis c'est le témoin qui était faux

```text
CALIB 1 · POSITIF   /opportunities renderRadar     NON PROTÉGÉ        OK
CALIB 2 · NÉGATIF   /opportunities renderCalendar  PROTÉGÉ            OK
CALIB 3 · NÉGATIF   /opportunities renderOptions   PROTÉGÉ …      ÉCHEC
```

**Premier échec — un homonyme.** Ma fonction de lecture cherchait **par nom
seul** : `renderOptions` existe sur `/opportunities` **et** sur `/portfolio`, et
elle ramenait le mauvais. Famille **521-B**, corrigée en cherchant par
**(page, nom)**.

**Second échec, plus intéressant : c'était le TÉMOIN qui avait tort.** Au lot
531, j'avais noté « `renderOptions` : try · catch » sur un test grossier — « le
corps contient-il `try` ? ». Relecture du code :

```js
async function renderOptions(){
  const scan = await VX.fetch('/scan', {ttl:120000});   // ← HORS de tout try
```

Le `try` existe, mais **ailleurs dans la fonction**. **L'instrument avait
raison, ma lecture du 531 était trop grossière.**

**Publiés puis corrigés : 20 → 21.**

## La mesure, sur tout le JS servi

```text
fonctions appelant `VX.fetch`                          76
appels `VX.fetch` au total                             93
appels NON PROTÉGÉS                                    12
fonctions NON PROTÉGÉES                                 7
```

**Quatre-vingt-un appels sur quatre-vingt-treize sont protégés — 87 %.** Le
motif dominant du produit est **le bon**.

## Le second contrôle : le crible statique accuse six, l'exécution en disculpe deux

Six fonctions non protégées écrivent dans un conteneur qui porte un
`vx-skeleton`. **Mais un risque quantifié n'est pas un risque réalisé**
(**524-B**) — et l'une d'elles, `loadConnections`, avait été mesurée au 531
comme peignant **770 caractères** en régime d'échec. **Contradiction : il faut
exécuter** (**520-B**).

```text
CALIB 1 · POSITIF   renderAnomalies (muet, confirmé au 531)   0 car.   OK
CALIB 2 · NÉGATIF   renderCalendar  (protégé)                50 car.   OK

page             chargeur           conteneurs   texte   erreur
/opportunities   renderAnomalies             0       0   HTTP 500
/opportunities   renderRadar                 0       0   HTTP 500
/opportunities   renderOptions               0       0   HTTP 500
/opportunities   renderStocks                0       0   HTTP 500
/opportunities   renderCalendar              1      50
/options         loadStructure               5       7
/system          loadConnections            14     770
/system          loadData                    4     314
```

**`loadConnections` et `loadData` sont DISCULPÉS** : non protégés, mais ils
peignent **770** et **314** caractères sur panne. Leur code écrit avant, ou
autour, de l'appel fragile.

## 531-A s'élargit : deux chargeurs → **quatre**

```text
/opportunities   renderRadar        0 caractère en régime d'échec
/opportunities   renderAnomalies    0
/opportunities   renderOptions      0   ← nouveau
/opportunities   renderStocks       0   ← nouveau
```

Les deux nouveaux avaient échappé au 531 : en régime **riche** et **vide**, ils
butaient sur `PARAMS is not defined`, la limite connue du résolveur. **En régime
d'échec, `VX.fetch` lève AVANT que `PARAMS` ne soit évalué** — la fonction
devient mesurable, et elle est muette.

**Quatre des cinq vues d'`/opportunities` laissent donc un squelette de
chargement perpétuel sur panne réseau. Seule `calendar` survit.** Le dossier
**531-A garde son rang 3** ; c'est son **ampleur** qui double.

## Ce que le dépôt fait bien, mesuré

- **87 % des appels `VX.fetch` sont protégés** (81 sur 93). Le bon motif est la
  norme, pas l'exception.
- **Sur les six candidats désignés par la lecture statique, deux se défendent
  très bien à l'exécution** : `loadConnections` peint 770 caractères sur panne,
  `loadData` 314. **Ne pas les avoir accusés est le résultat du second
  contrôle.**
- **Le défaut est concentré** : sept fonctions non protégées, dont **quatre dans
  un seul fichier**, `opportunities_page.py` — et la cinquième du même fichier,
  `renderCalendar`, **porte déjà le motif correct à quelques lignes de là**.

## Portée — ce que ce lot NE dit PAS

- **Le crible ne voit que `VX.fetch`.** Un chargeur qui passe par `get(...)` ou
  `fetch` direct n'est pas compté.
- **`loadStructure` peint 7 caractères** sur panne : ce n'est pas zéro, mais
  c'est très peu. **Candidat nommé, non promu** — le vérifier demanderait de
  regarder ce que ces 5 conteneurs affichent réellement.
- Le régime d'échec simulé est **une levée** ; une réponse tronquée n'est pas
  couverte.
- **Aucun navigateur**, aucun réseau (`VX.fetch` stubé, `globalThis.fetch` lève).
- **Aucune correction engagée**, ni ici ni sur 531-A.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** ; harnais pris dans `l523_balayage.py`
  (**531-B**) et **contrôlé non vide** avant usage.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0**.

**Aucun dossier neuf — et un dossier existant qui double.** C'est la meilleure
suite possible au 531 : au lieu d'ajouter une ligne, le lot **mesure la vraie
taille** de ce qui était déjà trouvé, et **innocente deux accusés** au passage.

Trois règles neuves :

- **532-A · CHERCHER PAR (PAGE, NOM), JAMAIS PAR NOM SEUL** — `renderOptions`
  existe deux fois ; troisième forme d'homonyme après la fonction, le module et
  `get`.
- **532-B · UN TÉMOIN PEUT AVOIR TORT** — quand l'instrument et le témoin se
  contredisent, **relire le code** ; ici c'est le témoin, issu d'une lecture
  grossière, qui était faux.
- **532-C · UN RÉGIME DE PANNE PEUT RENDRE MESURABLE CE QUE LE RÉGIME NOMINAL
  BLOQUE** — `VX.fetch` lève avant `PARAMS`, et deux chargeurs invisibles au 531
  deviennent mesurables.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A**, dont l'ampleur passe de **2 à 4 chargeurs**.

Dettes nommées restantes : **`loadStructure` et ses 7 caractères** ; **les 9 vues
d'`/options`, non mesurées** ; **les chargeurs passant par `get(...)`** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 139 (+2)** ;
**publiés puis corrigés 21 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A, désormais deux fois plus large, attend un GO pour être corrigé.**
