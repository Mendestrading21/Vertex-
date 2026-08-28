# Lot 11 — Gateway IA unique (WORK_MANIFEST)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Objectif unique

Toute sortie IA (copilote, briefs, enrichissement) passe par les gardes
partagées déjà prouvées dans `investment_agent` : **limite de débit** +
**journal d'audit** + **repli déterministe honnête**. Aucun appel Anthropic
direct sans porte.

## Constat mesuré (audit préalable)

| Surface | Fichier | Appel | RateLimiter | AIAudit | Fallback |
|---|---|---|---|---|---|
| Agent d'analyse | `vertex/ai/investment_agent.py` | via AIProvider | ✅ | ✅ | ✅ |
| Copilote | `vertex/ai/copilot.py:138-145` | `Anthropic()` direct | ❌ | ❌ | ✅ `_fallback` |
| Briefs (news/profil/desc) | `vertex/ai/briefs.py` ×3 | `Anthropic()` direct | ❌ | ❌ | ✅ (Google/texte source) |
| Enrichissement web | `vertex/ai/enrichment.py` → `web_provider` | `messages.create` | ❌ | ❌ (santé seulement) | ✅ `prov.absent` |

Le plus exposé : le copilote — un appel Claude par clic utilisateur
(`POST /api/copilot/ask`), sans limite ni journal.

## Fichiers propriétaires du lot

- **NEUF** `vertex/ai/gateway.py` — porte partagée : budgets de débit par
  famille d'appel + enregistrement AIAudit + `reset_for_test()`.
- `vertex/ai/copilot.py` — passage par la porte (refus → repli déterministe
  étiqueté honnêtement, jamais une 500).
- `vertex/ai/briefs.py` — les 3 sites (`fr_news`, `company_brief`, `fr_desc`)
  passent par la porte ; refus → chemin non-IA existant.
- `vertex/ai/enrichment.py` — `run()` consomme le budget par appel de
  recherche ; budget épuisé → surface `absent` honnête + erreur consignée.
- **NEUF** `tests/test_gateway_ia_lot11.py` — bancs rouges d'abord.

## Contrat de données

- Aucun changement de schéma de réponse ; seuls les libellés de repli disent
  la vraie raison (« limite d'appels IA atteinte » ≠ « Claude non configuré »).
- Budgets par famille (fenêtre 60 s, par processus) : copilote 10,
  briefs 30, enrichissement 60 (un run complet = 24 titres × 2 = 48 appels).
- La porte n'est consultée QUE si `available()` est vrai : sans clé, zéro
  consommation, chemins actuels intacts.

## Hors périmètre (consigné, pas absorbé)

Schéma strict/citations/redaction/consentement du contrat gateway complet ;
minimisation PII des prompts (dette consignée lot 10) ; `web_provider` reste
le transport, la porte se tient dans `run()`.

## Rollback

`git revert` du commit du lot — aucun état persisté nouveau, aucun schéma
migré.
