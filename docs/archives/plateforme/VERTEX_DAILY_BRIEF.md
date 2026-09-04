# Vertex — Brief quotidien (§15)

`vertex/market/daily_brief.py` + pipeline
(`news_pipeline` → validation → `news_dedup` → classification/entités →
`news_impact` → synthèse).

- Types par horloge New York : PRE_MARKET / INTRADAY / CLOSE / WEEKLY.
- 10 sections §15 (situation, indices, taux/vol, actualité dominante,
  secteurs leaders/faibles, entreprises, options, portefeuille, discipline)
  + version compacte, what-changed sourcé, risque principal, opportunité
  principale, sources.
- **Rien d'inventé** : un événement exige titre + source + heure (rejets
  comptés) ; les doublons fusionnent (corroborations) ; l'impact est
  toujours POTENTIEL ; flux hors ligne → la section le dit
  (`test_brief_does_not_invent_news`). Trump/records/résultats n'y entrent
  que via un événement réel du flux — jamais pour rendre le texte
  spectaculaire.
- Servi par `/api/briefing/editorial` (schéma historique préservé),
  affiché dans le Brief hero du Briefing.
