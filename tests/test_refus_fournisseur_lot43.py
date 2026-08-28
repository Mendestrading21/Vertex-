"""Lot 43 — mémoire DATÉE des refus fournisseur (boucle des fondamentaux).

Mesuré au runtime (28 août 2026, session live) : l'univers contient des
titres morts — rachetés (JNPR, ANSS), renommés — qu'AUCUN fournisseur ne
sert. `_fund_loop` les voyait « manquants » pour toujours :

- les mêmes symboles redemandés à IBKR puis yfinance à CHAQUE cycle
  (« Aucune définition de titre », HTTP 404 — le bruit de log du produit) ;
- `batch = missing[:40]` : le cache plein, le lot n'était plus composé QUE
  de morts ;
- `still_missing` restait vrai à vie → la boucle tournait toutes les 45 s
  pour l'éternité au lieu de se calmer à 6 h.

La mémoire date chaque refus (TTL 24 h — un ticker peut renaître : un refus
n'est jamais définitif, il est daté) et l'état est EXPORTÉ (`fund_refus`) :
écarté ≠ oublié.
"""
import inspect

import terminal
from vertex.services.refus_fournisseur import MemoireRefus, TTL_DEFAUT_S


# ── La mémoire elle-même (horloge injectée) ──────────────────────────────────

def test_un_refus_recent_est_ecarte_puis_reessaye_apres_ttl():
    t = [0.0]
    m = MemoireRefus(ttl_s=100, horloge=lambda: t[0])
    assert m.refuse_recemment('JNPR') is False
    m.noter('JNPR')
    assert m.refuse_recemment('JNPR') is True
    t[0] = 99.0
    assert m.refuse_recemment('JNPR') is True
    t[0] = 101.0
    assert m.refuse_recemment('JNPR') is False      # le TTL échu, on réessaie


def test_filtrer_partitionne_sans_perdre_personne():
    t = [0.0]
    m = MemoireRefus(ttl_s=100, horloge=lambda: t[0])
    m.noter('ANSS')
    a_demander, ecartes = m.filtrer(['NVDA', 'ANSS', 'MSFT'])
    assert a_demander == ['NVDA', 'MSFT']
    assert ecartes == ['ANSS']


def test_la_casse_ne_cree_pas_deux_refus():
    m = MemoireRefus()
    m.noter('jnpr')
    assert m.refuse_recemment('JNPR') is True


def test_l_etat_nomme_chaque_ecarte_et_son_age():
    t = [1000.0]
    m = MemoireRefus(ttl_s=3600, horloge=lambda: t[0])
    m.noter('JNPR')
    t[0] = 1120.0
    etat = m.etat()
    assert etat['n'] == 1
    assert etat['age_s_par_symbole'] == {'JNPR': 120}
    assert etat['read_only'] is True


def test_l_etat_oublie_les_refus_echus():
    t = [0.0]
    m = MemoireRefus(ttl_s=100, horloge=lambda: t[0])
    m.noter('JNPR')
    t[0] = 200.0
    assert m.etat()['n'] == 0


def test_le_ttl_par_defaut_est_un_jour():
    #  Assez long pour tuer le bruit, assez court pour voir renaître un ticker.
    assert TTL_DEFAUT_S == 24 * 3600


# ── Intégration : la boucle des fondamentaux consulte et alimente la mémoire ─

def _src_fund_loop():
    return inspect.getsource(terminal._fund_loop)


def test_fund_loop_ecarte_les_refus_recents():
    src = _src_fund_loop()
    assert '.filtrer(' in src, \
        'la boucle redemande encore les morts à chaque cycle'


def test_fund_loop_note_les_symboles_que_personne_n_a_servis():
    src = _src_fund_loop()
    assert '.noter(' in src, \
        'un échec des deux fournisseurs doit être daté, pas oublié'


def test_le_rythme_se_calme_quand_il_ne_reste_que_des_morts():
    src = _src_fund_loop()
    assert 'refuse_recemment' in src.split('still_missing')[1].splitlines()[0], (
        'still_missing doit ignorer les refus récents — sinon la boucle '
        'tourne toutes les 45 s pour l’éternité')


def test_les_refus_sont_dits_pas_caches():
    src = _src_fund_loop()
    assert "scan_state['fund_refus']" in src, \
        'écarté ≠ oublié : l’état des refus doit être exporté'
