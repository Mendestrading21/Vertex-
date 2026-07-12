# Vertex — Analyse d'une position option (§20-21)

Accès : Portefeuille → Options → « Analyser » (drawer complet).

- **Identité** : contrat, DTE, quantité × multiplicateur 100, prime/action
  dérivée du coût total desk, capital engagé.
- **Marché** : marque et P&L si cotés ; bid/ask/volume/OI/IV/Greeks
  UNIQUEMENT via IBKR — jamais estimés en agrégat (n/d honnête sinon).
- **Plan** : invalidation sous-jacent, objectif, +50 % typique (jamais
  garanti), time stop indicatif (DTE/6, min 5 j).
- **Décision analytique** : moteur unique `/api/position-decision/<sym>`
  (MAINTENIR/SURVEILLER/SÉCURISER/RÉDUIRE/SORTIE PROPOSÉE/INVALIDÉE) +
  raisons + état du sous-jacent. Aucune exécution.
- **Graphiques** : payoff à l'échéance (arithmétique du contrat) ; la
  matrice spot×temps×IV, theta et sensibilité IV vivent dans le desk
  options (`/api/options/simulate`) car elles exigent IV + spot frais.
- Compteurs : CALLS et PUTS séparés partout (PUT max 1/3).
