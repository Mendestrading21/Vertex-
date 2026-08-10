# SKYLER LOT 518 — La dette la plus ancienne, enfin mesurée : ce ne sont pas « 29 vues sans empreinte » mais **27 vues servies sur 35 dont aucun test ne regarde le contenu**. Et mon premier banc disait le contraire

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-518` (base : lot 517 fusionné,
`0ddaa4e1`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** — la dette portée par la feuille depuis le lot 505 et **jamais entamée** :
« 37 vues servies, 8 seulement ont une empreinte ». Après trois lots passés à
réparer mes propres instruments (515, 516, 517), c'est la seule dette restante
qui porte sur le **produit servi**.

## Deux corrections d'entrée

**Ce ne sont pas 37 vues, ce sont 35.** Mesuré en important chaque module de page
et en lisant **tout** registre dont le nom contient `VIEWS` :

```text
/                briefing              aucun registre        0 vue
/markets         markets_page          _VIEWS 5              5
/opportunities   opportunities_page    _VIEWS 5              5
/analysis        analysis_page         aucun registre        0 vue
/portfolio       portfolio_page        _VIEWS 6              6
/options         options_intel_page    _ALL_VIEWS 9          9   (6 + 3 legacy)
/journal         performance_page      _VIEWS 5              5
/system          system_page           VIEWS 5               5
                                                     TOTAL  35
```

Le piège des trois noms d'attribut (`_VIEWS` / `VIEWS` / `_ALL_VIEWS`) est réel
et l'instrument le franchit — mais **`/` et `/analysis` n'ont aucun registre**,
ce que le « 37 » ne disait pas.

**Et « sans empreinte » n'était pas la bonne question.** Une empreinte publiée
dans un rapport ne protège rien. Ce qui protège un rendu, c'est un **test**.

## Le premier banc rassurait — à tort

```text
vues servies                                    35
empreintes MD5 DISTINCTES                       35   ← aucune vue n'est un doublon
repli sur la vue par défaut (vue fabriquée)    8 / 8 ← le repli documenté marche
vues requêtées explicitement par un test        29
```

J'allais conclure que la dette était un mythe. **Le second contrôle l'a
renversé.**

## Le second contrôle — « requêtée » n'est pas « gardée »

Un test qui fait `cli.get('/markets?view=macro')` et vérifie `status_code == 200`
ne protège **rien** du contenu : la vue pourrait se vider entièrement, la suite
resterait verte. C'est la règle 508 (« un gardien teste souvent le cas qui
marche ») appliquée à la couverture elle-même.

Mesuré sur les **35 paires (page, vue) réelles** :

```text
vues dont au moins un test regarde le CONTENU       8
vues testées UNIQUEMENT par un code de statut      16
vues dont AUCUN test ne nomme l'URL                11
                                            ────────
                                                   35
```

**Vingt-sept vues sur trente-cinq — 77 % de la surface servie — n'ont aucun test
qui regarde ce qu'elles affichent.**

Et l'essentiel du « 29 requêtées » vient d'**un seul test**,
`tests/test_redesign_ui.py::test_subviews_return_200`, qui parcourt 21 vues et
n'assert que le statut.

Les 11 sans aucun test nommant l'URL, en détail :

```text
DÉFAUTS (atteintes par l'URL nue, elle-même testée)   4
   /markets?view=overview · /journal?view=overview
   /options?view=structure · /portfolio?view=team

NON-DÉFAUTS, aucune trace nulle part                  7
   /journal?view=progression      /options?view=events
   /options?view=overview         /options?view=radar
   /options?view=volatility       /portfolio?view=options
   /system?view=automations
```

**Sept vues qu'un utilisateur peut afficher et qu'aucun test ne demande jamais.**

## Classement — 518-A, rang 4

Rien de faux n'est montré : les 35 vues répondent 200, portent 35 empreintes
distinctes, et le repli sur la vue par défaut fonctionne sur les 8 pages. **Ce
n'est pas un défaut du produit, c'est un défaut de PROTECTION** — et c'est pour
cela que ce n'est pas plus haut.

Ce qui le distingue d'une curiosité : **l'échelle**. 77 % de la surface visible
peut se vider sans que la suite de 2 864 tests bronche. La règle 508 disait
qu'un gardien teste souvent le cas qui marche ; ici, seize gardiens ne testent
même pas cela — ils testent que le serveur répond.

Correction pressentie, non engagée : ajouter à chaque vue une assertion de
contenu minimale (un littéral propre à la vue). **Aucun GO, rien n'est engagé.**

## Une trouvaille secondaire — un paramètre accepté et jamais lu

`analysis_page.render_index(view: str = '')` accepte un paramètre `view`. Compté
par AST dans le corps de la fonction : **zéro occurrence de `view`**. La route
`/analysis?view=n-importe-quoi` rend donc exactement la même page. Ce n'est pas
un défaut visible — juste un contrat qui promet ce qu'il ne tient pas.

## Deux arrêts avant publication, tous deux sur mon banc

1. **J'ai agrégé la couverture par NOM de vue, en perdant la page.** Résultat :
   mon compte mélangeait `committee`, `memory`, `research`, `strategy` — qui sont
   des vues d'`intelligence_page`, **page morte établie au 515** — et
   `inexistant`, `zzz`, qui sont des **noms fabriqués par les tests négatifs**.
   Refait sur les 35 paires (page, vue) réelles.
2. **J'ai compté `vx-error-banner` et `vx-empty` dans les octets servis** et
   j'allais en tirer « 10 vues affichent une bannière d'erreur ». **Faux** : ces
   classes vivent aussi dans les **gabarits JS inertes** de la page. Compter le
   mot n'est pas constater la chose — piège 495, que j'ai laissé passer dans mon
   premier tableau et que je retire ici.

**Arrêtés avant publication : 113 → 115.**

## Ce que le dépôt fait bien, mesuré

- **Les 35 vues rendent 35 empreintes distinctes** : aucune n'est un doublon
  silencieux, aucune ne retombe par accident sur une autre.
- **Le repli fonctionne sur les 8 pages** : `?view=nexiste-pas` rend exactement
  la vue par défaut, comme le code le documente
  (`view = view if view in dict(_VIEWS) else '…'`).
- **Zéro vue en HTTP ≠ 200** sur les 35.
- Un test dédié protège déjà le repli
  (`test_robust_lot74.py::test_unknown_view_param_never_5xx`).

## Portée — ce que ce lot NE dit PAS

- **« Sans test de contenu » n'est pas « cassée ».** Les 35 vues fonctionnent
  aujourd'hui ; le lot mesure une **exposition**, pas une panne.
- Le crible de couverture cherche l'**URL littérale** dans le corps du test. Un
  test qui construirait l'URL par variables lui échapperait — j'ai compté 236
  boucles paramétrées dans la suite et je ne peux pas exclure qu'une d'elles
  couvre davantage. **Le « 27 » est donc une borne haute.**
- Mesuré en **DÉMO**, où certaines vues affichent légitimement des états vides.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques** — et c'était la calibration
  positive du banc, pas seulement une vérification de fin.
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4**.

Le 517 concluait que « la veine d'audit sur cet axe est épuisée ». C'était vrai
de l'axe des instruments. **En changeant d'axe — le produit servi plutôt que mes
cribles — la première mesure rend un dossier.** Et elle le rend en corrigeant
l'énoncé même de la dette : ce n'étaient ni 37 vues, ni un problème d'empreinte.

La leçon que je retiens : **une dette portée douze lots sans être mesurée finit
par être mal énoncée.** Celle-ci l'était sur trois points — le nombre, la nature,
et la conclusion.

Feuille : **36 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 · **quatre**
rang 4**.

Dettes nommées restantes : **mesurer le contenu des 23 routes non appelées** ;
**le français construit en JavaScript** ; **l'assemblage entre fonctions** (7
cas) ; **la condition `k ≤ 5` sur un scan réel** ; **recribler les chiffres
publiés par motif textuel** ; **le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 115 (+2)** ; publiés
puis corrigés **15** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
