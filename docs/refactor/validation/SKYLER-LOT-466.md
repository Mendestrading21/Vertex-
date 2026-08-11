# SKYLER LOT 466 — Les routes qui travaillent pour personne : entre 22 et 37 des 189 règles déclarées n'ont aucun consommateur atteignable, et 15 d'entre elles ne sont citées que depuis du JS de `terminal.py` qui n'atteint plus aucune page

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-466` (base : lot 465 fusionné,
8532868)

Quarante-sixième lot de la veine, sixième de la tranche 460-469. Le 465 a nommé
une forme neuve et féconde — **du code complet et correct qui n'est pas servi**.
Ce lot attaque la classe entière : **les routes déclarées dont personne
n'appelle l'URL.**

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Une **ROUTE ORPHELINE** est une règle d'`app.url_map` qu'aucun consommateur ne
peut atteindre. Trois classes à distinguer d'avance — sinon on compte mort ce
qui vit : **K1** l'URL apparaît dans l'un des 42 objets servis · **K2** un autre
module serveur l'appelle · **K3** c'est une page que la navigation atteint.

**La règle d'appariement, et c'est elle qui décide de tout** : une règle
paramétrée (`/api/skyler/<sym>`) n'apparaît **jamais** littéralement dans les
octets servis — le client la construit par concaténation. L'appariement se fait
donc sur le **préfixe statique** jusqu'au premier `<`. **Sans cette règle, toute
route paramétrée serait faussement orpheline.**

## Trois corrections d'instrument — la première attrapée par le contrôle, les deux autres par la lecture

**(1) Le contrôle obligatoire a échoué au premier tir**, et c'est exactement à
cela qu'il sert. `/api/alerts/status` — l'orpheline **connue** du 465 — ressortait
« K2 serveur interne ». Cause : **`vertex/ui/**.py` sont du code Python, mais
leur contenu est du JS destiné au CLIENT.** Une URL citée là n'est pas un appel
serveur ; son seul citateur était `vx_kit.py`, non servi. Corpus K2 corrigé.

**(2) Il manquait une quatrième classe.** Douze règles ressortaient orphelines
alors qu'elles ne font qu'un `redirect(…, 301)` vers une page vivante
(`LEGACY_REDIRECTS`). **Leur non-citation est leur raison d'être** : elles
servent les favoris et les liens externes que le produit n'émet plus. Les classer
mortes était une faute. → **K4 redirection de compatibilité**. Et `/readyz`
rejoint `/healthz` en infrastructure — ma propre liste d'exclusion était
incohérente.

**(3) La correction (1) était incomplète, et `/news-feed` l'a montré.**
`terminal.py` est **à la fois** du code serveur **et** un générateur de JS
client. J'avais exclu `vertex/ui/**` du corpus K2, pas les chaînes JS de
`terminal.py`.

**Trois faux arrêtés avant publication. Total : 34 → 37.**

## La mesure

```text
règles déclarées (hors `static`)                      189
   K1 consommée par un objet SERVI                     98
   K2 « serveur interne »                              43     ← borne HAUTE, voir plus bas
   K3 navigation (les 8 pages + /analysis/<sym>)        9
   K4 redirection 301 de compatibilité                 12
   E3 infrastructure (healthz, readyz, sw, manifeste)   5
   ORPHELINES                                          22
```

### La classe K2 est contaminée — et je la borne au lieu de la réparer

```text
K2 « serveur interne »                                            43
   dont citées UNIQUEMENT depuis terminal.py
   ET absentes des octets servis                                  15

      /titre/<sym>   53 citations      /settings    22 citations
      /bordel        20 citations      /catalysts   15 citations
      /entreprises   13 citations      /ma-page     11 citations
      /api/rescan     7                /review       7
      /analyse-entreprise 5            + /api/committee-review · /api/company/<sym>
                                         /api/risk · /api/strategie · /api/validator
                                         /stocks
```

**Cinquante-trois citations de `/titre/<sym>`, vingt-deux de `/settings`, vingt
de `/bordel` — et pas un octet servi.** C'est la mesure de ce que le CLAUDE.md
décrit en prose : les pages mortes du monolithe. **Les citations vivent dans du
code de page qui ne rend plus.**

**Conséquence sur le résultat, dite franchement : le compte d'orphelines est un
INTERVALLE. 22 est un plancher ferme ; 37 est le plafond si les quinze
suspectes sont bien mortes.** Soit **12 % à 20 % de la surface HTTP déclarée**.
Je n'ai pas tranché les quinze une par une — cela demanderait de décider, pour
chaque citation, si elle est dans une chaîne JS ou dans un appel Python, et je
ne l'ai pas fait.

## Le coût réel des 22 orphelines fermes — et il est faible

```text
orphelines qui ÉCRIVENT sur disque                     1   /desc/<sym>
orphelines qui coûtent du RÉSEAU sortant               2   /desc/<sym>, /api/correlations/<sym>
orphelines INERTES (ni écriture ni réseau)            20
```

**Vingt sur vingt-deux ne coûtent rien tant que personne ne les appelle.** C'est
de la **surface de maintenance**, pas un mensonge à l'écran. Aucune ne change ce
que l'utilisateur voit. **Rang 4** — la valeur de ce lot est la **mesure**, pas
la trouvaille.

`/desc/<sym>` est la seule qui fasse les deux : elle va chercher une description
sur le réseau **et** écrit un cache — pour personne.

## Le fait nommé : deux des trois « sorties assainies » n'ont aucun consommateur

Le `CLAUDE.md` du dépôt, invariant n°5, pose :

> « *Sortie assainie au serveur* : `/news-feed`, `/api/events/<sym>`,
> `/api/skyler/<sym>` → **toujours** via `news_plus.sanitize_news()` avant de
> servir, **car leurs consommateurs injectent le titre brut en innerHTML**. »

Mesuré sur les 42 objets servis :

```text
/api/skyler/    → CITÉE par 4 objets  (/opportunities, /analysis/AAPL,
                                       /portfolio, /journal)
/api/events/    → AUCUN OBJET SERVI
/news-feed      → AUCUN OBJET SERVI
```

**Sur les trois sorties dont l'invariant justifie l'assainissement par leurs
consommateurs, une seule en a un.** L'assainissement lui-même reste **juste et
utile** — c'est de la sûreté gratuite, et le gardien
`tests/test_xss_exits_lot177.py` protège un consommateur futur. **Ce qui est
inexact, c'est la JUSTIFICATION consignée** : elle affirme des consommateurs que
la mesure ne trouve pas. Même famille que la correction du SHA du lot 399
publiée au 460 : **une affirmation de la documentation contredite par la
mesure.** Je le nomme, je ne le classe pas comme défaut produit.

### Le piège des homonymes, dixième récurrence — évité par construction

`/api/live/events` **est** servi (`live-updates.js`, flux SSE). `/api/events/`
ne l'est pas. Une recherche naïve du mot « events » — 27 occurrences dans les
octets servis, dont `n_events`, `?view=events`, `d.events`, `addEventListener` —
aurait conclu l'inverse. **L'appariement par préfixe d'URL, posé dans le
calibrage, a évité le faux sans que j'aie à y penser.**

## Ce que le lot ne prétend pas

- **Le compte d'orphelines est un intervalle [22, 37]**, pas un nombre. Les
  quinze suspectes de K2 ne sont **pas tranchées une par une**.
- K1 repose sur la présence du **préfixe statique** dans les octets servis. Une
  route dont le client construirait l'URL autrement — table de correspondance,
  variable assemblée en plusieurs morceaux — serait **faussement orpheline**.
  **Non quantifié.**
- « Écrit » et « réseau » sont établis par **motifs dans la source de la vue**,
  pas par exécution : une écriture ou un appel réseau **dans une fonction
  appelée** par la vue échapperait. La mesure **sous-estime** donc le coût.
- Les 12 redirections sont classées **par lecture** de `LEGACY_REDIRECTS`, pas
  par appel.
- **Aucune route n'a été appelée** — ni orpheline, ni autre. **`/desc/<sym>`,
  `/api/correlations/<sym>` et `/options/<sym>` en particulier N'ONT PAS été
  appelées** (réseau sortant et écriture disque).
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `app.url_map` et `inspect.getsource` en mémoire ; les
  8 pages + `/analysis/AAPL` en **GET** ; `persist` redirigé ; **aucun écrivain
  appelé**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-neuvième lot court, sixième de la tranche.

Le lot ne trouve **aucun mensonge à l'écran** — et il rend une mesure que la
boucle n'avait jamais faite : **la part de la surface HTTP qui ne sert
personne**, entre 12 % et 20 %. Sur les vingt-deux fermes, **vingt sont
inertes**. **Huitième bornage consécutif.**

Le fait de méthode est une répétition, mais d'une netteté nouvelle : **trois
corrections d'instrument dans un seul lot**, et les trois portent sur **la même
confusion** — *du texte destiné au client, écrit dans un fichier Python, n'est
pas du code serveur*. `vertex/ui/**` d'abord, les chaînes JS de `terminal.py`
ensuite. Le contrôle obligatoire a attrapé la première ; **seule la lecture a
attrapé les deux autres**, comme aux 463, 464 et 465.

Et un renfort pour la règle du 465 : ici, ce n'est pas seulement le consommateur
d'`/api/alerts/status` qui n'est pas servi — **c'est une famille entière de
citations, cinquante-trois pour une seule route, qui vivent dans un code que le
navigateur ne reçoit jamais.**

Genre confirmé : **UNE ROUTE QUI TRAVAILLE POUR PERSONNE** — et sa variante
mesurée ici, **UNE CITATION QUI NE SORT JAMAIS DU DÉPÔT**.

Comptes séparés : résultats faux **arrêtés avant publication** **37** (+3) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
