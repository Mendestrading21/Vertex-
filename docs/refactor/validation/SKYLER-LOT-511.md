# SKYLER LOT 511 — Instrument NEUF : « producteur sans consommateur ». **Quarante et une routes de données sur cent trois — 39,8 % — ne sont demandées par aucun octet servi.** Et j'ai dû corriger mon propre chiffre TROIS FOIS avant d'y arriver

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-511` (base : lot 510 fusionné,
`58c6eb3b`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)**, l'instrument neuf, né d'une dette que le 510 avait lui-même créée. Le
507 avait montré qu'`iv_unit`, `iv_detected_from` et `warnings` sont produits et
lus par personne — pour **une** famille de clés, sur **une** page. La question
transversale n'avait jamais été posée :

> **quelle part de ce que le serveur calcule n'atteint jamais l'écran ?**

## La réponse

```text
routes de données exposées en GET (app.url_map, hors /static)      103
citées dans les octets servis (9 pages + 33 scripts)                62
JAMAIS citées                                                       41   (39,8 %)
```

Le constat est **immune à l'angle mort principal** de ce genre de mesure : il ne
dépend d'aucun nom de clé, seulement d'une URL.

## Les quarante et une — et une nuance que je ne masque pas

```text
produit (32)   /api/cockpit · /api/watchlist · /api/watchlist-tv · /api/brief
               /api/comite · /api/committee-review · /api/strategie · /api/weekly
               /news-feed · /api/system/status · /api/risk · /api/search
               /api/portefeuille · /api/options-lab · /api/options/environment
               /api/events/<sym> · /api/vertex/<sym> · /api/tracking/* …
exploitation (9)  /api/rescan · /api/system/jobs · /api/validator · /api/healthz
               /api/positions/audit · /api/positions/reconcile · /api/positions/report
               /api/live/report · /api/live/events/stats
```

**Une route d'exploitation n'est pas du gâchis** : elle est faite pour être
appelée à la main ou par un outil. Je les sépare plutôt que de gonfler le
chiffre. **Le 39,8 % est donc une borne haute de ce qu'on pourrait appeler du
travail perdu ; la part « produit » est de 32 sur 103, soit 31 %.**

Et je n'ai **pas** classé les 41 une par une par intention — seulement écarté les
neuf manifestement techniques. Le reste demanderait de lire chaque handler.

## J'ai corrigé mon propre chiffre TROIS FOIS

C'est l'histoire de ce lot, et elle vaut le résultat.

```text
1er jet   197 clés muettes / 399   = 49,4 %
          ← FAUX : mon collecteur comptait les CLÉS DE MAP comme des noms de
            champ. Les 133 « muettes » de /scan étaient des TICKERS (ABBV, ABNB…),
            et ACHETER / RENFORCER / AVOID des étiquettes de verdict. Ce sont des
            entrées de dictionnaire lues dynamiquement, pas des champs calculés
            pour rien.                                    (leçon 501)

2e jet    173 / 372 champs réels   = 46,5 %
          ← toujours fragile : « jamais lu » suppose une lecture LITTÉRALE.

3e jet    au niveau ROUTE : 49 / 103 = 47,6 %
          ← FAUX : mon corpus servi n'avait que /analysis (l'index), pas
            /analysis/<sym> (le détail) — pourtant établi comme servi dès le 502.
            Huit routes en dépendaient.

4e jet    41 / 103 = 39,8 %   ← corpus complet, page détail incluse
```

Les huit routes récupérées par la page détail : `/api/analyst/<sym>`,
`/api/anomalies/<sym>`, `/api/decision/<sym>`, `/api/evidence/<sym>`,
`/api/options-for/<sym>`, `/api/skyler/<sym>`, `/api/strategy/decision/<sym>`,
`/api/ticker/<sym>`.

**Arrêtés avant publication : 97 → 100.**

## Le second contrôle — il borne le crible par clé, et le disqualifie

Le comptage par clé suppose `.cle`, `['cle']` ou `cle:`. Or le JS lit aussi sans
écrire le nom :

```text
Object.entries(                     20
Object.keys(                        55
Object.values(                       6
destructuration { a, b } =         126
accès calculé  d[k]                705
                            TOTAL  912
```

**Neuf cent douze constructions** peuvent consommer une clé sans la nommer. Le
« 173 champs jamais lus » est donc une **borne supérieure**, pas un compte — et
c'est précisément pourquoi j'ai basculé sur la mesure au niveau **route**, qui
n'a pas ce défaut. **Le chiffre que je publie est celui des routes, pas celui des
clés.**

## Un piège d'homonyme, vingt-septième récurrence

`/api/brief` apparaît **deux fois** dans les octets servis… à l'intérieur de
`/api/briefing/editorial`, **une autre route**. Une recherche par sous-chaîne
nue l'aurait compté « appelé ». C'est mon compteur strict (préfixe + délimiteur)
qui avait raison, et ma vérification « plus large » qui produisait le faux
positif. **Collision de préfixe** — une forme d'homonymie que la veine n'avait
pas encore rencontrée.

## Ce que le résultat éclaire ailleurs

`/news-feed` est **jamais appelé** par les octets servis. Or `CLAUDE.md` en fait
une **règle critique n°5** (« toujours via `news_plus.sanitize_news()` car leurs
consommateurs injectent le titre brut en innerHTML ») et un gardien la protège
(`tests/test_xss_exits_lot177.py`). **Le gardien protège une sortie que personne
ne demande.** Je ne touche à rien — un gardien qui protège une route inutilisée
reste utile le jour où elle le redevient — mais l'écart documentation/réalité est
du même genre que celui du 381 sur `vx_kit`.

## Classement — rang 4

L'étalon est le **454** : *une conséquence CALCULÉE, SÉRIALISÉE et ENVOYÉE n'est
toujours pas AFFICHÉE*, **rang 4**, motif « rien de faux n'est montré, et c'est
pour cela que ce n'est pas plus haut ».

**Ici non plus rien de faux n'est montré.** Aucune de ces 41 routes ne peint un
chiffre erroné : elles ne peignent rien du tout. C'est du **poids mort d'API**,
pas un défaut d'affichage. Ce qui le distingue d'une simple curiosité, c'est
**l'échelle mesurée** — 31 % de la surface de données côté produit — et le fait
que chaque route non appelée reste un contrat à maintenir, à tester et à sécuriser.

**Pas plus haut** : aucune donnée fausse, aucun ordre, READONLY intact, et une
partie du lot est explicitement de l'exploitation légitime.

Correction pressentie, non engagée : décider route par route entre **retirer** et
**brancher** — plusieurs de ces routes (`/api/comite`, `/api/committee-review`,
`/api/brief`) portent des raisonnements de comité que le produit n'affiche nulle
part, ce qui est peut-être une occasion manquée plutôt qu'un déchet. **Aucun GO,
rien n'est engagé, et surtout : NE RIEN SUPPRIMER.**

## Portée — ce que ce lot NE dit PAS

- **« Jamais cité » n'est pas « jamais appelé ».** Une route peut être appelée
  par le service worker, un signet, un outil externe, ou l'utilisateur tapant
  l'URL. Je mesure ce que **les octets servis demandent**, rien d'autre.
- **Je n'ai pas classé les 41 par intention.** Neuf sont manifestement
  techniques ; pour les 32 autres je n'ai pas lu chaque handler.
- Le comptage **par clé** (46,5 %) est **abandonné au profit du comptage par
  route** — les 912 constructions dynamiques le rendent non concluant. Je le
  publie comme borne, pas comme mesure.
- Les routes **POST** ne sont pas dans le périmètre (seul GET).
- **Aucun navigateur, aucun POST, aucune route interdite appelée.** Le corpus est
  obtenu par `test_client`, `persist` redirigé et vérifié.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**L'instrument neuf a rendu un chiffre**, ce que les deux lots précédents
n'avaient pas fait. La question « combien le serveur calcule-t-il pour rien ? »
a maintenant une réponse : **41 routes de données sur 103, dont 32 côté produit.**

Mais le vrai enseignement de ce lot est ailleurs : **j'ai publié quatre chiffres
successifs et corrigé les trois premiers moi-même**, dont deux par des artefacts
de mon propre collecteur (clés de map, corpus incomplet). Sans le second contrôle
j'aurais publié 49,4 % — faux d'un quart. La série des règles 501, 507-A, 510-B
a servi trois fois dans un seul lot.

Feuille : **32 dossiers · seize rang 1 · onze rang 2 · cinq rang 3 · un rang 4**.

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **classer les
41 routes muettes par intention** (dette neuve) ; **un producteur de synthèse
d'une autre forme** ; **l'espion au troisième niveau** (toujours déconseillé) ;
**le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 100 (+3)** ; publiés
puis corrigés **13** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
