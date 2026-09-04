# Vertex — couverture du moteur de risque portefeuille

Le rapport de risque expose désormais `beta_coverage` pour distinguer les positions dont le bêta est réellement connu des positions non couvertes. Le bêta agrégé existant n’est pas repondéré ni remplacé lorsque la couverture est partielle.

Lorsqu’une exposition options est disponible, `options_exposure.coverage` décrit la part des deltas connus. Les grecques absentes restent absentes et ne sont jamais assimilées à zéro.
