# SKYLER V2 — LOT 30 : type de catalyseur figé + découpe by_catalyst_type

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-30-catalyst-type`
(base : `integration/vertex-skyler-v2` @ `8cf1876`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) type de catalyseur figé au freeze,
(b) drill-down UI cellule de calibration, (c) fuzz déterministe,
(d) RC courte périodique. Choix : **(a)**, premier par valeur estimée.

- La question « mes décisions autour des earnings tiennent-elles mieux que
  celles autour du macro ? » est exactement le genre de biais que la mémoire
  doit rendre MESURABLE. Sans le kind figé, elle est indécidable à jamais.
- Le fait existe déjà en amont : chaque événement du moteur `events` porte
  un `kind` explicite (`earnings`/`macro`/`news`/`anomaly` —
  `vertex/engines/events.py`). Le lot ne fait que le transporter sans perte
  jusqu'au ledger — zéro heuristique, zéro invention.
- (b) dépend de cellules mesurées qui n'existent pas encore en usage réel ;
  (c) et (d) restent au backlog.

## 2. Périmètre livré

### 2.1 Moteur — `catalyst_kind` émis (0.8.0 → 0.9.0)

`vertex/engines/skyler_core.py` : `decide()` émet `catalyst_kind`, le
`kind` du **même** événement daté le plus proche qui produit déjà
`catalyst` — source unique (anti-divergence), jamais re-parsé depuis le
label. Aucun événement daté → `None` (comme `catalyst`). Aucune règle de
décision ne change : champ descriptif. Bump `ENGINE_VERSION = '0.9.0'`
documenté dans l'en-tête — la discipline « un record figé appartient à sa
version » exige que l'apparition d'un champ figé soit fencée par version.

### 2.2 Ledger — figé au freeze, jamais rétroactif

`vertex/engines/decision_memory.py` : `freeze()` stocke
`'catalyst_kind': d.get('catalyst_kind')`. Une décision d'un moteur
antérieur (catalyst présent, kind absent) fige `None` — le kind n'est
JAMAIS deviné en re-parsant « CPI (J-3) » (prouvé par test).

### 2.3 Calibration — découpe `by_catalyst_type` (OBSERVATION uniquement)

- `_measured_hits` : 6-uplets (niveau, décision, régime, catalyseur?,
  kind, hit) ;
- `calibration_by_context` : cellules `by_catalyst_type` (mêmes règles
  d'échantillon `MIN_CALIBRATION_SAMPLE=20`), SEULEMENT pour les records
  avec catalyseur ; kind absent → bucket `inconnu` honnête ; records sans
  catalyseur exclus (leur domicile est `by_catalyst.sans_catalyseur`) ;
- **non-consommation prouvée** : `calibration_factor_for` inchangé
  (signature sans paramètre catalyseur, sélection niveau → régime →
  global — test dédié) ; note du payload mise à jour ;
- servie automatiquement par `/api/skyler/memory` (payload existant).

Aucun changement de shell → **SW v101 inchangé**, pas de preuve navigateur
requise (API/moteur seulement).

## 3. Méthode — rouge d'abord

`tests/test_catalyst_type_lot30.py` (9 tests) écrit AVANT
l'implémentation ; confirmé rouge : **6 failed / 3 passed** (les 3 verts
étant les gardes déjà satisfaites par construction : non-consommation,
non-devinette sur champ absent, déterminisme). Après : **9 passed**.

Couverture : version prospective ≥ 0.9.0 ; kind du plus proche événement
daté (macro J-5 bat earnings J-12) ; None sans événement daté ; freeze
stocke le kind explicite ; jamais deviné depuis le label ; cellules par
type avec règles d'échantillon (25 earnings MESURE hit 0,8 / 3 macro
INSUFFISANT / sans-catalyseur exclus) ; bucket `inconnu` pour les anciens
records ; non-consommation par la sélection ; déterminisme + note.

## 4. Preuves

```text
python -m pytest tests/test_catalyst_type_lot30.py -q
→ 9 passed in 0.06s

python -m compileall -q terminal.py vertex   → exit 0
python -m pytest tests/ -q
→ 1531 passed, 2 skipped in 8.52s            (baseline 1522 → +9)
```

Le bump 0.8.0 → 0.9.0 n'a cassé aucun gardien : tous prospectifs (`>=`).
Coût réel du bump : les records 0.8.0 ne nourrissent pas la calibration
0.9.0 (discipline anti-mélange) — coût nul en pratique, aucun magasin
réel n'atteint encore `MIN_CALIBRATION_SAMPLE`.

## 5. Invariants tenus

- READONLY absolu — aucun ordre, champ descriptif uniquement ;
- données réelles uniquement — kind = fait du moteur events, absent →
  `None`/`inconnu` honnête, jamais re-parsé ni rétroactif ;
- découpe d'observation NON consommée par la sélection (prouvé) ;
- fichiers runtime jamais commités ; gardiens prospectifs ; pas
  d'aléatoire ; `main` intacte ; SW inchangé (aucun shell visible).

## 6. Backlog restant (candidats lot 31)

1. Drill-down UI cellule de calibration (cellule → décisions mesurées) ;
2. Fuzz déterministe ciblé (export, calibration_factor_for, propagate) ;
3. RC courte périodique (navigateur 8 pages + /api/client-log=0) ;
4. Surfaçage des cellules by_catalyst_type dans la carte Mémoire quand
   des cellules mesurées existeront.

**Arrêt après ce lot — validation humaine requise.**
