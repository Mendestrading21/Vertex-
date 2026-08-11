# SKYLER V2 — LOT 83 : boucle continue — tri/filtres/contrôles interactifs

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-83-controles`
(base : `integration/vertex-skyler-v2` @ `56bebfd`, fraîchement fetchée).

## 1. Méthode (Playwright, cliqué en vrai, publié)

Sur 8 pages/vues (/markets, /opportunities ×4 vues, /portfolio,
/options, /journal) : chaque contrôle interactif est CLIQUÉ et son effet
VÉRIFIÉ — en-têtes de tri (l'ordre des lignes doit réellement changer,
double-clic testé pour l'inversion), onglets/segmented controls de vue
(URL ou état actif aria-selected/classe doit basculer, re-localisés à
chaque tour car la navigation SPA détruit le contexte), selects visibles
(le contenu doit réagir).

## 2. Résultat : 26 contrôles testés — 0 inerte, 0 erreur console

Aucun contrôle qui « ne fait rien », aucun qui casse. Les tableaux
trient, les vues basculent avec leur état visuel, les selects réagissent.
**SAIN — lot documentaire.**

Outillage versionné : `tools/controls_audit.js` (rejouable — complète
tools/rc_short_audit.js et tools/user_journeys.js).

## 3. Preuves

```text
python -m pytest tests/ -q → 1720 passed, 2 skipped   (baseline tenue)
tools/controls_audit.js → 26 contrôles, 0 défaut, 0 erreur console
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

Pas de bump SW ni de nouveau test pytest : aucun changement de code
produit (lot d'audit pur, outil versionné).

## 4. Suite

Lot 84 : angle suivant le plus porteur ; au lot 85, mini-bilan 81-85.
