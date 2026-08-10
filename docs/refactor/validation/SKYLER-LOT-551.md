# SKYLER LOT 551 — L'étendue du filet : **médiane 2 champs JSON nommés, 388 au total, 29 au maximum** — et TROIS arrêts, dont mon compteur qui rangeait un fichier JavaScript en tête des mieux vérifiés

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-551` (base : lot 550 fusionné,
`381ed347`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(w)** — le 550 a dit lui-même sa limite : *« CONTENU ne veut pas dire
COMPLET »*, une seule lecture de `get_json()` suffisant à classer un point
d'entrée au niveau le plus haut. Ce lot compte les **champs réellement nommés**.

**550-B en tête du banc** : ne jamais nommer un seau d'après ce que
l'instrument ne voit pas. Les **formes** (`isinstance`, `len`, comparaison à un
littéral) sont comptées **à part, avant** toute qualification, et **aucun point
d'entrée n'est appelé « pauvre » dans ce rapport**.

## Trois arrêts — et l'instrument s'est trompé dans les deux sens

**1. La contamination ne partait jamais.** Ma première version n'amorçait le
suivi que si le **parent immédiat** de l'appel était une affectation. Or
l'idiome dominant du dépôt est :

```python
j = terminal.app.test_client().get('/cal-feed').get_json()
assert 'macro' in j and isinstance(j['macro'], list)
```

Le parent de l'appel est le `.get_json()`, **pas** l'affectation : `j` n'était
jamais suivi. Effet mesuré en corrigeant : **médiane 1 → 3, total 220 → 577**.
L'erreur faisait paraître la suite **plus mince qu'elle n'est**.

**2. Puis le compteur a gonflé, dans l'autre sens.** `system.service_worker` —
un fichier **JavaScript** — ressortait **en tête** avec 36 « champs » :

```text
'Content-Type', 'Service-Worker-Allowed', 'javascript',
'td-shell-v95', 'td-shell-v96', … 'td-shell-v187'
```

Ce sont **34 recherches de sous-chaîne** dans un corps texte et **2 noms
d'en-tête HTTP**. Un `'x' in corps` n'est pas un champ JSON : **deux prédicats
différents mélangés** (546-A). Le **genre** de la valeur est désormais suivi le
long de la chaîne d'accès (`get_json` → json, `get_data`/`text` → texte,
`headers` → en-têtes), et les trois familles sont comptées séparément.

**3. Une variable de boucle nomme des champs.** `/api/session/manifest`
tombait dans le seau « ni champ ni forme » alors que le test écrit :

```python
for k in ('session_id', 'status', 'coverage_pct', 'quality_pct', 'error', 'generator'):
    assert k in j
```

**Six champs nommés.** C'est la leçon **549-A** — une variable de boucle n'est
pas un inconnu — que je n'avais pas portée jusqu'aux noms de champs.

**Arrêtés avant publication : 170 → 173.**

## La mesure, après les trois corrections

```text
les 112 points d'entrée classés CONTENU au 550
   champs JSON distincts nommés · MÉDIANE                      2
   champs JSON distincts nommés · TOTAL cumulé                388
   maximum sur un point d'entrée                              29   (`/api/skyler`)
   points d'entrée à UN SEUL champ nommé                      11
   points d'entrée à AUCUN champ JSON                         32
```

```text
distribution
        0 champ   32          4 à 7 champs   23
        1 champ   11         8 à 15 champs   10
   2 à 3 champs   32       16 et plus        4
```

```text
les dix plus éprouvés
   29 api_skyler · 18 api_skyler_memory · 16 memory_export · 16 positions_state
   14 memory_import · 13 create_tracking · 12 news_feed · 10 options_analyze
   10 options_gex ·  9 copilot_ask
```

## Les 32 sans champ JSON — **ce ne sont pas des trous**

```text
vérifiés par SOUS-CHAÎNE sur le corps ou par EN-TÊTE          22
vérifiés par une FORME seulement                               4
aucun des quatre — À LIRE, non qualifié                        6
   desc_ep · /analysis (nu) · design_system_page · /tracking
   vx_static · widget_lab
```

**Les 22 sont des pages HTML et des ressources statiques** : leur vérification
passe par la recherche de sous-chaînes dans le corps servi — `aria-current`,
`aria-label`, `/static/vertex/js/vx-router.js`… Demander à une page HTML de
nommer un champ JSON n'a aucun sens ; **le compteur pose la mauvaise question à
ces points d'entrée, et c'est le compteur qu'il faut lire, pas la page**.

Les **6 derniers** sont nommés et **non qualifiés** : ce sont, eux aussi, des
surfaces HTML ou statiques.

## Second contrôle (481) — ce que le compteur ne voit pas

```text
vérifications par SOUS-CHAÎNE sur un corps texte              178
noms d'EN-TÊTE HTTP vérifiés                                   45
accès IMBRIQUÉS comptés comme un champ de surface              85
```

Ces trois familles sont des **vérifications réelles**, comptées à part et
jamais additionnées aux champs. Restent invisibles : les champs nommés **dans
une aide** qui reçoit le JSON, et les compréhensions sur la réponse — **un
point d'entrée peut donc être plus éprouvé que ce compte ne le dit**.

## Ce que le dépôt fait bien, mesuré

- **388 champs JSON distincts sont nommés** par la suite, et **`/api/skyler` en
  nomme 29 à lui seul** — la route de décision la plus lourde du produit est
  aussi la plus éprouvée.
- **La moitié des points d'entrée CONTENU nomment 2 champs ou plus** ; un quart
  en nomme 4 ou plus.
- **178 recherches de sous-chaîne et 45 en-têtes** : les pages HTML sont
  vérifiées par leur contenu servi, pas par leur seul statut.
- **Le test le plus discret nomme six champs d'un coup**, par une boucle sur un
  tuple littéral.

## Portée — ce que ce lot NE dit PAS

- **Nommer un champ n'est pas le vérifier profondément** : `'x' in j` compte
  autant que `j['x'] == 42`.
- **La médiane de 2 porte sur les points d'entrée CONTENU**, pas sur les 184.
- L'agrégation cumule tous les appels d'un même point d'entrée : c'est une
  **union**, pas la richesse d'un test unique.
- **Aucun point d'entrée n'est qualifié de pauvre** (550-B) ; les 6 sans aucune
  trace sont **nommés pour lecture future**, pas jugés.
- **Aucun appel réseau, aucun navigateur, aucune correction engagée.**

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
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. La dernière limite que le 550 s'était interdite est levée, et
elle donne un dépôt **plus solide** que la phrase « couvert ne veut pas dire
testé » ne le laissait craindre.

Ce qu'il faut dire sans le maquiller : **trois arrêts en un lot, tous dans mon
instrument, et deux d'entre eux dans des directions opposées.** Le premier
faisait paraître la suite anémique, le deuxième couronnait un fichier
JavaScript comme le mieux vérifié du produit, le troisième enterrait l'un des
meilleurs tests dans le seau des muets. Chaque fois, c'est la **lecture d'un
cas** — jamais l'intuition — qui a tranché.

Trois règles neuves :

- **551-A · LA CONTAMINATION PART DU BOUT DE LA CHAÎNE, PAS DE L'APPEL** —
  `j = client.get(…).get_json()` : le parent de l'appel n'est pas l'affectation.
- **551-B · UNE SOUS-CHAÎNE N'EST PAS UN CHAMP** — 34 versions de service worker
  comptées comme des champs JSON d'un fichier `.js`.
- **551-C · LA LEÇON D'UN LOT NE SE PORTE PAS TOUTE SEULE** — 549-A disait déjà
  qu'une variable de boucle n'est pas un inconnu ; il a fallu un troisième arrêt
  pour l'appliquer aux noms de champs.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 6 points d'entrée sans aucune trace de
vérification de contenu — à LIRE, non qualifiés** ; **les 15 points d'entrée
vérifiés au statut seul du 550, dont 5 routes de flux** ; **les 43 points
d'entrée couverts par personne** ; **les 11 identifiants de `/intelligence`,
`/tracking` et `pf-risk-gauge` — en attente d'un GO** ; **les 4 zones sous
attente sans annonce du 545** ; **les SEPT chiffres lourds encore NON
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

Comptes séparés : résultats faux **arrêtés avant publication 173 (+3)** ; publiés
puis corrigés **24** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
