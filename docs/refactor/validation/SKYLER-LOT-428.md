# SKYLER LOT 428 — L'entonnoir du scan est plat par construction : il cherche des verdicts en français dans un moteur qui répond en anglais

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-428` (base : lot 427 fusionné,
189f340)

Douzième lot de la veine, **quatrième mené depuis l'écran**. Le 427 avait porté
le recensement de 17 à **118 affirmations rendues** et n'en avait ouvert
**qu'une**. Celui-ci en ouvre une deuxième — et la vérification de cette
affirmation, qui s'est révélée **vraie**, a mis au jour un défaut chez sa
voisine.

**Aucun code, aucun gardien, aucun test.**

## L'affirmation ouverte — et elle est exacte

Carte « Répartition des verdicts du scan » (`/markets`, `vx-mk-verdicts`) :

> `explain:{shows:'Le décompte des verdicts moteur sur l’univers scanné`
> `(max 5 catégories).'}`

Le code tronque bien : `Object.entries(counts).sort(…).slice(0,5)`. Et le
vocabulaire du moteur est fermé — `vertex/strategy/config.py:51` :

```python
def verdict(score, trend, regime=None):
    """BUY / WATCH / WAIT / AVOID selon le profil (cahier §3/§8)."""
```

**Quatre valeurs, jamais vides.** Le `slice(0,5)` ne coupe donc **jamais** :
l'affirmation est **vraie**, mais elle ne mord jamais. C'est le genre de résultat
qu'il faut dire tel quel.

## Ce que la même mesure a révélé chez la voisine

Juste sous ce donut, dans la même fonction, **l'entonnoir de sélection** — servi
dans le marquage de `/markets?view=breadth` :

```javascript
const isBuy = v => ['ACHETER','RENFORCER'].includes((v||'').toUpperCase());
const isAct = v => { const u=(v||'').toUpperCase(); return u && u!=='ÉVITER' && u!=='EVITER'; };
const dossiers = rows.filter(r => isAct(r.verdict || r.decision)).length;
const buys     = rows.filter(r => isBuy(r.verdict || r.decision)).length;
```

**Les deux prédicats interrogent un vocabulaire FRANÇAIS. Le champ `verdict` des
lignes du scan ne contient que du vocabulaire ANGLAIS.** `isBuy('BUY')` est faux ;
`isAct('AVOID')` est vrai.

*(Le repli `|| r.decision` ne rattrape rien : la clé `decision` en français est
portée par la liste `recs` de `terminal.py:596`, pas par les `rows` du `/scan`,
construites en `terminal.py:412` avec `'verdict': d['verdict']`.)*

## Mesure — en EXÉCUTANT les octets servis

Le bloc de l'entonnoir (**1 148 octets**) a été extrait du **marquage servi** de
`/markets` par appariement d'accolades, puis exécuté sous Node 22 avec
`VXCharts.funnel` stubé, sur des univers fabriqués :

```text
univers                                     étapes rendues
30 BUY · 20 WATCH · 10 AVOID     Univers 60 → Notés 60 → Dossiers actionnables 60 → Achats 0
 2 BUY ·  8 WATCH · 50 AVOID     Univers 60 → Notés 60 → Dossiers actionnables 60 → Achats 0
100 % AVOID                      Univers 60 → Notés 60 → Dossiers actionnables 60 → Achats 0
TÉMOIN vocabulaire français      Univers 60 → Notés 60 → Dossiers actionnables 50 → Achats 30
```

**Le marché le plus porteur et l'univers entièrement rejeté produisent le même
entonnoir.** Le témoin positif — les mêmes lignes étiquetées `ACHETER` /
`ATTENDRE` / `ÉVITER` — resserre correctement : **la logique fonctionne, c'est le
vocabulaire qui ne se rencontre pas.**

Trois des quatre étages sont constants : `noted` compte les lignes dont
`score != null`, et `terminal.py:412` écrit `score` à la construction de **chaque**
ligne — l'étage « Notés » ne resserre que si un score vaut `null`.

## Et ce que la carte affirme, elle, est rendu

Dans le marquage servi de `/markets?view=breadth`, sous l'entonnoir :

> *« Chaque étape resserre l'univers scanné jusqu'aux verdicts d'achat du comité.
> Aucune idée n'est forcée : **un entonnoir plat = marché hostile.** »*

C'est le point qui fait basculer ce lot du rang 3 au rang 1. **La phrase donne au
trader la clé de lecture d'un entonnoir plat — et l'entonnoir est plat par
construction, toujours, quel que soit le marché.** Un décalage de vocabulaire est
présenté comme un signal de marché.

Le conteneur `id="vx-mk-funnel"` n'existe que dans **une vue sur les huit
mesurées** (`/markets?view=breadth`) ; la phrase d'aide y est injectée à
l'exécution. `C.funnel` est bien défini dans le `chart-core.js` servi.

## Bornage — sur les octets servis

Recherche de toute comparaison d'un champ `verdict`/`decision` au vocabulaire
français dans le corpus servi (95 objets, 3 829 722 octets) :

```text
page              accepte AUSSI le vocabulaire moteur (BUY/AVOID)
/opportunities    OUI   (3 fragments : `r.verdict==='AVOID'||r.verdict==='ÉVITER'`,
                         `r.verdict==='BUY'||r.verdict==='ACHETER'`, `opActive`)
/markets          NON   (2 comparaisons : isBuy, isAct)
```

**Le dépôt SAIT que ce champ peut porter les deux vocabulaires** — `/opportunities`
accepte systématiquement les deux formes sur le **même champ**. `/markets` est le
seul site servi qui n'accepte que le français. **1 site défectueux sur 2.**

À signaler sans l'expliquer : `vertex/ui/pages/analysis_page.py:524` porte un
`/ACHETER|BUY|RENFORCER|ACCUMULER/i` qui accepterait les deux — mais cette chaîne
**n'apparaît dans aucun octet servi**. Mesuré, non interprété.

## Le gardien existe, et il est vert

```python
def test_breadth_selection_funnel_real_data():
    """Vue Breadth : entonnoir de sélection alimenté par les données réelles du scan."""
    src = open(…'markets_page.py'…).read()
    for needle in ('vx-mk-funnel', 'VXCharts.funnel', 'Univers scanné', 'vx-mk-breadth-trend'):
        assert needle in src, needle
```

Son **nom** promet un entonnoir « alimenté par les données réelles du scan ». Ses
**assertions** vérifient la présence de quatre chaînes dans le fichier source. Il
**n'exerce pas une seule ligne de scan** et resterait vert quel que soit le
vocabulaire comparé. C'est le motif des lots 416 et 417 : *le nom d'un gardien
peut promettre autre chose que son assertion.*

## Ce que je n'ai pas observé, et que je dis

Le scan est vide au démarrage et aucun payload persisté ne contient de `rows` :
**je n'ai pas constaté d'entonnoir plat sur un scan réel.** Le décalage est établi
par exécution du code servi sur des univers fabriqués, avec le vocabulaire lu
dans la **source de vérité** du moteur (`config.py:51`), corroboré par trois
autres consommateurs de ce champ dans `terminal.py` (`:445` `== 'BUY'`, `:1460-1462`
`'BUY'`/`'WATCH'`/`'WAIT'`/`'AVOID'`, `:5512` les puces de filtre).

## Classement

**Rang 1**, famille des 422/425/427 : les **valeurs** du scan sont réelles, aucun
chiffre n'est inventé. Ce sont les **comptes dérivés** qui sont faux — « Achats »
vaut 0 en permanence, « Dossiers actionnables » compte les titres rejetés — sur
une carte qui **explique au trader comment lire sa propre platitude**.

Correction pressentie, minuscule : accepter les deux vocabulaires comme le fait
déjà `/opportunities` (`['ACHETER','RENFORCER','BUY']`, exclusion
`['ÉVITER','EVITER','AVOID']`). **Aucun GO, rien n'est engagé.**

## Portée

Deux affirmations ouvertes sur les 118 recensées (une au 427, une ici) ; **116
restent listées, non vérifiées**. Le recensement reste borné aux littéraux de 10 à
200 caractères : **les phrases construites dynamiquement lui échappent toujours**
— la phrase d'aide de l'entonnoir, elle, a été trouvée par voisinage, pas par le
recensement.

L'entonnoir n'a pas été rendu dans un navigateur ; `VXCharts.funnel` est stubé et
le rendu SVG n'a pas été exécuté. Je mesure les **valeurs passées** aux étages,
pas leurs pixels.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** (leçon du 427) : 21 fichiers, aucun
  apparu, aucun disparu. Les trois fichiers ré-horodatés par la suite ont été
  **restaurés à l'octet près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente et unième lot court. Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ ·
419 ✓ · 421 ✗ · 422 ✓ · 423 ✗ · 424 ~ · 425 ✓ · 426 ✗ (bornage) · 427 ✓ · 428 ✓**.

Le motif tient une neuvième fois, et le 427 avait donné la bonne consigne de
recherche : *chercher partout où un libellé vient d'une source et sa valeur d'une
autre.* Ici ce n'est plus un index qui glisse, c'est une **langue** — deux
vocabulaires pour un même champ, dont un seul est produit. Et comme au 425, la
phrase qui devrait protéger le lecteur est celle qui l'égare : elle lui apprend à
interpréter une platitude qui n'a aucune cause de marché.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
