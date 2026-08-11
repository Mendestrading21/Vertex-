# SKYLER V2 — LOT 80 : boucle continue — parcours utilisateur bout-en-bout

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-80-parcours`
(base : `integration/vertex-skyler-v2` @ `04174ba`, fraîchement fetchée).

## 1. Les 5 parcours « du réveil à la décision » (Playwright, publiés)

```text
P1 / → brief lisible → meilleure opp cliquée → /analysis/ACN avec
   verdict → retour arrière sur /                       4/4 OK
P2 sidebar → /markets → vue breadth → graphe rendu     3/3 OK
P3 /opportunities → ticker shortlist (AFL) cliqué →
   /analysis/AFL ouverte                               2/2 OK
P4 fiche → menu entité ouvert → refermé proprement     3/3 OK
P5 /journal → décision mémoire → /memory/<hash>
   lisible                                             2/2 OK

TOTAL : 14 étapes, 0 échec.
```

Outillage versionné : `tools/user_journeys.js` (rejouable à chaque RC).

## 2. Les 2 erreurs console — expliquées, dites

- `/api/live/events` avorté à la navigation : le flux live est coupé
  quand on quitte la page — **bénin par nature** (aucun impact) ;
- `fonts.googleapis.com` inaccessible dans ma sandbox : **CONSTAT
  RÉEL** — les polices (Inter, JetBrains Mono) dépendent du CDN Google
  (préconnect + stylesheet dans le shell ET les pages legacy de
  terminal.py), aucun fichier local. Conséquences : offline/PWA en
  polices système, ping Google à chaque chargement. Le CDN est
  accessible via le proxy → **le lot 81 rapatriera les polices en
  auto-hébergé** (fichiers woff2 locaux, plus aucune requête externe).

## 3. Verdict : parcours SAINS — un chantier réel identifié pour le lot 81

## 4. Preuves

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/ -q → 1714 passed, 2 skipped   (baseline tenue)
tools/user_journeys.js → 14 étapes, 0 échec
tools/rc_short_audit.js → RC COURTE : GO — 0 défaut (SW v125)
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 5. Mini-bilan de tournée (lots 76-80)

5 lots : 2 défauts réels corrigés (href="#", cache des données
personnelles), 2 classes documentées saines (libellés FR, fraîcheur),
parcours 14/14, 8 gardiens ajoutés, outil parcours versionné, suite
1706 → 1714. Prochain chantier concret : polices auto-hébergées (81).
