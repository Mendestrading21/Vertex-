# Vertex — contexte de drawdown Skyler

La route Skyler fournit un contexte `drawdown` calculé uniquement à partir des clôtures canoniques du titre. Sur une fenêtre maximum de 63 séances, il expose le drawdown courant, le drawdown maximum constaté, le plus haut observé et le nombre d’observations.

Moins de 21 clôtures, une clôture invalide ou une série non positive produisent `INSUFFICIENT_SERIES`. Vertex ne complète pas la série, ne déduit pas de rebond et ne modifie ni score, ni gate, ni verdict à partir de ce contexte.
