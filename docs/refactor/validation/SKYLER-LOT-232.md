# SKYLER LOT 232 — Vues internes à 390px : 1 débordement réel trouvé et soldé (.vx-update replie)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-232` (base : lot 231 fusionné)

## Objet

Le protocole discriminant du lot 222 appliqué aux **10 VUES internes à
onglets** — jamais balayées (seules les pages racines l'avaient été) —
en contexte navigation : /opportunities options|anomalies|calendar,
/options volatility|positioning, /markets sectors|volatility|breadth,
/portfolio watchlist|risk.

## Mesure (avant correctif)

- **9 vues sur 10 : 0 défaut** (overflowX 0, 0 dépassement droit,
  0 marqueur malhonnête, 0 erreur console) ;
- **1 dépassement RÉEL** : `/portfolio?view=risk` — la ligne de
  fraîcheur/source `.vx-update` du bloc knowledge graph
  (« À l'instant · knowledge graph (secteur déclaré · co-mouvement ·
  catalyseurs datés…) », 562 px, `white-space:nowrap`) finissait à
  **591 px** — 201 px coupés hors écran. Même famille que le lot 222 :
  un nowrap sans repli.

## Correctif minimal — `responsive.css`, bloc ≤768 px

```css
.vx-update{white-space:normal;overflow-wrap:anywhere}
```

La ligne de fraîcheur **replie** au lieu de déborder. L'ellipse a été
REFUSÉE délibérément : c'est une info d'honnêteté (traçabilité de la
source des données) — elle doit rester entièrement lisible. Aucun
changement desktop.

## Vérification (après)

- `/portfolio?view=risk` : la ligne replie (361 px ≤ 390),
  `white-space: normal` effectif ✔ ;
- balayage complet des 10 vues rejoué : **0 dépassement, 0 erreur
  console partout** ✔ ;
- captures avant/après envoyées.

## Décision SW

**Bump `td-shell-v172` → `td-shell-v173`** + les 5 gardiens : CSS du
shell (composant `.vx-update` utilisé par toutes les cartes) — le
correctif doit se déployer.

## Preuves

- Suite complète : **2486 passed / 2 skipped** (gardiens SW mis à
  jour ; défaut de géométrie navigateur, hors de portée de pytest).

## Suite

LOT 233 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
