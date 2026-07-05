"""
vertex/engines/stats.py — STATISTIQUES D'AGRÉGATION (Ch. II).

Helpers purs et sans état : corrélation de rangs (Spearman, pour l'Information
Coefficient de l'edge) et médianes de valorisation par secteur. Extraits
verbatim du monolithe pour être testés isolément.
"""

import math
import statistics

import numpy as np


def _spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 8:
        return None
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt(float((ra * ra).sum()) * float((rb * rb).sum()))
    return round(float((ra * rb).sum() / den), 3) if den else None


def _recompute_sectors(by_sym):
    """Médianes de valorisation par secteur (mirroir de fundamentals.build, sur le cache fusionné)."""
    import statistics
    by_sector = {}
    for sec in set(v.get('sector') for v in by_sym.values() if v.get('sector')):
        m = [v for v in by_sym.values() if v.get('sector') == sec]
        pes = [v['pe'] for v in m if v.get('pe') and 0 < v['pe'] < 250]
        fwd = [v['fwd_pe'] for v in m if v.get('fwd_pe') and 0 < v['fwd_pe'] < 250]
        mg = [v['margin'] for v in m if v.get('margin') is not None]
        gr = [v['growth'] for v in m if v.get('growth') is not None]
        if pes or fwd:
            by_sector[sec] = {'median_pe': round(statistics.median(pes), 1) if pes else None,
                              'median_fwd_pe': round(statistics.median(fwd), 1) if fwd else None,
                              'median_margin': round(statistics.median(mg) * 100, 1) if mg else None,
                              'median_growth': round(statistics.median(gr) * 100, 1) if gr else None,
                              'n': len(m)}
    return by_sector


__all__ = ['spearman', 'sector_medians']

spearman = _spearman
sector_medians = _recompute_sectors
