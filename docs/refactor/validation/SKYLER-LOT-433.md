# SKYLER LOT 433 — Le portefeuille calcule `allMarked`, s'en sert pour une classe CSS, et l'ignore dans les trois phrases qui rassurent

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-433` (base : lot 432 fusionné,
255afd9)

Seizième lot de la veine, et **bornage du 432**. La règle dit : *quand un lot
trouve, le suivant peut utilement borner.* Le 432 avait ouvert **une** synthèse
qui range l'inconnu avec le sain. Combien y en a-t-il ?

**Aucun code, aucun gardien, aucun test.**

## Le pool — les phrases qui rassurent, dans les octets servis

Corpus servi (95 objets, 3 829 722 octets), littéraux commençant par
*Aucun / Aucune / Rien / Pas de / Tout* :

```text
phrases RASSURANTES littérales servies    47
```

La grande majorité décrit une **absence d'ENTRÉE** — « Aucune position
déclarée », « Aucun titre scanné », « Aucun trade réel déclaré ». Celles-là sont
honnêtes par construction : l'utilisateur n'a rien fourni, la carte le dit.

La classe dangereuse est l'autre : celles qui affirment une **absence de
PROBLÈME** après une évaluation qui n'a peut-être pas eu lieu. **Trois d'entre
elles vivent sur `/portfolio`, et elles partagent le mécanisme du 432.**

## Les trois sites, mesurés en exécutant les octets servis

`thesisState`, `computeMetrics`, `dominantRisk` et le filtre de la liste de
décision extraits du marquage servi de `/portfolio` (appariement d'accolades),
exécutés sous Node 22 :

```text
cas                                    allMarked   risque dominant                        liste de décision
TÉMOIN POSITIF                          true       « 1 position(s) sous invalidation »    1 position(s)
1 thèse cassée (marque 80 < stop 90)                — AAA

4 positions SANS marque                 false      « Aucun risque critique détecté »      « Aucune position urgente —
(échec de /api/pos-quotes)                         — concentration et invalidations         toutes les thèses sont intactes
                                                     dans les repères                       ou en surveillance normale. »

1 seule position, sans marque           false      « Concentration élevée : AAA = 100 % » idem
```

Le témoin positif prouve que les deux synthèses savent parfaitement remonter une
position en danger. Le cas sans marque prouve qu'elles **affirment le contraire
du doute** :

- **« concentration et invalidations dans les repères »** — aucune invalidation
  n'a pu être vérifiée, faute de marque ;
- **« toutes les thèses sont intactes ou en surveillance normale »** — c'est la
  formulation la plus explicite des trois : elle nomme deux catégories et
  affirme que chaque position tombe dans l'une d'elles.

*(Le troisième cas est instructif : la branche « concentration » **mord quand
même**, parce que les poids se replient sur le coût investi. La ligne de risque
n'est donc pas aveugle en entier — seule sa partie « invalidations » l'est. Je le
dis parce que ça nuance mon propre constat.)*

## Ce qui rend ce lot différent du 432 : l'information EXISTE, calculée, à portée

`computeMetrics` (`portfolio_page.py:197`, servi) calcule :

```javascript
const allMarked = rich.length && rich.every(t => t.value !== null);
```

Mesuré : **`allMarked` apparaît cinq fois** dans les octets servis de
`/portfolio`. Elle est calculée, elle conditionne `plAbs`, elle est exportée dans
`m`, elle pose **une classe `vx-warn`** sur la ligne de trésorerie, et elle garde
une écriture `localStorage`.

**Elle ne conditionne aucune des trois phrases.** Et `m` est dans la portée de
`dominantRisk` — c'est son second argument.

Le fichier sait donc parfaitement dire « je n'ai pas toutes les marques ». Il le
dit avec une couleur, jamais avec une phrase.

## Le contre-exemple, mesuré lui aussi

`/system`, carte de qualité des données, dans le marquage servi :

```text
si aucun titre scanné   →  « Aucun titre scanné — la qualité ne peut pas être mesurée. »
sinon, si rien de dégradé →  « Aucun titre en qualité dégradée — rien à signaler. »
```

**Le dépôt sait faire la différence entre « rien à signaler » et « je ne peux pas
mesurer », et il l'écrit** — sur une autre page. C'est exactement la garde qui
manque aux trois phrases de `/portfolio`.

## Le compte du bornage

```text
phrases rassurantes servies                                     47
   absence d'ENTRÉE (l'utilisateur n'a rien fourni)             majorité — honnêtes par construction
   absence de PROBLÈME ouvertes ici, sur /portfolio              3   → les 3 rangent l'inconnu avec le sain
      dominantRisk               « Aucun risque critique détecté »
      liste de décision          « Aucune position urgente — toutes les thèses… »
      priorityAction (lot 432)   « Aucune décision urgente — laisser courir… »
   contre-exemple mesuré (/system)                               1   → garde correcte
   non ouvertes                                                 43
```

**Le défaut du 432 n'était pas isolé : c'est un motif de page.** Les trois
synthèses de `/portfolio` tombent ensemble, sur le même déclencheur — un échec de
`/api/pos-quotes` — et **aucun test du dépôt ne mentionne `dominantRisk`.**

## Classement

**Rang 1**, et le même que le 432 : aucune valeur n'est inventée, c'est la
**synthèse** qui ment, dans le sens qui **rassure**. Ici la conséquence est plus
lourde qu'au 432, parce que les trois phrases occupent le **haut de la page** —
risque dominant, action prioritaire, liste de décision — et disent la même chose
en chœur : tout va bien.

Correction pressentie, et elle est déjà écrite ailleurs dans le fichier :
conditionner les trois phrases à `m.allMarked` (ou au compte d'états
`insuffisant`) et rendre, sinon, une formulation du type « n position(s) non
évaluable(s) — marques indisponibles ». **Aucun GO, rien n'est engagé.**

## Portée

Quarante-trois des quarante-sept phrases rassurantes **n'ont pas été ouvertes** :
je les ai classées par leur forme (« absence d'entrée » contre « absence de
problème »), pas vérifiées une par une. Le recensement ne prend que les littéraux
commençant par les cinq mots cherchés — une phrase rassurante construite
dynamiquement lui échappe, et c'est la même zone d'ombre que depuis le 427.

Je n'ai **pas observé** un portefeuille réel privé de cotations : les trois
fonctions sont exécutées sur des positions fabriquées. Le chemin d'entrée
(`catch → {}` dans le producteur des cotations) a été établi au 432 par lecture,
et n'est pas re-mesuré ici.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **MD5 des 8 pages remesurés : 8/8 identiques** aux références des lots 390/396.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-sixième lot court. Séquence : **429 ✗ · 430 bilan · 431 ~ · 432 ✓ ·
433 ✓ (bornage qui AGGRAVE)**.

C'est la première fois qu'un bornage **aggrave** au lieu de rassurer. Les
bornages précédents disaient « exception, pas symptôme » (426, 429) ou levaient
une alerte (431). Celui-ci fait l'inverse : il montre que le défaut du 432 est le
**motif d'une page entière**, que trois phrases tombent au même moment, et que
l'information nécessaire pour les corriger est **déjà calculée, à trois lignes de
là**.

**Quatre bilans — n°9, n°10, n°11, n°12 — attendent une réponse.**
