# VERTEX WIDGET LIBRARY

> **La référence absolue du design de Vertex.** Ce document ne décrit pas des pages.
> Il décrit **l'identité** : une bibliothèque de composants signature à partir
> desquels toutes les pages seront reconstruites. On ne met pas « un graphique dans
> une carte » — on crée **un objet de design que personne d'autre n'a**.
>
> Objectif : qu'une capture d'écran fasse dire « **c'est Vertex** », pas « c'est un
> dashboard de trading ». On construit une identité, pas une interface.
>
> Contraintes permanentes : identité **NEUE EMBER / Neon Glass Orange**
> (`VERTEX_NEUE_EMBER_SYSTEM.md`), Constitution (`VERTEX_CONSTITUTION.md`) suprême.
> **ANALYSIS ONLY. IBKR READONLY. Aucune donnée inventée. Jamais de couleur
> décorative.** Ce document est une spécification de design — aucune page n'est
> modifiée tant que la bibliothèque n'est pas validée.

---

## 0. Pourquoi une bibliothèque, pas des pages

Un dashboard générique = des cartes qui contiennent des graphiques Chart.js
recolorés. On le reconnaît à… rien. Les produits qu'on reconnaît instantanément
(Apple, Stripe, Linear, Arc, TradingView, Bloomberg) n'ont pas de « meilleures
couleurs » : ils ont des **objets** avec une grammaire visible et répétée. La tuile
Météo d'Apple, la pill de statut de Linear, le panneau dense de Bloomberg — chacun
est un composant *signé*.

Vertex doit avoir ses objets signés. Ce ne sont pas des cartes : ce sont des
**widgets Vertex** — chacun répond à **une** question, porte **une** décision, et
se lit **avant** d'être analysé. La page n'est plus qu'une composition de ces objets.

**Règle d'or de cette bibliothèque :** si un widget pourrait exister à l'identique
dans un autre produit, il n'est pas encore un widget Vertex. On le retravaille
jusqu'à ce qu'il porte l'ADN ci-dessous.

---

## 1. L'ADN Vertex — les 8 signatures reconnaissables

Ce qui rend un composant *reconnaissable comme Vertex*. Chaque widget de cette
bibliothèque en porte au moins **quatre**.

### S1 — La colonne Ember (*Ember Spine*)
Un unique fil orange `#FF6D29` traverse chaque widget pour marquer **le point qui
décide** : la valeur active, l'élément sélectionné, le « maintenant » d'une série,
le seuil franchi. **Une seule fois par widget.** L'orange n'est jamais une couleur
de donnée — c'est le regard du produit posé sur *ce qui compte*. C'est le fil rouge
(orange) qui signe Vertex d'un écran à l'autre.

### S2 — Réponse d'abord (*Answer-first*)
La ligne du haut de chaque widget **est** la réponse : un verdict, un état, un
nombre-décision. La preuve (courbe, barres, table) vit **sous** la réponse, jamais
au-dessus. On lit Vertex en 10 secondes parce que la conclusion précède toujours
la donnée (Constitution §5).

### S3 — Verre chaud à profondeur intentionnelle (*Warm Glass*)
Surfaces translucides chaudes (jamais bleues), blur local, **bord intérieur fin**
(`inset 0 1px 0 rgba(255,255,255,.05)`), ombre douce. La profondeur **encode la
priorité** : un widget décisionnel est plus profond qu'un widget de contexte. On
reconnaît la matière Vertex à sa chaleur sombre et à ses arêtes de cuivre.

### S4 — Vérité tabulaire (*Tabular Truth*)
Tout nombre est en `tabular-nums`, mono pour les chiffres denses. **Unité, période,
fraîcheur** sont toujours attachées à la valeur — jamais un nombre nu. La densité
n'est autorisée que lorsqu'elle est **ordonnée** (Constitution §13).

### S5 — Loi sémantique de la couleur (*Color Law*)
Émeraude = gain/sain · corail = perte/risque/invalidation · ambre = attente/seuil ·
violet = options/volatilité · cyan = comparaison technique · **ember = identité,
sélection, point actif**. Gris chaud = neutre/indisponible. **Aucun bleu
identitaire. Aucune couleur décorative.** Une couleur = une signification stable.

### S6 — La machine à états honnête (*Honest States*)
Chaque widget rend **nativement 8 états** — pas des états ajoutés après coup :
`loading → content · empty · insufficient · stale · demo · offline · live`. Vertex
préfère dire « je ne sais pas » (Constitution §9). Un widget sans ses états n'existe
pas dans cette bibliothèque.

### S7 — Micro-mouvement « ressenti, pas regardé » (*Felt Motion*)
Reveal court (skeleton → contenu, 160–240 ms, `cubic-bezier(.23,1,.32,1)`), **pulse
live** bref réservé au direct, **glow du point actif** réservé à la sélection, hover
qui *soulève* de 2 px. Jamais de glow permanent, jamais d'animation décorative.
Respect strict de `prefers-reduced-motion`.

### S8 — Le couple Verdict + Preuve (*Verdict Pairing*)
Aucune visualisation n'est décorative (Constitution §4). Chaque graphe est **collé à
une phrase de conclusion** (« participation saine — hausse partagée », « spread 10a-3m
inversé — signal de récession »). La preuve sans conclusion n'est pas un widget
Vertex : c'est un graphique.

---

## 2. Systèmes partagés (les briques de tous les widgets)

### 2.1 Grammaire de forme
Vertex a un **vocabulaire de formes** réutilisé partout — c'est lui qui crée la
famille visuelle. Chaque widget est bâti à partir de ces primitives, pas de canvas
génériques :

| Forme | Rôle | Signature |
|---|---|---|
| **Spine** | valeur/conviction verticale qui se remplit | fil ember + graduations |
| **Rail** | position sur un axe borné (calme↔stress, défense↔attaque) | piste en verre + marqueur ember |
| **Dial** | métrique bornée semi-circulaire | bandes sémantiques + valeur centrale dominante |
| **Comb** | multi-horizon (1S/1M/1T/1A) en prongs | peigne d'intensité sémantique |
| **Ribbon** | tendance multi-séries fluide | aire dégradée + point actif |
| **Ledge** | nuage qualité×timing avec « corniche » gagnante | quadrant + étiquettes directes |
| **Orbit** | rotation/trajectoire (RRG) avec traînée | comète + queue temporelle |
| **Tide** | flux montant/descendant (avancées/déclins) | ligne de marée + remplissage |
| **Reactor** | composition pondérée (santé du marché) | cœur + barres contributrices |
| **Slab** | verdict/décision monolithique | bloc dense, réponse géante |
| **Runway** | timeline d'événements qui « approchent » | piste en perspective + comptes à rebours |
| **Well** | drawdown/creux (sous l'eau) | puits négatif rempli de corail |
| **Compass** | relations cross-asset (taux/dollar/or…) | rose des vents sémantique |
| **Ladder** | classement (leaders, scores) | échelons à barres d'intensité |
| **Aura** | régime/environnement ambiant | halo radial dont la température code l'état |

### 2.2 Profondeur (3 tiers)
- **Tier 3 — Décision** (hero, verdict, opportunité dominante) : le plus profond,
  halo cuivre discret, bord fort.
- **Tier 2 — Analyse** (graphes, matrices) : profondeur médium, bord cuivre fin.
- **Tier 1 — Contexte** (KPI, chips, rails secondaires) : allégé, quasi-plat.
La profondeur n'est jamais uniforme : elle **hiérarchise**.

### 2.3 Système de mouvement
`--vx-t-fast:140ms · --vx-t:200ms · --vx-t-slow:260ms`, easing `cubic-bezier(.23,1,.32,1)`.
Reveal (opacity+translateY 6px), pulse live (opacity 1↔.55, 1.8 s), glow actif
(2–6 px ember, sélection seulement), hover lift (−2 px + bord renforcé), changement
de période (crossfade 160 ms). `prefers-reduced-motion` → tout `animation:none`.

### 2.4 Machine à états (contrat universel)
Chaque widget implémente ce contrat — c'est ce qui rend Vertex *honnête* et
reconnaissable :

| État | Rendu signature |
|---|---|
| **loading** | skeleton en verre qui *shimmer*, forme du widget préservée (pas un spinner) |
| **content** | le widget plein |
| **empty** | forme réduite + phrase honnête + prochaine action (jamais un grand vide) |
| **insufficient** | « données insuffisantes — Vertex ne tranche pas » + ce qui manque |
| **stale** | badge ambre « périmé » + fraîcheur, données grisées |
| **demo** | badge « DÉMO » orange discret, jamais présenté comme réel |
| **offline** | pastille + dernière valeur connue horodatée |
| **live** | live-dot émeraude + pulse bref (le SEUL glow permanent autorisé) |

### 2.5 Schéma de spécification (répété pour chaque widget)
Chaque widget ci-dessous répond, dans cet ordre, aux questions imposées :

- **Existe pour** · **Question** · **> qu'un graphe classique** · **Forme** ·
  **Hiérarchie** · **Profondeur** · **Couleur** · **Motion** · **Hover** ·
  **Mobile** · **États** · **Données** (source réelle, note d'honnêteté).

---

## 3. Familles & widgets

> Numérotation `Wxx`. Les widgets marqués ★ sont **signature** (fortement détaillés).
> Les variantes `V2/V3` d'un même widget explorent une densité ou une occasion
> différentes — même ADN, forme distincte.

### Famille A — Régime & Environnement
*Question de famille : « Le vent est-il dans le dos ou de face ? »*

#### ★ W01 — Regime Aura (Market Regime V1)
- **Existe pour** : donner l'état de l'environnement *avant* toute donnée, de façon ressentie.
- **Question** : dans quel régime opère la stratégie, et avec quelle confiance ?
- **> classique** : une jauge dit « 62 % » ; l'Aura fait *sentir* le régime — un halo radial dont la **température de couleur** code l'état (émeraude=porteur, corail=défensif, ambre=transition) et dont **l'intensité** code la confiance. On lit l'environnement d'un coup d'œil périphérique.
- **Forme** : `Aura` — disque de verre avec halo radial + nom de régime en grand + confiance en anneau fin périphérique. Aucune roue arc-en-ciel.
- **Hiérarchie** : 1) nom de régime (réponse) · 2) une phrase (« vent dans le dos ») · 3) confiance + dimensions évaluées.
- **Profondeur** : Tier 3 (décision).
- **Couleur** : température du halo = tonalité du régime ; anneau de confiance en ember uniquement au niveau atteint (S1).
- **Motion** : le halo **respire** très lentement (opacity 6 %→10 %, 6 s) — signe de « live » sans clignoter ; reveal à l'apparition.
- **Hover** : révèle les votes de dimensions (breadth/vix/leadership) en tooltip verre.
- **Mobile** : Aura compacte au-dessus, phrase + confiance dessous (empilé).
- **États** : *insufficient* = halo éteint gris + « régime indéterminé, <3 dimensions » (jamais « UNKNOWN 0 % » géant) ; *demo* badge ; *live* respiration active.
- **Données** : `/api/market/regime` (regime, confidence, dimensions_used, adjustments). Absence → indéterminé honnête.

#### W02 — Regime Slab (Market Regime V2)
- **Existe pour** : version dense « cockpit » du régime pour barre supérieure de page.
- **Question** : même question, format compact horizontal.
- **> classique** : bloc `Slab` monolithique — régime + chips de modulation (nouveau risque, priorité setups, confirmations) alignés ; se lit comme une plaque d'instrument, pas une carte.
- **Forme** : `Slab` horizontal, réponse à gauche, chips à droite.
- **Hiérarchie** : régime → modulations → fraîcheur.
- **Profondeur** : Tier 2.
- **Couleur** : tonalité régime sur le mot ; chips à état on/off (émeraude/corail).
- **Motion** : crossfade au changement de régime.
- **Hover** : chip « nouveau risque » explique le blocage.
- **Mobile** : chips passent en 2 lignes.
- **États** : *insufficient* = Slab compact éditorial + signaux réels dispo (VIX/breadth/S&P).
- **Données** : idem W01 + `scan.market_ctx`.

#### W03 — Regime Timeline (Market Regime V3)
- **Existe pour** : montrer que le régime **bascule** dans le temps (transitions).
- **Question** : le régime s'améliore-t-il ou se dégrade-t-il ?
- **> classique** : `Runway` horizontal de segments colorés par régime successif — on voit les bascules, pas un état figé.
- **Forme** : ruban segmenté + marqueur ember sur « maintenant ».
- **Hiérarchie** : segment actuel (ember) → historique → prochain catalyseur macro.
- **Profondeur** : Tier 2.
- **Couleur** : chaque segment = tonalité de son régime ; ember sur le présent.
- **Motion** : le marqueur « maintenant » pulse doucement.
- **Hover** : segment → dates + confiance de la période.
- **Mobile** : ruban scrollable horizontalement (défilement contrôlé).
- **États** : *insufficient* = « historique de régime en constitution ».
- **Données** : historique régime réel s'il existe ; sinon état honnête (aucune interpolation).

#### ★ W04 — Risk-of-Day Verdict
- **Existe pour** : donner le verdict de risque du jour comme une phrase-décision.
- **Question** : le marché autorise-t-il de prendre du risque neuf aujourd'hui ?
- **> classique** : pas un graphe — un **Slab** verbal : « MARCHÉ EN TENDANCE · RISK-OFF · participation 50 % · VIX 12,7 » avec le mot-clé de risque en tonalité sémantique. La décision, pas la data.
- **Forme** : `Slab` texte, verdict en tête, sous-lignes risk-on/off + régime S&P.
- **Hiérarchie** : verdict → roro → régime → fraîcheur.
- **Profondeur** : Tier 3.
- **Couleur** : RISK-OFF corail / RISK-ON émeraude / neutre gris.
- **Motion** : reveal ; changement de verdict = crossfade.
- **Hover** : —(déjà textuel).
- **Mobile** : pleine largeur, lignes empilées.
- **États** : *empty* « verdict non calculé — lancer un scan » + action.
- **Données** : `scan.market_ctx` (verdict, roro, spy_regime). Jamais fabriqué.

#### W05 — Risk-On/Off Rail
- **Existe pour** : positionner l'appétit sur un axe unique et lisible.
- **Question** : risk-on ou risk-off, et à quel point ?
- **> classique** : `Rail` défense↔attaque avec marqueur ember + graduation centrale ; plus lisible qu'une jauge circulaire pour une bipolarité.
- **Forme** : rail en verre horizontal, remplissage sémantique depuis le centre, marqueur ember.
- **Hiérarchie** : mot (RISK-OFF) → rail → écart chiffré.
- **Profondeur** : Tier 1.
- **Couleur** : remplissage émeraude (droite) / corail (gauche).
- **Motion** : le marqueur glisse au changement (200 ms).
- **Hover** : valeur exacte de l'écart.
- **Mobile** : identique, pleine largeur.
- **États** : *empty* « écart risk indisponible ».
- **Données** : `/api/market/summary.roro_gap`.

#### W06 — Regime Confidence Ring
- **Existe pour** : isoler la **confiance** comme métrique bornée autonome.
- **Question** : le signal de régime est-il net ou faible ?
- **> classique** : `Dial`/anneau compact, texte central dominant, lecture sous la valeur (« signal net » / « prudence accrue »).
- **Forme** : anneau fin, valeur centrale, bandes corail/ambre/émeraude.
- **Hiérarchie** : % → lecture → seuils.
- **Profondeur** : Tier 1.
- **Couleur** : bande atteinte en couleur, reste en verre ; aiguille ember.
- **Motion** : l'arc se remplit au reveal.
- **Hover** : rappel des seuils 40/70.
- **Mobile** : réduit à un chip valeur+lecture.
- **États** : *insufficient* = anneau vide + « confiance nulle : <3 dimensions ».
- **Données** : `regime.confidence`.

### Famille B — Momentum & Tendance
*Question de famille : « La poussée est-elle réelle et partagée dans le temps ? »*

#### ★ W07 — Momentum Comb
- **Existe pour** : montrer le momentum **sur plusieurs horizons d'un coup** (1S/1M/1T/1A).
- **Question** : la poussée tient-elle du court au long terme ?
- **> classique** : pas une courbe unique — un **Comb** : 4 prongs verticaux d'intensité sémantique, un par horizon. On voit instantanément si le momentum est cohérent (peigne régulier) ou en retournement (prongs opposés). Signature Vertex reconnaissable.
- **Forme** : peigne de 4 barres (hauteur = |perf|, couleur = signe), labels 1S/1M/1T/1A.
- **Hiérarchie** : forme du peigne (réponse visuelle) → valeurs au survol.
- **Profondeur** : Tier 1 (s'intègre dans cartes ticker/dominante).
- **Couleur** : émeraude (positif) / corail (négatif) par prong.
- **Motion** : les prongs montent en cascade (stagger 40 ms) au reveal.
- **Hover** : prong → valeur exacte + fenêtre.
- **Mobile** : identique, largeur compressée.
- **États** : *empty* = peigne absent, « momentum n/d ».
- **Données** : `perf_w/perf_m/perf_q/perf_y` réels du scan.

#### W08 — Trend Ribbon
- **Existe pour** : la tendance de fond d'une série, fluide et lumineuse.
- **Question** : la tendance reste-t-elle exploitable ?
- **> classique** : `Ribbon` — aire dégradée + ligne + **point actif ember** sur le dernier point, conclusion attachée. Pas une courbe posée dans une boîte : une preuve conclue.
- **Forme** : aire dégradée sémantique, point actif ember, grille faible contraste.
- **Hiérarchie** : conclusion (« tendance intacte ») → ruban → source/période.
- **Profondeur** : Tier 2.
- **Couleur** : ligne ember ou sémantique selon contexte ; fill discret.
- **Motion** : tracé qui se dessine (draw 240 ms) ; point actif pulse si live.
- **Hover** : crosshair + valeur horodatée, tooltip verre.
- **Mobile** : hauteur réduite, labels directs.
- **États** : *empty*/*insufficient* selon longueur de série.
- **Données** : séries `close` réelles du scan (aucune interpolation).

#### W09 — Relative Strength Dial
- **Existe pour** : la force relative vs marché, bornée.
- **Question** : ce titre mène-t-il ou suit-il le marché ?
- **> classique** : `Dial` compact avec zone « leader » (>70) surlignée.
- **Forme** : demi-cadran, valeur centrale, secteur leader en ember.
- **Hiérarchie** : valeur → lecture (« leader » / « à la traîne »).
- **Profondeur** : Tier 1.
- **Couleur** : bande émeraude en tête de plage.
- **Motion** : remplissage au reveal.
- **Hover** : rappel de la base de comparaison.
- **Mobile** : chip.
- **États** : *empty* « force relative n/d ».
- **Données** : `rs` réel.

#### W10 — Streak Widget
- **Existe pour** : matérialiser une série (séances up/down, discipline).
- **Question** : y a-t-il une série en cours qui compte ?
- **> classique** : rangée de pastilles (comme des jours) — lisible instantanément, pas un mini-graphe.
- **Forme** : chapelet de points sémantiques + compteur.
- **Hiérarchie** : compteur (réponse) → chapelet.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude/corail par unité ; ember sur l'unité active.
- **Motion** : la dernière pastille pulse si live.
- **Hover** : date/valeur par pastille.
- **Mobile** : tronqué avec « +N ».
- **États** : *empty* « pas de série ».
- **Données** : séquences réelles ; jamais complétées.

#### W11 — Momentum Heat Bar
- **Existe pour** : une lecture ultra-compacte du momentum en une barre.
- **Question** : chaud ou froid, maintenant ?
- **> classique** : barre unique dont le **remplissage + la teinte** codent l'intensité — se glisse dans une ligne de table sans casser la densité.
- **Forme** : barre horizontale mince, remplissage sémantique.
- **Hiérarchie** : la barre EST la valeur ; nombre optionnel à droite.
- **Profondeur** : Tier 1.
- **Couleur** : gradient corail→gris→émeraude.
- **Motion** : remplissage 160 ms.
- **Hover** : valeur exacte.
- **Mobile** : idem.
- **États** : *empty* barre vide gris.
- **Données** : `mom`/`roc` réels.

### Famille C — Leadership & Rotation
*Question de famille : « Qui mène, qui s'essouffle, où va le capital ? »*

#### ★ W12 — Sector Rotation Orbit (RRG V2)
- **Existe pour** : voir la rotation sectorielle comme une **trajectoire**, pas un instantané.
- **Question** : quels secteurs entrent en leadership, lesquels en sortent ?
- **> classique** : un RRG statique montre des points ; l'**Orbit** ajoute une **queue de comète** (traînée des séances précédentes) → on voit la *direction* du mouvement, pas seulement la position. Le point actif est ember. C'est LA pièce signature de Marchés.
- **Forme** : `Orbit` — quadrants nommés (LEADING/IMPROVING/WEAKENING/LAGGING), points à traînée, étiquettes directes sur les secteurs de tête.
- **Hiérarchie** : conclusion (« Tech migre vers Leading ») → quadrants → points → labels.
- **Profondeur** : Tier 2.
- **Couleur** : point sémantique (force×momentum) ; sélection ember ; traînée en dégradé d'opacité.
- **Motion** : les comètes *avancent* légèrement au reveal (trace) ; sélection glow ember.
- **Hover** : secteur → force, momentum, leader, trajectoire.
- **Mobile** : quadrants conservés, labels réduits aux 4 dominants, pan/zoom tactile.
- **États** : *insufficient* « <2 secteurs — rotation non calculable ».
- **Données** : `scan.sectors` (avg_score, avg_change). Traînée = historique réel si dispo, sinon point simple (jamais inventée).

#### W13 — Leadership Ladder
- **Existe pour** : classer les secteurs meneurs de façon lisible et actionnable.
- **Question** : quel secteur mène, avec quel leader ?
- **> classique** : `Ladder` — échelons à **barres d'intensité** (meneur en ember), leader cliquable par ligne. Hiérarchie par intensité, pas arc-en-ciel.
- **Forme** : liste d'échelons : nom · barre · score · ticker leader.
- **Hiérarchie** : meneur (ember) en haut → dégradé de gris vers le bas.
- **Profondeur** : Tier 1/2.
- **Couleur** : barre ember pour #1, gris chaud ensuite.
- **Motion** : barres se remplissent en cascade.
- **Hover** : ligne → score moyen, nb titres.
- **Mobile** : empilé, tickers en chips.
- **États** : *empty* « secteurs non calculés ».
- **Données** : `scan.sectors`.

#### ★ W14 — Sector Heatmap Premium
- **Existe pour** : la carte de chaleur sectorielle **lisible**, pas un damier saturé.
- **Question** : quels secteurs attirent le capital aujourd'hui ?
- **> classique** : saturation **contrôlée**, texte toujours lisible (ombre), échelle explicite, **conclusion sur les zones dominantes**. Une heatmap qui conclut, pas qui décore.
- **Forme** : grille de cellules à intensité maîtrisée, colonnes (var/score/rvol/n).
- **Hiérarchie** : conclusion (« flux vers Tech ») → grille → échelle.
- **Profondeur** : Tier 2.
- **Couleur** : émeraude (entrée) / corail (sortie), jamais au-delà de ~60 % de saturation.
- **Motion** : cellules apparaissent en vague (stagger).
- **Hover** : cellule → détail + lien opportunités du secteur.
- **Mobile** : lisible à 390 px ; colonnes secondaires masquables.
- **États** : *empty* « secteurs non calculés ».
- **Données** : `scan.sectors`. `—` honnête si champ manquant.

#### W15 — Leaders / Laggards Split
- **Existe pour** : opposer visuellement gagnants et perdants du jour.
- **Question** : qui monte fort, qui chute fort ?
- **> classique** : deux colonnes miroir (Top / Flop) avec tickers ember et % sémantiques — comparaison immédiate.
- **Forme** : split gauche/droite, lignes ticker + % + secteur.
- **Hiérarchie** : titres → % → secteur → score.
- **Profondeur** : Tier 1.
- **Couleur** : % émeraude/corail ; tickers ember.
- **Motion** : reveal en liste.
- **Hover** : ligne → mini-fiche.
- **Mobile** : deux sections empilées.
- **États** : *empty* « aucune variation exploitable ».
- **Données** : `scan.rows` triés (aucune fabrication).

#### W16 — Institution Flow Widget
- **Existe pour** : signaler accumulation / distribution institutionnelle.
- **Question** : les gros acteurs accumulent-ils ou distribuent-ils ?
- **> classique** : `Tide` bipolaire (accumulation vert / distribution corail) + intensité — un flux, pas un histogramme.
- **Forme** : barre de marée centrée, débordant du côté dominant.
- **Hiérarchie** : verdict (accumulation) → intensité → note de fiabilité.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude/corail.
- **Motion** : la marée « pousse » vers le côté dominant.
- **Hover** : mesure + limites (univers partiel).
- **Mobile** : idem.
- **États** : *insufficient* « signal institutionnel non mesuré ».
- **Données** : `accumulation/distribution` réels ; sinon honnête.

### Famille D — Breadth & Participation
*Question de famille : « La hausse est-elle partagée ou étroite ? »*

#### ★ W17 — Breadth Tide
- **Existe pour** : rendre la participation *vivante* (marée montante/descendante).
- **Question** : la participation s'élargit-elle ou se rétrécit-elle ?
- **> classique** : au lieu d'une jauge %, une **ligne de marée** avec niveau d'eau — au-dessus de 55 % « marée haute / hausse partagée », en dessous « marée basse / sélectivité ». Métaphore lisible instantanément.
- **Forme** : `Tide` — surface d'eau animée à hauteur = % >MM50, ligne de flottaison à 55 %.
- **Hiérarchie** : lecture (« participation saine ») → niveau → seuil.
- **Profondeur** : Tier 2.
- **Couleur** : eau émeraude si >55, ambre 45–55, corail <45.
- **Motion** : ondulation lente (2 % d'amplitude) = signe live discret.
- **Hover** : valeur exacte + rappel du seuil.
- **Mobile** : hauteur réduite, lecture conservée.
- **États** : *empty* « participation non calculée » + action scan.
- **Données** : `/api/market/summary.breadth.above50`.

#### W18 — Participation Ring
- **Existe pour** : version bornée compacte de la participation (>MM50/>MM200).
- **Question** : combien de titres au-dessus de leurs moyennes ?
- **> classique** : double anneau concentrique (MM50 externe, MM200 interne) — deux mesures en un objet.
- **Forme** : anneaux, valeurs centrales.
- **Hiérarchie** : MM50 → MM200 → interprétation.
- **Profondeur** : Tier 1.
- **Couleur** : bandes sémantiques.
- **Motion** : remplissage.
- **Hover** : détail avancées/déclins.
- **Mobile** : chips empilés.
- **États** : *empty* honnête.
- **Données** : `breadth.above50/above200`.

#### W19 — Advance/Decline Balance
- **Existe pour** : l'équilibre avancées/déclins et nouveaux hauts/bas.
- **Question** : plus de titres montent-ils que ne descendent ?
- **> classique** : balance bipolaire (fléau) — l'inclinaison code le déséquilibre, plus parlant qu'un ratio.
- **Forme** : fléau de balance + compteurs.
- **Hiérarchie** : côté qui l'emporte → chiffres.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude/corail.
- **Motion** : le fléau s'incline (spring court).
- **Hover** : valeurs exactes.
- **Mobile** : compteurs empilés.
- **États** : *empty* « adv/déc non fournis ».
- **Données** : `breadth.adv/dec/nh/nl` réels.

#### W20 — Breadth Trend Ribbon
- **Existe pour** : la **tendance** de participation multi-séances.
- **Question** : la participation s'améliore-t-elle sur la durée ?
- **> classique** : `Ribbon` multi-séries (>MM50, >MM200, santé) rebasé, conclusion attachée.
- **Forme** : ruban 3 séries, point actif ember.
- **Hiérarchie** : conclusion → ruban → limites (univers partiel).
- **Profondeur** : Tier 2.
- **Couleur** : émeraude/cyan/gris chaud.
- **Motion** : tracé + point actif.
- **Hover** : crosshair daté.
- **Mobile** : hauteur réduite.
- **États** : *insufficient* « historique en constitution ».
- **Données** : `internals.history` réel.

#### ★ W21 — Health Reactor (Composition de santé)
- **Existe pour** : montrer **d'où vient** le score de santé du marché.
- **Question** : le score de santé est-il solide ou creux ?
- **> classique** : au lieu d'un waterfall plat, un **Reactor** — un cœur central (score) alimenté par des **barres contributrices** pondérées (>MM50 30 %, >MM200 25 %, breadth 25 %, adv/déc 20 %). On voit la structure de la santé, pas juste son total.
- **Forme** : cœur + barres radiales/latérales contributrices étiquetées avec leur poids.
- **Hiérarchie** : score central → contributions → pondérations (réelles).
- **Profondeur** : Tier 2.
- **Couleur** : contributions sémantiques ; cœur ember si sain.
- **Motion** : les barres « chargent » le cœur en cascade.
- **Hover** : contribution → valeur × poids.
- **Mobile** : barres empilées sous le cœur.
- **États** : *insufficient* « internals indisponibles ».
- **Données** : `internals` (health, pct_a50/a200, breadth, advpct). Pondérations moteur réelles — **aucune inventée**.

#### W22 — Score Distribution Histogram
- **Existe pour** : la distribution des scores de l'univers scanné.
- **Question** : le marché est-il globalement fort ou faible ?
- **> classique** : histogramme à **intensité** (rouge bas / ambre milieu / vert haut) + conclusion « décalage à droite = univers fort ».
- **Forme** : barres par tranche de score, coins arrondis.
- **Hiérarchie** : conclusion → histogramme.
- **Profondeur** : Tier 2.
- **Couleur** : gradient sémantique par tranche.
- **Motion** : barres montent en cascade.
- **Hover** : tranche → nb titres.
- **Mobile** : lisible, labels alternés.
- **États** : *empty* « distribution indisponible ».
- **Données** : `internals.dist` réel.

### Famille E — Volatilité & Stress
*Question de famille : « L'environnement paie-t-il la convexité, ou menace-t-il ? »*

#### ★ W23 — Stress Thermocline
- **Existe pour** : représenter la volatilité comme une **profondeur** (calme en surface, stress en profondeur).
- **Question** : sommes-nous en eaux calmes ou en zone de stress ?
- **> classique** : au lieu d'une jauge VIX, une **colonne verticale type thermocline** — un curseur descend dans une eau qui vire de l'émeraude (calme, primes bon marché) au corail (stress, expansion). Le VIX devient une *profondeur* intuitive.
- **Forme** : colonne verticale à gradient, curseur ember à la profondeur = VIX.
- **Hiérarchie** : lecture (« volatilité comprimée ») → valeur VIX → variation.
- **Profondeur** : Tier 2.
- **Couleur** : gradient émeraude→ambre→corail du haut vers le bas.
- **Motion** : le curseur descend/monte au changement ; frémissement si live.
- **Hover** : VIX exact, bande, variation vs hier.
- **Mobile** : colonne fine à gauche, lecture à droite.
- **États** : *empty* « VIX non fourni » + action.
- **Données** : `/api/market/summary.vix` (+ vix_chg, vix_band).

#### W24 — VIX Dial
- **Existe pour** : version cadran bornée du VIX (barre supérieure).
- **Question** : niveau de volatilité implicite du marché ?
- **> classique** : `Dial` à bandes (calme <15 / prudence <25 / stress) + lecture.
- **Forme** : demi-cadran, valeur centrale, aiguille ember.
- **Hiérarchie** : valeur → lecture.
- **Profondeur** : Tier 1.
- **Couleur** : bandes sémantiques.
- **Motion** : aiguille glisse.
- **Hover** : bande + variation.
- **Mobile** : chip.
- **États** : *empty* honnête.
- **Données** : `summary.vix`.

#### W25 — Calm↔Stress Rail
- **Existe pour** : positionner le stress sur un axe borné 10→40.
- **Question** : où se situe le marché entre calme et stress ?
- **> classique** : `Rail` gradué (10/25/40+), marqueur ember.
- **Forme** : rail horizontal, remplissage, marqueur.
- **Hiérarchie** : position → échelle.
- **Profondeur** : Tier 1.
- **Couleur** : gradient calme→stress.
- **Motion** : marqueur glisse.
- **Hover** : valeur.
- **Mobile** : pleine largeur.
- **États** : *empty*.
- **Données** : `vix` projeté sur 10–40 (transformation d'affichage, non inventée).

#### W26 — Vol Term Structure
- **Existe pour** : la structure par échéance de la volatilité implicite (contango/backwardation).
- **Question** : la vol court terme est-elle plus chère que la longue ?
- **> classique** : `Ribbon` par échéance avec zone contango/backwardation annotée.
- **Forme** : courbe par maturités réelles, zones interprétées.
- **Hiérarchie** : conclusion (backwardation = stress) → courbe.
- **Profondeur** : Tier 2.
- **Couleur** : ember sur la structure ; zones sémantiques.
- **Motion** : tracé.
- **Hover** : maturité → IV.
- **Mobile** : hauteur réduite.
- **États** : *insufficient* « échéances non fournies » (seulement si données réelles).
- **Données** : term structure réelle par titre (Options) — **affichée uniquement si disponible**, jamais interpolée.

#### W27 — Volatility Regime Badge
- **Existe pour** : étiqueter le régime de vol (expansion/compression).
- **Question** : la volatilité s'étend-elle ou se comprime-t-elle ?
- **> classique** : badge d'état + micro-flèche de direction — pas un graphe pour une info catégorielle.
- **Forme** : pastille d'état + direction.
- **Hiérarchie** : état → direction.
- **Profondeur** : Tier 1.
- **Couleur** : corail (expansion) / cyan (compression).
- **Motion** : flèche pulse.
- **Hover** : définition.
- **Mobile** : chip.
- **États** : *insufficient*.
- **Données** : régime vol réel.

### Famille F — Cross-Asset & Macro
*Question de famille : « Que disent taux, dollar, matières et crypto au risque ? »*

#### ★ W28 — Cross-Asset Compass
- **Existe pour** : lire les relations macro d'un coup (taux/dollar/or/pétrole/BTC).
- **Question** : les cross-assets sont-ils alignés pour le risque ou contre ?
- **> classique** : au lieu de 5 KPI séparés, une **rose des vents** (`Compass`) où chaque actif est une branche dont la longueur = variation et la couleur = impact sur le risque. On voit l'*alignement* macro, pas 5 chiffres isolés.
- **Forme** : `Compass` — branches étiquetées (10Y, DXY, WTI, Or, BTC), longueur+teinte.
- **Hiérarchie** : verdict d'alignement → branches → valeurs.
- **Profondeur** : Tier 2.
- **Couleur** : par impact (dollar fort = corail pour le risque, etc.).
- **Motion** : branches s'étirent au reveal.
- **Hover** : branche → niveau, variation, relation.
- **Mobile** : compass compacte ou repli en liste.
- **États** : *empty* « macro non fournie ».
- **Données** : `scan.macro/indices/commodities`. Chaque actif absent est **omis**, jamais inventé.

#### W29 — Premium Index Card
- **Existe pour** : un indice comme **objet** (monogramme, valeur, aire, plage, état relatif).
- **Question** : où en est cet indice et dans quelle partie de sa plage ?
- **> classique** : pas un KPI + sparkline — un widget à **monogramme** (S&P/NDQ/DJIA/RUT), **mini-aire dégradée + point actif**, **plage de série**, **état relatif** (« près du haut »), accent latéral sémantique. Identité forte, non clonable.
- **Forme** : carte à accent latéral, monogramme, valeur, variation, aire, plage.
- **Hiérarchie** : valeur+variation → aire → plage/état relatif.
- **Profondeur** : Tier 2.
- **Couleur** : accent latéral émeraude/corail ; aire dégradée sémantique.
- **Motion** : aire se dessine ; hover lift.
- **Hover** : point → valeur horodatée.
- **Mobile** : empilé 1 colonne.
- **États** : *empty* « série n/d ».
- **Données** : `indices` (price, change, spark).

#### W30 — Yield Curve Widget
- **Existe pour** : la courbe des taux et son message (normale/inversée).
- **Question** : la courbe est-elle inversée (signal de récession) ?
- **> classique** : `Ribbon` 2 séries (actuelle vs séance préc.) + **conclusion sur le spread 10a-3m** + zone d'inversion annotée. Une courbe qui conclut.
- **Forme** : courbe par maturités réelles, points marqués, zone inversion.
- **Hiérarchie** : conclusion (spread) → courbe → limites (4 maturités réelles).
- **Profondeur** : Tier 2.
- **Couleur** : ember (actuelle) / gris (précédente) ; zone d'inversion corail.
- **Motion** : tracé.
- **Hover** : maturité → rendement.
- **Mobile** : hauteur réduite.
- **États** : *insufficient* « maturités non fournies ».
- **Données** : `scan.macro` (^IRX/^FVX/^TNX/^TYX) — 4 maturités réelles, **non interpolées**.

#### W31 — Macro Asset Card (flat)
- **Existe pour** : un actif macro sans série (taux/DXY) — sans demi-carte vide.
- **Question** : niveau + variation + relation clé ?
- **> classique** : layout **flat plein-largeur** (valeur + variation « ·niveau » + relation en phrase) — jamais de zone morte.
- **Forme** : carte compacte, monogramme, valeur, variation, relation.
- **Hiérarchie** : valeur → variation → relation.
- **Profondeur** : Tier 1.
- **Couleur** : variation neutre pour niveaux (taux/DXY).
- **Motion** : hover lift.
- **Hover** : —.
- **Mobile** : pleine largeur.
- **États** : *empty* « n/d ».
- **Données** : `macro` (value, chg en points).

#### W32 — Commodity Pulse
- **Existe pour** : matières/crypto avec aire vivante.
- **Question** : le baromètre d'inflation/appétit bouge-t-il ?
- **> classique** : carte à **aire dégradée** + relation (« baromètre d'inflation »).
- **Forme** : identique W29 pour matières/crypto.
- **Hiérarchie** : valeur → aire → relation.
- **Profondeur** : Tier 2.
- **Couleur** : aire sémantique.
- **Motion** : aire.
- **Hover** : point daté.
- **Mobile** : empilé.
- **États** : *empty*.
- **Données** : `commodities` (price, change, spark).

### Famille G — Opportunité & Décision
*Question de famille : « Qu'est-ce qui mérite mon attention et mon capital ? »*

#### ★ W33 — Opportunity Dominant Slab
- **Existe pour** : imposer LA meilleure opportunité comme un objet distinct, pas une carte parmi d'autres.
- **Question** : quelle est la meilleure asymétrie disponible, et pourquoi ?
- **> classique** : un **Slab** signature pleine largeur — ticker géant + grade, score, momentum comb, grille de métriques (asymétrie/prob. gain/R:R/edge), catalyseur daté, invalidation, CTA « Ouvrir le dossier ». Rien à voir avec une carte ticker : c'est la pièce maîtresse d'Opportunités.
- **Forme** : bandeau 2 zones (identité | métriques+décision).
- **Hiérarchie** : ticker+grade → score → métriques → catalyseur/invalidation → CTA.
- **Profondeur** : Tier 3 (halo cuivre, bord fort).
- **Couleur** : grade ember (S+/S) ; métriques « chaudes » soulignées en ember ; invalidation corail.
- **Motion** : reveal ; hover CTA glow ember.
- **Hover** : métrique → définition.
- **Mobile** : empilé pleine largeur, métriques 2×2.
- **États** : *empty* « aucune opportunité — attendre est valide » ; *demo* badge.
- **Données** : `scan` (grade, score, vx_asym, vx_pwin, vx_rr, vx_edge, vx_stopfirst) + catalyseur `/cal-feed`. Sans nom de société → secteur/industrie. **Rien inventé.**

#### ★ W34 — Ticker Card (Opportunity Card)
- **Existe pour** : une opportunité secondaire comme objet reconnaissable, non-cloné.
- **Question** : ce titre mérite-t-il une analyse, et sur quel momentum ?
- **> classique** : monogramme + grade + score + **momentum comb** + asym/R:R/prob + catalyseur court + action. Densité variable selon priorité — jamais 6 clones.
- **Forme** : carte compacte, monogramme, grade, comb en pied.
- **Hiérarchie** : ticker/grade → score → asym → momentum → action.
- **Profondeur** : Tier 2.
- **Couleur** : grade ember si S+/S ; comb sémantique.
- **Motion** : hover lift ; comb en cascade.
- **Hover** : mini-fiche.
- **Mobile** : empilé.
- **États** : *empty* rare (liste vide).
- **Données** : `scan.rows`.

#### ★ W35 — Asymmetry Ledge (Op-Scatter V2)
- **Existe pour** : localiser les rares asymétries fortes (qualité×timing).
- **Question** : où sont les meilleurs couples qualité × timing ?
- **> classique** : le nuage devient une **corniche** — le coin haut-droit « À ÉTUDIER » est visuellement une *ledge* surélevée ; les meilleurs points y sont **étiquetés directement** et le meilleur est ember. On voit la corniche gagnante, pas un nuage indistinct.
- **Forme** : `Ledge` — scatter à quadrants nommés, corniche haut-droit accentuée, labels directs top-4.
- **Hiérarchie** : conclusion (« N candidats en zone actionnable ») → corniche → points.
- **Profondeur** : Tier 2.
- **Couleur** : points sémantiques (verdict) ; sélection/meilleur ember ; taille = intensité signal.
- **Motion** : points apparaissent ; sélection glow ember ; hover grossit.
- **Hover** : point → qualité/timing/asym ; clic → panneau + « Ouvrir dossier ».
- **Mobile** : quadrants conservés, labels top-4, tap pour inspecter.
- **États** : *empty* « aucun candidat en zone actionnable ».
- **Données** : `strat_score`, `st_tech/rs`, `anomaly_score`. Aucune fabrication.

#### ★ W36 — Selection Funnel
- **Existe pour** : montrer la discipline de sélection (univers → S+/S) et les déperditions.
- **Question** : que reste-t-il après filtrage, et où le flux se resserre-t-il ?
- **> classique** : trapèzes décroissants réels + **conclusion « plus forte déperdition »** + « entonnoir plat = marché hostile ». Compact (jamais 40 % d'écran). Un entonnoir qui *conclut*.
- **Forme** : trapèzes empilés, % par étage, chips de rôles.
- **Hiérarchie** : étages → conclusion de déperdition → actionnables nommés.
- **Profondeur** : Tier 2.
- **Couleur** : étages en gris chaud → émeraude (actionnables) ; jamais arc-en-ciel.
- **Motion** : étages se remplissent de haut en bas.
- **Hover** : étage → compte + %.
- **Mobile** : compact, largeur bornée.
- **États** : *insufficient* repli si <2 étages (pas de fausse progression).
- **Données** : `/api/opportunities/funnel`.

#### ★ W37 — Comparison Matrix
- **Existe pour** : comparer 2–4 candidats sans radar illisible.
- **Question** : lequel offre le meilleur couple asymétrie × probabilité ?
- **> classique** : matrice à **rails d'intensité** par critère, **meilleur du critère en ember**, colonne tête surlignée. Les barres se comparent d'un coup ; un radar superposé, non.
- **Forme** : table critères × tickers, cellules à rail + valeur.
- **Hiérarchie** : critères en lignes → meilleur par ligne (ember) → tête de shortlist.
- **Profondeur** : Tier 2.
- **Couleur** : rail gris chaud, meilleur en ember ; `n/d` honnête.
- **Motion** : rails se remplissent en cascade.
- **Hover** : cellule → valeur exacte + critère.
- **Mobile** : défilement horizontal contrôlé.
- **États** : *insufficient* si <2 candidats.
- **Données** : `score, vx_asym, vx_pwin, vx_rr, vx_edge, perf_m, vx_tq`. Réels.

#### W38 — Conviction Spine
- **Existe pour** : matérialiser la conviction comme une colonne qui se remplit.
- **Question** : quelle est la force de conviction sur cette idée ?
- **> classique** : `Spine` verticale ember graduée — la conviction *monte*, plus physique qu'un %.
- **Forme** : colonne à remplissage ember + graduations + label.
- **Hiérarchie** : niveau → décomposition (données+probabilité, jamais émotion — §16).
- **Profondeur** : Tier 1.
- **Couleur** : ember (identité de la conviction).
- **Motion** : la colonne se remplit au reveal.
- **Hover** : sources de conviction.
- **Mobile** : horizontale compacte.
- **États** : *insufficient* « conviction non calculable ».
- **Données** : score/edge/pwin combinés (transformation d'affichage, non inventée).

#### W39 — Grade Badge
- **Existe pour** : le niveau (S+/S/A/B) comme sceau reconnaissable.
- **Question** : quel niveau de qualité ?
- **> classique** : sceau ember pour S+/S, neutre bordé pour A/B — un objet, pas un texte.
- **Forme** : pastille grade.
- **Hiérarchie** : le grade EST le contenu.
- **Profondeur** : Tier 1.
- **Couleur** : ember (S+/S) / neutre (A/B) / corail (ÉVITER).
- **Motion** : —.
- **Hover** : seuils du grade.
- **Mobile** : idem.
- **États** : « — » si non noté.
- **Données** : `r.grade` réel.

#### W40 — Score Widget
- **Existe pour** : le score /100 comme nombre-décision dominant.
- **Question** : quel score Vertex ?
- **> classique** : nombre géant tabulaire + unité + micro-décomposition optionnelle. La réponse, pas un gauge.
- **Forme** : nombre + « /100 » + barre fine de sous-scores.
- **Hiérarchie** : nombre → unité → sous-scores.
- **Profondeur** : Tier 1/2.
- **Couleur** : neutre ; sous-scores sémantiques.
- **Motion** : compteur qui monte (respecte reduced-motion → instantané).
- **Hover** : sous-scores fund/tech/mom/risk.
- **Mobile** : idem.
- **États** : *empty* « non noté ».
- **Données** : `score, st_*`.

### Famille H — Catalyseurs & Timeline
*Question de famille : « Qu'est-ce qui peut faire bouger mes dossiers, et quand ? »*

#### ★ W41 — Catalyst Runway
- **Existe pour** : voir les catalyseurs *approcher* dans le temps.
- **Question** : quels événements peuvent changer le régime / mes dossiers ?
- **> classique** : au lieu d'une liste, une **piste en perspective** (`Runway`) où les événements proches sont grands/nets et les lointains petits/estompés, avec comptes à rebours. On *sent* l'imminence.
- **Forme** : `Runway` — axe horizontal en perspective, jalons à J-n, hiérarchisés par importance.
- **Hiérarchie** : événement le plus proche/important → suivants → lointains.
- **Profondeur** : Tier 2.
- **Couleur** : ember (point actif/aujourd'hui), corail (risque/position exposée), ambre (attente).
- **Motion** : jalons « avancent » légèrement au reveal ; aujourd'hui pulse.
- **Hover** : jalon → détail + verdict moteur + « position exposée ».
- **Mobile** : piste verticale scrollable.
- **États** : *empty* « aucun événement identifié ».
- **Données** : `/cal-feed` (macro + earnings dte). Jamais d'événement inventé.

#### W42 — Event Countdown
- **Existe pour** : un compte à rebours d'événement unique (résultats).
- **Question** : dans combien de temps le prochain catalyseur ?
- **> classique** : pastille « J-5 » + verdict moteur — objet, pas ligne de table.
- **Forme** : pastille J-n + label + risque.
- **Hiérarchie** : J-n → événement → exposition.
- **Profondeur** : Tier 1.
- **Couleur** : ambre (proche), corail (position exposée).
- **Motion** : léger pouls à J-1.
- **Hover** : détail.
- **Mobile** : chip.
- **États** : *empty* « aucun catalyseur daté ».
- **Données** : `cal.items` (sym, dte).

#### W43 — Earnings Proximity Bar
- **Existe pour** : signaler la proximité des résultats sur un titre.
- **Question** : suis-je proche d'un événement à risque sur ce titre ?
- **> classique** : rail de proximité (0–60 j) + marqueur — intégrable en ligne.
- **Forme** : `Rail` court + marqueur.
- **Hiérarchie** : proximité → date.
- **Profondeur** : Tier 1.
- **Couleur** : ambre→corail à mesure que J diminue.
- **Motion** : marqueur.
- **Hover** : date exacte.
- **Mobile** : idem.
- **États** : *empty* « pas de résultats datés ».
- **Données** : earnings dte réel.

### Famille I — Analyse & Scénario
*Question de famille : « J'entre, j'attends ou j'évite ? »*

#### ★ W44 — Verdict Slab (Carte-Verdict)
- **Existe pour** : trancher — le cœur de la page Analyse.
- **Question** : entrer, attendre ou éviter ce titre ?
- **> classique** : **Slab** monolithique : Verdict · Score /40 · Niveau · Confiance · Prix · Entrée · Invalidation, réponse géante en tête. La décision comme un instrument, pas une carte.
- **Forme** : bloc dense, verdict géant, plan (entrée/stop) en pied.
- **Hiérarchie** : verdict → score/niveau/confiance → prix/entrée/invalidation.
- **Profondeur** : Tier 3.
- **Couleur** : verdict sémantique (émeraude entrer / ambre attendre / corail éviter).
- **Motion** : reveal ; crossfade au changement de titre (ticker actif voyage).
- **Hover** : chaque champ → source.
- **Mobile** : empilé, verdict pleine largeur.
- **États** : *insufficient* « Vertex ne tranche pas — données insuffisantes » (aucune fausse conviction).
- **Données** : `decision_stack` (verdict, confidence, plan, invalidation).

#### ★ W45 — Scenario Triptych (Carte-Scénario)
- **Existe pour** : montrer les 3 futurs (pessimiste/probable/exceptionnel).
- **Question** : que risque-t-on, qu'attend-on, que peut-on gagner ?
- **> classique** : **triptyque** à 3 volets alignés (risque max | scénario probable | scénario exceptionnel) + asymétrie + catalyseur 90 j. On voit l'asymétrie *spatialement*.
- **Forme** : 3 panneaux, largeur proportionnelle à la probabilité.
- **Hiérarchie** : probable (centre, ember) → extrêmes → asymétrie.
- **Profondeur** : Tier 3.
- **Couleur** : pessimiste corail / probable neutre-ember / exceptionnel émeraude.
- **Motion** : les 3 volets se déploient.
- **Hover** : volet → hypothèses.
- **Mobile** : 3 volets empilés.
- **États** : *insufficient* honnête.
- **Données** : moteur de scénarios réel (risque max, asymétrie, catalyseur).

#### ★ W46 — Trade Plan Chart (chandeliers annotés)
- **Existe pour** : le graphique principal d'Analyse avec plan tracé.
- **Question** : où entrer, où est l'invalidation, quels objectifs ?
- **> classique** : chandeliers LWC + MM + **plan entrée/stop/TP tracé sur le prix** + événements annotés. Le plan *sur* le graphe, pas à côté.
- **Forme** : chandeliers (moteur canonique TradingView Lightweight), lignes de plan, marqueurs d'événements.
- **Hiérarchie** : prix → plan (entrée/stop/TP) → événements → volume secondaire.
- **Profondeur** : Tier 2.
- **Couleur** : entrée ember, stop corail, TP émeraude ; volume discret.
- **Motion** : lignes de plan se dessinent ; point actif.
- **Hover** : crosshair OHLC + niveau de plan.
- **Mobile** : hauteur adaptée, plan conservé.
- **États** : *insufficient* « série insuffisante ».
- **Données** : séries + `plan` réels. Jamais d'indicateur recalculé côté UI.

#### W47 — Factor Bars
- **Existe pour** : décomposer fondamental/technique/momentum/risque.
- **Question** : d'où vient le score ?
- **> classique** : 4 barres sémantiques par dimension (pas arc-en-ciel — une couleur par sens).
- **Forme** : barres étiquetées.
- **Hiérarchie** : dimension → valeur.
- **Profondeur** : Tier 1.
- **Couleur** : fund émeraude, tech cyan, mom ambre, risque corail.
- **Motion** : remplissage cascade.
- **Hover** : valeur.
- **Mobile** : empilé.
- **États** : `n/d` par dimension.
- **Données** : `st_fund/st_tech/st_mom/st_risk`.

#### W48 — Scorecard Radar (unique)
- **Existe pour** : la seule vue radar autorisée — profil multi-facteurs d'UN titre.
- **Question** : quel est le profil d'ensemble du titre ?
- **> classique** : radar **unique** (jamais superposé), axes nommés, remplissage ember discret.
- **Forme** : radar à 5–6 axes.
- **Hiérarchie** : forme globale → axes.
- **Profondeur** : Tier 2.
- **Couleur** : remplissage ember à faible opacité.
- **Motion** : le polygone se déploie.
- **Hover** : axe → valeur.
- **Mobile** : réduit, axes essentiels.
- **États** : *insufficient*.
- **Données** : facteurs réels. **Un seul radar** (règle anti-superposition).

#### W49 — Thesis State Chip
- **Existe pour** : l'état d'une thèse (intacte/surveiller/invalidée).
- **Question** : ma thèse tient-elle encore ?
- **> classique** : chip d'état à sémantique stricte — anti « renforcer la perte » (§18).
- **Forme** : pastille + libellé.
- **Hiérarchie** : état.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude intacte / ambre surveiller / corail invalidée.
- **Motion** : transition d'état = crossfade + micro-shake si invalidée.
- **Hover** : raison.
- **Mobile** : chip.
- **États** : *insufficient*.
- **Données** : état de thèse moteur réel.

### Famille J — Options & Greeks
*Question de famille : « L'environnement paie-t-il la convexité ? »*

#### ★ W50 — Payoff Premium
- **Existe pour** : visualiser le P&L d'un contrat avant d'engager la prime.
- **Question** : que rapporte/coûte ce contrat, et où est le breakeven ?
- **> classique** : zone de perte **corail sombre**, zone favorable **émeraude**, breakeven + spot marqués, coût/perte max/gain max **reliés au graphe**, distinction échéance/avant échéance. Un payoff qui décide.
- **Forme** : courbe de payoff remplie par zones, marqueurs spot/breakeven.
- **Hiérarchie** : conclusion (breakeven, prime) → courbe → coût/perte/gain.
- **Profondeur** : Tier 3.
- **Couleur** : perte corail, gain émeraude, breakeven ember, spot ligne fine.
- **Motion** : courbe se dessine ; curseur spot déplaçable.
- **Hover** : spot → P&L à l'échéance et avant.
- **Mobile** : hauteur réduite, marqueurs conservés.
- **États** : *insufficient* « contrat non simulable ».
- **Données** : `option-payoff` / `scenario_pricer` réels.

#### ★ W51 — Greeks Constellation
- **Existe pour** : lire les Greeks *interprétés*, pas en table brute.
- **Question** : comment ce contrat réagit-il au spot, au temps, à la vol ?
- **> classique** : une **constellation** — delta/gamma/theta/vega en points reliés, chacun avec sa lecture (« theta : −X/j, réévaluer à 5-8 séances »). Les Greeks racontent une histoire, pas une grille.
- **Forme** : petits cadrans/points reliés + lecture par Greek.
- **Hiérarchie** : lecture dominante (le Greek qui pilote) → autres.
- **Profondeur** : Tier 2.
- **Couleur** : violet (options) ; theta corail si coûteux.
- **Motion** : points apparaissent, lignes se tracent.
- **Hover** : Greek → définition + valeur.
- **Mobile** : empilé.
- **États** : *insufficient* « Greeks non disponibles (board legacy : delta seul) ».
- **Données** : `scenario_pricer` (gamma/theta/vega) à la simulation. Honnête sur le board legacy.

#### W52 — Options Environment Gauge
- **Existe pour** : dire si l'environnement paie la convexité.
- **Question** : est-ce le moment d'acheter de l'option longue ?
- **> classique** : `Dial` long-option + biais + régime de vol — verdict d'environnement.
- **Forme** : cadran + badges biais/régime.
- **Hiérarchie** : verdict → biais → régime vol.
- **Profondeur** : Tier 2.
- **Couleur** : violet ; sémantique sur le verdict.
- **Motion** : aiguille.
- **Hover** : composantes.
- **Mobile** : compact.
- **États** : *insufficient*.
- **Données** : moteur options réel.

#### W53 — Theta Decay Widget
- **Existe pour** : montrer le coût du temps.
- **Question** : combien coûte chaque jour d'attente ?
- **> classique** : courbe de décroissance + **time-stop conseillé** annoté.
- **Forme** : `Ribbon` décroissant + marqueur de time-stop.
- **Hiérarchie** : conclusion (« réévaluer à 5-8 séances ») → courbe.
- **Profondeur** : Tier 2.
- **Couleur** : corail (érosion).
- **Motion** : tracé.
- **Hover** : jour → valeur temps.
- **Mobile** : réduit.
- **États** : *insufficient*.
- **Données** : `scenario_pricer`.

#### W54 — Vol Surface
- **Existe pour** : la surface de volatilité (expert, replié).
- **Question** : comment l'IV varie par strike et échéance ?
- **> classique** : surface lisible, jamais décorative ; repliée par défaut (expert).
- **Forme** : heatmap/surface strike×échéance.
- **Hiérarchie** : zones extrêmes → structure.
- **Profondeur** : Tier 2.
- **Couleur** : gradient violet contrôlé.
- **Motion** : reveal.
- **Hover** : cellule → IV.
- **Mobile** : simplifiée en heatmap.
- **États** : *insufficient* si données absentes.
- **Données** : surface réelle uniquement.

#### W55 — Contract Compare Trio
- **Existe pour** : comparer défensif/principal/explosif.
- **Question** : quel contrat domine et pourquoi ?
- **> classique** : trio à **frontière de Pareto** expliquée (« gagne sur delta, perd sur coût ») — pas un simple tableau.
- **Forme** : 3 colonnes + explication de dominance.
- **Hiérarchie** : principal (ember) → alternatives → pourquoi.
- **Profondeur** : Tier 2.
- **Couleur** : ember sur le principal.
- **Motion** : reveal.
- **Hover** : dimension gagnante.
- **Mobile** : empilé.
- **États** : *empty* « aucun contrat comparable ».
- **Données** : board options réel.

### Famille K — Portefeuille & Risque
*Question de famille : « Où est mon risque, et qu'a changé ? »*

#### ★ W56 — Portfolio Health Reactor
- **Existe pour** : l'état de santé global du portefeuille en un objet.
- **Question** : mon portefeuille est-il sain, concentré, exposé ?
- **> classique** : `Reactor` — cœur = santé, barres = exposition/concentration(HHI)/P&L latent/drawdown. On voit la structure du risque.
- **Forme** : cœur + contributions.
- **Hiérarchie** : santé → contributions → ce qui a changé.
- **Profondeur** : Tier 3.
- **Couleur** : contributions sémantiques ; cœur ember si sain.
- **Motion** : chargement du cœur.
- **Hover** : contribution → détail.
- **Mobile** : empilé.
- **États** : *empty* premium sans IBKR (« aucune position — pas de faux chiffres »).
- **Données** : `/api/portfolio/team` (positions explicites). Sans IBKR → vide honnête.

#### ★ W57 — Exposure Treemap
- **Existe pour** : voir la répartition du capital d'un coup.
- **Question** : où mon capital est-il concentré ?
- **> classique** : treemap **unique** (jamais donut ET treemap), cellules à taille = poids, couleur = P&L/rôle, texte lisible. Concentration visible instantanément.
- **Forme** : treemap à cellules étiquetées.
- **Hiérarchie** : conclusion (concentration) → cellules.
- **Profondeur** : Tier 2.
- **Couleur** : P&L émeraude/corail ; sélection ember.
- **Motion** : cellules se déploient.
- **Hover** : cellule → poids, P&L, rôle.
- **Mobile** : treemap simplifiée ou liste.
- **États** : *empty* honnête.
- **Données** : positions réelles.

#### W58 — Concentration HHI Dial
- **Existe pour** : mesurer la concentration (indice HHI).
- **Question** : suis-je trop concentré ?
- **> classique** : `Dial` avec zone d'alerte — borné, lisible.
- **Forme** : cadran + lecture.
- **Hiérarchie** : valeur → alerte.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude→corail.
- **Motion** : aiguille.
- **Hover** : top contributeurs.
- **Mobile** : chip.
- **États** : *empty*.
- **Données** : HHI calculé sur positions réelles.

#### ★ W59 — Position Card
- **Existe pour** : une position comme objet (thèse, perte max, paliers gain).
- **Question** : cette position tient-elle sa thèse, quel est mon risque ?
- **> classique** : carte à **état de thèse** + perte max + paliers de gain (+20/+30/+50…) — surface les règles gagnants, **jamais « renforcer la perte »** (§18-19).
- **Forme** : carte position, thèse en tête, paliers en pied.
- **Hiérarchie** : thèse → perte max → paliers.
- **Profondeur** : Tier 2.
- **Couleur** : thèse sémantique ; paliers émeraude.
- **Motion** : hover lift ; alerte micro-shake si invalidée.
- **Hover** : détail P&L.
- **Mobile** : empilé.
- **États** : *empty* sans position.
- **Données** : position réelle + règles moteur.

#### ★ W60 — What-Changed Diff
- **Existe pour** : montrer ce qui a changé depuis hier (le premier réflexe).
- **Question** : qu'est-ce qui a bougé pendant mon absence ?
- **> classique** : un **flux de deltas** (entrées/sorties/changements de thèse/franchissements) daté — pas un état statique. C'est le widget « bon retour ».
- **Forme** : liste de deltas horodatés, icônes de type.
- **Hiérarchie** : changements majeurs → mineurs.
- **Profondeur** : Tier 2.
- **Couleur** : sémantique par type de changement ; ember sur le plus important.
- **Motion** : deltas entrent en cascade.
- **Hover** : delta → détail.
- **Mobile** : liste.
- **États** : *empty* « rien n'a changé — RAS ».
- **Données** : diff réel du desk/scan.

#### W61 — Risk Alert Widget
- **Existe pour** : hisser un risque prioritaire.
- **Question** : quel est le risque le plus urgent ?
- **> classique** : bandeau d'alerte à sévérité, glow **réservé** aux alertes (S7).
- **Forme** : bandeau + niveau + action.
- **Hiérarchie** : risque → cause → action.
- **Profondeur** : Tier 2.
- **Couleur** : corail (risque) / ambre (surveiller).
- **Motion** : glow bref à l'apparition (autorisé : alerte).
- **Hover** : détail.
- **Mobile** : pleine largeur.
- **États** : *empty* « aucun risque prioritaire ».
- **Données** : risques priorisés réels.

### Famille L — Performance & Edge
*Question de famille : « Mon edge tient-il ? »*

#### ★ W62 — Equity Curve Premium
- **Existe pour** : la courbe d'équité comme preuve d'edge.
- **Question** : ma performance progresse-t-elle réellement ?
- **> classique** : `Ribbon` avec point actif ember + **conclusion (« edge tient : oui/non »)** + jalons de règles. Pas une courbe nue.
- **Forme** : aire d'équité + jalons + point actif.
- **Hiérarchie** : conclusion → courbe → jalons.
- **Profondeur** : Tier 2.
- **Couleur** : ember/émeraude ; drawdowns en creux corail.
- **Motion** : tracé ; point actif.
- **Hover** : date → équité, drawdown.
- **Mobile** : hauteur réduite.
- **États** : *insufficient* « historique insuffisant ».
- **Données** : équité réelle (edge_ledger).

#### ★ W63 — Drawdown Well
- **Existe pour** : montrer les creux « sous l'eau » (protéger le capital §17).
- **Question** : à quel point suis-je descendu, et suis-je encore sous l'eau ?
- **> classique** : `Well` — un puits négatif rempli de corail (underwater plot) ; la profondeur *fait mal* visuellement, ce qui est le but pédagogique.
- **Forme** : aire négative depuis 0, remplie corail.
- **Hiérarchie** : drawdown max/actuel → courbe.
- **Profondeur** : Tier 2.
- **Couleur** : corail (profondeur du creux).
- **Motion** : le puits « se remplit ».
- **Hover** : date → drawdown.
- **Mobile** : réduit.
- **États** : *insufficient*.
- **Données** : drawdown réel.

#### W64 — Return Distribution
- **Existe pour** : la distribution des rendements (asymétrie de l'edge).
- **Question** : mes gains sont-ils asymétriques (peu de grosses pertes) ?
- **> classique** : histogramme à intensité + ligne de moyenne, conclusion d'asymétrie.
- **Forme** : histogramme, ligne moyenne ember.
- **Hiérarchie** : conclusion → distribution.
- **Profondeur** : Tier 2.
- **Couleur** : corail (gauche) / émeraude (droite).
- **Motion** : barres montent.
- **Hover** : tranche → fréquence.
- **Mobile** : lisible.
- **États** : *insufficient*.
- **Données** : rendements réels.

#### W65 — Win-Rate Dial
- **Existe pour** : le taux de réussite réel, borné.
- **Question** : quel est mon win rate réel ?
- **> classique** : `Dial` + contexte (« edge = win rate × asymétrie »).
- **Forme** : cadran + lecture.
- **Hiérarchie** : valeur → contexte.
- **Profondeur** : Tier 1.
- **Couleur** : sémantique.
- **Motion** : aiguille.
- **Hover** : échantillon.
- **Mobile** : chip.
- **États** : *insufficient*.
- **Données** : win rate réel.

#### W66 — Monthly P&L Heatmap
- **Existe pour** : la saisonnalité du P&L (mois × année).
- **Question** : quels mois performent ?
- **> classique** : heatmap calendaire à saturation contrôlée + conclusion.
- **Forme** : grille mois×année.
- **Hiérarchie** : conclusion → grille.
- **Profondeur** : Tier 2.
- **Couleur** : émeraude/corail contrôlés.
- **Motion** : vague.
- **Hover** : mois → P&L.
- **Mobile** : scroll horizontal contrôlé.
- **États** : *insufficient*.
- **Données** : P&L mensuel réel.

#### W67 — Return-by-Verdict Bars
- **Existe pour** : le rendement moyen +20j par verdict moteur.
- **Question** : les verdicts d'achat gagnent-ils vraiment ?
- **> classique** : barres par verdict, conclusion (« ACHETER surperforme »).
- **Forme** : barres étiquetées.
- **Hiérarchie** : conclusion → barres.
- **Profondeur** : Tier 1.
- **Couleur** : sémantique par verdict.
- **Motion** : cascade.
- **Hover** : verdict → moyenne, n.
- **Mobile** : empilé.
- **États** : *insufficient*.
- **Données** : track record réel.

### Famille M — Système & Confiance des données
*Question de famille : « Puis-je faire confiance aux données ? »*

#### ★ W68 — Trust Verdict
- **Existe pour** : un verdict unique de confiance aux données.
- **Question** : les données sont-elles fiables, dégradées ou démo ?
- **> classique** : `Slab` verdict (vert/ambre/corail) + fraîcheur globale — la confiance comme décision, en tête de Système.
- **Forme** : bloc verdict + fraîcheur.
- **Hiérarchie** : verdict → fraîcheur → domaines.
- **Profondeur** : Tier 3.
- **Couleur** : émeraude (fiable) / ambre (dégradé) / corail (démo/hors-ligne).
- **Motion** : reveal.
- **Hover** : composantes.
- **Mobile** : pleine largeur.
- **États** : *offline*/*demo* explicites.
- **Données** : `/api/live/status`, data-quality réels.

#### W69 — Data Quality Donut
- **Existe pour** : la répartition de la qualité des données.
- **Question** : quelle part de mes données est réelle/estimée/démo ?
- **> classique** : donut **sobre** à anneau fin + labels externes + conclusion de concentration. Pas de donut sans message.
- **Forme** : anneau fin + labels.
- **Hiérarchie** : conclusion → répartition.
- **Profondeur** : Tier 2.
- **Couleur** : émeraude/ambre/gris.
- **Motion** : anneau se trace.
- **Hover** : segment → part.
- **Mobile** : compact.
- **États** : *empty*.
- **Données** : `/api/data-quality`.

#### W70 — Connection Status Grid
- **Existe pour** : l'état des connexions (IBKR/TV/IA).
- **Question** : quelles sources sont configurées et actives ?
- **> classique** : grille de pastilles état + impact — objet, pas texte.
- **Forme** : grille de statuts + impact.
- **Hiérarchie** : source → état → impact.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude (ok) / gris (non configuré) / corail (erreur).
- **Motion** : pastille live pulse.
- **Hover** : détail + fraîcheur.
- **Mobile** : liste.
- **États** : *offline* clair.
- **Données** : statut réel des connexions.

#### W71 — Engine Health Strip
- **Existe pour** : l'état des moteurs (scan, décision, options…).
- **Question** : les moteurs tournent-ils correctement ?
- **> classique** : bande de statuts moteur + dernière exécution.
- **Forme** : rangée de pastilles moteur.
- **Hiérarchie** : global → par moteur.
- **Profondeur** : Tier 1.
- **Couleur** : sémantique.
- **Motion** : —.
- **Hover** : moteur → dernier run.
- **Mobile** : liste.
- **États** : *error* par moteur.
- **Données** : santé moteurs réelle.

#### ★ W72 — Live Status Pulse
- **Existe pour** : signer le « direct » — le seul glow permanent autorisé.
- **Question** : les données sont-elles en direct, différées ou figées ?
- **> classique** : pastille + **pulse** émeraude quand live, ambre « différé », gris « figé », badge « démo ». La respiration du produit.
- **Forme** : freshness pill + live-dot.
- **Hiérarchie** : état → âge.
- **Profondeur** : Tier 1.
- **Couleur** : émeraude (live) / ambre (delayed) / gris (frozen) / orange (demo).
- **Motion** : pulse 1.8 s si live (arrêté sinon).
- **Hover** : horodatage exact.
- **Mobile** : idem.
- **États** : *tous* (c'est le widget d'état par excellence).
- **Données** : `updateIndicator` (source, timestamp, mode).

### Famille N — Journal & Discipline
*Question de famille : « Suis-je un investisseur discipliné ? »*

#### ★ W73 — Discipline Meter
- **Existe pour** : mesurer la discipline comportementale (pas la performance).
- **Question** : est-ce que je suis mon process ?
- **> classique** : `Spine`/jauge de discipline + comportements déviants surlignés — un miroir, pas un score de perf.
- **Forme** : colonne discipline + tags de déviation.
- **Hiérarchie** : niveau → déviations récentes.
- **Profondeur** : Tier 2.
- **Couleur** : ember (identité de la discipline) ; déviations corail.
- **Motion** : remplissage.
- **Hover** : déviation → détail.
- **Mobile** : compact.
- **États** : *insufficient* « pas assez d'historique ».
- **Données** : `vxJournal` réel (local + sync).

#### W74 — Hypothesis Card
- **Existe pour** : suivre une hypothèse (validée/en cours/réfutée).
- **Question** : mes hypothèses tiennent-elles ?
- **> classique** : carte hypothèse à état + échéance de revue.
- **Forme** : carte + état + revue due.
- **Hiérarchie** : hypothèse → état → échéance.
- **Profondeur** : Tier 2.
- **Couleur** : émeraude/ambre/corail.
- **Motion** : transition d'état.
- **Hover** : détail.
- **Mobile** : empilé.
- **États** : *empty* « aucune hypothèse ».
- **Données** : journal réel.

#### W75 — Behavior Stats Strip
- **Existe pour** : statistiques comportementales (patience, respect des stops…).
- **Question** : quels sont mes biais récurrents ?
- **> classique** : bande de mini-stats comportementales, chacune conclusive.
- **Forme** : rangée de stats.
- **Hiérarchie** : biais dominant → autres.
- **Profondeur** : Tier 1.
- **Couleur** : sémantique.
- **Motion** : reveal.
- **Hover** : stat → définition.
- **Mobile** : liste.
- **États** : *insufficient*.
- **Données** : journal réel.

#### W76 — Streak Calendar
- **Existe pour** : la régularité (jours suivis, entrées journalisées).
- **Question** : suis-je régulier dans ma discipline ?
- **> classique** : calendrier à pastilles (type contribution graph) sémantique.
- **Forme** : grille calendaire.
- **Hiérarchie** : série en cours → historique.
- **Profondeur** : Tier 1.
- **Couleur** : intensité émeraude ; ember sur aujourd'hui.
- **Motion** : aujourd'hui pulse.
- **Hover** : jour → activité.
- **Mobile** : semaines scrollables.
- **États** : *empty*.
- **Données** : journal réel.

### Famille O — Primitives & Micro-widgets
*Les briques atomiques réutilisées dans tous les widgets ci-dessus. Elles portent
l'ADN à l'échelle micro — c'est leur répétition qui crée la famille visuelle.*

- **W77 — KPI Glass** : label + valeur tabulaire + delta sémantique + micro-spark. La cellule de base.
- **W78 — Delta Chip** : variation ±% ou ±pts, couleur sémantique (neutre pour taux/DXY).
- **W79 — Sparkline+** : ligne + **aire dégradée + point actif ember** (jamais une polyline nue).
- **W80 — Rail** : axe borné en verre + marqueur ember + graduation.
- **W81 — Ring** : métrique bornée compacte, valeur centrale, bande atteinte.
- **W82 — Monogram** : sceau ticker/indice (S&P, NDQ, 10Y) en pastille ember-soft.
- **W83 — Grade Seal** : niveau S+/S/A/B (cf. W39).
- **W84 — Freshness Dot** : pastille live/delayed/frozen/demo (cf. W72).
- **W85 — Section Header** : titre de section léger, filet cuivre, majuscules espacées.
- **W86 — State Block** : conteneur d'état honnête (loading/empty/error/insufficient) à forme préservée.
- **W87 — Glass Tooltip** : infobulle en verre chaud, valeur+unité+fraîcheur, jamais rognée (overflow visible).
- **W88 — Conclusion Line** : la phrase de verdict attachée sous chaque graphe (S8).
- **W89 — Chip Row** : rangée de chips à état on/off (modulations, rôles).
- **W90 — Progress Bar (intensity)** : barre à intensité, pas arc-en-ciel.
- **W91 — Value Big** : nombre-décision géant tabulaire + unité.
- **W92 — Badge Demo** : marqueur « DÉMO » discret, jamais présenté comme réel.
- **W93 — Live Pill** : pastille de direct (variante compacte de W72).
- **W94 — Quadrant Frame** : cadre à quadrants nommés (base de Ledge/Orbit).
- **W95 — Comet Dot** : point à traînée temporelle (base d'Orbit).
- **W96 — Aura Halo** : halo radial à température (base d'Aura).
- **W97 — Reactor Core** : cœur + barres contributrices (base de Reactor/Health).
- **W98 — Runway Axis** : axe en perspective à comptes à rebours (base de Runway).
- **W99 — Tide Surface** : surface d'eau à niveau (base de Tide/Breadth).
- **W100 — Thermocline Column** : colonne verticale à gradient de profondeur (base de Stress).

---

## 4. Index & couverture

**100 widgets** répartis en 15 familles (A→O). ~35 **signature** (★ + primitives de
forme W94–W100) portent une forme *ownable* (Aura, Orbit, Ledge, Tide, Reactor,
Slab, Runway, Well, Compass, Thermocline, Comb, Spine). Les autres composent avec
ces formes et les primitives micro (W77–W93).

Chaque widget répond aux 14 exigences (existe pour · question · > graphe classique ·
lisibilité · beauté · fonctionnement · animation · hover · mobile · hiérarchie ·
profondeur · vide · erreur · live · démo) via le schéma §2.5.

## 5. Test de reconnaissance (le critère final)

Un widget entre dans la bibliothèque seulement s'il passe ces 3 tests :
1. **Test de la capture muette** — sans logo ni texte de marque, reconnaît-on Vertex à la seule forme + matière + couleur ? (colonne Ember, verre chaud, forme signature)
2. **Test du clone** — pourrait-il exister *à l'identique* dans un autre produit ? Si oui → retravailler.
3. **Test de la décision** — porte-t-il une réponse/décision, ou n'est-ce qu'une donnée ? Si donnée seule → ajouter le couple Verdict+Preuve (S8) ou le supprimer (Constitution §4).

## 6. Doctrine de reconstruction des pages

Quand cette bibliothèque est validée, **les pages ne sont plus un assemblage de
cartes** — elles sont un **assemblage de widgets Vertex** :

- **Aujourd'hui** = Regime Aura + Risk-of-Day Verdict + Catalyst Runway + What-Changed Diff + Opportunity Dominant.
- **Marchés** = Regime Aura + Breadth Tide + Sector Rotation Orbit + Sector Heatmap + Cross-Asset Compass + Stress Thermocline + Health Reactor.
- **Opportunités** = Opportunity Dominant Slab + Ticker Cards + Asymmetry Ledge + Selection Funnel + Comparison Matrix.
- **Analyse** = Verdict Slab + Scenario Triptych + Trade Plan Chart + Factor Bars + Scorecard Radar.
- **Portefeuille** = Portfolio Health Reactor + Exposure Treemap + Position Cards + What-Changed Diff + Risk Alert.
- **Options** = Options Environment Gauge + Payoff Premium + Greeks Constellation + Contract Compare Trio.
- **Performance** = Equity Curve Premium + Drawdown Well + Return Distribution + Monthly P&L Heatmap.
- **Système** = Trust Verdict + Data Quality Donut + Connection Status + Engine Health + Live Status Pulse.

Une page = **une mission**, composée de 5–8 widgets signature, jamais un damier de
cartes identiques.

## 7. Feuille de route (après validation de la bibliothèque)

1. **Valider la bibliothèque** (ce document) — direction humaine.
2. **Prototyper les 12 formes signature** (Aura, Orbit, Ledge, Tide, Reactor, Slab,
   Runway, Well, Compass, Thermocline, Comb, Spine) comme composants réutilisables
   (SVG/CSS, sans dépendance réseau nouvelle, états inclus), sur une page de
   démonstration `design_system`.
3. **Reconstruire les pages** espace par espace comme assemblages de widgets, avec
   validation humaine à chaque étape (comme Marchés/Opportunités).
4. **Gardiens** : chaque widget a son test (forme présente, états présents, zéro
   bleu, couple verdict+preuve, ember unique).

## Interdits (rappel)
Pas de graphe standard posé dans une carte · pas de simple recolorisation Chart.js ·
pas de couleur décorative · pas de donnée inventée · pas de glow permanent (hors
live) · pas de bleu identitaire · pas de widget sans ses états · pas de forme clonable.

---

*Cette bibliothèque est la source de vérité du design Vertex. Aucune page ne sera
retravaillée tant qu'elle n'est pas validée. Puis chaque page deviendra un
assemblage de ces objets — pour qu'une capture dise « c'est Vertex », pas « c'est un
dashboard de trading ».*
