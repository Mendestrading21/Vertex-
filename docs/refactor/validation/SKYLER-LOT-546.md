# SKYLER LOT 546 — **Les « 72 identifiants jamais servis » n'existent pas : 51 des 72 SONT servis.** Le chiffre était un écart de définition, hérité du 544 et repris par le 545. Ce qui reste : 21 identifiants, deux pages routées jamais mesurées, ZÉRO code mort

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-546` (base : lot 545 fusionné,
`6585b7b3`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(o)** — le 545 a laissé **72 identifiants à squelette « encore jamais
servis »**. Trois hypothèses, qui ne se valent pas : d'autres pages jamais
appelées, une condition serveur, ou **du code mort**. La question : de quel
fichier viennent-ils, et lesquels appartiennent à un module que CLAUDE.md
déclare sans consommateur ?

## Premier arrêt — **le témoin du brief est faux pour la DEUXIÈME fois de suite**

Le brief exigeait : « au moins un des 72 doit venir de `vertex/ui/journal.py`
ou d'un autre module déclaré SANS CONSOMMATEUR ». Vérification au code, avant
d'écrire une ligne d'instrument :

```text
occurrences de `vx-skeleton`
   vertex/ui/journal.py       0      vertex/ui/options_lab.py   0
   vertex/ui/vault.py         0      vertex/ui/signals.py       0
   vertex/ui/strategy_os.py   0
```

**Les cinq reliques nommées dans CLAUDE.md ne portent AUCUN squelette.** Elles
ne peuvent contribuer à aucun des 72. Le brief a fabriqué un lien qui n'existe
pas. Témoin remplacé par `vx-trk-chart`, **lu dans le code**.

## Second arrêt — **et il annule le chiffre lui-même**

En listant les 72 par fichier, deux noms ont sauté aux yeux : **`vx-hero` et
`vx-demo-banner`**, que CLAUDE.md cite comme présents sur `/`. Un identifiant
« jamais servi » qui est cité comme servi : il fallait ouvrir les octets.

```text
les 72 « orphelins », confrontés aux octets servis des 44 URL
   SERVIS comme identifiant, sans `vx-skeleton` dans les octets      51
   RÉELLEMENT absents des octets servis                              21
```

**51 des 72 sont servis.** La cause, lue dans `briefing.py` :

```text
id="vx-hero" … puis, 197 caractères plus loin :
   <div id="vx-brief-body">%%LOADING%%</div>
```

Le critère côté source — *un `id=` suivi, dans les 400 caractères, de
`vx-skeleton` ou `%%LOADING%%`* — **attribue à `vx-hero` le squelette de son
VOISIN**. Ce n'est pas un compte de conteneurs : c'est une **heuristique de
proximité**.

**Conséquence, dite sans la maquiller** : les **150** et les **87 « jamais
servis »** publiés au 544, puis le **72** publié au 545, reposent tous sur ce
critère de proximité. **L'arithmétique était juste ; l'étiquette
« jamais servis » était fausse.** Les rapports 544 et 545 restent tels qu'ils
ont été publiés — l'historique n'est pas réécrit — et la correction est ici.

**Le 63, lui, tient** : il a été mesuré sur les octets servis par deux chemins
indépendants (544) et ne dépend d'aucune fenêtre.

**Arrêtés avant publication : 164 → 166. Publiés puis corrigés : 22 → 23.**

## Ce qui reste vraiment : 21 identifiants, et ils ont une adresse

```text
                                        absents   servis sans squelette
vertex/ui/pages/intelligence_page.py        15            0
vertex/ui/pages/tracking_page.py             5            1
vertex/ui/pages/portfolio_page.py            1            1
vertex/ui/pages/system_page.py               0           16
vertex/ui/pages/options_intel_page.py        0           13
vertex/ui/pages/markets_page.py              0            8
vertex/ui/pages/briefing.py                  0            6
vertex/ui/pages/analysis_page.py             0            4
vertex/ui/pages/performance_page.py          0            3
vertex/ui/pages/opportunities_page.py        0            1
                                            21           51
```

Les 21 se répartissent en **exactement trois cas** :

- **15** viennent de `intelligence_page.py`, servi par `@bp.route('/intelligence')`
  (`redesign.py:116`) ;
- **5** viennent de `tracking_page.py`, servi par `@bp.route('/tracking')`
  (`redesign.py:138`) ;
- **1** est `pf-risk-gauge` — celui-là même que le 544 avait démasqué : il vit
  **dans une chaîne JavaScript** de `/portfolio`, donc dans aucun octet servi
  comme DOM (**544-A**).

## L'hypothèse « code mort » est RÉFUTÉE

```text
fichiers portant un des 72             10
   importés par un module de routes    10   (tous par `vertex/app/routes/redesign.py`)
   SANS AUCUN IMPORTEUR                 0
```

**Aucun fichier orphelin. Aucun code mort.** Les deux pages qui portent les 20
identifiants réellement absents sont **routées et vivantes** ; elles n'ont
simplement **jamais été dans mon corpus**.

## Second contrôle (481) — ce que la lecture de source ne peut pas décider

```text
règles d'URL dans l'application                   190
   dont GET, hors `static`                        175
      dont SANS paramètre                         137
pages du corpus des 43 URL                          8
routes GET sans paramètre HORS corpus             129
```

**L'absence de service dans mon corpus n'est PAS une preuve de mort** — le 545
vient de le prouver : `/analysis/<symbole>`, jamais appelée jusque-là, sert 15
identifiants parfaitement vivants. **Mon corpus couvre 8 routes GET sans
paramètre sur 137.** Ce lot ne mesure pas les 129 autres : `/intelligence` et
`/tracking` ne sont pas dans la liste des routes vérifiées sûres, et **je ne
les appelle pas sans GO**.

## Ce que le dépôt fait bien, mesuré

- **Zéro fichier de page orphelin** : les dix fichiers portant un squelette
  sont tous importés par le même module de routes.
- **Les cinq reliques de CLAUDE.md ne portent aucun squelette** : quel que soit
  leur sort, elles ne laissent aucune barre de chargement derrière elles.
- **Deux pages entières du produit existent, routées, et n'ont jamais été
  auditées** — ce n'est pas un défaut du produit, c'est un défaut de mon
  corpus, et il est maintenant chiffré : **8 routes mesurées sur 137**.

## Portée — ce que ce lot NE dit PAS

- **Il ne dit pas que les 21 sont sans chargeur.** Il dit qu'ils ne sont pas
  servis par les 44 URL mesurées. Mesurer `/intelligence` et `/tracking`
  demande un GO.
- **Il ne dit pas que les 51 sont bien annoncés.** Il dit que leur identifiant
  est servi et que le squelette compté côté source appartenait à un voisin.
- Le critère de proximité (400 caractères) **reste utilisé** pour rester
  comparable au 544 ; sa limite est désormais mesurée, pas supposée.
- L'attribution « importé par un module de routes » est **statique** : un
  import n'est pas une preuve d'exécution.
- **Aucun appel réseau, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans chaque banc.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés pendant le lot** (`ai_enrichment.json`, `daily_prev.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Mais **une dette nommée pendant deux lots vient de se dissoudre
sous la mesure**, et ce qui la remplace est plus petit, plus précis, et
adressable : deux pages routées jamais auditées.

Ce qu'il faut dire sans le maquiller : **j'ai transporté un chiffre faux sur
deux lots.** Le 544 a écrit « 87 jamais servis », le 545 a fait « 87 → 72 », et
aucun des deux n'avait ouvert les octets pour vérifier que ces identifiants
étaient bien absents. Ce n'est pas le calcul qui était faux : c'est le mot
« servis », employé pour deux prédicats différents. **Deux mesures qui ne
définissent pas la même chose ne se soustraient pas.**

Trois règles neuves :

- **546-A · DEUX PRÉDICATS DIFFÉRENTS NE SE SOUSTRAIENT PAS** — « id proche
  d'un marqueur, côté source » moins « conteneur à squelette, côté servi » ne
  donne pas « jamais servi ». Il donne un artefact.
- **546-B · UNE FENÊTRE DE N CARACTÈRES ATTRIBUE LE VOISIN** — `vx-hero` porte
  le `%%LOADING%%` de `vx-brief-body`, 197 caractères plus loin.
- **546-C · UN NOM CONNU DANS UNE LISTE D'INCONNUS EST UNE ALARME** — c'est
  `vx-hero`, cité par CLAUDE.md, qui a fait ouvrir les octets.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **`/intelligence` et `/tracking`, deux pages routées
jamais mesurées — 20 identifiants, en attente d'un GO** ; **les 4 zones sous
attente sans annonce du 545 — candidat, non arbitré** ; **129 routes GET sans
paramètre hors corpus** ; **les SEPT chiffres lourds encore NON RECOMPTÉS**
(112 atténuations, 103 états, 53 refus, 178 appels, 156 variables serveur, 25
fonctions, 11 limites) ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les
4 noms de clé du 542** ; **les 15 messages d'erreur sans pourquoi du 541** ;
**les 95 atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors
de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes —
outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 166 (+2)** ; publiés
puis corrigés **23 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
