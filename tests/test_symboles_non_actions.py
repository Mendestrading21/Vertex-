"""Vertex Test 1.0 — NE PAS DEMANDER AU COURTIER CE QU'IL NE PEUT PAS CONNAÎTRE.

## Le défaut, et il est de moi

`fetch_universe_bars` reçoit la liste des tickers du scan. Le scan télécharge
l'historique des **indices, matières premières et macro par le même chemin que
les actions** — ils portent donc des conventions *yfinance* :

| symbole | ce que c'est | chez IBKR |
|---|---|---|
| `^TNX`, `^VIX` | indice | jamais une action US |
| `GC=F`, `SI=F` | future | jamais une action US |
| `BTC-USD` | paire crypto | jamais une action US |
| `DX-Y.NYB` | indice + suffixe de place | jamais une action US |

`_contrat` — écrit au lot 1, par moi — tentait **trois** qualifications
d'action pour chacun (SMART, puis `primaryExchange` NYSE, puis NASDAQ). Relevé
dans le journal du courtier le 25 août 2026 :

```text
Error 200 ... Stock(symbol='^TNX', exchange='SMART', currency='USD')
Error 200 ... Stock(symbol='^TNX', exchange='SMART', primaryExchange='NYSE', ...)
Error 200 ... Stock(symbol='^TNX', exchange='SMART', primaryExchange='NASDAQ', ...)
```

Trois allers-retours perdus par symbole et **par scan**, dans la file partagée
avec les requêtes interactives — plus trois erreurs 200 qui noient les vraies.

## Ce qui a été vérifié AVANT d'écrire le filtre

Sur les **517** symboles de l'univers : **zéro** ne commence par `^`, ne finit
par `=F` ou `-USD`, ne contient de point. Les deux seuls à porter un tiret sont
`BRK-B` et `BF-B` — des actions de classe B que `_forme_ibkr` traite déjà. Le
filtre n'écarte donc **aucun titre réel**, et c'est mesuré, pas espéré.

## Ce que le filtre ne dit pas

Répondre `False` n'affirme pas que l'instrument n'existe pas — seulement qu'il
ne peut pas être qualifié comme action US, donc qu'il est inutile de le
demander. Il part au repli, qui connaît ces conventions.
"""
from __future__ import annotations

import re

import pytest

from vertex.data.universe import UNIVERSE
from vertex.data_sources.ibkr_historical import est_action_us, fetch_universe_bars


#  ═══════════  1. les formes qui ne peuvent pas être une action US  ═══════════

@pytest.mark.parametrize('symbole', ['^TNX', '^TYX', '^VIX', '^IRX', '^GSPC'])
def test_un_INDICE_yfinance_n_est_pas_demande(symbole):
    assert est_action_us(symbole) is False


@pytest.mark.parametrize('symbole', ['GC=F', 'SI=F', 'CL=F', 'BZ=F'])
def test_un_FUTURE_n_est_pas_demande(symbole):
    assert est_action_us(symbole) is False


def test_une_PAIRE_CRYPTO_n_est_pas_demandee():
    assert est_action_us('BTC-USD') is False


def test_un_symbole_a_SUFFIXE_DE_PLACE_n_est_pas_demande():
    """`DX-Y.NYB` : le point porte la place, pas le titre."""
    assert est_action_us('DX-Y.NYB') is False


def test_un_symbole_VIDE_n_est_pas_demande():
    assert est_action_us('') is False
    assert est_action_us(None) is False


#  ═══════════  2. LA contre-épreuve : aucun titre réel écarté  ════════════════

@pytest.mark.parametrize('symbole', ['AAPL', 'MSFT', 'BRK-B', 'BF-B', 'nvda'])
def test_une_VRAIE_action_reste_demandee(symbole):
    """Un filtre qui écarterait un titre réel serait pire que le gaspillage
    qu'il corrige : le titre disparaîtrait du scan IBKR sans rien dire."""
    assert est_action_us(symbole) is True


def test_AUCUN_symbole_de_l_univers_n_est_ecarte():
    """La vérification faite avant d'écrire le filtre, tenue par un banc : sur
    les 517 symboles, aucun ne doit tomber. Si l'univers gagne un jour un
    symbole en `^` ou en `=F`, ce banc le dira avant que le filtre ne le mange
    en silence."""
    ecartes = [s for s in UNIVERSE if not est_action_us(s)]
    assert ecartes == [], (
        "ces titres de l'univers seraient ecartes de la collecte IBKR : %s"
        % ecartes)


def test_les_deux_titres_a_TIRET_de_l_univers_sont_bien_des_actions():
    """`BRK-B` et `BF-B` sont la raison pour laquelle le filtre ne peut pas se
    contenter de rejeter tout tiret."""
    tirets = sorted(s for s in UNIVERSE if '-' in s)
    assert tirets == ['BF-B', 'BRK-B'], tirets
    assert all(est_action_us(s) for s in tirets)


#  ═══════════  3. écartés = NOMMÉS, jamais retirés en silence  ════════════════

def test_les_ecartes_sont_RAPPORTES_et_non_confondus_avec_des_refus():
    """Les compter parmi les `inconnus` ferait croire qu'IBKR les a refusés,
    alors qu'on ne les lui a jamais demandés — deux causes, deux gestes."""
    frames, rapport = fetch_universe_bars(['^TNX', 'GC=F', 'DX-Y.NYB'])
    assert frames == {}
    assert sorted(rapport['non_actions']) == ['DX-Y.NYB', 'GC=F', '^TNX']
    assert rapport['inconnus'] == []
    assert rapport['vides'] == []


def test_une_liste_ENTIEREMENT_filtree_ne_touche_pas_le_courtier(monkeypatch):
    """Sans ce court-circuit, on ouvrirait une session TWS pour ne rien
    demander — le coût que le lot supprime, repayé à l'entrée."""
    import vertex.data_sources.ibkr_historical as H
    appels = []
    monkeypatch.setattr(H, 'passerelle',
                        lambda *a, **k: appels.append(1) or None, raising=False)
    frames, rapport = fetch_universe_bars(['^VIX', 'BTC-USD'])
    assert frames == {} and appels == []
    assert len(rapport['non_actions']) == 2


def test_une_liste_VIDE_rapporte_la_meme_forme():
    """Un rapport dont les clés changent selon le cas force l'appelant à
    tester leur présence — et il finira par ne plus les lire."""
    _, rapport = fetch_universe_bars([])
    assert set(rapport) >= {'servis', 'inconnus', 'vides', 'non_actions'}


#  ═══════════  4. le motif reste ÉTROIT  ══════════════════════════════════════

def test_le_filtre_ne_rejette_pas_un_ticker_ordinaire_a_cinq_lettres():
    """Contre-épreuve de largeur : un motif trop gourmand aurait mangé des
    tickers longs ou inhabituels."""
    for s in ['GOOGL', 'ABNB', 'ZM', 'A', 'AA', 'PANW', 'ZZZZ']:
        assert est_action_us(s) is True


def test_le_motif_est_ecrit_UNE_fois_et_documente():
    """Un filtre dont la raison n'est pas écrite là où il vit se fera élargir
    par le prochain lot pressé."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex'
           / 'data_sources' / 'ibkr_historical.py').read_text(encoding='utf-8')
    assert '_NON_ACTIONS' in src
    assert re.search(r'BRK-B', src), (
        "la raison pour laquelle le tiret n'est PAS un critere doit rester "
        "ecrite a cote du filtre")
