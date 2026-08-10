# SKYLER LOT 521 — **Trois instruments, trois échecs de calibration sur le même témoin.** On ne prouve pas statiquement qu'une route ne sort pas sur le réseau — voilà pourquoi cette dette dort depuis neuf lots. Alors j'ai construit le **verrou** qui la débloquera

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-521` (base : lot 520 fusionné,
`a4371d20`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. AUCUNE des 23 routes appelée.**

## Le choix

**(a)** — la dette du 512, **ouverte depuis neuf lots**, la plus ancienne non
entamée : mesurer le contenu des 23 routes que personne n'appelle. Le 512 les a
**lues**, pas **mesurées**, et qualifie lui-même ce classement de « plus faible
d'un cran ».

Le blocage a toujours été le même : **plusieurs de ces routes sont hors liste
sûre**. Avant de mesurer, il fallait établir leur innocuité réseau. C'est ce
préalable que ce lot a attaqué — et c'est lui qui a résisté.

## Trois instruments, trois échecs, le même témoin

Chaque crible a été calibré sur **deux réponses connues d'avance** :
`/api/correlations/<sym>`, interdite depuis des dizaines de lots parce qu'elle
sort sur le réseau, doit ressortir **RÉSEAU** ; `/api/system/status`, appelée
sans dommage au 512, doit ressortir **HORS RÉSEAU**.

### I · Le graphe d'appel par NOM de fonction

```text
CALIB POSITIF  /api/correlations/<sym>  → RÉSEAU  ['yf.T', 'yfinance']      OK
CALIB NÉGATIF  /api/system/status       → RÉSEAU  ['socket', 'yfinance']    ÉCHEC
```

Cause : `fonctions_de(nom)` résout les appels **par nom, partout dans le dépôt**.
Une fonction homonyme dans un module sans rapport, et le graphe explose — 284
modules atteints pour `/api/correlations`, 39 pour une route qui n'en touche
qu'une poignée. **Collision de noms**, famille 511-C / 519-A.

### II · Le graphe des IMPORTS de modules

Reconstruit sans collision possible : fermeture transitive des `import`.

```text
CALIB NÉGATIF  /api/system/status  → RÉSEAU  ['requests (via vertex.ai.briefs)']  ÉCHEC
```

Cause, plus profonde : **importer un module n'est pas exécuter son réseau.** Un
handler qui importe `vertex.app.state` atteint, de proche en proche, un module
qui importe `requests` — sans jamais l'appeler. La fermeture transitive des
imports est structurellement trop grossière.

### III · La délégation vers la liste sûre accumulée

Troisième approche : ne pas prouver, mais **reprendre** — vingt-cinq lots ont
établi des fonctions de moteur appelables en processus ; un handler qui délègue à
l'une d'elles est mesurable.

```text
premier compte    16 routes « mesurables » sur 23
après nettoyage    2
```

Cause : j'avais mis **`get`** dans la liste sûre. Il collisionne avec
`dict.get`, `args.get`, `scan_state.get`, `repo.get`, `p.get`, `d.get` —
c'est-à-dire avec **presque toute ligne de Python du dépôt**. Mon « 16 » comptait
des accès de dictionnaire.

**Il reste deux routes** délégant réellement à un moteur reconnu :
`/api/position-decision/<sym>` → `decision_stack.evaluate` et `/api/risk` →
`portfolio_risk.build`.

**Arrêtés avant publication : 118 → 121.** Trois, dans un seul lot, tous
attrapés par leur propre témoin négatif.

## Ce que ces trois échecs établissent

**On ne démontre pas statiquement, à cette granularité, qu'un chemin d'exécution
ne sortira pas sur le réseau.** Ce n'est pas un défaut de soin : c'est une limite
de la méthode. Un appel se résout à l'exécution ; un import ne dit rien de ce qui
est appelé ; un nom de fonction ne dit rien du module.

**C'est la réponse à une question que je ne m'étais jamais posée : pourquoi cette
dette dort-elle depuis neuf lots ?** Parce que son préalable — la sûreté — n'est
pas établissable par les moyens que j'employais. Je la recommandais lot après
lot sans voir que je recommandais une impasse.

## La sortie par le haut : ne pas prouver, IMPOSER

Le problème se renverse. Au lieu de démontrer qu'une route **ne sortira pas**,
**empêcher toute sortie** : un verrou de processus qui fait lever
`socket.socket`. La sûreté devient vraie **par construction** — et mieux, l'échec
devient l'information : une route qui tente de sortir lève, ce qui **prouve** sa
dépendance réseau au lieu de la supposer.

Ce lot **construit et valide ce verrou** :

```text
CALIB 1 · LE VERROU BLOQUE          création de socket → levée              OK
CALIB 2 · N'ABÎME PAS LE SÛR        5 / 5 routes sûres répondent 200        OK
             /api/system/status 200 · /healthz 200 · /api/market/regime 200
             /api/portfolio/context 200 · /api/positions/state 200
CALIB 3 · RÉVERSIBLE                socket recréé après retrait             OK
```

**Cinq routes sûres continuent de répondre 200 verrou posé** : le verrou
n'ampute pas le produit, il ne coupe que la sortie.

**Je ne l'applique à AUCUNE des 23.** C'est un outil prêt, pas une autorisation.
La mesure des 23 reste soumise à un **GO humain** — et avec ce verrou, elle
devient sûre par construction plutôt que sûre par pari.

Reste un angle que le verrou ne couvre pas : les **effets de bord non réseau**
(écritures de fichiers). Le snapshot runtime les attrape déjà — 22 fichiers,
comparaison par md5 — et il est en place à chaque lot.

## Ce que le dépôt fait bien, mesuré

- **Les cinq routes sûres testées répondent 200 sans aucune sortie réseau
  possible.** Elles n'ont donc pas de dépendance réseau cachée : ce qui était une
  liste empirique se trouve, pour ces cinq-là, **confirmé par construction**.
- `/api/system/status` répond même verrou posé, alors que trois cribles
  statiques l'accusaient de sortir. **C'est le produit qui avait raison, pas mes
  instruments.**

## Portée — ce que ce lot NE dit PAS

- **Aucune des 23 routes n'a été appelée ni mesurée.** La dette du 512 reste
  **entière**. Ce lot mesure pourquoi elle résiste, et fabrique l'outil ; il ne la
  solde pas.
- Le verrou n'a été validé que sur **cinq** routes sûres. Qu'il n'abîme rien
  ailleurs n'est pas établi.
- Le verrou bloque `socket.socket` et `socket.create_connection`. Une
  bibliothèque qui ouvrirait un descripteur autrement lui échapperait — je ne l'ai
  pas cherché.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.**

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

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0**.

Aucun dossier, et le lot le plus utile depuis longtemps — parce qu'il **débloque
une impasse** au lieu d'en contourner une. Pendant neuf lots j'ai recommandé
cette dette en tête de liste sans jamais mesurer pourquoi elle ne bougeait pas.
La réponse était méthodologique, et elle a demandé trois échecs pour apparaître.

Le collisionneur récurrent a maintenant un nom : **`get`**. Troisième forme de la
famille homonyme dans un seul lot, après le nom de fonction et le nom de module.

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **mesurer les 23 routes — DÉBLOQUÉE, en attente d'un
GO** (l'outil est prêt et validé) ; **recribler les chiffres publiés par motif
textuel** ; **le français construit en JavaScript** ; **l'assemblage entre
fonctions** ; **la condition `k ≤ 5` sur un scan réel** ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 121 (+3)** ; publiés
puis corrigés **15** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et le 521 ajoute une
question précise : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
