# SKYLER — LOT 595

## Ce que le lot établit

**La règle 594-C est fausse, et je la retire.** Elle affirmait qu'un piège à
deux volets — l'un qualitatif, l'autre un classement précis — produit un MIXTE
« par construction », les volets qualitatifs passant presque toujours et les
précis échouant presque toujours.

Mesuré sur les volets réellement publiés :

| classe *(critère fixé d'avance)* | confirmés | total tranchés | taux |
| --- | --- | --- | --- |
| **QUALITATIF** | 2 | 5 | **40 %** |
| **PRÉCIS** | 7 | 14 | **50 %** |

**Les volets précis sont confirmés PLUS souvent que les qualitatifs.** La règle
prédisait l'inverse. Et les deux taux sont à portée d'un tirage à pile ou face.

**Interprétations retirées : 13 → 14.** Le rapport 594 n'est pas réécrit — les
corrections sont en append (591-B).

## Le choix (ooo)

Le 594 a accusé ma propre méthode de fabriquer ses MIXTE. **Une accusation n'est
pas une mesure.** Elle était testable ; elle ne tient pas.

## La prémisse du brief était fausse — 9 lots, pas 31

Le brief demandait de relire « pour chaque lot de 564 à 594 » le piège écrit
d'avance. **Cette machinerie n'existe pas sur 31 lots.**

| critère | rapports sur 31 |
| --- | --- |
| mentionnent « piège » dans le corps | **26** |
| ont un **titre** de section « piège » | **18** |
| ont un **tableau** volet/verdict | **9** |
| ne mentionnent jamais le mot | **5** — 566, 567, 570, 571, 572 |

Les trois comptes ne s'additionnent pas (546-A). **594-C portait sur une forme
d'écriture qui a neuf occurrences** : 585→589 et 591→594.

## Le classement, fait à l'aveugle

Le problème central était nommé avant de commencer : **c'est moi qui classe, et
je connais déjà les verdicts.** La parade : un critère **syntaxique**, fixé dans
`l595_piege.md` avant d'avoir ouvert un seul rapport, appliqué à la **cellule
gauche seule** — le programme ne lit jamais la cellule verdict pour décider.

> **PRÉCIS** si l'attente contient un nombre (chiffres, « des dizaines / des
> centaines / la moitié / tous / aucun »), un superlatif (« le plus », « la
> plus », « majoritairement », « surtout »), ou un nom de code entre backticks.
> **QUALITATIF** sinon.

**29 volets extraits · 19 tranchés · 10 non tranchés** (6 verdicts hors
vocabulaire — « DÉCISIF », « respecté », « A PAYÉ » — et 4 lignes « global »).
**Comptés, jamais répartis au jugé** (588-A).

## La parade échoue, et c'est le résultat le plus solide du lot

J'avais promis de publier les désaccords entre le critère et la lecture. Sur les
**5** volets que le critère range en QUALITATIF :

| lot | attente | lecture | pourquoi |
| --- | --- | --- | --- |
| 587 | « la famille BORNE TECHNIQUE **domine largement** » | **PRÉCIS** | revendication de rang |
| 588 | « la **GÉOMÉTRIE domine** » | **PRÉCIS** | revendication de rang |
| 589 | « **la plupart** sont de l'arithmétique de dessin » | **PRÉCIS** | revendication de proportion |
| 591 | « une poignée, **moins de dix** » | **PRÉCIS** | un nombre, écrit en lettres |
| 593 | « **au moins un** autre gardien a un écart » | QUALITATIF | existentiel faible — accord |

**Quatre désaccords sur cinq.** Le critère ignore « domine », « la plupart » et
les nombres écrits en toutes lettres — trois formes de précision qu'aucune de
mes trois catégories ne capture.

**Après lecture, la classe QUALITATIF compte UN membre, contre 18 précis.**

## Le verdict réel : NON MESURABLE, puis RÉFUTÉ

**Comparer deux classes dont l'une a un seul membre n'a pas de sens.** Le
verdict « NON MESURABLE » était nommé d'avance dans le piège, précisément pour
que je ne puisse pas m'y dérober.

Ce qui reste mesurable est plus intéressant que ce que je cherchais : **je
n'écris quasiment pas de volets qualitatifs.** Dix-huit attentes sur dix-neuf
sont des affirmations précises. **La prémisse de 594-C — que mes pièges
mélangent un volet large et un volet précis — est fausse sur mes propres
textes.**

Sur les volets précis, seuls assez nombreux pour être lus : **7 confirmés sur
14**. Pas « presque toujours réfutés ». **594-C est réfutée par les deux bouts :
sa prémisse et sa prédiction.**

## Le piège de ce lot — et la série de MIXTE s'arrête

| volet | verdict |
| --- | --- |
| **(a)** « les volets qualitatifs sont majoritairement confirmés » | **RÉFUTÉ** — 40 %, et l'effectif tombe à 1 après lecture |
| **(b)** « les volets précis sont majoritairement réfutés » | **RÉFUTÉ** — 50 %, un tirage à pile ou face |
| **global** | **RÉFUTÉ** |

**Ce n'est pas un MIXTE.** Après quatre d'affilée, le cinquième est un refus
net — sur le lot même qui testait l'affirmation « le MIXTE est fabriqué par
construction ». **Si la fabrication était structurelle, elle aurait dû produire
un cinquième MIXTE ici.** Elle ne l'a pas fait.

## L'arrêt du lot — mon détecteur cherchait le mauvais mot

Mon premier relevé annonçait **4 tableaux sur 31**. Il exigeait le mot `volet`
dans l'en-tête. **La lecture montre que les lots 585→589 écrivent
`| piège | verdict |`.** Le compte réel est **9**.

**C'est la troisième fois d'affilée qu'un critère syntaxique trop étroit me
trompe** — 591 (le chemin `docs/` littéral), 594 (mon propre bilan), 595. La
règle 591-A existe et je la cite à chaque lot ; **la citer ne suffit pas à
l'appliquer.**

Le banc fautif `l595_corps.py` est **conservé tel quel**, avec son « 4 / 31 ».

**Arrêtés avant publication : 220 → 221 (+1).**

## Second contrôle (481) — les lots antérieurs à 564

Fenêtre de **même taille**, 533→563, mesurée au même critère :

| fenêtre | corps | titre | tableau |
| --- | --- | --- | --- |
| **533 → 563** *(avant la règle 564)* | **2** | **0** | **0** |
| **564 → 594** | **26** | **18** | **9** |

Dates de naissance, cherchées et non supposées : première mention dans un corps
**lot 537** · premier titre de section **lot 568** · premier tableau
**lot 585**.

**Mon attente est confirmée : on ne peut pas classer les volets d'avant, parce
qu'il n'y en a pas.** L'instrument mesure donc **la date de naissance d'une
forme d'écriture**, pas une propriété du dépôt. C'est la limite la plus dure de
tout le lot.

## Recouvrement avec le lot 590 (589-B)

Le 590 a mesuré des pièges sur les bornes **574→589**. **Mon périmètre en
compte 9, le sien 16 — deux définitions.** Le mien exige un *tableau* de volets ;
le sien comptait des *sections* de piège, tableau ou non. **Les deux totaux ne
sont ni additionnés ni soustraits** (546-A) ; le recouvrement se lit sur les lots
communs, il ne se calcule pas depuis les totaux.

## Ce que le lot n'établit pas

- **Si j'écris mes pièges pour qu'ils soient à moitié vrais.** C'est une
  question d'intention, comme celle du 593 sur `assert 'GO' in idx`. **Les
  fréquences ne répondent pas aux intentions** — je ne prétends pas y répondre.
- Qu'un taux de 50 % soit bon ou mauvais : **il n'y a pas de référence externe**.
- Que ces 19 volets tranchés soient représentatifs : **dix-neuf, sur neuf
  lots**. Refuser d'en tirer une loi est la seule conduite tenable (590-C).
- Que les 10 volets non tranchés seraient tombés d'un côté ou de l'autre.

## Limites déclarées

- **La parade syntaxique est fausse 4 fois sur 5** sur la classe qu'elle isole.
  Je la publie avec ses erreurs plutôt que de la régler après coup — tout
  ajustement du critère après avoir vu les verdicts serait un réglage a
  posteriori.
- La lecture qui corrige la parade est **une lecture**, portée par un tableau,
  pas un programme (583-A).
- « 9 lots portant un tableau » vient d'un motif d'en-tête ; un lot pourrait
  publier des verdicts par volet sous une forme que ce motif ne voit pas.
  **Je ne prouve pas l'exhaustivité.**
- Les rapports 564→594 ont été **lus, jamais modifiés** — pas même une coquille
  (591-B).

## Règles neuves

- **595-A — UNE RÈGLE NÉE D'UN SEUL LOT DOIT ÊTRE MESURÉE AVANT D'ÊTRE CITÉE.**
  594-C a été énoncée comme une loi et reprise dans un index ; elle a tenu un
  lot. Le coût de la vérifier était d'un lot.
- **595-B — CITER 591-A NE SUFFIT PAS À L'APPLIQUER.** Trois lots d'affilée, un
  critère syntaxique trop étroit m'a trompé alors que la règle contre ce piège
  était écrite en tête de chaque brief. **Une règle connue n'est pas une règle
  tenue** ; seule la calibration l'attrape.
- **595-C — QUAND UNE CLASSE TOMBE À UN MEMBRE, LE VERDICT EST « NON
  MESURABLE », PAS UN POURCENTAGE.** Nommer ce verdict *avant* la mesure est ce
  qui empêche de le contourner ensuite.

## Ce que le dépôt fait bien

- **Les pièges sont écrits avant la mesure et publiés avec leur verdict**, y
  compris quand ils tombent : sur 19 volets tranchés, **10 sont des réfutations
  de mes propres attentes**, écrites noir sur blanc.
- **La forme s'est durcie toute seule** : mention libre au 537, titre de section
  au 568, tableau à verdicts au 585. Personne ne l'a imposée.
- **Les contre-pièges portent leur numéro de règle** (585-B, 587-A, 588-C…) :
  on peut retracer d'où vient chaque garde-fou.
- **Aucun rapport n'a été retouché** pour se donner raison — c'est ce qui rend
  cette mesure possible.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucun rapport
  corrigé** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 595) **vides**

## Comptes

- Arrêtés avant publication : **221 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14 (+1 — la règle 594-C)**
