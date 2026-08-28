# Lot 30 — Performance CSS (bundle) et a11y peuplée à 100 (RAPPORT)

Date : 2026-08-28

## Livré

1. **Bundle CSS** : la coque charge UNE feuille (`/asset/css/bundle.css`,
   versionnée par la coque, immutable) au lieu de 19 requêtes en chaîne
   critique. L'ordre de cascade devient un CONTRAT nommé
   (`vertex/ui/shell.CSS_ORDER`) ; l'assemblage se fait EN MÉMOIRE au
   premier appel (aucun artefact généré dans l'arbre suivi) ; les feuilles
   individuelles restent servies (développement, bancs, rollback).
2. **A11y peuplée 96 → 100** (défauts que seule la page PEUPLÉE montrait) :
   - `opacity:.66/.7` sur `.vx-chart-question` abaissait le jeton AA à
     3,84:1. Trois couches fautives : glass.css (annulée par la couche
     finale §30) ET deux mini-thèmes locaux de page (briefing,
     opportunities) qui écrasaient tout — retirés, avec un GARDIEN qui
     interdit toute opacité locale future sur les questions.
   - le bouton plein écran des graphiques portait un texte visible
     (« ⤢ Agrandir ») absent de son aria-label — aligné (commande vocale).

## Mesures Lighthouse (peuplées, émulation mobile standard)

| page | avant (lot 29) | après | requêtes CSS |
|---|---|---|---|
| accueil | a11y 100 · FCP 3,5 s | perf 68 · a11y 100 · FCP 3,0 s | 19 → **1** |
| opportunités | **a11y 96** · FCP 3,4 s | perf 60 · **a11y 100** · FCP 2,9 s | 19 → **1** |
| marchés | a11y 100 · FCP 3,3 s | perf 63 · a11y 100 · FCP 2,9 s | 19 → **1** |

FCP : **−15 %**. Le LCP peuplé (7,5 s simulés) est désormais dominé par le
rendu des graphiques/JS, plus par le CSS — prochaine piste nommée : budget
JS par page et différé des graphiques sous le pli (lot futur, jamais un
raccourci discret).

## Preuves

- 7 bancs nés rouges → verts (bundle : lien unique, cascade exacte,
  immutable, jamais sur disque ; a11y : contraste, aria, gardien
  anti-opacité) ; 3 bancs historiques réécrits vers la cible.
- Suite : **4415 passés · 152 ignorés · 0 échec**. SW **v272**.
