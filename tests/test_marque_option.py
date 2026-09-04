"""Vertex Test 1.0 — D'OÙ VIENT LA MARQUE D'UNE OPTION, ET CE QU'ELLE VAUT.

Mesuré sur le compte réel le 24 août 2026, contrat URA 20270115 C 50 :

| grandeur | valeur |
|---|---:|
| marché | **3,50 / 4,30** — spread **20,5 %** |
| dernier échange | 3,70 (du jour, 13 contrats) |
| milieu de fourchette | 3,90 |
| clôture de la veille | 3,88 |
| marque du courtier | 3,8546 |

Vertex marquait à **3,70** — le dernier échange — et l'écran affichait
`mark 3,70`, `last: None`, `mid: None`. Trois conséquences :

1. impossible de savoir que la marque vient d'un **échange**, pas d'un milieu ;
2. impossible de voir que le marché est large de **20,5 %**, donc que toute
   valorisation est incertaine de ±10 % ;
3. l'écart de 272 USD avec le courtier restait inexplicable.

## Ce que ce banc NE demande pas

Il ne demande pas de changer la convention. Le dernier échange est un fait
réel et récent ; le milieu est le milieu d'une fourchette très large ; la
marque du courtier est un mélange propriétaire. Choisir entre les trois est un
**arbitrage**, et D-041 dit que Vertex ne tranche pas entre deux chiffres du
courtier.

Il demande que la marque **dise d'où elle vient** et que l'incertitude soit
visible. Une valorisation dont on ignore la convention n'est pas auditable.
"""
from __future__ import annotations

from vertex.positions import calculator as C


def _pos(**kw):
    base = {'symbol': 'URA', 'asset_type': 'OPTION', 'quantity': 20.0,
            'multiplier': 100.0, 'capital_committed': 7008.81,
            'cost_total': 7008.81, 'avg_cost': 3.504,
            'right': 'CALL', 'strike': 50.0, 'expiration': '20270115',
            'data_quality': {}}
    base.update(kw)
    return base


#  ═══════════  1. la provenance de la marque est EXPOSÉE  ═════════════════════

def test_une_marque_venue_du_dernier_echange_le_DIT():
    """Le cas réel du 24 août : mark 3,70 = le dernier échange, avec un marché
    3,50/4,30 autour. Sans provenance, l'écran montre un chiffre sans origine."""
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70,
                                 'bid': 3.50, 'ask': 4.30})
    assert p['mark'] == 3.70
    assert p['mark_source'] == C.MARQUE_DERNIER_ECHANGE
    assert p['last'] == 3.70, "le dernier échange doit être TRANSMIS, pas perdu"


def test_une_marque_venue_du_MILIEU_le_dit_aussi():
    p = C.enrich_option(_pos(), {'bid': 3.50, 'ask': 4.30})
    assert p['mark'] == 3.90
    assert p['mark_source'] == C.MARQUE_MILIEU
    assert p['mid'] == 3.90


def test_une_marque_venue_de_la_CLOTURE_est_signalee_comme_telle():
    """Une clôture de la veille servie comme marque du jour est la plus
    trompeuse des trois : elle a l'air d'un prix courant."""
    p = C.enrich_option(_pos(), {'mark': 3.88, 'close': 3.88})
    assert p['mark_source'] == C.MARQUE_CLOTURE


def test_une_marque_ABSENTE_ne_devient_pas_zero():
    p = C.enrich_option(_pos(), {})
    assert p['mark'] is None
    assert p['mark_source'] == C.MARQUE_ABSENTE
    assert p.get('market_value') is None
    assert p.get('unrealized_pnl') is None


#  ═══════════  2. le MILIEU est toujours calculé quand il existe  ═════════════

def test_le_milieu_est_calcule_MEME_quand_la_marque_vient_d_ailleurs():
    """Avant, `mid` restait None dès que la marque venait du dernier échange :
    on ne pouvait donc pas comparer les deux, ni voir l'écart entre le prix
    d'un échange et le milieu du marché courant."""
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70,
                                 'bid': 3.50, 'ask': 4.30})
    assert p['mid'] == 3.90
    assert p['mark'] == 3.70, "exposer le milieu ne change PAS la marque"


def test_sans_les_deux_cotes_il_n_y_a_pas_de_milieu():
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70, 'bid': 3.50})
    assert p.get('mid') is None


#  ═══════════  3. l'incertitude du marché est VISIBLE  ════════════════════════

def test_un_marche_large_rend_la_valorisation_incertaine_et_le_dit():
    """20,5 % de spread : la valorisation est incertaine de ±10 %. Afficher un
    P&L au centime sur une telle fourchette donne une précision que la donnée
    n'a pas."""
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70,
                                 'bid': 3.50, 'ask': 4.30})
    assert p['spread_absolute'] == 0.80
    assert round(p['spread_pct'], 1) == 20.5
    assert p['valorisation_incertaine'] is True


def test_un_marche_serre_n_est_PAS_signale():
    """Contre-épreuve : un avertissement présent partout ne distingue plus rien."""
    p = C.enrich_option(_pos(), {'mark': 4.00, 'bid': 3.98, 'ask': 4.02})
    assert p['valorisation_incertaine'] is False
    assert round(p['spread_pct'], 1) == 1.0


def test_sans_fourchette_l_incertitude_est_INCONNUE_pas_fausse():
    """Ne pas connaître le spread n'est pas la même chose que le savoir étroit.
    Rendre `False` ferait passer une ignorance pour une garantie."""
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70})
    assert p.get('spread_pct') is None
    assert p.get('valorisation_incertaine') is None


#  ═══════════  4. la valorisation reste inchangée  ════════════════════════════

def test_ce_lot_ne_CHANGE_aucune_valorisation():
    """Le point d'honnêteté du lot. Choisir entre dernier échange, milieu et
    marque du courtier est un ARBITRAGE — D-041 : Vertex ne tranche pas.
    Ce lot rend la convention lisible, il ne la remplace pas."""
    p = C.enrich_option(_pos(), {'mark': 3.70, 'last': 3.70,
                                 'bid': 3.50, 'ask': 4.30})
    assert p['market_value'] == 7400.0        # 3,70 × 100 × 20, comme avant
    assert p['unrealized_pnl'] == round(7400.0 - 7008.81, 2)
