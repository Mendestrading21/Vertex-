# SKYLER LOT 229 — Cycle drawer/modal au CLAVIER : constat comportemental (0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-229` (base : lot 228 fusionné)

## Objet

Complément COMPORTEMENTAL des lots 209/210 (qui prouvaient les
attributs aria-hidden/inert) : dérouler le vrai parcours clavier dans
le navigateur — clic réel sur le déclencheur, Échap, retour de focus.

## Protocole (Playwright, DEMO, 1440×900, page `/`)

1. état initial ; 2. clic réel `#vx-notifs-btn` (drawer) ; 3. Échap ;
4. `VX.shell.openModal` (chemin produit) ; 5. Échap ; 6. drawer +
modal ouverts ensemble puis UN SEUL Échap (chemin closeAll). À chaque
étape : `data-open`, `aria-hidden`, `inert`, overlay, élément focusé.

## Résultat — 0 défaut, cycle exemplaire

| Étape | Attendu | Mesuré |
|---|---|---|
| Initial | 2 panneaux fermés, aria-hidden+inert | ✔ (open=0, hidden, inert ×2) |
| Drawer ouvert (clic réel) | attributs levés, overlay, focus DANS le panneau | ✔ (open=1, focus sur un bouton du panneau) |
| Échap | fermé, attributs reposés, **focus revenu au déclencheur** | ✔ (focus = `vx-notifs-btn`) |
| Modal ouvert | attributs levés, focus piégé dedans | ✔ |
| Échap | fermé, focus revenu au déclencheur précédent | ✔ |
| Les 2 ouverts + 1 Échap | les DEUX reposent aria-hidden/inert | ✔ (focus → body : closeAll ne peut pas choisir UN déclencheur — limitation connue, pas un défaut) |
| Erreurs console | 0 | ✔ |

Observation classée : le modal s'ouvre SANS l'overlay partagé — VOULU,
son conteneur est lui-même plein écran (`position:fixed; inset:0`,
`components.css` L110) et centre la boîte ; l'overlay sert au drawer.
Échap + boutons `data-close-modal` + piège de focus câblés.

Aucun correctif nécessaire — **constat honnête, aucun code touché**.
(Le retour de focus `lastFocus?.focus?.()` posé au lot 209 fonctionne
en conditions réelles — c'est précisément ce que ce lot prouve.)

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : constat pur.

## Preuves

- JSON du cycle complet (6 états × 5 mesures) produit par le
  protocole ; synthèse dans ce rapport.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 230 : MINI-BILAN 226-230. Purge terminal.py toujours EN ATTENTE
d'accord humain explicite.
