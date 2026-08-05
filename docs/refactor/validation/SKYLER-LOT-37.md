# SKYLER V2 — LOT 37 : fraîcheur du ledger dans la carte Mémoire

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-37-ledger-freshness`
(base : `integration/vertex-skyler-v2` @ `71d0343`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) fraîcheur du ledger en UI, (b) bilan
consolidé 29-36, (c) drill-down cellule. Choix : **(a)**, premier par
valeur.

- La carte Mémoire dit combien de décisions sont figées et si le ledger
  est cohérent (lot 35), mais pas QUAND la dernière l'a été — or une
  mémoire qui n'enregistre plus est un signal opérationnel majeur pour
  un système dont la valeur est l'accumulation d'historique.
- Coût minimal : `session_date` est déjà figée dans chaque record ; la
  fraîcheur est un affichage dérivé côté client, zéro moteur.
- (b) reste un bon candidat pour le prochain lot ; (c) toujours limité.

## 2. Périmètre livré

### 2.1 Carte Mémoire (`vertex/ui/pages/performance_page.py`)

L'en-tête gagne un méta honnête à trois états :

- ledger vide → « aucune décision figée » ;
- dernière décision sans date → « dernière décision figée : n/d » ;
- date présente → « dernière décision figée : YYYY-MM-DD (J-N) » —
  ancienneté en **différence de dates calendaires UTC** (J-0 =
  aujourd'hui), notation J-N (grammaire catalyseur du desk, aucune
  apostrophe fragile dans la chaîne JS).

### 2.2 Service worker

Shell visible modifié → bump `td-shell-v103` → `td-shell-v104` + les
4 gardiens (prospectifs, v103 absent).

## 3. Méthode — rouge d'abord + défaut attrapé en preuve navigateur

`tests/test_ledger_freshness_lot37.py` (4 tests) écrit AVANT ; confirmé
rouge : **4 failed**. Après : **4 passed**.

**Défaut réel attrapé par la preuve navigateur** : la première version
calculait l'ancienneté avec `Date.now()` brut — une décision figée
AUJOURD'HUI affichait « J-1 » dès 12h UTC (arrondi d'heures écoulées,
pas différence de dates). Corrigé en différence de minuits UTC
(`Date.UTC(y,m,d)` − minuit de `session_date`) ; re-vérifié en live :
**« 2026-08-05 (J-0) »** correct. C'est exactement pourquoi la preuve
navigateur est un invariant — les tests de source ne voient pas ça.

## 4. Preuves

```text
python -m pytest tests/test_ledger_freshness_lot37.py -q → 4 passed
python -m compileall -q terminal.py vertex               → exit 0
python -m pytest tests/ -q → 1576 passed, 2 skipped      (baseline 1572 → +4)

Navigateur (serveur DEMO, décision AAPL figée puis /journal) :
  avant correctif : « dernière décision figée : 2026-08-05 (J-1) » ← FAUX
  après correctif : « dernière décision figée : 2026-08-05 (J-0) » ← exact

tools/rc_short_audit.js : 8 pages HTTP 200 · console_err=0 · pageerror=0
  /api/client-log n=0 · sw.js td-shell-v104 · RC COURTE : GO — 0 défaut.
```

Moteur 0.9.0 inchangé (affichage dérivé client uniquement, rien de figé).

## 5. Invariants tenus

- données réelles uniquement : trois états honnêtes (vide / n/d / date
  réelle), ancienneté = arithmétique de dates, jamais une invention ;
- apostrophes : notation J-N choisie pour éviter toute apostrophe dans
  la chaîne JS ; `esc()` sur la date affichée (XSS) ;
- SW bump v104 + 4 gardiens ; preuve navigateur exécutée ET utile (un
  défaut réel attrapé et corrigé avant livraison) ;
- READONLY absolu ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog restant (candidats lot 38)

1. Bilan consolidé du travail continu lots 29-37 dans STATUS (synthèse
   pour la validation humaine à venir) ;
2. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
3. RC courte re-jouée après le prochain lot UI.

**Arrêt après ce lot — validation humaine requise.**
