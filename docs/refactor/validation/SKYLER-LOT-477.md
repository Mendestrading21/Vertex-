# SKYLER LOT 477 — Le 378 classé RANG 2 : deux replis `0` atteignent bien l'entonnoir de `/opportunities`, et l'atténuation que le 378 avait publiée pour se rassurer est RÉFUTÉE — le handler interne avale l'erreur avant que la route puisse la marquer

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-477` (base : lot 476 fusionné,
`b8981ee`)

Deuxième dossier tiré des **dix-sept jamais classés**. Le 476 avait montré le
rythme : quand la mesure existe déjà, il ne manque que **le classement et le
devis**.

**Il ne corrige rien.** Aucun fichier de production touché.

## Le contrôle — réponse connue du lot précédent, et il passe

```text
attendu (mesuré au 476)   performance_page.py:450 — la seule colonne qui affiche
                          son dénominateur, via ' % (' + s.tp1_resolved + ')'
mesuré                    :450  …VX.fmt.num(s.tp1_rate,0)+' % ('+s.tp1_resolved+')'
verdict                   CONTRÔLE PASSÉ
```

## Pourquoi le 378, et pas un autre des dix-sept

1. **C'est le seul des dix-sept qui contredit une règle ÉCRITE.** L'invariant
   produit dit : *donnée absente → `—`/`n/d` honnête*. Un repli `0` est
   exactement l'inverse. Je n'ai pas à construire un critère : **il est déjà dans
   `CLAUDE.md`.**
2. **Le 378 s'était lui-même arrêté à mi-chemin.** Il a livré un recensement gelé
   (254 handlers, 12 replis numériques) et une **caractérisation**, en disant
   franchement « pas de faute prouvée ». Il a versé les deux replis `0` en
   « observation adjacente », avec une atténuation. **Il restait donc une question
   ouverte, précise et bornée** — exactement ce qu'un lot de classement doit
   prendre.
3. **La forme est neuve dans le classement.** Aucun des dix-sept dossiers déjà
   devisés ne porte « un zéro substitué à une absence ».

Écartés : le **416** (redevenu légitime, mais je préfère une forme neuve à une
forme que je viens de nommer), le **407** (erreur d'unité, déjà calibrée au 467 —
moins instructive), le **386+431** (le 431 a déjà posé son critère, donc moins de
travail neuf).

---

# LA MESURE

## La chaîne, remontée jusqu'à l'écran

```text
opportunities_api.py:17-22   def _followed_count():  … except Exception: return 0
opportunities_api.py:25-34   def _positions_count(): … except Exception: return 0
opportunities_api.py:37-42   @bp.route('/api/opportunities/funnel')
                             build_funnel(rows, followed=_followed_count(),
                                                positions=_positions_count())
funnel.py:102                {'key':'followed',  'label':'Suivis',    'count': int(followed or 0)}
funnel.py:103                {'key':'positions', 'label':'Positions', 'count': int(positions or 0)}
opportunities_page.py:194    f = await VX.fetch('/api/opportunities/funnel', …)
opportunities_page.py:220    VXCharts.funnel('op-funnel-viz',{stages: f.stages.map(s =>
                                              ({label: s.label, value: s.count})), …})
```

**Les deux zéros deviennent deux étages de l'entonnoir, affichés avec leur
libellé.** La chaîne est complète, du handler jusqu'au composant graphique.

## ATTEIGNABILITÉ — prouvée par exécution, dans les deux sens

```text
grep « opportunities/funnel » dans les 8 pages servies  →  /opportunities  (1 page)
opportunities_page.py:194   la route est bien FETCHÉE par la page servie
GET /api/opportunities/funnel → 200
   stages : Univers 0 · Éligibles 0 · Radar 0 · Prioritaires 0 · Actionnables 0
            · Suivis 0 · Positions 0
   clé « error » présente ?  NON
```

## L'atténuation du 378 est RÉFUTÉE

Le 378 écrivait, pour borner son observation adjacente :

> « Portée limitée : la route qui les consomme **marque bien ses propres
> erreurs** (`500` + `error`). »

**C'est faux, et la structure du code suffit à le montrer :**

```python
def _followed_count():
    try:  …
    except Exception:
        return 0            # ← LE HANDLER INTERNE AVALE ICI

@bp.route('/api/opportunities/funnel')
def opportunities_funnel():
    try:
        return jsonify(_funnel.build_funnel(…, followed=_followed_count(), …))
    except Exception as e:
        return jsonify({…, 'error': …}), 500     # ← NE SE DÉCLENCHE JAMAIS pour ces deux-là
```

**L'exception est capturée à l'intérieur, avant de pouvoir remonter.** Le
`500 + error` de la route protège tout **sauf** les deux fonctions que le 378
prétendait couvrir par lui. L'exécution le confirme : `200`, sept zéros, **aucune
clé `error`**.

**Je le compte : publiés puis corrigés, 5 → 6.** Le 378 avait bien nommé le
défaut ; c'est **son atténuation** qui était fausse, et elle allait dans le sens
qui rassure.

## Le témoin positif est dans le MÊME objet — une fois sur sept

```python
funnel.py:111-113
   'zero_actionable_is_valid': True,
   'note': ('Aucun dossier actionnable aujourd\'hui — c\'est un résultat valide, '
            'pas un manque à remplir.') if not actionable else None,
```

**Le module sait distinguer un zéro légitime d'un zéro qui manque — et il le
fait, explicitement, pour UN étage sur SEPT.** C'est le motif des 457 et 476 :
la bonne pratique est connue de l'auteur, appliquée à une fraction de son propre
objet. Sans ce témoin, j'aurais mesuré « le module ignore la question » ; avec
lui, la mesure désigne **six étages qui ne portent pas la marque que le septième
porte**.

## Classement — RANG 2, et je dis pourquoi pas rang 1

**Ce qui est établi** : sur une page servie, deux étages de l'entonnoir peuvent
afficher `0` alors que la donnée est **illisible**, sans rien qui les distingue
d'un zéro vrai — contrairement à un invariant écrit du produit, et alors que le
même objet sait marquer un zéro légitime.

**Pourquoi pas rang 1 :**

- Le chemin fautif est le **chemin d'exception**, pas le chemin normal. Sur le
  chemin normal, `0` est **exact** : `persist.load_json('desk_data.json', {})`
  rend `{}` quand le fichier est absent, `trades` devient `[]`, et
  `len([]) == 0` — **un zéro honnête**.
- **Je n'ai pas mesuré la fréquence** du chemin d'exception, et je ne l'estime
  pas. Il faut un `desk_data.json` corrompu, ou un échec de `persist`, ou une
  panne de `vertex.tracking.repository`.
- Le zéro affiché ne **change pas une consigne d'action** : l'entonnoir décrit,
  il ne prescrit pas.

**Pourquoi pas rang 3 non plus** : c'est **affiché**, c'est **servi**, c'est
**contraire à une règle écrite**, et l'objet lui-même démontre que la marque était
possible. Ce n'est pas une imperfection interne.

**Rang 2.**

## Mutualisation — mesurée, et il n'y en a aucune

Aucun des dix-sept dossiers devisés ne touche `opportunities_api.py` ni
`funnel.py`. Le 434 et le 458 vivent dans `opportunities_page.py` (lot D), mais
**pas dans les mêmes fonctions** : `renderAnomalies` (`:571`) et `catOf`
(`:475`) contre `renderFunnel` (`:192`). **Le dossier est isolé** — je le dis
parce que la mutualisation était à chercher explicitement et qu'elle est absente.

---

# LE CHIFFRAGE

**Deux variantes, et elles ne coûtent pas la même chose.**

```text
(a) MARQUER L'ÉTAT DÉGRADÉ — 3 lignes, 2 fichiers, RECOMMANDÉE
    opportunities_api.py:22  return 0  →  return None
                        :34  return 0  →  return None
    funnel.py:102-103        int(followed or 0) → conserver None et poser
                             'unknown': followed is None sur l'étage
    → le composant reçoit une valeur nulle et peut rendre « — », comme partout ailleurs

(b) N'AJOUTER QU'UN DRAPEAU — 2 lignes, 1 fichier
    poser 'degraded': True dans la réponse quand l'un des deux comptes a échoué
    → moins invasif, mais laisse le « 0 » à l'écran : la marque est dans le payload,
      pas dans le chiffre. C'est plus faible et je le dis.
```

**(a) est recommandée** parce qu'elle rend au produit son propre vocabulaire :
`—` pour l'absent. **Coût réel probable : (a) + 1 ligne de rendu** si
`VXCharts.funnel` ne sait pas afficher une valeur nulle — **je ne l'ai pas
vérifié**, et je le nomme comme un point ouvert plutôt que de le chiffrer à
l'aveugle.

## Gardien et régression

```text
gardien       tests/test_replis_zero_entonnoir_lot4xx.py
assertion     quand _followed_count / _positions_count échouent, la réponse de
              /api/opportunities/funnel NE présente PAS un compte de 0 indiscernable
              (soit None, soit un marqueur)
échoue-t-il aujourd'hui ?   OUI — mesuré par lecture : `except Exception: return 0`
              aux lignes 22 et 34, et aucune clé de dégradation dans le payload
              (vérifié à l'exécution : la réponse ne porte pas de clé « error »)

GARDIENS EXISTANTS — ET IL Y EN A, contrairement à la plupart des dossiers devisés
  tests/test_replis_exception_lot378.py   cite _followed_count ET _positions_count
  tests/test_opportunity_funnel.py        cite _positions_count, build_funnel,
                                          zero_actionable_is_valid (×2)
  tests/test_routes_closure_lot176.py     cite la route et build_funnel
  tests/test_cross_page_consistency.py    cite le libellé « Suivis »

RÉGRESSION — LA PLUS ÉLEVÉE DES DIX-HUIT DOSSIERS
  passer de 0 à None change le TYPE d'un champ consommé par au moins 4 fichiers de
  test. `test_opportunity_funnel.py` assert sur des comptes ; un `assert count == 0`
  deviendrait faux. RISQUE MOYEN À ÉLEVÉ — à relire AVANT toute correction.
  C'est la variante (b) qui minimise ce risque, au prix de la qualité du résultat.

octet servi ?  NON — routes et moteur uniquement → AUCUN BUMP, AUCUN _EMPREINTE
               (sauf si l'on touche au rendu, cas de la ligne supplémentaire ci-dessus)
moteur touché ? OUI — `vertex/opportunities/funnel.py`, mais sur deux clés d'étage,
               aucun calcul, aucun seuil
```

---

# LA FEUILLE DE DÉCISION — DIX-HUIT DOSSIERS

```text
avant ce lot   17 dossiers · 45 à 53 lignes · 17 gardiens · douze rang 1
ce lot         +1 dossier (378, RANG 2) · +3 lignes · +1 gardien
après          18 DOSSIERS · 48 à 56 LIGNES · 18 GARDIENS · DOUZE RANG 1 · SIX RANG 2
```

**Nouveau lot de travail** :

```text
I « l'entonnoir »   378   3 lignes · 2 fichiers · RANG 2 · aucun octet servi
                    ISOLÉ — aucune mutualisation avec les dix-sept autres.
                    SEUL dossier du plan dont la régression est MOYENNE À ÉLEVÉE.
```

Les huit lots A à H sont **inchangés**.

## Ce qui reste hors devis

**Seize dossiers jamais classés** (17 − 1) : 388 · 406 · 407 · 408 · 409 · 411 ·
426 · 416 · 422 · 391/396 · 379 · 363 · 386+431 · 452 (volet rang 2) · 456+459 ·
461 `winnerRule`. Plus les **trois dossiers de DÉCISION** (469, 468, 466/467).

**Et les dix autres replis numériques du recensement du 378** — les douze moins
les deux traités ici. Le 378 en avait innocenté deux (`entry_quality`,
`target_room_score`) comme **non atteints**, sans le prouver ; **les dix restants
ne sont ni tracés ni classés**. Je les nomme et je ne les compte pas.

## Ce que le lot ne prétend pas

- **Je n'ai pas rejoué le recensement du 378** (254 handlers, 12 replis
  numériques). Ces chiffres sont **les siens**, cités comme tels. Ce que **ce lot**
  mesure, c'est la **chaîne jusqu'à l'écran** de deux d'entre eux, et la
  **réfutation de son atténuation**.
- **Je n'ai pas mesuré la fréquence du chemin d'exception**, et le classement en
  tient compte : c'est la raison principale du rang 2 plutôt que 1.
- **Je n'ai pas vérifié** si `VXCharts.funnel` sait rendre une valeur nulle. La
  variante (a) pourrait coûter une ligne de plus — **point ouvert nommé, pas
  chiffré**.
- **Aucun navigateur.** Le rendu est établi sur la source servie de
  `/opportunities` et sur l'exécution de la route via `test_client`.
- **Aucun réseau. Aucun écrivain appelé. Aucun fichier de production touché.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts avec
  `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- Pages en **GET** ; `/api/opportunities/funnel` appelée en **GET** (lecture —
  `build_funnel` n'écrit rien) ; `persist` redirigé vers un `mkdtemp` **et la
  redirection vérifiée par `cache_path()`** ; **`/options/<sym>`,
  `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-dix-neuvième lot court, **deuxième de la reprise de mesure**.

Deux dossiers classés en deux lots, l'un rang 1 et l'autre rang 2. Le rythme
annoncé au 476 se confirme : **quand la mesure existe, le classement va vite** —
et il rend à chaque fois quelque chose que le rapport d'origine n'avait pas.

Le fait de méthode du lot est un cas particulier, et il est le plus utile de la
reprise :

*Le 378 s'était rassuré avec une atténuation qu'il n'avait pas vérifiée.* Il a
écrit que la route « marque bien ses propres erreurs » — c'est vrai en général,
et **faux précisément pour les deux cas qu'il bornait**, parce qu'un `try/except`
interne avale avant le `try/except` externe.

**Genre neuf : UNE PROTECTION QUI EXISTE, MAIS PAS SUR LE CHEMIN QU'ON CROIT
COUVERT.** C'est le pendant de la leçon 471 (*une donnée présente dans la page
n'est pas présente dans la fonction*) : ici, **une garde présente dans la route
n'est pas une garde présente sur l'appel**.

Et une observation que je note sans la transformer en règle : sur les six
derniers lots, **cinq atténuations ou mitigations publiées ont été démenties par
la vérification** (471 ×2, 473, 476, 477). Les défauts, eux, tiennent presque
toujours. **Ce que la boucle publie de plus fragile, ce ne sont pas ses
trouvailles — ce sont les phrases par lesquelles elle les minimise.**

Comptes séparés : résultats faux **arrêtés avant publication** **43** ; **publiés
puis corrigés** **6** (+1, l'atténuation du 378) ; **interprétations retirées**
**3** ; re-localisation **0**.

**Huit bilans — n°9 à n°16 — attendent une réponse ; le plan couvre dix-huit
dossiers, douze de rang 1, pour 48 à 56 lignes.**
