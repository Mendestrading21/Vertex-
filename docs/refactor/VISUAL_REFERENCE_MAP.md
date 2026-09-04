# VERTEX — Carte canonique des références visuelles

> Direction figée le 12 août 2026 à partir des images fournies par l’utilisateur.
> Elles orientent la hiérarchie, la densité et les interactions. Elles ne sont
> jamais copiées littéralement et ne remplacent ni les données ni la logique de
> Vertex.

## Décision de direction artistique

L’identité reste **VERTEX OBSIDIAN COPPER INSTITUTIONAL** : surfaces obsidienne
et graphite, texte ivoire, cuivre pour l’identité/la sélection/l’action primaire,
émeraude pour un effet financier réellement favorable, corail pour une perte ou
un risque réel, jaune pour attente/seuil/avertissement, cyan pour comparaison
technique et violet pour options/volatilité.

Les références convergent vers une même architecture :

1. navigation calme et stable ;
2. titre, contexte, période, provenance et filtres sur un seul niveau ;
3. trois ou quatre KPI maximum ;
4. un graphique dominant par vue ;
5. un rail de contexte pour risques, événements, sources ou actions READONLY ;
6. un tableau de preuve sous le graphique ;
7. les détails secondaires dans un disclosure ou un drawer.

## Corpus reçu

Vingt fichiers ont été transmis. Dix-sept sont uniques ; trois sont des doublons
octet pour octet et ne comptent pas comme des votes supplémentaires.

| Fichier | Rôle retenu | À reprendre | À écarter |
|---|---|---|---|
| `9D8A6E05-1286-4EFB-ABE8-527D3DBCECA6.jpeg` | **Squelette maître de page** | 4 KPI → graphique hero → composition → preuves → tableau, rythme vertical, surfaces mates | orange répété partout, avatars/pills décoratifs |
| `E1654E95-662F-45DF-B385-565FA015E530.jpeg` | **Grille maître** | grille 12 colonnes, gap 16 px, couple 4/8, heatmap lisible, tooltip/crosshair, tableau dense | corail comme marque, courbes trop lissées |
| `9604FA1F-630C-418D-9909-42001FB3ED1E.jpeg` | **Hiérarchie analytique** | 4 KPI, graphique 8/12 + insight rail 4/12, tableau + ranking | carte KPI orange pleine, jauge sans échelle métier |
| `E95FBE06-D504-46C8-932A-B8ABAE021B01.jpeg` | **Interaction de détail** | drawer contextuel, header/footer sticky, onglets, contexte visible, navigation précédent/suivant | grand verre coloré, rayons excessifs, actions exécutables |
| `8CB3C7B2-9007-4B73-B5C4-44A461C244AB.jpeg` | **Échelle des graphiques** | variantes micro, compact, standard, hero avec une même grammaire | arc-en-ciel, glow, axes/units absents |
| `542A1447-F9BE-4278-8C0A-5EB38E86446C.jpeg` | Tables, sources et rail | liste aérée, métriques avant/après, couverture et sources à droite | bleu identitaire, contrôles icon-only ambigus |
| `E87498C2-A3B8-40C2-B280-CC4588169934.jpeg` | Opportunités | trois candidats comparables, sparkline annotée, détail sélectionné | promo dans une zone premium, violet de marque |
| `90A9332C-B22F-4E48-83B7-BC5B99633C29.jpeg` | Analyse financière | axe zéro clair, graphique dominant + synthèse latérale, conclusion intégrée | hachures décoratives, rose/bleu de marque |
| `8D0DB98B-6B95-42D7-85FB-78E1ACCD5344.jpeg` | Densité compacte | composition asymétrique, tableau d’historique propre, contrôles locaux | microtexte, graphiques sans provenance |
| `8F93937E-16E2-4A8C-924E-BBB8327BB11D.jpeg` | Fiche instrument | contexte → métriques → chart hero → rail instrument | fond arc-en-ciel, courbe lissée, Buy/Sell |
| `299590B5-0D79-4D34-A0F2-2CB570E2BC53.jpeg` | Monitoring sobre | barres classées, histogramme centré, zones de seuil | halos permanents, jauges décoratives |
| `F9CEAA58-E025-4496-BB11-BEFCE2D20042.jpeg` | Sévérité et statuts | échelle vert/jaune/orange/rouge, listes compactes | série de donuts et carte sans décision |
| `3D6078B5-352A-4125-ABAE-2B572EE48831.jpeg` | Précision opérationnelle | unités, fraîcheur, période commune, crosshair synchronisé | mur de données, tuiles saturées, texte minuscule |
| `2B36DD9C-D3A6-4578-8AEF-665C8F371A3C.jpeg` | Respiration | grands groupes cohérents, graphique accompagné d’une liste | halo de cadre, hero marketing, navigation tentaculaire |
| `A14A8BB9-F440-4F2E-B976-CCE0058ABEC3.jpeg` | Anti-pattern / Système | unité + fraîcheur, sparklines de santé | mosaïque arc-en-ciel, tableau entièrement coloré |
| `A36B0F79-3213-42F4-A492-6A40C04164EB.jpeg` | Expertise avancée | diagrammes de dépendances uniquement si données réelles, période compacte | esthétique cyber, lignes néon et topologie décorative |
| `3615BBD1-DC07-4AB6-8404-94145D817414.jpeg` | Cockpit compact | micro-classements, barres d’objectif | densité sans priorité, trop de couleurs et de graphes égaux |

Doublons confirmés par SHA-256 :

- `F957A92C-1CAB-4E91-A6F9-24DA8BC3FC75.jpeg` = `8F93937E-16E2-4A8C-924E-BBB8327BB11D.jpeg` ;
- `783C28A5-236E-4A3A-A258-03949C66E070.jpeg` = `90A9332C-B22F-4E48-83B7-BC5B99633C29.jpeg` ;
- `C5677D66-C840-4351-A65E-65BAD9DE33D8.jpeg` = `8D0DB98B-6B95-42D7-85FB-78E1ACCD5344.jpeg`.

## Contrat de layout

- Contenu : grille 12 colonnes, `gap: 16px`, `minmax(0, 1fr)`.
- Carte : rayon 14–16 px, bordure 1 px, padding 20 px desktop / 16 px mobile.
- Premier écran : une réponse, quatre KPI maximum, un graphe principal, trois
  alertes/actions maximum, un tableau principal.
- Gabarit analytique : hero `8/12` + rail `4/12` ; passage commun en une colonne
  à 1024 px ; mobile à 390 px sans débordement horizontal.
- Les cartes analytiques sont inertes. Seuls liens, boutons, lignes annoncées et
  éléments `[data-clickable]` reçoivent un hover de déplacement.
- Drawer : `min(520px, 40vw)` sur desktop, plein écran sur mobile, focus piégé,
  fermeture Échap, retour du focus, header et footer sticky.

## Contrat graphique

| Variante | Hauteur du tracé desktop | Usage |
|---|---:|---|
| `micro` | 72 px | KPI + sparkline |
| `compact` | 176 px | preuve secondaire |
| `standard` | 240 px | graphique analytique |
| `hero` | 360 px | prix, portefeuille ou décision principale |

À 390 px, ces tracés passent respectivement à 64, 156, 208 et 268 px afin de
préserver les contrôles, la conclusion et la provenance sans créer une page
artificiellement interminable.

- Série principale cuivre 2–2,25 px ; comparaison cyan 1,25–1,5 px ; benchmark
  sable/acier ; options violet.
- Émeraude/corail ne sont employés que si le sens favorable/défavorable est
  certain. Une simple hausse n’est pas automatiquement verte.
- Grille horizontale à 5–6 % de blanc, remplissage limité à 8–12 %, points au
  survol et sur la dernière valeur seulement, zéro/seuil plus visible.
- Quatre ticks maximum sur mobile, six sur desktop ; unité identique sur axe,
  tooltip et conclusion.
- Tooltip graphite : date/heure exacte, série, valeur, unité et provenance ;
  interaction tactile et clavier lorsque le rendu le permet.
- Aucune courbe de prix/P&L lissée si cela peut inventer un sommet ou un creux.
- Donut seulement pour une composition exacte ; jauge seulement pour une mesure
  bornée ; radar seulement si tous les axes comparables sont disponibles.
- Toute carte porte période, source, fraîcheur, état et limite ; `n/d` ne devient
  jamais zéro.

## Contrat tableau

- Header sticky de 38–40 px, lignes de 46–52 px, aucune séparation verticale.
- Texte à gauche ; nombres et unités à droite en JetBrains Mono tabulaire.
- Première colonne forte avec contexte secondaire ; statut en pill uniquement.
- Hover graphite discret, sélection/focus par liseré cuivre et affordance
  « Ouvrir »/chevron toujours perceptible.
- Colonnes secondaires masquées progressivement ; la comparaison reste dans une
  zone scrollable contenue ou devient une carte mobile explicite.
- États chargement, vide, erreur, périmé, démo et données insuffisantes restent
  visuellement et sémantiquement distincts.

## Application aux espaces Vertex

| Espace | Mission visible | Preuve principale | Détails |
|---|---|---|---|
| Aujourd’hui | ce qui mérite une action maintenant | contexte régime + changements | alertes, calendrier, opportunités |
| Marchés | vent de dos ou de face | régime/breadth/volatilité selon la vue | internals et méthodologie repliés |
| Opportunités | meilleur couple asymétrie × probabilité | classement + matrice ou scatter | funnel, scores techniques, options |
| Analyse | verdict, niveaux et invalidation | chandeliers/prix | thèse, preuves et outils repliés |
| Portefeuille | risque et action prioritaires | performance ou stress | concentration, dépendances, discipline |
| Options | asymétrie et risque de structure | payoff/IV/GEX selon la vue | Greeks, scénarios et contrats |
| Journal | améliorer la méthode | erreur/calibration la plus utile | mémoire et ledger avancés |
| Système | peut-on faire confiance aux données | matrice de santé et fraîcheur | intégrations et diagnostics |

## Interdits

- palette différente par page, glow permanent, verre lourd et néon crypto ;
- plus de trois graphiques de poids égal dans la zone visible ;
- chiffres ou courbes inventés, valeur absente remplacée par zéro ;
- plusieurs représentations du même KPI sans nouvelle question ;
- labels inférieurs à 11 px sur un graphique décisionnel ;
- boutons Acheter/Vendre/Exécuter ou toute ambiguïté avec un ordre ;
- détails d’implémentation (`canonique`, paragraphes de Constitution, clés brutes)
  dans le parcours principal.

## Autorités complémentaires

La carte s’applique avec `.interface-design/system.md`,
`docs/archives/interface-visuel/VERTEX_DESIGN_TOKENS.md`, `docs/archives/interface-visuel/VERTEX_OBSIDIAN_COPPER_DEEP.md`,
`docs/refactor/CHART_INVENTORY.md` et le skill `vertex-total-rebuild`. En cas de
conflit visuel, ce document tranche la composition ; les invariants de données,
de provenance, d’accessibilité et READONLY restent toujours supérieurs.
