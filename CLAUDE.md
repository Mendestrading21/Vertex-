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
- **Monolithe** `terminal.py` (**7 158 lignes**, mesuré ; il en faisait 10 743 avant la purge É1 du lot 323) : HTML/JS construits en chaînes Python. Modules `vertex/ui/*.py` restants : `nav`, `vx_kit`, `sync_center`, `design_system`, `home_art` — c'est la **liste complète**, mesurée. Les cinq reliques `options_lab`, `journal`, `vault`, `signals`, `strategy_os` ont été **supprimées** au lot 17 de la refonte Signal OS (1 624 lignes, aucun consommateur en production) : ne pas les chercher, ne pas les rétablir. Historique : `docs/refactor/validation/SKYLER-LOT-327.md` (le constat) et `docs/refactor/validation/SIGNAL-OS-17-MODULES-MORTS.md` (la suppression).
- **Moteurs** : `vertex/engines/` (decision_stack = vérité des verdicts, recommendation = façade unique + vocabulaire `__VXVOCAB`, options_lab, track_record, evidence…).
- **Routes** : `vertex/app/routes/` (Blueprints) + routes restantes dans terminal.py.
- **État partagé** : `vertex/app/state.py` (`scan_state` muté en place — ne JAMAIS réassigner).
- **Données perso utilisateur** : localStorage navigateur (`myTrades`, `myRecos`, `myFavs`, `vxJournal`, `vxAlerts`…) synchronisé serveur en blob `desk_data.json` (last-writer-wins + backup quotidien `desk_backup_*.json`).

## Règles critiques (violations = données perdues ou app cassée)
1. **Clés de sync desk** : toute nouvelle clé localStorage à synchroniser doit être ajoutée dans **LES 2 listes RÉELLEMENT SERVIES** — `DESK_KEYS` de `vertex/static/vertex/js/vx-entities.js` (fichier statique chargé par les 8 pages) et le **repli** de `deskKeys()` dans `vertex/ui/pages/system_page.py` (inline dans `/system`, utilisé si `VXEntities` n'est pas chargé) — sinon un push l'efface côté serveur. Mesuré au lot 381 : `vertex/ui/vx_kit.py` porte bien `DESK_KEYS` et sert de **référence de comparaison** aux gardiens, mais son JS (21 727 o) **n'atteint aucune des 8 pages** — le décrire comme « kit global présent sur toutes les pages » était faux ; le garder synchronisé reste utile tant qu'il sert d'ancre, mais ce n'est pas lui que le navigateur lit. `vertex/ui/journal.py` **n'existe plus** (supprimé au lot 17 avec les quatre autres reliques) : la « 4ᵉ copie » de `DESK_KEYS` qu'on lui prêtait avait déjà disparu du fichier avant sa suppression, et le fichier lui-même a suivi. Depuis la purge É1, terminal.py n'en héberge aucune. Tests gardiens : `tests/test_desk_keys_servies_lot381.py` (**garde les listes par ce qu'elles SERVENT** — le repli de `system_page` n'était couvert par rien, retirer une clé y passait les 2 754 tests), plus `tests/test_production.py::test_desk_sync_keys_single_source_of_truth` et `tests/test_strategy_os_final_guards.py::test_all_sync_keys_match` (comparaison sur disque).
2. **Apostrophes françaises dans les chaînes JS** de terminal.py : toujours échapper (`aujourd\\'hui`) — deux SyntaxError silencieuses ont déjà vécu.
3. **Service worker** : bump `td-shell-vN` dans `vertex/app/routes/system.py` dès qu'un **octet servi** change — HTML de shell **ET tout fichier sous `/static`** (CSS, JS, polices, images). Le SW met en cache les navigations + **tout `/static`** + le manifeste ; `activate` supprime tous les caches dont la clé diffère, donc **le bump est ce qui purge la copie de repli hors-ligne**. Il n'est pas là « pour que l'utilisateur voie la nouvelle interface » : le SW est *network-first* (le frais gagne toujours en ligne, repli cache au-delà de 4,5 s ou hors-ligne). Fenêtre d'exposition sans bump : visiteur déjà venu, hors-ligne ou réseau lent, servi depuis un cache assemblé à des visites différentes. Gardien : `tests/test_sw_cache_scope_lot361.py` (empreinte des assets ↔ version enregistrée ; message d'échec = marche à suivre).
4. **Données RÉELLES uniquement** : jamais de chiffre inventé affiché comme réel. Donnée absente → `—`/`n/d` honnête. Le mot « démo » ne s'affiche que si le serveur le confirme.
5. **News/textes externes** : le point de départ est que **`news_state['items']` est BRUT** — la boucle d'actualités de `terminal.py` y dépose les titres yfinance/RSS tels quels, et c'est **chaque sortie** qui neutralise. Il y a **deux** familles de sorties, deux contrats — ne pas les mélanger (lot 358).
   - *Sortie assainie au serveur* : `/news-feed`, `/api/events/<sym>`, `/api/skyler/<sym>` → **toujours** via `news_plus.sanitize_news()` avant de servir, car leurs consommateurs injectent le titre **brut** en innerHTML. Gardien : `tests/test_xss_exits_lot177.py` — dont le lot 32 a mesuré (par mutation) qu'il ne couvrait que 12 des 18 affaiblissements possibles de `sanitize_news` ; le contrat de la fonction est tenu à part par `tests/test_news_plus_lot102.py`.
   - *Sortie échappée au rendu* — le serveur **retire le balisage** (`news_plus.strip_markup`) mais **n'échappe pas** : le rendu échappe déjà, un échappement serveur en plus afficherait `AT&amp;T` et `Barron&#39;s`.
     - `/api/ai/enrichment` (`vertex/ai/enrichment.py::parse_news`, cerveau Claude+web). Sûreté : citations filtrées http(s) (`provenance._safe_url`), forme reconstruite et bornée (4 champs), rendu via `esc()` dans `system_page.py::loadBrain`. Gardien : `tests/test_ai_news_exit_lot358.py`.
     - `/api/briefing/editorial` — **la quatrième sortie, découverte au lot 32** : `daily_brief` (via `news_pipeline.collect`) et `editorial.build_narrative` composent des phrases qui **embarquent le titre externe**. Elles servaient `<img src=x onerror=…>` vivant dans `daily.what_changed`, `daily.compact`, `daily.sections[].text` et `editorial.narrative` ; aucun de ces champs n'était rendu, mais rien ne l'interdisait. Les deux seuls champs consommés (`sources`, `main_risk` dans `briefing.py`) passent par `esc()`. Gardien : `tests/test_signal_os_sortie_editoriale_lot32.py`.
6. **desk_data.json** : ne jamais l'écraser à la main ; en cas de doute, backups `desk_backup_*.json` + `/api/desk/restore`. **Ce que le filet couvre vraiment** (mesuré au lot 362) : le snapshot est pris **une fois par jour**, avant la 1ʳᵉ écriture — un restore rend donc l'état d'**avant la première sync du jour** et **perd le travail de la journée** ; profondeur maximale **7 jours** (`BACKUP_KEEP`). Le last-writer-wins est **total** : un push partiel remplace le blob entier (les clés absentes disparaissent) et un push `data: {}` est **accepté** (la validation porte sur le type, pas le contenu) — l'écrasement n'a pas besoin d'être « à la main ». Le client protège bien (`vx_kit.py` : push seulement après hydratation réussie, abstention si `bootSync` échoue, re-remplissage des clés absentes) ; le scénario résiduel est un navigateur dont l'écriture localStorage échoue en silence. Gardiens : `tests/test_desk_backup_lot178.py` (chaîne de sauvegarde) et `tests/test_desk_perte_lot362.py` (caractérisation des pertes — à mettre à jour si le serveur est durci).

## Git
- Pour Skyler V2, suivre exclusivement la gouvernance du skill `vertex-skyler-v2`.
- **`main` = version canonique publiée** — la mettre à jour SEULEMENT avec accord explicite de l'utilisateur.
- Données runtime (edge_ledger, desk_backup_*, track_meta, alerts_fired, .env, .vertex_secret) : gitignorées, jamais commitées.

## Sécurité
- Verrou d'accès : `VERTEX_CODE` dans `.env` (chargé automatiquement ; `.env.example` = modèle). `VERTEX_SECRET` indépendant sinon secret aléatoire persistant `.vertex_secret`.
- Sans code d'accès, le serveur n'écoute que 127.0.0.1 (LAN/iPhone : définir `VERTEX_CODE`, ou `VERTEX_LAN=1` en connaissance de cause).
- IBKR : `readonly=True` toujours ; worker unique avec `RequestTimeout=45` (ne pas retirer — anti-blocage).

## Couleurs — la règle réellement tenue (mesuré au lot 382)

**Identité : violet néon `#9B7BFF`** (`--vx-violet-500`), une seule et même
couleur sur l'interface **et** sur les graphiques. La rampe canonique vit dans
`vertex/static/vertex/css/tokens.css` ; `vertex/visualization/palette.py` et
`vertex/static/vertex/js/charts/chart-theme.js` en dérivent. Les anciens noms
`--vx-ember-*` / `--vx-copper-*` sont des **alias** de la rampe violette : ils
ne repeignent rien, mais leur nom ment — ne pas en introduire de nouveaux.
Deux contraintes non évidentes, apprises par l'échec : les teintes sombres de la
rampe sont volontairement décalées vers le rouge pour ne pas devenir des bleus
au sens du gardien anti-bleu, et `--vx-violet-600` vaut `#8767F2` (et non
`#7F5DF0`) pour que l'encre sombre du bouton primaire tienne 4,5:1.

L'énoncé « tokens/VXChartTheme uniquement, **aucun littéral couleur** » était
**faux** : `vertex/ui/**` contient **265 littéraux `#RRGGBB` distincts, dont 53
atteignent une page servie**. La règle que le code respecte et qu'un gardien
impose réellement est plus étroite : **aucun bleu NON-MARQUE en dur**
(`tests/test_obsidian_theme.py::test_no_blue_in_ui_pages`, vérifié par mutation —
un `#1e6fd9` échoue, un `#ff00ff` passe).

Pour tout NOUVEAU travail : préférer les tokens. Ce qui est verrouillé :
`tests/test_litteraux_couleur_servis_lot382.py` interdit la **croissance** du
nombre de littéraux servis (borne fixée à la mesure) et vérifie l'absence de bleu
non-marque **dans les octets servis**, pas seulement dans les sources.

## Utilisateur
Trader francophone, interface en FR. Compte IBKR réel connecté via TWS (lecture seule). Préfère : données réelles partout, zéro erreur, tout synchronisé automatiquement au lancement. Aucun nom personnel ne doit apparaître dans le code, l'interface ou la documentation.
