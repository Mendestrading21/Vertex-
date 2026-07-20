# 12 — Audit accessibilité

Cible : contraste **AA**, focus visible, navigation clavier, et **le risque ne dépend jamais uniquement du
rouge/vert** (signe/icône/label en plus). À vérifier page par page via `vertex-ui-auditor` + audit navigateur réel.

## Ce qui est en place
- `aria-current` sur l'item de nav actif (gardien `test_redesign_ui.py::test_active_nav_item_marked`).
- Icônes SVG inline sobres dans le shell (`_ICONS`), pas d'emojis comme unique porteur de sens dans la nav canonique.
- Onglets = liens (`<a class="vx-tab">`) → navigables au clavier nativement.

## Findings
- **A11Y-01 (P1) — Sémantique couleur seule.** La palette encode positif/négatif/risque par la **couleur**
  (vert/corail/ambre). Vérifier que chaque indicateur de risque/direction porte **aussi** un signe (`+`/`-`),
  une icône ou un label (daltonisme). Prioriser : verdicts de décision, deltas de prix, jauges de risque, greeks.
- **A11Y-02 (P2) — Focus visible.** Vérifier un anneau de focus visible sur boutons, onglets, champs, cartes
  cliquables (tokens `--vx-*` dédiés). Ne pas supprimer l'outline sans alternative.
- **A11Y-03 (P2) — Contraste AA.** Auditer le texte gris sur verre translucide (labels secondaires, footers de
  provenance) — les gris faibles sur fond sombre translucide risquent < 4.5:1. Mesurer, ajuster les tokens.
- **A11Y-04 (P2) — Cibles tactiles & clavier.** Boutons de topbar (Refresh, Connexions, Notifications) et
  command palette : taille de cible ≥ 40 px, ordre de tabulation logique, `Esc` ferme la palette.
- **A11Y-05 (P3) — Réduction de mouvement.** `prefers-reduced-motion` déjà pris en compte côté graphes
  (`chart-core.js` : `reduced` désactive les plugins de glow). Étendre aux animations de shell (`vnIn`, pulses).

## Méthode
Vérification navigateur réel (Playwright) : tabulation complète, contraste (outils intégrés), rendu sans couleur.
DoD a11y par page : `references/page-definition-of-done.md`.
