# Vertex — preuve temporelle canonique

La validation `vertex.data.temporal_evidence.assess` contrôle les paires `series.dates` / `series.close` sans modifier les prix. Elle exige des listes de même longueur, des dates ISO strictement croissantes et des clôtures positives finies.

Les statuts `TEMPORAL_EVIDENCE_AVAILABLE`, `TEMPORAL_EVIDENCE_REQUIRED` et `INSUFFICIENT_SAMPLE` sont descriptifs. Les espaces entre séances sont comptés comme information (`long_gaps`) mais Vertex n’interpole jamais de clôture et ne déduit jamais un prix absent.
