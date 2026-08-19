# G5 — Protocole de la première connexion réelle

Banc : `tools/vertex_1_0/mesurer_g5_live.py`
Gardien : `tests/test_vertex_1_0_g5_live.py` (15 tests, 9 mutations éprouvées)
État : **prêt à tourner** · G5 reste **vide** tant qu'il n'a pas tourné

---

## Pourquoi ce document existe

Tout ce que la campagne a prouvé l'a été sous `DEMO=1 NO_IBKR=1`. Les 57
fichiers de tests qui citent IBKR lisent le **texte** du code — `READONLY is
True`, `REQUEST_TIMEOUT_S == 45`, `inspect.getsource(...)`. Ils prouvent ce que
le code *dit*, pas ce qu'il *fait* face à un broker. L'import d'`ib_async` est
paresseux, précisément pour que l'app démarre sans TWS : ce chemin n'a jamais
été exécuté ici.

Donc : **G5 n'est pas en attente d'une formalité, il est vide.** Brancher TWS
n'est pas la dernière case à cocher, c'est le premier vrai test.

Le bilan de la campagne est l'argument : **neuf défauts produits trouvés, tous
invisibles sous une suite verte**, et **l'instrument s'est trompé avant le
produit sept fois sur sept**. Ce qui n'est pas mesuré est généralement faux.
La première connexion doit donc produire des preuves, pas une impression.

## Les deux règles du banc

**1. L'absence de TWS n'est jamais un succès.** Sans broker joignable, sortie 3
et aucun verdict :

```
G5 — AUCUNE MESURE N'A ETE FAITE
TWS / IB Gateway injoignable sur 127.0.0.1:7497
Ceci n'est PAS un succes. Aucune conclusion ne peut etre tiree.
```

Un banc qui rendrait « 0 anomalie » sans avoir rien mesuré serait pire que pas
de banc : il autoriserait à ne plus mesurer.

**2. « Ma sonde est en faute » ne se confond pas avec « le produit est en
faute ».** Les hypothèses de forme sur `ib_async` — noms de champs, `nan` contre
`None`, structure des Greeks — ne sont vérifiées **par rien** tant que ça n'a pas
tourné. Chaque sonde est encapsulée et rapporte son échec dans
`sondes_en_echec`, une rubrique séparée qui ne noircit ni ne blanchit le verdict
produit.

## Ce que le banc mesure

| # | axe | ce qui est cherché |
| --- | --- | --- |
| 1 | **Souscriptions** | un prix absent reste-t-il absent, ou devient-il `0` |
| 2 | **Live / différé** | le mode réel, et l'étiquette que le produit en tire |
| 3 | **Greeks** | `modelGreeks` vide → le calculateur rend-il `None` |
| 4 | **Rythme** | violations de rythme du broker, durée des requêtes |
| 5 | **Réconciliation** | positions du broker contre trades déclarés |

Transversalement, **le contrôle central** : les valeurs brutes du broker passent
par le calculateur **réel** du produit (`vertex.positions.calculator`), pas par
une copie. Éprouver une copie ne prouverait rien — c'est une leçon payée
plusieurs fois pendant la campagne.

`0` est la valeur fabriquée la plus fréquente et la plus crédible : elle
s'affiche sans alerter personne. C'est elle que le contrôle vise.

## Sur la lecture seule : la limite est dite, pas contournée

Ce qui **est** vérifié : l'état `readonly` de la session, et l'absence de toute
capacité d'écriture sur la façade (noms assemblés à l'exécution — les écrire en
clair ferait échouer `tests/test_no_orders.py`, on ajouterait une exception au
gardien, et c'est par là que l'invariant s'érode).

> **Constat à porter au dossier de fusion.** `CLAUDE.md` décrit la défense
> READONLY comme « une liste BLANCHE mesurée, pas une liste noire de noms »,
> tenue par `tools/mesurer_surface_ibkr.py` et
> `tests/test_signal_os_surface_ibkr_lot34.py`. **Ces deux fichiers n'existent
> pas sur cette branche** : ils vivent sur la ligne Signal OS. Ce que la
> release-candidate porte réellement, c'est `tests/test_no_orders.py` — une
> **liste noire de noms**, dont le lot 31 avait justement montré la limite :
> elle ne peut rien contre un chemin qu'on n'a pas pensé à nommer.
>
> Ce n'est pas une faille ouverte — la surface employée est petite et
> `readonly=True` est codé en dur — mais la garantie est **plus faible que ce
> que le guide annonce**, et il vaut mieux le savoir avant de brancher un compte
> réel qu'après. Importer ces deux fichiers est une décision de fusion : le
> mandat interdit de fusionner Signal OS en bloc, et je ne l'ai pas fait.

Ce qui n'est **pas** vérifié, et ne le sera jamais par ce banc : **la preuve par
tentative**. Envoyer quoi que ce soit pour voir si c'est refusé violerait
l'invariant que ce banc défend. Une preuve partielle présentée comme entière
serait pire qu'une preuve absente, parce qu'elle autoriserait l'acte.

## Comment le banc a été éprouvé sans broker

Un **faux broker** pilote la sonde de bout en bout — c'est ce qui rend ce banc
testable alors qu'il ne tournera qu'une fois, dans des conditions qu'on ne
pourra pas rejouer. Deux scénarios, parce qu'un seul ne discrimine pas :

- **broker sain** — cotations réelles, Greeks présents, portefeuille
  concordant → aucune anomalie, **aucune sonde en échec** (si une sonde tombe
  sur un broker parfait, elle tombera aussi le jour J) ;
- **broker dégradé** — aucun abonnement (`nan` partout), Greeks absents, codes
  354 et 100, portefeuille divergent → chaque défaut vu, rangé dans la bonne
  famille, et **aucune valeur fabriquée par le produit**.

Le second est l'état le plus probable d'une première connexion.

Neuf mutations appliquées sur disque, neuf détectées :

| mutation | issue |
| --- | --- |
| un `nan` redevient une valeur | détectée |
| le contrôle d'absence honnête ne trouve jamais rien | détectée |
| un relevé sans connexion se déclare mesuré | détectée |
| les capacités d'écriture ne sont plus cherchées | détectée |
| une sonde en échec devient une anomalie produit | détectée |
| les familles d'erreurs fusionnent | détectée |
| une coquille de Greeks passe pour des Greeks | détectée |
| le rendu sans broker n'avoue plus son silence | détectée |
| une session non-readonly n'est plus signalée | détectée |

## Marche à suivre

1. Ouvrir **TWS** ou **IB Gateway**, se connecter au compte réel.
2. Activer l'API : *Configuration → API → Settings* → **Enable ActiveX and
   Socket Clients**. Vérifier le port (**7497** paper / **7496** live ;
   4002/4001 pour IB Gateway) et que `127.0.0.1` est dans les adresses
   autorisées.
3. Laisser **Read-Only API** coché côté TWS. Le produit force déjà
   `readonly=True` à la connexion ; le cocher côté TWS ajoute une seconde
   serrure, indépendante du code.
4. Depuis la racine du dépôt :

```bash
python tools/vertex_1_0/mesurer_g5_live.py
#  ou, pour viser d'autres titres / le JSON complet :
python tools/vertex_1_0/mesurer_g5_live.py --symboles AAPL,MSFT,NVDA --json
```

Variables si la configuration diffère : `IBKR_HOST`, `IBKR_PORT`,
`IBKR_CLIENT_ID` (défaut 17).

### Lire la sortie

| code | signification |
| --- | --- |
| **0** | mesuré, aucune anomalie produit |
| **2** | témoin muet — le banc lui-même est cassé, ne rien conclure |
| **3** | TWS injoignable — **rien n'a été mesuré**, G5 reste vide |
| **4** | anomalies produit : lire la rubrique `ANOMALIES PRODUIT` |

Et surtout : lire la rubrique **`SONDES EN ECHEC`** avant tout le reste. Si elle
n'est pas vide, une partie de la mesure n'a pas eu lieu, et le « aucune
anomalie » qui suit ne porte que sur le reste.

## Ce que ce banc ne fera pas

- Il ne remplace pas une **séance d'observation** : les défauts de rythme et de
  souscription se révèlent sur la durée et à l'ouverture des marchés, pas sur
  une passe de trois symboles. Le lancer une fois marché fermé, une fois marché
  ouvert.
- Il ne couvre pas la **chaîne d'options réelle** (`reqSecDefOptParams`,
  contrats ambigus, devises et places multiples). C'est le chantier suivant, et
  il demande un compte avec les droits correspondants.
- Il ne prouve pas la lecture seule par tentative (voir plus haut).
