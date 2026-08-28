# Lot 14 — Fondations et shell : VÉRIFICATION (WORK_MANIFEST)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Position du lot

Le checkpoint graphique (`checkpoint/vertex-2-0-graphique-20260828`, fusionné
dans l'intégration) a DÉJÀ livré les fondations du lot 14 (trace service
worker v220→v263) : vertex-2-0.css (palette canonique Black Glass Signal
Light, --vx-smoke relevé AA mesuré → VX2-DESIGN-01 soldé), Geist/Geist Mono
préchargées, navigation groupée Piloter/Explorer/Gérer/Intelligence +
Système épinglé (NavigationManifest = NAV_GROUPS/PRIMARY_NAV, source
unique), barre mobile, palette de commandes 12 pages, vx2.py propriétaire
visuel unique, collision /options/<sym> résolue (lot 9 : zéro collision),
routeur persistant arbitré et chargé (lot 2), neon-glass.css étiquetée NON
SERVIE (v232). Ce lot est donc une **vérification runtime contre le
blueprint**, pas une refonte.

## Protocole

1. `audit_runtime.py --enforce-target` (12 pages, collisions, routeur).
2. Navigateur réel (Chromium/Playwright) : 12 pages × 1600/1024/390 px —
   statut, erreurs console, pageerror, débordement horizontal, captures.
3. `/api/client-log` après le parcours complet.
4. Tout défaut trouvé → banc rouge → correctif minimal → bump SW.

## Fichiers propriétaires

- `vertex/ui/pages/briefing.py` (correctif fuite), `vertex/app/routes/system.py`
  (bump v264) + les 3 tests qui épinglent la version.
- **NEUF** `tests/test_trace_source_lot14.py`.
- Preuves : `captures-verification/` (36), `verification-navigateur.json`.
