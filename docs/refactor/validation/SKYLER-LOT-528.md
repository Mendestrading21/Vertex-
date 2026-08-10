# SKYLER LOT 528 — La lacune de couverture ne se lève pas par un motif : **trois des huit « nouveaux dossiers » étaient des CITATIONS d'autres lots**. Et la « confirmation des cinq rangs 4 » du 527 était un **artefact de couverture**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-528` (base : lot 527 fusionné,
`840ee44c`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien arbitré.**

## Le choix

**(j)** — lever la lacune que le 527 avait chiffrée : **54 rapports de la période
couverte mentionnent un rang sans porter de section `## Classement`**. Le relevé
canonique en dépendait.

## Les formes alternatives d'annonce, trouvées par lecture

Deux formes existent : une section **« Verdict du lot »** contenant « classé rang
N », et un **bilan** qui récapitule les rangs d'**autres** lots dans un tableau.
La seconde est une **citation** — exactement la dérive d'attribution que le 527
venait de corriger.

```text
CALIB 1 · POSITIF   lot 421 (« Classé rang 4 » dans « Verdict du lot »)
                    → DOSSIER, rang 4                                    OK
CALIB 2 · NÉGATIF   lot 430 (bilan, 6 lignes de tableau citant 423, 425…)
                    → CITATION                                           OK
CALIB 3 · VARIÉTÉ   les deux classes peuplées                            OK
```

```text
les 54 cas
   INDÉTERMINÉ    42
   DOSSIER         8
   CITATION        4
```

## Premier arrêt : une section qui REFUSE ne livre pas un rang

Mon premier jet classait le **lot 482** « DOSSIER rang 2 » — alors que son titre
de section dit **« Classement — AUCUN, et c'est le résultat »**. Le crible lisait
un rang dans une section de **refus**. Corrigé, re-passé.

## Deuxième arrêt, le plus grave : trois « dossiers » sur huit sont des CITATIONS

Les huit candidats ont été **vérifiés à la lecture**, un par un.

| lot | après lecture | ce que dit vraiment le rapport |
|---|---|---|
| 480 | **CITATION** | « classé rang 1 » est dans un **tableau** récapitulant les lots 476 et 447 |
| 483 | **CITATION** | « 456 + 459 … DÉJÀ CLASSÉ rang 2 » désigne les lots **456 et 459** |
| 488 | **CITATION** | « le 486 — qui a classé rang 2 » désigne le lot **486** |

**Trois sur huit : 37 % de faux positifs.** Un crible par phrase refabrique
instantanément la dérive d'attribution corrigée au 527. **La lacune de couverture
ne se lève pas par un motif.**

**Arrêtés avant publication : 130 → 132.**

## Les cinq candidats qui survivent — et aucun n'est net

| lot | rang annoncé | la réserve, lue dans le rapport |
|---|---|---|
| 421 | 4 | « Classé rang 4 » — **annonce propre**, la plus nette des cinq |
| 423 | 4 | verdict « **Négatif sur le produit** » — la portée du dossier est elle-même discutable |
| 431 | 4 | « **versant recoupement du dossier 386** (rang 1, déjà ouvert) » — un versant, pas forcément une entrée neuve |
| 453 | 4 | « **un sous-produit**, classé rang 4 » — pas l'objet principal du lot |
| 456 | 4 | « à requalifier si un banc l'exécute » — **et le 459 l'a requalifié RANG 2** |

**Aucun n'est un dossier neuf sans réserve. Les cinq restent `AMBIGU`. Rien n'est
arbitré** (**527-A**).

## Ce que cela fait à la « confirmation » du 527

Le 527 annonçait que le sous-ensemble fiable donnait **exactement cinq rangs 4**,
et y voyait le chiffre de la feuille **retrouvé par un chemin indépendant**.

**Cinq autres candidats de rang 4 existent dans la période couverte.** Ils sont
tous discutables, aucun ne s'impose — mais leur existence suffit à retirer au
« cinq » sa valeur de confirmation : **c'était un artefact de la lacune que le
527 avait lui-même signalée.** La règle **527-C** se retourne contre son auteur.

**Publiés puis corrigés : 18 → 19.**

## Une dimension qui manquait au relevé : LES RANGS BOUGENT

En vérifiant le 456, une chose apparaît que ni le 527 ni moi n'avions vue : **un
rang peut être requalifié après coup.** Le lot 480 l'avait déjà mesuré :

```text
459 → 456   rang 4 « par lecture » → RANG 2, établi par exécution     HAUSSE
478 → 407   le dossier fusionné 406+407 classé RANG 2                 BAISSE
479 → 416   rang 1 → rang 3                                           BAISSE
```

**Le relevé du 527 est statique ; la réalité ne l'est pas.** Un relevé qui ignore
les mouvements ne pourra **jamais** s'accorder avec un compte fait à une autre
date — et cela explique peut-être une part de l'écart 35 / 37 / 38.

Le relevé `docs/skyler/DOSSIERS.md` est complété en conséquence, **généré depuis
les JSON des bancs**, jamais édité à la main.

## Ce que le dépôt — et la boucle — font bien, mesuré

- **Les rapports disent leurs réserves.** « versant », « sous-produit », « à
  requalifier », « négatif sur le produit » : les cinq candidats portent tous,
  **écrite dans leur propre texte**, la raison pour laquelle ils sont douteux.
  **La prudence était déjà là ; il manquait seulement de la relire.**
- **Le 480 avait déjà mesuré les requalifications** — la donnée existait, elle
  n'avait simplement jamais rejoint le relevé.
- **Quatre bilans sont correctement identifiés comme des citations** par le
  crible, sans intervention.

## Portée — ce que ce lot NE dit PAS

- **Il n'ajoute aucun dossier au relevé.** Cinq candidats, cinq `AMBIGU`.
- **Il ne tranche pas le total.** « 37 ou 38 » face à 35 + 5 candidats reste
  ouvert, et **seule une décision humaine peut le clore**.
- **42 cas sur 54 restent INDÉTERMINÉS** : aucune forme d'annonce reconnue. Je ne
  les ai pas lus un par un.
- **Il ne relit pas les 24 rapports antérieurs** au plus ancien relevé.
- **Aucun navigateur, aucun POST, aucune route appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Le lot devait **lever** une lacune ; il établit qu'elle **ne se
lève pas automatiquement**, et il corrige au passage une conclusion publiée la
veille. C'est le troisième lot d'affilée où l'objet mesuré est **ma propre
comptabilité**, et le troisième où elle cède — mais elle cède **de moins en moins
loin** : le 526 découvrait une somme fausse, le 527 un relevé absent, le 528
seulement une frontière mal placée.

Trois règles neuves :

- **528-A · UNE PHRASE N'EST PAS UNE ATTRIBUTION** — « classé rang N » désigne
  souvent le dossier d'un autre lot ; 37 % de faux positifs mesurés.
- **528-B · UN CHIFFRE CONFIRMÉ SUR UN CORPUS PARTIEL N'EST PAS CONFIRMÉ** — la
  « confirmation » du 527 tenait à la lacune qu'il signalait lui-même.
- **528-C · UN RELEVÉ STATIQUE NE PEUT PAS DÉCRIRE UNE POPULATION QUI BOUGE** —
  trois requalifications de rang sont mesurées ; un relevé doit les porter.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; **relevé strict : 35** ;
**5 candidats ambigus de plus** ; **3 requalifications de rang mesurées** ; les
cinq rangs 4 du 527 (511-A, 512-A, 513-A, 518-A, 519-A) restent **nommés**, mais
**leur exclusivité n'est plus établie**.

Dettes nommées restantes : **les 42 cas indéterminés** ; **les 24 rapports
antérieurs** ; **les 25 rangs fragiles du 527** ; **les 33 identifiants
reconstruits** ; **les définitions des chiffres porteurs** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **les 17 chargeurs
muets** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en
attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 132 (+2)** ;
**publiés puis corrigés 19 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
