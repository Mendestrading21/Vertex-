# VERTEX — Audit forensique (Phase 0)

Analyse factuelle du dépôt `Mendestrading21/IBKT-DASHBORD-`. Chaque constat est
mesuré, pas subjectif. Objectif : établir la base honnête avant transformation.

---

## Scores actuels

| Axe | Score | Justification (factuelle) |
|---|---|---|
| **Global** | **62 / 100** | Produit riche, sûr et fonctionnel, mais porté par un monolithe difficile à maintenir. |
| **Architecture** | **35 / 100** | `terminal.py` = 9 782 lignes ; **452 lignes > 400 caractères** (JS embarqué) ; UI en chaînes Python ; 6× la même barre de nav dupliquée. |
| **UI / Design** | **55 / 100** | Visuellement riche et récemment nettoyée (débordements corrigés), mais dense, chargée d'emojis, styles inline, aucun design system. |
| **Quant** | **78 / 100** | Point fort : Monte-Carlo, bootstrap, Kelly plafonné, validator walk-forward **sans lookahead**, physique (Hurst/entropie/OU), confluence multi-horizons, scores bornés [0,100]. |
| **Sécurité** | **85 / 100** | **0 appel d'ordre** dans tout le dépôt, IBKR `readonly=True`, verrou d'accès, secrets hors dépôt (`.env` gitignoré), JSON NaN-safe. |
| **Maintenabilité** | **38 / 100** | God-functions (274/266/256 lignes), UI non testable (dans des f-strings), duplication. Atténué : suite de tests désormais présente. |

---

## Architecture actuelle

- **`terminal.py` (9 782 lignes, 142 fonctions)** — mélange routes Flask + HTML/CSS/JS
  embarqués + logique métier + workers + données. C'est le cœur du problème.
- **`elio/` (23 modules, ~4 300 lignes)** — moteurs quant bien séparés. `terminal.py`
  dépend de **21** d'entre eux (physique ×24, options ×13, anomalies ×10, vertex ×9…).
- **`vertex/` (nouveau)** — package institutionnel amorcé (data/app/services).
- **Scripts racine (~2 000 lignes)** — outils/legacy (`paper_bot`, `dashboard`,
  `gex_dashboard`, `notion_sync`, `ib_reader`, backtests…), statut à clarifier.

### Fonctions trop longues (à découper)
| Fonction | Lignes | Rôle |
|---|---|---|
| `_ibkr_opt_worker` | 274 | worker options IBKR |
| `analyse` | 266 | moteur d'analyse par titre (fait tout) |
| `scan` | 256 | boucle de scan de l'univers |
| `options_pack` | 132 | assemblage fiche options |
| `posq` / `edge_backtest` / `api_command` | 107 / 97 / 88 | — |

---

## Dette technique classée

### 🔴 CRITIQUE
1. **Monolithe `terminal.py`** — routes + UI + logique + données dans un seul fichier de ~9,8k lignes. Bloque la testabilité, la relecture, la parallélisation du travail.
2. **UI en chaînes Python** — HTML/CSS/JS dans des f-strings (**452 méga-lignes > 400 car.**). Non testable, non lintable, source des débordements de texte.

### 🟠 HAUTE
3. **God-functions** — `analyse` (266), `scan` (256), `_ibkr_opt_worker` (274) font trop de choses. À décomposer par responsabilité.
4. **Logique dupliquée** — barre de nav ×6, Black-Scholes (`_gamma/_npdf/_ncdf`) dans `terminal.py` ET `elio/options.py`, scoring de reco en double dans `options.py`. Risque de divergence silencieuse.
5. **`except Exception: pass`** — plusieurs blocs avalent les erreurs (boucle de scan par titre) : des bugs deviennent invisibles (moins de titres, sans raison).

### 🟡 MOYENNE
6. **Double source pour l'auth** — verrou d'accès défini dans `vertex/app/config.py` (nouveau) et encore dans `terminal.py`. À consolider (Phase Sécurité).
7. **Pas de couche Data-Quality** — la fraîcheur/absence de données n'est pas toujours répercutée dans les décisions (Phase 10).
8. **Pas de Decision Stack unifié** — la décision est éparpillée (`verdict`, `vertex`, `committee`, `research`). À unifier (Phase Decision Stack).
9. **Performance** — réponse `/scan` volumineuse (~8 Mo, gzip actif) ; scan lourd sur CPU bridé.

### 🟢 BASSE
10. **Scripts racine legacy** — statut à clarifier / déplacer sous `tools/`.
11. **Nombres magiques** — certains seuils de scoring non nommés/documentés.
12. **UI emoji-heavy** vs cible institutionnelle sobre.

---

## Risques évalués

| Risque | Niveau | Constat |
|---|---|---|
| **Crash / NaN** | 🟡 faible | Garde-fous NaN posés (RSI, MM, JSON provider) ; restent des `except` larges. |
| **Fausses données** | 🟡 moyen | Mode démo clairement étiqueté ; mais staleness pas toujours pénalisée dans la décision → **Phase 10**. |
| **Lookahead bias** | 🟢 OK | Validator & backtest utilisent le **signal de la veille** — vérifié, pas de lookahead. |
| **IBKR / threading** | 🟢 OK | `ib_async` non thread-safe → **un seul worker** en file d'attente (mitigation correcte). |
| **Cache / stale** | 🟡 moyen | Caches disque présents ; fraîcheur exposée via `/api/system-status` mais pas encore contraignante. |
| **UI** | 🟢 OK | Débordements corrigés, tables enveloppées, 0 erreur JS (15 pages auditées). |
| **Performance** | 🟡 moyen | Payload `/scan` lourd, scan CPU-intensif → **Phase 11**. |

---

## Conclusion & priorités

Le **quant et la sécurité sont solides** ; le **frein est l'architecture** (monolithe + UI en chaînes). La transformation doit donc, dans l'ordre :

1. **Architecture** — package `vertex/`, factory Flask, routes découpées (Phase 1). *(fondation posée)*
2. **UI hors des chaînes Python** + design system (Phases 2-5).
3. **Decision Stack unifié** + Data-Quality (Phases 6, 10).
4. **Tests par moteur + CI** en filet permanent (Phase 12). *(amorcé)*

Chaque étape en PR petite, testée, sans régression, en préservant l'invariant **lecture seule**.
