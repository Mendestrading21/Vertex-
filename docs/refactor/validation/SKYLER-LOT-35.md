# SKYLER V2 — LOT 35 : santé du ledger multi-versions

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-35-ledger-health`
(base : `integration/vertex-skyler-v2` @ `a0e3b8a`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) santé du ledger surfacée, (b) fuzz de
`/api/skyler/<sym>`, (c) drill-down cellule. Choix : **(a)**, premier
par valeur.

- Deux bumps de moteur (0.8.0 → 0.9.0) et les trouvailles des lots 31/34
  (magasins corruptibles) rendent le besoin concret : le ledger est la
  donnée la plus précieuse du programme, et rien ne DISAIT s'il était
  cohérent (doublons, orphelins, mélanges de versions). La table
  par-version de la carte Mémoire existait, le contrôle de cohérence
  manquait.
- Principe tenu : le contrôle **dit**, il ne répare JAMAIS rien en
  silence (l'historique original gagne toujours) — même philosophie que
  `append_decision` (le doublon est refusé, jamais remplacé).
- (b) et (c) restent au backlog.

## 2. Périmètre livré

### 2.1 Moteur — `decision_memory.ledger_health(memory)` (nouveau)

Contrôle de cohérence déterministe, honnête et sans réparation :

- `duplicate_decision_ids` : ids apparaissant plus d'une fois (un magasin
  édité hors moteur peut en contenir — `append_decision` les refuse) ;
- `orphan_outcomes` : résultats mesurés sans décision correspondante ;
- `version_mismatches` : outcome mesuré sous une AUTRE version que sa
  décision — mélange interdit par la discipline du ledger ;
- `corrupted_entries` : entrées non-dict (magasin corrompu) ;
- `status` : `SAIN` (0 anomalie) / `ANOMALIES`, avec `basis` lisible qui
  répète : « rien n'est réparé en silence, l'historique original gagne ».
- Entrées dégénérées (memory None/{}/champs non-liste) → réponse honnête,
  jamais d'exception (leçon des lots 31/34 appliquée d'entrée).

### 2.2 Route — `/api/skyler/memory`

Champ `ledger_health` ajouté au payload existant (lecture seule).

### 2.3 UI — carte Mémoire (badge conditionnel)

Badge rouge `LEDGER : ANOMALIES` (title = basis) dans l'en-tête de la
carte Mémoire, affiché **SEULEMENT** si `status === 'ANOMALIES'` — un
ledger sain n'ajoute aucun bruit. Shell visible → **SW v102 → v103** +
4 gardiens.

## 3. Méthode — rouge d'abord

`tests/test_ledger_health_lot35.py` (10 tests) écrit AVANT ; confirmé
rouge : **10 failed / 0 passed**. Après : **10 passed**. Couverture :
ledger sain → SAIN avec comptes à zéro ; doublons dits ; orphelins dits ;
mélange de versions dit ; entrées corrompues comptées sans crash ;
mémoires dégénérées honnêtes ; déterminisme ; route sert `ledger_health` ;
la carte Mémoire câble le badge (littéraux `ledger_health` + `ANOMALIES`) ;
SW ≥ v103 avec v102 absent.

## 4. Preuves

```text
python -m pytest tests/test_ledger_health_lot35.py -q → 10 passed
python -m compileall -q terminal.py vertex            → exit 0
python -m pytest tests/ -q → 1565 passed, 2 skipped   (baseline 1555 → +10)

tools/rc_short_audit.js (serveur DEMO=1 NO_IBKR=1) :
  8 pages HTTP 200 · console_err=0 · pageerror=0 · /healthz 200
  /api/client-log n=0 · sw.js td-shell-v103
  RC COURTE : GO — 0 défaut.

GET /api/skyler/memory (live) → ledger_health:
  {status: SAIN, n_decisions: 1, n_outcomes: 0, 0 anomalie partout,
   basis: « ledger cohérent : 1 décision(s), 0 résultat(s), 0 anomalie »}
```

Aucun bump moteur (contrôle en lecture, aucune règle de décision ne
change ; le champ n'est PAS figé dans les records — il est calculé à la
lecture).

## 5. Invariants tenus

- le contrôle DIT, ne répare jamais (append-only intact, historique
  original gagne) ; READONLY absolu ;
- données réelles uniquement : badge seulement si anomalie réelle, ledger
  sain silencieux ; basis chiffrée exacte ;
- XSS : basis échappée via `esc()` dans le title du badge ;
- SW bump v103 + 4 gardiens ; preuve navigateur RC courte GO ;
- fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 36)

1. Fuzz de `/api/skyler/<sym>` (paramètres/symboles dégénérés) ;
2. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
3. Vue Système : reprendre `ledger_health` dans le cockpit technique
   (même source, autre domicile — si jugé utile) ;
4. RC courte re-jouée après le prochain lot UI.

**Arrêt après ce lot — validation humaine requise.**
