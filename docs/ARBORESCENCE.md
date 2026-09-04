# Arborescence — Vertex Test 1.0

État après le tri. Le dépôt passe de **2 546 à 1 021 fichiers suivis**, sans
qu'une seule route servie disparaisse : **204 avant, 204 après**.

## Ce que contient le dépôt

| Chemin | Fichiers | Rôle |
|---|---|---|
| `vertex/` | 398 | le paquet canonique — entrée WSGI `vertex.runtime:app`, entrée locale `python -m vertex` |
| `tests/` | 502 | les gardiens : `python -m pytest -q` |
| `tools/audit/` | 17 | instruments d'audit d'interface (balisage, a11y, boutons morts, captures, service worker) |
| `tools/mesures/` | 17 | mesureurs de runtime (branches, moteurs, rollback, surfaces vides, sondes HTTP) |
| `static/` | 2 | les deux seuls actifs servis depuis la racine : `chart.umd.min.js`, `icon-180.png` |
| `tradingview/` | 2 | le script Pine et le contrat du webhook |
| `docs/` | 3 | l'index, cet audit, les contrats de gouvernance |
| `.claude/` | 53 | la doctrine `/vertex-2-0`, les règles de périmètre, les six auditeurs |
| `.github/` | 2 | la CI et le modèle de PR |
| `.interface-design/` | 1 | la mémoire de design |
| racine | 22 | `terminal.py` (adaptateur historique), `ib_reader.py`, les lanceurs, la configuration |

## Ce qui a été supprimé, et sur quelle preuve

### Code injoignable — 66 modules, 4 665 lignes

Recensement refait sur le SHA courant, pas repris d'une archive. Méthode :

1. **Mesure au runtime** — démarrage réel de `vertex.runtime`, relevé des
   modules `vertex.*` présents dans `sys.modules` : 205.
2. **Clôture transitive AST** depuis quatre racines produit **plus les
   21 blueprints montés par `importlib`** dans `vertex/app/factory.py`. Cette
   deuxième racine est indispensable : sans elle, un premier passage déclarait
   morts `vol_charts`, `gex_history` et `gex_scan`, qui servent des routes.
   L'erreur a été prise par la suite de tests, pas par le graphe.
3. **Filtre par point fixe** — tout module encore cité par du code vivant, la
   CI, les outils ou le skill est retiré des candidats, et l'opération est
   répétée jusqu'à stabilité.
4. **Règle de paquet** — un `__init__.py` ne part que si tout le paquet part.

Restent 66 modules qu'aucune surface servie n'atteint : `research/` (23),
`data_sources/` (8, dont les connecteurs IBKR jamais branchés —
`cotation_unifiee.py` écrivait lui-même « la fusion était écrite ; elle n'était
pas branchée »), `options/` (8), `strategy/memory/` (8), et quinze autres
répartis dans onze paquets.

**Conservé malgré l'absence de consommateur** : `vertex/ai/tool_registry.py`,
la liste `FORBIDDEN_TOOLS` qui interdit `place_order`, `cancel_order`,
`transfer_cash` et consorts. Supprimer un registre de sécurité parce qu'il est
inutilisé affaiblirait la preuve « analyse seule » ; il coûte un fichier.

### Tests devenus sans objet — 42 fichiers

20 gardiens mono-sujet du code supprimé, 5 gardiens de documents supprimés,
plus l'élagage chirurgical de 13 fichiers mixtes : imports morts et fonctions
qui s'en servaient retirés, le reste du fichier conservé. Aucun test d'une
capacité vivante n'a été perdu.

### Documentation historique — 1 434 fichiers, 148 Mo

Rapports de lots, captures d'écran, index de refonte, audits datés. Tout est
retiré de l'arbre de travail ; l'historique Git le conserve intégralement.
`docs/` ne porte plus que des documents vrais sur le commit courant.

## Trois défauts réels trouvés en chemin

Le renommage des fichiers de tests a changé l'ordre de collecte de pytest et
révélé trois dépendances d'ordre que l'ancien classement alphabétique
masquait. Elles ont été corrigées à la cause, pas contournées.

1. **La constitution fuyait.** `activate_release_profile()` remplace en place
   quatre attributs du module `constitution` et se garde d'un drapeau sans
   inverse. Le premier module de test qui l'appelait — à l'import, donc pendant
   la collecte — imposait V4 à toute la suite. `tests/conftest.py` fige
   désormais l'état vierge avant la collecte et le restaure autour de chaque
   test.
2. **`UNIVERSE` restait tronqué.** `test_scan_vide_muet` réduisait l'univers du
   monolithe à 12 titres sans le remettre ; tout banc ultérieur comptant
   l'univers échouait. Restauré en `finally`, et `scan_state` restauré par une
   fixture.
3. **Un faux graphe survivait à `monkeypatch`.** `test_graphe_chaud` et
   `test_graphe_memoise` injectaient un graphe de test qui restait dans le
   magasin de snapshots après le démontage : `/api/skyler/graph/<sym>` levait
   ensuite `KeyError: 'as_of'`. Le magasin est vidé avant et après chaque test.

## Noms

**349 fichiers de tests renommés.** Les numéros de lot (`_lot385`) et les
préfixes de version (`vertex_1_0_`) disparaissent ; les 32 collisions reçoivent
un nom tiré de leur sujet réel — `test_audit_lot66.py` devient
`test_audit_coherence.py`, `test_polish_lot58.py` devient
`test_polish_portefeuille_options.py`. **34 outils renommés** :
`tools/vertex_2_0_*.py` → `tools/audit/*.py`, `tools/vertex_1_0/` →
`tools/mesures/`. Les 372 citations croisées dans le code, les docstrings et la
CI ont suivi.

**Deux noms conservés volontairement.** `skyler` reste : c'est le préfixe des
routes réellement servies (`/api/skyler/graph`) — le retirer des tests les
éloignerait de ce qu'ils testent. `/vertex-2-0` reste : c'est la commande que
l'utilisateur tape et l'identifiant de la doctrine, pas un nom de fichier.

## Validation

- `python -m compileall -q terminal.py vertex` — OK.
- `python -m pytest -q` — **4 109 passés, 147 ignorés, 1 échec**.
  L'échec est `test_branches.py::test_la_classification_est_discriminante`, qui
  exige plus de 100 branches distantes et n'en voit que 2 dans un conteneur
  cloné à plat. Échec d'environnement, présent à la baseline, sans rapport avec
  ce tri.
- `python -m pytest tests/test_no_orders.py -q` — 3 passés.
- Démarrage réel : `Vertex Test 1.0`, 204 routes, `/healthz` 200.

## Rollback

`git revert` du commit restaure l'arbre complet : code injoignable,
documentation et anciens noms. Rien n'a été effacé de l'historique.
