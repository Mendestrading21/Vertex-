# VERTEX — Guide pour les sessions Claude (local & cloud)

Terminal d'ANALYSE de trading (Flask, port 5002). **Lecture seule : aucun ordre n'est jamais passé** — invariant produit absolu (`READONLY=True` dans `vertex/app/config.py`).

## Lancer & vérifier
- App : `python terminal.py` (ou `.claude/launch.json` → serveur « vertex », port 5002). Windows : `Lancer_VERTEX.bat`.
- Tests : `python -m pytest tests/ -q` → **doivent passer à 100 %** avant tout commit.
- Santé : `GET /healthz` · erreurs JS clients : `GET /api/client-log` (doit rester à 0) · état live : `GET /api/live/status`.
- Après un changement lourd : vérifier en vrai navigateur (pas seulement curl) + 0 erreur console.

## Architecture (la vraie)
- **Monolithe** `terminal.py` (~10 500 lignes) : HTML/JS construits en chaînes Python. Pages extraites : `vertex/ui/*.py` (nav, options_lab, journal, vault, signals, sync_center, vx_kit, design_system).
- **Moteurs** : `vertex/engines/` (decision_stack = vérité des verdicts, recommendation = façade unique + vocabulaire `__VXVOCAB`, options_lab, track_record, evidence…).
- **Routes** : `vertex/app/routes/` (Blueprints) + routes restantes dans terminal.py.
- **État partagé** : `vertex/app/state.py` (`scan_state` muté en place — ne JAMAIS réassigner).
- **Données perso utilisateur** : localStorage navigateur (`myTrades`, `myRecos`, `myFavs`, `vxJournal`, `vxAlerts`…) synchronisé serveur en blob `desk_data.json` (last-writer-wins + backup quotidien `desk_backup_*.json`).

## Règles critiques (violations = données perdues ou app cassée)
1. **Clés de sync desk** : toute nouvelle clé localStorage à synchroniser doit être ajoutée dans **LES 4 listes** (`__DESK_KEYS` terminal.py, sSyncPush/Pull, `vertex/ui/journal.py`, `DESK_KEYS` de `vx_kit.py`) — sinon un push l'efface côté serveur. Test gardien : `tests/test_production.py::test_desk_sync_keys_single_source_of_truth`.
2. **Apostrophes françaises dans les chaînes JS** de terminal.py : toujours échapper (`aujourd\\'hui`) — deux SyntaxError silencieuses ont déjà vécu.
3. **Service worker** : tout changement de shell visible utilisateur → bump `td-shell-vN` dans `vertex/app/routes/system.py`.
4. **Données RÉELLES uniquement** : jamais de chiffre inventé affiché comme réel. Donnée absente → `—`/`n/d` honnête. Le mot « démo » ne s'affiche que si le serveur le confirme.
5. **News/textes externes** : toujours via `news_plus.sanitize_news()` avant de servir (XSS — rendus en innerHTML).
6. **desk_data.json** : ne jamais l'écraser à la main ; en cas de doute, backups `desk_backup_*.json` + `/api/desk/restore`.

## Git
- Branche de travail : `vertex-system-launch` (local) → push fast-forward sur `origin claude/vertex-system-launch-0bsizs`.
- **`main` = version canonique** — la mettre à jour SEULEMENT avec accord explicite de l'utilisateur.
- Données runtime (edge_ledger, desk_backup_*, track_meta, alerts_fired, .env, .vertex_secret) : gitignorées, jamais commitées.

## Sécurité
- Verrou d'accès : `VERTEX_CODE` dans `.env` (chargé automatiquement ; `.env.example` = modèle). `VERTEX_SECRET` indépendant sinon secret aléatoire persistant `.vertex_secret`.
- Sans code d'accès, le serveur n'écoute que 127.0.0.1 (LAN/iPhone : définir `VERTEX_CODE`, ou `VERTEX_LAN=1` en connaissance de cause).
- IBKR : `readonly=True` toujours ; worker unique avec `RequestTimeout=45` (ne pas retirer — anti-blocage).

## Utilisateur
Trader francophone, interface en FR. Compte IBKR réel connecté via TWS (lecture seule). Préfère : données réelles partout, zéro erreur, tout synchronisé automatiquement au lancement. Aucun nom personnel ne doit apparaître dans le code, l'interface ou la documentation.
