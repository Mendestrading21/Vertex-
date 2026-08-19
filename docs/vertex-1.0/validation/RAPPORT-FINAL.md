# Vertex 1.0 — Rapport final

État à la fin de la campagne autonome. Ce document dit ce qui est **mesuré**, ce
qui reste **ouvert**, et pourquoi le verdict n'est pas GO.

---

## 1. Verdict

> **NO-GO pour `v1.0.0`. RC constituée : un SHA candidat existe et il est vert.**

Une seule raison subsiste, et ce n'est pas un jugement de qualité :

**G5 est intestable ici.** Il demande un TWS / IB Gateway réel — connexion,
reconnexion, market data, chaîne d'options, portefeuille, erreurs. Aucun
environnement de cette campagne n'en dispose. `HUMAN_REQUIRED`, bloquant.

Le second blocage — *« aucun SHA ne porte les huit chantiers »* — **a été levé**.
Les trois chantiers orphelins (`wmb`, `domaines`, `persistance`) fusionnent
**sans conflit** dans la chaîne principale :

```text
main ─ d52a39d ─ runtime ─ memoire ─ moteurs ─ qa ─ design
                     └─────────── + persistance + domaines + wmb
                                  = integration/vertex-1-0-rc   (SHA candidat)
```

Suite complète sur ce SHA : **3 422 passed**. Une fusion propre au niveau du
texte ne prouvant rien, le SHA a été éprouvé : compilation, suite entière,
balayage navigateur des huit espaces, modes dégradés et exploitation.

Le tag n'est **pas** créé. La consigne « ne crée PAS le tag `v1.0.0` tant qu'un
gate critique manque » est respectée : G5 manque.

---

## 2. Architecture finale

**Le monolithe n'est plus le centre.**

```text
terminal.py        7 276 → 6 789 lignes
routes LEGACY         14 → 0        (il ne sert plus AUCUNE route)
blueprints            21 → 7
stores                11 → 2
```

`terminal.py` héberge encore les boucles de fond qui remplissent `scan_state` —
c'est pourquoi il reste une **surface servie** au sens de l'audit des moteurs,
même sans déclarer de route. Cette subtilité a invalidé une première version de
l'instrument.

**Propriétaires modulaires** (les quatre de G1) :

| responsabilité | propriétaire |
| --- | --- |
| fabrique Flask | `vertex/app/factory.py` — 21 blueprints, 7 à injection |
| démarrage unique | `vertex/app/lifecycle.py` |
| routes | `vertex/app/routes/*` (7 modules ajoutés) |
| planification | `vertex/scheduler/registry.py` |

Plus `vertex/app/{ibkr_state,rescan_gate,weekly_selection,caches,state}.py`,
`vertex/options/pack.py`, `vertex/data/descriptions_fr.py`.

**Moteurs** : 59 recensés, **58 atteints ET appelés** depuis une surface servie.
Un seul isolé — `performance_ledger` (124 lignes), importé par trois fichiers de
tests et par rien d'autre.

**Interface** : 8 espaces canoniques (`vertex/ui/shell/PRIMARY_NAV`), 17
feuilles CSS (152 Ko), **toutes servies sur les huit**.

---

## 3. Preuves

Toutes mesurées **sur le SHA candidat** `integration/vertex-1-0-rc`.

```text
pytest tests/ -q       3 422 passed
compileall             exit 0
/healthz               200
/api/client-log        count: 0
8 espaces × 3 largeurs 24 relevés — 0 débordement, 0 anneau manquant,
                       0 contraste sous AA, 0 erreur JS
18 surfaces servies    0 fuite de secret, 0 verbe d'ordre,
                       0 anomalie de fraîcheur, 0 fabrication (ticker inconnu)
exploitation (G6)      aller-retour de sauvegarde fidèle, rétention 7 j,
                       10 dépendances déclarées et bornées, `main` intacte
```

Repères d'écart : `agent/vertex-1-0-design` seule donnait **3 382** ; la fusion
des trois chantiers orphelins a porté le total à **3 408** ; le gardien G6
ajouté ensuite le porte à **3 422**.

---

## 4. Défauts trouvés et corrigés

Chacun était **invisible sous une suite verte**.

| # | défaut | comment il se cachait |
| --- | --- | --- |
| 1 | les boucles de fond démarraient **en double** | aucun test ne comptait les démarrages |
| 2 | **18 des 27** automatisations déclarées n'avaient aucun émetteur | l'écran disait « jamais exécuté » — le même mot pour un job en panne et un job inexistant — et un pied de page *expliquait* ce silence par des « intégrations absentes », faux pour 18 lignes |
| 3 | un push de bureau **effaçait** ce qu'il n'envoyait pas | un `data: {}` était accepté : la validation portait sur le type, pas le contenu |
| 4 | le moteur **ne se notait jamais** | `_fwd` cherchait un libellé `'%m-%d'` dans des dates ISO → `resolved: 0` toujours, sous un test vert dont la fixture employait un format que le produit ne produit pas |
| 5 | les cartes d'indices **coupaient leur en-tête** | 198 px dans 143, sous `overflow-x:hidden`, sans ellipse ni barre |
| 6 | le fil d'Ariane était **illisible en mobile** | 84 px pour 122-185 px sur 7 espaces sur 8 ; séparateur réduit à 2 px |
| 7 | son segment d'espace mesurait **19,5 px** de haut | seule cible tactile du produit sous le plancher de 32 px |
| 8 | `requests` et `markupsafe` importés **fermement mais non déclarés** | ils arrivaient comme dépendances *transitives* — rien ne casse tant que l'intermédiaire ne change pas. `markupsafe` sert à l'**échappement HTML** : une primitive de sûreté adossée à un pari qu'on ne sait pas qu'on a pris |

---

## 5. Ce que cette campagne a appris (et qui vaut au-delà)

**L'instrument a été faux avant le produit — quatre fois.** À chaque fois il
aurait été plus rapide de « corriger » le produit :

1. **136 débordements** inexistants — la sonde comparait chaque élément à
   `window.innerWidth` et signalait les panneaux **garés** hors-écran
   (`aria-hidden`, `inert`). Mesure : `scrollWidth == clientWidth` partout.
2. **34 contrastes faibles** sur le bouton primaire — la remontée du fond ne
   lisait que `backgroundColor`, nul sur un `linear-gradient` : ~7:1 lu 1,04:1.
3. **113 cibles tactiles trop petites** — le produit s'est donné **deux** seuils
   (40 primaire / 32 secondaire, lot 612) ; en imposer un seul revenait à
   l'accuser d'une décision prise exprès.
4. **5 cibles trop étroites** — symptôme, pas défaut : le lien était étroit
   *parce que son conteneur l'était*. L'élargir aurait soigné le thermomètre.

**Un témoin doit vivre au bord du seuil qu'il défend.** `#888` sur `#777`, c'est
1,3:1 — ça survit à n'importe quel assouplissement. La mutation « seuil AA à
1,5:1 » passait donc. Corrigé par un témoin à **3,50:1**.

**Un témoin qui éprouve une copie du code mesuré ne prouve rien.** Les témoins
posaient leur propre écouteur `pageerror` : supprimer celui du balayage les
laissait tous verts pendant que la mesure devenait aveugle.

**Une liste d'exceptions de gardien est l'endroit par où l'invariant s'érode.**
Écrire les 7 verbes d'ordre en clair faisait échouer deux gardiens maison. Ils
ont raison : la liste est assemblée à l'exécution, aucune exception ajoutée.

**Mesurer avant de choisir la correction.** J'allais masquer le sous-libellé du
fil d'Ariane. Les `h1` mesurés disent l'inverse : le nom d'espace est répété à
l'identique sur les huit, le sous-libellé n'existe nulle part ailleurs.

**Un outil ne voit pas qu'on l'a aveuglé quand il n'y a rien à voir.** Sur les
neuf mutations de l'instrument G6, les trois qui portaient sur ses propres
détecteurs passaient toutes : sur un produit sain, neutraliser un détecteur
laisse le compteur à zéro — avant comme après. La parade n'est pas de mieux
compter, c'est de rendre le détecteur **éprouvable** : comparaison extraite en
fonction pure, classification rendue injectable, de sorte qu'un témoin puisse
leur présenter un cas fabriqué. Les trois mordent désormais (9/9).

**Ce que la docstring promet, le code doit le faire.** L'instrument G6 annonçait
vérifier les dépendances « dans les deux sens » ; il n'en faisait qu'un. Le
second sens — importé mais non déclaré — est celui qui a trouvé le défaut.

**Un seuil peut reposer sur une coïncidence.** Mon gardien des branches exigeait
« au moins 3 classes non vides ». Deux seulement sont structurellement
atteignables dans sa configuration rapide ; la troisième tenait à **une** branche
dont le diff avec `main` était vide. Un clone ne la portant pas (693 refs au lieu
de 697) faisait échouer le test sans qu'aucun code n'ait changé. Le test vérifie
désormais la propriété qui guide vraiment la décision — la séparation entre
« perte prouvée nulle » et « porte du travail », aucune des deux n'avalant tout.

---

## 6. Sûreté — invariants vérifiés

- **Analyse uniquement.** `READONLY` / `ANALYSIS_ONLY` intacts.
- **Aucun chemin d'ordre**, et désormais vérifié sur les **octets servis** :
  7 verbes d'exécution cherchés sur 18 surfaces, 0 trouvé.
- **Aucune donnée inventée.** Sur un ticker inexistant : `verdict: null`,
  `REFUS_WATCH`, 6 blocs `INSUFFICIENT`, `confidence 0.0`, calibration
  « facteur plafonné à 0,50, **jamais inventé** ».
- **Fraîcheur honnête.** Aucun domaine hors ligne ne porte `age_s = 0` — donc
  aucun n'affiche « à l'instant » sur du vide.
- **Aucun secret servi** (valeurs `.env`/`.vertex_secret` + motifs compte IBKR,
  clés d'API, clé privée). Le rapport ne recopie jamais ce qu'il trouve.
- **Surface IBKR** : liste blanche mesurée à l'AST, 22 capacités, toutes en
  lecture.
- **Aucun hard gate contourné**, aucun moteur remplacé par Claude.

---

## 7. Gates

Mesurés sur le SHA candidat `integration/vertex-1-0-rc`.

| gate | état | ce qui manque |
| --- | --- | --- |
| G0 Fondation | **PASS** (au merge `bf49f9b`) | — |
| G1 Runtime modulaire | **preuves complètes** | acceptation humaine |
| G2 Données et domaines | **partiel** | persistance prouvée de bout en bout ; convergence des doublons non close |
| G3 Intelligence | **partiel** | mémoire réparée, WMB versionné ; **spécimen WMB réel** manquant |
| G4 Expérience | **preuves complètes** | résidu assumé : 2 fils tronqués de ~12 px |
| G5 Live read-only | **HUMAN_REQUIRED** | TWS / IB Gateway réel — **bloquant** |
| G6 Exploitation | **preuves complètes** | rollback applicatif et CVE non couverts (voir §8) |
| G7 Release | **NO** | G5, plus l'acceptation humaine du SHA |

---

## 8. Dette technique et décisions humaines

**Dette mesurée, aucune action unilatérale prise :**

- **476 règles CSS sur 1 025** jamais appariées au chargement — *candidates*,
  pas une preuve : une règle d'état ne peut pas s'apparier au relevé.
  `CLEANUP_POLICY.md` demande une preuve de non-usage.
- **`neon-glass.css` = 35,5 %** des 152 Ko de CSS servis.
- **`performance_ledger`** — 124 lignes, atteint par les seuls tests.
- **697 branches distantes classées**, aucune supprimée : 31 fusionnées,
  1 au contenu identique, 51 contenues ailleurs, **614 uniques**. La série
  Skyler n'est **pas** une chaîne linéaire (vérifié : `lot-100` n'est pas un
  ancêtre de `lot-101`) — il n'y a pas de collapse facile.
- **2 fils d'Ariane** tronquent encore de ~12 px, gelés dans un recensement.
- **Rollback applicatif non testé** : revenir à un SHA antérieur et démarrer
  demanderait un second arbre de travail. Ce qui *est* prouvé : la rotation
  garde 7 jours et la restauration rend l'état d'origine à l'identique.
- **Vulnérabilités connues des dépendances non recherchées** : il faudrait une
  base de CVE à jour, absente de cet environnement.

**HUMAN_REQUIRED :**

1. **TWS / IB Gateway réel** — G5, bloquant pour toute release.
2. **Spécimen de brief WMB réel** — G3.
3. **Autorisation de suppression de branches** — 32 sont prouvées sans perte.
4. **Acceptation du SHA candidat** `integration/vertex-1-0-rc`, et décision
   d'ordre de fusion vers `main` (l'intégration est faite et verte ; la fusion
   dans `main` demande un accord explicite).
5. **Décision `performance_ledger`** : le brancher ou le retirer.

---

## 9. Branches et PR

Huit PR brouillon ouvertes vers `main`, aucune fusion automatique :

| PR | chantier | branche |
| --- | --- | --- |
| #785 | #779 runtime modulaire | `agent/vertex-1-0-runtime` |
| #786 | #780 adapter WMB | `agent/vertex-1-0-wmb` |
| #787 | #783 carte des domaines | `agent/vertex-1-0-domaines` |
| #788 | #783 persistance du bureau | `agent/vertex-1-0-persistance` |
| #789 | #783 mémoire / track record | `agent/vertex-1-0-memoire` |
| #790 | audit moteurs + branches #782 | `agent/vertex-1-0-moteurs` |
| #791 | QA G4 | `agent/vertex-1-0-qa` |
| #792 | #781 couche visuelle | `agent/vertex-1-0-design` |
| #793 | intégration RC + G6 exploitation | `integration/vertex-1-0-rc` |

La dernière **contient les huit autres** : c'est le SHA candidat. Les huit PR de
chantier restent ouvertes séparément — elles portent le raisonnement lot par
lot, que la fusion aplatit.

`#654` (Signal OS) reste **ouverte et non fusionnée**, conformément au mandat :
extraction sélective seulement, jamais en bloc. Mesure à l'appui — la prémisse
« plusieurs directions visuelles empilées » est vraie en **volume** et fausse en
**divergence** : les huit espaces reçoivent la même pile. Il n'y a pas de couches
concurrentes à départager, il y a une couche à amincir.

`main` n'a **pas** été modifié.
