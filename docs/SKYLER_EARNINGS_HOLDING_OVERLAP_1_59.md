# Vertex — résultats et plan de détention Skyler

Le contexte `earnings_holding_overlap` rend simultanément visibles le plan de détention du mandat, exprimé en séances, et le DTE de résultats, exprimé en jours calendaires lorsqu’il est déclaré.

Vertex publie le statut `UNITS_NOT_COMPARABLE` plutôt que de convertir implicitement les séances en jours calendaires. Sans plan de détention déclaré, le statut est `HOLDING_PLAN_UNAVAILABLE`; sans DTE de résultats déclaré, il est `EARNINGS_DTE_UNAVAILABLE`. Le contexte ne produit ni signal, ni recommandation, ni modification de score, gate ou verdict.
