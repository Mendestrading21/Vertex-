# Definition of Done — par page (§22)

Une page n'est **terminée** que lorsque TOUS ces points sont vrais (sinon : en cours) :

## Sens & données
- [ ] Mission de la page claire (une question principale).
- [ ] Audit de la page documenté (`docs/vertex-audit/pages/<route>.md`).
- [ ] Chaque donnée a une **source vérifiée** (IBKR/yfinance/stooq/demo/moteur) et une **fraîcheur visible**.
- [ ] Calculs testés (unitaires) ; aucun chiffre inventé ; absence → `—`/`n/d`/estimation (jamais `0`).
- [ ] Aucune donnée factice non étiquetée (`DÉMO/MOCK` sinon).

## Design & composants
- [ ] Respecte les tokens (`--vx-*`) — zéro couleur en dur ; palette sémantique (zéro bleu hors info ; violet=options).
- [ ] Cartes = variantes `vx-card` partagées (pas de carte ad hoc).
- [ ] Graphiques = primitives `VXCharts` + contrat (source/ts/question/conclusion) + état vide honnête.
- [ ] Typographie/format via l'échelle centrale + `VX.fmt.*` (chiffres tabulaires alignés).

## Interactions & états
- [ ] Tous les boutons/filtres **fonctionnent** (aucun handler manquant, aucun lien `#`).
- [ ] États gérés : chargement (skeleton fidèle), vide (explique pourquoi + action), erreur (contextualisée),
      déconnexion, données retardées/périmées, marché fermé, mode démo/paper/live.
- [ ] Accessible au clavier ; risque non dépendant uniquement du rouge/vert.
- [ ] Responsive selon l'objectif (desktop prioritaire ; pas de débordement de carte/table).

## Qualité
- [ ] **0 erreur console** ; `/api/client-log` = 0 après visite.
- [ ] `python -m pytest tests/ -q` = 100 % (ne casse aucun test).
- [ ] Vérifiée **dans l'app en fonctionnement** (vrai navigateur, pas seulement curl).
- [ ] Document d'audit de la page mis à jour (résultats, captures, écarts restants, dette).
- [ ] Bump `td-shell-vN` (`vertex/app/routes/system.py`) si le shell visible a changé.
