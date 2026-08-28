# Lot 11 — Gateway IA unique (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Livré

Toute sortie IA passe désormais par une porte partagée
(`vertex/ai/gateway.py`) : budget de débit par famille d'appel + journal
d'audit commun (`vertex.ai.audit.AUDIT`) + repli déterministe honnête.

| Surface | Avant | Après |
|---|---|---|
| Copilote (`/api/copilot/ask`) | `Anthropic()` direct, ni limite ni audit | porte `copilot` (10/60 s) ; succès, panne et réponse vide audités (durée, modèle) ; refus → repli étiqueté « limite d'appels IA atteinte » (plus jamais le mensonge « configure la clé » quand la clé existe) |
| Briefs ×3 (`fr_news`, `company_brief`, `fr_desc`) | 3 appels directs | porte `briefs` (30/60 s) via `_appel_claude` ; refus → chemin non-IA existant (Google gratuit / texte source / `{}`) |
| Enrichissement (`run()`) | recherches non bornées, santé seulement | porte `enrichment` (60/60 s — un run complet 24×2=48 tient entier) ; budget épuisé → `prov.absent('budget IA atteint')` + erreur consignée, jamais un chiffre |
| Agent d'analyse | déjà gardé (référence) | inchangé |

## Preuves

- `tests/test_gateway_ia_lot11.py` : 10 bancs **nés rouges** (ImportError :
  la porte n'existait pas) → verts. Couvrent : budgets indépendants, refus
  journalisé, copilote refusé sans atteindre Anthropic (`_ClientInterdit`
  lève si appelé), succès/panne audités, briefs repliés sans appel,
  enrichissement absent honnête + erreurs `rate_limited`.
- Suite complète : **4331 passés · 153 ignorés · 0 échec** (130 s).
- Runtime sans clé : `POST /api/copilot/ask` → 200, `source=deterministic`,
  libellé inchangé, **zéro consommation de porte** (consultée seulement si
  `available()`).

## Contrats

- Aucun schéma de réponse modifié ; seuls les libellés de repli disent la
  vraie raison. Aucun état persisté nouveau. Pas de changement de shell → pas
  de bump service worker.
- `gateway.status()` disponible (lecture seule) pour la page Système —
  branchement UI non inclus (hors périmètre du lot).

## Limites consignées (dette explicite, pas absorbée)

- Le contrat gateway complet (schéma strict, citations, redaction,
  consentement, cancellation, manifeste de troncature) reste à couvrir —
  ce lot livre budget + audit + repli, les deux gardes mesurées manquantes.
- Minimisation PII des prompts copilote (positions desk dans le contexte
  JSON) : dette déjà consignée au lot 10, à traiter avec le contrat complet.
- `web_provider` reste le transport nu ; la porte se tient dans `run()`.

## Rollback

`git revert` du commit du lot.
