# Vertex Validation — Definition of Done

## Sommaire
- Page DoD
- Component DoD
- Chart DoD
- Copy DoD
- Responsive matrix
- Accessibility
- Data honesty
- Security
- Tests
- Final release gate

## Page Definition of Done
Une page est terminée uniquement si toutes les cases sont vraies.

### Structure
- [ ] La question principale de la page est évidente.
- [ ] L’information primaire apparaît avant les détails.
- [ ] Le risque/invalidation est visible lorsque pertinent.
- [ ] Les doublons ont été supprimés ou fusionnés.
- [ ] Les sections suivent une logique de décision.
- [ ] Aucun widget n’existe uniquement pour remplir l’espace.

### Visuel
- [ ] Palette sémantique respectée.
- [ ] Une seule famille de radius/borders/surfaces.
- [ ] Hiérarchie typographique cohérente.
- [ ] Pas de glow/gradient décoratif excessif.
- [ ] Alignements et gaps réguliers.
- [ ] Les chiffres dominants sont réellement les chiffres importants.

### Interactions
- [ ] Tous les boutons ont un handler.
- [ ] Tous les liens internes répondent.
- [ ] Hover/pressed/focus visibles.
- [ ] Escape ferme drawer/modal.
- [ ] Focus trap si modal.
- [ ] Command palette et navigation restent fonctionnelles.

### Données
- [ ] Source affichée si nécessaire.
- [ ] Timestamp/fraîcheur visible.
- [ ] Loading présent.
- [ ] Empty présent.
- [ ] Error présent.
- [ ] Stale présent si applicable.
- [ ] Demo/offline impossibles à confondre avec live.
- [ ] Aucune donnée synthétique inventée pour éviter un vide.

### Copy
- [ ] Titres courts.
- [ ] Labels cohérents.
- [ ] Pas de texte marketing.
- [ ] Pas de mélange FR/EN évitable.
- [ ] Les boutons utilisent des verbes explicites.
- [ ] Les scénarios décrivent les conditions, pas seulement les gains.

## Component Definition of Done
- [ ] Fonction unique claire.
- [ ] API/props ou helper cohérent avec les primitives existantes.
- [ ] États normal/hover/focus/disabled/loading/empty selon besoin.
- [ ] Mobile prévu.
- [ ] Aucun style dupliqué inutilement.
- [ ] Aucun littéral couleur si token disponible.
- [ ] Accessible clavier.
- [ ] Pas de calcul financier local ajouté.

## Chart Definition of Done
- [ ] Une question décisionnelle explicite.
- [ ] Une conclusion.
- [ ] Titre.
- [ ] Timeframe.
- [ ] Unité.
- [ ] Source.
- [ ] Timestamp/fraîcheur.
- [ ] Palette canonique.
- [ ] Projection distincte du réalisé.
- [ ] Tooltip concis.
- [ ] Axes non surchargés.
- [ ] État vide honnête.
- [ ] Aria-label/résumé.
- [ ] Pas d’instance Chart.js orpheline au teardown.

## Responsive matrix
Tester chaque page sur :

| Largeur | Shell | Header | Grille | Charts | Tables | Modals/drawers |
|---|---|---|---|---|---|---|
| 1440 | complet | complet | 2–3 cols | complet | complet | desktop |
| 1024 | compact | complet | 2 cols | lisible | scroll si besoin | desktop compact |
| 768 | rail/mobile transition | compact | 1–2 cols | réduit | scroll | quasi plein écran |
| 390 | mobile | priorité | 1 col | 280–340px | cards/scroll | plein écran |
| 320–360 | mobile | minimum vital | 1 col | sans clipping | utilisable | plein écran |

À chaque largeur :
- [ ] zéro scroll horizontal global ;
- [ ] aucune valeur coupée ;
- [ ] aucun bouton inaccessible ;
- [ ] aucun header de carte sur deux lignes absurdes ;
- [ ] tooltips/popovers restent dans viewport.

## Accessibilité
- [ ] `aria-current` pour nav active.
- [ ] Icônes seules nommées.
- [ ] Labels de formulaires.
- [ ] Focus visible.
- [ ] Contraste lisible.
- [ ] Pas d’information portée uniquement par couleur.
- [ ] Reduced motion respecté.
- [ ] Dialogues correctement nommés.
- [ ] Escape / tab order corrects.

## Sécurité produit
- [ ] Aucun `placeOrder`.
- [ ] Aucun `place_order`.
- [ ] Aucun `submit_order`.
- [ ] Aucun `transmit` d’ordre.
- [ ] Aucun auto-execute.
- [ ] Aucun bouton présenté comme un achat/vente réel.
- [ ] Les actions restent analyse/suivi/alerte/notes/export.

## Tests minimaux après une page
Exécuter les tests ciblés de page + :
- gardiens de navigation/routes ;
- gardiens boutons/handlers ;
- gardiens graphiques si charts touchés ;
- gardiens palette si couleur touchée ;
- gardiens accessibilité ;
- gardiens readonly ;
- gardiens service worker si `/static` touché.

## Suite complète
Avant de déclarer la refonte générale prête : `pytest -q` doit être vert. Si des tests échouent pour une ancienne attente volontairement remplacée, mettre à jour le contrat et le test de façon cohérente, jamais masquer l’échec.

## Contrôle navigateur
Si un environnement navigateur est disponible :
- [ ] ouvrir chaque route canonique ;
- [ ] vérifier console ;
- [ ] vérifier network critique ;
- [ ] tester navigation au clavier ;
- [ ] tester resizing ;
- [ ] tester modales/drawers ;
- [ ] tester graphiques ;
- [ ] tester états sans données si reproductibles.

## Final release gate
La branche n’est prête à fusionner que si :
1. les 8 pages ont passé leur DoD ;
2. le shell est cohérent ;
3. la palette Python/JS/CSS est synchronisée ;
4. le cache PWA est cohérent ;
5. la suite complète est verte ;
6. la sécurité READONLY est verte ;
7. aucune dette visuelle majeure n’est cachée ;
8. le PR décrit les limitations restantes.
