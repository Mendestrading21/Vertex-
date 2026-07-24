# Validation — PR n°2 : Navigation & Architecture des pages

> Branche `agent/vertex-total-rebuild`. Décision produit : **8 espaces canoniques,
> registre unique.** Aucune refonte de contenu, aucun moteur modifié, IBKR
> READONLY intact, pas de migration big-bang. Conforme à `VERTEX_CONSTITUTION.md`.

## 1. Arborescence de navigation — avant / après

| # | AVANT (9) | APRÈS (8) |
|---|---|---|
| 1 | Briefing `/` | **Aujourd'hui** `/` |
| 2 | Marchés `/markets` | Marchés `/markets` |
| 3 | Opportunités `/opportunities` | Opportunités `/opportunities` |
| 4 | Portefeuille `/portfolio` | **Analyse** `/analysis` |
| 5 | Analyse `/analysis` | **Portefeuille** `/portfolio` |
| 6 | Options `/options` | Options `/options` *(autonome)* |
| 7 | Performance `/performance` | **Journal** `/journal` |
| 8 | Intelligence `/intelligence` | Système `/system` |
| 9 | Système `/system` | — |

- **Retirés du nav principal** : Performance, Intelligence.
- **Ajouté** : Journal (espace n°7).
- **Renommé** : Briefing → « Aujourd'hui ».
- Système reste épinglé en pied de sidebar (dernier élément).
- **Un seul registre canonique** : `vertex/ui/shell/__init__.py` `PRIMARY_NAV`.
  `vertex/ui/nav.py` = registre du **monolithe legacy** (encore utilisé par les
  pages `PAGE_*` de `terminal.py`, gardé par `test_nav.py`) → **conservé**,
  retrait différé après preuve complète (Constitution loi 24).

## 2. Décisions d'architecture appliquées

- **Intelligence** n'est plus autonome. Page conservée **joignable hors nav**
  (`/intelligence` 200) ; l'intégration du raisonnement de comité dans Analyse est
  différée à la refonte Analyse (aucune fonctionnalité perdue).
- **Performance** n'est plus autonome. `/journal` rend la page méthode +
  journal + apprentissage ; la **performance de portefeuille** (equity/drawdown)
  y reste temporairement et migrera vers Portefeuille lors de la refonte de contenu.
- **Options** : espace principal **autonome** — retrait du back-link
  « ← Opportunités · Options » et de l'ambiguïté de double rattachement.
- **Suivis / tracking** rattachés au **Journal** (joignables hors nav, `/tracking`).
- **Contexte ticker** préservé d'Opportunités vers Analyse (vérifié navigateur).
- **Navigation mobile 390 px** repensée : barre = 5 espaces prioritaires
  (Aujourd'hui/Marchés/Opportunités/Analyse/Portefeuille), « Plus » = Options/
  Journal/Système. **0 débordement.**
- **Palette ⌘K** (infrastructure existante) mise à jour sur les 8 espaces + suivis
  + comité + design system + recherche de ticker.

## 3. Routes déplacées / redirigées

| Ancienne route | Nouveau comportement |
|---|---|
| `/performance` | **301 → `/journal`** (query préservée) |
| `/journal` | **route réelle 200** (était une redirection vers `/performance?view=journal`) |
| `/decisions` | 301 → `/journal?view=journal` (était `/performance?view=journal`) |
| `/review`, `/research`, `/equipe`, `/equipe-du-mois`, `/bordel`, `/strategy-os`, `/vertex-intelligence` | 301 → `/intelligence?view=…` (inchangé, page conservée) |
| `/journal?view=…`, `/journal?sym=…` | servis directement (sous-vues journal/track-record/learnings) |
| 37 autres redirections legacy | inchangées, toujours 301 |

Liens internes `/performance…` mis à jour → `/journal…` (analysis_page, intelligence_page,
vx-entities.js, performance_page) pour éviter un saut de redirection.

## 4. Doublons supprimés / levés

- **Double rattachement Options** (espace principal **et** sous-page d'Opportunités) → **levé** : Options est un espace autonome unique.
- **Deux « domiciles » de la performance de méthode** (Performance vs Journal) → **un seul** : Journal (`/performance` redirige).
- **Palette ⌘K** ne pointe plus vers les espaces disparus (Performance/Intelligence en tant qu'espaces) → entrées ré-ancrées (Journal, Analyse · Comité).
- Menu mobile « Plus » ne référence plus `intelligence` (id disparu du nav).

## 5. Fichiers modifiés

- `vertex/ui/shell/__init__.py` — `PRIMARY_NAV` (8), icône `book`, `_mobile_bar` (5 prioritaires).
- `vertex/app/routes/redesign.py` — route `/journal`, `/performance`→`/journal`, `/decisions`→`/journal`, commentaires Options/tracking.
- `vertex/ui/pages/performance_page.py` — identité **Journal** (shell, H1, tabs, liens).
- `vertex/ui/pages/options_intel_page.py` — Options autonome (H1, retrait back-link, sub-label, docstring).
- `vertex/static/vertex/js/vx-shell.js` — palette ⌘K (8 espaces) + menu mobile « Plus ».
- `vertex/ui/pages/analysis_page.py`, `intelligence_page.py`, `vx-entities.js` — liens `/performance`→`/journal`.
- `vertex/app/routes/system.py` — SW `td-shell-v44 → v45`.
- Tests : `test_redesign_ui.py` (nav 8, sous-vues, redirections, shell), `test_ui_v3.py`, `test_full_system_integration.py`, `test_journal_page.py`, `test_options_routes.py`, `test_production_guards_canonical.py` (SW v45).

## 6. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **908 passed, 2 skipped**.
- Gardiens clés verts : `test_primary_navigation_has_eight_canonical_spaces`,
  `test_every_primary_route_returns_200` (8×200), `test_old_routes_redirect`
  (toutes 301, Location correcte), `test_no_dead_links`, `test_subviews_return_200`,
  `test_redirect_preserves_ticker_and_filters` (`/decisions?sym=NVDA` conserve `sym`),
  `test_nav.py` (registre legacy monolithe intact), `test_no_orders` (READONLY).

## 7. Contrôle navigateur (390 / 768 / 1440)

Overflow réel (contenu hors conteneur de scroll intentionnel) :

| Viewport | Résultat |
|---|---|
| **mobile 390** | 8/8 pages **OK** (today, journal, options, analyse, opportunités, portefeuille, système, marchés) |
| **tablet 768** | 8/8 pages **OK** |
| **desktop 1440** | today / journal / options **OK** |

- **Contexte ticker** : `/opportunities` → clic sur `ACN` → **`/analysis/ACN`** ✔.
- **Retour arrière navigateur** : revient à `/opportunities` ✔.
- Sidebar affiche les **8 libellés** (Aujourd'hui … Journal … Système), aucun
  Performance/Intelligence. `/sw.js` sert `td-shell-v45`.
- Captures : scratchpad `nav2shots/` (desktop + mobile de Aujourd'hui, Journal, Options).

## 8. Erreurs restantes

- `GET /api/client-log` → `{"count":0,"errors":[]}` — **0 erreur applicative**.
- Console navigateur : **0 erreur d'app** (hors `ERR_CONNECTION_RESET` = ressource
  externe Google Fonts bloquée par le proxy sandbox, non applicative).

## 9. Risques

- **Interim assumé** : la performance de portefeuille vit temporairement sous
  Journal ; le raisonnement de comité reste sous `/intelligence` (hors nav). Ces
  contenus migreront lors des refontes Portefeuille / Analyse (documenté, non perdu).
- **`ui/nav.py` conservé** : deux registres coexistent encore (canonique
  `PRIMARY_NAV` vs legacy monolithe) tant que les pages `PAGE_*` de `terminal.py`
  vivent — retrait uniquement après preuve (Constitution loi 24).
- **SW** : les clients doivent recharger pour prendre `v45` (comportement normal).
- Validation navigateur en Chromium **headless** (pas d'appareil physique).

## 10. Plan précis de la PR suivante — Aujourd'hui + Marchés

**Objectif** : refondre le **contenu** des deux premiers espaces selon la
`VERTEX_PRODUCT_BIBLE.md` (§3.1, §3.2) et la Constitution, en s'appuyant sur les
composants de la PR Design n°1.

**Aujourd'hui (`/`)**
1. Niveau 1 : bandeau **régime + confiance** (jauge unique) · **risque n°1** ·
   **action du jour** · **diff « depuis ta dernière visite »** (composant nouveau).
2. Niveau 2 : 3 catalyseurs datés · top 2 opportunités (R:R) · mini-marché
   (→ Marchés) · posture comité. **Supprimer** SPY/rotation/calendrier *détaillés*
   (domiciliés dans Marchés) — dé-duplication (Constitution loi 6).
3. Densité ≤ 4 KPI / ≤ 3 graphiques ; prochaine action analytique explicite.

**Marchés (`/markets`)**
1. Niveau 1 : régime + confiance (**une** jauge) · breadth · rotation dominante.
2. **Fusionner** la suite secteurs (4 vues → 2 : RRG décisionnel + heatmap détail) ;
   **une** jauge par métrique (retirer les jauges régime/breadth/VIX dupliquées).
3. Chart Shell complet (conclusion + fraîcheur + unité) sur chaque graphique.

**Validation cible** : tests 100 % · 0 débordement 390/768/1440 · 0 console ·
chaque graphique avec conclusion · dé-duplication mesurée (compte de graphiques
avant/après) · SW bump · READONLY intact · captures avant/après.

## Verdict

**GO.** Architecture de navigation unique à 8 espaces livrée, testée et vérifiée
au navigateur ; 908 tests verts ; 0 lien mort ; contexte ticker et retour arrière
préservés ; 0 débordement ; 0 erreur console. Prête pour la refonte de contenu
page par page (PR suivante : Aujourd'hui + Marchés).
