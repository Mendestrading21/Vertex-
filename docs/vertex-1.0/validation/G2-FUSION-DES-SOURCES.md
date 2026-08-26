# Fusionner les deux piles IBKR et les replis — une seule table de priorité

Module : `vertex/data_sources/cotation_unifiee.py`
Gardien : `tests/test_vertex_1_0_repli_cotations.py` (19 tests)

---

## Ce qui était éclaté

Le produit portait **deux piles IBKR**, plus des replis ad hoc :

| pile | ce qu'elle fait | provenance |
| --- | --- | --- |
| workers de `terminal.py` | tout le travail réel (options, cotations, indices, compte) | **aucune** |
| `vertex/data_sources/ibkr_*` | passerelle, snapshots, historique | complète (`ProvenancedValue`) |

Et à côté, **`source_router.py`** — qui implémente *exactement* la fusion
demandée : IBKR live → différé → figé → secondaire → EOD → absence honnête,
avec disjoncteur et mesure de latence — avec **zéro appelant**.

Troisième module de cette campagne dans ce cas, après `fallback_market_data.py`
(zéro appelant) et le repli de cotation que je venais d'écrire à la main. **La
fusion était écrite ; elle n'était pas branchée.**

## Pourquoi un `if` ne suffisait pas

Mon propre correctif de la veille faisait `si broker, sinon scan`. Ça marche, et
ça n'apporte rien de ce qui compte :

- **l'ordre écrit une seule fois.** Trois `if` dans trois fichiers, c'est trois
  priorités qui divergeront — déjà arrivé **deux fois** dans ce produit (les
  cinq ordres de ports, les trois escalades de type de données) ;
- **l'étiquette de provenance.** `SOURCE_IBKR/MODE_LIVE` n'est pas
  `SOURCE_SECONDARY/MODE_DELAYED`, et l'écran doit pouvoir le dire ;
- **`fallback_used`**, posé par le routeur dès qu'on quitte la source de tête,
  sans que l'appelant y pense ;
- **le disjoncteur** : une source qui échoue deux fois est mise au repos 30 s au
  lieu d'être retentée à chaque requête.

## Mesuré, bout en bout

```json
{"fallback_used": true, "results": {"ACN|||": {
  "spot": 198.0, "spot_chg": -0.53, "type": "STK",
  "source": "SECONDARY", "mode": "DELAYED", "fallback_used": true}}}
```

- cotation broker présente → `IBKR` / `LIVE`, `fallback_used: false` ;
- broker muet → `SECONDARY` / `DELAYED`, `fallback_used: true` ;
- aucune source → **rien**. Pas de zéro plausible : un `—` honnête.

Le vocabulaire vient de `models.py`, pas d'une chaîne inventée au point
d'appel — c'est ce qui permet à l'écran de traduire une provenance sans la
deviner.

## Vérifié au passage : le budget de lignes IBKR

Le guide rappelle la limite dure de **100 lignes de données simultanées** et le
pacing associé. Mesuré sur le code plutôt que supposé :

| flux | lignes | nature |
| --- | --- | --- |
| worker options (unique, lots exclusifs) | **40** | flux, relâchées (`cancelMktData`) |
| worker cotations (`reqTickersAsync`, lots de 20) | **20** | transitoires |
| worker indices | **3** | flux permanents |
| **pire cas simultané** | **63** | sous la limite de 100 |

`LIVE_SYMBOLS` compte **517 symboles**, ce qui alarme au premier regard — mais
ils sont demandés par lots de 20, lignes relâchées entre les lots. L'auteur
d'origine le savait, le commentaire le dit, et la mesure le confirme. **Aucun
dépassement.**

## Une nuance du guide qui touche mon correctif d'hier

Le guide indique qu'IBKR **ne fournit plus de cotations différées sur les
actions US** (contrainte réglementaire), et qu'à la place le compte dispose
gratuitement de **Cboe One / IEX en temps réel non consolidé**.

Conséquence : l'échelle `1 → 2 → 3 → 4` que j'ai posée hier reste correcte de
forme (elle descend, puis remonte), mais pour une action US le type 3
n'apportera rien. Ce qui fait fonctionner le type 1 sans abonnement payant,
c'est **l'entitlement gratuit à activer dans le Client Portal** — une action de
configuration, pas de code.

Je n'ai pas pu vérifier cette affirmation ici (aucun accès IBKR) : elle est
consignée comme **information à confirmer**, pas comme fait mesuré.

## Vérification

- Suite complète : **3 551 passed** · `compileall` → 0
- Bout en bout sur serveur réel : priorité, étiquettes et absence honnête
  conformes.
