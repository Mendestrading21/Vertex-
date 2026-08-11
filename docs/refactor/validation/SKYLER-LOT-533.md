# SKYLER LOT 533 — Le crible élargi à **cinq** helpers : +27 appels, +15 fonctions non protégées… et **zéro nouveau squelette perpétuel**. Quatre arrêts, dont la faute 521-B refaite à l'identique

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-533` (base : lot 532 fusionné,
`2fbc84b5`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(t)** — fermer les deux bornes que le 532 avait nommées : **son crible ne
voyait que `VX.fetch`**, et **les 9 vues d'`/options` n'avaient jamais été
mesurées**.

## Les helpers de récupération, trouvés **par lecture**

Pas une liste de noms devinée (**521-B**) : on cherche dans le JS servi les
fonctions qui **rendent** le résultat d'un `fetch`.

```text
board      /options
get        /options
getScan    /markets
rawFetch   les 8 pages
VX.fetch   vx-core.js
                            5 helpers
```

## Quatre arrêts — dont la faute 521-B refaite à l'identique

**1. Mon extracteur ne gardait que la PREMIÈRE définition par nom.** Sur
`/options`, un homonyme sans `fetch` masquait le vrai `get`, et **le témoin
positif échouait**. C'est la collision **532-A, mais à l'intérieur d'une page**.

**2. « Helper » était trop large.** Je retenais **toute** fonction contenant
`fetch(` — ce qui ramassait `reportError` (qui **poste un log**), `vaultSet`,
`wireCopilot`… **Compte gonflé : 213 appels dont 101 nus.** Un helper de
récupération **rend** la donnée ; les autres ne sont pas des sources.

**3. `\bget\s*\(` attrape TOUS les `.get(` du dépôt.** Entre `.` et `g`, `\b`
s'applique. **C'est exactement la faute du 521-B — le nom générique dans une
correspondance par nom — refaite deux lots après l'avoir écrite en règle.**
Compte gonflé : **195 appels dont 85 nus**. Corrigé par `(?<![.\w$])`.

**4. Quatre chargeurs d'`/options` « muets » ne le sont pas.** `loadOverview`,
`loadRadar`, `loadEvents` et `loadVolatility` échouent sur
« `Cannot read properties of undefined (reading 'then')` » : mon extracteur leur
a fourni **le mauvais `get`** — le même homonyme qu'au point 1, non corrigé côté
extraction. **Ce sont des artefacts d'instrument, pas des vues cassées.**

**Arrêtés avant publication : 139 → 143.**

## La mesure, après les quatre corrections

```text
                            532 (VX.fetch seul)      533 (5 helpers)
fonctions appelant           76                      102
appels au total              93                      120
appels NON PROTÉGÉS          12                       28
fonctions NON PROTÉGÉES       7                       22
```

## Le résultat qui compte : **zéro nouveau squelette perpétuel**

```text
SQUELETTES PERPÉTUELS POTENTIELS      6   (532 : 6)
   /opportunities   renderAnomalies · renderOptions · renderRadar · renderStocks
   /options         loadStructure
   /system          loadConnections
dont NOUVEAUX par rapport au 532      0
```

**L'élargissement ajoute 27 appels et 15 fonctions non protégées — et pas un
seul squelette perpétuel de plus.** Les quinze fonctions supplémentaires écrivent
dans des conteneurs **qui ne portent pas de squelette** : leur zone ne ment pas
sur son état.

**Le dossier 531-A garde donc exactement l'ampleur mesurée au 532 : quatre
chargeurs, tous sur `/opportunities`.** L'élargissement du crible **ne l'aggrave
pas** — et c'est une information.

## `/options`, mesurée pour la première fois

Preuve de sûreté réseau, montrée avant d'exécuter :

```text
le harnais contient `globalThis.fetch = async ()=>{ throw … RESEAU INTERDIT` : oui
`VX.fetch` du harnais est un STUB qui CAPTURE l'URL                        : oui
```

```text
chargeur           conteneurs   texte   URL demandées AU STUB
loadOverview                4       0   (artefact — mauvais `get`)
loadRadar                   1       0   (artefact)
loadEvents                  1       0   (artefact)
loadVolatility              1       0   (artefact)
loadScenarios               1      18
loadStructure               5       7   /api/options/strategies/…, /api/options
loadLeaps                   1       0   /api/options
loadPositions               1     131
renderVolCharts             4     123
```

**Aucune de ces URL n'a été envoyée** : elles sont capturées par le stub, et
`globalThis.fetch` lève.

**Quatre chargeurs peignent** (18, 7, 131, 123 caractères). **`loadLeaps` écrit
un conteneur sans texte visible** — **candidat nommé, NON PROMU** : il faudrait
regarder ce que ce conteneur contient réellement avant de conclure.

## Ce que le dépôt fait bien, mesuré

- **Élargir le crible de 93 à 120 appels n'ajoute aucun squelette perpétuel.**
  Le défaut reste **circonscrit à une seule page**.
- **Cinq chargeurs d'`/options` sur neuf peignent sur panne**, dont
  `loadPositions` (131 caractères) et `renderVolCharts` (123).
- Le produit n'a que **cinq helpers de récupération** pour 120 appels : la
  couche d'accès aux données est **concentrée**, donc corrigible en peu
  d'endroits.

## Portée — ce que ce lot NE dit PAS

- **Quatre chargeurs d'`/options` restent non mesurés** : mon extracteur leur
  donne le mauvais `get`. Limite nommée, non levée.
- **`loadLeaps` n'est pas tranché.**
- Le crible ne voit que les helpers **nommés** ; une récupération écrite en ligne
  dans un chargeur lui échappe.
- Le régime d'échec est **une levée**, pas une réponse tronquée.
- **Aucun navigateur, aucun réseau, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** ; harnais pris dans `l523_balayage.py` et
  **contrôlé non vide**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0**.

Aucun dossier. Le lot fait deux choses : il **borne** le 531-A (l'élargissement
ne l'aggrave pas) et il **mesure `/options` pour la première fois**. Mais il
faut dire le reste sans le maquiller : **quatre arrêts en un lot, dont la faute
521-B refaite deux lots après l'avoir écrite en règle**. Écrire une règle ne
suffit pas à la tenir.

Trois règles neuves :

- **533-A · UN HELPER DE RÉCUPÉRATION EST CELUI QUI REND LA DONNÉE** — une
  fonction qui contient `fetch` peut n'être qu'un émetteur de journal.
- **533-B · `\b` NE PROTÈGE PAS D'UN APPEL POINTÉ** — `\bget(` attrape tous les
  `.get(` ; il faut `(?<![.\w$])`.
- **533-C · CORRIGER UN HOMONYME À UN ENDROIT NE LE CORRIGE PAS PARTOUT** — je
  l'ai réparé dans la détection des helpers et laissé dans l'extraction, d'où
  quatre faux muets.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, inchangée).

Dettes nommées restantes : **les 4 chargeurs d'`/options` non mesurés** ;
**`loadLeaps`** ; **`loadStructure` et ses 7 caractères** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 92 rapports non additionnés du
526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ;
**mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 143 (+4)** ; publiés
puis corrigés **21** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend un GO pour être corrigé.**
