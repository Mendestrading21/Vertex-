# Lot 16 — Marchés et Opportunités : VÉRIFICATION (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Mesures (navigateur réel, 1600 px, pleine page)

**Marchés** : CONFORME en mode dégradé — question en 5 s (« Dans quel
environnement la stratégie opère-t-elle ? »), barre de contexte
UNIVERS/NATURE/FRAÎCHEUR (« Scan non horodaté — âge inconnu » honnête),
6 sous-vues (Synthèse/Macro/Indices/Secteurs/Participation/Volatilité),
« RÉGIME NON QUALIFIÉ » avec explication et **nouveau risque bloqué**,
chaque carte vide renvoie vers Système → Données. Zéro squelette
perpétuel, zéro anglais, zéro erreur console.

**Opportunités** : CONFORME en mode dégradé — 7 sous-vues (Radar/Actions/
ETF/Options/Anomalies/Catalyseurs/Positions × moteur), état vide qui
explique la CAUSE et pointe la barre de contexte. Zéro défaut d'état.

## Livré

**Delta d'entonnoir affiché** (consigné au lot 12, contrat Radar
« changements depuis le dernier scan ») : la carte Entonnoir rend
`fn.delta` — « Premier scan — pas encore de comparaison » honnête,
« Aucun changement d'actionnables… », ou « Entrés : … · Sortis : … »
(texte neutre, pas de sur-coloration ; listes bornées côté serveur).
Service worker **v266** + 4 épingles.

## Preuves

- `tests/test_delta_entonnoir_ui_lot16.py` : 2 bancs nés rouges → verts.
- Captures pleine page : `markets-full.png`, `opportunities-full.png`.
- Suite : **4368 passés · 153 ignorés · 0 échec**.

## Limites consignées

- Réseau sortant coupé dans cet environnement : les vues PEUPLÉES
  (heatmap secteurs, screener chargé, entonnoir avec étages non nuls,
  delta avec listes) n'ont pas pu être vérifiées visuellement — le rendu
  du delta est prouvé au niveau HTML servi + bancs. À re-vérifier sur un
  scan réel (contrôle 150 / acceptation humaine).
- Quand zéro ligne scorée, l'état vide remplace toute la vue Radar
  (entonnoir compris) : préséance de l'honnêteté, comportement voulu.

## Rollback

`git revert` du commit du lot.
