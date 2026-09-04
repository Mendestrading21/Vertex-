# ▲ VERTEX TEST 1.0 — Démarrer ici

Vertex est un terminal d'**analyse** et d'aide à la décision. Il est
**strictement en lecture seule** et ne passe jamais d'ordre.

## Lancement en un clic

- macOS: double-cliquer `Lancer_VERTEX.command`;
- Windows: double-cliquer `Lancer_VERTEX.bat`;
- démonstration sans IBKR: utiliser `Lancer_VERTEX_DEMO`.

La première exécution crée `.venv` et installe les dépendances. Le navigateur
s'ouvre sur `http://localhost:5002`.

## Lancement manuel canonique

```bash
python -m venv .venv
pip install -r requirements.txt
python -m vertex
```

`python terminal.py` reste temporairement compatible, mais ne doit plus être
utilisé dans les nouveaux scripts ou déploiements.

## IBKR live en lecture seule

1. ouvrir TWS ou IB Gateway;
2. activer l'API;
3. activer impérativement **Read-Only API**;
4. autoriser `127.0.0.1`;
5. lancer Vertex.

Sans TWS, Vertex fonctionne en mode différé ou dégradé et l'affiche.

## Accès protégé

Copier `.env.example` vers `.env`, puis définir `VERTEX_CODE` et idéalement
`VERTEX_SECRET`. Le fichier `.env` ne doit jamais être publié.

## Mandats actifs

- options longues: revues à 2/4/6 semaines, échéance cible environ 180 jours;
- actions: horizons 3/6/12 mois;
- WMB Brief: contexte macro quotidien sourcé;
- TradingView: signal de réévaluation uniquement.

## Vérifier l'installation

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

L'espace **Système** et `/healthz` indiquent ensuite l'état des sources,
moteurs, caches et données.

## Rappel

Vertex structure une analyse; il ne garantit aucun rendement, ne remplace pas
une décision humaine et n'exécute aucune transaction.
