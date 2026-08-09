# SKYLER LOT 430 — BILAN n°12 (tranche 420 → 429) : cinq trouvailles affichées, zéro octet de production touché, et une correction sur ma propre affirmation

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-430` (base : lot 429 fusionné,
1ac8446)

Douzième bilan. Fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert, aucun nouveau point de contrôle.

## Ce que la tranche a déposé — mesuré

```text
base 0676d78 (lot 419 fusionné) → tête 1ac8446 (lot 429 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 231 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 420→429 présents                    10 / 10
lignes d'index 420→429                       10 / 10
blocs STATUS par lot                          9  (+ le BILAN n°11, qui EST le lot 420)
volume des dix rapports                  78 145 octets
```

## Une correction sur une affirmation que je répétais

La consigne de boucle porte depuis plusieurs lots la phrase *« la production n'a
pas bougé depuis le lot 399 »*. **Je l'ai vérifiée, et elle est vraie sur le
fond mais fausse à la lettre.**

```text
lot 399 (29f4435) → tête (1ac8446)         31 commits
fichiers HORS docs/ modifiés                1   ← tests/test_skyler_sweep_x1.py
fichiers de PRODUCTION modifiés             0   (terminal.py + vertex/**)
```

Le seul fichier non documentaire touché est un **test**, corrigé au **lot 401**
(un gardien qui passait selon l'ordre d'exécution : `if v is None: pop`
confondait « valeur `None` » et « clé absente », ce qui supprimait `market_ctx`
du `scan_state` partagé). **Aucun octet de production n'a changé depuis le lot
399** — c'est la formulation exacte, et je la substitue à l'ancienne.

**Et il faut dire comment je l'ai su.** Ma première commande de vérification a
rendu « aucun fichier », ce qui confirmait commodément l'affirmation. Elle était
**fausse** : le `git log --grep` n'avait rien trouvé, la variable de base était
vide, et `git diff ..HEAD` comparait la tête à elle-même. **Une commande peut
rendre une ligne propre, alignée et fausse** (leçon du lot 415) — le contrôle
a été refait avec le commit résolu explicitement.

## Ce que les dix lots ont produit

```text
420  BILAN n°11 (tranche 410 → 419)
421  scoring.compose — hypothèse d'inversion RÉFUTÉE par la mesure          ✗
422  scenario_pricer — repli MUET de l'expected-move, absent des limites     ✓ rang 1
423  committee — « $None (structure) », chaîne remontée → inatteignable      ✗ rang 4
424  thesis_health — INTACT avec confiance 0.0, affichage NON PROUVÉ         ~ rang 2
425  « 4 maturités réelles » en dur, courbe tracée dès 2 points              ✓ rang 1
426  bornage — 6 affirmations de méthode sur 6 EXACTES                       ✗
427  vivier 17 → 118 ; légende multi-indices sur liste fixe                  ✓ rang 1
428  entonnoir de sélection PLAT PAR CONSTRUCTION                            ✓ rang 1
429  bornage — trois vocabulaires légitimes, 13 porteurs exacts sur 14       ✗

              4 trouvailles de rang 1 · 1 de rang 2 · 1 de rang 4
              3 bornages négatifs · 1 hypothèse réfutée · 1 bilan
```

**Quatre nouveaux dossiers de rang 1 en dix lots** (422, 425, 427, 428), tous
**prouvés sur les octets servis**, aucun engagé.

## Ce que la tranche a changé dans la manière de mesurer

Trois acquis, et ils comptent plus que le compte de trouvailles.

**1. Partir de l'écran (425).** Trois lots partis du moteur (421, 423, 424)
avaient buté sur des branches inatteignables ou un affichage non prouvé.
Renverser l'ordre — extraire une phrase **réellement rendue**, puis remonter au
code — a produit une trouvaille en une seule mesure, et n'a plus cessé.

**2. Exécuter les octets servis (427, 428).** Extraire une fonction du marquage
servi par appariement d'accolades, stuber ses dépendances et l'exécuter sous
Node : ce n'est ni une lecture ni une transcription. C'est ce qui a permis
d'affirmer « 60 → 60 → 60 → 0 quel que soit le marché » comme une **mesure**.

**3. Le recensement lui-même peut être la limite (427).** Le bornage du 426
concluait « exception, pas symptôme » — c'était juste, mais il désignait autre
chose : le vivier était **sept fois plus grand** que ce qui avait été recensé
(17 → 118). En l'élargissant, la première affirmation ouverte a mordu.

## Ce que les dix rapports NE prouvent PAS

À dire clairement, parce que c'est ce qui manque :

- **Aucune trouvaille n'a été constatée sur des données réelles.** Le scan est
  vide au démarrage, le board d'options aussi, aucun payload persisté ne porte de
  `rows` ni d'`indices`. Les défauts des 425, 427 et 428 sont démontrés **par
  construction ou par exécution sur des payloads fabriqués**, avec leur porte
  d'entrée établie dans le code — pas observés à l'écran d'un vrai scan.
- **Aucun navigateur n'a été ouvert.** Les rendus SVG n'ont pas été exécutés ;
  je mesure les **valeurs passées** aux graphiques, pas leurs pixels.
- **116 des 118 affirmations rendues restent non vérifiées**, et le recensement
  lui-même exclut toujours les phrases construites dynamiquement.
- **Les MD5 des 8 pages n'ont pas été remesurés** depuis les lots 390 et 396 :
  leur constance est une **inférence** (aucun fichier de production touché
  depuis), pas une mesure fraîche.
- Le « 13 sur 14 » du lot 429 ne vaut que pour les vocabulaires en majuscules
  comparés explicitement : 44 couples en minuscules et 15 porteurs lus par table
  n'ont pas été confrontés.

## La question, posée franchement

La boucle mesure de mieux en mieux et **ne corrige rien**. Depuis le lot 399,
zéro octet de production a changé. Les bilans n°9, n°10 et n°11 posaient déjà
cette question — **s'y reporter, elle n'est pas reformulée ici**. Ce qui a changé
depuis le n°11 et qui compte : il y avait deux chiffres faux affichés, il y en a
maintenant **quatre familles de défauts prouvés à l'écran** (422, 425, 427, 428),
dont deux qui **égarent activement la lecture** — une carte qui explique comment
lire une platitude qu'elle fabrique, une légende qui nomme une courbe par le nom
d'une autre.

Les options restent : **(a)** continuer à mesurer, **(b)** obtenir un GO sur les
dossiers de rang 1 les moins coûteux, **(c)** arrêter la boucle et attendre.

### Classement coût/risque des corrections de rang 1 les moins chères

Ordre de coût croissant. **Rien n'est engagé, aucun GO n'est demandé implicitement.**

```text
#  dossier                          geste                                     surface        risque
1  427 légende multi-indices        bâtir la légende depuis `sets`            1 ligne JS     très faible
                                    au lieu de `wanted`                       markets_page
2  428 entonnoir de sélection       accepter les deux vocabulaires, comme     2 lignes JS    très faible
                                    le fait déjà /opportunities               markets_page
3  425 « 4 maturités réelles »      compte dynamique `${pts.length}` +        2 chaînes      très faible
                                    panneau sans nombre fixe                  markets_page
4  424 thesis_health INTACT         rendre UNKNOWN quand pos_ev et neg_ev     1 branche      faible
                                    sont tous deux vides                      Python
5  422 expected-move muet           ajouter le repli à la liste de limites    1 chaîne +     faible
                                    que la carte affiche déjà                 1 étiquette
```

Les trois premiers touchent **le même fichier** (`vertex/ui/pages/markets_page.py`)
et **aucun moteur** : un seul lot, un seul bump de service worker, une seule
preuve navigateur. Les deux suivants touchent un moteur chacun et demandent un
gardien.

Les dossiers plus lourds (406/407/408/409/411 sur la carte d'équité, 388 points
MSFT, 417 dénominateurs `track_record`, 416 RSI 100) **ne sont pas classés ici** :
ils demandent une décision de produit, pas une correction de deux lignes.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier de production touché** — `git status` vide de bout en bout. Pas
  de preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-troisième lot court, **douzième bilan**. La tranche 420-429 est la plus
productive en défauts **affichés** depuis le début de la veille — et la seule
dont **toutes** les trouvailles ont été prouvées sur le marquage servi.

Elle est aussi la douzième à se terminer sans qu'un seul de ces défauts ait été
corrigé.

**Quatre bilans — n°9, n°10, n°11 et n°12 — attendent une réponse.**
