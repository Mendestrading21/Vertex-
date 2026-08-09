# SKYLER LOT 448 — « simulation impossible : 'NoneType' object has no attribute 'spot' » : une exception Python s'affiche sur `/options` comme motif à l'utilisateur

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-448` (base : lot 447 fusionné,
b29b3d1)

Trentième lot de la veine. Le 447 avait validé la stratégie « trier par
affichage » ; ce lot l'applique au dernier gros champ non ouvert : **`reason`**,
7 phrases composées, **sept producteurs différents** — donc un test du contraste
moteurs/pages sur sept sources d'un coup.

**Aucun code, aucun gardien, aucun test.**

## Les sept, classées par nature

```text
producteur                              nature de la phrase
options_intel_api.py:113                VIDAGE D'EXCEPTION   'simulation impossible: %s' % e
options_lab_api.py:57                   VIDAGE D'EXCEPTION   f'{type(e).__name__}: {e}'
options_lab_api.py:72                   VIDAGE D'EXCEPTION   f'{type(e).__name__}: {e}'
tradingview_signal_store.py:52          refus de validation  'signal inconnu: %s'
horizon_scanners.py:47                  refus de config      'univers inconnu : %r (attendu %s)'
anomaly.py:56                           claim CHIFFRÉ        'série trop courte (%d points, %d requis)'
evidence_lab.py:59                      claim CHIFFRÉ        'série trop courte (%s points, %d requis)'
```

## Étape 1 — l'affichage d'abord (leçon 447), et ce que je n'établis pas

Lectures de champ `.reason` / `['reason']`, jamais un jeton nu (quatre récidives
du piège « un nom, plusieurs payloads ») :

```text
ÉTABLI — payload identifié par sa forme
  evidence_lab.py:59        → {available:false, reason}   analysis_page, route /analysis à paramètre
  anomaly.py:56             → {empty, points, reason}     anomaly-scan.js:15
  options_intel_api.py:113  → {symbol, empty, reason}     options-intel.js:413   (page /options)

NON ÉTABLI — je les nomme et je ne les compte pas
  options_lab_api.py:57 et :72   {available:false, reason} — forme partagée avec d'autres
  horizon_scanners.py:47         plausible sur options-scanner.js:32, non prouvé
  tradingview_signal_store.py:52 aucun lecteur trouvé
```

**Trois sur sept sont concluantes.** Les quatre autres ne sont pas « non
affichées » : elles sont **non établies**, ce qui n'est pas la même chose.

## Les deux claims chiffrés : exacts, mesurés

Banc sur `evidence_lab.study()`, fonction réelle, séries de longueurs
croissantes :

```text
clôtures   available   phrase rendue                                    contrôle
       0     False     série trop courte (0 points, 41 requis)          annoncé 0 = réel 0
       5     False     série trop courte (5 points, 41 requis)          annoncé 5 = réel 5
      20     False     série trop courte (20 points, 41 requis)         annoncé 20 = réel 20
      21     False     série trop courte (21 points, 41 requis)         annoncé 21 = réel 21
      30     False     série trop courte (30 points, 41 requis)         annoncé 30 = réel 30
      40     False     série trop courte (40 points, 41 requis)         annoncé 40 = réel 40
      41     True      —                                                bascule EXACTE au seuil
      60     True      —
```

**8 cas sur 8.** Le compte annoncé est toujours le compte réel, le seuil affiché
est bien `MIN_POINTS`, et la bascule tombe **exactement** à 41 — le témoin positif
est dans la mesure elle-même.

Un point d'attention levé et **écarté** : la garde est un `or`
(`d.get('empty') or d['points'] < MIN_POINTS`) — la forme qui, au 418, testait le
repli au lieu de la donnée. Ici elle est saine : `anomaly.scan` n'a **qu'une seule
branche `empty`** (`len(cl) < 21`), donc `empty` implique `points < 21 < 41` et la
phrase reste vraie. Les deux seuils diffèrent volontairement — **21** pour
l'anomalie, **41** pour l'évidence — et chaque module affiche **le sien**.

## La trouvaille : une exception Python rendue à l'écran

`options_intel_api.py:113` :

```python
except Exception as e:
    return jsonify({'symbol': sym, 'empty': True,
                    'reason': 'simulation impossible: %s' % e}), 200
```

`options-intel.js:413`, servi sur `/options` :

```javascript
if (!d || d.empty) { el.innerHTML = VX.states.empty(esc((d && d.reason) || 'Indisponible.')); return; }
```

**Mesuré** — exception réelle levée par le moteur réel `scenario_pricer.simulate`
sur trois contrats mal formés, formatée par la ligne de la route :

```text
contrat vide            « simulation impossible: 'NoneType' object has no attribute 'spot' »
contrat sans strike     « simulation impossible: 'NoneType' object has no attribute 'spot' »
setup absent            « simulation impossible: 'NoneType' object has no attribute 'spot' »

et la forme des deux autres routes                « KeyError: 'x' »
```

**C'est ce que le trader lit dans la carte d'état vide.** Un message
d'implémentation — nom de type Python, nom d'attribut — présenté comme le
**motif** pour lequel la simulation n'est pas disponible.

### Pourquoi rang 2, et pas plus

Ce n'est **pas une affirmation fausse** : rien n'est inventé, aucun chiffre n'est
faux. C'est pour cela que ce n'est pas un rang 1.

Ce n'est **pas non plus sans conséquence** : c'est affiché, en texte visible, sur
une page produit — donc pas un rang 4. Et cela **déroge à la norme que le dépôt
tient partout ailleurs** : ses états vides nomment l'entrée manquante en français
(« série trop courte (20 points, 41 requis) — aucune statistique inventée »,
« Aucun titre scanné — lancer un scan depuis Système »). **Le contre-exemple est
le champ voisin, produit par le même `reason` du même corpus.**

**Rang 2.** Correction pressentie : journaliser l'exception côté serveur et rendre
au client un motif écrit, comme le font `anomaly` et `evidence_lab`. **Aucun GO,
rien n'est engagé.**

Aucun test du dépôt ne vérifie qu'un `reason` servi est une phrase et non une
exception : **aucun gardien.**

## Ce que le lot dit du contraste moteurs/pages

Sept producteurs testés. Les deux qui **affirment un chiffre** sont **exacts**.
Le défaut trouvé est d'une **autre nature** : ni un faux nombre, ni une
attribution trompeuse, mais **un message technique là où le produit promet une
phrase**.

Le contraste établi au 445 puis nuancé au 446 tient donc encore, à une
précision près : **les moteurs disent vrai ; ce sont les chemins d'exception qui
ne disent rien d'utile.**

## Portée

**Trois phrases sur sept** ont leur affichage établi ; **quatre restent non
établies** — je les nomme, je ne les compte pas, et je ne conclus **ni** qu'elles
sont affichées **ni** qu'elles ne le sont pas.

L'exception mesurée est **réelle** (levée par `scenario_pricer.simulate`), mais
son formatage est **la ligne de la route recopiée**, pas la route exécutée :
`/api/options-for/…` exige un board peuplé, vide au démarrage. **Je le dis plutôt
que de présenter une reproduction comme une exécution** (règle 443).

Je n'ai **pas** cherché si d'autres exceptions produisent des messages plus
révélateurs (chemins de fichiers, valeurs internes) : une seule famille d'entrées
mal formées a été essayée.

**Aucun navigateur ouvert.** Sur les 110 phrases concluantes du 444, **93 restent
fermées**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `evidence_lab.study` et `scenario_pricer.simulate`
  appelés en mémoire ; routes en **GET** ; `persist` redirigé.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante et unième lot court. Séquence : **445 ✗ · 446 ~ · 447 ✓ rang 1 ·
448 ✓ rang 2**.

Deux lots de suite qui trouvent, et les deux par le même geste : **regarder
d'abord qui lit la phrase**. Le tri par affichage, adopté au 446 et confirmé au
447, tient une troisième fois.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **20** ;
**publiés puis corrigés** **1**.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
