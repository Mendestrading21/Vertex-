# Vertex — synthèse de couverture du board options

`board_coverage` agrège les métadonnées déjà présentes sur les contrats du board : exhaustivité des champs de liquidité, bid/ask réellement cotés et horodatages reportés.

La synthèse est strictement descriptive. Elle ne modifie ni le classement, ni les contrats, ni les scénarios ou les recommandations pédagogiques.

Le payload `/options/<sym>` expose cette synthèse sous `option_board_coverage`. La liste `contracts` conserve son format et son ordre existants.
