# Vertex — RC1 Rollback Procedure

> But : revenir à un état antérieur **sans perte**, en cas de problème détecté sur la
> Release Candidate. `main` (`origin/main` = `2b4fa70`) n'a **jamais** été modifié :
> le rollback ultime est trivial. Toute la refonte vit sur `agent/vertex-total-rebuild`.

## Points de repère (SHA)
- **Base intouchée** : `origin/main` = `2b4fa70` (état pré-refonte, canonique).
- **Tip refonte produit** (PR n°7) : `4b98726`.
- **RC1 stabilisation** : commits `6cfcb18` (code mort), `f201528` (cohérence/éditorial),
  puis les commits de documentation RC1 (voir `git log`).

## Cas 1 — Rien n'a été fusionné dans `main` (état actuel)
Aucune action de rollback n'est nécessaire : `main` est déjà l'ancienne version.
Pour abandonner la RC1, il suffit de **ne pas fusionner** `agent/vertex-total-rebuild`.
La branche reste disponible pour reprise ultérieure.

## Cas 2 — Revenir en arrière DANS la branche (annuler la stabilisation RC1)
Les changements RC1 sont en petits commits réversibles :
```
git checkout agent/vertex-total-rebuild
git revert --no-edit <sha_doc_rc1> f201528 6cfcb18   # annule RC1, garde PR 1→7
```
ou, pour repositionner la branche sur la fin de PR n°7 :
```
git reset --hard 4b98726        # retour au tip PR n°7 (perte des commits RC1 locaux)
```
> `revert` est préféré (préserve l'historique). Les 6 fichiers de graphes supprimés
> restent récupérables via l'historique Git (`git show 6cfcb18^:vertex/static/vertex/js/charts/vol-surface.js`).

## Cas 3 — Après une fusion éventuelle dans `main` (FUTUR, sur accord explicite)
Si un jour `agent/vertex-total-rebuild` est fusionné dans `main` puis qu'un incident
survient :
```
git checkout main
git revert -m 1 <sha_du_merge>   # annule le merge, restaure 2b4fa70
git push origin main
```
Aucune donnée utilisateur n'est affectée : les données desk vivent dans le
navigateur (localStorage) + blob serveur `desk_data.json` avec backups quotidiens
`desk_backup_*` — indépendants du code déployé.

## Données & état runtime (jamais perdus par un rollback code)
- **Données perso** : localStorage navigateur ↔ `desk_data.json` (last-writer-wins) +
  backups quotidiens. Restauration : `/api/desk/restore` ou import JSON via
  Système → Réglages.
- **Service worker** : après rollback, l'ancienne version reprend la main ; le cache
  `td-shell-vN` s'invalide au prochain chargement (l'ancien SW supprime les caches ≠ à
  sa version). Forcer si besoin : recharger deux fois (skipWaiting + clients.claim).
- **Secrets** : `.env` / `.vertex_secret` gitignorés — non affectés par un rollback code.

## Vérification post-rollback
1. `python -m compileall -q terminal.py vertex` → exit 0.
2. `python -m pytest tests/ -q` → vert.
3. `curl /healthz` → 200 ; `curl /api/system-status` → `readonly: true`.
4. Charger les 8 espaces en démo : aucun 404 d'asset, console propre.
