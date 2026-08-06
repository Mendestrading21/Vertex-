# SKYLER V2 — LOT 115 : boucle continue — backtest recherche figé + mini-bilan 111-115

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-115`
(base : `integration/vertex-skyler-v2` @ `e9679aa`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/research/backtest.py` (§29 — simple_backtest, la brique AVANT
walk-forward) et `factory.apply_costs` n'avaient AUCUN test direct. La
promesse « un backtest n'est jamais une preuve » et le modèle de coûts
par rotation n'étaient figés nulle part.

## 2. Les 8 comportements figés (nés verts, dits)

```text
position constante → rotation 0, AUCUN coût, composition d'équité
  exacte (1.01 → 1.040604)                                             OK
bascules 1→0→1 → rotation 2.0, coût exact par pas — chaque
  aller-retour se PAIE, jamais un backtest sans coûts                  OK
position 0 → ne gagne rien, ne paie rien, équité plate                 OK
séries vides → None honnête (jamais 0 inventé), équité []              OK
l'avertissement constitutionnel « walk-forward requis » accompagne
  CHAQUE résultat, même vide                                           OK
longueurs dépareillées → tronquées au plus court (aucun rendement
  sans position appariée)                                              OK
apply_costs : formule exacte (spread+slippage)/100 × rotation —
  10 bp par pas au défaut · rotation 0 → gratuit                       OK
demi-position → exactement la moitié de l'exposition                   OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1960 passed, 2 skipped   (1952 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. MINI-BILAN tournée 111-115 (chiffres vérifiés dans les rapports)

```text
5 lots · 40 tests · suite 1928 → 1960 passed / 2 skipped
111 config_validation (8)  conséquence exacte par absence, secrets
                           jamais exposés, rien d'obligatoire
112 ai/health (8)          clé ≠ preuve — jamais CONNECTED sans appel
113 provenance models (8)  STALE utilisable, 0/False vraies valeurs
114 iv_units (8)           unité devinée = bug, legacy étiquetée
115 research/backtest (8)  un backtest n'est jamais une preuve
0 défaut moteur trouvé · 0 sonde corrigée (premier passage partout) ·
SW v127 stable · skyler_core 0.9.0 intact · PR #144 → #148.
Note d'exploitation : le serveur MCP des réveils a changé deux fois de
nom (Claude_Code_Remote ↔ UUID) — absorbé, repli encodé au canevas.
```

## 5. Suite

Lot 116 : angle suivant ; lot 120 = mini-bilan 116-120.
