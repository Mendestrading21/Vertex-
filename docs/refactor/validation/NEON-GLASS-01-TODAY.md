# Validation — NEON GLASS 01 : Prototype « Aujourd'hui »

> Issue #14. Premier livrable : audit graphique + Graph System V2 + **prototype
> Aujourd'hui uniquement** + tests + captures. Branche `agent/vertex-neon-glass-graphs`
> (base `84fbdc5`). **Aucun moteur, aucune donnée, aucun calcul, aucun IBKR modifié.
> READONLY intact. Pas de migration des 7 autres espaces avant validation humaine.**

## 1. Fichiers du livrable

- `docs/visual/VERTEX_NEON_GLASS_GRAPH_AUDIT.md` — **audit graphique complet** (Phase 0).
- `docs/visual/VERTEX_NEON_GLASS_SYSTEM.md` — **Graph System V2** (tokens, variantes de
  carte, Chart Shell V2, tooltip/légende/axes/annotations V2, états).
- `vertex/static/vertex/css/neon-glass.css` (**nouveau**) — le système rendu visible,
  **scopé** `.vx-content[data-space="briefing"]`.
- `vertex/ui/shell/__init__.py` — lien CSS neon-glass + `data-space="{active}"` sur
  `.vx-content` (hook de scope, sans effet sur les autres espaces).
- `vertex/app/routes/system.py` — service worker `td-shell-v50 → v51` (le head du shell
  a changé : nouvel asset CSS).
- `tests/test_neon_glass_01.py` (**nouveau, 8 gardiens**) + gardiens SW v51.

## 2. Audit graphique (résumé)

**~41 instances de graphes → ~15 primitives** réutilisables. Doublons majeurs : jauge
**×7**, timeline **×3**, payoff **×3**, scatter/quadrants **×2**, funnel **×2**,
contribution bars **×3-7**. Contrat `C.card` documenté et **à préserver**. Détail
complet : `VERTEX_NEON_GLASS_GRAPH_AUDIT.md`.

## 3. Direction visuelle appliquée (prototype)

| Règle issue #14 | Implémentation |
|---|---|
| Fond noir profond légèrement bleuté | halos radiaux fonctionnels (cuivre + bleu discret) sur `#05070c→#080b12` |
| Cartes glass premium | `backdrop-filter: blur(14px)` + bordure chaude `rgba(255,150,70,.16)` + filet cuivre + ombre douce |
| Identité orange néon / cuivre | `--ng-neon #ff7a1e`, `--ng-copper #c9631f` ; titre Hero + bouton action en orange néon |
| **Aucun bleu identitaire** | le bleu n'existe que comme halo de fond très discret ; `--vx-brand` local = orange néon |
| Sémantiques | vert=gain, rouge=risque/perte, ambre=attente, violet=options (inchangés) |
| Glow seulement live/actif/hover | `.vx-live-dot` sans glow par défaut ; halo pulsé uniquement `data-live` ; lift au hover |
| Micro-graphes vivants | conteneurs canvas en verre, reveal 180 ms, skeleton shimmer |
| Motion 120-240 ms + reduced-motion | `--ng-motion 180ms` ; `@media (prefers-reduced-motion: reduce)` coupe tout |

## 4. Périmètre (scopé, pas de big-bang)

Le prototype ne peint QUE `[data-space="briefing"]` : Hero, 4 KPI, Diff, Régime (jauge),
opportunités, alertes, catalyseurs, portefeuille — **sans changer une seule donnée**.
Les 7 autres espaces sont **strictement inchangés** (vérifié : `/markets` porte
`data-space="markets"`, aucune règle `.vx-card` non scopée dans neon-glass.css).

## 5. Tests

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **958 passed, 2 skipped** (+8 gardiens neon-glass).
- Gardiens neon-glass : css présent+lié, scope briefing only (pas de `.vx-card` global),
  identité orange néon sans bleu, glass premium (blur + bordure chaude), glow réservé
  live/hover, reduced-motion respecté, autres espaces intacts, READONLY intact.
- Gardiens SW v51 (vN présent, v(N-1) absent) mis à jour.

## 6. Captures & responsive (mesuré)

Sweep Playwright sur **/** (Aujourd'hui) à 3 viewports :

| Viewport | Débordement réel | Erreurs console applicatives |
|---|---|---|
| **1440×900 desktop** | **0 px** | **0** |
| **768×1024 tablette** | **0 px** | **0** |
| **390×844 mobile** | **0 px** | **0** |

Captures : `scratchpad/neon1shots/today-{desktop,tablet,mobile}.png`. Vérifié
visuellement : fond bleuté, cartes glass, titre + bouton orange néon, KPI glass,
sémantiques correctes (risque rouge / opportunité vert / breadth ambre), bannière DÉMO
glass. La sidebar (hors `.vx-content`) conserve l'ancien thème — normal (prototype scopé).

## 7. Invariants respectés

READONLY absolu (aucun chemin d'ordre) · aucun moteur/donnée/calcul modifié · aucune
donnée inventée (états honnêtes conservés) · pas de duplication de graphiques ajoutée ·
pas de nouvelle route métier · pas de suppression de code · pas de bleu identitaire ·
**pas de merge `main`, pas de tag, pas de release**.

## 8. Reste à faire (APRÈS validation humaine — ne pas démarrer sans accord)

Migration page par page dans l'ordre imposé (Marchés → Système), convergence des ~41
graphes vers les ~15 primitives (jauge unique, timeline unique, payoff unique, quadrant
unique, contribution bars unique), Chart Shell V2 sur les canvas Chart.js (tooltip verre,
légendes/axes V2), captures avant/après par page, bump SW par page si nécessaire, rapport
de validation dédié par espace. **Le prototype établit le niveau de qualité final.**

## Verdict

**Prototype Aujourd'hui livré.** Le langage neon-glass est établi et visible, scopé,
sans régression (958 tests verts, 0 débordement, 0 console, READONLY intact). **Arrêt
pour validation humaine avant de migrer les 7 autres espaces**, conformément à l'issue.
