# Lot 0 — Baseline visuelle Vertex 2.0

Aucune modification runtime dans ce lot : relevé, inventaire et captures avant.

## Repère de départ

| Élément | Valeur |
|---|---|
| Branche de travail | `claude/vertex-2-0-visual-redesign-vy3h7s` |
| SHA de base | `eff337f` (`main`) |
| Skill maître | PR #838 — `agent/vertex-design-2-0-master-20260827` (importé dans la branche) |
| Mode d'exécution des preuves | `DEMO=1 NO_IBKR=1`, serveur Flask local `127.0.0.1:8099` |
| `/healthz` | `200` |

## Suite de tests — état de départ

`python -m pytest -q` → **4243 passés, 154 ignorés, 1 échec**.

| Test | État | Cause |
|---|---|---|
| `test_vertex_1_0_branches.py::test_la_classification_est_discriminante` | Échec | **Environnemental** : le test exige `> 100` références git ; ce clone frais n'en porte que 3. Aucun rapport avec la refonte. |
| `test_namespace_guards.py::test_no_personal_name_in_current_tree` | Corrigé | Le skill importé de la PR #838 contenait un nom personnel dans `references/product-contract.md`. Neutralisé (« son utilisateur »), gardien vert. |

Dépendances installées pour exécuter le produit : `flask, pandas, numpy, requests,
python-dotenv, markupsafe, yfinance, ib_async, anthropic, gunicorn, pytest, playwright`.

## Limite d'environnement déclarée

**L'egress réseau vers les fournisseurs de marché est bloqué** (yfinance/stooq → `CONNECT tunnel failed, 403`).
Vertex s'exécute donc dans son état dégradé honnête : `—` / `n/d` partout où une valeur
de marché serait attendue. Cet état est **déterministe**, ce qui le rend valide comme base
avant/après (même route, même viewport, même état de données), et il exerce directement les
contrôles 007, 008, 009, 044 et 056. Les états `LIVE`/`DELAYED` réels ne sont pas
observables ici et resteront une limite déclarée.

## Inventaire des routes réellement servies

| Route | Code | Destination réelle | Page cible 2.0 |
|---|---|---|---|
| `/` | 200 | `briefing.py` — « Dashboard » | **Aujourd'hui** |
| `/markets` | 302 | → `/` (Marchés fusionné dans le Dashboard) | **Marchés** (à rétablir) |
| `/opportunities` | 200 | `opportunities_page.py` | **Opportunités** |
| `/analysis` | 200 | `analysis_page.py` | **Analyse** |
| `/options` | 200 | `options_intel_page.py` | **Options** |
| `/portfolio` | 200 | `portfolio_page.py` | **Portefeuille** |
| `/journal` | 200 | `performance_page.py` | **Performance** (Journal devient sous-vue) |
| `/tracking` | 200 | `tracking_page.py` | **Suivi** |
| `/intelligence` | 200 | `intelligence_page.py` | **Vertex IA** |
| `/system` | 200 | `system_page.py` | **Système** |
| `/design-system` | 200 | `design_system_page.py` | interne QA |
| `/calendar` | 301 | → `/opportunities?view=calendar` | **Calendrier** (page propre) |
| `/performance` | 301 | → `/journal` | **Performance** |
| `/simulator` | 404 | — | **Simulateur** (à composer) |
| `/follow-up` | 404 | — | **Suivi** |

## Écart navigation : 7 entrées servies vs 12 pages cibles

`PRIMARY_NAV` (`vertex/ui/shell/__init__.py`) porte 7 entrées **non groupées** :
Dashboard · Opportunités · Analyse · Portefeuille · Options · Journal · Système.

Cible : 4 groupes + utilitaire épinglé —
**Piloter** (Aujourd'hui, Calendrier) · **Explorer** (Marchés, Opportunités, Analyse,
Options, Simulateur) · **Gérer** (Portefeuille, Suivi, Performance) ·
**Intelligence** (Vertex IA) · **Système** épinglé en bas.

Manquants dans la navigation actuelle : Calendrier, Marchés, Simulateur, Suivi, Performance.
Aucune page existante ne sera supprimée : `/journal` et `/tracking` deviennent des
destinations conservées qui pointent vers leur propriétaire canonique.

## Contradictions visuelles relevées (captures avant)

1. **Polices hors doctrine** — `fonts.css` charge General Sans + JetBrains Mono ;
   la direction 2.0 impose Geist + Geist Mono.
2. **Rectangle vide brut** — `/options`, bloc « Depuis le tableau : » rend un rectangle
   graphite sans titre, sans cause, sans action. Violation directe de
   « Jamais de rectangle vide » et du contrôle 044.
3. **Navigation plate** — aucun regroupement par travail ; l'utilisateur ne distingue pas
   Piloter d'Explorer.
4. **`Dashboard` en anglais** dans la navigation et le titre de page, alors que le produit
   est intégralement francophone (contrôles 029, 114, 115).
5. **15 feuilles CSS empilées** (`tokens → … → glass`) sans couche de vérité finale unique ;
   la doctrine 2.0 demande une source de vérité de tokens.
6. **Marchés sans page propre** — la sous-vue est diluée dans le Dashboard, ce qui empêche
   « une visualisation dominante par sous-vue ».
7. **Bande KPI de 12 tuiles égales** en tête d'accueil : aucun point focal, contradiction
   avec « le point focal est une DecisionTrace, pas une grille de KPI égaux » (contrôles 032, 035).

## Captures avant

`docs/vertex-2-0/preuves/lot-00-avant/` — 11 routes × desktop 1440×1000 + mobile 390×844,
capturées sur l'application **réellement exécutée** (Chromium, `device_scale_factor=2`,
locale `fr-FR`, fuseau `Europe/Zurich`). Outil : `tools/vertex_2_0_capture.py`.

`rapport.json` enregistre par route : erreurs page, messages console `error`/`warning`
et débordement horizontal mesuré.

**Résultat de départ : 0 erreur page, 0 débordement horizontal sur les 11 routes,
en desktop comme en mobile.** C'est le niveau à ne pas régresser.

## Actif ajouté dans ce lot

`vertex/static/vertex/fonts/geist-variable.woff2` (69 ko) et
`geist-mono-variable.woff2` (71 ko), auto-hébergés — aucune dépendance CDN, le produit
reste fonctionnel hors ligne. Licence **SIL Open Font License 1.1** copiée dans
`vertex/static/vertex/fonts/licences/GEIST-OFL.txt` (contrôle 073). Les fichiers ne sont
pas encore déclarés dans `fonts.css` : la bascule appartient au lot 1.

## Rollback

`git revert` du commit de lot suffit : aucun moteur, endpoint, store ni schéma n'est touché.
