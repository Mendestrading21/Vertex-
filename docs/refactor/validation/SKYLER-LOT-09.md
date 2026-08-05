# SKYLER V2 — LOT 09 — CALIBRATION (infrastructure)

> Date : 2026-08-05
> Branche : `agent/skyler-v2-lot-09-calibration`
> Base : `agent/skyler-v2-lot-08c-options-scanners`
> Périmètre : journal des décisions + machinerie de calibration — la RC complète
> (Brier sur probabilités calibrées, MAE/MFE, benchmark SPY, audit accessibilité)
> exige des SEMAINES de décisions enregistrées : ce lot pose l'infrastructure
> honnête qui les accumule dès maintenant.

## 1. Constat

Aucune décision Skyler n'était enregistrée : impossible de mesurer quoi que ce
soit ex post, aujourd'hui comme dans un mois. Sans journal, le lot 9 « complet »
serait resté à jamais bloqué.

## 2. Décision

- **`vertex/engines/skyler_journal.py`** (pur — horloge et journal injectés) :
  - `record(journal, decision, price, now)` : entrée {symbole, décision, as_of,
    score, niveau, gate plafonnante, **prix au moment de la décision**,
    horodatage} — **dédupliqué** par (symbole, as_of, décision) (un rechargement
    de page ne crée rien), **borné** à 2000 entrées ; prix absent enregistré
    None (jamais inventé) ;
  - `brier(probs, outcomes)` : machinerie PROUVÉE à la main
    (¼·0+¼... → 0.25/3 exact), entrées invalides refusées — prête pour le jour
    où un modèle calibré émettra des probabilités ;
  - `calibration(journal, quotes)` : comptages exacts par décision/niveau ;
    **résultats ex post = rendements RÉELS** depuis le prix enregistré vers la
    cote actuelle (entrée sans prix ou sans cote = NON MESURÉE, comptée et
    dite) ; **Brier `available: false`** avec raison explicite — les scénarios
    n'affichent volontairement aucune probabilité (lot 5), il n'y a rien à
    noter : l'indisponibilité est la seule réponse honnête.
- **Routes** : `/api/skyler/<sym>` journalise chaque décision servie (le journal
  ne casse jamais la décision — try/except) ; `GET /api/skyler/calibration`
  sert l'état. Fichier runtime `skyler_decisions.json` **gitignoré**.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/skyler_journal.py` | nouveau (pur) | faible |
| `vertex/app/routes/analysis_api.py` | journalisation + 1 route additive | faible |
| `tests/test_skyler_calibration_lot9.py` | nouveau — 9 tests | faible |
| `.gitignore` | + `skyler_decisions.json` | nul |

## 4. Tests

```text
rouge : collection error (module inexistant)
vert  : 9 passed (dédup/bornage/prix None, Brier exact à la main + refus,
        calibration vide honnête, rendements réels ±10 % exacts, non-mesuré
        jamais inventé, route enregistre + sert)
suite : 1279 passed, 2 skipped · compileall exit 0
```

## 5. Validation runtime (DEMO=1 NO_IBKR=1)

Deux appels `/api/skyler/{GOOGL,ABBV}` puis `/api/skyler/calibration` →
`n_decisions: 3` (dont 1 persistée d'un run précédent — la persistance marche),
`by_decision {REFUSER: 3}`, résultats mesurés 2/3 (rendement 0,0 % — même scan,
honnête ; le 3e sans cote compté non mesuré), **Brier indisponible avec raison**.
`/api/client-log` = 0. Aucune UI modifiée → pas de bump SW.

## 6. Invariants vérifiés

- [x] jamais un chiffre inventé : non mesuré ≠ 0, Brier absent tant que rien à noter ;
- [x] le journal ne modifie AUCUNE décision (enregistrement après coup, fail-safe) ;
- [x] fichier runtime gitignoré ; aucune donnée personnelle ; READONLY.

## 7. Restant pour la RC (après accumulation de données réelles)

Brier sur probabilités calibrées (exige d'abord un modèle calibré — noté dans la
sortie), MAE/MFE (chemins de prix intra-détention), résultats par régime/niveau,
benchmark SPY, dérive des scores, audit sécurité/perf/accessibilité, docs release.
Le journal qui démarre MAINTENANT est la condition de tout ce qui précède.

## 8. Verdict

**GO** — infrastructure honnête posée et prouvée (tests + runtime), suite 1279 verte.

**Arrêt de lot — validation humaine groupée (accord utilisateur).**
