# Lot 21 — Responsive, accessibilité et netteté : VÉRIFICATION (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Mesures (navigateur réel Chromium)

- **Responsive** : 12 pages × 7 largeurs (390/430/768/1024/1280/1440/1600)
  = 84 combinaisons — **0 débordement horizontal, 0 erreur console,
  0 échec de navigation**.
- **Clavier** : skip-link « Aller au contenu principal » premier arrêt de
  tabulation ; les 6 premiers arrêts ont tous un focus VISIBLE (outline ou
  box-shadow calculés ≠ none).
- **Reduced motion** : émulation `prefers-reduced-motion: reduce` — page
  d'accueil sans erreur.
- **Zoom 200 %** : équivalent 640 px CSS (device_scale_factor 2) —
  0 débordement horizontal.
- **HiDPI** : rendu à facteur 2 sans défaut.
- **Contraste** : la couche finale a déjà relevé `--vx-smoke`/`--vx-text-faint`
  au niveau AA MESURÉ sur la surface la plus claire (vertex-2-0.css:41-52,
  5,91:1 — travail du checkpoint, trace SW v222) ; l'accent IA a rejoint
  l'argent (lot 20).
- **Touch/mobile** : barre mobile à 390 px vérifiée au lot 14 (captures).

## Verdict

CONFORME — aucun correctif nécessaire, aucun changement de code dans ce
lot (donc pas de bump service worker).

## Limites consignées

- **Lighthouse budgets** : non exécutable ici (réseau sortant coupé,
  pas de chrome-launcher autorisé vers l'extérieur) — à passer lors de
  l'acceptation (contrôle 150), budgets à fixer à ce moment-là.
- Pages mesurées en mode dégradé (sans données) : les tableaux/graphiques
  PEUPLÉS à 390 px restent à re-vérifier sur scan réel.
- `430` et `1440` px vérifiés ici pour la première fois (le lot 14 avait
  fait 390/1024/1600).
