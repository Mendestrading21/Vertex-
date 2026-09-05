"""LE BACKTEST DE L'EDGE NE VOIT PAS L'AVENIR — et c'est enfin vérifiable.

## Ce que ce lot change

`edge_backtest` répond à la question la plus importante que Vertex se pose sur
lui-même : « notre score prédit-il quelque chose ? ». Elle vivait dans
`terminal.py` et n'avait **aucun test** — non par négligence, mais parce
qu'elle appelait directement la collecte réseau : aucun banc ne pouvait la
faire tourner. Une fonction qui juge la valeur du produit, jamais éprouvée.

Extraite dans `vertex/engines/edge_validation.py`, elle reçoit `telecharger`
et `analyser` en paramètre. Avec des séries fabriquées et un analyseur
déterministe, la propriété qui compte devient mesurable au lieu d'être
supposée.

## La propriété qui compte

**Zéro look-ahead.** Un backtest qui laisse fuir une information postérieure à
la date évaluée produit une courbe magnifique et un mensonge. C'est le mode de
panne classique de cet exercice, et il ne se voit dans aucun résultat : la
sortie a exactement la même forme, avec de meilleurs chiffres.

Deux contrôles indépendants le bornent ici :

  1. **la fenêtre reçue** — l'analyseur ne reçoit jamais une barre postérieure
     à la date qu'il évalue ;
  2. **l'épreuve du futur divergent** — deux histoires IDENTIQUES jusqu'à une
     date, puis radicalement différentes après. Les scores calculés avant la
     bifurcation doivent être RIGOUREUSEMENT identiques dans les deux mondes.
     S'ils diffèrent d'un cheveu, une information du futur est entrée.

Le second est le plus fort : il ne suppose rien de la forme des données, il
change l'avenir et vérifie que le passé ne bouge pas.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from vertex.engines import edge_validation as ev


def _series(graine, n=700, syms=('AAA', 'BBB', 'CCC', 'DDD'), bench='SPY'):
    r = np.random.RandomState(graine)
    idx = pd.bdate_range('2022-01-03', periods=n)
    out = {}
    for k, s in enumerate(list(syms) + [bench]):
        pas = r.normal(0.0004 + k * 0.0002, 0.014, n)
        close = 100 * np.exp(np.cumsum(pas))
        out[s] = pd.DataFrame({'Open': close * .995, 'High': close * 1.01,
                               'Low': close * .99, 'Close': close,
                               'Volume': r.randint(10 ** 5, 10 ** 6, n)}, index=idx)
    return out


def _telechargeur(data):
    return lambda syms, period=None: {s: data[s] for s in syms if s in data}


def _analyseur_momentum(journal=None):
    """Déterministe, et fonction de la SEULE fenêtre reçue."""
    def analyser(sub, bret):
        if journal is not None:
            journal.append((len(sub), sub.index[-1]))
        c = sub['Close']
        if len(c) < 60:
            return {'score': None}
        mom = float(c.iloc[-1]) / float(c.iloc[-60]) - 1
        return {'score': max(0.0, min(100.0, 50 + 400 * mom + 10 * bret))}
    return analyser


UNIVERS = ['AAA', 'BBB', 'CCC', 'DDD']


# ── 1. Anti-vide : le backtest produit vraiment quelque chose ───────────────

def test_le_backtest_rend_un_resultat_peuple():
    """Sans ce dénominateur, tous les contrôles suivants seraient vrais sur du
    vide — le mode d'échec exact que ce dépôt reproche aux détecteurs muets."""
    r = ev.edge_backtest(telecharger=_telechargeur(_series(0)),
                         analyser=_analyseur_momentum(),
                         univers=UNIVERS, bench='SPY')
    assert r is not None, 'le backtest ne produit rien sur des séries valides'
    assert r['n_obs'] >= ev.OBSERVATIONS_MINIMUM
    assert r['n_syms'] == len(UNIVERS)
    assert set(r['buckets']) == {'5', '21', '63'}
    assert sum(b['n'] for b in r['buckets']['21']) == r['n_obs'], (
        'les tranches ne totalisent pas les observations — un point se perd')


def test_la_sortie_porte_son_denominateur():
    """Un IC ou un écart sans population est un chiffre sans portée."""
    r = ev.edge_backtest(telecharger=_telechargeur(_series(1)),
                         analyser=_analyseur_momentum(),
                         univers=UNIVERS, bench='SPY')
    for cle in ('n_obs', 'n_syms', 'n_dates', 'horizons'):
        assert cle in r, 'dénominateur manquant : %s' % cle
    for tranche in r['buckets']['21']:
        assert 'n' in tranche
        if tranche['n'] == 0:
            assert tranche['mean'] is None and tranche['hit'] is None, (
                'une tranche VIDE affiche une moyenne — un chiffre inventé')


# ── 2. Zéro look-ahead, contrôle 1 : la fenêtre reçue ───────────────────────

def test_l_analyseur_ne_recoit_jamais_une_barre_du_FUTUR():
    data = _series(2)
    journal = []
    ev.edge_backtest(telecharger=_telechargeur(data),
                     analyser=_analyseur_momentum(journal),
                     univers=UNIVERS, bench='SPY')
    assert journal, 'l’analyseur n’a jamais été appelé — rien n’est prouvé'
    dates = {s: list(data[s].dropna().index) for s in UNIVERS}
    for taille, derniere in journal:
        #  La fenêtre est un PRÉFIXE : sa longueur donne sa dernière position,
        #  et cette position doit porter exactement la date reçue.
        trouve = any(len(d) >= taille and d[taille - 1] == derniere
                     for d in dates.values())
        assert trouve, (
            'fenêtre de %d barres finissant le %s : elle ne correspond à aucun '
            'préfixe des séries — une barre a été ajoutée ou décalée'
            % (taille, derniere))


def test_le_controle_de_fenetre_mordrait_sur_une_fuite():
    """Contre-épreuve : si le contrôle ci-dessus acceptait n'importe quelle
    fenêtre, il ne garderait rien. Une fenêtre allongée d'une barre doit être
    reconnue comme impossible."""
    data = _series(2)
    dates = {s: list(data[s].dropna().index) for s in UNIVERS}
    taille = 300
    vraie = dates['AAA'][taille - 1]
    fuite = dates['AAA'][taille]            # une barre plus loin : le futur
    assert any(len(d) >= taille and d[taille - 1] == vraie for d in dates.values())
    assert not any(len(d) >= taille and d[taille - 1] == fuite
                   for d in dates.values()), 'le critère ne discrimine pas'


# ── 3. Zéro look-ahead, contrôle 2 : l'épreuve du futur divergent ───────────

def test_changer_l_AVENIR_ne_change_AUCUN_score_du_PASSE():
    """Le contrôle le plus fort, et le seul qui ne suppose rien de la forme des
    données. Deux mondes identiques jusqu'à une date, puis radicalement
    différents. Tout score calculé avant la bifurcation doit être identique
    au bit près : la moindre différence signe une information du futur.
    """
    n, coupure = 700, 500
    monde_a = _series(3, n=n)
    monde_b = {s: df.copy() for s, df in monde_a.items()}
    for s, df in monde_b.items():
        #  Après la coupure, l'avenir devient méconnaissable : effondrement
        #  puis envolée. Aucun modèle honnête du passé ne peut en dépendre.
        futur = df['Close'].to_numpy(copy=True)
        futur[coupure:] = futur[coupure:] * np.linspace(0.2, 5.0, n - coupure)
        df['Close'] = futur
        df['Open'], df['High'], df['Low'] = futur * .995, futur * 1.01, futur * .99

    def scores(data):
        vus = {}

        def analyser(sub, bret):
            c = sub['Close']
            if len(c) < 60:
                return {'score': None}
            mom = float(c.iloc[-1]) / float(c.iloc[-60]) - 1
            note = max(0.0, min(100.0, 50 + 400 * mom + 10 * bret))
            #  Clé : la taille de fenêtre. Deux mondes, même position évaluée.
            vus.setdefault(len(sub), []).append(note)
            return {'score': note}

        ev.edge_backtest(telecharger=_telechargeur(data), analyser=analyser,
                         univers=UNIVERS, bench='SPY')
        return vus

    a, b = scores(monde_a), scores(monde_b)
    communes = [k for k in sorted(set(a) & set(b)) if k <= coupure]
    assert len(communes) >= 10, (
        'seulement %d positions évaluées avant la bifurcation — l’épreuve ne '
        'porterait presque sur rien' % len(communes))
    for taille in communes:
        assert a[taille] == b[taille], (
            'à %d barres — donc AVANT la bifurcation en %d — les scores '
            'diffèrent entre deux mondes qui ne se distinguent que par leur '
            'AVENIR : %r contre %r. Une information postérieure à la date '
            'évaluée entre dans le score.' % (taille, coupure,
                                              a[taille][:3], b[taille][:3]))


def test_l_epreuve_du_futur_divergent_saurait_voir_une_fuite():
    """Contre-épreuve du banc précédent : un analyseur qui TRICHE — à qui l'on
    donne l'avenir — doit faire diverger les scores. Sans ce témoin, le banc
    ci-dessus pourrait passer parce que les deux mondes sont trop semblables,
    et non parce que le backtest est honnête."""
    n, coupure = 700, 500
    monde_a = _series(3, n=n)
    monde_b = {s: df.copy() for s, df in monde_a.items()}
    for s, df in monde_b.items():
        futur = df['Close'].to_numpy(copy=True)
        futur[coupure:] = futur[coupure:] * np.linspace(0.2, 5.0, n - coupure)
        df['Close'] = futur

    def scores(data):
        vus = {}
        #  L'analyseur tricheur lit la série ENTIÈRE, pas la fenêtre reçue.
        entier = data['AAA']['Close']

        def analyser(sub, bret):
            note = float(entier.iloc[-1]) % 100          # dépend du futur
            vus.setdefault(len(sub), []).append(note)
            return {'score': note}

        ev.edge_backtest(telecharger=_telechargeur(data), analyser=analyser,
                         univers=UNIVERS, bench='SPY')
        return vus

    a, b = scores(monde_a), scores(monde_b)
    communes = [k for k in sorted(set(a) & set(b)) if k <= coupure]
    assert any(a[t] != b[t] for t in communes), (
        'un analyseur qui lit ouvertement l’avenir ne fait pas diverger les '
        'scores — l’épreuve du futur divergent ne prouverait rien')


# ── 4. Le refus : sous le seuil, une absence et non un verdict ──────────────

def test_sous_le_seuil_d_observations_le_backtest_REFUSE_de_conclure():
    """Un IC calculé sur douze points a l'air d'un résultat et n'en est pas."""
    assert ev.OBSERVATIONS_MINIMUM == 50
    court = _series(4, n=300)               # trop court : < 260 + Hmax
    r = ev.edge_backtest(telecharger=_telechargeur(court),
                         analyser=_analyseur_momentum(),
                         univers=UNIVERS, bench='SPY')
    assert r is None, 'un verdict est publié sur un échantillon insuffisant'


def test_une_collecte_en_ECHEC_rend_une_absence_et_non_un_zero():
    def telechargeur_casse(syms, period=None):
        raise RuntimeError('réseau indisponible')

    r = ev.edge_backtest(telecharger=telechargeur_casse,
                         analyser=_analyseur_momentum(),
                         univers=UNIVERS, bench='SPY')
    assert r is None


def test_un_analyseur_MUET_ne_fabrique_pas_d_observations():
    """Si l'analyseur ne rend aucun score, il n'y a rien à mesurer — et surtout
    pas un score de remplacement."""
    r = ev.edge_backtest(telecharger=_telechargeur(_series(5)),
                         analyser=lambda sub, bret: {'score': None},
                         univers=UNIVERS, bench='SPY')
    assert r is None


# ── 5. La porte du produit reste branchée ───────────────────────────────────

def test_terminal_expose_toujours_la_porte_avec_sa_signature():
    """`_edge_loop` appelle `terminal.edge_backtest()` sans argument. Si la
    porte changeait de forme, la boucle échouerait en silence dans son
    `except`."""
    import inspect

    import terminal
    sig = inspect.signature(terminal.edge_backtest)
    assert list(sig.parameters) == ['syms', 'horizons', 'step', 'lookback']
    for nom, p in sig.parameters.items():
        assert p.default is not inspect.Parameter.empty, (
            '%s n’a plus de valeur par défaut — `edge_backtest()` casserait' % nom)
    assert '_edge_validation.edge_backtest' in inspect.getsource(terminal.edge_backtest)
