# SIGNAL OS · LOT 17 — LES CINQ MODULES MORTS, SUPPRIMÉS

Branche : `agent/vertex-signal-os-v1` · SW **v223 inchangé** · Suite **3101 passed**

`CLAUDE.md` les décrivait « reliques **en attente de décision** ». La décision
est arrivée ; ce lot l'exécute, et refuse d'emporter au passage ce qui protège
du code vivant.

---

## 1. La vérification qui aurait pu tout arrêter

Avant de supprimer, j'ai listé les **routes réellement servies** :

```
/journal · /strategy · /options-lab · /strategy-os · /vault
```

Cinq URL vivantes portant les noms des modules à supprimer. Si l'une d'elles
était servie **par** un de ces modules, il n'était pas mort.

**Mesuré, gestionnaire par gestionnaire :**

| route | servie par |
| --- | --- |
| `/journal` | `redesign.journal_route` — espace canonique n°7 |
| `/strategy`, `/options-lab`, `/strategy-os`, `/vault` | `redesign._view` — **redirections** |

Aucune ne touche les cinq modules. Suppression confirmée.

---

## 2. Ce qui est supprimé

`vertex/ui/` : `journal.py` · `options_lab.py` · `vault.py` · `signals.py` ·
`strategy_os.py` — **1 624 lignes**, 0 consommateur en production, 0 route
déclarée.

### `CLAUDE.md` disait vrai à 80 %

La documentation affirmait aussi que `journal.py` portait « une 4ᵉ copie de
`DESK_KEYS` ». **Mesuré au lot 13 : le symbole n'y existait plus** — corrigé
alors, et c'est cette correction qui a rendu la suppression lisible.

---

## 3. Quatre gardiens touchés, et aucun affaibli par accident

### `tests/test_journal_page.py` — supprimé, mais pas entièrement

Cinq tests, dont **quatre** lisaient le JS d'une page que plus aucune route ne
servait. Le cinquième gardait du **vivant** : `/journal` rend 200, et
`/performance` y redirige.

**Relogé** dans `tests/test_signal_os_journal_rangs_lot11.py`. *Supprimer un
fichier de tests avec son sujet est juste ; emporter la seule assertion qui
protégeait autre chose ne l'est pas.*

### `tests/test_vault.py` — 6 tests → 2

Quatre lisaient `vault.JS`. Les deux conservés gardent les **redirections**
`/vault` et `/archive` (301 → Système › Archive) et la place de l'entrée de
navigation, **après** Settings donc en section SYSTEM.

### `tests/test_strategy_os_routes.py` — 9 tests → 8

Huit testent les routes **réelles** du blueprint `strategy_os_api`. Le neuvième
montait `/strategy-os` **lui-même**, sur le module mort — alors qu'en production
cette URL est une redirection. *Il ne décrivait pas le produit : il fabriquait
une route pour se la tester à soi-même.*

### `test_production.py` et `test_strategy_os_final_guards.py` — l'ancre déplacée

Les deux comparaient `vx_kit.JS` **et** `journal.JS` pour verrouiller
`DESK_KEYS`. Or **aucun des deux n'est servi** (mesure du lot 381 : les
21 727 octets de `vx_kit.JS` n'atteignent aucune des 8 pages).

`test_strategy_os_final_guards` compare désormais `vx_kit` au **repli inline de
`system_page.py`** — et c'est un **gain** : on confronte deux listes que le
navigateur reçoit, au lieu d'une servie et d'une morte.

---

## 4. Un gardien a fait exactement son travail

`test_references_vivantes_lot364` a mordu : `ANNEXE-E1-RETRAITS.md` citait
`tests/test_journal_page.py`, désormais inexistant.

C'est précisément sa raison d'être — *un document vivant qui cite un gardien
disparu doit le dire*. Le document est **annoté**, pas amputé : la mention reste,
marquée « RETIRÉ au lot 17 », avec la raison et l'adresse du test relogé.

---

## 5. Mesures — serveur `td-shell-v223` vérifié avant lecture

| relevé | résultat |
| --- | --- |
| les 8 espaces canoniques | **200** — 8/8 |
| `/vault`, `/archive` | 301 → `/system?view=archive` |
| `/strategy-os` | 301 → `/intelligence?view=strategy` |
| `/options-lab` | 301 → `/opportunities?view=options` |
| `/strategy` | 301 → `/portfolio` |
| `/performance` | 301 → `/journal` |

Aucune référence résiduelle aux cinq modules dans le code. Suite **3101
passed** (3110 − 9 tests supprimés avec leur sujet).

**Réversible** : `git revert` du commit restaure les cinq fichiers et leurs
tests.

---

## 6. Dette restante

- Rang 3 du Journal (grade / setup / horizon) et win/loss par bucket — à
  instruire avant de construire.
- Étiquetage démo : figé en caractérisation (lot 08), correction subordonnée à
  l'établissement de quelle donnée est réellement synthétique.
- Fiche `/analysis/<ticker>` inaccessible dans cet environnement.
