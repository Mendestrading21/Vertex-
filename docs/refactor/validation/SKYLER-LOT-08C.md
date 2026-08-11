# SKYLER V2 — LOT 08c — NEON GLASS · OPTIONS (scanner par univers)

> Date : 2026-08-05
> Branche : `agent/skyler-v2-lot-08c-options-scanners`
> Base : `agent/skyler-v2-lot-08b-today-diff`
> Périmètre : UNE vue (Options → LEAPS), une carte + un fichier JS — aucun moteur modifié

## 1. Constat

Les scanners par univers du lot 6 (`/api/options/scanner/<universe>` : fenêtres
strictes, mandat V2, probabilité de doublement) n'étaient visibles nulle part.

## 2. Décision

Carte « **Scanner par univers** » en tête de la vue LEAPS (son domicile : la vue
horizon long) : 3 onglets TACTICAL/SWING/LEAPS, filtre titre optionnel, tableau
Titre/Type/Strike/DTE/Delta/IV/OI/Spread/Qualité/**Mandat**/**P(doubler)** —
hors-mandat en badge rouge avec raisons au survol (jamais caché), P(doubler)
suffixée « EST. » + note modèle non calibré, badge DÉMO quand le serveur le dit.
Nouveau `options-scanner.js` autonome (actif seulement si `#vx-sc-out` présent),
`VX.fetch` TTL 120 s.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/ui/pages/options_intel_page.py` | carte dans la vue leaps + script (additif) | faible |
| `vertex/static/vertex/js/pages/options-scanner.js` | nouveau (node --check OK) | faible |
| `vertex/app/routes/system.py` | SW v89 → **v90** | faible |
| 4 gardiens SW + gardien de page (`test_options_intelligence_lot6.py`) | v90 + présence carte | nul |

## 4. Tests

```text
python -m compileall -q → exit 0 · node --check options-scanner.js → OK
suite : 1270 passed, 2 skipped
```

## 5. Validation navigateur (DEMO=1 NO_IBKR=1, Chromium réel)

- 1440×900 : « LEAPS · fenêtre 180-540 DTE · 33 contrat(s) · DÉMO », mandat
  étiqueté par ligne ; bascule TACTICAL → « fenêtre 20-60 DTE · 18 contrat(s) »
  (séparation stricte prouvée À L'ÉCRAN) ; capture `scanner_1440.png` ;
- 390×844 : même contenu, tableau en rangées empilées, 0 débordement ;
- **0 erreur console** (2 tailles) ; `/api/client-log` = 0 ; SW v90 servi.

## 6. Invariants vérifiés

- [x] jamais une échéance courte sur l'onglet LEAPS (prouvé à l'écran) ;
- [x] hors-mandat affiché, jamais filtré en silence ; P(doubler) étiquetée EST. + note ;
- [x] DÉMO affiché seulement si le serveur le confirme ; bump SW + gardiens ; READONLY.

## 7. Verdict

**GO** — suite 1270 verte, séparation des univers et honnêteté du mandat prouvées en navigateur.

## 8. Prochaine étape

Lot 9 : infrastructure de calibration (journal des décisions Skyler + Brier honnête-vide).

**Arrêt de lot — validation humaine groupée en fin de série (accord utilisateur).**
