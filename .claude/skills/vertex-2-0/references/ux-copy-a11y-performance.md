# Français, UX, accessibilité, responsive et performance

## Écriture française

Tout le produit est en français simple. Employer les mots de l'utilisateur : Position, Opportunité, Thèse, Risque, Échéance, Suivi, Source, Donnée retardée. Conserver ticker, CALL/PUT, Greeks, IV, DTE ou drawdown lorsque le terme est standard, avec aide contextuelle.

Voix active et sentence case. Un contrôle annonce son résultat : « Enregistrer la vue », « Ajouter au suivi », « Ouvrir le dossier ». Le toast reprend le même verbe. Éviter « Soumettre », « Cliquer ici », jargon d'architecture et phrases marketing.

Les erreurs disent ce qui a échoué, l'impact et l'action possible. Les états vides orientent sans inventer. Un label ne fait qu'un travail.

## Priorités de qualité

1. Accessibilité.
2. Interaction/touch.
3. Performance visuelle.
4. Hiérarchie et responsive.
5. Typographie/couleur.
6. Formulaires/feedback.
7. Motion.
8. Graphiques.

## Accessibilité

- Contraste 4.5:1 pour texte courant, 3:1 pour grand texte et contrôles.
- Focus visible non masqué ; ordre clavier logique ; skip link.
- Nom accessible pour boutons icône, graphiques et statuts live.
- Cible 44×44 tactile lorsque nécessaire, espacement suffisant.
- Aucune action hover-only ; tooltips disponibles au focus.
- Couleur jamais seule ; labels, signes ou motifs.
- `aria-live` réservé aux changements utiles, sans annoncer chaque tick.
- Respect zoom 200 %, taille de texte et reduced motion.

## Responsive

Vérifier 390, 430, 768, 1024, 1280, 1440, 1600 et écran large. Aucun scroll horizontal global. Le contenu change de hiérarchie, pas seulement de largeur : sidebar → drawer, grilles → piles, rail → accordéon, table → colonnes prioritaires/drawer.

Sur mobile, conserver Aujourd'hui, Recherche, Suivi, Alertes et Plus dans une barre inférieure de cinq destinations maximum. Les pages profondes utilisent un header compact et un retour prévisible.

## Performance visuelle

- CLS < .1 sur parcours vérifiés ; réserver l'espace graphiques/skeletons.
- Lazy-load des vues/graphiques secondaires sans changer leurs sources.
- Debounce uniquement des interactions de recherche/filtre déjà existantes.
- Virtualiser les longues tables dans la couche visuelle si le contrat le permet.
- Transformer/opacity pour motion ; éviter layout thrashing.
- Détruire graphiques, listeners et observers visuels.

## Audit avant livraison

Parcourir au clavier, touch simulé, zoom, reduced motion, offline, stale, partial, error et demo. Vérifier aucun débordement, texte essentiel tronqué, focus perdu, bouton icône sans nom, erreur console, layout shift ou graphique sans résumé.
