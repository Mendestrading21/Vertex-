# SKYLER V2 — LOT 182 : gardien global de syntaxe JS (règle critique n°2)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-182`
(base : `integration/vertex-skyler-v2` @ `1e9c69f`, lot 181 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey honnête : tracking_page, vault et sync_center ont déjà leurs
gardiens de CONTENU (full_system_integration, test_vault,
live_engine). La lacune TRANSVERSE : la règle critique n°2 (« tout
JS généré depuis Python doit être valide — deux SyntaxError
silencieuses ont déjà vécu ») n'était gardée que ponctuellement
(home_art au lot 181). Ce lot la SYSTÉMATISE : chaque bloc <script>
inline de chaque route HTML servie passe au vrai parseur.

## 2. Ce qui est figé (`tests/test_js_syntax_sweep_lot182.py`, 6 tests)

```text
Balayage — les 16 routes HTML canoniques ('/', markets,
  opportunities, portfolio, journal, options, system, tracking,
  intelligence, titre/AAPL, company/AAPL, analysis/AAPL, login,
  widget-lab, design-system ×2) répondent TOUTES 200 ; chaque bloc
  <script> inline de chaque page est validé par node --check —
  0 erreur de syntaxe tolérée (une apostrophe française non
  échappée fait désormais échouer la suite)
Anti-vide — le balayage exige ≥ 12 blocs réellement contrôlés : si
  l'extraction cassait (regex, refonte), le gardien ne pourrait pas
  passer en silence sans rien vérifier
Chaînes module — sync_center.JS et le _HEATMAP_JS du vault validés
  AVANT injection
Gardien du gardien — l'extracteur ignore <script src=> et les blocs
  type json, garde l'inline exécutable (testé unitairement)
Constat : les 9+ blocs actuellement servis parsent tous — l'état
  présent est sain, le gardien empêche la régression
```

## 3. Preuves

```text
python -m pytest tests/test_js_syntax_sweep_lot182.py -q → 6 passed
python -m pytest tests/ -q → 2430 passed, 2 skipped (2424 + 6)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 183 : candidats — vx_kit (314 l, 2 mentions), pages legacy non
routées de terminal.py (PAGE_ME/PAGE_VAULT : vérifier vie ou mort),
ou nouvelle direction au survey. MINI-BILAN 181-185 au lot 185.
