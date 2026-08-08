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
3. **Service worker** : bump `td-shell-vN` dans `vertex/app/routes/system.py` dès qu'un **octet servi** change — HTML de shell **ET tout fichier sous `/static`** (CSS, JS, polices, images). Le SW met en cache les navigations + **tout `/static`** + le manifeste ; `activate` supprime tous les caches dont la clé diffère, donc **le bump est ce qui purge la copie de repli hors-ligne**. Il n'est pas là « pour que l'utilisateur voie la nouvelle interface » : le SW est *network-first* (le frais gagne toujours en ligne, repli cache au-delà de 4,5 s ou hors-ligne). Fenêtre d'exposition sans bump : visiteur déjà venu, hors-ligne ou réseau lent, servi depuis un cache assemblé à des visites différentes. Gardien : `tests/test_sw_cache_scope_lot361.py` (empreinte des assets ↔ version enregistrée ; message d'échec = marche à suivre).
4. **Données RÉELLES uniquement** : jamais de chiffre inventé affiché comme réel. Donnée absente → `—`/`n/d` honnête. Le mot « démo » ne s'affiche que si le serveur le confirme.
5. **News/textes externes** : **deux** familles de sorties, deux contrats — ne pas les mélanger (lot 358).
   - *Sortie assainie au serveur* : `/news-feed`, `/api/events/<sym>`, `/api/skyler/<sym>` → **toujours** via `news_plus.sanitize_news()` avant de servir, car leurs consommateurs injectent le titre **brut** en innerHTML. Gardien : `tests/test_xss_exits_lot177.py`.
   - *Sortie échappée au rendu* : `/api/ai/enrichment` (`vertex/ai/enrichment.py::parse_news`, cerveau Claude+web) n'appelle **pas** `sanitize_news` et ne le doit pas — son unique rendu (`system_page.py::loadBrain`) échappe déjà via `esc()`, et un assainissement serveur double-échapperait les titres légitimes. Sa sûreté tient à 3 propriétés : citations filtrées http(s) (`provenance._safe_url`), forme reconstruite et bornée (4 champs), rendu via `esc()`. Gardien : `tests/test_ai_news_exit_lot358.py`.
6. **desk_data.json** : ne jamais l'écraser à la main ; en cas de doute, backups `desk_backup_*.json` + `/api/desk/restore`. **Ce que le filet couvre vraiment** (mesuré au lot 362) : le snapshot est pris **une fois par jour**, avant la 1ʳᵉ écriture — un restore rend donc l'état d'**avant la première sync du jour** et **perd le travail de la journée** ; profondeur maximale **7 jours** (`BACKUP_KEEP`). Le last-writer-wins est **total** : un push partiel remplace le blob entier (les clés absentes disparaissent) et un push `data: {}` est **accepté** (la validation porte sur le type, pas le contenu) — l'écrasement n'a pas besoin d'être « à la main ». Le client protège bien (`vx_kit.py` : push seulement après hydratation réussie, abstention si `bootSync` échoue, re-remplissage des clés absentes) ; le scénario résiduel est un navigateur dont l'écriture localStorage échoue en silence. Gardiens : `tests/test_desk_backup_lot178.py` (chaîne de sauvegarde) et `tests/test_desk_perte_lot362.py` (caractérisation des pertes — à mettre à jour si le serveur est durci).

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
