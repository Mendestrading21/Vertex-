# SKYLER V2 — LOT 08e — NEON GLASS · JOURNAL (Calibration Skyler)

> Date : 2026-08-05
> Branche : `agent/skyler-v2-lot-08e-journal-calibration`
> Base : `agent/skyler-v2-lot-08d-portfolio-discipline`
> Périmètre : UNE vue (Journal → Performance), une carte — aucun moteur modifié

## 1. Constat

Le journal de calibration (lot 9 : décisions enregistrées, rendements ex post,
Brier honnête) n'était visible que par API.

## 2. Décision

Carte « **Calibration Skyler — les décisions vieillissent-elles bien ?** » sur
la vue Performance du Journal (son domicile : discipline & résultats), sous le
post-mortem : compteur de décisions journalisées + répartition par décision,
tableau des 12 derniers rendements ex post RÉELS (prix décision → prix actuel,
coloré), mesurées/non-mesurées dites, **raison d'indisponibilité du Brier
affichée telle quelle**, badge DÉMO si le serveur le confirme, vide honnête
(« le journal se remplit à chaque fiche Analyse consultée »).

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/ui/pages/performance_page.py` | carte + `loadCalibration()` (additif) | faible |
| `vertex/app/routes/system.py` | SW v91 → **v92** | faible |
| 4 gardiens SW + gardien de page (corrigé : `/performance` redirige vers `/journal`) | v92 | nul |

## 4. Tests

```text
tests/test_skyler_calibration_lot9.py → 10 passed
suite : 1283 passed, 2 skipped · compileall exit 0
```

## 5. Validation navigateur (DEMO=1 NO_IBKR=1, Chromium réel)

1440×900 et 390×844 : carte vivante sur le journal RÉEL — « 5 décision(s)
journalisée(s) · REFUSER × 5 · DÉMO », tableau GOOGL/ABBV avec prix décision =
prix actuel (0 % — même scan, honnête), raison Brier affichée. **0 erreur
console, 0 débordement** ; `/api/client-log` = 0 ; SW v92.

## 6. Invariants vérifiés

- [x] rendements réels uniquement ; non-mesuré compté et dit ; Brier absent expliqué à l'écran ;
- [x] DÉMO seulement si serveur ; vide honnête ; bump SW + gardiens ; READONLY.

## 7. Clôture du lot 8

Les 8 espaces sont servis : Aujourd'hui (8b), Marchés/Opportunités (données
canoniques déjà à domicile — refonte Neon Glass antérieure, rien à dupliquer),
Analyse (8a), Portefeuille (8d), Options (8c), Journal (8e), Système (état
moteurs/connexions déjà à domicile). Ajouter des cartes Skyler à Marchés/
Opportunités/Système dupliquerait des domiciles existants — refusé par
l'invariant « une donnée = un seul domicile ».

## 8. Verdict

**GO** — suite 1283 verte, carte prouvée sur journal réel, 2 tailles, 0 erreur.

**Arrêt de lot — validation humaine groupée (accord utilisateur).**
