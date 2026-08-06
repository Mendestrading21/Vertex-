# SKYLER V2 — LOT 82 : boucle continue — offline/service worker réel

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-82-offline`
(base : `integration/vertex-skyler-v2` @ `a1fb0e5`, fraîchement fetchée).

## 1. Défaut réel MAJEUR trouvé par le scénario offline

Le service worker n'était enregistré QUE par les pages legacy de
terminal.py — **le shell canonique (les 8 espaces) ne l'enregistrait
JAMAIS** : registration absente, 0 précache, et un rechargement
hors-ligne donnait la page d'erreur du navigateur. Tout le travail
SW/précache (dont les polices du lot 81) était inopérant sur l'UI
principale.

## 2. Correction (minimale, par la source)

Enregistrement dans `vx-shell.js` (chargé par tout le shell) — PAS en
`<script>` inline : le gardien anti-reflet XSS du fuzz lot 43 interdit
toute balise script nue dans la page (mon premier essai inline l'a
déclenché — attrapé par la suite, corrigé en externe, dit).

## 3. Preuves (scénario Playwright AVANT/APRÈS)

```text
AVANT : SW actif=false · caches=[] · reload offline → ERR_INTERNET_DISCONNECTED
APRÈS : SW actif=true · précache td-shell-v127 (5 entrées, polices incluses)
        reload OFFLINE → page rendue depuis le cache (title « Aujourd'hui ·
        Vertex », shell présent, Inter chargée OFFLINE=true), aucun chiffre
        non étiqueté inventé · retour online → page re-fraîche
python -m pytest tests/ -q → 1720 passed, 2 skipped   (1718 + 2)
tools/rc_short_audit.js → GO — 0 défaut (SW v127 servi)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Tests (rouges d'abord — 2)

`tests/test_offline_lot82.py` : vx-shell.js enregistre /sw.js + le shell
charge vx-shell.js · SW ≥ v127. SW `td-shell-v126` → `td-shell-v127` +
4 gardiens (v126 absent).

## 5. Suite

Lot 83 : angle suivant le plus porteur de la tournée perpétuelle.
