# SKYLER LOT 580 — **trois familles d'états, pas deux** — et `data-state=` en porte deux à la fois

Date : 2026-08-11 · Branche : `agent/skyler-v2-lot-580` (base : lot 579 fusionné,
`7f6d5578`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route hors liste sûre.**

## Le choix

**(zz)** — le 579 avait nommé la seconde fabrique de `chart-core.js` sans
l'inventorier. Un `if (state === 'stale')` implique d'autres valeurs.

Piège écrit **avant** de mesurer : *les deux vocabulaires se recouvriront
**presque**, la différence tenant à un ou deux états propres aux graphiques.
**Mais un nom identique ne prouve pas un rendu identique** — comparer les
**sorties**, pas les noms.*

**Verdict : la première moitié est fausse, la seconde est le cœur du lot.**

## La seconde fabrique, lue — `C._stateBody(state, opts)`

```text
branche      octets   délègue ?                classes / attributs / replis
loading         105   OUI → VX.states.loading  —
stale           340   NON                      vx-stale-banner + vx-state ·
                                               state=stale · 2 replis
error           239   NON                      vx-state · tone=error, state=error ·
                                               'Impossible de charger ce graphique.'
empty (défaut)  246   NON                      vx-state · state=empty ·
                                               'Aucune donnée à afficher.'
```

**Aucun état propre aux graphiques** : les quatre noms sont un sous-ensemble
strict de `VX.states` (qui a en plus `ghost`). Le piège se trompait sur ce point.

**Mais une branche sur quatre délègue.** `loading` appelle la fabrique
canonique ; `stale`, `error` et `empty` réécrivent leur HTML. **La délégation
était donc possible** — elle a été faite une fois sur quatre.

## Le piège, vérifié — **même nom, sortie différente**

```text
`error` chez VX.states     bouton « Réessayer » + lien « Ouvrir Système »
                           repli 'Erreur de chargement'
`error` chez _stateBody    AUCUN bouton, AUCUN lien
                           data-tone="error" en plus
                           repli 'Impossible de charger ce graphique.'
```

Deux états portant le même nom, l'un proposant deux issues, l'autre aucune.
`stale` va plus loin : elle produit **deux éléments** (bannière + bloc) avec
**deux replis distincts** — « dernière valeur connue affichée. » et « Rafraîchir
pour actualiser. »

## Ce que je n'attendais pas — **une troisième famille**

En lisant le contexte de `state: 'unknown'` (au lieu de conclure de son nom) :

```javascript
VX.freshness = {
  THRESH: { live: 20000, snapshot: 1800000, stale: 2100000 },   // 20 s / 30 min / 35 min
  …
  chip(a) { return '<span class="vx-fresh-chip" data-state="' + a.state + '" …' }
}
```

**Huit noms**, lus dans ses tables : `live`, `snapshot`, `saved`, `stale`,
`refreshing`, `error`, `offline`, `unknown`. Appelée par `freshness.assess`
(4 fichiers) et `freshness.chip` (4 fichiers).

**Et elle pose `data-state=` — le même attribut que les états de rendu.**

## Les trois familles, croisées **par nom**

```text
(1) VX.states               empty, error, ghost, loading, stale
(2) chart-core._stateBody   empty, error, loading, stale
(3) VX.freshness            error, live, offline, refreshing, saved,
                            snapshot, stale, unknown

présents dans LES TROIS     error, stale
(1) et (2) seulement        empty, loading
propres à (3)               live, offline, refreshing, saved, snapshot, unknown
propre à (1)                ghost
```

**Conséquence, mesurée et non supposée** : `data-state="stale"` et
`data-state="error"` sont **ambigus dans le DOM** — ils peuvent venir d'un état
de rendu **ou** d'une puce de fraîcheur. Un sélecteur CSS, un test ou un lecteur
d'écran qui cible `[data-state="error"]` attrape **les deux familles**.

Ce que le 579 avait vu comme « deux vocabulaires pour le même état » (579-B) est
en réalité **trois vocabulaires qui partagent deux mots**.

## Une correction d'unité, arrêtée avant publication

Mon premier relevé annonçait **16 appelants**. Ce sont **2 sites** : un fichier
`/static/**` est servi sur les 8 pages, et ma clef `(page|nom, position)` le
comptait huit fois.

```text
appelants — cumul (page × fichier)   16
appelants — sites DISTINCTS           2
```

C'est la même faute d'unité que celle des lots 511 et 552, dans un habillage
neuf. Le corpus de base compte **41 fichiers servis distincts** pour 113 parties.

**Arrêtés avant publication : 206 → 207 (+1).**

## Second contrôle (481) — comptage **brut**, par fichier distinct

```text
vx-state           14 occurrences ·  3 fichiers
data-state="       15 occurrences ·  7 fichiers
vx-error-banner    11 occurrences ·  6 fichiers
vx-stale-banner     5 occurrences ·  5 fichiers
vx-skeleton         5 occurrences ·  4 fichiers

valeurs littérales de `data-state=` : empty 4 · loading 1 · stale 2 · error 2
```

Neuf valeurs littérales seulement — et **`chip()` en pose d'autres par
concaténation**, invisibles à tout relevé littéral. Le comptage par littéral est
donc un **plancher**, y compris ici.

## Ce que le dépôt fait bien, mesuré

- **Les quatre noms d'état de rendu sont partagés** : aucune fabrique n'invente
  un état à elle.
- **`loading` délègue** : la fabrique canonique est réellement réutilisée là où
  elle l'est.
- **Les trois familles nomment leur état dans le DOM** — rien n'est muet.
- **La fraîcheur a des seuils écrits et lisibles** (20 s / 30 min / 35 min),
  alignés en commentaire sur la cadence de la session d'analyse.
- **Chaque branche a un repli** : aucun état ne peut s'afficher vide.

## Portée — ce que ce lot NE dit PAS

- L'ambiguïté de `data-state=` est **structurelle, pas observée** : aucun défaut
  d'affichage n'a été constaté — c'est la **forme** qui le permet.
- Les 8 noms de `VX.freshness` sont **lus dans ses tables**, pas suivis jusqu'à
  l'écran.
- **Rien n'est corrigé** : les deux vocabulaires restent, `VX.states.stale`
  reste, les replis restent.
- Corpus du 541 et du 575 : **plancher**, DÉMO sans IBKR.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. Bancs écrits **en fichier**, en chemin
  **absolu** ; aucun banc antérieur touché.
- Note d'hygiène : dans un banc de ce lot, la variable `c` a servi
  successivement à un compteur puis au corpus — le JSON écrit en fin de script
  en a hérité (3,3 Mo). **Les mesures imprimées, calculées avant, ne sont pas
  affectées** ; aucun chiffre publié n'en dépend.
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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier.

Ce que je retiens : **trois lots de suite, une famille entière est apparue en
suivant un fil que l'instrument ne savait pas expliquer.** Le 578 a trouvé
`VX.states.error` en poursuivant une occurrence brute ; le 579 a trouvé la
seconde fabrique en refusant de conclure d'un compte nul ; le 580 a trouvé
`VX.freshness` en **lisant le contexte d'un nom** au lieu de le classer. Les
trois fois, le geste était le même : ne pas s'arrêter à ce que l'outil sait dire.

Trois règles neuves :

- **580-A · UN MÊME ATTRIBUT PEUT PORTER DEUX ESPACES DE VALEURS** —
  `data-state=` sert les états de rendu **et** les puces de fraîcheur ; `stale`
  et `error` y sont ambigus.
- **580-B · DÉLÉGUER UNE BRANCHE SUR QUATRE PROUVE QUE LES TROIS AUTRES
  POUVAIENT L'ÊTRE** — `loading` appelle la fabrique canonique, les trois autres
  réécrivent.
- **580-C · UN FICHIER SERVI SUR HUIT PAGES N'EST PAS HUIT SITES** — 16 en
  cumul, **2** en distinct.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **l'ambiguïté de `data-state=` entre trois familles,
constatée et NON corrigée** ; **les 8 noms de `VX.freshness`, lus et non suivis
jusqu'à l'écran** ; **les 3 branches de `_stateBody` qui ne délèguent pas** ;
**`VX.states.stale`, morte et NON supprimée** ; **les deux vocabulaires du même
état, NON unifiés** ; **les 73 appels à `empty`, comptés et non lus** ; **les 30
appels à la fabrique d'erreur** ; **les 2 appels à « identifiant nu »** ; **les 6
bannières qui relaient `e.message`** ; **le repli « réponse indisponible »** ;
**les 38 sites du relevé structurel neuf du 576** ; **les 29 branches de produit
de la borne (B) neuve** ; **le filtre `chart.umd` des six instruments** ; **les 8
programmes d'`/analysis/AAPL`, non lus ligne à ligne** ; **les 269 branches qui
s'arrêtent sans rien dire** ; **les 14 sites « ailleurs » du 573** ; **les 19
toasts d'erreur littéraux** ; **les 6 toasts sans ton** ; **`warn` et `warning`,
non unifiés** ; **les 23 toasts `success`** ; **les 57 sites qui ne signalent pas
un échec** ; **le total réel des signalements d'échec, toujours inconnu** ; **les
27 appelés du relevé structurel du 570** ; **les 82 corps vides du 569, NON
JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ; **les 42 refus du 567** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 207 (+1)** ;
**publiés puis corrigés 38** ; interprétations retirées **11**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
