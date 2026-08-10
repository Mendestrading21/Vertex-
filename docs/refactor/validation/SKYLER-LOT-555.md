# SKYLER LOT 555 — **les 7 routes sans filet tiennent leur contrat** : 12 clés lues en portée, **12 confirmées, zéro divergence** — et quatre chiffres faux arrêtés avant publication

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-555` (base : lot 554 fusionné,
`463be276`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. AUCUNE de ces 7 routes n'a été
appelée** — tout est lu : la fonction de vue par `app.view_functions`, sa source
par `inspect.getsource`, son contrat par `ast`.

## Le choix

**(aa)** — le 554 a nommé **7 routes que le produit appelle au chargement d'une
page et qu'aucun test ne couvre**. Elles ne sont pas autorisées à l'appel, mais
leur code est lisible. Question du lot : **pour chacune, quel contrat le
gestionnaire promet-il, et la page lit-elle des clés que ce contrat ne produit
pas ?**

## L'arrêt du lot — **le témoin du brief est faux pour la cinquième fois**

Le brief demandait de vérifier qu'au moins une clé littérale sort du `jsonify`
de `api_track_record`. Lecture, `terminal.py:7067` :

```python
def api_track_record():
    return jsonify(_track.evaluate(scan_state))
```

**Aucun dictionnaire littéral.** Le contrat est construit dans un autre module.
Témoin remplacé par un témoin **lu dans le code** —
`vertex/app/routes/strategy_os_api.py:147` porte
`jsonify({'active': ALERTS.active_alerts(), 'status': ALERTS.status()})`.

Et, comme au 554, **le témoin faux désignait l'angle mort** : les gestionnaires
qui **délèguent**. Trois des sept le font.

## Trois autres chiffres faux, arrêtés avant publication

Le lot a produit **quatre** versions successives du même seau — « clés lues par
la page, hors du contrat du serveur ». Les trois premières étaient fausses, et
**toutes fausses dans le sens accusatoire** (548-A) :

```text
version 1   40 clés « hors contrat »   ← espace de noms PLAT du 553
version 2    8 clés « hors contrat »   ← `ast.walk` entrait dans les auxiliaires
version 3    3 clés « hors contrat »   ← seuls les `return` étaient lus
version 4    0 clé  « hors contrat »   ← mesure publiée
```

**1 · L'espace de noms plat du 553.** Le crible du 553 marquait les variables
dans **un seul espace par fichier**. Dans `options-structure.js`, la ligne 24
lie le nom `d` à `/api/options` ; la ligne 439 réutilise `d` pour un
`fetch('/api/pos-quotes')`. Résultat : `d.results` était compté **sur
`/api/options`**, une route qui rend `{board, updated}`. Mesuré : **3 collisions**
(fichier, variable), toutes sur le nom `d` :

```text
/portfolio inline#1   d -> /api/portfolio/context, /api/portfolio/stress, /api/skyler/graph
/journal   inline#1   d -> /api/journal/postmortem, /api/skyler/calibration, /api/skyler/memory
/system    inline#1   d -> /api/system/automations, /api/system/connections, /api/tradingview/signals
```

Le 553 gardait la **dernière** liaison : une route **absorbe** des clés qui ne
sont pas les siennes, une autre est **affamée** des siennes. C'est exactement ce
qu'on observe : `/api/system/automations` recevait 8 clés, `/api/tradingview/signals`
zéro. Un banc de **portée** (la liaison doit englober le site de lecture) ramène
les 43 clés brutes à **12 en portée**.

**2 · `ast.walk` descendait dans les auxiliaires internes.** Sur
`track_record.evaluate`, il rapportait les clés de la fonction interne `agg`
(`avg_1j`, `win_5j`, `tp1_rate`…) au lieu des clés réellement rendues. J'aurais
publié « 5 clés lues hors du contrat » alors que **les 5 sont promises**.

**3 · Un contrat peut être écrit hors de tout `return`.** `startup_report()`
rend `dict(_REPORT)` ; ses clés sont écrites ligne 91 de
`vertex/services/startup.py` par `_REPORT.update({'ran':…, 'ts':…, 'steps':…,
'order_execution':…})`. Un lecteur qui ne regarde que les `return` conclut
« aucune clé promise » — et accuse les 3 clés que la page lit.

**Arrêtés avant publication : 175 → 179 (+4).**

## La mesure

```text
clés lues par les pages sur ces 7 routes, EN PORTÉE          12
   confirmées par le contrat LU                              12
   hors du contrat lu                                         0
-- pour mémoire, le brut du 553 (espace de noms plat)         43
```

| route | lue en portée | promise par le code |
|---|---|---|
| `/api/alerts/active` | `active` | `active`, `status` |
| `/api/options` | `board` | `board`, `updated` |
| `/api/system/automations` | `jobs` | `jobs` |
| `/api/system/config` | — | contrat **dynamique** (une clé par variable d'env) + `_summary` |
| `/api/system/startup-report` | `order_execution`, `steps`, `ts` | écrites par `_REPORT.update` |
| `/api/track-record` | `as_of`, `by_verdict`, `entries`, `note`, `resolved` | les 8 clés de `evaluate` |
| `/api/tradingview/signals` | `signals` | `signals`, `status` |

**Zéro divergence.** Les sept routes que personne ne teste **tiennent le contrat
que la page attend d'elles**, pour tout ce que la lecture peut décider.

## Second contrôle (481) — ce que la lecture ne peut pas décider

```text
retours DÉLÉGUÉS à un appel                          3
   résolus à UN niveau                               3
   non résolus                                       0
retours NON LISIBLES (ni littéral ni appel)          0
clés écrites HORS de tout `return`, par mutation     8
   /api/system/config           `out` : `_summary`
   /api/system/startup-report   `_REPORT` : demo_mode, ok, order_execution,
                                ran, readonly, steps, ts
```

Les deux délégations d'abord non résolues l'étaient pour une raison lisible :
`from vertex.services.startup import startup_report` est écrit **dans** la
fonction, donc invisible depuis `__globals__`. Les deux modules concernés ne
font que des définitions à l'import (lu **avant** de les importer) : aucun
réseau, aucune écriture.

**Limites énoncées** : profondeur **un** niveau ; la portée est syntaxique (la
fonction englobante), pas une vraie analyse de portées JavaScript ; le contrat
de `/api/system/config` est **dynamique** — une clé par variable d'environnement
— donc non comparable clé à clé. **Une clé lue et absente du contrat lu ne serait
PAS déclarée inexistante (550-B)** — le cas ne s'est pas présenté.

## Ce que le dépôt fait bien, mesuré

- **Les 7 routes sans filet tiennent leur contrat** : 12 clés lues, 12 promises.
- **Les pages lisent peu et lisent juste** : une seule clé de premier niveau sur
  quatre des sept routes.
- `validate_config()` **n'expose aucune valeur de secret** — statut, obligation,
  conséquence, et rien d'autre (lu, `config_validation.py`).
- `startup_report()` porte `'order_execution': 'disabled-by-design'` — l'invariant
  READONLY est **inscrit dans le rapport de démarrage**, pas seulement dans le code.

## Portée — ce que ce lot NE dit PAS

- **Ces 7 routes n'ont pas été appelées.** Aucun contrat n'a été observé à
  l'exécution : tout est lu.
- « Le contrat tient » vaut **pour les clés de premier niveau que la page lit en
  portée** — pas pour les valeurs, ni pour les clés imbriquées, ni pour le
  contrat d'échec.
- Les **31 clés** que le 553 attribuait à ces routes et que la portée retire ne
  sont pas « fausses » : elles sont lues **ailleurs**, sur d'autres routes. Le
  553 les rangeait au mauvais endroit.
- **Le seau « hors contrat » du 553 n'a pas été recompté** au-delà de ces 7
  routes : les 3 collisions touchent aussi `/api/portfolio/*`, `/api/journal/*`,
  `/api/skyler/*`. **Constat, non arbitré.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la
  suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier
  apparu ni disparu. *(La première rédaction disait « aucun modifié » : elle
  avait été écrite **avant** le lancement de la suite — 544-D.)*
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Mais ce lot dit quelque chose que les précédents n'avaient pas
dit : **un résultat rassurant a coûté quatre corrections d'instrument.** Les
trois versions fausses accusaient toutes le produit — 40, puis 8, puis 3 clés
« hors contrat » — et la mesure juste en trouve **zéro**. Un instrument
insuffisamment lu ne produit pas du bruit neutre : **il produit des reproches.**

Trois règles neuves :

- **555-A · UN ESPACE DE NOMS PLAT FABRIQUE DES REPROCHES** — un crible qui lie
  `d` à une route et lit tous les `d` du fichier fait **absorber** à une route
  les clés d'une autre, et **affame** la seconde. La liaison doit **englober**
  le site de lecture.
- **555-B · UN CONTRAT N'EST PAS TOUJOURS DANS LE `return`** — celui de
  `/api/system/startup-report` est écrit par `_REPORT.update` dans une autre
  fonction. Ne lire que les `return`, c'est conclure « rien promis ».
- **555-C · `ast.walk` N'EST PAS UNE PORTÉE** — il descend dans les fonctions
  imbriquées et rapporte les clés d'un auxiliaire interne comme si elles étaient
  le contrat.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **le seau « hors contrat » du 553, non recompté hors
de ces 7 routes** ; **les 3 collisions de nom du 553** ; **les 14 candidates, en
attente d'un GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, appelé par `/analysis/<symbole>`, hors corpus** ;
**les 19 clés du contrat non gardé du 553** ; **les 20 candidates du 553** ;
**les 21 tests de membre ambigus du 551** ; **les 128 clés servies non nommées du
552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points d'entrée du
551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43 points
d'entrée couverts par personne** ; **les 11 identifiants de `/intelligence`,
`/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **les
SEPT chiffres lourds encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC serveur,
jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages d'erreur du
541** ; **les 95 atténuations non affichées** ; **`initSettings`** ; **les 8
appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil
prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 179 (+4)** ; publiés
puis corrigés **25** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
