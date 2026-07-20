# Règles d'édition sûre Vertex

## Invariant produit ABSOLU — lecture seule
- Vertex ne passe **JAMAIS** d'ordre (live ni paper). `READONLY=True` (`vertex/app/config.py`) ; `readonly=True`
  sur les 4 workers IBKR ; 17 outils d'ordre interdits (`vertex/ai/tool_registry.py`). Gardiens :
  `test_redesign_ui.py::test_no_order_execution_in_ui`, `test_ai_api.py`. Le « Desk » = préparation + simulation +
  ticket prêt-à-coller ; jamais de transmission. **Ne jamais introduire de chemin d'ordre.**

## Avant de modifier
- Lire le vrai code d'abord. Ne pas réécrire aveuglément. Ne pas supprimer une fonctionnalité sans avoir compris
  objectif / dépendances / consommateurs (autres pages).
- Ne pas remplacer une architecture fonctionnelle pour une préférence.

## Pièges connus de ce dépôt
- **Apostrophes françaises dans les chaînes JS** (terminal.py & pages) : toujours échapper (`aujourd\\'hui`) ou
  utiliser des entités — deux SyntaxError silencieuses ont déjà existé.
- **Service worker** : changement de shell visible → bump `td-shell-vN` (`vertex/app/routes/system.py`) + les 3
  tests qui l'épinglent (`test_ui_v3.py`, `test_production_guards_canonical.py`, `test_redesign_ui.py`).
- **`scan_state`** (`vertex/app/state.py`) : muté EN PLACE, jamais réassigné.
- **Collision de route connue** : `/options/<sym>` est déclaré 2× (JSON `opt_ep` terminal.py + page `redesign.py`).
  Toute intervention options doit dédupliquer, pas aggraver.
- **Double nav** : `PRIMARY_NAV` (shell, 8 items) fait autorité ; `vertex/ui/nav.py` (10 items) est un vestige du
  monolithe legacy.

## Par lot
1. Décrire le problème → fichiers → approche → **changement limité et cohérent**.
2. `python -m pytest tests/ -q` = **100 %** avant tout commit ; byte-identique là où déterministe.
3. Relancer l'app (démo) + vérifier en **vrai navigateur** (0 erreur console, `/api/client-log`=0).
4. Corriger les régressions → mettre à jour l'audit → **rapport** (`templates/implementation-report-template.md`).
5. **Commits atomiques** (`audit(vertex):`, `refactor(ui):`, `feat(portfolio):`, `fix(ibkr):`, `test(trading):`).
   Ne jamais mélanger : refonte globale + logique trading + migration données + connexion IBKR + nettoyage.
6. Identité modèle **jamais** dans commit/PR/code. Aucun nom personnel dans code/UI/docs. Aucun secret dans l'audit.

## Sécurité
- Ne pas exposer de secret (`.env`, `VERTEX_SECRET`, clés API). Masquer les identifiants de compte dans
  captures/logs. Runtime gitignoré (edge_ledger, desk_backup_*, .vertex_secret) — jamais commité.
