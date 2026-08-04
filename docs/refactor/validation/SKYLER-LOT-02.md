# SKYLER V2 — LOT 02 — CONSTITUTION STRATÉGIQUE V2

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-02-constitution-v2`
> Base : `agent/skyler-v2-lot-01-options-correctness`
> Périmètre : nouveau profil versionné uniquement (aucun moteur de calcul modifié)

## 1. Constat

Le profil actif était la V1 (`vertex_strategy_v1.json`) : 8–10 lignes, DTE 60–270,
catégories BALANCED/DYNAMIC/ULTRA_CONVEX/BEARISH_TACTICAL — sans niveaux S+/S/A/B,
sans mandat LEAPS (180–540 DTE, delta 0,70–0,90), sans règles gagnants/perdants
codifiées, sans hard gates listés. Le mécanisme de versioning existait déjà
(`propose_new_version` : rien n'est écrit sans `confirm=True`, la V1 reste sur disque).

## 2. Décision

Créer la **V2 exclusivement via le mécanisme officiel** (`propose_new_version(changes,
confirm=True)` — validation `_validate_raw` avant tout écrit, vente toujours interdite),
la V1 restant intacte octet pour octet. Contenu ajouté :

- `conviction_levels` : S+ 36–40 (10–15 %), S 32–35 (7–10 %), A 28–31 (3–5 %),
  B 24–27 (1–2 %), refus < 24 — **plafonds analytiques, jamais un ordre** (flags
  `allocations_are_analytical_caps` / `never_triggers_orders` codés en dur) ;
- `skyler_score` : 8 blocs = 40 points exactement (fondamentaux 5, catalyseurs 5,
  technique 6, institutions/flux/anomalies 4, régime/secteur 4, asymétrie/scénarios 6,
  qualité option 6, qualité données 4) — « le score ne contourne jamais les hard gates » ;
- `position_rules` : `never_add_to_losers`, renforcement seulement sur confirmation
  (cassure/retest/résultats/révisions/tendance), gagnants jamais vendus automatiquement
  à +100 %, sécurisation partielle 25–50 % + runner, `reward_risk_min: 2.0` ;
- `hard_gates` : 13 portes (R:R<2, invalidation absente, qualité données, conflit de
  sources, spread, OI, DTE hors mandat, thèse cassée, renforcement perdant,
  concentration, quota options, risque illimité non signalé, proba de doublement) ;
- `options_profile.universes` : TACTICAL 20–60 / SWING 60–180 / LEAPS 180–540
  (strictement séparés) ; `dte.absolute_maximum` 270 → **540** (admission LEAPS,
  fenêtre préférée globale inchangée 90–210) ;
- catégorie **LEAPS** : delta 0,70–0,90, DTE préféré 180–540, détention propre
  30–540 j, OI ≥ 500, spread ≤ 5 %, catalyseur + invalidation + IV-crush +
  coût total/perte max + scénarios spot×temps×IV + proba de doublement étiquetée ;
- portefeuille : 8–**15** lignes (V1 : 8–10).

Interdits préservés (validés par `_validate_raw` à l'écriture) : `short_options`,
`covered_calls`, `protective_puts`, `credit_spreads`, `naked_options`,
`automatic_execution` tous à `false` ; `primary_direction: LONG_CALL` ;
décisions finales canoniques ; drawdowns négatifs ; `target_is_guarantee: false`.

## 3. Fichiers modifiés

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/strategy/profiles/vertex_strategy_v2.json` | nouveau (généré par le mécanisme, jamais à la main) | faible |
| `tests/test_constitution_v2.py` | nouveau — 14 tests (12 rouges avant création) | faible |
| `tests/test_constitution.py` | 2 gardiens rendus version-conscients (documenté) | faible |
| `tests/test_options_engine.py` | bornes DTE lues dans le profil actif (30 tjs rejeté ; 400 admissible en V2) | faible |
| `tests/test_portfolio_executive.py` | slots libres = max du profil − positions | faible |

Les 3 gardiens mis à jour épinglaient des valeurs V1 sur le profil COURANT ; la V2
les change délibérément (mandat validé) — ce ne sont pas des résultats faux acceptés,
mais le nouveau contrat. Chaque test vérifie AUSSI que la V1 reste intacte.

## 4. Tests rouges avant création

```text
python -m pytest tests/test_constitution_v2.py -q → 12 failed, 2 passed
```

## 5. Tests après

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_constitution_v2.py tests/test_constitution.py -q → 24 passed
python -m pytest tests/ -q → 1189 passed, 2 skipped
```

Preuves versioning/diff/rollback : `test_v1_untouched_byte_identical_values`
(V1 rechargeable, valeurs historiques exactes, pas de `conviction_levels` glissé),
`test_diff_v1_v2_is_explicit` (diff lisible), tests historiques de proposition
sans confirmation (rien d'écrit) toujours verts. Rollback = `load_profile(version=1)`
ou suppression du fichier V2 (la V1 redevient la dernière).

## 6. Validation runtime

Serveur `DEMO=1 NO_IBKR=1` relancé : `/api/strategy/profile` sert la V2
(catégorie LEAPS delta 0,70, `absolute_maximum: 540`) ; `/api/client-log` = 0.
Effet de bord assumé et documenté : `contract_filter`/`call_selector` admettent
désormais les échéances jusqu'à 540 DTE (mandat LEAPS voulu) ; le labo multileg
lit `profile_version: 2` et ses bornes DTE via `_options_mandate()`.

## 7. Invariants vérifiés

- [x] V1 jamais modifiée (test byte-level) ; V2 générée par le mécanisme, validée avant écrit ;
- [x] vente/exécution toujours interdites en V2 (gardien + `_validate_raw`) ;
- [x] allocations = plafonds analytiques, jamais un ordre (flags codés) ;
- [x] READONLY intact ; aucun secret ; aucun moteur de calcul modifié.

## 8. Risques restants

1. Les niveaux S+/S/A/B et hard_gates sont désormais CODIFIÉS mais pas encore
   CONSOMMÉS par un moteur — c'est le périmètre du **lot 5** (Skyler Core).
2. La catégorie LEAPS n'est pas encore servie par un scanner dédié — **lot 6**.
3. `holding_period_days` global (2–28 j) reste celui du swing V1 ; les LEAPS portent
   leur propre fenêtre dans leur catégorie (documenté).

## 9. Verdict

**GO** — V2 créée par le mécanisme officiel, 12 tests rouges → verts, V1 prouvée
intacte, suite 1189 verte, profil V2 servi en runtime.

## 10. Prochaine étape autorisée

`/vertex-skyler-v2 lot-3` (Market Intelligence — MarketContext canonique).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**
