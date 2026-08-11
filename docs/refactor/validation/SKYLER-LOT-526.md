# SKYLER LOT 526 — **La feuille ne s'additionne pas.** Douze lots publiés, de 511 à 525, annoncent un total qui contredit sa propre répartition — toujours de un. Et le désaccord **ne se tranche pas** : aucune liste canonique des dossiers n'existe

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-526` (base : lot 525 fusionné,
`59c85978`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix, et son échec

**(f)** — écrire les définitions des chiffres qui portent les cinq dossiers de
rang 4. La règle **525-A** venait d'être payée cher ; l'appliquer à toute la
feuille était le prolongement naturel.

**Premier geste : retrouver ces cinq dossiers dans les rapports, sans les
deviner** (**523-C**). Le crible a été calibré à trois étages.

```text
CALIB 1 · POSITIF   `518-A` ressort au rang 4                        OK
CALIB 2 · NÉGATIF   un identifiant FABRIQUÉ ne rend rien             OK
CALIB 3 · TOTAL     34 dossiers retrouvés · 18 rang 1 · 6 rang 2 ·
                    1 rang 3 · 9 rang 4                          ÉCHEC
                    la feuille annonce 37 · 16 · 12 · 5 · 5
```

**Le témoin positif passe, le témoin de total échoue.** Neuf dossiers de rang 4
là où la feuille en annonce cinq ; un seul de rang 3 là où elle en annonce cinq.
Et l'attribution dérape : le crible range « 511-A » sous le **lot 512**, parce
que le rapport du 512 cite le dossier du lot précédent.

**Un instrument qui ne retrouve pas le total de sa propre référence ne mesure
rien** (**516-A**). **Je ne publie pas la liste des cinq. Arrêt.**

## Alors j'ai retourné la question sur la feuille elle-même

Au lieu de forcer l'extracteur, une question qui ne demande **aucun
instrument** — seulement une addition : **la feuille est-elle cohérente avec
elle-même ?**

```text
CALIB 2 · POSITIF   phrase FABRIQUÉE juste (38 = 16+12+5+5) → cohérente   OK
CALIB 3 · NÉGATIF   phrase FABRIQUÉE fausse (30 ≠ 38)       → incohérente OK
CALIB 1 · CHARGE    12 occurrences de la phrase de feuille                OK
```

```text
occurrences trouvées                    12
   COHÉRENTES (total = somme)            0
   INCOHÉRENTES                         12
écart (somme − total)                   +1  dans les douze cas
```

```text
lot 513 : 34 dossiers annoncés · 16 + 11 + 5 + 3 = 35   (+1)
lot 515 : 35 dossiers annoncés · 16 + 12 + 5 + 3 = 36   (+1)
lot 516 : 35 …                                     36   (+1)
lot 517 : 35 …                                     36   (+1)
lot 520 : 37 dossiers annoncés · 16 + 12 + 5 + 5 = 38   (+1)
lot 521 : 37 …                                     38   (+1)
lot 522 : 37 …                                     38   (+1)
lot 523 : 37 …                                     38   (+1)
lot 524 : 37 …                                     38   (+1)
lot 525 : 37 …                                     38   (+1)
```

**Douze lots publiés, zéro cohérent, toujours le même écart de un.** Le chiffre
de tête de chaque rapport — celui que je republie à chaque lot — **se contredit
lui-même**, et personne, moi le premier, ne l'a additionné.

**Publiés puis corrigés : 17 → 18.**

## Lequel des deux est faux ? **On ne peut pas le savoir**

Trancher demanderait une **liste canonique des dossiers**. Il n'en existe
aucune.

```text
662 documents markdown balayés
   identifiants `NNN-A` distincts, tous documents confondus     44
```

Quarante-quatre — ni 37, ni 38. Et pour une raison qui invalide ce compte :
**`NNN-A` désigne tantôt un dossier, tantôt une règle de méthode.** `515-A`
(« préférer l'AST au motif »), `521-B`, `523-C`, `525-A` sont des **règles**, pas
des dossiers. Les deux populations partagent la même forme d'identifiant.

**Le désaccord 37 / 38 est donc NON TRANCHABLE par ce chemin.** Conformément à
**525-B**, je ne choisis pas le nombre qui m'arrange : **la feuille compte 37
OU 38 dossiers, et je ne sais pas lequel.**

## Ce que je change, et qui ne coûte rien

À partir de ce lot, la ligne de feuille s'écrira **« 37 ou 38 dossiers — le
total et la répartition se contredisent depuis au moins le lot 511, désaccord
non tranché faute de liste canonique »**, jusqu'à ce qu'une liste existe.
**C'est moins beau et c'est vrai.**

## Second contrôle — ce que mon motif EXCLUT (règle 481)

```text
rapports mentionnant une répartition de rangs        104
   attrapés par mon motif strict                      12
   NON attrapés, donc NON vérifiés                    92
```

**« Première incohérence au lot 511 » est une propriété de MON MOTIF, pas de la
feuille.** Les 92 rapports non attrapés emploient une autre formulation et n'ont
pas été additionnés. L'incohérence est peut-être **bien plus ancienne** — le
« depuis 511 » est une **borne haute de récence**, pas une date.

Et mon crible de dossiers, celui qui a échoué, avait une seconde faiblesse : il
lit la section « ## Classement » d'un rapport, où un lot peut citer le dossier
d'un autre. **Un identifiant trouvé dans un rapport n'appartient pas
nécessairement à ce rapport** — famille 519-A.

## Ce que le dépôt fait bien, mesuré

- **La trace existe** : `SKYLER-INDEX.md` porte 44 identifiants distincts et
  `STATUS.md` 38 — chaque lot a bien déposé sa ligne. **Ce n'est pas la mémoire
  qui manque, c'est l'agrégat qui a dérivé.**
- **Vertex n'est pas en cause.** Ce lot ne trouve rien sur le produit : le défaut
  est entièrement dans **ma comptabilité**. Le code, les tests, les octets servis
  sont intacts — MD5 8 / 8, suite 2864.

## Portée — ce que ce lot NE dit PAS

- **Il ne dit pas que la feuille est fausse**, mais qu'elle est **incohérente
  avec elle-même**. Les dossiers existent, ils sont documentés un par un ; c'est
  leur **somme** qui ne tient pas.
- **Il ne dit pas depuis quand.** 92 rapports n'ont pas été vérifiés.
- **Il ne dit pas quel nombre est juste.** Établir la liste canonique demanderait
  de décider ce qui compte comme dossier — un travail qui touche la feuille
  elle-même, et **je ne l'engage pas sans GO**.
- Le travail annoncé — écrire les définitions des cinq dossiers de rang 4 — **n'a
  pas été fait** : je n'ai pas pu établir lesquels ils sont.
- **Aucun navigateur, aucun POST, aucune route appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Le lot devait documenter la feuille ; il a découvert qu'**elle ne
s'additionne pas**. C'est le prolongement direct du 525 : après un chiffre
**non recomptable faute de définition**, un chiffre **incohérent faute
d'addition**. Deux lots de suite, la faiblesse n'est pas dans Vertex — elle est
dans la façon dont je tiens mes comptes.

Trois règles neuves :

- **526-A · UNE FEUILLE DOIT S'ADDITIONNER** — vérifier la cohérence interne
  d'un agrégat avant de le republier. Douze lots ont recopié une somme fausse.
- **526-B · UN AGRÉGAT REPORTÉ DE LOT EN LOT N'EST VÉRIFIÉ PAR PERSONNE** — sans
  liste canonique, un total est une rumeur qui se transmet.
- **526-C · UN IDENTIFIANT PARTAGÉ PAR DEUX POPULATIONS NE COMPTE NI L'UNE NI
  L'AUTRE** — `NNN-A` désigne ici un dossier, là une règle de méthode ; les
  compter ensemble ne mesure rien.

Feuille : **37 ou 38 dossiers — total et répartition se contredisent, désaccord
non tranché** · seize rang 1 · douze rang 2 · cinq rang 3 · cinq rang 4.

Dettes nommées restantes : **établir la liste canonique des dossiers** (dette
neuve, bloquante pour tout compte futur) ; **les 92 rapports non additionnés** ;
**les définitions des chiffres de rang 4, non écrites** ; **les quinze lots
exposés non recomptés** ; **l'ampleur du 518-A, encadrée** ; **les 17 chargeurs
muets** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en
attente d'un GO** ; **l'assemblage entre fonctions** ; **la condition `k ≤ 5` sur
un scan réel**.

Comptes séparés : résultats faux **arrêtés avant publication 129 (+1)** ;
**publiés puis corrigés 18 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
