# SKYLER LOT 389 — Les deux dernières écritures de test, et une mesure qui piégeait

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-389` (base : lot 388 fusionné,
8800f55)

## Piste

Deux questions laissées ouvertes par le lot 388, dans l'ordre :

1. **Vérifier mon propre énoncé** — « les 3 fichiers restants ne changent qu'un
   horodatage ». Je ne l'avais contrôlé qu'au **premier niveau de clés**.
2. Trancher le cas **SKYX/TSTQ** dans `skyler_sessions.json`.

## 1. L'énoncé du 388 tient — vérifié récursivement cette fois

Diff **feuille à feuille** (aplatissement récursif : le diff top-level ne voit
pas ce qui se cache sous une clé) après la suite complète :

```text
ai_enrichment.json          1 feuille modifiée : .as_of
desk_data.json              1 feuille modifiée : .ts
session_digest_cache.json   1 feuille modifiée : .age_s
weekly_snapshot.json        1 feuille modifiée : .generated_at
```

Exactement **une** feuille par fichier, un horodatage à chaque fois. Aucune
feuille perdue, aucune ajoutée. L'énoncé du 388 était juste — il repose
désormais sur la bonne mesure.

## 2. Le piège : l'écriture était devenue invisible

`skyler_sessions.json` **n'a pas bougé** lors de cette exécution. Conclusion
tentante : « personne n'écrit ». **Fausse.** Le point du jour existait déjà, donc
l'écriture est **idempotente** — la croissance est d'un point **par jour**, pas
par exécution.

En retirant le point du jour avant chaque essai, l'écriture redevient
observable. C'est la règle du lot 387 appliquée à l'envers : *« rien ne bouge »
ne vaut que si l'on s'assure qu'il y avait quelque chose à observer.*

## Le périmètre, encore quatre fois trop large

Huit fichiers de test mentionnent SKYX ou TSTQ. Rejoués **un par un** depuis un
état sans point du jour :

```text
test_skyler_core.py         OUI  {'SKYX': 1}
test_xss_exits_lot177.py    OUI  {'TSTQ': 1}
les 6 autres                non — ils ne font que MENTIONNER les tickers
```

**Deux sur huit.** Les deux appellent `/api/skyler/<sym>`, qui journalise une
séance via `session_log`. Corriger huit fichiers aurait été six changements
gratuits.

## Correction

Redirection de `persist._BASE_DIR` vers un dossier temporaire dans les **deux**
tests concernés — **aucune production touchée**.

```text
avant : 5 fichiers runtime touchés par la suite
après : 4 — `skyler_sessions.json` sort de la liste
```

Les 4 restants sont exactement ceux dont le diff récursif ci-dessus prouve
qu'ils ne changent qu'un horodatage.

## Gardien — étendu, pas dupliqué

`tests/test_caches_runtime_lot388.py` passe de 5 à **9 tests**. La propriété est
la même qu'au 388 (« un test qui exerce une route journalisante redirige son
stockage ») : créer un fichier jumeau aurait été du bruit.

Ajouts : les deux entrées au recensement · un **anti-vide** sur la
journalisation de séance · la **borne `MAX_SESSIONS = 400`**, sans laquelle un
ticker semé chaque jour croîtrait sans fin.

### Preuve ROUGE

```text
redirection retirée de test_skyler_route          ROUGE OK  | restauration identique
redirection retirée du test XSS skyler            ROUGE OK  | restauration identique
borne des séances neutralisée                     ROUGE OK  | restauration identique
journalisation de séance retirée (anti-vide)      ROUGE OK  | restauration identique
[témoin] commentaire reformulé, borne inchangée   ne mord pas — correct
après restauration : 9 passed
```

## Deux fois l'outil en cause — dont une répétition d'une faute déjà apprise

**Mon témoin a mordu.** Je renommais `SESSIONS_FILE` en `SESSIONS_FILE2` en
croyant faire un changement anodin : c'est une `AttributeError` en production, et
le recensement l'a correctement signalée comme un **13ᵉ site de journalisation**.
Le gardien avait raison, le témoin était faux — remplacé par un commentaire, qui
reste muet.

**Mon anti-vide était creux — la faute du lot 386, refaite.** J'avais écrit
`'SESSIONS_FILE' in src` : la chaîne apparaît **6 fois** dans le fichier pour
seulement **2 sites d'écriture**, donc en retirer un laissait le test vert. La
preuve ROUGE l'a démasqué. Réécrit en comptant les sites par AST — il mord.

Avoir la règle écrite ne suffit pas à ne pas la re-violer ; **c'est la preuve
ROUGE qui l'attrape**, et c'est précisément pourquoi elle n'est pas négociable.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- `integration/vertex-skyler-v2` à jour (tête = lot 388, 8800f55) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Copies de sûreté des **21** fichiers runtime prises avant toute sonde, puis
  restaurées ; effet de la suite remesuré après correction.
- Suite : **2831 → 2835 passed / 2 skipped** (+4). SW : `td-shell-v187`.

## Portée

Les 4 fichiers encore touchés le sont **aujourd'hui** sur un horodatage : c'est
une caractérisation datée, pas une propriété garantie — rien ne l'impose au code.
Et le gardien reste **statique** : il vérifie qu'un test recensé redirige, il
n'observe pas les écritures à l'exécution.

La pollution historique n'est pas nettoyée : **7 points MSFT fabriqués** dans
`gex_history_cache.json` et les points SKYX/TSTQ déjà accumulés. Ce sont des
données runtime de l'utilisateur — leur purge est une décision, pas un effet de
bord de lot.

## Suite

La veine « écritures runtime par la suite » est **close** : ouverte au 386,
mesurée au 387 (desk), élargie au 388 (20 fichiers, GEX), terminée ici. Deux
trouvailles réelles sur trois lots — le chemin d'effacement des notes (387) et
l'injection GEX sur un vrai titre (388).

**Le lot 390 est le bilan de la tranche 380-389.**
