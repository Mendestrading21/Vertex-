# SKYLER V2 — LOT 77 : boucle continue — sécurité en-têtes/contenu servi

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-77-headers`
(base : `integration/vertex-skyler-v2` @ `705e6b9`, fraîchement fetchée).

## 1. Mesures (publiées)

- **4 en-têtes de sécurité** (nosniff, X-Frame-Options SAMEORIGIN,
  Referrer-Policy, Permissions-Policy) : présents sur pages HTML, API,
  statiques, sw.js — **cohérents partout** (middleware
  `_security_headers` de terminal.py, + HSTS derrière HTTPS) ;
- **Content-Type** : corrects partout (html/json/js/css) ; `sw.js` en
  no-cache (mises à jour immédiates) ; statiques max-age=3600 ;
- **Contenu servi** (8 pages + tous les JS statiques) : 0 email,
  0 secret/clef, 0 chemin absolu, aucun nom personnel — SAIN.

## 2. Défaut réel corrigé : blob desk sans Cache-Control

`/api/desk` sert les données PERSONNELLES (trades, positions, journal)
sans directive de cache — un cache intermédiaire ou un navigateur partagé
pouvait les stocker. Corrigé PAR la source (middleware) :
`Cache-Control: no-store` sur toutes les routes `/api/desk*`.
Preuve serveur APRÈS : `curl -i /api/desk` → `Cache-Control: no-store`.

## 3. Tests (rouges d'abord — 2)

`tests/test_headers_lot77.py` : /api/desk et /api/desk/backups en
no-store obligatoire · les 4 en-têtes de sécurité gardés sur pages ET
API (contrat verrouillé).

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1710 passed, 2 skipped   (1708 + 2)
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v125)
Responsive 8 × 3 → 0 débordement, 0 erreur
```

Pas de bump SW : middleware serveur, aucun changement de shell visible.

## 5. Suite

Lot 78 : cohérence des libellés français affichés (orthographe, accents,
uniformité des termes) — ou angle plus porteur si découvert.
