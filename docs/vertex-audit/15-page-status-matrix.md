# 15 — Matrice de statut des pages

Statuts : ✅ conforme · 🟡 à polir (dette identifiée) · 🔴 problème structurant · ⬜ non encore audité en détail.
Colonnes = axes de la Definition of Done (`references/page-definition-of-done.md`). Mise à jour à chaque lot.

| Espace / route | Question claire | Données réelles + provenance | États vide/erreur | 0 fausse fonction | Design unifié (card/charts) | A11y AA | Tests + capture | Statut |
|---|---|---|---|---|---|---|---|---|
| Dashboard `/` | ✅ | 🟡 (DAT-03) | 🟡 | ⬜ (FCT-01) | 🟡 (CMP-02) | 🟡 (A11Y-01) | 🟡 | 🟡 |
| Opportunités `/opportunities` | ✅ | 🟡 | 🟡 | ⬜ (FCT-01 filtres) | 🟡 | 🟡 | 🟡 | 🟡 |
| Portefeuille `/portfolio` | ✅ | 🔴 (DAT-01/03 provenance) | 🟡 | ⬜ | 🟡 (CMP-02) | 🟡 | 🟡 | 🟡 |
| Analyse `/analysis/<sym>` | ✅ | 🟡 | ✅ (vides corrigés) | 🟡 | 🟡 | 🟡 | 🟡 (payload 8 Mo, PRF-01) | 🟡 |
| Options `/options` (+`/<sym>`) | ✅ | 🟡 (greeks étiquetés ✅) | 🟡 | 🔴 (RT-01 route) | 🟡 (violet=options ✅) | 🟡 | 🟡 | 🔴 |
| Performance `/performance` | ✅ | 🟡 | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Intelligence `/intelligence` | ✅ | 🟡 | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Système `/system` | ✅ | ✅ (statut socket honnête) | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Shell (transverse) | ✅ | — | — | 🔴 (IA-01 double nav, CMP-03) | 🔴 (sidebar orange inline) | 🟡 | 🟡 | 🔴 |
| Préparation (prep/sim) | ⬜ à créer | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Lecture
- **🔴 prioritaires** : Shell (IA-01/CMP-03), Options (RT-01), Portefeuille (provenance/0-masquerade).
- **🟡 majoritaire** : base fonctionnelle saine, dette de cohérence (cards/charts/provenance/a11y) à résorber par lots.
- **⬜ Préparation** : nouveau sous-espace à bâtir en lecture seule (sizing/perte max/ticket), Phase 4-13.

Détail par page à produire dans `docs/vertex-audit/pages/<route>.md` au fil de l'implémentation.
