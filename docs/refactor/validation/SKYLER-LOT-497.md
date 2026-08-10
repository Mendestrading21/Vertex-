# SKYLER LOT 497 — Le 495-A borné : il atteint bien `/portfolio`, mais par un chemin ÉTROIT et CONDITIONNEL — et il n'y arrive que si la position n'a PAS de thèse. Quatre faux résultats arrêtés, dont trois branches d'échec que mes propres calibrations ne couvraient pas

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-497` (base : lot 496 fusionné,
`8fb22844`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

## Le choix

J'ai pris **(c)** : borner un dossier **rang 1 déjà posé** plutôt qu'ouvrir une
famille neuve. **(a)** est prématuré avant le 500, et **(b)** — l'audit `PAGE_*`
— **reste une dette nommée** depuis le 495.

## Règle 491 d'abord — la chaîne, établie avant tout banc

```text
portfolio_page.py:478   VX.fetch('/api/positions/state')
positions_api.py:51-60  → recalculate_all(...)
recalculator.py:99-105  packet : st_fund · fund_score · earnings_dte · st_timing
recalculator.py:114     p['decision'] = verdict['final_decision']
recalculator.py:159-163 'positions_needing_action' : priority · status · action · decision
portfolio_page.py:445   rows = pf.positions_needing_action
portfolio_page.py:460   colonne « Verdict moteur » → r.decision      ← SURFACE SERVIE
```

`/portfolio` fetche bien `/api/positions/state` et `/api/positions/alerts`
(mesuré : 1 occurrence chacune dans les octets servis). **La surface existe.**

## Ce que le banc établit — et la condition qui change tout

Positions **fabriquées en mémoire** sur les 20 titres du scan DEMO
(`desk_data.json` jamais touché), A/B avec et sans la clé `st_fund` remplie :

```text
                                  carte affichée   verdict changé
SANS thèse, en gain                 20 lignes          4 / 20
AVEC thèse, en gain                  0 ligne           —  (rien n'est affiché)
AVEC thèse, sous invalidation       20 lignes          0 / 20
SANS thèse, sous invalidation       20 lignes          0 / 20
```

**Le 495-A atteint `/portfolio`, mais seulement pour une position SANS THÈSE et
EN GAIN.** Sous invalidation, le verdict est dominé par `thesis_invalidated` et
le fondamental ne change plus rien ; avec une thèse et rien qui cloche, la
position tombe en `P3_LOW` et **la carte n'est pas rendue du tout**
(`actionListHtml` retourne `''` sans lignes P0/P1).

C'est une **extension réelle mais étroite**, et je refuse de la publier comme
« 4/20 sur `/portfolio` » : ce serait vrai du banc et faux du produit.

**Fait de méthode qui mérite d'être nommé** : les deux défauts **co-occurrent**.
La carte n'apparaît que quand quelque chose ne va pas ; et quand ce qui ne va pas
est « thèse absente », le moteur est **aussi** aveugle au fondamental.

## Le second contrôle — les TROIS autres clés mortes

Mon A/B n'injectait que `st_fund`. Il excluait les trois autres lectures mortes
du même paquet.

```text
référence (production, 4 clés mortes)          REFUSER 18 · ATTENDRE 2
  + st_fund                          4 / 20 changées      ATTENDRE 6
  + earnings_dte                     2 / 20               ATTENDRE 4
  + st_timing                        0 / 20               inchangé
  + st_fund + earnings_dte           4 / 20   ← PAS 6
  + les trois                        4 / 20   ← PAS 6
```

**L'effet n'est PAS additif** : les deux titres que `earnings_dte` déplace sont
un **sous-ensemble** des quatre que `st_fund` déplace, et `st_timing` ne fait
**rien du tout**. Le dossier est donc borné : **l'effet conjoint des quatre clés
mortes vaut celui de `st_fund` seule.** Sans ce contrôle j'aurais laissé croire
qu'elles se cumulent.

## Ce que le banc trouve et qui ne se classe pas

Avec une thèse renseignée — la branche réellement instruite en production —
`thesis_health` **change sur 20 titres sur 20**, et son échelle **s'effondre** :

```text
production (st_fund mort)   statuts observés : INTACT · WEAKENING          → 2
st_fund rempli              AT_RISK · INTACT · MIXED · STRENGTHENING ·
                            WEAKENING                                       → 5
« fondamental » quitte les inconnues de la thèse : 20 / 20
```

**Une échelle à cinq états rendue binaire par une clé jamais écrite.** Mais
`thesis_health` et `overall_status` sortent à **0 occurrence** dans les octets
servis, et `positions_needing_action` expose `lifecycle_status`, **pas**
`thesis_health`. → **nommé, non classé** (règles 486, 491, 492).

## Quatre faux résultats arrêtés avant publication

1. **Mon blob fabriqué n'était pas lu.** `repository._parse_key` lit
   `blob['data']['myTrades']` ; je passais `blob['myTrades']`. Le banc a rendu
   **« 0 changement sur 0 position »** — un non-résultat parfaitement lisible
   comme « aucun impact ». **Ma calibration (B) ne couvrait pas le cas zéro
   position** : elle testait « une seule décision partout », pas « aucune
   décision ». Calibration **(A bis)** ajoutée : le banc doit charger 20/20.
2. **Ma première mesure de `thesis_health` tombait dans un retour anticipé.**
   `assess()` sort immédiatement si `thesis_text` est absent — mes positions
   n'en avaient pas. Résultat : « inchangé 0/20 ». Avec une thèse : **20/20**.
   **Deuxième branche d'échec dans le même lot.**
3. **`thesisState` de `/portfolio` est un HOMONYME** de `thesis_health` : il est
   calculé **côté client** à partir de `entrySnap.stop` et du cours
   (`portfolio_page.py:131-145`), et n'a rien à voir avec le moteur.
   **Vingt-quatrième récurrence**, arrêtée avant de servir de preuve.
4. **J'allais publier « 4/20 sur `/portfolio` ».** La mesure de la condition
   d'affichage montre que dans la seule configuration où le verdict change, la
   carte n'existe **que parce que la thèse manque** ; et que dès qu'une thèse est
   écrite sans problème par ailleurs, **la carte disparaît**.

**Arrêtés avant publication : 69 → 73.**

## Portée

- Les positions sont **fabriquées** : 20 actions sur les titres du scan DEMO,
  toutes du même profil par configuration. **Ce n'est pas un portefeuille réel**,
  et les quatre lignes du tableau ci-dessus décrivent **quatre configurations**,
  pas une distribution.
- Le taux **4/20** reste un **taux de démonstration** (règle 495). Ce qui est
  établi sans dépendre de la démo : le **mécanisme** (les quatre clés ne sont
  écrites nulle part sur le détail), la **non-additivité**, et la **condition
  d'affichage**.
- Je n'ai pas exploré les positions **OPTION** — seulement des actions.
- `/api/positions/state` renvoie aussi le tableau complet des positions, dont
  `thesis_health` : **servi, jamais lu** (`posState` n'est consommé qu'une fois,
  `portfolio_page.py:538`, par `actionListHtml`, qui ne lit que
  `state.portfolio`).
- **Aucun navigateur ouvert.** La chaîne est établie sur les octets servis et le
  code des routes ; `/portfolio` aurait pu être ouvert sans risque réseau, mais
  il n'aurait montré que ce que le banc établit déjà, **avec un portefeuille vide
  par défaut**.
- Le **rang 1 du 495-A n'est pas modifié** : il tient sur `/analysis`, où il est
  **inconditionnel**. Ce lot ajoute une seconde surface, **conditionnelle**, et
  ne crée **aucun dossier neuf**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** à chaque banc ; positions **fabriquées en
  mémoire**, `desk_data.json` **jamais ouvert en écriture** ; **aucune route
  réseau sortante**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le lot fait ce qu'on lui demandait — **borner** — et le bornage **réduit** la
portée annoncée plutôt que de l'étendre. C'est inhabituel dans cette tranche, et
c'est sain : quatre lots d'affilée ont ajouté ou requalifié quelque chose ; celui-ci
**resserre**.

Le fait le plus utile est de méthode, et il est cher payé : **trois des quatre
faux arrêtés étaient des branches d'échec de mon propre banc** — blob non lu,
retour anticipé sur thèse absente, condition d'affichage non instruite. La règle
« calibrer le banc sur sa propre validité » existe depuis le 492 ; **elle n'a
attrapé aucun des trois**, parce qu'elle testait la mauvaise chose. Une
calibration doit vérifier que le banc **charge quelque chose**, pas seulement
qu'il **rend quelque chose de varié**.

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
Le **495-A** gagne une seconde surface, **conditionnelle**, et une borne :
l'effet conjoint des quatre clés mortes **égale** celui de `st_fund` seule.

Comptes séparés : résultats faux **arrêtés avant publication 73 (+4)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
