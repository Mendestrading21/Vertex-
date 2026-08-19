# G6 — Revenir en arrière est-il possible sans rien perdre ?

Instrument : `tools/vertex_1_0/mesurer_rollback.py`
Gardien : `tests/test_vertex_1_0_rollback.py` (7 tests, 5 mutations éprouvées)
Mesuré le 19/08/2026, depuis `8093088` vers `d52a39d`

---

## Ce que le rapport disait, et pourquoi c'était une renonciation

> « **Rollback applicatif non testé** : revenir à un SHA antérieur et démarrer
> demanderait un second arbre de travail. »

C'était présenté comme une limite d'environnement. Ce n'en était pas une :
`git worktree` fait exactement cela, et il restait 28 Go. La phrase décrivait le
fait de ne pas l'avoir fait, pas une impossibilité. Elle est levée ici.

## La question n'est pas « est-ce que ça redémarre »

Un rollback qui démarre mais rend un bureau vide n'est pas un rollback — c'est
une panne différente, et plus difficile à diagnostiquer. Deux points sont donc
mesurés, et **c'est le second qui répond** :

1. la version antérieure démarre-t-elle, et sert-elle une **page** (pas
   seulement `/healthz`, qui répond avant que le rendu n'existe) ;
2. relit-elle **les données écrites par la version récente**, à l'identique.

Le point 2 échappe par construction aux tests unitaires : il ne se voit qu'en
faisant tourner **deux versions sur les mêmes octets**.

## Fidélité du montage

`persist.cache_path` ancre les fichiers à la racine du dépôt. Un `worktree` a sa
propre racine, alors qu'un vrai rollback (`git checkout <sha>` sur place) garde
la même. `desk_data.json` est donc **recopié** dans l'arbre antérieur — sans
cela on mesurerait un démarrage à vide, c'est-à-dire une réponse « oui » à une
question qu'on n'a pas posée. Le gardien tient cette recopie.

## L'instrument s'est trompé le premier, une fois de plus

Premier essai : « la version antérieure NE DÉMARRE PAS ». Le journal disait :

```
Address already in use
Port 5002 is in use by another program.
```

Le banc passait `VERTEX_PORT`, **que rien ne lit** — le produit lit
`os.environ.get('PORT', 5002)`, des deux côtés du rollback. La version
antérieure s'était donc liée au port déjà occupé. L'instrument accusait le
produit d'un défaut qui était le sien ; c'est la sixième fois de la campagne, et
le gardien épingle désormais la variable réellement lue par le produit.

## Résultat

```
version courante  : 8093088c6280
retour vers       : d52a39d4baf1        (base commune avec main)

1. la version anterieure DEMARRE      : oui
2. elle SERT la page d'accueil        : 200 (40 336 octets)
3. elle relit le bureau ECRIT PAR LA VERSION RECENTE :
     7 cles ecrites -> 7 cles relues
     identique : OUI
```

**Le retour arrière est prouvé sans perte** sur les sept clés du bureau
(`myTrades`, `myFavs`, `myNotes`, `vxJournal`…), contenus compris — pas
seulement les noms de clés.

## Les trois façons de perdre, nommées séparément

Le comparateur distingue, et ce n'est pas de la taxinomie :

| famille | ce que l'utilisateur voit | gravité |
| --- | --- | --- |
| **absentes** | la liste est vide, il appelle | franche, visible |
| **différentes** | un écran plausible, et faux | **silencieuse** |
| **ajoutées** | rien | bénin, mais premier signe d'un écart de format |

Les confondre permettrait d'écrire « aucune clé perdue » sur un bureau vidé de
sa substance. La mutation R1 (fusionner « différentes » dans « absentes ») et R2
(ne juger « identique » que sur les disparitions) sont toutes deux détectées.

## Ce que ce chantier NE prouve pas

- **le rollback du service worker** n'est pas mesuré ici. Le raisonnement dit
  qu'il se règle seul (`activate` supprime tout cache dont la clé diffère, donc
  un retour de v211 à v210 purge v211), mais un raisonnement n'est pas une
  mesure et il ne faut pas le lire comme telle ;
- **la migration de format à l'endroit** (`checkout` dans le même répertoire)
  n'est pas éprouvée : le montage passe par un arbre séparé et une recopie.
  L'écart est le chemin des fichiers, pas leur contenu.

## Note sur l'autre résidu G6 — les CVE

Le rapport annonçait « vulnérabilités connues non recherchées : il faudrait une
base de CVE à jour, absente de cet environnement ». Vérifié plutôt que supposé :
la politique réseau de l'environnement refuse le `CONNECT` vers tout hôte hors
registres de paquets — `api.osv.dev` répond **403, `policy denial`**. Le résidu
tient, avec désormais sa raison exacte : ce n'est pas un outillage manquant,
c'est une politique. Il se lèvera dans un environnement à la politique plus
large, ou par un scan hors ligne alimenté par une base embarquée.
