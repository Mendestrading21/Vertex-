# SKYLER V2 — LOT 81 : boucle continue — polices auto-hébergées

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-81-fonts`
(base : `integration/vertex-skyler-v2` @ `c34a75d`, fraîchement fetchée).

## 1. Chantier (constat du lot 80 → réglé)

Inter + JetBrains Mono étaient chargées depuis fonts.googleapis.com
(préconnect + stylesheet dans le shell ET 6 blocs des pages legacy de
terminal.py) : offline/PWA en polices système, ping Google à chaque
chargement. Réglé :

- **2 fichiers VARIABLES woff2 locaux** (`inter-var.woff2` 47 kB,
  `jetbrains-mono-var.woff2` 31 kB — un seul fichier couvre tous les
  poids ; Google servait le même fichier pour chaque graisse, vérifié
  aux empreintes md5 → 10 téléchargements dédupliqués en 2) ;
- **`fonts.css` local** (@font-face plages 100-900/100-800,
  font-display:swap, subset latin) ;
- **7 remplacements** : shell (bloc preconnect/preload/noscript → un
  lien local) + 6 blocs legacy terminal.py — 0 résidu ;
- **Service worker v126** : fonts.css + les 2 woff2 ajoutés au précache
  d'installation (offline dès la première visite).

## 2. Preuves

```text
python -m pytest tests/ -q → 1718 passed, 2 skipped   (1714 + 4 nouveaux)
Navigateur 8 pages : requêtes EXTERNES = 0 ·
  document.fonts : « Inter 100 900 », « JetBrains Mono 100 800 » chargées
tools/rc_short_audit.js → GO — 0 défaut (SW v126 servi)
tools/user_journeys.js → 14 étapes, 0 échec, 0 ERREUR CONSOLE
  (l'erreur fonts.googleapis du lot 80 a DISPARU)
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 3. Tests

4 nouveaux (rouges d'abord — `tests/test_fonts_lot81.py`) : plus aucune
référence CDN · woff2 locaux présents + fonts.css 100 % local · shell lié
à fonts.css · SW ≥ v126. **2 gardiens hérités mis à jour** (ils
verrouillaient l'ANCIENNE architecture CDN — même intention, nouveau
contrat : test_continuity_shell.py::test_font_is_non_blocking,
test_design_system_v1.py::test_shell_loads_official_fonts — dits).

SW `td-shell-v125` → `td-shell-v126` + 4 gardiens (v125 absent).

## 4. Suite

Lot 82 : angle suivant le plus porteur de la tournée perpétuelle.
