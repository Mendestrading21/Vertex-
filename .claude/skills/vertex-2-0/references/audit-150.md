# Audit final — 150 contrôles Vertex 2.0

Chaque contrôle reçoit `OK + preuve`, `N/A + justification` ou `Écart + ticket`. Une case sans preuve n'est pas validée. L'audit porte sur la refonte visuelle ; il ne donne aucun droit de modifier le backend.

## A. Périmètre, sécurité et vérité — 001 à 015

001. Le diff ne modifie aucun moteur, formule, score, gate, stratégie ou verdict.
002. Le diff ne modifie aucun provider, endpoint financier, worker, job ou intégration.
003. Le diff ne modifie aucun store, schéma métier, desk sync ou donnée utilisateur.
004. `READONLY`, `ANALYSIS_ONLY` et IBKR readonly restent vrais.
005. Aucun bouton, libellé ou raccourci ne prépare ou transmet un ordre.
006. Aucun calcul financier nouveau n'existe dans template, CSS ou JavaScript visuel.
007. Aucune donnée fictive n'est affichée comme réelle.
008. `—`, `n.d.` et états manquants sont employés honnêtement.
009. Live, delayed, stale, demo, offline et missing restent distinguables.
010. Source, timestamp et fraîcheur survivent à la recomposition visuelle.
011. Positions, signaux, idées, simulations et trades réels restent séparés.
012. Les scénarios ne sont jamais présentés comme des prédictions certaines.
013. Aucun secret, identifiant compte ou payload sensible n'apparaît dans l'UI/log.
014. Les textes externes rendus conservent leur sanitization.
015. Les limites non vérifiées sont déclarées dans la PR.

## B. Architecture de l'information — 016 à 030

016. La sidebar suit Piloter/Explorer/Gérer/Intelligence/Système.
017. Aujourd'hui est la destination initiale claire.
018. Calendrier est global sans dupliquer ses propriétaires spécialisés.
019. Marchés, Opportunités, Analyse, Options et Simulateur sont distincts.
020. Portefeuille, Suivi et Performance ont des responsabilités distinctes.
021. Vertex IA n'absorbe pas les pages métier.
022. Système reste utilitaire et épinglé.
023. Journal appartient à Performance.
024. Watchlist appartient à Suivi/Portefeuille.
025. Design System reste interne à la QA.
026. Chaque route secondaire conserve breadcrumb, origine et retour.
027. Drawer est utilisé pour comparer/scanner ; page pour profondeur/historique.
028. La recherche globale retrouve ticker, page et fonction existante.
029. Les libellés de navigation sont français, courts et non ambigus.
030. Aucune fonction existante ne devient introuvable après déplacement.

## C. Hiérarchie et clarté page — 031 à 045

031. Chaque page formule sa question métier.
032. Le point focal est compris en cinq secondes.
033. Le premier viewport répond à situation, attention, raison et risque.
034. Une seule visualisation ou table domine la page.
035. Les KPI secondaires ne rivalisent pas tous au même niveau.
036. PageHeader expose périmètre et fraîcheur.
037. ContextBar expose période, univers, filtres et source.
038. DecisionZone contient le point focal réel.
039. EvidenceZone explique sans répéter.
040. WorkZone porte la tâche principale.
041. DepthZone contient méthode, historique et détails.
042. Les actions sûres sont proches de leur objet.
043. Les explications longues sont progressives, pas dans le premier écran.
044. Les états vides donnent cause et prochaine action sûre.
045. Le test de distance confirme une hiérarchie nette.

## D. Composants, tables et widgets — 046 à 060

046. Chaque primitive a un propriétaire visuel unique.
047. Tokens, pas de valeurs répétées en dur.
048. Une famille unique de cartes et MetricCard est utilisée.
049. Boutons, tabs, filtres, champs, badges et drawers sont cohérents.
050. Les tables utilisent chiffres tabulaires et alignement numérique.
051. Unités et devises sont visibles dans colonnes ou valeurs.
052. Headers et colonnes clés sticky fonctionnent sans recouvrement.
053. Tri, filtre et recherche annoncent leur état.
054. Densité compacte/confortable ne masque aucune donnée critique.
055. Drawer de ligne conserve contexte et focus.
056. Loading, empty, partial, stale, delayed, offline, demo et error existent.
057. ValueFlash est court, tonal et désactivé en reduced motion.
058. DataLedger expose couverture et données absentes.
059. Aucun widget décoratif ne survit sans question utile.
060. Le registre page → widget correspond au catalogue canonique.

## E. Graphiques et visualisation — 061 à 075

061. Chaque graphique formule question, conclusion, source, unité et période.
062. Les séries, valeurs, agrégations et timeframes sont inchangés.
063. Les axes ne trompent pas et le zéro apparaît quand nécessaire.
064. Les gaps ne sont pas reliés silencieusement.
065. Une hausse n'est pas automatiquement colorée comme positive.
066. Argent, gris, vert, rouge, ambre, violet et cyan respectent leur sémantique.
067. Tooltip, légende et formatters sont centralisés.
068. ResizeObserver ne crée ni boucle ni débordement.
069. Instances, listeners et observers sont détruits au démontage.
070. Canvas/SVG reste net en HiDPI.
071. Un tableau équivalent existe pour toute visualisation critique.
072. Le résumé accessible annonce les valeurs clés.
073. Une bibliothèque externe possède licence et attribution documentées.
074. Les plugins proof-of-concept sont durcis avant production.
075. Le fallback fonctionne quand Canvas/WebGL/JS échoue.

## F. Options et Simulateur — 076 à 090

076. La chaîne garde CALL/strike/PUT et ATM neutre.
077. Bid, ask, mid, spread, volume, OI, IV et Greeks absents restent absents.
078. Multiplicateur, coût par contrat et coût total ne sont pas confondus.
079. Le drawer contrat expose mark, source, heure, qualité et limites.
080. Term structure et smile/skew ont table et unités.
081. OI/GEX montrent zéro et provenance des niveaux.
082. Payoff étiquette date, hypothèses, breakevens et nature théorique.
083. Vol surface possède une alternative 2D accessible.
084. Le Simulateur accepte seulement les classes réellement supportées.
085. Montant et quantité sont explicitement distingués.
086. Action, ETF, Option et Forex gardent leurs unités spécifiques.
087. Chaque valeur est marquée Marché/Portefeuille/Moteur/Saisie.
088. Scénarios A/B/C utilisent la même base de date et devise.
089. Aucune sauvegarde n'apparaît sans store canonique.
090. Aucun libellé du Simulateur ne ressemble à une action d'ordre.

## G. Portefeuille, suivi et performance — 091 à 105

091. Valeur, cash, exposition et P&L précisent leur disponibilité.
092. Réconciliation et fraîcheur IBKR sont visibles.
093. Positions et options ont des tables distinctes.
094. Allocation indique niveau, total et catégorie Autres.
095. Treemap possède labels prioritaires et table fallback.
096. Contribution positive/négative utilise base commune.
097. Corrélation indique période, échantillon et données manquantes.
098. Concentration et limites viennent d'un calcul existant.
099. Impact simulé est séparé du portefeuille réel.
100. Suivi conserve statut workflow et verdict financier séparés.
101. Performance sépare toutes les populations.
102. Equity et drawdown utilisent la même période.
103. Benchmark, échantillon et limites sont visibles.
104. Heatmap mensuelle affiche chiffres et légende numérique.
105. Journal conserve sync, backups et liens aux dossiers.

## H. Identité visuelle et français — 106 à 120

106. Black Glass domine sans devenir gris opaque.
107. La distribution 82/13/5 est respectée approximativement.
108. Une lumière dominante maximum existe par carte.
109. Deux accents maximum structurent un écran hors rouge/vert directionnels.
110. Aucune bordure néon permanente n'encadre les cartes.
111. Les niveaux de surface et l'espace assurent la séparation.
112. Geist et Geist Mono sont chargées avec fallbacks corrects.
113. Prix, dates, tickers et mesures utilisent tabular nums.
114. Les titres français sont courts et naturels.
115. Le jargon anglais inutile a été remplacé.
116. Les sigles financiers conservés ont une aide contextuelle.
117. Decision Trace apparaît seulement aux cinq emplacements canoniques.
118. Vertex Beam reste un reflet de matière discret.
119. Le test de permutation confirme une identité non générique.
120. Le test des tokens ne trouve pas de mini-design-system de page.

## I. Accessibilité, responsive et performance — 121 à 135

121. Contraste AA est vérifié pour textes et contrôles.
122. Focus visible n'est jamais masqué.
123. Ordre clavier suit l'ordre visuel.
124. Skip link atteint le contenu principal.
125. Modales/drawers piègent puis restaurent le focus.
126. Labels, erreurs et aides sont reliés aux champs.
127. Le sens ne dépend jamais de la couleur seule.
128. Reduced motion supprime transitions non essentielles.
129. Zoom 200 % conserve contenu et actions.
130. 390 et 430 px sont réellement utilisables.
131. 768 et 1024 px ont une composition dédiée.
132. 1280, 1440, 1600 et écran large gardent une ligne de lecture saine.
133. Aucun overflow horizontal global n'est présent.
134. Tables et graphiques conservent accès aux données sur mobile.
135. Le budget performance et le poids des bibliothèques sont respectés.

## J. Runtime, tests et livraison — 136 à 150

136. Captures avant/après utilisent mêmes données, route, viewport et état.
137. Console navigateur ne contient aucune erreur applicative.
138. `/api/client-log` reste sans erreur liée au lot.
139. `/healthz` reste conforme.
140. Compileall passe.
141. Suite pytest ciblée passe.
142. Suite no-orders passe.
143. Les tests des routes et contrats JS passent.
144. Les modes live/delayed/stale/demo/offline/missing sont vérifiés.
145. Le service worker est bumpé si le contrat l'exige.
146. Les caches servent bien les nouveaux actifs visuels.
147. Aucun consommateur legacy actif n'est supprimé sans preuve.
148. Le rollback est documenté et réalisable.
149. La PR reste brouillon avec risques, limites et preuves.
150. Une validation humaine du commit candidat précède toute fusion/release.
