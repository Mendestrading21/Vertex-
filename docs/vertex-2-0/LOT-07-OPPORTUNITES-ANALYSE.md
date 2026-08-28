# Lot 7 — Opportunités et Analyse

## Le défaut le plus grave de la refonte, trouvé sur une capture

Le dossier d'un titre — la page la plus importante du produit — **était
structurellement cassé**, et l'était avant cette refonte.

`<section id="an-hero">` était fermée par un **`</div>` orphelin**. Un navigateur
ignore une balise fermante qui ne correspond à rien : la section restait donc
ouverte, et **tout le dossier** — scores, physique, workspace, rail décisionnel —
s'imbriquait dans cette carte collante à bordure d'accent.

Le résultat était spectaculaire et invisible aux tests : cartes empilées les unes
sur les autres, colonnes réduites à **un mot par ligne**, texte se chevauchant.

Aucun contrôle ne l'attrapait :

- **0 débordement horizontal** — le contenu débordait *verticalement*, pas
  latéralement ;
- **0 erreur console** — un balisage mal fermé n'est pas une erreur JavaScript ;
- **0 bloc vide** — les blocs contenaient du texte, simplement illisible ;
- **4246 tests verts** — aucun ne rend la page dans un navigateur.

Il a fallu **regarder la capture**. C'est la seule raison pour laquelle ce lot a
commencé par une réparation.

Correction : `</div>` → `</section>`. Le marcheur de pile de balises confirme
qu'aucune balise ne reste ouverte.

## Le verdict canonique était calculé, puis jeté

`paintDecision()` faisait bien `$('an-verdict')` — mais **`#an-verdict` n'existait
dans aucune section**. Sur les 67 identifiants `an-*` déclarés, il n'y était pas.
La garde `if(V)` avalait donc silencieusement le rendu.

Mesuré au navigateur avant correction :

```
an-verdict présent   : False
.vx-verdict-card     : False
```

Le dossier passait de l'identité aux scénarios **sans jamais dire ce que Vertex
conclut**. Le renderer n'a pas été touché : on lui a rendu son domicile.

Deux bancs auraient dû l'attraper. `test_analysis_visual_lot619::test_analysis_dom_is_decision_first…`
est dans la liste des gardes supersédées ; `test_pages_opportunities_analysis_04`
assertait `'an-verdict' in src` — satisfait par un **commentaire** qui mentionnait
le nom.

Et la carte n'avait **aucun style** : ni `.vx-verdict-head`, ni `-label`, ni
`-score`, ni `-grid`, ni `-cell`, ni `.vx-insufficient`. Personne n'avait vu
l'habillage manquer, puisque la carte ne s'affichait jamais. D'où
« Données insuffisantesconfiance 0 » — trois éléments sans aucune règle
d'espacement. Habillée dans la couche 2.0, l'accent porté par un liseré gauche
piloté par `data-tone` : le verdict est la conclusion, il n'a pas besoin d'être
crié deux fois.

## Decision Trace sur le dossier — deuxième des cinq emplacements

`Donnée → Moteur → Décision → Portefeuille`, à `analyse-hero`.

Le serveur ne connaît ici que le symbole : il rend les quatre nœuds à `—` avec le
ton « missing », et `paintTrace()` les complète depuis la décision réellement
reçue. **Aucun nœud ne part sur une valeur optimiste.**

Le balisage vient de `vx2` ; le client n'écrit que du texte et un ton dans des
nœuds déjà rendus. Aucune valeur n'est dérivée côté client.

Dans l'état dégradé de cet environnement, il rend :

| Nœud | Valeur | Méta |
|---|---|---|
| Donnée | `—` | qualité C · démo |
| Moteur | 0/100 | confiance moteur |
| Décision | **Vertex ne tranche pas** | données insuffisantes |
| Portefeuille | Aucune position | rien à confronter |

## Opportunités — vocabulaire et provenance

**Trois libellés de sous-vue mentaient.** Les clés d'URL n'ont pas bougé — elles
sont en favori, dans des liens internes et dans plusieurs bancs. Seuls les
libellés changent :

| Avant | Après | Pourquoi |
|---|---|---|
| Screener | **Radar** | Jargon anglais dans un produit francophone ; c'est le nom du contrat. |
| Portefeuille | **Positions × moteur** | Se lisait comme un doublon de la page Portefeuille. La vue ne montre pas le portefeuille : elle **confronte** les positions déclarées aux verdicts du moteur. |
| Calendrier | **Catalyseurs** | Se lisait comme un doublon de la page Calendrier depuis le lot 2. Cette vue montre les catalyseurs des dossiers suivis. |

**`#op-fresh` était un emplacement de fraîcheur mort** — déclaré dans l'en-tête,
rempli par personne. La page n'affichait donc ni source, ni horodatage, ni
univers, y compris quand elle disait « aucun titre scanné » : l'utilisateur ne
pouvait pas savoir si la cause venait de la source, du scan ou du rendu.

Remplacé par une **ContextBar** — Univers · Dernier scan · Source · Fraîcheur —
peinte par les **cinq** sous-vues. Une barre de contexte qui n'apparaîtrait que
sur une sous-vue laisserait les quatre autres sans provenance.

L'état vide porte désormais sa cause et une action sûre vers Système → Données.

## Un gardien élargi, et vérifié

`test_etats_vides_bureau_lot608` tient une exigence précise : une zone alimentée
par un **moteur** ne doit jamais imputer son vide au **bureau**. Il ne
reconnaissait que `VX.states.empty*`. Les zones refondues écrivent un bloc
`vx2-state` — parce qu'elles portent en plus une cause et une action, que
`VX.states.empty` ne sait pas rendre.

Le gardien reconnaît désormais les deux mécanismes. **Contre-épreuve exécutée** :
un bloc 2.0 qui parlerait de synchro du bureau ressort toujours comme `emptyDesk`,
donc en faute. L'exigence est intacte.

## Preuves

| Élément | Résultat |
|---|---|
| `python -m pytest -q` | **4246 passés**, 154 ignorés, 1 échec environnemental connu |
| Structure du dossier | marcheur de pile : **aucune balise ouverte** |
| `#an-verdict` au runtime | présent, rendu, stylé |
| ContextBar | peinte par les 5 sous-vues d'Opportunités |
| Blocs vides | **0** sur 13 routes |
| Accessibilité | **0 défaut** sur 12 pages × 2 viewports |
| Console | 0 erreur page |

Service worker `v227` → **`v228`**.

## Limites

- Les sous-vues **Actions** et **ETF** du contrat n'ont pas été créées : le
  screener porte déjà un filtre « véhicule », et en faire des onglets exigerait de
  toucher sa logique de filtrage. Consigné pour un lot ultérieur.
- L'entonnoir de détection existe (`/api/opportunities/funnel`, 7 étages) et est
  branché, mais reste invisible faute de données scannées dans cet environnement.
