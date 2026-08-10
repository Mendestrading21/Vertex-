# SKYLER — RELEVÉ DES DOSSIERS

> **Ceci est un RELEVÉ, pas un arbitrage.** Il enregistre ce que les rapports
> disent, y compris quand ils se contredisent. **Rien n'est tranché ici.**
> Les cas douteux sont marqués `AMBIGU` avec leurs deux lectures.
> Produit par le lot 527 · banc `l527_releve.py`.

## Pourquoi ce fichier existe

Le lot **526** a mesuré que la ligne de feuille republiée à chaque lot **se
contredit elle-même** : le total annoncé vaut toujours **un de moins** que la
somme de sa propre répartition, et cela sur **douze occurrences publiées**.
Le désaccord ne pouvait pas se trancher : **aucune liste canonique**
n'existait, et un identifiant de la forme `NNN-A` désigne tantôt un dossier,
tantôt une règle de méthode.

## Comment ce relevé est construit

Une entrée est créée quand un rapport `SKYLER-LOT-NNN.md` porte une section
`## Classement` qui **annonce un rang de 1 à 4** et **ne refuse pas** le
dossier (« aucun dossier », « rang 0 »).

Deux corrections par rapport au crible du 526, qui avait échoué :

- **auto-attribution** : un identifiant `NNN-A` n'est retenu que s'il porte
  le numéro du rapport lui-même. Le 526 rangeait « 511-A » sous le lot 512
  parce que le rapport du 512 cite le dossier du lot précédent ;
- **exclusion des refus** : les rapports qui publient explicitement « aucun
  dossier » ne produisent plus d'entrée.

### Fiabilité du rang — deux qualités, à ne pas mélanger

- **TITRE** : le rang est écrit dans le titre de section. **Fiable.**
- **CORPS** : le rang n'apparaît que dans le texte, où il peut désigner un
  rang **rejeté** (« ce n'est pas un rang 2, c'est un rang 4 »). **Fragile.**

```text
dossiers relevés                                    35
   rang lu dans le TITRE  (fiable)                   10
   rang lu dans le CORPS  (fragile)                  25

répartition des rangs FIABLES   rang 1 : 2 · rang 2 : 3 · rang 4 : 5
répartition des rangs FRAGILES  rang 1 : 16 · rang 2 : 3 · rang 3 : 1 · rang 4 : 5
```

**Le sous-ensemble fiable donne exactement CINQ dossiers de rang 4** — le
même nombre que la feuille publiée. C'est la première fois qu'un chiffre de
la feuille se trouve **retrouvé par un chemin indépendant**.

## Les cinq dossiers de rang 4 — rang lu dans le titre

### 511-A — lot 511

Quarante et une routes d API ne sont appelees par personne — 31 % de la surface de donnees.

- chiffre porteur : **41 routes · 31 %**. Definition de « surface de donnees » : **non verifiee par ce lot**.
- titre de section : `## Classement — rang 4`
- rapport : `docs/refactor/validation/SKYLER-LOT-511.md`
- **identifiant `511-A` reconstruit** : le rapport ne le nomme pas dans sa
  section de classement. `AMBIGU` sur l'identifiant, pas sur le rang.

### 512-A — lot 512

`context.headline` est calculee et jamais peinte : la phrase existe, il ne manque qu un consommateur.

- chiffre porteur : **aucun chiffre unique** — le dossier nomme un moteur, un fichier, une fonction et trois routes.
- titre de section : `## Classement — rang 4`
- rapport : `docs/refactor/validation/SKYLER-LOT-512.md`

### 513-A — lot 513

La formulation « Top X % » devient un chiffre faux le jour ou elle est affichee — dossier conditionne a sa propre correction.

- chiffre porteur : **« Top 2 % » en DEMO, n = 20**. Definition ECRITE dans le rapport (environnement et taille d univers cites).
- titre de section : `## Classement — rang 4, et je dis pourquoi pas plus haut`
- rapport : `docs/refactor/validation/SKYLER-LOT-513.md`
- **identifiant `513-A` reconstruit** : le rapport ne le nomme pas dans sa
  section de classement. `AMBIGU` sur l'identifiant, pas sur le rang.

### 518-A — lot 518

La majorite des vues servies n a aucun test qui regarde ce qu elles affichent.

- chiffre porteur : **77 %**. **DEFINITION MANQUANTE** — etabli par le lot 525 : selon ce qu on appelle « regarder le contenu », la valeur va de **57 %** a **94 %**.
- titre de section : `## Classement — 518-A, rang 4`
- rapport : `docs/refactor/validation/SKYLER-LOT-518.md`

### 519-A — lot 519

Trois vues heritees de `/options` sont servies et maintenues sans aucune porte d entree.

- chiffre porteur : **3 vues · 358 lignes · 21 621 octets** (module entier, perimetre cite dans le rapport).
- titre de section : `## Classement — rang 4`
- rapport : `docs/refactor/validation/SKYLER-LOT-519.md`
- **identifiant `519-A` reconstruit** : le rapport ne le nomme pas dans sa
  section de classement. `AMBIGU` sur l'identifiant, pas sur le rang.

## Le relevé complet

| id | lot | rang | fiabilité | titre de section |
|---|---|---|---|---|
| `416-?` | 416 | 1 | **CORPS — fragile** | ## Classement |
| `417-?` | 417 | 1 | **CORPS — fragile** | ## Classement, sans le gonfler |
| `418-?` | 418 | 2 | **CORPS — fragile** · `AMBIGU` | ## Classement — calibré, pas gonflé |
| `422-?` | 422 | 1 | **CORPS — fragile** | ## Classement — famille du 417, pas du 407 |
| `424-?` | 424 | 2 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `425-?` | 425 | 1 | **CORPS — fragile** | ## Classement |
| `427-?` | 427 | 1 | **CORPS — fragile** | ## Classement |
| `428-?` | 428 | 1 | **CORPS — fragile** | ## Classement |
| `432-?` | 432 | 1 | **CORPS — fragile** | ## Classement |
| `433-?` | 433 | 1 | **CORPS — fragile** | ## Classement |
| `434-?` | 434 | 1 | **CORPS — fragile** | ## Classement |
| `435-?` | 435 | 4 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `436-?` | 436 | 3 | **CORPS — fragile** | ## Classement |
| `437-?` | 437 | 1 | **CORPS — fragile** | ## Classement |
| `442-?` | 442 | 1 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `443-?` | 443 | 1 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `445-?` | 445 | 4 | **CORPS — fragile** | ## Classement |
| `446-?` | 446 | 4 | **CORPS — fragile** | ## Classement |
| `447-?` | 447 | 1 | **CORPS — fragile** | ## Classement |
| `449-?` | 449 | 2 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `451-?` | 451 | 4 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `452-?` | 452 | 1 | **CORPS — fragile** · `AMBIGU` | ## Classement |
| `454-?` | 454 | 4 | **CORPS — fragile** | ## Classement |
| `457-?` | 457 | 1 | TITRE | ## Classement — rang 1 |
| `460-?` | 460 | 1 | **CORPS — fragile** · `AMBIGU` | ## Classement coût/risque — mis à jour avec 452, 455, 456, 457, 458 |
| `470-?` | 470 | 1 | **CORPS — fragile** · `AMBIGU` | ## Classement coût/risque — mis à jour avec 461, 463, 464, 466/467, 468, 469 |
| `476-?` | 476 | 1 | TITRE | ## Classement — RANG 1 |
| `477-?` | 477 | 2 | TITRE · `AMBIGU` | ## Classement — RANG 2, et je dis pourquoi pas rang 1 |
| `478-?` | 478 | 2 | TITRE · `AMBIGU` | ## Classement — RANG 2, et l'argument contre le rang 1 est solide |
| `511-?` | 511 | 4 | TITRE | ## Classement — rang 4 |
| `512-A` | 512 | 4 | TITRE | ## Classement — rang 4 |
| `513-?` | 513 | 4 | TITRE · `AMBIGU` | ## Classement — rang 4, et je dis pourquoi pas plus haut |
| `514-?` | 514 | 2 | TITRE · `AMBIGU` | ## Classement — rang 2 |
| `518-A` | 518 | 4 | TITRE | ## Classement — 518-A, rang 4 |
| `519-?` | 519 | 4 | TITRE | ## Classement — rang 4 |

## Ce que ce relevé NE tranche PAS

- **Le total.** Il compte **35** entrées ; la feuille publie « 37 ou 38 ».
  Le crible ne voit que les rapports structurés en `## Classement` : le plus
  ancien relevé est le **lot 416**, donc les dossiers antérieurs, s'il en
  existe, sont **hors de portée**. **L'écart n'est donc pas une
  contradiction, c'est une lacune de couverture.**
- **La répartition.** Seuls **10** rangs sur 35 sont lus dans un titre.
  Les 25 autres peuvent citer un rang **rejeté**.
- **Les identifiants.** 2 entrées seulement sont nommées par leur rapport ;
  les autres portent un identifiant **reconstruit** à partir du numéro de lot.

**Aucune de ces incertitudes n'est résolue ici. Elles sont enregistrées pour
qu'une décision humaine puisse s'appuyer sur autre chose qu'une rumeur.**

---

# Complément du lot 528 — la lacune de couverture, examinée

Le lot 527 signalait **54 rapports de la période couverte mentionnant un
rang sans section `## Classement`**. Ils sont ici examinés un par un.

```text
les 54 cas, classés par forme d'annonce
   INDETERMINE    42
   DOSSIER        8
   CITATION       4
```

## Les huit candidats, VÉRIFIÉS À LA LECTURE

**Trois sur huit ne sont pas des dossiers mais des CITATIONS** : la phrase
« classé rang N » y désigne un **autre lot**. C'est la dérive d'attribution
que le 527 avait corrigée et qu'un crible par phrase refabrique aussitôt.

| lot | verdict après lecture | rang | ce que dit le rapport |
|---|---|---|---|
| 421 | **CANDIDAT** | rang 4 | « Classé rang 4 » dans « Verdict du lot » — annonce propre au rapport. |
| 423 | **CANDIDAT** | rang 4 | rang lu dans « Verdict du lot » ; le verdict est « Négatif sur le produit », donc la portée du dossier est elle-même discutable. |
| 431 | **CANDIDAT** | rang 4 | « Rang 4, **versant recoupement du dossier 386** (rang 1, déjà ouvert) » — un versant, pas nécessairement une entrée neuve. |
| 453 | **CANDIDAT** | rang 4 | « ## Un **sous-produit**, classé rang 4 » — sous-produit du lot, pas son objet principal. |
| 456 | **CANDIDAT** | rang 4 | « je le classe rang 4 en l'état, **à requalifier si un banc l'exécute** » — et le **459 l'a requalifié RANG 2**. |
| 480 | **CITATION** | — | la phrase « classé rang 1 » appartient à un TABLEAU récapitulant les lots 476 et 447. **Pas un dossier du 480.** |
| 483 | **CITATION** | — | « 456 + 459 … DÉJÀ CLASSÉ rang 2 » désigne les lots 456 et 459. **Pas un dossier du 483.** |
| 488 | **CITATION** | — | « le 486 — qui a classé rang 2 » désigne le lot 486. **Pas un dossier du 488.** |

**Aucun des cinq candidats n'est un dossier NEUF sans réserve** : un est un
*versant* d'un dossier existant, un est un *sous-produit*, un a été
**requalifié au rang 2** par un lot ultérieur, un porte un verdict négatif.
**Tous restent `AMBIGU`. Rien n'est arbitré.**

## Une dimension qui manquait au relevé : LES RANGS BOUGENT

Le relevé du 527 est **statique**. Or le lot 480 avait déjà mesuré des
**requalifications** :

```text
459 → 456    rang 4 « par lecture » → RANG 2, établi par exécution          HAUSSE
478 → 407    le dossier fusionné 406+407 classé RANG 2                      BAISSE
479 → 416    rang 1 → rang 3                                                BAISSE
```

Un dossier peut donc changer de rang après coup. **Un relevé qui ignore
cette dimension ne pourra jamais s'accorder avec un compte fait à une
autre date.**

## Ce que devient le total

```text
relevé du 527 (section « ## Classement »)              35
candidats de forme alternative, TOUS AMBIGUS          + 5
citations écartées après lecture                        3
cas restés INDÉTERMINÉS parmi les 54                   42
```

**Le total n'est toujours pas tranché, et il ne le sera pas par un motif.**
La feuille annonce « 37 ou 38 » ; le relevé strict en compte 35 ; cinq
candidats ambigus s'y ajoutent peut-être. **Seule une décision humaine peut
clore ce compte.**


---

# Complément du lot 529 — les chiffres porteurs, VÉRIFIÉS sur le code

| dossier | chiffre porteur | verdict après vérification |
|---|---|---|
| **513-A** | « Top 2 % », DÉMO n = 20 | **CONFIRMÉ au chiffre près** — n = 20 mesuré, minimum observé Top 2 %. **Sa définition était écrite.** |
| **512-A** | phrase calculée, jamais consommée | **CONFIRMÉ** — produite (« Top 43% de l'univers · #1/3 dans Healthcare »), et les 8 occurrences de « headline » dans les octets servis sont **toutes homonymes**. |
| **519-A** | 3 vues · 358 lignes · 21 621 « octets » | **JUSTE, MOT FAUX** — 358 lignes ✓, 3 vues ✓, mais le fichier fait **21808 octets** ; 21 621 est un compte de **CARACTÈRES** (187 d'écart = les accents). |
| **511-A** | 41 / 103 · 39,8 % | **NON REPRODUCTIBLE** — quatre prédicats plausibles donnent 173, 164, 102, 99 routes, **aucun ne rend 103**. |
| **518-A** | 77 % | **ENCADRÉ** 57 %–94 %, établi au lot 525. |

**Deux dossiers sur cinq ont un chiffre exactement vérifiable, et les deux avaient leur définition ÉCRITE.**

## 511-A — la part jamais citée, sous quatre lectures

```text
prédicat                       total   jamais citées   part
toutes GET hors /static         173            89    51.4 %
hors les 9 pages                164            88    53.7 %
/api + feeds                    102            45    44.1 %
/api seul                        99            43    43.4 %
publié au 511                    103            41    39.8 %
```

**La conclusion du 511 tient et se trouve RENFORCÉE** : la part réelle est
partout **supérieure** à celle qu'il a publiée. Le dossier n'était pas
gonflé, il était prudent. **Seul son corpus n'est pas retrouvable.**


---

# Complément du lot 531 — un dossier NEUF : `531-A`, rang 3

| dossier | lot | ce qu il dit | chiffre porteur et DEFINITION |
|---|---|---|---|
| **531-A** | 531 | Deux vues d Opportunites laissent un squelette de chargement **perpetuel** quand la requete echoue. | **2 vues sur 22 mesurees peignent 0 caractere en regime d echec** — definition : le chargeur est execute sous le harnais node v3, `VX.fetch` levant une erreur HTTP 500, et l on compte les caracteres de texte ecrits dans le DOM factice. `renderRadar` et `renderStocks` n ont **ni try ni catch** ; `op-body` est servi avec un `vx-skeleton`. |

**La definition est ECRITE des la publication** — regle 529-B appliquee a
chaud.

## Ce qui borne ce dossier

- il faut une **panne de la requete** pour l atteindre, et `VX.fetch`
  **retente deux fois** avant de lever ;
- en marche normale la vue peint **1 526 caracteres** ;
- **aucun chiffre faux** n est affiche — ce qui l empeche d etre rang 2 ;
- mais **un etat de chargement faux** est montre — ce qui l empeche d etre
  rang 4.

