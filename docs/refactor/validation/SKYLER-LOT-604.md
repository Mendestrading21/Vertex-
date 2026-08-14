# SKYLER — LOT 604 · LA SYNCHRO DES DONNÉES PERSONNELLES ÉCHOUAIT EN SILENCE

Le 603 déclarait hors périmètre trois formes de silence. Ce lot les mesure. Deux
sont **propres**. La troisième cachait le défaut le plus coûteux trouvé depuis
le 531.

## Le défaut : deux silences dans une ligne

`vx-entities.js::pushNow` pousse les données **personnelles** de l'utilisateur —
positions, journal, alertes, watchlist, notes — vers `/api/desk` :

```js
fetch('/api/desk', { method: 'POST', … }).catch(() => {});
```

1. **Un échec réseau est avalé** par le `.catch` vide.
2. **Un 4xx/5xx ne déclenche même pas ce `catch`.** `fetch` ne rejette que sur
   échec réseau ; **une réponse d'erreur RÉSOUT la promesse**, et `r.ok` n'était
   jamais lu. **Un refus du serveur était donc totalement invisible** — pas même
   au chemin d'erreur du code.

Trois sites portaient ce motif : `vx-entities.js` (le chemin de production, servi
aux 8 pages) et **deux copies inline** dans `/system` (import de clés, écriture
du coffre).

### Ce que ça coûte, exactement — et ce que ça ne coûte pas

**Rien n'est perdu.** `localStorage` garde tout et le push suivant rattrape. Le
coût réel est ailleurs : l'utilisateur **croit être synchronisé** alors que le
blob serveur vieillit. La facture arrive à l'ouverture sur un autre appareil, ou
après un vidage du navigateur. Le message le dit ainsi, sans dramatiser.

## La preuve, rouge puis verte, dans un vrai Chromium

Le banc injecte un **500 sur `POST /api/desk`**, déclenche une écriture de bureau
**réelle** (`VXEntities.toggleFavorite('AAPL')`), et regarde ce que
l'utilisateur apprend.

| | POST observés | toasts | `VX.store.desk_sync` |
| --- | --- | --- | --- |
| **AVANT — nominal** | 1 | aucun | `null` |
| **AVANT — serveur refuse (500)** | **1** | **aucun** | **`null`** |
| **APRÈS — nominal** | 1 | aucun | **`'ok'`** |
| **APRÈS — serveur refuse (500)** | **1** | **« Synchronisation du bureau impossible (refus du serveur, HTTP 500) — tes données restent sur cet appareil et repartiront à la prochaine réussite. »** | **`'error'`** |

**Le POST a bien eu lieu dans les quatre passes** (1 à chaque fois) : la voie
d'échec a été **exercée**, pas supposée — c'est **602-A** appliquée avant de
conclure.

L'avertissement est **unique** : deux nœuds `.vx-toast` sont présents, mais le
second est la confirmation « AAPL ajouté aux favoris ». Une **deuxième écriture
dans la fenêtre de 10 minutes n'ajoute aucun nouvel avertissement** — le
throttle tient, vérifié.

## Les deux autres formes exclues par le 603 : propres

### Forme B — 37 gardes `if(!x)return;` hors `catch`

Presque toutes de la forme `const host=$('x'); if(!host)return;`. Le garde est
sain **si l'hôte existe** ; s'il n'existe sur **aucune vue**, la zone
n'apparaît **jamais** — le silence le plus complet possible.

**Mesure sur les 35 URL des 8 pages : 31 hôtes gardés, 31 présents dans le HTML
SERVI, 0 introuvable.**

### Forme D — `Promise.allSettled` sur les deux vues de `/system`

`/system` est la page qui **rapporte** l'état des connexions : son silence
coûterait le plus cher. Ses deux vues ouvrent par un `allSettled` qui transforme
chaque rejet en `null`.

| passe | erreurs console | texte | états honnêtes affichés |
| --- | --- | --- | --- |
| `view=connections` nominal | 0 | 4 106 car. | 0 |
| **`view=connections`, 4 sources en 500** | 8 *(injectées)* | 3 164 car. | **5** — « État système indisponible », « Live Engine injoignable », « /healthz injoignable »… |
| `view=data` nominal | 0 | 2 056 car. | 1 |
| **`view=data`, 3 sources en 500** | 6 *(injectées)* | 1 175 car. | **4** — « Diagnostics indisponibles », « Rapport de qualité indisponible »… |

**`/system` dit la vérité quand ses propres sources tombent.**

## L'arrêt du lot — 603-B commise dans le lot suivant celui qui l'a écrite

Mon premier contrôle d'hôtes **devinait** les vues (`?view=learning` au lieu de
`learnings`, `progression` jamais servie) et déclarait `vx-pf-prog`
**INTROUVABLE**. Il ne l'est pas : il vit sur `view=progression`, que je n'avais
pas chargée. **C'est exactement 603-B — une voie ne s'exerce que sur la vue qui
l'appelle — commise au lot 604.**

Second défaut du même jet : il acceptait un id trouvé **dans la source du
module** à défaut du HTML servi. Cette porte de secours aurait fait passer un id
construit par une chaîne morte (**600-A**). Le banc corrigé **lit la liste des
vues dans le code** (`_VIEWS` / `VIEWS`) et n'accepte **que** le HTML servi.

**Arrêtés avant publication : 234 → 235 (+1).**

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « les 3 formes exclues cachent au moins autant de défauts que la forme `catch` (4) » | **RÉFUTÉ — 3 sites, un seul motif** |
| **(b)** | « la forme B, la plus nombreuse (37), est la plus dangereuse » | **RÉFUTÉ — 0 défaut sur 37** |
| **(c)** | « le défaut, s'il existe, est un problème d'affichage » | **RÉFUTÉ — c'est un problème de DONNÉES**, sur le seul chemin qui écrit chez l'utilisateur |
| **global** | | **RÉFUTÉ trois fois — et le lot vaut plus que le piège** |

**Le volume est un mauvais guide.** 37 gardes bénins, 2 `allSettled` propres,
**3 lignes** qui portent le seul vrai défaut. Le rapport nombre/gravité est
**inverse** — comme au second contrôle du 603.

## Ce que le lot n'établit pas

- **Que `sendBeacon` dise son échec.** Le flush au `pagehide` passe par
  `navigator.sendBeacon`, dont la valeur de retour n'indique que la mise en
  file, jamais la réponse du serveur. **Ce chemin reste muet par construction** —
  nommé, non traité.
- Que le message soit le bon **au bout de dix minutes** de panne continue : le
  throttle affiche une alerte par fenêtre, il ne tient pas de registre.
- Que `/system` reste honnête sur ses **trois autres vues** (`automations`,
  `settings`, `archive`) : seules `connections` et `data` portent un `allSettled`.
- Que les 31 hôtes existent **à l'exécution** : je les ai vérifiés dans le HTML
  servi, pas après manipulation du DOM.

## Règles neuves

- **604-A — `fetch` NE REJETTE PAS SUR 4xx/5xx : UN `.catch` SEUL NE VOIT RIEN.**
  Un refus du serveur résout la promesse. Sans lecture de `r.ok`, le chemin
  d'erreur du code **n'est jamais exécuté** — le silence est plus profond qu'un
  `catch` vide, qui au moins s'exécute.
- **604-B — LE VOLUME D'UNE FORME EST UN MAUVAIS GUIDE VERS SA GRAVITÉ.**
  37 gardes → 0 défaut ; 3 lignes → le défaut le plus coûteux du lot. Deuxième
  fois dans l'arc, après le second contrôle du 603.
- **604-C — UN SILENCE SUR LE CHEMIN D'ÉCRITURE COÛTE PLUS QU'UN SILENCE À
  L'AFFICHAGE.** Une zone muette se voit ; une synchro muette laisse croire que
  tout va bien. La première se répare en rechargeant, la seconde se découvre sur
  un autre appareil.

## Ce que le dépôt fait bien

- **Le gardien du lot 361 a arrêté le commit.** Premier changement d'un octet
  sous `/static` de tout l'arc : le test a échoué en donnant **la marche à
  suivre exacte** (bumper, puis ré-enregistrer empreinte et version). Il a fait
  précisément ce pour quoi il a été écrit.
- **31 hôtes gardés sur 31 existent.** Aucune zone fantôme dans le produit.
- **`/system` reste honnête quand tout tombe** : 5 et 4 états explicites, aucun
  chiffre inventé, aucun zéro de complaisance.
- **`localStorage` protège la donnée** : le défaut portait sur l'information de
  l'utilisateur, jamais sur son travail.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **3 fichiers de production** : `vertex/static/vertex/js/vx-entities.js`,
  `vertex/ui/pages/system_page.py`, `vertex/app/routes/system.py` (bump).
- **6 gardiens mis à jour** : les 5 épingles de version `td-shell-v189` →
  **`td-shell-v190`**, plus `tests/test_sw_cache_scope_lot361.py` (empreinte des
  assets **et** `_SW_VERSION`, qui pointait encore 187).
- MD5 des 8 pages : **7 / 8 identiques** — seule `/system` bouge
  (`73e917c0f2d0` → **`f657bf63178b`**). `vx-entities.js` étant un fichier
  statique, les 7 autres pages ne changent pas d'un octet **alors même que leur
  comportement de synchro change** : la preuve que le correctif est au bon endroit.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**
  (20 fichiers ; 8 modifiés par les sessions navigateur, restaurés).
- Suite : **2864 passed / 0 skipped**.
- Navigateur : **8 passes** (2 desk avant, 2 desk après, 4 `/system`), voies
  d'échec exercées et prouvées.
- **READONLY intact**.

## Comptes

- Arrêtés avant publication : **235 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
- **Dossiers produit corrigés : 3**
