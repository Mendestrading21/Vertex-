# Vertex — contrat des données et de leur provenance

> **Status: ACTIVE**
> Last verified: 2026-07-22
> Owner: Vertex data

## Priorité canonique (§16)

1. IBKR Live → 2. IBKR Delayed → 3. IBKR Frozen → 4. fournisseur secondaire
validé (différé ~15 min) → 5. fallback EOD → 6. indisponible (honnête).
Routeur : `vertex/data_sources/source_router.py` (fallback_used marqué,
jamais de mélange silencieux). Structure canonique : `ProvenancedValue`
{value, source, source_mode, timestamp, age_seconds, quality, fallback_used,
warnings}.

## Par domaine

| Domaine | Source primaire | Repli | Fraîcheur/quality | Consommateurs |
|---|---|---|---|---|
| Spot actions | IBKR (`/quotes`, adaptateur) | téléchargement différé / EOD / démo étiquetée | scan_age, badges live/delayed/fallback | market strip, fiche, positions |
| Historique quotidien | téléchargement différé (repli Stooq) | cache 6 min | `scan_ts`, source dans `/scan` | graphiques, indicateurs moteur |
| Chaînes d'options | IBKR (worker unique, entonnoir §18) | moteur legacy différé | `options_source` | board, sélecteur, simulateur |
| Greeks | IBKR modelGreeks (BROKER_GREEKS) | BS interne (MODEL_ESTIMATE/FALLBACK_ESTIMATE) | étiquette obligatoire | fiche options, anomalies |
| Positions réelles | IBKR `/api/ibkr/positions` (lecture seule) + desk déclaratif (`myTrades`) | marques `/api/pos-quotes` TTL 45 s | live flag | Portefeuille, risque |
| Fondamentaux | fournisseur secondaire (`tk.info`, cache) | profil entreprise curé | cache hebdo | fiche, scanner |
| Calendrier | `/cal-feed` (earnings + macro) | — | ts du feed | Briefing, Opportunités |
| Signaux TradingView | webhook signé (`TRADINGVIEW_SECRET`) | 503 si non configuré — rien d'inventé | anti-replay 15 min, dédup 10 min | fiche, Intelligence |
| Taux sans risque | courbe par échéance (`rates.py`) | plat 0.045 `fallback_used=True` | note dans la simulation | pricer |
| Régime de marché | moteur de régimes (≥3 dimensions sinon UNKNOWN) | UNKNOWN honnête | recalcul par requête | Briefing, Marchés |
| Données perso | localStorage 17 clés | `/api/desk` (blob, backups quotidiens) | `deskTs` LWW + beacon | toutes pages |

## Clés localStorage — registre canonique

**Synchronisées desk (17)** — `VXEntities.DESK_KEYS` = `__DESK_KEYS`
(terminal) = `vx_kit` = `journal` = `vault` (gardien
`test_all_sync_keys_are_canonical` + `test_desk_sync_keys_single_source_of_truth`) :
`myTrades, myTradesClosed, myTradesEquity, myRecos, myRecosClosed, myCapital,
simCash, simStart, simTrades, simClosed, myFavs, myNotes, vxJournal,
myTradeLog, vxVault, vxAlerts, vxWatchlist`.

**Locales par appareil (volontairement non synchronisées)** :
`vxSidebarState` (état sidebar), `vxNavigationContext` (sessionStorage —
contexte de retour), `vxRecentTickers`, `vxDashboardLayout` (densité +
blocs masqués), `vxNotificationPrefs`, `vxSavedFilters` (réservé),
`deskTs` (horloge de sync), `td_scan`/`td_scan_ts` (cache scan legacy).

**Mémoire stratégique (serveur, §33)** : `vxStrategyProfile, vxStrategyRules,
vxStrategyTheses, vxStrategyFeedback, vxStrategyLearnings, vxStrategyPending,
vxStrategyVersions` — store `vertex/strategy/memory/` (statuts OBSERVED→
CONFIRMED, jamais actifs sans confirmation humaine).

## Protocole de synchronisation

POST `/api/desk {ts, data}` — last-writer-wins par blob, pull toutes les
120 s (comparaison `d.ts > deskTs` : jamais écraser du plus récent), push
débouncé 1.2 s + **flush sendBeacon au pagehide**, backups quotidiens
`desk_backup_*.json` (7 rotations) + `/api/desk/restore`.

## Réconciliation (§17)

`vertex/data_sources/reconciliation.py` : écarts de prix (0.5 % alerte,
2 % bloquant), ratio compatible split → `SPLIT_MISMATCH` bloquant, devise,
multiplicateur, mapping de contrat, bid>ask, spot/chaîne de séances
différentes (>6 h), earnings divergents. **Bloquant ⇒ ACTIONABLE interdit,
décision maximale ATTENDRE**, raison exposée.
