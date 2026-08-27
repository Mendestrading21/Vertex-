# Règles de design Vertex 2.0

1. Charger `.claude/skills/vertex-design-2-0/SKILL.md` pour tout travail UI. Ses références sont l'unique doctrine de design.
2. Utiliser les tokens `--vx-*` ; aucun hex, rayon ou espacement répété en dur dans une page.
3. Identité **Black Glass — Signal Light** : obsidienne, verre noir, argent, Geist/Geist Mono, sans bordures lourdes ni glow permanent.
4. Sémantique stricte : vert positif, rouge négatif/risque, ambre prudence/stale, violet options. Zéro bleu identitaire, cuivre legacy ou Signal Green de marque.
5. Ne pas ajouter une couche de thème. Corriger le propriétaire le plus bas, migrer les consommateurs, tester, puis retirer le legacy sans consommateur.
6. Faire converger les cartes et métriques vers les primitives partagées ; une page ne crée pas son propre design system.
7. Tous les graphiques passent par le contrat VXCharts : question, conclusion, source, période, unité, fraîcheur, état, resize, destruction et fallback.
8. Une nouvelle page/table doit avoir une question, une route propriétaire, une source réelle, des états et une place claire dans l'architecture.
9. Chiffres tabulaires, formats centralisés, valeurs alignées ; tout le texte visible en français clair.
10. Contraste AA, focus visible, clavier, reduced motion ; gain/risque jamais exprimé uniquement par couleur.
11. Donnée absente = —/n.d. ou état honnête. Aucun exemple présenté comme réel et aucun verdict recalculé dans l'UI.
12. Tout changement visible du shell/statique implique le bump du service worker et les tests associés.
