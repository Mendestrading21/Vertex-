"""LA SOURCE STOOQ A UN SEUL PROPRIÉTAIRE, ET CE N'EST PLUS `terminal.py`.

## Ce que ce lot déplace

`terminal.py` est l'adaptateur historique que le CLAUDE.md demande de réduire
par strangler pattern. Il hébergeait la source de secours Stooq — trois
fonctions et une table de symboles — qui n'a rien à y faire : c'est une source
de données, et `vertex/data_sources/` est son voisinage naturel.

## Le risque réel d'un déplacement, et ce qui le borne ici

Un déplacement se paie de deux façons quand on le fait mal :

  · **un second propriétaire.** Si le module copiait le cache au lieu de le
    partager, deux caches vivraient en parallèle et le scan lirait tantôt l'un,
    tantôt l'autre — sans erreur, sans trace. Le cache et son TTL restent la
    propriété de `vertex/app/caches.py`, et l'identité des objets est vérifiée
    ici, pas supposée ;
  · **une doublure de test qui ne remplace plus rien.** Deux bancs substituent
    `terminal._stooq_download` pour éprouver la dégradation du scan
    (`test_active_source_timeouts`, `test_scan_timeout_degradation`). La
    substitution ne tient que parce que l'appelant résout le nom dans les
    globales de `terminal` au moment de l'appel. Si quelqu'un « nettoyait » le
    réexport, ces deux bancs deviendraient VERTS EN NE MESURANT PLUS RIEN.
    Ce banc-ci reproduit la substitution et vérifie qu'elle mord encore.

## Ce que ce banc ne fige PAS

Aucun nombre de lignes, ici ni ailleurs : `terminal.py` doit rétrécir, mais un
seuil gelé deviendrait faux au lot suivant et se ferait desserrer sans examen.
Le contrat porte sur la PROPRIÉTÉ, pas sur la taille.
"""
from __future__ import annotations

import inspect
import os

import pytest

import terminal
from vertex.app import caches
from vertex.data_sources import stooq

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_NOMS = ('_stooq_symbol', '_stooq_one', '_stooq_download')


# ── 1. Anti-vide : le code déplacé existe bien là où on l'annonce ───────────

def test_le_module_porte_vraiment_le_code():
    """Un module vide rendrait toutes les assertions suivantes vraies pour rien."""
    for nom in _NOMS:
        f = getattr(stooq, nom, None)
        assert callable(f), '%s absente de vertex/data_sources/stooq.py' % nom
        corps = inspect.getsource(f)
        assert len(corps.splitlines()) >= 4, '%s est une coquille' % nom
    assert len(stooq._STOOQ_IDX) >= 8, 'table de symboles quasi vide'


def test_le_code_est_defini_dans_le_module_et_non_dans_terminal():
    """Le cœur du lot : `terminal` EXPOSE ces noms, il ne les DÉFINIT plus."""
    attendu = os.path.join(_RACINE, 'vertex', 'data_sources', 'stooq.py')
    for nom in _NOMS:
        source = inspect.getsourcefile(getattr(terminal, nom))
        assert os.path.abspath(source) == os.path.abspath(attendu), (
            '%s est encore définie dans %s — le déplacement n’a pas eu lieu, '
            'ou une seconde définition l’a recouverte' % (nom, source))


# ── 2. Un seul propriétaire : les objets sont les MÊMES ─────────────────────

def test_le_cache_n_est_pas_duplique_par_le_deplacement():
    """Deux caches en parallèle ne lèveraient aucune erreur : le scan lirait
    tantôt l'un, tantôt l'autre. C'est précisément ce qui ne se voit pas."""
    assert stooq._STOOQ_CACHE is caches._STOOQ_CACHE
    assert terminal._STOOQ_CACHE is caches._STOOQ_CACHE
    assert stooq._SOURCE_BUDGET_STATE is caches._SOURCE_BUDGET_STATE
    assert terminal._SOURCE_BUDGET_STATE is caches._SOURCE_BUDGET_STATE
    assert stooq._STOOQ_TTL == caches._STOOQ_TTL


def test_l_ecriture_du_module_est_LUE_par_terminal():
    """Contre-épreuve de l'identité : si les objets étaient deux copies, ce
    banc passerait quand même sur `is` mal écrit — pas sur une mutation."""
    temoin = object()
    caches._SOURCE_BUDGET_STATE['__temoin__'] = temoin
    try:
        assert terminal._SOURCE_BUDGET_STATE.get('__temoin__') is temoin
        assert stooq._SOURCE_BUDGET_STATE.get('__temoin__') is temoin
    finally:
        caches._SOURCE_BUDGET_STATE.pop('__temoin__', None)


def test_les_reexports_pointent_sur_les_memes_objets():
    for nom in _NOMS:
        assert getattr(terminal, nom) is getattr(stooq, nom), nom
    assert terminal.STOOQ_REQUEST_TIMEOUT_SECONDS == stooq.STOOQ_REQUEST_TIMEOUT_SECONDS
    assert terminal._STOOQ_IDX is stooq._STOOQ_IDX


# ── 3. Parité de comportement ───────────────────────────────────────────────

@pytest.mark.parametrize('entree,attendu', [
    ('AAPL', 'aapl.us'),          # action américaine
    ('BRK-B', 'brk-b.us'),        # tiret conservé
    ('^GSPC', '^spx'),            # indice, via la table
    ('^VIX', '^vix'),
    ('^ABCDEF', 'abcdef'),        # indice HORS table : le `^` tombe
    ('GC=F', 'xauusd'),           # matière première
    ('BTC-USD', 'btcusd'),        # crypto — et NON « btc-usd.us »
])
def test_la_traduction_des_symboles_est_inchangee(entree, attendu):
    assert stooq._stooq_symbol(entree) == attendu


def test_la_table_ne_se_confond_pas_avec_la_regle_generique():
    """Contre-épreuve : sans la table, `BTC-USD` deviendrait `btc-usd.us`, un
    symbole que Stooq ne connaît pas — et la source échouerait en silence."""
    assert stooq._stooq_symbol('BTC-USD') != 'btc-usd.us'
    assert stooq._stooq_symbol('SPY') == 'spy.us', 'la règle générique a changé'


# ── 4. La substitution des deux bancs mord toujours ─────────────────────────

def test_remplacer_terminal_stooq_download_change_VRAIMENT_le_scan(monkeypatch):
    """Reproduit ce que font `test_active_source_timeouts` et
    `test_scan_timeout_degradation`. Si le réexport disparaissait, ces deux
    bancs passeraient au vert en ne mesurant plus rien.

    `_download_universe` ÉCRIT dans `scan_state` — c'est son travail, et
    `scan_state` est partagé par tout le processus de test. Sans les
    `setitem` ci-dessous, ce banc laissait `source='unavailable'` derrière
    lui, et `test_tracking_api::test_action_au_prix_reel_du_scan` échouait
    plus loin dans la suite en lisant cette provenance-là. La panne a
    réellement eu lieu : elle est verte en isolé, rouge en suite. Ce n'est pas
    de la prudence décorative, c'est la réparation d'une fuite mesurée.
    """
    appels = []
    for cle in ('source', 'source_detail', 'abandon_debit'):
        monkeypatch.setitem(terminal.scan_state, cle, terminal.scan_state.get(cle))
    monkeypatch.setitem(terminal._SOURCE_BUDGET_STATE, 'yfinance',
                        terminal._SOURCE_BUDGET_STATE.get('yfinance'))
    monkeypatch.setattr(terminal, '_stooq_download',
                        lambda tickers: appels.append(list(tickers)) or {})

    class Vide:
        def __len__(self):
            return 0

    monkeypatch.setattr(terminal.yf, 'download', lambda *a, **k: Vide())
    terminal._download_universe(['AAA'], chunk=1)
    assert appels, (
        '`_download_universe` n’appelle plus la doublure posée sur '
        '`terminal._stooq_download` — la substitution ne remplace plus rien')


def test_sans_substitution_c_est_bien_la_vraie_fonction_qui_serait_appelee():
    """Dénominateur du banc précédent : hors monkeypatch, le nom résolu dans
    les globales de `terminal` est la fonction réelle du module."""
    assert terminal.__dict__['_stooq_download'] is stooq._stooq_download


# ── 5. La politique de fraîcheur reste écrite au bon endroit ────────────────

def test_la_politique_du_cache_reste_declaree_dans_caches():
    """Le cache a changé d'appelant, pas de propriétaire. Sa politique doit
    rester là où `test_caches_parity` la vérifie."""
    assert '_STOOQ_CACHE' in caches.POLITIQUE
    entree = caches.POLITIQUE['_STOOQ_CACHE']
    assert entree['proprietaire'] == '_stooq_download'
    assert '21600' in entree['fraicheur'] or '6 h' in entree['fraicheur']
