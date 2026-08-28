# Sources méthodologiques GitHub

Ces projets servent à améliorer la méthode. Ils ne sont ni copiés dans Vertex
ni requis au runtime. Le contrat produit, la confidentialité, les licences et
les preuves du dépôt restent prioritaires.

## UI UX Pro Max

Source : https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Retenu : design system persistant, raisonnement par domaine, dials densité/motion/variance, priorité accessibilité → interaction → performance → layout, discipline graphiques et contrôle avant livraison.

## Interface Design

Source : https://github.com/Dammyjay93/interface-design

Retenu : mémoire `.interface-design/system.md`, design craft-first, refus des défauts génériques, navigation et données comme décisions de design, tests permutation/distance/signature/tokens.

## Vercel Web Interface Guidelines

Source : https://github.com/vercel-labs/web-interface-guidelines

Retenu : audit final séparé de la création, revue du code visuel réellement modifié, accessibilité, formulaires, navigation, dark mode, performance et internationalisation.

## Anthropic Frontend Design

Source : https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

Retenu : direction spécifique au sujet, une signature unique, critique avant/après construction, complexité proportionnée à la vision, motion concentrée et microcopy conçue comme matériau d'interface.

## Anthropic Code Review et Security Review

Sources : https://github.com/anthropics/claude-code/tree/main/plugins/code-review
et https://github.com/anthropics/claude-code-security-review

Retenu : revues indépendantes du diff, seuil de confiance, modèle de menace,
priorité aux défauts exploitables et preuves reproductibles.

## GitHub Awesome Copilot — méthodes retenues

Source : https://github.com/github/awesome-copilot/tree/main/skills

Retenir uniquement les méthodes utiles, sans installer le catalogue :

- `acquire-codebase-knowledge` : documenter seulement ce qui est prouvé par
  le dépôt ou le terminal, marquer les inconnues et comparer intention/réalité ;
- `audit-integrity` : vérifier que tests, rapports et exceptions n'occultent
  pas une perte réelle ; particulièrement important avec `_supersede.py` ;
- `anti-ui-slop` : partir du produit, des composants et des états réels, puis
  exécuter une passe de finition observable ; aucune dépendance UIZZE requise ;
- `agent-supply-chain` : traiter skills, hooks, MCP et actions comme une chaîne
  logicielle à permissions et provenance vérifiables.

Ces skills sont des sources de méthode. Leur structure, leurs templates et
leurs services optionnels ne sont ni copiés ni activés automatiquement.

## Trail of Bits

Source : https://github.com/trailofbits/skills

Retenu : differential review, insecure defaults, property-based testing,
analyse statique et supply-chain risk. Licence CC-BY-SA-4.0 : ne pas recopier
le corps des skills dans Vertex.

## Qualité et observabilité

Sources : https://github.com/microsoft/playwright,
https://github.com/GoogleChrome/lighthouse-ci,
https://github.com/astral-sh/ruff,
https://github.com/open-telemetry/opentelemetry-python et
https://github.com/locustio/locust.

Retenu : comportement navigateur réel, budgets visuels/performance, lint rapide,
télémétrie redacted et charge reproductible. Chaque adoption reste séparée et
auditée ; Playwright doit réellement installer/exécuter Chromium en CI.

Compléments officiels à évaluer lot par lot :

- axe-core : règles d'accessibilité automatisées, complétées par clavier,
  zoom, lecteur d'écran et revue humaine ;
- Semgrep/CodeQL : règles ciblées sur secrets, routes d'écriture, appels IBKR
  interdits, `innerHTML` et défauts Flask ;
- `pip-audit` : vulnérabilités des dépendances Python verrouillées ;
- OpenSSF Scorecard : santé supply-chain des nouvelles dépendances ;
- OpenTelemetry : traces et métriques redacted ;
- Locust : profils de charge chaude, froide, dégradée et concurrente.

Sources : https://github.com/dequelabs/axe-core,
https://github.com/semgrep/semgrep,
https://github.com/github/codeql,
https://github.com/pypa/pip-audit et
https://github.com/ossf/scorecard.

## Recherche quantitative et contrats de données

Sources qualifiées :

- [skfolio](https://github.com/skfolio/skfolio) : API inspirée de scikit-learn,
  optimisation, risque, stress et méthodes de validation chronologique/purgée ;
- [PyBroker](https://github.com/edtechre/pybroker) : walk-forward, slippage,
  bootstrap et diagnostics de stratégies ;
- [vectorbt](https://github.com/polakowo/vectorbt) : exploration vectorisée à
  grande échelle, à confiner au sandbox pour limiter l'overfit ;
- [QuantLib](https://github.com/lballabio/QuantLib) : moteurs de pricing et jeux
  de tests numériques servant de référence possible ;
- [QuantStats](https://github.com/ranaroussi/quantstats) et
  [QuantInvestStrats](https://github.com/ArturSepp/QuantInvestStrats) :
  performance, risque et formes de factsheets ;
- [Pandera](https://github.com/unionai-oss/pandera) : validation de DataFrames,
  à comparer à des validateurs locaux car son coût peut être significatif ;
- [Hypothesis](https://github.com/HypothesisWorks/hypothesis) : tests par
  propriétés et réduction automatique des cas financiers hostiles.

Lire `strategy-research-lab.md` pour les règles anti-look-ahead, coûts,
walk-forward, biais, stabilité et acceptation. Ces projets ne forment pas une
stack à installer ensemble.

## Frontend Design Principles

Source : https://github.com/joshuadavidthomas/agent-skills/tree/main/frontend-design-principles

Retenu : explorer le monde réel du produit, nommer les défauts à rejeter, tokens appartenant au domaine et cohérence entre intention, palette, typographie, profondeur et structure.

## Adaptation Vertex

- Densité 8/10, motion 2/10, variance 4/10.
- Signature structurelle `Decision Trace`, propre à la chaîne de décision financière.
- Black Glass avec lumière locale issue des références, pas un dark dashboard générique.
- Flask/Python/JS existant, aucune hypothèse React/Tailwind.
- Français simple, données réelles, lecture seule et auditabilité avant esthétique.
- Les méthodes externes guident un lot ; elles n'autorisent jamais une
  permission, dépendance ou modification métier implicite.

## Matrice d'adoption

| Besoin Vertex | Méthode prioritaire | Preuve exigée avant adoption |
|---|---|---|
| Cartographie du monolithe | codebase knowledge + inventaire local | propriétaires, imports, routes, stores et preuves de chemin |
| Refonte visuelle | Frontend Design + Interface Design + anti-ui-slop | capture réelle, tokens locaux, états et test de finition |
| Régression fonctionnelle | Playwright + pytest de contrat | défaut rouge, parité, console/réseau et rollback |
| Accessibilité | axe-core + revue manuelle | 390/1024/1600, clavier, zoom, contraste et reduced motion |
| Sécurité applicative | Anthropic + Trail of Bits + Semgrep/CodeQL | modèle de menace, cas exploitable et faux positifs revus |
| Unités financières | dimensional analysis + golden/property tests | unité, conversion, tolérance et source documentées |
| Supply chain | pip-audit + Scorecard + revue des skills | version/SHA, licence, permissions, hooks et plan de retrait |
| Performance | Lighthouse CI + Locust + traces | baseline p50/p95/p99, budgets et scénario reproductible |
| Stratégies | skfolio/PyBroker comme méthodes + moteur local | point-in-time, walk-forward, coûts, benchmark, stabilité et replay |
| Calculs options | QuantLib comme référence potentielle | golden cases, unités, Greeks, tolérances et modèle nommé |
| Contrats tabulaires | validation locale puis Pandera si justifié | schéma hostile, coût p95 et plan de retrait |

La quantité de skills installés n'est jamais un objectif. Une méthode entre
dans le skill maître seulement si elle améliore un contrôle Vertex précis sans
ajouter d'autorité concurrente.

## Sources de widgets trading

Le catalogue détaillé et les licences sont dans `trading-widget-catalog.md`. Les sources principales auditées sont TradingView Lightweight Charts et ses plugins officiels, Perspective, Apache ECharts, Plotly.js, Grid.js, D3FC, Lab49 Value Flash, Ghostfolio, FreqUI, QuantStats, VolVisualizer, OpenAlgo et NQGEX. Une source peut inspirer une forme sans autoriser la copie de son code.

Le skill officiel Lightweight Charts a aussi été étudié pour retenir les pièges v5 : vérifier les typings locaux, timestamps en secondes, séries triées, lifecycle, resize, destruction, plugins et API publiques. Il ne remplace pas le contrat graphique Vertex.
