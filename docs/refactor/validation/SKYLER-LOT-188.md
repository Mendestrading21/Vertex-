# SKYLER V2 — LOT 188 : liens d'API des pages vivantes + intelligence

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-188`
(base : `integration/vertex-skyler-v2` @ `7f26a1c`, lot 187 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Complète la famille des gardiens transverses (182 : inline, 186 :
fichiers src= + assets) par les LIENS D'API : chaque URL fetchée par
les pages vivantes doit exister dans l'app — un fetch vers une route
inexistante serait un lien mort invisible (erreur réseau à chaque
visite). Plus les invariants d'`intelligence_page.py` (662 l, la
page vivante la moins gardée).

## 2. Ce qui est figé (`tests/test_api_links_intelligence_lot188.py`, 5 tests)

```text
Liens d'API — les ≥ 40 endpoints fetchés par les 11 pages servies
  existent TOUS dans l'url_map (motifs paramétrés + préfixes
  concaténés gérés) — constat : 54 endpoints, 0 mort
intelligence_page — les 6 vues (analyst/committee/strategy/impacts/
  research/memory) rendent 200 avec UN SEUL onglet actif, le bon
  (aria-selected) ; vue inconnue → retombe sur la vue par défaut
  (jamais une page cassée) ; aucun id dupliqué dans aucune vue ;
  états honnêtes omniprésents (≥ 12 VX.states) ; #8f8a83 absent ;
  aucun verbe d'ordre
```

## 3. Preuves

```text
python -m pytest tests/test_api_links_intelligence_lot188.py -q → 5 passed
python -m pytest tests/ -q → 2461 passed, 2 skipped (2456 + 5)
Aucun changement UI → pas de bump SW (v152 courante)
```

## 4. Suite — NOUVELLE DIRECTIVE UTILISATEUR (prioritaire)

L'utilisateur demande (captures TradingView à l'appui) la REFONTE DE
TOUS LES GRAPHIQUES de Vertex dans un langage visuel TradingView :
jauges semi-circulaires dégradées à aiguille, cône de projection
min/moy/max, barres de consensus, zones d'estimation hachurées,
graphiques double-axe annotés — moderne, équilibré, structuré.
LOT 189 : ouvrir la « TOURNÉE GRAPHIQUE TV » — grammaire commune
dans chart-core puis refonte lot par lot de chaque builder, avec
protocole UI complet (serveur DEMO, captures, SW bump, gardiens).
