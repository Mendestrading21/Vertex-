# Design system final — Vertex Black Glass Signal Light

## Références utilisateur

Les neuf références du 27 août 2026 définissent le langage visuel : sidebar noire compacte, grande zone analytique, cartes graphite/verre, angles doux, graphiques lumineux, contrôles précis, mise en page desktop dense et adaptation mobile réelle.

### À reprendre

- structure latérale stable et contenu principal très organisé ;
- cartes profondes, peu opaques, séparées par niveaux de surface ;
- grandes visualisations dominantes entourées de petites preuves ;
- chiffres très lisibles, tables compactes et sparklines ;
- lumière locale cyan/violet/orange sur interactions ou séries ;
- responsive qui conserve la hiérarchie ;
- sensation de produit financier/IA premium.

### À corriger

- ne pas entourer chaque contrôle d'un néon permanent ;
- ne pas utiliser six couleurs dans le même écran ;
- ne pas multiplier donuts/jauges décoratifs ;
- ne pas reprendre les boutons « Upgrade », blocs marketing ou chiffres fictifs ;
- ne pas compresser un terminal desktop entier sur mobile ;
- ne pas colorer une navigation active comme un signal financier.

## Intention

Froid, calme et institutionnel comme une salle d'analyse privée après la clôture ; dense comme un terminal, mais hiérarchisé comme un produit premium. Variance visuelle 4/10, motion 2/10, densité 8/10 desktop et 6/10 tablette.

## Signature unique : Decision Trace

Une ligne argentée fine relie quatre nœuds : **Donnée → Moteur → Décision → Portefeuille**. Chaque nœud expose source/âge, gate, verdict ou impact. La couleur n'apparaît qu'au nœud qui porte réellement ce sens. Utiliser la signature dans exactement ces familles : hero Aujourd'hui, drawer Opportunité, hero Analyse, audit de décision IA et simulation d'impact Portefeuille.

Le `Vertex Beam` reste un reflet matériel discret sur une surface élevée ; il n'est pas une deuxième signature.

## Palette canonique

| Token de rôle | Valeur cible | Usage |
|---|---:|---|
| `--vx-night` | `#050607` | fond profond |
| `--vx-shell` | `#090b0e` | shell |
| `--vx-graphite` | `#0e1116` | niveau secondaire |
| `--vx-glass-subtle` | `rgba(255,255,255,.025)` | groupe |
| `--vx-glass-card` | `rgba(255,255,255,.045)` | surface standard |
| `--vx-glass-raised` | `rgba(255,255,255,.070)` | hero/drawer |
| `--vx-ink` | `#f5f7fa` | texte principal |
| `--vx-silver` | `#c9ced8` | structure/sélection/série |
| `--vx-mist` | `#b8bec8` | texte secondaire |
| `--vx-smoke` | `#7a828f` | meta |
| `--vx-positive` | `#36c889` | positif réel |
| `--vx-negative` | `#ed655c` | négatif/risque |
| `--vx-caution` | `#dda23b` | prudence/stale |
| `--vx-options` | `#9c79d0` | options seulement |
| `--vx-analysis-light` | `#65d8e8` | interaction analytique rare |

Le cyan analytique est limité aux crosshairs, focus d'un graphique ou comparaison technique. Il ne devient jamais couleur de marque, navigation ou verdict. Aucun bleu identitaire, cuivre, Signal Green ou dégradé multicolore.

## Distribution de couleur

- 82 % obsidienne/graphite ;
- 13 % blanc/argent/gris ;
- 5 % couleurs sémantiques et lumière analytique.

Maximum une couleur lumineuse dominante par carte et deux par écran hors vert/rouge directionnels. Le halo reste sous 12 % d'opacité et ne passe jamais derrière un texte long.

## Profondeur

Une seule stratégie : niveaux de verre + contraste tonal + espace négatif. Hairlines blanches .045–.075 ; strong .14 pour focus/sélection. Pas de bordure décorative lourde. Ombre noire diffuse uniquement pour drawer/modal. `backdrop-filter` avec fallback graphite.

## Typographie

- UI : Geist variable 400–700.
- Données : Geist Mono 400–650.
- Page 30–32/650 ; section 18–20/600 ; carte 13–14/600 ; corps 14/450 ; meta 11–12 ; KPI 24–32.
- Table 12.5–13 minimum en dense ; préférence de taille disponible.
- Chiffres tabulaires, décimales alignées, unités stables.
- Sentence case en français ; capitales réservées aux micro-labels et tickers.

## Grille et mesures

Base 4 px ; espaces 4/8/12/16/20/24/32/40. Sidebar 236 px, réduite 72 px ; topbar 60–64 px ; contenu max 1600–1680 px ; grille 12 colonnes ; gaps 12/16. Rayon contrôle 9–10, carte 14–16, modal 18, pill uniquement badge/chip.

Composition inspirée des références : bande KPI compacte, une carte graphique dominante sur 7–8 colonnes, rail analytique sur 4–5 colonnes, puis table pleine largeur. Éviter le bento aléatoire.

## Motion

140 ms interaction, 200 ms transition, 260 ms entrée, ease-out. Hover tonal + 1 px maximum ; press .98. Animer transform/opacity, pas width/height. Une orchestration courte à l'entrée d'une page, pas des animations dispersées. Reduced motion obligatoire.

## Tests de craft

- Permutation : remplacer logo/copie ; l'interface reste identifiable par Decision Trace, hiérarchie et tokens.
- Distance : à 25 % de zoom, le point focal et les groupes restent visibles.
- Signature : cinq emplacements précis fonctionnent sans duplication décorative.
- Tokens : chaque nom exprime le monde Vertex ou un rôle fonctionnel clair.
- Retrait : supprimer une décoration avant livraison si elle n'améliore ni hiérarchie ni compréhension.
