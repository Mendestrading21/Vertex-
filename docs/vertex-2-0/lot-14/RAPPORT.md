# Lot 14 — Fondations et shell : VÉRIFICATION (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Mesures

- `audit_runtime.py --enforce-target` : **code 0** — 12 pages en 200, zéro
  collision de route, routeur persistant chargé.
- Navigateur réel (Chromium), 12 pages × 3 largeurs (1600/1024/390) :
  **36/36 sans défaut** — 200 partout, 0 erreur console, 0 pageerror,
  0 débordement horizontal (390 px compris).
- `/api/client-log` après parcours : `{"count":0,"errors":[]}`.
- Barre mobile présente à 390 px (Aujourd'hui/Opportunités/Portefeuille/
  Suivi/Performance/Plus) ; états honnêtes partout (« — », « n/d »,
  « Analyse uniquement · aucun ordre », « âge inconnu ») — réseau sortant
  coupé dans cet environnement = cas de panne RÉEL, bien rendu.
- Captures : `captures-verification/` (36 PNG) ; détail JSON :
  `verification-navigateur.json`.

## Défaut trouvé et corrigé

**Fuite d'un jeton interne anglais** : à 390 px, scan tourné sans
contributeur, l'étape DONNÉE de la DecisionTrace affichait « unavailable »
brut (terminal.py:515 → briefing.py rendait `str(source)` sans mapper le
jeton). Corrigé (`briefing.py`) : « Aucune source · aucune source n'a
répondu au scan », distinct du cas « aucun scan servi » ; une vraie source
(yfinance+stooq…) reste affichée. Banc né rouge :
`tests/test_trace_source_lot14.py` (3 bancs). Service worker bumpé
**v264** + 4 tests épinglés mis à jour (dont `test_design_system_page_lot187`, absent de la liste historique « 3 tests » des règles internes — liste corrigée de fait).

## Tickets restants du lot 0 (inchangés, décision humaine)

VX2-DESIGN-02 partiellement soldé par cascade (vertex-2-0.css chargée en
DERNIER remappe les jetons — 4 feuilles définissent encore des :root, dette
cosmétique) ; VX2-DESIGN-03 (hex en dur) ; VX2-CLEANUP-01 (neon-glass.css
non servie — suppression = autorisation humaine) ; VX2-CLEANUP-03 (128 Mo
PNG suivis).

## Verdict

Fondations et shell : **CONFORMES au blueprint**, un défaut d'honnêteté
corrigé. Phase D continue page par page (lots 15-19 = vérifications).
