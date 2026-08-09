# SKYLER LOT 415 — 288 identifiants servis, aucun doublon ; le gardien n'en surveille que 3 pages sur 8

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-415` (base : lot 414 fusionné,
f2ad8f8)

Deux éléments qui portent le même `id`, c'est un défaut silencieux :
`getElementById` rend **le premier**. Le second n'est jamais mis à jour — carte
figée, aucune erreur en console, aucune alerte. Le trader voit une donnée qui ne
bouge plus et n'a aucun moyen de le savoir.

**Aucun code, aucun gardien, aucun test.**

## Trois classes de doublon, trois mesures

Périmètre : les 8 pages et leurs 26 scripts demandés au serveur en mémoire
(méthode du 413). Les `<script>` sont **retirés du marquage** avant comptage :
une chaîne dans du JS n'est pas un nœud.

**1. Doublon dans le marquage servi**

```text
identifiants d'éléments dans le marquage des 8 pages   288
pages avec au moins un doublon                           0
```

**2. Collision entre le marquage et un gabarit JS de la même page**

```text
candidats                                                1   → #op-compare, /opportunities
```

Ouvert. Les deux porteurs sont dans des **vues mutuellement exclusives** :
`renderRadar()` (ligne 240) émet `<div id="op-compare">`, `renderOptions()`
(ligne 509) émet `<button id="op-compare">`, et **les deux écrasent le même
`$('op-body').innerHTML`**. Ils ne coexistent jamais. Mieux : `renderCompare()`
n'a **qu'un seul appelant**, ligne 256, à l'intérieur de `renderRadar` — la
fonction qui vient de créer le `div`. **Aucune conséquence.**

*Note de rang 4* : l'`id` du bouton n'est cherché par personne (son handler est
un `onclick` inline). C'est un nom en double sans effet aujourd'hui, pas un
défaut.

**3. Identifiant littéral émis à l'intérieur d'une répétition**

C'est la forme qui fabrique vraiment des doublons : un `id` fixe dans un gabarit
passé à `.map()` donne N nœuds identiques.

```text
identifiants littéraux fabriqués par le JS servi       113
   dont à l'intérieur d'un .map()/.forEach()             1   → « strat-pf- »
```

Ouvert : `'<div id="strat-pf-' + i + '"'`, et la relecture ligne 499 fait
`getElementById('strat-pf-' + i)`. L'identifiant est **interpolé avec l'indice
de boucle** — unique par élément, code correct. Mon extracteur tronquait au `+`,
ce qui l'a fait passer pour un littéral.

**Zéro doublon réel, sur les trois classes.**

## L'instrument, deux fois

**Une heuristique de proximité qui ressemblait à un résultat.** Premier
détecteur : « un `.map(` dans les 700 caractères précédents » → **9 candidats**.
Remplacé par un vrai **appariement de parenthèses** (le `.map(` doit se *fermer*
après l'identifiant) → **1 candidat**. Les 9 étaient un artefact de voisinage,
pas de structure. Témoins des deux côtés : un `id` dans un `.map()` fabriqué est
détecté, un `id` hors `.map()` ne l'est pas.

**Un test d'englobement carrément faux.** Une version intermédiaire remontait
jusqu'au premier guillemet rencontré pour trouver l'ouverture du gabarit — elle
tombait sur `class="` et rendait un verdict sur le mauvais contexte. Elle
produisait des lignes propres, alignées, et fausses. Jetée.

## Ce que le filet couvre — mesuré par mutation

`tests/test_production_guards_canonical.py::test_no_duplicate_ids` ne visite que
**3 pages sur 8** : `/`, `/portfolio`, `/system`. (Un second gardien,
`test_api_links_intelligence_lot188`, couvre les vues de `/intelligence`, hors
des 8.)

Un doublon réel a donc été fabriqué des deux côtés de la frontière :

```text
doublon posé sur /markets  (page NON visitée)  →  suite complète : 2864 passed
doublon posé sur /         (page visitée)      →  test_no_duplicate_ids : FAILED
```

**Le gardien mord — là où il regarde.** Sur `/markets`, `/opportunities`,
`/analysis`, `/options`, `/journal`, un identifiant dupliqué serait servi au
navigateur sans qu'aucun des 2 864 tests ne le signale.

Je ne comble pas : l'invariant n'est **pas** violé aujourd'hui (mesuré 8/8), et
livrer un gardien parce qu'un trou existe est interdit depuis le 384. **Classé
rang 3** — étendre la liste des pages est trivial, mais c'est un choix de
couverture, pas une réparation.

À noter pour qui l'étendra : la regex du gardien, `id="([^"]+)"`, **ne retire pas
les `<script>`**. Elle compte donc les identifiants écrits dans les gabarits JS
comme s'ils étaient des nœuds. Sur les 3 pages actuelles cela ne déclenche rien,
mais élargir le périmètre sans corriger ce point ferait remonter des doublons qui
n'existent pas dans le DOM — exactement le `#op-compare` ci-dessus.

## Portée

Le contrôle porte sur les identifiants **statiquement observables** : le marquage
servi et les gabarits du JS servi. Un identifiant entièrement calculé
(`id="'+kind+'"`) échapperait au recensement, et l'exécution réelle du JS n'a pas
été rejouée dans un navigateur — la troisième classe est donc une **borne
statique**, pas une observation du DOM final.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier livré modifié.** Les deux sondes (`markets_page.py`,
  `briefing.py`) **restaurées à l'octet**, `git status` vide, suite de référence
  rejouée après restauration. Pas de preuve MD5 requise, pas de bump. SW :
  `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Dix-neuvième lot court. Deuxième lot d'affilée qui rend le **même diagnostic de
forme** : le produit est sain, le filet s'arrête avant la fin du périmètre. Après
les boutons (149/167), les identifiants (3 pages sur 8). Ce n'est pas une
coïncidence — c'est ce qu'on trouve quand on cesse de mesurer la **couleur** des
gardiens pour mesurer leur **couverture**.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
