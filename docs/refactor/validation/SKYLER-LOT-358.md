# SKYLER LOT 358 — Le second point de sortie de news : couvert, et dit vrai

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-358` (base : lot 357 fusionné,
46d7b71)

## Piste calibrée

Règle critique n°5 du projet : « tout texte externe passe par
`sanitize_news()` avant d'être servi (XSS — rendus en innerHTML) ».
Question du lot : **cette règle couvre-t-elle vraiment tous les points de
sortie de news servis aujourd'hui ?**

## Ce que l'audit a trouvé

Il existe **deux** familles de sorties, pas une.

**Famille A — assainie au serveur** (`sanitize_news`) : `/news-feed`
(`routes/content.py`), `/api/events/<sym>` et `/api/skyler/<sym>`
(`analysis_api.py` ×2), `skyler_sweep`. Couverte par le gardien du lot 177.
Ce contrat est **nécessaire** : les consommateurs de `/news-feed` injectent
le titre **brut** en innerHTML (`_OV_EXTRA_JS::renderFeed`, terminal.py
L6163). *Note d'état* : ces trois consommateurs vivent dans les constantes
`PAGE_*` de terminal.py, qui ne sont routées par aucune page servie
aujourd'hui — aucun fichier de `vertex/ui/` ni de `vertex/static/` ne
fabrique `/news-feed`. L'assainissement serveur reste la bonne défense (la
route, elle, est bien vivante) ; c'est le rendu brut qui est une relique.

**Famille B — échappée au rendu**, non couverte jusqu'ici :
`/api/ai/enrichment` (`vertex/ai/enrichment.py::parse_news`) sert des titres
d'actualité issus d'une recherche web relayée par Claude. Mesure directe :

```text
headline servi : '<script>alert(1)</script>Titre'
why servi      : '<img src=x onerror=alert(2)>'
```

Le serveur **ne neutralise pas** ce texte. Ce n'est pas un trou : son
**unique** rendu (`vertex/ui/pages/system_page.py::loadBrain`, L350) passe par
`esc()`, et `why` n'est rendu nulle part. La sûreté est réelle — mais elle
reposait sur trois propriétés qu'**aucun test ne figeait**.

### Pourquoi ne PAS « corriger » en ajoutant `sanitize_news`

Les deux familles ont des contrats **opposés et cohérents** : famille A =
serveur assainit / client injecte brut ; famille B = serveur borne la forme /
client échappe. Ajouter `sanitize_news` en famille B **double-échapperait**
les titres légitimes — un titre `Résultats « record »` s'afficherait
`&quot;record&quot;` à l'écran. Le défaut ici n'est pas dans le code : il est
dans la règle écrite, qui énonce un absolu là où il y a deux contrats.

## Ce que le lot livre

1. **Gardien neuf** `tests/test_ai_news_exit_lot358.py` (5 tests) qui fige les
   trois propriétés dont dépend la sûreté de la famille B :
   - citations filtrées au schéma web (`provenance._safe_url`) — `javascript:`,
     `data:`, `vbscript:`, relatif et non-texte rejetés, bout en bout via `run()` ;
   - forme reconstruite et **bornée** (exactement 4 champs, 200/280/40 car.,
     `impact` dans un ensemble fermé car il pilote une classe CSS) ;
   - **seul rendu via `esc()`** : analyse des appels englobants du texte servi
     (remontée de parenthèses) — pas un simple « `esc(` est quelque part avant ».
2. **Règle n°5 de `CLAUDE.md` corrigée** : les deux familles, leurs contrats,
   leurs gardiens, et l'avertissement sur le double-échappement.

### Preuve ROUGE (le gardien mord)

Chaque défense retirée une par une, test relancé, fichier restauré (MD5 vérifié
identique à chaque fois) :

```text
ROUGE OK  system_page.py  (esc retiré)        -> test_le_titre_ia_n_est_rendu_que_via_esc
ROUGE OK  provenance.py   (_safe_url neutre)  -> test_seules_les_citations_http_s_sont_servies
ROUGE OK  enrichment.py   (impact non borné)  -> test_la_forme_des_actualites_ia_reste_bornee_et_fermee
VERDICT: gardien mordant sur les 3 défenses
```

Première rédaction du 3ᵉ test : **ne mordait pas** (fenêtre de 30 caractères
avant le motif — `esc(n.impact)` voisin la satisfaisait à tort). Corrigée en
analyse des appels englobants, re-prouvée rouge. Noté ici parce qu'un gardien
qui ne mord pas est pire qu'aucun gardien.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 357, 46d7b71) ; arbre propre.
- Suite complète : **2506 passed / 2 skipped** (2501 + 5 neufs) — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : aucun octet servi n'a changé — le lot ne
touche que `tests/`, `CLAUDE.md` et `docs/`. Pas de re-mesure smoke/MD5
nécessaire (dernière mesure complète : lot 350).

## Portée — ce que ce lot ne prétend pas

Aucune vulnérabilité n'a été trouvée ni corrigée : les deux familles sont sûres
aujourd'hui. Le lot ajoute un filet là où il n'y en avait pas et remet la règle
écrite en accord avec le code. Le rendu brut de `/news-feed` dans les `PAGE_*`
reste un candidat de la purge É2/É3 — en attente de décision humaine, rien
engagé.

## Suite

LOT 359 : veille active. Prochaine échéance périodique : ~lot 360 (smoke + MD5
des 8 pages + bilan de la tranche 350-359).
