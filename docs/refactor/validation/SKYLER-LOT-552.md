# SKYLER LOT 552 — Le contrat servi contre le contrat testé : **171 clés servies, 43 nommées et servies, 128 servies sans être nommées à ce niveau.** Et le serveur a désigné tout seul un défaut de mon compteur du 551

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-552` (base : lot 551 fusionné,
`dc571bb2`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(x)** — les lots 548 à 551 ont mesuré ce que la suite **vérifie**. Personne
n'avait vérifié l'inverse : **les champs que les tests nomment sont-ils ceux
que le serveur retourne ?** Périmètre strict : **23 routes JSON déjà vérifiées
sûres**, appelées en DÉMO. Aucune route neuve, aucun POST, aucun réseau
sortant.

## L'arrêt du lot — **le croisement a désigné le défaut tout seul**

Parmi les champs « nommés par un test » absents du premier niveau servi
figuraient `<`, `Fed`, `NVDA`, `fr`. Lecture :

```python
# tests/test_live_engine.py:144
assert len(j['items']) == 1 and 'Fed' in j['items'][0]['title']
```

**`'Fed'` est une sous-chaîne cherchée dans une FEUILLE DE CHAÎNE du JSON**,
pas un nom de champ. Le 551 avait corrigé `'x' in <corps texte>` — sa règle
**551-B** — mais **pas** `'x' in <feuille de chaîne JSON>` : la même faute, un
niveau plus bas. **C'est 551-C appliqué à moi-même : la leçon d'un lot ne se
porte pas toute seule.**

Mesuré plutôt que retiré à la main (**547-B**) :

```text
tests de membre sur une valeur JSON
   sur la RACINE (appartenance à un dictionnaire)          35   ← vrais champs
   sur un ACCÈS IMBRIQUÉ (dictionnaire OU chaîne)          21   ← AMBIGU
```

Les deux lectures existent réellement : `'vix' in d['dimensions']` est une
appartenance ; `'Fed' in j['items'][0]['title']` est une sous-chaîne.
**Conséquence sur le chiffre du 551 : les 388 champs sont une BORNE HAUTE ;
367 est le plancher** si les 21 ambigus étaient tous des sous-chaînes.

**Arrêtés avant publication : 173 → 174. Publiés puis corrigés : 24 → 25.**

## Ce que le serveur rend, mesuré en appelant

```text
23 routes JSON sûres appelées en DÉMO — toutes 200, toutes des objets
clés de premier niveau servies, total                      171
```

```text
/api/decision/AAPL          29        /api/system/status         12
/api/market/summary         18        /healthz                   11
/api/session/manifest       11        /api/committee-review       9
/api/skyler/calibration      9        /api/brief                  7
/api/live/status             7        /api/market/regime          6
/api/strategie               6        …                    /api/weekly  0
```

**`/api/weekly` rend un objet VIDE en DÉMO.** C'est l'une des cinq routes de
flux que le 550 avait relevées comme vérifiées au statut seul. Constat, non
arbitré.

## Le croisement

```text
clés de premier niveau SERVIES                             171
champs NOMMÉS par les tests sur ces routes                  76
NOMMÉS **et** SERVIS                                        43
servis mais NON NOMMÉS à ce niveau                         128
nommés mais ABSENTS du premier niveau servi                 33
```

**Le témoin positif tient** : `/api/session/manifest` rend bien les six clés
que `tests/test_continuity_session.py:67` exige — vérifié **en appelant**.

### Les 33 « nommés mais absents » — à comprendre, pas à accuser

Ils se lisent en deux familles :

- **des clés d'un niveau plus bas** — `/api/positions/state` nomme `action`,
  `current_price`, `decision`, `priority`… qui sont les clés **d'une
  position**, pas de la réponse ;
- **des artefacts de mon compteur** — les `<`, `Fed`, `NVDA`, `fr` de
  `/news-feed`, expliqués ci-dessus.

## Le mot que je n'emploie pas

Les **128** clés servies hors croisement sont dites **NON NOMMÉES**, jamais
« non testées ». Le 551 a listé ce que son compteur ne voit pas — champs
nommés dans une aide, compréhensions, boucles — et une clé peut être couverte
par une **forme**. **Le mot dit exactement ce qui est mesuré, rien de plus**
(550-B).

## Second contrôle (481) — ce qui n'est pas comparable

```text
clés IMBRIQUÉES servies (un niveau plus bas)               148
accès imbriqués comptés côté TESTS au 551                   85
```

**Ces deux nombres ne se comparent pas** : ni le même périmètre (23 routes
contre toute la suite), ni la même définition (**546-A**). Aucune conclusion
n'en est tirée. Aucune des 23 routes ne rend une liste au premier niveau.

## Ce que le dépôt fait bien, mesuré

- **Les 23 routes sûres répondent toutes 200 et rendent toutes un objet JSON**
  — aucune surprise de forme.
- **`/api/decision/<sym>` rend 29 clés de premier niveau** : la route de
  décision est aussi la plus riche.
- **Le contrat exigé par le test du manifeste est tenu en DÉMO**, six clés sur
  six.
- **Aucun champ nommé par un test n'est un pur fantôme** : les 33 s'expliquent
  par la profondeur ou par mon propre instrument.

## Portée — ce que ce lot NE dit PAS

- **23 routes sur 184.** Rien n'est extrapolé aux autres (**529-B**).
- **Le contrat mesuré est celui du mode DÉMO** : un champ conditionnel peut
  être absent ici et présent en réel.
- Le croisement porte sur le **premier niveau** ; les clés imbriquées ne sont
  pas croisées.
- **Aucun point d'entrée n'est qualifié** ; les 128 sont *non nommées*, pas
  *non testées*.
- **Aucune route neuve appelée, aucun navigateur, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **4 modifiés pendant le lot** (`ai_enrichment.json`, `daily_prev.json`, `desk_data.json`, `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Pour la première fois depuis le 547, **le défaut n'a pas été
trouvé par relecture de mon propre code, mais par confrontation au serveur** :
c'est le croisement lui-même qui a fait sortir `Fed` et `NVDA` d'une liste de
noms de champs.

Ce qu'il faut dire sans le maquiller : **j'ai corrigé au 551 une faute que je
venais de commettre, et j'en ai laissé la version profonde intacte.** `'x' in
<texte>` était traité ; `'x' in <feuille de chaîne JSON>` ne l'était pas. Le
chiffre publié — 388 — devient une **borne haute**, et je le dis ici plutôt que
d'attendre qu'un autre lot le découvre.

Trois règles neuves :

- **552-A · UN CROISEMENT AVEC LE SERVEUR RÉVÈLE LES DÉFAUTS DU CRIBLE** —
  `Fed` et `NVDA` dans une liste de noms de champs n'étaient visibles qu'en
  regardant ce que la route rend vraiment.
- **552-B · UNE FAUTE CORRIGÉE À UN NIVEAU SURVIT AU NIVEAU DU DESSOUS** —
  551-B traitait le corps texte, pas la feuille de chaîne d'un JSON.
- **552-C · « NON NOMMÉ » N'EST PAS « NON TESTÉ »** — le mot publié doit dire
  exactement ce que l'instrument mesure, ni plus, ni moins.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 21 tests de membre AMBIGUS du 551** ; **les
128 clés servies non nommées, sur 23 routes seulement** ; **`/api/weekly` rend
un objet vide en DÉMO — constat** ; **les 6 points d'entrée du 551 sans trace
de vérification de contenu** ; **les 15 points d'entrée vérifiés au statut seul
du 550, dont 5 routes de flux** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge` — en attente d'un GO** ; **les 4 zones sous attente sans
annonce du 545** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** ; **le
contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du 542** ;
**les 15 messages d'erreur sans pourquoi du 541** ; **les 95 atténuations non
affichées** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes »
du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 174 (+1)** ; publiés
puis corrigés **25 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
