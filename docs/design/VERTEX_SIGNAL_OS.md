# Vertex Signal OS — contrat visuel et éditorial

## 1. Mission

Vertex n'est pas un dashboard générique. C'est un cockpit de décision pour repérer peu d'opportunités, comprendre l'asymétrie, protéger le capital et agir seulement lorsque les probabilités deviennent favorables.

L'interface doit permettre de répondre, dans cet ordre :

1. **Quel est le signal ?**
2. **Quelles preuves le soutiennent ?**
3. **Quel est le risque maximal ?**
4. **Quelle action analytique est prioritaire ?**

La profondeur des moteurs ne doit jamais devenir de la complexité visuelle. Une page peut contenir beaucoup de données, mais elle ne doit présenter qu'une décision principale à la fois.

## 2. Ce qui a été retenu des références visuelles

Les références partagent six qualités utiles :

- un fond sombre homogène, sans décor concurrent du contenu ;
- une grille modulaire et compacte ;
- une grande valeur dominante par carte ;
- des contrôles courts sous forme de segments ou de pills ;
- des graphiques sobres, lisibles et faiblement chargés ;
- une navigation stable, identifiable en moins d'une seconde.

Vertex ne copie aucun écran. Il reprend ces principes et les adapte à son propre langage de décision : score, asymétrie, catalyseur, invalidation, allocation, suivi de thèse et options LEAPS.

## 3. Identité : Signal OS

### 3.1 Palette fonctionnelle

Une couleur correspond à une seule fonction :

| Couleur | Signification autorisée |
|---|---|
| Violet Vertex | sélection, interaction, navigation active, action principale |
| Vert | gain, validation, confirmation réelle |
| Rouge | perte, risque, invalidation |
| Jaune | attente, seuil, prudence, donnée à surveiller |
| Cyan | comparaison technique, série secondaire |
| Gris | structure, contexte, donnée neutre ou indisponible |

Le violet ne signifie jamais « achat ». Le vert ne sert jamais de couleur décorative.

### 3.2 Matière

- Canvas quasi noir.
- Cartes mates, légèrement plus claires que le canvas.
- Une bordure fine et neutre, pas de contour lumineux permanent.
- Aucun effet verre lourd sur chaque composant.
- Un halo violet très discret est réservé aux éléments réellement prioritaires : navigation active, carte de décision, bouton principal.
- Les ombres servent uniquement à distinguer un niveau d'élévation.

### 3.3 Typographie

- Inter / Neue Montreal fallback pour l'interface.
- JetBrains Mono pour les nombres, tickers et valeurs tabulaires.
- Titres en casse normale, jamais en capitales systématiques.
- Valeurs majeures : grandes, serrées, tabulaires.
- Métadonnées : petites, contrastées mais lisibles.

### 3.4 Rayons et rythme

- Grille de base : 8 px.
- Carte : 16 à 18 px.
- Contrôle : 9 à 12 px.
- Pill sémantique : 8 à 10 px, pas un arrondi excessif partout.
- Espacement entre cartes : 12 à 16 px.

## 4. Architecture d'une carte

Chaque carte doit choisir un seul rôle.

### Carte Signal

Répond immédiatement à la question principale de la section.

Contenu recommandé :

- libellé court ;
- valeur ou verdict principal ;
- variation / confiance / fraîcheur ;
- action analytique unique.

### Carte Preuve

Explique pourquoi le signal existe.

Contenu recommandé :

- graphique ou tableau ;
- une phrase de conclusion ;
- source et fraîcheur ;
- détail accessible à la demande.

### Carte Action

Présente la prochaine étape : ouvrir le dossier, créer une alerte, comparer, documenter une décision ou surveiller un niveau.

Elle ne doit jamais devenir un chemin d'exécution d'ordre. Vertex reste strictement en lecture seule.

## 5. Grammaire de décision Vertex

Une opportunité prioritaire doit afficher, dès que les données existent :

- ticker et secteur ;
- grade S+ / S / A / B ;
- score Vertex ;
- asymétrie ;
- risque maximal ou invalidation ;
- scénario pessimiste ;
- scénario probable ;
- scénario exceptionnel ;
- catalyseur ;
- confirmation institutionnelle / marché ;
- action analytique recommandée.

### Grades

| Grade | Traitement visuel | Allocation informative de la Constitution |
|---|---|---|
| S+ | Violet plein, priorité maximale | 10–15 % maximum |
| S | Violet doux | 7–10 % |
| A | Vert doux | 3–5 % |
| B | Jaune doux | 1–2 % |

L'allocation reste informative. Aucun composant ne doit laisser croire qu'un ordre est préparé ou exécuté.

### Scénarios

Les trois scénarios sont toujours présentés dans le même ordre :

1. **Pessimiste** — perte maximale / invalidation.
2. **Probable** — rendement central plausible.
3. **Exceptionnel** — convexité possible si les catalyseurs se réalisent.

La comparaison doit être visuelle et immédiate. Une asymétrie médiocre doit être identifiable avant toute lecture détaillée.

## 6. Contrat par espace

### Aujourd'hui

**Question :** quels signaux méritent une action aujourd'hui ?

Ordre :

1. Signal du jour.
2. Régime et risque principal.
3. Top opportunités.
4. Alertes.
5. Calendrier.
6. Portefeuille.

Interdit : recopier toute la page Marchés ou afficher dix KPIs de même importance.

### Marchés

**Question :** le vent est-il favorable, neutre ou hostile ?

Ordre :

1. Régime.
2. Risque principal.
3. Indices / cross-asset.
4. Leadership.
5. Breadth et volatilité.

Les graphiques doivent conclure. Un graphique sans question ni conclusion est un décor, pas un outil.

### Opportunités

**Question :** quels dossiers méritent réellement une analyse ?

Ordre :

1. Opportunité dominante.
2. Shortlist limitée.
3. Comparaison directe.
4. Univers complet.

La dominante doit montrer l'asymétrie, la probabilité de gain, le R:R, le catalyseur et l'invalidation. Le tableau complet vient après, pas avant.

### Analyse

**Question :** cette société mérite-t-elle du capital maintenant ?

Ordre :

1. Verdict et score /40.
2. Scénarios.
3. Thèse et catalyseurs.
4. Fondamentaux.
5. Timing technique.
6. Sentiment / institutionnels.
7. Plan de niveaux.
8. Structure options éventuelle.
9. Compatibilité portefeuille.

Le verdict doit rester visible sans recouvrir le contenu. Les détails avancés peuvent être repliés.

### Portefeuille

**Question :** où le capital est-il exposé et quelle position demande une décision ?

Ordre :

1. Valeur / exposition / P&L.
2. Risque dominant.
3. Position exigeant une attention.
4. Concentration et corrélations.
5. État des thèses.
6. Performance.

La page ne doit pas être un inventaire. Les gagnants, perdants, invalidations et catalyseurs doivent être hiérarchisés.

### Options

**Question :** où se trouve la meilleure convexité et à quel coût ?

Ordre :

1. Verdict de structure.
2. Delta, DTE, spread, open interest.
3. IV / IV rank.
4. Payoff et scénarios.
5. Risque événementiel.
6. Greeks interprétés.
7. Comparaison des contrats.

Profil LEAPS de référence : delta 0,70–0,90, échéance 6–18 mois, liquidité élevée et spread faible.

### Journal

**Question :** la qualité des décisions s'améliore-t-elle ?

Afficher :

- respect du plan ;
- pertes évitées ;
- gagnants laissés courir ;
- erreurs de timing ;
- décisions sous émotion ;
- résultats par grade et par setup.

Éviter les métriques de vanité et les scores sans explication.

### Système

**Question :** les données et moteurs sont-ils fiables maintenant ?

Afficher en premier :

- état global ;
- IBKR ;
- fraîcheur ;
- erreurs ;
- jobs ;
- sauvegarde / synchronisation.

Les détails techniques restent accessibles mais ne dominent pas la première vue.

## 7. Micro-copy

### Règles

- Une phrase = une idée.
- Un titre de carte idéal contient deux à quatre mots.
- Pas de jargon lorsque le mot courant suffit.
- Le libellé décrit la décision, pas l'implémentation technique.
- Une action utilise un verbe : Analyser, Comparer, Surveiller, Documenter, Ouvrir.
- « n/d » ou « — » lorsque l'information manque. Jamais de formulation qui masque l'absence de données.

### Exemples canoniques

| Ancien libellé | Signal OS |
|---|---|
| Brief Vertex | Signal du jour |
| Depuis ta dernière visite | Ce qui a changé |
| Meilleures opportunités | Top opportunités |
| Alertes prioritaires | Alertes |
| Dans quel environnement la stratégie opère-t-elle ? | Régime, risque et leadership. |
| Quelles opportunités méritent réellement une analyse ? | Les dossiers qui méritent ton attention. |
| Où mon capital est-il réellement exposé… | Exposition, risque et prochaine décision. |
| Où est la meilleure convexité… | Convexité, volatilité et risque événementiel. |

## 8. Icônes

- SVG inline, style monoline, `stroke-width` proche de 1,7.
- Taille navigation : 18 px.
- Taille action : 16 px.
- Taille mobile : 20 px.
- Pas d'emoji comme langage d'interface principal.
- Une icône garde toujours la même signification.
- Les icônes seules ont un `aria-label` et un `title` lorsque nécessaire.

## 9. Graphiques

### Principes

- Une question par graphique.
- Une série principale, une comparaison au maximum sauf nécessité analytique.
- Légende proche des données.
- Axe, unité, source et fraîcheur visibles.
- Vert et rouge uniquement pour un sens financier réel.
- Estimations, projections et zones de modèle distinguées par trame ou opacité.
- Valeur dominante marquée sans saturer toute la surface.

### Interdit

- dégradé décoratif sans signification ;
- glow permanent ;
- trois graphiques montrant la même donnée ;
- animation qui retarde la lecture ;
- couleur seule comme unique moyen d'information.

## 10. Responsive

### Desktop

- Sidebar persistante.
- Grille 12 colonnes.
- Densité élevée mais lisible.

### Tablette

- Colonnes secondaires repliées sous la principale.
- Actions de page sur une seconde ligne.

### Mobile

- Une colonne.
- Navigation basse limitée aux espaces prioritaires.
- Contrôles tactiles d'au moins 40 px lorsqu'ils sont essentiels.
- Titres et breadcrumbs tronqués proprement.
- Tables converties en cartes lorsque la lecture horizontale devient pénible.

## 11. Implémentation

Fichiers canoniques de cette migration :

- `vertex/static/vertex/css/signal-os.css` — couche visuelle finale ;
- `vertex/static/vertex/js/signal-os.js` — normalisation de micro-copy et attributs sémantiques ;
- `vertex/static/vertex/js/live-updates.js` — charge Signal OS après les styles historiques ;
- `tests/test_signal_os_contract.py` — gardiens de présence, couverture et sécurité.

Cette couche est une étape de migration. Lorsqu'un espace est réécrit nativement, ses règles doivent être déplacées vers les composants canoniques, sans dupliquer la palette ou les principes.

## 12. Critères d'acceptation

Une modification UI est acceptable uniquement si :

- les huit espaces utilisent la même navigation, les mêmes cartes et les mêmes contrôles ;
- le signal principal est identifiable en moins de cinq secondes ;
- les gains, risques, attentes et options respectent la sémantique couleur ;
- aucune donnée n'est inventée ;
- aucune fonction d'exécution d'ordre n'est introduite ;
- les états live, delayed, stale, demo, offline et missing restent explicites ;
- le rendu reste utilisable à 390 px ;
- le clavier et les lecteurs d'écran conservent un chemin complet ;
- les tests passent ;
- le navigateur réel ne remonte aucune erreur dans `/api/client-log`.
