# Vertex — délais actifs de fournisseurs et dégradation sûre

## Portée

Le cycle de scan applique maintenant des **délais effectifs** aux deux fournisseurs de données historiques réellement utilisés. Cette protection s’ajoute aux codes d’erreur sûrs et à la santé descriptive du scan ; elle ne produit ni prix, ni signal, ni recommandation artificielle lorsqu’un fournisseur est indisponible.

| Fournisseur actif | Appel protégé | Budget appliqué | Dégradation observée |
|---|---|---:|---|
| yfinance | `yf.download()` par lot | 10 secondes | Le lot est ignoré ; les titres manquants basculent vers le repli Stooq. |
| Stooq | `urllib.request.urlopen()` par titre | 8 secondes | Le titre est absent du repli ; le scan conserve seulement les séries effectivement reçues. |

## Invariants

Le champ `source_health` expose uniquement les états `AVAILABLE`, `UNAVAILABLE`, `CACHED`, `NOT_COLLECTED`, `UNKNOWN` ou `DEGRADED`. Le champ ne contient ni URL, ni message de fournisseur, ni détail d’exception. Les erreurs globales de scan restent `market_data_unavailable` ou `scan_failed`.

> Un délai protège le temps d’attente réseau, mais ne transforme pas une source lente en donnée valide. Si le benchmark indispensable n’est pas reçu, Vertex passe en mode dégradé et ne présente pas le scan comme actionnable.

## Vérifications

Les tests `test_active_source_timeouts_lot651.py` vérifient la transmission effective des deux budgets au client yfinance et à Stooq. La suite complète garantit aussi que les tests de téléchargement n’altèrent pas la provenance des prix des autres parcours.
