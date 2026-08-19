# #781 · Lot 2 — La preuve de non-usage, et ses trois trous

Instrument : `tools/vertex_1_0/mesurer_regles_mortes.py`
Gardien    : `tests/test_vertex_1_0_regles_mortes.py` (11 tests)

---

## Ce qu'il fallait produire

Le lot 1 a rendu **476 règles CSS jamais appariées au chargement**. C'est une
liste de **candidates**, et `CLEANUP_POLICY.md` demande davantage : une **preuve
de non-usage**. Ce lot produit cette preuve.

```text
476 candidates
 63 PROUVÉES inatteignables   aucune de leurs classes n'est écrite nulle part
401 atteignables              une classe existe quelque part dans les octets
 12 indécidables              sélecteur sans classe, ou dérivé d'un préfixe assemblé

corpus : 99 documents servis · 4,34 Mo
```

## Le critère

Une règle est **prouvée inatteignable** quand **aucune** classe de son sélecteur
n'apparaît, comme littéral, dans **aucun octet servi** — ni dans le HTML des
pages, ni dans le JavaScript qu'elles chargent.

Le raisonnement : si `vx-machin` n'est écrit nulle part dans ce que le navigateur
reçoit, aucun chemin — rendu serveur, `classList.add`, gabarit — ne peut le
poser. La règle ne peut pas s'allumer.

**Le doute profite à la règle.** Une seule classe présente suffit à classer le
sélecteur `ATTEIGNABLE`, même s'il ne s'apparie jamais au chargement. C'est ce
qui protège le CSS des **états** — `.vx-drawer.open`, `.vx-row.is-selected` —
celui qu'on voit le moins et dont on a le plus besoin.

---

## Les trois trous, trouvés avant d'agir

Une preuve trouée est **pire qu'une absence de preuve** : elle autorise l'acte.
Chacun de ces trois défauts aurait fait supprimer du CSS vivant.

### 1. Le corpus ne couvrait que les huit espaces

`.ds-note` ressortait « prouvée inatteignable ». Elle est **écrite deux fois
dans la page `/design-system` servie**.

Le produit sert bien plus que huit routes HTML — `/widget-lab`,
`/intelligence`, `/tracking`, `/design-system`, `/vault`… Le corpus vient
désormais de la **table de routage**, pas d'une liste choisie à la main.

```text
corpus 35 → 88 documents      preuves 92 → 63
```

**29 fausses preuves, soit près d'un tiers.**

### 2. Les routes paramétrées manquaient

`/analysis/<sym>`, `/company/<sym>`, `/options/<sym>` rendent un balisage que
les pages d'index n'ont pas. Elles sont instanciées avec un symbole réel.

```text
corpus 88 → 99 documents      preuves 63 → 63
```

Le compte n'a pas bougé — ce qui rend la preuve d'autant plus solide : **elle a
résisté à l'élargissement**.

### 3. Les noms de classe assemblés à l'exécution

`'vx-chart-size-' +` fabrique un nom à l'exécution. Le nom complet n'existe
**nulle part** dans les octets, et c'est *précisément parce qu'il est fabriqué*.
Les règles qui en dérivent sont écartées vers `INDÉCIDABLE`, jamais vers les
preuves.

### Le piège évité de justesse

La première version cherchait **toute** interpolation `${…}` pour détecter les
noms construits. Elle aurait trouvé chaque gabarit de texte, d'URL ou de nombre
du produit, déclaré la preuve « non fiable » partout, et rendu l'outil
inutilisable. Un détecteur qui crie sur tout ne guide rien — c'est la même
leçon que les 113 fausses cibles tactiles et les 34 faux contrastes.

---

## Ce qui est fait, et ce qui ne l'est pas

**Fait.** La preuve existe, elle est reproductible, et le recensement est **gelé
à 63** dans un gardien : il peut baisser librement (on a nettoyé), il ne peut
pas monter en silence. C'est exactement ce que `CLEANUP_POLICY.md` demande en
interdisant « tout empilement de CSS temporaire sans date de retrait » — ce
plafond **est** la date de retrait.

**Pas fait, et c'est un choix.** Les 63 règles ne sont **pas supprimées**. Le
gain est de quelques kilo-octets sur une release candidate verte ; le risque
d'une réécriture automatisée de six feuilles CSS ne l'est pas. La valeur
durable de ce lot est la preuve et le plafond, pas la suppression.

La suppression reste disponible à la demande : la liste exacte est dans
`--json`, sous `detail`, feuille par feuille.

---

## Ce que cette preuve ne dit pas

- Elle porte sur les **octets servis** en mode démo sans IBKR. Une page qui ne
  s'affiche qu'avec un compte réel connecté n'est pas dans le corpus.
- Un fichier JavaScript qui ne serait pas référencé par un `<script src>` —
  chargé dynamiquement — échapperait au corpus.
- `/memory/<decision_id>` est instanciée avec un identifiant inexistant : son
  balisage d'erreur est couvert, pas celui d'une décision réelle.
- Les routes qui **déclenchent** du travail (`/scan`, `/weekly-regen`) sont
  exclues : mesurer ne doit rien provoquer.
