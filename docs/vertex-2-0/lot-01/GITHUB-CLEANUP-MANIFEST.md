# GITHUB_CLEANUP_MANIFEST — lot 1

Inventaire **en lecture seule** du dépôt distant, mesuré le 28 août 2026
(`git ls-remote`, puis fetch sans blobs et `git branch -r --merged/--no-merged
origin/main`). **Aucune suppression n'est exécutée par ce lot.** La section
finale liste ce qui est *proposé* à la suppression, avec SHA et preuve — elle
attend une autorisation explicite.

## Vue d'ensemble

| Élément | Nombre |
|---|---:|
| Branches distantes | 748 |
| … fusionnées dans `main` (contenu déjà préservé) | 30 |
| … NON fusionnées (portent des commits absents de `main`) | 717 |
| Tags | 1 (`vertex-premium-2026-07-07`) |
| PR ouvertes | 2 — #838 (programme maître), #839 (travail graphique) |
| Worktrees locaux | 0 |

## Protections absolues — jamais touchées

`main` · `agent/vertex-design-2-0-master-20260827` (#838) ·
`claude/vertex-2-0-visual-redesign-vy3h7s` (#839) ·
`checkpoint/vertex-2-0-graphique-20260828` ·
`agent/vertex-2-0-integration-20260828` (branche courante).

## Famille par famille

### 1. `agent/skyler-v2-*` — 636 branches, la masse historique

- **Dernier commit : août 2026 (échantillon vérifié : 4–5 août).** `CLAUDE.md`
  les déclare « historiques, ne servent jamais de base ».
- **Fusionnées dans `main` : 0.** Les autres portent des commits absents de
  `main` — chaque lot Skyler travaillait sur sa branche, et la convergence
  s'est faite par PR d'intégration, pas par fusion directe de chaque branche.
- **Préservation :** le *résultat* du programme Skyler vit dans `main` ; les
  branches individuelles conservent le *déroulé* (commits intermédiaires).
- **Proposition :** conserver un **tag d'archive unique** (`archive/skyler-v2-20260804`
  posé sur les têtes via un commit octopus, ou simplement laisser les branches),
  puis **supprimer les 636 branches** après votre accord. Risque : perte du
  déroulé fin, jamais du résultat. Rollback : impossible après suppression sans
  archive — c'est pourquoi l'archive précède.
- **Décision : À AUTORISER explicitement — rien n'est fait sans votre accord.**

### 2. `agent/vertex-1-0-*` — 51 branches

**26 fusionnées dans `main`** — contenu intégralement préservé, suppression sûre :

- `agent/vertex-1-0-bls-officiel` @ `6639c1d1e` — fusionnée
- `agent/vertex-1-0-calendrier-macro` @ `774ad5c77` — fusionnée
- `agent/vertex-1-0-chiffres-du-packet` @ `e739af4b5` — fusionnée
- `agent/vertex-1-0-constitution-active` @ `18fb218b2` — fusionnée
- `agent/vertex-1-0-contexte-en-tete` @ `1db603640` — fusionnée
- `agent/vertex-1-0-demarrage-auto` @ `6736c913d` — fusionnée
- `agent/vertex-1-0-ecritures-protegees` @ `a22161807` — fusionnée
- `agent/vertex-1-0-entrees-mesurees` @ `e0b15fc00` — fusionnée
- `agent/vertex-1-0-exposition-reseau` @ `14ebfc33d` — fusionnée
- `agent/vertex-1-0-fred-vintages` @ `7c3f6b66e` — fusionnée
- `agent/vertex-1-0-g5-open-interest` @ `0747a838f` — fusionnée
- `agent/vertex-1-0-historique-revisions` @ `fd6e0f50e` — fusionnée
- `agent/vertex-1-0-instantane-borne` @ `8ea7cfe82` — fusionnée
- `agent/vertex-1-0-iv-cotee` @ `e33625025` — fusionnée
- `agent/vertex-1-0-journal-sans-secret` @ `f49fac89d` — fusionnée
- `agent/vertex-1-0-modele-declare` @ `0bc5fd9da` — fusionnée
- `agent/vertex-1-0-moteur-de-live` @ `b5ef0f70a` — fusionnée
- `agent/vertex-1-0-moteurs-mesures` @ `263eb324f` — fusionnée
- `agent/vertex-1-0-point-in-time-garde` @ `3870edc5c` — fusionnée
- `agent/vertex-1-0-publieur-unique` @ `5a52c253c` — fusionnée
- `agent/vertex-1-0-rejets-nommes` @ `f953b3cd4` — fusionnée
- `agent/vertex-1-0-rendement-dividende` @ `040396d0e` — fusionnée
- `agent/vertex-1-0-sources-consolidees` @ `37033247c` — fusionnée
- `agent/vertex-1-0-symboles-morts` @ `b1a42955e` — fusionnée
- `agent/vertex-1-0-xml-durci` @ `4baf26207` — fusionnée
- `agent/vertex-1-0-xss-news` @ `2deb8561e` — fusionnée

**25 non fusionnées** — commits uniques, à examiner une par une avant toute décision :

- `agent/vertex-1-0-aveu-navigateur` @ `7b99b92fb`
- `agent/vertex-1-0-date-indicative` @ `daba999ea`
- `agent/vertex-1-0-design` @ `67be086f6`
- `agent/vertex-1-0-dom-sur-complet` @ `4f55faeb2`
- `agent/vertex-1-0-domaines` @ `75e27b1a6`
- `agent/vertex-1-0-foundation` @ `5bd316a10`
- `agent/vertex-1-0-g5-cloture` @ `a427ec072`
- `agent/vertex-1-0-gain-mesurable` @ `73de92f50`
- `agent/vertex-1-0-governance` @ `c23f01c0d`
- `agent/vertex-1-0-graphe-chaud` @ `67c609078`
- `agent/vertex-1-0-marque-option` @ `5ef554a54`
- `agent/vertex-1-0-marque-visible` @ `ad86e7dc7`
- `agent/vertex-1-0-memoire` @ `e894c38f1`
- `agent/vertex-1-0-mesure-lenteur` @ `c1d7848ee`
- `agent/vertex-1-0-moteurs` @ `077a0b006`
- `agent/vertex-1-0-persistance` @ `c310b2b63`
- `agent/vertex-1-0-pnl-visible` @ `6b74b8b09`
- `agent/vertex-1-0-point-in-time` @ `4397d58bb`
- `agent/vertex-1-0-portabilite-windows` @ `d77b06d48`
- `agent/vertex-1-0-qa` @ `c8764476e`
- `agent/vertex-1-0-reconciliation-pnl` @ `7d8526947`
- `agent/vertex-1-0-runtime` @ `b996b19ae`
- `agent/vertex-1-0-sec-edgar` @ `be6dbc8b1`
- `agent/vertex-1-0-surfaces-lentes` @ `6beeee3fe`
- `agent/vertex-1-0-wmb` @ `49d6b9568`

### 3. Prototypes design abandonnés — candidats à l'archivage

Ces branches portent les directions visuelles **abandonnées** (V4, néon,
total-rebuild, Signal OS). Aucune n'est fusionnée ; leur valeur est de preuve
historique et de source visuelle, pas de code à reprendre :

- `agent/lanceur-ipad` @ `64bedde63` — non fusionnée
- `agent/regime-aura-629` @ `b550dc17e` — non fusionnée
- `agent/vertex-intelligence-2-0-blueprint` @ `c5efe3b2e` — fusionnée
- `agent/vertex-neon-glass-graphs` @ `a802155b0` — non fusionnée
- `agent/vertex-signal-os-v1` @ `1e27415f1` — non fusionnée
- `agent/vertex-total-rebuild` @ `28d1e4e39` — non fusionnée
- `agent/vertex-total-rebuild-obsidian-v2` @ `5426c2e45` — non fusionnée

### 4. `feature/* fix/* test/* integration*` — 35 branches

Travaux ponctuels antérieurs au programme. `integ-complete` et
`integration-vertex-live` sont **fusionnées** (préservées). Les autres portent
des commits uniques et datent d'avant la consolidation :

- `feature/active-source-timeouts` @ `d5872ce46` — non fusionnée
- `feature/bounded-analytic-payloads` @ `4010dec0b` — non fusionnée
- `feature/freshness-drift-monitor` @ `95ba03e00` — non fusionnée
- `feature/measurement-intelligence` @ `77b0918f4` — non fusionnée
- `feature/multi-asset-evidence-guard` @ `06af4b619` — non fusionnée
- `feature/multi-asset-market-coherence` @ `959b2488c` — non fusionnée
- `feature/operational-input-bounds` @ `386165f81` — non fusionnée
- `feature/opportunity-reliability` @ `6b3a1d794` — non fusionnée
- `feature/option-contract-measurement` @ `97cc5abcd` — non fusionnée
- `feature/persistence-cache-hardening` @ `052c77d7c` — non fusionnée
- `feature/portfolio-historical-stress` @ `c860c3973` — non fusionnée
- `feature/regime-break-diagnostic` @ `ffff452d0` — fusionnée
- `feature/rescan-rate-limit` @ `e7c049f84` — non fusionnée
- `feature/safe-latency-observability` @ `d0704b9b5` — non fusionnée
- `feature/scan-singleflight` @ `306f9e579` — non fusionnée
- `feature/scan-source-resilience` @ `0d42f8722` — non fusionnée
- `feature/segmented-drift-monitor` @ `edf5df97b` — non fusionnée
- `feature/swing-options-decision-packet` @ `500d080f4` — non fusionnée
- `feature/vertex-hyper-visual-intelligence` @ `99d68525c` — non fusionnée
- `feature/walk-forward-validation` @ `a097d612b` — non fusionnée
- `feature/webhook-delivery-hardening` @ `a0f8deb75` — non fusionnée
- `fix/complete-safe-api-errors` @ `df92e9225` — non fusionnée
- `fix/dual-source-unavailable` @ `9d52938ee` — non fusionnée
- `fix/request-limit-cache-freshness` @ `3c941c980` — non fusionnée
- `fix/safe-api-errors` @ `b91b81196` — non fusionnée
- `glass-plus-charts` @ `9086f0dee` — non fusionnée
- `glass-plus-charts-oz8jmh` @ `0ee0f3599` — non fusionnée
- `integ-complete` @ `d379d9102` — fusionnée
- `integration-vertex-live` @ `34c686c39` — fusionnée
- `integration/vertex-1-0-rc` @ `d77b06d48` — non fusionnée
- `integration/vertex-skyler-v2` @ `1589e4e6b` — non fusionnée
- `integration/vertex-v4-clean` @ `0354ab7d8` — non fusionnée
- `integration/vertex-visual-merge` @ `e4c5f160a` — non fusionnée
- `redesign/vertex-v4-master` @ `3a847f723` — non fusionnée
- `test/scan-timeout-degradation` @ `21a4163ce` — non fusionnée

### 5. `claude/*` — 15 branches de sessions

Branches créées par des sessions Claude. `claude/vertex-2-0-visual-redesign-vy3h7s`
est **protégée** (PR #839). Les autres :

- `claude/v4-01-foundations` @ `57d23a094` — non fusionnée
- `claude/v4-02-shell` @ `978730d24` — non fusionnée
- `claude/v4-03-components` @ `b0746718a` — non fusionnée
- `claude/v4-04-charts` @ `af301f5e7` — non fusionnée
- `claude/v4-06-markets` @ `b9c4e6677` — non fusionnée
- `claude/v4-10-options` @ `ece5ffdcd` — non fusionnée
- `claude/v4-qa-conformance` @ `dab5abd08` — non fusionnée
- `claude/vertex-2-0-visual-redesign-vy3h7s` @ `cfec71450` — **PROTÉGÉE (PR #839)**
- `claude/vertex-connection-setup-4j3h4j` @ `e78b84394` — non fusionnée
- `claude/vertex-glass-redesign-system` @ `5b25e723d` — non fusionnée
- `claude/vertex-improvements-kybc4p` @ `d9c68ad91` — non fusionnée
- `claude/vertex-latest-screenshots-0tuja0` @ `50d9a9bf5` — non fusionnée
- `claude/vertex-strategy-os-h17dso` @ `c55659054` — non fusionnée
- `claude/vertex-system-launch-0bsizs` @ `45ba41201` — non fusionnée
- `claude/vertex-visual-rebuild-1ofi8r` @ `7151d3541` — non fusionnée

## Suppressions distantes PROPOSÉES — en attente d'autorisation

**Tranche A — sûres (contenu prouvé dans `main`)** : les 30 branches marquées
« fusionnée » ci-dessus. Preuve : `git branch -r --merged origin/main`.

**Tranche B — masse Skyler (636 branches)** : après pose d'une archive.

**Tranche C — tout le reste** : décision différée ; chaque branche non
fusionnée exige un examen individuel avant proposition.

Aucune de ces tranches n'est exécutée. Répondre par exemple :
« autorise la tranche A » — et seule celle-ci sera exécutée, avec un rapport
listant chaque référence supprimée et son SHA final.

