# SKYLER LOT 542 — Le pendant serveur du 541 : **53 refus JSON, 53 expliqués, ZÉRO nu** — sous une définition étroite comme sous une définition large. Et trois arrêts, dont une liste de noms qui accusait dix refus honnêtes

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-542` (base : lot 541 fusionné,
`24180f7c`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(j)** — le 541 a mesuré ce que le **client** affiche quand ça casse. Voici le
pendant : **ce que le serveur répond quand il n'a pas la réponse.**

**Leçon du 541 appliquée — lire d'abord.** Un gestionnaire réel, lu **avant**
d'écrire une ligne d'instrument :

```python
return jsonify({'available': False, 'reason': f'{type(e).__name__}: {e}'}), 200
```

**Le serveur répond 200 et dit pourquoi.** La question n'était donc pas
« 500 nu contre réponse riche » : le motif du dépôt est le **refus expliqué**,
et c'est lui qu'il fallait mesurer.

## Trois arrêts

**1. Ma liste de noms de clé accusait dix refus honnêtes.** Je cherchais
`reason`, `error`, `message`… et j'avais oublié **`err`** et **`note`**.
Résultat : les dix refus de `desk.py` — « nom invalide », « backup
introuvable », « payload invalide », « backup illisible » — sortaient **« NUS »**
alors qu'ils disent très exactement pourquoi. **C'est la faute 521-B, une liste
de noms devinée, et cette fois elle produisait une accusation.**

**2. La correction a sur-corrigé.** Ma règle de repli — « toute clé dont la
valeur est une chaîne » — ramassait `final_decision`, `label`, `login`, qui ne
sont pas des raisons. **J'ai donc publié les DEUX bornes** au lieu de choisir.

**3. J'allais croiser des homonymes.** Comparer « routes rendant `ok` » et
« lectures de `.ok` côté client » n'a aucun sens : **`.ok` est aussi la propriété
standard d'une réponse `fetch`** (`if (!r.ok) throw`). Idem pour `.demo` et
`.source`, trop communs. Les trois sont **exclus du croisement**, et c'est dit.

**Arrêtés avant publication : 155 → 158.**

## La mesure — et les deux bornes coïncident

Corpus : **22 fichiers** (`vertex/app/routes/*.py` + `terminal.py`), lus avec le
module `ast` de Python — un vrai analyseur, comme acorn côté client.

```text
REFUS JSON repérés                                53
   expliqués, borne BASSE (clé de raison)         53
   expliqués, borne HAUTE (toute clé chaîne)      53
   NUS, encadrés                                0 à 0     FEUILLE : OK
```

**Les deux bornes coïncident : le 53 sur 53 n'est pas une estimation.** Chaque
refus JSON du corpus lu transmet une raison.

```text
formes : drapeau négatif 21 · code 404 11 · 400 9 · 500 9 · 422 2 · 401 1
```

## Le vocabulaire de la raison, **relevé et non deviné**

```text
`reason` · `error` · `err` · `note`
                    4 noms de clé différents pour la même idée
```

C'est la seule irrégularité mesurée du lot : le contrat est **tenu partout**,
mais **écrit de quatre façons**. Un client qui ne lirait que `reason` raterait
les refus de `desk.py`.

## Les 21 routes sûres, appelées en DÉMO

Toutes répondent **200**, aucune n'est en échec — donc ce que j'ai mesuré ici est
le **contrat NOMINAL**, pas le contrat d'échec :

```text
/api/portfolio/context   3 clés   raison=['reason']   drapeau=['available']
/api/session/manifest   11 clés   raison=['error']
les 19 autres            de 0 à 18 clés, aucun champ de refus — normal : rien
                         n'échoue en DÉMO
```

**Le contrat d'échec n'est donc lisible que dans le code** (partie a). Je ne
provoque aucun échec : cela demanderait des appels hors du périmètre autorisé.

## Ce que le client lit, et le seul croisement qui tient

```text
.reason      33 lectures        .available   7 lectures
.ok 52 · .demo 52 · .source 52  EXCLUS — homonymes (532-A)
```

**Le client lit `reason` 33 fois** ; le serveur l'écrit dans tout son corpus de
refus. Les deux moitiés se répondent.

## Ce que le dépôt fait bien, mesuré

- **Zéro refus JSON muet sur 53.** Le serveur ne se contente jamais d'un code.
- **Le refus expliqué à 200** (`{'available': False, 'reason': …}`) est un choix
  fort : le client reçoit une réponse *lisible* plutôt qu'une erreur brute.
- **Même les 404 HTML nomment ce qui manque** : « Groupe inconnu », « Cellule
  inconnue », « Décision inconnue », et leur pendant JSON porte en plus un
  `note` : « aucune décision… ».
- **`desk.py`, le point le plus sensible du produit** (synchronisation du poste),
  est celui qui explique le plus : dix refus, tous nommés.

## Portée — ce que ce lot NE dit PAS

- **Le contrat d'ÉCHEC n'a pas été observé, seulement lu.** Les 21 routes sûres
  répondent 200 en DÉMO ; provoquer un échec sortirait du périmètre autorisé.
- **Les 23 routes interdites sans GO sont hors périmètre** et comptées à part :
  un refus **lu** n'est pas un refus **observé**, et on n'extrapole pas de l'un à
  l'autre (**529-B**).
- Le relevé porte sur les refus **JSON** ; les pages d'erreur HTML sont citées
  mais pas comptées dans le 53.
- `.ok`, `.demo`, `.source` sont exclus du croisement — leur lecture brute est
  donnée, sans conclusion.
- **Aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Le serveur tient son bout du contrat **partout**, et mieux que le
client : là où quinze messages d'erreur d'interface se contentent de deux mots
(541), **les cinquante-trois refus du serveur donnent tous une raison**.

Ce qu'il faut dire sans le maquiller : **trois arrêts, et le premier accusait
`desk.py` à tort.** Une liste de noms devinée — la faute que j'ai écrite en règle
au lot 521 — a failli transformer dix refus exemplaires en défaut. Ce qui l'a
arrêtée n'est pas une intuition : c'est d'avoir **lu les dix lignes** avant de
publier.

Trois règles neuves :

- **542-A · UN SYNONYME MANQUANT ACCUSE À TORT** — `err` et `note` absents de ma
  liste transformaient dix refus explicites en refus muets.
- **542-B · QUAND UNE DÉFINITION EST DISCUTABLE, PUBLIER LES DEUX BORNES** — ici
  elles coïncident, donc le 53 sur 53 n'est pas une estimation.
- **542-C · NE PAS CROISER DES HOMONYMES** — `.ok` est aussi la propriété d'une
  réponse `fetch` ; l'exclusion est dite, pas cachée.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **le contrat d'ÉCHEC observé, jamais mesuré** ; **les
4 noms de clé pour la même idée** ; **les 15 messages d'erreur sans pourquoi du
541 — arbitrage humain** ; **les 95 atténuations non affichées** ;
**`initSettings`, mesurée partiellement** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 158 (+3)** ; publiés
puis corrigés **22** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
