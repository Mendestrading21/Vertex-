# SKYLER LOT 478 — 406 et 407 sont UN SEUL dossier, classé RANG 2 : deux clés du contrat de synchronisation que le produit LIT sans que RIEN ne les ÉCRIVE — trois `||0` en vivent, et la garde honnête est dix lignes plus bas

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-478` (base : lot 477 fusionné,
`0ab1e8b`)

Troisième dossier tiré des **seize jamais classés**. **Il ne corrige rien.**
Aucun fichier de production touché.

**Résultat de cadrage avant tout le reste : 406 et 407 ne sont pas deux dossiers,
c'en est UN.** Le classement passe donc de seize à quinze non classés **en en
traitant deux**.

## Le contrôle — réponse connue du lot précédent, et il passe

```text
attendu (mesuré au 477)   funnel.py:102-103 — les étages « Suivis » et « Positions »
                          avec int(followed or 0) / int(positions or 0)
mesuré                    :102 {'key':'followed','label':'Suivis','count': int(followed or 0)}
                          :103 {'key':'positions','label':'Positions','count': int(positions or 0)}
verdict                   CONTRÔLE PASSÉ
```

## Pourquoi ce dossier, et pourquoi les DEUX ensemble

Le 407 écrit lui-même, dans sa conclusion :

> « Deux lots de suite (406, 407) ont trouvé un défaut visible, et ils partagent
> **une seule cause** : deux clés du contrat de synchronisation que le produit lit
> sans jamais les écrire. »

**C'est exactement la leçon du 475 — compter les SOURCES, pas les fichiers.** Les
traiter séparément, ce serait compter deux fois une cause unique et gonfler le
classement. J'ai donc pris les deux, et **la mesure confirme la cause commune**.

Écartés : le **416** (légitime, mais je gardais une forme neuve en réserve), le
**391/396** (le réveil signale lui-même le risque de doublon avec le 463 déjà
classé), le **386+431** (critère déjà posé, donc moins de travail neuf).

---

# LA MESURE

## La cause, prouvée : deux clés lues, jamais écrites

```text
myCapital        DESK_KEYS   vx-entities.js:20 · system_page.py:920 · vx_kit.py:259 · journal.py (morte)
                 LECTURE     vx-entities.js:235   capital() { const c = get('myCapital', null); … }
                 ÉCRITURE    AUCUNE — grep setItem('myCapital' / set('myCapital' : 0 occurrence

myTradesEquity   DESK_KEYS   vx-entities.js:19 · system_page.py:919 · vx_kit.py:259 · journal.py (morte)
                 LECTURE     vx-entities.js:236   equity() { return get('myTradesEquity', []); }
                 ÉCRITURE    AUCUNE — 0 occurrence
```

**Les deux clés sont déclarées dans le contrat de synchronisation, lues par des
accesseurs dédiés, et aucune ligne du dépôt ne les écrit.** `capital()` rend donc
**toujours `null`**, `equity()` **toujours `[]`** — non pas dans un cas de bord,
mais **en permanence**.

## Les consommateurs — et le compte de SITES change le dossier

```text
portfolio_page.py:296   const cash = E().capital();                    → null
                 :200   const netValue = grossVal + (cash||0);         ← ||0  n°1
                 :208   const denom    = grossVal + (cash||0);         ← ||0  n°2
                 :718   cash: E().capital()||0                         ← ||0  n°3, envoyé au serveur
                 :586   const eq = (E()?E().equity():[])||[];          → []
                 :604   if(eq.length>=2 && …)  sinon emptyCard(…)      ← GARDE HONNÊTE
```

**Le 407 avait cité UN site — celui de l'API (`:718`). Il y en a TROIS.** Les
deux autres vivent dans `computeMetrics`, à huit lignes d'écart l'un de l'autre,
et ils alimentent la valeur nette **et** le dénominateur des poids.

**Leçon du 471/472 rejouée, et elle triple le dossier.**

## Le témoin positif est sur la même page, dix lignes plus bas

`:604` — `if(eq.length >= 2 …)` puis `emptyCard(host, reason, action)` avec un
motif et un bouton « Ouvrir le journal ». **Face à l'absence de `myTradesEquity`,
la page se tait honnêtement.** Face à l'absence de `myCapital`, elle écrit `0`.

**Même page, même cause, deux traitements opposés.** C'est le motif des 457, 476
et 477 — et c'est ce qui rend le classement possible : je n'accuse pas une
pratique absente du dépôt, je mesure **une pratique appliquée à un consommateur
sur deux**.

## Atteignabilité — prouvée par exécution

```text
GET /portfolio   « myTradesEquity » dans les octets servis : OUI
                 « capital() »      dans les octets servis : OUI
```

Les deux accesseurs et le libellé de source sont **dans les octets envoyés au
navigateur**. Le dossier est servi.

## Classement — RANG 2, et l'argument contre le rang 1 est solide

**Ce qui est établi** : la valeur nette et le dénominateur des poids sont
calculés en traitant un capital **inconnu** comme un capital **nul**, en
permanence, sur une page servie — alors que la même page sait se taire quand
l'autre clé manque.

**Pourquoi pas rang 1 — trois raisons, et la troisième est la plus honnête :**

1. **L'erreur va dans le sens PRUDENT.** Ignorer le cash **gonfle** les poids et
   la concentration : le produit sur-alerte au lieu de rassurer. Le critère posé
   au 431 — *une étiquette flatteuse compte, une étiquette conservatrice non* —
   joue ici **contre** le rang 1.
2. **`myCapital` n'est écrivable par personne.** Il n'existe aucun champ pour
   déclarer un capital. Le produit ne perd donc pas une donnée que l'utilisateur
   lui aurait confiée : **il n'a jamais offert de la recevoir.**
3. **Une lecture alternative tient debout, et je la publie** : si le capital
   n'est pas déclarable, alors « concentration entre les positions » est la seule
   grandeur calculable, et elle est **correcte**. Le défaut serait alors dans le
   **libellé** (qui laisse croire à une concentration du portefeuille total), pas
   dans le calcul. **Je ne tranche pas entre les deux lectures** — et le rang 2
   est le classement qui survit aux deux.

**Pourquoi pas rang 3** : c'est servi, c'est permanent, et le témoin de la
ligne 604 prouve que l'état honnête était disponible à dix lignes.

## Mutualisation — mesurée, et elle est FORTE

```text
portfolio_page.py porte déjà   457 (:266-268) · 461 (:221) · 432/433 (:231, :244, :398)
ce dossier ajoute              :200 · :208 · :718
```

**Le lot de travail C passe de trois à quatre dossiers dans le même fichier.**
Et une précision utile : `computeMetrics` (`:194-208`) est appelée en `:297`,
**juste avant** `dominantRisk` (`:298`) — la fonction que les dossiers 461 et
432/433 visent. **Les quatre dossiers du lot C tiennent dans une quinzaine de
lignes consécutives.**

---

# LE CHIFFRAGE

```text
CLIENT — vertex/ui/pages/portfolio_page.py
  :200  netValue = grossVal + (cash||0)   → distinguer cash null de cash 0        1 ligne
  :208  denom    = grossVal + (cash||0)   → idem                                   1 ligne
  :718  cash: E().capital()||0            → n'envoyer le champ que s'il existe     1 ligne
  + affichage : marquer « hors liquidités » quand cash est null                    1 ligne
                                                                          ─────────
                                                                   TOTAL   4 lignes
fichiers            1 · moteur touché : NON
```

**Variante alternative, plus ambitieuse et hors chiffrage** : l'option 2 que le
407 recommandait — **ouvrir un champ « capital / liquidités » dans le desk**.
Elle supprimerait la cause au lieu du symptôme et **réglerait aussi le volet
`myTradesEquity`**. Mais ce n'est pas un correctif de quatre lignes : c'est une
**fonctionnalité**, avec une clé à écrire, une saisie à créer, une synchronisation
à vérifier. **Je ne la chiffre pas** — je la nomme comme une décision de produit,
au même titre que les trois dossiers de décision du plan.

## Gardien et régression

```text
gardien       tests/test_capital_inconnu_lot4xx.py
assertion     quand `capital()` rend null, le dénominateur des poids ne vaut pas
              grossVal + 0 sans marque, et l'affichage porte une mention d'absence
échoue-t-il aujourd'hui ?   OUI — mesuré par lecture : trois `(cash||0)` / `||0`
              aux lignes 200, 208 et 718, aucune distinction entre null et 0
gardiens existants   `capital()` → 0 · `computeMetrics` → 0
                     `myCapital` → 3 et `myTradesEquity` → 2, MAIS uniquement dans
                     test_desk_keys_servies_lot381.py et test_production.py :
                     ils vérifient que les clés sont dans les LISTES de synchronisation,
                     PAS qu'elles soient écrites ni lues honnêtement
régression    aucun test ne touche computeMetrics ni capital(). Les 5 tests des clés
              portent sur les listes DESK_KEYS et ne seraient pas affectés.
              RISQUE FAIBLE — le plus bas des dix-neuf dossiers avec le 434 et le 427.
octet servi ?  OUI (/portfolio) → bump SW + 5 gardiens · _EMPREINTE NON
```

---

# LA FEUILLE DE DÉCISION — DIX-NEUF DOSSIERS

```text
avant ce lot   18 dossiers · 48 à 56 lignes · 18 gardiens · douze rang 1 · six rang 2
ce lot         +1 dossier (406+407 FUSIONNÉS, RANG 2) · +4 lignes · +1 gardien
après          19 DOSSIERS · 52 à 60 LIGNES · 19 GARDIENS · DOUZE RANG 1 · SEPT RANG 2
```

**Lot de travail C révisé — il devient le plus dense du plan :**

```text
C « /portfolio »   457 + 461 + 432/433 + 406/407   14 lignes · 1 fichier · 2 RANG 1
                   461 (:221) et 432/433 (:231) dans dominantRisk
                   406/407 (:200, :208) dans computeMetrics, appelée juste avant
                   → QUATRE dossiers dans une quinzaine de lignes consécutives
```

Les huit autres lots (A, B, D, E, F, G, H, I) sont **inchangés**.

## Ce qui reste hors devis

**Quinze dossiers jamais classés** (16 − 1, deux traités d'un coup) : 388 · 408 ·
409 · 411 · 426 · 416 · 422 · 391/396 · 379 · 363 · 386+431 · 452 (volet rang 2) ·
456+459 · 461 `winnerRule`. Plus les **trois dossiers de DÉCISION** (469, 468,
466/467) — **et désormais un quatrième candidat à la décision** : *faut-il ouvrir
un champ « capital » dans le desk ?*

## Ce que le lot ne prétend pas

- **Je n'ai pas rejoué les bancs des 406 et 407.** Le facteur « ×170 » du 407 est
  **son chiffre**, cité comme tel, et il provenait de positions **fabriquées pour
  la mesure**. Ce que **ce lot** mesure : l'absence totale d'écrivain, les **trois**
  sites `||0`, la garde honnête voisine, et la présence dans les octets servis.
- **Je n'ai pas tranché entre les deux lectures** (défaut de calcul ou défaut de
  libellé). Le rang 2 est choisi **parce qu'il survit aux deux**, et je le dis
  plutôt que de choisir la lecture qui donnerait le rang le plus élevé.
- **Je n'ai pas vérifié l'atténuation du 407** au sens du 477, parce qu'il n'en
  posait pas : il a publié trois options et une recommandation, sans minimiser.
  **C'est le premier des trois dossiers classés dont le rapport d'origine ne
  contient aucune phrase à démentir** — je le note, c'est à son crédit.
- **Aucun navigateur.** La présence à l'écran est établie sur les octets servis
  de `/portfolio`.
- **Aucun réseau. Aucun écrivain appelé. Aucun fichier de production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `persist` redirigé vers un `mkdtemp` **et la redirection
  vérifiée par `cache_path()`** ; **`/api/portfolio/team` NON appelée** (elle est
  en POST, hors du périmètre de lecture) ; **`/options/<sym>`, `/api/analyst/`,
  `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quatre-vingtième lot court, **troisième de la reprise de mesure**.

Trois lots, trois dossiers classés — **et celui-ci en a absorbé deux**. Le compte
des non classés tombe de dix-huit à quinze en trois lots, et le plan gagne un
dossier au lieu de deux : **la fusion est un gain de lisibilité, pas une perte de
contenu.**

Le fait de méthode du lot est double, et le second est le plus utile :

**(1)** *Le compte de sites a triplé le dossier.* Le 407 citait le `||0` de
l'API ; il y en a **trois**, et les deux autres sont dans le moteur de métriques
de la page, donc plus en amont. C'est la troisième fois (471, 472, 478) que
« compter les sites » change le chiffrage d'un facteur.

**(2)** *Un dossier peut être RÉDUIT par la mesure autant qu'aggravé.* J'ai
commencé ce lot en pensant tenir un rang 1 — un dénominateur faussé sur une page
de risque. Trois mesures l'ont ramené à un rang 2 : l'erreur va dans le sens
**prudent**, la clé n'est **écrivable par personne**, et une lecture alternative
rend le calcul **correct** avec un libellé fautif. **Aucune de ces trois
observations n'était dans le rapport d'origine, et les trois jouent contre moi.**

C'est le pendant exact de l'observation du 477 : *ce que la boucle publie de plus
fragile, ce sont les phrases par lesquelles elle minimise*. **La symétrie
s'impose : elle doit se méfier autant des phrases par lesquelles elle aggrave.**

Comptes séparés : résultats faux **arrêtés avant publication** **44** (+1, le
rang 1 que j'allais poser sans mesurer le sens de l'erreur) ; **publiés puis
corrigés** **6** ; **interprétations retirées** **3** ; re-localisation **0**.

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre dix-neuf
dossiers, douze de rang 1, pour 52 à 60 lignes.**
