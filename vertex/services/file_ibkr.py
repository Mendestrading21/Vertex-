"""vertex/services/file_ibkr.py — file du worker IBKR unique (lot 40).

ib_async n'est pas thread-safe : UN seul thread possède la connexion, ça ne
change pas. Ce que la FIFO nue n'offrait pas, la file l'apporte :

- PRIORITÉS par domaine : une cotation du desk (posq, borne 12 s) ne fait
  plus la queue derrière un lot de fondamentaux de 90 s ;
- COALESCENCE : deux demandes identiques en vol ne coûtent qu'UN job
  courtier — le résultat est partagé entre tous les demandeurs ;
- PÉREMPTION : un job dont tous les demandeurs ont abandonné (evt.wait
  échu) n'est jamais exécuté — la FIFO nue le payait quand même ;
- CIRCUIT BREAKER de connexion : après un échec de connexion, la file
  répond None immédiatement pendant la fenêtre au lieu de re-sonder tous
  les ports à chaque job (6 s × ports × jobs en attente).

Aucune dépendance ib_async ici : la file est PURE (horloge injectable) et
testée à froid — `tests/test_file_ibkr_lot40.py`.
"""
from __future__ import annotations

import heapq
import threading
import time

# Plus petit = plus urgent. posq : l'utilisateur REGARDE son desk. meta/chain :
# il vient d'ouvrir une fiche options. news/scan : rythme de fond du produit.
# fund : lots de 90 s, personne n'attend devant l'écran.
PRIORITES = {'posq': 0, 'meta': 1, 'chain': 2, 'news': 3, 'scan': 3, 'fund': 4}
_PRIO_DEFAUT = 5

BREAKER_FENETRE_S = 30.0


class JobIBKR:
    __slots__ = ('kind', 'args', 'cle', 'box', 'evt', 'expire', 'fini')

    def __init__(self, kind, args, cle, expire):
        self.kind, self.args, self.cle = kind, args, cle
        self.box, self.evt = {}, threading.Event()
        self.expire = expire          # au-delà : plus AUCUN demandeur n'attend
        self.fini = False


class FileIBKR:
    def __init__(self, horloge=time.time):
        self._h = horloge
        self._lock = threading.Lock()
        self._dispo = threading.Condition(self._lock)
        self._tas = []                # (priorité, seq, job) — FIFO à priorité égale
        self._seq = 0
        self._en_vol = {}             # clé -> job (en file OU en cours d'exécution)
        self._breaker_jusqua = 0.0

    # ── côté demandeurs ─────────────────────────────────────────────────────
    def deposer(self, kind, args, timeout):
        """Enfile (ou s'attache à) un job. Rend (job, neuf)."""
        cle = (kind, repr(args))
        with self._dispo:
            job = self._en_vol.get(cle)
            if job is not None and not job.fini:
                # Coalescence : même demande déjà en vol — on la partage, et on
                # prolonge sa péremption jusqu'à la patience du nouveau venu.
                job.expire = max(job.expire, self._h() + timeout)
                return job, False
            job = JobIBKR(kind, args, cle, self._h() + timeout)
            self._en_vol[cle] = job
            heapq.heappush(self._tas, (PRIORITES.get(kind, _PRIO_DEFAUT), self._seq, job))
            self._seq += 1
            self._dispo.notify()
            return job, True

    def attendre(self, job, timeout):
        job.evt.wait(timeout)
        return job.box.get('res')

    def soumettre(self, kind, args, timeout):
        """Contrat historique de `_opt_job` : bloque jusqu'à `timeout`, None sinon."""
        job, _ = self.deposer(kind, args, timeout)
        return self.attendre(job, timeout)

    # ── côté worker (le SEUL thread qui parle à ib_async) ───────────────────
    def prochain(self, bloquant=True):
        """Job le plus urgent encore attendu ; les périmés sont soldés sans
        exécution (personne n'attend plus leur résultat)."""
        with self._dispo:
            while True:
                while not self._tas:
                    if not bloquant:
                        return None
                    self._dispo.wait()
                _, _, job = heapq.heappop(self._tas)
                if job.expire < self._h():
                    job.fini = True
                    self._en_vol.pop(job.cle, None)
                    job.box['res'] = None
                    job.evt.set()
                    continue
                return job

    def terminer(self, job, res):
        with self._lock:
            job.fini = True
            self._en_vol.pop(job.cle, None)
        job.box['res'] = res
        job.evt.set()

    # ── circuit breaker de connexion ────────────────────────────────────────
    def connexion_permise(self):
        """False pendant la fenêtre qui suit un échec de connexion : le worker
        répond None immédiatement au lieu de re-sonder les ports job après job.
        La fenêtre échue, UN essai repart (demi-ouvert) ; son issue referme ou
        rouvre le breaker via `noter_connexion`."""
        return self._h() >= self._breaker_jusqua

    def noter_connexion(self, ok):
        self._breaker_jusqua = 0.0 if ok else self._h() + BREAKER_FENETRE_S


__all__ = ['FileIBKR', 'JobIBKR', 'PRIORITES', 'BREAKER_FENETRE_S']
