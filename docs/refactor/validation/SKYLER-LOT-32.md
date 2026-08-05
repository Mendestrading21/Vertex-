# SKYLER V2 — LOT 32 : RC courte périodique (outillée)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-32-short-rc`
(base : `integration/vertex-skyler-v2` @ `e3a55e1`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) RC courte périodique, (b) surfaçage
by_catalyst_type dans la carte Mémoire, (c) fuzz des routes HTTP du
graphe, (d) drill-down cellule. Choix : **(a)**, premier par valeur.

- Cinq lots ont été fusionnés depuis le dernier audit navigateur complet
  (lot 27) — dont un changement de shell (bouton Exporter, SW v101) et un
  bump moteur (0.9.0). Les tests unitaires ne remplacent pas la preuve
  navigateur : c'est un invariant du projet.
- Le lot rend l'audit RÉPÉTABLE : le script est versionné
  (`tools/rc_short_audit.js`), la RC courte devient un outil du backlog
  périodique au lieu d'un effort ad hoc à chaque fois.
- (b) exigerait un bump SW + preuve navigateur — mieux après cette RC ;
  (c) et (d) restent au backlog.

## 2. Livré

**`tools/rc_short_audit.js`** (nouveau, versionné) — audit léger
Playwright des 8 espaces canoniques :

- 0 erreur console au repos par page (bruit d'environnement documenté au
  lot 27 exclu : requêtes in-flight d'une navigation abandonnée,
  `fonts.googleapis.com` injoignable en sandbox) ;
- 0 `pageerror` (exception JS non rattrapée) ;
- HTTP 200 par page ; `/healthz` 200 ; `/api/client-log` à 0 ;
- service worker courant servi (`td-shell-vNNN` affiché en preuve) ;
- code retour 0 (GO) / 1 (défauts listés) → intégrable en périodique.

Usage : serveur démo lancé, puis
`NODE_PATH=/opt/node22/lib/node_modules node tools/rc_short_audit.js`.
`waitUntil: domcontentloaded` (jamais `networkidle` — le poll live ne
s'arrête pas), viewport 1440×900.

## 3. Résultats de l'audit (serveur DEMO=1 NO_IBKR=1)

```text
/               HTTP 200  console_err=0  pageerror=0
/markets        HTTP 200  console_err=0  pageerror=0
/opportunities  HTTP 200  console_err=0  pageerror=0
/analysis       HTTP 200  console_err=0  pageerror=0
/portfolio      HTTP 200  console_err=0  pageerror=0
/options        HTTP 200  console_err=0  pageerror=0
/journal        HTTP 200  console_err=0  pageerror=0
/system         HTTP 200  console_err=0  pageerror=0
/healthz        HTTP 200  {"build":"VERTEX-1.0","data_source":"demo",…}
/api/client-log n=0
sw.js           td-shell-v101

RC COURTE : GO — 0 défaut.
```

Vérification live complémentaire du chemin neuf (lot 29) :

```text
GET /api/skyler/memory/export
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="skyler_export_20260805.json"
```

**Verdict : GO — 0 défaut produit constaté.** Le `data_source":"demo"`
de `/healthz` est honnête (serveur lancé en DEMO pour l'audit sandbox) ;
la validation sur appareil physique avec TWS réel reste l'étape humaine
(réserve n°1 de la RC du lot 27, inchangée).

## 4. Preuves complémentaires

```text
python -m compileall -q terminal.py vertex   → exit 0
python -m pytest tests/ -q
→ 1543 passed, 2 skipped                     (baseline inchangée — audit,
                                              aucun comportement modifié)
```

Aucun changement de shell → SW v101 inchangé ; aucun test nouveau requis
(aucun comportement ne change — le livrable est l'outil d'audit + la
preuve navigateur).

## 5. Invariants tenus

- READONLY absolu (audit en lecture seule, serveur démo) ;
- données réelles uniquement (démo étiquetée par le serveur lui-même) ;
- fichiers runtime jamais commités ; `main` intacte ;
- `domcontentloaded` (jamais `networkidle`) ; pkill exit 144 bénin géré.

## 6. Backlog restant (candidats lot 33)

1. Surfaçage by_catalyst_type dans la carte Mémoire (badges contexte,
   bump SW v102 + 4 gardiens + preuve navigateur) ;
2. Fuzz des routes HTTP du graphe (`/api/skyler/graph/<sym>?hops=`,
   `/api/skyler/memory/<decision_id>` avec ids dégénérés) ;
3. Drill-down cellule de calibration (quand des cellules mesurées
   existeront) ;
4. RC courte re-jouable après chaque lot UI via `tools/rc_short_audit.js`.

**Arrêt après ce lot — validation humaine requise.**
