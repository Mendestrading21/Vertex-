# SKYLER V2 — LOT 08b — NEON GLASS · AUJOURD'HUI (diff marché serveur)

> Date : 2026-08-05
> Branche : `agent/skyler-v2-lot-08b-today-diff`
> Base : `integration/vertex-skyler-v2` (chaîne 0–8a fusionnée et validée)
> Périmètre : UNE page (Aujourd'hui) + durcissement du moteur MarketContext sur bug réel attrapé en runtime

## 1. Constat

Le MarketContext (lot 3) et son « ce qui a changé depuis la dernière session »
n'étaient visibles nulle part. En le branchant, la validation navigateur a
**attrapé un bug réel** : `/api/market/context` → 500 (`TypeError: dict - dict`)
car l'état RÉEL du scan porte `market['breadth']` en **dict**
(`{'above200': 45, ...}`) et `roro` en **chaîne** (`'RISK-OFF'`) — pas les
nombres attendus. De plus, le régime réel vit dans `market_ctx.spy_regime`
(pas `market.regime`) → régime UNKNOWN à tort (2 dimensions au lieu de 4).

## 2. Décision

- **UI (Aujourd'hui)** : bloc « Marché (serveur) » ajouté DANS la carte existante
  « Depuis ta dernière visite » (son domicile canonique — pas de doublon avec
  Marchés) : transition de régime (badge X → Y), liste `changes_since_prev`,
  conflits de sources en avertissement, états honnêtes (« Première session
  enregistrée — pas de comparaison » / « Aucun changement »), fraîcheur du scan.
- **Moteur durci** (`market_context.py`) : coercition numérique `_num` partout
  (jamais de TypeError sur l'état réel) ; breadth dict → `above200` (la dimension
  EST la part au-dessus de la MM200) ; roro numérique → ratio, chaîne → catégorie
  étiquetée ; tendance depuis `market.regime` OU `market_ctx.spy_regime` ;
  leadership depuis `market.risk` OU la catégorie roro. Résultat : le régime se
  classifie désormais en démo (TREND_UP, 4 dimensions, confiance 0.5) au lieu
  d'un UNKNOWN artificiel.

## 3. Fichiers

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/ui/pages/briefing.py` | bloc `vx-mkt-diff` + `loadMarketDiff()` (additif) | faible |
| `vertex/engines/market_context.py` | durcissement formes réelles (comportement numérique inchangé) | faible |
| `vertex/app/routes/system.py` | SW v88 → **v89** | faible |
| 4 gardiens SW + `tests/test_market_context.py` | v89 + 3 tests de régression (formes réelles, mapping spy_regime/roro, gardien de page) | faible |

## 4. Tests

```text
rouge : test_real_state_shapes_dict_breadth_and_string_roro → 1 failed (bug reproduit)
vert  : tests/test_market_context.py → 14 passed
suite : 1269 passed, 2 skipped · compileall exit 0
```

## 5. Validation navigateur (DEMO=1 NO_IBKR=1, Chromium réel)

- Avant correction : 500 sur `/api/market/context`, carte « injoignable » — bug
  attrapé par cette validation, corrigé test-rouge-d'abord.
- Après : 1440×900 et 390×844 → bloc rendu (« Aucun changement de marché depuis
  la dernière session » + fraîcheur du scan), **0 erreur console, 0 débordement** ;
- `/api/market/context` → régime **TREND_UP** (dims : trend, breadth 45, vix 12.7,
  leadership DEFENSIVE), roro exposé en catégorie ; `/api/client-log` = 0 ;
  `sw.js` sert v89.

## 6. Invariants vérifiés

- [x] une donnée = un seul domicile (bloc dans la carte diff existante, détail sur /markets) ;
- [x] jamais inventé : première session et zéro-changement dits explicitement ;
- [x] bug corrigé test rouge d'abord ; coercition = extraction honnête, pas d'approximation ;
- [x] bump SW + gardiens ; READONLY ; aucun moteur financier modifié.

## 7. Risques restants

1. Le contexte précédent persiste par republication de scan — sur un serveur
   redémarré souvent (dev), le diff reste souvent vide : normal, dit à l'écran.
2. Effet positif collatéral : le bloc `market_regime_sector` du score Skyler
   se remplit désormais en démo (régime classifié) — le total /40 montera.

## 8. Verdict

**GO** — bug réel attrapé et corrigé (rouge→vert), carte prouvée 2 tailles
0 erreur, suite 1269 verte.

## 9. Prochaine étape

Lot 8c : espace Options — vue scanners TACTICAL/SWING/LEAPS (mandat + doublement).

**Arrêt de lot — validation humaine groupée en fin de série (accord utilisateur).**
