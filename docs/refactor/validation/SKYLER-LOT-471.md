# SKYLER LOT 471 — LE DEVIS : cinq dossiers chiffrés ligne par ligne, et l'exercice invalide DEUX affirmations publiées — la correction « déjà reçue par la page » du 457 ne l'est pas, et la garde du 434 n'est pas « vingt lignes plus haut » mais trois cent soixante-deux

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-471` (base : lot 470 fusionné,
`693bc5b`)

Premier lot de la tranche 470-479, et **premier lot d'un genre nouveau**. Le
bilan n°16 a constaté que les défauts affichés reculaient de 7 à 3 et que le
critère posé d'avance au bilan n°15 était rempli ; il recommandait **(b), le lot
devis**. Ce lot est ce devis.

**Il ne corrige rien.** Aucun fichier de production touché, aucun gardien écrit,
aucun test ajouté. Il **chiffre**.

## Ce qu'un devis doit prouver, et pourquoi il pouvait rater

Un devis est une **affirmation sur l'avenir** : *ce correctif coûtera tant*. Le
fait de méthode dominant du bilan n°16 — l'instrument faux au premier jet dans
huit lots de mesure sur neuf — s'applique **ici plus qu'ailleurs**, parce qu'un
devis ne mesure pas le produit : il mesure **mes propres rapports**.

La parade posée avant la première mesure : **relire chaque ligne citée dans le
fichier réel avant de la chiffrer.** Une ligne citée de mémoire est une ligne
fausse.

**Elle a servi deux fois.** Deux affirmations publiées n'ont pas survécu à la
relecture. Elles sont corrigées plus bas, à leur place.

## Le contrôle — un cas dont la réponse était DÉJÀ connue (leçon 467)

Le 457 a mesuré et publié : `portfolio_page.py:265-271`, littéral `' / 10'`. Si
l'instrument du devis ne retrouve pas exactement cela, c'est **le devis** qui est
faux, pas le 457.

```text
attendu (rapport 457)   portfolio_page.py, plage 265-271, littéral « / 10 »
mesuré (ce lot)         portfolio_page.py:266   stocks.length+' / 10'
                                          :267   stocks.length>=10 ? 'complet — remplacement obligatoire'
                                          :268   stocks.length>=10 ? 'vx-warn'
verdict                 CONTRÔLE PASSÉ — même fichier, même plage, même littéral
```

Le contrôle a porté sur un cas connu, et il est **passé avant** que je chiffre
quoi que ce soit.

---

# DOSSIER 457 — la borne V1 figée · RANG 1

## Le site, relu

```text
vertex/ui/pages/portfolio_page.py:266   +cell('Actions',stocks.length+' / 10',
                                  :267     stocks.length>=10?'complet — remplacement obligatoire':'places disponibles',
                                  :268     stocks.length>=10?'vx-warn':'');
```

**Trois lignes portent le 10**, pas une : le dénominateur affiché **et** les deux
seuils qui déclenchent la consigne « remplacement obligatoire ». Un correctif qui
ne changerait que le `' / 10'` laisserait la consigne fausse en place.

## Ce que le 457 a supposé, et que le devis RÉFUTE

Le 457 écrivait : « Correction pressentie : lire `d.bounds.max` — **déjà reçu par
la page** — au lieu du littéral. » **`d.bounds` n'est pas reçu par la fonction
qui affiche le KPI.**

```text
renderSummary(rich)        déclarée l.248   ne reçoit QUE `rich`  → aucun `bounds` dans sa portée
renderDiscipline()         déclarée l.950   fetch /api/portfolio/context   l.952
                                            const b = d.bounds||{}         l.961
occurrences de « bounds » dans tout le fichier : 2 — l.961 et l.962, les deux dans renderDiscipline
```

**Deux fonctions différentes.** La correction n'est pas « remplacer un littéral
par une variable en portée » : la variable n'y est pas.

## La co-visibilité, mesurée — et elle n'est vraie que sur UNE vue

```text
renderSummary appelée par   renderPositions   l.470     vue « positions »
                            renderPerformance l.585     vue « performance »
                            renderOptions     l.669     vue « options »
                            renderRisk        l.713     vue « risque »
renderDiscipline appelée par  RENDER.risk     l.978     vue « risque » UNIQUEMENT
routeur : (RENDER[VIEW]||renderSynthese)()    l.989     UNE vue rendue à la fois
```

Le KPI « Actions n / 10 » apparaît sur **quatre vues** ; la carte « 8-15 lignes
cibles » sur **une seule**. Ils sont donc co-visibles sur **`risque`, et là
seulement** — et sur la vue « Synthèse » (`team` → `renderSynthese`) le KPI
**n'apparaît pas du tout**.

Le 457 écrivait « la page affiche « 8-15 lignes cibles » **trois cartes** sous un
KPI qui déclare le book complet à 10 ». **C'est vrai sur la vue Risque, faux sur
les trois autres.** Le 457 avait posé la réserve honnête (« la co-visibilité est
établie sur la source servie, pas observée au rendu ») — la mesure lui donne
raison sur un quart de son périmètre.

**Cela ne touche pas le rang 1**, qui repose sur la consigne d'action fausse et
non sur la co-visibilité. Cela **aggrave** même la lecture : sur trois vues sur
quatre, **rien à l'écran ne contredit le « complet »**.

## Le chemin de lecture du plafond — troisième récurrence de la leçon 468

J'allais chiffrer `load_profile().portfolio_target_positions.max`. **Cet attribut
n'existe pas.**

```text
StrategyProfile attributs publics — mesurés :
  allowed_final_decisions · analysis_order · benchmark · category · display_name
  dte · holding · max_simultaneous_options · max_stock_weight_pct · options_profile
  portfolio_max_drawdown_pct · portfolio_max_positions · portfolio_min_positions
  raw · stock_max_drawdown_pct · strategy_id · style · version

  portfolio_max_positions  = 15      ← la borne V2
  portfolio_min_positions  = 8
  max_stock_weight_pct     = 15.0
  load_profile(version=1).portfolio_max_positions = 10   ← d'où vient le littéral
```

`portfolio_target_positions` est la clé **du JSON**, pas l'attribut **de l'objet**.
Un devis qui l'aurait cité aurait envoyé le correcteur droit dans un
`AttributeError`. **Mesuré, pas supposé.**

## Trois chemins de correction, chiffrés

| # | chemin | lignes | portée | verdict |
|---|---|---|---|---|
| **a** | **injection serveur** — `%%PFMAX%%` via `json_for_script`, comme `%%VIEW%%` déjà utilisé l.1005 | **≈ 5** | 1 fichier, 0 moteur, 0 réseau, **les 4 vues** | **RETENU** |
| b | `VX.fetch.peek('/api/portfolio/context')` (API réelle, `vx-core.js:316`) | 2-3 | rend `null` hors vue Risque → exige un repli honnête | insuffisant seul |
| c | `await VX.fetch(...)` dans `renderSummary` | 6-8 | rend la fonction `async`, **4 sites d'appel** à reprendre, +1 requête sur 3 vues | le plus cher |

**Le chemin (a) est le moins cher parce que le mécanisme est déjà dans le
fichier** : `render()` fait déjà `_JS.replace('%%VIEW%%', json_for_script(view))`
à la ligne 1005, et `json_for_script` est déjà importé à la ligne 28. Il n'y a
rien à inventer — il y a un geste à copier deux lignes plus haut.

Détail : `load_profile()` **n'a pas de cache** (aucun `lru_cache` dans
`vertex/strategy/constitution.py`) — l'appeler au rendu relit un JSON à chaque
requête. C'est un coût réel, faible, **à nommer** dans le devis.

## Gardien à écrire, et régression

```text
gardien       tests/test_borne_portefeuille_v2_lot4xx.py
assertion     " / 10" absent de portfolio_page.py  ET  valeur injectée == load_profile().portfolio_max_positions
échoue-t-il aujourd'hui ?   OUI — le littéral est à la ligne 266, vérifié par lecture
gardiens existants sur ce site   « / 10' » → 0 · « remplacement obligatoire » → 0
tests touchant portfolio_page.py  11 — AUCUN ne touche ce site
octet servi modifié ?         OUI (HTML de /portfolio) → BUMP SW + 5 gardiens
_EMPREINTE / _SW_VERSION ?    NON — rien sous vertex/static
```

---

# DOSSIER 455 — la phrase pré-trade sans les inconnus · RANG 2

## Le site, relu

```text
vertex/engines/pretrade.py:161   n_ko   = statuses.count(KO)
                           :162   n_warn = statuses.count(WARN)
                           :163   narrative = ('Vérification pré-trade %s : %d contrôle(s) défavorable(s), %d à surveiller, '
                           :164-166  'sur %d. Rapport DESCRIPTIF — …' % (sym, n_ko, n_warn, len(checks)))
```

Confirmé mot pour mot. **Aucun `statuses.count(UNKNOWN)`** ; le gabarit ne porte
que **trois** `%d` numériques.

## Chiffrage

```text
lignes à modifier   2  (+1 ligne n_unk après :162 · gabarit :163-166 étendu d'un %d)
fichiers            1
moteur touché ?     OUI, le fichier est sous vertex/engines/ — mais la modification
                    porte sur la CHAÎNE DE RENDU, aucun calcul, aucun statut, aucun seuil
```

**Correction de l'attendu du réveil.** Le devis devait vérifier « si le correctif
touche un moteur (attendu : AUCUN pour ces cinq) ». **Un des cinq en touche un** :
`pretrade.py` vit sous `vertex/engines/`. Je le dis plutôt que de le ranger.
La nuance qui compte pour le risque : la ligne modifiée est une f-string, pas une
décision.

## Gardien à écrire, et régression

```text
gardien       tests/test_pretrade_inconnus_lot4xx.py
assertion     un build dont `statuses` contient UNKNOWN produit un `narrative` qui CITE le compte d'inconnus
échoue-t-il aujourd'hui ?   OUI — le gabarit :163-166 n'a que 3 %d, aucun ne porte les UNKNOWN
gardiens existants  0 sur la phrase
régression    15 tests mentionnent pretrade ; tests/test_pretrade.py:71 est le SEUL à lire
              `narrative`, et il n'assert que la clause READONLY (« jamais d'ordre »),
              pas les compteurs → RISQUE FAIBLE, l'ajout d'un %d ne le casse pas
octet servi ?  NON — sortie JSON d'API, ni shell ni /static → AUCUN BUMP
```

**C'est le seul des cinq qui ne demande pas de bump.**

---

# DOSSIER 461 — `dominantRisk`, la fenêtre morte 15-25 % · RANG 2

## Le site, relu — et un piège que seule la relecture montre

```text
vertex/ui/pages/portfolio_page.py:221   if(m.top1&&m.top1.w>25)          ← LE dossier 461
                                  :223     detail:'au-delà d’un repère prudent (~15 % pour un titre)'
                                  :228   if(m.optPct!=null&&m.optPct>25) ← UN AUTRE SUJET
```

**Il y a DEUX littéraux `>25` dans la même fonction**, à sept lignes d'écart. Le
premier porte sur la concentration d'un titre ; le second sur l'exposition
options — **un seuil différent, pour une grandeur différente**. Un correcteur qui
remplacerait « le 25 de `dominantRisk` » sans lire les deux casserait le second.

C'est le **douzième** cas du piège des homonymes, sous sa forme la plus banale et
la plus dangereuse : **le même nombre, dans la même fonction, pour deux choses
différentes.**

## Chiffrage

```text
lignes à modifier   1 (la ligne 221) — 2 si l'on aligne aussi le détail de la lig 223
fichiers            1  (le MÊME que le 457)
moteur touché ?     non
MUTUALISATION       le 461 a besoin de max_stock_weight_pct (15.0), le 457 de
                    portfolio_max_positions (15) — MÊME profil, MÊME injection.
                    Faits ensemble, les deux dossiers coûtent UNE injection au lieu de deux,
                    UN bump au lieu de deux, et le second dossier ne coûte plus qu'UNE ligne.
```

## Gardien à écrire, et régression

```text
gardien       tests/test_risque_dominant_constitution_lot4xx.py
assertion     `top1.w>25` absent du source ET le seuil de concentration == load_profile().max_stock_weight_pct
échoue-t-il aujourd'hui ?   OUI — le littéral est à la ligne 221
gardiens existants   « dominantRisk » → 0 · « Risque dominant » → 0
octet servi ?  OUI → bump SW + 5 gardiens · _EMPREINTE NON
apostrophes    la ligne 223 porte une apostrophe TYPOGRAPHIQUE (’), pas une apostrophe
               droite — aucun échappement en jeu, la règle 2 de CLAUDE.md ne s'applique pas ici
```

---

# DOSSIER 434 — `renderAnomalies` sans garde de scan · RANG 1

## Le site, relu

```text
vertex/ui/pages/opportunities_page.py:571   async function renderAnomalies(){
                                      :572     const scan=await VX.fetch('/scan',{ttl:120000});
                                      :573     const rows=(scan.rows||[]).filter(r=>(r.anomalies||[]).length);
                                                    ← AUCUNE garde entre :573 et la phrase
                                      :599     :VX.states.empty('Aucune anomalie action détectée sur le scan courant.');
```

La garde modèle, dans le **même fichier** :

```text
vertex/ui/pages/opportunities_page.py:237   if(!rows.length){$('op-body').innerHTML=
                                              VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
```

## Le chiffre du 434 est FAUX, et le devis le corrige

Le 434 écrit **deux fois** — dans son titre et dans sa correction pressentie —
que la garde correcte est « **vingt lignes plus haut** ».

```text
garde modèle      opportunities_page.py:237   (dans renderRadar)
phrase fautive    opportunities_page.py:599   (dans renderAnomalies)
distance réelle   362 lignes
gardes « if(!…length) » du fichier entier : 2 — l.139 et l.237. Aucune entre 531 et 599.
```

**La substance du 434 tient intégralement** : la garde existe, elle est dans le
même fichier, elle lit la même source `/scan`, et `renderAnomalies` ne l'a pas.
**C'est la distance qui est fausse** — et elle n'était pas décorative : « vingt
lignes plus haut » suggère un oubli local, « trois cent soixante-deux lignes plus
haut, dans une autre fonction, sous un autre onglet » décrit autre chose.

**Je le compte : publiés puis corrigés, 4 → 5.**

## Chiffrage

```text
lignes à ajouter   1, après la ligne 572 :
                   if(!(scan.rows||[]).length){$('op-body').innerHTML=
                     VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
fichiers           1 · moteur touché : non
note               la garde doit porter sur scan.rows (« y a-t-il un scan ? »), PAS sur `rows`
                   (« y a-t-il des anomalies ? ») — c'est toute la distinction du 434, et
                   se tromper de variable reproduirait le défaut à l'identique
```

## Gardien à écrire, et régression

```text
gardien       tests/test_anomalies_sans_scan_lot4xx.py
assertion     le corps de renderAnomalies (extrait par appariement d'accolades) contient une
              garde portant sur scan.rows AVANT la phrase « Aucune anomalie action détectée »
échoue-t-il aujourd'hui ?   OUI — mesuré : aucune garde entre :571 et :599
gardiens existants   « renderAnomalies » → 0 · « Aucune anomalie action » → 0
octet servi ?  OUI (HTML de /opportunities) → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# DOSSIER 427 — la légende des quatre indices · RANG 1

## Le site, relu

```text
vertex/ui/pages/markets_page.py:511   const wanted=['S&P 500','Nasdaq','Dow Jones','Russell 2000'];
                                :512   const sets=wanted.map(…).filter(x=>x.spark.length>5);   ← FILTRÉ
                                :513   if(!sets.length){emptyCard(…);return;}
                                :521   legend:wanted.map((n,i)=>({label:n,color:VXCharts.colors.series[i%6]}))
                                                ↑ NON filtré — la légende énumère `wanted`, le graphique trace `sets`
                                :526-527  render: … sets.map(x=>({label:x.n, …}))
```

Confirmé exactement : `legend:` lit `wanted`, `render:` lit `sets`. Le décalage
naît entre la ligne 512 et la ligne 521.

## Chiffrage

```text
lignes à modifier   1 — la ligne 521 devient  legend:sets.map((x,i)=>({label:x.n,color:VXCharts.colors.series[i%6]}))
                    (+1 facultative : rendre conditionnel le `shows:` de la ligne 522)
fichiers            1 · moteur touché : non
propriété           le MÊME geste corrige les deux défauts du 427 — l'indice fantôme
                    dans la légende ET le glissement des couleurs — parce que les deux
                    viennent de la même divergence wanted/sets
```

## Gardien à écrire, et régression

```text
gardien       tests/test_legende_indices_lot4xx.py
assertion     « legend:wanted.map » absent du source ET la légende dérive du même tableau que render
échoue-t-il aujourd'hui ?   OUI — le littéral `legend:wanted.map` est à la ligne 521
gardiens existants   « loadMultiIndex » → 0 · « vx-mk-multi » → 0
octet servi ?  OUI (HTML de /markets) → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# LE DEVIS, RASSEMBLÉ

| # | dossier | rang | fichier | lignes | moteur | gardien à écrire | octet servi |
|---|---|---|---|---|---|---|---|
| 1 | 457 borne V1 | **1** | `portfolio_page.py` | ≈ 5 | non | 1 | oui |
| 2 | 455 pré-trade | 2 | `pretrade.py` | 2 | **oui (rendu)** | 1 | **non** |
| 3 | 461 `dominantRisk` | 2 | `portfolio_page.py` | 1-2 | non | 1 | oui |
| 4 | 434 `renderAnomalies` | **1** | `opportunities_page.py` | 1 | non | 1 | oui |
| 5 | 427 légende | **1** | `markets_page.py` | 1 | non | 1 | oui |

```text
TOTAL       4 fichiers · 10 à 12 lignes · 4 gardiens à écrire · 3 dossiers de RANG 1
BUMP SW     UN SEUL suffit pour les quatre pages — les cinq gardiens de version sont
            test_reconstruction_today.py:78 · test_production_guards_canonical.py:306
            test_ui_v3.py:229 · test_redesign_ui.py:316 · test_design_system_page_lot187.py:72
_EMPREINTE  JAMAIS — aucun des cinq dossiers ne touche vertex/static (mesuré : l'empreinte
            de test_sw_cache_scope_lot361 n'agrège que vertex/static, l.32 et l.61)
```

**Le fait le plus utile du devis n'est aucun des cinq chiffres pris isolément,
c'est la mutualisation** : les dossiers 457 et 461 vivent dans le **même fichier**
et ont besoin du **même profil**. Faits ensemble, ils partagent une injection et
un bump ; le second ne coûte alors plus qu'**une ligne**. Un plan de correction
qui les traiterait séparément paierait deux fois.

Et un fait de cadrage : **quatre des cinq correctifs tiennent en une à deux
lignes**. Le plus cher, le 457, en coûte cinq — parce que la variable dont le 457
disait qu'elle était « déjà reçue » ne l'est pas.

## Ce que le devis a coûté à mes propres rapports

```text
457   « lire d.bounds.max — déjà reçu par la page »        RÉFUTÉ — hors portée de renderSummary
457   « trois cartes plus bas »                            VRAI sur 1 vue / 4
434   « la garde est vingt lignes plus haut »              FAUX — 362 lignes
457   attribut portfolio_target_positions                  N'EXISTE PAS — portfolio_max_positions
```

Quatre relectures, quatre écarts. **Aucun ne renverse un classement** — les cinq
défauts tiennent tous, aux mêmes rangs. Mais trois d'entre eux auraient envoyé un
correcteur au mauvais endroit, et le quatrième droit dans une exception.

**C'est exactement ce que le bilan n°16 annonçait** en recommandant (b) : *un
devis se vérifie en le lisant, une mesure ne se vérifie qu'en la refaisant.* Le
devis vient de se vérifier lui-même en relisant — et il a trouvé quatre choses
que quinze bilans de mesure n'avaient pas vues, **parce qu'aucun n'avait eu
besoin de savoir où poser la main.**

**Genre neuf : UNE CORRECTION PRESSENTIE QUI DÉSIGNE UNE VARIABLE HORS DE PORTÉE
— le rapport voit juste au niveau de la PAGE et faux au niveau de la FONCTION.**
C'est la leçon 465 transposée : *une chaîne complète dans le code n'est pas une
chaîne dans le produit* devient ici *une donnée présente dans la page n'est pas
une donnée présente dans la fonction*.

## Les trois dossiers qui ne sont PAS des correctifs

Hors périmètre de ce devis, et **ils doivent rester hors de tout devis** — ils ne
demandent pas qu'on répare, ils demandent qu'on **décide** :

```text
469   le board sélectionne sous le minimum DTE absolu de la Constitution (bucket court,
      cible 45 j, plancher V2 = 60)
      QUESTION : la Constitution fait-elle loi, ou le bucket court est-il une exception assumée
      qu'il faut alors ÉCRIRE dans la Constitution ?

468   six seuils décident sans source de configuration
      QUESTION : ces six concepts doivent-ils entrer dans la Constitution, ou rester
      des constantes de présentation ?

466/467  28 routes orphelines sur 189 (14,8 %)
      QUESTION : les supprimer, ou les documenter comme surface d'API assumée ?
```

Chiffrer ces trois-là serait une **erreur de catégorie** : on ne devise pas le
coût d'un correctif dont personne n'a dit qu'il fallait corriger.

## Ce que le lot ne prétend pas

- Le devis **chiffre des lignes, pas des heures**. Il dit où poser la main et ce
  qui casse, pas combien de temps cela prend.
- Les chiffres de lignes sont **des minima structurels** : ils comptent le
  correctif, **pas** le gardien à écrire ni la mise à jour des cinq témoins de
  version.
- **Aucun test n'a été écrit** pour vérifier qu'il échoue. Les « échoue
  aujourd'hui ? OUI » sont établis **par lecture du code**, comme la consigne le
  demandait — c'est plus faible qu'une exécution, et je le dis.
- Le chemin (a) du 457 est **conçu, pas prototypé**. Que `json_for_script`
  fonctionne pour `%%VIEW%%` établit le mécanisme, pas l'absence de surprise.
- **Aucun défaut n'a été rejoué.** Les cinq classements sont ceux de leurs
  rapports d'origine ; ce lot n'en confirme ni n'en infirme aucun, il les
  localise.
- **Aucun navigateur. Aucun réseau. Aucun écrivain appelé. Aucun fichier de
  production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché** — seuls les trois documents de ce lot
  apparaissent dans `git status`. Pas de bump. SW : `td-shell-v187`.
- `constitution.load_profile()` appelée en mémoire (n'écrit rien) ; les 8 pages
  en **GET** via `test_client` ; `persist` redirigé vers un `mkdtemp` **et la
  redirection vérifiée par `persist.cache_path()`** ; **`/options/<sym>`,
  `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-treizième lot court, **premier de la tranche 470-479**, et le premier
qui ne cherche pas.

Il fallait le faire, et le bilan n°16 avait raison sur le motif : la boucle
mesure depuis quarante-neuf lots et n'a **jamais** rendu la décision possible.
Dix-neuf dossiers prouvés, aucun corrigé, aucune réponse. Un devis ne trouve
rien, mais il transforme « il y a un défaut » en « voici la ligne, voici le
gardien, voici ce qui casse ».

Le fait de méthode est net et il vaut pour la suite : **relire ses propres
rapports est un acte de mesure à part entière, et il rend autant qu'un
balayage.** Quatre écarts sur cinq dossiers, dont un attribut qui n'existe pas —
et pas un seul n'avait été détectable sans ouvrir le fichier.

Comptes séparés : résultats faux **arrêtés avant publication** **40** (+0 — les
quatre écarts de ce lot étaient **déjà publiés**, ils ne comptent pas ici) ;
**publiés puis corrigés** **5** (+1, le « vingt lignes » du 434) ;
**interprétations retirées** **3** (+1, le « déjà reçu par la page » du 457).

Le devis est posé. **Il n'y a plus rien à mesurer avant une décision humaine sur
ces cinq dossiers** — et c'est la première fois que je peux l'écrire.

**Huit bilans — n°9 à n°16 — attendent une réponse, et le devis du 471 attend le
premier GO.**
