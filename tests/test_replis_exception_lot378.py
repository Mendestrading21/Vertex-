"""
LOT 378 — LES EXCEPTIONS COMME CONVENTION DE REFUS : recensement gelé.

Angle mort déclaré au lot 377. Risque produit précis : un `except` qui avale une
erreur transforme une donnée MANQUANTE en **blanc muet**, ou pire en **chiffre
plausible** — l'utilisateur lit « rien à signaler » ou « 50 » là où la vérité est
« je n'ai pas pu savoir ». C'est l'invariant n°4.

## Mesure (254 handlers `except` dans `vertex/`)

```
except → repli NU (ni trace ni marque)   124   48,8 %
except → autre (continue/assign…)         66   26,0 %
except: pass (avale tout)                 46   18,1 %
except → repli MARQUÉ                     17    6,7 %
except → trace conservée                   1    0,4 %
raise : 39 portant une exception, dont 1 seul sans message
```

(Mon premier audit annonçait « 40 dont 2 » : il comptait avec un critère plus
large — les messages construits par `%` y passaient pour absents. Chiffre corrigé
sur le critère réellement employé par le gardien.)

Le chiffre de 124 « replis nus » est trompeur, et mon premier classement
confondait deux choses opposées. Ce que le handler **renvoie** tranche :

```
None          70   ← contrat « valeur ou None » : HONNÊTE, l'appelant affiche —
expression    35
NOMBRE        12   ← seule famille qui menace l'invariant
liste vide     8
dict vide      7
dict           5
booléen        4
```

## Les 12 replis numériques, examinés un par un

La plupart sont des **compteurs** où 0 est exact : `track_record` renvoie le
nombre d'enregistrements écrits, donc 0 si rien n'a été écrit.

Deux méritaient un examen : `quant_engine.entry_quality` et
`target_room_score`, qui renvoient **50** — une valeur de milieu d'échelle.
J'allais les excuser en disant que 50 est le neutre déclaré de l'échelle
(`s = 50.0` en tête de fonction, `_f(…, 50)` pour les entrées manquantes).
**Vérification sur valeurs réelles : c'est faux.**

```
entry_quality({})    = 76      ← entrée VIDE, tout par défaut
entry_quality(None)  = 50      ← chemin except
entry_quality(réel)  = 95
```

`s = 50.0` est un point de départ **interne**, pas ce que la fonction produit
pour une entrée neutre : à vide elle rend 76. Le repli 50 est donc bien un
nombre **plausible et indiscernable** d'un score calculé. La vérification sur
valeurs réelles m'a corrigé dans le sens inverse de d'habitude — j'étais sur le
point d'innocenter le code sur une prémisse fausse.

## Verdict : CARACTÉRISATION, pas de faute prouvée

Le chemin est **défensif** : il exige que `d` ne soit pas un dict (`None`), alors
que les appelants passent des lignes de scan. Il n'est pas atteint en
production, et je n'ai pas trouvé d'entrée réelle qui l'atteigne. Mais **s'il
l'était, l'utilisateur verrait 50 sans rien qui le distingue d'une mesure**.

Je ne touche donc à rien : ce serait modifier un moteur de scoring sur un défaut
non démontré. Ce que ce lot livre, c'est le **recensement gelé** — aucun nouveau
repli numérique ne pourra apparaître en silence, et la dérive de la population
des handlers sera visible.

Observation adjacente, versée aux dossiers : `opportunities_api._followed_count`
et `_positions_count` renvoient `0` sur exception, rendant « desk illisible » et
« desk vide » indiscernables. Portée limitée — la route qui les consomme marque
bien ses propres erreurs (`500` + `error`).
"""
import ast
import os

import pytest

from vertex.engines import quant_engine

RACINE = 'vertex'

# Recensement GELÉ des replis numériques, avec leur justification. Tout ajout
# doit passer ici — et être justifié — plutôt que d'apparaître en silence.
REPLIS_NUMERIQUES = {
    ('vertex/options/legacy_engine.py', 0),
    ('vertex/options/legacy_engine.py', 0.0),
    ('vertex/app/routes/opportunities_api.py', 0),     # compteurs (voir docstring)
    ('vertex/engines/quant_engine.py', 0),
    ('vertex/engines/quant_engine.py', 50),            # score plausible — caractérisé
    ('vertex/engines/quant_engine.py', 0.0),
    ('vertex/engines/track_record.py', 0),             # nombre d'écritures : exact
    ('vertex/quant/ml_calibration.py', 0.0),
    #  #779/G1 — `_i` et `_f` ont suivi leur unique appelant, `options_pack`,
    #  depuis `terminal.py`. Ce sont les MÊMES coercitions, au même endroit de
    #  la chaîne d'options, et les garde-fous qui écartent leur 0 avant tout
    #  calcul servi (`if iv <= 0 or oi <= 0`, `if K < lo or K > hi`) ont déménagé
    #  avec elles — c'est ce déplacement conjoint qui préserve le raisonnement.
    #  Recensé ici pour que la frontière `vertex/` reste complète.
    ('vertex/options/pack.py', 0),      # _i : coercition, 0 écarté au site d'appel
    ('vertex/options/pack.py', 0.0),    # _f : idem
}

# Bornes de population. Elles ne jugent pas le code : elles rendent la DÉRIVE
# visible. Un écart réclame un examen, pas une correction automatique.
MAX_PASS_SEC = 50          # mesuré : 46
MAX_NUMERIQUES = 14        # mesuré : 14 apres l'arrivee de _i/_f


def _fichiers():
    out = []
    for rac, _d, noms in os.walk(RACINE):
        for nom in sorted(noms):
            if nom.endswith('.py'):
                out.append(os.path.join(rac, nom).replace(os.sep, '/'))
    return out


def _handlers():
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if isinstance(n, ast.ExceptHandler):
                yield chemin, n


def _replis_numeriques():
    """[(fichier, ligne, valeur)] — un `except` qui renvoie un NOMBRE."""
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


def _pass_secs():
    return [(c, h.lineno) for c, h in _handlers()
            if all(isinstance(x, ast.Pass) for x in h.body)]


# ── 1. Périmètre et anti-vide ───────────────────────────────────────────────

def test_le_perimetre_couvre_les_moteurs():
    f = _fichiers()
    assert 'vertex/engines/quant_engine.py' in f, 'périmètre incomplet'
    assert len(f) >= 100, 'seulement %d fichiers balayés' % len(f)


def test_le_detecteur_voit_bien_des_handlers():
    """Sans dénominateur, les bornes ci-dessous ne prouveraient rien
    (leçon des lots 375-377)."""
    n = sum(1 for _ in _handlers())
    assert n >= 150, 'seulement %d handlers `except` trouvés — détecteur cassé' % n


# ── 2. Le recensement gelé ──────────────────────────────────────────────────

def test_aucun_repli_numerique_non_recense():
    """LA propriété. Un `except` qui renvoie un nombre substitue une valeur
    plausible à une donnée manquante : l'utilisateur ne peut pas distinguer la
    mesure du repli. Tout nouveau cas doit être justifié ici, pas apparaître en
    silence."""
    inconnus = [(c, l, v) for c, l, v in _replis_numeriques()
                if (c, v) not in REPLIS_NUMERIQUES]
    assert not inconnus, (
        'repli numérique NON RECENSÉ dans un `except` — un chiffre plausible y '
        'remplace une donnée manquante sans que rien ne le signale : %s'
        % ' | '.join('%s L%d → %r' % x for x in inconnus))


def test_le_recensement_ne_se_perime_pas():
    """Anti-péremption (leçon des lots 373-377) : une entrée du recensement qui
    ne correspond plus à rien doit être retirée, sinon la liste blanche pourrit
    en silence et couvre des cas qui n'existent plus."""
    vus = {(c, v) for c, _l, v in _replis_numeriques()}
    mortes = REPLIS_NUMERIQUES - vus
    assert not mortes, 'entrées périmées à retirer du recensement : %s' % sorted(mortes)


@pytest.mark.parametrize('quoi,mesure,borne', [
    ('replis numériques', lambda: len(_replis_numeriques()), MAX_NUMERIQUES),
    ('`except: pass` secs', lambda: len(_pass_secs()), MAX_PASS_SEC),
])
def test_la_population_des_handlers_ne_derive_pas(quoi, mesure, borne):
    """Ces bornes ne jugent pas le code : elles rendent la DÉRIVE visible. Un
    dépassement réclame un examen humain, pas une correction automatique."""
    n = mesure()
    assert n <= borne, (
        '%d %s (borne %d) — la population a dérivé, examiner les nouveaux cas '
        'avant de relever la borne' % (n, quoi, borne))


# ── 3. La caractérisation, sur VALEURS RÉELLES ──────────────────────────────

def test_le_repli_50_n_est_pas_le_neutre_de_l_echelle():
    """Caractérisation du lot, vérifiée en exécution — et non déduite du code.

    J'allais innocenter `except: return 50` en disant que 50 est le neutre
    déclaré (`s = 50.0`). C'est faux : à entrée VIDE la fonction rend 76. Le
    repli est donc un score plausible, indiscernable d'une mesure. Si un jour ce
    test échoue parce que les deux valeurs coïncident, la caractérisation change
    et le rapport du lot 378 doit être relu."""
    vide = quant_engine.entry_quality({})
    repli = quant_engine.entry_quality(None)
    assert repli == 50, 'le chemin except ne rend plus 50 (%r)' % repli
    assert vide != repli, (
        'entrée vide et repli coïncident (%r) — la caractérisation du lot 378 '
        'ne tient plus' % vide)


def test_le_chemin_except_est_bien_atteignable():
    """Anti-vide de la caractérisation : si l'except n'était plus atteignable,
    le test précédent ne prouverait rien."""
    assert quant_engine.entry_quality(None) == 50
    assert isinstance(quant_engine.entry_quality({}), (int, float))


# ── 4. Les `raise` portent un message ───────────────────────────────────────

def test_presque_tous_les_raise_portent_un_message():
    """40 `raise` mesurés, 2 sans message littéral. Un `raise` muet remonte une
    erreur que personne ne peut interpréter."""
    total = muets = 0
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if not (isinstance(n, ast.Raise) and n.exc is not None):
                continue
            total += 1
            exc = n.exc
            a_msg = isinstance(exc, ast.Call) and bool(exc.args)
            if not a_msg:
                muets += 1
    assert total >= 20, 'seulement %d `raise` trouvés — détecteur cassé' % total
    # Mesuré avec CE critère : 39 `raise`, dont 1 muet (`vertex/ai/provider.py`,
    # un `NotImplementedError` d'interface). La borne est fixée À la mesure, pas
    # au-dessus : une tolérance de 3 absorbait la première régression sans
    # mordre — constaté en preuve ROUGE. **Une borne qui absorbe la première
    # régression n'est pas une borne.**
    assert muets <= 1, '%d `raise` sans message sur %d — la dérive commence' % (muets, total)
