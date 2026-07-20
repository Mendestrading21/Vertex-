# 13 — Architecture cible

On **consolide** l'existant (strangler quasi abouti), on ne reconstruit pas. Cible = un monolithe Flask **propre
par couches**, une seule grammaire visuelle, une seule bibliothèque de graphes, une enveloppe de données unique,
des moteurs explicables, **lecture seule** de bout en bout.

## Couches cibles
1. **Acquisition & provenance** (`data_sources/`, `data/`) → produit des `ProvenancedValue`
   (`value·source·timestamp·quality·latency·environment·isEstimated·isDelayed·isStale·error`). IBKR read-only,
   fallbacks étiquetés, jamais de mock silencieux. (Résout DAT-01/02.)
2. **Moteurs de décision** (`engines/`, `quant/`, `options/`) : pipeline déterministe raw→signaux→scores→
   scénarios→**recommandations** ; plafonds testés (Kelly, p_win) ; explicabilité (evidence/reasoning) ; verdicts
   via `decision_stack` + vocabulaire `__VXVOCAB`. **Jamais → ordre.** (Résout ENG-01..05.)
3. **Préparation (ex-« Desk »)** (`planning/`, `portfolio/`, `app/routes/desk.py`, `planning_api.py`) : sizing,
   perte max, impact marge/risque, greeks, **ticket prêt-à-coller dans TWS**. Simulation only, aucune transmission.
4. **Routage** (`app/routes/`) : blueprints par domaine + API sous préfixe `/api/*` ; legacy `@app.route` de
   `terminal.py` migré progressivement. (Résout RT-01/02.)
5. **Rendu** (`ui/shell/` + `ui/pages/`) : **un** shell (`PRIMARY_NAV`, 8 espaces), pages par espace, onglets-URL.
   Nav legacy `nav.py` + sidebar inline orange de `terminal.py` supprimées. (Résout IA-01, CMP-03.)
6. **Design system** (`static/vertex/css` + `js/charts`) : tokens `--vx-*` seule source de style ; **une**
   `.vx-card` + modificateurs ; **un** MetricCard ; **une** bibliothèque `VXCharts` avec contrat. (Résout CMP-01/02, CHT-*.)
7. **Observabilité & QA** (`observability/`, `tests/`) : `METRICS`, gardiens (lecture seule, sync desk, SW pinning),
   `/api/client-log`=0, byte-identique sur les calculs déterministes.

## Invariants cible (non négociables)
- Lecture seule absolue. Données réelles ou honnêtement absentes/étiquetées. Un concept = un mot = une couleur.
- Tout changement de shell visible → bump `td-shell-vN` + tests d'épinglage.
- `scan_state` muté en place, jamais réassigné. Clés desk-sync dans les 4 listes.

## Principe directeur
« L'ordinateur de décision au-dessus d'IBKR » : chaque octet affiché sert une question de la boucle
OBSERVER→…→APPRENDRE, avec provenance et explication. Migration par lots vérifiés (`14-prioritized-roadmap.md`).
