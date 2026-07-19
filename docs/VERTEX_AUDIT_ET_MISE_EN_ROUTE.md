# VERTEX — Audit complet & mise en route (analyste privé, actions + options)

> Terminal d'**analyse** trading en **lecture seule** (`READONLY=True`, invariant absolu :
> aucun ordre n'est jamais passé). Flask, port 5002, interface FR, direction visuelle
> « Black Glass Institutional » (fond noir/graphite, argent/gris structurel, sémantique
> stricte vert/rouge/orange, violet = options, zéro bleu).

Ce document = (1) état réel du projet, (2) **checklist de mise en live sur ta machine**,
(3) comment vérifier que tout marche.

---

## 1) État réel — ce qui marche

### Le cerveau (déterministe, honnête, réel)
- **Verdicts** : `executive_engine.decide()` (constitution : ACHETER/RENFORCER/ATTENDRE/
  REDUIRE/REFUSER) + `decision_stack.evaluate()` (vue « comité ») + `evidence.gather()`
  (~10 analystes mono-domaine pondérés par régime, contradictions exposées) +
  `reasoning.build()` (3 scénarios conditionnels, invalidations, points de bascule).
  **Même entrée → même verdict** (déterministe).
- **Physique / quant RÉELS** (`vertex/market/regime_features.py`, `vertex/engines/quant_engine.py`,
  `vertex/quant/`) : Hurst (variance des différences), entropie de Shannon, efficience de
  Kaufman, demi-vie d'Ornstein-Uhlenbeck ; Monte-Carlo GBM 1200 chemins (proba TP/stop,
  P10/P90), block-bootstrap sur rendements réels, calibration ML (numpy, p_win ≤ 0.85).
- **Options** : greeks Black-Scholes + IV par bissection + PoP lognormale sur **chaînes
  réelles** ; en live, greeks **courtier IBKR** (`modelGreeks`, jamais estimés).

### Lecture seule (invariant produit)
- Toutes les connexions IBKR passent `readonly=True` (4 workers : options/scan, compte,
  cotations, indices). Aucune méthode d'ordre dans aucun chemin. Registre IA : 17 outils
  d'ordre **interdits** (rejetés à l'enregistrement).

### Données
- **Scan** (scores/tableaux) : bougies **journalières** yfinance → repli Stooq. En mode
  IBKR, l'intraday (spot, chaînes, indices) est **superposé** — les scores restent EOD
  (honnêtement étiqueté dans Système → Sync Center).
- **Démo** (`DEMO=1`, auto sur cloud) : univers + chaîne d'options **synthétiques**,
  clairement étiquetés « DÉMO » — jamais présentés comme réels.

---

## 2) Nouveautés de cette session (options, physique, honnêteté)

- **Grille de chaîne d'options** (`/options/<sym>`) : vraie grille strikes × échéances
  PUTS ← Strike → CALLS (Bid/Ask/IV/Δ/Θ/V/OI, ombrage ITM argent, repère spot, sélecteur
  d'échéance). Route `GET /api/options/chain-grid/<sym>` ; greeks **courtier IBKR** en live.
- **Surface de volatilité + skew par échéance** (`/options/<sym>`) : heatmap IV strike ×
  échéance (module `vol-surface.js` réveillé) + courbe de skew. Route
  `GET /api/options/surface/<sym>`.
- **Physique & probabilités** (`/analysis/<sym>`) : dispersion Monte-Carlo/bootstrap
  (P05/P50/P95 + course TP1-avant-stop), radar structure statistique (Hurst/efficience/
  ordre) + demi-vie, jauge de Kelly (demi-Kelly capé, jamais automatique), flux
  d'alignement multi-horizons (MTF). Tout depuis `/api/ticker/<sym>` — aucune invention.
- **Analyste IA branché** (`/intelligence?view=analyst`) : « Interroger l'analyste »
  appelle désormais `GET /api/ai/analyst/<sym>` — Claude **interprète** le dossier RÉEL
  des moteurs (verdict exécutif + physique + Monte-Carlo + bootstrap + Kelly + MTF +
  anomalies) et répond à la question posée. **Claude ne décide jamais** : le verdict reste
  au moteur exécutif. Sans `ANTHROPIC_API_KEY` → synthèse déterministe des moteurs (source
  affichée franchement « IA indisponible — synthèse moteurs »), jamais de texte inventé.
  Modèle résolu une seule fois (`VERTEX_AI_MODEL` > `ANTHROPIC_MODEL` > `claude-opus-4-8`)
  — cohérent entre `/api/ai/status` et l'appel réel.
- **Honnêteté (règle 4)** : le badge « IBKR temps réel » s'allume **uniquement** sur le
  socket réel (`/healthz` → `ibkr_live`), plus sur un flag de config.
- **IBKR configurable** : `IBKR_HOST/PORT/CLIENT_ID` sont **enfin respectés** par les 4
  workers (sonde REAL-first cohérente, timeout de connexion porté à 6 s).
- **Refonte visuelle** « argent lumineux » sur toute l'app (cartes, tableaux, KPI, titres,
  graphes : jauge à bille blanche, donut glossy, courbes lumineuses, plein écran premium,
  châssis sidebar/topbar, en-têtes dégradés).

---

## 3) Checklist de mise en LIVE sur ta machine (lecture seule)

### A. TWS / IB Gateway
1. Lance **TWS** (ou IB Gateway), connecté à ton compte **réel**.
2. Global Configuration → API → Settings :
   - ✅ **Enable ActiveX and Socket Clients**
   - ✅ **Read-Only API** (coché — double sécurité)
   - **Trusted IPs** : ajoute `127.0.0.1`
   - **Socket port** : `7496` (TWS réel) · `7497` (TWS papier) · `4001`/`4002` (Gateway)
   - Autorise **≥ 4 clients API simultanés** (l'app ouvre 4 workers).
3. Au 1er lancement, clique **Accept** sur la popup « Accept incoming connection ».
4. Abonnements données actifs : actions US temps réel, **OPRA** (greeks options),
   **indices CBOE** (SPX/VIX), fondamentaux Reuters (tick 258) — sinon dégradation
   honnête en différé.

### B. Fichier `.env` (copie `.env.example` → `.env`)
```
# Accès (recommandé — sinon écoute 127.0.0.1 seulement)
VERTEX_CODE=un-code-a-toi
VERTEX_SECRET=une-longue-chaine-aleatoire

# IA (optionnel — active l'analyste Claude & l'enrichissement web ; sans clé,
#     synthèse déterministe des moteurs, aucun chiffre inventé)
ANTHROPIC_API_KEY=sk-ant-...
VERTEX_AI_MODEL=claude-opus-4-8          # profondeur max (ou claude-sonnet-5)

# IBKR LIVE : laisse NO_IBKR et DEMO VIDES/non définis (= live si TWS ouvert)
# NO_IBKR=1        ← à NE PAS mettre en live
# DEMO=1           ← à NE PAS mettre en live
IBKR_HOST=127.0.0.1
IBKR_PORT=7496                            # 7496 réel · 7497 papier · 4001/4002 Gateway
# IBKR_CLIENT_ID=41                       # optionnel (base ; 4 ids dérivés)
```

### C. Lancer
- macOS : `./Lancer_VERTEX.command` — Windows : `Lancer_VERTEX.bat` — sinon `python terminal.py`.
- Ouvre `http://localhost:5002` (entre `VERTEX_CODE` si défini).

---

## 4) Vérifier que tout est LIVE (et honnête)
| Contrôle | Attendu en live |
|---|---|
| `GET /healthz` | `ibkr_enabled:true`, **`ibkr_live:true`** quand TWS coté temps réel |
| `GET /api/system/connections` | IBKR = **LIVE** (ou DELAYED) — vue honnête, jamais LIVE sans preuve |
| `GET /api/live/status` | mode `live` / `delayed` par domaine |
| `GET /api/ai/status` | `CONNECTED` + modèle si clé valide, sinon `MISSING` (jamais estimé) |
| `GET /api/ai/analyst/<sym>` | `source:claude` + modèle si clé, sinon `deterministic-fallback` |
| `GET /api/client-log` | **0 erreur** (doit le rester) |
| Badge d'en-tête | 🟢 « IBKR temps réel » **seulement** si le socket est réellement live |
| `/options/<sym>` | grille de chaîne + surface IV + skew peuplés (greeks courtier) |
| `/analysis/<sym>` | dispersion Monte-Carlo, radar physique, Kelly, MTF |

Si TWS est fermé : tout reste en **différé/EOD honnête** (marques desk/EOD, greeks
`MODEL_ESTIMATE`), jamais présenté comme du temps réel.

---

## 5) Points connus / limites (transparence)
- Les **scores** dérivent du journalier (yfinance/Stooq) même en mode IBKR — l'intraday
  ne fait que superposer spot/chaînes/indices. C'est honnêtement étiqueté.
- **Claude ne décide jamais** : il interprète/explique ; le verdict vient des moteurs
  déterministes (invariant).
- Vérification **live** impossible depuis le cloud (pas de TWS, données bloquées) : tout a
  été validé en **DÉMO** (0 erreur console, 909 tests) + ce runbook ; la validation temps
  réel se fait sur ta machine avec TWS + clé API.

---

## 6) Développement (rappels)
- Tests : `python -m pytest tests/ -q` → **100 %** avant tout commit.
- Après changement de shell visible : bump `td-shell-vN` (`vertex/app/routes/system.py`).
- Palette : uniquement `C.colors` (zéro bleu ; violet = options). Données absentes → `—`/`n/d`.
- Branche de travail de la refonte : `glass-plus-charts`.
