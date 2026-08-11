# PRODUCT_EXPERIENCE_REVIEW.md — Phase 2.5

> Revue d'expérience produit de Vertex, écrite non comme un développeur mais comme
> un **Head of Product** chez Apple, Linear ou Bloomberg. On ne juge pas le code ;
> on juge ce que **ressent** et ce que **décide** l'utilisateur. Ce document est la
> fondation de toute la refonte visuelle. Branche `agent/vertex-total-rebuild`.

## Vérité produit en une phrase

> **Vertex n'est pas un dashboard de marché. C'est un instrument de décision qui
> doit faire dire à son utilisateur, en dix secondes : « je vois, je comprends,
> je sais quoi faire ensuite. »**

Aujourd'hui Vertex montre *beaucoup*. Un grand produit ne montre pas beaucoup — il
montre **la bonne chose au bon moment**, et cache le reste jusqu'à ce qu'on le
demande. Le péché actuel n'est pas la laideur : c'est la **simultanéité**. Tout
parle en même temps, au même volume.

---

## 1. Workflows utilisateur idéaux

Un investisseur asymétrique ne « consulte » pas un terminal — il y entre avec
**une intention**. Quatre rituels couvrent 95 % de l'usage réel :

**A. Le rituel du matin (2 min, avant l'ouverture).** *« Qu'est-ce qui a changé
pendant que je dormais, et est-ce que ça menace ou sert ma thèse ? »* → **Briefing**
donne le régime, le risque n°1, les 3 catalyseurs du jour, et *une* action
analytique. Fin du rituel : l'utilisateur sait s'il doit agir aujourd'hui ou
observer.

**B. La chasse à l'asymétrie (10 min, hebdo).** *« Où sont les 1-2 opportunités
exceptionnelles cette semaine ? »* → **Opportunités** filtre l'univers en entonnoir
jusqu'à une short-list S+/S, puis **Analyse** ouvre le dossier d'un titre : verdict,
score /40, scénarios pessimiste/probable/exceptionnel, invalidation, catalyseur
90 j. Fin : une thèse écrite ou rejetée, jamais un « peut-être » flou.

**C. La gestion de position (quotidien, 30 s par position).** *« Ma thèse tient-elle
encore ? Dois-je renforcer, tenir, alléger ? »* → **Portefeuille** montre chaque
position avec son état de thèse (intacte / à surveiller / invalidée), sa perte max,
et le palier de gain atteint (+20/+50/+100). Règle d'or produit : **jamais** un
bouton qui renforce une perte ; toujours la distinction invalidation ≠ volatilité
normale.

**D. L'apprentissage (hebdo/mensuel).** *« Mes verdicts tiennent-ils dans le temps ?
Où me trompé-je systématiquement ? »* → **Performance / Journal** mesure le process
réel, pas seulement le P&L. Fin : une règle apprise, ajoutée à la mémoire.

**Ce qui manque aujourd'hui** : ces workflows existent en pièces détachées, mais
**aucune main invisible ne conduit** l'utilisateur de A→B→C→D. Chaque page est une
île. Le grand produit relie les rituels par des **prochaines actions
contextuelles** (« → Ouvrir le dossier », « → Poser une alerte d'invalidation »,
« → Journaliser cette décision »).

---

## 2. Missions réelles de chaque page (une mission, une question)

| Espace | Mission réelle (une phrase) | La seule question à laquelle il répond | À couper |
|---|---|---|---|
| **Briefing** | Orienter la journée en 10 s. | *« Dois-je agir aujourd'hui, et sur quoi ? »* | Tout ce qui duplique Marchés (SPY, rotation, calendrier détaillés). |
| **Marchés** | Situer le régime et où va le capital. | *« Le vent est-il dans le dos ou de face ? »* | 3 vues secteurs sur 4 ; jauges triplées. |
| **Opportunités** | Réduire l'univers à 1-2 asymétries. | *« Qu'est-ce qui mérite un dossier cette semaine ? »* | Tout ce qui n'aide pas à *classer* (charts décoratifs). |
| **Analyse** | Trancher une thèse sur un titre. | *« J'entre, j'attends, ou j'évite — et où j'ai tort ? »* | Le 2ᵉ moteur de chandeliers ; le radar dupliqué. |
| **Portefeuille** | Protéger le capital et gérer les gagnants. | *« Où est mon risque, et qu'est-ce qui a changé ? »* | Treemaps redondants ; couleur PUT/CALL sans sens. |
| **Options** | Juger la convexité et le timing. | *« L'environnement paie-t-il la convexité maintenant ? »* | Greeks avancés hors du 1er écran (niveau expert). |
| **Performance** | Mesurer la méthode, pas l'ego. | *« Mon edge tient-il dans le temps ? »* | Rien de majeur — page saine. |
| **Intelligence** | Expliquer *pourquoi* un verdict. | *« Sur quoi le comité est-il d'accord / en désaccord ? »* | La dispersion en 6 sous-vues ; recentrer sur le raisonnement. |
| **Système** | Prouver que les données sont fiables. | *« Puis-je faire confiance à ce que je vois ? »* | Réglages avancés hors du 1er écran. |

Deux pages ont une **mission diffuse** et doivent être re-cadrées : **Intelligence**
(6 domaines hétérogènes empilés) et **Système** (hub fourre-tout). Une page = une
mission ; le reste passe en niveau expert dépliable.

---

## 3. Informations des 10 premières secondes (la « couche réponse »)

Le manifeste l'exige : à l'ouverture, répondre à *régime · risque · opportunités ·
ce qui a changé · prochaine action*. Décliné par page, le **premier écran** (avant
tout scroll) doit contenir **une seule idée forte + 4 KPI max** :

- **Briefing** → 1 phrase de régime (« RISK-OFF, prudence »), le risque n°1 nommé,
  3 catalyseurs datés, **1 action** (« Surveiller X avant NFP »).
- **Marchés** → régime + confiance (jauge unique), breadth (participation saine ?),
  1 rotation dominante. Pas 19 graphiques.
- **Opportunités** → le **compte** d'idées S+/S trouvées + la meilleure, avec son
  asymétrie. Le reste au scroll.
- **Analyse** → **verdict · score /40 · niveau · confiance · prix · entrée ·
  invalidation** en un bloc « hero », avant le graphique.
- **Options** → stratégie · biais · coût · gain/perte max · breakevens · PoP.
  Gamma/vega/vanna en expert.
- **Portefeuille** → exposition · risque de concentration · P&L latent · **ce qui a
  changé** depuis hier.
- **Performance** → win rate réel · asymétrie moyenne · edge tient-il (oui/non).
- **Système** → **un seul verdict** : « Données fiables / dégradées / démo »,
  vert/ambre.

Aujourd'hui, **aucune page ne hiérarchise ainsi** : la réponse est noyée au milieu
des justifications. C'est le chantier n°1 de la refonte.

---

## 4. Éléments qui génèrent une surcharge cognitive

- **La simultanéité** : Marchés affiche ~19 graphiques d'égale importance visuelle.
  L'œil ne sait pas où se poser. *Un* graphique doit dominer, les autres se
  subordonner.
- **Trois jauges pour la même chose** (régime × plusieurs, breadth × 3) : le cerveau
  croit qu'il y a 3 informations là où il n'y en a qu'une.
- **Les quatre vues secteurs** (bar + heatmap + RRG + treemap) : quatre grammaires
  pour un seul message = charge sans gain.
- **Densité indifférenciée** : titres, KPI, tableaux et graphiques ont le même poids
  typographique → pas de « chemin de lecture ».
- **Le `breadthCard` à une seule barre** : un graphique pour une valeur = friction
  pure (un KPI suffit).
- **Les tableaux qui débordent/scrollent sur mobile** : effort physique pour lire
  une donnée.
- **Le vocabulaire mêlé** : verdicts, scores, niveaux S+/A, confiance, conviction —
  utiles mais non hiérarchisés, l'utilisateur doit *reconstruire* la relation entre
  eux.

Principe Bloomberg mal appliqué : la densité n'est légitime que si elle est
**ordonnée**. Dense ≠ encombré.

---

## 5. Informations répétées

- **Régime de marché** : Briefing **et** Marchés (jauges), parfois deux fois par page.
- **VIX / Breadth** : Briefing + Marchés (jusqu'à 3× dans Marchés).
- **Courbe SPY / marché US** : Briefing (`vx-market-chart`) ≈ Marchés (`vx-mk-spy`).
- **Rotation sectorielle** : Briefing ≈ Marchés (mêmes `scan.sectors`).
- **Calendrier / catalyseurs** : Briefing ≈ Marchés.
- **Radar scorecard** : Analyse ≈ Intelligence (mêmes 5 scores).
- **Funnel de sélection** : Marchés ≈ Opportunités.

Règle produit : **le Briefing résume, il ne duplique pas.** Chaque donnée a **un**
domicile canonique ; ailleurs elle n'apparaît qu'en écho cliquable (« → voir dans
Marchés »).

---

## 6. Décisions qui demandent trop de clics

- **Du signal à la thèse** : repérer une opportunité → ouvrir le dossier → lire
  scénarios → poser une alerte d'invalidation → journaliser. Aujourd'hui ce chemin
  traverse plusieurs pages sans fil conducteur. Cible : **≤ 2 clics** du signal à la
  thèse écrite.
- **De la position au diagnostic** : voir une position → comprendre si la thèse
  tient → agir. La « décision de gestion » existe (`/api/position-decision`) mais
  n'est pas à un clic de la position.
- **Poser une alerte** depuis un niveau de graphique existe (`alertFromLevel`) mais
  n'est pas évident — un « moment magique » enfoui.
- **Comparer deux titres** : dispersé.
- **Retrouver « ce qui a changé »** depuis la dernière visite : pas d'entrée directe
  unique.

Cible produit : les **3 actions les plus fréquentes de chaque page** doivent être
atteignables sans chercher (barre d'action contextuelle, pas menu).

---

## 7. Moments « wow » manquants

- **Le « ce qui a changé depuis ta dernière visite »** : un diff intelligent à
  l'ouverture (nouveau S+, une thèse invalidée, un catalyseur imminent). *C'est* le
  moment Linear.
- **La carte de thèse vivante** : verdict + scénarios + invalidation qui **se met à
  jour** et te dit « ta thèse tient toujours » ou « attention, invalidation
  approchée ».
- **Le payoff options interactif** : glisser le spot/temps et voir la zone de profit
  respirer — pédagogique et tactile (moment TradingView).
- **La preuve d'honnêteté** : un micro-geste où Vertex dit « je ne sais pas » avec
  élégance (donnée absente traitée comme une *qualité*, pas un trou) — différenciateur
  émotionnel unique.
- **Le « brief qui te parle »** : une phrase éditoriale, pas un tableau, à
  l'ouverture (moment Apple : la machine s'adresse à toi).
- **La transition dossier** : cliquer un ticker et voir la fiche se *composer* devant
  toi, pas apparaître d'un coup.

---

## 8. Animations réellement utiles (les seules à garder/créer)

Une animation est légitime **uniquement** si elle communique un changement d'état ou
guide l'attention. À conserver/créer :

- **Apparition de valeur** (une donnée qui se met à jour « pulse » brièvement) — dit
  *« ceci vient de changer »*.
- **Ouverture de dossier / drawer** (slide + fade court) — dit *« tu descends d'un
  niveau »*.
- **Transition d'onglet / sous-vue** (glissement latéral discret) — préserve
  l'orientation spatiale.
- **Chargement progressif / skeleton** — dit *« ça arrive, ce n'est pas cassé »*.
- **Focus clavier** (halo net) — accessibilité.
- **Feedback tactile** (press `scale(.97)`) — le produit répond au doigt.

Durées < 300 ms, courbe ease-out (`felt, not watched`), et **respect strict de
`prefers-reduced-motion`**.

**À bannir** : flottements permanents, halos pulsants décoratifs, cascades longues,
tout mouvement « casino ». Le calme institutionnel est une émotion — le mouvement
gratuit la détruit.

---

## 9. Transitions à créer

- **Espace → espace** : préserver le contexte (le ticker actif « voyage »
  d'Opportunités à Analyse).
- **Ticker → dossier** : composition en cascade *courte* du hero (verdict d'abord,
  puis graphique, puis détails) — hiérarchie rendue *temporelle*.
- **Niveau 1 → niveau expert** : dépliage fluide d'un panneau « Expertise » (méthodo,
  données brutes) sans quitter la page.
- **Vide → rempli** : skeleton → contenu, jamais un saut brutal ni un écran blanc.
- **Frais → périmé** : transition douce du badge de fraîcheur (LIVE → DELAYED →
  STALE) pour signaler la dégradation *sans* alarme.
- **Alerte** : apparition latérale calme (pas de pop agressif).

---

## 10. Émotions que doit transmettre chaque page

| Page | Émotion cible | Anti-émotion à éviter |
|---|---|---|
| **Briefing** | **Clarté** — « je sais quoi faire aujourd'hui » | Anxiété du flux d'infos |
| **Marchés** | **Maîtrise** — « je situe le terrain » | Vertige du bruit |
| **Opportunités** | **Excitation disciplinée** — « il y a peut-être quelque chose ici » | Fièvre du casino |
| **Analyse** | **Conviction lucide** — « je sais pourquoi, et où j'ai tort » | Fausse certitude |
| **Options** | **Précision** — « je paie la bonne convexité » | Complexité intimidante |
| **Portefeuille** | **Sérénité vigilante** — « mon capital est sous contrôle » | Panique / déni |
| **Performance** | **Honnêteté** — « voici la vérité sur ma méthode » | Flatterie de l'ego |
| **Intelligence** | **Confiance** — « je comprends le raisonnement » | Boîte noire |
| **Système** | **Fiabilité** — « je peux faire confiance aux données » | Doute silencieux |

Fil rouge émotionnel : **calme, précis, premium, honnête.** Vertex doit rassurer par
la clarté, jamais exciter par le clignotement.

---

## 11. Composants premium qui manquent

- **La Carte-Verdict** (hero de dossier) : verdict + score /40 + confiance + entrée +
  invalidation, dans un objet unique, dense mais aéré — la signature visuelle du
  produit.
- **La Carte-Scénario** : pessimiste / probable / exceptionnel côte à côte, avec
  risque max et asymétrie, lisible d'un regard.
- **Le Badge de fraîcheur** universel (LIVE / DELAYED / STALE / DEMO / OFFLINE) —
  présent sur *chaque* donnée, cohérent, discret. Le langage visuel de l'honnêteté.
- **L'État vide premium** : quand une donnée manque, une carte élégante qui l'assume
  (« Donnée indisponible — voici pourquoi ») plutôt qu'un trou.
- **La Barre d'action contextuelle** : les 3 gestes de la page, toujours accessibles.
- **Le Diff « depuis ta dernière visite »** : composant d'ouverture.
- **Le Chart-Shell unique** : titre · question · **conclusion** · période · unité ·
  source · fraîcheur · aide · résumé accessible — un cadre commun qui rend *chaque*
  graphique conclusif.
- **La Command Palette** (⌘K) : sauter à un ticker/une page instantanément (moment
  Linear/Raycast).
- **Le Tiroir de Thèse** : la thèse écrite, éditable, reliée à la position.

---

## 12. Graphiques à faire disparaître même s'ils sont techniquement corrects

Un graphique correct mais non-décisionnel est un **coût cognitif net**. À retirer :

- **Le `breadthCard` à une seule barre** (Briefing) : techniquement juste, produit
  inutile → **un KPI**.
- **Les jauges régime/breadth/VIX en doublon** (2ᵉ et 3ᵉ occurrences par page) :
  correctes, redondantes.
- **3 des 4 vues secteurs de Marchés** : chacune correcte, ensemble = surcharge.
  Garder RRG (décisionnel) + heatmap (détail).
- **Le treemap options coloré PUT/CALL** : exact, mais la couleur ne porte aucune
  décision.
- **Le strip de sparklines d'indices** (Briefing) sans conclusion : décoratif.
- **Le `rings` de participation** : répète des chiffres déjà en clair.
- **La galerie `dsc-*`** (design system demo) : données factices, hors produit final.
- **Le radar scorecard dupliqué** (une des deux occurrences Analyse/Intelligence).

Principe : *« Un graphique qui ne change ni la compréhension ni la décision n'a pas
sa place »* — même s'il est parfaitement calculé. La rigueur d'un Head of Product,
c'est de **supprimer du correct**.

---

## Trois principes directeurs pour toute la refonte

1. **Réponse d'abord, preuve ensuite, expertise à la demande.** Chaque page :
   niveau 1 (la réponse en 10 s) → niveau 2 (la justification) → niveau 3
   (l'expertise dépliable). Jamais tout à plat.
2. **Une donnée, un domicile.** Le Briefing résume et pointe ; il ne duplique pas.
   Chaque métrique a une source canonique visible ailleurs seulement en écho.
3. **L'honnêteté est une émotion premium.** « Je ne sais pas » rendu avec élégance
   vaut mieux qu'un chiffre inventé. La fraîcheur et la source sont des composants de
   première classe, pas des mentions légales.

> *Mesure du succès (Head of Product) : l'utilisateur comprend plus vite, décide
> mieux, voit son risque plus clairement, et peut expliquer chaque verdict — sans
> traverser dix écrans contradictoires.*

---

## Lien avec la suite

Ce document est la **fondation produit** des PR de refonte. Il précède et oriente :
- **PR Design n°1** (tokens/typo + chart-shell + composants) → doit livrer la
  Carte-Verdict, la Carte-Scénario, le Badge de fraîcheur, l'État vide premium et le
  Chart-Shell unique décrits en §11.
- **PR navigation & pages** → appliquer §1 (workflows), §2 (missions), §3 (réponse
  10 s), §5 (dé-duplication), et retirer les graphiques de §12.

Aucune décision de ce document n'autorise à inventer une donnée, à contourner
READONLY, ni à ajouter une couche visuelle de plus : il sert à **retrancher et
hiérarchiser**, pas à empiler.
