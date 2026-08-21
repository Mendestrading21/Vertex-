# Branches supprimées — le registre de restauration

Supprimées le 2026-08-19, sur la branche d'intégration RC.

## Pourquoi la suppression est sans perte

Chacune est **entièrement fusionnée dans `origin/main`** : tous ses commits
sont des ancêtres de `main`. `git branch -r --merged origin/main` le dit, et
c'est la définition même de « rien à perdre » — le contenu ne disparaît pas,
seule la référence disparaît.

`CLEANUP_POLICY.md` protège explicitement `UNIQUE` et `UNKNOWN` ; il ne
protège pas les fusionnées. Les **614 branches uniques** mesurées au lot #782
ne sont pas touchées.

## Restauration

Une seule commande par branche, le SHA étant consigné ci-dessous :

```bash
git push origin <sha>:refs/heads/<nom-sans-le-prefixe-origin/>
```

Les commits vivant dans `main`, ils ne peuvent pas avoir été perdus par le
ramasse-miettes : la restauration reste possible sans limite de temps.

## Le registre

| branche | SHA | sujet du dernier commit |
| --- | --- | --- |
| `origin/agent/regime-aura-629` | `b550dc17e15865b158238d49739701dbb167f187` | lot 629 : une jauge complete pour un regime jamais mesure |
| `origin/claude/vertex-strategy-os-h17dso` | `c55659054f9a021c75f538891afacf48db1fbe69` | fix: corrections de revue adversariale (honnêteté cotation + confluenc |
| `origin/claude/vertex-system-launch-0bsizs` | `45ba412017dee95ef83e866a4da3d77bdd8618c9` | feat(secu+lancement): verrou facile (.env), exposition reseau sure, em |
| `origin/claude/vertex-visual-rebuild-1ofi8r` | `7151d3541be5b29bc463ef8dea17bb63ccd46d26` | docs(design): sauvegarde le design system (.interface-design/system.md |
| `origin/feature/active-source-timeouts` | `d5872ce46cd09fd0dd05a72ff6fea6434e514823` | feat: enforce active market data timeouts |
| `origin/feature/bounded-analytic-payloads` | `4010dec0b208a6bfaf7ba7a078ff38e21eb64dea` | feat: validate bounded analytic POST payloads |
| `origin/feature/freshness-drift-monitor` | `95ba03e00d9a4167801b531db146293fea0e5374` | feat: monitor freshness within data quality drift |
| `origin/feature/measurement-intelligence` | `77b0918f46f975892108bedfec02f08cd3f6fa81` | feat: measure option outcomes and intelligence drift |
| `origin/feature/multi-asset-evidence-guard` | `06af4b6194cdb4537eb7cff1d36ec0f5d2bd25b3` | feat: add multi-asset evidence guard |
| `origin/feature/multi-asset-market-coherence` | `959b2488ce934695633986ee0fef0bfd80e2616e` | feat: add multi-asset market coherence diagnostics |
| `origin/feature/operational-input-bounds` | `386165f81a02137b9b2ab28751243265436754bf` | feat: bound analytic inputs and options execution |
| `origin/feature/opportunity-reliability` | `6b3a1d794207ebd6416ff376823556ba332784e8` | feat: expose opportunity reliability diagnostics |
| `origin/feature/option-contract-measurement` | `97cc5abcd9e3b5b133e45784d758c69e38423955` | feat: measure observed option contract cohorts |
| `origin/feature/persistence-cache-hardening` | `052c77d7c5e11e768d933c0dd525de7c965948f2` | feat: harden persistence and cache observability |
| `origin/feature/portfolio-historical-stress` | `c860c3973dcf42039ba49060fc2e7ddb4d01fac1` | feat: ajouter un stress historique portefeuille |
| `origin/feature/regime-break-diagnostic` | `ffff452d017bfe14e3c00a8a8188fc7dcf82f05c` | fix: valider metriques top individuelles |
| `origin/feature/rescan-rate-limit` | `e7c049f84d45030b8e2738fca843a536dbb87adf` | feat: limiter les déclenchements de rescan |
| `origin/feature/safe-latency-observability` | `d0704b9b5c63df4ac0a1aa33d7e65974529bc482` | feat: add safe API latency observability |
| `origin/feature/scan-singleflight` | `306f9e57904183a9393a6c798ffbd3d64af88df8` | feat: prevent concurrent market scans |
| `origin/feature/scan-source-resilience` | `0d42f8722c37d5dd1485001b2606b4a6b1904b27` | feat: harden scan source resilience |
| `origin/feature/segmented-drift-monitor` | `edf5df97b4f29248a88c8f929459379fb8f5654f` | feat: monitor segmented performance and data drift |
| `origin/feature/swing-options-decision-packet` | `500d080f4970787105d68535ead2c2374cde59f2` | feat: add option quote evidence and decision readiness |
| `origin/feature/walk-forward-validation` | `a097d612b87546862bc526303f34561e63757847` | feat: valider la mémoire hors échantillon |
| `origin/feature/webhook-delivery-hardening` | `a0f8deb755e3b60969cdf4d99b6fe48d34af8a5c` | feat: harden tradingview webhook delivery |
| `origin/fix/complete-safe-api-errors` | `df92e92257c2eab28326a2c070ab5caa80926c3c` | fix: harden remaining API error responses |
| `origin/fix/dual-source-unavailable` | `9d52938eeffeb0033a03341de36a1bae655daca9` | fix: mark dual source failures unavailable |
| `origin/fix/request-limit-cache-freshness` | `3c941c9809fb7ee7b5e00f9cb3fec77ca6e080f6` | fix: verify request limits and cache freshness |
| `origin/fix/safe-api-errors` | `b91b81196918805591a451f4105049b9f3885106` | fix: prevent internal API error disclosure |
| `origin/integration/vertex-visual-merge` | `e4c5f160ac077e5b03d5ab4226e03acf0e2ffd88` | test(readonly): exclut .venv/site-packages du scan chemins d'ordre |
| `origin/test/scan-timeout-degradation` | `21a4163ce59744df6a7bee9fc864b7bd08fbe385` | test: prove scan timeout degradation |

**30 branches.**
