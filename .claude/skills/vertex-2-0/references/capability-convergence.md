# Convergence des capacités existantes

## Registre obligatoire

Avant de développer un domaine, inventorier :

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
| Décision | conserver, fusionner, migrer, retirer |
| Preuves | tests, navigateur, données, logs |

## Méthode

1. Rechercher le symbole, la route, les appels et les tests.
2. Vérifier le comportement au runtime ; un nom de fonction n'est pas une capacité fonctionnelle.
3. Identifier le propriétaire le plus fiable et les données réellement disponibles.
4. Porter les consommateurs vers ce propriétaire.
5. Ajouter des gardiens de non-régression.
6. Retirer le doublon seulement lorsque son dernier consommateur a migré.

## Dette à traiter

- routes/pages décrites sous plusieurs noms ;
- anciennes identités visuelles et composants dupliqués ;
- calculs ou formats répétés dans l'UI ;
- palettes Python/CSS/JS divergentes ;
- navigation huit/neuf espaces incohérente ;
- tracking, journal, performance et watchlist qui se chevauchent ;
- plusieurs tableaux ou drawers pour le même objet ;
- modules présents mais jamais appelés ;
- actions UI sans handler ou handlers sans surface ;
- documentation historique présentée comme active.

## Règle d'ajout

Une nouvelle capacité n'est autorisée qu'après le registre. Elle doit posséder source, contrat, états, propriétaire, consommateur réel, tests, observabilité et rollback. Si elle exige un nouveau provider, traiter licence, entitlement, pacing, cache, timeout, point-in-time, replay et panne partielle avant l'UI.

