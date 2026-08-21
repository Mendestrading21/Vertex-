# Une valeur connue ne doit pas rester invisible

Gardien : `tests/test_vertex_1_0_repli_cotations.py` (16 tests, 7 mutations)

---

## Le défaut, reproduit en local

```
POST /api/pos-quotes {"positions":[{"sym":"ACN"}]}
  ->  {"live": false, "results": {}}
```

…pendant que **le même serveur portait ACN à 198,0 en mémoire**, établi par le
cycle de scan. Le client exige une cotation par ligne : sans elle il pose
`ok = false` et n'affiche **aucun P&L**. Un seul fournisseur était consulté —

```python
if todo and ibkr_enabled:            # <- et rien d'autre, jamais
```

— et son silence vidait l'écran. C'est le pendant exact du défaut hors séance :
là un prix réel était **jeté** faute de clôture ; ici un prix réel n'était même
pas **cherché**.

C'est la surface qui compte le plus : le P&L du portefeuille, sur Aujourd'hui et
sur Portefeuille.

## Ce qui existait déjà, et n'était pas branché

`vertex/data_sources/fallback_market_data.py` — le module qui sait étiqueter
honnêtement un repli EOD ou secondaire — a **zéro appelant**. Il décrit la bonne
discipline (`fallback_used=True`, `source_mode=EOD`) et personne ne s'en sert.
Un module non branché ne corrige rien : c'est la démonstration vivante que la
bonne intention ne suffit pas.

Le reste du produit, lui, replie déjà : le scan a yfinance + Stooq, les indices
IBKR sont une **surcouche** sur du yfinance différé, les options ont
`_YF_FOR_OPTIONS` en repli si TWS est fermé. La cotation des positions était le
seul chemin sans filet.

## Le correctif

Un dernier recours pour les **actions**, injecté (`cotation_repli`) donc
éprouvable sans serveur :

```
{"fallback_used": true, "results": {
   "ACN|||": {"type":"STK","spot":198.0,"spot_chg":-0.53,"source":"scan"}}}
```

- **après** le passage broker, jamais avant — sinon un cours de scan serait
  servi alors qu'une vraie cotation était disponible ;
- **jamais une option** : le scan ne cote pas de contrats, et dériver un prix
  d'option du sous-jacent serait exactement la donnée inventée que le produit
  interdit. Une option non cotée reste absente, donc honnêtement `—` ;
- **étiqueté `source: 'scan'`** — sans étiquette, un cours de scan se fait
  passer pour une cotation broker, le mensonge de provenance le plus facile à
  commettre ;
- **pas mis en cache** : le cache sert les cotations broker, et y ranger un
  cours de scan le ferait servir *à la place* d'une vraie cotation pendant tout
  le TTL ;
- **aucune requête réseau** : la valeur est déjà en mémoire. Un appel réseau ici
  serait lent, faillible et soumis aux limites de débit du fournisseur — au
  moment précis où tout le reste est déjà en panne. Un test l'interdit.

## Vérification

- Avant : `results: {}` · après : les actions cotées, l'option laissée absente.
- 7 mutations, 7 détectées : combler les options · ignorer la casse de `right` ·
  écraser une cotation broker · retirer l'étiquette de source · accepter un
  `spot` absent · consulter le repli avant le broker · ne plus injecter la
  source.
- Suite complète : **3 522 passed**.

## Sur les API du guide — ce que j'ai fait et ce que je n'ai pas fait

**Fait** : exploiter la source gratuite que le produit embarque déjà (yfinance,
via le scan) partout où son absence vidait un écran. Zéro clé, zéro compte,
zéro requête supplémentaire.

**Pas fait, et volontairement** : brancher FRED, SEC EDGAR ou Alpha Vantage.
Le réseau de cet environnement **bloque tout hôte hors registres de paquets** —
vérifié : `yfinance` lui-même y échoue en `CONNECT tunnel failed, response 403`.
Une intégration écrite ici ne pourrait pas être exécutée une seule fois avant
d'atterrir chez toi. Après huit fautes d'instrument mesurées dans cette
campagne, livrer du code réseau non exécuté serait le pire travail possible :
il aurait l'air fini et ne le serait pas.

Ce qu'elles apporteraient, si tu les veux : **FRED** la macro (taux BNS, BCE,
Fed — une clé gratuite), **SEC EDGAR** les fondamentaux US officiels (sans clé),
**Alpha Vantage** les indicateurs techniques et matières premières (25 requêtes
par jour, à mettre en cache). Aucune ne remplace yfinance pour la Suisse : les
tiers gratuits de Finnhub, FMP et Twelve Data sont limités aux actions US, et
l'API officielle SIX est payante. `.SW` reste la seule voie gratuite.
