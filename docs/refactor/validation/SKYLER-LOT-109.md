# SKYLER V2 — LOT 109 : boucle continue — registre des jobs figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-109`
(base : `integration/vertex-skyler-v2` @ `3d4e907`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/scheduler/registry.py` (§24 — le registre des boucles de fond que
la vue Système/Automatisations affiche) n'avait AUCUN test direct : son
seul usage en test est un `len()` dans startup. Particularité
d'infrastructure découverte en écrivant le test : le package rebinde le
nom `registry` vers l'objet façade, si bien que même `import … as` rend
l'objet — le module réel s'attrape via `sys.modules` (commenté dans le
test). État module `_JOBS` sauvegardé/restauré autour de chaque test.

## 2. Les 8 comportements figés (nés verts, dits)

```text
snapshot ordonné EXACTEMENT selon la priorité produit canonique
  (positions ouvertes avant univers) · jamais exécuté → last_run/age/
  ETA None (aucune ETA inventée)                                       OK
battement d'un job NON canonique : enregistré mais JAMAIS exposé dans
  le snapshot (pas de surprise en UI)                                  OK
beat ok : runs incrémente, last_ok True, durée arrondie (12.7 → 13)    OK
beat erreur : last_ok False, message tronqué à 200                     OK
ETA seulement pour les jobs à intervalle (0..60 après battement) ·
  job à la demande → ETA None même après battement                     OK
boucle EN RETARD → ETA 0, jamais un délai négatif · age_s exact        OK
façade registry.beat/jobs = les fonctions module (delegation pure)     OK
le snapshot est une COPIE — le muter ne falsifie jamais le registre    OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1912 passed, 2 skipped   (1904 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 110 : lot de travail + MINI-BILAN tournée 106-110.
