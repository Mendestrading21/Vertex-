# Arborescence du dépôt — audit et propriétaires

Baseline : `main` à `c683c94`, branche `claude/repository-cleanup-organization-ok29ee`.
Mesure : 2 544 fichiers suivis, 952 modules Python, 524 fichiers de tests.
Suite au SHA de baseline : **4 469 passés, 153 ignorés, 1 échec** —
`tests/test_vertex_1_0_branches.py::test_la_classification_est_discriminante`,
qui exige plus de 100 branches distantes et n'en voit que 2 dans un conteneur
cloné à plat. Échec d'environnement, antérieur à ce lot, non traité ici.

Ce document répond à une seule question, dossier par dossier : **qui le
consomme ?** Un dossier sans consommateur prouvé est nommé comme tel ; il n'est
pas supprimé pour autant. L'invariant 9 de `CLAUDE.md` interdit tout retrait
avant preuve d'absence d'import, de route, de test, de consommateur, de donnée
et de chemin de rollback.

## Verdict

**Aucun dossier de code n'est mort.** Les dix entrées de premier niveau hors
`docs/` ont toutes un consommateur prouvé — import, route servie, test gardien,
étape de CI ou fichier réellement servi en HTTP. Le désordre mesuré était
entièrement documentaire : 177 fichiers à plat à la racine de `docs/`, dont 162
sans aucune référence dans le dépôt, et quatre sous-dossiers sans consommateur
hors `docs/`.

## Code et runtime — tous consommés

| Entrée | Fichiers | Propriétaire | Preuve de consommation |
|---|---|---|---|
| `vertex/` | 464 | paquet canonique | entrée WSGI `vertex.runtime:app`, entrée locale `python -m vertex`, activée par `render.yaml` et la CI |
| `tests/` | 527 | suite de gardiens | `python -m pytest -q`, exécutée par les deux jobs de `.github/workflows/ci.yml` |
| `tools/` | 38 | instruments de mesure | lus **et** gardés par les tests : `tests/test_vertex_1_0_registre_jobs.py`, `tests/test_vertex_1_0_rollback.py`, `tests/test_frontiere_ibkr_lot02.py` en mode `--enforce`, `tests/test_repli_sans_js_lot27.py` |
| `static/` | 2 | actifs servis | `chart.umd.min.js` et `icon-180.png` servis par la fabrique et pré-cachés par le service worker ; parité gardée par `tests/test_vertex_1_0_factory_parity.py` |
| `tradingview/` | 2 | webhook TradingView | `vertex/ui/pages/analysis_page.py` renvoie le lecteur vers `tradingview/README.md` ; le blueprint `/api/tradingview/webhook` est monté dans `terminal.py` |
| `.claude/` | 53 | doctrine et outillage agent | `SKILL.md` est l'autorité unique de `CLAUDE.md` ; `.claude/rules/` cadre les périmètres ; `tests/test_promesses_docstrings_lot366.py` balaie le skill |
| `.github/` | 2 | CI et modèle de PR | `ci.yml` exécute compile, contrat 1.0, suite complète, fumée runtime et invariant analyse-seule |
| `.interface-design/` | 1 | mémoire de design | périmètre déclaré par `.claude/rules/vertex-ui.md` |
| `terminal.py` + scripts racine | 8 | adaptateur historique et lanceurs | recensés et gardés fichier par fichier par `tests/test_replis_racine_lot385.py` et `tests/test_vertex_1_0_constitution_active.py` |
| `render.yaml`, `pytest.ini`, `requirements*.txt` | 4 | déploiement et outillage | `render.yaml` lance `gunicorn vertex.runtime:app`, vérifié par `tests/test_vertex_1_0_contract.py` |

### Cas examinés puis conservés

- **`vertex/strategy/profiles/` vs `release_profiles/`** — trois JSON identiques
  de part et d'autre. Ce n'est pas un doublon accidentel : `release_profiles/`
  porte le profil V4 exécuté par le runtime, `profiles/` porte le chemin de
  rollback V1–V3 chargé par `vertex/strategy/constitution.py`. Les deux sont
  cités par la CI et par `tests/test_vertex_1_0_constitution_active.py`.
  **Conservés.**
- **Scripts racine hors production** — `test_connection.py`, `verifier_vertex.py`
  et `lancer_ipad.py` ne sont importés par aucun module de l'application.
  `tests/test_replis_racine_lot385.py` les déclare explicitement
  `HORS_PRODUCTION` et vérifie qu'ils restent à la racine. **Conservés.**
- **`tools/vertex_1_0/`** — outillage d'une itération précédente, mais chaque
  mesureur est encore lu par un test qui garde son résultat. **Conservé.**
- **Captures dupliquées à l'octet près** — 25 PNG identiques répartis entre
  `preuves/final/`, `preuves/lot-NN-apres/` et `lot-NN/`. Git ne stocke qu'un
  blob par contenu : la duplication ne coûte rien au dépôt, et retirer une copie
  amputerait le jeu de preuves d'un lot. **Conservées.**

## Documentation — la zone réellement en désordre

État avant : 1 434 fichiers, dont **177 à plat** à la racine de `docs/`.
Mesure des références par chemin exact `docs/<nom>`, sur l'ensemble des
2 177 fichiers texte du dépôt : **15 fichiers référencés, 162 sans aucune
référence**. Sur les 15, deux seulement sont cités hors de `docs/`, et
uniquement dans une docstring de test.

Quatre sous-dossiers — `claude/`, `release/`, `research/`, `vertex-audit/` —
n'avaient aucun consommateur hors `docs/`.

### Ce qui a été fait

176 fichiers plats et ces quatre sous-dossiers ont été déplacés sous
`docs/archives/`, rangés en onze thèmes, par `git mv`. Les 48 mentions
textuelles de leurs anciens chemins ont été réécrites dans 31 fichiers, de sorte
qu'aucune référence ne pende. Contrôle après déplacement : les 29 chemins
`docs/…` inexistants encore cités dans le dépôt sont **tous** antérieurs au
rangement — `docs/redesign/`, `docs/screenshots/`, `docs/skyler/baseline/`,
`docs/tests/`, `docs/captures/` avaient déjà disparu au SHA de baseline.
Ce lot n'en a créé aucun.

Aucun fichier n'a été supprimé, aucun contenu réécrit hors chemins.

### Après

| Chemin | Fichiers | Statut |
|---|---|---|
| `docs/README.md`, `docs/ARBORESCENCE.md` | 2 | index et audit, vivants |
| `docs/vertex-2-0/` | 474 | preuves du programme en cours ; lu par `tools/vertex_2_0_capture.py` |
| `docs/refactor/` | 683 | journal SKYLER ; gardé par `tests/test_skyler_index_integrity_lot228.py` et `tests/test_visual_shell_lot620.py` |
| `docs/vertex-1.0/` | 58 | contrats 1.0 ; existence gardée par `tests/test_vertex_1_0_contract.py` |
| `docs/visual/` | 6 | bibliothèque de widgets ; lue par `vertex/ui/pages/widget_lab.py` |
| `docs/skyler/` | 4 | statut et convergence ; gardé par `tests/test_references_vivantes_lot364.py` |
| `docs/archives/` | 209 | rapports historiques, onze thèmes, index propre |

## Ce que cet audit ne dit pas

- Il porte sur les **dossiers et fichiers**, pas sur les fonctions. Un module
  atteignable peut contenir du code mort ; cette mesure ne le voit pas.
- Il ne rouvre pas le recensement d'atteignabilité des modules `vertex/`
  (85 modules non atteignables depuis `terminal.py` relevés en son temps).
  Non atteignable n'est pas synonyme de supprimable, et trancher demande un lot
  par paquet, avec migration et rollback — pas un rangement d'arborescence.
- Il ne juge pas le **contenu** des archives. Leurs chiffres décrivent leur
  commit d'origine, pas le commit courant.

## Rollback

Le rangement est un ensemble de `git mv` et de substitutions de chemins.
`git revert` du commit restaure l'arborescence antérieure sans perte : aucun
octet de contenu documentaire n'a été supprimé.
