---
paths:
  - "vertex/data_sources/**"
  - "vertex/positions/**"
  - "vertex/portfolio/**"
  - "vertex/app/routes/**"
  - "vertex/ai/**"
  - "terminal.py"
---

# Données, confidentialité et backend

- Appliquer `ibkr-market-data-only.md`, `manual-portfolio.md` et
  `ai-decision-contract.md` du skill maître.
- Aucun `accountId` dans l'enveloppe de marché. Origine de position et source
  de prix restent séparées.
- Une connexion `enabled` n'est pas `CONNECTED` sans preuve socket/fraîcheur.
- GET reste sans effet de bord. Une panne ne détruit aucun snapshot utilisateur.
- Aucun réseau lent dans une requête UI ; utiliser snapshot borné et daté.
- `scan_state` est muté en place jusqu'à migration canonique prouvée.
- Texte externe sanitizé ; cache privé `no-store` pour données personnelles.
- Toute migration du desk sauvegarde, prévisualise, teste l'idempotence et le
  rollback. Ne jamais éditer `desk_data.json` à la main.
