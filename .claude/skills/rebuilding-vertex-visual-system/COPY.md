# Vertex Copy System

## Sommaire
- Principe
- Ton
- Titres
- Labels
- Verdicts
- Risque
- Scénarios
- États
- Boutons
- Tables
- Aides
- Interdits

## Principe
L’interface doit parler comme un terminal décisionnel, pas comme un rapport, une publicité ou un chatbot. Une phrase visible doit soit orienter, soit qualifier, soit expliquer une limite.

## Ton
- Direct.
- Court.
- Précis.
- Neutre.
- Pas de superlatifs marketing.
- Pas d’anthropomorphisme inutile.
- Pas de formulations vagues.

## Titres
Préférer des noms d’objets ou de décisions :
- `Signal du jour`
- `Top opportunités`
- `Risque portefeuille`
- `Catalyseurs`
- `Asymétrie`
- `Volatilité`
- `Track record`
- `Connexions`

Éviter :
- `Overview of your portfolio`
- `Here is what you need to know`
- `Insights and analysis`
- `Explore more`

## Sous-titres
Maximum une ligne. Expliquer ce que la zone aide à décider.
Exemples :
- `Régime, risque et leadership.`
- `Les dossiers qui méritent ton attention.`
- `Exposition, risque et prochaine décision.`
- `Convexité, volatilité et risque événementiel.`

## Labels KPI
Courts et stables :
`Score Vertex`, `Risque max.`, `Asymétrie`, `Catalyseur`, `IV`, `Delta`, `DTE`, `P&L`, `Exposition`, `Cash`, `Drawdown`.

## Verdicts
Une phrase, sujet + fait + implication.
Exemples :
- `Momentum confirmé, valorisation encore acceptable.`
- `Catalyseur proche, asymétrie favorable mais IV élevée.`
- `Tendance intacte ; invalidation sous 172.`
- `Qualité élevée, timing insuffisant.`

Ne pas écrire `Strong Buy`, `Guaranteed`, `Easy win`.

## Risque
Toujours concret :
- `Risque max. estimé : -14%`
- `Invalidation : clôture sous 172`
- `Risque événementiel : résultats dans 8 jours`
- `Concentration élevée : semi-conducteurs 38%`

## Scénarios
### Pessimiste
`-12% · cassure du support / guidance faible`

### Probable
`+46% · croissance conforme + multiple stable`

### Exceptionnel
`+118% · accélération + révision des estimations`

Les scénarios doivent décrire leurs conditions, pas uniquement des pourcentages.

## Boutons
Utiliser verbes explicites :
- `Analyser`
- `Comparer`
- `Voir options`
- `Créer une alerte`
- `Ajouter au suivi`
- `Exporter`
- `Réessayer`
- `Ouvrir Système`

Éviter : `Go`, `Submit`, `View more`, `Learn more`, `Click here`.

## Filtres
Utiliser l’objet filtré : `Grade`, `Secteur`, `Catalyseur`, `Liquidité`, `Échéance`, `Delta`, `IV`, `Statut`.

## Tables
En-têtes compacts. Unités dans header si homogènes : `Prix ($)`, `IV (%)`, `P&L (%)`.

## Fraîcheur
- `Live`
- `Différé`
- `Périmé`
- `Démo`
- `Hors ligne`
- `Indisponible`

## Empty states
Format : objet absent + raison + action éventuelle.
- `Aucune opportunité S/S+` / `Aucun dossier ne passe les filtres actuels.`
- `Pas de données IV` / `La source actuelle ne fournit pas cette série.`

## Erreurs
Ne pas exposer stack trace ou jargon réseau brut. Traduire en impact :
`Impossible de charger les données de marché.` puis action `Réessayer` ou `Ouvrir Système`.

## Tooltips pédagogiques
Deux phrases maximum. Expliquer la métrique et son usage, pas l’histoire complète de la finance.

## Textes de sécurité
La lecture seule doit être explicite lorsqu’une action pourrait être interprétée comme exécutable. Préférer : `Analyse uniquement — aucun ordre n’est transmis.`

## Interdits
- Promesses de performance.
- Faux degré de certitude.
- `AI powered` comme décoration répétée.
- Paragraphes de 4 lignes dans une carte compacte.
- Répétition du nom de page dans chaque section.
- Mélange FR/EN hors termes financiers usuels.
- Emoji comme ponctuation de produit.
