# SKYLER V2 — LOT 121 : amélioration graphique n°3 — entonnoir monochrome + scatter ciblé (Opportunités)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-121`
(base : `integration/vertex-skyler-v2` @ `11f657b`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE : chaque graphique/widget de tout Vertex
au maximum le plus beau, sans jamais demander.**
Moteurs INTACTS — diff = chart-core.js + opportunities_page.py + SW +
gardiens + docs.

## 1. Diagnostic (capture AVANT, /opportunities)

L'entonnoir de sélection était le pire de la page : couleurs disparates
sans logique (blanc, beige, violet, jaune), trapèzes bruts, CHIFFRES
DOUBLÉS à chaque étage (valeur + %). Le scatter : zone actionnable
invisible tant qu'on ne lit pas les axes.

## 2. Améliorations

```text
C.funnel (chart-core.js) — entonnoir « ultra propre » :
  UN SEUL ton de marque en dégradé vertical brand → cyan · opacité
  qui DÉCROÎT avec la profondeur (la matière raconte la déperdition)
  · UN chiffre par étage (les % doublés supprimés — directive « pas
  de chiffres sur chiffres ») · liseré brand très fin · la plus
  forte perte marquée d'un −N discret en négatif
scatter (opportunities_page.py) — la zone actionnable (haut-droit)
  est TEINTÉE d'un dégradé positif très léger : on voit la cible
  avant de lire les axes
Aucun littéral couleur nouveau (C.colors.brand/cyan/negative/positive)
```

SW `td-shell-v129` → `td-shell-v130` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v130)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées à l'utilisateur
```

## 4. Suite

Lot 122 : amélioration graphique n°4 (page Analyse) ; lot 125 =
mini-bilan 121-125.
