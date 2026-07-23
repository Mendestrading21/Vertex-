# VERTEX V4 — MASTER VISUAL SPEC

## 0. Mission

Refondre intégralement l’interface de Vertex pour que **toutes les pages, tous les graphiques et tous les états** ressemblent à un seul produit premium, cohérent avec la référence visuelle validée.

Cette refonte est **strictement visuelle et ergonomique**.

### Invariants absolus

- Ne jamais modifier les moteurs financiers, calculs, verdicts, scores ou règles métier.
- Ne jamais modifier la logique IBKR, TradingView, Claude, les flux live ou les contrats API.
- Conserver `READONLY=True` et l’interdiction totale de passer des ordres.
- Ne jamais fabriquer de donnée pour remplir un écran.
- Donnée absente = `—`, `n/d`, état vide ou explication honnête.
- Ne jamais écrire un nom personnel en dur dans le code, l’interface ou la documentation.
- Ne pas renommer les routes ou casser les liens existants sans nécessité technique démontrée.
- `main` reste canonique et ne doit pas être modifiée directement.

Branche d’intégration de la refonte :

```text
integration/vertex-v4-clean
```

Décisions figées : `docs/vertex-v4/DECISIONS.md`.

---

## 1. Référence visuelle officielle

La maquette approuvée montre un terminal financier sombre composé de :

- fond noir bleuté très profond ;
- navigation latérale étroite ;
- cartes graphite et verre sombre ;
- accents violet / magenta / corail réservés à la marque et à la sélection ;
- vert réservé aux données positives ;
- rouge réservé aux pertes, risques et baisses ;
- ambre réservé à l’attente, à l’incertitude et aux avertissements ;
- grands graphiques lisibles et prioritaires ;
- tableaux compacts ;
- hiérarchie forte entre panneau principal, cartes analytiques, métriques et inspecteur ;
- déclinaison desktop et mobile cohérente.

La référence maître est versionnée dans le dépôt et doit être ouverte au début de
chaque session visuelle importante :

```text
docs/vertex-v4/reference/00-master-obsidian-prism.jpg
```

Les 23 autres images sont classées dans `docs/vertex-v4/reference/README.md`.
La référence maître est une **direction de design**, pas une source de chiffres ni
de fonctionnalités fictives.

---

## 2. Identité : VERTEX OBSIDIAN PRISM

### 2.1 Intention

Vertex doit ressembler à un terminal d’analyse institutionnel moderne :

- sombre ;
- précis ;
- dense mais respirant ;
- technologique sans apparence gaming ;
- premium sans effets décoratifs permanents ;
- immédiatement compréhensible par un utilisateur qui scanne rapidement les marchés.

### 2.2 Palette cible

Valeurs de départ à centraliser dans `tokens.css`. Claude peut légèrement les ajuster après contrôle de contraste, mais ne doit pas créer de palettes locales par page.

```css
/* Canvas */
--vx-v4-black: #030509;
--vx-v4-obsidian: #050810;
--vx-v4-canvas: #070B12;
--vx-v4-sidebar: #080B13;

/* Surfaces */
--vx-v4-surface-1: rgba(13, 18, 29, 0.88);
--vx-v4-surface-2: rgba(17, 23, 36, 0.92);
--vx-v4-surface-3: rgba(23, 30, 46, 0.94);
--vx-v4-glass: rgba(18, 23, 38, 0.72);
--vx-v4-hover: rgba(38, 45, 64, 0.72);

/* Borders */
--vx-v4-border-faint: rgba(255, 255, 255, 0.045);
--vx-v4-border-soft: rgba(255, 255, 255, 0.075);
--vx-v4-border-default: rgba(255, 255, 255, 0.115);
--vx-v4-border-strong: rgba(255, 255, 255, 0.18);

/* Texte */
--vx-v4-text: #F5F7FB;
--vx-v4-text-2: #BEC5D2;
--vx-v4-text-3: #858E9F;
--vx-v4-text-4: #596273;

/* Marque — jamais utilisée pour signifier gain/perte */
--vx-v4-brand-1: #6D4AFF;
--vx-v4-brand-2: #9A5CFF;
--vx-v4-brand-3: #D86CB7;
--vx-v4-brand-warm: #F08A62;
--vx-v4-brand-soft: rgba(138, 82, 255, 0.15);

/* Sémantique financière */
--vx-v4-positive: #35D28B;
--vx-v4-positive-soft: rgba(53, 210, 139, 0.14);
--vx-v4-negative: #FF625F;
--vx-v4-negative-soft: rgba(255, 98, 95, 0.14);
--vx-v4-warning: #E6A846;
--vx-v4-warning-soft: rgba(230, 168, 70, 0.14);
--vx-v4-option: #A875FF;
--vx-v4-neutral-chart: #7E8798;
--vx-v4-secondary-series: #5F7CFF;
```

### 2.3 Règles de couleur

- Violet / magenta / corail : marque, navigation active, action principale, série principale neutre.
- Vert : uniquement résultat positif, gain, amélioration, validation favorable.
- Rouge : uniquement perte, baisse, risque, blocage ou erreur.
- Ambre : attente, incertitude, donnée retardée ou risque modéré.
- Bleu secondaire : autorisé uniquement comme série de comparaison limitée ; jamais comme identité dominante.
- Une couleur = une signification stable sur toutes les pages.
- Aucun hex de page ne doit contourner les tokens, sauf contraintes de bibliothèque documentées.

---

## 3. Typographie

Combinaison officielle, déjà auto-hébergée dans le dépôt :

```text
Interface : General Sans
Données / nombres : JetBrains Mono
```

Ne pas ajouter de CDN ou de nouvelle famille sans décision explicite.

### Échelle cible

- Titre de page : 25–30 px, 700/750.
- Grand nombre hero : 34–46 px, 700/800, tabular nums.
- Titre de section : 16–19 px, 650/700.
- Titre de carte : 12–14 px, 600/650.
- Corps : 12.5–14 px.
- Métadonnées : 10.5–11.5 px.
- Valeurs financières : toujours `font-variant-numeric: tabular-nums`.

Éviter l’usage systématique des majuscules. Les labels courts peuvent être en uppercase léger ; les titres doivent rester naturels et éditoriaux.

---

## 4. Architecture visuelle globale

### 4.1 Shell desktop

- Sidebar : environ 164–184 px ouverte, 64–72 px repliée.
- Topbar : 54–60 px.
- Contenu maximal : 1680 px.
- Grille : 12 colonnes.
- Espacement principal : 12–16 px.
- Rayon cartes : 10–14 px.
- Rayon contrôles : 7–10 px.
- Bordures fines, jamais de gros contours lumineux.

### 4.2 Quatre niveaux de composants

1. **Hero panel**
   - Message principal, graphique majeur ou décision centrale.
   - Peut utiliser glass, halo ou gradient localisé.
   - Maximum un ou deux par écran.

2. **Analytical panel**
   - Graphique, table, analyse ou comparaison.
   - Surface stable, bordure douce, peu d’effet.

3. **Metric tile**
   - KPI compact, chiffre, delta, sparkline.
   - Très dense et immédiatement scannable.

4. **Inspector panel**
   - Rail droit, drawer ou carte latérale.
   - Verdict, détails, risques, niveaux, actions secondaires.

Toutes les cartes ne doivent pas recevoir le même poids visuel.

### 4.3 Glass

Le verre sombre est réservé à :

- topbar ;
- hero panels ;
- drawers et modals ;
- navigation ou élément sélectionné ;
- quelques zones premium de synthèse.

Ne pas appliquer `backdrop-filter` à toutes les cartes. Le produit doit rester rapide et lisible.

### 4.4 Motion

- 120–220 ms ;
- ease-out ;
- hover : bordure, légère élévation ou variation de surface ;
- active : pression courte ;
- aucune animation continue décorative ;
- respecter `prefers-reduced-motion`.

---

## 5. Navigation

Navigation principale cible :

- Briefing
- Marchés
- Opportunités
- Portefeuille
- Analyse
- Options
- Performance
- Intelligence
- Système

Règles :

- icônes filaires cohérentes ;
- élément actif violet sombre, avec bordure ou liseré discret ;
- labels courts ;
- Système et réglages placés en bas ;
- profil utilisateur générique, jamais de nom codé en dur ;
- recherche globale en topbar ;
- ticker tape optionnel dans la topbar uniquement avec données réelles.

---

## 6. Système de graphiques V4

### 6.1 Contrat commun

Chaque graphique doit partager :

- même typographie ;
- même grille ;
- même tooltip ;
- mêmes contrôles de période ;
- mêmes légendes ;
- mêmes couleurs sémantiques ;
- mêmes marges internes ;
- même footer de source et fraîcheur ;
- même état loading / empty / stale / error ;
- même drawer « Comprendre ce graphique » lorsque pertinent.

### 6.2 Style

- Fond transparent dans la carte.
- Grille très discrète.
- Axes peu contrastés.
- Ligne principale violette ou gradient violet-magenta si neutre.
- Ligne positive verte seulement si la série elle-même signifie un gain.
- Ligne négative rouge seulement si elle signifie une perte.
- Benchmark gris ou bleu secondaire discret.
- Aire sous courbe : opacité faible.
- Tooltip compact, riche et aligné numériquement.
- Crosshair sur les graphiques de prix.
- Candlesticks : vert positif / rouge négatif.
- Volume : couleurs assourdies.

### 6.3 Types à normaliser

- line / area ;
- candlestick + volume ;
- barres positives/négatives ;
- donut d’allocation ;
- treemap ;
- heatmap ;
- radar ;
- gauge ;
- rings ;
- waterfall ;
- option payoff ;
- drawdown ;
- equity vs benchmark ;
- sparklines.

Éviter les graphiques décoratifs. Chaque graphique doit répondre à une question métier.

---

## 7. Direction page par page

### 7.1 Briefing

Objectif : morning command center.

Premier viewport :

- statut du marché ;
- action ou posture prioritaire ;
- pouls du marché ;
- principaux indices ;
- graphique dominant ;
- alertes importantes.

Deuxième niveau :

- top opportunités ;
- exposition portefeuille ;
- calendrier ;
- événements ou risques.

Éviter de montrer tous les modules avec le même poids.

### 7.2 Marchés

- Hero : indice ou régime sélectionné.
- Rangée KPI compacte.
- Grand graphique au centre.
- Rail de marché : indices, breadth, secteurs ou internals.
- Sous-vues cohérentes : Vue d’ensemble, Macro, Secteurs, Breadth, Volatilité.
- Maximum un grand graphique dominant par sous-vue.

### 7.3 Opportunités

- Table premium compacte en vue principale.
- Top 3 mis en avant sans dupliquer toutes les actions.
- Une action principale visible : `Analyser`.
- `Suivre`, `Alerte`, TradingView dans menu secondaire.
- Filtres regroupés dans une seule barre.
- Inspector latéral au clic pour score, R:R, thèse et signaux.

### 7.4 Portefeuille

- Valeur totale, P&L latent, P&L jour, exposition nette en haut.
- Courbe portefeuille vs benchmark dominante.
- Allocation et exposition dans des cartes secondaires.
- Table de positions compacte.
- Rail secteur / concentration / risque.
- La métaphore d’équipe peut rester secondaire, jamais dominer l’architecture.

### 7.5 Analyse

- Header du titre : symbole, nom, cours, variation, marché, badges.
- Grand candlestick ou graphique principal.
- Rail droit sticky : décision, confiance, objectif, stop, R:R.
- Thèse et catalyseurs sous le graphique.
- Sous-vues : Vue d’ensemble, Fondamentaux, Technique, Événements, Options, Portefeuille.
- Ne pas afficher toutes les dimensions dans une longue page unique si elles peuvent être organisées en onglets.

### 7.6 Options

Workspace à trois zones :

- gauche : stratégie, jambes, coût, gain/perte, R:R ;
- centre : payoff et scénarios ;
- droite : Greeks, IV, probabilité, sous-jacent, verdict.

Topbar locale : ticker, échéance, type de stratégie, spot, régime.

Les couleurs options peuvent utiliser le violet ; le payoff positif reste vert et le négatif reste rouge.

### 7.7 Performance

- Courbe d’équité dominante.
- KPIs : rendement, benchmark, alpha, drawdown, win rate, profit factor.
- Séparation visuelle stricte entre signaux théoriques et trades déclarés.
- Drawdown et distributions comme secondaires.
- Journal en table dense et lisible.

### 7.8 Intelligence

- `Ask Vertex` comme expérience centrale.
- Grande zone de question.
- Réponse structurée, sources, preuves et limites.
- Historique récent à droite.
- Comité, Stratégie, Recherche et Mémoire restent des vues avancées.
- L’IA explique ; elle ne remplace jamais le moteur déterministe.

### 7.9 Système

- Statut global clair.
- Connexions et fraîcheur.
- Incidents / erreurs / données dégradées.
- Automatisations et réglages en sous-vues.
- Badge READONLY permanent et discret ; ne pas répéter de grands avertissements sur chaque écran.

### 7.10 Mobile

- Bottom navigation limitée aux espaces majeurs.
- Une colonne.
- KPI en grilles 2 × N.
- Graphiques adaptés à 320–430 px.
- Tables converties en cartes ou scroll horizontal contrôlé.
- Actions principales accessibles au pouce.
- Aucune perte d’information critique.

---

## 8. Architecture CSS cible

Réduire les superpositions actuelles et tendre vers :

```text
vertex/static/vertex/css/
  tokens.css
  base.css
  layout.css
  components.css
  controls.css
  charts.css
  states.css
  responsive.css
  pages/
    briefing.css
    markets.css
    opportunities.css
    portfolio.css
    analysis.css
    options.css
    performance.css
    intelligence.css
    system.css
    tracking.css
```

À terme, absorber ou supprimer les couches contradictoires telles que :

```text
polish.css
control-surface.css
cockpit.css
```

Ne pas les supprimer brutalement. Migrer les règles utiles, vérifier page par page, puis retirer uniquement lorsque les tests et captures prouvent qu’elles sont devenues inutiles.

Les styles inline doivent progressivement devenir des classes réutilisables.

---

## 9. Workflow ChatGPT ↔ Claude Code ↔ utilisateur

### ChatGPT

Responsable de :

- direction artistique ;
- architecture UX ;
- rédaction et mise à jour de la spécification ;
- audit de cohérence ;
- lecture des diffs GitHub ;
- revue des captures ;
- détection des régressions entre pages ;
- rédaction des corrections à transmettre à Claude Code.

ChatGPT ne doit pas modifier simultanément les mêmes fichiers que Claude Code.

### Claude Code

Responsable de :

- audit local détaillé ;
- implémentation ;
- migrations CSS/HTML/JS de présentation ;
- tests ;
- captures desktop/tablette/mobile ;
- commits et push ;
- mise à jour de `docs/vertex-v4/STATUS.md`.

Claude Code ne doit pas improviser une nouvelle direction visuelle sans mettre à jour cette spécification ou demander validation.

### Utilisateur

Responsable de :

- validation des maquettes et lots ;
- décision de fusion ;
- validation ou réorientation de la référence visuelle versionnée ;
- arrêt ou réorientation lorsqu’un lot ne correspond pas au résultat attendu.

---

## 10. Git et collaboration

### Branche

Tous les travaux V4 s’intègrent sur :

```text
integration/vertex-v4-clean
```

Claude Code peut créer des branches temporaires :

```text
claude/v4-01-foundations
claude/v4-02-shell
claude/v4-03-components
...
```

ou travailler directement sur la branche d’intégration avec un commit strictement séparé par lot. Ne jamais travailler directement sur `main`.

### Commits

Format :

```text
feat(v4-foundations): ...
feat(v4-shell): ...
feat(v4-briefing): ...
fix(v4-qa): ...
```

Un lot = un commit principal ou une petite série de commits cohérents.

### Pull request finale

La PR vers `main` ne doit être ouverte qu’après :

- tous les lots approuvés ;
- tests à 100 % ;
- captures de toutes les pages ;
- aucun débordement horizontal ;
- aucune erreur console réelle ;
- invariants READONLY vérifiés ;
- comparaison visuelle finale avec la référence.

---

## 11. Definition of Done de chaque lot

Un lot n’est pas terminé sans :

- code limité au périmètre visuel annoncé ;
- aucune logique métier modifiée ;
- tests existants verts ;
- capture desktop 1536 × 960 ou proche ;
- capture tablette 768 × 1024 ;
- capture mobile 390 × 844 ;
- 0 overflow horizontal ;
- 0 erreur console ;
- loading / empty / stale / error vérifiés ;
- contraste et focus clavier vérifiés ;
- `STATUS.md` mis à jour ;
- commit poussé sur GitHub.

---

## 12. Ordre des lots

0. Baseline et consolidation du dépôt.
1. Tokens et identité V4.
2. Shell global.
3. Composants et contrôles.
4. Système de graphiques.
5. Briefing.
6. Marchés.
7. Opportunités.
8. Portefeuille.
9. Analyse.
10. Options.
11. Performance.
12. Intelligence.
13. Système.
14. Suivis et mobile.
15. Nettoyage des anciennes couches.
16. QA finale toutes pages.
17. PR finale vers `main`, après autorisation explicite.

Ne pas refaire toutes les pages en une seule passe aveugle. Construire les fondations, valider visuellement, puis migrer page par page.

---

## 13. Interdictions

- Aucun ordre broker.
- Aucun chiffre fictif déguisé en réel.
- Aucun gros remplacement automatique sans audit.
- Aucun nouveau framework UI sans justification et validation.
- Aucun CDN supplémentaire non nécessaire.
- Aucun gradient arc-en-ciel.
- Aucun glow permanent sur toutes les cartes.
- Aucun vert de marque pouvant être confondu avec un gain.
- Aucun style local non documenté qui contourne les tokens.
- Aucune suppression massive de fichiers avant validation que leur contenu a été migré.
- Aucune fusion sur `main` sans accord explicite.

---

## 14. Résultat attendu

À la fin, un utilisateur doit pouvoir passer de Briefing à Marchés, Portefeuille, Analyse, Options ou Intelligence et reconnaître immédiatement :

- la même marque ;
- la même profondeur ;
- les mêmes cartes ;
- les mêmes contrôles ;
- le même langage graphique ;
- la même sémantique de couleurs ;
- la même qualité desktop et mobile.

Vertex V4 doit donner l’impression d’avoir été conçu une seule fois, par une seule équipe, autour d’un seul système visuel.
