"""Vertex Test 1.0 — QUATRE CINQUIÈMES DES DEMANDES AU COURTIER ÉTAIENT JETÉES.

## Le défaut, mesuré le 25 août 2026 sur le compte réel

`reqSecDefOptParams` rend les strikes **toutes échéances confondues**. Le
produit en fait l'union (`terminal.meta`), puis applique cette liste à
**chaque** échéance — alors que le pas d'IBKR change avec l'échéance : 1 $ sur
les hebdomadaires proches, 5 $ ou 10 $ au-delà.

Relevé dans le journal du serveur, échantillon de 250 lignes :

| titre | échéance | refus | strikes refusés |
|---|---|---:|---|
| MRNA | 2026-10-16 | 12 | 136, 137, 138, 139, 141, 142, 143, 144, 146, 147… |
| MRNA | 2026-11-20 | 12 | *les mêmes* |
| MRNA | 2027-03-19 | 12 | *les mêmes* |
| ORCL | 2026-11-20 | 11 | 138, 139, 141…147, 148, 149 |
| NRG  | 2026-12-18 | 11 | 104, 106…109, 111…114, 116 |

**Tout sauf les multiples de 5**, et les mêmes strikes redemandés à chaque
échéance, à chaque cycle. **214 refus sur 250 lignes.** La rotation demande 14
strikes par échéance : il en revient trois ou quatre.

Cette file est la même que celle des requêtes interactives — d'où les fiches
mesurées à 30–46 s le même jour, pour un contenu que yfinance rend en 1,3 s.

## Ce que ce banc garde

Que la mémoire filtre, sans jamais **inventer** un strike ni **aveugler** le
produit. Les deux contre-épreuves comptent plus que la mesure : une mémoire qui
viderait la chaîne en silence serait pire que le gaspillage qu'elle corrige.
"""
from __future__ import annotations

import time

import pytest

from vertex.options import strike_memory as M


@pytest.fixture(autouse=True)
def _memoire_neuve():
    M.oublier_tout()
    yield
    M.oublier_tout()


#  ═══════════  1. ce que le courtier a refusé n'est plus redemandé  ═══════════

def test_un_strike_REFUSE_n_est_plus_demande():
    """Le cas MRNA : douze strikes refusés, redemandés à chaque cycle."""
    M.noter_refus('MRNA', '20261016', [136, 137, 138, 139, 141, 142])
    demandes = M.filtrer('MRNA', '20261016', [136, 137, 138, 139, 140, 141, 142, 145])
    assert demandes == [140, 145]


def test_la_memoire_est_par_ECHEANCE_pas_par_titre():
    """Un strike valide en octobre ne l'est pas forcément en mars : c'est
    précisément l'erreur que le produit faisait en unifiant les deux."""
    M.noter_refus('MRNA', '20270319', [137])
    assert 137 in M.filtrer('MRNA', '20261016', [137, 140])
    assert 137 not in M.filtrer('MRNA', '20270319', [137, 140])


def test_les_deux_orthographes_d_echeance_designent_la_MEME():
    """`2027-03-19` et `20270319` circulent toutes deux dans le produit. Les
    traiter comme deux clés ferait retenir un refus qu'on ne relirait jamais —
    une mémoire qui n'oublie pas mais ne se souvient pas non plus."""
    M.noter_refus('ORCL', '2027-03-19', [138])
    assert M.filtrer('ORCL', '20270319', [138, 140]) == [140]


#  ═══════════  2. elle n'INVENTE jamais un strike  ════════════════════════════

def test_la_memoire_ne_rend_QUE_ce_qu_on_lui_a_propose():
    """Déduire « le pas est de 5, donc 155 existe » fabriquerait un contrat que
    personne n'a listé — l'invention que le produit s'interdit."""
    M.noter_refus('NRG', '20261218', [104, 106])
    rendus = M.filtrer('NRG', '20261218', [105, 110])
    assert set(rendus) <= {105, 110}


def test_sans_aucune_connaissance_le_comportement_est_INCHANGE():
    """Premier passage : aucune régression possible."""
    propose = [100, 105, 110]
    assert M.filtrer('ZZZ', '20261016', propose) == propose


def test_une_liste_vide_reste_vide():
    assert M.filtrer('ZZZ', '20261016', []) == []


#  ═══════════  3. elle n'AVEUGLE jamais le produit  ═══════════════════════════

def test_si_TOUT_est_connu_refuse_on_redemande_quand_meme():
    """LA contre-épreuve. Une mémoire prise pendant une coupure du courtier —
    où tout échoue — viderait sinon la chaîne pendant six heures, en silence.
    Un board vide sans raison est pire que le gaspillage corrigé."""
    M.noter_refus('AAPL', '20261016', [300, 305, 310])
    assert M.filtrer('AAPL', '20261016', [300, 305, 310]) == [300, 305, 310]


def test_un_strike_qui_QUALIFIE_efface_le_refus_anterieur():
    """Un refus contredit par les faits est faux, et cesse immédiatement."""
    M.noter_refus('AAPL', '20261016', [305])
    assert M.filtrer('AAPL', '20261016', [300, 305]) == [300]
    M.noter_acceptes('AAPL', '20261016', [305])
    assert M.filtrer('AAPL', '20261016', [300, 305]) == [300, 305]


def test_un_refus_EXPIRE(monkeypatch):
    """Une échéance gagne de nouveaux strikes quand le sous-jacent s'éloigne.
    Retenir un refus pour toujours finirait par cacher des contrats listés."""
    M.noter_refus('AAPL', '20261016', [305])
    assert M.filtrer('AAPL', '20261016', [300, 305]) == [300]
    faux_temps = time.time() + M.DUREE_REFUS_S + 60
    monkeypatch.setattr(M.time, 'time', lambda: faux_temps)
    assert M.filtrer('AAPL', '20261016', [300, 305]) == [300, 305]


#  ═══════════  4. elle ne fuit pas, et ne gobe pas n'importe quoi  ════════════

def test_un_strike_ILLISIBLE_n_entre_pas_dans_la_memoire():
    """Une clé qu'aucune demande ne pourra jamais égaler encombre sans servir."""
    assert M.noter_refus('AAPL', '20261016', ['n/d', None, 305]) == 1


def test_une_valeur_illisible_PROPOSEE_est_simplement_ignoree():
    assert M.filtrer('AAPL', '20261016', [100, 'n/d', None, 110]) == [100, 110]


def test_la_memoire_est_PLAFONNEE():
    """Sans plafond, un produit qui tourne des semaines garde une entrée par
    couple visité — la fuite lente que personne ne voit avant qu'elle compte."""
    for i in range(M.MAX_ENTREES + 200):
        M.noter_refus('S%d' % i, '20261016', [100.0])
    assert M.statistiques()['couples'] <= M.MAX_ENTREES


def test_les_statistiques_permettent_de_MESURER_l_effet():
    """Un correctif dont on ne peut pas mesurer l'effet est une intention."""
    M.noter_refus('AAPL', '20261016', [300, 305])
    s = M.statistiques()
    assert s['couples'] == 1 and s['refus_retenus'] == 2


#  ═══════════  5. le branchement existe VRAIMENT  ═════════════════════════════

def test_la_rotation_CONSULTE_la_memoire_et_l_ALIMENTE():
    """Un module parfait que personne n'appelle ne corrige rien."""
    from pathlib import Path
    src = (Path(__file__).resolve().parents[1] / 'terminal.py').read_text(
        encoding='utf-8', errors='replace')
    i = src.index('def chain(sym, m, exp, right):')
    bloc = src[i:i + 2000]
    assert '_strike_memory.filtrer(' in bloc, 'la memoire n est pas consultee'
    assert '_strike_memory.noter_refus(' in bloc, 'les refus ne sont pas appris'
    assert '_strike_memory.noter_acceptes(' in bloc, (
        "sans cet apprentissage, un refus pris pendant une coupure resterait "
        "vrai six heures")
