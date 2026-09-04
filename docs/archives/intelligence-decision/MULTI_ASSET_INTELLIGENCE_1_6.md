# Vertex — intelligence multi-actifs 1.6

## Profil d’instrument

Vertex expose un `instrument_profile` pour chaque analyse Skyler. Ce profil distingue une action suivie dans la cartographie sectorielle, un ETF à proxy sectoriel déclaré, un ETF large déclaré, et un instrument non classifié. La classification est **descriptive** : elle ne reconstitue pas les composants d’un ETF et n’invente aucune exposition.

| Cas | Source de classification | Conséquence analytique |
|---|---|---|
| Action de la cartographie Vertex | `SECTOR_MAP` | Comparaison au secteur disponible. |
| ETF sectoriel couvert | `ETF_SECTOR_PROXY` | Comparaison au proxy sectoriel déclaré, sans prétendre détenir la composition complète. |
| ETF large couvert | `BROAD_ETFS` | Classe ETF connue, sans cohérence sectorielle forcée. |
| Instrument sans preuve canonique | `UNKNOWN` | Aucune classe présumée et aucune cohérence déclarée. |

## Cohérence sectorielle

`sector_coherence` compare, lorsque l’agrégat sectoriel du scan est présent, le score d’un instrument avec le score moyen sectoriel, la breadth (`pct_buy`), le niveau de risque et le rang parmi les membres. C’est un contexte de marché : il ne modifie ni le score Skyler ni le verdict.

## Exposition portefeuille

`portfolio_context.asset_mix` regroupe les valeurs et poids des types canoniques réellement déclarés dans les positions : `STOCK`, `ETF`, `OPTION`, `FUND`, `CRYPTO` ou `UNCLASSIFIED`. Les types absents restent explicitement `UNCLASSIFIED`; ils ne sont jamais assimilés silencieusement à des actions.

## Invariants

> Aucun profil, proxy sectoriel, poids d’actif ou niveau de cohérence ne crée un ordre, une allocation ou une recommandation d’exécution. Les données absentes restent indisponibles et les diagnostics restent en lecture seule.
