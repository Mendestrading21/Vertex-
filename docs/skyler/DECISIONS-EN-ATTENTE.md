# SKYLER V2 — LA FILE D'ATTENTE, UNE LIGNE PAR DÉCISION

> Produit par `tools/relever_dossiers_skyler.py`, qui applique les
> règles du lot 527 à **tous** les rapports — le relevé d'origine
> s'arrêtait à son époque et ne détaillait que cinq dossiers.
> **Rien n'est arbitré ici** : chaque ligne attend un mot.

> ⚠ **Ce compte ne retrouve pas celui du 527** : sur son propre
> périmètre (lots ≤ 527), cet outil relève **44** dossiers là où le 527
> en annonçait **35**. Un seul nombre coïncide, et c'est le plus
> contrôlé — **5 dossiers de rang 4 fiables**. Le désaccord n'est pas
> une surprise : `DOSSIERS.md` existe parce que les comptes publiés se
> contredisaient déjà. Ce relevé ne tranche pas ce différend ; il dit
> ses règles, et elles sont lisibles dans l'outil.

Choix possibles, un par ligne : **corriger** · **chiffrer** ·
**abandonner** · **garder en observation**.

Un identifiant `NNN-?` veut dire que le rapport **ne se nomme pas** dans
sa section de classement : le dossier existe, son étiquette n'a jamais
été écrite. C'est un fait sur les rapports, pas une lacune de l'outil.

| rang | dossiers |
| --- | --- |
| 1 | 22 |
| 2 | 10 |
| 3 | 3 |
| 4 | 10 |
| **total** | **45** |


**Trois qualités de rang, et elles ne se valent pas.**

| qualité | ce que ça veut dire | dossiers |
| --- | --- | --- |
| `TITRE` | le rang est écrit dans le titre de section | 16 |
| `AMORCE` | le rang est **affirmé** en tête de section (`**Rang N**`) | 8 |
| `CORPS` | le rang n'apparaît que plus loin — il peut désigner un rang **rejeté** | 21 |

Les **24** premiers (`TITRE` + `AMORCE`) sont ceux sur lesquels une décision peut se prendre sans rouvrir le rapport. Les **21** derniers demandent une lecture avant d'être tranchés.

## Rang 1

| dossier | fiabilité | ce que le rapport dit | décision |
| --- | --- | --- | --- |
| [`416-?`](../refactor/validation/SKYLER-LOT-416.md) | AMORCE | SKYLER LOT 416 — Un titre qui n'a pas bougé affiche « RSI 100 », et le gardien qui dit « neut… |  |
| [`417-?`](../refactor/validation/SKYLER-LOT-417.md) | AMORCE | SKYLER LOT 417 — « Rendement +20 séances » : le N affiché n'est pas le N du calcul |  |
| [`422-?`](../refactor/validation/SKYLER-LOT-422.md) | CORPS | SKYLER LOT 422 — Le R:R affiché repose sur un mouvement attendu que le moteur s'invente, et c… |  |
| [`425-?`](../refactor/validation/SKYLER-LOT-425.md) | AMORCE | SKYLER LOT 425 — « 4 maturités réelles » : le compte est écrit en dur, la courbe se trace dès… |  |
| [`427-?`](../refactor/validation/SKYLER-LOT-427.md) | AMORCE | SKYLER LOT 427 — La légende annonce quatre indices, le graphique en trace trois : les couleur… |  |
| [`428-?`](../refactor/validation/SKYLER-LOT-428.md) | AMORCE | SKYLER LOT 428 — L'entonnoir du scan est plat par construction : il cherche des verdicts en f… |  |
| [`430-?`](../refactor/validation/SKYLER-LOT-430.md) | TITRE | SKYLER LOT 430 — BILAN n°12 (tranche 420 → 429) : cinq trouvailles affichées, zéro octet de p… |  |
| [`432-?`](../refactor/validation/SKYLER-LOT-432.md) | AMORCE | SKYLER LOT 432 — « Aucune décision urgente — laisser courir les thèses intactes », dit la car… |  |
| [`433-?`](../refactor/validation/SKYLER-LOT-433.md) | AMORCE | SKYLER LOT 433 — Le portefeuille calcule `allMarked`, s'en sert pour une classe CSS, et l'ign… |  |
| [`434-?`](../refactor/validation/SKYLER-LOT-434.md) | AMORCE | SKYLER LOT 434 — « Aucune anomalie détectée sur le scan courant » quand il n'y a pas de scan … |  |
| [`437-?`](../refactor/validation/SKYLER-LOT-437.md) | CORPS | SKYLER LOT 437 — Le test de consommation ne se généralise pas (trois instruments, trois contr… |  |
| [`442-?`](../refactor/validation/SKYLER-LOT-442.md) | CORPS | SKYLER LOT 442 — « R:R structurel 3 » : le seul R:R affiché sur la page d'analyse vaut 3 sur … |  |
| [`443-?`](../refactor/validation/SKYLER-LOT-443.md) | CORPS | SKYLER LOT 443 — Trois R:R différents sur la même page, et le seul honnête n'apparaît que pou… |  |
| [`447-?`](../refactor/validation/SKYLER-LOT-447.md) | CORPS | SKYLER LOT 447 — « Max pain à J-3 de la plus proche échéance » : l'aimant annoncé est celui d… |  |
| [`450-?`](../refactor/validation/SKYLER-LOT-450.md) | CORPS | SKYLER LOT 450 — BILAN n°14 (tranche 440 → 449) : le tri par affichage paie, la cadence des r… |  |
| [`452-?`](../refactor/validation/SKYLER-LOT-452.md) | CORPS | SKYLER LOT 452 — 85 modules sur 299 sont injoignables depuis `terminal.py`, et le balayage to… |  |
| [`457-?`](../refactor/validation/SKYLER-LOT-457.md) | TITRE | SKYLER LOT 457 — « Actions 10 / 10 — complet, remplacement obligatoire » : le portefeuille af… |  |
| [`460-?`](../refactor/validation/SKYLER-LOT-460.md) | CORPS | SKYLER LOT 460 — BILAN n°15 (tranche 450 → 459) : sept défauts affichés au lieu de cinq, mais… |  |
| [`464-?`](../refactor/validation/SKYLER-LOT-464.md) | TITRE | SKYLER LOT 464 — Le ledger qui produit le track record affiché ne peut pas distinguer un verd… |  |
| [`470-?`](../refactor/validation/SKYLER-LOT-470.md) | CORPS | SKYLER LOT 470 — BILAN n°16 (tranche 460 → 469) : la cadence baisse pour la première fois de … |  |
| [`476-?`](../refactor/validation/SKYLER-LOT-476.md) | TITRE | SKYLER LOT 476 — Le devis clos, la mesure reprend : le 417 est CLASSÉ RANG 1 et chiffré à 5 l… |  |
| [`484-?`](../refactor/validation/SKYLER-LOT-484.md) | CORPS | SKYLER LOT 484 — Les 7 fractions que le 456 avait nommées sans les tracer : deux sont saines,… |  |

## Rang 2

| dossier | fiabilité | ce que le rapport dit | décision |
| --- | --- | --- | --- |
| [`418-?`](../refactor/validation/SKYLER-LOT-418.md) | CORPS | SKYLER LOT 418 — Le multiplicateur d'option vaut 100 partout, et le seul contrôle qui le surv… |  |
| [`424-?`](../refactor/validation/SKYLER-LOT-424.md) | CORPS | SKYLER LOT 424 — « Thèse INTACT, confiance 0.0 » : le titre médian reçoit un verdict sans une… |  |
| [`449-?`](../refactor/validation/SKYLER-LOT-449.md) | CORPS | SKYLER LOT 449 — La veine `reason` refermée : 7 phrases sur 7 tranchées, le rang 2 du 448 pas… |  |
| [`458-?`](../refactor/validation/SKYLER-LOT-458.md) | TITRE | SKYLER LOT 458 — Les littéraux de l'interface contre la Constitution : l'échelle de convictio… |  |
| [`461-?`](../refactor/validation/SKYLER-LOT-461.md) | TITRE | SKYLER LOT 461 — La carte « Risque dominant » de `/portfolio` déclare « Aucun risque critique… |  |
| [`477-?`](../refactor/validation/SKYLER-LOT-477.md) | TITRE | SKYLER LOT 477 — Le 378 classé RANG 2 : deux replis `0` atteignent bien l'entonnoir de `/oppo… |  |
| [`478-?`](../refactor/validation/SKYLER-LOT-478.md) | TITRE | SKYLER LOT 478 — 406 et 407 sont UN SEUL dossier, classé RANG 2 : deux clés du contrat de syn… |  |
| [`482-?`](../refactor/validation/SKYLER-LOT-482.md) | CORPS | SKYLER LOT 482 — Retour au produit : QUATRE des dix « dossiers en attente » ne sont pas des d… |  |
| [`486-A`](../refactor/validation/SKYLER-LOT-486.md) | CORPS | SKYLER LOT 486 — Le test du 485 appliqué à TOUS les barèmes : le score /40 est affiché sur DE… |  |
| [`514-?`](../refactor/validation/SKYLER-LOT-514.md) | TITRE | SKYLER LOT 514 — Le schéma du 513-A a une COPIE, et elle est **SERVIE**. Sur la fiche d'un ti… |  |

## Rang 3

| dossier | fiabilité | ce que le rapport dit | décision |
| --- | --- | --- | --- |
| [`436-?`](../refactor/validation/SKYLER-LOT-436.md) | CORPS | SKYLER LOT 436 — `/api/command` sert dix champs, le produit en lit deux : 95 % du payload ne … |  |
| [`469-?`](../refactor/validation/SKYLER-LOT-469.md) | TITRE | SKYLER LOT 469 — Les deux dettes du 468 soldées, et l'une CONTRE ma propre inclinaison : le b… |  |
| [`531-A`](../refactor/validation/SKYLER-LOT-531.md) | TITRE | SKYLER LOT 531 — **531-A, rang 3 : deux vues d'Opportunités laissent un squelette de chargeme… |  |

## Rang 4

| dossier | fiabilité | ce que le rapport dit | décision |
| --- | --- | --- | --- |
| [`435-?`](../refactor/validation/SKYLER-LOT-435.md) | CORPS | SKYLER LOT 435 — La décision du jour est calculée sur zéro titre, et personne ne la lit : je … |  |
| [`445-?`](../refactor/validation/SKYLER-LOT-445.md) | CORPS | SKYLER LOT 445 — J'ouvre les phrases que le serveur écrit, et elles sont justes : 15 accords … |  |
| [`446-?`](../refactor/validation/SKYLER-LOT-446.md) | CORPS | SKYLER LOT 446 — « Clôture séance +5 » compte les séances OBSERVÉES, pas les séances de march… |  |
| [`451-?`](../refactor/validation/SKYLER-LOT-451.md) | CORPS | SKYLER LOT 451 — Les quatre phrases `source` ne sont jamais produites : `build_surface` n'a a… |  |
| [`454-?`](../refactor/validation/SKYLER-LOT-454.md) | CORPS | SKYLER LOT 454 — Les six phrases `action` sont des ordres d'entrée chiffrés, calculés à chaqu… |  |
| [`511-?`](../refactor/validation/SKYLER-LOT-511.md) | TITRE | SKYLER LOT 511 — Instrument NEUF : « producteur sans consommateur ». **Quarante et une routes… |  |
| [`512-A`](../refactor/validation/SKYLER-LOT-512.md) | TITRE | SKYLER LOT 512 — Les 41 routes muettes, lues une par une. **Le brief se trompait : `/api/comi… |  |
| [`513-?`](../refactor/validation/SKYLER-LOT-513.md) | TITRE | SKYLER LOT 513 — La règle 507-A retournée contre mon propre dossier d'hier. **512-A survit : … |  |
| [`518-A`](../refactor/validation/SKYLER-LOT-518.md) | TITRE | SKYLER LOT 518 — La dette la plus ancienne, enfin mesurée : ce ne sont pas « 29 vues sans emp… |  |
| [`519-?`](../refactor/validation/SKYLER-LOT-519.md) | TITRE | SKYLER LOT 519 — Les 7 vues sans test **fonctionnent toutes**. Mais **3 vues servies sur 35 n… |  |

