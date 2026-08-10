# SKYLER LOT 553 — Le contrat de la page : **19 clés que le produit LIT et qu'aucun test ne nomme** — dont `vix`, `breadth`, `regime` et `confidence`

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-553` (base : lot 552 fusionné,
`6dbdd730`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(y)** — le 552 a mesuré **128 clés servies que la suite ne nomme pas**. La
question suivante est la seule qui compte pour l'utilisateur : **le JavaScript
du produit, lui, les lit-il ?** Une clé lue par la page sans qu'aucun test ne
la nomme est un **contrat non gardé** : le jour où le serveur la renomme, la
page casse et la suite reste verte.

Trois seaux écrits **avant** de mesurer, et le troisième porte un nom
volontairement faible : **candidate**, jamais « morte » (**550-B**, **552-C**).

## La mesure

```text
corpus : le JS SERVI des 8 pages
   programmes analysés                    41      octets   798 883
   erreurs d'analyse                        0
   routes atteintes par un `VX.fetch`      36
points d'entrée à la fois SERVIS (552) et LUS par une page   9
```

```text
sur les 56 clés servies de ces 9 points d'entrée
   LUE par la page ET NOMMÉE par un test                     17
   LUE par la page, NON NOMMÉE — contrat non gardé           19
   ni lue ni nommée — CANDIDATE, rien de plus                20
```

## Les 19 clés d'un contrat non gardé

```text
/api/market/summary     breadth · regime · roro · roro_gap · vix · vix_band · vix_chg
/api/market/regime      confidence · dimensions_used · secondary
/api/session/manifest   age_s · as_of · scanned · source
/api/opportunities/funnel  actionable_symbols · note
/api/positions/alerts   active
/api/live/status        demo
/api/data-quality       note
```

**Sept d'entre elles portent le climat de marché** — `vix`, `vix_band`,
`vix_chg`, `breadth`, `regime`, `roro`, `roro_gap` — et trois autres la
confiance du moteur de régimes. Ce sont exactement les valeurs que
`briefing.py` verse dans l'objet Regime Aura et dans les tuiles du premier
écran. **Un renommage côté serveur passerait la suite au vert et viderait le
haut de la page d'accueil.**

**Ce constat n'est pas arbitré et n'entre pas dans le relevé.** Il est borné à
**dix-neuf clés sur neuf points d'entrée**, et **rien n'est corrigé** — écrire
un test est une modification de production, qui demande un GO.

## Les 20 « candidates » — le mot est choisi

`best_sector`, `indices`, `market`, `market_verdict`, `spy`, `scan_age`,
`universe`, `errors`, `ibkr`, `last_refresh`, `notes`, `new`, `updated`… **Le
mot « morte » n'est pas employé.** Une clé de ce seau peut être lue par un
accès construit, par une destructuration, ou sur une page hors des huit —
et le second contrôle ci-dessous chiffre exactement ce que le crible laisse
passer.

## Un défaut d'instrument, corrigé — sans effet sur les chiffres publiés

Ma première version rangeait en « valeur partie dans un tableau » les
`VX.fetch` d'un `Promise.all`, sans jamais les suivre. Lu dans
`briefing.py:280` :

```javascript
const [r,sum,ed]=await Promise.all([
  VX.fetch('/api/market/regime',{ttl:120000}),
  VX.fetch('/api/market/summary',{ttl:60000}).catch(()=>({})), …]);
…  grammar={roro:(sum&&sum.roro)||null, breadth:…, vix:num(sum&&sum.vix)};
```

L'appariement est **positionnel**, donc décidable : il a été ajouté. **Effet
mesuré sur les trois seaux : aucun** — les mêmes clés étaient déjà lues sur une
autre page ; seuls les compteurs du second contrôle bougent (accès imbriqués
34 → 35, valeurs non suivies 10 → 9). **La valeur publiée étant inchangée, ce
n'est pas compté comme un arrêt** — même règle qu'au 550.

**Aucun arrêt dans ce lot.** C'est le premier depuis le 540.

## Second contrôle (481) — ce que le crible ne voit pas

```text
accès CONSTRUITS sur une valeur de route                       0
valeurs parties dans un tableau et non suivies                 9
accès IMBRIQUÉS (non comparables au premier niveau)           35
```

Le **zéro** d'accès construits mérite d'être dit sans être confondu : le 536
avait compté **132 accès non littéraux**, mais **sur des identifiants du DOM**,
pas sur des valeurs de route — **deux prédicats différents** (546-A). Ici, sur
les valeurs issues d'un `VX.fetch`, **le produit n'utilise que des noms
littéraux**.

## Ce que le dépôt fait bien, mesuré

- **Zéro accès construit sur une valeur de route** : tout ce que la page lit
  d'une réponse est nommé en clair, donc mesurable.
- **41 programmes servis, zéro erreur d'analyse** — le JS servi est
  intégralement analysable.
- **17 clés sur 56 sont gardées des deux côtés** : la page les lit et un test
  les nomme.
- **La page se protège** : `(sum&&sum.roro)||null`, `num(sum&&sum.vix)` — les
  lectures passent par des gardes, une clé disparue ne jette pas d'exception.

## Portée — ce que ce lot NE dit PAS

- **9 points d'entrée seulement.** Les pages appellent **36 routes** ; je n'en
  ai appelé que 23 au 552, et l'intersection fait 9. Le reste n'est pas mesuré.
- **Premier niveau uniquement**, des deux côtés, pour rester comparable
  (546-A).
- **Les 8 pages seulement** : `/analysis/<symbole>` et les pages hors corpus ne
  sont pas dans ce crible.
- **« Contrat non gardé » décrit un fait mesuré**, pas un défaut arbitré : la
  clé peut être couverte par une forme ou par une aide que le 551 a listées
  comme invisibles.
- **Aucun appel de route neuve, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : **8 / 8 identiques****
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés pendant le lot** (`ai_enrichment.json`, `daily_prev.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Mais la chaîne commencée au 548 se referme : on sait qui
**appelle** (548, 549), avec quelle **profondeur** (550), sur quelle
**étendue** (551), contre quel **contrat servi** (552), et enfin **ce que le
produit lit vraiment** (553).

Ce qu'il faut dire sans le maquiller : **pour la première fois depuis douze
lots, je n'ai pas eu à publier d'arrêt.** Un défaut d'instrument a bien été
trouvé et corrigé — le `Promise.all` non suivi — mais il ne changeait aucun
chiffre publié, et le dire autrement serait me donner un mérite que je n'ai
pas eu.

Trois règles neuves :

- **553-A · UN CONTRAT NON GARDÉ EST UN FAIT MESURABLE** — dix-neuf clés que la
  page lit et qu'aucun test ne nomme, dont le climat de marché entier.
- **553-B · UN DÉFAUT CORRIGÉ SANS EFFET N'EST PAS UN ARRÊT** — le
  `Promise.all` non suivi laissait les trois seaux inchangés ; le compter
  serait gonfler mon propre bilan.
- **553-C · UN ZÉRO SE LIT DANS SON PRÉDICAT** — zéro accès construit *sur une
  valeur de route* ne contredit pas les 132 accès non littéraux du 536, qui
  portaient sur des identifiants du DOM.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 19 clés d'un contrat non gardé — constat, non
arbitré** ; **les 20 candidates du troisième seau** ; **les 27 routes appelées
par les pages que je n'ai jamais appelées moi-même** ; **les 21 tests de membre
ambigus du 551** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly`
rend un objet vide en DÉMO** ; **les 6 points d'entrée du 551 sans trace de
vérification de contenu** ; **les 15 points d'entrée vérifiés au statut seul du
550** ; **les 43 points d'entrée couverts par personne** ; **les 11 identifiants
de `/intelligence`, `/tracking` et `pf-risk-gauge` — en attente d'un GO** ;
**les 4 zones sous attente sans annonce du 545** ; **les SEPT chiffres lourds
encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les
4 noms de clé du 542** ; **les 15 messages d'erreur sans pourquoi du 541** ;
**les 95 atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors
de toute fonction** ; **les 36 accès DOM non suivis** ; **la définition du
corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés
du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ;
**les 92 rapports non additionnés du 526** ; **les quinze lots exposés du 525** ;
**le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente
d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 174 (+0)** ; publiés
puis corrigés **25** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
