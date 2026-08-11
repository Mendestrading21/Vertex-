# SKYLER LOT 519 — Les 7 vues sans test **fonctionnent toutes**. Mais **3 vues servies sur 35 ne sont liées depuis aucune barre d'onglets** — trois écrans complets, câblés, au contenu **entièrement distinct**, qu'on n'atteint qu'en tapant l'URL

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-519` (base : lot 518 fusionné,
`01c7c958`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)** — la suite directe du dossier publié la veille. Le 518 a mesuré une
**absence de garde**, pas un contenu : il a établi que sept vues non-défaut
répondent 200 sans qu'aucun test ne les nomme. Mais **répondre 200 n'est pas
afficher quelque chose**, exactement comme « requêtée » n'était pas « gardée ».

## Le premier résultat : rien n'est cassé

Ces pages sont un squelette serveur hydraté par du JavaScript ; mesurer le HTML
seul serait naïf. J'ai donc extrait le **bloc propre** de chaque vue (sa
différence avec la vue par défaut), recensé ses **conteneurs**, et vérifié dans
le **JS servi** qu'un chargeur les vise.

```text
vues examinées                                  7
au bloc propre VIDE                             0
sans aucun conteneur                            0
ORPHELINES (ni aiguillage ni conteneur visé)    0
```

**Les sept sont câblées.** Aucune ne montre un squelette perpétuel. Le 518
mesurait une exposition ; le 519 confirme qu'elle est, aujourd'hui, **théorique**.

Je dois signaler que **ma calibration de variété a échoué** : n'ayant trouvé
aucune vue orpheline parmi les sept, je ne peux pas démontrer que l'instrument en
aurait repéré une. Les calibrations positive (`/markets?view=breadth`, dont le
508 avait exécuté le chargeur) et négative (bloc propre vide sur une vue
fabriquée) passent, mais la discrimination reste **non démontrée sur ce
lot-ci**. Je le publie plutôt que de le taire (règle 509-A).

## Le second contrôle a corrigé un chiffre que j'allais publier

Mon premier banc annonçait **7 conteneurs « non visés par le JS »**, dont quatre
pour `/options?view=overview`. J'allais en faire des conteneurs orphelins.

```text
conteneurs « non visés » annoncés            7
dont ENVELOPPES à jumeau `…-body` visé       7
ORPHELINS RÉELS                              0
```

Chaque `vx-opt-hero` a un `vx-opt-hero-body` que le JS remplit. **Le motif est
« carte enveloppe + corps hydraté » — du code normal.** Mon crible comparait le
mauvais niveau de l'arbre. Cousin du piège 511-C.

**Arrêtés avant publication : 115 → 116.**

## Le dossier — 519-A

Le second contrôle posait une autre question : **« branchée » n'est pas
« atteignable »**. Une vue peut avoir son chargeur et n'être liée depuis aucune
barre d'onglets. Mesuré sur les **35 vues servies** :

```text
vues liées depuis la barre d'onglets de leur page      32
vues liées depuis AUCUNE barre d'onglets                3
   /options?view=overview
   /options?view=radar
   /options?view=scenarios
```

Ce sont **exactement** les trois `_LEGACY_VIEWS` d'`options_intel_page`. Le
contrôle est interne et solide : sur **la même page**, les six vues de `_VIEWS`
ressortent liées et les trois de `_LEGACY_VIEWS` non — même mécanisme, même
gabarit, résultat opposé.

**Et ce ne sont pas des doublons.** Comparaison des conteneurs de chaque vue
legacy avec ceux des six vues visibles :

```text
legacy overview    8 conteneurs · plus proche visible : Jaccard 0,00 · communs AUCUN
legacy radar       2 conteneurs · plus proche visible : Jaccard 0,00 · communs AUCUN
legacy scenarios   6 conteneurs · plus proche visible : Jaccard 0,00 · communs AUCUN
```

**Zéro conteneur partagé.** Trois écrans complets, câblés, hydratés, au contenu
**entièrement distinct** de ce que la navigation propose — et qu'aucun lien ne
mène.

C'est la famille du **512-A** (produire sans consommateur), transposée du niveau
ROUTE au niveau **VUE**. Et comme au 512, la distinction décisive tombe du côté
**occasion manquée** plutôt que déchet : un doublon serait du gâchis, du contenu
unique inatteignable est autre chose.

## Ce que les deux lots disent ensemble

**Deux des trois vues inatteignables font partie des sept vues sans test.** Les
écrans que personne ne teste sont en bonne part les écrans que personne ne peut
atteindre — ce qui est cohérent, et ce qui **réduit la portée du 518-A** : sur ses
sept vues, deux ne sont de toute façon pas accessibles par la navigation.

Les cinq autres, elles, sont **liées, câblées et sans test** : c'est là que
l'exposition du 518-A reste entière.

## Classement — rang 4

Rien de faux n'est montré : les trois vues rendent un contenu propre et correct,
répondent 200, et le repli fonctionne. **Ce n'est ni un défaut d'affichage ni un
défaut de calcul — c'est une surface de produit sans porte d'entrée.**

Ce qui le distingue d'une curiosité : ces trois vues sont **maintenues** — code
présent dans `options_intel_page.py` (358 lignes, 21 621 octets pour le module
entier), servies à chaque requête, hydratées par du JS chargé sur la page.

Correction pressentie, non engagée : **décider entre les LIER et les retirer**.
Le contenu étant unique, les lier est au moins aussi défendable que les retirer.
**Aucun GO, rien n'est engagé, et NE RIEN SUPPRIMER** — le 511 et le 512 ont déjà
posé cette règle, et le 519 lui donne un troisième cas.

## Ce que le dépôt fait bien, mesuré

- **Les sept vues sans test fonctionnent** : bloc propre non vide, conteneurs
  présents, chargeurs branchés, zéro orphelin réel.
- **Le motif enveloppe / corps est propre et systématique** — c'est lui qui a
  fait échouer mon crible, pas l'inverse.
- **32 vues sur 35 sont correctement liées** depuis leur propre barre d'onglets.
- Les trois legacy sont **explicitement rangées** dans un registre nommé
  `_LEGACY_VIEWS` : le dépôt sait qu'elles sont d'un autre âge, il ne les cache
  pas.

## Portée — ce que ce lot NE dit PAS

- **« Câblée » n'est pas « peinte ».** J'ai vérifié qu'un chargeur vise les
  conteneurs ; je n'ai pas exécuté les chargeurs des sept vues. Le 508 l'a fait
  pour une vue, pas pour celles-ci.
- **Ma calibration de variété a échoué** (aucune orpheline parmi les sept) : la
  capacité du crible à repérer une vue non câblée reste **non démontrée ici**.
- Le test « liée » cherche `?view=X` **littéral** dans le HTML de la page. Un
  onglet construit entièrement en JavaScript lui échapperait — mais les 32 autres
  vues ressortent bien liées par ce même test, ce qui borne le risque.
- Mesuré en **DÉMO**, sur les 20 titres du scan.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les trois bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4**.

Deux lots de suite sur l'axe du **produit servi**, deux dossiers. Après trois
lots passés à réparer mes instruments, le changement d'axe tient ses promesses —
modestement : deux rangs 4, rien de faux à l'écran, mais deux constats que
personne n'avait mesurés.

Ce lot a aussi la vertu de **borner celui d'hier** : sur les sept vues du 518-A,
deux ne sont pas atteignables par la navigation, donc l'exposition réelle porte
sur cinq. Un lot qui rétrécit sa propre thèse de la veille en vaut un qui en
ouvre une (règle 507-C).

Feuille : **37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 · **cinq**
rang 4**.

Dettes nommées restantes : **mesurer le contenu des 23 routes non appelées**
(dette du 512, ouverte depuis huit lots — désormais la plus ancienne) ;
**exécuter les chargeurs des vues sans test** (dette neuve — « câblée » n'est pas
« peinte ») ; **le français construit en JavaScript** ; **l'assemblage entre
fonctions** ; **la condition `k ≤ 5` sur un scan réel** ; **recribler les chiffres
publiés par motif textuel** ; **le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 116 (+1)** ; publiés
puis corrigés **15** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
