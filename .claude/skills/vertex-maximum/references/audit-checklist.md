# Méthode & checklist d'audit Vertex

## Ordre d'audit (Phase 1)
1. Dépôt (arbo, stack, lancement) → `01-repository-map.md`
2. Routes + IA actuelle → `02-current-information-architecture.md`
3. Fonctionnel (par page + anti-fausse-fonctionnalité §25) → `03-functional-audit.md`
4. Design (tokens, cartes, cohérence) → `04-design-audit.md`
5. Composants (`vx-card`…) KEEP/IMPROVE/MERGE/REPLACE/REMOVE → `05-component-inventory.md`
6. Graphiques (`VXCharts`, grille de décision §7) → `06-chart-inventory.md`
7. IBKR (flux, workers readonly, états) → `07-ibkr-integration-audit.md`
8. Données (source/fraîcheur/complétude, demo/mock/réel, `0` vs absent) → `08-data-quality-audit.md`
9. Logique trading (moteurs, explicabilité, plafonds) → `09-trading-logic-audit.md`
10. Performance (mesurer avant d'optimiser) → `10-performance-audit.md`
11. Sécurité (secrets, endpoints, validation) → `11-security-audit.md`
12. Accessibilité (contraste, clavier, non-couleur) → `12-accessibility-audit.md`
→ 13 architecture cible · 14 roadmap priorisée · 15 matrice de pages · 16 risques · 17 journal de décisions.

## Fiche de problème (chaque item d'audit)
`ID` · `page` · `catégorie` · `description` · `gravité (P0/P1/P2/P3)` · `impact utilisateur` · `impact trading` ·
`cause probable` · `solution recommandée` · `complexité relative` · `statut` · `méthode de validation`.

## Classification de gravité
- **P0 — Bloquant** : données erronées, ordre incorrect (n/a car lecture seule mais = « recommandation dangereuse »),
  perte potentielle, app inutilisable, **faux statut live**, **démo présentée comme réel**.
- **P1 — Critique** : fonctionnalité majeure défaillante ou décision potentiellement trompeuse.
- **P2 — Important** : forte dégradation d'expérience ou de compréhension.
- **P3 — Amélioration** : cohérence, finition, performance, confort.

## Anti-fausse-fonctionnalité (§25) — chercher systématiquement
boutons sans handler · liens `#` · valeurs codées en dur · données aléatoires · faux chargements · **faux statut
live** · graphes alimentés par des exemples · widgets sans données · filtres qui ne filtrent rien · formulaires non
enregistrés · actions qui n'affichent qu'un toast · calculs faits seulement côté présentation · **fallback mock
silencieux**. Toute démo → étiquetée `DÉMO/MOCK/SIMULATED`.

## Preuves exigées (jamais « terminé » seul)
résultats de tests · état de compilation · routes vérifiées · captures · logs utiles · mesures de perf · éléments
restant à connecter.
