# SKYLER V2 — X1 — BALAYAGE DE L'UNIVERS (Classement Skyler)

> Date : 2026-08-05 · Branche : `agent/skyler-v2-x1-sweep` · Base : intégration (tout fusionné)

## Décision

`vertex/engines/skyler_sweep.py` (pur) : `decide` canonique appliqué à TOUS les
titres scannés — MarketContext calculé UNE fois et partagé, anomalies + timeline
+ OptionsContext LEAPS par titre, classement par score /40 (tri secondaire par
symbole = déterminisme strict). Chaque ligne : décision, score, niveau,
**gate plafonnante VISIBLE**, catalyseur daté, invalidation réelle, risque max.
Ne journalise JAMAIS (le journal ne s'alimente que sur consultation de fiche —
testé). Contexte portefeuille volontairement omis (classement d'univers ; l'étude
de candidat vit sur la fiche) — dit dans la note. Titres sans dossier technique
omis (jamais une ligne inventée). Coupe `limit` dite (`n` = total).

Route `GET /api/skyler/sweep` (+ earnings du calendrier réel par titre).
UI : carte « Classement Skyler — score canonique /40 » sur le Radar des
Opportunités (domicile du classement), idempotente, clic titre → fiche Analyse.
SW v92 → **v93** + gardiens.

## Preuves

```text
tests : 9 passed (tri, champs, gate visible, contexte partagé, vide honnête,
        déterminisme JSON, limite honnête, route + non-journalisation, page)
suite : 1292 passed, 2 skipped · compileall exit 0
```

Navigateur (démo) : **20 titres classés** — 1re ligne « ABNB · REFUSER · 22/40 ·
REFUS_WATCH · Résultats ABNB (J-34) · invalidation 288,78 ». 0 erreur console,
0 débordement, client-log 0. Capture `docs/skyler/baseline/x1_skyler_rank_1440.png`.

## Verdict

**GO** — l'assistant classe désormais l'univers entier avec le même moteur que
la fiche, gates et catalyseurs visibles. **Arrêt de lot — validation groupée.**
