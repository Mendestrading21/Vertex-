"""
LOT 385 — LE RECENSEMENT DES REPLIS S'ARRÊTAIT À `vertex/`. IL Y A 113 HANDLERS
DERRIÈRE CETTE FRONTIÈRE, DONT 101 DANS LE MONOLITHE.

Le lot 378 a gelé le recensement des replis numériques — « un `except` qui
renvoie un nombre substitue une valeur plausible à une donnée manquante :
l'utilisateur ne peut pas distinguer la mesure du repli » (invariant n°4). Sa
propriété centrale, `test_aucun_repli_numerique_non_recense`, est le seul filet
contre l'apparition silencieuse d'un tel repli.

Elle a un `RACINE = 'vertex'` en dur.

## La mesure

```
handlers `except` dans vertex/     254   ← périmètre du recensement 378
handlers `except` hors vertex/     113   ← jamais comptés
    dont terminal.py               101
         verifier_vertex.py          9   ← script d'audit, non importé par l'app
         ib_reader.py                2
         test_connection.py          1   ← script de diagnostic, non importé
```

**31 % des handlers de production étaient hors du filet**, dont la totalité du
monolithe qui sert encore des routes.

## La preuve que c'est un trou, et non un gardien inutile

Un `except: return 50` NEUF — exactement ce que la propriété 378 interdit —
ajouté dans `terminal.py` : **2 793 tests passent**. Le même défaut, mot pour
mot, ajouté dans `vertex/engines/stats.py` : **la suite tombe**.

Le gardien 378 fait donc précisément ce que son code dit. Ce n'est pas une
myopie du détecteur, c'est sa **frontière** — la catégorie de trou trouvée au
lot 381 (le repli servi de `deskKeys()` que rien ne gardait).

## Les trois replis existants de terminal.py : honnêtes, et pourquoi

Aucun n'est une faute — mais chacun est gelé ici avec sa raison, vérifiée sur
valeurs réelles et non par lecture.

- **`_seed_fund_from_company` (L162) → `0`** : compteur de titres enrichis. `0`
  signifie exactement « aucun enrichi ». Même famille que `track_record` dans le
  recensement 378 : le nombre est la mesure, pas un substitut.
- **`_i` (L203) → `0` et `_f` (L210) → `0.0`** : coercitions numériques. Leur
  `0` EST un substitut à une donnée absente — c'est la forme dangereuse. Ce qui
  les rend honnêtes n'est pas la fonction, **c'est le site d'appel** : les trois
  seuls appels du dépôt sont dans la chaîne d'options, où un `0` est
  immédiatement **écarté** (`if iv <= 0 or oi <= 0: continue`, et `K` hors de
  `[spot·0.9, spot·1.1]` saute aussi). La ligne servie ne compte donc jamais un
  repli comme une mesure.

  **C'est le garde-fou du site d'appel qui tient l'invariant, pas la coercition.**
  S'il disparaissait, un `0` de repli entrerait dans la médiane d'IV ATM et dans
  le GEX servis. Les tests ci-dessous le verrouillent explicitement, car c'est la
  seule pièce fragile des trois.

## Ce que ce gardien ne prétend pas

Il étend le recensement, il ne juge pas les 38 `except: pass` de `terminal.py`
un par un — le lot 379 l'a fait pour les 46 de `vertex/`. Et une borne de
population rend la **dérive** visible : elle ne dit pas que la population
actuelle est bonne.
"""
import ast
import os

import pytest

# Périmètre : les fichiers de PRODUCTION hors `vertex/`, c'est-à-dire ceux que
# l'application importe. `terminal.py` est le monolithe ; `ib_reader.py` est
# importé par lui (L2057) pour la connexion IBKR.
RACINES = ('terminal.py', 'ib_reader.py')

# Exclusions JUSTIFIÉES : scripts autonomes, jamais importés par l'application,
# donc hors de la surface où un repli pourrait être servi à l'utilisateur.
# Vérifié par `test_les_exclusions_restent_des_scripts_autonomes`.
HORS_PRODUCTION = ('test_connection.py', 'verifier_vertex.py')

# Recensement GELÉ — mêmes règles qu'au lot 378 : tout ajout doit passer ici,
# avec sa justification, plutôt que d'apparaître en silence.
REPLIS_NUMERIQUES = {
    ('terminal.py', 0),      # _seed_fund_from_company : compteur exact ;
                             # _i : coercition, le 0 est écarté au site d'appel
    ('terminal.py', 0.0),    # _f : idem
}

# Bornes fixées À LA MESURE (leçon du lot 378 : une borne qui absorbe la
# première régression n'est pas une borne). Un dépassement réclame un examen
# humain, pas un relèvement automatique.
NB_HANDLERS_TERMINAL = 101
MAX_PASS_SEC_TERMINAL = 38
MAX_NUMERIQUES = 3


def _arbre(chemin):
    return ast.parse(open(chemin, encoding='utf-8').read())


def _handlers(racines=RACINES):
    for chemin in racines:
        for n in ast.walk(_arbre(chemin)):
            if isinstance(n, ast.ExceptHandler):
                yield chemin, n


def _replis_numeriques():
    """[(fichier, ligne, valeur)] — un `except` qui renvoie un NOMBRE.

    Critère identique à celui du lot 378, pour que les deux recensements soient
    comparables.
    """
    out = []
    for chemin, h in _handlers():
        for n in ast.walk(ast.Module(body=h.body, type_ignores=[])):
            if not (isinstance(n, ast.Return) and n.value is not None):
                continue
            v = n.value
            if isinstance(v, ast.UnaryOp) and isinstance(v.operand, ast.Constant):
                v = v.operand
            if isinstance(v, ast.Constant) and isinstance(v.value, (int, float)) \
                    and not isinstance(v.value, bool):
                out.append((chemin, n.lineno, v.value))
    return out


def _pass_secs(chemin='terminal.py'):
    return [h.lineno for c, h in _handlers((chemin,))
            if all(isinstance(x, ast.Pass) for x in h.body)]


# ── 1. Le dénominateur — sans lui, un « 0 » ne prouverait rien ──────────────

def test_le_perimetre_existe_reellement():
    for chemin in RACINES:
        assert os.path.exists(chemin), 'périmètre cassé : %s absent' % chemin


def test_le_detecteur_voit_bien_les_handlers_du_monolithe():
    """Leçon des lots 375-377 : une propriété au vert sur un détecteur aveugle
    ne vaut rien. Si `terminal.py` fond ou si le détecteur casse, ce test le
    dit avant que le recensement ne devienne vide de sens."""
    n = len(list(_handlers(('terminal.py',))))
    assert n >= 80, (
        'seulement %d handlers `except` trouvés dans terminal.py (mesuré %d au '
        'lot 385) — détecteur cassé ou monolithe purgé : revérifier le '
        'recensement avant de faire confiance aux tests suivants'
        % (n, NB_HANDLERS_TERMINAL))


def test_le_detecteur_retrouve_les_trois_replis_connus():
    """Anti-vide du détecteur lui-même : s'il ne trouvait plus rien, la
    propriété centrale passerait pour une bonne raison ET pour une mauvaise."""
    trouves = _replis_numeriques()
    assert len(trouves) == MAX_NUMERIQUES, (
        'le détecteur trouve %d replis numériques, %d attendus au lot 385 : %s'
        % (len(trouves), MAX_NUMERIQUES, trouves))


# ── 2. La propriété — celle que le périmètre du lot 378 laissait passer ─────

def test_aucun_repli_numerique_non_recense_hors_vertex():
    """LA propriété, portée à la frontière que le lot 378 n'a jamais franchie.

    Prouvé au lot 385 : avant ce test, un `except: return 50` neuf dans
    `terminal.py` passait les 2 793 tests, alors que le même défaut dans
    `vertex/` faisait tomber la suite.
    """
    inconnus = [(c, l, v) for c, l, v in _replis_numeriques()
                if (c, v) not in REPLIS_NUMERIQUES]
    assert not inconnus, (
        'repli numérique NON RECENSÉ hors `vertex/` — un chiffre plausible y '
        'remplace une donnée manquante sans que rien ne le signale (invariant '
        'n°4) : %s' % ' | '.join('%s L%d → %r' % x for x in inconnus))


def test_le_recensement_ne_se_perime_pas():
    """Une entrée qui ne correspond plus à rien doit être RETIRÉE : sinon la
    liste blanche pourrit et couvre des cas disparus (leçon des lots 373-377)."""
    vus = {(c, v) for c, _l, v in _replis_numeriques()}
    mortes = REPLIS_NUMERIQUES - vus
    assert not mortes, 'entrées périmées à retirer du recensement : %s' % sorted(mortes)


def test_la_population_des_pass_secs_ne_derive_pas():
    """Ne juge pas le code : rend la dérive visible. Borne fixée À la mesure."""
    n = len(_pass_secs())
    assert n <= MAX_PASS_SEC_TERMINAL, (
        '%d `except: pass` secs dans terminal.py (borne %d, fixée à la mesure '
        'du lot 385) — examiner les nouveaux cas avant de relever la borne'
        % (n, MAX_PASS_SEC_TERMINAL))


# ── 3. Aucune surface de production ne doit rester hors des deux filets ─────

def test_aucun_module_racine_echappe_aux_deux_recensements():
    """Anti-rot du périmètre lui-même. Un nouveau module de production à la
    racine tomberait aujourd'hui dans l'angle mort des DEUX recensements
    (`vertex/` pour le 378, RACINES pour celui-ci) : ce test force la décision
    au lieu de la laisser passer en silence."""
    connus = set(RACINES) | set(HORS_PRODUCTION)
    orphelins = []
    for nom in sorted(os.listdir('.')):
        if not nom.endswith('.py') or nom in connus:
            continue
        try:
            arbre = _arbre(nom)
        except SyntaxError:
            continue
        if any(isinstance(n, ast.ExceptHandler) for n in ast.walk(arbre)):
            orphelins.append(nom)
    assert not orphelins, (
        'module(s) racine avec des handlers `except` hors des deux '
        'recensements : %s — les ajouter à RACINES (production) ou à '
        'HORS_PRODUCTION (script autonome), avec la justification'
        % ', '.join(orphelins))


def test_les_exclusions_restent_des_scripts_autonomes():
    """Les exclusions ne valent que tant qu'elles sont vraies : si un script
    exclu devenait importé par l'application, ses replis deviendraient
    servables et l'exclusion silencieusement fausse."""
    sources = []
    for chemin in RACINES:
        sources.append(open(chemin, encoding='utf-8').read())
    for rac, _d, noms in os.walk('vertex'):
        for nom in noms:
            if nom.endswith('.py'):
                sources.append(open(os.path.join(rac, nom), encoding='utf-8').read())
    blob = '\n'.join(sources)
    for exclu in HORS_PRODUCTION:
        mod = exclu[:-3]
        assert ('import %s' % mod) not in blob, (
            '%s est désormais importé par la production : il doit passer dans '
            'RACINES et ses replis être recensés' % exclu)


# ── 4. Ce qui tient réellement l'invariant : le site d'appel ────────────────

def test_les_coercitions_transforment_bien_une_absence_en_zero():
    """Sur VALEURS RÉELLES, pas par lecture (leçon du lot 378, où `50` s'est
    révélé ne PAS être le neutre de l'échelle). Établit la prémisse : le `0` de
    `_i`/`_f` est bien un substitut, pas une mesure."""
    import terminal
    for absent in (None, float('nan'), 'abc', {}):
        assert terminal._i(absent) == 0
        assert terminal._f(absent) == 0.0
    assert terminal._i('7') == 7 and terminal._f('7') == 7.0


@pytest.mark.parametrize('garde', [
    'if iv <= 0 or oi <= 0:',
    'if K < lo or K > hi:',
])
def test_le_site_d_appel_ecarte_le_zero_de_repli(garde):
    """LA pièce fragile. Les coercitions sont inoffensives UNIQUEMENT parce que
    leur `0` est écarté avant d'entrer dans un calcul servi. Si ce garde-fou
    disparaissait, un repli entrerait dans la médiane d'IV ATM et dans le GEX
    rendus à l'utilisateur — un chiffre inventé présenté comme réel."""
    src = open('terminal.py', encoding='utf-8').read()
    assert garde in src, (
        'garde-fou « %s » disparu de la chaîne d\'options : les 0 de repli de '
        '_i/_f entreraient désormais dans des calculs SERVIS (IV ATM, GEX). '
        'C\'est ce garde-fou, et non la coercition, qui tient l\'invariant n°4.'
        % garde)


def test_les_coercitions_n_ont_pas_essaime():
    """Le raisonnement ci-dessus tient parce que `_i`/`_f` ne sont appelées
    QUE dans la chaîne d'options. Un nouvel appel ailleurs échapperait à la
    démonstration et devrait être examiné."""
    appels = [n for n in ast.walk(_arbre('terminal.py'))
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id in ('_i', '_f')]
    assert len(appels) <= 3, (
        '%d appels à _i/_f (3 au lot 385, tous dans la chaîne d\'options où le '
        '0 est écarté) — vérifier que les nouveaux sites écartent aussi le '
        'repli avant de relever la borne' % len(appels))


def test_le_compteur_de_seeding_est_bien_un_compteur(monkeypatch):
    """`_seed_fund_from_company` → 0 n'est un repli honnête que si 0 signifie
    « aucun enrichi ». Vérifié sur le vrai retour, pas sur la docstring.

    L'écriture du cache est neutralisée : sur une machine au cache incomplet,
    la fonction sauvegarderait `fund_cache.json` — un test ne doit jamais muter
    un fichier runtime.
    """
    import terminal
    ecritures = []
    monkeypatch.setattr(terminal, '_save_json',
                        lambda *a, **k: ecritures.append(a[:1]))
    n = terminal._seed_fund_from_company()
    assert not ecritures, 'le test a tenté une écriture runtime : %s' % ecritures
    assert isinstance(n, int) and not isinstance(n, bool), (
        'le retour n\'est plus un compteur entier : %r' % (n,))
    assert n >= 0, 'un compteur d\'écritures ne peut pas être négatif : %r' % (n,)
