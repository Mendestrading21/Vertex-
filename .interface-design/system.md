# Vertex — Système d'interface canonique

> Mémoire de craft alignée sur `.claude/skills/vertex-2-0/SKILL.md`.
> Le skill maître et ses références priment en cas de divergence.

## Intention

**Vertex Black Glass — Signal Light** est un centre personnel de trading IA,
calme, dense et précis. La lecture doit être évidente en cinq secondes : ce qui
se passe, ce qui mérite l'attention, pourquoi et avec quel risque.

La refonte est uniquement visuelle. Ne modifier ni logique métier, ni données,
ni moteurs, ni endpoints, ni intégrations, ni persistance.

## Ce que les références imposent

Conserver : sidebar compacte, grands espaces analytiques, bandeau de KPI,
tables professionnelles, sparklines sobres, glows locaux, verre noir,
hiérarchie nette et véritable adaptation mobile.

Éviter : néon sur chaque bord, cartes multicolores, donuts décoratifs,
blocs marketing, faux chiffres, navigation colorée comme un signal financier
et terminal desktop simplement compressé sur mobile.

## Signature

La signature unique est **Decision Trace** : une hairline argentée avec quatre
nœuds `Données → Moteur → Décision → Portefeuille`. Elle existe uniquement dans
le hero Aujourd'hui, le drawer Opportunité, le hero Analyse, l'audit de décision
IA et l'impact Portefeuille.

Le **Vertex Beam** est seulement un reflet de matière très discret ; ce n'est
pas une seconde signature et il n'est jamais permanent.

## Palette et distribution

- 82 % obsidienne/graphite : `#050607`, `#090b0e`, `#0e1116`.
- 13 % blanc/argent/gris : `#f5f7fa`, `#c9ced8`, `#b8bec8`, `#7a828f`.
- 5 % signal : positif `#36c889`, risque `#ed655c`, prudence `#dda23b`,
  options `#9c79d0`, analyse/focus exceptionnel `#65d8e8`.

Une couleur lumineuse dominante maximum par carte et deux par écran, hors
vert/rouge directionnels nécessaires. La séparation vient des surfaces, de
l'espace et de hairlines presque invisibles, jamais de cadres lumineux.

## Typographie, géométrie et densité

Geist pour l'interface ; Geist Mono pour tickers, prix, pourcentages, dates et
mesures. Chiffres tabulaires. Titres courts en français, sans longues capitales.

- Grille 4 px ; espaces 8/12/16/20/24/32.
- Sidebar 236 px, repliée 72 px ; topbar 60–64 px.
- Contenu 12 colonnes, max 1600–1680 px.
- Cartes 14–16 px ; contrôles 9–10 px.
- Densité desktop 8/10, variance visuelle 4/10, motion 2/10.

## Navigation canonique

- **Piloter** : Aujourd'hui, Calendrier.
- **Explorer** : Marchés, Opportunités, Analyse, Options, Simulateur.
- **Gérer** : Portefeuille, Suivi, Performance.
- **Intelligence** : Vertex IA.
- **Utilitaire épinglé** : Système.

Recherche globale, état marché, fraîcheur, calendrier, alertes et profil
restent dans la topbar. Journal vit dans Performance ; watchlist dans Suivi ou
Portefeuille ; Design System reste une route interne de QA.

## Composants et graphiques

Une seule famille de cartes, KPI, badges, contrôles, tables, drawers, états et
ChartCard. Chaque widget de données rend visibles question, conclusion, source,
timestamp, fraîcheur et état lorsque ces informations existent.

Le thème graphique peut changer conteneur, axes, grille, labels, tooltip,
légende, interactions visuelles, resize et accessibilité. Séries, valeurs,
calculs, agrégations, sources et timeframes canoniques restent inchangés.

Le Simulateur est une surface analytique multi-actifs. Il compare des scénarios
explicites pour Actions, ETF, Options et Forex avec les moteurs existants ; il
ne promet pas une prévision, n'invente aucun calcul et ne prépare aucun ordre.

## États, accessibilité et responsive

Traiter loading, empty, partial, stale, delayed, offline, demo et error sans
inventer de contenu. Contraste AA, focus visible, clavier, reduced motion et
sens jamais porté par la couleur seule. Concevoir réellement pour 390, 768,
1024, 1280 et 1600+ px ; les tables deviennent priorisées ou inspectables, pas
illisibles.

## Tests de craft

- **Permutation** : Vertex ne doit pas devenir un template générique si le logo
  est remplacé.
- **Distance** : hiérarchie lisible en plissant les yeux.
- **Signature** : Decision Trace seulement aux cinq emplacements.
- **Tokens** : aucune couleur, ombre, rayon ou espacement répété en dur.
- **Vérité** : avant/après utilise les mêmes données et comportements.
