# Vertex Visual Rebuild Workflow

## Sommaire
- Préparation
- Audit
- Architecture
- Design
- Implémentation
- Graphiques
- Micro-copy
- Tests
- Validation
- Commit/PR
- Règles de progression

## Préparation
1. Lire `CLAUDE.md`.
2. Lire `SKILL.md`.
3. Lire uniquement les références pertinentes.
4. Identifier la route canonique et le fichier page.
5. Identifier les CSS/JS/primitives réellement chargés.
6. Lire les tests qui gardent la page.
7. Vérifier si la modification touche `/static` et donc le service worker.

## Audit de page
Créer un inventaire avant de coder :

| Élément | Rôle | Donnée/source | Action | Problème | Décision |
|---|---|---|---|---|---|
| Hero | résumé | API X | aucune | trop long | REWRITE |
| KPI | risque | moteur Y | analyse | faible poids | REDESIGN |

Décisions autorisées :
- `KEEP`
- `MERGE`
- `MOVE`
- `REWRITE`
- `REDESIGN`
- `DELETE`

### Questions d’audit
- Quel est le premier chiffre que l’œil voit ? Est-ce le bon ?
- L’utilisateur sait-il quoi regarder en 5–10 secondes ?
- Y a-t-il des informations dupliquées ?
- Des cartes existent-elles seulement parce qu’elles existaient avant ?
- Les couleurs portent-elles du sens ?
- Les actions sont-elles vivantes ?
- Les textes sont-ils plus longs que nécessaire ?
- Les graphiques répondent-ils à une question ?
- Le risque est-il visible sans interaction ?
- L’état live/différé est-il honnête ?

## Architecture avant design
Écrire la nouvelle page sous forme de blocs, par exemple :

`Header`
`Signal row`
`Decision hero 8 cols | Risk panel 4 cols`
`Price chart 8 cols | Catalysts 4 cols`
`Evidence grid`
`Detail table`

Ne pas commencer par modifier 200 règles CSS sans architecture.

## Wireframe logique
Pour chaque bloc, définir :
- but ;
- information primaire ;
- information secondaire ;
- action ;
- état vide ;
- comportement mobile.

## Réutilisation
Avant de créer : rechercher classes, builders, chart primitives, tables, badges, drawers et helpers existants. Étendre le canonique si l’usage se répète.

## Implémentation
Ordre recommandé :
1. markup/structure ;
2. tokens/primitives ;
3. layout ;
4. visual polish ;
5. micro-copy ;
6. interactions ;
7. graphiques ;
8. responsive ;
9. accessibilité ;
10. tests.

## CSS
- Token d’abord.
- Pas d’hex local si token disponible.
- Pas de `!important` sauf dette legacy explicitement justifiée.
- Pas de sélecteur de 5 niveaux si une classe composant suffit.
- Supprimer les anciennes règles devenues mortes lorsque la preuve est claire.
- Garder `signal-os.css` comme couche cohérente, mais migrer les règles structurelles vers primitives canoniques si elles deviennent durables.

## JavaScript UI
- La couche visuelle ne fait pas de calcul financier.
- Réutiliser le bus/context existant.
- Pas de handler inline dupliqué si délégation globale possible.
- Tout bouton a un handler réel.
- Teardown des charts/listeners si navigation SPA.
- Respect clavier/Escape/focus trap.

## Graphiques
Suivre `CHARTS.md`. Pour chaque chart, écrire dans le code ou le plan :
- question ;
- conclusion ;
- source ;
- timeframe ;
- unité ;
- fraîcheur ;
- état vide.

## Micro-copy
Faire une passe dédiée après la structure. Rechercher :
- répétitions ;
- titres longs ;
- `Overview`/`View more`/labels génériques ;
- mélange FR/EN ;
- texte marketing ;
- explications permanentes qui peuvent aller dans drawer/tooltip.

## Responsive
Tester au minimum :
- 1440 px ;
- 1024 px ;
- 768 px ;
- 390 px ;
- 320–360 px si composant critique.

Pour chaque breakpoint : navigation, header, grilles, charts, tables, drawers, modals, action bar.

## Accessibilité
- landmarks/aria-label utiles ;
- `aria-current` navigation ;
- labels inputs ;
- focus visible ;
- contraste ;
- bouton icône avec nom accessible ;
- navigation clavier ;
- reduced motion ;
- chart avec aria-label/résumé.

## Tests
### Avant changement
Exécuter les tests ciblés pour établir la baseline si possible.

### Après changement
1. tests de la page ;
2. gardiens UI ;
3. gardiens design/palette ;
4. tests PWA si `/static` changé ;
5. suite complète avant PR prête.

## Cache PWA
Tout octet servi sous `/static` peut modifier le fallback offline. Si `/static` change :
- bump `td-shell-vN` ;
- aligner tous les gardiens de version ;
- recalculer l’empreinte du test de cache ;
- exécuter les tests associés.

Ne jamais contourner un test de cache en le supprimant.

## Validation visuelle
Une page n’est pas validée uniquement parce que les tests passent. Contrôler :
- hiérarchie ;
- alignements ;
- clipping ;
- overflow ;
- wrapping ;
- contraste ;
- hover/focus ;
- skeleton ;
- empty/error ;
- charts ;
- table ;
- mobile.

## Commit
Un commit de refonte doit décrire l’intention, ex. :
`design: rebuild opportunities around asymmetry and grade`

Éviter `fix ui`.

## PR
Maintenir une section :
- Page reconstruite
- Avant / problème
- Nouvelle hiérarchie
- Primitives touchées
- Tests
- Responsive
- Risques/dette restante

## Règle de progression
Ne pas lancer cinq pages en parallèle. Une page validée devient la référence pour la suivante. Si un problème global est découvert, corriger la primitive puis revalider les pages déjà migrées affectées.
