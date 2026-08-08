# SKYLER LOT 375 — Les promesses de forme de retour tiennent ; les promesses en un mot ne sont pas décidables

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-375` (base : lot 374 fusionné,
657a932)

## Piste calibrée

Le gardien du lot 366 ne couvrait que les identifiants CAPS_SNAKE des docstrings
de **modules** de moteurs. Ce lot descend aux **fonctions**, dans la veine des
lots 365 (PORTFOLIO_FIT annoncé, jamais évalué) et 368 (promesse d'échappement
fausse) : chercher les docstrings qui annoncent un comportement que le code ne
tient pas.

## Volet 1 — les promesses de forme de retour : SAINES

`Retourne {a, b, c}` est le contrat le plus objectivement vérifiable qui soit.
Six fonctions en portent un :

```text
vertex/options/liquidity.py::assess                       {score, tradeable, issues}
vertex/options/contract_filter.py::hard_filter            {kept, rejected}
vertex/options/call_selector.py::select_calls             {per_category, primary, rejected, notes}
vertex/engines/recommendation.py::position_decision       {verdict, label, tone, cls,
                                                           reason, risk, action, confidence}
vertex/engines/recommendation.py::options_for_position    {sym, held_type, suggestions, note}
vertex/data_sources/tradingview_signal_store.py::add      {accepted, reason}
```

**Résultat : 0 promesse non tenue.** Sur **toutes** les branches
`return {littéral}` — 14 au total — aucune clé annoncée ne manque.

Un test d'exécution n'aurait prouvé qu'un chemin : `assess` a une **sortie
anticipée** (bid/ask absent) qui renvoie 3 clés, et un chemin normal qui en
renvoie 4. La collecte statique de **chaque** branche est ici plus forte qu'un
appel.

### Trois sous-déclarations, volontairement non corrigées

```text
assess               chemin normal   renvoie en plus : spread_pct
add                  signal accepté  renvoie en plus : entry
options_for_position pack() (13 clés) renvoie en plus : delta   (docstring : 12)
```

Ce sont des **enrichissements**, pas des promesses fausses : rien de ce qui est
annoncé ne manque. Je ne les corrige pas et le gardien n'exige pas l'égalité
exacte — l'imposer le rendrait intenable dès qu'une branche d'erreur renvoie le
socle minimal, et **un gardien qui crie au loup finit désactivé** (leçon du
lot 374). La troisième porte sur une forme **imbriquée** que le gardien ne
vérifie pas ; c'est déclaré plutôt que tu.

## Volet 2 — les promesses en un seul mot majuscule : NON DÉCIDABLES

C'est la seconde moitié de la piste, et elle se referme sur un constat, pas sur
un vert.

```text
mots majuscules distincts cités en docstring de fonction : 359
dont introuvables dans le paquet                         :   0
échantillon : ACHETER, ATTENDRE, ATTAQUE, ARBITRAIRE, ABSENTES, APPLICABLE…
```

Le « 0 » est **vide de sens**. L'échantillon le montre : sans underscore, un mot
majuscule dans une docstring française est presque toujours une **emphase**, pas
un identifiant — et le filet de recherche (n'importe quel jeton majuscule parmi
299 fichiers) les déclare tous « trouvés ». Le lot 366 avait déjà rencontré ce
mur dans l'autre sens : son premier filtre produisait 139 faux positifs, resserrés
en exigeant un underscore. **Sans underscore, la question n'est pas décidable
ainsi.** Annoncer « 0 problème » ici serait un faux vert. Piste close par la
mesure.

## Correction de méthode

Ma première passe utilisait `ast.walk`, qui **descend dans les fonctions
imbriquées**. Le `return` de `pack()` — le constructeur de suggestions, 13 clés —
était comparé à la promesse de `options_for_position`, qui en annonce 4 :

```text
options_for_position L182 (13) MANQUE held_type, note, suggestions
```

Une « violation » de trois clés, **entièrement imaginaire**. Corrigé en
n'explorant que les nœuds appartenant à la fonction auditée.

**10ᵉ fois** de la boucle qu'un doute sur l'outil change le résultat, et
**troisième d'affilée** où c'est mon détecteur qui accuse du code sain (lot 374
deux fois, lot 375 une fois). La règle vaut d'être retenue : quand un audit
signale une faute grossière dans du code mûr, l'outil est le premier suspect.

**Verdict : sain, rien touché.**

## Gardien

`tests/test_promesses_retour_lot375.py` (10 tests) :

- **périmètre** (leçon du lot 373) : ≥ 100 fichiers, moteurs inclus ;
- **anti-vide** ×2 : ≥ 5 promesses trouvées, et chacune doit avoir des branches
  vérifiables ;
- **la propriété** : aucune clé annoncée ne manque, sur toutes les branches ;
- **pas trop strict** : les clés supplémentaires sont tolérées — et un test exige
  qu'il en reste au moins une, sinon cette tolérance est devenue sans objet et
  doit être retirée plutôt que gardée à vide ;
- **anti-ré-attribution** : le détecteur ne doit jamais attribuer à
  `options_for_position` un `return` de plus de 6 clés — ma faute exacte,
  verrouillée, avec vérification qu'il reste bien une fonction imbriquée à
  piéger ;
- **anti-dérive** : les 4 contrats les plus lourds sont épinglés nommément, pour
  qu'une docstring amoindrie échoue ici plutôt que de laisser le test générique
  passer sur une promesse rétrécie.

### Preuve ROUGE

```text
ROUGE OK  clé promise `score` retirée du chemin normal         | restauration identique
          1 failed, 9 passed
ROUGE OK  clé promise retirée de la SORTIE ANTICIPÉE           | restauration identique
          1 failed, 9 passed
ROUGE OK  docstring réécrite en douce (contrat amoindri)       | restauration identique
          1 failed, 9 passed
ROUGE OK  détecteur redescendant dans les fonctions imbriquées | restauration identique
          2 failed, 8 passed
après restauration : 10 passed
VERDICT : gardien mordant sur les 4 cas
```

Le premier cas a d'abord été **sauté** (mon motif visait un `return` qui n'existe
pas sous cette forme) — signalé par le script, puis corrigé sur la vraie ligne
plutôt que laissé de côté. Le deuxième cas est celui qui compte le plus : c'est
la branche qu'un test d'exécution unique ne visiterait jamais.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 374, 657a932) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2693 → 2703 passed / 2 skipped** — verte (+10).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Seule la forme `Retourne {…}` est reconnue : une docstring qui décrit son retour
en prose (« renvoie un dictionnaire avec le score et les alertes ») échappe au
détecteur, et je n'ai pas mesuré combien il en existe. Les formes **imbriquées**
(les clés d'un élément de liste) ne sont pas vérifiées — c'est justement là que
se cache la sous-déclaration de `delta`. `select_calls` construit son dict puis
renvoie la variable : sa promesse n'est pas vérifiable statiquement, seulement
son existence. Enfin, une promesse tenue n'est pas une promesse **juste** : ce
lot vérifie que les clés sont là, pas que leurs valeurs ont le sens annoncé.

## Suite

LOT 376 : veille active. Pistes ouvertes — (b) les trois sites de concaténation à
constantes du lot 374, sondés pour eux-mêmes ; (c) les docstrings qui décrivent
leur retour **en prose** plutôt qu'en `Retourne {…}` — angle mort déclaré
ci-dessus. Prochaine échéance périodique : **~lot 380**.
