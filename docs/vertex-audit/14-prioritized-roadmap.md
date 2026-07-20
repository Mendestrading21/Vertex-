# 14 — Roadmap priorisée (séquence des lots)

Chaque lot = **un** problème ciblé → fichiers → approche → implémentation limitée → `pytest` 100 % → app relancée
→ vérification navigateur réel (0 erreur console, `/api/client-log`=0) → correction régressions → mise à jour
audit → rapport (`templates/implementation-report-template.md`). **Ne jamais mélanger** dans un lot : refonte
globale + logique trading + migration données + IBKR + nettoyage.

## Phase 0 — Sécurisation (fait cette session)
- Skill `vertex-maximum` + agents auditeurs + rules + **cet audit**. Zéro code applicatif touché. 919 tests verts.

## Phase 1 — Audit (ce dossier) — EN COURS → livré
- P0/P1 identifiés, roadmap séquencée. `pages/*` amorcées.

## Phase 2 — Fondations design/données (P0/P1 prioritaires)
0. **RT-01 (P1) — ✅ FAIT** — `/options/<sym>` dédupliqué (JSON → `/api/options/pack/<sym>`, 2 consommateurs
   corrigés, page réservée). Vérifié DEMO + 919 tests.
1. **DAT-01/IBK-03 — révisé P2 après vérification** — la couche d'affichage est déjà honnête (normalisation `None`
   + état vide `available:false`, vérifié DEMO). Résidu étroit (OI/vol au producteur IBKR live) à traiter **en
   local** (non testable en cloud) ; ne pas dégrader l'affichage honnête.
2. **CMP-01 (P1)** — `.vx-card` canonique (une définition + modificateurs), retirer les 6 redéfinitions.
3. **CMP-02 (P1) — ✅ Phases 1-2 faites** — Phase 1 : builder `VX.tile` + bug tuiles stat nues corrigé
   (tracking/options-intel → `VX.tile.stat`), SW v90. Phase 2 : builders `vx-metric` des pages options migrés
   vers `VX.tile.metric` (options-symbol/options-intel), vérifié DEMO **identique** (diff = seul `data-tone=""`
   inerte), SW v91. Reste : `analysis_page metric()` (ajouter chip `-cmp`), `briefing tile()`, `portfolio H/_rk`
   (différé, non byte-identique) ; retrait `vx-stat-xl` (test-pinned).
4. **DES-01 (P1)** — réaligner/étiqueter les docs de design périmés (orange/bleu) sur `glass.css`.
5. **CHT-02 (P2)** — contrat de graphe appliqué (source/ts/question/conclusion/état vide) sur les graphes de décision.

## Phase 3 — Shell unifié (P1)
6. **IA-01 + CMP-03 (P1)** — une seule nav (`PRIMARY_NAV`) ; rediriger les routes legacy ; supprimer la sidebar
   inline orange (`terminal.py` ×4) une fois les dépendances confirmées ; **bump `td-shell-vN`** + 3 tests.
   _(RT-01 déjà résolu en Phase 2 — voir §0 ci-dessus.)_

## Phases 4-13 — Page par page (DoD par page)
Dashboard → Portefeuille → Opportunités → Analyse → Options → **Préparation (prep/sim)** → Performance →
Intelligence → Journal → Events → Watchlist → Settings. Pour chacune : provenance visible (DAT-03), anti-fausse-
fonctionnalité (FCT-01), a11y (A11Y-*), MetricCard/charts unifiés. Fiche `docs/vertex-audit/pages/<route>.md`.

## Phase transverse — Trading & perf (au fil)
- **ENG-01/04 (P1)** — plafonds testés + sémantique unique des verdicts.
- **PRF-01 (P1)** — réduire le payload fiche ~8 Mo sans perte d'info. **PRF-03 (P2)** — tests byte-identiques des memos.
- **SEC-01 (P1)** — sanitiser tout `innerHTML` alimenté par des sources externes.

## Phase 14 — Validation finale
Parcours complet des 8 espaces en navigateur réel, 0 erreur, tous gardiens verts, matrice de pages à « OK »
(`15-page-status-matrix.md`), rapport global.

## Ordre de valeur (résumé)
P0 (DAT-01) → P1 structurants (CMP-01/02, DES-01, IA-01, RT-01, CMP-03, ENG-01/04, PRF-01, SEC-01) → P2 → P3.
