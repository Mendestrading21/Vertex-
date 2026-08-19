# « Je lance TWS et ça se connecte » — ce qui s'y opposait

Module : `vertex/data_sources/ibkr_link.py`
Gardien : `tests/test_vertex_1_0_ibkr_link.py` (18 tests, 9 mutations éprouvées)
Sites recâblés : 4 dans `terminal.py` + `ibkr_gateway.py`

---

## Le constat

La connexion elle-même n'était pas cassée. Ce qui l'était, c'est **l'accord
entre les cinq endroits qui se connectaient** — et ce genre de défaut ne se voit
pas en ouvrant une connexion, seulement en comparant les sites entre eux.

| site | ports essayés | clientId |
| --- | --- | --- |
| worker options (`terminal.py`) | 7496, 7497, 4001, 4002 | 41 |
| lecture du compte (`terminal.py`) | **7497, 7496, 4002, 4001** | **17** |
| cotations live (`terminal.py`) | 7496, 7497, 4001, 4002 | 18 |
| indices (`terminal.py`) | 7496, 7497, 4001, 4002 | 22 |
| passerelle (`ibkr_gateway.py`) | **7497 seul** | **17** |

### Trois défauts, dont un qui fausse l'écran

**1. La lecture du compte cherchait le PAPIER en premier**, les trois flux le
RÉEL. Quand les deux TWS répondent — ce qui arrive à qui teste une stratégie à
côté de son compte réel — l'écran affiche **le cash d'un compte et les cotations
d'un autre**, sans que rien ne le dise. Chaque chiffre est vrai ; l'écran est
faux. C'est un mensonge de composition, la variété la plus difficile à repérer
parce qu'aucune valeur prise isolément n'est fausse.

**2. Deux sites partageaient le clientId 17.** IBKR refuse une seconde session
portant un identifiant déjà pris. Selon l'ordre de démarrage, l'un des deux
échouait — et le message d'erreur ne mentionne jamais la collision, donc on
cherche ailleurs.

**3. La passerelle n'essayait qu'un port** (7497, TWS papier). Sur un TWS réel
seul — la configuration de ce terminal — elle ne se connectait **jamais**, en
silence.

## Le correctif : un point unique de découverte

`ibkr_link` dit **où essayer** et **avec quel identifiant**. Il ne se connecte à
rien lui-même : sa sonde est de niveau TCP, elle ne parle pas le protocole IBKR,
n'ouvre aucune session, ne consomme aucun clientId — une sonde qui se
connecterait vraiment pourrait faire tomber le flux qu'elle vient vérifier.

- **un seul ordre de ports**, réel d'abord : `7496, 7497, 4001, 4002` ;
- **un identifiant par rôle**, tous distincts (la passerelle passe de 17 à 19) ;
- **le port qui a marché est partagé** : les flux suivants l'essaient en
  premier. Auparavant chacun repayait la découverte — TWS éteint, le worker
  options attendait 4 essais × 6 s = **24 s par job** ;
- **le souvenir est effacé** dès que plus aucun rôle n'y arrive : un souvenir
  qu'on ne remet jamais en question devient un mensonge le jour où l'on passe du
  papier au réel ;
- `IBKR_PORT`, s'il est défini, **passe devant sans supprimer les autres** — une
  variable oubliée dans un `.env` couperait sinon la connexion sans rien dire.

### Le verrou lecture seule n'a pas bougé de place

`readonly=True` reste écrit **sur chaque site d'appel**, à côté de `clientId=`,
là où `tests/test_no_orders.py` le cherche. Le déplacer dans `ibkr_link` aurait
rendu la protection invisible aux garde-fous : elle existerait encore, mais plus
rien ne la tiendrait. Un test dédié vérifie qu'elle est restée en place.

## Ce que l'écran dit maintenant

Avant : « Vérifier TWS/Gateway et le port IBKR » — soit demander à l'utilisateur
de vérifier ce que le produit sait déjà.

Après, mesuré sur un lancement réel (`DEMO=0`, sans TWS) :

```
port retenu   : None
ports essayes : [7496, 7497, 4001, 4002]
roles echec   : ['cotations', 'indices']
raison        : TWS / IB Gateway ne répond sur aucun des ports standards
                (7496, 7497, 4001, 4002). Vérifier que TWS est lancé et que
                l'API est activée (Configuration → API → Enable ActiveX and
                Socket Clients), avec 127.0.0.1 dans les adresses autorisées.
```

L'état est servi par `/api/system/diagnostics` sous `ibkr_link`.

**Une erreur de placement, trouvée en interrogeant l'endpoint** : la ligne avait
d'abord été greffée dans le bloc `if scheduler is not None:`, que l'appelant
n'atteint pas — elle n'était donc jamais exécutée. Une portée n'est pas une
sortie ; relire le code ne l'aurait pas montré.

## Le mode d'emploi, désormais

1. Lancer Vertex (`python terminal.py`). Il démarre **sans TWS**, sans erreur.
2. Lancer TWS ou IB Gateway, API activée, Read-Only API cochée.
3. Ne rien faire d'autre. Les flux réessaient toutes les 20 s : la connexion
   s'établit **sans redémarrer Vertex**, sur le port trouvé, quel qu'il soit.

Aucune variable d'environnement n'est nécessaire. `IBKR_HOST` et `IBKR_PORT`
restent respectés pour les montages inhabituels (TWS sur une autre machine).

## Ce qui est prouvé, et ce qui ne l'est pas

**Prouvé sans TWS** : l'ordre unique, l'unicité des identifiants, le partage du
port trouvé, l'oubli à l'échec, la priorité d'`IBKR_PORT` sans exclusion des
autres, l'absence de session ouverte par la sonde (contrôlé à l'AST — la
docstring du module cite `clientId`, un contrôle textuel interdirait d'expliquer
ce qu'on garde), et la découverte **contre un vrai socket** ouvert sur 4002.

**Non prouvé** : la poignée de main IBKR elle-même. Le socket répond, le
protocole n'est pas parlé. C'est G5, et G5 reste vide tant que
`tools/vertex_1_0/mesurer_g5_live.py` n'a pas tourné contre un vrai TWS.

## Une régression que j'ai introduite, et que le gardien a trouvée

En recâblant la passerelle, j'avais écrit `self._ib, self.port = ib, port`.
`tools/mesurer_surface_ibkr.py` dérive les porteurs d'objet `IB` en suivant les
**alias** (`self._ib = ib`) ; écrite en tuple, l'affectation n'est plus reconnue
et **tous les appels passant par `self._ib` deviennent invisibles à la liste
blanche lecture seule**. Le gardien a échoué avec le bon message. C'est le code
qui a été corrigé, pas lui — deux affectations simples, et un commentaire pour
que le prochain ne refasse pas le geste.

Ce gardien-là vit sur la ligne Signal OS et **n'est pas sur cette branche** :
c'est en y passant par accident (conteneur réinitialisé) qu'il a attrapé la
faute. Sur la branche de release, rien ne l'aurait vue — ce qui donne une valeur
concrète à la décision de fusion déjà consignée dans `RAPPORT-FINAL.md`.

## Un défaut d'instrument que seul le mode réel révélait

Lancer en `DEMO=0` sans TWS met les pages dans un état qu'aucune mesure n'avait
encore vu : le **squelette de chargement reste à l'écran**. La sonde de
débordement a alors signalé `.vx-skeleton` sur `/options` — 655 px de contenu
dans une boîte de 366.

C'était l'instrument, pour la huitième fois. Le squelette est **vide** ; son
débordement vient du reflet `::after` qui balaie en `transform:translateX(100%)`
— en fin d'animation son bord droit est à deux fois la largeur de la boîte. Le
`overflow:hidden` est là exactement pour le rogner. Aucun contenu n'est caché,
puisqu'il n'y en a pas.

Critère ajouté, et il reste honnête : **une troncature suppose du contenu à
tronquer**. Un conteneur sans texte ni enfant ne peut rien cacher. Deux
mutations le tiennent — retirer l'atténuation fait crier le témoin (le squelette
redevient un « défaut »), l'élargir à tout conteneur aveugle la vraie coupe. Le
squelette figure désormais dans la page témoin **négative**, à côté du
conteneur `overflow-x:auto` : deux motifs sains qu'on ne doit pas confondre avec
un défaut.

## Vérification

- `python -m compileall -q terminal.py vertex` → 0
- `python -m pytest tests/ -q` → **3 487 passed**
- Lancement réel `DEMO=0` sans TWS : `/healthz` 200, aucune erreur, diagnostic
  actionnable.
- Garde-fous de sûreté verts : `test_no_orders`, `test_ibkr_honesty`,
  `test_ibkr_timeout_lot216`, `test_strategy_os_final_guards`, `test_data_sources`.
