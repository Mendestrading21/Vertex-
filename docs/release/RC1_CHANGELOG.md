# Vertex — RC1 Changelog

> Branche `agent/vertex-total-rebuild` · base `origin/main` (`2b4fa70`, **jamais
> modifié**). Refonte produit totale en 7 PR + stabilisation RC1. Aucun moteur
> financier modifié pour l'esthétique ; IBKR READONLY strict de bout en bout.

## Gouvernance (fondations)
- **Constitution** (`VERTEX_CONSTITUTION.md`) — 26 lois immuables + priorité
  documentaire.
- **Product Bible** (`VERTEX_PRODUCT_BIBLE.md`) — storyboard, wireframes, composants,
  états, couleurs, typographie, accessibilité des 8 espaces.
- **Product Experience Review** (`PRODUCT_EXPERIENCE_REVIEW.md`) — revue produit.

## PR n°1 — Hygiène & identité (`f578f9f`, `3da17d1`, `ee824c5`, `9f707e2`, `1421c79`)
Untrack des données runtime, identité OBSIDIAN COPPER, palette source unique,
data-quality démo étiquetée, décision « données insuffisantes » honnête, débordement
mobile supprimé. SW → v43.

## PR Design n°1 — Design system (`2281e25`)
Typographie officielle (Inter + JetBrains Mono), **Chart Shell canonique**,
composants premium (Verdict/Scénario/Freshness/Insufficient), DATA_INSUFFICIENT.

## PR n°2 — Navigation (`992a497`)
**8 espaces canoniques** (Aujourd'hui · Marchés · Opportunités · Analyse ·
Portefeuille · Options · Journal · Système), registre unique, redirections legacy,
route `/journal`, Options standalone. SW → v45.

## PR n°3 — Aujourd'hui + Marchés (`640c743`)
Aujourd'hui **résume** (Hero éditorial + 4 KPI + Diff honnête), Marchés **explique** ;
**30 → 15 graphiques** (−50 %), déduplication. SW → v46.

## PR n°4 — Opportunités + Analyse (`08f4d74`)
Hero éditorial + `op-radar → op-scatter` ; **Carte-Verdict** + **Carte-Scénario** +
**raisonnement du comité** ; parcours opportunité → thèse en **1 clic**. SW → v47.

## PR n°5 — Portefeuille (`f474241`)
**Synthèse** premier écran (Hero + risque dominant + action + Diff) ; **tableau
canonique** avec **état de thèse** ; **garde-fou perdants** (testé) ; concentration
S+/S/A/B ; **performance migrée** depuis Journal (domicile unique). SW → v48.

## PR n°6 — Options (`3bbc378`)
**Carte-Verdict d'asymétrie** + Carte-Scénario + **payoff canonique** (`multileg_lab`,
moteur unique) + **Greeks interprétés** + **LEAPS explicable** + positions canoniques +
garde-fou perdants. **Correction de calcul prouvée** : IV %→décimale (PoP 100 %→22 %,
delta saturé→54). SW → v49.

## PR n°7 — Journal + Système (`4b98726`)
Journal = **discipline uniquement** (Hero éditorial honnête + KPI comportementaux +
hypothèses + progression + biais) ; Système = **Hero technique cockpit** de confiance.
SW → v50.

## Stabilisation RC1
Gel fonctionnel ; audit du code mort (avec preuve) ; cartographie + extraction à faible
risque de `terminal.py` ; consolidation composants ; inventaire routes/API + gardien
READONLY ; mesures de performance ; audit accessibilité ; validation responsive
390/768/1024/1440/1920 ; audit sécurité ; cohérence éditoriale FR ; documentation de
release. **Aucune nouvelle fonctionnalité.**

## Chiffres clés
- Tests : **952** collectés (100 % verts).
- Graphiques inter-pages : **−50 %** sur Aujourd'hui+Marchés.
- Service worker : **v50**.
- IBKR : `readonly=True` codé en dur ; **0 endpoint d'ordre**.
