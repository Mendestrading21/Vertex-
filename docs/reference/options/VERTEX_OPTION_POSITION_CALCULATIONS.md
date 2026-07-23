# Vertex — Calculs options (§11-12)

| Grandeur | Formule | Golden |
|---|---|---|
| Prime/action | capital / (qty × mult) | 3680/(2×100)=18,40 |
| Valeur de marché | mark × mult × qty | 22×100×2 = 4400 |
| P&L | market_value − capital | 4400−3680 = 720 |
| Valeur intrinsèque (CALL) | max(0, spot − strike) | 540−520 = 20 |
| Valeur temps | mark − intrinsèque | 30−20 = 10 |
| Breakeven (CALL) | strike + prime/action | 520+18,40 = 538,40 |
| Delta positionnel | Δ × mult × qty | 0,55×100×2 = 110 |
| Theta positionnel | θ × mult × qty | −0,08×100×2 = −16 |

**Multiplicateur appliqué UNE fois** (`test_multiplier_is_applied_once`).
**Greeks positionnels signés** : long CALL Δ>0, long PUT Δ<0, θ<0, Γ/vega>0.
Toute incohérence → `DELTA_SIGN_INCONSISTENT` etc.

## Source des Greeks (§12)
Priorité BROKER_GREEKS > MODEL_ESTIMATE > FALLBACK_ESTIMATE > UNAVAILABLE.
Divergence broker/modèle ≥ 0,12 → `BROKER_MODEL_GREEK_DIVERGENCE`. Une
estimation n'est jamais présentée comme une valeur broker.
