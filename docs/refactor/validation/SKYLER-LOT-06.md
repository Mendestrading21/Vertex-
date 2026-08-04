# SKYLER V2 — LOT 06 — OPTIONS INTELLIGENCE

> Date : 2026-08-04
> Branche : `agent/skyler-v2-lot-06-options-intelligence`
> Base : `agent/skyler-v2-lot-05-skyler-core`
> Périmètre : scanners par univers + probabilité de doublement + OptionsContext Skyler — moteurs GEX/Greeks/EM existants inchangés

## 1. Constat

Déjà couvert par les lots pré-Skyler (inchangés ici) : GEX/walls/zero-gamma/Vanna/
Charm/max-pain/skew (`vertex/options/gex.py` + vue Positionnement), expected move,
spot×temps×IV (`scenario_pricer`), earnings/IV-crush (`event_risk`), vol surface.
Manquaient : la SÉPARATION STRICTE des horizons (le labo sélectionne ~35 DTE),
la probabilité de DOUBLEMENT (≠ PoP), et un OptionsContext branché dans le score
Skyler (bloc `options_quality` toujours 0).

## 2. Décision

- **`vertex/options/horizon_scanners.py`** : `scan(board, universe, sym)` —
  fenêtres lues dans la Constitution V2 (`universes`), TACTICAL [20,60) /
  SWING [60,180) / LEAPS [180,540] (borne 180 → LEAPS, documenté) ; **jamais une
  échéance courte pour une requête LEAPS** (testé) ; calls et puts LONGS analysés ;
  IV normalisée à la frontière étiquetée (`iv_units`) ; **mandat LEAPS évalué par
  candidat et AFFICHÉ** (`mandate.delta_ok/oi_ok/spread_ok` + bornes,
  `hors_mandat`) — jamais filtré en silence ; conformes classés d'abord.
  `options_context(scan)` → contexte minimal pour le SkylerPacket.
- **`vertex/options/double_prob.py`** : P(valeur ≥ 2×coût) — modèle
  `lognormal_terminal_intrinsic` DOCUMENTÉ (call : S_T ≥ K+2p ; put : S_T ≤ K−2p,
  seuil ≤ 0 → 0.0 jamais inventé) ; hypothèses affichées (tenue à l'échéance, pas
  de trajectoire d'IV, spread exclu, mesure risque-neutre) ; statut **ESTIMATED**,
  confiance **RÉDUITE**, `calibrated: false` (lot 9) ; refus structurés (IV %
  non convertie refusée) ; **prouvé ≠ PoP** (P(double) < P(profit), testé).
- **Skyler branché** : `build_packet(..., options_ctx=)` ; bloc `options_quality`
  noté depuis la qualité réelle du meilleur candidat, **plafonné à 3/6 si le
  meilleur candidat est hors mandat** ; `/api/skyler/<sym>` fournit le contexte
  LEAPS du board réel.
- Route additive `GET /api/options/scanner/<universe>?sym=` (doublement calculé
  sur les 5 meilleurs).

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/options/horizon_scanners.py` | nouveau (pur) | faible |
| `vertex/options/double_prob.py` | nouveau (pur) | faible |
| `vertex/engines/skyler_core.py` | param `options_ctx` + bloc options réel (additif) | faible |
| `vertex/app/routes/options_intel_api.py` | +1 route additive | faible |
| `vertex/app/routes/analysis_api.py` | /api/skyler nourrit le contexte LEAPS | faible |
| `tests/test_options_intelligence_lot6.py` | nouveau — 16 tests | faible |

## 4. Tests

```text
rouge : collection error (modules inexistants)
vert  : 16 passed (lot 6) · 34 passed (lot 5+6 après câblage)
suite : 1248 passed, 2 skipped · compileall exit 0
```

Cas à la main : doublement call S=100 K=100 p=5 1 an IV 30 % → seuil 110,
d=ln(100/110)/0.3=−0.318 → **P=0.375 exact** ; put → seuil 90, P≈0.363 ;
P(double) < PoP prouvé ; fenêtres strictes ; mandat 0.30∉[0.70,0.90] / OI 100<500 /
spread 9 %>5 % tous flagués ; contexte absent → bloc INSUFFICIENT (non-régression).

## 5. Validation runtime (DEMO=1 NO_IBKR=1)

- `/api/options/scanner/LEAPS?sym=GOOGL` → fenêtre [180,540], candidat PUT 180 DTE
  **hors_mandat étiqueté** (delta −0.50 hors [0.70,0.90], spread 5.8 %>5 %),
  `double_prob 0.025 ESTIMATED` seuil 98.86, modèle documenté ;
- `/api/options/scanner/TACTICAL?sym=GOOGL` → uniquement 45 DTE ;
- `/api/skyler/GOOGL` → bloc `options_quality` **3/6 PARTIAL** (« qualité 66/100
  → 4/6 — plafonné : meilleur candidat HORS MANDAT »), total 15→**18**/40 ;
- `/api/client-log` = 0.

## 6. Invariants vérifiés

- [x] jamais ~35 DTE pour une requête LEAPS ; univers strictement séparés ;
- [x] doublement ≠ PoP, modèle/mesure/hypothèses affichés, ESTIMATED non calibré ;
- [x] hors-mandat étiqueté, jamais filtré en silence, plafonne le score ;
- [x] IV typée à la frontière ; refus structurés ; moteurs existants intacts ;
- [x] READONLY ; aucun secret.

## 7. Risques restants

1. Le mandat delta LEAPS s'évalue sur le delta du board (|δ|) — chaîne complète
   IBKR (TWS ouvert) l'affinera par expiration réelle.
2. Doublement : horizon de sortie < échéance et scénarios d'IV non modélisés
   (hypothèses affichées) — calibration lot 9.
3. Vomma absent du board (vanna/charm servis par le moteur GEX) — à exposer avec
   la chaîne complète.

## 8. Verdict

**GO** — 16 tests, cas exacts à la main, univers stricts prouvés en runtime,
score Skyler enrichi honnêtement, suite 1248 verte.

## 9. Prochaine étape autorisée

`/vertex-skyler-v2 lot-7` (Portfolio Intelligence — PortfolioContext, sizing
S+/S/A/B, garde-fous renforcement).

**Arrêt après ce lot — validation humaine différée en fin de session (accord utilisateur du 2026-08-04).**
