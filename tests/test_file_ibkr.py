"""Lot 40 — refonte de la file worker IBKR (le « vrai corps du lot 6 »).

La FIFO nue sérialisait TOUT derrière un worker unique : une cotation UI
(borne 12 s) attendait un lot de fondamentaux de 90 s, deux demandes
identiques coûtaient deux jobs courtier, un job dont le demandeur avait
abandonné s'exécutait quand même, et en panne de connexion chaque job
re-sondait tous les ports (6 s × ports × jobs en attente).

Bancs PURS : aucune connexion IBKR, aucun thread worker réel — la file est
testée à froid avec une horloge injectée.
"""
import threading
from pathlib import Path

from vertex.services.file_ibkr import FileIBKR, PRIORITES

RACINE = Path(__file__).resolve().parent.parent


# ── Priorités ────────────────────────────────────────────────────────────────

def test_priorites_la_cotation_ui_passe_avant_le_fond():
    """posq (l'utilisateur regarde son desk) double fund/scan déposés avant."""
    f = FileIBKR()
    f.deposer('fund', ('batch-1',), timeout=90)
    f.deposer('scan', ('TOP_PERC_GAIN',), timeout=45)
    f.deposer('posq', ('lots',), timeout=12)
    assert f.prochain(bloquant=False).kind == 'posq'
    assert f.prochain(bloquant=False).kind == 'scan'
    assert f.prochain(bloquant=False).kind == 'fund'


def test_fifo_conserve_a_priorite_egale():
    f = FileIBKR()
    f.deposer('chain', ('AAA', 'm', '2027-01-15', 'C'), timeout=75)
    f.deposer('chain', ('BBB', 'm', '2027-01-15', 'C'), timeout=75)
    assert f.prochain(bloquant=False).args[0] == 'AAA'
    assert f.prochain(bloquant=False).args[0] == 'BBB'


def test_toutes_les_sortes_du_worker_ont_une_priorite_declaree():
    for kind in ('posq', 'meta', 'chain', 'news', 'scan', 'fund'):
        assert kind in PRIORITES, kind


# ── Coalescence ──────────────────────────────────────────────────────────────

def test_coalescence_deux_demandes_identiques_un_seul_job():
    f = FileIBKR()
    j1, neuf1 = f.deposer('chain', ('NVDA', '2027-01-15', 'C'), timeout=75)
    j2, neuf2 = f.deposer('chain', ('NVDA', '2027-01-15', 'C'), timeout=75)
    assert neuf1 is True and neuf2 is False
    assert j1 is j2
    assert f.prochain(bloquant=False) is j1
    assert f.prochain(bloquant=False) is None      # un seul job en file


def test_coalescence_le_resultat_est_partage():
    f = FileIBKR()
    res = {}

    def demandeur(nom):
        res[nom] = f.soumettre('meta', ('SPY',), timeout=5)

    t1 = threading.Thread(target=demandeur, args=('a',))
    t2 = threading.Thread(target=demandeur, args=('b',))
    t1.start(); t2.start()
    # worker simulé : UN job sort, un seul résultat sert les deux demandeurs
    job = f.prochain()
    f.terminer(job, {'spot': 431.5})
    t1.join(2); t2.join(2)
    assert res['a'] == {'spot': 431.5}
    assert res['b'] == {'spot': 431.5}
    assert f.prochain(bloquant=False) is None


def test_des_cles_differentes_ne_coalescent_pas():
    f = FileIBKR()
    f.deposer('meta', ('SPY',), timeout=5)
    f.deposer('meta', ('QQQ',), timeout=5)
    a = f.prochain(bloquant=False)
    b = f.prochain(bloquant=False)
    assert {a.args[0], b.args[0]} == {'SPY', 'QQQ'}


def test_apres_terminer_la_cle_est_libre_pour_un_job_neuf():
    f = FileIBKR()
    j1, _ = f.deposer('meta', ('SPY',), timeout=5)
    f.terminer(f.prochain(bloquant=False), {'v': 1})
    j2, neuf = f.deposer('meta', ('SPY',), timeout=5)
    assert neuf is True and j2 is not j1


# ── Péremption (jobs abandonnés) ─────────────────────────────────────────────

def test_un_job_abandonne_n_est_jamais_execute():
    """La FIFO nue exécutait des jobs que plus personne n'attendait."""
    t = [0.0]
    f = FileIBKR(horloge=lambda: t[0])
    f.deposer('chain', ('MSFT', '2027-01-15', 'C'), timeout=10)
    t[0] = 11.0                                    # le demandeur est parti
    assert f.prochain(bloquant=False) is None      # sauté, pas exécuté


def test_une_attache_prolonge_la_peremption():
    t = [0.0]
    f = FileIBKR(horloge=lambda: t[0])
    f.deposer('chain', ('MSFT', '2027-01-15', 'C'), timeout=10)
    t[0] = 8.0
    f.deposer('chain', ('MSFT', '2027-01-15', 'C'), timeout=10)   # 2e demandeur
    t[0] = 15.0                                    # 1er parti, 2e attend encore
    job = f.prochain(bloquant=False)
    assert job is not None and job.kind == 'chain'


def test_soumettre_rend_none_quand_personne_ne_sert():
    f = FileIBKR()
    assert f.soumettre('meta', ('SPY',), timeout=0.05) is None


# ── Circuit breaker de connexion ─────────────────────────────────────────────

def test_breaker_ouvre_apres_echec_et_reessaie_apres_la_fenetre():
    t = [0.0]
    f = FileIBKR(horloge=lambda: t[0])
    assert f.connexion_permise() is True
    f.noter_connexion(False)
    assert f.connexion_permise() is False          # ouvert : None immédiat
    t[0] = 29.0
    assert f.connexion_permise() is False
    t[0] = 31.0
    assert f.connexion_permise() is True           # demi-ouvert : on réessaie
    f.noter_connexion(True)
    assert f.connexion_permise() is True           # refermé


def test_breaker_reste_ferme_apres_succes():
    f = FileIBKR()
    f.noter_connexion(True)
    assert f.connexion_permise() is True


# ── Intégration terminal.py ──────────────────────────────────────────────────

def test_terminal_consomme_la_file_lot40_et_plus_la_fifo_nue():
    src = (RACINE / 'terminal.py').read_text(encoding='utf-8')
    assert 'file_ibkr' in src, 'terminal.py doit consommer vertex.services.file_ibkr'
    assert '_optq = _queue.Queue()' not in src, 'la FIFO nue doit disparaître'
    assert 'connexion_permise' in src, 'le worker doit honorer le breaker'
