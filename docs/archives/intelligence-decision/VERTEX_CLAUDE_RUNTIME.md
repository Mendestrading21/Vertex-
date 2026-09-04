# Vertex — Runtime Claude

Intégration API séparée de Claude Code : `vertex/ai/`
(provider.py interface · anthropic_provider.py · fallback.py déterministe ·
tool_registry.py whitelist+denylist · response_validator.py schéma strict ·
prompt_builder.py + strategy_context.py contexte · health.py santé ·
audit.py trace).

Claude PEUT : expliquer, résumer, comparer, rédiger le Brief, analyser une
entreprise/position, avocat du diable, proposer une alerte ou une règle
(proposition seulement). Claude NE PEUT PAS : passer un ordre (registre
sans outil d'ordre — `test_ai_registry_has_no_order_tool`), produire seul
un calcul financier, inventer une donnée (validation stricte), modifier la
constitution, activer une règle, supprimer l'historique, remplacer une
décision déterministe.

Indisponible → repli déterministe étiqueté, statut visible, zéro page
cassée (`test_claude_outage_uses_fallback`).
