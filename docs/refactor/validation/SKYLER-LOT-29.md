# SKYLER V2 — LOT 29 : export souverain de la mémoire

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-29-memory-export`
(base : `integration/vertex-skyler-v2` @ `a69b705`) · Mode : travail continu
(directive utilisateur « go sans validation humaines », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) type de catalyseur dans le ledger,
(b) drill-down UI d'une cellule de calibration, (c) export JSON de la
mémoire, (d) fuzz déterministe du moteur. Choix : **(c) export souverain**.

- Les fichiers runtime (`skyler_memory.json`, `skyler_sessions.json`,
  `skyler_journal.json`) sont **gitignorés et périssables** : un disque
  perdu = l'historique décisionnel du trader perdu. C'est la donnée la
  plus précieuse du programme (le ledger immuable) et elle n'avait
  **aucune sortie de secours**. L'export la rend souveraine.
- (a) exige un nouveau champ gelé → bump moteur + découpe de calibration,
  plus lourd, mieux placé après davantage d'échantillons mesurés ;
- (b) exige une API cellule→décisions dédiée, dépend de cellules mesurées
  qui n'existent pas encore en démo ;
- (d) est partiellement couvert par la batterie adversariale du lot 12.

Le lot (c) est le plus petit lot à valeur maximale immédiate : lecture
seule, zéro bump moteur, zéro risque sur les invariants.

## 2. Périmètre livré

### 2.1 Route `GET /api/skyler/memory/export` (nouvelle)

`vertex/app/routes/analysis_api.py` — placée AVANT
`/api/skyler/memory/<decision_id>` (le segment statique gagne dans Flask,
ordre documenté). Bundle JSON strictement lecture seule :

- `exported_at` : horodatage UTC réel (`%Y-%m-%dT%H:%M:%SZ`) ;
- `versions` : `decision_engine` (0.8.0), `memory_schema`,
  `packet_schema` — indispensable pour réimporter sans mélanger les
  versions (règle : jamais recomputer un record d'une autre version) ;
- `memory` : `skyler_memory.json` complet (ledger + outcomes) ;
- `sessions` : `skyler_sessions.json` (clôtures datées) ;
- `journal` : `skyler_journal.json` (journal de calibration) ;
- `note` : phrase explicite « export lecture seule … » ;
- magasin absent → forme vide honnête (`empty_memory()` / `empty_log()` /
  `[]`), jamais inventée ;
- en-tête `Content-Disposition: attachment;
  filename="skyler_export_YYYYMMDD.json"` → téléchargement direct.

Aucune écriture : la route ne fait que `load_json`. Prouvé par test de
comparaison octet-à-octet des fichiers avant/après l'appel.

### 2.2 Surfaçage UI — carte Mémoire (page Performance, `/journal`)

`vertex/ui/pages/performance_page.py` : bouton fantôme
`Exporter →` (lien `href="/api/skyler/memory/export"` + attribut
`download`) dans l'en-tête de la carte Mémoire, et la ligne-question
gagne « L'export est ta sauvegarde souveraine ». Aucun JS nouveau —
un lien natif suffit (pas de fetch, pas d'état).

### 2.3 Service worker

Shell visible modifié → bump `td-shell-v100` → `td-shell-v101`
(`vertex/app/routes/system.py` L211) + les 4 gardiens mis à jour
(prospectifs `>= 101`, assertions vN-1 → `v100` absent) :
`test_production_guards_canonical.py`, `test_reconstruction_today.py`,
`test_redesign_ui.py`, `test_ui_v3.py`.

## 3. Méthode — rouge d'abord

`tests/test_memory_export_lot29.py` (7 tests) écrit AVANT
l'implémentation ; confirmé rouge : **6 failed / 1 passed** (tous les
tests de comportement rouges — route absente, bouton absent, SW v100).
Après implémentation : **7 passed**.

Couverture : bundle complet des 3 magasins + versions ; en-tête de
téléchargement ; magasins vides honnêtes ; **lecture seule stricte**
(octets identiques avant/après) ; JSON valide en aller-retour ; bouton
Exporter présent sur `/journal` ; SW ≥ v101 et v100 absent.

## 4. Preuves

```text
python -m pytest tests/test_memory_export_lot29.py -q
→ 7 passed in 1.52s

python -m compileall -q terminal.py vertex   → exit 0
python -m pytest tests/ -q
→ 1522 passed, 2 skipped in 8.93s            (baseline 1515 → +7)
```

## 5. Invariants tenus

- READONLY absolu — la route n'écrit rien (prouvé octet-à-octet) ;
- données réelles uniquement — magasins vides rendus vides, horodatage
  réel, versions réelles du moteur ;
- moteur **inchangé** (0.8.0, aucun bump — l'export ne décide rien) ;
- fichiers runtime jamais commités (supprimés avant commit) ;
- gardiens prospectifs (`>= 101`) ;
- `main` intacte ; aucun ordre passé ; pas d'aléatoire.

## 6. Backlog restant (candidats lot 30)

1. Type de catalyseur dans le ledger gelé (earnings/macro/note) →
   découpe `by_catalyst_type` en observation ;
2. Drill-down UI d'une cellule de calibration (cellule → décisions) ;
3. Fuzz déterministe ciblé des nouveaux chemins (export compris) ;
4. RC courte périodique (audit léger navigateur + client-log).

**Arrêt après ce lot — validation humaine requise.**
