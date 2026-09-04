# Vertex — mémoire, calibration et gates `SWING_3_6M`

## Objet et périmètre

Le mandat `SWING_3_6M` vise une **détention de 5, 10 ou 15 séances** au moyen de contrats dont l’échéance laisse une marge de temps importante. Vertex reste un système d’analyse : il prépare, compare, plafonne ou refuse une décision, mais ne transmet aucun ordre.

Le mécanisme se compose de trois couches distinctes. Le scanner qualifie les contrats selon leur mandat. Les hard gates empêchent le score de contourner une non-conformité critique. Enfin, la mémoire append-only mesure a posteriori ce que le moteur a vu au moment de sa décision, sans réécrire l’historique ni utiliser d’information future.

| Couche | Question traitée | Sortie principale |
|---|---|---|
| Scanner options | « Ce contrat respecte-t-il le mandat ? » | `IN_MANDATE`, `PARTIAL_MANDATE` ou `OUT_OF_MANDATE` |
| Gates Skyler | « Une décision doit-elle être plafonnée ? » | `triggered=True`, `False` ou `None` |
| Mémoire | « Qu’a décidé cette version du moteur, avec quelles preuves ? » | Record immuable par décision |
| Calibration | « Les scénarios directionnels ont-ils contenu les résultats mesurés ? » | Facteur borné et segments descriptifs |

## 1. Mandat de sélection `SWING_3_6M`

Le scanner est séparé des univers `TACTICAL`, `SWING` et `LEAPS`. Pour `SWING_3_6M`, le contrat doit appartenir à la fenêtre de **75 DTE inclus à 210 DTE exclu**. La fenêtre préférée est **90–180 DTE** et la cible de classement est **135 DTE**. Un contrat situé dans la fenêtre admissible mais éloigné de 135 DTE reste visible ; il est simplement moins bien classé à conformité égale.

| Contrôle du mandat | Seuil appliqué | Traitement si donnée absente |
|---|---:|---|
| DTE de l’univers | `75 ≤ DTE < 210` | Le contrat n’entre pas dans ce scanner si le DTE est absent ou hors fenêtre |
| Delta absolu | `0,30 ≤ |Δ| ≤ 0,60` | `PARTIAL_MANDATE` |
| Open interest | `OI ≥ 500` | `PARTIAL_MANDATE` |
| Volume | `volume ≥ 50` | `PARTIAL_MANDATE` |
| Spread | `spread_pct ≤ 8,0 %` | `PARTIAL_MANDATE` |
| Âge de quote | `≤ 900 s` | `PARTIAL_MANDATE` |
| Plan de détention | `H5 / H10 / H15` | Toujours figé avec le contexte sélectionné |

Le statut suit une règle simple et conservative. Si **au moins un contrôle est faux**, le contrat est `OUT_OF_MANDATE`. Si aucun contrôle n’est faux mais qu’au moins une donnée est absente, il devient `PARTIAL_MANDATE`. Il n’est `IN_MANDATE` que lorsque tous les contrôles disponibles sont positifs.

> Une donnée manquante ne devient jamais une conformité implicite. Elle reste visible dans `mandate_reasons` et ne disparaît pas du scanner.

Les candidats sont classés dans cet ordre : `IN_MANDATE`, puis `PARTIAL_MANDATE`, puis `OUT_OF_MANDATE`; à statut égal, Vertex privilégie le DTE le plus proche de 135, la meilleure note de qualité, puis un strike plus bas. Le premier candidat devient `options_context.best`; il est le seul contrat que les gates Skyler évaluent.

## 2. Gates options : effet sur la décision

Les hard gates sont évaluées **après** la constitution du packet et **avant** le verdict final. Elles sont prioritaires sur le score. Elles possèdent trois états : `True` signifie qu’une porte est effectivement déclenchée, `False` signifie que le contrôle est conforme, et `None` signifie que la porte ne peut pas être évaluée faute de contexte.

| Gate | Source effective | Déclenchée lorsque | État `None` |
|---|---|---|---|
| `SPREAD_EXCESSIVE` | `best.mandate.spread_ok` | Le spread du meilleur contrat dépasse 8,0 % | Spread ou candidat absent |
| `OI_INSUFFICIENT` | `best.mandate.oi_ok` | L’open interest est inférieur à 500 | OI ou candidat absent |
| `DTE_OUT_OF_MANDATE` | `best.dte` et `options_context.window` | Le DTE sort de la fenêtre de l’univers transmis | DTE, fenêtre ou candidat absent |

La gate DTE ne réinterprète pas le mandat : elle lit la fenêtre réelle du contexte. Ainsi, pour `SWING_3_6M`, un contrat est conforme si `75 ≤ DTE < 210`; pour `LEAPS`, la borne supérieure est incluse. Ce comportement évite qu’une règle cachée ou un seuil codé en double crée une divergence.

Les contrôles **delta, volume et fraîcheur de quote** font bien partie du statut de mandat du scanner. Dans cette version, ils ne sont pas encore des hard gates séparées. Une non-conformité les fait apparaître comme `PARTIAL_MANDATE` ou `OUT_OF_MANDATE` et plafonne le bloc `options_quality` du score, mais elle ne produit pas encore une gate autonome. C’est une distinction importante entre **signal de conformité** et **blocage dur**.

Lorsque plusieurs gates sont déclenchées, la première selon l’ordre de la Constitution explique `capped_by_gate`. Les gates options viennent après `RR_BELOW_2`, `NO_INVALIDATION`, `DATA_QUALITY_CRITICAL` et `SOURCES_CONFLICT`, et avant les gates de thèse et de portefeuille.

| Situation finale | Conséquence Skyler |
|---|---|
| Au moins une gate `True` et score inférieur à 24/40 | `REFUSER` |
| Au moins une gate `True` et score au moins égal à 24/40 | `ATTENDRE` |
| Aucune gate `True`, score au moins égal à 28/40 | `ACHETER`, sous réserve du verdict canonique et des autres plafonds |
| Gate à `None` | Elle est listée parmi les inconnues ; elle ne se transforme pas automatiquement en conformité |

La dernière ligne décrit une limite assumée. Une gate options non évaluable n’est pas, à elle seule, une gate déclenchée. En revanche, la qualité et la réconciliation des données disposent de leur propre gate `DATA_QUALITY_CRITICAL`, qui plafonne le dossier quand les preuves critiques ne sont pas actionnables.

## 3. Mémoire décisionnelle : ce qui est figé

À chaque décision servie, `freeze()` produit un record append-only. Son identifiant inclut le symbole, l’horodatage, la décision, la version du moteur et le statut démo. Une modification de règle qui change `ENGINE_VERSION` produit donc une nouvelle population de mémoire : Vertex ne mélange pas silencieusement les résultats d’un moteur ancien et ceux d’un moteur modifié.

| Élément figé | Utilité analytique |
|---|---|
| Version moteur et profil | Séparation stricte des générations de règles |
| Prix à la décision et empreinte des 8 dernières clôtures | Ancrage de la mesure sans look-ahead |
| Score /40, blocs insuffisants, niveau et gates | Explication reproductible du verdict |
| Régime, contradictions, thèse, catalyseur et scénarios | Post-mortem sur le dossier réellement connu à l’instant T |
| Contexte options | Univers, DTE, bucket DTE, delta, IV, OI, volume, spread, âge de quote, statut de mandat et plan H5/H10/H15 |
| Contexte portefeuille | Nombre de lignes, concentration HHI, ligne dominante et poids dominant |

Le record précise explicitement que le P&L du contrat est indisponible tant qu’aucune quote de sortie, aucun spread de sortie et aucun slippage observé ne sont stockés. Ce n’est pas une lacune masquée : c’est une barrière contre une calibration artificielle d’options.

## 4. Mesure sans look-ahead

Pour mesurer une décision, Vertex retrouve l’empreinte `tail_at_decision` dans la série actuelle. Il ne conserve que les clôtures **strictement postérieures** à cette occurrence. Si l’empreinte ne peut pas être retrouvée — série révisée, tronquée ou non alignée — le résultat est `NON_MESURABLE`; le moteur ne cherche pas une date « proche » et ne comble pas l’écart.

Les horizons du mandat sont `H5`, `H10` et `H15`. `H20` et `H60` restent disponibles pour l’observation de thèse plus longue. Chaque horizon peut être `EN_ATTENTE`, `MESURE`, `NON_MESURABLE` ou `NON_APPLICABLE`.

Le rendement mesuré est celui du **sous-jacent à la clôture**, par rapport au prix de la décision. Les métriques MFE et MAE utilisent les extrêmes des seules clôtures postérieures disponibles. Elles ne sont pas des résultats de contrat option.

## 5. Calibration globale réellement consommée

La calibration répond à une question limitée : les scénarios directionnels du moteur ont-ils correctement contenu les résultats du sous-jacent ? Une mesure est considérée comme un « hit » lorsque sa classification est `DECISION_CORRECTE` ou `VARIANCE_NORMALE`, au plus long horizon déjà mesuré pour le record.

Le calcul est effectué **pour une version de moteur unique**. Avant 20 décisions mesurées, le facteur vaut strictement `0,50`; aucun hit rate n’est affiché. À partir de 20 mesures :

> `facteur = 0,50 + 0,40 × hit_rate`

Ce facteur est donc borné entre `0,50` et `0,90`; il ne peut jamais porter la confiance à 1,00. La confiance Skyler est ensuite le produit de quatre facteurs : qualité des données, accord entre contextes, robustesse aux perturbations et calibration. Des plafonds supplémentaires s’appliquent en régime `UNKNOWN`, en présence d’un conflit de sources ou d’une contradiction.

La sélection du facteur suit cet ordre : cellule du **niveau** (`S_PLUS`, `S`, `A`, `B`, etc.) si elle contient au moins 20 observations, puis cellule du **régime** si elle est mature, puis facteur global de la version, puis 0,50. Vertex évite volontairement le croisement niveau × régime afin de ne pas créer des échantillons trop petits.

## 6. Segments options : observation, pas probabilité de P&L

La mémoire segmente aussi les décisions mesurées par univers options, bucket DTE et plan de détention. Les buckets DTE sont : `UNDER_75`, `75_104`, `105_134`, `135_164`, `165_180`, `181_210` et `OVER_210`. Pour le mandat 3–6 mois, les observations se concentrent normalement dans les buckets `75_104` à `181_210`.

| Segment | Exemple de clé | Ce que la cellule mesure aujourd’hui |
|---|---|---|
| Univers options | `SWING_3_6M` | Résultat directionnel du sous-jacent des décisions ayant ce contexte |
| Bucket DTE | `105_134` | Résultat directionnel du sous-jacent avec ce DTE initial |
| Plan de détention | `5_10_15` | Résultat directionnel associé au plan figé |

Chaque cellule exige aussi 20 mesures avant de recevoir le statut `MESURE`. Malgré cela, ces cellules restent **descriptives uniquement** : `option_calibration_summary()` les étiquette `DIRECTIONAL_PROXY_ONLY` et elles ne sont pas consommées par le facteur de confiance. Cette règle tient tant que Vertex ne mesure pas le prix d’entrée du contrat, les quotes de sortie, le spread réellement subi, le slippage, les Greeks et l’effet du temps.

## 7. Interprétation opérationnelle et limites

Le système peut dire qu’un dossier est techniquement favorable, qu’un contrat respecte ou non le mandat, ou qu’une décision historique a été correcte à H5/H10/H15 sur le sous-jacent. Il ne peut pas encore affirmer qu’un contrat `SWING_3_6M` spécifique a généré un rendement probabiliste calibré.

Pour faire évoluer ces segments vers une calibration de P&L option, le pipeline doit enregistrer de manière horodatée le contrat exact, le bid/ask et le mid à l’entrée et à chaque horizon, les Greeks, le prix du sous-jacent, l’IV, les coûts/slippage et la cause de sortie. Ces données devront être réconciliées avant toute promotion d’un segment descriptif en composant de confiance.

## Références de code

Les règles décrites proviennent du code versionné dans les fichiers suivants : `vertex/engines/decision_memory.py`, `vertex/options/horizon_scanners.py`, `vertex/engines/skyler_core.py` et `vertex/strategy/profiles/vertex_strategy_v3.json`.
