# Lot 22 — Nettoyage prouvé : MANIFESTE (RIEN N'EST SUPPRIMÉ SANS AUTORISATION)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

Conformément à la directive de consolidation : **aucune suppression
automatique**. Ce manifeste présente la liste exacte, les preuves et le
rollback de chaque candidat. L'exécution attend une autorisation humaine
explicite, élément par élément.

## A. Fichiers du dépôt — suppression proposée

### A1. `vertex/static/vertex/css/neon-glass.css` (ticket VX2-CLEANUP-01)
- **Preuve de mort** : demandée par AUCUNE page (vérifié au navigateur,
  trace SW v232) ; seules références restantes = commentaires (SW,
  vertex-2-0.css) qui documentent précisément qu'elle n'est PAS servie ;
  ses règles utiles ont été rapatriées (v256 « disposition rapatriée
  depuis la feuille non servie »).
- **Risque** : nul mesuré ; ses règles `.vx-verdict-card` ont déjà induit
  en erreur pendant la refonte (raison POSITIVE de la retirer).
- **Rollback** : `git revert` du commit de suppression.

## B. Renommages proposés (aucune suppression)

### B1. `chart-theme-obsidian-copper.js` (ticket VX2-CLEANUP-02)
- **CONSOMMÉ** par `vertex/ui/shell/__init__.py` et
  `vertex/visualization/palette.py` — ne PAS supprimer.
- Proposition : renommer vers `chart-theme-black-glass.js` (le nom décrit
  une palette abandonnée) + mise à jour des 2 consommateurs + bump SW.
  Peut attendre : dette cosmétique.

## C. Politique des captures PNG (ticket VX2-CLEANUP-03)
- **Mesuré aujourd'hui** : 485 PNG suivis, **155 Mo** (dont les captures
  de preuve des lots 0/14/15/16/17-20 ajoutées par ce programme).
- Options (décision humaine) : 1) statu quo (preuves dans l'historique) ;
  2) Git LFS pour `docs/**/*.png` ; 3) purge des captures des programmes
  HISTORIQUES (pré-2.0) en gardant celles du programme actif.

## D. Distant GitHub (tranches du GITHUB-CLEANUP-MANIFEST, lot 0)
- 748 refs distantes inventoriées ; tranches A/B/C déjà documentées dans
  `docs/vertex-2-0/lot-00/`. **Toujours en attente d'autorisation
  explicite.** Aucune branche supprimée, aucun force-push, aucune
  réécriture d'historique.

## E. Explicitement NON supprimable (preuve de vie)
- `vertex/ui/nav.py` : consommé par terminal.py (mode rollback V3).
- `terminal.py` : adaptateur historique, réduction par strangler
  (dette consignée), jamais une suppression sèche.
- Skills historiques `.claude/skills/vertex-1-0`, `vertex-redesign-*` :
  preuves historiques au sens de la doctrine, décision humaine.
