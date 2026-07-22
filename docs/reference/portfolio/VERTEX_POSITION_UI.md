# Vertex — Interface positions (§31-38)

> **Status: REFERENCE**
> Last verified: 2026-07-22

Portefeuille → Positions :
- Synthèse : valeur, P&L latent, Équipe actions X/10, Options X/3 (CALLS et
  PUTS comptés séparément, PUT max 1).
- **Positions nécessitant une action** (§31) : priorité, ticker, actif,
  statut, action analytique, verdict moteur, P&L, dernière MàJ.
- Table par groupe (Actions/Options) : Source (IBKR/Manuelle/Paper/
  Simulation), statut de cycle de vie, marque, P&L — donnée absente = n/d.

Portefeuille → Options : Options Command Center + drawer d'analyse par
position (identité, marché, plan, décision analytique, payoff).

Sémantique V4 : ACHETER/RENFORCER vert atténué, ATTENDRE ambre,
RÉDUIRE rouge atténué, REFUSER/INVALIDÉE rouge, options dans l'identité prism.
Mise à jour live via le flux SSE existant (aucun rechargement).
