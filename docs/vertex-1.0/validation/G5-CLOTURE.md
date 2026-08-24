# G5 — clôture broker réel : ce qui est prouvé, ce qui ne l'est pas

Lot `agent/vertex-1-0-g5-cloture`, empilé sur la PR #794
(`3d3a6150`). Mesures prises le 24 août 2026 sur TWS réel, port 7496,
lecture seule, compte masqué.

Ce dossier ne rejoue pas la démonstration déjà faite au SHA `d77b06d` — session
live, quatre rôles connectés, huit espaces servis, zéro erreur client. Il
complète les cases du protocole qui manquaient, et **nomme celles qui restent
hors de portée d'une machine**.

## Le verrou levé

L'audit du 24 août avait mesuré une zone aveugle que la couverture globale de
87 % masquait : quatre adaptateurs IBKR à **0 %**. La session réelle prouvait la
connexion ; elle ne faisait exécuter **aucune ligne** de ces fichiers.

| Adaptateur | Avant | Après |
|---|---:|---:|
| `ibkr_contracts.py` | 0 % | **100 %** |
| `ibkr_market_data.py` | 0 % | **100 %** |
| `ibkr_option_chain.py` | 0 % | **100 %** |
| `ibkr_positions.py` | 0 % | **100 %** |

Mesure : `pytest --cov=vertex.data_sources tests/test_vertex_1_0_g5_adaptateurs.py`.

## Comment, sans rejouer TWS à chaque fois

`vertex/data_sources/ibkr_replay.py` fait deux choses et rien de plus :

1. **anonymiser** un relevé ou une capture, avec un contrôle séparé qui refuse
   l'écriture s'il reste une trace ;
2. **rejouer** des callbacks enregistrés, pour piloter le *vrai* code des
   adaptateurs hors TWS.

La capture `tests/fixtures/ibkr/g5_capture.json` vient d'une session réelle :
contrats qualifiés, cotations, échéances d'options et contrats d'options
authentiques. Les doubles reproduisent les pièges d'IBKR plutôt que de les
lisser — `NaN` pour un champ absent, `-1` comme sentinelle de « pas de
cotation ». Un double qui rendrait `None` ferait passer les gardes du produit
pour inutiles.

## Un défaut trouvé par la mesure, et corrigé

La sonde `mode_donnees` échouait à **chaque** exécution réelle :
`'Client' object has no attribute 'marketDataType'`.

`ib_async` 2.1.0 n'expose aucun moyen de relire le type de marché — il n'a que
le setter `reqMarketDataType`. Le produit lisait donc un attribut inexistant et
retombait **silencieusement** sur « différé » à chaque appel, dans
`ibkr_market_data.fetch_snapshot`.

Ce n'était pas dangereux — se tromper vers « différé » est la direction
prudente — mais c'était **muet**, et l'acceptation G5 exige que le type de
marché soit *capturé par requête*.

Corrigé en remplaçant la supposition par une observation : IBKR remplit
`delayedLast/delayedBid/delayedAsk` au lieu des champs directs quand la donnée
est différée. Ce qui n'est pas observable est **avoué** (`TYPE_INCONNU`) plutôt
que présenté comme mesuré.

Limite conservée et écrite : **temps réel et figé remplissent les mêmes
champs**. Les distinguer exigerait l'accusé de réception IBKR que `ib_async`
n'expose pas. Le produit ne revendique donc jamais `LIVE` sur cette seule base.

## L'artefact

`docs/vertex-1.0/validation/G5-ARTEFACT-2026-08-24.json`, écrit par
`python -m tools.vertex_1_0.mesurer_g5_live --artefact <chemin>`.

Anonymisation **non optionnelle** : le relevé contient les positions réelles du
compte, et `enregistrer` refuse d'écrire tant qu'une trace subsiste. Ce qui est
conservé du portefeuille, ce sont les **cardinalités** des écarts — compter
suffit à prouver que la réconciliation tourne ; nommer publierait le
portefeuille.

Relevé du 24 août 2026, 10:26:37 UTC :

```text
connecte            True
mode_donnees        DIRECT_NON_QUALIFIE
cotations           AAPL REELLE 310,55 · MSFT REELLE 483,52 · SPY REELLE 764,41
erreurs broker      0 (souscription [] · rythme [] · autres [])
positions           1 détenue non déclarée · 2 déclarées non détenues · 0 divergente
lecture seule       façade True · capacités d'écriture exposées : aucune
sondes en échec     aucune
anomalies produit   aucune
```

## Matrice du protocole

| Case | État | Preuve |
|---|---|---|
| Session TWS réelle, port 7496, lecture seule | **PROUVÉ** | SHA `d77b06d`, rejoué ici |
| Quatre rôles IBKR connectés | **PROUVÉ** | diagnostics, 0 rôle en échec |
| Aucune méthode d'ordre accessible | **PROUVÉ** | statique + double de rejeu |
| Qualification de contrat action | **PROUVÉ** | rejeu, capture réelle |
| Contrat option ≠ conId du sous-jacent | **PROUVÉ** | témoin dédié |
| Cotation : réelle / différée / clôture / absente | **PROUVÉ** | rejeu + observation |
| Type de marché capturé par requête | **PROUVÉ** (avec limite) | `type_observe` |
| Distinguer temps réel de figé | **HUMAN_REQUIRED** | non exposé par `ib_async` |
| Chaîne options : bid/ask/mid/IV/Greeks/volume/horodatage | **PROUVÉ** | rejeu, deux branches |
| Open interest | **NON COUVERT** | `fetch_contract_details` rend `None` |
| Positions, quantités nulles, quantité illisible | **PROUVÉ** | rejeu |
| Réconciliation broker / bureau | **PROUVÉ** | 3 écarts nommés séparément |
| Erreurs 354 / 100 / 10167 classées | **PARTIEL** | classées ; non rencontrées en séance |
| Entitlements (fondamentaux, NDX) | **PROUVÉ** | 10358 et 354 mesurés |
| Compte réel / papier | **HUMAN_REQUIRED** | un seul compte disponible |
| Reconnexion après coupure | **HUMAN_REQUIRED** | exige de couper TWS |
| Pacing et backpressure sous charge | **HUMAN_REQUIRED** | 70 requêtes sans violation ≠ preuve de limite |
| Panne partielle d'un rôle | **HUMAN_REQUIRED** | exige de désactiver un abonnement |
| Account summary (devise réelle, tag absent = `None`) | **PROUVÉ** | lot `reconciliation-pnl`, compte réel |
| Réconciliation P&L (4 sources confrontées) | **PROUVÉ** | écart réel de **95,46 USD** détecté et nommé |
| Arbitrage entre deux chiffres du courtier | **HUMAN_REQUIRED** | Vertex rapporte, il ne tranche pas |
| Signature humaine de G5 | **HUMAN_REQUIRED** | décision, pas mesure |

## Ce que ce lot ne prouve pas

Un rejeu n'est pas un broker. Il ne dit rien du rythme réel, de la
reconnexion, des droits du compte ni du comportement en séance. Il empêche
seulement qu'une régression sur ces quatre adaptateurs passe inaperçue jusqu'à
la prochaine fois où quelqu'un rallume TWS — ce qui, mesuré, n'était jamais
arrivé.

## Rollback

Le lot est additif : un module neuf, un banc neuf, une fixture neuve, une
option `--artefact`. Les deux seules modifications de code existant sont
`ibkr_market_data.type_observe` et la sonde `mode_donnees` — toutes deux
remplacent un attribut inexistant par une observation. Revenir en arrière
restaure un repli silencieux ; `git revert` du commit suffit.
