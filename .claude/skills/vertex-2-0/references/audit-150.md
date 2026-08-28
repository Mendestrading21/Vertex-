# Audit final — 150 contrôles Vertex 2.0

Chaque contrôle reçoit `OK + preuve`, `N/A + justification` ou
`Écart + ticket`. Une affirmation, une capture isolée ou une suite verte sans
preuve du contrat ne suffit pas.

## A. Autorité, baseline et périmètre — 001 à 015

001. Le SHA de `main`, HEAD, branche, dirty state, PR et CI sont relevés.
002. Les routes, services, moteurs, jobs, stores et pages touchés sont inventoriés.
003. Les consommateurs statiques, dynamiques, navigateur et persistés sont recensés.
004. Le problème ou état initial est reproduit avec une preuve datée.
005. Les capacités sont classées `RÉEL`, `PARTIEL`, `DÉGRADÉ`, `ABSENT` ou `NON_IMPLÉMENTÉ`.
006. Un seul dossier actif existe sous `.claude/skills` : `vertex-2-0`.
007. `CLAUDE.md` ne route vers aucun alias ou skill historique.
008. Toutes les références relatives du skill maître existent.
009. Les docs historiques ne sont pas traitées comme doctrine active.
010. Le lot définit objectif, non-objectifs, propriétaires, risques et rollback.
011. Une découverte hors périmètre est séparée au lieu d'être corrigée opportunément.
012. Les modifications utilisateur préexistantes sont identifiées et préservées.
013. Aucune capacité n'est déclarée livrée depuis son seul nom ou sa documentation.
014. Le résultat attendu est mesurable avant l'écriture.
015. La PR reste brouillon et aucune fusion/déploiement n'est automatique.

## B. Vie privée, IBKR et sécurité — 016 à 030

016. `READONLY=True` et `ANALYSIS_ONLY=True` sont protégés par tests.
017. Aucun appel d'ordre, paper order, exécution, transfert ou exercice n'existe.
018. Un seul module autorisé importe la bibliothèque IBKR.
019. Le gateway ne retourne jamais l'objet client IBKR brut.
020. L'allowlist IBKR contient uniquement contrats et données de marché.
021. `managedAccounts`, `accountSummary`, `positions`, `portfolio` et `reqPnL` sont impossibles.
022. Aucune route ne renvoie compte, cash, NAV, marge, position ou P&L broker.
023. Le statut connecté provient d'une preuve runtime, jamais du flag de configuration.
024. Une panne IBKR ne crée, ferme ou modifie aucune position déclarée.
025. Les routes personnelles renvoient `private, no-store` et ne passent pas en cache partagé.
026. Un service privé non-loopback refuse de démarrer sans authentification.
027. La démo publique ne lit ni ne persiste de données personnelles.
028. Prompts, logs, traces, captures et fixtures excluent données de compte et secrets.
029. Le partage IA du portefeuille est désactivé par défaut, minimisé et consenti.
030. Scans secrets/PII, dépendances et permissions CI passent sur tout l'arbre suivi.

## C. Portefeuille manuel et contrats de données — 031 à 045

031. Le portefeuille a une seule vérité : la déclaration utilisateur.
032. Comptes internes, cash déclaré, positions, thèses et transactions ont un propriétaire unique.
033. Origine de position et source de prix sont deux champs distincts.
034. `SAISIE`, `MARCHÉ`, `MOTEUR`, `ESTIMATION` et `SIMULATION` restent distinguables.
035. Un rafraîchissement de marché laisse quantité, coût, compte et thèse bit-identiques.
036. `UNKNOWN` n'est jamais converti en zéro, neutre, conforme ou réel.
037. Valeur, unité, devise, source, heure, fraîcheur, qualité et fallback accompagnent les champs critiques.
038. Instrument, place, devise, multiplicateur et contrat ont une identité canonique.
039. Les conversions fraction/pourcentage, par action/par contrat et devise sont explicites.
040. Les migrations de store sont versionnées, idempotentes et testées old→new→rollback.
041. Une sauvegarde vérifiée précède toute migration de données utilisateur.
042. CSV/import reste explicite avec mapping, aperçu, déduplication et confirmation.
043. Positions, trades, idées, signaux, simulations et tracking ne partagent aucun KPI ambigu.
044. Une donnée manquante réduit la couverture au lieu d'être imputée silencieusement.
045. Export, suppression, rétention et restauration du portefeuille sont testés.

## D. Architecture, performance et automatisations — 046 à 060

046. Un propriétaire canonique existe par route, capacité, métrique, composant et job.
047. `terminal.py` ne reçoit aucune nouvelle capacité hors correctif bloquant avant extraction.
048. Les requêtes UI lisent des snapshots bornés et n'appellent aucun fournisseur lent.
049. Les snapshots sont immuables, datés et publiés atomiquement.
050. Timeouts, pacing, circuit breaker, coalescence et retries bornés sont définis.
051. Chaque cache documente clé, scope, TTL, maximum, invalidation et stale behavior.
052. Les états `LIVE`, `DELAYED`, `FROZEN`, `STALE`, `PARTIAL`, `OFFLINE` et `ERROR` sont honnêtes.
053. Chaque job affiché possède un exécuteur et un heartbeat réels ou vaut `NON_IMPLÉMENTÉ`.
054. Jobs et migrations sont idempotents après retry ou redémarrage.
055. Dernière tentative, réussite, durée, prochaine exécution et erreur sont observables.
056. Les threads, sessions, listeners et ressources se ferment proprement.
057. Logs structurés utilisent request/job/source IDs sans données privées.
058. `/healthz`, `/readyz` et la page Système ont des responsabilités distinctes.
059. Latence p50/p95/p99, payload, cache hit et âge des données ont une baseline.
060. Charge, timeout, fournisseur lent, cache stale et mode hors ligne respectent les budgets.

## E. Décision, moteurs et preuves — 061 à 075

061. Une seule API publique produit le `AdviceResult` utilisateur.
062. Aucun autre moteur, route ou composant n'émet un verdict concurrent.
063. Le flux respecte faits→normalisation→calculs→gates→conseil→explication.
064. Chaque conseil porte snapshot ID, versions de moteurs/profil et empreinte d'entrée.
065. Tous les hard gates ont une implémentation fail-closed et des tests négatifs.
066. Une section critique absente plafonne réellement le conseil.
067. Un seul R:R structurel, une seule formule et une seule unité sont utilisés.
068. Aucun score proxy n'est renommé comme fait fondamental ou sentiment réel.
069. Le moteur exécutif reçoit qualité, réconciliation et garde portefeuille complets.
070. Comité, scorecard, Skyler et chemins legacy ont été migrés ou cessent d'être autorités.
071. Opportunités consomme le même `AdviceResult` que l'Analyse.
072. Aucune règle financière, seuil, score ou verdict n'est recalculé en JavaScript.
073. GET est sans effet de bord ; gel, journalisation et écriture utilisent une action explicite.
074. Les conseils sont rejouables de façon déterministe depuis leur snapshot.
075. Toute probabilité affiche calibration hors échantillon, taille, version et incertitude ou reste une estimation.

## F. Options et Simulateur — 076 à 090

076. Un pipeline options unique possède filtre, score, scénario, limites et provenance.
077. Chaîne, contrat, expiration, strike, droit, devise et multiplicateur ont une identité unique.
078. Bid, ask, mark, spread, volume, OI, IV et Greeks gardent unités et timestamp.
079. Données absentes ne sont jamais remplacées par zéro ou une Greek inventée.
080. Fraction/percent IV et prime par action/par contrat ne reposent sur aucune heuristique ambiguë.
081. Term structure, skew, surface et GEX exposent méthode, source et couverture.
082. Les mandats DTE, stratégie, risque et revue ne se contredisent plus.
083. Une stratégie non supportée ou interdite n'est jamais proposée par un moteur legacy.
084. Les trois surfaces de simulation sont consolidées ou clairement non concurrentes.
085. Actions, ETF, Options et Forex conservent leurs paramètres et unités propres.
086. Montant, quantité, effet de levier, multiplicateur et devise sont explicitement distingués.
087. Scénarios A/B/C partagent date, hypothèses et base de comparaison.
088. Payoff, breakeven, pertes, stress et impact portefeuille sont étiquetés théoriques.
089. Une simulation ne modifie le portefeuille qu'après confirmation humaine distincte.
090. Aucun contrôle du simulateur ne ressemble à une transmission d'ordre.

## G. IA, sources et recherche — 091 à 105

091. Tous les appels Claude passent par une gateway unique.
092. Le schéma de sortie, grounding numérique, citations et fallback sont obligatoires.
093. Les contenus externes sont traités comme non fiables et défendus contre prompt injection.
094. Claude n'invente ni prix, Greek, probabilité, score, source ou disponibilité.
095. Claude ne modifie ni gate, verdict, portefeuille, règle active ou job.
096. Les prompts ont budget de taille et manifeste explicite des éléments omis.
097. Rate limit, concurrence, coût, timeout et cancellation sont partagés globalement.
098. Les réponses IA distinguent fait, calcul, estimation et interprétation.
099. Chaque affirmation externe critique conserve une citation consultable et datée.
100. Les publications officielles priment sur éditorial, alerte et interprétation IA.
101. Les alertes TradingView déclenchent une réévaluation, jamais un ordre.
102. News et recherches sont dédupliquées, bornées, sourcées et mises en cache.
103. Aucune collecte IA automatique ne révèle implicitement les holdings.
104. Mémoire et journal ont rétention, consentement et suppression explicites.
105. L'IA reste utilisable en fallback déterministe quand le fournisseur est absent.

## H. Pages, clarté et identité Black Glass — 106 à 120

106. La navigation suit Piloter, Explorer, Gérer, Intelligence et Système.
107. Aujourd'hui, Calendrier, Marchés, Opportunités, Analyse et Options ont des missions distinctes.
108. Simulateur, Portefeuille, Suivi, Performance, Vertex IA et Système ont des missions distinctes.
109. Chaque page répond à une question principale comprise en cinq secondes.
110. Une visualisation ou table dominante structure le premier viewport.
111. PageHeader, ContextBar, DecisionZone, EvidenceZone et WorkZone restent cohérents.
112. Tous les textes utilisateur sont en français clair et les sigles sont expliqués.
113. Black Glass Signal Light utilise obsidienne, graphite, argent et accents sémantiques sobres.
114. Une lumière dominante maximum par carte et deux accents structurels maximum par écran.
115. Aucune bordure néon permanente, arc-en-ciel, esthétique casino ou template SaaS générique.
116. Geist et Geist Mono ont fallbacks, chiffres tabulaires et rendu net HiDPI.
117. Boutons, filtres, champs, badges, tables, drawers et états ont un propriétaire visuel unique.
118. Chaque graphique expose question, source, unité, période, tooltip et fallback tabulaire.
119. Loading, empty, partial, stale, delayed, offline, demo et error sont conçus.
120. Aucun widget décoratif ou KPI redondant ne subsiste sans décision utile.

## I. Accessibilité, navigateur et qualité — 121 à 135

121. Contraste AA, focus visible et sens indépendant de la couleur sont vérifiés.
122. Ordre clavier, skip link, labels, erreurs et restauration du focus fonctionnent.
123. Reduced motion, zoom 200 % et lecteurs d'écran gardent l'information critique.
124. 390, 430, 768, 1024, 1280, 1440 et 1600 px sont testés.
125. Aucun overflow global ; tables et graphiques restent consultables sur mobile.
126. Captures avant/après utilisent route, état, données et viewport identiques.
127. Console navigateur et `/api/client-log` ne contiennent aucune nouvelle erreur.
128. Interactions principales, erreurs réseau et retours clavier sont testés avec Playwright.
129. Canvas/SVG se redimensionne et détruit observers/listeners/instances au démontage.
130. CSS, JS, images, fonts et bibliothèques respectent leurs budgets.
131. Lighthouse ou mesure équivalente ne régresse pas au-delà du budget approuvé.
132. `compileall`, lint/statique ciblé et tests unitaires du lot passent.
133. Les tests de routes, contrats, migrations et no-orders passent.
134. La suite complète passe ou chaque écart préexistant est reproduit et documenté.
135. Les modes sans IBKR, sans Claude, réseau lent, offline et données partielles restent utilisables.

## J. Consolidation, preuves et release — 136 à 150

136. Chaque retrait a une recherche d'imports, routes, scripts, tests, docs et runtime dynamique.
137. Les données persistées, clés navigateur, service worker et backups sont examinés avant retrait.
138. Le propriétaire canonique couvre la capacité de l'ancien chemin.
139. Parité fonctionnelle, données et captures est prouvée avant suppression.
140. Le rollback du lot est documenté et testé quand il touche des données.
141. Aucun fichier n'est supprimé uniquement parce qu'il est ancien, gros ou mal nommé.
142. Les branches distantes ne sont pas supprimées sans inventaire et accord séparé.
143. Les données personnelles de l'arbre courant sont remplacées par fixtures synthétiques.
144. Toute réécriture d'historique Git reçoit une autorisation destructive explicite.
145. Dépendances, skills et actions externes ont licence, version, permissions et retrait documentés.
146. Le diff final ne contient ni secret, artefact généré accidentel ni changement hors lot.
147. `git diff --check`, statut, liste des fichiers et commit candidat sont revus depuis zéro.
148. La PR décrit résultats exacts, risques, limites, métriques, migrations et rollback.
149. Les 150 contrôles sont eux-mêmes continus, uniques et tous renseignés.
150. Une validation humaine du commit candidat précède toute fusion ou release.
