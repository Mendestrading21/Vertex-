# SKYLER LOT 474 — RE-LOCALISATION : trois dossiers sur quatre retrouvés et chiffrés, la collision de route du 452 PROUVÉE PAR LE ROUTEUR LUI-MÊME (deux règles vivantes pour une seule URL), et le 433 tombe DANS LA FONCTION que le devis du 461 vise déjà

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-474` (base : lot 473 fusionné,
`e04adee`)

Le 473 a refusé de chiffrer quatre dossiers **tous RANG 1** parce que leurs sites
publiés ne pointaient plus sur ce qu'ils annoncent. Ce lot **rétablit d'abord,
chiffre ensuite** — et dit pour chacun si le dossier **tient toujours**.

**Il ne corrige rien.** Aucun fichier de production touché.

**Résultat : trois retrouvés et chiffrés, un borné au 475. Les trois retrouvés
TIENNENT tous les trois.**

## Le contrôle — réponse déjà connue, et il passe

```text
attendu (rétabli par le 473)   analysis_page.py:856 = `async function loadAnomalies(){`
mesuré                          :856  async function loadAnomalies(){
                                :859  const d=await VX.fetch('/api/anomalies/'+SYM,{ttl:120000});
verdict                         CONTRÔLE PASSÉ
```

Et il rend davantage : la ligne `:859` **nomme l'URL**, ce qui a ouvert le second
volet du 452.

---

# A. 447 — MAX PAIN MULTI-ÉCHÉANCES · RANG 1 · RETROUVÉ, TIENT, CHIFFRÉ

## Les sites, rétablis

Le 473 avait mesuré que `max_pain` **n'apparaît dans aucun** des deux fichiers
cités par le 447. Recherche par **producteur** puis par **consommateurs**, sans
passer par un mot de la phrase :

```text
PRODUCTEUR
  vertex/options/gex.py:232   def max_pain(contracts)   ← itère TOUS les contrats,
                                                          AUCUN filtre d'échéance
  vertex/options/gex.py:226   'max_pain': max_pain(contracts)   ← appelé dans compute()

CONSOMMATEURS (5, mesurés)
  vertex/app/routes/positions_api.py:206-215   PIN RISK — LE SITE DU DOSSIER
  vertex/options/gex_scan.py:49                repasse le champ
  vertex/options/dealer_synthesis.py:69        `mp = gex.get('max_pain')`
  vertex/static/vertex/js/pages/options-gex.js:69   tuile « Max pain »
  vertex/static/vertex/js/pages/options-gex.js:149  colonne de tableau
```

## Pourquoi le 447 citait `portfolio_page.py:484` — et pourquoi il avait raison

```text
positions_api.py:213-215   'detail': 'Spot collé au max pain (%s ~ %s) à J-%d de la plus
                                      proche échéance — risque d\\'épinglage…'
                                      % (spot, mp, int(min(dtes)))
portfolio_page.py:484      ((alerts&&alerts.gamma)||[]).forEach(g=>survRows.push({…txt:g.detail}))
portfolio_page.py:488      `<li>… ${esc(r.txt||'')}</li>`
```

**La chaîne est complète et le 473 avait raison À LA LETTRE** : `:484` ne contient
pas « max pain », il rend `g.detail` — une chaîne **construite ailleurs**. La
référence n'était pas fausse, elle était **indirecte**. C'est une nuance que le
473 n'avait pas su formuler et que la re-localisation rend nette :

**Un site de RENDU GÉNÉRIQUE ne porte pas le vocabulaire du défaut qu'il
affiche.** Chercher le mot dans le fichier de rendu ne prouve rien.

## Le défaut, confirmé par lecture

`max_pain(contracts)` prend la liste **entière** et construit sa grille sur
`{k for k, _, _ in rows}` — **tous strikes, toutes échéances confondues**.
`positions_api.py:209-215` attribue ce résultat global à `min(dtes)`, **l'échéance
la plus proche**. Le dossier **tient**.

## Chiffrage

```text
lignes à modifier   2  — filtrer `contracts` sur l'échéance minimale AVANT d'appeler
                       max_pain dans positions_api (1 l.) + passer la liste filtrée (1 l.)
                    OU 1 ligne — retirer l'attribution « à J-%d de la plus proche échéance »
fichiers            1  (positions_api.py) · moteur touché : NON si l'on filtre chez l'appelant
CHOIX               le filtrage chez l'APPELANT évite de toucher gex.max_pain(), donc évite
                    d'impacter les 4 autres consommateurs. C'est le geste le moins risqué.
```

**Ne PAS modifier `gex.max_pain()`** : quatre autres consommateurs en dépendent,
et pour eux le max pain global est **le bon chiffre**. Le défaut n'est pas dans
le moteur, il est dans **l'attribution faite par un seul appelant**.

## Gardien et régression

```text
gardien       tests/test_pin_risk_echeance_lot4xx.py
assertion     sur un board à deux échéances dont les max pain diffèrent, l'alerte
              GAMMA_PIN_RISK cite le max pain de l'échéance NOMMÉE
échoue-t-il aujourd'hui ?   OUI — `mp = prof.get('max_pain')` (:206) lit le champ GLOBAL,
              et rien entre :206 et :215 ne restreint par échéance
gardiens existants   `max_pain` → 4 (tests/test_gex.py, sur la fonction, pas l'attribution)
                     `GAMMA_PIN_RISK` → 4 (tests/test_gamma_surveillance.py)
régression    les 4 tests de test_gamma_surveillance touchent CE site → à relire avant
              correction. C'est le dossier le plus couvert des quinze : RISQUE MOYEN,
              le seul du devis à ne pas être « aucun gardien ».
octet servi ?  NON (route JSON) → aucun bump, aucun _EMPREINTE
```

---

# B. 452 — `/analysis` ANOMALIES + COLLISION DE ROUTE · RANG 1 · RETROUVÉ, TIENT, CHIFFRÉ

## Volet 2 — la collision, PROUVÉE PAR LE ROUTEUR

Le 473 laissait ce volet « à localiser ». Il est résolu, et pas par lecture :
**en interrogeant `app.url_map`**, qui est la source d'autorité.

```text
règle /api/anomalies/<sym>  →  endpoint analysis_api.api_anomalies      (analysis_api.py:59)
règle /api/anomalies/<sym>  →  endpoint strategy_os.anomalies_for       (strategy_os_api.py:104)
```

**DEUX règles vivantes pour UNE seule URL.** Werkzeug n'en sert qu'une ; la
seconde est **inatteignable**. Ce n'est plus une hypothèse de lecture : les deux
règles sont **dans le routeur de l'application réelle**, listées côte à côte.

Et les deux implémentations ne rendent pas la même chose :

```text
strategy_os_api.py:107-116   lit scan_state['detail'][sym]['series']['close'],
                             fabrique des barres CLOSE-ONLY, exige >= 30 barres,
                             et sert une `note` honnête : « série close-only du scan :
                             gaps/volumes non couverts sur cette route »
analysis_api.py:59-60        l'autre implémentation, celle qui est SERVIE
```

**La route morte est celle qui porte l'avertissement d'honnêteté sur ses propres
limites.** Le consommateur (`analysis_page.py:859`) reçoit donc l'autre payload.

## Chiffrage

```text
lignes à modifier   1  — supprimer ou renommer l'une des deux règles
fichiers            1 · moteur touché : non
DÉCISION PRÉALABLE  LAQUELLE des deux doit vivre ? Ce n'est PAS un choix technique :
                    les deux calculent des anomalies différemment. C'est une question
                    de produit — et je ne la tranche pas.
```

## Gardien et régression

```text
gardien       tests/test_routes_uniques_lot4xx.py
assertion     aucune URL n'apparaît deux fois dans app.url_map avec deux endpoints distincts
échoue-t-il aujourd'hui ?   OUI — mesuré à l'instant sur le routeur réel : deux règles
              pour /api/anomalies/<sym>. C'est le SEUL gardien du devis dont l'échec est
              établi par EXÉCUTION et non par lecture.
gardiens existants   `api/anomalies` → 3 fichiers · `anomalies_for` → 1
régression    tests/test_analysis_lot146.py cible `anomalies_for` — c'est-à-dire
              l'endpoint MORT. À vérifier avant suppression : le test l'appelle-t-il par
              son endpoint (donc via url_for) ou par l'URL (donc l'autre) ?
octet servi ?  NON → aucun bump
```

**Ce gardien est le plus rentable des quinze** : il coûte quelques lignes, ne
touche aucun fichier de production, et **protège les 189 règles à la fois**.

---

# C. 432 + 433 — LES TROIS SYNTHÈSES DE `/portfolio` · RANG 1 · RETROUVÉ, TIENT

## Les phrases, retrouvées

Le 473 avait mesuré que les lignes citées étaient les **mécanismes**. Les
**phrases** sont ailleurs, et elles sont trois :

```text
portfolio_page.py:231   return {label:'Aucun risque critique détecté', …}       ← dans dominantRisk
portfolio_page.py:244   return {sym:null,label:'Aucune décision urgente — laisser courir
                                 les thèses intactes',tone:'muted'}
portfolio_page.py:398   VX.states.empty('Aucune position urgente — toutes les thèses sont
                                 intactes ou en surveillance normale.')
```

(Deux variantes voisines existent en `:742` et `:744`, sur la vue Risque — elles
partagent le mécanisme et sont à traiter dans le même geste.)

Le 433 nommait `thesisState`, `computeMetrics`, `dominantRisk` et le filtre de la
liste de décision : **les quatre mécanismes produisent exactement ces trois
phrases.** Le dossier **tient**.

## LA MUTUALISATION LA PLUS FORTE DU DEVIS ENTIER

```text
portfolio_page.py:216-232   function dominantRisk(rich,m)
     :221   if(m.top1&&m.top1.w>25)              ← LE DOSSIER 461, déjà devisé 1-2 lignes
     :231   return {label:'Aucun risque critique détecté'}   ← LE DOSSIER 432/433
```

**Le dossier 461 et le dossier 433 sont dans la MÊME FONCTION, à dix lignes
d'écart.** Le premier corrige le seuil qui fait entrer dans la branche d'alerte ;
le second corrige ce que dit la branche de sortie quand rien n'a pu être mesuré.
Les traiter séparément, ce serait ouvrir deux fois une fonction de dix-sept
lignes.

Et le 457 vit dans le même fichier. **Le lot de travail C du 473 (« /portfolio »,
457 + 461) doit devenir 457 + 461 + 432/433.**

## Chiffrage

```text
lignes à modifier   3  (les trois phrases, conditionnées à `allMarked` — déjà calculé
                       en :197 et déjà utilisé pour une classe CSS, c'est tout le dossier 433)
                    +2 si l'on aligne les variantes :742 et :744
fichiers            1 (le MÊME que 457 et 461) · moteur touché : non
gardien       tests/test_synthese_portefeuille_lot4xx.py — les trois phrases n'apparaissent
              pas quand `allMarked` est faux
échoue-t-il aujourd'hui ?   OUI — mesuré : `Aucun risque critique` et `Aucune décision
              urgente` → ZÉRO occurrence dans tests/, et les retours :231/:244 ne
              consultent pas `allMarked`
octet servi ?  OUI → bump + 5 gardiens · _EMPREINTE NON
```

---

# D. 442 + 443 — LES TROIS R:R · BORNÉ, RENVOYÉ AU 475

Seize fichiers cités par deux rapports croisés, sur une grandeur calculée en
plusieurs endroits. Le 473 avait écrit qu'un devis honnête pour celui-là est **un
lot entier**. La re-localisation le confirme sans le résoudre.

**Je le borne explicitement et je le renvoie au 475** plutôt que de le bâcler.
Un bornage est un résultat — c'est la onzième fois de la veine.

**Ce que le 475 devra faire** : établir combien de FORMULES distinctes de R:R
existent réellement (les seize fichiers ne sont pas seize formules), laquelle est
servie, et si les trois valeurs affichées divergent parce qu'elles mesurent des
choses différentes ou parce qu'elles se contredisent.

---

# LA FEUILLE DE DÉCISION, MISE À JOUR — QUINZE DOSSIERS

| # | dossier | rang | fichier | lignes | moteur | servi | gardien existant |
|---|---|---|---|---|---|---|---|
| 1 | **457** borne V1 | **1** | `portfolio_page.py` | ≈5 | non | oui | 0 |
| 2 | 455 pré-trade | 2 | `pretrade.py` | 2 | oui | non | 1 (clause READONLY) |
| 3 | 461 `dominantRisk` | 2 | `portfolio_page.py` | 1-2 | non | oui | 0 |
| 4 | **434** anomalies | **1** | `opportunities_page.py` | 1 | non | oui | 0 |
| 5 | **427** légende | **1** | `markets_page.py` | 1 | non | oui | 0 |
| 6 | **428** entonnoir | **1** | `markets_page.py` | 2 | non | oui | 0 |
| 7 | **437** fraîcheur | **1** | 3 pages + `terminal.py` | 5 | non | oui | 0 |
| 8 | 456 dénominateur | 2 | `strategy_os_api.py` | 1 | non | non | 0 |
| 9 | 463 provenance GEX | 2 | `gex_history.py` (+JS) | 4 | oui | oui si JS | 0 |
| 10 | **425** maturités | **1** | `markets_page.py` | 2 | non | oui | 0 |
| 11 | 458 `catOf` | 2 | `opportunities_page.py` | 1 | non | oui | 0 |
| 12 | **464** journaux | **1** | 3 × `engines/` | 6 | oui | non | 0 |
| 13 | **447** max pain | **1** | `positions_api.py` | 1-2 | non | non | **4 — le seul couvert** |
| 14 | **452** collision | **1** | 1 route | 1 | non | non | 3+1 |
| 15 | **432+433** synthèses | **1** | `portfolio_page.py` | 3 (+2) | non | oui | 0 |

```text
QUINZE DOSSIERS · 36 à 44 LIGNES · 15 GARDIENS · DIX DE RANG 1
UN SEUL bump SW · _EMPREINTE une seule fois (463)
```

## Regroupement par fichier — mis à jour

```text
portfolio_page.py       457 · 461 · 432+433        3 dossiers · 2 rang 1 · 10 lignes
                        dont 461 et 433 DANS LA MÊME FONCTION (dominantRisk, 17 lignes)
markets_page.py         427 · 428 · 425 · 437(p)   4 dossiers · 3 rang 1 ·  6 lignes
opportunities_page.py   434 · 458 · 437(p)         3 dossiers · 1 rang 1 ·  3 lignes
engines/ journaux       464                        1 dossier  · 1 rang 1 ·  6 lignes
routes                  447 · 452 · 456            3 dossiers · 2 rang 1 ·  4 lignes
```

**Treize des quinze dossiers tiennent dans cinq emplacements.**

## Lots de travail — révisés

```text
A « /markets »        427+428+425        6 l. · 1 fichier · 3 RANG 1 · 0 gardien existant
B « les journaux »    464                6 l. · 3 fichiers · aucun bump
C « /portfolio »      457+461+432/433   10 l. · 1 fichier · 2 RANG 1 — 461 et 433 dans
                                         la MÊME fonction : ne surtout pas les séparer
D « /opportunités »   434+458            2 l. · 1 fichier
E « la fraîcheur »    437                5 l. · 4 fichiers · à faire seul
F « les routes »      447+452+456        4 l. · 3 routes · 2 RANG 1 · AUCUN octet servi
G « isolés »          455+463            6 l. · 463 en dernier (seul _EMPREINTE)
```

**Le lot F est nouveau et c'est le second meilleur du plan** : deux rangs 1, quatre
lignes, aucun octet servi donc **aucun bump, aucun navigateur, aucune capture**.
Réserve honnête : **c'est aussi le seul lot qui touche un site déjà couvert par
quatre tests** (447) et **le seul qui exige une décision de produit avant
correction** (452 — laquelle des deux routes doit vivre).

## Ce qui reste hors devis

**442+443** (RANG 1, borné au 475) et **dix-huit dossiers jamais classés** :
388 · 406 · 407 · 408 · 409 · 411 · 426 · 416 · 417 · 422 · 391/396 · 379 · 363 ·
378 · 386+431 · 452 (volet rang 2) · 456+459 · 461 `winnerRule`. Plus les **trois
dossiers de DÉCISION** (469, 468, 466/467), qui ne sont pas des correctifs.

## Ce que le lot ne prétend pas

- **Aucun test n'a été écrit.** Tous les « échoue aujourd'hui ? OUI » sont
  établis par lecture — **sauf celui du 452**, établi par **exécution du routeur**,
  et je le distingue parce que c'est plus fort.
- Le 447 est chiffré **chez l'appelant** ; je n'ai pas mesuré si les quatre autres
  consommateurs souffrent du même travers — **je ne l'affirme ni ne l'exclus**.
- La question « laquelle des deux routes doit vivre » (452) est une **décision de
  produit** que je ne tranche pas.
- Les lots A à G sont un **découpage proposé** ; le regroupement par fichier,
  lui, est mesuré.
- **Aucun défaut rejoué**, aucun classement modifié : les trois dossiers
  retrouvés **tiennent tous les trois**, aux rangs de leurs rapports d'origine.
- **Aucun navigateur. Aucun réseau. Aucun écrivain appelé. Aucun fichier de
  production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `app.url_map` **lu** (n'écrit rien) ; pages en **GET** ; `persist` redirigé vers
  un `mkdtemp` **et la redirection vérifiée par `cache_path()`** ; **aucun
  écrivain appelé** ; **`/options/<sym>`, `/api/analyst/`, `/api/correlations/`,
  `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-seizième lot court.

Le 473 avait posé que *un rapport de mesure établit qu'un défaut EXISTE, pas OÙ
il est d'une façon qui survive au temps.* Ce lot en donne la suite, et elle est
plus encourageante que je ne l'attendais : **les quatre dossiers refusés n'étaient
pas perdus — trois ont été retrouvés en une passe, et les trois tiennent.** Ce
qui avait échoué au 473, ce n'était pas la mesure d'origine : c'était la
**référence**.

Le fait de méthode neuf, et il explique le 473 rétrospectivement :

*Un site de RENDU GÉNÉRIQUE ne porte pas le vocabulaire du défaut qu'il affiche.*
`portfolio_page.py:484` rend `g.detail` ; la phrase « max pain » est construite
trois fichiers plus loin. Chercher le mot dans le fichier de rendu ne prouve rien
— **le 473 en a conclu « site introuvable » là où il fallait conclure « référence
indirecte ».** Ce n'est pas une erreur du 473, qui a refusé de chiffrer plutôt
que d'inventer ; c'est la limite de son instrument, et elle est levée.

Et un résultat de plan : **le 461 et le 433 sont dans la même fonction de
dix-sept lignes.** Aucun des deux rapports ne pouvait le savoir — ils ont été
écrits à trente lots d'écart, sur deux veines différentes. **Seul le devis, qui
regarde les lignes et non les défauts, pouvait le voir.**

Comptes séparés : résultats faux **arrêtés avant publication** **42** ;
**publiés puis corrigés** **5** ; **interprétations retirées** **3** ; **dossiers
en attente de re-localisation 4 → 1** (442+443, borné au 475).

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan de travail couvre
désormais quinze dossiers, dix de rang 1, pour 36 à 44 lignes.**
