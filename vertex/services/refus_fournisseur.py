"""vertex/services/refus_fournisseur.py — mémoire DATÉE des refus (lot 43).

L'univers contient des titres morts — rachetés, renommés, radiés — qu'aucun
fournisseur ne sert. Sans mémoire, la boucle des fondamentaux les redemandait
à IBKR puis yfinance À CHAQUE cycle (« Aucune définition de titre », 404),
et son rythme « rapide tant que ça remplit » ne se calmait jamais.

Principes :

- un refus n'est JAMAIS définitif : il est daté, et le TTL échu (24 h par
  défaut) le symbole est redemandé — un ticker peut renaître ;
- écarté ≠ oublié : `etat()` nomme chaque écarté et son âge, pour que
  l'interface puisse le DIRE au lieu de le taire.

Module PUR (horloge injectable) — `tests/test_refus_fournisseur.py`.
"""
from __future__ import annotations

import time

TTL_DEFAUT_S = 24 * 3600


class MemoireRefus:
    def __init__(self, ttl_s=TTL_DEFAUT_S, horloge=time.time):
        self._ttl = float(ttl_s)
        self._h = horloge
        self._refus = {}                  # SYMBOLE -> instant du dernier refus

    def noter(self, symbole):
        self._refus[str(symbole).strip().upper()] = self._h()

    def refuse_recemment(self, symbole):
        t = self._refus.get(str(symbole).strip().upper())
        return t is not None and (self._h() - t) < self._ttl

    def filtrer(self, symboles):
        """Partitionne sans perdre personne : (à demander, écartés)."""
        a_demander, ecartes = [], []
        for s in symboles:
            (ecartes if self.refuse_recemment(s) else a_demander).append(s)
        return a_demander, ecartes

    def etat(self):
        """L'état exportable — chaque écarté nommé avec son âge en secondes."""
        now = self._h()
        actifs = {s: int(round(now - t)) for s, t in self._refus.items()
                  if (now - t) < self._ttl}
        return {'n': len(actifs), 'ttl_s': self._ttl,
                'age_s_par_symbole': actifs, 'read_only': True}


__all__ = ['MemoireRefus', 'TTL_DEFAUT_S']
