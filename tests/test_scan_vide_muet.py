"""Vertex Test 1.0 — LE SCAN RENDAIT ZÉRO LIGNE ET SE DÉCLARAIT SAIN.

## Ce qui a été mesuré, le 26 août 2026

Sur le programme fusionné (Black Glass + les lots de `main`), mode démo, douze
titres :

```text
rows 0    scan_error None    scanned None
```

**Aucune ligne, aucune erreur.** Le desk affiche `n/d` partout et `/healthz`
répond « ok » — le symptôme exact rapporté sur le poste réel.

## La cause

`vertex-live` a écrit un bloc de mémoïsation dans `_analyse_one` :

```python
_fp = _analyse_fp(df, bench_ret, _fund or None)
_memo = _ANALYSE_MEMO.get(sym)
```

**Ni `_analyse_fp` ni `_ANALYSE_MEMO` n'existaient.** Vérifié sur `main`, sur
`vertex-live` et dans tout l'arbre : zéro définition. Chaque symbole levait
donc `NameError` à sa première ligne utile.

Et `_safe_one` avalait tout :

```python
except Exception:
    return None   # un titre en échec est simplement ignoré
```

Ce commentaire est vrai pour **un** titre. Quand la cause est commune — un nom
absent — les 513 tombent ensemble, et « simplement ignoré » devient « produit
vide, sans un mot ».

## Les trois corrections

1. `_analyse_fp` écrite : empreinte des trois entrées d'`analyse()`.
2. `_ANALYSE_MEMO` défini.
3. `_safe_one` **nomme** ses échecs dans `scan_state['titres_en_echec']`.

Après : **12 lignes sur 12**.

## Ce que ce banc protège

Pas la mémoïsation — l'optimisation peut disparaître sans dommage. Ce qu'il
protège, c'est qu'un scan qui perd tous ses titres **le dise**.
"""
from __future__ import annotations

import os

import pytest

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('START_ON_IMPORT', '0')
os.environ.setdefault('DEMO_MODE', '1')


@pytest.fixture(scope='module')
def T():
    import terminal
    return terminal


#  ═══════════  1. les deux noms existent  ═════════════════════════════════════

def test_les_deux_noms_du_memo_EXISTENT(T):
    """Le défaut nu. Les deux étaient employés, aucun n'était défini."""
    assert hasattr(T, '_analyse_fp'), '`_analyse_fp` : NameError sur chaque titre'
    assert hasattr(T, '_ANALYSE_MEMO')
    assert isinstance(T._ANALYSE_MEMO, dict)


def test_l_empreinte_est_STABLE_pour_des_entrees_identiques(T):
    df, b, f = _serie(), _bench(), {'pe': 19.4}
    assert T._analyse_fp(df, b, f) == T._analyse_fp(df, b, f)


@pytest.mark.parametrize('quoi', ['barre', 'cloture', 'bench', 'fond'])
def test_l_empreinte_CHANGE_quand_une_entree_change(T, quoi):
    """Contre-épreuve, la seule qui compte : une empreinte qui ne bougerait pas
    servirait un résultat périmé — silencieusement, et c'est pire qu'un cache
    absent."""
    df, b, f = _serie(), _bench(), {'pe': 19.4}
    ref = T._analyse_fp(df, b, f)
    if quoi == 'barre':
        df = _serie(n=61)
    elif quoi == 'cloture':
        df = _serie(); df.iloc[-1, df.columns.get_loc('Close')] = 999.0
    elif quoi == 'bench':
        b = _bench(n=61)
    else:
        f = {'pe': 19.5}
    assert T._analyse_fp(df, b, f) != ref, quoi


def test_une_entree_ILLISIBLE_ne_produit_pas_deux_fois_la_meme_empreinte(T):
    """`None == None` est vrai : rendre `None` sur échec ferait passer deux
    échecs successifs pour un hit, et l'on servirait le résultat d'un AUTRE
    titre. Le pire défaut possible pour un cache."""
    a, b = T._analyse_fp(object(), None, None), T._analyse_fp(object(), None, None)
    assert a != b


#  ═══════════  2. le scan produit des lignes  ═════════════════════════════════

def test_le_scan_demo_rend_des_LIGNES(T):
    """Zéro avant, douze sur douze après."""
    _scan(T)
    assert len(T.scan_state.get('rows') or []) >= 10


def test_aucun_titre_n_est_en_echec_sur_un_scan_sain(T):
    _scan(T)
    assert T.scan_state.get('titres_en_echec') is None


def test_deux_passes_donnent_les_MEMES_scores(T):
    """Le mémo doit accélérer sans rien changer."""
    a = _scores(_scan(T))
    b = _scores(_scan(T))
    assert a and a == b


def test_le_memo_ne_sert_pas_le_resultat_d_un_AUTRE_titre(T):
    """Contre-épreuve du mémo : des scores tous identiques trahiraient une clé
    qui ne distingue pas les symboles."""
    s = _scores(_scan(T))
    assert len(set(s.values())) > 1, 'tous les titres ont le meme score'


#  ═══════════  3. l'échec ne se tait plus  ════════════════════════════════════

def test_un_echec_COMMUN_est_rapporte_et_non_avale(T, monkeypatch):
    """Le cœur du lot. On casse `analyse` : le scan doit rendre zéro ligne —
    c'est légitime — mais il doit le DIRE."""
    def _tombe(*a, **k):
        raise RuntimeError('panne simulee')
    monkeypatch.setattr(T, 'analyse', _tombe)
    _scan(T)
    bilan = T.scan_state.get('titres_en_echec')
    assert bilan, "zero ligne ET aucun echec declare : le defaut d'origine"
    assert bilan['n'] == bilan['total']
    assert 'panne simulee' in str(bilan['exemples'])


def test_le_rapport_est_ABSENT_quand_tout_va_bien(T):
    """Sans cette contre-épreuve, un bloc toujours présent crierait à la panne
    sur chaque scan sain, et on cesserait de le lire."""
    _scan(T)
    assert T.scan_state.get('titres_en_echec') is None


def test_le_handler_ne_reste_pas_MUET_dans_le_code(T):
    """Le recensement : un `except Exception: return None` sans trace ferait
    revenir le défaut à l'identique."""
    import inspect
    src = inspect.getsource(T._scan_once)
    i = src.index('def _safe_one')
    fenetre = src[i:i + 1400]
    assert '_echecs_titres[' in fenetre
    assert 'titres_en_echec' in src


#  ═══════════  outils  ════════════════════════════════════════════════════════

def _serie(n=60):
    import numpy as np
    import pandas as pd
    idx = pd.date_range('2026-01-01', periods=n, freq='D')
    px = np.linspace(100.0, 130.0, n)
    return pd.DataFrame({'Open': px, 'High': px * 1.01, 'Low': px * 0.99,
                         'Close': px, 'Volume': np.full(n, 1e6)}, index=idx)


@pytest.fixture(autouse=True)
def _etat_de_scan_restaure():
    #  `_scan` remplit `scan_state` du monolithe. Sans remise en etat, les
    #  bancs d'autres fichiers lisaient les lignes de CE fichier — et
    #  `test_tracking_api` voyait la provenance « demo » au lieu de « scan ».
    import terminal as T
    etat = dict(T.scan_state)
    yield
    T.scan_state.clear()
    T.scan_state.update(etat)
    T._ANALYSE_MEMO.clear()


def _bench(n=60):
    import numpy as np
    import pandas as pd
    return pd.Series(np.linspace(0.0, 0.1, n),
                     index=pd.date_range('2026-01-01', periods=n, freq='D'))


def _scan(T, n=12):
    #  `UNIVERSE` est un global du monolithe : le tronquer sans le remettre
    #  faisait echouer tout banc ulterieur qui compte l'univers, selon le seul
    #  ordre alphabetique des noms de fichiers.
    univers = T.UNIVERSE
    try:
        T.UNIVERSE = univers[:n]
        T._ANALYSE_MEMO.clear()
        T.scan_state.pop('titres_en_echec', None)
        T._scan_once()
        return T.scan_state.get('rows') or []
    finally:
        T.UNIVERSE = univers


def _scores(rows):
    out = {}
    for r in rows:
        k = r.get('symbol') or r.get('ticker') or r.get('t')
        if k:
            out[k] = r.get('score')
    return out
