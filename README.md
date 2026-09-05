# ▲ VERTEX TEST 1.0

**Centre personnel d'intelligence de marché et d'aide à la décision — analyse
uniquement.**

Vertex Test 1.0 centralise le régime de marché, le brief quotidien, les
opportunités, l'analyse d'entreprises, le portefeuille déclaré et l'intelligence
options. Il produit des décisions structurées, mesurables, traçables et
explicables. **Aucun chemin d'exécution d'ordre n'existe dans ce dépôt.**

## Lancer

```bash
python -m venv .venv
. .venv/bin/activate            # Windows : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m vertex
```

Ouvrir `http://localhost:5002`. Les lanceurs `Lancer_VERTEX` et
`Lancer_VERTEX_DEMO` restent disponibles ; `python terminal.py` fonctionne encore
en mode de repli mais n'est plus l'entrée canonique.

### Voir Vertex peuplé, sans TWS ni compte

```bash
DEMO=1 NO_IBKR=1 python -m vertex      # Windows : $env:DEMO=1; $env:NO_IBKR=1
```

La vitrine remplit les douze pages avec des données **synthétiques**, et le dit :
un bandeau « DÉMO — données synthétiques clairement identifiées, jamais
présentées comme réelles » reste visible, la provenance affiche `demo`. C'est le
moyen de parcourir l'interface entière sans TWS, sans clé et sans compte.

### Ce qui est normal au premier lancement

| Ce que vous voyez | Ce que ça veut dire |
|---|---|
| `TWS / IB Gateway injoignable sur 7496, 7497, 4001, 4002` | Aucune session courtier ouverte. **État normal.** Vertex sert le différé yfinance et l'étiquette. Une seule ligne : les répétitions de la bibliothèque sont comptées, pas réaffichées. |
| `Failed to get ticker 'X'` en rafale | Votre réseau ne joint pas Yahoo (VPN, pare-feu, réseau d'entreprise). Le scan reste vide et le dit — `source: unavailable`, jamais un chiffre inventé. |
| Système → Connexions : `Claude — Secours` | Aucune `ANTHROPIC_API_KEY`. La synthèse déterministe des moteurs est servie ; l'enrichissement IA affiche « indisponible ». |

### Vérifier que tout marche

```bash
curl http://localhost:5002/healthz      # build, moteurs, constitution
curl http://localhost:5002/readyz       # prêt à servir
```

Puis, dans l'interface, **Système** répond à la question en une page : santé
globale, matrice des connexions (configuré ≠ connecté), jobs de fond avec leur
état réel (`ACTIF`, `ERREUR`, `SILENCIEUX`, `EN_ATTENTE`, `NON_IMPLÉMENTÉ`) et
fraîcheur par domaine.

### Rejouer les preuves

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q                      # suite complète
python -m pytest tests/test_no_orders.py -q
```

Les deux gardiens navigateur (`tests/test_qa_espaces.py`,
`tests/test_couche_visuelle.py`) exigent un serveur local **et** Chromium ; sans
eux ils s'écartent d'eux-mêmes plutôt que de mesurer du vide. Lancer Vertex
avant la suite si vous voulez la preuve visuelle complète.

## Mandats de décision

| Mandat | Cadre |
|---|---|
| Options tactiques longues | détention typique 2/4/6 semaines ; DTE préféré 120–240 jours ; cible 180 jours |
| Actions | horizons de décision 3/6/12 mois |
| WMB Brief | contexte macro quotidien, daté et sourcé ; jamais une source de prix |

Le profil de release exécuté est
`vertex/strategy/release_profiles/vertex_strategy_v4.json`. Les profils V1–V3
restent en place comme chemin de rollback ; le runtime active V4 avant de charger
l'application.

## Sources et intégrations

- **IBKR** — contrats, cours, historiques, chaînes, IV et Greeks de marché
  uniquement, connexion forcée en lecture seule. Aucun compte, solde, position,
  NAV, P&L, ordre ni exécution du courtier n'entre dans Vertex.
- **Portefeuille** — enveloppes, cash et positions saisis volontairement par
  l'utilisateur. Aucune source externe ne les crée, ne les modifie ni ne les
  ferme.
- **TradingView** — signaux authentifiés qui demandent une réévaluation, jamais
  un achat.
- **WMB Brief** — contexte macro quotidien avec provenance.
- **yfinance** — repli différé, explicitement étiqueté comme tel.
- **Claude** — synthèse et explication uniquement. Les calculs, scores, Greeks,
  probabilités, hard gates et verdicts restent déterministes.

## Architecture

```text
sources réelles
  → normalisation / qualité / fraîcheur / provenance
  → moteurs déterministes
  → packet immuable
  → hard gates
  → scénarios / score / portefeuille
  → décision canonique
  → explication IA
  → interface / journal / audit
```

`vertex.runtime` est l'entrée WSGI canonique : il active le profil de release
puis importe `terminal.py`. Le monolithe reste un adaptateur historique en cours
de décomposition ; aucune nouvelle capacité ne doit y être ajoutée.

## Espaces réellement servis

Dashboard, Opportunités, Analyse, Portefeuille, Options, Journal, Système, plus
Intelligence et Suivis en pages secondaires. Calendrier redirige vers
Opportunités et Marchés vers le Dashboard. Simulateur et Suivi n'existent pas
encore et ne sont pas présentés comme livrés.

## Développement

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

Claude Code utilise exclusivement `/vertex-2-0`
(`.claude/skills/vertex-2-0/SKILL.md`), seule doctrine active du dépôt.

## Documentation

[`docs/README.md`](docs/README.md) — index.
[`docs/ARBORESCENCE.md`](docs/ARBORESCENCE.md) — propriétaire et preuve de
consommation de chaque dossier.
[`docs/CONTRATS.md`](docs/CONTRATS.md) — les contrats de gouvernance nommés dans
le code.

## Sécurité

- `READONLY=True` et `ANALYSIS_ONLY=True` ;
- aucune route ni fonction d'ordre, de transfert ou d'exercice ;
- secrets dans `.env`, jamais dans Git ;
- données absentes, différées, rassies, démo ou hors ligne explicitement
  distinguées les unes des autres ;
- aucune promesse de performance ni conseil financier personnalisé.
