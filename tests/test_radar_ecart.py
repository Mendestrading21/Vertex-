"""LE RADAR NOMME CE QUI MANQUE — au lieu de se taire.

## Le défaut mesuré

`_radar_loop` interroge quatre flux du courtier : trois scanners du marché
entier (gainers, losers, most active) et le fil Dow Jones / Briefing. Ils
étaient gardés par deux `except: pass`.

Quand les quatre échouaient — **le cas nominal sans TWS** — `out` restait vide,
le `if out` sautait l'écriture, et `scan_state['radar']` gardait sa valeur
précédente PAR OMISSION. Aucune erreur, aucun état, aucune trace : la page
montrait un radar figé, et la raison de ce gel n'existait nulle part.

Une absence silencieuse ressemble à une absence de marché. Ce n'en est pas une.

## Ce que ce banc garde

1. l'écart est PUBLIÉ dès qu'un flux manque, qu'il en manque un ou quatre ;
2. la valeur précédente reste servie — elle est réelle — mais ne passe plus
   pour fraîche en silence ;
3. le job `MARKET_RADAR_REFRESH` se déclare en échec avec son motif ;
4. et le contre-exemple : quand tout va bien, aucun écart n'est publié.

## Deux destinataires, deux niveaux de détail

`radar_ecart` part au client par `/scan`, qui sérialise `{**scan_state}` : il
ne porte donc que des NOMS DE FLUX. Le vocabulaire d'erreur servi est fait de
codes stables, jamais d'un type Python — c'est la règle de
`tests/test_aucune_exception_servie.py`, et l'oublier ici aurait rouvert la
fuite que ce dépôt venait de refermer.

Le motif complet (`RuntimeError: TWS injoignable`) va au REGISTRE, surface
d'exploitation, où nommer la cause est au contraire le contrat — `_weekly_loop`
le fait déjà.
"""
from __future__ import annotations

import importlib

import pytest

import terminal

_reg = importlib.import_module('vertex.scheduler.registry')

#: Signatures d'exception Python qui n'ont rien à faire dans une charge servie.
_SIGNATURES = ('RuntimeError', 'TypeError', 'KeyError', 'ValueError',
               'IndexError', 'AttributeError', 'Traceback')


class _Sortie(BaseException):
    """Quitte la boucle après un tour. Hérite de `BaseException` pour ne pas
    être avalée par les `except Exception` de la boucle."""


@pytest.fixture()
def tour(monkeypatch):
    """Fait tourner `_radar_loop` UN tour et rend l'état observé."""
    def _lancer(job):
        dodos = []

        def _dodo(s):
            #  La 1re pause est l'amorçage de 30 s, avant la boucle.
            dodos.append(s)
            if len(dodos) > 1:
                raise _Sortie
        monkeypatch.setattr(terminal, '_opt_job', job)
        monkeypatch.setattr(terminal.time, 'sleep', _dodo)
        monkeypatch.setitem(terminal.scan_state, 'radar_ecart',
                            terminal.scan_state.get('radar_ecart'))
        monkeypatch.setitem(terminal.scan_state, 'radar',
                            terminal.scan_state.get('radar'))
        memoire = dict(_reg._JOBS.get('MARKET_RADAR_REFRESH', {}))
        _reg._JOBS.setdefault('MARKET_RADAR_REFRESH', {}).update(
            {'last_run': None, 'last_ok': None, 'last_error': None})
        try:
            with pytest.raises(_Sortie):
                terminal._radar_loop()
        finally:
            monkeypatch.undo() if False else None
        #  L'état SERVI est lu ICI, avant la restauration : le lire dans le
        #  banc donnerait l'état d'avant le tour, et le contrôle passerait
        #  pour une raison qui n'a rien à voir avec ce qu'il mesure.
        etat = {'ecart': terminal.scan_state.get('radar_ecart'),
                'radar': terminal.scan_state.get('radar'),
                'job': dict(_reg._JOBS['MARKET_RADAR_REFRESH']),
                'etat_servi': next(x for x in _reg.jobs()
                                   if x['name'] == 'MARKET_RADAR_REFRESH')['etat'],
                'dodos': dodos}
        if memoire:
            _reg._JOBS['MARKET_RADAR_REFRESH'].update(memoire)
        return etat
    return _lancer


def _tout_casse(*_a, **_k):
    raise RuntimeError('TWS injoignable')


def _tout_marche(kind, args=(), timeout=None):
    if kind == 'news':
        return [{'title': 'depeche', 'link': 'https://exemple.test/1'}]
    return [{'sym': 'AAA', 'chg': 4.2}]


# ── 1. Le cas nominal sans TWS : les quatre flux tombent ────────────────────

def test_quatre_flux_en_echec_publient_un_ecart_NOMME(tour):
    etat = tour(_tout_casse)
    ec = etat['ecart']
    assert ec, (
        'les quatre flux ont échoué et AUCUN écart n’est publié — le radar '
        'garderait sa valeur précédente par omission, sans raison nulle part')
    assert sorted(ec['flux_absents']) == ['active', 'gainers', 'losers', 'news']
    assert ec['attendus'] == 4, 'le dénominateur manque : 4 absents sur combien ?'


def test_le_job_se_declare_en_echec_avec_son_motif(tour):
    j = tour(_tout_casse)['job']
    assert j['last_ok'] is False, (
        'les quatre flux ont échoué et le job se déclare sain — vert de façade')
    assert 'TWS injoignable' in (j['last_error'] or ''), (
        'le registre reçoit un échec sans cause : %r' % j['last_error'])


def test_l_etat_servi_du_job_est_ERREUR(tour):
    etat = tour(_tout_casse)['etat_servi']
    assert etat == 'ERREUR', 'état servi après un tour tout en échec : %s' % etat


def test_l_etat_servi_apres_un_tour_SAIN_est_ACTIF(tour):
    """Contre-épreuve du précédent : un banc qui verrait « ERREUR » partout
    ne discriminerait rien."""
    assert tour(_tout_marche)['etat_servi'] == 'ACTIF'


# ── 2. La charge SERVIE ne porte aucun type Python ──────────────────────────

def test_l_ecart_servi_ne_fuit_aucune_exception(tour):
    """`radar_ecart` part au client par `/scan` (`{**scan_state}`). La règle du
    dépôt : des codes stables, jamais `RuntimeError`."""
    ec = tour(_tout_casse)['ecart']
    texte = repr(ec)
    trouvees = sorted({s for s in _SIGNATURES if s in texte})
    assert trouvees == [], (
        'l’écart servi porte une signature d’exception %s — %s' % (trouvees, texte))


def test_le_detecteur_verrait_une_fuite():
    """Contre-épreuve : sans elle, « aucune signature » pourrait vouloir dire
    « je ne sais pas en reconnaître une »."""
    fautif = repr({'flux_absents': ['gainers: RuntimeError: TWS injoignable']})
    assert [s for s in _SIGNATURES if s in fautif], 'détecteur aveugle'


def test_le_motif_complet_va_bien_au_REGISTRE(tour):
    """Le pendant du précédent : le détail n'est pas perdu, il est adressé à
    la surface d'exploitation plutôt qu'au client."""
    j = tour(_tout_casse)['job']
    assert 'RuntimeError' in (j['last_error'] or ''), (
        'le motif technique a disparu des DEUX côtés — on aurait troqué une '
        'fuite contre une perte de diagnostic')


# ── 3. Contre-épreuve : quand tout va bien, rien n'est crié ─────────────────

def test_un_tour_SAIN_ne_publie_aucun_ecart(tour):
    etat = tour(_tout_marche)
    assert etat['ecart'] is None, (
        'un tour sans échec publie un écart : le signal deviendrait du bruit '
        '— %r' % etat['ecart'])
    assert etat['job']['last_ok'] is True
    assert etat['radar'] and etat['radar'].get('ts'), (
        'le relevé sain ne porte pas son époque serveur : la page ne peut pas '
        'afficher un âge vrai')


def test_un_tour_PARTIEL_nomme_seulement_ce_qui_manque(tour):
    """Trois flux sur quatre : l'écart doit être précis, pas binaire."""
    def _news_seule_casse(kind, args=(), timeout=None):
        if kind == 'news':
            raise RuntimeError('flux courtier indisponible')
        return [{'sym': 'AAA'}]

    etat = tour(_news_seule_casse)
    assert etat['ecart'] and etat['ecart']['flux_absents'] == ['news'], (
        'un seul flux manque et l’écart ne le dit pas précisément : %r'
        % etat['ecart'])
    assert etat['radar'], 'les trois flux servis doivent quand même être publiés'
    assert etat['job']['last_ok'] is True, (
        'trois flux sur quatre ont abouti : le tour n’est pas un échec, '
        'l’écart suffit à le dire')
