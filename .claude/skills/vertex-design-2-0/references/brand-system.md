# Identité Vertex Black Glass — Signal Light

## Sensation recherchée

Vertex doit évoquer un bureau d'analyse privé, pas une plateforme crypto, un jeu ou un template d'administration. Le noir donne le calme ; le verre organise les niveaux ; l'argent structure ; les couleurs sémantiques attirent l'œil seulement lorsqu'une décision l'exige.

## Palette cible

Conserver les tokens sémantiques existants lorsqu'ils sont compatibles, puis faire converger leur exécution vers cette matrice :

| Rôle | Cible | Usage |
|---|---:|---|
| Fond profond | `#050607` | page et zones les plus basses |
| Fond principal | `#090b0e` | shell |
| Graphite | `#0e1116` | zones secondaires |
| Verre subtil | `rgba(255,255,255,.025)` | groupes sans interaction |
| Verre carte | `rgba(255,255,255,.045)` | carte standard |
| Verre élevé | `rgba(255,255,255,.070)` | hero, drawer, sélection |
| Texte principal | `#f5f7fa` | titres et valeurs |
| Texte secondaire | `#b8bec8` | labels et explications |
| Texte discret | `#7a828f` | meta, sources, aide |
| Argent | `#c9ced8` | marque, sélection, focus, série principale |
| Positif | `#36c889` | gain, hausse, validation réelle |
| Négatif | `#ed655c` | perte, baisse, risque, blocage |
| Prudence | `#dda23b` | stale, delayed, incertitude, surveillance |
| Options | `#9c79d0` | IV/Greeks/options, jamais verdict |

Ne pas utiliser de bleu identitaire. Ne pas ajouter une couleur pour différencier une série si une nuance, un motif, un dash ou une forme suffit.

## Surfaces sans « boîtes »

- Préférer fond, espace, contraste tonal et regroupement à une bordure visible.
- Hairline standard : blanc entre `.045` et `.075` d'opacité ; strong uniquement pour focus ou sélection.
- Une carte standard n'a pas besoin d'ombre externe. Les niveaux élevés peuvent recevoir une ombre noire diffuse.
- `backdrop-filter` est un enrichissement, jamais une condition de lisibilité. Prévoir un fallback graphite.
- Aucun gradient coloré de remplissage. Les gradients neutres sont courts et presque imperceptibles.

## Vertex Beam

Signature exclusive : une ligne/reflet argenté de 1 px, diffusé sur 20 à 35 % de la largeur, placé en haut d'un hero ou d'une sélection structurante. Maximum un Beam fort dans la hauteur visible. Il ne s'anime qu'à l'entrée ou au changement d'état, moins de 260 ms, puis reste fixe.

## Typographie

- Interface : `Geist`, puis `Inter`, `system-ui`, sans-serif.
- Données : `Geist Mono`, puis `JetBrains Mono`, monospace.
- Toute valeur dynamique utilise `tabular-nums`.
- Page 30–32 px / 650–700 ; section 18–20 px / 600 ; carte 13–14 px / 600 ; corps 13–14 px / 400–500 ; meta 11–12 px ; KPI 24–32 px.
- Pas de titres entièrement en capitales hors micro-labels de 11 px maximum.
- Limiter le tracking. Les chiffres restent compacts et alignés.
- Les formulations françaises sont courtes : titre, conclusion, preuve, source.

## Géométrie

- Grille 4 px ; espaces principaux 8, 12, 16, 20, 24, 32.
- Carte : rayon 14–16 px ; contrôle : 9–10 px ; pill uniquement pour badge ou filtre compact.
- Hauteur bouton 36 px desktop, 42 px tactile ; ligne de table 40–44 px.
- Grille 12 colonnes ; largeur de contenu maximale proche de 1600 px ; gaps 12–16 px.

## Motion

- 140 ms interaction, 200 ms transition, 260 ms entrée ; courbe ease-out.
- Hover : variation tonale et déplacement maximal de 1 px.
- Press : `scale(.98)`.
- Aucune animation infinie hors indicateur de chargement indispensable.
- Respect intégral de `prefers-reduced-motion`.

