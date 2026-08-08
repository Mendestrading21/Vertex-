# SKYLER LOT 324 — Hygiène post-purge : 11 imports orphelins retirés + gardien

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-324` (base : lot 323 fusionné,
80a1729)

## La piste, trouvée avant de toucher

Une purge de -33 % laisse forcément des résidus : les **imports dont les
consommateurs viennent de disparaître**. Audit AST de `terminal.py` (noms liés
par import vs noms réellement référencés) → **11 imports orphelins**, dont 10
créés par la purge É1 et 1 antérieur.

| import | pourquoi orphelin |
|---|---|
| `from zoneinfo import ZoneInfo` | dernier usage dans une page morte |
| `vertex.data.constants as _vconst` | idem |
| `vertex.services.status_service as _status_svc` | idem |
| `vertex.engines.decision_stack as _decision` | idem |
| `vertex.engines.indicators as _indicators` | idem |
| `vertex.ui.options_lab as _olab_ui` | page Options Lab morte |
| `vertex.ui.journal as _tj_ui` | page Journal legacy morte |
| `vertex.ui.signals as _sg_ui` | page Signals morte |
| `vertex.ui.vault as _av_ui` | page Vault morte |
| `vertex.ui.strategy_os as _strategy_os_ui` | page Strategy OS morte |
| `vertex.strategy.config` | **antérieur à É1** — le commentaire au-dessus
  documentait déjà 5 retraits du même genre ; celui-ci avait survécu |

## Vérifications faites AVANT de retirer

1. **Aucun effet de bord d'import perdu** : chacun des 5 modules `vertex/ui/*`
   retirés est une bibliothèque de rendu pure (constante `JS`, fonctions) —
   aucun `@app.route`, aucun `Blueprint`, aucun enregistrement au chargement.
   `vertex/strategy/config.py` est un fichier de constantes.
2. **Aucun consommateur en production** : `grep` sur `journal.JS`, `vault.JS`,
   `signals.JS`, `options_lab.JS` → **0 hit** hors tests. Les tests importent
   ces modules **directement**, ils ne dépendent pas de l'import de
   `terminal.py`.
3. **Les 4 modules moteur/service** (`constants`, `status_service`,
   `decision_stack`, `indicators`) sont importés ailleurs dans `vertex/`
   (`routes/system.py`, `routes/decision_api.py`, `engines/backtest.py`,
   `engines/analysis.py`) → ils restent chargés par l'application.

**Non touchés, volontairement** : `from vertex.data.universe import *` et
`from vertex.data.constants import BENCH, R, BUILD, REFRESH_SEC  # noqa: F401`.
Le `noqa: F401` déclare un ré-export intentionnel ; y toucher serait un pari,
pas une correction.

## Preuves

- `git diff --stat` sur `terminal.py` : **12 deletions, 2 insertions**
  (7 164 → **7 153 lignes**, net -11). Les 2 insertions sont la reformulation
  du commentaire qui documente déjà les retraits de ce genre, pas du code.
  `compileall` exit 0.
- **MD5 des 8 pages servies IDENTIQUES aux références du lot 323** :
  `/` fc15688d1af6 · `/markets` c0bb91c6971a · `/opportunities` 6a22a6abbd03 ·
  `/analysis` 113827718e99 · `/portfolio` f1b41b665d4a · `/options` 6387210de785 ·
  `/journal` 243699ace2d5 · `/system` 85d1cb065d2e.
  → zéro octet servi modifié.
- Navigateur (`tools/probe_smoke.py`, `vertex_ready` atteint) : 8 × HTTP 200,
  **0 erreur console/pageerror**, `client-log count: 0`.
  (`/journal` à 3 684 caractères : toujours le `desk_data.json` local chargé de
  trades de sonde, cf. lot 323 — pas un effet du code.)
- Suite : **2500 passed / 2 skipped** (2499 + le gardien neuf).

## Le gardien

`tests/test_terminal_imports_lot324.py` — analyse AST de `terminal.py` et
échoue si un import n'est jamais référencé. Tolère exactement deux choses :
`import *` et les lignes marquées `# noqa: F401` (ré-export déclaré). Le
monolithe ne réaccumulera plus d'imports morts en silence.

## Décision SW

**Pas de bump** (`td-shell-v186`) : MD5 identiques sur les 8 pages, aucun octet
servi ne change.

## Invariants

READONLY intact, moteurs intacts (aucun fichier de `vertex/engines/` modifié —
seuls des imports du monolithe partent), `main` non touchée, aucun fichier
runtime commité.

## Suite

LOT 325 : veille active (référence de suite **2500 / 2**). É2/É3 de la purge
restent en attente de GO explicite. Prochaine échéance périodique : ~lot 330.
