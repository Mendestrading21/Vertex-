# SKYLER LOT 475 — LE DERNIER DOSSIER : seize fichiers cachaient SIX sources, dont DEUX fonctions homonymes `_rr` et surtout UNE CONSTANTE — « R:R structurel 3.0 » n'est pas une mesure, c'est une TAUTOLOGIE affichée comme un résultat

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-475` (base : lot 474 fusionné,
`6762d6f`)

Dernier dossier non chiffré du classement, **RANG 1**, borné au 474 et renvoyé
ici. Le 473 avait écrit qu'un devis honnête pour celui-là est **un lot entier** :
c'est ce lot.

**Il ne corrige rien.** Aucun fichier de production touché.

**Le dossier TIENT — et il tient plus fort que ses deux rapports ne le
disaient.**

## Le contrôle — réponse connue mot pour mot, et il passe

```text
attendu (relu au 471)   pretrade.py:161  n_ko = statuses.count(KO)
mesuré                  pretrade.py:161  n_ko = statuses.count(KO)
verdict                 CONTRÔLE PASSÉ
```

---

# ÉTAPE 1 — SEIZE FICHIERS, SIX SOURCES

Le 474 avait posé la question : *seize fichiers ne sont pas seize formules.*
Mesuré, ce sont **six sources distinctes** — et l'une d'elles n'est pas une
formule du tout.

```text
№  site                            expression                              nature
─────────────────────────────────────────────────────────────────────────────────
1  analysis.py:262                 'rr': 3.0                               CONSTANTE
2  analysis.py:264                 'rr_res': round(rr_res, 1)              ratio vs résistance
3  scenario_pricer.py:173          round(gain / abs(loss), 2)              ratio options
4  order_ticket.py:92  def _rr()   round((t - e) / (e - s), 2)             ratio du ticket
5  options_lab.py:70   def _rr()   _r2(pot / 100.0, 2)                     potentiel / prime
6  terminal.py:432                 'vx_rr': _vx.get('rr')                  noyau quant (`vertex`)
```

**Les treize autres sites cités par les 442 et 443 sont des CONSOMMATEURS**, pas
des calculs. Réduction mesurée : **16 fichiers → 6 sources → 4 formules
réelles + 1 constante + 1 relais**.

## Le piège des homonymes, treizième récurrence — et sous une forme neuve

```text
vertex/planning/order_ticket.py:92   def _rr(entry, stop, target)   → (cible − entrée) / (entrée − stop)
vertex/engines/options_lab.py:70     def _rr(c)                     → potentiel(%) / 100
```

**Deux fonctions du même nom, dans deux modules, qui ne calculent pas la même
chose.** Jusqu'ici l'homonymie portait sur un *nombre* (446), sur un *champ*
(469), sur un *littéral dans une fonction* (471). Ici c'est **le nom d'une
FONCTION**. La n°5 n'est même pas un rapport gain/perte : c'est un **potentiel
rapporté à une prime**, une grandeur qui n'a pas la même unité que les quatre
autres.

---

# ÉTAPE 2 — LESQUELLES ATTEIGNENT L'ÉCRAN

```text
source  consommateur servi                                                   verdict
   1    analysis_page.py:402  ` · R:R structurel ${plan.rr}`                  SERVI
        analysis_page.py:591  kv('R:R structurel',plan.rr)                    SERVI
        analysis_page.py:582  aria « …, R:R '+plan.rr »                       SERVI (lecteur d'écran)
        analysis_page.py:600  horizonLabel « plan moteur · R:R '+plan.rr »    SERVI
   3    analysis_page.py:631  `<div class="vx-meta">R:R</div>… t.reward_risk` SERVI
   6    opportunities_page.py:118 · :150 · :167 · :188 · :271  (`vx_rr`)      SERVI
   2    rr_res — consommée par order_ticket.py:122, PAS affichée telle quelle  non servi directement
   4    repli interne du ticket (order_ticket.py:124)                          non servi directement
   5    vertex/ui/options_lab.py:248 · :258 · :317 · :350                      NON SERVI — page morte
```

**`vertex/ui/options_lab.py` n'a AUCUN consommateur en production** (mesuré ; et
`CLAUDE.md` le documente déjà comme relique). **La source n°5 — la seule dont
l'unité diffère — n'atteint donc jamais l'écran.** C'est la leçon 465 appliquée,
et elle **réduit le dossier** : l'homonyme le plus dangereux est inatteignable.

**Trois sources atteignent l'écran, sur deux pages, toutes trois sous le libellé
« R:R ».**

---

# ÉTAPE 3 — DIVERGENT-ELLES, ET POURQUOI

## Le cœur du dossier : la source n°1 n'est PAS une mesure

```text
analysis.py:260-262
   plan = {'entry': round(last, 2), 'stop': round(stop, 2),
           'tp1': round(last + risk, 2), 'tp2': round(last + 2 * risk, 2),
           'tp3': round(last + 3 * risk, 2), 'rr': 3.0, …}
```

`tp3` est **défini** comme `entrée + 3 × risque`. Le rapport
`(tp3 − entrée) / (entrée − stop)` vaut donc **3 par construction, toujours,
pour tout titre, dans tout régime**. Le champ `'rr': 3.0` ne le calcule même
pas : il l'écrit en dur, ce qui est **cohérent** avec le reste du plan.

**Le défaut n'est pas dans le moteur — il est dans le LIBELLÉ.** L'écran annonce
« **R:R structurel 3.0** » : le mot « structurel » et le format numérique font
lire un **résultat mesuré sur ce titre**, alors que c'est **une définition**. Un
trader qui compare deux fiches y verra deux titres « également asymétriques » —
ils le sont par décret, pas par mesure.

**Genre neuf : UNE TAUTOLOGIE AFFICHÉE COMME UN RÉSULTAT — le nombre est exact,
et il n'informe de rien.**

## Les deux autres divergent parce qu'elles mesurent des choses différentes

```text
source 1  « R:R structurel »   /analysis    ratio défini par construction, toujours 3.0
source 3  « R:R »              /analysis    gain simulé / perte simulée d'un CONTRAT
source 6  « R:R visé »         /opportunités  champ `rr` du noyau quant `vertex`
```

Trois grandeurs, **trois objets différents** (un plan action, un contrat option,
un score quant), **un seul mot à l'écran**. Le libellé « R:R visé » de
`/opportunities` est le plus honnête des trois — il dit « visé ».

**Le défaut est donc un LIBELLÉ dans les trois cas, pas un calcul** — sauf que le
premier cumule les deux : mauvais libellé **et** grandeur sans contenu.

---

# ÉTAPE 4 — LE CHIFFRAGE

```text
CE QU'IL FAUT CHANGER — 4 sites d'affichage, tous dans analysis_page.py
  :402   ` · R:R structurel ${plan.rr}`
  :582   aria « …, R:R '+plan.rr »
  :591   kv('R:R structurel',plan.rr)
  :600   horizonLabel « … · R:R '+plan.rr »

lignes à modifier   4   (libellé, ou retrait de l'affichage)
fichiers            1   (analysis_page.py)
moteur touché       NON — et il ne FAUT PAS toucher analysis.py:262 :
                    `rr: 3.0` est cohérent avec tp3 et order_ticket lit `rr_res`,
                    pas `rr`. Modifier le moteur casserait la cohérence du plan
                    pour corriger un problème d'écran.
```

**Deux variantes, et je recommande la seconde :**

| variante | lignes | ce qu'elle donne |
|---|---|---|
| (a) renommer « R:R structurel » en « objectif à 3× le risque » | 4 | dit la vérité : c'est une définition |
| **(b) afficher `rr_res` (source n°2) à la place** | **4** | **remplace une tautologie par une MESURE réelle — le ratio vers la résistance observée** |

**(b) coûte le même nombre de lignes et rend un chiffre qui informe.** La source
n°2 est **déjà calculée** (`analysis.py:264`) et **déjà transmise dans le même
dictionnaire `plan`** — c'est la famille 433/457 : *l'information honnête est
déjà là*. Réserve : `rr_res` peut être `None`, il faudra un repli honnête.

## Gardien et régression

```text
gardien       tests/test_rr_structurel_lot4xx.py
assertion     aucun objet servi n'affiche un ratio dont la valeur est CONSTANTE
              pour tout titre — concrètement : « R:R structurel » absent des
              octets servis de /analysis
échoue-t-il aujourd'hui ?   OUI — mesuré : `R:R structurel` est présent aux lignes
              402 et 591 de analysis_page.py, servi sur /analysis
gardiens existants   « R:R structurel » → 0 · « plan.rr » → 0
                     (`vx_rr` → 3 dans test_strategy_fit_lot147.py, sur la source n°6,
                      qui n'est PAS le site à corriger)
régression    AUCUN test ne touche les 4 sites. Les 3 tests `vx_rr` portent sur
              strategy_fit, source différente → RISQUE FAIBLE
octet servi ?  OUI (/analysis) → bump SW + 5 gardiens · _EMPREINTE NON
```

## Ce que le dossier N'EST PAS — et je le retire

Le 442 parlait d'un « R:R structurel » dans `vertex/ai/fallback.py:24`
(`f"R:R structurel {tech['reward_risk']}"`). Le **455** avait déjà mesuré que ce
module est **jamais produit — non atteignable**. Ce site **sort du dossier** :
il ne compte pas, et un correctif ne doit pas y toucher.

De même la source n°5 (`options_lab._rr`), la plus divergente en unité, vit dans
une **page morte**. **Deux des sites les plus spectaculaires du dossier sont
inatteignables** — et le dossier tient quand même, sur les quatre sites servis de
`/analysis`.

---

# ÉTAPE 5 — LE DEVIS EST CLOS

## La feuille de décision finale — SEIZE DOSSIERS

| # | dossier | rang | fichier | lignes | moteur | servi | `_EMPREINTE` |
|---|---|---|---|---|---|---|---|
| 1 | **457** borne V1 | **1** | `portfolio_page.py` | ≈5 | non | oui | non |
| 2 | 455 pré-trade | 2 | `pretrade.py` | 2 | oui | non | non |
| 3 | 461 `dominantRisk` | 2 | `portfolio_page.py` | 1-2 | non | oui | non |
| 4 | **434** anomalies | **1** | `opportunities_page.py` | 1 | non | oui | non |
| 5 | **427** légende | **1** | `markets_page.py` | 1 | non | oui | non |
| 6 | **428** entonnoir | **1** | `markets_page.py` | 2 | non | oui | non |
| 7 | **437** fraîcheur | **1** | 3 pages + `terminal.py` | 5 | non | oui | non |
| 8 | 456 dénominateur | 2 | `strategy_os_api.py` | 1 | non | non | non |
| 9 | 463 provenance GEX | 2 | `gex_history.py` (+JS) | 4 | oui | oui si JS | **oui si JS** |
| 10 | **425** maturités | **1** | `markets_page.py` | 2 | non | oui | non |
| 11 | 458 `catOf` | 2 | `opportunities_page.py` | 1 | non | oui | non |
| 12 | **464** journaux | **1** | 3 × `engines/` | 6 | oui | non | non |
| 13 | **447** max pain | **1** | `positions_api.py` | 1-2 | non | non | non |
| 14 | **452** collision | **1** | 1 route | 1 | non | non | non |
| 15 | **432+433** synthèses | **1** | `portfolio_page.py` | 3 (+2) | non | oui | non |
| 16 | **442+443** R:R | **1** | `analysis_page.py` | **4** | **non** | oui | non |

```text
SEIZE DOSSIERS · 40 à 48 LIGNES · 16 GARDIENS · ONZE DE RANG 1
UN SEUL bump SW · _EMPREINTE une seule fois (463)
```

## Les lots de travail — définitifs

```text
A  « /markets »        427+428+425        6 l. · 1 fichier · 3 RANG 1 · 0 gardien existant
B  « les journaux »    464                6 l. · 3 fichiers · aucun bump
C  « /portfolio »      457+461+432/433   10 l. · 1 fichier · 2 RANG 1
                                          NE PAS séparer 461 et 433 : MÊME fonction
D  « /opportunités »   434+458            2 l. · 1 fichier
E  « la fraîcheur »    437                5 l. · 4 fichiers · à faire seul
F  « les routes »      447+452+456        4 l. · 3 routes · 2 RANG 1 · AUCUN octet servi
G  « /analysis »       442+443            4 l. · 1 fichier · 1 RANG 1        ← NOUVEAU
H  « isolés »          455+463            6 l. · 463 en dernier (seul _EMPREINTE)
```

**Huit lots. Quatre d'entre eux (A, C, D, G) ne touchent qu'UN fichier chacun.**

## Regroupement par fichier — définitif

```text
portfolio_page.py       457 · 461 · 432+433     3 dossiers · 2 rang 1 · 10 l.
markets_page.py         427 · 428 · 425 · 437p  4 dossiers · 3 rang 1 ·  6 l.
opportunities_page.py   434 · 458 · 437p        3 dossiers · 1 rang 1 ·  3 l.
analysis_page.py        442+443                 1 dossier  · 1 rang 1 ·  4 l.
routes                  447 · 452 · 456         3 dossiers · 2 rang 1 ·  4 l.
engines/                464 · 455 · 463         3 dossiers · 1 rang 1 · 12 l.
```

**Quatorze des seize dossiers tiennent dans six emplacements.**

## LE DEVIS EST CLOS

**Il n'y a plus rien à chiffrer dans le classement.** Les seize dossiers du
classement coût/risque sont localisés, relus ligne à ligne, chiffrés, avec leur
gardien, leur régression, leur impact service worker et leurs contraintes
d'exécution. **La boucle attend une décision, et elle n'a plus d'excuse pour
mesurer davantage.**

## Ce qui reste explicitement HORS du devis

**Les trois dossiers de DÉCISION** — 469 (la Constitution fait-elle loi ?), 468
(six seuils sans source), 466/467 (28 orphelines) : ils demandent qu'on
**décide**, pas qu'on répare.

**Dix-huit dossiers jamais classés, donc jamais chiffrés** : 388 · 406 · 407 ·
408 · 409 · 411 · 426 · 416 · 417 · 422 · 391/396 · 379 · 363 · 378 · 386+431 ·
452 (volet rang 2) · 456+459 · 461 `winnerRule`.

**Seize sur une trentaine.** Je le redis pour qu'on ne lise pas « 40 à 48
lignes » comme le coût de la dette entière.

## Ce que le lot ne prétend pas

- **Aucun test n'a été écrit.** L'« échoue aujourd'hui ? OUI » est établi **par
  lecture** des lignes 402 et 591.
- Je n'ai **pas exécuté** `analyse()` pour vérifier que `rr` vaut 3.0 sur un
  titre réel : c'est établi **par lecture du littéral** `'rr': 3.0` et de la
  définition de `tp3` deux lignes plus haut. C'est suffisant pour une constante,
  ce ne le serait pas pour une formule.
- La variante **(b)** est un **jugement** ; **(a)** est chiffrée à l'identique
  pour qu'on puisse trancher contre moi.
- `rr_res` peut être `None` — la variante (b) exige un repli honnête que je n'ai
  pas chiffré séparément (il tient dans les 4 lignes).
- **Aucun défaut rejoué.** Le classement rang 1 du 442+443 est **maintenu**, et
  il est **mieux étayé** qu'à l'origine.
- **Aucun navigateur. Aucun réseau. Aucun écrivain appelé. Aucun fichier de
  production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `persist` redirigé vers un `mkdtemp` **et la redirection
  vérifiée par `cache_path()`** ; **aucun écrivain appelé** ; `analyse()` **non
  appelée** ; **`/options/<sym>`, `/api/analyst/`, `/api/correlations/`,
  `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-dix-septième lot court, **cinquième et dernier du devis**.

Le dossier le plus intimidant du classement — seize fichiers, deux rapports
croisés, un lot entier annoncé — s'est réduit à **quatre lignes dans un seul
fichier**. Non parce qu'il était surestimé, mais parce que **compter les sources
au lieu des fichiers a divisé le problème par quatre**, et que **deux des sites
les plus voyants étaient inatteignables**.

Le fait de méthode du lot, et il clôt bien la série :

*Un défaut peut être exact, servi, et vide. « R:R structurel 3.0 » n'est pas un
chiffre faux — c'est un chiffre qui n'a jamais rien mesuré. La veine a passé
cinquante lots à chercher des nombres FAUX ; celui-ci est VRAI et n'informe de
rien, et c'est une catégorie que je n'avais pas nommée.*

**Genre neuf : UNE TAUTOLOGIE AFFICHÉE COMME UN RÉSULTAT.**

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **42** ;
**publiés puis corrigés** **5** ; **interprétations retirées** **3** ; **dossiers
en attente de re-localisation 1 → 0**.

**Le devis est clos : seize dossiers, onze de rang 1, 40 à 48 lignes, huit lots
de travail autonomes. Huit bilans — n°9 à n°16 — attendent une réponse, et il
n'y a plus rien à mesurer avant une décision.**
