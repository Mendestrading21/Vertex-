# SKYLER V2 — LOT 131 : passe n°6 — stress tests Portefeuille en verre + pire scénario mis en avant

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-131`
(base : `integration/vertex-skyler-v2` @ `ca57efa`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
portfolio_page.py + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /portfolio?view=risk & performance)

Vue Performance : états vides honnêtes en démo (équité/drawdown/
saisonnalité/contribution — corrects). Vue Risque : jauge HHI et donut
sectoriel héritent déjà du noyau verre. Le widget fait main encore
BRUT : les barres des **STRESS TESTS (§26)** — aplats rouges uniformes
pleine largeur, et le pire scénario noyé dans la liste.

## 2. Améliorations (stress bars, portfolio_page.py)

```text
matière VERRE : chaque barre est un dégradé de sa propre couleur,
  doux au zéro → dense à l'extrémité de l'impact — via color-mix
  sur les tokens (aucun littéral nouveau)
le PIRE scénario est MIS EN AVANT : libellé en négatif gras + halo
  doux sur sa barre + « pire scenario » dans l'aria — LE chiffre
  éducatif d'un stress test (déjà repris dans Risques priorisés)
axe, étiquettes tabulaires, table détaillée et note inchangés
```

SW `td-shell-v139` → `td-shell-v140` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v140)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (vue Risque)
```

## 4. Suite

LOT 132 : passe n°7 (candidats : Options desk /options sous-vues,
Opportunités vues restantes — radar/anomalies/calendrier).
