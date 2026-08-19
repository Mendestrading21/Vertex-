# G1 · #779 — `/scan` et `/api/rescan` sortent avec leur porte

Modules : `vertex/app/rescan_gate.py`, `vertex/app/routes/scan_api.py`
Gardien : `tests/test_vertex_1_0_scan_api_parity.py` (10 tests) +
`tests/test_rescan_rate_limit.py` (retargeté, 5 tests) · **7 mutations**

---

```text
routes LEGACY      7 → 5
lignes terminal.py 7 169 → 7 145
routes canoniques  147 → 149
```

## Le piège que l'analyse statique ne pouvait pas voir

`terminal.py` fait `from vertex.data.universe import *`. Les six ensembles
d'indices servis par `/scan` — `_DOW30`, `_NDX100`, `_SP500_SET`, `_RUT_SET`,
`_EU_SET`, `_ASIA_SET` — venaient donc du paquet **sans qu'aucune ligne d'import
ne les nomme**.

Mon inventaire de dépendances croise les symboles *utilisés* avec les symboles
*déclarés*. Ces six-là n'apparaissaient dans **aucune** des deux listes : leur
intersection était vide, et la route paraissait plus simple qu'elle ne l'était.
Un `import *` rend une mesure de dépendances **silencieusement incomplète** —
elle ne se trompe pas, elle ne voit pas.

C'est un `curl /scan` qui l'a révélé, pas l'AST. Ils sont désormais importés
explicitement dans `scan_api.py`, et un test vérifie que les six ensembles sont
servis **non vides** : vides, la page Marchés ne saurait plus dire à quel indice
appartient un titre, et aucune erreur ne serait levée.

## La porte anti-rafale, et ce qu'elle refuse de retenir

`/api/rescan` réveille la boucle de scan. Sans borne, un client qui rafraîchit en
boucle — ou huit onglets ouverts — relancerait un scan d'univers complet toutes
les secondes.

La porte ne trace **aucune identité de demandeur** : pas d'IP, pas de session,
pas de compteur par client. La fenêtre est **globale**. Un quota par utilisateur
supposerait de savoir qui demande, donc de le retenir ; sur un terminal
personnel, ça n'apporterait qu'une donnée de plus à conserver. Un test vérifie
qu'aucun de `ip`, `address`, `client`, `requester`, `identity`, `token`
n'apparaît dans le refus.

Trois choix qui ne sont pas des détails, chacun tenu par une mutation :

- **`time.monotonic()`, jamais `time.time()`.** Une horloge murale peut reculer
  — NTP, changement d'heure, sortie de veille. Un recul rendrait le délai
  restant négatif, donc la porte ouverte, au moment précis où elle doit tenir.
- **La fenêtre est bornée à 1 s au minimum.** `VERTEX_RESCAN_COOLDOWN_SEC=0`
  l'ouvrirait en grand ; une valeur illisible retombe sur le défaut plutôt que
  de faire échouer le démarrage — mais elle ne doit pas non plus désactiver la
  garde en silence.
- **Le verrou couvre la lecture du délai ET l'écriture de l'horodatage.** Sans
  lui, deux demandes simultanées verraient toutes deux la porte ouverte, et deux
  scans d'univers partiraient.

## L'événement est partagé, jamais recréé

`vertex/services/live_engine.py::configure` transmet `EVENEMENT` à la boucle de
scan, qui attend **cet objet précis**. Le réassigner laisserait la boucle
attendre un objet que plus personne ne réveille : `/api/rescan` répondrait 200,
et rien ne repartirait. Même famille de piège que `scan_state` (« muter en place,
jamais réassigner »).

## Un test à moi qui dépendait de l'ordre des autres

La première version affirmait `live_engine._CFG['rescan_event'] is
rescan_gate.EVENEMENT`. Elle **passait seule et échouait dans la suite
complète** : `tests/test_live_engine.py` reconfigure légitimement le moteur avec
ses propres états. Un test qui dépend de l'ordre des autres ne prouve rien — il
vise désormais le **câblage** de `terminal.py`, qui est stable.

Deuxième correction du même genre dans ce lot : la borne de la fenêtre était
d'abord testée par `importlib.reload(rescan_gate)`. Ce rechargement **recrée
`EVENEMENT`** — le test aurait cassé le partage pour tous les tests suivants,
c'est-à-dire cassé le produit pour se prouver juste. La borne est maintenant une
fonction pure, testée sans rien recharger.

## `scan_age` avait deux implémentations identiques

`terminal.py::_scan_age` et une fermeture locale de
`vertex/app/routes/decision_api.py` calculaient exactement la même chose. Deux
copies dérivent au premier ajustement, et l'écran afficherait alors deux âges
différents pour la même donnée. Une seule maison : `vertex.app.state.scan_age`,
qui rend **`None`** — pas `0` — quand aucun scan n'a eu lieu : une absence n'est
pas de la fraîcheur parfaite.

## Le dixième piège de sous-chaîne

`test_l_horloge_de_la_porte_ne_recule_jamais` cherchait `time.time()` dans le
fichier. Il échouait sur un module parfaitement correct : la chaîne vit dans le
docstring qui **explique pourquoi elle est bannie**. Retargeté sur les appels
réels, extraits à l'AST.

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 311 passed        (3 299 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations                      7/7 mordent, contrôle vert
```

Les sept : porte sans verrou · horloge murale · fenêtre désactivable ·
ensembles d'indices vidés · `/scan` annonce un délai différent de la porte ·
`scan_age` retombe sur `0` · le monolithe recrée son propre événement.

Serveur réel, `DEMO=1 NO_IBKR=1` :

```text
huit espaces        200 · 0 débordement · 0 erreur console
/api/client-log     count: 0
GET  /scan          200
POST /api/rescan    200 puis 429 (Retry-After)
```

## Six gardiens maison ont réagi — aucun contourné

| gardien | ce qu'il a vu |
| --- | --- |
| `test_rescan_rate_limit` | patchait `terminal._last_rescan_ts`, disparu — **retargeté sur le module de porte**, et enrichi de deux tests |
| `test_references_vivantes_lot364` | mon docstring citait `vertex/services/live.py`, qui n'existe pas — **une vraie erreur de doc que j'avais introduite** |
| `test_terminal_imports_lot324` | `time` devenu orphelin dans `decision_api` |
| `test_pass_terminal_lot386` | cherchait `{**scan_state` dans `terminal.py` — le constat est intact, seul le fichier a changé |
| `test_persistance_demo_lot391` | cherchait `data_source` dans `terminal.py` — le **marquage** reste dans le monolithe, la **sortie** est ailleurs |
| `test_vertex_1_0_factory_parity` | le registre compte 17 entrées |

## Les cinq LEGACY restantes

| route | ce qui la retient |
| --- | --- |
| `/options/<sym>`, `/api/ticker/<sym>` | `options_pack`, une fonction du monolithe partagée par les deux |
| `/api/correlations/<sym>` | le trio `_CORR_MAP` / `_corr_benchmarks` / `_to_naive` |
| `/desc/<sym>` | le trio de cache de descriptions `_DESC_PATH` / `_FR_DESC` / `_desc_lock` |
| `/weekly-regen` | `WEEKLY_PATH` et `_earnings_map` |

Même geste répété : un petit groupe auto-suffisant part avec sa route.

**G1 reste non déclaré PASS.**
