# SKYLER LOT 388 — Un point fabriqué par jour dans l'historique GEX réel

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-388` (base : lot 387 fusionné,
86ae097)

## Piste

Le lot 387 avait traité `desk_data.json`. Il n'avait regardé **que celui-là**.
Ce lot applique la même méthode aux **vingt fichiers runtime** du dépôt — et non
aux quatre que je croyais concernés.

## Mesure — 7 fichiers sur 20 touchés par la suite

```text
ai_enrichment.json          horodatage seul (`as_of`)
session_digest_cache.json   horodatage seul (`age_s`)
weekly_snapshot.json        horodatage seul (`generated_at`)
desk_data.json              connu (lot 387), `data` byte-identique
desk_backup_20260809.json   CRÉÉ — la suite consomme le créneau du jour
skyler_sessions.json        un point/jour sur les tickers SYNTHÉTIQUES SKYX/TSTQ
gex_history_cache.json      un point/jour sur MSFT — un VRAI titre
```

La création de `desk_backup_<jour>.json` **confirme par la mesure** ce que le lot
387 n'avait qu'annoncé : lancer la suite consomme le snapshot quotidien du desk.

## La trouvaille

`test_options_gex_route_real_numbers` sème un board d'options **fabriqué**
(MSFT, strikes 460/420, gamma 0.05/0.03, spot 440) puis appelle
`/api/options/gex/MSFT`. La route **journalise le profil** via
`gex_history.record()` — dans le vrai `gex_history_cache.json`, la fixture
`client` du fichier ne redirigeant rien.

```text
MSFT   avant 7 pts 2026-08-02..08  → après 8 pts   (ajouté : 2026-08-09)
ACN    avant 2 pts                 → après 2 pts   (—)
ADBE   avant 2 pts                 → après 2 pts   (—)
```

Les huit points MSFT portent des valeurs **strictement identiques** — `net_gex`
36 784 000, `spot` 440.0, `zero_gamma` 429.6 — un par exécution de la suite.
ACN et ADBE, eux, portent des valeurs variées et n'ont pas bougé : la comparaison
interne au fichier suffit à distinguer le fabriqué du mesuré.

**Ce fichier est servi.** `vertex/app/routes/options_intel_api.py` le lit pour
`/api/options/gex-radar`. Des chiffres fabriqués par un test étaient donc rendus
à l'utilisateur comme un historique mesuré — **sur un titre qu'il détient
réellement**. C'est l'invariant n°4, cette fois sur un vrai symbole et non sur un
ticker de test.

## Correction

Redirection de `persist._BASE_DIR` vers un dossier temporaire dans le seul test
concerné — le mécanisme déjà employé par `test_desk_routes.py`. **Aucune
production touchée**, donc ni preuve MD5 ni bump.

Périmètre choisi par la mesure, pas par l'intuition : les 19 tests du fichier ont
été rejoués **un par un** depuis un état restauré à l'octet ; **un seul** écrit.
Rediriger tout le module aurait été un changement plus large que nécessaire.

### Effet vérifié

```text
avant correction : 7 fichiers runtime touchés · MSFT 7 → 8 points
après correction : 5 fichiers runtime touchés · MSFT 7 → 7 points
```

Les 5 restants sont sans danger : trois horodatages, `desk_data.json` (traité au
387, `data` byte-identique) et `skyler_sessions.json` — voir ci-dessous.

## Ce que ce lot ne corrige pas, et pourquoi

`skyler_sessions.json` accumule aussi un point par jour, mais sur **SKYX** et
**TSTQ** : des tickers **synthétiques** utilisés par 8 fichiers de test, non
confondables avec un titre réel, et bornés (`MAX_SESSIONS = 400`). Le dégât n'est
pas de même nature — rien de faux n'est attribué à un vrai symbole. Corriger huit
fichiers dépasse la piste calibrée de ce lot ; **versé aux dossiers**.

Reste aussi une **pollution historique** : les 7 points MSFT fabriqués accumulés
par les exécutions passées sont toujours dans le fichier. C'est une donnée
runtime de l'utilisateur, gitignorée — **je ne la supprime pas de ma propre
initiative**. La purge de la clé `MSFT` est une décision à prendre, pas un effet
de bord d'un lot.

## Gardien

`tests/test_caches_runtime_lot388.py` (5 tests) :

- **anti-vide** — la route GEX doit toujours journaliser, sinon exiger une
  redirection ne protégerait plus rien et le test passerait pour la mauvaise
  raison ;
- les **bornes anti-croissance** de l'historique restent explicites
  (`_MAX_DAYS = 120`, `_MAX_SYMBOLS = 80`) — `_MAX_SYMBOLS` évince les symboles
  les plus anciens, donc un symbole réinjecté en boucle par un test resterait
  « récent » et pourrait chasser un vrai symbole ;
- **LA propriété** — le test qui exerce une route journalisante doit rediriger
  son stockage ;
- **anti-péremption** du recensement ;
- **recensement des caches écrits par la production**, gelé à 12 sites : chaque
  nouveau venu pose la même question que le GEX.

### Preuve ROUGE

```text
redirection retirée du test journalisant             ROUGE OK  | restauration identique
route GEX ne journalise plus (gardien sans objet)    ROUGE OK  | restauration identique
borne anti-croissance des symboles affaiblie         ROUGE OK  | restauration identique
nouveau cache journalisé non recensé                 ROUGE OK  | restauration identique
[témoin] commentaire sur une borne inchangée         ne mord pas — correct
après restauration : 5 passed
```

## Un recensement opaque ne recense rien

Mon premier détecteur rendait « ? » pour toute cible de `save_json` qui n'était
ni une constante ni un nom simple — il comptait **8 sites**. En le rendant
explicite (attributs, chaînes formatées), il en trouve **12**, et surtout il
nomme `_slog.SESSIONS_FILE` : **précisément le fichier qui accumule les tickers
synthétiques**. La borne a été fixée sur la vraie mesure, pas sur la première.

C'est la même leçon qu'aux lots 385 et 387, sous une forme de plus : un
dénominateur mesuré par un outil myope est un faux dénominateur.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- `integration/vertex-skyler-v2` à jour (tête = lot 387, 86ae097) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- Copies de sûreté des **20** fichiers runtime prises avant toute sonde, puis
  restaurées ; effet de la suite remesuré après correction.
- Suite : **2826 → 2831 passed / 2 skipped** (+5). SW : `td-shell-v187`.

## Portée

Le gardien est **statique** : il vérifie qu'un test recensé redirige son
stockage, il n'observe pas les écritures à l'exécution. Un test qui atteindrait
un cache par un autre chemin lui échapperait — c'est d'ailleurs ainsi que le cas
GEX a échappé au lot 387, dont le périmètre s'arrêtait au desk. Et le recensement
des 12 sites de production rend la **dérive** visible : il ne dit pas que les 12
sont correctement isolés dans les tests.

## Suite

Deux pistes nées de ce lot : **les tickers SKYX/TSTQ dans `skyler_sessions.json`**
(8 fichiers, dégât mineur) et **la purge de la clé MSFT polluée** (décision
utilisateur). Restent les pistes fines : refus construits en variable (377) ·
formes imbriquées des promesses de retour (375) · trois sites de concaténation à
constantes (374).

Prochaine échéance périodique : **~lot 390** — bilan de la tranche 380-389.
