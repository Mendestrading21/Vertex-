# Vertex — Renforcement de l’intelligence 1.2

## Objectif de l’itération

Cette itération déplace des contrôles critiques **en amont** du moteur Skyler. Les décisions continuent d’être exclusivement analytiques et en lecture seule : aucun ordre, aucune connexion de courtage transactionnelle et aucune action d’exécution ne sont ajoutés.

## Preuves de données produites pendant le scan

Chaque cycle construit désormais un `AnalyticsPacket` par titre depuis la série réellement téléchargée. Le paquet conserve la provenance, l’horodatage et la fraîcheur du spot et de l’historique. La chaîne d’options ne devient disponible pour la décision que si son horodatage est explicitement publié par la boucle options. Une chaîne présente mais non datée reste `MISSING` ; elle ne peut pas autoriser une décision.

La boucle du board options publie maintenant `options_as_of` à chaque mise à jour, ce qui permet au scan suivant de rapprocher le spot et la chaîne et de produire un rapport de réconciliation par symbole.

> Le système ne transforme jamais la simple présence d’un board ou d’un cache en preuve de fraîcheur.

## Régime et macro

Le `MarketContext` canonique utilise maintenant les mesures réellement calculées par le scan : la courbe 10 ans–3 mois, exprimée en points de base, et le dollar (`DX-Y.NYB`) avec variation. Une courbe inversée ou un dollar en renforcement sont des modulateurs secondaires du régime. Ils n’écrasent pas les variables de prix, breadth et volatilité ; en particulier, un VIX de panique conserve toujours le régime `PANIC`.

## Diversification portefeuille

Le `PortfolioContext` peut désormais exposer les corrélations uniquement si les positions disposent de séries de clôture **datées**, de format cohérent, et d’au moins 31 séances communes. Les rendements sont alignés sur les dates communes avant le calcul. Sans ces prérequis, la corrélation reste indisponible, sans approximation à partir de prix non alignés.

## Intégrité des signaux

Strategy OS ne fabrique plus de chandeliers artificiels à partir de simples clôtures. Il appelle le même contexte d’anomalies que Skyler : OHLCV enrichi lorsqu’il est réellement fourni, sinon `CLOSE_ONLY` avec une limite déclarée.

## Validation

La suite intégrale a été exécutée après les changements : **3 034 tests réussis**. Les nouveaux tests couvrent les paquets de preuve par titre, les dates de chaînes d’options, les dimensions macro, le maintien de `PANIC` et les corrélations strictement alignées.
