# SKYLER V2 — LOT 137 : passe n°12 — poids de position en barre de verre avec repère du plafond

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-137`
(base : `integration/vertex-skyler-v2` @ `360f1b7`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
portfolio_page.py + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /portfolio?view=positions & Synthèse)

La table canonique des positions affichait le POIDS en chiffre nu
(« 65,2 % / 15 % ») — la donnée la plus disciplinaire du portefeuille
(la Constitution plafonne chaque tier) se lisait comme n'importe
quel nombre.

## 2. Amélioration (wgtBar, portfolio_page.py)

```text
le poids devient une MINI-BARRE de verre avec REPÈRE DU PLAFOND :
  le tick à 60 % du rail marque le plafond du tier (ex. 15 %) —
  sous 80 % du plafond → positive, proche → warning, AU-DESSUS →
  negative avec halo. Le chiffre éducatif d'un poids, c'est sa
  distance au plafond.
sans tier connu (démo, entrée manuelle) : échelle simple 0-100 %,
  aucun plafond inventé — honnêteté conservée
valeur % et mention « / plafond % » conservées · color-mix sur
  tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v145` → `td-shell-v146` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v146)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (Positions)
```

## 4. Suite

LOT 138 : passe n°13 (candidats : Synthèse Portefeuille, page
Aujourd'hui — tuiles KPI, design system).
