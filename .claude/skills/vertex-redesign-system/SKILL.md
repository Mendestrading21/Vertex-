---
name: vertex-redesign-system
description: Planifier puis exécuter la refonte Black Glass du command center Système Vertex.
argument-hint: "[connections | data | automations | settings | archive | design-system | tout]"
disable-model-invocation: true
---

# Refonte Système

Lire `CLAUDE.md`, le plan directeur et les contrats `docs/claude/`.

Demande :

> $ARGUMENTS

## Cible

- route : `/system`
- fichier : `vertex/ui/pages/system_page.py`
- vues : connections, data, automations, settings, archive ;
- page QA : `/design-system`.

## Mission

Créer un command center honnête de santé, connexions, fraîcheur, jobs, préférences et stockage.

## Points obligatoires

- afficher READONLY et preuve réelle de connexion ;
- configuré ≠ connecté ; jamais LIVE sans preuve socket ;
- connections : IBKR, TradingView, Claude, sync, stockage et moteurs ;
- data : qualité, fraîcheur, dernier scan, domaines et titres dégradés ;
- automations : jobs, priorité, dernier/prochain run, erreurs et startup report ;
- settings : densité, sidebar, notifications, export/import, langue et sécurité ;
- archive : coffre, recherche, tags, création, export et sync ;
- ne jamais exposer de secret ;
- mettre `/design-system` à jour comme QA vivante du Black Glass ;
- bump du service worker obligatoire après changement visible.

## Validation

IBKR off/on, TradingView non configuré/configuré/actif, Claude absent/présent, données stale, import/export, archive vide, responsive, console et tests.
