# SKYLER — LOT 586

## Ce que le lot établit

**Les deux « sites les plus conséquents » du 585 sont inertes.** Un repli `|| 0`
placé devant un seuil **strictement positif** ne change **rien** :
`undefined >= 78` est faux, `(undefined || 0) >= 78` est faux aussi. Évalué sur
**25 combinaisons** (5 formes d'absence × 5 seuils) : le repli ne modifie le
résultat que pour un seuil **≤ 0**, et seulement sur `undefined` et `NaN` —
**4 cas sur 25, aucun aux seuils 78 et 80**.

**Je retire donc une interprétation du 585.** Sa phrase « le repli ne produit pas
un “0” visible — il produit une catégorie différente » est **fausse quant au
repli** : le déclassement se produit **avec ou sans lui**. Ce qui déclasse, c'est
la comparaison elle-même, écrite **sans repli** trois lignes plus haut.

## Le choix (fff)

Le 585 avait explicitement déclaré **non mesuré** le point qui tranche :
`score` peut-il être absent côté serveur ? Ce lot le mesure — et découvre que la
question, seule, ne suffisait pas.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

| piège | verdict |
| --- | --- |
| **Attente 1a** — `r.score` vient du scanner serveur et est toujours présent | **CONFIRMÉE**, et **lue** : `score = int(max(0, min(100, base_score + struct_adj)))` — toujours un entier |
| **Attente 1b** — `snap.score` est un instantané client où le champ peut manquer | **CONFIRMÉE**, et **lue** : la branche de repli de `tSnapOf` ne contient **aucune clef `score`** |
| **Contre-piège 1 (585-B)** — lire ce que la branche fait du `0` | **DÉCISIF** : elle n'en fait **rien**, le repli est inerte au-dessus de 0 |
| **Contre-piège 2 (584-B)** — une garde peut porter sur une clef sœur | **CONFIRMÉ** : `b==='Actionnable'` exige déjà `r.score>=72`, **écrit sans repli** |

## Les deux origines, lues dans le code

### `r.score` — `/opportunities`

La page appelle **`/scan`** (`opportunities_page.py:235`, `:366`), pas
`/api/opportunities/funnel` (qui ne sert que le widget entonnoir).

```python
rows.append({'symbol': sym, 'price': d['price'], 'change': d['change'],
             'score': d['score'], 'grade': d['grade'], 'verdict': d['verdict'], …})
…
rows.sort(key=lambda x: x['score'], reverse=True)
```

*(`terminal.py:411-412`, `:444`.)* Deux **accès nus** — pas de `.get`. Une ligne
sans `score` lèverait, et le `except Exception: continue` la ferait **tomber**.
Et à la source :

```python
score = int(max(0, min(100, base_score + struct_adj)))
```

*(`vertex/engines/analysis.py:228`.)* **Le champ ne peut pas manquer, et ne peut
pas valoir `None`.**

### `snap.score` — `/portfolio`

Aucune origine serveur. Le champ est écrit par le client, à l'ouverture d'une
position :

```javascript
var snap=(typeof window.tSnapOf==='function')?window.tSnapOf(s)
        :{spot:price,stop:stop,tgt:tgt,date:new Date().toISOString().slice(0,10)};
…entrySnap:snap,…
```

*(`vertex/ui/vx_kit.py:187`, lu.)* **La branche de repli ne contient aucune clef
`score`.** L'absence est donc un chemin réel — mais côté client, et sans
conséquence au seuil 78.

## Ce que le repli change dans un seuil — évalué, pas déduit

| valeur absente | seuil | `x >= S` | `(x‖0) >= S` | différent ? |
| --- | --- | --- | --- | --- |
| `undefined` | 78 · 80 · 1 | false | false | **non** |
| `undefined` | **0 · -1** | false | **true** | **OUI** |
| `null` | 78 · 80 · 1 | false | false | non |
| `''` | 78 · 80 · 1 | false | false | non |
| `NaN` | **0 · -1** | false | **true** | **OUI** |
| `false` | 78 · 80 · 1 | false | false | non |

**4 cas sur 25**, tous à un seuil `≤ 0`. `null`, `''` et `false` sont **coercés
en `0`** par `>=` : pour eux, les deux écritures sont identiques **partout**.

## Second contrôle (481) — le seuil écrit sans repli

La restriction des lots 583-585 est « le site porte un `|| 0` ». Elle exclut les
seuils écrits sur un **champ nu** — pourtant c'est la même décision. Comptés sur
les octets servis, seuils `> 1`, fichiers dédupliqués (580-C) :

| forme | sites |
| --- | --- |
| seuil sur un champ **nu** | **210** |
| seuil sur un champ **replié** | **3** |

**Le repli est l'exception : 3 sur 213, soit 1,4 %.** Les trois, tous listés :

```javascript
(r.score||0)>=80              // /opportunities
(snap.score||0)>=78           // /portfolio
(d.top_weight_pct||0)>15      // /portfolio  ← découvert par ce contrôle
```

Le troisième n'avait été nommé par aucun lot précédent comme seuil : le 583 le
comptait parmi les 52 « mesure », sans savoir que c'était une **décision**.
Comme les deux autres, son seuil est positif — **donc inerte lui aussi**.

Et le témoin du contrôle, `r.score>=72` dans `bucketOf`, est bien un des 210 :
**le déclassement d'une opportunité sans score est décidé là, sans aucun repli.**

## Constat — deux scanners, deux contrats opposés sur le même nom

Le dépôt contient **deux** producteurs de `score`, avec des contrats **inverses** :

- `terminal.py` / `analysis.py` (route `/scan`) : `int(max(0, min(100, …)))` —
  **jamais `None`** ;
- `vertex/scanner/stages.py`, dont l'en-tête déclare
  `{'passed': bool, 'score': 0..100 | None, …}` et précise « **une donnée absente
  ne fabrique JAMAIS un score** », avec
  `'score': round(sum(scores)/len(scores), 1) if scores else None`
  (`candidate_pipeline.py:52`) — **`None` par conception**.

Le second alimente `/api/opportunities/funnel`, **qui ne nourrit pas `tierOf`**.
Les deux contrats coexistent sans se croiser ici — mais **le nom `score`, seul,
ne dit pas lequel on tient**.

## Ce que le lot n'établit pas

- Que ces trois replis soient inutiles : ils sont **inertes**, ce qui n'est pas
  la même chose qu'inutile — un seuil peut changer.
- Que les 210 seuils nus soient corrects : **ils n'ont pas été lus**, seulement
  comptés.
- Que `tSnapOf` soit réellement absent en pratique : la branche existe, sa
  fréquence n'est pas mesurée.
- Que le contrat `None` de `stages.py` n'atteigne aucun seuil ailleurs : **non
  mesuré**.

## Limites déclarées

- Le relevé (B) ne garde que les seuils dont la **droite est un littéral
  numérique `> 1`** : un seuil comparé à une variable (`>= state.minScore`) lui
  échappe. Le relevé est un **plancher** (550-B).
- L'évaluation (A) porte sur cinq formes d'absence ; une valeur exotique
  (objet, tableau vide) n'y figure pas.
- Aucun arrêt ce lot : la calibration est passée du premier coup, aucun banc
  n'a été jeté. **Les compteurs d'arrêts ne bougent pas — le dire est aussi une
  mesure.**

## Règles neuves

- **586-A — UN REPLI DANS UN SEUIL EST INERTE SI LE SEUIL EST STRICTEMENT
  POSITIF.** `x >= S` et `(x || 0) >= S` ne diffèrent que pour `S <= 0`.
  Avant d'accuser un repli, évaluer les deux écritures.
- **586-B — DEUX PRODUCTEURS DU MÊME DÉPÔT PEUVENT AVOIR DES CONTRATS OPPOSÉS
  SUR LE MÊME NOM DE CHAMP.** Nommer la **route**, jamais le champ seul.
- **586-C — MESURER LA FRÉQUENCE DE L'ÉCRITURE CONCURRENTE AVANT DE QUALIFIER
  UNE ÉCRITURE.** 3 seuils repliés contre 210 nus : ce qui semblait la forme
  dominante est l'exception.

## Ce que le dépôt fait bien

- **`bucketOf` compare sans repli** : `r.score>=72`, `>=66`, `>=56`. Une absence
  y tombe en `Radar`, ce qui est le classement prudent.
- **Le score du scanner est borné à la source** (`max(0, min(100, …))`) : le
  contrat est tenu par construction, pas par des gardes dispersées.
- **`stages.py` documente son contrat en tête de fichier** et refuse de
  fabriquer un score : « une donnée absente ne fabrique JAMAIS un score ».
- **Sur la même page**, le même champ est affiché avec une garde honnête :
  `const n=Number(v); if(!isFinite(n)) return VX.fmt.nd(v);` — le dépôt sait
  écrire la branche prudente, et l'écrit là où elle sert.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **213 (inchangé)**
- Publiés puis corrigés : **38**
- Interprétations retirées : **12 (+1 — celle du 585 sur les deux seuils)**
