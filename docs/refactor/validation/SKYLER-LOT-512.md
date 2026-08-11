# SKYLER LOT 512 — Les 41 routes muettes, lues une par une. **Le brief se trompait : `/api/comite` ne cache rien.** Mais un MOTEUR ENTIER — `context.py`, le classement d'un titre dans son univers — est calculé pour trois routes muettes et n'atteint l'écran sous AUCUNE formulation

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-512` (base : lot 511 fusionné,
`a210817f`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)**, la dette que le 511 avait lui-même créée en écrivant : « Je n'ai pas
classé les 41 par intention. Neuf sont manifestement techniques ; pour les 32
autres je n'ai pas lu chaque handler. » C'est la seule dette ouverte qui puisse
rendre du **produit** plutôt que de l'audit, parce qu'elle sépare deux
conclusions opposées : **déchet** ou **occasion manquée**.

## Ce que le brief affirmait, et ce que la mesure dit

Le brief de ce lot — comme le rapport 511 — avançait que **`/api/comite`,
`/api/committee-review` et `/api/brief` portent des raisonnements de comité que
le produit n'affiche nulle part**. Mesuré, charge utile décodée, scan peuplé :

```text
route muette            chaînes  déjà dans les    déjà reçues par une   INTROUVABLES
                        ≥ 8 car.  OCTETS SERVIS   ROUTE APPELÉE         ailleurs
────────────────────────────────────────────────────────────────────────────────
/api/committee-review        44          15                  1              28
/api/brief                   30          17                  1              12
/api/system/status           20          15                  1               4
/api/cockpit                 35           5                 29               1
/news-feed                    2           1                  0               1
/api/comite                  67           9                 58            ► 0
/api/strategie               19           5                 14            ► 0
/api/watchlist              118          14                104            ► 0
/api/weekly                   0  — charge vide : alimentée par `_weekly_loop()`, jamais démarrée ici
```

**`/api/comite` ne cache rien.** Onze kilo-octets, profondeur 5, soixante-sept
chaînes — et **pas une seule** que le client ne reçoive déjà. Même chose pour
`/api/strategie` (52 ko, profondeur 7) et `/api/watchlist` (39 ko). Le brief se
trompait sur ces trois-là ; je le dis, comme l'avertissement l'exige.

**Deux routes sur neuf confirment la thèse**, pas trois : `/api/brief` et
`/api/committee-review`.

## Le dossier — 512-A · le moteur `context.py`

Les phrases introuvables ne sont pas décoratives. Elles disent **où se situe un
titre parmi tous les autres** :

```text
« Top 2% de l'univers · #1/3 dans Technology »
« Bas 25% de l'univers · #2/3 dans Healthcare »
« Bas 42% de l'univers · #2/2 dans Basic Materials »
```

Leur producteur est `vertex/engines/context.py:52 context_for(sym, detail_map)` —
« Situe `sym` parmi tous les titres scannés : percentiles + rang sectoriel ». Il
calcule, pour chaque dimension, le **percentile dans l'univers** et le
**percentile dans le secteur**, le **rang sectoriel**, les **pairs nommés**, et
une **phrase de situation** (`_headline`).

**Il a exactement un consommateur**, `decision_api.py:46 _ctx_for`, qui alimente
exactement **trois routes — les trois muettes** : `/api/brief`,
`/api/committee-review`, `/api/position-decision/<sym>`.

Mesuré dans le corpus servi (9 pages, page détail incluse, + 33 scripts) :

```text
« de l'univers »   0        « percentile »  0
« #1/ »            0        « quartile »    0
```

**Zéro sous toutes les formulations cherchées.** Le positionnement relatif d'un
titre — l'information qu'un trader regarde en premier pour savoir si une idée
vaut mieux que les autres — est calculé à chaque brief et n'arrive jamais à
l'écran.

## Les 41, par intention

```text
 9  EXPLOITATION — légitime, faite pour un outil ou la main
    /api/healthz · /api/rescan · /api/validator · /api/system/jobs
    /api/live/report · /api/live/events/stats
    /api/positions/audit · /api/positions/reconcile · /api/positions/report

 9  APPELABLES ET MESURÉES  → 2 occasions manquées · 5 contenu déjà chez le
    client · 1 ops (system/status) · 1 non mesurable (weekly)

23  LUES, NON APPELÉES (sûreté réseau non établie) — classées par lecture seule :
    drill-down par entité (12) : /api/vertex/<sym> · /api/events/<sym>
      /api/company/<sym> · /api/company/twin/<sym> · /api/correlations/<sym>
      /api/position-decision/<sym> · /api/positions/<id>/changes
      /api/skyler/graph/<sym> · /api/skyler/memory/<id>
      /api/skyler/memory/cell/<group>/<key> · /api/tracking/<id>
      /api/charts/<chart_id>/interpretation
    suivi hypothétique (3) : /api/tracking/<id>/history · /api/tracking/<id>/performance
      /api/tracking/summary
    autonomes (8) : /api/risk · /api/portefeuille · /api/options-lab
      /api/options/environment · /api/search · /api/watchlist-tv
      /api/alerts/status · /api/strategy/profile
```

`/api/position-decision/<sym>` est le troisième débouché de `context.py` : il est
dans la liste des non appelées, et c'est cohérent avec le dossier.

## Trois arrêts avant publication, dans un seul lot

**1 · La charge utile mesurée SANS SCAN.** Premier passage : `/api/comite` = 3
octets, `/api/strategie` = 3 octets, `/api/weekly` = 3 octets. J'allais publier
« ces routes sont vides ». Elles lisent `scan_state['committee' | 'strategy']` :
**sans scan elles sont vides par construction**. Après `terminal.scan()` :
11 648 et 52 153 octets. C'était mon banc, pas le produit.

**2 · La classe « REDONDANT » bâtie sur des NOMS DE CLÉ.** Premier passage,
`/api/brief` classé *redondant* parce que `breadth`, `setups`, `market`
apparaissent dans le JS servi. **Vingt-huitième récurrence de l'homonyme** : ces
mots y désignent autre chose. Mesuré sur les **contenus**, `/api/brief` est la
deuxième plus grosse occasion manquée du lot. Le crible par nom de clé l'avait
mis dans la case exactement opposée.

**3 · Mon banc comparait des ÉCHAPPEMENTS.** Flask sérialise en ASCII
(`Marché`), les octets servis portent `Marché`. Une phrase présente des deux
côtés ne pouvait pas se reconnaître. Recompté après décodage des deux côtés :

```text
/api/committee-review   31 inédites → 28
/api/brief              13 inédites → 12
```

**L'artefact était réel mais petit, et il n'a renversé aucune conclusion.** Je
publie l'écart plutôt que le seul chiffre corrigé — un contrôle qui ne change
rien mérite d'être montré autant qu'un contrôle qui renverse.

**Arrêtés avant publication : 100 → 103.**

## Le second contrôle — le cas que l'instrument EXCLUT (règle 481)

Mon instrument conclut « occasion manquée » quand le **texte** est introuvable.
Il exclut par construction le cas où **l'information est à l'écran sous une autre
formulation**, produite par un autre moteur. Si ce cas s'appliquait, « occasion
manquée » deviendrait « doublon reformulé ».

Vérifié par lecture, pas par présence de mot : le seul producteur de percentile
d'univers dans tout le dépôt est `context.py`, `context_for` n'a qu'un
consommateur, et aucun des quatre vocabulaires possibles (`percentile`,
`de l'univers`, `#n/`, `quartile`) n'existe dans les octets servis.
**L'exclusion ne s'applique pas ici** — mais c'est une lecture qui l'établit, pas
le crible.

Témoin positif du même contrôle : le concept « régime », dont je sais qu'il est
peint, ressort sous **quatre** formulations différentes dans le corpus servi
(`régime` 35, `regime` 69, `TREND` 6, `RISK-ON` 1). L'instrument sait donc voir
une information reformulée quand elle existe.

## Classement — rang 4

L'étalon reste le **454** puis le **511-A** : *rien de faux n'est montré, et
c'est pour cela que ce n'est pas plus haut.* Ici non plus aucun chiffre erroné
n'est peint — le classement d'univers n'est simplement jamais peint.

Ce qui distingue **512-A** de son parent 511-A, c'est la **précision** : le 511
disait « 41 routes ne sont pas demandées » ; le 512 nomme **un moteur, un
fichier, une fonction, une phrase utilisateur déjà rédigée** et trois routes qui
la portent. C'est le premier élément de la veine qui soit **directement
actionnable en produit** sans rien réécrire : la phrase existe, il ne manque
qu'un consommateur.

Correction pressentie, non engagée : afficher `context.headline` sur la fiche
d'un titre. **Aucun GO, rien n'est engagé, et NE RIEN SUPPRIMER** — le 511 le
disait déjà, ce lot le confirme : sur les neuf routes mesurées, **deux** sont des
occasions manquées et **aucune** n'est du déchet établi.

## Portée — ce que ce lot NE dit PAS

- **« Déjà reçue par une route appelée » n'est pas « affichée ».** Pour
  `/api/comite`, 58 chaînes sur 67 arrivent au client via `/scan` ; qu'il les
  peigne est une autre question. Ma conclusion exacte est : **brancher
  `/api/comite` n'apporterait pas d'information neuve au client**, pas qu'elle
  soit visible.
- **Seules 9 des 41 ont été MESURÉES.** Les 23 non appelées sont classées par
  **lecture du handler**, ce que le lot demandait — mais lire une intention n'est
  pas mesurer un contenu. Leur classement est plus faible d'un cran, et je ne le
  déguise pas.
- **`/api/weekly` n'est pas jugée.** Sa charge vient de `_weekly_loop()`, une
  boucle de fond que je n'ai pas le droit de démarrer. Vide ici ≠ vide en
  production.
- Le crible de couverture cherche une **égalité de chaîne**. Une même information
  reformulée mot pour mot autrement lui échappe ; c'est précisément pour cela que
  le second contrôle a été fait **par lecture**.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.** Les 32 routes
  hors liste sûre n'ont **pas** été appelées, seulement lues.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les quatre bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4**. Deux lots de rang 4
d'affilée : la veine ne rend plus de défaut grave, elle rend des **occasions
manquées**. C'est un changement de nature, pas une baisse de rendement — et le
512 est le premier depuis longtemps dont la suite naturelle est **d'ajouter
quelque chose à l'écran** plutôt que de corriger un calcul.

Le lot corrige aussi une affirmation que j'avais moi-même propagée sur deux lots
(`/api/comite` porterait un raisonnement caché). Elle est fausse, mesurée à zéro.

Feuille : **33 dossiers · seize rang 1 · onze rang 2 · cinq rang 3 · deux rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **mesurer le
contenu des 23 routes non appelées** (dette neuve — elles sont lues, pas
mesurées) ; **un producteur de synthèse d'une autre forme** ; **l'espion au
troisième niveau** (toujours déconseillé) ; **le compte des rangs relatifs
postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 103 (+3)** ; publiés
puis corrigés **13** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
