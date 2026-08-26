---
name: vertex-maximum
description: Documentation opérationnelle durable de Vertex — vision produit, design system, chart system, contrat de données IBKR, règles trading, méthode d'audit, ordre des lots et critères de validation. À lancer pour tout travail d'audit ou de refonte structurante de Vertex.
argument-hint: "[phase, page, moteur ou contrainte]"
disable-model-invocation: true
---

# VERTEX MAXIMUM — cerveau opérationnel de la refonte

Vertex est **l'ordinateur de décision situé AU-DESSUS d'Interactive Brokers** : IBKR détient les comptes,
positions, ordres et données ; Vertex centralise, vérifie la qualité, analyse, détecte le risque, identifie
les opportunités, construit les scénarios, **recommande** les décisions, **prépare** les ordres, mesure les
résultats, apprend, et **explique chaque décision de façon auditable**.

> ⛔ **INVARIANT ABSOLU — LECTURE SEULE.** Vertex ne passe **JAMAIS** d'ordre (ni live, ni paper). `READONLY=True`
> (`vertex/app/config.py`), `readonly=True` sur les 4 workers IBKR, 17 outils d'ordre interdits dans le registre
> IA (`vertex/ai/tool_registry.py`), tests gardiens. Le « Desk / Exécution » de Vertex est un centre de
> **PRÉPARATION + simulation + contrôles pré-trade** : il calcule sizing, perte max, impact marge/risque, greeks,
> et produit un **ticket prêt-à-coller dans TWS**. L'humain transmet manuellement dans IBKR. Aucune régression de
> cet invariant n'est acceptable.

## À lire AVANT toute action
- `CLAUDE.md` (règles critiques : 4 listes desk-sync, apostrophes JS, bump SW, données réelles, sanitize news).
- Ce skill : `references/*` (vision, IA, design, charts, données IBKR, règles trading, checklist, DoD, QA).
- `.claude/rules/*` (design, intégrité des données, édition sûre).
- Contrats existants : `docs/claude/VERTEX_CHART_CONTRACT.md`, `VERTEX_GLASS_VISUAL_CONTRACT.md`,
  `VERTEX_PAGE_MATRIX.md`, `VERTEX_REFACTOR_RULES.md`, `VERTEX_ACCEPTANCE_CHECKLIST.md`.
- Audit vivant : `docs/vertex-audit/` (repo map, IA, audits, architecture cible, roadmap, matrice de pages).

## Vision produit — la boucle de décision
Toute page participe à : **OBSERVER → COMPRENDRE → DÉTECTER → ÉVALUER → DÉCIDER → EXÉCUTER(=préparer) →
SURVEILLER → MESURER → APPRENDRE.** Une information ne s'affiche jamais « parce qu'elle est disponible » : elle
répond à une question précise (que se passe-t-il ? pourquoi ? quelle exposition ? quel risque ? quelle
opportunité ? quelle décision ? quelle confiance ? quel scénario défavorable ? quelle taille ? quand sortir ?
qu'est-ce qui invalide la thèse ? quel résultat ? qu'apprend Vertex ?). Détail : `references/product-vision.md`.

## Architecture RÉELLE (ne pas supposer un frontend React)
- **Stack** : Python 3.11 / Flask. Monolithe `terminal.py` (~10,8k lignes, HTML+JS construits en chaînes
  Python) + package `vertex/` : `engines/`, `options/`, `market/`, `quant/`, `ai/`, `app/routes/` (blueprints),
  `app/state.py` (`scan_state` muté en place), `ui/pages/` (pages extraites), `data_sources/`, `data/`,
  `services/`, `portfolio/`, `scheduler/`, `observability/`. Statiques : `vertex/static/vertex/` (CSS `glass.css`
  chargé en dernier ; JS `charts/chart-core.js` → `window.VXCharts` ; `vx-core.js` → `window.VX`).
- **Design system** = variables CSS `--vx-*` (glass.css) + variantes de carte `vx-card` + `VX.fmt.*`
  (formats). PAS de composants React. Détail : `references/design-system.md`.
- **Chart system** = primitives `VXCharts.*` (une seule bibliothèque). Détail : `references/chart-system.md`.
- **Moteurs** = pipeline déterministe raw→signaux→scores→scénarios→recommandations (jamais → ordre). Détail :
  `references/trading-domain-rules.md`.
- **IBKR** = 4 workers `readonly=True`, états live/delayed/stale honnêtes. Détail : `references/ibkr-data-contract.md`.
- Index complet des routes/pages : `references/information-architecture.md` + `docs/vertex-audit/01-repository-map.md`.

## Méthode de travail (non négociable)
1. **Comprendre avant de modifier** : lire le vrai code, ne rien réécrire aveuglément, ne rien supprimer sans
   avoir compris objectif/dépendances/consommateurs.
2. **Par lots vérifiables** : un lot = un problème ciblé → fichiers → approche → implémentation limitée →
   `pytest` 100 % → app relancée → vérification visuelle (vrai navigateur, 0 erreur console, `/api/client-log`=0)
   → correction des régressions → mise à jour de l'audit → rapport (`templates/implementation-report-template.md`).
3. **Preuves, jamais d'affirmation** : « terminé » exige tests verts + captures + routes vérifiées.
4. **Ne jamais mélanger** dans un lot : refonte globale + logique trading + migration données + connexion IBKR +
   nettoyage sans rapport. Commits atomiques (`audit(vertex):`, `refactor(ui):`, `feat(portfolio):`, `fix(ibkr):`…).
5. **Definition of Done par page** : `references/page-definition-of-done.md`.
6. **Anti-fausse-fonctionnalité** : aucun bouton sans handler, lien `#`, faux statut live, graphe décoratif,
   filtre qui ne filtre pas, fallback mock silencieux. Démo → étiquetée `DÉMO/MOCK/SIMULATED`.

## Ordre des lots (adapté à la réalité — beaucoup existe déjà : consolider/combler/polir)
Phase 0 Sécurisation → Phase 1 Audit (`docs/vertex-audit/`) → Phase 2 Fondations (tokens/formats/cartes/charts
partagés) → Phase 3 Shell (nav/header/statut IBKR/recherche) → Phases 4-13 page par page (Dashboard, Portefeuille,
Opportunités, Analyse, Options, Desk=prep/sim, Performance, Intelligence, Journal, Events, Watchlist, Settings) →
Phase 14 Validation finale. Détail et priorisation : `docs/vertex-audit/14-prioritized-roadmap.md`.

## Sous-agents & règles
- Auditeurs : `.claude/agents/vertex-{product,ui,trading,ibkr,qa,performance}-auditor.md` (lecture/recherche
  uniquement, jamais d'ordre) — pour l'audit ET les revues de lot.
- Règles : `.claude/rules/vertex-{design,data-integrity,safe-editing}-rules.md`.
- Skills de refonte par espace existants (CONSERVÉS, complémentaires) : `.claude/skills/vertex-redesign-*`.

## Vocabulaire canonique (cohérence sémantique — §27)
signal (observation) ≠ recommandation (signaux + contraintes) ≠ décision (recommandation validée) ≠ ordre
(instruction, JAMAIS transmise par Vertex). opportunité · position · stratégie · scénario · risque · confiance ·
score · statut. Un même concept = un même mot partout (code, UI, docs). Table : `references/product-vision.md`.

## Vérification transverse
`python -m pytest tests/ -q` (100 %) · `GET /healthz` · `GET /api/client-log` (=0) · `GET /api/system/connections`
(honnête) · `GET /api/live/status`. Serveur démo : `DEMO=1 NO_IBKR=1 python terminal.py`.
