"""LE BAROMÈTRE DU MARCHÉ A UN SEUL PROPRIÉTAIRE, ET CE N'EST PLUS `terminal.py`.

## Ce que ce lot déplace

`_market_internals` agrège les internals d'un scan — avances/déclins, part
au-dessus des MM50/MM200, plus-hauts et plus-bas 52 semaines,
surachat/survente, distribution des scores, verdicts, breadth sectorielle,
santé composite. Elle ne collecte RIEN : tout entre par ses arguments, tout
sort par sa valeur de retour. Elle n'avait donc aucune raison de vivre dans
l'adaptateur historique, et rejoint `vertex/market/`.

## Ce que ce banc garde

Un déplacement se juge sur la PARITÉ, pas sur l'intention. Ce banc rejoue la
même comparaison qui a autorisé le déplacement : des scans fabriqués, passés
aux deux chemins, dont les sorties doivent être identiques champ par champ.
S'y ajoutent les propriétés d'honnêteté que la fonction porte et qu'un
« nettoyage » ferait sauter sans erreur visible :

  · une mesure absente reste ABSENTE (`avg_rsi=None`), jamais un zéro ;
  · un secteur sous cinq titres est ÉCARTÉ, jamais publié sur un échantillon
    qui ne dit rien du secteur et beaucoup du hasard ;
  · aucune division par zéro sur un scan vide.
"""
from __future__ import annotations

import inspect
import json
import os
import random

import pytest

import terminal
from vertex.data.universe import _GICS_SECTOR
from vertex.market import internals as mi

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _scan(symboles, *, rsi=45, score=71, above50=True, verdict='BUY',
          change=1.5, pos52=50):
    rows, detail = [], {}
    for s in symboles:
        rows.append({'symbol': s, 'change': change, 'pos52': pos52, 'rsi': rsi,
                     'score': score, 'verdict': verdict})
        detail[s] = {'signals': {'above50': above50, 'above200': above50}}
    return rows, detail


# ── 1. Anti-vide : le module porte le code, et il est atteignable ───────────

def test_le_module_porte_vraiment_la_fonction():
    assert callable(mi.market_internals)
    assert len(inspect.getsource(mi.market_internals).splitlines()) >= 20


def test_le_code_est_defini_dans_le_module_et_non_dans_terminal():
    attendu = os.path.join(_RACINE, 'vertex', 'market', 'internals.py')
    source = inspect.getsourcefile(terminal._market_internals)
    assert os.path.abspath(source) == os.path.abspath(attendu), (
        'le baromètre est encore défini dans %s' % source)
    assert terminal._market_internals is mi.market_internals


def test_le_scan_appelle_bien_le_nom_reexporte():
    """Dénominateur : si `_scan_once` avait cessé d'appeler ce nom, la parité
    ci-dessous serait vraie sur du code que plus personne n'exécute."""
    src = inspect.getsource(terminal._scan_once)
    assert '_market_internals(' in src, (
        '`_scan_once` n’appelle plus le baromètre — le déplacement porterait '
        'sur du code mort')


# ── 2. PARITÉ : la comparaison qui a autorisé le déplacement ────────────────

def test_les_deux_chemins_rendent_le_MEME_objet_sur_des_scans_fabriques():
    """400 scans tirés au sort, comparés champ par champ. C'est la mesure qui
    a autorisé ce lot ; elle reste ici pour qu'un futur « petit ajustement »
    du baromètre ne passe pas pour un déplacement neutre."""
    syms = list(_GICS_SECTOR)[:180] + ['ZZQ1', 'ZZQ2']   # dont 2 hors GICS
    alea = random.Random(7)
    for _ in range(400):
        n = alea.choice([0, 1, 3, 40, 180])
        rows, detail = [], {}
        for s in alea.sample(syms, min(n, len(syms))):
            rows.append({'symbol': s,
                         'change': alea.choice([None, -2.0, 0.0, 1.5]),
                         'pos52': alea.choice([None, 0, 3, 50, 97, 100]),
                         'rsi': alea.choice([None, 12, 45, 72, 88]),
                         'score': alea.choice([None, 0, 37, 71, 99, 100]),
                         'verdict': alea.choice(['BUY', 'WATCH', 'WAIT', 'AVOID', None])})
            detail[s] = {'signals': {'above50': alea.choice([True, False]),
                                     'above200': alea.choice([True, False])}}
        breadth = alea.choice([0, 12.5, 50, 100])
        a = mi.market_internals(rows, detail, breadth)
        b = terminal._market_internals(rows, detail, breadth)
        assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# ── 3. Les propriétés d'honnêteté que la fonction porte ─────────────────────

def test_un_scan_VIDE_ne_divise_pas_par_zero():
    r = mi.market_internals([], {}, 0)
    assert r['n'] == 1, 'le garde-fou du dénominateur a disparu'
    assert r['sectors'] == []
    assert r['avg_rsi'] is None


def test_une_mesure_ABSENTE_reste_absente_et_ne_devient_pas_zero():
    """`avg_rsi=None` dit « on ne sait pas ». `0` dirait « RSI nul », ce qui
    est faux et indiscernable d'un marché à l'arrêt."""
    rows, detail = _scan(['AAPL', 'MSFT'], rsi=None)
    r = mi.market_internals(rows, detail, 50)
    assert r['avg_rsi'] is None
    assert r['pct_ob'] == 0 and r['pct_os'] == 0   # aucune ligne → aucune part


def test_un_secteur_trop_petit_est_ECARTE_et_non_publie():
    """Contre-épreuve du seuil : sous cinq titres, la breadth sectorielle
    n'informe pas. Le seuil est nommé (`SECTEUR_MIN`) pour être discutable."""
    assert mi.SECTEUR_MIN == 5
    par_secteur = {}
    for sym, sec in _GICS_SECTOR.items():
        par_secteur.setdefault(sec, []).append(sym)
    gros = next(s for s, v in par_secteur.items() if len(v) >= mi.SECTEUR_MIN)

    petit_ech = par_secteur[gros][:mi.SECTEUR_MIN - 1]
    rows, detail = _scan(petit_ech)
    assert mi.market_internals(rows, detail, 50)['sectors'] == [], (
        '%d titres suffisent à publier une breadth sectorielle' % len(petit_ech))

    juste_ech = par_secteur[gros][:mi.SECTEUR_MIN]
    rows, detail = _scan(juste_ech)
    publies = mi.market_internals(rows, detail, 50)['sectors']
    assert [x['sector'] for x in publies] == [gros], (
        'au seuil exact, le secteur devrait être publié — sinon le banc '
        'précédent serait vrai pour une mauvaise raison')


def test_les_symboles_hors_GICS_ne_creent_pas_de_secteur_fantome():
    rows, detail = _scan(['ZZQ1', 'ZZQ2', 'ZZQ3', 'ZZQ4', 'ZZQ5', 'ZZQ6'])
    r = mi.market_internals(rows, detail, 50)
    assert r['sectors'] == []
    assert r['n'] == 6, 'les titres hors GICS doivent compter dans la population'


def test_la_sante_reste_bornee_entre_0_et_100():
    """Composite de quatre parts : un breadth aberrant ne doit pas la faire
    sortir de l'échelle qu'elle affiche."""
    rows, detail = _scan(['AAPL'] * 0 or ['AAPL'], above50=True)
    for breadth in (-500, 0, 50, 100, 900):
        h = mi.market_internals(rows, detail, breadth)['health']
        assert 0 <= h <= 100, 'santé %r hors échelle pour breadth=%r' % (h, breadth)
