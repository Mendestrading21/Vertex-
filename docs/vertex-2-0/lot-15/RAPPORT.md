# Lot 15 — Aujourd'hui et Calendrier : VÉRIFICATION (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Protocole

Pages `/` et `/calendar` vérifiées contre la matrice du blueprint
(`page-widget-intelligence-blueprint.md`) au navigateur réel (1600 px,
pleine page) + DOM : question, zone dominante, provenance/fraîcheur,
action primaire, états, français, jetons internes.

## Mesures

**Calendrier** : CONFORME. Question en 5 s ; agenda chronologique dominant
avec filtres (horizon/type/périmètre « Mes positions seulement ») ;
fraîcheur affichée (« Horodatage indisponible » honnête) ; états vides
exemplaires (« Aucun événement… Ce n'est pas une absence de données : le
calendrier a répondu ») ; table « Couverture du calendrier » déclarant
chaque catégorie Alimentée/Aucune source avec sa source ; avertissement
« Calendrier officiel épuisé » au-delà des dates publiées. Aucun défaut.

**Aujourd'hui** : conforme (DecisionTrace dominante, 8 sections ancrées,
états honnêtes partout, bannière démo conditionnelle) SAUF un défaut réel :

- **Carte morte « Ce qui a changé »** : `#vx-diff` portait un squelette
  PERPÉTUEL — aucun remplisseur dans tout le dépôt, alors que le
  producteur canonique existe (`market_context.changes_since_prev`,
  « jamais inventé », déjà transporté par `/scan`). `#vx-mkt-diff` était
  un second nœud mort. Corrigé : `loadDiff(scan)` branché au boot, trois
  états honnêtes (pas de base de comparaison / rien de notable / liste
  échappée via `VX.esc`), nœud mort retiré (test de retrait du blueprint).
  Vérifié en direct après redémarrage : état vide honnête rendu, zéro
  squelette, zéro erreur console. Service worker **v265** + 4 épingles.

## Preuves

- `tests/test_diff_session_lot15.py` : 3 bancs nés rouges → verts.
- Captures pleine page : `accueil-full.png`, `calendar-full.png`.
- Suite complète : **4366 passés · 153 ignorés · 0 échec** (136 s).

## Rollback

`git revert` du commit du lot.
