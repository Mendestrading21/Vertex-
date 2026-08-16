# Vertex — itération de mesure d’intelligence 1.4

## Objet

Cette itération augmente la capacité de Vertex à **mesurer** ses opportunités plutôt qu’à ajouter des prédictions non vérifiables. Elle ne transmet aucun ordre, ne modifie pas la constitution stratégique automatiquement et sépare strictement une observation de marché d’une performance réelle.

| Module | Rôle | Source d’entrée | Sortie honnête |
|---|---|---|---|
| `record_option_board()` | Figer les marques de contrats suivis | `options_board` réellement publié | Snapshot hypothétique avec source et type de référence |
| `opportunity_attribution` | Expliquer les moteurs et contraintes d’un score | Packet et décision Skyler déjà calculés | Drivers, faiblesses, gates, preuves manquantes |
| `intelligence_monitor` | Surveiller une baisse persistante du hit rate | Outcomes mémoire aux horizons mesurés | `STABLE`, `UNDER_WATCH` ou `INSUFFICIENT_SAMPLE` |

## Quotes d’options et performance hypothétique

À chaque publication du board, `terminal._publish_board()` appelle `record_option_board()`. Seuls les suivis de type `OPTION`, actifs et associés à un identifiant exact `SYM|EXP|STRIKE|C/P` sont candidats à un snapshot.

La résolution de prix accepte les données réellement présentes, dans l’ordre du référentiel existant : midpoint bid/ask valide, `mid`, `mark`, puis `last` avec avertissement. Le champ `cost` n’est jamais promu en quote de marché courante. Si le contrat est absent du board, le suivi reçoit une preuve de résolution indisponible ; aucun prix nul ou prix fictif n’est écrit.

Les snapshots sont dédupliqués par horodatage de publication du board. Ils permettent de mesurer une trajectoire hypothétique, le maximum favorable/défavorable et, à terme, les horizons de contrat. Ils ne représentent ni une exécution, ni un remplissage, ni un résultat encaissé.

## Attribution d’opportunité

`decision.opportunity_attribution` classe un dossier de manière descriptive :

| Statut | Condition prioritaire |
|---|---|
| `REJECTED_BY_GATES` | Au moins une hard gate est déclenchée. |
| `EVIDENCE_REQUIRED` | Un contexte est indisponible ou une gate est non évaluable. |
| `SCORE_INCOMPLETE` | Des blocs de score restent insuffisants. |
| `CANDIDATE_FOR_ANALYTICAL_REVIEW` | Aucun blocage, score ≥ 24/40, mais lecture analytique seulement. |
| `LOW_CONVICTION` | Score inférieur au seuil de revue. |

Les drivers sont triés par couverture de bloc et les faiblesses par points manquants. La structure explique donc pourquoi un dossier mérite une revue ou reste incomplet, sans l’élever au rang d’instruction de marché.

## Surveillance de dérive

`GET /api/skyler/monitor?horizon=H5|H10|H15|H20|H60` utilise exclusivement les outcomes dont le statut est `MESURE` dans la mémoire append-only du moteur courant. Il produit un statut global, puis des sorties distinctes par régime et par univers d’options. Chaque segment attend trois fenêtres non chevauchantes de dix résultats par défaut avant d’évaluer une décroissance du hit rate.

> Sous le seuil de trente résultats mesurés, le statut est obligatoirement `INSUFFICIENT_SAMPLE`. Vertex ne déduit pas une stabilité ni une dérive à partir d’un échantillon trop petit.

Une décroissance monotone d’au moins 15 points de hit rate donne `UNDER_WATCH`. Une seconde surveillance compare la proportion de preuves actionnables de qualité/réconciliation figées entre les mêmes fenêtres ; une baisse monotone d’au moins 20 points produit `DATA_QUALITY_DRIFT`. Le moniteur ne change ni score, ni gate, ni constitution ; il expose seulement une justification de revue.

## Contrat de présentation

Le contrat destiné aux couches de présentation est documenté dans `docs/CLAUDE_VERTEX_INTELLIGENCE_CONTRACT.md`. Les champs d’intelligence sont servis par `GET /api/skyler/<SYMBOL>` sous `decision.readiness`, `decision.opportunity_attribution` et `decision.performance_monitor`. La route dédiée `/api/skyler/monitor` fournit le même diagnostic global sans forcer le calcul d’une fiche titre.

## Limites conservées

Le P&L de contrat ne peut devenir une calibration pleinement contractuelle que lorsque les snapshots couvrent réellement l’entrée et les échéances de sortie, avec une convention explicite de slippage et de frais. Jusqu’à cette collecte, les résultats d’options restent hypothétiques et la calibration existante conserve son périmètre `DIRECTIONAL_PROXY_ONLY`.
