# SKYLER LOT 472 — LE DEVIS, SECONDE TRANCHE : six dossiers chiffrés, et le résultat structurant n'est aucun des six — `markets_page.py` porte à lui seul TROIS dossiers, et un signataire d'API impose un mot-clé à valeur par défaut sous peine de casser quatre tests

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-472` (base : lot 471 fusionné,
`d50429c`)

Second lot du devis, dossiers **6 à 11** du classement coût/risque du bilan n°16 :
**428** (entonnoir plat), **437** (« Catalyseurs imminents »), **456** (« 200
titres »), **463** (`gex_history` journalise la démo), **425** (« 4 maturités
réelles »), **458** (`catOf`).

**Il ne corrige rien.** Aucun fichier de production touché, aucun gardien écrit,
aucun test ajouté.

## Le contrôle — un cas doublement connu

Le 471 avait posé la règle : le contrôle porte sur un cas dont la réponse est
**déjà** connue. Ici j'ai pris le seul site du lot qui a été publié **deux fois
par deux instruments différents** — `catOf`, mesuré au 458 puis remesuré au 461
(l'incident du `return'X'` sans espace).

```text
attendu (458 + 461)   opportunities_page.py:475-477, prédicat à 3 branches,
                      écriture `return'BALANCED'` SANS espace, rendu en :489
mesuré (ce lot)       :475  function catOf(c){const d=Math.abs(c.delta||0);
                      :476    if(d>=0.40&&d<=0.60)return'BALANCED';if(d>=0.28&&d<0.45)return'DYNAMIC';
                      :477    if(d>=0.18&&d<0.30)return'ULTRA_CONVEX';return'AUTRE';}
                      :489  <span class="vx-badge" …>${catOf(c)}</span>
verdict               CONTRÔLE PASSÉ — trois lignes, quatre `return` collés, rendu confirmé
```

Passé **avant** tout chiffrage.

---

# DOSSIER 428 — l'entonnoir plat par construction · RANG 1

## Les sites, relus

```text
vertex/ui/pages/markets_page.py:786   const isBuy=v=>['ACHETER','RENFORCER'].includes((v||'').toUpperCase());
                                :787   const isAct=v=>{const u=(v||'').toUpperCase();return u&&u!=='ÉVITER'&&u!=='EVITER';};
                                :788-789  les deux filtres qui alimentent l'entonnoir
                                :797   la phrase « un entonnoir plat = marché hostile »
```

Le producteur, relu lui aussi :

```text
terminal.py:412   'verdict': d['verdict']            ← les rows du /scan
config.py:51      def verdict(...) → 'BUY' / 'WATCH' / 'WAIT' / 'AVOID'   ANGLAIS
terminal.py:596   'decision': v['decision']          ← porté par `recs`, PAS par les rows
```

**Deux lignes portent le défaut** (786 et 787), et elles suffisent : `:788` et
`:789` ne font qu'appeler les prédicats.

## Chiffrage

```text
lignes à modifier   2  (ajouter 'BUY' à isBuy · ajouter 'AVOID' à la liste d'exclusion de isAct)
fichiers            1 · moteur touché : non
piège mesuré        NE PAS remplacer le vocabulaire français — le retirer casserait le
                    chemin `|| r.decision`, qui LUI est en français (terminal.py:596).
                    Les deux vocabulaires doivent COEXISTER : c'est un ajout, pas un remplacement.
```

C'est le premier enseignement du lot : **le correctif naturel — « le champ est en
anglais, mettons le prédicat en anglais » — serait faux.** Le repli `|| r.decision`
est bien alimenté, ailleurs, en français.

## Gardien et régression

```text
gardien       tests/test_entonnoir_vocabulaire_lot4xx.py
assertion     isBuy accepte 'BUY' ET 'ACHETER' ; isAct rejette 'AVOID' ET 'ÉVITER'
échoue-t-il aujourd'hui ?   OUI — la ligne 786 ne contient pas 'BUY', la 787 ne teste pas 'AVOID'
gardiens existants   « isBuy » 0 · « entonnoir plat » 0 · « vx-mk-funnel » 1 (test_cockpit.py,
                     présence du conteneur seulement — ne touche pas les prédicats)
octet servi ?  OUI → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# DOSSIER 437 — « Catalyseurs imminents » toujours fraîche · RANG 1

## Les sites, relus — TROIS clients, DEUX producteurs

```text
CLIENT (le repli qui ment)
  vertex/ui/pages/briefing.py:351            timestamp:cal.ts||Date.now()
  vertex/ui/pages/markets_page.py:637        timestamp:cal.ts||Date.now()
  vertex/ui/pages/opportunities_page.py:634  timestamp:cal.ts||Date.now()

SERVEUR (ce qui existe réellement)
  terminal.py:1200  cal_state['updated'] = datetime.now().strftime('%H:%M %d/%m')
  terminal.py:1220  idem
  vertex/app/routes/content.py:40   return jsonify({**cal_state, 'macro': …})
```

**Trois fichiers portent le défaut côté client**, pas un. Le 437 le disait
(« trois pages la portent ») — la relecture confirme et donne les trois lignes.

## Un fait que la relecture ajoute et qui change le chiffrage

`content.py:40` sert **`{**cal_state}`** — le dictionnaire entier. **Toute clé
ajoutée à `cal_state` est servie sans toucher à la route.** Le correctif complet
ne coûte donc pas de modification de route.

## Chiffrage — deux variantes, et elles ne valent pas la même chose

| variante | lignes | fichiers | ce qu'elle donne |
|---|---|---|---|
| **(a) honnête et minimale** — retirer `\|\|Date.now()` aux 3 sites | **3** | 3 | l'affirmation fausse disparaît ; **la carte n'affiche plus aucune fraîcheur** |
| **(b) complète** — `cal_state['ts']=time.time()` aux 2 sites serveur + lire `cal.ts` aux 3 sites client | **5** | 4 | fraîcheur **réelle** affichée ; la route est servie telle quelle |

**(b) coûte deux lignes de plus que (a) et rend le service au lieu de le
supprimer.** Le devis recommande **(b)** — c'est le seul cas des onze où la
variante chère est la bonne, et l'écart est de deux lignes.

## Gardien et régression

```text
gardien       tests/test_fraicheur_catalyseurs_lot4xx.py
assertion     le payload de /cal-feed porte un `ts` numérique ET aucun des 3 fichiers
              ne contient « ||Date.now() » sur la ligne du timestamp du calendrier
échoue-t-il aujourd'hui ?   OUI — mesuré : aucune clé `ts` dans cal_state, et les
              trois `cal.ts||Date.now()` sont aux lignes 351 / 637 / 634
gardiens existants   « cal.ts » 0 · « catalystRunway » 1 (test_reconstruction_today.py,
                     présence du builder — ne touche pas le timestamp)
octet servi ?  OUI (3 pages) → bump SW + 5 gardiens · _EMPREINTE NON
moteur touché ?  non — `terminal.py` ici n'est qu'un producteur d'état, pas un calcul
```

---

# DOSSIER 456 — le dénominateur plafonné à 200 · RANG 2

## Le site, relu — et il tient en UNE ligne

```text
vertex/app/routes/strategy_os_api.py:167   for s in list(detail)[:200]]
                                     :168   report = data_quality_report(packets)
vertex/observability/diagnostics.py:44     return {'total': len(packets), …}
vertex/ui/pages/system_page.py:699         title:'Qualité des données ('+dq.total+' titres)'
                                     :701   conclusion:'Dominante : '+dominant+' ('+byQ[dominant]+' / '+dq.total+')…'
```

La chaîne est complète et **le plafond est à un seul endroit** : `[:200]`, ligne
167. `diagnostics.py` compte honnêtement ce qu'on lui donne ; la page affiche
honnêtement ce qu'on lui sert. **Personne ne ment ; un seul tronque.**

## Chiffrage

```text
lignes à modifier   1  (relever ou retirer le plafond) — OU 1 ligne côté page pour nommer
                    l'échantillon (« 200 titres échantillonnés sur 517 »)
fichiers            1 · moteur touché : non (c'est une route)
DEUX CORRECTIFS POSSIBLES, ET LE CHOIX EST UNE DÉCISION, PAS UNE ÉVIDENCE :
   retirer le plafond → chiffre exact, coût de calcul ×2,6 (517 au lieu de 200)
   nommer l'échantillon → chiffre honnête, coût nul, mais la carte reste partielle
```

## Gardien et régression

```text
gardien       tests/test_qualite_denominateur_lot4xx.py
assertion     rep['total'] == len(UNIVERSE) sur un scan complet — OU le libellé servi
              contient le mot « échantillon » quand total < len(UNIVERSE)
échoue-t-il aujourd'hui ?   OUI — `[:200]` est à la ligne 167 et le titre l.699 ne
              qualifie pas le nombre
gardiens existants   « [:200] » 0 · « data_quality_report » 5, dont
              tests/test_observability_lot179.py:108 `assert rep['total'] == 30`
régression    ce test porte sur une liste FABRIQUÉE de 30 paquets, pas sur le plafond :
              relever le plafond ne le casse pas → RISQUE FAIBLE
octet servi ?  seulement si l'on corrige côté page ; côté route, NON
```

---

# DOSSIER 463 — l'historique GEX journalise la démo · RANG 2

## Les sites, relus

```text
vertex/options/gex_history.py:8-9    la docstring qui promet « QUE des profils réels »
                              :19    _MAX_DAYS = 120
                              :27    def record(profile):          ← UN SEUL paramètre
                              :30-34 la garde : type, `empty`, `symbol`, `net_gex_total` — RIEN sur la provenance
vertex/app/routes/options_intel_api.py:173  # commentaire « best-effort, réel seulement »
                                      :177  _gh.record(profile)
                                      :182  'demo': bool(DEMO_MODE)   ← le drapeau est DANS LA MÊME RÉPONSE
vertex/static/vertex/js/pages/options-gex.js:32   var demo = d.demo ? '…DÉMO…' : '';
                                            :107  '… points réels uniquement.</div>'
```

**Le « 75 lignes plus bas » du 463 est exact** : 107 − 32 = 75. Contrairement au
« vingt lignes » du 434, cette distance-là survit à la relecture.

## Le fait de chiffrage le plus contraignant du lot

`record()` prend **un seul paramètre**. Quatre tests existants l'appellent ainsi :

```text
tests/test_gex_history.py:25   assert gex_history.record(_profile()) is True
                         :34   gex_history.record(_profile())
                         :35   gex_history.record(_profile())
                         :40   assert gex_history.record(gex.compute([])) is False
```

**Ajouter un second paramètre POSITIONNEL casserait les quatre.** Le correctif
doit donc s'écrire `def record(profile, demo=False)` — **un mot-clé à valeur par
défaut**, et le défaut doit être `False` pour que les tests existants restent
verts. Ce n'est pas un détail de style : c'est la différence entre un correctif à
coût nul et un correctif qui rouvre quatre tests.

## Chiffrage

```text
lignes à modifier   4  (signature :27 · garde `if demo: return False` :30 · appel :177
                       en passant DEMO_MODE · docstring :8-9 alignée)
                    +1 si l'on rend la légende conditionnelle (options-gex.js:107)
fichiers            2 (ou 3 avec le JS) · moteur touché : OUI — vertex/options/ est un moteur,
                    mais la modification est une GARDE D'ENTRÉE, aucun calcul GEX n'est touché
DEUX NIVEAUX        (i) empêcher l'écriture en démo → le fichier reste propre à l'avenir,
                        MAIS les points déjà écrits restent 120 jours
                    (ii) marquer chaque point d'un `demo: true` et filtrer à la lecture →
                        traite aussi l'historique déjà pollué. +2 lignes.
```

**C'est le seul des onze dossiers où le correctif ne suffit pas à réparer le
passé** : `_MAX_DAYS = 120` garantit qu'un point écrit aujourd'hui en démo sera
resservi pendant quatre mois. Un devis honnête doit le dire — le coût affiché
(4 lignes) achète l'avenir, pas le présent.

## Gardien et régression

```text
gardien       tests/test_gex_history_provenance_lot4xx.py
assertion     record(profile, demo=True) retourne False et n'écrit rien
échoue-t-il aujourd'hui ?   OUI — la signature l.27 n'accepte pas le mot-clé : le test
              lèverait TypeError, ce qui EST un échec (et pas un faux vert)
gardiens existants   « gex_history » 15 fichiers · « points réels uniquement » 0
régression    les 4 appels de test_gex_history.py sont à UN argument → le défaut
              `demo=False` les préserve. RISQUE FAIBLE À CONDITION DE RESPECTER LE DÉFAUT.
octet servi ?  OUI SI l'on touche options-gex.js — et c'est le SEUL dossier des onze
               qui vit sous vertex/static → **_EMPREINTE ET _SW_VERSION à mettre à jour
               dans tests/test_sw_cache_scope_lot361.py**, en plus du bump et des 5 gardiens
```

**C'est la découverte de cadrage du lot** : le 471 avait conclu « `_EMPREINTE`
jamais » sur ses cinq dossiers. **Ce n'était vrai que de ces cinq-là.** Le
chemin réel du fichier est `vertex/static/vertex/js/pages/options-gex.js` — sous
`pages/`, pas à la racine des JS.

---

# DOSSIER 425 — « 4 maturités réelles » · RANG 1

## Les sites, relus — TROIS, pas un

```text
vertex/ui/pages/markets_page.py:93-94   <div class="vx-insight">Courbe tracée sur les <b>4 maturités
                                        réelles</b> du scan (3M · 5A · 10A · 30A)…      ← HTML STATIQUE
                                  :580   /* Courbe des taux US — 4 maturités RÉELLES … */  ← COMMENTAIRE
                                  :584   const mats=[['^IRX','3M'],['^FVX','5A'],['^TNX','10A'],['^TYX','30A']];
                                  :585   const pts=mats.filter(m=>byId[m[0]]&&byId[m[0]].value!=null);  ← FILTRÉ
                                  :586   if(pts.length<2){emptyCard(…);return;}          ← LA COURBE SE TRACE DÈS 2
                                  :598   limits:'4 maturités réelles (3M/5A/10A/30A)'    ← AFFICHÉ
                                  :600   explain.shows:'… points réels du scan, non interpolés'
```

Le 425 citait `:584-586` — **le mécanisme**. La relecture ajoute **où le chiffre
est écrit** : deux sites **visibles** (`:93-94` et `:598`) plus un commentaire.
C'est la leçon du 471 rejouée — *compter les SITES, pas les occurrences* — et
elle change le chiffrage d'un facteur deux.

## Chiffrage

```text
lignes à modifier   2 visibles  (:93-94 → formulation sans nombre figé · :598 → pts.length)
                    +1 facultative (le commentaire :580, invisible mais servi)
fichiers            1 · moteur touché : non
contrainte mesurée  :93-94 est du HTML STATIQUE dans _CONTENT — il ne peut PAS lire pts.
                    Sa seule correction honnête est de retirer le nombre figé
                    (« les maturités réelles fournies par le scan »), pas de l'interpoler.
```

## Gardien et régression

```text
gardien       tests/test_maturites_courbe_lot4xx.py
assertion     aucun « 4 maturités » figé dans les octets servis de /markets
échoue-t-il aujourd'hui ?   OUI — deux occurrences visibles, lignes 93-94 et 598
gardiens existants   « 4 maturit » 0 · « loadYield » 0
octet servi ?  OUI → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# DOSSIER 458 — `catOf`, la taxonomie amputée · RANG 2

## Les sites, relus

```text
vertex/ui/pages/opportunities_page.py:475-477   le prédicat (3 lignes)
                                          :481   filtre par catégorie
                                          :489   rendu de l'étiquette
vertex/options/legacy_engine.py:291             'type': direction.upper()  ← la donnée qui manque au prédicat
vertex/ui/pages/portfolio_page.py:185-189       l'échelle de conviction — CONCORDE, ne pas y toucher
```

## Chiffrage — et ici le devis refuse de donner un seul chiffre

```text
variante (i)  RENOMMER la colonne pour ce qu'elle mesure — une bande de delta
              1 ligne (:489 et l'en-tête :483). Coût minimal, aucune logique touchée.
variante (ii) AJOUTER le type au prédicat + les 2 catégories manquantes
              4 à 6 lignes. MAIS les catégories de la Constitution SE CHEVAUCHENT
              (BALANCED 0.40-0.60, DYNAMIC 0.28-0.45, BEARISH_TACTICAL 0.30-0.55) :
              même avec le type, un delta 0.42 sur un call reste ambigu entre
              BALANCED et DYNAMIC. Le prédicat ne peut PAS être rendu exact.
```

**C'est le seul dossier des onze dont le correctif complet est IMPOSSIBLE**, et
la mesure du 458 le disait déjà : *« ce n'est pas un bug d'implémentation, c'est
une grandeur insuffisante »*. Un devis qui chiffrerait « 4 à 6 lignes » sans dire
cela vendrait une réparation qui n'en est pas une.

**Le devis recommande la variante (i)** — une ligne, honnête, et qui ferme le
dossier au lieu de prétendre le résoudre.

## Gardien et régression

```text
gardien       tests/test_categorie_options_lot4xx.py
assertion     l'en-tête de colonne ne promet pas une catégorie de la Constitution
              (ou, si variante (ii) : catOf lit c.type)
échoue-t-il aujourd'hui ?   OUI — l'en-tête :483 dit « Catégorie » et :489 rend catOf(c)
gardiens existants   « catOf » 0
octet servi ?  OUI → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# LE DEVIS RASSEMBLÉ — SECONDE TRANCHE

| # | dossier | rang | fichiers | lignes | moteur | gardien | servi | `_EMPREINTE` |
|---|---|---|---|---|---|---|---|---|
| 6 | 428 entonnoir | **1** | `markets_page.py` | 2 | non | 1 | oui | non |
| 7 | 437 fraîcheur | **1** | 3 pages + `terminal.py` | **5** (variante b) | non | 1 | oui | non |
| 8 | 456 dénominateur | 2 | `strategy_os_api.py` | 1 | non | 1 | non | non |
| 9 | 463 provenance GEX | 2 | `gex_history.py` + route (+ JS) | 4 (+1) | **oui (garde)** | 1 | oui si JS | **OUI si JS** |
| 10 | 425 maturités | **1** | `markets_page.py` | 2 (+1) | non | 1 | oui | non |
| 11 | 458 `catOf` | 2 | `opportunities_page.py` | 1 (variante i) | non | 1 | oui | non |

```text
TOTAL SECONDE TRANCHE   6 fichiers distincts · 15 à 18 lignes · 6 gardiens · 3 rangs 1
TOTAL DES ONZE DOSSIERS 25 à 30 lignes · 10 gardiens · 6 rangs 1 · UN SEUL bump SW
```

## La mutualisation — cherchée explicitement, et elle est plus forte qu'au 471

```text
markets_page.py    porte 428 (:786-787) · 425 (:93-94, :598) · 437 (:637)
                   → TROIS dossiers sur six, dont DEUX rang 1, dans UN fichier
opportunities_page.py  porte 458 (:475-477) · 437 (:634)
briefing.py            porte 437 (:351)
```

**Trois des six dossiers de cette tranche vivent dans `markets_page.py`.** Traités
ensemble : une ouverture de fichier, une relecture, **un** bump, et le risque de
régression s'évalue une fois. Traités séparément : trois fois le même travail
d'approche.

Et en combinant les deux tranches du devis : **`markets_page.py` (3 dossiers),
`portfolio_page.py` (2), `opportunities_page.py` (2)** — **sept des onze dossiers
tiennent dans trois fichiers.**

## Les quatre pièges que la relecture a désamorcés

```text
428   « le champ est en anglais, mettons le prédicat en anglais » → FAUX :
      le repli || r.decision est alimenté EN FRANÇAIS par terminal.py:596.
      Les deux vocabulaires doivent COEXISTER.
463   ajouter un paramètre POSITIONNEL à record() casse QUATRE tests existants.
      Il faut `demo=False`, mot-clé à valeur par défaut.
463   `_EMPREINTE` n'est PAS « jamais » — la conclusion du 471 ne valait que pour
      ses cinq dossiers. options-gex.js est sous vertex/static/vertex/js/pages/.
425   deux des trois sites du « 4 maturités » sont VISIBLES, et l'un d'eux
      (:93-94) est du HTML statique qui NE PEUT PAS lire pts.length.
```

Aucun de ces quatre n'était visible sans ouvrir le fichier. Aucun ne renverse un
classement — **les six défauts tiennent tous, aux mêmes rangs** — mais chacun
aurait fait échouer, ralentir ou sur-vendre un correctif.

## Ce que le devis établit et qui n'est pas un chiffre

Deux dossiers de cette tranche **ne se réparent pas complètement**, et il faut le
dire avant qu'un GO soit donné :

- **463** : le correctif achète l'avenir, pas le présent. `_MAX_DAYS = 120`
  garantit qu'un point écrit en démo est resservi quatre mois. Réparer le passé
  coûte deux lignes de plus (marquer et filtrer).
- **458** : le prédicat **ne peut pas** être rendu exact, parce que les catégories
  de la Constitution se chevauchent sur le delta. La seule correction honnête est
  de **renommer** ce que la colonne mesure.

Un devis qui aurait rendu « 4 lignes » et « 4 à 6 lignes » sans ces deux phrases
aurait été exact et trompeur.

## Ce que le lot ne prétend pas

- Le devis chiffre **des lignes, pas des heures**, et les nombres sont des
  **minima structurels** : le correctif seul, **hors** gardien et hors mise à jour
  des cinq témoins de version (et hors `_EMPREINTE` pour le 463).
- **Aucun test n'a été écrit.** Les « échoue aujourd'hui ? OUI » sont établis
  **par lecture**, comme au 471 — plus faible qu'une exécution, et je le redis.
- Les variantes recommandées ((b) pour le 437, (i) pour le 458) sont des
  **jugements**, pas des mesures. Les deux options sont chiffrées pour qu'on
  puisse trancher contre moi.
- **Aucun défaut rejoué** : les six classements sont ceux des rapports d'origine.
- **Aucun navigateur. Aucun réseau. Aucun écrivain appelé. Aucun fichier de
  production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** via `test_client` ; `persist` redirigé vers un `mkdtemp` **et
  la redirection vérifiée par `persist.cache_path()`** ; **`/options/<sym>`,
  `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON appelées** ;
  `gex_history.record()` **non appelée** (lecture de la signature seule).
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-quatorzième lot court, deuxième de la tranche 470-479, **deuxième lot
qui ne cherche pas**.

Le devis est maintenant complet sur **onze dossiers** : **25 à 30 lignes, dix
gardiens, six de rang 1, un seul bump de service worker, et sept dossiers
concentrés dans trois fichiers.** C'est tout ce qu'il faut pour décider.

Le fait de méthode confirme celui du 471 et le précise : **relire ses propres
rapports rend, mais ce qu'elle rend n'est pas ce qu'on cherchait.** Au 471 la
relecture a corrigé des faits (une portée, une distance, un attribut). Ici elle a
surtout révélé des **contraintes d'exécution** — un vocabulaire qui doit coexister,
une signature qui doit rester rétro-compatible, un fichier statique qui déclenche
`_EMPREINTE`, un HTML qui ne peut pas lire une variable. **Ces contraintes ne se
lisent dans aucun rapport de mesure : elles n'apparaissent qu'en préparant le
geste.**

Et une correction de portée que je publie contre le 471 : **sa conclusion
« `_EMPREINTE` jamais » n'était vraie que de ses cinq dossiers.** Elle est
généralisée à tort si on la lit comme une règle. Je ne la compte pas en résultat
faux — le 471 l'avait écrite dans son propre périmètre — **mais je la restreins
ici explicitement pour qu'elle ne serve pas de règle au lot suivant.**

Comptes séparés, inchangés en substance : résultats faux **arrêtés avant
publication** **40** ; **publiés puis corrigés** **5** ; **interprétations
retirées** **3**. Les quatre pièges de ce lot sont des **contraintes découvertes**,
pas des erreurs corrigées : je ne gonfle aucun compteur avec eux.

**Huit bilans — n°9 à n°16 — attendent une réponse, et le devis complet des onze
dossiers attend le premier GO.**
