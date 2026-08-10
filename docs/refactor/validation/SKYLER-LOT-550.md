# SKYLER LOT 550 — La profondeur du filet, enfin mesurée : **112 points d'entrée sur 141 sont vérifiés au CONTENU, 29 au statut seul, ZÉRO au néant.** Et j'ai failli calomnier quinze des meilleurs tests du dépôt

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-550` (base : lot 549 fusionné,
`fb89103d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(u)** — les lots 548 et 549 ont établi **qui appelle quoi**. Ils ont écrit,
deux fois, que *« couvert » ne veut pas dire « bien testé »* — **sans jamais le
mesurer**. Ce lot mesure la **profondeur**, entièrement en statique.

Trois niveaux, écrits **avant** de mesurer : **RIEN** (le résultat n'est jamais
lu) · **CODE** (`status_code` seul) · **CONTENU** (le corps ou les en-têtes).
Ranger `headers`/`location` en CONTENU est un **choix**, et il est dit :
vérifier une redirection par son en-tête `Location` est plus qu'un code.

## L'arrêt du lot — **« RIEN » était un mauvais nom, et il accusait à tort**

Le crible a rendu **15 appels dont le résultat n'est jamais lu**. Publier
« quinze appels ne vérifient rien » aurait été une accusation. Trois cas lus
**avant** de publier :

```python
# tests/test_command_routes.py:94
client.get('/api/portefeuille?capital=999999999')
assert seen['capital'] == command.CAPITAL_MAX      # ← effet de bord, monkeypatch

# tests/test_session_api_lot175.py:59
client.get('/api/session/digest'); client.get('/api/session/digest')
assert writes.count('session_digest_cache.json') == 1   # ← écriture de cache

# tests/test_desk_cycle_lot84.py:45  (dans un `finally`)
client.post('/api/desk', json={…})                 # ← remise en état, pas un test
```

**Mon échelle ne voit que la RÉPONSE. Elle est aveugle aux assertions sur EFFET
DE BORD** — qui sont ici *plus fortes* qu'une lecture du corps : elles vérifient
le bornage serveur et l'écriture de cache.

Plutôt que de retirer ces cas à la main (**547-B**), je les ai **mesurés** :

```text
appels dont le résultat n'est jamais lu                    15
   suivis d'au moins une assertion dans la fonction        11   (effet de bord)
   sans aucune assertion après eux                          4
      dont RENDUS par une aide (`return client.post(…)`)    3   (l'assertion est chez l'appelant)
      inexpliqués                                           1
```

Le dernier, lu : `tests/test_desk_cycle_lot84.py:45`, un `post` de **remise en
état dans un `finally`**. Ce n'est pas une vérification faible : ce n'est pas
une vérification du tout.

**Aucun des 15 n'est un test faible. Zéro appel faible sur 437.**

**Arrêtés avant publication : 169 → 170.**

## La mesure

```text
appels suivis (chemin résoluble, récepteur reconnu client)     437
   CONTENU   (corps ou en-têtes vérifiés)                      375
   CODE      (statut seul)                                      47
   résultat non lu (tous expliqués ci-dessus)                   15
```

Ce **437** est la somme exacte des **415** appels littéraux du 548 et des **22**
appels résolus par boucle du 549 — les trois lots s'additionnent.

```text
par point d'entrée
   atteints par un appel suivi                                 141
      CONTENU                                                  112
      CODE seul                                                 29
      RIEN                                                       0
   non atteints                                                 43
```

## Un contrôle croisé que je n'attendais pas

Les **43 points d'entrée non atteints** de ce lot sont **exactement le même
ensemble** que les 43 du 549 : zéro écart dans les deux sens. Deux instruments
écrits pour deux questions différentes — la couverture, puis la profondeur —
tombent sur la même liste.

## Les 29 vérifiés au statut seul — la vraie trouvaille du lot

```text
redirections héritées                    14
autres                                   15
   /api/cockpit · /api/comite · /api/options · /api/strategie · /api/weekly
   /api/risk · /api/validator · /api/vertex/<sym> · /api/names
   /api/client-log · /api/tradingview/webhook
   /api/tracking/<id>/restart · /stop · /history · /performance
```

Pour les redirections, un 200 après redirection est à peu près tout ce qu'on
peut demander. **Mais cinq des routes de flux que les pages du produit
consomment — `cockpit`, `comité`, `options`, `stratégie`, `weekly` — ne sont
vérifiées que par leur code de statut.** Une réponse vide, ou un contrat de
données changé, passerait.

**Ce constat n'est pas arbitré et n'entre pas dans le relevé** : c'est un
CONSTAT, borné à quinze points d'entrée hors redirections, et **rien n'est
corrigé** — écrire un test est une modification de production, qui demande un
GO.

## Second contrôle (481) — ce que le suiveur ne voit pas

```text
appels dont le résultat est TRANSMIS à une fonction            0
```

**Ce zéro a été vérifié, pas supposé.** Une recherche a trouvé un seul candidat
au motif « aide qui reçoit une réponse » — `_no_nan(r)` dans
`tests/test_redteam_repricing_lot21.py:143` — et la lecture montre que `r` y
vient de `RT.review(…)`, **un moteur en processus, pas une réponse HTTP**.

Un défaut latent de l'instrument a tout de même été corrigé au passage : le
drapeau « transmis » était perdu dès que la variable était **aussi** lue. **La
valeur publiée est inchangée** — c'est pourquoi ce n'est pas compté comme un
arrêt.

## Ce que le dépôt fait bien, mesuré

- **112 points d'entrée sur 141 sont vérifiés au contenu** — près de huit sur
  dix.
- **Zéro point d'entrée appelé sans que rien ne soit vérifié.**
- **Les tests les plus discrets sont les plus exigeants** : ceux qui n'ouvrent
  jamais la réponse vérifient le bornage du capital côté serveur et le nombre
  d'écritures de cache.
- **Les aides rendent la réponse** au lieu d'assener leurs propres assertions :
  un idiome propre, que seul un lecteur d'arbre distingue d'un test creux.

## Portée — ce que ce lot NE dit PAS

- **CONTENU ne veut pas dire COMPLET** : lire `get_json()` une fois suffit à
  classer un point d'entrée au niveau le plus haut. Ce lot mesure la
  **nature** de la vérification, pas son **étendue**.
- L'agrégation par point d'entrée retient le **niveau le plus profond** observé.
  Un point d'entrée appelé vingt fois superficiellement et une fois en
  profondeur ressort CONTENU.
- Les 33 appels sans liaison lisible du 549 restent hors du corpus suivi.
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
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Une phrase répétée deux fois sans preuve — « couvert ne veut pas
dire testé » — est enfin chiffrée, **et elle est plus favorable au dépôt que je
ne l'attendais**.

Ce qu'il faut dire sans le maquiller : **j'avais quinze coupables et pas un seul
n'était coupable.** Mon échelle mesurait la lecture de la réponse et appelait
« rien » tout ce qu'elle ne voyait pas ; les quinze appels vérifiaient un effet
de bord, rendaient la réponse à leur appelant, ou remettaient le dépôt en état.
Le seul défaut trouvé dans ce lot était dans mon instrument.

Trois règles neuves :

- **550-A · UNE ASSERTION PEUT PORTER AILLEURS QUE SUR LA RÉPONSE** — bornage
  serveur, écriture de cache : les tests les plus exigeants n'ouvrent jamais le
  corps.
- **550-B · UN SEAU NOMMÉ « RIEN » EST UNE ACCUSATION** — nommer un niveau
  d'après ce que l'instrument ne voit pas, c'est publier son propre angle mort
  comme un défaut du dépôt.
- **550-C · DEUX INSTRUMENTS QUI TOMBENT SUR LE MÊME ENSEMBLE VALENT MIEUX
  QU'UN TOTAL** — les 43 du 549 et les 43 du 550 coïncident exactement.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 15 points d'entrée hors redirections vérifiés
au statut seul, dont 5 routes de flux consommées par les pages — constat, non
arbitré** ; **les 43 points d'entrée couverts par personne, dont 20 redirections
héritées** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge` — en attente d'un GO** ; **les 4 zones sous attente sans annonce
du 545** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** (112 atténuations,
103 états, 53 refus, 178 appels, 156 variables serveur, 25 fonctions, 11
limites) ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé
du 542** ; **les 15 messages d'erreur sans pourquoi du 541** ; **les 95
atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 170 (+1)** ; publiés
puis corrigés **24** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
