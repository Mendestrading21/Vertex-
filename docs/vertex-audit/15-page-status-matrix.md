# 15 — Matrice de statut des pages

Statuts : ✅ conforme · 🟡 à polir (dette identifiée) · 🔴 problème structurant · ⬜ non encore audité en détail.
Colonnes = axes de la Definition of Done (`references/page-definition-of-done.md`). Mise à jour à chaque lot.

| Espace / route | Question claire | Données réelles + provenance | États vide/erreur | 0 fausse fonction | Design unifié (card/charts) | A11y AA | Tests + capture | Statut |
|---|---|---|---|---|---|---|---|---|
| Dashboard `/` | ✅ | 🟡 (DAT-03) | 🟡 | ⬜ (FCT-01) | 🟡 (CMP-02) | 🟡 (A11Y-01) | 🟡 | 🟡 |
| Opportunités `/opportunities` | ✅ | 🟡 | 🟡 | ⬜ (FCT-01 filtres) | 🟡 | 🟡 | 🟡 | 🟡 |
| Portefeuille `/portfolio` | ✅ | 🟡 (DAT-03 provenance ; DAT-01 révisé P2) | 🟡 | ⬜ | 🟡 (CMP-02) | 🟡 | 🟡 | 🟡 |
| Analyse `/analysis/<sym>` | ✅ | 🟡 | ✅ (vides corrigés) | 🟡 | 🟡 | 🟡 | 🟡 (payload 8 Mo, PRF-01) | 🟡 |
| Options `/options` (+`/<sym>`) | ✅ | 🟡 (greeks étiquetés ✅) | ✅ (état vide honnête vérifié) | ✅ (RT-01 résolu) | 🟡 (violet=options ✅) | 🟡 | ✅ (919 + DEMO) | 🟡 |
| Performance `/performance` | ✅ | 🟡 | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Intelligence `/intelligence` | ✅ | 🟡 | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Système `/system` | ✅ | ✅ (statut socket honnête) | 🟡 | ⬜ | 🟡 | 🟡 | 🟡 | 🟡 |
| Shell (transverse) | ✅ | — | — | 🔴 (IA-01 double nav, CMP-03) | 🔴 (sidebar orange inline) | 🟡 | 🟡 | 🔴 |
| Préparation (prep/sim) | ⬜ à créer | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Lecture
- **🔴 prioritaire restant** : Shell (IA-01 double nav + CMP-03 sidebar orange inline). Options (RT-01) ✅ résolu ;
  Portefeuille repassé 🟡 (DAT-01 révisé P2 après vérif ; reste DAT-03 provenance).
- **🟡 majoritaire** : base fonctionnelle saine, dette de cohérence (cards/charts/provenance/a11y) à résorber par lots.
- **⬜ Préparation** : nouveau sous-espace à bâtir en lecture seule (sizing/perte max/ticket), Phase 4-13.

Détail par page à produire dans `docs/vertex-audit/pages/<route>.md` au fil de l'implémentation.
