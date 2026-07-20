# 00 — Résumé exécutif (audit de référence Vertex)

> Audit **vivant**. Source de vérité = le code réel (chemins:lignes cités). Consolide/relie les ~40 docs
> existants sans les copier. Gravité : **P0** (bloquant/mensonge de donnée/casse) · **P1** (incohérence
> structurante) · **P2** (dette) · **P3** (finition).

## Ce qu'est Vertex
L'**ordinateur de décision au-dessus d'IBKR** : IBKR détient comptes/positions/ordres/données ; Vertex lit,
vérifie la qualité, analyse, détecte le risque et les opportunités, recommande, **prépare** les ordres, mesure,
apprend, et **explique**. Stack = **Flask monolithe** `terminal.py` (~11k lignes, HTML/JS en chaînes Python) +
package `vertex/`. **Pas de React.**

## Invariant produit ABSOLU
**Lecture seule.** Vertex ne passe **jamais** d'ordre (live ni paper). `READONLY=True` (`vertex/app/config.py`),
4 workers IBKR `readonly=True` (`terminal.py:846/2378/2492/2587`), 17 outils d'ordre interdits
(`vertex/ai/tool_registry.py`). Le « Desk » = **préparation + simulation + ticket prêt-à-coller** ; jamais de
transmission. Cet audit ne propose aucun chemin d'ordre.

## État général
Base **mature et fonctionnelle** : 8 espaces servis par le blueprint `redesign` via un shell unique + `ui/pages/`,
design Black Glass (`glass.css`), chart system unifié `VXCharts`, moteurs de décision déterministes, IBKR
read-only honnête (garde-fou fraîcheur 75 s), **919 tests verts**. La mission n'est **pas** de reconstruire mais
de **consolider, combler, polir**.

## Top findings (détail dans les docs dédiés)
| ID | Gravité | Sujet | Doc |
|----|---------|-------|-----|
| IA-01 | **P1** | Double navigation : `PRIMARY_NAV` (shell, 8 items canoniques) vs `vertex/ui/nav.py` (10 items legacy, routes `/stocks`,`/strategie`,`/journal`…) | 04 |
| RT-01 | **P1** | Collision de route `/options/<sym>` : JSON `opt_ep` (`terminal.py:2354`) **et** page HTML `options_symbol_route` (`redesign.py:137`) | 02 |
| CMP-01 | **P1** | `.vx-card` redéfini dans 6 feuilles CSS (base/cockpit/components/glass/polish/premium) | 05 |
| CMP-02 | **P1** | 4 systèmes de tuiles KPI concurrents : `vx-kpi`(36) · `vx-metric`(50) · `vx-stat`(52) · `vx-stat-xl`(6) → fusionner en un MetricCard | 05 |
| DES-01 | **P1** | Docs de design périmés (`VERTEX_DESIGN_TOKENS`, `VERTEX_CHART_LIBRARY` : palette orange/bleu abandonnée) contredisent `glass.css` | 05 |
| DAT-01 | **P0** | Piège « 0-masquerade » : chaîne d'options vide risque de s'afficher `0` au lieu de `unavailable` (`terminal.py:~900-905`) | 06 |
| DAT-02 | P2 | Enveloppe de provenance éclatée (`_live_meta`/`_live_quotes`/`marketDataType`) — pas de `ProvenancedValue` unique | 06 |

## Décisions structurantes actées
1. **Lecture seule STRICTE conservée** — « Desk/Exécution » reformulé en préparation/simulation (voir `17-decisions-log.md`).
2. **Fondation d'abord** : cette session = skill + agents + rules + audit (docs), **zéro code applicatif touché**
   → 919 tests inchangés. Implémentation par lots vérifiés ensuite.

## Séquence recommandée
Phase 0 sécurisation → Phase 1 (cet audit) → Phase 2 fondations (tokens/cartes/charts partagés, résoudre CMP-01/02,
DES-01) → Phase 3 shell (résoudre IA-01) → Phases 4-13 page par page → Phase 14 validation. Détail : `14-prioritized-roadmap.md`.
