# Vertex — contexte de force relative Skyler

Le contexte `relative_strength` compare le rendement observé du titre et de SPY sur des fenêtres de 20 et 63 séances, uniquement lorsque les clôtures canoniques datées sont communes et alignées.

La sortie fournit les rendements observés et l’écart de rendement. Sans séries valides, alignées ou assez longues, le statut est `INSUFFICIENT_ALIGNED_SERIES`. Vertex n’aligne jamais des séries sans date, ne prédit pas la surperformance et ne modifie ni score, ni gate, ni verdict.
