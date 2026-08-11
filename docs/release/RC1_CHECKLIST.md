# Vertex — RC1 Checklist

> À compléter/relire avant toute fusion. **RC1 interne** : aucun merge `main`, aucun
> tag, aucune release publique tant que la validation humaine n'est pas donnée.

## Identité
- **Branche** : `agent/vertex-total-rebuild`
- **Base intouchée** : `origin/main` = `2b4fa70`
- **SHA RC1** : voir `git rev-parse HEAD` (tip de la stabilisation ; commits clés
  `6cfcb18` code mort, `f201528` cohérence/éditorial, + commits docs RC1)
- **Service worker** : `td-shell-v51`

## Critères GO / NO-GO
| Critère | État | Preuve |
|---|---|---|
| compileall vert | ✅ | `python -m compileall -q terminal.py vertex` → exit 0 |
| pytest complet vert | ✅ | **954 passed, 2 skipped** (956 collectés) |
| 0 endpoint d'ordre | ✅ | grep `def/place/submit/transmit/... order` → 0 def, 0 call ; seulement blocklist/labels/tests |
| READONLY prouvé | ✅ | `readonly=True` codé en dur partout ; `config.READONLY=True` ; ~20 tests gardiens |
| 0 erreur console applicative | ✅ | sweep navigateur (hors 404 transitoires corrigés) |
| 0 débordement critique | ✅ | 0 px sur **75** combinaisons (15 vues × 5 viewports) |
| 0 faille critique connue | ✅ | pas de secret committé ; XSS échappé ; voir RC1-STABILIZATION §I |
| 0 donnée inventée | ✅ | états `n/d`/DEMO/OFFLINE honnêtes ; Hero calculés sur faits |
| mode démo honnête | ✅ | badges DÉMO ; `DEMO=1` sert des données synthétiques étiquetées |
| mode sans IBKR fonctionnel | ✅ | `NO_IBKR=1` ; marques `n/d`, Greeks « Insufficient » |
| stale / missing / insufficient corrects | ✅ | gardiens + états premium |
| service worker cohérent | ✅ | v51 ; install/activate/claim ; gardiens vN présent, v(N-1) absent |
| documentation release complète | ✅ | 5 fichiers (voir §Docs) |
| rollback documenté | ✅ | `RC1_ROLLBACK.md` |

**Verdict : GO (RC1 interne).**

## Tests
- `python -m compileall -q terminal.py vertex`
- `python -m pytest tests/ -q` → 954 passed, 2 skipped
- Routes/API 200, READONLY (×~20), démo, sans-IBKR, stale/missing/insufficient,
  options, portefeuille, journal, système, service worker.

## Responsive (mesuré)
390 · 768 · 1024 · 1440 · 1920 → **0 débordement réel** sur les 15 vues principales.
Tableaux larges = scroll intentionnel (desktop) / cartes (mobile).

## Accessibilité
Landmarks + aria-label, H1 unique/espace, résumés accessibles des graphiques (Chart
Shell), P&L/verdicts sans couleur (libellés). Limites (audit clavier complet,
reduced-motion exhaustif, contrastes AA mesurés) → `RC1_KNOWN_ISSUES.md`.

## Sécurité / READONLY
- IBKR `readonly=True` (codé en dur) ; `order_execution: disabled-by-design`.
- 0 endpoint/fonction/bouton d'ordre (preuve grep) ; `/api/planning/ticket` non transmis.
- Secrets gitignorés ; XSS échappé (`esc`, `sanitize_news`).

## Captures
`scratchpad/pr3shots … pr7shots/` (par PR) + sweeps RC1. Espaces couverts : les 8.

## Docs release
- `docs/refactor/validation/RC1-STABILIZATION.md`
- `docs/release/RC1_CHECKLIST.md` (ce fichier)
- `docs/release/RC1_KNOWN_ISSUES.md`
- `docs/release/RC1_CHANGELOG.md`
- `docs/release/RC1_ROLLBACK.md`

## Validation humaine
- [ ] Relecture des 8 espaces en démo par l'utilisateur.
- [ ] Contrôle sur appareil physique (hors headless sandbox).
- [ ] Accord explicite avant toute action sur `main`.

## Procédure de merge (FUTUR — sur accord explicite uniquement)
1. `git checkout main && git pull`
2. `git merge --no-ff agent/vertex-total-rebuild` (message de merge = résumé RC1)
3. `python -m pytest tests/ -q` sur `main` → vert
4. bump SW final si shell modifié ; tag `rc1` (optionnel, interne)
5. push `main` **uniquement après validation humaine**.

## Procédure de rollback
Voir `docs/release/RC1_ROLLBACK.md` (main intouché = rollback trivial ; `revert`
préféré ; données desk indépendantes du code).
