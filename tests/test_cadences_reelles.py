"""LA CADENCE ANNONCÉE EST CELLE DE LA BOUCLE — mesurée, pas recopiée.

## Ce que `interval_s` décide vraiment

Le registre s'en sert pour DEUX choses servies à l'écran :

    next_run_eta_s  = last_run + interval_s − maintenant     (« prochaine dans… »)
    etat SILENCIEUX = (maintenant − last_run) > 2 × interval_s

Le second est un diagnostic : « la boucle est morte ou coincée ». Une cadence
fausse le rend faux dans les deux sens, et aucun des deux ne se voit sans
mesurer.

## Les trois écarts mesurés

    MARKET_DATA_REFRESH   360 s annoncées   1800 s réelles
    WEEKLY_REVIEW      604800 s annoncées    300 s réelles
    TRACK_RECORD_UPDATE  86400 s annoncées  21600 s réelles

Le premier est le plus cher. Le seuil de silence tombait à 2 × 360 = 720 s,
alors que le scan ne repasse qu'à 1800 s : le job CENTRAL du produit — « Scan
univers + indices + contexte marché » — était déclaré « mort ou coincé »
pendant 1080 s de chaque cycle, soit **60 % du temps**, en tournant
parfaitement. Vérifié sur le registre lui-même, pas déduit : à 700 s ACTIF, à
800 s SILENCIEUX, jusqu'à 1799 s.

Les deux autres penchent de l'autre côté : `WEEKLY_REVIEW` annonçait la
période du ROSTER (une semaine) au lieu de la cadence de la BOUCLE (5 min), ce
qui donnait un seuil de silence de **14 jours** — une boucle réellement morte
aurait mis deux semaines à se voir.

## Pourquoi ce banc plutôt qu'une valeur figée

`test_registre_jobs::test_les_intervalles_annonces_ne_sont_pas_inventes` fait
déjà ce travail — à la main, pour deux jobs, en cherchant une chaîne dans le
source. Trois écarts lui ont échappé parce qu'il ne couvrait pas ces jobs-là.
Ici la cadence RÉELLE est extraite de la boucle par AST : le banc ne se périme
pas quand un job s'ajoute, et il n'a rien à mettre à jour quand une boucle
change de rythme — il exige seulement que les deux disent la même chose.

## La règle de lecture, et ce qu'elle écarte

La cadence réelle d'une boucle est sa PLUS LONGUE attente terminale. Les
attentes plus courtes qu'on y trouve sont des reprises et des temporisations :
`time.sleep(30 if echec else 3 * 3600)` recule de 30 s après un échec,
`45 if still_missing else 6 * 3600` accélère tant que le cache se remplit, et
`time.sleep(0.12)` espace deux appels réseau. Aucune n'est le rythme de
croisière ; c'est celui-là que l'écran annonce.

Sont hors du banc : les émetteurs qui ne vivent pas dans une boucle
(`DATA_BACKUP`, déclenché par une sauvegarde du desk) et les jobs sans cadence
déclarée — il n'y a rien à comparer.
"""
from __future__ import annotations

import ast
import importlib
import os

import pytest

import terminal

_reg = importlib.import_module('vertex.scheduler.registry')
_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SOURCE = os.path.join(_RACINE, 'terminal.py')

with open(_SOURCE, encoding='utf-8') as _f:
    _ARBRE = ast.parse(_f.read())
_FONCTIONS = {n.name: n for n in ast.walk(_ARBRE) if isinstance(n, ast.FunctionDef)}


def _secondes(n):
    """Plie une expression d'attente en secondes, ou rend None.

    `terminal` est interrogé pour les constantes nommées (`REFRESH_SEC`) :
    lire la valeur RÉELLEMENT en vigueur, et non un littéral recopié, est tout
    l'objet de ce banc.
    """
    try:
        return float(ast.literal_eval(n))
    except (ValueError, TypeError, SyntaxError):
        pass
    if isinstance(n, ast.Name):
        v = getattr(terminal, n.id, None)
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult):
        a, b = _secondes(n.left), _secondes(n.right)
        return a * b if (a is not None and b is not None) else None
    if isinstance(n, ast.IfExp):                    # `30 if echec else 3 * 3600`
        vs = [v for v in (_secondes(n.body), _secondes(n.orelse)) if v is not None]
        return max(vs) if vs else None
    return None


def _attentes(fn) -> list[float]:
    """Toutes les attentes d'une fonction : `time.sleep`, `wait_force`, `.wait`."""
    out = []
    for n in ast.walk(fn):
        if not isinstance(n, ast.Call):
            continue
        nom = getattr(n.func, 'attr', None)
        if nom == 'sleep' and n.args:
            v = _secondes(n.args[0])
        elif nom == 'wait_force' and len(n.args) >= 2:
            v = _secondes(n.args[1])
        elif nom == 'wait' and n.args:
            v = _secondes(n.args[0])
        else:
            continue
        if v is not None:
            out.append(v)
    return out


def _boucles_emettrices() -> dict[str, str]:
    """{job: nom de la fonction-boucle qui l'émet}. Seules les fonctions qui
    portent un `while` : un émetteur hors boucle n'a pas de cadence propre."""
    out = {}
    for nom, fn in _FONCTIONS.items():
        if not any(isinstance(x, ast.While) for x in ast.walk(fn)):
            continue
        for n in ast.walk(fn):
            if (isinstance(n, ast.Call) and getattr(n.func, 'attr', None) == 'beat'
                    and n.args and isinstance(n.args[0], ast.Constant)):
                out[n.args[0].value] = nom
    return out


def _a_comparer() -> list[tuple[str, int, str]]:
    boucles = _boucles_emettrices()
    return [(nom, iv, boucles[nom])
            for nom, _d, iv, impl in _reg._CANONICAL_4
            if impl and iv is not None and nom in boucles]


# ── 1. Anti-vide ────────────────────────────────────────────────────────────

def test_le_lecteur_de_cadence_plie_bien_les_trois_formes():
    """Un lecteur qui rend `None` partout ferait passer ce banc en ne comparant
    rien. Les trois formes qui existent dans le dépôt sont éprouvées."""
    lu = lambda code: _secondes(ast.parse(code, mode='eval').body)  # noqa: E731
    assert lu('120') == 120
    assert lu('3 * 3600') == 10800
    assert lu('30 if echec else 3 * 3600') == 10800, 'la reprise doit perdre'
    assert lu('REFRESH_SEC') == float(terminal.REFRESH_SEC), (
        'une constante nommée n’est pas résolue — le banc comparerait un '
        'littéral recopié au lieu de la valeur en vigueur')
    assert lu('une_variable_qui_n_existe_pas') is None


def test_le_banc_couvre_bien_les_boucles_connues():
    couverts = {nom for nom, _iv, _fn in _a_comparer()}
    attendus = {'MARKET_DATA_REFRESH', 'CATALYST_REFRESH', 'NEWS_REFRESH',
                'ALERTS_EVALUATION', 'WEEKLY_REVIEW', 'TRACK_RECORD_UPDATE',
                'FUNDAMENTALS_REFRESH', 'OPTIONS_BOARD_REFRESH',
                'MARKET_RADAR_REFRESH'}
    manquants = sorted(attendus - couverts)
    assert not manquants, (
        'ces boucles cadencées ne sont plus comparées — leur émetteur a quitté '
        'sa boucle, ou leur cadence est passée à None : %s' % manquants)


def test_chaque_boucle_comparee_a_bien_des_attentes():
    """Dénominateur : une fonction dont on ne sait lire aucune attente rendrait
    la comparaison vide, donc toujours vraie."""
    for nom, _iv, fnnom in _a_comparer():
        assert _attentes(_FONCTIONS[fnnom]), (
            'aucune attente lisible dans %s (job %s) — la comparaison ne '
            'porterait sur rien' % (fnnom, nom))


# ── 2. Le contrat ───────────────────────────────────────────────────────────

@pytest.mark.parametrize('job,declare,boucle', _a_comparer())
def test_la_cadence_annoncee_est_celle_de_la_boucle(job, declare, boucle):
    reel = max(_attentes(_FONCTIONS[boucle]))
    assert reel == declare, (
        '%s annonce %g s, mais %s tourne à %g s. Deux conséquences servies : '
        '« prochaine dans ~%g s » est faux, et l’état SILENCIEUX tombe à %g s '
        'pour un cycle de %g — %s.'
        % (job, declare, boucle, reel, declare, 2 * declare, reel,
           ('le job serait déclaré mort %g s par cycle en tournant '
            'normalement' % (reel - 2 * declare)) if 2 * declare < reel else
           ('une boucle réellement morte mettrait %.1f jours à se voir'
            % (2 * declare / 86400.0))))


# ── 3. La conséquence, éprouvée sur le registre et non déduite ──────────────

@pytest.mark.parametrize('job,declare,boucle', _a_comparer())
def test_une_boucle_SAINE_n_est_jamais_declaree_silencieuse(job, declare, boucle):
    """La propriété que la cadence sert. Un job qui vient de battre et repasse
    à son rythme normal doit rester ACTIF jusqu'au bout de son cycle."""
    import time

    reel = max(_attentes(_FONCTIONS[boucle]))
    memoire = dict(_reg._JOBS[job])
    try:
        _reg.beat(job, ok=True)
        #  Juste avant le passage suivant : le pire instant d'un cycle sain.
        _reg._JOBS[job]['last_run'] = time.time() - (reel - 1)
        etat = next(j for j in _reg.jobs() if j['name'] == job)['etat']
        assert etat == 'ACTIF', (
            '%s est « %s » une seconde avant son passage suivant, alors qu’il '
            'tourne normalement : la page Système annonce une panne qui '
            'n’existe pas' % (job, etat))
    finally:
        _reg._JOBS[job].update(memoire)


@pytest.mark.parametrize('job,declare,boucle', _a_comparer())
def test_une_boucle_MORTE_est_bien_declaree_silencieuse(job, declare, boucle):
    """Contre-épreuve : allonger une cadence rendrait le banc précédent vrai
    partout et le diagnostic inutile. Passé deux cycles, le silence doit être
    dit."""
    import time

    reel = max(_attentes(_FONCTIONS[boucle]))
    memoire = dict(_reg._JOBS[job])
    try:
        _reg.beat(job, ok=True)
        _reg._JOBS[job]['last_run'] = time.time() - (2 * reel + 60)
        etat = next(j for j in _reg.jobs() if j['name'] == job)['etat']
        assert etat == 'SILENCIEUX', (
            '%s muet depuis plus de deux cycles ressort « %s » — une boucle '
            'morte ne serait plus signalée' % (job, etat))
    finally:
        _reg._JOBS[job].update(memoire)


# ── 4. La cadence du scan n'est plus un duplicata ───────────────────────────

def test_la_cadence_du_scan_est_DERIVEE_et_non_recopiee():
    """Elle valait 360 dans le registre pour un `REFRESH_SEC` de 1800 : deux
    nombres pour une seule vérité, et c'est toujours le duplicata qui dérive.
    Le registre lit désormais le propriétaire."""
    from vertex.data import constants
    par_nom = {n: i for n, _d, i, _o in _reg._CANONICAL_4}
    assert par_nom['MARKET_DATA_REFRESH'] == constants.REFRESH_SEC
    with open(os.path.join(_RACINE, 'vertex', 'scheduler', 'registry.py'),
              encoding='utf-8') as f:
        src = f.read()
    assert 'from vertex.data.constants import REFRESH_SEC' in src, (
        'le registre a cessé de dériver la cadence du scan : elle peut de '
        'nouveau diverger de son propriétaire sans que rien ne le dise')
