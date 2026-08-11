# SKYLER LOT 473 — LE DEVIS, TROISIÈME TRANCHE : le rang 1 le plus utile est chiffré à 4 lignes, MAIS QUATRE DOSSIERS SUR CINQ NE SONT PAS DEVISABLES EN L'ÉTAT — leurs lignes publiées ne pointent plus sur ce qu'elles annoncent, et je refuse de chiffrer sur des références qui ont dérivé

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-473` (base : lot 472 fusionné,
`7e4e807`)

Troisième lot du devis, dossiers **12 à 16**. **Il ne corrige rien.** Aucun
fichier de production touché, aucun gardien écrit, aucun test ajouté.

**Ce lot ne rend pas ce qu'on lui demandait, et c'est son résultat.** Un des cinq
dossiers est chiffré au standard des 471/472. **Quatre ne le sont pas**, pour une
raison mesurée et non supposée : **leurs sites publiés ne contiennent plus ce
qu'ils annoncent.** Chiffrer par-dessus aurait produit un devis propre et faux —
exactement ce que la parade des trois lots interdit.

## Le contrôle — et il ÉCHOUE au premier jet, pour la deuxième fois de la veine

Le contrôle portait sur un cas dont la réponse était censée être connue : le
témoin positif du 464, annoncé en `decision_memory.py:54` comme
`'demo': bool(p.get('demo'))`.

```text
mesuré  decision_memory.py:54   return None            ← dans le corps de _num()
        decision_memory.py:111  'demo': bool(p.get('demo'))   ← LE VRAI TÉMOIN
        decision_memory.py:71-72  raw = '%s|%s|%s|%s|%s' % (…, bool(p.get('demo')))
                                  ← le drapeau entre AUSSI dans le hash d'identité
verdict CONTRÔLE ÉCHOUÉ AU PREMIER JET — 57 lignes d'écart
```

**La référence fautive venait de mon propre réveil, pas du rapport 464** — qui,
lui, ne cite pas `decision_memory.py`. Le contrôle a donc fait exactement ce
qu'on attend de lui : arrêter une référence fausse **avant** le chiffrage.

Et il a rendu mieux que prévu : `decision_memory` ne se contente pas d'écrire la
provenance, **il la fait entrer dans l'identité de la décision** (`:71-73`). Deux
versions du même verdict, l'une en démo l'autre en réel, portent des
`decision_id` différents et **coexistent séparées**. C'est un modèle plus fort
que ce que le 464 en disait.

**Compte : arrêté avant publication, 40 → 41.**

---

# DOSSIER 12 — 464, les trois journaux sans provenance · RANG 1 · CHIFFRÉ

## La carte exacte des quatre journaux, relue

```text
fichier                  écrivain                              provenance ?
skyler_memory.json       decision_memory.freeze()   :111       OUI — et dans le hash :71-72
skyler_decisions.json    skyler_journal.record()    :24, :40-44   NON — 8 champs, aucun demo
skyler_sessions.json     session_log.record_close() :46        NON — (log, sym, date, close)
edge_ledger.jsonl        track_record.record()      :31, :52-58   NON — 12 champs, aucun demo
```

**Le 464 est exact** : trois journaux sur quatre n'écrivent pas la provenance, et
le quatrième — celui qui la fait le mieux — est **dans le même bloc appelant**
(`analysis_api.py:175` / `:189` / `:199`, trois écritures voisines de vingt-cinq
lignes). Le modèle à copier est littéralement à côté.

## Une atteignabilité que j'ai failli publier fausse

Mon premier relevé donnait **« `track_record.record()` : aucun appelant en
production »** — ce qui aurait vidé le dossier de son rang 1 sur `edge_ledger`.

```text
grep « track_record.record »  →  AUCUN en production
grep « _track. »              →  terminal.py:1430   _track.record(scan_state)
                                 terminal.py:7070   _track.evaluate(scan_state)
```

**L'appel existe, sous un alias d'import** (`terminal.py:66`
`from vertex.engines import track_record as _track`). C'est le **piège du
détecteur à une seule forme**, quatorzième récurrence — et cette fois sur la
forme d'un **appel**, pas d'un champ ni d'une écriture de fichier. Le rapport 464
citait bien `terminal.py:1430` ; **c'est mon grep qui était borgne.**

**Compte : arrêté avant publication, 41 → 42.**

## Chiffrage — et le coût dépend d'une contrainte mesurée

```text
skyler_journal.record(journal, decision, price=None, now=None)   :24
   → + `demo=False` en mot-clé · + 1 champ dans le record :40-44 · appel :175 passe _demo
   → AUCUN test n'appelle sj.record — mesuré, 0 occurrence dans tests/     2 lignes

session_log.record_close(log, sym, date, close)                  :46
   → + `demo=False` en mot-clé · + 1 champ · appel :199 passe _demo
   → HUIT appels de test à QUATRE arguments positionnels
     (test_session_log_lot15.py ×5, test_import_full_lot46.py ×3, test_memory_export_lot29.py ×1)
   → LE MOT-CLÉ À DÉFAUT EST OBLIGATOIRE — un paramètre positionnel casse les huit  2 lignes

track_record.record(state)                                       :31
   → + 1 champ dans `rec` :52-58. AUCUN changement de signature.
   → MAIS : track_record.py n'importe PAS DEMO_MODE (imports mesurés : json, time,
     datetime, persist) et `scan_state` ne porte NI 'source' NI 'demo' (mesuré
     dans vertex/app/state.py) → il faut UN IMPORT en plus.                        2 lignes
                                                                        ─────────
                                                             TOTAL      6 lignes
```

**Le devis corrige donc le chiffre annoncé par le bilan n°16** — qui parlait de
« passer `demo` à `record()` », suggérant un geste. **C'est six lignes dans trois
fichiers**, et l'un des trois exige un import parce que ni sa signature ni son
argument ne portent la provenance.

## Gardien et régression

```text
gardien       tests/test_journaux_provenance_lot4xx.py
assertion     les trois écrivains produisent un enregistrement portant `demo`,
              et record_close/sj.record acceptent l'appel HISTORIQUE sans le mot-clé
échoue-t-il aujourd'hui ?   OUI — mesuré champ par champ : skyler_journal.py:40-44
              (8 champs), session_log.record_close (4 paramètres), track_record :52-58
              (12 champs) — aucun ne porte `demo`
octet servi ?  NON — trois journaux runtime, ni shell ni /static → AUCUN BUMP, AUCUN _EMPREINTE
moteur touché ?  OUI, trois fichiers de vertex/engines/ — mais ce sont des AJOUTS DE CHAMP
                 et des mots-clés à défaut : aucun calcul, aucun seuil, aucune décision
```

**Ce que le correctif n'achète pas** : les enregistrements **déjà écrits** restent
sans provenance. `edge_ledger.jsonl` est **append-only** — même famille que le 463,
et il faut le dire avant un GO.

---

# DOSSIERS 13 à 16 — NON DEVISABLES EN L'ÉTAT, et voici pourquoi

La règle des trois lots de devis est : *relire chaque ligne citée dans le fichier
réel avant de la chiffrer.* Appliquée à ces quatre dossiers, elle **refuse** de
rendre un chiffre.

## 447 — max pain multi-échéances · le site publié n'existe plus

```text
publié au 447   options_lab.py:81 · portfolio_page.py:484 · :488 · positions_api.py:202
mesuré          options_lab.py:81       → `leaps = [c for c in board if (c.get('dte') or 0) >= 300]`
                portfolio_page.py:484   → boucle des alertes gamma de la carte « Surveillance »
                portfolio_page.py:488   → rendu d'une puce de cette même carte
                grep « max_pain » dans options_lab.py       → AUCUNE OCCURRENCE
                grep « max_pain|maxPain » dans portfolio_page.py → AUCUNE OCCURRENCE
```

**Les deux fichiers cités ne contiennent pas un seul « max pain ».** Le moteur
réel est ailleurs (`gex.max_pain()`, hors des références publiées). Le dossier
n'est pas invalidé — **ses sites doivent être rétablis avant tout chiffrage.**

## 452 — `/analysis` « Anomalies » · la référence pointe l'APPEL, pas le défaut

```text
publié au 452   analysis_page.py:929
mesuré          :929 → `loadAnomalies();`      ← la simple invocation
                :856 → `async function loadAnomalies(){`   ← LE CORPS
                :185-188 → la carte « Anomalies » dans _CONTENT
                :510 → le commentaire de section
```

Le site est **localisable** (`:856`), mais la référence publiée désigne la ligne
qui **appelle**, pas celle qui **fait**. Devise-t-on sur `:929` ? On chiffrerait
une ligne d'une instruction. **Le dossier reste chiffrable au lot suivant, à
partir de `:856`** — je le nomme et je ne l'invente pas.

## 432 + 433 — les trois synthèses de `/portfolio` · références de mécanisme

```text
publié   portfolio_page.py:93-101 · :130 · :197
mesuré   :93-101 → `enrich(pos,quotes)`, la construction des valeurs
         :130    → un commentaire de `thesisState`
         :197    → `const allMarked=…` dans le calcul des métriques
```

Ce sont les **mécanismes** des synthèses, pas les **phrases** fautives. Les trois
synthèses incriminées ne sont pas à ces lignes ; les localiser demande de
reconstruire ce que chaque rapport visait. **Non chiffré.**

## 442 + 443 — les trois R:R · seize sites publiés, deux rapports croisés

Les deux rapports citent **seize** fichiers différents (`analysis.py`,
`analysis_page.py` ×3, `committee.py`, `decide.py`, `decision_stack.py`,
`evidence.py`, `skyler_core.py`, `order_ticket.py`, `chart_read.py`,
`planning_api.py`, `pretrade.py` ×2, `weekly.py`, `chart-core.js`,
`candlestick-lwc.js` ×2, `price-chart.js`, `vx-core.js`). **C'est le dossier le
plus large des seize, et le seul à croiser deux rapports sur une grandeur
calculée en plusieurs endroits.** Un devis honnête pour celui-là est **un lot
entier**, pas un paragraphe. **Non chiffré.**

## Pourquoi je ne force pas

J'aurais pu rendre cinq lignes de chiffres pour ces quatre dossiers. Elles
auraient été **présentables et fausses** — et le 471 a montré exactement ce que
coûte un chiffre posé sur une référence non relue : *trois auraient envoyé un
correcteur au mauvais endroit, le quatrième droit dans une exception.*

**Un devis qui invente ses sites est pire qu'un devis manquant : le second se
voit, le premier se paie.**

---

# PARTIE B — LA FEUILLE DE DÉCISION, SUR LES DOUZE DOSSIERS RÉELLEMENT CHIFFRÉS

| # | dossier | rang | fichier(s) | lignes | moteur | servi | `_EMPREINTE` |
|---|---|---|---|---|---|---|---|
| 1 | **457** borne V1 | **1** | `portfolio_page.py` | ≈5 | non | oui | non |
| 2 | 455 pré-trade | 2 | `pretrade.py` | 2 | oui (rendu) | non | non |
| 3 | 461 `dominantRisk` | 2 | `portfolio_page.py` | 1-2 | non | oui | non |
| 4 | **434** anomalies sans scan | **1** | `opportunities_page.py` | 1 | non | oui | non |
| 5 | **427** légende indices | **1** | `markets_page.py` | 1 | non | oui | non |
| 6 | **428** entonnoir plat | **1** | `markets_page.py` | 2 | non | oui | non |
| 7 | **437** fraîcheur | **1** | 3 pages + `terminal.py` | 5 | non | oui | non |
| 8 | 456 dénominateur | 2 | `strategy_os_api.py` | 1 | non | non | non |
| 9 | 463 provenance GEX | 2 | `gex_history.py` + route (+JS) | 4 (+1) | oui (garde) | oui si JS | **oui si JS** |
| 10 | **425** maturités | **1** | `markets_page.py` | 2 (+1) | non | oui | non |
| 11 | 458 `catOf` | 2 | `opportunities_page.py` | 1 | non | oui | non |
| 12 | **464** trois journaux | **1** | 3 × `engines/` | **6** | oui (champ) | **non** | non |

```text
DOUZE DOSSIERS · 31 à 37 LIGNES · 12 GARDIENS À ÉCRIRE · SEPT DE RANG 1
UN SEUL bump SW couvre tout · _EMPREINTE UNE SEULE FOIS (463, et seulement si l'on touche le JS)
```

## Regroupement PAR FICHIER — la clé du plan

```text
markets_page.py         427 · 428 · 425 · 437(part)      4 dossiers · 3 rang 1 ·  6 lignes
portfolio_page.py       457 · 461                        2 dossiers · 1 rang 1 ·  7 lignes
opportunities_page.py   434 · 458 · 437(part)            3 dossiers · 1 rang 1 ·  3 lignes
engines/ (journaux)     464                              1 dossier  · 1 rang 1 ·  6 lignes
briefing.py             437(part)                        1 ligne
pretrade.py             455                              2 lignes
strategy_os_api.py      456                              1 ligne
gex_history.py + route  463                              4 lignes
```

**Dix des douze dossiers tiennent dans quatre fichiers.**

## Les lots de travail proposés — chacun autonome

```text
LOT DE TRAVAIL A — « /markets »            427 + 428 + 425          6 lignes · 1 fichier · 3 RANG 1
   un seul fichier, un seul bump, un seul examen de régression. AUCUN gardien existant sur
   les trois sites. C'est le meilleur rapport valeur/risque des douze.

LOT DE TRAVAIL B — « les journaux »        464                      6 lignes · 3 fichiers · RANG 1
   AUCUN octet servi, AUCUN bump, AUCUN _EMPREINTE. Contrainte dure : mots-clés à défaut
   obligatoires (8 appels de test à 4 positionnels sur record_close).

LOT DE TRAVAIL C — « /portfolio »          457 + 461                7 lignes · 1 fichier · 1 RANG 1
   les deux partagent l'injection du profil : faits ensemble, le 461 coûte UNE ligne.

LOT DE TRAVAIL D — « /opportunities »      434 + 458                2 lignes · 1 fichier · 1 RANG 1

LOT DE TRAVAIL E — « la fraîcheur »        437                      5 lignes · 4 fichiers · RANG 1
   le seul qui traverse trois pages ET le serveur. À faire seul.

LOT DE TRAVAIL F — « les isolés »          455 + 456 + 463          7 lignes · 4 fichiers
   463 est le seul à déclencher _EMPREINTE : le mettre en dernier.
```

## Ce qui ne se répare pas complètement — à savoir AVANT un GO

```text
463   n'achète que l'AVENIR : _MAX_DAYS = 120, un point écrit en démo est resservi 4 mois.
464   n'achète que l'AVENIR : edge_ledger.jsonl est append-only, l'existant reste sans provenance.
458   le prédicat NE PEUT PAS être rendu exact — les catégories de la Constitution se
      chevauchent sur le delta. Seule correction honnête : RENOMMER la colonne.
```

## Les TROIS dossiers de DÉCISION — ils ne sont pas des correctifs

```text
469   le board sélectionne sous le plancher DTE de la Constitution (bucket court, cible 45,
      plancher 60).   QUESTION : la Constitution fait-elle loi, ou l'exception doit-elle y être ÉCRITE ?
468   six seuils décident sans source de configuration.
      QUESTION : entrent-ils dans la Constitution, ou restent-ils des constantes de présentation ?
466/467  28 routes orphelines sur 189.
      QUESTION : les supprimer, ou les documenter comme surface d'API assumée ?
```

## CE QUE LE DEVIS NE COUVRE PAS — nommé, non chiffré

**Les quatre dossiers de ce lot** : 447 (max pain), 452 (`/analysis` Anomalies +
collision de route), 432+433 (les trois synthèses `/portfolio`), 442+443 (les
trois R:R) — **tous RANG 1**. Sites à rétablir ; pour le 452 le point de départ
est établi (`analysis_page.py:856`).

**Et tous les dossiers en attente jamais classés** : MSFT (388) · `myCapital`
(406) · HHI ×170 (407) · 1 site (408) · 1 carte (409) · libellés (411) ·
drawdown (426) · RSI 100 (416) · dénominateurs `track_record` (417) ·
expected-move muet (422) · scan DEMO → `breadth_history.json` (391/396) ·
`context()` (379) · « points réels du scan » (363) · replis `0` (378) · badge
IBKR (386+431) · `/opportunities` (452, rang 2) · `symbols_usable` 30 (456+459) ·
`winnerRule` (461, rang 3).

**Le devis couvre douze dossiers sur une trentaine ouverts.** Je le dis pour
qu'on ne lise pas « 31 à 37 lignes » comme le coût de la dette entière.

## Ce que le lot ne prétend pas

- Le devis chiffre **des lignes, pas des heures** ; **minima structurels**, hors
  gardien et hors témoins de version.
- **Aucun test n'a été écrit.** Les « échoue aujourd'hui ? OUI » du 464 sont
  établis **champ par champ, par lecture**.
- Les lots de travail A à F sont un **découpage proposé**, pas une mesure. Ils
  découlent du regroupement par fichier, qui, lui, est mesuré.
- **Aucun défaut rejoué**, aucun classement modifié.
- **Aucun navigateur. Aucun réseau. Aucun écrivain appelé. Aucun fichier de
  production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `persist` redirigé vers un `mkdtemp` **et la redirection
  vérifiée par `persist.cache_path()`** ; **aucun des quatre écrivains appelé**
  (lecture de signatures et de champs seulement) ; **`/options/<sym>`,
  `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-quinzième lot court, troisième du devis.

Le devis est **clos sur douze dossiers**, avec un plan de travail en six lots
autonomes. C'est la livraison que le bilan n°16 réclamait, et elle est là.

Mais le fait de méthode du lot n'est pas le plan — **c'est le taux d'échec des
références publiées.** Sur cinq dossiers ouverts aujourd'hui : **un chiffré,
quatre dont les sites ne tiennent pas.** Ajouté aux quatre écarts du 471 et aux
quatre contraintes du 472, cela dessine une conclusion que je n'aurais pas
formulée avant les trois lots :

*Un rapport de mesure établit qu'un défaut EXISTE. Il n'établit pas OÙ il est
d'une façon qui survive au temps. Les deux ne sont pas le même travail, et
quarante-neuf lots de veille n'avaient produit que le premier.*

C'est l'argument le plus solide en faveur du devis, et il ne se voyait qu'après
l'avoir fait.

Comptes séparés : résultats faux **arrêtés avant publication** **42** (+2 : le
témoin `decision_memory:54` du réveil, et le « aucun appelant en production » de
`track_record`) ; **publiés puis corrigés** **5** ; **interprétations retirées**
**3**. Les quatre dossiers non devisés ne sont **ni des erreurs ni des
corrections** — ce sont des **références à rétablir**, et je les compte à part :
**4 dossiers en attente de re-localisation.**

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan de travail des douze
dossiers est prêt et attend le premier GO.**
