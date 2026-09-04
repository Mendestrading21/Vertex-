# Vertex — structure call-put Skyler

Le contexte `call_put_structure` réutilise le comptage observé du board options pour le symbole : nombre de calls, de puts et ratio calls/puts quand les deux côtés existent.

Un board absent produit `OPTION_BOARD_UNAVAILABLE`; un seul côté de contrats produit `ONE_SIDED_CONTRACT_SET`. Le contexte ne mesure pas un flux net, ne prédit aucune direction et ne modifie ni score, ni gate, ni verdict.
