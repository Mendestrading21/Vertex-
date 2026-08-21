# Vertex 1.0 · #783 — Carte des domaines dupliqués

SHA : `d52a39d4baf1` · généré par `tools/vertex_1_0/inventaire_domaines.py`

> Régénéré, jamais édité à la main. **Aucune fusion n'est proposée ici** :
> un nom qui paraît ancien n'est pas une preuve d'obsolescence, et deux
> paquets au nom voisin peuvent être deux responsabilités correctement
> séparées. Ce sont les chiffres qui informent la décision.

## Famille « entreprise »

| paquet | existe | symboles publics | consommateurs | fichiers possédés |
| --- | --- | --- | --- | --- |
| `vertex/company` | oui | 3 | **2** | — |
| `vertex/companies` | oui | 5 | **2** | — |

**Aucune dispute de fichier** : chaque paquet possède les siens.

**Aucun symbole commun.** Malgré des noms voisins, ces paquets
n'exposent pas la même chose : les « converger » sans autre preuve
détruirait une séparation qui tient peut-être debout.

## Famille « donnees »

| paquet | existe | symboles publics | consommateurs | fichiers possédés |
| --- | --- | --- | --- | --- |
| `vertex/data` | oui | 65 | **25** | `company_cache.json`, `constituents_cache.json` |
| `vertex/data_sources` | oui | 107 | **19** | `analyst_cache.json` |

**Aucune dispute de fichier** : chaque paquet possède les siens.

**Recouvrement de noms** — c'est ici que se joue la question du doublon :

- `data ∩ data_sources` : 1 symbole(s) — `get`

## Famille « portefeuille »

| paquet | existe | symboles publics | consommateurs | fichiers possédés |
| --- | --- | --- | --- | --- |
| `vertex/portfolio` | oui | 33 | **16** | — |
| `vertex/positions` | oui | 37 | **4** | `position_inventory.json` |
| `vertex/tracking` | oui | 35 | **9** | `tracking.json` |

**Aucune dispute de fichier** : chaque paquet possède les siens.

**Recouvrement de noms** — c'est ici que se joue la question du doublon :

- `portfolio ∩ positions` : 1 symbole(s) — `assess`
- `portfolio ∩ tracking` : 1 symbole(s) — `build`
- `positions ∩ tracking` : 1 symbole(s) — `mae_mfe`

