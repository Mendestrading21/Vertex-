# SKYLER LOT 557 — **`Promise.allSettled` était invisible à trois de mes bancs** : la moitié de la « quatrième cellule » était un artefact, et le contrat non gardé passe de 19 à 35

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-557` (base : lot 556 fusionné,
`cb909907`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — les mesures
du 552 et le corpus JS du 553 sont sur disque.

## Le choix

**(cc)** — le 556 a exhumé une quatrième cellule : **8 clés qu'un test nomme et
que la page ne lit pas**. Symétrique exact du contrat non gardé. Question :
**sont-elles servies sans lecteur, ou lues sous une forme que le crible ne suit
pas ?**

## L'arrêt du lot — **la prémisse était fausse pour la moitié d'entre elles**

Avant de chercher ailleurs, j'ai relu le code de la page qui consomme
`/api/data-quality`. `vertex/ui/pages/system_page.py:680` :

```javascript
const [dqR,diagR,liveR]=await Promise.allSettled([
  VX.fetch('/api/data-quality',{ttl:30000}), … ]);
const dq=dqR.status==='fulfilled'?dqR.value:null;
…
if(dq&&dq.total>0){ … dq.total … dq.by_quality … dq.scan_source … }
```

**`total` est lue, au premier niveau.** Le 553, le 555 et le 556 ne la voyaient
pas : ils suivent `Promise.all` **positionnellement** mais ignorent
`Promise.allSettled`, dont chaque élément est une **enveloppe** `{status, value}`
déballée par `.value`.

Sur les 8 clés de la quatrième cellule, **4 sont bel et bien lues** : `total` et
`degraded` (`/api/data-quality`), `mode` et `domains` (`/api/live/status`).

**Et l'erreur allait encore dans le sens accusatoire** (548-A) : elle faisait
croire que le produit n'utilise pas ce qu'un test garde.

Le plus dur à écrire : **le second contrôle du 553 signalait déjà « 9 valeurs
parties dans un tableau et non suivies »**. Sept d'entre elles sont exactement
ces enveloppes `allSettled`. **Mon propre instrument imprimait le chiffre depuis
quatre lots, et j'ai publié des seaux comme si le tableau était complet.**

## Un second arrêt — un défaut que j'ai introduit dans ce lot même

En ajoutant la seconde forme du motif (`let a,b; [a,b] = await Promise.all(…)`,
employée à `system_page.py:320`), j'ai passé au résolveur de portée un **nœud
synthétique**, absent de la table des parents. `englobante` rendait alors `null`
— **c'est-à-dire la racine du programme**. La liaison couvrait tout le fichier
et fabriquait une **fausse collision** sur le nom `st`, qui a englouti **11
clés** de `/api/system-status`.

Le signal : les totaux ont **baissé** après un ajout qui ne pouvait
qu'augmenter. J'allais publier 11 points d'entrée et `A 22 · B 26 · C 27` ; le
vrai compte est 12 et `A 24 · B 35 · C 28`.

**Arrêtés avant publication : 180 → 182 (+2).**

## La mesure

```text
                                        553 (plat)   557 (portée + allSettled)
points d'entrée communs                       9            12
A · LUE par la page ET NOMMÉE par un test    17            24
B · LUE, NON NOMMÉE — contrat non gardé      19            35
C · ni lue ni nommée — CANDIDATE             20            28
D · NOMMÉE mais NON LUE                       5             6
total des clés servies de ces routes         61            93
```

Décomposition (556-C — on ne publie pas un total sans le défaire) :

```text
sur les 9 points d'entrée d'origine   A 19 · B 23 · C 16 · D 3
sur les 3 exhumés                     A  5 · B 12 · C 12 · D 3
   `/api/skyler/calibration` (556) · `/healthz` · `/api/system-status`
```

Comparé au 556 **sur le même périmètre de 9**, `allSettled` déplace exactement
quatre clés dans chaque sens : **A +4, B +4, C −4, D −4**, total conservé à 61.

**Le contrat non gardé passe de 19 à 35** — non parce que le dépôt a changé,
mais parce que trois de mes bancs successifs sous-comptaient. **Les « 19 clés »
publiées au 553 étaient un plancher.**

## Les corrections de chiffres publiés

- **553** : « 19 clés d'un contrat non gardé » sur 9 points d'entrée → **23** sur
  ces mêmes 9 points d'entrée.
- **556** : « 8 clés nommées et non lues » → **4** l'étaient réellement ; la
  cellule vaut **6** aujourd'hui, dont deux clés (`build`, `engines`) apportées
  par `/healthz`, qui vient seulement d'entrer dans le périmètre.

Les rapports 553 et 556 **ne sont pas réécrits** — la correction est portée ici,
en ajout.
**Publiés puis corrigés : 26 → 28 (+2).**

## Ce qui reste dans la quatrième cellule

```text
/api/skyler/calibration    generator
/api/market/summary        score · verdict
/api/session/manifest      generator
/healthz                   build · engines
```

**Six clés qu'un test nomme et dont aucune lecture n'a été observée.** Le mot
juste est **« sans lecture observée »**, pas « servie pour rien » (550-B) : il
reste 26 routes portant des lectures ambiguës, 35 accès imbriqués jamais nommés,
et les pages hors des huit ne sont pas dans ce corpus.

## Second contrôle (481) — ce que la lecture ne décide toujours pas

```text
enveloppes `Promise.allSettled` désormais suivies                7
valeurs `Promise.all` en forme d'AFFECTATION désormais suivies   2
   -> les 9 « valeurs non suivies » du 553 le sont toutes
collisions de nom restantes                                      4
   `d` ×3 (556) + `st` (/api/ai/status vs /api/system-status)
routes portant au moins une lecture AMBIGUË                     26
OMBRES — nom marqué, redéclaré dans une fonction imbriquée       3
appels `VX.fetch.peek` (enveloppe {data, age, ts})               8
```

La collision sur `st` est **réelle** : deux fonctions de `/system` emploient le
même nom local pour deux routes différentes. La contenance la tranche pour
l'essentiel — il ne reste que **2 clés ambiguës** de part et d'autre.

## Ce que le dépôt fait bien, mesuré

- **La page lit plus que je ne le croyais** : quatre clés que je donnais pour
  ignorées sont lues, et `/api/system-status` en lit **onze**.
- `/api/system-status` et `/api/system/status` **désignent le même point
  d'entrée** (vérifié dans `url_map`) : le produit emploie l'alias, j'avais
  mesuré l'autre — **aucune route nouvelle n'a été appelée**.
- **Le produit se protège** : `Promise.allSettled` + `status==='fulfilled'`
  signifie qu'une API en panne n'écroule pas la vue Système.
- Le total des clés servies est **conservé** sur le périmètre d'origine : les
  quatre cellules partitionnent, vérifié par assertion.

## Portée — ce que ce lot NE dit PAS

- **12 points d'entrée** : l'intersection entre les 23 routes mesurées au 552 et
  ce que les pages lisent. Le reste n'est pas mesuré.
- **Premier niveau uniquement**, des deux côtés (546-A).
- **Aucune des 6 clés restantes n'est déclarée inutile.**
- La portée reste **syntaxique** : ni ombre, ni hissage, ni fermeture.
- **Aucune route appelée, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0**.

Aucun dossier. Trois lots de suite ont corrigé le même instrument, et à chaque
fois le défaut poussait dans la même direction : **faire croire que le produit
lit moins, garde moins, utilise moins qu'il ne le fait.** Le 555 l'a dit, le 556
l'a nuancé, le 557 le confirme sur un quatrième mécanisme.

Mais le vrai reproche est ailleurs, et il m'est adressé : **mon second contrôle
imprimait « 9 valeurs non suivies » depuis le 553, et je ne suis pas allé
voir.** Un second contrôle n'a de valeur que si son chiffre non nul déclenche
quelque chose. Ici, il a mis quatre lots à le faire.

Trois règles neuves :

- **557-A · UN CHIFFRE NON NUL DU SECOND CONTRÔLE EST UNE DETTE, PAS UNE NOTE
  DE BAS DE PAGE** — « 9 valeurs non suivies » désignait précisément l'angle
  mort qui a faussé trois lots.
- **557-B · UN NŒUD SYNTHÉTIQUE N'A PAS DE PORTÉE** — passer un objet fabriqué
  à un résolveur qui interroge une table de parents rend « racine du
  programme », c'est-à-dire *tout le fichier*.
- **557-C · UN TOTAL QUI BAISSE APRÈS UN AJOUT EST UN SIGNAL D'ALARME** — un
  ajout de liaisons ne peut qu'augmenter la couverture ; la baisse a révélé le
  défaut avant publication.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 35 clés du contrat non gardé — constat, non
arbitré** ; **les 28 candidates** ; **les 6 clés sans lecture observée** ; **les
26 routes à lectures ambiguës** ; **les 4 collisions de nom** ; **les 35 accès
imbriqués jamais nommés** ; **les 3 ombres de `briefing.py`** ; **les 5 routes
affamées hors intersection du 556** ; **les 14 candidates du 554, en attente
d'un GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du
554/555** ; **les 21 tests de membre ambigus du 551** ; **les 128 clés servies
non nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6
points d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ;
**les 43 points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **les 95 atténuations non affichées** ; **`initSettings`** ;
**les 8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil
prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 182 (+2)** ; publiés
puis corrigés **28 (+2)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
