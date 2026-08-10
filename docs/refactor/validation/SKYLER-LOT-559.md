# SKYLER LOT 559 — les « 21 tests de membre ambigus » : **mal attribués depuis sept rapports, et huit d'entre eux ne testent pas une réponse HTTP du tout**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-559` (base : lot 558 fusionné,
`aa883fad`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — tout est lu :
les fichiers de tests par `ast`, les vues par `url_map` et `inspect`.

## Le choix

**(ee)** — encore une dette laissée à l'état de nombre depuis huit lots, et le
557-A vaut pour elle : **un chiffre non nul du second contrôle est une dette**.

## Premier arrêt — **la dette est mal attribuée depuis sept rapports**

La liste de dettes des rapports **552 à 558** dit « les 21 tests de membre
ambigus **du 551** ». Vérification : le rapport 551 **ne contient ni le nombre 21
ni le mot « ambigu »** à ce sujet. Les 21 ont été mesurés **au 552**, comme une
conséquence *sur* le chiffre du 551. **Sept rapports ont propagé
l'attribution.**

Et la définition du brief était fausse aussi. Il parlait d'assertions où l'on ne
saurait dire si `x` est une clé, une sous-chaîne **ou un élément de liste**. Le
552 dit précisément autre chose (lu dans son banc) :

```text
MEMBRE DE RACINE    'x' in j          appartenance à un dictionnaire   35, NON ambigus
SUR ACCÈS IMBRIQUÉ  'x' in j[…][…]    dictionnaire OU chaîne           21, AMBIGUS
```

Le banc de ce lot **reproduit exactement 35 / 21** avant de recompter — sinon il
s'arrête (546-A, 556-B).

## Deuxième arrêt — mon premier classement était une collision, pas une lecture

J'ai d'abord cherché le producteur de chaque clé receveuse **dans tout le
dépôt**. Résultat : `note` a **93** producteurs, `label` **100**, `reason`
**60** — et 18 des 21 ressortaient « indécidables ».

**C'est l'espace de noms plat du 553 (555-A), transposé en Python.** Un nom de
clé cherché globalement n'est pas une lecture de contrat. Publier « 18
indécidables » aurait été un chiffre sans objet.

Resserré au **module de la route** (route → `url_map` → vue → module + modules
`vertex.*` qu'il importe), le même classement donne : 3 chaînes, 3 indécidables,
15 sans producteur dans ce module.

**Arrêtés avant publication : 183 → 185 (+2).**

## L'arrêt qui compte — **huit des 21 ne testent pas une réponse HTTP**

Lu dans `tests/test_anomaly_engine.py:25` :

```python
def test_calm_series_has_no_spikes():
    d = anomaly.scan(_flat(40))
    assert 'Aucun mouvement statistiquement anormal' in d['narrative']
```

**`d` n'est pas une réponse** : c'est le retour direct du moteur. Le banc du 552
marque les noms de variables **par FICHIER, pas par fonction** — un autre test
du même fichier fait `d = client.get(…).get_json()`, et ce marquage a suffi.
**Encore l'espace de noms plat, cette fois dans le banc du 552 lui-même.**

```text
les 21 « tests de membre sur une valeur JSON »
   sur une VRAIE RÉPONSE HTTP                        13
   sur un APPEL DIRECT à un moteur — hors sujet       8
      `anomaly.scan` ×3 · `stress.build` ×3 · `pretrade.build` ×2
```

**Correction d'un chiffre publié : les 21 ambigus du 552 sont 13.** Le rapport
552 n'est pas réécrit — la correction est portée ici, en ajout. Sa conclusion
(« 388 est une borne haute, 367 un plancher ») **repose donc sur 21 là où
treize seulement sont en cause** ; le plancher exact n'est pas recalculé dans ce
lot, faute d'avoir remesuré le corpus du 551.
**Publiés puis corrigés : 28 → 29 (+1).**

## Ce que la lecture décide, sur les 13 vrais cas

```text
CHAÎNE — sous-chaîne, pas une clé                    3
   /api/skyler/memory/export  note
   /api/portfolio/team        usage  ×2
INDÉCIDABLE — producteurs de natures mélangées       3
   /api/portefeuille          label
   /api/data-quality          by_quality
   /api/positions/reconcile   note
aucun producteur dans le module de la route          7
   /api/options-for/…  note · /news-feed  title · /news-feed  err
   /api/market/context  dimensions · /api/skyler/…  weights
   /api/portfolio/stress  reason · /api/live/refresh  answer
```

**La lecture ne tranche que 3 des 13.** C'est le résultat, et il est modeste. Il
faut le dire ainsi plutôt que de gonfler un seau : **dix cas restent ouverts**,
et aucun n'est déclaré être une chose plutôt qu'une autre (550-B).

## Second contrôle (481) — ce que la lecture ne décide pas

```text
clés receveuses sans producteur DANS LE MODULE de leur route      7
clés aux producteurs de natures mélangées                          3
tests portant sur un appel direct, hors du périmètre « réponse »   8
```

**Un producteur littéral n'est pas une preuve d'unicité** : une même clé peut
être remplie ailleurs par une valeur calculée, hors de tout dictionnaire
littéral. Et la recherche s'arrête au module de la route plus ses imports
`vertex.*` directs — **un producteur situé deux niveaux plus loin n'est pas
vu**.

## Ce que le dépôt fait bien, mesuré

- **Les 35 tests de membre sur la racine ne sont pas ambigus** : ce sont bien des
  appartenances à un dictionnaire.
- Les 8 cas « hors sujet » sont de **vrais tests de moteur** — ils vérifient la
  prose déterministe (`narrative`, `reason`) produite sans appel réseau.
- `anomaly.scan` rend `'narrative': ' '.join(parts)` : une **chaîne assemblée à
  partir de constantes**, jamais un texte inventé.

## Portée — ce que ce lot NE dit PAS

- **Le plancher du 551 n'est pas recalculé.** Savoir que les 21 sont 13 ne suffit
  pas : il faudrait remesurer le corpus de champs du 551.
- **Aucun des 10 cas non tranchés n'est déclaré clé ni sous-chaîne.**
- La résolution s'arrête au module de la route et à ses imports directs.
- **Aucune route appelée, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0**.

Aucun dossier. Trois lots d'affilée ont trouvé **le même défaut sous trois
formes** : un espace de noms plat. Au 555 dans le crible JavaScript du 553, au
559 dans mon propre classificateur Python, et **au 559 encore dans le banc du
552 lui-même**, qui marquait les variables par fichier.

Ce qu'il faut en tirer sans se ménager : **je répare l'instrument au niveau où
le défaut apparaît, jamais au niveau où il vit.** Le défaut vit dans une
habitude — nommer par identifiant plutôt que par lieu — et il ressort dans
chaque banc que j'écris tant que je ne l'écris pas dans la méthode.

Trois règles neuves :

- **559-A · UNE DETTE SE VÉRIFIE À SA SOURCE AVANT D'ÊTRE PAYÉE** — « les 21 du
  551 » ont voyagé dans sept rapports sans que le 551 les ait jamais publiés.
- **559-B · UN NOM DE CLÉ CHERCHÉ GLOBALEMENT N'EST PAS UNE LECTURE DE
  CONTRAT** — `note` a 93 producteurs ; le lieu fait la mesure, pas le nom.
- **559-C · MARQUER PAR FICHIER PLUTÔT QUE PAR FONCTION FAIT ENTRER DES VALEURS
  QUI N'ONT RIEN À FAIRE LÀ** — 8 des 21 sont des retours de moteur, pas des
  réponses HTTP.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 10 cas non tranchés sur les 13** ; **le
plancher du 551, non recalculé** ; **les 16 sous-clés du 558, dont 12 sur des
routes au contrat non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes
ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28 candidates** ;
**les 6 clés sans lecture observée** ; **les 26 routes à lectures ambiguës** ;
**les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ; **les 5 routes
affamées du 556** ; **les 14 candidates du 554, en attente d'un GO** ; **les 4
routes construites `/api/options/…` et les 3 préfixes illisibles** ;
**`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du 554/555** ; **les
128 clés servies non nommées du 552** ; **`/api/weekly` rend un objet vide en
DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points d'entrée au statut
seul du 550** ; **les 43 points d'entrée couverts par personne** ; **les 11
identifiants de `/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones
sous attente du 545** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** ; **le
contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les
15 messages d'erreur du 541** ; **les 95 atténuations non affichées** ;
**`initSettings`** ; **les 8 appels hors de toute fonction** ; **les 36 accès DOM
non suivis** ; **la définition du corpus de routes du 511-A** ; **l'ampleur du
518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les
33 identifiants reconstruits** ; **les 92 rapports non additionnés du 526** ;
**les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 185 (+2)** ; publiés
puis corrigés **29 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
