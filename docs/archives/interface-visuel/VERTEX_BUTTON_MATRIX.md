# Vertex — Matrice des boutons (nouvelle UI)

Conventions : `E()` = `window.VXEntities` · toast = `VX.toast` ·
modal/drawer = `VX.shell` · lectures via `VX.fetch` (retry ×2 + cache TTL).
« Succès » = rendu/toast ; « Erreur » = comportement observé en cas d'échec.
Gardien automatique : `test_every_button_has_handler` (chaque bouton du HTML
généré doit être câblé — inline, id référencé ou délégation `data-*`).

## Shell (toutes pages) — `vertex/ui/shell/__init__.py` + `vx-shell.js` / `vx-entities.js`

| Libellé | Déclencheur | Fonction | API | Succès | Erreur |
|---|---|---|---|---|---|
| Réduire | `#vx-collapse-btn` | toggle sidebar + localStorage | — | état persistant | — |
| Nav mobile | `#vx-mobile-nav-btn` | drawer navigation | — | overlay | — |
| Plus (mobile) | `#vx-mobile-more` | `shell.openDrawer` liens | — | drawer | — |
| Retour | `#vx-back-btn` | `location.href` depuis `VX.context` | — | navigation + filtres restaurés | caché sans contexte |
| Connexions | `#vx-connections-btn` | drawer état IBKR/TV/Claude | `/api/system/diagnostics`, `/api/live/status` | drawer KV | drawer partiel (dégrade) |
| Notifications | `#vx-notifs-btn` | alertes → drawer | `/api/alerts/active` | drawer + badge lu | dégrade |
| Actualiser | `#vx-refresh-btn` | `VX.refresh.runAll` | toutes tâches page | toast « Données actualisées » | `dataset.state='error'` |
| Ajouter | `#vx-add-btn` | `E().openAddModal()` | localStorage | modal 3 étapes | ticker invalide → toast error |
| Recherche / ⌘K | `#vx-global-search` | palette de commandes | `/api/names` (TTL 600 s) | palette | repli ticker brut |
| Items palette | click / Enter | openAnalysis / nav / openAddModal | — | navigation | — |
| Fermer | `[data-close-drawer/modal]`, overlay, Échap | `closeDrawer/closeModal/closeAll` | — | ferme | — |
| Menu ⋯ (délégué global) | `[data-entity-menu]` | `E.openMenu` (12 actions) | — | menu contextuel clavier | — |
| Ouvrir analyse (délégué) | `[data-open-analysis]` | `VX.openAnalysis` | — | navigation | — |
| Modal Ajouter : Continuer / destination / Confirmer | `#vx-add-next` / `[data-dest]` / `#vx-add-confirm` | `confirmAdd` → E.* (favori/watchlist/suivi/position/alerte/note) | POST `/api/desk` (débounce) | toast + événement bus | champ manquant → toast error |

## Briefing (`/`) — APIs : `/api/market/summary`, `/scan`, `/api/briefing/editorial`, `/api/market/regime`, `/api/command`, `/api/alerts/status`, `/api/pos-quotes`, `/cal-feed`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Personnaliser | `#vx-customize-btn` | modal disposition | modal | — |
| Enregistrer / Réinitialiser | `#vx-layout-save/reset` | localStorage `vxDashboardLayout` | toast | — |
| Compact/Confort/Dense | `[data-density-btn]` | densité persistée | aria-pressed | — |
| Tout voir → / Radar → / Ouvrir → | liens | navigation | — | — |
| Ticker / ⋯ (top actions, opportunités, alertes, portefeuille) | `[data-open-analysis]` / `[data-entity-menu]` | openAnalysis / openMenu | rendu cartes | état vide honnête |
| Créer une alerte / Déclarer une position | onclick (états vides) | `openAddModal('','alert'/'position')` | modal | — |
| Voir les preuves → / Marchés → | liens | navigation | — | — |

## Marchés (`/markets`) — APIs : `/scan`, `/api/market/regime`, `/cal-feed`, `/api/market/summary`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Secteurs → / Ouvrir fiche analyse → | liens | navigation | — | — |
| Leader ticker / ⋯ | `[data-open-analysis]` / `[data-entity-menu]` (esc appliqué) | openAnalysis/openMenu | rendu | lien Système/Données si scan absent |
| Secteur (table) | `<a onclick="VX.context.save()">` | nav `/opportunities?sector=` | filtre pré-appliqué | — |

## Opportunités (`/opportunities`) — APIs : `/scan`, `/api/options/simulate`, `/api/data-quality`, `/cal-feed`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| + Ajouter | onclick | `openAddModal()` | modal | — |
| Analyse / ⋯ / Actions ▾ | `[data-open-analysis]` / `[data-entity-menu]` | openAnalysis/openMenu | cartes | états vides + lien Système |
| Effacer les filtres | `#op-clear` | reset état + `paint()` | re-rendu | — |
| Chips décision / setup / agressivité | `[data-filter-key]` / `[data-ag]` | filtre + `paint()` | aria-pressed | — |
| Filtres secteur/setup/symbole | select/input | état + re-rendu | — | — |
| Simulateur contrat | ligne `[data-ct]` | fetch simulate → drawer scénarios | grilles spot×temps×IV | 400/422 → message API affiché |
| Chercher un titre (état vide) | onclick | palette globale | — | — |

## Portefeuille (`/portfolio`) — APIs : `/api/pos-quotes`, `/scan`, `/api/ibkr/positions`, `/api/portfolio/team`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| + Position / + Watchlist / + Ajouter | onclick | `openAddModal('','position'/'watchlist')` | modal | — |
| Ticker / Analyse / ⋯ | `[data-open-analysis]` / `[data-entity-menu]` | openAnalysis/openMenu | rendu + marques live (`/api/pos-quotes`, contrat composite corrigé) | « marques indisponibles » honnête |
| Clôturer | `[data-close-pos]` → `#pf-close-confirm` | `E().closePosition` (entrée journal auto) | toast + journal | — |
| Retirer (watchlist) | `[data-wl-del]` | `E().removeFromWatchlist` | toast + re-rendu | — |
| Retirer (suivi) | `[data-unfollow]` | `E().unfollow` | toast | — |
| Statut watchlist | `[data-wl-status]` change | met à jour statut | — | — |
| Risque équipe | rendu vue | POST `/api/portfolio/team` | risque/stress réels | état vide honnête |

## Analyse (`/analysis[/SYM]`) — APIs : `/api/names`, `/api/ticker/<sym>`, `/api/strategy/decision`, `/api/anomalies`, `/api/tradingview/signals`, `/api/options-for`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Recherche (index) | `#an-search` input | autocomplete `/api/names` | liste | dégrade |
| Titres récents | `[data-open-analysis]` | openAnalysis | navigation | — |
| ★ Favori | `#an-fav` | `E().toggleFavorite` + badges | toast | — |
| Actions ▾ | `[data-entity-menu]` | openMenu | menu | — |
| Éditer / Écrire la thèse | onclick | `openAddModal(SYM,'note')` | modal | — |
| Chips timeframe | `[data-tf]` | recharge dossier | re-chart | bandeau + lien Système |
| Double-clic graphe | `dblclick` canvas | `VXCharts.alertFromLevel` | modal alerte pré-remplie | — |
| Créer un suivi / Alerte sur l'entrée | onclick | openAddModal / alertFromLevel | modal | — |
| Ouvrir dans TradingView ↗ | lien `target=_blank rel=noopener` | externe | — | — |
| Analyser → / Desk options | liens | nav `/opportunities?view=options` | — | — |
| Barre mobile (Favori/Suivre/Alerte/Options/Plus) | onclick | E.* / nav | toast/modal | — |

## Performance (`/performance`) — API : `/api/track-record`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Ajouter une entrée | `#vx-pf-add(-empty)` | `openEntryModal` → `#j-confirm` → `E().addJournalEntry` | toast | — |
| Ticker / ⋯ (journal) | `[data-open-analysis]` / `[data-entity-menu]` (esc) | openAnalysis/openMenu | rendu | — |
| Filtre journal | `#vx-pf-filter` input | `loadJournal` | re-rendu | — |
| Ouvrir le journal → / Règles proposées → | liens | navigation | — | lien Système si vide |

## Intelligence (`/intelligence`) — APIs : `/api/strategy/decision`, `/api/decision`, `/api/committee-review`, `/api/strategy/profile`, `/api/validator`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Analyser | `#vx-analyst-form` submit | double décision (exécutive + stack) | fiche rendue | état vide + lien scan |
| Ticker / Ouvrir l'analyse / Actions | `[data-open-analysis]` / `[data-entity-menu]` | openAnalysis/openMenu | nav/menu | — |
| Chips filtre comité | `[data-filter-key="decision"]` | filtre + render | table | lien Système si vide |
| Détail (comité) | `[data-committee-detail]` | expand ligne | détail | — |
| Nouvelle thèse / Modifier | `#vx-memory-add` / `[data-edit-note]` | `openAddModal(sym,'note')` | modal | — |

## Système (`/system`) — APIs : `/api/system-status`, `/api/live/status`, `/api/system/diagnostics`, `/healthz`, `/api/data-quality`, `/api/live/refresh`, `/api/desk`

| Libellé | Déclencheur | Fonction | Succès | Erreur |
|---|---|---|---|---|
| Actualiser (maintenant) | `#vx-data-refresh(-empty)` | `doRefresh` → POST `/api/live/refresh` + runAll | toast success | **toast error explicite** |
| Densité / Sidebar / Notifications | `[data-density-btn]` / `[data-sidebar-btn]` / `[data-notif-btn]` | préférences localStorage | toast + aria-pressed | — |
| Exporter (JSON) desk | `#vx-desk-export` | blob téléchargé | download | — |
| Importer | `#vx-desk-import-file` → `#vx-desk-import-confirm` | `importDesk` → POST `/api/desk` | toast + sync | — |
| Nouvelle entrée / Exporter vault | `#vx-vault-new` / `#vx-vault-export` | modal / blob | modal/download | — |
| Ouvrir / Modifier / Supprimer vault | `[data-vault-open/edit]` → `#vv-save/#vv-delete` | drawer/modal + `set('vxVault')` | toast | — |
| Chips type vault | `[data-filter-key="type"]` | filtre | re-rendu | — |
| Voir le radar / Détail par domaine → | liens | navigation | — | — |

## Boutons morts / anomalies — état final

- ~~Contrat `/api/pos-quotes` cassé~~ → **corrigé** (payload `{positions:…}`,
  ré-indexation des clés composites vers les ids ; P&L live vérifié).
- ~~Télémétrie orpheline~~ → **corrigé** (`vx-core.js` → `/api/client-log`).
- `?view=compare` d'Analyse : paramètre accepté mais non exploité —
  limitation déclarée n° 11 (comparateur → recherche Analyse).
- Aucun autre bouton mort : tout est câblé par délégation
  (`[data-entity-menu]`/`[data-open-analysis]`) ou handler explicite —
  vérifié par `test_every_button_has_handler`.
