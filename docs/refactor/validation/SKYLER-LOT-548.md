# SKYLER LOT 548 — **L'angle mort total, mesuré pour la première fois : 67 points d'entrée sur 184 ne sont appelés NI par la suite NI par moi.** Et mon détecteur de client a failli en inventer beaucoup plus

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-548` (base : lot 547 fusionné,
`799f1a70`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(r)** — le 546 a mesuré que **mon corpus couvre 8 routes sur 137**. Mais je ne
suis pas le seul filet : **la suite de 2864 tests en couvre certaines**.
Question : **quelles routes ne sont couvertes NI par mes 44 URL NI par un
test ?** Mesure entièrement **statique** — lecture des 301 fichiers de `tests/`
par `ast`, croisée avec `terminal.app.url_map`. **Aucun appel réseau, aucune
route neuve.**

## L'appariement — la leçon du 546-A appliquée d'emblée

Une règle (`/api/decision/<sym>`) et une chaîne de test
(`/api/decision/AAPL`) **ne sont pas le même objet**. On ne compare donc jamais
les chaînes : on apparie par la **règle**, avec
`url_map.bind(…).match(chemin, method=…)`, qui rend le point d'entrée que
Flask choisirait réellement.

## L'arrêt du lot — **mon détecteur de client, en trois erreurs successives**

Il fallait décider ce qu'est un client de test. **Pas par une liste de noms
devinée** (521-B) — et le piège est réel : `tests/test_vault.py:27` contient
`items.get('/vault')`, un accès à un **dictionnaire**. J'ai donc pris un critère
structurel : un nom lié à un `….test_client()`.

**Il était trop étroit, trois fois de suite :**

```text
version 1  ne voyait que `return …test_client()`        112 appels rejetés
version 2  + `yield …test_client()` et `with … as c:`    39 appels rejetés
version 3  + `c = _client()` (point fixe)                26 appels rejetés
version 4  + fixture rendant un TUPLE, `c, tmp = client`  2 appels rejetés
```

**Et l'erreur allait dans le mauvais sens** : chaque appel rejeté à tort
*retire* de la couverture, donc **gonfle l'angle mort**. Publier la version 1
aurait produit un chiffre spectaculaire et faux.

**Arrêtés avant publication : 167 → 168.**

## Les deux bornes, et ce qui les sépare

```text
appels à chemin LITTÉRAL, borne HAUTE (tout `X.verbe('/…')`)      417
appels à chemin LITTÉRAL, borne BASSE (récepteur reconnu client)  415
écart                                                               2
   tests/test_tradingview.py:21  post('/api/tradingview/webhook')
   tests/test_vault.py:27        get('/vault')
```

```text
couverts par PERSONNE, borne BASSE   67
couverts par PERSONNE, borne HAUTE   66
différence                            1   →  redesign.legacy_vault
```

**Les deux bornes ne diffèrent que d'un point d'entrée**, et la lecture le
tranche : `items.get('/vault')` est un accès à un dictionnaire, **pas un appel
HTTP**. `/vault` n'est donc couvert par personne, et **67 est le bon chiffre**.

## La mesure

```text
points d'entrée hors `static`                       184
   couverts par la SUITE de tests                   116
   couverts par MON CORPUS de 44 URL                  9
      dont déjà couverts par la suite                 8
      que moi seul couvre                             1   (`/analysis` nu)
   COUVERTS PAR PERSONNE                             67
```

**Mes 44 URL ne valent que 9 points d'entrée** — les 35 vues sont des chaînes de
requête sur les mêmes routes de page. Le 546 disait « 8 sur 137 » ; c'est
confirmé et précisé.

## Les 67, par famille

```text
redirections héritées (`redesign.legacy_*`)          36
points d'entrée `/api/…`                             27
autres                                                4
   /ibkr · /options/<sym> · /quotes · /weekly-regen
```

**Une partie de cet angle mort est aveugle PAR CONSTRUCTION** : quatre des cinq
routes que je m'interdis d'appeler (réseau sortant) y figurent —
`/api/analyst/<sym>`, `/api/correlations/<sym>`, `/api/ticker/<sym>`,
`/options/<sym>`. La cinquième, `/desc/<sym>`, **est couverte par la suite**.

**La plus grosse famille n'est pas une surface produit** : ce sont les **36
redirections héritées** (`/analyse`, `/bordel`, `/moi`, `/settings`…), dont le
519-A avait déjà nommé trois. Aucun test ne vérifie qu'elles redirigent.

## Ce que le dépôt fait bien, mesuré

- **La suite couvre 116 points d'entrée sur 184** — près des deux tiers, et
  bien au-delà de ce que mon corpus voit.
- **Elle couvre 8 des 9 points d'entrée de mon corpus** : mon travail est un
  sur-ensemble marginal, pas un filet parallèle.
- **415 appels HTTP à chemin littéral** dans 301 fichiers : le filet est dense
  là où il existe.

## Portée — ce que ce lot NE dit PAS

- **« Couvert par personne » est une BORNE HAUTE de l'angle mort** : **90
  appels à chemin construit** (`'/api/skyler/' + s`, variables, f-chaînes) sont
  comptés à part et peuvent couvrir des règles comptées ici comme non
  couvertes.
- **« Couvert » ne veut pas dire « bien testé »** : un point d'entrée appelé une
  fois pour vérifier un code 200 compte autant qu'un point d'entrée éprouvé.
- Les appels via `url_for` ou par un client passé de fonction en fonction
  restent invisibles.
- 3 chemins littéraux ne s'apparient à aucune règle : ce sont des tests de
  404 (`/api/nexiste-pas`, `/page-fantome`) et un test d'échappement.
- **Aucun navigateur, aucune correction engagée, aucune route neuve appelée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés pendant le lot** (`ai_enrichment.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Mais **l'angle mort du produit a enfin un chiffre**, et il n'est
pas celui que je craignais : la suite de tests couvre bien plus que moi, et ce
qui reste est dominé par des **redirections**, pas par des surfaces d'analyse.

Ce qu'il faut dire sans le maquiller : **j'ai dû corriger mon instrument quatre
fois avant qu'il cesse de mentir**, et chaque version intermédiaire aurait
produit un angle mort plus gros que le vrai. Le chiffre spectaculaire était
toujours à portée de main ; c'est la version la moins spectaculaire qui est la
bonne.

Trois règles neuves :

- **548-A · UN INSTRUMENT TROP ÉTROIT FABRIQUE DES TROUS** — rejeter un appel
  légitime *retire* de la couverture, donc *invente* de l'angle mort. Le sens
  de l'erreur compte autant que sa taille.
- **548-B · UN IDIOME DE TEST N'EST PAS UN IDIOME** — `return`, `yield`,
  `with … as`, `c = _client()`, fixture rendant un tuple : cinq façons de
  fabriquer le même objet dans le même dépôt.
- **548-C · QUAND DEUX BORNES NE DIFFÈRENT QUE D'UN CAS, ON LIT CE CAS** —
  `items.get('/vault')` est un dictionnaire ; une ligne lue vaut mieux qu'un
  arbitrage.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 67 points d'entrée couverts par personne, dont
36 redirections héritées — borne haute, à affiner avec les 90 chemins
construits** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge` — en attente d'un GO** ; **les 4 zones sous attente sans annonce
du 545 — candidat, non arbitré** ; **les SEPT chiffres lourds encore NON
RECOMPTÉS** (112 atténuations, 103 états, 53 refus, 178 appels, 156 variables
serveur, 25 fonctions, 11 limites) ; **le contrat d'ÉCHEC serveur, jamais
observé** ; **les 4 noms de clé du 542** ; **les 15 messages d'erreur sans
pourquoi du 541** ; **les 95 atténuations non affichées** ; **`initSettings`** ;
**les 8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42
cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes —
outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 168 (+1)** ; publiés
puis corrigés **23** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
