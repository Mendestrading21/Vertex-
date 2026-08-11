# SKYLER — LOT 606 · LE DOSSIER 582 EST FERMÉ, ET LE DÉFAUT A ÉTÉ VU

Le dossier 582 est ouvert depuis vingt-quatre lots. Il se terminait ainsi :
« **Rien n'est corrigé. Le `|| 0` reste tel quel : sa correction est une décision
humaine.** » La décision est donnée.

## Le défaut, en une ligne

`/system` construisait sa puce de fraîcheur ainsi :

```javascript
ageMs:(man.age_s||0)*1000
```

Un **repli**, pas une garde. `null || 0` vaut **0**, pas `null`.

Or le serveur met `age_s` à `null` **délibérément**, dans deux endroits qui
portent leur intention par écrit :

```python
# vertex/engines/session_snapshot.py
'age_s': (round(time.time() - ts) if isinstance(ts, (int, float)) … else None)

# vertex/app/routes/session_api.py
# HONNÊTETÉ : l'âge figé au build sous-estimerait la vraie ancienneté d'un
# instantané restauré […]. On l'efface → le client n'affiche que l'horodatage
# absolu `as_of`, jamais un âge faussement frais.
restored['age_s'] = None
```

**Le serveur efface l'âge pour ne pas mentir ; le client le remplaçait par zéro.**

## Ce que le 582 avait déduit, ce lot l'a VU

Le 582 déclarait explicitement sa limite : « **Le libellé "Analyse" n'a pas été
observé à l'écran** : il est déduit de l'ordre de décision. » Il l'est désormais.

Trois passes sur `/system?view=data` — la seule vue qui appelle
`loadContinuity` — service worker bloqué (**602-B**), manifeste injecté :

| manifeste | AVANT le correctif | APRÈS |
| --- | --- | --- |
| nominal (serveur réel) | `snapshot / ANALYSE` | `snapshot / ANALYSE` |
| **`age_s: null`** *(le serveur dit qu'il ignore)* | **`snapshot / ANALYSE`** | **`unknown / —`** |
| `age_s: 42` *(âge réel de 42 s)* | `snapshot / ANALYSE` | `snapshot / ANALYSE` |

**Avant, les trois passes étaient indiscernables.** Un âge que le serveur déclare
ignorer était présenté exactement comme un âge de quarante-deux secondes. C'est
la formulation la plus dure du défaut, et elle n'apparaît que parce que la
troisième passe existe : sans elle, on aurait montré un changement sans prouver
que le **cas normal ne bouge pas**.

**Zéro erreur console sur les six passes.**

## Le gardien, vérifié par mutation

`tests/test_fraicheur_garde_type_lot606.py` — **5 tests**, dont **2 échouent**
sur le code d'avant.

Il ne garde pas le site fautif : il garde **la famille**. Aucune des **cinq**
pages servies ne peut réintroduire un `|| 0` sur un âge. Et il tient **les trois
bouts de la chaîne** — sinon la garde de type deviendrait décorative :

1. le serveur rend `None` (jamais `0`) quand il ignore l'âge ;
2. les cinq pages laissent passer `null` ;
3. `assess` rend bien `{state:'unknown', label:'—'}` sur un âge nul.

Plus un **garde-fou de volume** (`591-C`) : si les cinq appels disparaissaient, le
test principal passerait en ne vérifiant plus rien.

## Le piège, écrit avant de toucher la ligne

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « la garde de type suffit : la puce dira `—` » | **CONFIRMÉ**, observé |
| **(b)** | « `/system` est le dernier des **quatre** sites » | **RÉFUTÉ sur le compte** — ils sont **cinq** : `analysis_page.py:323` s'est ajouté depuis le 582. **Confirmé sur le fond** : le cinquième (`pk ? pk.age : null`) est honnête |
| **(c)** | « aucun test n'épingle le comportement actuel » | **CONFIRMÉ** — zéro occurrence du littéral dans `tests/` |
| **(d)** | « le défaut est visible à l'écran » | **CONFIRMÉ** — c'est l'apport du lot |
| **global** | | **CONFIRMÉ, avec un compte corrigé** |

**Le seul volet qui bouge est un nombre**, et il bouge parce qu'un chiffre a
vingt-quatre lots. C'est `594-A` : un compte est juste à sa date, pas pour
toujours.

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure **les appels à `assess`**. Le cas exclu : **les affichages de
fraîcheur qui ne passeraient pas par `assess`** — ils échapperaient entièrement à
la garde.

```text
appels à `freshness.chip()` SANS `assess()`   0
```

**Toujours zéro, vingt-quatre lots après la mesure du 582.** Personne ne fabrique
un état de fraîcheur à la main.

## Ce que le lot n'établit pas

- **À quelle fréquence `age_s` arrive nul en production.** Le chemin est réel
  (`restored['age_s'] = None`, instantané restauré), mais je l'ai **injecté**
  pour l'observer, pas rencontré.
- Que `analysis_page.py:323` soit correct dans tous les cas : `pk ? pk.age : null`
  rend `undefined` si `pk` existe sans `age`, et `undefined == null` est vrai en
  JavaScript — donc honnête **par coïncidence du langage**, pas par garde
  explicite. Nommé, non traité.
- Que les autres `|| 0` du produit soient inoffensifs : ce lot ne borne que
  **les âges**, sur **cinq fichiers**.

## Règles neuves

- **606-A — UN CORRECTIF D'HONNÊTETÉ DOIT ÊTRE MONTRÉ, PAS DÉDUIT.** Le 582
  avait tout juste — l'ordre de décision, les entrées, la conclusion — et a
  quand même dû écrire « non observé à l'écran ». Vingt-quatre lots plus tard,
  l'observation a coûté trois passes de navigateur.
- **606-B — UNE PREUVE DE CORRECTIF A BESOIN D'UNE PASSE QUI NE DOIT PAS
  BOUGER.** Sans la passe `age_s: 42`, montrer `ANALYSE → —` ne distinguerait
  pas un correctif d'une casse. Le témoin immobile fait la moitié de la preuve.
- **606-C — GARDER LA FAMILLE, PAS LE CAS.** Le défaut était sur un site ; le
  gardien couvre les cinq, et les trois bouts de la chaîne. Un gardien qui
  n'interdit que la faute déjà commise n'empêche que sa répétition littérale.

## Ce que le dépôt fait bien

- **Le serveur écrit son intention d'honnêteté en commentaire**, et le lot n'a
  eu qu'à la faire respecter côté client.
- **Quatre sites sur cinq gardaient déjà l'ignorance.** L'idiome correct était
  majoritaire ; le défaut était l'exception.
- **Zéro puce de fraîcheur hors de l'ordre de décision**, deux fois mesuré à
  vingt-quatre lots d'écart.
- **Le dossier 582 était exact dans ses moindres détails.** Sa seule faiblesse
  était déclarée par lui-même, et c'est celle que ce lot lève.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/ui/pages/system_page.py`,
  `vertex/app/routes/system.py` (bump).
- **1 gardien neuf** (5 tests, vérifié par mutation) + **5 épingles de version**
  `td-shell-v190` → **`td-shell-v191`**.
- MD5 des 8 pages : **7 / 8 identiques** — seule `/system` bouge
  (`f657bf63178b` → **`024ff6d83691`**).
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2875 passed / 0 skipped** *(2870 + les 5 du gardien neuf)*.
- Navigateur : **6 passes** (3 avant, 3 après), **0 erreur console**, rouge puis
  vert sur la même machine.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **238**
- Publiés puis corrigés : **40**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 5** *(582 fermé ici, vingt-quatre lots après son
  ouverture)*
