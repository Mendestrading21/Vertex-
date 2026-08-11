# SKYLER LOT 440 — BILAN n°13 (tranche 430 → 439) : quatre trouvailles de rang 1 pour la deuxième tranche d'affilée, quatorze instruments jetés, et un chiffre-titre que je dois corriger moi-même

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-440` (base : lot 439 fusionné,
d400bf2)

Treizième bilan. Fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert, aucun nouveau point de contrôle. Une seule mesure fraîche a été
prise — les MD5 — et elle est dite comme telle.

## Ce que la tranche a déposé — mesuré

```text
base 1ac8446 (lot 429 fusionné) → tête d400bf2 (lot 439 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 133 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 430→439 présents                    10 / 10
lignes d'index 430→439                       10 / 10
blocs STATUS par lot 430→439                 10 / 10
volume des dix rapports                  80 011 octets
```

**La base a été résolue explicitement** (leçon du 430). Ma première tentative
prenait `e62fecb` comme base — mais `e62fecb` **est** le commit du lot 430, si
bien que l'intervalle ne couvrait que 431→439, **neuf commits**. Corrigé avant
publication : la base d'une tranche 430-439 est le lot **429** fusionné.

Contrôle refait sur toute la période depuis le lot 399 (`29f4435..d400bf2`) :
**1 fichier hors `docs/`** — `tests/test_skyler_sweep_x1.py`, lot 401 — et
**0 fichier de production**. La formulation substituée au 430 tient toujours :
**aucun octet de production n'a changé depuis le lot 399.**

## Ce que les dix lots ont produit

```text
430  BILAN n°12 + correction d'une affirmation que je répétais           —
431  modeOf ne peut jamais rendre « Live » — J'ANNULE MON PROPRE RANG 1  ✗ rang 4
432  priorityAction range l'INCONNU avec le SAIN                         ✓ rang 1
433  bornage AGGRAVANT — les trois synthèses de /portfolio tombent       ✓ rang 1
434  renderAnomalies sans la garde écrite VINGT LIGNES PLUS HAUT         ✓ rang 1
435  la décision du jour, calculée sur zéro titre — et jamais lue        ~ rang 4 (+ rang 2)
436  /api/command : 2 champs lus sur 10, et la suite défend le reste     ~ rang 3
437  « Catalyseurs imminents » se déclare fraîche « à l'instant », TOUJOURS ✓ rang 1
438  bornage NÉGATIF — six contrats rompus, six faux positifs            ✗
439  trois pages ouvertes, aucun défaut nouveau, une métrique abandonnée ✗

      4 trouvailles de rang 1 · 1 de rang 2 · 1 de rang 3 · 2 de rang 4
      3 bornages (1 aggravant, 2 négatifs) · 1 annulation de soi-même · 1 bilan
```

## Le fait nouveau de la tranche : quatorze instruments jetés en six lots

C'est la statistique que le 439 demandait de regarder en face. Le détail, par
lot, tel que les rapports l'écrivent :

```text
430   git diff comparant la tête à elle-même (base vide)                   1
434   détecteur de garde v1 (page entière) puis v2 (mauvaise fonction)     2
435   motif sans DOTALL → « 0 appel » là où il y en a 16                   1
437   passe 1 (motif large) · passe 2 (0/4 invraisemblable) · passe 3 (bouillie)  3
438   trois lignes fausses issues d'une collision de noms de payloads      3
439   compteur de contrat de carte, v1 → v4, métrique abandonnée           4
                                                                        ─────
                                                                          14
```

**Tous arrêtés avant publication**, par trois contrôles seulement : **témoin
positif** (l'instrument mord-il là où je sais déjà qu'il doit mordre ?),
**invraisemblance** (ce résultat est-il trop gros pour être vrai ?), **lecture de
la sortie brute** (que dit le comptage littéral ?).

### Le chiffre-titre lui-même n'est pas homogène — et je le corrige

En le reprenant pièce par pièce, l'unité change en cours de route. Sur les lots
437 et 439, l'unité comptée est une **version d'instrument écartée**. Sur le 438,
c'est une **ligne fausse produite par un seul et même instrument**. Les deux
conventions ne donnent pas le même total :

```text
par VERSION D'INSTRUMENT écartée      430:1  434:2  435:1  437:3  438:1  439:4  = 12
par RÉSULTAT FAUX produit             430:1  434:2  435:1  437:3  438:3  439:4  = 14
```

**Le « quatorze » que le 439 a publié — et que j'ai repris — mélange les deux.**
Il n'est faux dans aucune des deux conventions, il est simplement **inconstant**.
Convention retenue pour la suite : **résultat faux produit**, donc **14**, et
c'est dit.

C'est exactement la règle que la boucle applique aux moteurs du produit,
appliquée à sa propre comptabilité : *ne jamais publier comme un chiffre un total
dont les lignes ne se comptent pas de la même façon* (437).

## Durcissement, ou rendement décroissant ? — les deux lectures, puis la réponse

**Lecture « rendement décroissant »** : quatorze instruments jetés en six lots,
c'est plus d'effort dépensé à se contrôler qu'à mesurer le produit. Deux des trois
derniers lots (438, 439) ne rendent **aucun défaut nouveau**, et le 439 finit sur
un aveu — *aucun taux de couverture n'est annoncé*. Le coût par trouvaille
monterait, et la veine serait en train de s'épuiser.

**Lecture « méthode qui se durcit »** : les quatorze ont **tous** été arrêtés
**avant** publication, par des contrôles qui coûtent quelques secondes chacun.
Aucun résultat faux n'est entré dans un rapport. Et les questions posées ont
changé de nature : jusqu'au 433, la boucle lisait **un fichier, une fonction** ;
à partir du 434 elle balaie **3 829 722 octets servis** à la recherche de motifs.
Un balayage de corpus casse plus souvent qu'une lecture de fonction — c'est
attendu, pas dégradé.

### Ce qui tranche : le rendement, lui, n'a pas bougé

```text
tranche 420 → 429     4 trouvailles de rang 1 sur 10 lots
tranche 430 → 439     4 trouvailles de rang 1 sur 10 lots
```

**Identique.** Et les quatre de cette tranche sont, comme celles de la
précédente, **prouvées sur les octets servis** — dont une (437) affichée sur
**trois pages** à la fois, ce que la tranche précédente n'avait pas.

**Réponse : durcissement, pas rendement décroissant.** Le nombre d'instruments
jetés a monté parce que **la portée des questions a monté**, pas parce que les
trouvailles se raréfient — leur cadence est strictement la même.

### Deux réserves, que je ne cache pas

**(1) Le « quatorze en six lots » est en partie un artefact de comptage.** La
boucle ne journalisait pas systématiquement ses instruments écartés avant le 434 ;
elle a commencé à les compter à ce moment-là. On ne conclut pas à une **tendance**
à partir d'une série qui commence quand on se met à compter. Des instruments
fautifs, il y en avait avant — le 414, le 415 et le 429 en portent chacun un — mais
je **n'ai pas** de recomptage rétrospectif à coût égal, et je ne le fabrique pas.

**(2) Cette lecture juge la boucle sur ce qu'elle TROUVE, pas sur ce qu'elle
CHANGE.** Sur ce second critère, le rendement est **nul par construction depuis
treize bilans** : aucun octet de production touché.

## Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles.** Les lots 435 à 439
  mesurent tous **sur le scan vide du démarrage** — état réel mais unique. Le 438
  l'a payé : deux de ses six faux positifs venaient de là.
- **Aucun navigateur ouvert** de toute la tranche ; les rendus SVG ne sont pas
  exécutés en pixels.
- **Le vivier reste très peu ouvert** : 118 affirmations recensées, 47 phrases
  rassurantes triées au 433, et les **35 affirmations de `/options` sont
  recensées, non vérifiées** (439). Les phrases construites dynamiquement
  échappent toujours au recensement — zone d'ombre inchangée depuis le 427.
- **Cinq routes sur huit restent non conclues** au test de consommation (437), et
  je n'en publie aucun taux.
- **Aucun taux de couverture du contrat de carte** (439) : la métrique elle-même
  est mal définie, et c'est un aveu, pas une omission.

### Une limite du bilan n°12 qui, elle, est levée

Le n°12 listait parmi ses lacunes : *« MD5 des 8 pages non remesurés depuis les
lots 390/396 : leur constance est une inférence, pas une mesure fraîche. »* Les
neuf rapports 431→439 les remesurent chacun, et **je viens de les remesurer une
fois de plus pour ce bilan : 8/8 identiques**. La constance des huit pages est
désormais **une mesure**, pas une inférence.

## Classement coût/risque — mis à jour avec 432+433, 434 et 437

Ordre **par coût et risque croissants**, comme au 430. Le rang de gravité est
rappelé à part, il ne dicte pas l'ordre.

```text
#  dossier                          geste                                      surface        risque
1  434 renderAnomalies              copier la garde écrite 20 lignes plus haut 3 lignes JS    très faible
2  427 légende multi-indices        bâtir la légende depuis `sets`             1 ligne JS     très faible
3  428 entonnoir de sélection       accepter les deux vocabulaires             2 lignes JS    très faible
4  437 « Catalyseurs imminents »    retirer `|| Date.now()` (3 pages)          3 lignes JS    très faible
5  425 « 4 maturités réelles »      compte dynamique `${pts.length}`           2 chaînes      très faible
6  432+433 synthèses /portfolio     conditionner sur `allMarked` DÉJÀ CALCULÉ  3 branches     faible
7  424 thesis_health                UNKNOWN quand les 2 listes sont vides      1 branche      faible
8  422 expected-move muet           l'ajouter à la liste de limites            1 chaîne       faible
```

Trois remarques sur cette liste, toutes mesurées dans les rapports :

**Les six premiers ne touchent aucun moteur.** Ils vivent dans **quatre fichiers
de page** — `markets_page.py` (2, 3, 5), `opportunities_page.py` (1), les trois
sites de 4 (`briefing.py`, `markets_page.py`, `opportunities_page.py`),
`portfolio_page.py` (6). Un seul lot, un seul bump de service worker, une seule
preuve navigateur suffiraient aux six.

**Le n°1 a son propre modèle dans son propre fichier** : la garde manquante à
`renderAnomalies` est écrite en toutes lettres vingt lignes plus haut, dans
`renderRadar`. C'est la correction la moins risquée de toute la liste.

**Le n°6 n'invente rien non plus** : `allMarked` est déjà calculé dans
`portfolio_page.py` — il sert une couleur, jamais une phrase. Il coûte plus cher
que les autres parce qu'il touche **trois** synthèses, pas parce qu'il demande un
calcul.

Les dossiers plus lourds (406/407/408/409/411, 388, 417, 416, 436) ne sont **pas**
classés ici : ils demandent une **décision de produit**, pas une correction.

**Aucun GO n'est demandé par ce classement, et rien n'est engagé.**

## Portée de ce bilan

Il mesure ce que la tranche a **déposé dans le dépôt** et ce que les dix rapports
**affirment**. Il ne rejoue aucune trouvaille : si un rapport s'est trompé sur un
fait qu'il présente comme mesuré, ce bilan reprend l'erreur. La seule mesure
fraîche prise ici est celle des MD5.

La comparaison de rendement entre les deux tranches porte sur le **nombre de
trouvailles de rang 1**, un classement que **j'attribue moi-même** — ce n'est pas
une métrique indépendante, et le 431 montre qu'elle bouge (j'y ai annulé mon
propre rang 1).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure et
  après chaque bloc lancé depuis le scratchpad.
- **MD5 des 8 pages remesurés pour ce bilan : 8/8 identiques** aux références des
  lots 390/396.
- **Aucun fichier de production touché** — seuls les trois documents du bilan.
  Pas de bump. SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Quarante-troisième lot court, **treizième bilan**.

La tranche 430-439 égale la précédente en trouvailles affichées et la dépasse en
**discipline d'instrument** : quatorze résultats faux arrêtés avant d'entrer dans
un rapport, et un chiffre-titre corrigé dans ce bilan même. C'est une méthode qui
se durcit.

C'est aussi la treizième tranche à se terminer sans qu'un seul des défauts
prouvés — huit désormais classés, dont six à moins de dix lignes et sans moteur —
ait été corrigé.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
