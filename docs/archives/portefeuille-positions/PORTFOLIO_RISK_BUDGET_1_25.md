# Vertex — budget de risque portefeuille

Le contexte portefeuille expose `risk_budget` à partir des cotations, quantités et stops réellement déclarés. Le risque connu est la distance entre la cote et le stop multipliée par la quantité, uniquement pour les positions non-options mesurables.

Les options et positions sans stop, cote ou quantité restent listées dans `unmeasured` avec leur motif. Vertex ne valorise pas une perte de stop options sans grecques de position, et ne complète jamais un stop absent.
