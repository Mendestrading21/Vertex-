# SKYLER LOT 500 — BILAN n°18 de la tranche 490-499 : la boucle a TRIPLÉ son taux d'auto-arrêt et DIVISÉ PAR DEUX sa production de dossiers — et la moitié de ce qu'elle arrête, ce sont ses PROPRES instruments

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-500` (base : lot 499 fusionné,
`96f827e9`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**
Bilan **sur pièces** : les dix rapports relus, les chiffres vérifiés dans le
dépôt et dans `git log`, **aucune trouvaille rejouée**. Seule mesure fraîche :
les MD5.

## Calibration — et elle a arrêté ce lot DEUX FOIS

Série objective : le compteur « arrêtés avant publication » que chaque rapport
porte. Deux réponses connues, sortie programmée.

```text
(A) lot 490 → 55        (B) lot 499 → 76
```

**Premier passage : ÉCHEC.** Mon extracteur rendait `None` pour le 490 et `76`
pour le 499. Diagnostic : le motif était **sensible à la casse** et le 490 écrit
« **A**rrêtés avant publication : 54 → 55 » en début de phrase.

**Deuxième passage : ÉCHEC ENCORE.** Corrigé pour la casse, il rendait `55` puis
**`1`** pour le 499 — parce que je prenais le **dernier** nombre de la fenêtre, et
que le 499 écrit « 76 **(+1)** ». Les rapports emploient **deux formes**
(`54 → 55` et `76 (+1)`) et il faut lire l'une par la flèche, l'autre par le
premier nombre.

Troisième version : **les deux témoins passent.** C'est la **quatrième fois de la
tranche** qu'une calibration arrête un lot avant qu'il ne publie (493, 496, 498,
et celui-ci).

**Je compte cela pour UN arrêt, pas deux** : les deux échecs portent sur le même
extracteur et le même objet. Sans eux, **toute la série de ce bilan aurait été
fausse**. **Arrêtés avant publication : 76 → 77.**

## 1. Les chiffres de la tranche, vérifiés

```text
suite            2864 passed / 0 skipped — déclaré par les DIX rapports
service worker   td-shell-v187 — sur les DIX
MD5 des 8 pages  8/8 déclaré par les dix, et remesuré 8/8 aujourd'hui
production       ZÉRO fichier hors docs/ dans les dix commits — vérifié dans
                 `git show --name-only`, pas seulement déclaré
gardiens         ZÉRO ajouté
PR               #522 (490) → #531 (499)
```

## 2. Rendement : DEUX dossiers en dix lots

Taille de la feuille, lue **dans les lignes d'index** (leçon 490 — le chiffre
n'est pas dans le corps des rapports) :

```text
480-482 : 20   ·   483 : 21   ·   484-485 : 23   ·   486-489 : 24
491-494 : 24   ·   495 : 25   ·   496-499 : 26
```

**Tranche 480-489 : 20 → 24, soit +4. Tranche 490-499 : 24 → 26, soit +2.**
La production de dossiers a été **divisée par deux**.

Les deux neufs : **495-A** (rang 1 — le moteur exécutif décide en aveugle sur
quatre entrées) et **496-A** (rang 2 — « R:R visé » affiche un score /100). Plus
une **requalification** : le **442** est plus large qu'écrit (496).

## 3. Auto-correction : de +3 à +1

```text
publiés puis corrigés    480 : 7  →  489 : 10   (+3)
                         490 : —  →  499 : 11   (+1, au lot 494)
```

**Le taux a baissé des deux tiers.** Je refuse de le présenter comme une
amélioration nette : la tranche a aussi publié **moins de chiffres neufs** — deux
dossiers au lieu de quatre. **Moins publier, c'est moins avoir à corriger.** Le
seul point solide est que la correction unique du 494 portait sur **une ligne
d'index**, pas sur une trouvaille.

## 4. Faux arrêtés : +22, et la MOITIÉ sont mes propres instruments

```text
479 : 45   ·   489 : 54   ·   499 : 76
tranche 480-489 :  +9        tranche 490-499 :  +22
```

**Le taux d'auto-arrêt a été multiplié par 2,4.** C'est le chiffre le plus
frappant de la tranche — et le plus ambigu, parce qu'il ne dit pas *ce qui* est
arrêté. Classement des **22**, à la lecture de chaque rapport :

```text
DÉFAILLANCE DE MON INSTRUMENT (le banc mesurait autre chose)     11
   490 mauvais document · 491 sonde mal étiquetée · 492 branche DATA_INSUFFICIENT
   492 scan AST faux · 493 agrégation par nom nu · 493 mauvaise clé
   493 branches neutres · 496 artefact de grille · 497 blob non lu
   497 retour anticipé · 498 témoin positif invalide

ERREUR DE LECTURE DU RÉSULTAT (la mesure était juste, pas ma conclusion) 10
   491 homonyme · 494 mot nu · 494 homonyme · 494 vocabulaire « orphelin »
   495 liste brute de 33 · 495 homonyme · 497 homonyme · 497 condition
   d'affichage · 498 fragment partagé · 499 repli qui marche

SONDE DANGEREUSE ÉVITÉE                                            1
   495 navigateur sur /analysis → route réseau sortante
```

**ONZE sur VINGT-DEUX — exactement la moitié — ne sont pas des faits sur le
produit : ce sont des pannes de mes propres bancs.** C'est la réponse à la
question la plus dure de la tranche, et elle n'est pas flatteuse. Un compteur qui
monte n'est pas en soi une vertu : **il mesure autant ma rigueur que ma
maladresse.**

## 5. Les règles de calibration ont-elles servi ? Mesuré : un tiers

Sur les **onze** défaillances d'instrument, combien ont été attrapées par une
**calibration écrite d'avance**, et combien par la simple lecture de la sortie ?

```text
attrapées par une CALIBRATION   3   (493 témoin `rr` · 496 témoin de validité
                                     · 498 témoin positif)   + celle-ci = 4
attrapées EN LISANT la sortie   8   (490, 491, 492 ×2, 493 ×2, 497 ×2)
```

**La calibration attrape environ un tiers des pannes de banc.** Les deux autres
tiers viennent de la lecture attentive de la sortie — c'est-à-dire de la
discipline, pas du dispositif.

Et le **497** est le contre-exemple utile : il a subi **trois** pannes de banc et
sa calibration **n'en a attrapé aucune**, parce qu'elle testait la variété de la
sortie et non le chargement de l'entrée. C'est de là qu'est sortie la règle
« **témoin de CHARGE avant témoin de VARIÉTÉ** », et le 498 puis ce lot-ci l'ont
appliquée.

## 6. Fermer ou découvrir ? La boucle ferme

```text
veines CLOSES        4   493 producteur constant · 496 barèmes
                         498 PAGE_* · 499 symétrie ROW/DÉTAIL
veine OUVERTE        1   495 la clé lue sur le mauvais objet
lots de BORNAGE      5   490 bilan · 491 nettoyage de liste · 492 traçage
                         494 second /40 · 497 bornage du 495-A
```

**Quatre fermetures pour une ouverture.** La tranche a passé l'essentiel de son
temps à **délimiter ce qui n'est pas un défaut** — et c'est un travail réel : le
496 a montré qu'un barème est sain, le 498 que 61,1 % de `terminal.py` ne sert
personne, le 499 que la famille du 495 tient sur **un seul objet**. Mais une
boucle qui ferme quatre fois plus qu'elle n'ouvre **approche la fin de ce qu'elle
peut trouver seule**, et c'est déjà ce que disait le bilan n°17.

## 7. Le second contrôle — les chiffres de CE RÉVEIL, que le bilan exclurait

Un bilan lit les rapports ; il ne vérifie pas son propre brief. Quatre chiffres
du réveil passés à la mesure :

| chiffre du réveil | mesuré |
|---|---|
| « la feuille est passée de 24 à 26 » | **CONFIRMÉ** |
| « +21 en dix lots » | **FAUX : +22.** Le réveil part de 55, la valeur du 490, qui inclut déjà l'arrêt du 490 lui-même. La tranche produit **54 → 76**. |
| « PR #521 (489) → #531 (499) » | étiquetage **correct**, mais la plage propre à la tranche est **#522 → #531** |
| « 301 fichiers de test » | **300** fichiers `test_*.py` ; **301** `.py` en comptant `conftest.py`. Vrai sous la seconde lecture, à préciser. |

**Quatrième réveil consécutif porteur d'une imprécision** (480, 482, 490, 495,
500). La règle « le brief est une source comme une autre » **se paie encore**, et
c'est le second contrôle qui la fait payer.

## 8. Le stock, et la question que je ne tranche pas

```text
26 dossiers   quinze rang 1 · neuf rang 2 (dont un conditionnel) · trois rang 3
dix lots de travail A-J     ·  7 à chiffrer  ·  7 arbitrages humains
17+ observations non classées  ·  8 rangs relatifs non re-vérifiés
un devis de purge : 4 369 lignes, 19 constantes, 12 pages, zéro consommateur
corrections engagées : 0   ·   gardiens ajoutés : 0   ·   octets servis modifiés : 0
```

**Vingt lots — deux tranches complètes — sans qu'un seul octet servi change.**
C'est la discipline tenue, et c'est aussi l'état du problème : la boucle produit
un stock qu'elle ne peut pas consommer.

**Est-ce soutenable ? Je pose la question et je n'y réponds pas à la place de
l'utilisateur**, comme le bilan n°17. Ce que je peux dire de neuf : la valeur du
stock ne se dégrade pas — les dossiers sont reproductibles, calibrés, et deux
d'entre eux ont été **resserrés** par des lots ultérieurs plutôt qu'abandonnés
(495-A borné au 497, 442 requalifié au 496). **Le stock vieillit bien. Il reste
inutilisable sans une décision.**

## Portée

- **Aucune trouvaille rejouée.** Les verdicts des dix lots sont **cités**, pas
  re-mesurés ; ce bilan établit ce que la tranche **dit avoir fait**, plus les
  chiffres transverses que j'ai vérifiés au dépôt et dans `git log`.
- Le classement des 22 arrêts en « instrument / lecture / sonde » est **mon
  jugement**, pas une mesure. Un autre lecteur pourrait déplacer deux ou trois
  cas — **il ne pourrait pas faire tomber la moitié en dessous du tiers**.
- Le compteur d'arrêts est **incrémenté par moi**. Il est fidèle si je l'ai
  toujours incrémenté à bon escient ; **je n'ai pas audité les 22 occurrences
  une à une**, j'ai vérifié deux valeurs connues en calibration et lu les
  vingt-deux libellés.
- Les MD5 sont la seule mesure fraîche. **Aucun navigateur.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché** — et vérifié **sur pièces** pour les dix
  lots de la tranche, pas seulement déclaré. Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où va la boucle

La tranche 480-489 avait produit **trois défauts et une méthode**. La tranche
490-499 produit **deux défauts et une méthode plus dure** — calibration à témoin
de charge, témoin du même genre, espion d'exécution. Les instruments se sont
améliorés au rythme exact où les trouvailles se sont raréfiées, ce qui est
logique : **plus il reste peu à trouver, plus il faut d'exactitude pour ne pas
inventer.**

Le fait que je retiens, parce qu'il est mesuré et qu'il me concerne : **la moitié
de ce que j'arrête, c'est moi.** Onze pannes de banc en dix lots. La discipline
tient — aucune n'a été publiée — mais elle coûte, et elle dit où va le temps.

Comptes séparés : résultats faux **arrêtés avant publication 77 (+1)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
