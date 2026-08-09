# SKYLER LOT 470 — BILAN n°16 (tranche 460 → 469) : la cadence baisse pour la première fois de façon nette — le critère que j'avais posé bascule, et il faut le suivre

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-470` (base : lot 469 fusionné,
c44ef80)

Seizième bilan. Fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. **Une seule mesure fraîche — les MD5 — et elle est dite comme
telle.**

## Ce que la tranche a déposé — mesuré

**Base résolue explicitement AVANT tout chiffre** (leçon 430/440/450/460, cinq
fois payée) :

```text
candidats « lot 459 » dans le journal   1b23377
1b23377  ancêtre de la tête ?           OUI          ← vérifié, pas supposé
base 1b23377 → tête c44ef80             10 commits
```

```text
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +3 047 / −0        (addition pure)

terminal.py + vertex/** touchés               0 fichier
rapports / index / blocs STATUS          10/10, 10/10, 10/10
volume des dix rapports                 114 435 octets
MD5 des 8 pages remesurés                     8/8 identiques   ← mesure fraîche
SW enregistré                           td-shell-v187

depuis 20a917f (lot 399, référence corrigée au 460)
   70 commits · 73 fichiers · 1 HORS docs/ (tests/test_skyler_sweep_x1.py) · 0 PRODUCTION
```

**Aucun octet de production n'a changé depuis le lot 399 — recompté, pas hérité.**

## Une correction de comptes que je publie contre mon propre réveil

L'orientation que j'avais rédigée au 469 annonçait « arrêtés avant publication
**32 → 40** ». **C'est faux sur deux points**, et la chaîne des rapports le dit :

```text
bilan n°15 (lot 460) clôturait à                     26
461 +3 → 29    462 +2 → 31    463 +1 → 32    464 +1 → 33
465 +1 → 34    466 +3 → 37    467 +2 → 39    468 +1 → 40    469 +0 → 40
```

Le point de départ était **26, pas 32**, et l'énumération omettait 465 et 467.
**Mesuré : 26 → 40, soit +14 sur la tranche.** La chaîne lot par lot est
interne­ment cohérente ; c'est mon résumé qui ne l'était pas.

## Ce que les dix lots ont produit

Relu dans la section « Classement » de chaque rapport.

```text
460  BILAN n°15                                                          —
461  dominantRisk « aucun risque » dans 15-25 % · winnerRule type perdu  ✓ rang 2 + 3
462  phrases-seuil : 26/28 concordent — le 461 est un ACCIDENT ISOLÉ     ✗ bornage
463  gex_history journalise la démo 120 j sous « points réels »          ✓ rang 2
464  edge_ledger + 2 journaux sans provenance : le track record affiché  ✓ RANG 1
465  les deux dettes du 464 soldées — 0 nouvel accumulateur              ✗ bornage
466  28 orphelines sur 189 règles, publiées en INTERVALLE [22, 37]       ~ rang 4
467  l'intervalle RÉSOLU à 28 — 9 des 15 étaient des redirections        ✗ bornage
468  19 seuils concordants, 0 divergence neuve · 6 concepts sans loi     ~ rang 4
469  le board sélectionne SOUS le minimum absolu de la Constitution      ✓ rang 3

      1 rang 1 · 2 rang 2 · 2 rang 3 · 2 rang 4
      6 lots sur 10 BORNENT · 1 bilan
```

## Le rendement — et cette fois il baisse franchement

```text
                     rang 1 PAR LOT   rang 1 PAR DOSSIER   DÉFAUTS AFFICHÉS
                                                           (rang 1 + rang 2)
tranche 420 → 429          4                 4                    —
tranche 430 → 439          4                 3                    5
tranche 440 → 449          3                 2                    5
tranche 450 → 459          2                 2                    7
tranche 460 → 469          1                 1                    3      ← −4
```

**Le rang 1 tombe de 2 à 1. Les défauts affichés tombent de 7 à 3.** Les deux
lectures vont dans le même sens pour la première fois depuis le bilan n°12.

Je ne cherche pas d'excuse à ce chiffre. On pourrait dire que la tranche a
consacré **six lots sur dix à borner ou à solder** plutôt qu'à chercher — c'est
vrai, et c'est même sa qualité. Mais **le critère que j'ai posé ne porte pas sur
l'effort, il porte sur le résultat**, et le résultat recule.

## Le critère bascule — et je le suis

Le bilan n°15 avait écrit, textuellement :

> « Le critère posé était : **(b) si et seulement si la cadence des trouvailles
> baisse ; sinon (a)**. […] **Au premier bilan où les défauts affichés
> reculeront, (b) devient la bonne réponse.** »

**Ils reculent : 7 → 3.** Le critère est rempli sans ambiguïté.

**Je recommande donc (b) : un lot « DEVIS ».** Chiffrer le coût de correction
exact des dossiers les moins chers — fichiers, lignes, gardiens à écrire, risque
de régression — **sans rien corriger**, pour rendre la décision humaine possible.

C'est la première fois en sept bilans que la recommandation change. Je le dis
franchement : **elle ne change pas parce que j'ai changé d'avis, elle change
parce que le chiffre que j'avais choisi d'avance a franchi le seuil que j'avais
fixé d'avance.** C'était l'intérêt de poser le critère à l'époque où il donnait
la réponse inverse.

## Le fait de méthode dominant — et il est dérangeant

**Dans huit des neuf lots de mesure, l'instrument était faux au premier jet.**
Et la parade a changé de nature à chaque fois :

```text
461  le CONTRÔLE attrape la cécité         `return'X'` sans espace, 3 corrections
462  la TAILLE trahit le bavardage         186 → 30, tokeniseur + chevrons nus
463  la LECTURE de la liste                88 → 31, « affirmer » ≠ « nommer »
464  la LECTURE encore                     un écrivain qui appende par open()
466  la LECTURE, trois fois               client/serveur confondus
467  le CONTRÔLE LUI-MÊME était faux       il condamnait un classeur juste
468  un CHEMIN DE LECTURE trop court       deux clés déclarées « absentes »
469  une ATTEIGNABILITÉ SUPPOSÉE           et elle était fausse
```

**Treize corrections d'instrument, plus deux erreurs de raisonnement** (465 et
469). La conclusion honnête n'est pas « la boucle s'améliore » — c'est
celle-ci :

**Si l'instrument est faux au premier jet presque à chaque fois, alors tout lot
qui N'A PAS attrapé son instrument est suspect.** Les lots où je n'ai rien
corrigé ne sont pas les plus sûrs ; ce sont ceux dont je ne sais pas s'ils
étaient justes. C'est un argument de plus pour **(b)** : un devis se vérifie en
le lisant, une mesure ne se vérifie qu'en la refaisant.

## L'atteignabilité : ce qu'elle a coûté, ce qu'elle vaut

Elle a tué trois candidats sérieux — « cible 1 » (462), l'alerte de démo (465),
le seuil DTE (468) — **et le 469 a montré que le troisième verdict était FAUX**.

```text
462  « cible 1 »        branche inatteignable   VÉRIFIÉE (un seul producteur)   tient
465  alerte de démo     consommateur non servi  VÉRIFIÉE (URL absente)          tient
468  seuil DTE          « probablement filtré » SUPPOSÉE                        FAUX
```

**Deux sur trois ont été mesurés, un a été supposé — et c'est celui-là qui était
faux.** Le filtre est excellent quand on le mesure et dangereux quand on
l'invoque. C'est la seule erreur de la tranche qui ait atteint la publication.

## Mes comptes, recomptés sur pièces

```text
arrêtés avant publication      26 → 40      +14
publiés puis corrigés           3 →  4       +1   le « probablement inatteignable »
                                                  du 468, corrigé au 469
interprétations retirées        1 →  2       +1   l'équivalence d'échelle du 468,
                                                  retirée au 469
```

**Le +1 de la deuxième ligne est le premier depuis trois tranches**, et il vient
d'une phrase que j'avais **hedgée et non classée**. Le 469 a tranché que cela
comptait quand même. Je maintiens ce jugement : *un lecteur qui repart avec une
croyance fausse a été mal informé, que la phrase ait porté un « probablement »
ou non.*

## Classement coût/risque — mis à jour avec 461, 463, 464, 466/467, 468, 469

Ordre **par coût et risque croissants**. Le rang de gravité est rappelé ; **il ne
dicte pas l'ordre**.

```text
#   dossier                        geste                                      surface       risque
1   457 borne V1 figée             lire d.bounds.max — DÉJÀ REÇU              1 expression  très faible  rang 1
2   455 synthèse pré-trade         ajouter statuses.count(UNKNOWN)            1 ligne       très faible  rang 2
3   461 dominantRisk 15-25 %       comparer à max_stock_weight_pct            1 littéral    très faible  rang 2
4   434 renderAnomalies            copier la garde écrite 20 lignes plus haut 3 lignes JS   très faible
5   427 légende multi-indices      bâtir la légende depuis `sets`             1 ligne JS    très faible
6   428 entonnoir de sélection     accepter les deux vocabulaires             2 lignes JS   très faible
7   437 « Catalyseurs imminents »  retirer `|| Date.now()` (3 pages)          3 lignes JS   très faible
8   456 titre « 200 titres »       dire le plafond, ou lever la troncature    1 chaîne      très faible  rang 2
9   463 gex_history démo           passer la provenance à record()            1 paramètre   faible       rang 2
10  425 « 4 maturités réelles »    compte dynamique `${pts.length}`           2 chaînes     très faible
11  458 classeur catOf             ajouter le type au prédicat (2 sites)      6 lignes JS   faible       rang 2
12  464 ledger sans provenance     passer `demo` à record() — DÉJÀ en portée  3 écrivains   faible       RANG 1
13  447 max pain multi-échéances   filtrer sur l'échéance la plus proche      1 filtre      faible       rang 1
14  432+433 synthèses /portfolio   conditionner sur `allMarked` DÉJÀ CALCULÉ  3 branches    faible
15  442+443 les trois R:R          afficher rr_res + nommer chaque référence  4 rendus      faible
16  452 collision de route         retirer la règle masquée OU lire les clés  1 règle       faible       rang 1
17  469 DTE sous la Constitution   DÉCISION DE PRODUIT — pas un correctif     —             —            rang 3
18  468 six seuils sans loi        DÉCISION DE PRODUIT — pas un correctif     —             —            rang 4
19  466/467 28 orphelines          DÉCISION DE PRODUIT — pas un correctif     —             —            rang 4
```

Trois remarques mesurées :

**Le n°12 est le rang 1 le plus utile du classement.** `DEMO_MODE` est déjà dans
la portée de l'appelant, et `decision_memory` **fait déjà exactement ce qu'il
faut** — il y a un modèle à copier dans le même fichier.

**Les onze premiers ne touchent aucun moteur.**

**Les trois derniers ne sont pas des correctifs** : le DTE court, les six seuils
sans configuration et les 28 routes orphelines demandent qu'on **décide**, pas
qu'on répare. Un devis doit les présenter comme tels.

## Portée de ce bilan

Il mesure ce que la tranche a **déposé** et ce que les dix rapports
**affirment**. Il ne rejoue rien : **si un rapport s'est trompé sur un fait qu'il
présente comme mesuré, ce bilan reprend l'erreur** — et la tranche vient
justement de démontrer que cela arrive.

Le classement des rangs est **attribué par moi-même**. Ce n'est pas une métrique
indépendante, et **le constat de baisse en dépend directement** : si j'avais
classé le DTE du 469 en rang 2 plutôt qu'en rang 3, les défauts affichés
seraient 4 et non 3 — la conclusion tiendrait quand même (4 < 7), mais elle
serait moins nette. Je le dis pour qu'on puisse contester le chiffre en
connaissance de cause.

**La seule mesure fraîche prise ici est celle des MD5 : 8/8 identiques.**

## Où en est la boucle

Soixante-treizième lot court, **seizième bilan**.

La tranche 460-469 est la plus **économe** de toutes : un seul rang 1, mais
**six lots sur dix qui bornent, soldent ou résolvent**. Elle a refermé trois
veines sans laisser une seule dette. Elle a corrigé son propre plafond
(37 → 28), son propre compte d'unités (53 → 12), et **son propre verdict
d'atteignabilité**.

C'est une tranche qui **range** plus qu'elle ne trouve. Et c'est exactement ce
que le critère détecte : **quand le rangement prend le pas sur la trouvaille, il
est temps de présenter la facture.**

**Seizième tranche consécutive sans qu'un seul des défauts prouvés ait été
corrigé.** Le classement en compte désormais **dix-neuf**, dont **onze à moins de
six lignes et sans moteur**, dont **deux rang 1** parmi les cinq premiers.

## Orientation pour le 471

**(b) — LE LOT DEVIS.** Le critère posé au bilan n°15 est rempli : les défauts
affichés reculent de 7 à 3, et le rang 1 de 2 à 1.

Le devis doit chiffrer, **sans rien corriger** : fichier et ligne exacts, nombre
de lignes à changer, gardien à écrire, risque de régression, et — pour les trois
dossiers qui n'en sont pas — **la question à trancher plutôt que le correctif à
appliquer**. Il doit commencer par les cinq premiers du classement, dont deux
rang 1.

**Et je dis ce qui plaide contre**, comme le bilan n°15 l'avait fait dans
l'autre sens : un devis ne mesure rien de neuf, et **quinze bilans de mesure
n'ont pas encore obtenu une seule décision**. Rien ne garantit que le seizième,
même chiffré, en obtienne une. Mais c'est le geste qui manque, et c'est le seul
que la boucle n'a jamais tenté.

Comptes séparés : résultats faux **arrêtés avant publication** **40** ;
**publiés puis corrigés** **4** ; **interprétations retirées** **2**.

**Huit bilans — n°9, n°10, n°11, n°12, n°13, n°14, n°15 et n°16 — attendent une
réponse.**
