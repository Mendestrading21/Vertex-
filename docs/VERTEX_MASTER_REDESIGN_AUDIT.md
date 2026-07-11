# Vertex Master Redesign — Audit forensique et visuel

Date : 2026-07-11 · Baseline : 414 tests verts · Captures : `docs/redesign/before/`
(20 captures, 11 pages × 4 viewports clés, mode démo — aucune donnée privée).

## 1. Mécanique actuelle de génération des pages

- Anciennes grandes pages (`/`, `/watchlist`, `/options-desk`, `/strategie`,
  `/ma-page`, `/entreprises`) : chaînes brutes `PAGE_* = r"""…"""` avec leur
  propre `var NAV`/`var VSEC` réinjectés (`terminal.py:6291-6296`) + rail CSS
  `_RAIL_CSS`/`_rail()` (`terminal.py:3785-3875`).
- Pages récentes : helper `_vpage(title, body, head, js)` (`terminal.py:6520`)
  + nav canonique `vertex/ui/nav.py`.
- Design system partiel : `vertex/ui/design_system.py` (tokens `--vx-*`),
  `vertex/ui/vx_kit.py` (`window.VX`, actions), `vertex/ui/sync_center.py`.
- **Deux systèmes de navigation concurrents** (nav.py 10 items / rail legacy
  aux libellés différents) + une page autonome sans shell (`/strategy-os`).

## 2. Inventaire des pages et destinations (extrait décisionnel)

| Route(s) | Objectif réel | APIs consommées | Destination |
|---|---|---|---|
| `/`, `/daily` | Market Overview (cockpit marché, tops, secteurs, news, calendrier) | `/scan`, `/api/command`, `/quotes`, `/cal-feed`, `/news-feed`, `/api/market/summary` | **Briefing + Marchés** |
| `/stocks` | recherche titre | `/scan`, `/api/names` | **Analyse** |
| `/titre/<sym>`, `/company/<sym>` | fiche titre institutionnelle | `/api/ticker/<sym>`, `/api/correlations`, `/options/<sym>` | **Analyse (fiche canonique)** |
| `/compare`, `/entreprises` | comparateur / explorateur | `/scan`, `/quotes` | **Analyse** |
| `/strategie`, `/strategy` | Trading Desk (trades perso, simulateur, équité) | `/scan`, `/api/desk`, `/api/pos-quotes`, `/api/ibkr/positions` | **Portefeuille** |
| `/ma-page`, `/moi`, `/watchlist`, `/suivi` | watchlist perso / hebdo / recos suivies | `/scan`, `/quotes`, `/api/desk` | **Portefeuille / Watchlist** |
| `/options`, `/options-lab`, `/options-desk` | Options Research Center (12 chapitres) | `/api/options-lab`, `/api/options-for/<sym>` | **Opportunités / Options** |
| `/sectors`, `/heatmap` | rotation sectorielle, heatmap | `/scan` | **Marchés / Secteurs** |
| `/catalysts` | calendrier earnings + macro | `/cal-feed` | **Opportunités / Calendrier** |
| `/anomalies` | radar signaux qualité×intensité | `/scan` | **Opportunités / Anomalies** |
| `/journal` (+`/decisions` fusionné) | Trade Journal 2.0 (18 stats, coach, heatmap) | `/api/desk` | **Performance** |
| `/review`, `/brief` | comité / morning brief | `/api/committee-review`, `/api/brief` | **Intelligence / Briefing** |
| `/research`, `/equipe`, `/bordel` | research lab, playbook, hub | local + `/scan` | **Intelligence** |
| `/health`, `/settings` | santé système, préférences | `/api/system-status` | **Système** |
| `/vault`, `/archive` | coffre interne | `/api/desk` | **Système / Archive** |
| `/strategy-os`, `/vertex-intelligence` | hub Strategy OS | `/api/strategy/*` | **Intelligence** |

Routes cachées de la nav : `/suivi`, `/bordel`, `/heatmap`, `/strategy-os`,
`/review`, `/brief`, `/research`, `/health`, `/equipe`.

## 3. Schémas localStorage (contrat à PRÉSERVER à l'identique)

Clés synchronisées (`__DESK_KEYS` terminal.py:8996, dupliqué vx_kit.py:259,
sSyncPush/Pull:7790, vault.py:92) :
`myTrades, myTradesClosed, myTradesEquity, myRecos, myRecosClosed, myCapital,
simCash, simStart, simTrades, simClosed, myFavs, myNotes, vxJournal,
myTradeLog, vxVault, vxAlerts`.

- `myTrades` : `[{id, type:'STK'|'CALL'|'PUT', sym, exp, strike, right, qty,
  cost, added:'YYYY-MM-DD', entrySnap:{spot,stop,tgt,score,verdict,pb,thesis},
  note?}]`
- `myTradesClosed` : `[{sym,type,strike,exp,qty,cost,exit,added,closed,note}]`
- `myTradesEquity` : `[{d,v,i}]` (180 max)
- `myRecos` (suivis ⭐) : STK `{id,kind:'STK',sym,entry_spot,stop,tgt,followed}`
  · OPT `{id,kind:'OPT',sym,exp,strike,cost,tgt,be,q,pop,pot,spot,followed}`
- `myFavs` : `["NVDA",…]` · `myNotes` : `{"NVDA":"note"}`
- `vxJournal` : `[{id,ticker,tf,dir,reason,entry,stop,tp,risk,emo,conf,disc,
  trigger,result,exit,pnl,lesson,mistake,date,auto?,kind?,strike?,invested?,
  recovered?}]`
- `vxAlerts` : `[{id,sym,cond:'above'|'below'|'target',level,note,created,
  active}]` — évaluées serveur toutes les 60 s (`_alerts_loop`),
  déclenchements dans `/api/alerts/status`.
- `vxVault` : `[{id,title,type,content,tags,createdAt,updatedAt,source,
  status,priority,linkedPage}]`
- Sync : POST `/api/desk {ts, data:{clé:valeurStringifiée}}` ; pull compare
  `d.ts > deskTs` (last-writer-wins, blob complet, backups quotidiens).

## 4. APIs disponibles (matière première des nouvelles pages)

`/scan` (état géant à fractionner), `/api/market/summary`, `/api/cockpit`,
`/api/command`, `/api/brief`, `/api/committee-review`, `/api/ticker/<sym>`,
`/api/names`, `/api/correlations/<sym>`, `/options/<sym>`, `/quotes`,
`/cal-feed`, `/news-feed`, `/weekly-feed`, `/api/options-lab`,
`/api/options-for/<sym>`, `/api/decision/<sym>`, `/api/position-decision/<sym>`,
`/api/desk` (+backups/restore), `/api/pos-quotes`, `/api/ibkr/positions`,
`/api/watchlist-tv`, `/api/track-record`, `/api/alerts/status`,
`/api/strategy/profile`, `/api/strategy/decision/<sym>`, `/api/market/regime`,
`/api/anomalies/<sym>`, `/api/portfolio/team`, `/api/alerts/active`,
`/api/system/diagnostics`, `/api/data-quality`, `/api/live/status`,
`/api/system-status`, `/api/tradingview/signals`, `/api/vertex/<sym>`,
`/api/validator`, `/api/risk`, `/healthz`.

## 5. Duplications à éliminer

1. `vsideDesk` (sidebar JS) copié verbatim 5× (terminal.py:2386, 4027, 4374,
   4831, 5331) + shell CSS mobile copié 5×.
2. Logique desk-sync définie 4× (16 clés × 4 listes).
3. Helpers trades dupliqués (`vxFollowStk` ×3, `rGet` ×2, `getFavs` ×3).
4. Trois helpers de cartes KPI concurrents + tokens redéclarés par page.
5. Deux paradigmes graphiques (Chart.js sur `/` seulement, SVG/canvas custom
   ailleurs).
6. Deux implémentations de la densité (`wDensity`).

## 6. Défauts UX / design / responsive constatés (captures)

- Identité visuelle hétérogène : 3 générations de pages (rail legacy néon,
  `_vpage`, strategy-os autonome) — palettes, nav et composants différents.
- Aucune fiche unique : `/titre`, `/stocks`, `/entreprises`, `/compare` se
  recouvrent.
- Aucun retour contextuel : navigation par liens directs, filtres perdus.
- Provenance des données inégalement affichée (bien sur strategy-os, absente
  des vieilles pages).
- Mobile : le rail legacy déborde sur 390 px (menu hamburger maison par page).
- Emojis comme langage d'icônes principal sur les vieilles pages.

## 7. Décisions de refonte

- Un shell unique (`vertex/ui/shell/`) + design system CSS
  (`vertex/static/vertex/css/*`) + JS canonique (`vertex/static/vertex/js/*`).
- 8 espaces (§10) ; toutes les anciennes routes redirigent avec conservation
  ticker/vue/filtres (§11).
- Entités : Favoris=`myFavs` (inchangé), Suivis=`myRecos` (inchangé),
  Watchlist=NOUVELLE clé `vxWatchlist` (ajoutée aux 4 listes de sync),
  Positions=`myTrades` (inchangé), Alertes=`vxAlerts` (inchangé) — un seul
  module `vx-entities.js`, zéro réimplémentation par page.
- Graphiques : Chart.js (déjà embarqué) comme moteur unique + wrappers
  `charts/*` respectant le contrat §34 (question/conclusion/source/timestamp).
- Le monolithe conserve ses APIs ; ses pages HTML legacy sont remplacées par
  redirections (strangler pattern).
