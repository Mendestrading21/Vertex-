# Définition de terminé

## Pour un composant

- propriétaire visuel unique et API de présentation documentée ;
- tokens canoniques, tous états, clavier/touch, responsive ;
- aucune logique financière ajoutée ou modifiée ;
- démontré sur `/design-system` si réutilisable ;
- tests ou preuve navigateur proportionnés.

## Pour une page

- question et point focal compris en cinq secondes ;
- mêmes données, calculs, endpoints et fonctions qu'avant ;
- première hauteur utile à 1440×900 ;
- loading, empty, missing, partial, delayed, stale, offline, demo et error selon applicability ;
- deep links, retour, filtres et préférences stables ;
- clavier, zoom, reduced motion et largeurs cibles ;
- console et `/api/client-log` sans erreur applicative ;
- captures avant/après sur le même SHA ;
- tests ciblés et garde-fous verts.

## Pour le lot complet

- toutes les pages existantes auditées et classées ;
- navigation finale cohérente et libellés français ;
- aucun bloc fonctionnel perdu, aucune action existante cassée ;
- composants, graphiques et tables visuellement unifiés ;
- aucun style inline répété lorsque la primitive existe ;
- ancienne doctrine visuelle active supprimée ou explicitement historique ;
- aucune modification dans moteurs, stratégie, providers, endpoints financiers, stores ou sync ;
- compileall, suite pytest et no-orders verts ;
- healthz, client-log, desktop/mobile et modes dégradés vérifiés ;
- service worker à jour ;
- décision humaine avant merge/release.

Ne jamais déclarer « 100 % terminé » avec uniquement une suite de tests verte. Il faut preuve runtime, navigateur, données inchangées et acceptation humaine sur le commit candidat.
