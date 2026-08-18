# SIGNAL OS · LOT 58 — L'INVENTAIRE FERMÉ, ET TROIS VERDICTS PLUTÔT QUE TROIS CHANTIERS

Branche : `agent/vertex-signal-os-v1` · SW **v241, inchangé** (aucun octet servi
touché) · Suite **3 476 passed** (3 470 → +6)

---

## 1. Le brouillard levé : trente « indéterminés » → quatorze

L'instrument laissait 30 moteurs dont l'AST voyait l'appel mais pas la clé de
sortie. Trois sauts structurels, bornés, jamais devinés, en résolvent la moitié :

| forme dans le code | clé déduite |
| --- | --- |
| `build_packet(events=ev)` — argument nommé | `events` |
| `{'paths': paths}` — littéral de dictionnaire | `paths` |
| `jsonify(moteur.build(...))` — appel **non affecté** | corps entier |
| `jsonify({'risque': moteur.f(...)})` — appel non affecté | `risque` |

Le dernier cas concernait **quatorze moteurs sur trente** : leur appel n'est
affecté à aucune variable, et je rangeais « indéterminé » ce que l'arbre disait
tout haut. Chaque candidat reste confronté au produit vivant — la structure
propose, le serveur décide.

**Et deux angles morts levés d'un coup** en interrogeant **la route du moteur**
plutôt qu'une seule : `build_packet(...)` publie dans `packet.events`, pas dans
`packet.contexts` que seul je regardais ; et `knowledge_graph` sort sur
`/api/skyler/graph/<sym>`, que `/api/skyler/ACN` ne pouvait évidemment pas
contenir.

### L'inventaire, sur 87 moteurs

| famille | lot 55 | lot 57 | **lot 58** |
| --- | --- | --- | --- |
| peints | 22 | 35 | **49** |
| muets | 11 (→ 3) | 1 | **3** |
| indéterminés | 27 | 30 | **14** |
| indirects | — | 11 | 11 |
| sans appelant trouvé | 10 | 10 | 10 |

Les trois muets remontent de 1 à 3 parce que la nouvelle résolution **découvre**
deux routes servies que personne ne demande : ce n'est pas une régression, c'est
la fin d'un angle mort.

---

## 2. Les trois muets ne sont pas trois chantiers

Mesuré un par un. **Aucun ne demande d'être peint tel quel** — et c'est un
résultat, pas une dérobade.

**`recommendation` → `/api/position-decision/<sym>`.** Recoupe la carte-verdict
du Portefeuille. Le peindre ailleurs créerait un **second domicile pour la même
donnée**, ce que l'invariant « une donnée = un seul domicile » interdit.

**`legacy_basket_risk` → `/api/risk`.** Le nom dit vrai : **superseded**. Tout ce
qu'il calcule a déjà un domicile canonique dans `/api/portfolio/context` —
`hhi`, `correlations`, `sector_mix`, `bounds`, et `in_bounds` qui porte le même
sens que son `no_new_risk`. Le peindre dupliquerait le risque de panier. Sa
retraite est une décision humaine : supprimer une route servie touche tout ce
qui pourrait l'appeler.

**`options_lab` → `/api/options-lab`.** Riche — contexte marché, secteur,
entreprise, plan, comparateur, recherche. Et **26 emoji littéraux** dans le
moteur (`🌍 🏭 🚀 🛑 …`), servis dans les champs `icon`. La règle mesurée aux
lots 41/47/48 est *zéro emoji peint*. Tant que la route n'est pas consommée,
aucune violation ; le jour où quelqu'un la peint sans filtrer, il en injecte des
dizaines d'un coup. Un test tient l'**alternative** : ou bien la route n'est pas
demandée, ou bien le moteur ne porte plus d'emoji.

---

## 3. Trois fautes d'instrument, dont deux trouvées par mutation

**3.1 Un état que le produit ne peut pas atteindre — deux fois de suite.** Le
test qui prouve que le risque de panier a un domicile canonique interrogeait
`/api/portfolio/context` sur un desk vide. La route répondait, **correctement**,
`available: false — aucune position réelle déclarée`, sans aucune clé de risque.
Je concluais à une régression en mesurant un état sain. Trois positions semées —
et la route répondait encore `valeur totale nulle — poids incalculables` : les
poids viennent de `scan_state['detail']`, pas du desk. **Deux portes, pas une.**
C'est la faute du lot 38, payée pour la sixième fois de la série.

**3.2 Le cinquième gardien creux, trouvé par mutation.** Le test des emoji lisait
la **charge** renvoyée par le client de test. Celui-ci répond `empty: true` —
aucune donnée de scan, donc **aucun emoji**. Le test passait même en simulant une
page qui peint la route. Corrigé : les emoji sont des **littéraux du moteur**,
fait de structure stable quel que soit l'état des données.

**3.3 Un gardien du dépôt m'a accusé, et il avait raison.**
`tests/test_desk_ecritures_lot387.py` protège les **données personnelles** de
l'utilisateur : aucun test ne doit écrire dans le vrai `desk_data.json`. Mon
fichier en écrit un (il sème des positions). Ma redirection était réelle mais
**invisible** : j'affectais `persist._BASE_DIR` directement, alors que le gardien
reconnaît la forme `setattr(persist, '_BASE_DIR', …)` — convention suivie par
douze fichiers. Je me suis conformé à la convention plutôt que d'élargir le
gardien ou de réclamer une exemption : *une règle qu'un gardien ne peut pas
vérifier ne protège plus rien.*

---

## 4. Réserves

1. **14 moteurs restent indéterminés.** Leur variable traverse plusieurs
   affectations, ou l'appel vit hors d'une route (`via _scan_once`). Les
   trancher demande un suivi de flux, pas un saut de plus.
2. **10 sans appelant trouvé** — « trouvé » reste le mot juste : un import
   dynamique resterait invisible. Ne pas conclure « code mort » sans vérifier
   pièce par pièce.
3. **La retraite de `legacy_basket_risk` n'est pas faite.** Supprimer une route
   servie est une action à effet externe : elle appartient à une décision
   humaine, pas à ce lot.
4. **Le verdict sur `recommendation` est une lecture de conception**, appuyée sur
   la comparaison des sorties — pas sur une preuve formelle que les deux disent
   exactement la même chose.
