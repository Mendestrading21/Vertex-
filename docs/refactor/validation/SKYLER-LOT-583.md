# SKYLER LOT 583 — **mon attente était inversée** : `|| 0` porte deux fois plus souvent sur une **mesure** que sur un compte

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-583` (base : lot 582 fusionné,
`983add74`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(ccc)** — le 582 a trouvé **un** repli `|| 0` sur un âge. La règle 582-A ne vaut
que si l'on sait combien de fois le motif se répète : un défaut isolé est une
bévue, dix occurrences une habitude d'écriture.

Piège écrit **avant** de mesurer : *la grande majorité des `|| 0` porteront sur
des **comptes** (`length`, `count`), où 0 est la valeur honnête d'un ensemble
vide ; seule une poignée portera sur des grandeurs où 0 ment. **Si c'est vrai, le
582 est une exception, et il faut le dire aussi clairement que l'inverse.***

**Le piège est faux.** Et l'écart n'est pas marginal.

## La part tierce, isolée **avant** tout total (576-C)

```text
sites relevés (deux corpus, dédupliqués)   188
   dont `chart.umd.min.js` / `/vendor/`     52   (27,7 %)
   sites de PRODUIT                        136
```

Les noms tiers, lus, confirment l'isolement : `minRotation`, `borderWidth`,
`paddingLeft`, `autoSkipPadding`, `hoverOffset`, `startAngle`,
`actualBoundingBoxAscent`… — de la mise en page de graphique, pas des données.

## L'arrêt du lot — **mon classeur appariait par suffixe**

Mon premier classement rangeait **neuf** sites en « âge / horodatage ». Trois
d'entre eux étaient `puts` : la racine `'ts'` était testée avec `endswith`, et
`puts` finit par `ts`.

```text
âge / horodatage (classement automatique)   9
   dont `puts` — un compte d'options        3   ← faux positifs
```

Le même défaut menaçait les autres familles : la racine `'n'` apparie `position`,
`open`, `median` ; `'val'` apparie `interval` ; `'ts'` apparie encore `charts`,
`points`, `results`. **Un classement par racine avec `endswith` n'est pas une
mesure : c'est un devinement automatisé** — 521-B, mécanisé.

J'ai donc jeté le classeur et **lu les 136 noms**, comme au 574, avec
vérification de couverture exacte.

**Arrêtés avant publication : 209 → 210 (+1).**

## Les 136 replis de produit, **lus** par nature

```text
MESURE            52    prix, montant, score, pourcentage, exposition
                        → 0 est une VALEUR du domaine, pas une absence
COMPTE            35    nombre d'éléments → 0 est honnête pour un ensemble vide
TEMPS              6    âge ou horodatage → 0 signifie « à l'instant »
AUTRE / non nommé 43    expression, clef calculée, `Number()`, `getItem()`
                        → non classable par le nom
```

**Les comptes ne sont pas la majorité** : 35 sur 136, soit 26 %. La plus grande
famille nommée est **MESURE**, avec 52 sites :

```text
score ×10 · delta ×5 · call_gex ×5 · put_gex ×5 · confidence ×4 · value ×3
net_gex ×3 · quality ×2 · cost ×2 · cash ×2 · strike ×2 · max_loss ×2
pct_a50 · pct_a200 · brNum · advpct · capital() · top_weight_pct · maxAbs
```

## Les six sites « temps », lus un par un

```text
/portfolio      (now - (base.ts || 0)) > 43200000
/system         VX.fmt.ago((s.received_ts || 0) * 1000)
/system         assess({ ageMs: (man.age_s || 0) * 1000, … })   ← le dossier du 582
/system         VX.updateIndicator((r.ts || 0) * 1000, 'séquence de démarrage')
/analysis/AAPL  (Date.now()/1000 - (s.received_ts || 0)) <= 6*3600
/analysis/AAPL  VX.fmt.ago((s.received_ts || 0) * 1000)
```

**Aucun des six n'a de garde en amont.** Sur un horodatage, `|| 0` ne vaut pas
« maintenant » : il vaut **le 1ᵉʳ janvier 1970**. Selon l'usage, cela donne
« à l'instant » (`ago` d'un delta nul si l'on soustrait) ou une ancienneté
absurde — je ne tranche pas, je n'ai tracé la chaîne complète que sur **un** de
ces six, au 582.

## Ce que ce lot établit, et ce qu'il n'établit pas

**Établi** : **58 sites de produit** (6 temps + 52 mesure) appliquent un repli
numérique à une grandeur dont **0 est une valeur plausible du domaine**. Le motif
du 582 **n'est pas une exception** : c'est la forme dominante des replis nommés.

**Non établi** : qu'aucun de ces 58 soit un défaut. Un `|| 0` sur un score peut
être délibéré, ou la valeur peut ne jamais manquer. **Le 582 reste le seul dont
la chaîne serveur → client ait été lue aux deux bouts** — c'est ce qui en fait un
dossier, et pas ces 58.

## Second contrôle (481) — les replis écrits autrement

```text
formes `typeof/isNaN/isFinite … ? … : 0`   5
   toutes dans `chart.umd.min.js`          5
   dans du code de produit                 0
```

L'instrument ne voit que `||` et `??` : le relevé est un **plancher** (550-B).
Mais mesuré sur ce corpus, l'écart côté produit est **nul** — le dépôt écrit ses
replis numériques d'une seule façon.

## Ce que le dépôt fait bien, mesuré

- **Une seule forme de repli numérique dans tout le code de produit** : aucun
  `isNaN(x) ? 0 : x` ailleurs que dans la bibliothèque tierce.
- **35 replis sur des comptes** — l'usage légitime, et il est massif.
- **La part tierce est nettement séparable** : 52 sites, tous des propriétés de
  mise en page, aucun sur une donnée de marché.
- **Les trois quarts des `|| 0` de produit ne touchent pas au temps** : le
  problème du 582 est circonscrit à six sites, tous lisibles en une page.

## Portée — ce que ce lot NE dit PAS

- **La classification est une LECTURE**, pas une règle exécutable : elle est
  reproductible par relecture, et le programme n'en vérifie que la **couverture**
  (136 sur 136).
- Les **43 « autre / non nommé »** ne sont pas jugés : `None` (la gauche n'est
  pas un nom simple), `[calculé]`, `Number()`, `getItem()`.
- **Aucun des 58 n'est corrigé ni signalé comme défaut** ; seul le 582 l'est, et
  il attend un GO.
- Corpus du 541 et du 575 : **plancher**, DÉMO sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu**, une variable par objet ; aucun banc antérieur touché — **le classeur
  fautif reste tel quel**, c'est la preuve de l'arrêt.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- MD5 des 8 pages remesurés : **8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu
  ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
0**.

Aucun dossier neuf — **celui du 582 reste ouvert**.

Ce que je retiens : **j'ai écrit une attente confortable et la mesure l'a
retournée.** Je pensais trouver une majorité de comptes, où le zéro est honnête ;
j'ai trouvé deux fois plus de **mesures**, où le zéro est une valeur du domaine.
Le 582 n'était pas une bévue isolée : c'était le seul membre d'une famille de
cinquante-huit dont j'aie lu les deux bouts.

Et une leçon sur mes propres outils : **mon classeur automatique s'est trompé
exactement comme un humain pressé** — il a vu « ts » à la fin de « puts » et a
conclu. La parade n'était pas un meilleur classeur : c'était de **lire les
quatre-vingt-six noms** et de vérifier que la lecture couvre tout.

Trois règles neuves :

- **583-A · UN CLASSEUR PAR SUFFIXE EST UN DEVINEMENT AUTOMATISÉ** — la racine
  `ts` a rangé `puts` parmi les horodatages : **3 faux positifs sur 9**.
- **583-B · `|| 0` PORTE PLUS SOUVENT SUR UNE MESURE QUE SUR UN COMPTE** — 52
  contre 35 ; mon attente était exactement inversée.
- **583-C · UN REPLI N'EST PAS UN DÉFAUT TANT QUE LES DEUX BOUTS N'ONT PAS ÉTÉ
  LUS** — 58 sites de même forme, **un seul** dossier.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A + le dossier du 582**.

Dettes nommées restantes : **les 58 replis sur une grandeur où 0 est plausible,
NON tracés jusqu'au serveur** ; **les 43 « autre / non nommé »** ; **le `|| 0` de
`/system`, dossier ouvert en attente d'un GO** ; **les 5 autres sites « temps »
sans garde** ; **les quatre vocabulaires d'état, NON unifiés** ; **les trois
renommages nom → attribut** ; **le repli `['fallback', freshness]`** ;
**l'ambiguïté de `data-state=`** ; **les 3 branches de `_stateBody` qui ne
délèguent pas** ; **`VX.states.stale`, morte et NON supprimée** ; **les 73 appels
à `empty`** ; **les 30 appels à la fabrique d'erreur** ; **les 2 appels à
« identifiant nu »** ; **les 6 bannières qui relaient `e.message`** ; **le repli
« réponse indisponible »** ; **les 38 sites du relevé structurel neuf du 576** ;
**les 29 branches de produit de la borne (B) neuve** ; **le filtre `chart.umd`
des six instruments** ; **les 8 programmes d'`/analysis/AAPL`** ; **les 269
branches qui s'arrêtent sans rien dire** ; **les 14 sites « ailleurs » du 573** ;
**les 19 toasts d'erreur littéraux** ; **les 6 toasts sans ton** ; **`warn` et
`warning`** ; **les 23 toasts `success`** ; **les 57 sites qui ne signalent pas
un échec** ; **le total réel des signalements d'échec** ; **les 27 appelés du
relevé structurel du 570** ; **les 82 corps vides du 569** ; **les 18 gardes
portant un `VX.fetch`** ; **les 42 refus du 567** ; **les 4 refus non-JSON du
542** ; **les 74 variables serveur sans atténuation** ; **les 67 atténuations non
affichées** ; **les 25 atténuations de la bibliothèque tierce** ;
**`/options|chips`** ; **`renderCalendar`** ; **les 4 limites distinctes du
564** ; **les 12 signatures partagées du 562** ; **les 5 cas de réponse absents
du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10 cas non tranchés
du 559** ; **les 16 sous-clés du 558** ; **les 5 chaînes nues** ; **les 10
chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
candidates** ; **les 6 clés sans lecture observée** ; **les 26 routes à lectures
ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ;
**les 5 routes affamées du 556** ; **les 14 candidates du 554, en attente d'un
GO** ; **les 4 routes construites `/api/options/…`** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **`initSettings`** ; **les 8 appels
hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les 92 rapports non additionnés du 526** ; **les quinze lots exposés du 525** ;
**le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente
d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 210 (+1)** ;
**publiés puis corrigés 38** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Le 531-A
attend un GO. Et le dossier du 582 — le `|| 0` de `/system` — attend un GO.**
