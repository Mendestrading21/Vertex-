# SKYLER V2 — LOT 129 : passe n°4 — rails sémantiques rétablis + courbe des taux lisible (Macro/Volatilité)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-129`
(base : `integration/vertex-skyler-v2` @ `6bb3c26`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
neon-glass.css + markets_page.py + chart-core.js + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /markets?view=volatility & macro)

Trois défauts : (a) **bug visuel réel** — les rails CALME↔STRESS et
DÉFENSE↔ATTAQUE étaient INVISIBLES : une règle neon-glass
(`background:rgba(0,0,0,.28)!important`) écrasait le dégradé
sémantique du rail (vérifié au navigateur : `backgroundImage: none`) ;
(b) la courbe des taux US traçait « Actuelle » en brand (quasi blanc)
et « Séance préc. » en gris — indistinctes ; (c) leurs étiquettes de
fin de ligne s'écrivaient l'une SUR l'autre (même hauteur d'arrivée).

## 2. Améliorations

```text
rails (neon-glass.css) : l'override noir !important supprimé — les
  rails retrouvent leur dégradé sémantique cockpit.css (calme vert →
  stress rouge ; défense rouge → attaque vert), seul l'arrondi reste
  harmonisé. Correction délibérée d'une règle qui prétendait
  « conserver le remplissage sémantique » et faisait l'inverse
courbe des taux (markets_page.py) : « Actuelle » passe en cyan
  (C.colors.info) points compris — la courbe du jour se détache
  enfin de l'ombre grise de la veille ; légende alignée
C.endDotsPlugin (chart-core.js) : ANTI-COLLISION des noms de série —
  deux lignes qui finissent à la même hauteur écartent leurs
  étiquettes d'au moins 11 px (toutes les multiLine héritent)
aucun littéral couleur nouveau
```

SW `td-shell-v137` → `td-shell-v138` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v138)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Volatilité + Macro)
```

## 4. Suite

LOT 130 : passe n°5 + MINI-BILAN 126-130.
