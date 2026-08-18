# SIGNAL OS · LOT 55 — L'INSTRUMENT QUI S'ÉTAIT TROMPÉ TROIS FOIS, REMPLACÉ

Branche : `agent/vertex-signal-os-v1` · SW **v239, inchangé** (aucun octet servi
touché) · Suite **3 454 passed** (3 442 → +12)

Le rapport 54 laissait une réserve explicite : *« `tools/mesurer_moteurs_muets.py`
porte encore la méthode fautive. S'y fier de nouveau reproduirait l'erreur. »*
Ce lot la paie — et la paie en remplaçant l'instrument, pas en le rafistolant.

---

## 1. Pourquoi un rafistolage n'aurait pas suffi

L'ancienne sonde cherchait la chaîne `"nom_du_module"` dans le corps des
réponses servies. Cela ne dit la vérité **que si** un moteur publie sous une clé
portant son nom de fichier. Mesuré, la plupart ne le font pas :

| moteur | ce qu'il publie réellement |
| --- | --- |
| `drawdown_context` | `contexts.drawdown` |
| `decision_readiness` | `decision.readiness` |
| `historical_stress` | `stress_test` |
| `walk_forward_validation` | **le corps entier** de `/api/skyler/validation` |
| `option_cohort` | **le corps entier** de `/api/tracking/options/cohort` |

Les deux derniers sont le cas décisif : **un corps de réponse ne se nomme jamais
lui-même.** Aucun réglage de la recherche ne pouvait les trouver — d'où un
remplacement plutôt qu'un correctif.

## 2. La méthode juste : remonter la chaîne réelle

`tools/mesurer_moteurs_par_appelant.py` suit **appelant → clé reçue → route →
écran**, par analyse AST :

1. imports d'un moteur et appels correspondants ;
2. ce qui **reçoit** l'appel — clé de dictionnaire, ou variable rendue par
   `jsonify(...)`, donc corps entier ;
3. le décorateur `@route(...)` de la fonction englobante ;
4. la clé est-elle lue dans `vertex/ui/**` ou le JS servi ?

Et, pour les cas que l'AST ne peut pas trancher seul, une **résolution contre le
produit vivant** : la structure propose des candidats, le serveur décide. C'est
la différence entre deviner et mesurer.

---

## 3. L'inventaire mesuré

87 moteurs (`engines`, `market`, `portfolio`, `tracking`), témoin 6/6 :

| famille | nombre |
| --- | --- |
| **peints** — la clé est lue | **22** |
| **muets** — la sortie atteint une route, rien ne la lit | ~~**11**~~ → **3**, corrigé au lot 57 |
| **indéterminés** — la variable poursuit son chemin, l'AST ne suit pas | 27 |
| **indirects** — appelés par un autre moteur, sortent sous SA clé | 24 |
| **sans appelant trouvé** | 10 |

> ⚠ **CORRIGÉ AU LOT 57 — sept de ces onze étaient peints.** Cet outil demandait
> « la clé est-elle lue ? » à des moteurs qui **servent le corps entier** d'une
> route et n'en publient donc aucune : la réponse était non *par construction*.
> `anomaly`, `evidence_lab`, `decision_stack`, `session_digest`,
> `skyler_journal`, `multileg_lab` et `performance` sont demandés par
> l'interface, route comprise. Septième fois que cette famille de faute revient,
> et cette fois **dans l'outil écrit pour corriger les six précédentes**. La
> bonne question, pour un moteur sans clé, est : *l'écran demande-t-il cette
> route ?* Détail et inventaire corrigé : `SIGNAL-OS-57-CREDIBILITE.md` §1.

Les onze muets, nommés, parce que c'est le gisement :

```text
anomaly                  /api/anomalies/<sym>              corps entier
decision_stack           /api/decision/<sym>               corps entier
evidence_lab             /api/evidence/<sym>               corps entier
intelligence_monitor     /api/skyler/monitor               corps entier
multileg_lab             /api/options/strategies/<sym>     corps entier
performance              /api/tracking/<id>/performance    corps entier
recommendation           /api/position-decision/<sym>      corps entier
red_team                 /api/skyler/<sym>                 decision.red_team
session_digest           /api/session/digest               corps entier
skyler_journal           /api/skyler/calibration           corps entier
walk_forward_validation  /api/skyler/validation            corps entier
```

`red_team` mérite d'être signalé : il répond aujourd'hui, sur `ACN`, *« revue
red-team 10/10 questions fondées sur les données réelles — COMPLÈTE »*, et
**personne ne le lit**. Une revue adversariale de la décision, calculée et
jamais montrée, est exactement ce qu'un opérateur voudrait voir.

---

## 4. Trois corrections trouvées en construisant l'instrument — toutes du même genre

Chacune est un cas où **j'ai pris ma convention pour la structure**.

**4.1 « Ne pas savoir » rangé avec « savoir que non ».** Le premier jet
classait MUET tout moteur dont l'AST ne retrouvait pas la clé. Or quand l'appel
est reçu par une variable intermédiaire (`pctx`, `ev`, `packet0`), l'outil ne
*sait pas* sous quelle clé elle ressort. Ces moteurs ont désormais leur propre
famille, et le chiffre des muets ne les gonfle plus.

**4.2 Un défaut d'ordre dans ma propre sonde.** L'ensemble « clés lues par
l'écran » était calculé **avant** la résolution contre le produit vivant : une
clé découverte à la résolution ne pouvait donc jamais y figurer.
`instrument_profile` — peint depuis le lot 49, confirmé au navigateur au lot 52
— ressortait MUET. Corrigé : l'écran est interrogé au moment du classement.

**4.3 Le plus gros fichier du produit n'était pas ouvert, et une forme d'import
sur deux était ignorée.** L'outil ne lisait que `vertex/app/routes/*.py`. Il
annonçait donc « 22 moteurs sans appelant », dont `track_record`, `committee` et
`scorecard` — tous importés par **`terminal.py`**. Et
`from vertex.market.daily_brief import build_daily_brief` lie la **fonction**,
pas le module : l'appel est `build_daily_brief(...)`, invisible à une détection
qui n'attendait que `module.fonction(...)`. `daily_brief` et `editorial`
passaient pour orphelins alors que `redesign.py` les appelle.

Effet mesuré des deux corrections : **57 → 66** moteurs appelés depuis une
route, et « sans appelant » **22 → 10**.

---

## 5. L'ancien outil est retiré, pas effacé

`tools/mesurer_moteurs_muets.py` ne mesure plus : il imprime pourquoi sa méthode
est fausse, nomme son remplaçant, et rend 2. Son texte d'origine est conservé —
il documente une leçon qui a coûté trois rapports, et l'effacer la ferait
oublier. Mais un instrument dont on sait la méthode fausse ne doit pas pouvoir
produire un quatrième inventaire crédible. Un test le vérifie.

---

## 6. Le gardien, et ses trois mutations

`tests/test_signal_os_chaine_moteurs_lot55.py` tient le **câblage du produit**,
pas l'outil pour lui-même : renommer `decision['readiness']` ou déplacer un
moteur hors de sa route casse un test qui dit lequel. La moitié AST ne demande
aucun serveur — elle tient donc en intégration continue.

| mutation | test qui tombe |
| --- | --- |
| clé servie renommée (`readiness` → `readiness_v2`) | le câblage figé |
| `jsonify(out)` passé par une variable intermédiaire | la détection « corps entier » |
| l'ancien outil remesure | le refus de mesurer |

La deuxième est la plus importante : elle garde vivante la capacité à voir la
famille de moteurs qui a produit trois inventaires faux.

---

## 7. Réserves

1. **27 moteurs restent « indéterminés ».** L'AST ne suit pas une variable
   au-delà de son affectation. Les trancher demande soit un suivi de flux, soit
   une lecture manuelle — travail réel, non fait ici.
2. **10 moteurs sans appelant trouvé.** « Trouvé » est le mot juste : un import
   dynamique, une indirection par attribut ou un appel construit resteraient
   invisibles. Ne pas conclure « code mort » sans vérification pièce par pièce.
3. **Onze moteurs muets non peints.** Ce lot les nomme, il n'en peint aucun.
   Ils vivent sur cinq pages différentes.
4. **La résolution contre le produit vivant utilise un seul titre** (`ACN`, mode
   démonstration). Un moteur dont la clé n'apparaît que dans un autre état du
   produit serait classé « indéterminé » plutôt que peint.
