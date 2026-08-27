# Règles de design Vertex 2.0

1. Charger `.claude/skills/vertex-2-0/SKILL.md` pour tout chantier visuel ;
   `vertex-design-2-0` n'est qu'un alias historique.
2. Modifier uniquement la présentation : navigation, templates, CSS, tokens,
   composants, états, rendu graphique, responsive, accessibilité et texte.
3. Ne modifier aucun moteur, calcul, score, gate, donnée, endpoint, provider,
   store, persistance, sync, intégration, prompt métier ou comportement financier.
4. Une nouvelle vue compose uniquement des capacités existantes. Une capacité
   absente devient un état honnête et un besoin hors périmètre.
5. Préserver routes, IDs DOM, contrats JS, clés localStorage, desk sync et
   interfaces consommées, sauf migration visuelle explicitement cartographiée.
6. Utiliser les tokens `--vx-*` et les primitives partagées ; aucune page ne
   crée son propre design system ou une nouvelle couche de thème.
7. Identité canonique : Black Glass — Signal Light, obsidienne, verre noir,
   argent, Geist/Geist Mono, surfaces sans bordures lourdes ni glow permanent.
8. Couleur stricte : vert positif, rouge risque, ambre prudence, violet options,
   cyan exceptionnel pour focus technique. Une lumière dominante par carte.
9. Signature unique Decision Trace aux cinq emplacements documentés. Le Vertex
   Beam reste un reflet de matière discret.
10. Les graphiques peuvent changer de thème et d'options de rendu seulement ;
    séries, valeurs, sources, calculs, agrégations et timeframes ne changent pas.
11. Tout le texte visible est en français clair. Chiffres tabulaires, formats
    centralisés, unités visibles, valeurs alignées.
12. Loading, empty, partial, stale, delayed, offline, demo et error sont
    explicites. Donnée absente = `—` ou `n.d.`, jamais une valeur fabriquée.
13. Contraste AA, focus visible, clavier, reduced motion et sens non dépendant
    de la couleur. Vérifier 390, 768, 1024, 1280 et 1600+ px.
14. Travailler page par page depuis les propriétaires les plus bas : tokens →
    shell → primitive → chart core → page. Captures avant/après au même état.
15. Vérifier tests, console, healthz, client-log et service worker. PR brouillon,
    rollback documenté, aucune fusion automatique.
16. Toute bibliothèque de widget suit `trading-widget-catalog.md` : licence,
    maintenance, poids, sécurité, accessibilité et fallback vérifiés avant usage.
17. Le Simulateur affiche des scénarios multi-actifs issus des capacités
    existantes ; jamais de prédiction certaine, calcul inventé ou action broker.
18. Avant acceptation, exécuter les 150 contrôles documentés et joindre les
    preuves ; une case sans preuve n'est pas validée.
