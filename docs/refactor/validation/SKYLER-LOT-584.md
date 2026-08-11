# SKYLER — LOT 584

## Ce que le lot établit

**L'origine d'un champ ne dit pas si son repli ment.** Les cinq sites « temps »
restants du 583 portent tous le même motif que le dossier du 582 —
`(champ || 0)` sur un horodatage. **Aucun des cinq ne produit le défaut du 582**,
et pour trois raisons différentes, dont **aucune n'est celle que je cherchais** :

- le champ ne peut pas manquer (`received_ts`) — mais **ce n'est pas ce qui les
  sauve** ;
- le consommateur regarde `0` lui-même et rend « — » (`VX.fmt.ago`) ;
- la branche est gardée par une **clef sœur** (`r.steps`) ;
- et sur `/portfolio`, le repli a l'effet **opposé** : il déclenche la branche,
  et cette branche est la réparation.

**Le défaut du 582 ne tient pas à l'origine du champ. Il tient au
consommateur** : `VX.fmt.ago` traite `0` comme une absence, `VX.freshness.assess`
le traite comme un âge réel.

## Le choix (ddd)

Le 583 a nommé six sites « temps » et constaté qu'**aucun n'a de garde en
amont**. Restait à savoir si ce constat vaut accusation. Le 582 avait tranché
pour un seul d'entre eux, en le lisant **aux deux bouts**. Ce lot fait le même
travail pour les cinq autres.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

Écrits dans `l584_piege.md` **avant** toute mesure.

### Attente 1 — « `received_ts` vient d'un flux de prix où l'horodatage est toujours présent ; le 582 reste seul »

**À moitié vraie, et fausse dans sa prémisse.**

- **Prémisse fausse** : `received_ts` ne vient d'**aucun flux de prix**. Il vient
  d'un **magasin de signaux TradingView** alimenté par un webhook
  (`vertex/data_sources/tradingview_signal_store.py`). J'aurais publié une
  origine inventée si je ne l'avais pas lue (581-A).
- **Conclusion vraie, mais pour la mauvaise raison** : le champ est bien toujours
  présent — et ce n'est pas ce qui rend le site sûr.
- **Fausse sur `r.ts`** : ce champ, lui, **peut être absent**.

### Attente 2 — contre-piège (582-C) : sur `base.ts`, le repli a l'effet OPPOSÉ

**Confirmée**, et plus encore : la branche déclenchée est la **réparation**.

## Les cinq sites, tracés aux deux bouts

### `base.ts` — `/portfolio`

**Origine : aucune côté serveur.** Le champ est écrit par **la page elle-même** :

```javascript
let base=null;try{base=JSON.parse(localStorage.getItem('vxPortfolioBaseline')||'null');}catch(e){}
const now=Date.now();
const snapshot={ts:now,netValue:m.netValue,plAbs:m.plAbs, …};
/* (Re)poser la référence : première fois, ou si > 12 h (une « visite » distincte), … */
if(m.allMarked&&(!base||(now-(base.ts||0))>43200000)){
  try{localStorage.setItem('vxPortfolioBaseline',JSON.stringify(snapshot));}catch(e){}
}
```

*(`vertex/ui/pages/portfolio_page.py:412-419`, lu.)*

**La question du lot ne s'y pose pas** : il n'y a pas de bout serveur. Le seul
écrivain pose toujours `ts`. Un `base` sans `ts` ne peut venir que d'une valeur
d'un autre format.

**Effet du repli** : `(now - 0) > 43200000` est **vrai** → la référence est
**reposée**. Le repli **déclenche** la branche au lieu de la masquer — l'inverse
exact du 582 — et cette branche **remplace** la valeur douteuse. Noter aussi que
`!base ||` court-circuite : `base.ts||0` n'est évalué que si `base` existe.

### `s.received_ts` — `/system` (1 site) · `/analysis/AAPL` (2 sites)

**Origine, lue** :

```python
entry = {'symbol': symbol, 'signal': signal, 'event_ts': event_ts,
         'received_ts': now, 'payload': dict(payload or {}),
         'action': 'REEVALUATE'}  # jamais un achat
self._signals.append(entry)
```

*(`tradingview_signal_store.py:75-78`.)* Servi par
`/api/tradingview/signals` → `jsonify({'signals': store.recent(symbol=sym), …})`
(`tradingview_webhooks.py:68`).

**Absence : non.** `_signals` n'a **qu'un seul écrivain** (`append`, ligne 78) et
l'entrée porte toujours `received_ts` ; `recent()` recopie l'entrée (`e = dict(s)`).

**Effet du repli, exécuté** : `VX.fmt.ago(0)` rend **`"—"`**, parce que le
consommateur garde lui-même :

```javascript
ago(ts) {
  if (!ts) return '—';
```

*(`vertex/static/vertex/js/vx-core.js:56`.)* **Le repli est neutralisé en aval.**

### `r.ts` — `/system`

**Origine, lue** : `vertex/services/startup.py:90-97`

```python
_REPORT.clear()
_REPORT.update({
    'ran': True, 'ts': time.time(),
    …
    'steps': steps,
    'ok': all(s['status'] not in ('ERROR',) for s in steps),
})
```

**Absence : OUI.** `_REPORT: dict = {'ran': False}` (ligne 14) — tant que la
séquence n'a pas tourné, **ni `ts` ni `steps`**, et `startup_report()` rend
`dict(_REPORT)` tel quel.

**Mais la branche est inatteignable**, gardée par une **clef sœur** :

```javascript
const r=await VX.fetch('/api/system/startup-report',{ttl:60000});
$('vx-auto-startup').innerHTML=(r.steps||[]).length ?
  ( … +`<div class="vx-card-footer">${VX.updateIndicator((r.ts||0)*1000,'séquence de démarrage','live')}</div>`)
  :VX.states.empty('Rapport non généré (serveur fraîchement démarré ?).');
```

La garde ne tient **que parce que `ts` et `steps` sont écrits par le même
`update()`** — un couplage, pas une vérification.

## Ce que `0` produit chez chaque consommateur — exécuté, pas déduit

`vx-core.js` chargé dans un bac à sable, fonctions **appelées** (`l584_effet.js`).
Calibration : `ago(horodatage réel, -5 min)` → `"Il y a 5 min"`.

| appel | résultat |
| --- | --- |
| `VX.fmt.ago(0)` | `"—"` |
| `VX.fmt.ago(undefined)` | `"—"` |
| `VX.fmt.ago((undefined\|\|0)*1000)` | `"—"` — la forme **exacte** des 3 sites |
| `VX.fmt.isoFull(0)` | `"01/01/1970 00:00:00"` |
| `VX.updateIndicator((undefined\|\|0)*1000,…)` | texte `—` · **infobulle `title="01/01/1970 00:00:00"`** |
| `assess({ageMs:(undefined\|\|0)*1000})` | `{state:'snapshot', label:'Analyse', tone:'info'}` |
| `assess({ageMs:null})` | `{state:'unknown', label:'—', tone:'muted'}` |

**Le contraste est là, en deux lignes** : `ago` **regarde** `0` et rend « — » ;
`assess` **prend** `0` pour un âge réel. Même motif, deux consommateurs, un seul
défaut.

## Constats — nommés, non corrigés

1. **L'infobulle n'est pas gardée comme le texte.** `updateIndicator` rend `—`
   en visible et `01/01/1970 00:00:00` en `title=`. Branche inatteignable
   aujourd'hui ; le constat porte sur la **forme**, pas sur un symptôme observé.
2. **Le serveur lui-même hésite sur `received_ts`** : deux replis défensifs
   (`s.get('received_ts', now)`, lignes 91 et 105) et **un accès nu**
   (`self._signals[-1]['received_ts']`, ligne 103). Si le champ pouvait vraiment
   manquer, la ligne 103 lèverait. Les trois lignes ne peuvent pas avoir raison
   ensemble.
3. **Quatre des cinq sites n'ont pas de bout serveur unique** au sens du 582 :
   un est purement client, trois viennent d'un magasin en mémoire non persisté.

**Rien n'est corrigé, ni signalé comme défaut. Le dossier du 582 reste le seul
ouvert, et il reste en attente d'un GO.**

## L'arrêt du lot — j'ai appliqué ma propre règle 580-C à contretemps

Mon second contrôle a d'abord annoncé **« 304 appels `Date.now()` sur 49
programmes »**. Ce total compte **un fichier statique une fois par page** — la
faute d'unité exacte que **j'ai nommée moi-même il y a quatre lots** (580-C).
Après déduplication des fichiers servis sur les 8 pages : **87 appels sur 49
fichiers distincts** (121 couples page|fichier). Le nombre publié est le second.

**Arrêtés avant publication : 210 → 211 (+1).**

## Second contrôle (481) — le cas que la restriction exclut

L'instrument du lot trace un champ **jusqu'au serveur**. Le cas qu'il exclut par
construction : un horodatage **produit client**, sans aucune source serveur —
`Date.now()`, **87 appels dans 49 fichiers servis**. La question « le champ
serveur peut-il être absent ? » n'y a pas de sens. `base.ts` en fait partie : le
lot l'a découvert **en cours de route**, ce qui montre que la frontière du
second contrôle n'était pas connue d'avance.

## Ce que le lot n'établit pas

- Que les 52 replis « mesure » du 583 soient sûrs : **aucun n'a été lu aux deux
  bouts**.
- Que l'infobulle `01/01/1970` s'affiche quelque part : la branche est
  inatteignable.
- Que le magasin de signaux ne puisse jamais être alimenté autrement : mesuré
  sur le code **présent** (`grep _signals`, un seul `append`).

## Limites déclarées

- Le bac à sable de `l584_effet.js` est un **remplacement**, pas un navigateur :
  `document`, `localStorage` et `fetch` y sont des coquilles. Les fonctions
  appelées (`ago`, `isoFull`, `updateIndicator`, `assess`) ne touchent ni au DOM
  ni au réseau ; pour d'autres fonctions, la mesure ne vaudrait pas.
- Les trois sites `received_ts` sont **deux programmes** (`/system` et
  `/analysis/AAPL`) — pas trois pages.

## Règles neuves

- **584-A — L'ORIGINE D'UN CHAMP NE DIT PAS SI SON REPLI MENT.** C'est le
  **consommateur** qui décide. Deux fonctions du même fichier traitent `0`
  autrement : l'une le lit comme une absence, l'autre comme une valeur.
- **584-B — UNE GARDE PEUT PORTER SUR UNE CLEF SŒUR.** Elle ne tient alors que
  parce que les deux clefs sont écrites par la même instruction. C'est un
  **couplage**, à nommer comme tel, pas une vérification.
- **584-C — UN TEXTE VISIBLE HONNÊTE N'ENTRAÎNE PAS UNE INFOBULLE HONNÊTE.**
  Vérifier les deux sorties d'un même appel.

## Ce que le dépôt fait bien

- **`VX.fmt.ago` garde `0` à sa source** — un seul `if (!ts) return '—'` protège
  **quatre** sites d'appel du défaut du 582.
- **Le magasin de signaux a un écrivain unique**, ce qui rend la question de
  l'absence tranchable en une lecture.
- **Le rapport de démarrage a un état initial explicite** (`{'ran': False}`) et
  un état vide honnête côté client (« Rapport non généré (serveur fraîchement
  démarré ?) »).
- Le commentaire de `/portfolio` **explique la règle des 12 h** au lieu de la
  laisser deviner.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **211 (+1)**
- Publiés puis corrigés : **38**
- Interprétations retirées : **11**
