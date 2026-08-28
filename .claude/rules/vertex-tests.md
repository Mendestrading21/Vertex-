---
paths:
  - "tests/**"
  - ".github/**"
  - "tools/**"
---

# Tests et preuves

- Un test protège le contrat cible, pas une collision ou dette historique.
- Ne jamais figer un nombre de tests, une ligne ou une taille comme vérité
  permanente ; mesurer le SHA courant.
- Les tests no-orders vérifient qu'une connexion existe et que toutes les
  connexions sont readonly, puis scannent aussi les appels interdits IBKR.
- Les fixtures financières sont synthétiques, explicites et sans compte réel.
- Playwright n'est une preuve que si Chromium est installé et les tests non
  skippés. Captures avant/après : même route, données, état et viewport.
- Résultats exacts, skips, limites, métriques et rollback sont consignés ; une
  suite verte ne remplace pas l'audit runtime et navigateur.
