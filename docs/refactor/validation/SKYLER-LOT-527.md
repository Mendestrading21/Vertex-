# SKYLER LOT 527 — Le relevé canonique existe : `docs/skyler/DOSSIERS.md`. **Trente-cinq dossiers, dont seulement DIX ont leur rang écrit dans un titre — et ces dix donnent exactement CINQ rangs 4, le chiffre de la feuille, retrouvé pour la première fois par un chemin indépendant**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-527` (base : lot 526 fusionné,
`ee3f3a1b`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.** Un fichier de documentation créé.

## Le choix

**(h)** — établir la liste canonique des dossiers. Le 526 a montré que **tout
compte futur est impossible sans elle** : le total ne se tranche pas, les rangs
ne se recomptent pas, et un identifiant `NNN-A` peut désigner un dossier **ou**
une règle de méthode. C'est la seule dette qui **bloque toutes les autres**.

**Ce lot produit un RELEVÉ, pas un arbitrage.** Les cas douteux sont inscrits
`AMBIGU` avec leurs deux lectures. L'humain tranchera.

## Deux corrections au crible qui avait échoué au 526

- **Auto-attribution** : un identifiant `NNN-A` n'est retenu que s'il porte **le
  numéro du rapport lui-même**. Le 526 rangeait « 511-A » sous le **lot 512**,
  parce que le rapport du 512 cite le dossier du lot précédent.
- **Exclusion des refus** : un rapport qui publie « aucun dossier » ou « rang 0 »
  ne produit plus d'entrée.

```text
CALIB 1 · POSITIF NOMMÉ        `518-A` figure, rang 4                   OK
CALIB 2 · NÉGATIF DE POPULATION `525-A` (règle de méthode) absent       OK
CALIB 3 · NÉGATIF DE REFUS     le lot 520 (rang 0 publié) ne produit
                               aucune entrée                            OK
CALIB 4 · TOTAL                35 dossiers · 18 rang 1 · 6 rang 2 ·
                               1 rang 3 · 10 rang 4 — annoncé TEL QUEL
```

**Le total ne vaut ni 37 ni 38, et la répartition ne ressemble pas à celle
publiée.** C'est le résultat, pas un échec : c'est exactement ce que le lot
cherchait à établir.

## Le vrai résultat : séparer les rangs FIABLES des rangs FRAGILES

Un rang écrit dans le **titre** de section est fiable. Un rang qui n'apparaît que
dans le **corps** peut désigner un rang **rejeté** — « ce n'est pas un rang 2,
c'est un rang 4 ». **Les mélanger fabrique un faux compte.**

```text
dossiers relevés                                   35
   rang lu dans le TITRE   (fiable)                10
   rang lu dans le CORPS   (fragile)               25

répartition FIABLE     rang 1 : 2 · rang 2 : 3 · rang 4 : 5
répartition FRAGILE    rang 1 : 16 · rang 2 : 3 · rang 3 : 1 · rang 4 : 5
```

**Le sous-ensemble fiable donne exactement CINQ dossiers de rang 4.** C'est le
chiffre de la feuille — **retrouvé pour la première fois par un chemin
indépendant**. Tout le bruit vit dans le sous-ensemble fragile.

## Les cinq dossiers de rang 4, enfin nommés

| dossier | lot | ce qu'il dit | son chiffre porteur, et sa définition |
|---|---|---|---|
| **511-A** | 511 | 41 routes d'API que personne n'appelle | **41 routes · 31 %** — définition de « surface de données » **non vérifiée par ce lot** |
| **512-A** | 512 | `context.headline` est calculée et jamais peinte | **aucun chiffre unique** — un moteur, un fichier, une fonction, trois routes |
| **513-A** | 513 | « Top X % » devient un chiffre faux le jour où il s'affiche | **« Top 2 % », DÉMO, n = 20** — **définition ÉCRITE** |
| **518-A** | 518 | La majorité des vues servies n'a aucun test de contenu | **77 %** — **DÉFINITION MANQUANTE**, établi au 525 : de **57 %** à **94 %** |
| **519-A** | 519 | Trois vues servies et maintenues, sans porte d'entrée | **3 vues · 358 lignes · 21 621 octets** — périmètre **cité** |

**Sur cinq chiffres porteurs : un a sa définition écrite, un n'a pas de chiffre
unique, un a son périmètre cité, un a sa définition manquante et prouvée
manquante, un n'a pas été vérifié.** Voilà la vraie photographie de la feuille.

Trois de ces cinq identifiants — `511-A`, `513-A`, `519-A` — sont
**reconstruits** : leur rapport ne les nomme pas dans sa section de classement.
`AMBIGU` sur l'identifiant, **pas** sur le rang.

## L'arrêt du lot

Devant « 18 · 6 · 1 · 10 » contre « 16 · 12 · 5 · 5 », j'ai failli écrire que
**la répartition publiée est réfutée**. La séparation fiable / fragile montre
que ce n'est pas mesurable ainsi : **les 25 rangs fragiles portent tout
l'écart**, et le sous-ensemble fiable **confirme** les cinq rangs 4.

**Arrêtés avant publication : 129 → 130.**

## Second contrôle — ce que le relevé EXCLUT (règle 481)

```text
rapports au total                                        524
   COUVERTS par le relevé                                 35
   REFUS explicites (aucun dossier / rang 0)              13
   mentionnent un rang SANS section de classement         78
   ne mentionnent aucun rang                             398

parmi les 78 sans section
   antérieurs au plus ancien relevé (lot 416)             24
   DANS la période couverte                               54
```

**Le « 35 » est une BORNE BASSE.** Jusqu'à 78 rapports pourraient porter un
dossier non structuré, dont **54 en pleine période couverte** — ceux-là sont les
plus suspects.

**Donc l'écart avec « 37 ou 38 » n'est pas une contradiction : c'est une lacune
de couverture.** Mon crible ne voit que les rapports structurés en
`## Classement`, et cette structure ne s'est imposée qu'avec le temps.

## Ce que le dépôt — et la boucle — font bien, mesuré

- **Treize rapports publient un refus explicite** (« aucun dossier », « rang
  0 »). Ne rien trouver et le dire est une pratique tenue, pas une exception.
- **La discipline du titre s'est installée** : sur les dix rangs écrits dans un
  titre, **six appartiennent aux lots 511 à 519** — la période récente. La
  pratique s'est améliorée d'elle-même avant qu'on ne la nomme.
- **La trace n'a jamais manqué** : chaque dossier est documenté dans son
  rapport. C'est l'agrégat qui dérivait, pas la mémoire.

## Portée — ce que ce lot NE dit PAS

- **Il ne tranche pas le total.** 35 est une borne basse ; « 37 ou 38 » reste
  non tranché.
- **Il ne tranche pas 25 rangs sur 35.** Les rangs lus dans un corps peuvent
  désigner un rang rejeté.
- **Il ne nomme pas 33 dossiers sur 35** : leurs identifiants sont
  **reconstruits** depuis le numéro de lot.
- **Il ne vérifie pas les définitions**, sauf celle du 518-A que le 525 avait
  déjà établie comme manquante.
- **Rien n'est arbitré, rien n'est corrigé, rien n'est supprimé.**
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
- Fichier créé : `docs/skyler/DOSSIERS.md`, **généré depuis le JSON du banc**,
  jamais recopié à la main.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier — et la dette la plus bloquante de la boucle est **entamée et
bornée**. Après deux lots où mes propres comptes se sont effondrés (525 : un
chiffre non recomptable ; 526 : une feuille qui ne s'additionne pas), celui-ci
**reconstruit un sol** : un fichier qui dit ce qu'on sait, ce qu'on ne sait pas,
et pourquoi.

Trois règles neuves :

- **527-A · UN RELEVÉ N'EST PAS UN ARBITRAGE** — enregistrer les deux lectures
  d'un cas douteux vaut mieux que trancher vite.
- **527-B · SÉPARER LE FIABLE DU FRAGILE AVANT D'AGRÉGER** — dix rangs lus dans
  un titre disent plus que trente-cinq rangs mélangés, et c'est cette séparation
  qui a retrouvé les cinq rangs 4.
- **527-C · UN ÉCART AVEC UNE RÉFÉRENCE PEUT ÊTRE UNE LACUNE DE COUVERTURE** —
  avant de crier à la contradiction, mesurer ce que l'instrument ne voit pas.

Feuille : **37 ou 38 dossiers annoncés — désaccord non tranché** ; **relevé
canonique : 35 entrées, borne basse** ; seize rang 1 · douze rang 2 · cinq
rang 3 · **cinq rang 4, confirmés et nommés : 511-A, 512-A, 513-A, 518-A,
519-A**.

Dettes nommées restantes : **les 54 rapports non structurés en période
couverte** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les définitions des chiffres porteurs, quatre sur cinq non vérifiées** ; **les
quinze lots exposés non recomptés** ; **les 92 rapports non additionnés du
526** ; **les 17 chargeurs muets** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 130 (+1)** ; publiés
puis corrigés **18** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
