# Rapport — Lot 9 · Convergence du runtime (tranche : zéro collision, routeur branché)

## 1. La dernière collision de route — résolue par retrait

`GET /api/anomalies/<sym>` avait deux propriétaires aux **formes de réponse
différentes**. Mesuré : `analysis_api.api_anomalies` gagnait au dispatch
(série canonique, consommé par la vraie page Analyse) ; la version de
`strategy_os_api` était **masquée depuis toujours**, et son seul consommateur
— la page legacy `/strategy-os` — est une **redirection 301**. Du code mort
des deux côtés. La règle masquée est retirée ; le propriétaire unique est le
canonique.

**Gardien générique** (`test_collisions_routes_lot09`) : énumère la carte
réelle des routes et échoue sur TOUTE règle (chemin + méthode) à deux
endpoints. L'ordre d'enregistrement n'est plus une protection, c'est un
détail. Les deux bancs qui épinglaient la coexistence sont mis à jour vers
l'état cible, leur intention documentée.

## 2. Le routeur persistant — deux moitiés jamais branchées

`vx-router.js` (264 lignes, progressive-enhancement, repli navigation dure
sur toute erreur) était documenté et testé ; le côté **serveur**
(`X-Vertex-Fragment`, `_render_fragment`) existait dans la coque. Il ne
manquait que le `<script>`. Branché.

**Preuve navigateur** : un témoin posé sur `window` **survit** au clic vers
`/markets` (le shell n'est pas reconstruit), le H1 et l'URL changent, le
retour arrière fonctionne, zéro erreur console. Sans JS, rien ne change :
les URL servent toujours le document complet.

## 3. La porte du programme

```
audit_runtime.py --enforce-target  →  code 0
```

Douze pages en 200 · zéro collision · routeur chargé. Cette porte devient
exigible en CI à partir du cutover.

## Dette restante du lot 9 (strangler complet)

`terminal.py` reste le monolithe legacy (~7 000 lignes) : trois doubles
écrivains de stores (`myRecos`/`myFavs`/`myNotes`), la carte V3, la file
worker. Réduction par étranglement — un propriétaire par PR — hors de cette
tranche.

## Preuves

Gardien rouge d'abord · suite **4316 passés · 0 échec** · SW v264.
