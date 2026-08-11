# SKYLER LOT 575 — les 35 vues n'ajoutent **141 octets**. Le vrai trou était ailleurs : **`/analysis` sans symbole**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-575` (base : lot 574 fusionné,
`4e353817`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(uu)** — le 574 a établi qu'un corpus JavaScript réutilisé par six lots avait
été prélevé en appelant les 8 pages à leur URL de base, et en a conclu que **les
35 vues (`?view=…`)** étaient le trou. Ce lot mesure le trou.

Piège écrit **avant** de mesurer (564, 568-B) : *je m'attends à ce que l'écart
soit **petit** — les vues partagent probablement le même script inline que la
page de base. Compter des « programmes nouveaux » sans dédupliquer par contenu
surestimerait massivement l'apport.*

**Verdict : le piège est à moitié juste, et à moitié faux.** Il l'est pour les
vues. Il ne l'est pas du tout pour `/analysis`.

## La correction — **le 574 avait nommé le mauvais coupable**

```text
registre de vues dans `analysis_page.py` : AUCUN
témoin `'Montant envisagé requis'` dans les 35 vues : ABSENT
témoin `'Montant envisagé requis'` dans `/analysis/AAPL` : inline#1
```

`/analysis` **n'a pas de vues**. Le témoin du 574 ne vit donc pas dans une vue :
il vit dans la forme **avec symbole** de la page. La borne de portée est réelle,
mais ce n'est pas celle que le 574 a nommée : le corpus des six lots est celui
des **URL sans paramètre**, et le paramètre qui compte ici est un **symbole**,
pas une vue.

**Publiés puis corrigés : 36 → 37 (+1).**

## L'arrêt du lot — **une empreinte exacte ne déduplique pas les quasi-doublons**

Mon propre garde-fou était insuffisant. J'ai dédupliqué par contenu — par
empreinte md5 **exacte** — et obtenu :

```text
corpus de base (8 pages, URL nue)   113 parties · 34 programmes · 782 670 octets
les 35 vues                         545 parties · 47 programmes
   programmes « neufs »                                    17
   octets « neufs », dédupliqués par empreinte        879 280
```

J'allais publier **879 280 octets jamais mesurés**. Puis j'ai lu les programmes
un par un :

```text
/portfolio?view=performance  inline#1   67 101 octets
/portfolio?view=positions    inline#1   67 099 octets
/portfolio?view=watchlist    inline#1   67 099 octets
```

Trois « programmes distincts » qui diffèrent de **deux octets**. Mesuré comme il
fallait — préfixe commun, suffixe commun, span divergent :

```text
page (n vues)        inline base   inline vue   diff réelle
/markets (5)              51 134       51 134         0 – 10
/opportunities (5)        49 155       49 155         0 –  9
/portfolio (6)            67 094       67 094         0 – 11
/journal (5)              35 655       35 655         0 – 12
/system (5)               60 124       60 124         0 –  0

octets « neufs » par empreinte exacte              879 280
octets qui DIFFÈRENT réellement                        141   (0,01 %)
```

**Les 35 vues ajoutent 141 octets.** Et ces 141 octets, lus, sont une seule
chose :

```javascript
// côté vue :  const VIEW='track-record';
// côté base : const VIEW='overview';
```

La page sert **tout** le JavaScript de ses vues dès l'URL de base et bascule sur
la valeur de `VIEW`. Les six lots n'ont donc **rien manqué du côté des vues** —
et aucun chiffre publié de 539 à 574 ne bouge pour cette raison.

**Arrêtés avant publication : 201 → 202 (+1).**

## Le banc qui échoue est une mesure — **`/options` ne sert aucun script de page**

Le premier banc d'écart s'est **arrêté** au lieu de sauter (543-A) :
« `inline#1` introuvable dans le corpus de base pour `/options` ». En ouvrant le
corpus (545) :

```text
/options   ->   inline#0 : 3 689 octets   ET RIEN D AUTRE
```

C'est le script de shell commun aux 8 pages. **`/options` ne sert aucun script de
page — ni à son URL de base, ni à aucune de ses 9 vues.** Tout son JavaScript
vit dans `/static/**` (`options-gex.js`, `options-intel.js`), qui sont bien dans
le corpus. Ce n'est pas un défaut ; c'est une architecture différente des cinq
autres pages, et personne ne l'avait écrit.

## Le vrai trou — **`/analysis` avec un symbole**

```text
`/analysis` sans symbole vs `/analysis/AAPL`
   parties de même nom, octets identiques        9
   parties de même nom, octets différents        1   inline#1
      inline#1 : 1 735 octets sans symbole → 50 557 avec   (× 29)
   parties présentes seulement avec symbole      7

programmes NEUFS apportés par `/analysis/AAPL` : 8   (241 516 octets)
   /static/…/vendor/lightweight-charts       163 684
   inline#1                                   50 557
   /static/…/charts/candlestick-lwc.js          8 502
   /static/…/charts/projection-cone.js          6 917
   /static/…/charts/anomaly-scan.js             4 963
   /static/…/charts/candlestick-chart.js        4 133
   /static/…/charts/price-chart.js              2 203
   /static/…/charts/annotations.js                557
```

Six lots ont mesuré `/analysis` en n'en voyant que **1 735 octets** de script de
page sur 50 557.

## Ce que l'angle mort coûte, mesuré avec **l'instrument du 570, tel quel**

```text
le canal de notification dans les 8 programmes neufs
   relevé (A), noms lus                3
   bannières `vx-error-banner`         8
   marqueur `dataset.state`            0
   plancher, même règle qu'au 570     11
   relevé (B), structurel             38
```

Trois sites lus, dont **le témoin, enfin trouvé** :

```javascript
VX.toast('Ticket copié — à saisir manuellement dans IBKR', 'success')
VX.toast('Écris une question', 'warn')
VX.toast('Montant envisagé requis', 'warn')
```

Deux conséquences chiffrées, à porter aux rapports concernés :

- **le plancher du canal passe de 90 à au moins 101** (570, 571, 573) ;
- **le 572 publiait « 10 bannières sur 10 interpolent la cause » : il en existe
  au moins 8 de plus**, jamais lues. Le « 10 / 10 » reste vrai *sur son corpus* —
  son dénominateur, lui, était plus petit que le produit.

## Second contrôle (481) — ce que l'instrument ne peut pas voir

Le serveur tourne en **DÉMO, sans IBKR**. Un écran dont le rendu dépend d'une
donnée absente en DÉMO peut servir **moins** de JavaScript qu'en réel : ce relevé
est donc lui aussi un **plancher**, comme celui qu'il corrige. Et il ne dit rien
des 9 vues d'`/options`, qui ne servent aucun script inline.

## Ce que le dépôt fait bien, mesuré

- **Une page sert ses vues sans aller chercher de code** : 141 octets d'écart
  pour 35 vues — pas de second aller-retour réseau pour changer d'onglet.
- **`/system` sert exactement les mêmes octets pour ses 5 vues** (écart 0 – 0) :
  la bascule y est entièrement côté client.
- **`/analysis` ne charge la bibliothèque de graphiques (163 Ko) que lorsqu'un
  symbole est demandé** — l'URL nue ne la sert pas.
- **La calibration négative tient** : une vue fabriquée (`?view=vueFabriquee575`)
  retombe sur la vue par défaut, sans servir un seul programme inconnu.

## Portée — ce que ce lot NE dit PAS

- Les **8 programmes neufs ne sont pas analysés** : comptés, situés, et leur
  canal relevé avec l'instrument du 570 — rien de plus.
- Le relevé **(B) structurel = 38** n'est **pas lu** ; l'écart (A)/(B) n'est pas
  arbitré ici.
- **Aucun chiffre de 539 à 574 n'est réécrit.** Les corrections sont en ajout :
  le 570/571/573 gardent « 90 », le 572 garde « 10 / 10 », avec la mention que
  leur corpus était plus petit que le produit.
- Ce lot **n'a appelé que des URL de la liste sûre** — les 8 pages, leurs 35
  vues, `/analysis/AAPL`, `/static/**`.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, bancs écrits **en fichier**, aucun tronqué avant d'avoir
  écrit son JSON.
- `persist._BASE_DIR` redirigé vers un répertoire temporaire, **redirection
  vérifiée** via `persist.cache_path()` dans chaque banc.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : **8 / 8 identiques.****
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés** (`ai_enrichment.json`, `daily_prev.json`,
  `desk_data.json`, `weekly_snapshot.json` — un de plus que les trois habituels,
  `daily_prev.json` étant touché par le `scan()` des bancs), **restaurés — écart
  final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **hier j'ai nommé un trou, aujourd'hui je l'ai mesuré, et il
n'était pas où je l'avais dit.** Le 574 accusait les 35 vues ; elles pèsent 141
octets. Le vrai angle mort était une page qui sert vingt-neuf fois plus de code
quand on lui donne un symbole. Nommer une limite est facile ; la mesurer la
déplace presque toujours.

Et une leçon sur mes propres garde-fous : j'avais écrit le bon piège — « ne pas
compter sans dédupliquer par contenu » — et ma parade, l'empreinte exacte, était
**insuffisante d'un facteur 6 200**. Un garde-fou écrit à l'avance n'est pas un
garde-fou vérifié.

Trois règles neuves :

- **575-A · UNE EMPREINTE EXACTE NE DÉDUPLIQUE PAS LES QUASI-DOUBLONS** — 17
  « programmes neufs » différant de deux octets ; 879 280 annoncés, **141**
  réels.
- **575-B · LA BORNE D'UN CORPUS N'EST PAS CELLE QU'ON A NOMMÉE LA VEILLE** — le
  574 accusait les vues ; le trou était l'URL sans paramètre d'`/analysis`.
- **575-C · UN BANC QUI ÉCHOUE EST UNE MESURE** — l'arrêt sur `/options` est ce
  qui a révélé que cette page ne sert aucun script de page.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 8 programmes d'`/analysis/AAPL`, comptés et
relevés mais NON LUS** ; **les 38 sites du relevé structurel de ce lot** ; **les
9 vues d'`/options`, qui ne servent aucun script inline** ; **le plancher du
canal, à reprendre à ≥ 101** ; **les bannières, à reprendre à ≥ 18** ; **les 269
branches qui s'arrêtent sans rien dire** ; **les 14 sites « ailleurs » du 573** ;
**les 19 toasts d'erreur littéraux, non jugés** ; **les 6 toasts sans ton** ;
**`warn` et `warning`, non unifiés** ; **les 23 toasts `success`** ; **les 57
sites qui ne signalent pas un échec** ; **le total réel des signalements d'échec,
toujours inconnu** ; **les 27 appelés du relevé structurel du 570** ; **les 82
corps vides du 569, NON JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ; **les
63 `empty` distincts du 568** ; **les 42 refus du 567, non lus un par un** ;
**les 4 refus non-JSON du 542** ; **les 74 variables serveur sans atténuation** ;
**les 67 atténuations non affichées** ; **les 25 atténuations de la bibliothèque
tierce** ; **`/options|chips`** ; **`renderCalendar`** ; **les 4 limites
distinctes du 564** ; **les 12 signatures partagées du 562** ; **les 5 cas de
réponse absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10
cas non tranchés du 559** ; **les 16 sous-clés du 558** ; **les 5 chaînes nues** ;
**les 10 chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
candidates** ; **les 6 clés sans lecture observée** ; **les 26 routes à lectures
ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ;
**les 5 routes affamées du 556** ; **les 14 candidates du 554, en attente d'un
GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du
554/555** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly` rend un
objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 202 (+1)** ;
**publiés puis corrigés 37 (+1)** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
