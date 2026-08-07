# SKYLER LOT 283 — Carte « Verrou d'accès » dans Système (directive « développe »)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-283` (base : lot 282 fusionné)

## Objet

Directive humaine reçue : « Continue à développer encore » → sortie de
veille, reprise du DÉVELOPPEMENT. Piste choisie : la seule amélioration
produit identifiée et en attente depuis le lot 259 — **le bouton de
verrouillage n'était atteignable nulle part dans l'UI** (il ne vivait
que dans PAGE_SETTINGS, page héritée jamais routée, preuve lot 248).

## Livré — `vertex/ui/pages/system_page.py`

Nouvelle carte **« Verrou d'accès »** dans Système → Connexions
(placée après Synchronisation/Stockage), rendue dynamiquement selon
l'état RÉEL du verrou (`AUTH_ON`, lu à la requête) :

- **Verrou actif** (VERTEX_CODE défini) : badge « actif », rappel des
  faits vérifiés au lot 259 (session signée 30 jours, anti-force-brute,
  temps constant) + bouton **« 🔓 Se déconnecter & verrouiller cet
  appareil »** → `/logout` (route existante, publique).
- **Verrou inactif** : état honnête — badge « inactif », PAS de bouton
  (rien à verrouiller), rappel du repli sécurité 127.0.0.1 et de la
  marche à suivre (`VERTEX_CODE` dans `.env`, SECURITE.md).

Conformité : classes existantes uniquement (`vx-card`, `vx-btn
vx-btn-sm vx-btn-ghost` — précédent analysis_page, `vx-badge`), aucun
littéral couleur, aucune apostrophe non échappée (HTML entités), FR,
domicile unique (vue Connexions seulement).

## Gardien neuf — `tests/test_lock_card_lot283.py` (3 tests)

1. Verrou actif → bouton `/logout` + faits exacts (30 j,
   anti-force-brute) ; 2. inactif → honnête SANS bouton (127.0.0.1,
   VERTEX_CODE) ; 3. la vue Connexions porte la carte, placeholder
   consommé, les autres vues ne l'ont pas.

## Preuves (navigateur réel, serveur DEMO)

- Carte visible sur /system, badge « inactif » (DEMO sans code),
  bouton absent comme attendu ; bord droit 1416/1440 et 378/390 —
  **aucun débordement** desktop/mobile ; **0 erreur console**.
- Capture envoyée (lot283_system_lock.png).
- Suite complète : **2489 passed / 2 skipped** (+3).

## Décision SW

**Bump v173 → v174** (changement de shell visible : nouvelle carte
servie) + les 5 gardiens SW mis à jour.

## Suite

LOT 284 : développement continue (directive active) — prochaines
pistes produit à calibrer. La purge attend toujours « GO purge
étape 1 » explicite.
