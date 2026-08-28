"""Lot 41 — banc de CHARGE de la file IBKR (dette dite au rapport du lot 40).

Le lot 40 a testé la mécanique à froid ; ce banc met la file SOUS CONTENTION
avec un worker simulé (mêmes appels `prochain`/`terminer` que terminal.py,
durée de job contrôlée) et prouve les promesses en situation :

- saturée de lots de fond, la cotation du desk double le backlog ;
- une tempête de demandes identiques ne coûte qu'UN appel courtier ;
- les jobs périmés ne consomment PAS le temps du worker ;
- les latences par priorité sont mesurées (chiffres au rapport lot 41).

Les asserts portent sur des ORDRES et des COMPTES, jamais sur des durées
serrées — le banc reste stable sur une machine chargée.
"""
import threading
import time

from vertex.services.file_ibkr import FileIBKR


def _worker(f, journal, stop, duree_s=0.02):
    """Le worker de terminal.py, réduit à sa mécanique : un thread, un job à
    la fois, `duree_s` de « courtier » par job."""
    while not stop.is_set():
        job = f.prochain(bloquant=False)
        if job is None:
            time.sleep(0.001)
            continue
        time.sleep(duree_s)
        journal.append(job.kind)
        f.terminer(job, {'ok': True, 'kind': job.kind})


def _avec_worker(fn, duree_s=0.02):
    f, journal, stop = FileIBKR(), [], threading.Event()
    t = threading.Thread(target=_worker, args=(f, journal, stop, duree_s), daemon=True)
    t.start()
    try:
        return fn(f, journal)
    finally:
        stop.set()
        t.join(2)


# ── 1. Saturation : la cotation double le backlog ────────────────────────────

def test_saturee_de_fond_la_cotation_sort_dans_les_premiers():
    def scenario(f, journal):
        for i in range(15):                          # backlog : 15 lots de fond
            f.deposer('fund', ('batch-%d' % i,), timeout=30)
        time.sleep(0.005)                            # le worker en croque un
        res = f.soumettre('posq', ('lots-desk',), timeout=10)
        assert res == {'ok': True, 'kind': 'posq'}
        return list(journal)
    j = _avec_worker(scenario)
    # posq est servi au plus derrière LE job en cours (jamais derrière la file) :
    # position 1 ou 2 du journal, pas 16e.
    assert 'posq' in j[:2], 'cotation servie en position %d : %r' % (j.index('posq') + 1, j[:5])


def test_sous_charge_mixte_l_ordre_de_service_suit_les_priorites():
    def scenario(f, journal):
        f.deposer('fund', ('b1',), timeout=30)
        f.deposer('scan', ('TOP',), timeout=30)
        f.deposer('chain', ('NVDA', 'e', 'C'), timeout=30)
        f.deposer('meta', ('SPY',), timeout=30)
        f.deposer('posq', ('lots',), timeout=30)
        # attendre le drain complet
        fin = time.time() + 5
        while len(journal) < 5 and time.time() < fin:
            time.sleep(0.005)
        return list(journal)
    j = _avec_worker(scenario)
    assert len(j) == 5
    # Le premier servi peut être n'importe lequel (course au démarrage du
    # worker) ; à partir du 2e, l'ordre est STRICTEMENT celui des priorités.
    reste = j[1:]
    assert reste == sorted(reste, key=lambda k: {'posq': 0, 'meta': 1, 'chain': 2,
                                                 'news': 3, 'scan': 3, 'fund': 4}[k]), j


# ── 2. Tempête de demandes identiques ────────────────────────────────────────

def test_tempete_de_25_demandes_identiques_un_seul_appel_courtier():
    def scenario(f, journal):
        res, fils = {}, []

        def demandeur(i):
            res[i] = f.soumettre('chain', ('NVDA', '2027-01-15', 'C'), timeout=10)

        for i in range(25):
            fils.append(threading.Thread(target=demandeur, args=(i,)))
        for t in fils:
            t.start()
        for t in fils:
            t.join(5)
        return list(journal), res
    j, res = _avec_worker(scenario)
    assert j.count('chain') == 1, 'la tempête a coûté %d appels courtier' % j.count('chain')
    assert len(res) == 25 and all(v == {'ok': True, 'kind': 'chain'} for v in res.values())


# ── 3. Les périmés ne consomment pas le worker ───────────────────────────────

def test_un_backlog_abandonne_ne_coute_rien_au_worker():
    f, journal = FileIBKR(), []
    for i in range(10):                              # 10 demandes à patience quasi nulle
        f.deposer('chain', ('SYM%d' % i, 'e', 'C'), timeout=0.001)
    time.sleep(0.05)                                 # tous les demandeurs sont partis
    stop = threading.Event()
    t = threading.Thread(target=_worker, args=(f, journal, stop, 0.02), daemon=True)
    t.start()
    try:
        res = f.soumettre('posq', ('lots',), timeout=5)   # le seul demandeur vivant
        assert res == {'ok': True, 'kind': 'posq'}
    finally:
        stop.set()
        t.join(2)
    assert journal == ['posq'], 'le worker a payé pour des partis : %r' % journal


# ── 4. Latences par priorité, mesurées ───────────────────────────────────────

def test_latence_posq_sous_contention_reste_bornee_par_un_job():
    """30 lots de fond de 20 ms devant : la FIFO nue ferait attendre la
    cotation ~600 ms ; la file la sert en ≲ 2 durées de job."""
    def scenario(f, journal):
        for i in range(30):
            f.deposer('fund', ('b%d' % i,), timeout=60)
        time.sleep(0.005)
        t0 = time.perf_counter()
        res = f.soumettre('posq', ('lots',), timeout=10)
        lat = time.perf_counter() - t0
        assert res == {'ok': True, 'kind': 'posq'}
        return lat
    lat = _avec_worker(scenario, duree_s=0.02)
    # Borne LARGE (machine chargée, granularité d'horloge Windows ~15 ms) :
    # un job en cours (20 ms) + le posq (20 ms) + marge → 300 ms, contre
    # ~600 ms minimum si la cotation avait fait la queue derrière les 30.
    assert lat < 0.3, 'latence posq sous contention : %.0f ms' % (lat * 1000)
