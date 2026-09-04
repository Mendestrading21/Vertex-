"""Vertex Test 1.0 — LES DEUX AUTRES MOTEURS TOURNAIENT AUSSI SUR LES CONSTANTES.

D-099 a sorti `scenario_pricer` des constantes. Recensement du 26 août 2026 :
**deux autres moteurs** portaient les mêmes, et **deux routes vivantes** les
appelaient sans jamais leur passer autre chose.

| moteur | constantes | route qui l'appelle | ce qu'elle sert |
|---|---|---|---|
| `engines/multileg_lab` | `R_DEFAULT=0.045`, `Q_DEFAULT=0.0` | `/api/options/strategies/<sym>`, `/api/options/analyze` | payoff, PoP, Greeks des **positions réelles du desk** |
| `options/double_prob` | `R_DEFAULT=0.045`, `Q_DEFAULT=0.0` | `/api/options/scanners` | **probabilité de doublement** des 5 meilleurs candidats |

## Ce que ça donnait, mesuré

Probabilité de **doublement** (call, la structure du produit) :

| candidat | constantes | mesuré | écart |
|---|---|---|---|
| KO 95 DTE 180 (q=2,26 %) | 28,33 % | 25,99 % | **−8,3 %** |
| MO 70 DTE 180 (q=6,19 %) | 24,89 % | 19,70 % | **−20,9 %** |
| AAPL 330 DTE 240 (q=0,34 %) | 22,49 % | 21,63 % | −3,8 % |
| KO 100 DTE 365 (q=2,26 %) | 26,15 % | 22,98 % | −12,1 % |

Multi-jambes, sur une jambe réelle (KO call 95, DTE 180) :

| sortie | constantes | mesuré |
|---|---|---|
| probabilité de profit | 35,2 % | 32,6 % |
| delta | 51,59 | 48,23 (−6,5 %) |
| theta | −2,63 | −2,23 (+15,4 %) |
| vomma | −0,58 | **+0,63** (changement de signe) |

L'écart va toujours dans le sens **optimiste** pour un call long — la structure
que Vertex recommande.

## Ce qui n'était PAS un mensonge

Ces deux moteurs **tracent déjà** `r` et `q` dans leur bloc `model`. Ils disent
donc la vérité sur ce qu'ils ont employé. Le défaut n'est pas une fausse
déclaration comme en D-097 : c'est que l'appelant ne leur a jamais rien donné
d'autre que la constante. Le dire évite de compter deux fois la même faute.

## Le chemin dégradé est IDENTIQUE

Le repli plat de la courbe vaut `0.045` — exactement `R_DEFAULT`. Sans scan,
ces moteurs reçoivent donc la valeur qu'ils prenaient déjà par défaut.
"""
from __future__ import annotations

import os

import pytest

from vertex.engines import multileg_lab as M
from vertex.options import double_prob as D
from vertex.options import entrees_mesurees as E

MACRO = [{'id': '^IRX', 'unit': '%', 'value': 3.71, 'date': '2026-08-25'},
         {'id': '^FVX', 'unit': '%', 'value': 4.35, 'date': '2026-08-25'},
         {'id': '^TNX', 'unit': '%', 'value': 4.64, 'date': '2026-08-25'},
         {'id': '^TYX', 'unit': '%', 'value': 5.17, 'date': '2026-08-25'}]
FOND = {'by_sym': {'KO': {'div': 0.0226, 'div_source': 'trailingAnnualDividendYield'},
                   'MO': {'div': 0.0619, 'div_source': 'trailingAnnualDividendYield'}}}
ETAT = {'macro': MACRO, 'fundamentals': FOND}


#  ═══════════  1. le repli reste EXACTEMENT la constante d'avant  ═════════════

def test_sans_scan_le_taux_vaut_EXACTEMENT_l_ancienne_constante():
    """La condition pour que ce lot ne soit pas une régression déguisée : un
    desk sans scan doit retrouver le chiffre au bit près."""
    assert E.taux({}, 180) == M.R_DEFAULT == D.R_DEFAULT == 0.045
    for jours in (1, 35, 180, 365, 730):
        assert E.taux({}, jours) == 0.045


def test_une_echeance_illisible_ne_fait_pas_tomber_le_taux():
    for mauvais in (None, 0, -5, 'n/d', float('nan')):
        assert 0.0 < E.taux({}, mauvais) < 0.2


#  ═══════════  2. chaque échéance reçoit SON taux  ════════════════════════════

def test_chaque_echeance_recoit_son_PROPRE_taux():
    """C'était tout l'objet de la couche §6.6, restée inerte jusqu'à D-098 :
    ces moteurs prennent un `r` scalaire, pas une courbe."""
    t35, t180, t365 = E.taux(ETAT, 35), E.taux(ETAT, 180), E.taux(ETAT, 365)
    assert t35 < t180 < t365, (t35, t180, t365)
    assert all(0.030 < t < 0.045 for t in (t35, t180, t365))


#  ═══════════  3. la probabilité de doublement  ═══════════════════════════════

@pytest.mark.parametrize('sym,spot,strike,prem,dte,iv,q', [
    ('KO', 91.64, 95.0, 4.20, 180, 0.30, 0.0226),
    ('MO', 68.07, 70.0, 4.00, 180, 0.28, 0.0619),
])
def test_la_probabilite_de_doublement_etait_SUREVALUEE(sym, spot, strike, prem, dte, iv, q):
    """Une probabilité servie à l'utilisateur sur la structure même du produit."""
    avant = D.double_probability(spot=spot, strike=strike, premium=prem, dte=dte,
                                 iv=iv, right='CALL')['probability']
    apres = D.double_probability(spot=spot, strike=strike, premium=prem, dte=dte,
                                 iv=iv, right='CALL',
                                 r=E.taux(ETAT, dte), q=q)['probability']
    assert apres < avant, '%s : %.4f -> %.4f' % (sym, avant, apres)


def test_l_ecart_CROIT_avec_le_rendement_du_titre():
    """Ce qui montre que la cause est bien le dividende ignoré, et pas un
    artefact : MO (6,19 %) doit être plus touché que KO (2,26 %)."""
    def ecart(q):
        a = D.double_probability(spot=100, strike=105, premium=5.0, dte=180,
                                 iv=0.30, right='CALL')['probability']
        b = D.double_probability(spot=100, strike=105, premium=5.0, dte=180,
                                 iv=0.30, right='CALL', r=E.taux(ETAT, 180), q=q)['probability']
        return (a - b) / a
    assert ecart(0.0619) > ecart(0.0226) > ecart(0.0034) > 0


def test_un_titre_SANS_dividende_bouge_peu():
    """Contre-épreuve : si l'écart existait aussi sans dividende, c'est que
    j'accuserais le mauvais coupable."""
    a = D.double_probability(spot=100, strike=105, premium=5.0, dte=180,
                             iv=0.30, right='CALL')['probability']
    b = D.double_probability(spot=100, strike=105, premium=5.0, dte=180,
                             iv=0.30, right='CALL', r=E.taux(ETAT, 180), q=0.0)['probability']
    assert abs(a - b) / a < 0.05


#  ═══════════  4. le moteur multi-jambes  ═════════════════════════════════════

def _jambe():
    return [{'type': 'call', 'strike': 95.0, 'qty': 1, 'premium': 4.20}]


def test_le_multijambes_TRACAIT_deja_ses_hypotheses():
    """Ce moteur ne mentait pas : il déclare `r` et `q`. Le défaut est que
    l'appelant ne lui passait que la constante — pas la même faute qu'en D-097,
    et le dire évite de la compter deux fois."""
    a = M.analyze_strategy(_jambe(), 91.64, 0.30, 180)
    assert a['model']['r'] == 0.045 and a['model']['q'] == 0.0


def test_le_multijambes_TRACE_les_entrees_mesurees_qu_on_lui_donne():
    b = M.analyze_strategy(_jambe(), 91.64, 0.30, 180,
                           r=E.taux(ETAT, 180), q=0.0226)
    assert b['model']['q'] == 0.0226
    assert 0.030 < b['model']['r'] < 0.045


def test_la_probabilite_de_profit_baisse_avec_les_entrees_mesurees():
    a = M.analyze_strategy(_jambe(), 91.64, 0.30, 180)['probability_of_profit']
    b = M.analyze_strategy(_jambe(), 91.64, 0.30, 180,
                           r=E.taux(ETAT, 180), q=0.0226)['probability_of_profit']
    assert b < a, '%s -> %s' % (a, b)


def test_les_STRATEGIES_par_symbole_transmettent_r_et_q():
    """`strategies_for_symbol` construit les jambes puis délègue : si elle ne
    transmet pas, la correction s'arrête à la porte du moteur."""
    import inspect
    sig = inspect.signature(M.strategies_for_symbol)
    assert 'r' in sig.parameters and 'q' in sig.parameters
    src = inspect.getsource(M.strategies_for_symbol)
    assert 'r=r' in src and 'q=q' in src


#  ═══════════  5. sur les VRAIES routes  ══════════════════════════════════════

@pytest.fixture()
def client(tmp_path, monkeypatch):
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    import terminal
    from vertex.app.state import scan_state
    return terminal.app.test_client(), scan_state


def _analyse(client, macro, fond, **extra):
    c, etat = client
    etat['macro'] = macro
    etat['fundamentals'] = fond
    charge = {'legs': [{'type': 'call', 'strike': 95.0, 'qty': 1, 'premium': 4.20}],
              'spot': 91.64, 'iv': 0.30, 'days': 180}
    charge.update(extra)
    r = c.post('/api/options/analyze', json=charge)
    assert r.status_code == 200
    return r.get_json()


def test_la_route_analyze_emploie_le_taux_MESURE(client):
    d = _analyse(client, MACRO, FOND, sym='KO')
    assert d['available'] is True
    assert 0.030 < d['model']['r'] < 0.045
    assert d['model']['q'] == 0.0226


def test_la_route_analyze_SANS_symbole_n_invente_pas_de_dividende(client):
    """Le dividende exige un titre. Sans lui, `q` reste 0,0 — et le bloc
    `model` le TRACE, donc la valeur est déclarée, pas dissimulée."""
    d = _analyse(client, MACRO, FOND)
    assert d['model']['q'] == 0.0
    assert 0.030 < d['model']['r'] < 0.045, 'le taux, lui, ne depend pas du titre'


def test_la_route_analyze_SANS_scan_est_identique_a_avant(client):
    d = _analyse(client, [], {}, sym='KO')
    assert d['model']['r'] == 0.045 and d['model']['q'] == 0.0


def test_la_route_analyze_porte_la_provenance(client):
    d = _analyse(client, MACRO, FOND, sym='KO')
    assert d['entrees']['dividende']['applique'] is True
    assert d['entrees']['taux']['repli'] is False


def test_un_symbole_INCONNU_ne_casse_pas_la_route(client):
    d = _analyse(client, MACRO, FOND, sym='ZZZZ')
    assert d['available'] is True and d['model']['q'] == 0.0


def test_la_charge_accepte_le_symbole_sans_rejeter_les_anciennes(client):
    """Compatibilité : le client actuel n'envoie pas `sym`, et il ne doit pas
    commencer à recevoir une erreur."""
    assert _analyse(client, MACRO, FOND)['available'] is True
    assert _analyse(client, MACRO, FOND, sym='KO')['available'] is True


#  ═══════════  6. un seul propriétaire, partout  ══════════════════════════════

def test_les_QUATRE_routes_de_pricing_passent_par_le_meme_proprietaire():
    """Quatre routes qui liraient l'état chacune de leur côté finiraient par
    servir quatre chiffres différents pour le même contrat."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    for chemin in ('vertex/app/routes/options_intel_api.py',
                   'vertex/app/routes/redesign.py',
                   'vertex/app/routes/options_lab_api.py'):
        src = (racine / chemin).read_text(encoding='utf-8')
        assert 'entrees_mesurees' in src, '%s construit ses entrees seul' % chemin


def test_aucun_moteur_de_pricing_ne_garde_une_constante_NON_surchargeable():
    """Une constante par défaut est acceptable — elle documente le repli. Une
    constante que l'appelant ne PEUT pas remplacer est un mur."""
    import inspect
    for fn in (M.analyze_strategy, M.strategies_for_symbol, D.double_probability):
        params = inspect.signature(fn).parameters
        assert 'r' in params and 'q' in params, fn.__name__
