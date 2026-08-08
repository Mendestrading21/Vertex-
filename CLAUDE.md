# VERTEX — Guide pour les sessions Claude (local & cloud)

Terminal d'ANALYSE de trading (Flask, port 5002). **Lecture seule : aucun ordre n'est jamais passé** — invariant produit absolu (`READONLY=True` dans `vertex/app/config.py`).

## SKYLER V2 — règle prioritaire

Pour tout travail lié à l’analyse marché, aux actions, aux options, au portefeuille, aux anomalies, aux catalyseurs, à l’IA Skyler ou à la refonte associée, lire et appliquer en premier :

```text
.claude/skills/vertex-skyler-v2/SKILL.md
```

Branche d’intégration :

```text
integration/vertex-skyler-v2
```

Commande initiale obligatoire :

```text
/vertex-skyler-v2 audit
```

Une invocation exécute un seul lot. Claude doit produire les preuves, mettre à jour `docs/skyler/STATUS.md`, créer un rapport de validation et s’arrêter. Aucun lot suivant sans validation humaine explicite.

Ne jamais travailler directement sur `main`. Les anciennes branches V4/Prism sont des références historiques et ne doivent pas devenir la base de Skyler V2.

## Lancer & vérifier
- App : `python terminal.py` (ou `.claude/launch.json` → serveur « vertex », port 5002). Windows : `Lancer_VERTEX.bat`.
- Tests : `python -m pytest tests/ -q` → **doivent passer à 100 %** avant tout commit.
- Santé : `GET /healthz` · erreurs JS clients : `GET /api/client-log` (doit rester à 0) · état live : `GET /api/live/status`.
- Après un changement lourd : vérifier en vrai navigateur (pas seulement curl) + 0 erreur console.

## Architecture (la vraie)
- **Monolithe** `terminal.py` (**~7 150 lignes** depuis la purge É1 du lot 323 ; il en faisait 10 743) : HTML/JS construits en chaînes Python. Modules `vertex/ui/*.py` réellement servis : `nav`, `vx_kit`, `sync_center`, `design_system`, `home_art`. ⚠️ `options_lab`, `journal`, `vault`, `signals`, `strategy_os` n'ont **plus aucun consommateur en production** (leurs pages sont mortes) — reliques en attente de décision, cf. `docs/refactor/validation/SKYLER-LOT-327.md`.
- **Moteurs** : `vertex/engines/` (decision_stack = vérité des verdicts, recommendation = façade unique + vocabulaire `__VXVOCAB`, options_lab, track_record, evidence…).
- **Routes** : `vertex/app/routes/` (Blueprints) + routes restantes dans terminal.py.
- **État partagé** : `vertex/app/state.py` (`scan_state` muté en place — ne JAMAIS réassigner).
- **Données perso utilisateur** : localStorage navigateur (`myTrades`, `myRecos`, `myFavs`, `vxJournal`, `vxAlerts`…) synchronisé serveur en blob `desk_data.json` (last-writer-wins + backup quotidien `desk_backup_*.json`).

## Règles critiques (violations = données perdues ou app cassée)
1. **Clés de sync desk** : toute nouvelle clé localStorage à synchroniser doit être ajoutée dans **LES 3 listes servies** — `DESK_KEYS` de `vertex/ui/vx_kit.py` (**source de vérité**, kit global présent sur toutes les pages), `DESK_KEYS` de `vertex/static/vertex/js/vx-entities.js`, et le **repli** de `deskKeys()` dans `vertex/ui/pages/system_page.py` (utilisé si `VXEntities` n'est pas chargé) — sinon un push l'efface côté serveur. `vertex/ui/journal.py` porte une 4ᵉ copie mais **n'est plus servi** (page morte) : la garder synchronisée est sans effet, ne pas s'y fier. Depuis la purge É1, terminal.py n'en héberge plus aucune. Tests gardiens : `tests/test_production.py::test_desk_sync_keys_single_source_of_truth` et `tests/test_strategy_os_final_guards.py::test_all_sync_keys_match`.
2. **Apostrophes françaises dans les chaînes JS** de terminal.py : toujours échapper (`aujourd\\'hui`) — deux SyntaxError silencieuses ont déjà vécu.
3. **Service worker** : tout changement de shell visible utilisateur → bump `td-shell-vN` dans `vertex/app/routes/system.py`.
4. **Données RÉELLES uniquement** : jamais de chiffre inventé affiché comme réel. Donnée absente → `—`/`n/d` honnête. Le mot « démo » ne s'affiche que si le serveur le confirme.
5. **News/textes externes** : toujours via `news_plus.sanitize_news()` avant de servir (XSS — rendus en innerHTML).
6. **desk_data.json** : ne jamais l'écraser à la main ; en cas de doute, backups `desk_backup_*.json` + `/api/desk/restore`.

## Git
- Pour Skyler V2, suivre exclusivement la gouvernance du skill `vertex-skyler-v2`.
- **`main` = version canonique publiée** — la mettre à jour SEULEMENT avec accord explicite de l'utilisateur.
- Données runtime (edge_ledger, desk_backup_*, track_meta, alerts_fired, .env, .vertex_secret) : gitignorées, jamais commitées.

## Sécurité
- Verrou d'accès : `VERTEX_CODE` dans `.env` (chargé automatiquement ; `.env.example` = modèle). `VERTEX_SECRET` indépendant sinon secret aléatoire persistant `.vertex_secret`.
- Sans code d'accès, le serveur n'écoute que 127.0.0.1 (LAN/iPhone : définir `VERTEX_CODE`, ou `VERTEX_LAN=1` en connaissance de cause).
- IBKR : `readonly=True` toujours ; worker unique avec `RequestTimeout=45` (ne pas retirer — anti-blocage).

## Utilisateur
Trader francophone, interface en FR. Compte IBKR réel connecté via TWS (lecture seule). Préfère : données réelles partout, zéro erreur, tout synchronisé automatiquement au lancement. Aucun nom personnel ne doit apparaître dans le code, l'interface ou la documentation.
