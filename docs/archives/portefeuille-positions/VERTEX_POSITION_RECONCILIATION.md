# Vertex — Réconciliation (§7)

Identité action : (classe, symbole, devise). Identité option : (sous-jacent,
droit, strike, expiration, multiplicateur, devise).

Codes : POSITION_DUPLICATE · QUANTITY_MISMATCH · COST_BASIS_MISMATCH ·
CURRENCY_MISMATCH · MULTIPLIER_MISMATCH · EXPIRED_OPTION_OPEN ·
MISSING_POSITION · UNKNOWN_POSITION · CLOSED_STATE_CONFLICT.

Aucune correction silencieuse : chaque écart produit `DATA_REPAIR_REQUIRED`
avec valeur locale, valeur broker, source préférée et champ `confirmed:false`
(confirmation humaine requise). **IBKR hors ligne** ⇒ aucune position locale
marquée disparue, aucune clôture (`test_ibkr_offline_does_not_close_positions`).
