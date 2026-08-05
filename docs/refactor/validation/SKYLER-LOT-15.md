# SKYLER V2 — LOT 15 — SÉRIE DATÉE PAR SÉANCE (HORIZONS RÉELS DE LA MÉMOIRE)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-15-dated-sessions`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `e968611`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Les horizons de la mémoire décisionnelle (5/20/60 séances, lot 10) comptaient
les séances par empreinte de fin de série sur la fenêtre canonique — honnête
mais lent : la fenêtre glissante rend l'alignement fragile et aucun comptage
de séances RÉEL n'existait (limite n° 1 documentée du lot 10).

## 2. Problème

Sans dates de séance, « 5 séances » restait approximé par la croissance d'une
série sans calendrier. Les horizons risquaient de rester `EN_ATTENTE`
indéfiniment dès que la fenêtre roulait au-delà de l'empreinte.

## 3. Décision

Nouveau moteur pur `vertex/engines/session_log.py` :

- **`record_close(log, sym, date, close)`** : UNE clôture par symbole et par
  jour de scan RÉEL — la date est la date d'observation effective (horloge
  réelle, UTC), jamais inventée ; même date = même séance (la dernière
  observation du jour raffine la clôture) ; trié, borné (400 séances/symbole),
  NaN/infinis/dates malformées refusés ; fonctions pures.
- **`closes_after_date(log, sym, date)`** : clôtures STRICTEMENT postérieures
  à la date de la décision — le comptage de séances réel ; titre non suivi ou
  date absente → `None` (jamais deviné). Un jour sans scan reste un trou.

Branchements :

- `/api/skyler/<sym>` : alimente le log fail-safe (prix du scan, date UTC du
  jour) et fige `session_date` dans le record mémoire (`freeze` accepte le
  paramètre ; anciens records → `None` honnête) ;
- `/api/skyler/memory` : le log est AUTORITAIRE quand il couvre le titre
  (comptage réel) ; l'empreinte de fin de série reste le SECOURS pour les
  anciens records sans date.

Persistance : `skyler_sessions.json` (runtime, gitignoré).

## 4. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/session_log.py` | moteur log de séances (nouveau) | faible |
| `vertex/engines/decision_memory.py` | `freeze(..., session_date=None)` figé dans le record | faible |
| `vertex/app/routes/analysis_api.py` | alimentation fail-safe + priorité au log dans la mesure | faible |
| `.gitignore` | + `skyler_sessions.json` | faible |
| `tests/test_session_log_lot15.py` | 12 tests rouges→verts | faible |

## 5. Tests rouges avant correction

```text
python -m pytest tests/test_session_log_lot15.py -q
ImportError — module vertex.engines.session_log inexistant
```

## 6. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_session_log_lot15.py -q → 12 passed
python -m pytest tests/ -q → 1410 passed, 2 skipped in 9.92s
```

Couverture : append/dédup par date (la dernière observation gagne), tri même
en désordre, refus NaN/dates malformées/symbole vide, borne, pureté, comptage
strictement postérieur, `None` honnête (titre non suivi, date absente),
`session_date` figée par `freeze` (None pour les anciens), mesure en séances
réelles (6 séances → H5 MESURÉ +5 %), route alimentant le log avec la date
UTC réelle et le prix du scan, endpoint mémoire préférant le log (3 séances
réelles → H5 `EN_ATTENTE` 3/5, MFE +6 %), gitignore.

Les deux tests de routes s'exécutent en client Flask réel (persist monkeypatché
vers tmp) — l'intégration bout en bout est prouvée par la suite elle-même.

## 7. Invariants vérifiés

- [x] date d'observation RÉELLE uniquement (horloge, UTC) — jamais inventée ;
- [x] un jour sans scan reste un trou — aucune interpolation ;
- [x] horizon non atteint = `EN_ATTENTE`, jamais un rendement inventé ;
- [x] anciens records sans date → secours par empreinte (compatibilité) ;
- [x] fichier runtime gitignoré, jamais commité ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1410/2 skipped ; SW v94.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1398/2 | 1410/2 |
| Comptage de séances | empreinte de série (fragile à la fenêtre) | dates réelles (log autoritaire) + empreinte en secours |
| Limite n° 1 du lot 10 | ouverte | levée (le log se remplit à chaque jour de scan) |

## 9. Risques et limites restantes

1. Le label de séance est le jour UTC d'observation — un scan après minuit UTC
   est daté du lendemain calendaire ; sans conséquence sur le comptage (ordre
   préservé), documenté.
2. Le log démarre vide : les horizons réels se remplissent au rythme des jours
   de scan effectifs — honnête, aucun rattrapage synthétique.
3. La clôture du jour est la DERNIÈRE observation du scan, pas le close
   officiel de l'échange — proxy réel observé, dit ici.

## 10. Rollback

`git revert` du commit ; supprimer `skyler_sessions.json` si présent (runtime).

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : LOT 16 — surfaçage UI (carte Mémoire
décisionnelle + dépendances cachées, SW v95, preuve navigateur).

**Arrêt après ce lot — validation humaine requise.**
