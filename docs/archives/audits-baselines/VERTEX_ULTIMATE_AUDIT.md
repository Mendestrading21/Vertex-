# Vertex Ultimate Institutional OS — Audit

Audit du 2026-07-11 sur l'état post-Experience-OS (543 tests verts).
Chaque constat est suivi de la décision. Les audits précédents
(`VERTEX_FULL_AUDIT.md`, `VERTEX_UI_V3_AUDIT.md`) restent valides pour
l'historique ; ne sont listés ici que les écarts vs la présente spec.

## A. Écarts stratégiques (violations de la constitution cible)

1. **R:R minimal à 1.5 au lieu de 2:1** (`contract_scorer.MIN_REWARD_RISK`)
   et **aucun hard gate R:R < 2 dans l'ExecutiveEngine** (l'asymétrie ne
   fait que pondérer le score). → CORRIGER : gate bloquant ACHETER/
   RENFORCER si `reward_risk < 2`, constante alignée, test
   `test_rr_gate_is_two`.
2. **Régime UNKNOWN n'interdit pas le risque neuf** : la table
   d'ajustements laisse `new_risk_allowed: True` par défaut → l'UI
   affichait « Nouveau risque : autorisé » avec confiance 0 % et
   0 dimension. → CORRIGER : UNKNOWN (et confiance insuffisante) →
   BLOQUÉ + priorité ATTENDRE + décision max ATTENDRE ; test
   `test_unknown_regime_blocks_risk`.
3. **Compteurs options non séparés** : l'UI affiche « Options X/3 » sans
   distinguer CALLS et PUTS tactiques (max 1 PUT). → CORRIGER (header
   portefeuille + Options Command Center) ; tests
   `test_calls_and_puts_counts_are_explicit`, `test_tactical_put_limit`.

## B. Intégrations & runtime

4. **Pas de séquence de démarrage formalisée** : les vérifications de
   connexions existent éparses (`/api/live/status`, diagnostics) mais pas
   de startup report ordonné (config → Claude → IBKR → TV → stockage →
   moteurs → scheduler → live). → CRÉER `vertex/services/startup.py` +
   affichage Système.
5. **`.env.example` incomplet** vs §11 (manquent ANTHROPIC_MODEL,
   IBKR_HOST/PORT/CLIENT_ID/ACCOUNT_ID/MARKET_DATA_MODE,
   TRADINGVIEW_DEFAULT_TIMEFRAME, VERTEX_TIMEZONE, MARKET_TIMEZONE,
   VERTEX_READONLY). → COMPLÉTER + validation
   CONFIGURED/MISSING/INVALID.
6. **vertex/ai** : broker/outils/schéma existent mais pas la façade
   provider unique (`provider.py`, `claude_provider.py`,
   `fallback_provider.py`, `health.py`, `context_builder.py`). → CRÉER en
   enveloppant l'existant (aucune régression du repli déterministe).
7. **Pas de flux temps réel** : uniquement polling par page (refresh
   manager). → CRÉER SSE `/api/live/events` + client reconnect
   (Last-Event-ID) + repli polling.
8. **Boucles de fond non inventoriées** : scan loop, évaluation d'alertes,
   backup quotidien vivent dans terminal.py sans registre. → CRÉER
   `vertex/scheduler/` (registre de jobs nommés, statut, dernière/
   prochaine exécution) + vue Système/Automatisations.

## C. Contenu

9. **Le Brief n'utilise pas les actualités réelles** : `/news-feed`
   (assaini serveur) est orphelin ; le brief éditorial est purement
   moteur. → CRÉER `vertex/market/{news_pipeline,news_dedup,news_impact,
   daily_brief}.py` : ingestion du flux existant, déduplication,
   classification, entités, impact, brief PRE_MARKET/INTRADAY/CLOSE/
   WEEKLY 150-280 mots + version compacte, chaque événement sourcé —
   **rien d'inventé, aucun événement non confirmé**.
10. **Pas de jumeau analytique entreprise** : profil + fondamentaux
    existent (`vertex/data/company.py`, `data_sources/fundamentals.py`)
    sans façade ni détection de changement. → CRÉER `vertex/companies/*`
    en enveloppant l'existant + `change_detector` (snapshot → diff →
    recalcul décision).
11. **Aucune analyse par position option** : le portefeuille liste les
    options mais sans page/drawer dédié (identité, marché, Greeks, vol,
    plan, événements, décision analytique, graphiques). → CRÉER (§20-21)
    sur les moteurs existants (`scenario_pricer`, `vol_surface`,
    chain IBKR quand disponible ; absent → « — » expliqué).
12. **Pas de comparateur de contrats** : le sélecteur retourne les
    catégories mais l'UI n'offre pas la comparaison 3 contrats
    (compromis/défensif/explosif) avec dominance expliquée. → CRÉER (§22).

## D. Design

13. **Le bleu reste identitaire** : liens `a{color:var(--vx-info)}`
    (#4ca6ff), série graphique n° 2 bleue, classe `.vx-info`. → Obsidian
    Copper Deep : liens cuivre, aucune série principale bleue, `--vx-info`
    re-mappé cuivre clair ; tests `test_no_blue_primary_theme`,
    `test_no_blue_primary_buttons`, `test_no_blue_main_series`.
14. **Palette V3 orange vif** (#f68a3c) → Obsidian Copper Deep : fonds
    obsidienne/graphite plus profonds, orange brûlé 950-400, cuivre,
    états atténués (#38b879/#dc5f52/#ce8a29), option violet sombre
    #85609f.
15. **États vides** : bornés à 240 px (V3) — la spec resserre
    (compact 120 / standard 170 / héro 220) avec raison + dépendance +
    action + dernière donnée valide. → AJUSTER.

## E. Ce qui est déjà conforme (ne pas retoucher)

READONLY en dur + gardiens d'appels ; webhook TV complet ; provenance
canonique ; moteur de décision unique déterministe ; scénarios options
spot×temps×IV ; 42 redirections ; sync 17 clés ; télémétrie 0-erreur ;
responsive 7 viewports ; accessibilité (focus trap, aria, reduced-motion).
