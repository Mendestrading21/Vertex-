# SKYLER LOT 522 — Audit de mes propres chiffres, par la MÉTHODE et non par la prose. **Sur 115 bancs, 13 ne reposent que sur un motif textuel — et quatre lots n'ont eu aucune autre mesure.** Recompté par AST, le « copie quasi mot pour mot » du 509 est **PARTIEL** : 54 %, pas 100

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-522` (base : lot 521 fusionné,
`0f561a43`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** — deux lots consécutifs ont montré que mes chiffres issus de motifs
textuels sont faux avec une régularité inquiétante : le **515** en a corrigé
trois (253→38, 82→16, 44→1), le **521** trois autres. **Six chiffres faux en deux
lots, dont un publié.**

La feuille repose sur des chiffres. Si une part d'entre eux vient de greps mal
bornés, c'est la feuille entière qui est fragile.

## L'instrument : ne pas chercher dans la prose

Chercher la réponse dans le **texte** des rapports aurait rejoué exactement le
travers que j'audite. **La méthode d'un chiffre n'est pas dans la phrase qui
l'annonce, elle est dans le SCRIPT qui l'a produit** — et tous mes bancs sont
encore là.

Classement de chaque banc par la nature de sa mesure, lue dans son code :
**AST** (immune aux noms) · **ROUTE** (`test_client`, `url_map`) · **NODE**
(exécution réelle du JS) · **MOTIF** (`grep`, `re.findall` sur des sources).

```text
bancs inventoriés                              115
   purement immunes (aucun motif)               23
   MIXTES (immune + motif)                      31
   reposant UNIQUEMENT sur un motif             13
```

Les 13 se répartissent sur huit lots. **Quatre de ces lots ont un banc immune
qui double la mesure** (483, 484, 507, 510). **Quatre n'en ont aucun** :

```text
490 · 491 · 500 · 509      ← le motif y est la SEULE mesure
```

Les **490** et **500** sont des **bilans** : leurs chiffres portent sur la boucle
(nombre de lots, de dossiers), pas sur le dépôt. Restent **deux affirmations
vérifiables sur le code**.

## Le chiffre du 509, recompté par AST

Le 509 affirmait que `_strat_tilt` est **« une copie quasi mot pour mot »** de
`climate` — affirmation qui a **doublé la portée du dossier 508-A**.

Comparaison par **squelette d'AST** (suite des types de nœuds, insensible aux
renommages) et par **constantes**, avec deux témoins :

```text
IDENTITÉ   climate vs climate      squelette 100 %   constantes 100 %
NÉGATIF    climate vs _pct_rank    squelette  27 %   constantes  12 %
────────────────────────────────────────────────────────────────────
MESURE     climate vs _strat_tilt  squelette  54 %   constantes  69 %
                                   texte brut 46 %
           climate      205 nœuds ·  811 caractères
           _strat_tilt  231 nœuds · 1594 caractères
```

**Verdict : PARTIEL.** L'échelle discrimine (54 % contre 27 % pour le témoin
négatif), mais on est loin d'une copie.

**Ce qui tient** : **34 constantes communes sur 54** — les mêmes seuils, les
mêmes étiquettes `FAVORABLE` / `NEUTRE` / `DANGEREUX`, les mêmes couleurs, les
mêmes clés `above50` / `breadth` / `calme` / `TREND` / `RISK-ON`. **Le défaut du
508-A est bien dupliqué**, et sa portée doublée reste juste.

**Ce qui ne tient pas** : « quasi mot pour mot ». `_strat_tilt` fait **presque le
double** de `climate` et ajoute ses propres playbooks et ses propres phrases
d'orientation. C'est un **noyau de scoring partagé à l'intérieur d'une fonction
plus large**, pas une copie.

**Le dossier survit, le qualificatif était gonflé.**

**Publiés puis corrigés : 15 → 16.**

## Le chiffre du 491 n'est pas re-vérifiable

Le 491 publiait « **7 barèmes** nommés mais jamais tracés ». Sa sortie de banc
n'a pas été conservée. Et **rejouer un banc à motif ne confirmerait rien** — la
règle 503 le dit : *un banc qui reproduit un chiffre publié n'est pas une
confirmation.* Le vérifier demanderait un instrument immune neuf.

**Je le laisse ouvert plutôt que de le blanchir par une re-exécution qui ne
prouverait rien.** Dette nommée.

## Le second contrôle — ma classification est trop grossière

Elle porte sur des **scripts**, pas sur des **chiffres**. Or un script peut
mélanger les méthodes : `l514_arrondis.py` est un crible **AST**, mais son triage
en familles F1/F2/F3 passe par des **regex sur le code**.

```text
scripts MIXTES (immune + motif)                          31
   dont appliquant une regex à du CODE SOURCE             3
lots concernés par au moins un script mixte              16
   484 · 486 · 494 · 506 · 508 · 510 · 511 · 512 · 514
   515 · 516 · 517 · 518 · 519 · 520 · 521
```

**Le « quatre lots » est donc une BORNE BASSE de l'exposition**, pas son compte.
Un chiffre issu d'une regex peut vivre dans un lot par ailleurs bien outillé —
c'est précisément ce qui est arrivé au 514.

## Ce que le dépôt — et la boucle — font bien

- **23 bancs sur 115 sont purement immunes** (AST, route, node), sans aucun
  motif. Ce n'est pas la majorité, mais ce n'est pas marginal.
- **Quatre des huit lots à motif ont un banc immune qui double la mesure.** Le
  réflexe du second contrôle a donc joué la moitié du temps, avant même que la
  règle 515-A ne soit écrite.
- La correction du 509 **ne casse pas son dossier** : le 508-A reste doublé,
  parce que ce qui compte — les constantes du scoring — est bien partagé.

## Portée — ce que ce lot NE dit PAS

- **Je n'ai recompté qu'UN chiffre.** Les 490, 500 (bilans) et 491 (non
  re-vérifiable) restent en l'état. Ce lot ne blanchit rien et ne condamne rien
  d'autre.
- La classification est **par script** et **par présence de motif**, pas par
  chiffre publié. Elle ne dit pas quel chiffre est faux, seulement lesquels sont
  **exposés**.
- Un chiffre issu d'un motif **n'est pas faux par principe** — la règle 515-C
  vaut ici aussi. Le 509 en est l'illustration : sa mesure était **inexacte dans
  le qualificatif, juste dans la conclusion**.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

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
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0**.

Aucun dossier — mais ce lot fait ce qu'aucun autre n'avait fait : il **retourne
l'exigence de preuve contre les preuves elles-mêmes**. Le résultat est mesuré et
il est nuancé : sur 115 bancs, **13 sont exposés et 4 lots n'ont eu aucun
recours** ; sur le seul chiffre recomptable, **le dossier tient et le
qualificatif était gonflé**.

Je n'incrémente **pas** le compteur d'arrêts avant publication : je n'ai arrêté
aucun résultat faux ce lot-ci, j'en ai **corrigé un déjà publié**. Gonfler ce
compteur serait exactement le travers que le lot dénonce.

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **le « 7 barèmes » du 491, non re-vérifiable sans
instrument neuf** (dette neuve) ; **mesurer les 23 routes — outil prêt, en
attente d'un GO** ; **le français construit en JavaScript** ; **l'assemblage
entre fonctions** ; **la condition `k ≤ 5` sur un scan réel** ; **le compte des
rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 121 (inchangé)** ;
**publiés puis corrigés 16 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
