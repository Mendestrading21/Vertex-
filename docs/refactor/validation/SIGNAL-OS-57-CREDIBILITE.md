# SIGNAL OS · LOT 57 — LA CRÉDIBILITÉ DU MOTEUR, ET SEPT ACCUSATIONS RETIRÉES

Branche : `agent/vertex-signal-os-v1` · SW **v240 → v241** · Suite **3 470 passed**
(3 459 → +11)

---

## 1. D'abord la correction, parce qu'elle change la taille du chantier

L'instrument du lot 55 — celui que je venais de livrer comme **le fiable** —
annonçait **onze moteurs muets**. Sept l'étaient à tort.

Il demandait « la clé est-elle lue par l'écran ? » à des moteurs qui **servent le
corps entier** d'une route et n'en publient donc **aucune**. La réponse était non
**par construction**, pour tous, toujours.

| moteur accusé | route que l'interface demande réellement |
| --- | --- |
| `anomaly` | `/api/anomalies/<sym>` |
| `evidence_lab` | `/api/evidence/<sym>` |
| `decision_stack` | `/api/decision/<sym>` |
| `session_digest` | `/api/session/digest` |
| `skyler_journal` | `/api/skyler/calibration` |
| `multileg_lab` | `/api/options/strategies/<sym>` |
| `performance` | `/api/tracking/<id>/performance` |

Septième fois que cette faute se présente dans la série, et la plus embarrassante
des sept : elle vivait dans l'outil écrit *pour corriger les six précédentes*.
La bonne question, pour un moteur sans clé, n'est pas « la clé est-elle lue ? »
mais **« l'écran demande-t-il cette route ? »**.

**Muets réels : trois.** `intelligence_monitor`, `recommendation`,
`walk_forward_validation`. Deux sont peints par ce lot.

---

## 2. Ce que ce lot peint : la crédibilité du moteur

`/api/skyler/validation` (validation walk-forward de la mémoire) et
`/api/skyler/monitor` (dérive de performance) répondent à la question qui
**précède** toute confiance dans un verdict : *ce moteur a-t-il été éprouvé, et
tient-il encore ?* Aucun fichier de l'interface ne demandait ces deux routes.

Ils vivent désormais sur Système, sous une carte « Crédibilité du moteur »,
voisine de la carte « Moteurs » — celle-ci répond « les moteurs tournent-ils ? »,
la nouvelle répond « leurs verdicts passés ont-ils tenu ? ». Deux questions
différentes, longtemps confondues faute d'affichage.

### Le point d'honnêteté, et c'est lui que le lot défend

Les deux répondent aujourd'hui `INSUFFICIENT_SAMPLE` :

```text
Validation walk-forward
échantillon insuffisant — aucune conclusion
60 séance(s) datée(s) requise(s) ; 0 disponible(s) · progression 0/60

Dérive de performance
échantillon insuffisant — aucune conclusion
30 résultats mesurés requis ; 0 disponible(s)

Diagnostics descriptifs, en lecture seule. Un échantillon insuffisant n'est ni une
validation ni un échec : c'est l'absence de conclusion, et aucun chiffre n'est
extrapolé pour la combler.
```

Un échantillon insuffisant n'est **ni** une validation **ni** un échec. En vert,
cela se lirait « validé » ; en rouge, « le moteur est cassé ». Les deux seraient
faux. D'où un état **neutre**, la raison chiffrée du moteur affichée telle
quelle, et la phrase qui l'énonce en toutes lettres.

C'est aussi la réponse honnête à la question que pose tout ce chantier : **non,
les verdicts de Skyler ne sont pas encore validés hors échantillon — et voici
exactement ce qu'il manque pour qu'ils puissent l'être** (60 séances datées).

---

## 3. Vérifié au navigateur, et un défaut de rendu corrigé à la vue

Bloc présent, 118 px, zéro erreur JS. Mais le premier rendu affichait :

```text
60 séance(s) datée(s) requise(s) ; 0 disponible(s) · 0/60 séance(s) datée(s)
```

Le compte **répétait la raison** mot pour mot. Corrigé à la vue : la raison dit
la phrase, le ratio (`progression 0/60`) montre la distance au seuil sans la
redire. Ce genre de défaut ne se voit pas dans un test — il se voit à l'écran.

---

## 4. Le gardien, et le quatrième gardien creux de la série

Trois mutations, chacune attrapée par un seul test : site d'appel retiré, état
« insuffisant » peint en vert, raison du moteur masquée.

**La première a d'abord passé.** Mon test cherchait `'loadCredibilite()'` dans
les octets servis — chaîne qui est **incluse dans la définition elle-même**,
`async function loadCredibilite(){`. Supprimer l'appel laissait les onze tests
verts. Quatrième gardien creux de la série, tous du même genre : *une
sous-chaîne qui existe ailleurs*. Il exige désormais l'enchaînement réel
`loadConnections();loadCredibilite();`.

Un cinquième test fige la correction du §1 : les sept moteurs sans clé sont
peints **par leur route**, et le test tient ce fait — pour qu'on ne refasse pas
le compte faux.

---

## 5. État du chantier des moteurs

| famille | lot 55 (annoncé) | lot 57 (mesuré) |
| --- | --- | --- |
| peints | 22 | **35** |
| muets | 11 | **1** |
| indéterminés | 27 | 30 |
| indirects | — | 11 |
| sans appelant trouvé | 10 | 10 |

(Les 35 peints incluent les sept rendus à tort muets au §1 et les deux ajoutés
par ce lot ; le reste de l'écart vient des corrections de nommage du lot 55.
Chiffres relevés par l'outil, pas estimés.)

Il reste **un** moteur réellement muet : `recommendation`
(`/api/position-decision/<sym>`), dont la sortie recoupe la carte-verdict du
Portefeuille — à trancher avant de peindre, sous peine de créer un second
domicile pour la même donnée.

---

## 6. Réserves

1. **`intelligence_monitor` et `walk_forward_validation` sont peints dans leur
   état d'indisponibilité seulement.** Le mode démonstration n'a pas d'historique
   daté ; leur chemin nominal (`OK`, `DRIFT`) n'a jamais été affiché. Les
   libellés existent et sont testés dans les octets, pas au pixel.
2. **Une seule vue, une seule largeur** : `/system?view=connections`, 1440 px.
3. **Le dernier muet n'est pas traité** (§5) : c'est une question de conception,
   pas de câblage.
4. **Les 30 « indéterminés » restent** — l'AST ne suit pas une variable au-delà
   de son affectation.
