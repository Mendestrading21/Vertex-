# Vertex — recouvrement résultats-expiration Skyler

Le contexte `earnings_option_overlap` compare le DTE du meilleur contrat options au DTE du prochain résultat fourni par le calendrier. Il indique uniquement si ce résultat déclaré survient avant ou après l’expiration du contrat retenu.

Les deux DTE doivent être explicitement présents. Sans DTE de contrat, le statut est `OPTION_DTE_UNAVAILABLE`; sans DTE de résultats déclaré, le statut est `EARNINGS_DTE_UNAVAILABLE`. Vertex n’estime aucune date, ne transforme pas ce constat en signal et ne modifie ni score, ni gate, ni verdict.
