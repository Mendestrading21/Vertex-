# Convergence des capacités existantes

## Registre obligatoire

Avant de refondre visuellement un domaine, inventorier en lecture seule :

| Champ | Contenu |
|---|---|
| Capacité | nom fonctionnel français |
| Question | décision ou besoin couvert |
| Propriétaire | module/route/store canonique |
| Entrées | sources, modèles et versions |
| Sorties | schéma et états |
| Consommateurs | pages, jobs, API, tests |
| Réalité | fonctionnel, partiel, fantôme, legacy |
| Doublons | propriétaires concurrents |
| Décision visuelle | conserver, regrouper, déplacer, reformuler, masquer |
| Preuves | tests, navigateur, données, logs |

## Méthode

1. Rechercher le symbole, la route, les appels et les tests.
2. Vérifier le comportement au runtime ; un nom de fonction n'est pas une capacité fonctionnelle.
3. Identifier le propriétaire existant et les données réellement disponibles sans les modifier.
4. Concevoir une présentation unique qui consomme les mêmes sorties.
5. Ajouter des gardiens de non-régression visuelle et fonctionnelle.
6. Retirer uniquement le doublon CSS/HTML lorsque son dernier consommateur visuel a migré.

## Dette à traiter

- routes/pages décrites sous plusieurs noms ;
- anciennes identités visuelles et composants dupliqués ;
- formats d'affichage répétés dans l'UI, sans toucher aux calculs ;
- palettes de rendu Python/CSS/JS divergentes, sans changer les valeurs métier ;
- navigation huit/neuf espaces incohérente ;
- tracking, journal, performance et watchlist qui se chevauchent ;
- plusieurs tableaux ou drawers pour le même objet ;
- actions UI sans handler ou handlers sans surface ;
- documentation historique présentée comme active.

## Règle de composition

Une nouvelle page ou sous-vue visuelle est autorisée uniquement si elle compose des routes, handlers, stores, endpoints et données déjà présents. Si une capacité métier manque, la consigner comme besoin hors périmètre et afficher un état honnête ; ne pas créer provider, endpoint, moteur, schéma ou persistance.
