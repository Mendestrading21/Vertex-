# SKYLER V2 — LOT 181 : caractérisation de la couche artistique de l'accueil

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-181`
(base : `integration/vertex-skyler-v2` @ `6096bda`, lot 180 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible — NOUVELLE DIRECTION : couches UI vivantes non gardées

Survey honnête : ibkr_scheduler/source_router sont couverts par
test_data_sources (22 tests — priorités, dédup, circuit breaker,
annulation des requêtes rassies) ; quant_engine par test_vertex
(17 tests d'invariants) ; swing (5, golden) et events (14). La vraie
lacune : `vertex/ui/home_art.py` (171 lignes, ZÉRO test — VIVANTE :
appliquée sur PAGE_DAILY et PAGE_STRATEGIE dans terminal.py). La
couche « salle de marché » de l'accueil : deux fonctions pures
d'injection + un tableau graphique canvas nourri par
/api/market/summary.

## 2. Ce qui est figé (`tests/test_home_art_lot181.py`, 8 tests)

```text
Injection pure — apply() injecte <style>+<script> UNE fois juste
  avant </body>, contenu intact ; page sans </body> → no-op
  silencieux (jamais une exception ni un doublon) ; apply_desk() →
  CSS SEUL, aucun <script> ajouté au Trading Desk
Syntaxe JS RÉELLE — ART_JS validé par `node --check` (règle
  critique n°2 : deux SyntaxError silencieuses ont déjà vécu dans
  des chaînes JS générées depuis Python — désormais un vrai parseur
  garde cette couche)
Progressive enhancement — sans IntersectionObserver → catch qui rend
  tout visible ; sans #ovMarket → arrêt propre ; reduced-motion
  respecté dans les DEUX CSS
Contrat de données — fetch('/api/market/summary'), rafraîchi toutes
  les 90 s SEULEMENT onglet visible (pas de fetch caché) ; chiffres
  localisés fr-FR ; bandes NARRATIVES du VIX ≤14 serein / ≥22 stress
  (distinctes des bandes de données 16/22 du moteur, lot 153) ;
  VIX absent → tiret honnête
Câblage réel — artBoard présent dans PAGE_DAILY (apply effectif),
  DESK_CSS dans PAGE_STRATEGIE, et le desk reste SANS artBoard
```

## 3. Preuves

```text
python -m pytest tests/test_home_art_lot181.py -q → 8 passed
python -m pytest tests/ -q → 2424 passed, 2 skipped (2416 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 182 : poursuivre les couches UI vivantes non gardées — candidats
au survey : sync_center (108 l, 1 mention), vault (301 l, 1),
tracking_page (69 l, 1), ou design_system_page (254 l, 0 — vérifier
si servie). MINI-BILAN au lot 185.
