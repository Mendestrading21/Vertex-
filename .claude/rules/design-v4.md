# Règles de design Vertex V4

Source courte : `.interface-design/system.md`. Source complète :
`docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`. Référence maître :
`docs/vertex-v4/reference/00-master-obsidian-prism.jpg`.

1. **Identité unique.** Obsidian Prism remplace Black Glass, Signal Green et
   Obsidian Copper. Ne jamais réintroduire une ancienne palette ou créer une
   variante locale.
2. **Tokens uniquement.** Couleur, rayon, espacement, ombre, typo et motion
   passent par les variables `--vx-*`. Nouveau besoin = token sémantique documenté.
3. **Couleur stable.** Violet/magenta/corail = marque et sélection ; vert =
   positif ; rouge = perte/risque/erreur ; ambre = attente/incertitude ; bleu =
   comparaison secondaire rare. Une couleur garde le même sens partout.
4. **Typographie.** General Sans pour l'interface, JetBrains Mono pour les
   nombres. Chiffres tabulaires, unités visibles, alignement à droite en table.
5. **Quatre niveaux.** HeroPanel, AnalyticalPanel, MetricTile et InspectorPanel.
   Dériver des primitives partagées au lieu de créer des cartes ad hoc.
6. **Graphiques.** Passer par `window.VXCharts` et
   `docs/canonical/CHART_CONTRACT.md`. Afficher question, source, période,
   unité, fraîcheur, tooltip et conclusion. Aucun graphe décoratif.
7. **États honnêtes.** Loading, empty, partial, stale et error sont conçus et
   testés. Une absence n'est jamais remplacée par zéro ou par une courbe fictive.
8. **Glass localisé.** Réserver le verre à la topbar, aux héros, overlays et
   sélections. Aucun blur/glow permanent sur chaque carte.
9. **Responsive réel.** Contrôler 1536×960, 768×1024 et 390×844 ; aucun overflow
   horizontal ; tables converties ou scrollées de manière intentionnelle.
10. **Accessibilité.** Contraste AA, focus visible, clavier, cibles tactiles et
    information jamais portée uniquement par la couleur.
11. **Service worker.** Tout changement visible du shell impose un bump
    `td-shell-vN` dans `vertex/app/routes/system.py` et la mise à jour des tests.
12. **Migration sûre.** Ne supprimer aucun CSS/script legacy encore chargé sans
    satisfaire chaque condition de `docs/vertex-v4/MIGRATION_MAP.md`.
