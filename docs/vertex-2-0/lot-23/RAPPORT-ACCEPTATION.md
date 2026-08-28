# Lot 23 — Acceptation finale (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`
Base de mesure : commit précédant ce rapport (voir git log).

## Batterie exécutée (preuves jointes)

| Contrôle | Résultat |
|---|---|
| `python -m compileall terminal.py vertex` | OK |
| Suite complète (`pytest -q`) | **4373 passés · 153 ignorés · 0 échec** (135 s) |
| `tests/test_no_orders.py` | 3 passés |
| `check_ibkr_boundary.py --enforce` | **code 0** — frontière market-data-only tenue (`frontiere-ibkr.txt`) |
| `audit_claude_surface.py` | **code 0** — autorité unique du skill (`surface-claude.txt`) |
| `audit_runtime.py --enforce-target` | **code 0** — 12 pages 200, zéro collision, routeur chargé (`audit-runtime.txt`) |
| Navigateur (phase D) | 12 pages × 7 largeurs : 0 hscroll, 0 erreur console, client-log vide ; clavier/skip-link/reduced-motion/zoom 200 % OK |

## Ce que le programme a livré (lots 0 → 23)

- **Phase A/B (lots 0-10)** : checkpoint graphique fusionné proprement,
  frontière IBKR 13→0 appels sensibles, exposition refusée par défaut,
  enveloppe de provenance 1.1 (17 champs), stale-while-revalidate desk,
  état SILENCIEUX des jobs, p99, zéro collision de route, façade
  `AdviceEngine.evaluate` (autorité de conseil unique).
- **Phase C (lots 11-13)** : porte IA partagée (budget de débit + audit +
  repli honnête) sur copilote/briefs/enrichissement ; entonnoir
  point-in-time avec gates canoniques, dedup, budgets, delta ; contrats
  StrategySpec/StrategyEvidence + manifeste de replay haché + séparation
  labo ⟂ conseil (gardiens AST) ; accord inter-moteurs BS verrouillé à
  1e-9 + devise déclarée.
- **Phase D (lots 14-21)** : 12 pages vérifiées contre le blueprint au
  navigateur réel — 7 défauts d'honnêteté trouvés et corrigés (jeton
  'unavailable' fuité, carte « Ce qui a changé » morte, delta entonnoir
  non affiché, [object Object], badge santé sur-affirmant, légende
  treemap, violet hors options) — chacun avec banc né rouge, bump SW
  (v264→v267) et vérification en direct.
- **Phase E (lot 22)** : manifeste de nettoyage avec preuves — RIEN
  supprimé sans autorisation.

## Écarts / réservés à la décision humaine (l'acceptation n'est PAS déclarée)

1. **Vérification sur données peuplées** : cet environnement n'a pas de
   réseau sortant — toutes les vues ont été vérifiées en mode dégradé
   honnête. Repasser les pages sur un scan réel.
2. **Lighthouse budgets** : non exécutables ici.
3. **Audit-150 exhaustif** : les familles couvertes par la batterie
   ci-dessus sont OK avec preuve ; le passage formel des 150 contrôles
   sur données réelles reste à faire à l'acceptation humaine.
4. **Nettoyages** (lot 22) et **tranches GitHub A/B/C** (lot 0) : en
   attente d'autorisation explicite.
5. **PR** : les PR #838 et #839 restent en brouillon ; la branche
   d'intégration `agent/vertex-2-0-integration-20260828` porte tout le
   programme. Aucune fusion automatique — validation humaine du commit
   candidat obligatoire.

## Dettes consignées (explicites, pas absorbées)

Refonte de la file worker IBKR unique ; retrait des paramètres
`ibkr_positions` des signatures desk ; strangler terminal.py (~7000
lignes) ; minimisation PII des prompts IA (contrat gateway complet) ;
persistance du registre d'essais (ADR) ; renommage
chart-theme-obsidian-copper.js ; corrections de multiplicité des essais.
