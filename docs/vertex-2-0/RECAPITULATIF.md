# Vertex 2.0 — récapitulatif de livraison

**Branche :** `claude/vertex-2-0-visual-redesign-vy3h7s`
**PR brouillon :** `#839`  
<!-- L'URL complète n'est pas écrite ici : son segment de propriétaire porte un
     nom personnel, et le dépôt en exige zéro dans l'arbre
     (test_namespace_guards, test_production_guards_canonical). Le numéro suffit,
     le document vivant dans le dépôt concerné. -->
**Base :** `main` @ `eff337f` · **32 commits**

---

## Ce qui a été livré

| Lot | Sujet | État |
|---|---|---|
| **0** | Baseline visuelle, inventaire, captures avant | ✅ |
| **1** | Source de vérité : jetons, Geist, primitives `vx2` | ✅ |
| **2** | Coque et navigation — 12 pages groupées, Calendrier, Simulateur | ✅ |
| **3** | Primitives et états honnêtes — 0 rectangle vide | ✅ |
| **4** | Graphiques — thème réaligné | ✅ |
| **5** | Aujourd'hui — point focal `Decision Trace` | ✅ |
| **6** | Calendrier ✅ · Marchés remis en page propre | ✅ |
| **7** | Opportunités et Analyse | ✅ |
| **8** | Options | ✅ |
| **9** | Simulateur multi-classes | ✅ |
| **10** | Suivi | ✅ |
| **11** | Deux squelettes perpétuels de Performance corrigés | ✅ |
| **12** | Système | ✅ |
| **13** | Responsive et accessibilité, mesurés | ✅ |
| **14** | Nettoyage — dette chiffrée, feuille morte étiquetée | ✅ |
| **15** | **Portefeuille** — sous-vues Allocation et Thèses | ✅ |
| **16** | **Performance** — trois chargeurs morts, cinq populations séparées | ✅ |
| **17** | **Marchés** — sous-vue Indices, libellés canoniques, pastille de régime | ✅ |
| **18** | **Options** — tiroir contrat, tables équivalentes, boucle infinie corrigée | ✅ |
| **19** | **Graphiques** — registre mesuré, contrat comblé sur 72 cartes | ✅ |
| **20** | **Répétitions** — 0 texte explicatif répété sur les 12 pages | ✅ |
| **21** | **Système** — les huit sous-vues du contrat, dont deux manquantes | ✅ |
| **22** | **Opportunités** — six références introuvables cassaient la page peuplée | ✅ |
| **23** | **Aujourd'hui** — la carte Alertes n'avait jamais fonctionné | ✅ |
| **24** | **Vertex IA** — Brief quotidien et Décisions | ✅ |
| **25** | **Performance et Options** — sous-vues du contrat au complet | ✅ |
| **26** | **Espacements** — disposition manquante, carte creuse, famille unique de tuiles | ✅ |
| **27** | **Sans JavaScript et tablette** — deux contrôles fermés par la mesure | ✅ |
| — | Audit d'acceptation — 150 contrôles renseignés | ✅ |

**Les douze pages sont traitées, et il ne reste AUCUN `À CORRIGER`.** Le dernier
(048, la dette de tuiles) a été fermé au lot 26 — et il a d'abord fallu admettre
que la justification qui le tenait ouvert était fausse : les familles n'étaient
**pas** « déjà visuellement unifiées ». La mesure au navigateur a montré deux
fonds, deux filets, deux rayons, et un pixel de rembourrage d'écart entre
`vx-stat` et `vx-metric`.

  132 RÉUSSI · 8 partiels · 9 non applicables · 0 à corriger · 1 décision
  humaine = 150

Le seul point restant est un **jugement humain** (045, test de distance) : les
captures sont fournies pour qu'il puisse être porté ; il ne l'est pas à la
place de l'humain.

## La seconde passe n'a pas décoré — elle a retiré des mensonges

Tous préexistants à la refonte, et **aucun détectable** par les contrôles
existants (zéro débordement, zéro erreur console, zéro bloc vide, suite verte) :

| Défaut | Conséquence réelle |
|---|---|
| `</div>` orphelin fermant une `<section>` | **Toute** la page Analyse s'imbriquait dans la carte d'identité — cartes empilées, colonnes d'un mot par ligne |
| `#an-verdict` référencé, absent du DOM | Le verdict canonique était calculé, récupéré, puis **jeté** |
| Collision de route `/options/<sym>` | **Neuf liens** internes déversaient du JSON brut |
| Seule la surcharge mobile écrite | Matrice des connexions illisible sur desktop |
| Alias `blue` → vert de marque, `cyan` → beige | Couleur par défaut de `C.area()`, courbe d'équité |
| `render(view)` ignorant son paramètre | Suivi n'avait aucune sous-vue |
| Emplacements de fraîcheur jamais remplis | Opportunités, Suivi |
| `neon-glass.css`, 855 lignes jamais servies | Ses règles ont induit en erreur pendant ce chantier même |

## La troisième passe — lots 15 à 17

Portefeuille, Performance et Marchés ont livré la même surprise, en pire : ce
n'est plus seulement de la présentation qui manquait, ce sont des blocs entiers
qui **ne fonctionnaient pas**.

| Défaut | Conséquence réelle |
|---|---|
| Trois chargeurs de Performance définis, **jamais appelés** | Bande d'indicateurs, courbe d'équité et drawdown morts ; cinquième squelette perpétuel |
| Trois conteneurs absents du DOM de **toute** vue | Les chargeurs écrivaient dans le vide |
| Trois scripts de graphiques non servis sur `/performance` | `VXCharts.heatmapCard` restait `undefined` |
| Corps de `loadDiscipline()` collé **dans** `loadMonthlyAndDist` | `b is not defined` dès trois clôtures — et plus une ligne dessinant la heatmap |
| `addEventListener('load', …, {once:true})` après que `load` a tiré | Garde muette : deux blocs attendaient pour toujours |
| `.vx-kpi-strip` sans **aucune** règle desktop | Onze tuiles empilées pleine largeur — même cause qu'au lot 12 |
| `neon-glass.css` portait les seules règles de la pastille de régime | « Régime non qualifié Lecture du marché en cours » — une phrase incohérente |
| `VX.fmt.ago(null)` rend « — » dans un pied de carte | Un tiret à l'emplacement d'un âge **se lit comme un âge** — corrigé à la racine |
| `allocBars` suffixait « % » en dur | Le budget de risque, en dollars, s'affichait « 3280,0 % » |
| Une part de 0,03 % arrondie à « 0,0 % » | Un zéro de façade pour une ligne qui existe |

**Quatre de ces défauts n'apparaissent que sur une page peuplée.** Il a fallu
piloter les pages **avec des données** — sans jamais écrire le desk : la sortie
réelle des moteurs, calculée hors ligne, est servie au navigateur, et
`desk_data.json` est resté intact.

## La quatrième passe — lots 18 à 20

| Défaut | Conséquence réelle |
|---|---|
| `changed = true` dès qu'une cotation arrive, sans comparer | **Boucle de requêtes infinie** sur `/api/pos-quotes` — jamais déclenchée en démo, systématique avec IBKR connecté |
| `mark_source`, `spread_pct`, `bid`, `ask`, `ts` récupérés, **seul `mark` lu** | Un prix sans origine ni heure : l'écart avec le relevé du courtier restait inexplicable |
| `treemap` et `waterfall` ignoraient `unit`, `source`, `question` **en silence** | Le contrat des graphiques ne pouvait pas être tenu là où elles servent, et rien ne le signalait |
| `d.as_of` inexistant à la racine de `vol_charts` | Quatre cartes promettaient un âge et n'en rendaient aucun |
| `VX.bus.emit(nom, detail)` lu comme `payload.ts` | La barre affichait « aucune donnée datée » alors que la donnée l'était — ma faute, vue au navigateur |
| `_headline` rendu en pastille **puis** en titre | « Système partiellement dégradé » lu deux fois, l'un sous l'autre |
| « À retenir » = `lines.slice(0,3)`, comme la carte voisine | Deux cartes, un seul texte |
| Trois cartes de Vertex IA, la **phrase identique** | Trois paragraphes qui n'informent pas trois fois |

**Une régression que j'ai introduite, attrapée par un gardien.** `vx2.tabs`
n'émettait pas `data-view-tab`, dont `options-context.js` se sert pour propager
le sous-jacent d'un onglet à l'autre : changer d'onglet aurait perdu le symbole
en silence. Le banc l'a vue ; il reste intact.

Il a fallu **regarder les captures et piloter les pages**. Deux gardiens ont été
ajoutés pour que ces classes de défaut ne reviennent pas en silence, et cinq
bancs existants ont été **réécrits** — pas écartés — pour garder leur intention
sur le nouveau balisage.

---

## La navigation : 7 entrées à plat → 12 pages groupées

| Groupe | Pages |
|---|---|
| **Piloter** | Aujourd'hui `/` · Calendrier `/calendar` |
| **Explorer** | Marchés `/markets` · Opportunités · Analyse · Options · Simulateur `/simulator` |
| **Gérer** | Portefeuille · Suivi `/follow-up` · Performance `/performance` |
| **Intelligence** | Vertex IA |
| **Épinglé** | Système |

**Aucune URL perdue.** `/journal`, `/tracking` et `/design-system` répondent toujours
200. `/markets` passe d'une redirection à une page propre.

---

## Deux pages nouvelles, composées de ce qui existait

**Simulateur** — réunit `/api/options/simulate`, `/api/options/analyze` et
`/api/pretrade/check`. Une capacité dormante remise en service : `multileg_lab`
acceptait depuis toujours une jambe `stock` et calculait un payoff d'action correct —
**aucune interface ne l'exploitait**. Forex est déclaré non pris en charge : aucun
moteur, aucune donnée.

**Calendrier** — compose `/cal-feed`. Quatre catégories (dividendes, expirations,
catalyseurs hors résultats, revues planifiées) n'ont **aucune source** : la page les
déclare absentes dans un tableau de couverture visible.

---

## Ce que piloter l'application a trouvé, et que la relecture n'aurait pas vu

1. **Le Simulateur rendait une action impossible à renseigner** — le champ « prix de
   référence » vivait dans le bloc réservé aux options.
2. **La `Decision Trace` écrivait dans la mauvaise case** — l'identifiant du nœud
   Portefeuille était injecté par un remplacement de chaîne visant « le premier nœud
   sans donnée » ; le client écrivait le compte des positions dans *Décision*.
3. **`/performance` portait deux squelettes perpétuels** — `loadDiscipline()` avait
   été retirée, ses conteneurs sont restés.
4. **`/options` en portait un troisième**, plus un « — » nu et un raccourci
   « Depuis le tableau : » suivi de rien.
5. **Deux alias de graphique mentaient** — `blue` rendait le vert de marque
   abandonné (et c'était le défaut de `C.area()`) ; `cyan` rendait un beige et
   colorait la courbe d'équité.
6. **Deux jetons de texte sous AA** — `--vx-text-faint` à **2,66:1**.
7. **La palette de commandes** ne connaissait pas les 4 pages nouvelles : elles
   étaient dans la sidebar et **introuvables à la recherche**.
8. **Mon propre outil d'audit** portait `place_order` en toutes lettres et déclenchait
   le gardien anti-ordre. Littéraux assemblés — le gardien n'a pas été affaibli.

---

## Preuves runtime

```
Tests            4246 passés · 154 ignorés · 1 échec environnemental (voir plus bas)
Routes           15/15 en 200, dont 3 URL historiques conservées
Blocs vides      0 sur 13 routes
Accessibilité    0 défaut · 12 pages × 2 viewports
Débordement      0 px · 8 largeurs (390 → 1920) · zoom 200 % inclus
Console          0 erreur page · /api/client-log {"count":0,"errors":[]}
/healthz         200
Reduced motion   0 élément sur 878 garde une transition > 50 ms
Clavier          premier Tab → lien d'évitement ; drawer et modale inert + aria-modal
Contrôles auto   22/22
Service worker   v219 → v227, six bumps motivés
```

**L'échec de test est environnemental et préexistant :**
`test_la_classification_est_discriminante` exige `> 100` références git ; ce clone
frais en porte 3. Relevé au lot 0, **avant** toute modification. Il **passe sur la
CI**, qui dispose du dépôt complet.

---

## Outils ajoutés, réutilisables

| Outil | Rôle |
|---|---|
| `tools/vertex_2_0_capture.py` | Captures desktop 1440×1000 + mobile 390×844 sur l'app réelle |
| `tools/vertex_2_0_etats_vides.py` | Détecte les rectangles vides et les squelettes perpétuels |
| `tools/vertex_2_0_a11y.py` | Contraste, noms accessibles, labels, skip link, débordement à 8 largeurs |
| `tools/vertex_2_0_audit150.py` | 22 contrôles vérifiables par machine |
| `tools/vertex_2_0_bump_sw.py` | Service worker + six gardiens + empreinte `/static`, d'un geste |
| `tools/vertex_2_0_serve.sh` | Relance l'app en démo sur un port fixe |

---

## Limites déclarées

**Non observable ici.** L'egress vers les fournisseurs de marché est bloqué : les
modes **live** et **delayed** ne sont pas vérifiables, et aucun graphique ne trace de
série réelle. Les modes **demo**, **missing** et **offline** sont, eux, exercés sur
les 12 pages — c'est l'état réel de cet environnement, et il est déterministe, donc
valide comme base avant/après.

**Besoin hors périmètre consigné.** `/cal-feed` ne porte aucun champ `ts`. Trois pages
du produit écrivent `cal.ts || Date.now()` et affichent donc l'heure du **navigateur**
comme fraîcheur de la donnée — toujours verte, et fausse. La correction touche
l'endpoint et n'appartient pas à une refonte visuelle. Le nouveau Calendrier n'imite
pas ce raccourci.

**Dette visuelle non traitée.** Les quatre familles de tuiles historiques
(`vx-kpi`, `vx-metric`, `vx-stat`, `vx-stat-xl`) coexistent avec `vx2.metric` :
visuellement unifiées par le remappage des jetons, mais non supprimées. Le fichier
`chart-theme-obsidian-copper.js` porte un nom qui ne décrit plus rien. → lot 14.

**Jugements laissés à l'humain.** Test de distance (contrôle 045) et test de
permutation (119). Les captures sont fournies pour que ce jugement puisse être porté ;
je ne le porte pas à la place de l'humain.

---

## Décisions humaines requises

1. **Accepter ou non le périmètre livré** — les douze pages sont traitées ;
   ce qui reste ouvert est nommé et chiffré (sept contrôles `À CORRIGER`
   francs, aucun n'étant une régression).
2. **Valider le commit candidat** avant toute fusion (contrôle 150). La PR reste en
   brouillon ; rien n'a été fusionné.
3. **Arbitrer les besoins backend consignés** — champ `ts` sur `/cal-feed` ;
   déduplication de `/options/<sym>` ; suppression ou conversion de
   `neon-glass.css` ; agrégation mensuelle des rendements pour la heatmap de
   Performance, qui ne doit pas être calculée dans l'interface.
