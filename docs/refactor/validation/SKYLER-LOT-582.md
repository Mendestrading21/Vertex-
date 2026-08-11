# SKYLER LOT 582 — **le serveur dit « je ne sais pas », un client répond « à l'instant »** — premier dossier depuis quarante-neuf lots

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-582` (base : lot 581 fusionné,
`508ebfed`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(bbb)** — le 581 a mesuré la fonction `assess` ; il n'a pas mesuré **ses
entrées**. La promesse « donnée réelle » ne tient que si `ageMs` est un âge réel.

Piège écrit **avant** de mesurer : *le site `/system` porte `(man.age_s||0)*1000`
— un `|| 0` sur un âge. Si `age_s` est absent, l'âge devient 0 ms, donc
« Live » : l'inverse exact du `—` honnête que le même module écrit trois lignes
plus haut. **À vérifier, pas à supposer** — un garde en amont peut rendre le cas
impossible.*

**Le piège avait la bonne direction et le mauvais libellé.**

## Les quatre sites, lus en entier

```text
/markets        ageMs = (typeof scan.scan_age === 'number') ? scan.scan_age*1000 : null
/opportunities  ageMs = (pk && pk.data && typeof pk.data.age_s === 'number')
                        ? pk.data.age_s*1000 : null
/portfolio      ageMs = (pk && pk.data && typeof pk.data.age_s === 'number')
                        ? pk.data.age_s*1000 : null
/system         ageMs = (man.age_s || 0) * 1000
```

**Trois sites sur quatre emploient le même idiome honnête** : une **garde de
type**, et `null` en cas d'échec — c'est-à-dire exactement l'entrée qui déclenche
la branche `—` mesurée au 581.

Le quatrième emploie un **repli**. Et un repli n'est pas une garde : `null || 0`
vaut **0**, pas `null`.

## Ce que le serveur envoie — lu dans le code, pas supposé

```python
# vertex/engines/session_snapshot.py:59
'age_s': (round(time.time() - ts)
          if isinstance(ts, (int, float)) and not isinstance(ts, bool) else None),
```

**Le serveur renvoie `None` quand il ne connaît pas l'âge.** C'est délibéré : la
route voisine porte le commentaire, mot pour mot —

```python
# vertex/app/routes/session_api.py
# HONNÊTETÉ : l'âge figé au build sous-estimerait la vraie ancienneté d'un
# instantané restauré […]. On l'efface → le client n'affiche que l'horodatage
# absolu `as_of`, jamais un âge faussement frais.
restored['age_s'] = None
```

**Le serveur efface l'âge pour ne pas mentir. Le client le remplace par zéro.**

## L'arrêt du lot — **« Analyse », pas « Live »**

J'allais publier « donc Live ». L'appel de `/system` ne passe **pas** `live` :

```javascript
const fr = (VX.freshness && man)
  ? VX.freshness.chip(VX.freshness.assess({ ageMs:(man.age_s||0)*1000,
      offline: net==='offline', error: man.error, refreshing: man.status==='analyzing' }))
  : '';
```

Sans `live`, `assess` saute la branche `live` et tombe dans
`0 < 1 800 000 → snapshot`, **libellé « Analyse »**. La direction du piège était
juste — le libellé, faux.

**Arrêtés avant publication : 208 → 209 (+1).**

## Le dossier, délimité exactement

**Ce qui est certain, mesuré aux deux bouts** : sur `/system`, la branche `—`
d'`assess` est **inatteignable par construction**. Un âge inconnu ne peut pas y
produire le tiret honnête, parce qu'il n'arrive jamais comme `null`.

**Ce qui dépend de l'état**, l'ordre de décision étant `offline → error →
refreshing → saved → ageMs == null → live → snapshot → stale` :

```text
man == null (manifeste injoignable)   → le garde `(VX.freshness && man) ? … : ''`
                                        rend une chaîne VIDE — honnête
status == 'analyzing' (démarrage      → `refreshing` passe AVANT l'âge
à froid)                                → « Recalcul… » — honnête
âge nul, ni offline, ni error,        → 0 ms → `snapshot` → **« Analyse »**
ni analyzing                            pour un âge que le serveur dit ignorer
```

**L'ordre de décision masque le défaut sans le corriger** : il rétrécit la
fenêtre, il ne la ferme pas.

## Second contrôle (481) — les appels qui court-circuiteraient l'ordre

```text
appels à `chip()` SANS passer par `assess()`   0
```

**Aucun.** Tout affichage de fraîcheur passe par l'ordre de décision ; personne
ne fabrique un état à la main.

## Ce que le dépôt fait bien, mesuré

- **Trois sites sur quatre gardent l'ignorance** : `typeof … === 'number' ? … :
  null` — la seule forme qui laisse la branche `—` atteignable.
- **Le serveur efface un âge qu'il ne peut pas garantir**, avec un commentaire
  qui dit pourquoi. L'intention d'honnêteté est écrite, pas seulement respectée.
- **Le garde `(VX.freshness && man)`** : manifeste injoignable → **rien**, plutôt
  qu'une puce fausse.
- **`refreshing` passe avant l'âge** : au démarrage à froid, l'utilisateur lit
  « Recalcul… », pas une fraîcheur inventée.
- **Zéro `chip()` hors ordre de décision.**

## Portée — ce que ce lot NE dit PAS

- **Le libellé « Analyse » n'a pas été observé à l'écran** : il est déduit de
  l'ordre de décision lu au 581 et des entrées lues ici. Ce qui est **mesuré**,
  c'est que la branche `—` est inatteignable sur ce site.
- **Rien n'est corrigé.** Le `|| 0` reste tel quel : sa correction est une
  décision humaine.
- **Ma remontée aux déclarations ne résout pas la portée** : `/opportunities`
  porte **quatre** liaisons du nom `a` (dont `a = chart.chartArea`) ; la bonne a
  été identifiée **par son contenu** (`age_s`), pas par une analyse de portée.
  Limite d'instrument déclarée (547-B), même famille que 549-A.
- Corpus du 541 : **plancher**, DÉMO sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu**, une variable par objet ; aucun banc antérieur touché. **Aucun nom
  recopié depuis le brief** (581-A) : les noms de propriété sont lus dans l'AST.
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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1**.

**Un dossier — le premier depuis quarante-neuf lots.**

Ce que je retiens : **quarante-neuf lots à mesurer des instruments, et le seul
dossier arrive quand j'ai enfin suivi une donnée d'un bout à l'autre.** Le 581 a
lu la fonction et l'a trouvée juste ; ce lot a lu **ce qu'on lui donne**, et le
défaut est là — pas dans la logique, dans l'entrée. Un module peut être
parfaitement écrit et rester contredit par un seul caractère chez son appelant.

Et la chaîne est complète des deux côtés : le serveur écrit `None` **avec un
commentaire expliquant qu'il refuse de mentir**, et le client écrit `|| 0` à
trois pages de là. Aucun des deux n'a tort isolément. C'est la jonction qui
casse.

Trois règles neuves :

- **582-A · UN REPLI `|| 0` SUR UN ÂGE REND UNE BRANCHE D'HONNÊTETÉ
  INATTEIGNABLE** — le serveur renvoie `null` pour dire « je ne sais pas » ;
  `null || 0` dit « à l'instant ».
- **582-B · UNE GARDE DE TYPE N'EST PAS UN REPLI** — `typeof x === 'number' ?
  x*1000 : null` préserve l'ignorance, `(x||0)*1000` la détruit. Trois sites sur
  quatre font le premier.
- **582-C · L'ORDRE DE DÉCISION PEUT MASQUER UN DÉFAUT SANS LE CORRIGER** —
  `refreshing` passe avant l'âge et sauve le démarrage à froid ; la fenêtre
  rétrécit, le défaut reste.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A**, **plus celui-ci**.

Dettes nommées restantes : **le `|| 0` de `/system`, CONSTATÉ et NON corrigé — en
attente d'un GO** ; **le libellé effectif, déduit et non observé à l'écran** ;
**les quatre vocabulaires d'état, coexistants et NON unifiés** ; **les trois
renommages nom → attribut** ; **le repli `['fallback', freshness]`** ;
**l'ambiguïté de `data-state=` entre trois familles** ; **les 3 branches de
`_stateBody` qui ne délèguent pas** ; **`VX.states.stale`, morte et NON
supprimée** ; **les 73 appels à `empty`** ; **les 30 appels à la fabrique
d'erreur** ; **les 2 appels à « identifiant nu »** ; **les 6 bannières qui
relaient `e.message`** ; **le repli « réponse indisponible »** ; **les 38 sites
du relevé structurel neuf du 576** ; **les 29 branches de produit de la borne (B)
neuve** ; **le filtre `chart.umd` des six instruments** ; **les 8 programmes
d'`/analysis/AAPL`** ; **les 269 branches qui s'arrêtent sans rien dire** ; **les
14 sites « ailleurs » du 573** ; **les 19 toasts d'erreur littéraux** ; **les 6
toasts sans ton** ; **`warn` et `warning`** ; **les 23 toasts `success`** ; **les
57 sites qui ne signalent pas un échec** ; **le total réel des signalements
d'échec** ; **les 27 appelés du relevé structurel du 570** ; **les 82 corps vides
du 569** ; **les 18 gardes portant un `VX.fetch`** ; **les 42 refus du 567** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 209 (+1)** ;
**publiés puis corrigés 38** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Le 531-A
attend toujours un GO. Et ce lot en ajoute un : le `|| 0` de `/system`, dont la
correction tient en une garde de type — mais que je ne toucherai pas sans GO.**
