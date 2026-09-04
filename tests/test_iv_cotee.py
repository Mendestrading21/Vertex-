"""Vertex Test 1.0 — L'IV DU PROXY ÉTAIT FAUSSE DANS 30 CAS SUR 30.

Le lot précédent (D-104…D-106) a fait **déclarer** au constructeur de stratégie
que ses primes étaient modélisées, et a laissé une limite ouverte : « je n'ai
pas comparé la prime modélisée à une prime cotée ». Ce lot lève cette limite,
et corrige ce qu'elle cachait.

## La mesure, faite le 26 août 2026

Historique réel via yfinance, **ATR de Wilder — la formule exacte de
`vertex/engines/indicators.py`**, celle que le produit emploie. Une première
tentative avec une moyenne `(haut − bas)` simplifiée sous-estimait l'écart : le
True Range étant supérieur ou égal, l'ATR réel est plus grand, donc le proxy
encore plus haut.

Comparaison à l'IV **réellement cotée** des 578 contrats du board du 25 août :

```text
titres mesures       : 30
IV proxy SUPERIEURE  : 30 / 30   (100 %)
ecart  mediane +40,0 %   p10 +20,2 %   p90 +64,4 %   max +77,9 %
```

**Trente sur trente.** Ce n'est pas du bruit : c'est un biais, dans une seule
direction. La cause est structurelle — `_iv_proxy` transforme l'ATR, qui mesure
la volatilité **réalisée**, en une IV, qui est de la volatilité **implicite**.
Ce ne sont pas la même grandeur.

## Ce que ça faisait à la page Stratégie

Prime d'un call ATM à 180 jours, sur les mêmes 30 titres :

```text
surcout  mediane +34,9 %   p10 +17,3 %   p90 +53,6 %   max +66,3 %
titres surevalues : 30 / 30
```

Et cette prime porte le **dimensionnement en dollars** : sur un budget de 15 k,
la médiane est de **2 contrats de moins** que ce que la cotation réelle
permettrait. Bout en bout sur AAPL : IV 37 → 27, prime 35,14 → 26,79, et
**5 contrats au lieu de 4**.

## La correction : lire ce qui est déjà coté

Le board porte l'IV **réellement cotée** de chaque titre — la même donnée que le
produit affiche et score déjà. La stratégie la lit désormais, et ne retombe sur
le proxy que si le titre n'a aucun contrat.

`n_contrats` accompagne la valeur : une médiane sur un contrat n'est pas une
surface de volatilité, et le lecteur doit pouvoir en juger. Mais exiger trois
contrats ne couvrirait que **145 des 211 titres** du board, et les 66 autres
retomberaient sur un proxy mesurablement faux de 40 %. **Préférer une erreur
connue à une cotation réelle serait un choix, et le mauvais.**
"""
from __future__ import annotations

import json
import pathlib

import pytest

from vertex.options import entrees_mesurees as E
from vertex.strategy import legacy_adapter as A

RACINE = pathlib.Path(__file__).resolve().parents[1]

#: Contrats de la MEME forme que le board de production (`iv` en POURCENT).
BOARD = [
    {'sym': 'AAPL', 'type': 'CALL', 'dte': 51, 'strike': 310.0, 'iv': 27.2, 'mid': 20.0},
    {'sym': 'AAPL', 'type': 'CALL', 'dte': 86, 'strike': 320.0, 'iv': 27.1, 'mid': 22.0},
    {'sym': 'AAPL', 'type': 'PUT', 'dte': 51, 'strike': 300.0, 'iv': 28.0, 'mid': 12.0},
    {'sym': 'KO', 'type': 'CALL', 'dte': 51, 'strike': 95.0, 'iv': 19.5, 'mid': 2.4},
    {'sym': 'SEUL', 'type': 'CALL', 'dte': 51, 'strike': 50.0, 'iv': 33.0, 'mid': 3.0},
]

DETAIL = {'AAPL': {'price': 309.90, 'atr_pct': 2.33, 'verdict': 'ACHETER',
                   'grade': 'A', 'score': 82,
                   'plan': {'stop': 290.0, 'tp1': 330.0, 'tp2': 350.0}}}
ROWS = [{'symbol': 'AAPL', 'score': 82}]


def _build(board):
    return A.build(ROWS, DETAIL, market={'regime': 'risk-on'}, top_n=1, board=board)


#  ═══════════  1. l'IV cotée est lue, et son unité est traitée  ═══════════════

def test_l_IV_du_board_est_en_POURCENT_et_devient_decimale():
    """`27.2` veut dire 27,2 %, pas 2 720 %. Même piège qu'en D-095 — et la
    même réponse : la conversion est faite une fois, par le propriétaire."""
    q = E.iv_cotee(BOARD, 'AAPL')
    assert 0.20 < q['valeur'] < 0.35, q


def test_la_MEDIANE_protege_d_une_cotation_aberrante():
    """Une seule ligne peut porter une cotation folle ; la médiane non."""
    pollue = BOARD + [{'sym': 'AAPL', 'iv': 280.0}, {'sym': 'AAPL', 'iv': 1.0}]
    assert 0.20 < E.iv_cotee(pollue, 'AAPL')['valeur'] < 0.35


def test_une_IV_IMPLAUSIBLE_est_ecartee_et_non_convertie():
    """Convertir au hasard produirait un chiffre plausible et faux."""
    assert E.iv_cotee([{'sym': 'X', 'iv': 900.0}], 'X')['valeur'] is None
    assert E.iv_cotee([{'sym': 'X', 'iv': 0.5}], 'X')['valeur'] is None


def test_la_BASE_de_la_valeur_est_declaree():
    """Une médiane sur un contrat n'est pas une surface de volatilité. On
    l'emploie quand même — un proxy faux de 40 % est pire — mais le lecteur
    doit pouvoir en juger."""
    assert E.iv_cotee(BOARD, 'AAPL')['n_contrats'] == 3
    assert E.iv_cotee(BOARD, 'SEUL')['n_contrats'] == 1
    assert E.iv_cotee(BOARD, 'SEUL')['source']


def test_un_titre_ABSENT_du_board_rend_None():
    assert E.iv_cotee(BOARD, 'ZZZZ')['valeur'] is None
    assert E.iv_cotee([], 'AAPL')['valeur'] is None
    assert E.iv_cotee(None, 'AAPL')['valeur'] is None


def test_les_entrees_illisibles_ne_font_pas_tomber_le_lecteur():
    for sale in ([{'sym': 'X', 'iv': None}], [{'sym': 'X', 'iv': 'n/d'}],
                 [{'sym': 'X', 'iv': True}], [None], ['pas un dict']):
        assert E.iv_cotee(sale, 'X')['valeur'] is None


#  ═══════════  2. la stratégie préfère la cotation  ═══════════════════════════

def test_la_strategie_emploie_l_IV_COTEE_quand_elle_existe():
    p = _build(BOARD)['picks'][0]
    assert p['iv_source'] == 'COTEE'
    assert p['iv_estimated'] is False
    assert p['iv_n_contrats'] == 3


def test_elle_retombe_sur_le_PROXY_et_le_DIT_quand_rien_n_est_cote():
    """Le repli doit rester possible — un titre hors board existe — mais il ne
    doit jamais se confondre avec une cotation."""
    p = _build([])['picks'][0]
    assert p['iv_source'] == 'PROXY_ATR'
    assert p['iv_estimated'] is True
    assert p['iv_n_contrats'] == 0


def test_SANS_board_le_comportement_est_celui_d_AVANT_ce_lot():
    """Contre-épreuve : l'ancien appel, sans argument, ne doit pas casser."""
    ancien = A.build(ROWS, DETAIL, market={'regime': 'risk-on'}, top_n=1)
    assert ancien['picks'][0]['iv_source'] == 'PROXY_ATR'
    assert ancien['picks'][0]['iv'] == _build([])['picks'][0]['iv']


#  ═══════════  3. l'effet mesuré, sur la sortie servie  ═══════════════════════

def test_la_prime_BAISSE_quand_on_lit_la_cotation():
    """Le proxy surévaluait l'IV dans 30 cas sur 30 ; la prime suit."""
    def prime6m(board):
        p = _build(board)['picks'][0]
        return next(j for j in p['call'] if j['key'] == 'm6')['premium']
    avant, apres = prime6m([]), prime6m(BOARD)
    assert apres < avant, '%s -> %s' % (avant, apres)
    assert (avant - apres) / avant > 0.10


def test_le_DIMENSIONNEMENT_recupere_des_contrats():
    """Ce que la surévaluation coûtait concrètement : sur 15 k, la médiane
    mesurée était de 2 contrats de moins que ce que la cotation permet."""
    def contrats(board):
        p = _build(board)['picks'][0]
        j = next(x for x in p['call'] if x['key'] == 'm6')
        return next(s for s in j['sizes'] if s['budget'] == 15000)['contracts']
    assert contrats(BOARD) > contrats([])


def test_le_PORTEFEUILLE_lit_aussi_la_cotation():
    """C'est lui qui engage 50 k à 200 k : s'il restait sur le proxy, la
    correction manquerait là où elle compte le plus."""
    pf = A.build_portfolio(ROWS, DETAIL, market={'regime': 'risk-on'},
                           capital=100000, board=BOARD)
    lignes = pf.get('positions') or []
    sources = [l.get('iv_source') for l in lignes]
    assert sources and all(s == 'COTEE' for s in sources), sources
    #  Chaque ligne porte un cout et un `maxloss` en dollars : elle doit dire
    #  d'ou vient la prime qui les produit.
    assert all(l.get('cost') and l.get('maxloss') for l in lignes)


#  ═══════════  4. plus aucun appel nu au proxy  ═══════════════════════════════

def test_AUCUN_chemin_n_appelle_le_proxy_sans_passer_par_l_arbitre():
    """`_iv_du_titre` est le seul endroit qui tranche entre cotation et proxy.
    Un troisième chemin qui appellerait `_iv_proxy` directement rouvrirait le
    défaut sur une surface, en silence."""
    src = (RACINE / 'vertex' / 'strategy' / 'legacy_adapter.py').read_text(encoding='utf-8')
    #  Une seule occurrence hors de sa definition : celle de l'arbitre.
    hors_def = [l for l in src.splitlines()
                if '_iv_proxy(' in l and not l.startswith('def _iv_proxy')]
    assert len(hors_def) == 1, hors_def
    assert 'return _iv_proxy(atr_pct)' in hors_def[0]


def test_les_DEUX_appelants_de_production_passent_le_board():
    """Sans le board, la correction ne quitte pas le banc."""
    for chemin, appel in (('terminal.py', 'strategy.build('),
                          ('vertex/app/routes/command.py', 'build_portfolio(')):
        src = (RACINE / chemin).read_text(encoding='utf-8')
        i = src.index(appel)
        assert 'board=' in src[i:i + 400], '%s ne passe pas le board' % chemin


#  ═══════════  5. la limitation dit la mesure, pas une vague réserve  ═════════

def test_la_limitation_porte_le_CHIFFRE_mesure():
    """« Le modèle a des limites » n'informe personne. « 30 sur 30, médiane
    +40 % » se vérifie et se discute."""
    lims = ' '.join(_build(BOARD)['limitations'])
    assert '30' in lims and '40' in lims
    assert 'REALISEE' in lims and 'IMPLICITE' in lims


def test_la_limitation_avoue_la_structure_par_terme_NON_modelisee():
    """Une seule IV par titre sert tous les horizons, de 1 à 12 mois. C'est une
    approximation réelle, et elle survit à ce lot."""
    lims = ' '.join(_build(BOARD)['limitations']).lower()
    assert 'structure par terme' in lims


def test_le_modele_nomme_la_REGLE_et_le_pick_nomme_le_FAIT():
    """Le bloc global dit ce qui est possible ; chaque pick dit ce qui lui est
    réellement arrivé. Confondre les deux redonnerait un texte écrit d'avance."""
    b = _build(BOARD)
    assert 'COTEE' in b['model']['iv_source'] and 'PROXY' in b['model']['iv_source']
    assert b['picks'][0]['iv_source'] in ('COTEE', 'PROXY_ATR')
