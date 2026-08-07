# SKYLER LOT 211 — Entretien : le dernier littéral couleur nu des pages → tokens

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-211` (base : lot 210 fusionné)

## Livré

### 1. Ré-examen du constat « movers » du lot 199 — bénin

La carte movers de Système (`#vx-brain-movers`) ne se rend pas en démo
— vérifié : ce n'est PAS un trou silencieux. L'hôte n'est créé que si
`movers.length`, et l'absence de cotations est déjà couverte par
l'état honnête de la table juste en dessous (« Aucune cotation web
pour l'instant… »). Constat clos.

### 2. Dette RÉELLE trouvée et soldée dans le même bloc

`system_page.py` L325 : les barres movers coloraient en HEX NUS
(`'#36c889'`/`'#ed655c'`) au lieu des tokens — le dernier littéral
couleur nu des pages (balayage complet : toutes les autres
occurrences sont des lookups de tokens AVEC fallback, motif légitime
`cc('amber','#…')` / `cssv('--vx-positive','#…')`).

Correctif : `VXCharts.colors.positive` / `VXCharts.colors.negative`
(VXCharts garanti présent — la branche est gardée par
`window.VXCharts && VXCharts.barCard`).

## Décision SW

Bump `td-shell-v168` → `v169` + 5 gardiens : la couleur rendue peut
changer subtilement (hex figé → vraie valeur du token) et le correctif
doit atteindre les clients en cache.

## Accros

Aucun. Note honnête : pas de capture possible — la carte movers exige
des cotations web (absentes en démo) ; preuve par le code (import OK,
gardien de syntaxe JS inline dans la suite) et par le balayage.

## Preuves

- Balayage `'#xxxxxx'` sur toutes les pages : 1 seul littéral nu
  (soldé) ; le reste = fallbacks de tokens légitimes.
- Suite complète : **2466 passed / 2 skipped**.

## Suite

LOT 212 : entretien suivant ou directive. Mini-bilan 211-215 au
lot 215. Purge terminal.py toujours EN ATTENTE d'accord humain.
