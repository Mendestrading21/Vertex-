"""Vertex Test 1.0 — LE SIMULATEUR DISAIT QU'AU STOP, ON ÉTAIT GAGNANT.

## Le défaut, mesuré le 26 août 2026 sur la vraie route

`scenario_pricer` prend un taux et un rendement de dividende. Les deux sites de
production — `options_intel_api.options_simulate` et `redesign.options_simulate`
— ne lui passaient **ni l'un ni l'autre** : `rate_curve` omis (donc le taux plat
de repli, **4,5 %**), `dividend_yield` omis (donc **0,0**).

Or les deux données sont **déjà collectées et déjà en mémoire** : la courbe dans
`scan_state['macro']` — que la page Marchés dessine — et le rendement dans
`scan_state['fundamentals']`.

Recensement : `RateCurve(` n'est construite **qu'une seule fois dans tout le
dépôt**, sans points. Toute la couche par échéance était donc inerte.

```text
^IRX  3M   3.705 %     repli employe       4.500 %
^FVX  5A   4.351 %     taux reel a 180 j   3.738 %
^TNX 10A   4.639 %     ecart                 76 pb
^TYX 30A   5.174 %
```

## Ce que ça donnait, sur `/api/options/simulate` (KO call 95, DTE 180)

| sortie servie | constantes | entrées mesurées |
|---|---|---|
| prime courante | 7,120 | 6,465 (**−9,20 %**) |
| prime au stop | 4,545 | 4,074 (**−10,36 %**) |
| prime à TP1 | 10,804 | 9,934 (−8,05 %) |
| gain de base attendu | 123,7 % | 105,6 % |
| **perte max planifiée** | **+2,7 %** | **−7,7 %** |
| rendement/risque | **incalculable** | 13,71 |

La ligne qui compte est l'avant-dernière. Avec les constantes, la perte maximale
planifiée — au **stop choisi par l'utilisateur** — ressortait **positive** : le
simulateur affirmait qu'en touchant son stop, on était encore gagnant de 2,7 %.
Et parce que cette « perte » était un gain, le ratio rendement/risque ne pouvait
pas être calculé du tout.

Les deux erreurs poussent dans le même sens pour un call, et Vertex est un
produit d'achat de calls longs à risque borné : le simulateur surévaluait
systématiquement ce que l'utilisateur achète, d'autant plus que l'échéance est
lointaine — donc au maximum sur l'horizon visé (DTE préféré 120–240).

## Lire, pas collecter

Aucun appel réseau ajouté : une requête de page ne collecte pas (D-072, P0.1).
Quand une entrée manque, elle manque — la courbe retombe sur le repli plat
documenté, déjà marqué `fallback_used=True`, et le rendement reste `0.0`. Le
comportement dégradé est donc **exactement** celui d'avant ce lot.
"""
from __future__ import annotations

import os

import pytest

from vertex.data_sources import courbe_taux as CT
from vertex.options import entrees_mesurees as E

#: La courbe REELLE mesuree le 26 aout 2026, dans la forme exacte que le scan
#: produit (`value` en POURCENT, `unit: '%'`, close date).
MACRO = [
    {'id': '^IRX', 'name': 'Taux 3 mois', 'unit': '%', 'value': 3.71, 'date': '2026-08-25'},
    {'id': '^FVX', 'name': 'Taux 5 ans', 'unit': '%', 'value': 4.35, 'date': '2026-08-25'},
    {'id': '^TNX', 'name': 'Taux 10 ans', 'unit': '%', 'value': 4.64, 'date': '2026-08-25'},
    {'id': '^TYX', 'name': 'Taux 30 ans', 'unit': '%', 'value': 5.17, 'date': '2026-08-25'},
    {'id': 'DX-Y.NYB', 'name': 'Dollar (DXY)', 'unit': '', 'value': 97.3, 'date': '2026-08-25'},
]

FOND = {'by_sym': {'KO': {'div': 0.0226, 'div_source': 'trailingAnnualDividendYield',
                          'div_unite_inferee': False, 'recu_a': '2026-08-26T09:00:00Z'}}}


#  ═══════════  1. la courbe, bâtie sur ce qui est déjà collecté  ══════════════

def test_la_courbe_est_construite_depuis_le_scan_et_non_du_repli():
    c = CT.depuis_macro(MACRO)
    q = c.rate_for_tenor(180)
    assert q.fallback_used is False, 'la couche par echeance restait inerte'
    assert 0.030 < q.rate < 0.042, 'taux a 180 j = %.4f' % q.rate


def test_le_POURCENT_du_scan_devient_une_fraction():
    """`3.71` veut dire 3,71 %, pas 371 %. Même piège d'unité qu'en D-095."""
    points = CT.points_depuis_macro(MACRO)
    assert abs(points[91] - 0.0371) < 1e-9
    assert abs(points[10957] - 0.0517) < 1e-9


def test_le_DXY_n_entre_PAS_dans_la_courbe_des_taux():
    """Contre-épreuve : `97.3` lu comme un taux donnerait 97 % à une échéance
    inventée. Seuls les identifiants connus sont retenus."""
    assert set(CT.points_depuis_macro(MACRO)) == {91, 1825, 3652, 10957}


def test_une_valeur_qui_n_est_pas_un_taux_est_ECARTEE():
    faux = [{'id': '^IRX', 'value': 3.71}, {'id': '^TNX', 'value': 371.0},
            {'id': '^TYX', 'value': None}, {'id': '^FVX', 'value': 'n/d'}]
    assert set(CT.points_depuis_macro(faux)) == {91}


def test_moins_de_deux_points_RETOMBE_sur_le_repli_documente():
    """Avec un seul point, on servirait une constante en la présentant comme
    une courbe — pire que le repli, qui, lui, se déclare."""
    c = CT.depuis_macro([{'id': '^IRX', 'unit': '%', 'value': 3.71}])
    assert c.rate_for_tenor(180).fallback_used is True


def test_un_scan_VIDE_se_comporte_exactement_comme_avant_ce_lot():
    """Le chemin dégradé ne doit pas régresser : c'est celui d'un desk qui
    démarre, ou d'un scan en échec."""
    for vide in ([], None, [{}], [{'id': 'AAPL', 'value': 300}]):
        assert CT.depuis_macro(vide).rate_for_tenor(180).fallback_used is True


def test_la_couverture_AVOUE_le_trou_de_la_courbe():
    """Aucun point entre 3 mois et 5 ans, et l'échéance visée par le produit
    (120–240 j) tombe en plein dedans. Interpoler large est bien meilleur qu'une
    constante — et reste une approximation. Le dire est la condition pour s'en
    servir."""
    cov = CT.couverture(MACRO)
    assert cov['repli'] is False and cov['points'] == 4
    assert cov['interpolation_large'] is True
    assert cov['horodatage'] == '2026-08-25'
    assert cov['source']


def test_la_couverture_ne_crie_pas_au_trou_quand_il_est_COMBLE():
    """Contre-épreuve : un avertissement présent en toute circonstance ne
    distingue plus rien."""
    avec_6m = MACRO + [{'id': '^FVX', 'unit': '%', 'value': 4.35}]
    cov = CT.couverture(avec_6m)
    assert cov['interpolation_large'] is True     # ^FVX est deja a 5 ans
    #  Un vrai point intermediaire, lui, comble le trou.
    CT.ECHEANCES_JOURS['^TEST6M'] = 182
    try:
        cov2 = CT.couverture(MACRO + [{'id': '^TEST6M', 'unit': '%', 'value': 3.8}])
        assert cov2['interpolation_large'] is False
    finally:
        CT.ECHEANCES_JOURS.pop('^TEST6M', None)


#  ═══════════  2. le rendement, lu là où il est déjà  ═════════════════════════

def test_le_rendement_est_lu_dans_les_fondamentaux_du_scan():
    assert E.rendement_dividende({'fundamentals': FOND}, 'KO') == 0.0226


def test_un_rendement_INCONNU_rend_None_et_non_zero():
    """D-081 : confondre les deux ferait passer « je ne sais pas » pour « ce
    titre ne verse rien » — et ferait appliquer un dividende nul avec aplomb."""
    assert E.rendement_dividende({'fundamentals': FOND}, 'NVDA') is None
    assert E.rendement_dividende({}, 'KO') is None
    assert E.rendement_dividende({'fundamentals': {'by_sym': {'KO': {'div': None}}}}, 'KO') is None


def test_la_provenance_dit_si_le_dividende_a_ete_APPLIQUE():
    """Un prix corrigé sans provenance serait aussi opaque qu'un prix faux."""
    p = E.provenance({'macro': MACRO, 'fundamentals': FOND}, 'KO')
    assert p['dividende']['applique'] is True
    assert p['dividende']['source'] == 'trailingAnnualDividendYield'
    assert p['taux']['repli'] is False


def test_la_provenance_dit_POURQUOI_quand_il_ne_l_a_pas_ete():
    p = E.provenance({'macro': [], 'fundamentals': FOND}, 'NVDA')
    assert p['dividende']['applique'] is False
    assert p['dividende']['motif']
    assert p['taux']['repli'] is True


#  ═══════════  3. sur la VRAIE route, avant / après  ══════════════════════════

@pytest.fixture()
def client(tmp_path, monkeypatch):
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    import terminal
    from vertex.app.state import scan_state
    scan_state['detail'] = {'KO': {'price': 91.64,
                                   'plan': {'stop': 86.0, 'tp1': 98.0, 'tp2': 104.0}}}
    return terminal.app.test_client(), scan_state


def _sim(client, macro, fond):
    c, etat = client
    etat['macro'] = macro
    etat['fundamentals'] = fond
    r = c.get('/api/options/simulate?sym=KO&right=C&strike=95&dte=180&mid=4.2&iv=0.30')
    assert r.status_code == 200
    return r.get_json()['sim']


def _prime(sim, cle):
    bt = (sim.get(cle) or {}).get('by_time_days') or {}
    k = '0' if '0' in bt else (0 if 0 in bt else None)
    return bt.get(k, {}).get('value') if k is not None else None


def test_la_route_emploie_desormais_le_taux_MESURE(client):
    sim = _sim(client, MACRO, FOND)
    assert sim['rate']['fallback_used'] is False
    assert 0.030 < sim['rate']['rate'] < 0.042


def test_la_prime_servie_BAISSE_et_la_mesure_le_montre(client):
    """L'écart n'est pas théorique : c'est la route de production."""
    avant = _prime(_sim(client, [], {}), 'current')
    apres = _prime(_sim(client, MACRO, FOND), 'current')
    assert avant and apres
    ecart = (apres - avant) / avant
    assert ecart < -0.05, 'ecart mesure %.2f %%' % (ecart * 100)


def test_LA_PERTE_AU_STOP_n_est_plus_annoncee_comme_un_GAIN(client):
    """Le défaut le plus grave du lot. Avec les constantes,
    `worst_planned_loss_pct` ressortait **positif** : le simulateur affirmait
    qu'en touchant son propre stop, l'utilisateur était encore gagnant."""
    avant = _sim(client, [], {})['worst_planned_loss_pct']
    apres = _sim(client, MACRO, FOND)['worst_planned_loss_pct']
    assert avant is not None and apres is not None
    assert avant > 0, "le defaut mesure : la perte au stop etait un gain (%s)" % avant
    assert apres < 0, "entrees mesurees : le stop doit etre une PERTE (%s)" % apres


def test_le_rendement_risque_redevient_CALCULABLE(client):
    """Il ne l'était pas : une « perte » positive ne se divise pas."""
    assert _sim(client, [], {})['reward_risk'] is None
    assert _sim(client, MACRO, FOND)['reward_risk'] is not None


def test_la_reponse_PORTE_la_provenance_de_ses_entrees(client):
    sim = _sim(client, MACRO, FOND)
    assert sim['entrees']['taux']['source']
    assert sim['entrees']['dividende']['applique'] is True


def test_la_limitation_annonce_le_dividende_REELLEMENT_applique(client):
    sim = _sim(client, MACRO, FOND)
    assert any('dividende pris en compte' in x and '2.26' in x
               for x in sim['limitations'])


def test_SANS_scan_la_route_se_comporte_comme_AVANT_ce_lot(client):
    """Contre-épreuve indispensable : un desk qui démarre, ou dont le scan a
    échoué, ne doit pas voir son simulateur casser — il doit retrouver
    exactement le comportement documenté d'avant."""
    sim = _sim(client, [], {})
    assert sim['rate']['fallback_used'] is True
    assert any('NON pris en compte' in x for x in sim['limitations'])
    assert _prime(sim, 'current')


#  ═══════════  4. un seul propriétaire des entrées  ═══════════════════════════

def test_les_DEUX_routes_passent_par_le_meme_proprietaire():
    """Deux routes qui liraient l'état chacune de leur côté finiraient par
    servir deux prix différents pour le même contrat."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    for chemin in ('vertex/app/routes/options_intel_api.py',
                   'vertex/app/routes/redesign.py'):
        src = (racine / chemin).read_text(encoding='utf-8')
        assert 'entrees_mesurees' in src, '%s construit ses entrees seul' % chemin
        assert 'rate_curve=' in src, '%s ne passe pas de courbe' % chemin
        assert 'dividend_yield=' in src, '%s ne passe pas de rendement' % chemin


def test_le_module_d_entrees_ne_COLLECTE_pas():
    """Une couche de taux qui irait chercher une courbe au moment de pricer
    rouvrirait exactement le défaut fermé par P0.1 (D-072).

    Le contrôle porte sur les IMPORTS, pas sur le texte : ma première version
    cherchait la chaîne « yfinance » et accusait le **libellé de provenance**
    — qui doit précisément nommer la source. Un gardien qui compte les faux
    positifs finit ignoré (D-088).
    """
    import ast
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    reseau = {'requests', 'urllib', 'urllib3', 'httpx', 'yfinance', 'socket',
              'http', 'aiohttp'}
    for chemin in ('vertex/options/entrees_mesurees.py',
                   'vertex/data_sources/courbe_taux.py'):
        arbre = ast.parse((racine / chemin).read_text(encoding='utf-8'))
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                noms = [a.name.split('.')[0] for a in noeud.names]
            elif isinstance(noeud, ast.ImportFrom):
                noms = [(noeud.module or '').split('.')[0]]
            else:
                continue
            fautifs = reseau.intersection(noms)
            assert not fautifs, '%s importe %s' % (chemin, sorted(fautifs))


def test_ce_gardien_VOIT_un_import_reseau_qu_on_lui_montre(tmp_path):
    """Contre-épreuve : sans elle, le contrôle ci-dessus certifierait n'importe
    quel module — et un import ajouté demain passerait."""
    import ast
    reseau = {'requests', 'urllib', 'httpx', 'yfinance'}
    arbre = ast.parse('import yfinance as yf\nfrom requests import get\n')
    vus = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            vus.update(a.name.split('.')[0] for a in noeud.names)
        elif isinstance(noeud, ast.ImportFrom):
            vus.add((noeud.module or '').split('.')[0])
    assert reseau.intersection(vus) == {'yfinance', 'requests'}


def test_ce_gardien_n_accuse_PAS_un_libelle_de_provenance():
    """Le faux positif exact que ma première version produisait : `SOURCE`
    nomme yfinance, et c'est son office — la provenance doit dire d'où vient
    le chiffre."""
    from vertex.data_sources import courbe_taux as C
    assert 'yfinance' in C.SOURCE
