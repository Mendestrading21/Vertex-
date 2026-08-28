# Lot 35 — Flux manuels de bout en bout : la position déclarée redevient gérable

## Problème

Vérification E2E des flux du portefeuille manuel (serveur démo, navigateur
réel) : la déclaration d'une position fonctionnait, mais **le cycle de vie
s'arrêtait là**. Trois défauts mesurés :

1. **Le menu POSITION était inaccessible.** `E.openPositionMenu` (Modifier /
   Clôturer / Supprimer, par id) existe dans vx-entities.js depuis le lot 3,
   déclenché par `[data-position-menu="<id>"]` — mais **aucune ligne d'aucune
   surface ne portait cet attribut**. Les trois surfaces (cartes d'équipe,
   tableau Actions/Options, tableau options dédié) posaient
   `data-entity-menu="${t.sym}"` : le menu du TITRE (favoris, watchlist,
   alerte…), sans aucune action de position. Une saisie erronée était
   indélébile depuis l'interface.
2. **Le bouton « Clôturer » du tableau était mort.** `data-close-pos="${t.id}"`
   n'avait aucun handler dans tout le dépôt — clic sans effet, mesuré au
   navigateur.
3. **« Déclarer une position » redemandait la destination.**
   `openAddModal('', 'position')` : le handler « Continuer » forçait
   `step = 2` (choix de destination) même quand la destination était déjà
   préréglée par le bouton cliqué.

Découverte connexe : le lot 32 avait **vidé par accident**
`tests/test_sw_cache_scope_lot361.py` (blob vide, jamais mentionné dans le
message de commit) — le gardien du contrat assets ↔ version de shell était
neutralisé en silence depuis 3 lots.

## Correctifs (minimaux)

- `vertex/ui/pages/portfolio_page.py` (3 sites : cartes d'équipe ligne 499,
  tableau positions ligne 651, tableau options ligne 814) : le bouton ⋯ passe
  de `data-entity-menu="${t.sym}"` à `data-position-menu="${t.id}"`, avec
  aria-label « Actions position SYM ». Le menu position surface aussi les
  actions utiles du titre (analyse, note, journal) — rien n'est perdu.
- `vertex/static/vertex/js/vx-entities.js` :
  - délégation globale : `[data-close-pos]` → `E.openClosePosition(id)` ;
  - handler « Continuer » : `step = dest ? 3 : 2` — la destination préréglée
    saute le choix ;
  - comparaisons d'id canoniques (`String(x.id) === String(id)`) — le desk
    JSON et les datasets DOM ne divergent plus jamais sur le type.
- `tests/test_sw_cache_scope_lot361.py` : restauré depuis le lot 31 (121
  lignes), contrat remis au courant (`_SW_VERSION = 276`, empreinte mesurée
  `ebd6d9a5…`).
- SW `td-shell-v276` + 4 épingles de version.

## Preuves (navigateur, DEMO=1, 127.0.0.1:5002)

- **Suppression** : déclaration test ACN 5 @ 190 → menu ⋯ de la ligne →
  « Supprimer la position » → confirmation → `/api/positions/state` revenu à
  `['NVDA']`. Menu mesuré : Modifier / Clôturer (→ journal) / Supprimer /
  Ouvrir l'analyse / note / journal / copier.
- **Clôturer** : clic sur le bouton de ligne → modal « Clôturer la position —
  NVDA · investi 5 000 » (avant : aucun effet).
- **Préréglage** : « Déclarer une position » → saisie ticker → Continuer →
  formulaire détails direct (`#f-qty` présent, aucun bouton de destination).
- **Suivi** : `followStock('NVDA', …)` → visible sur /follow-up.
- 1600/1024/390 px : débordement horizontal 0, console vide,
  `/api/client-log` = 0 erreur.
- Desk restauré à l'identique depuis la sauvegarde prise avant les tests
  (position NVDA d'origine seule ; ni ACN ni suivi de test ne subsistent).

## Tests

- `tests/test_position_row_actions_lot35.py` — 3 bancs nés rouges (menu
  position sur les lignes, handler Clôturer, préréglage honoré).
- `tests/test_sw_cache_scope_lot361.py` — 5 bancs restaurés (sémantique SW +
  contrat d'empreinte).
- Suite complète : **4430 passés · 152 ignorés · 0 échec**.

## Rollback

Revert du commit unique. Aucune migration de données : le desk n'est pas
touché par le code (seules les écritures E2E l'ont été, et il est restauré).
