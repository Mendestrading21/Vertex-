# Vertex — Portefeuille (Équipe Vertex)

- Structure : 8-10 composantes actions — Offensive (attaquants), Noyau
  (milieux), Défense/gardien (cash, réserve, stabilisateurs). **Les options
  ne sont JAMAIS le gardien** : section « Options tactiques » séparée
  (X/3, CALLS et PUTS comptés séparément).
- Header : valeur (au coût si marques absentes — étiqueté), P&L latent,
  équipe X/10, options X/3.
- Risque : positions RÉELLES/SIMULÉES explicites uniquement
  (`risk_engine`, ValueError sinon), garde-fous (11e position =
  remplacement obligatoire), stress tests (10 scénarios), Greeks agrégés
  broker only.
- Positions : marques `/api/pos-quotes` (spot actions, mark×100 options),
  clôture déclarative → journal automatique. Schéma desk : cost = TOTAL
  investi (unité vérifiée par tests golden).
- Sous-vues : Équipe · Positions · **Options** (command center) · Risque ·
  Watchlist.
