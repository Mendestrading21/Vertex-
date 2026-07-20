# Fiches d'audit par page

Une fiche `docs/vertex-audit/pages/<route>.md` par espace, au gabarit
`.claude/skills/vertex-maximum/templates/page-audit-template.md`. Produites **au fil de l'implémentation** (une
avant chaque lot de refonte de page) ; les plus urgentes sont amorcées ci-dessous.

| Fiche | Route | Renderer | Priorité | Statut |
|---|---|---|---|---|
| `options.md` | `/options` (+`/options/<sym>`) | `options_intel_page.py` · `options_symbol_page.py` | 🔴 RT-01 | amorcée |
| `portfolio.md` | `/portfolio` (+`/tracking`) | `portfolio_page.py` | 🔴 DAT-01/03 | amorcée |
| _dashboard.md_ | `/` | `briefing.py` | 🟡 | à produire |
| _opportunities.md_ | `/opportunities` | `opportunities_page.py` | 🟡 | à produire |
| _analysis.md_ | `/analysis/<sym>` | `analysis_page.py` | 🟡 (PRF-01) | à produire |
| _performance.md_ | `/performance` | `performance_page.py` | 🟡 | à produire |
| _intelligence.md_ | `/intelligence` | `intelligence_page.py` | 🟡 | à produire |
| _system.md_ | `/system` | `system_page.py` | 🟡 | à produire |
| _preparation.md_ | (à créer, prep/sim) | `desk.py`+`planning_api.py` | ⬜ | à concevoir |

Statut global des pages : `../15-page-status-matrix.md`.
