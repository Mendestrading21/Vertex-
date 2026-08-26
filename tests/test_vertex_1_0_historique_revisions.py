"""Vertex 1.0 — CHAQUE RAFRAÎCHISSEMENT EFFAÇAIT L'ÉTAT PRÉCÉDENT.

`VERTEX-INTELLIGENCE-2.0` Phase 4, dernier critère d'acceptation :

> historique des révisions

## Le défaut, mesuré le 26 août 2026

`analyst_deep.get()` écrit `cache[sym] = pack`. Chaque rafraîchissement — TTL
**12 heures** — écrase l'instantané précédent. Quand un consensus BPA, une
tendance de révision ou une croissance attendue change entre deux passages,
Vertex n'en garde **aucune trace**.

Le seul « historique » disponible venait de Yahoo : `surprises.history` et
`eps_trend.d90`, un unique point à 90 jours. Ce sont les observations de Yahoo,
pas celles de Vertex.

Or pour une thèse, **le changement est souvent l'information**. Un consensus
qui glisse de 5,32 à 5,31 ne dit rien ; trois révisions à la baisse en trente
jours disent quelque chose. Sans mémoire, la seconde lecture est impossible.

## Ce qu'on sait, et ce qu'on ne sait pas

On sait **quand Vertex a vu** le changement. On ignore **quand il a eu lieu** :
entre deux passages espacés de douze heures, la révision a pu tomber à
n'importe quel moment. C'est la distinction de D-076, et elle est portée par le
nom du champ — `vu_a`, jamais `date_revision`.

Renseigner une date de révision qu'on ignore ferait passer une observation pour
un fait daté, et rendrait ces entrées utilisables comme preuve historique — ce
qu'elles ne sont pas.
"""
from __future__ import annotations

import pytest

from vertex.data_sources import revisions as R

AVANT = {'eps_trend': {'current': 5.32, 'revision_pct_90d': -0.2},
         'eps_revisions': {'net30': 0, 'trend': 'flat'},
         'growth_fwd': 0.05}
APRES = {'eps_trend': {'current': 5.10, 'revision_pct_90d': -4.3},
         'eps_revisions': {'net30': -3, 'trend': 'down'},
         'growth_fwd': 0.05}


#  ═══════════  1. le changement est vu, et nommé  ═════════════════════════════

def test_les_changements_DECISIONNELS_sont_tous_releves():
    d = R.diff(AVANT, APRES, vu_a='2026-08-26T12:00:00Z')
    assert {x['champ'] for x in d} == {
        'eps_trend.current', 'eps_trend.revision_pct_90d',
        'eps_revisions.net30', 'eps_revisions.trend'}


def test_chaque_entree_porte_l_AVANT_et_l_APRES():
    """Un journal qui ne dirait que « ça a changé » n'apprendrait rien : c'est
    le sens du mouvement qui informe."""
    d = R.diff(AVANT, APRES, vu_a='t')
    eps = next(x for x in d if x['champ'] == 'eps_trend.current')
    assert eps['avant'] == 5.32 and eps['apres'] == 5.10


def test_un_champ_INCHANGE_ne_produit_rien():
    """Contre-épreuve : `growth_fwd` vaut 0.05 des deux côtés."""
    d = R.diff(AVANT, APRES, vu_a='t')
    assert 'growth_fwd' not in {x['champ'] for x in d}


def test_le_BRUIT_d_arrondi_de_la_source_est_ignore():
    """Sans seuil, chaque passage produirait des entrées pour des variations
    que personne ne peut lire — et un journal illisible cesse d'être lu."""
    assert R.diff({'growth_fwd': 5.32}, {'growth_fwd': 5.3201}, 't') == []


def test_un_vrai_mouvement_FAIBLE_reste_vu():
    """Contre-épreuve du seuil : trop haut, il masquerait des glissements
    réels."""
    d = R.diff({'growth_fwd': 5.32}, {'growth_fwd': 5.30}, 't')
    assert len(d) == 1


def test_une_APPARITION_et_une_DISPARITION_comptent_toutes_deux():
    """Passer de `None` à une valeur est une information ; l'inverse aussi —
    une couverture analyste qui s'arrête est un signal."""
    assert R.diff({'growth_fwd': None}, {'growth_fwd': 0.05}, 't')
    assert R.diff({'growth_fwd': 0.05}, {'growth_fwd': None}, 't')


def test_un_PREMIER_passage_n_invente_aucune_revision():
    """Sans état antérieur, il n'y a rien à comparer. Fabriquer des entrées
    ferait passer une première lecture pour un mouvement."""
    assert R.diff(None, APRES, 't') == []
    assert R.diff({}, APRES, 't') == []


def test_les_entrees_illisibles_ne_font_pas_tomber_le_module():
    for sale in ('texte', 42, [1, 2], None):
        assert R.diff(sale, APRES, 't') == []
        assert R.diff(AVANT, sale, 't') == []


#  ═══════════  2. `vu_a` n'est PAS une date de révision  ══════════════════════

def test_chaque_entree_porte_VU_A_et_non_une_date_de_revision():
    """D-076 : on sait quand Vertex a vu, pas quand ça a eu lieu. Le nom du
    champ porte la distinction — un `date_revision` ferait passer une
    observation pour un fait daté."""
    d = R.diff(AVANT, APRES, vu_a='2026-08-26T12:00:00Z')
    for x in d:
        assert x['vu_a'] == '2026-08-26T12:00:00Z'
        assert 'date_revision' not in x
        assert 'date' not in x


def test_la_couverture_DECLARE_que_la_date_reelle_est_inconnue():
    c = R.couverture(R.diff(AVANT, APRES, 't'))
    assert c['date_de_revision'] is None
    assert 'OBSERVE' in c['note']
    assert "s'annulent" in c['note'], 'la limite entre deux passages doit etre dite'


def test_la_couverture_distingue_VIDE_de_PREMIER_passage():
    """Une liste vide se lit « aucune révision » alors qu'elle peut signifier
    « premier passage » ou « rien au-dessus du seuil »."""
    c = R.couverture([])
    assert c['entrees'] == 0
    assert c['vu_a_le_plus_ancien'] is None and c['vu_a_le_plus_recent'] is None
    assert c['champs_suivis']


#  ═══════════  3. l'historique est borné, et le dit  ══════════════════════════

def test_le_plus_RECENT_passe_devant():
    """Un lecteur qui tronque doit lire ce qui vient d'arriver, pas ce qui a
    été oublié."""
    h = R.accumuler([{'champ': 'vieux', 'vu_a': '1'}],
                    [{'champ': 'neuf', 'vu_a': '2'}])
    assert [x['champ'] for x in h] == ['neuf', 'vieux']


def test_l_historique_est_BORNE():
    """Un cache qui grossit sans fin finit supprimé en entier, et l'historique
    avec."""
    h = []
    for i in range(50):
        h = R.accumuler(h, [{'champ': 'c%d' % i, 'vu_a': str(i)}])
    assert len(h) == R.MAX_PAR_TITRE
    assert h[0]['champ'] == 'c49', 'le plus recent doit survivre'


def test_la_couverture_SIGNALE_la_saturation():
    """Un historique plein a perdu son début : le dire évite de le lire comme
    complet."""
    plein = [{'champ': 'c', 'vu_a': str(i)} for i in range(R.MAX_PAR_TITRE)]
    assert R.couverture(plein)['sature'] is True
    assert R.couverture(plein[:3])['sature'] is False


#  ═══════════  4. le producteur l'accumule vraiment  ══════════════════════════

def _brancher(monkeypatch, A, eps_trend, eps_revisions):
    """Fige ce que la source rend, sans dependre de l'ordre d'evaluation.

    Ma premiere version avancait un compteur depuis l'interieur d'un `lambda`,
    et partait de `-1` — qui indexe la FIN d'une liste en Python. Les blocs ne
    lisaient donc pas le meme passage, et le banc accusait le code d'un defaut
    qu'il n'avait pas. Un double de test qui se trompe coute plus cher qu'un
    banc absent.
    """
    monkeypatch.setattr(A, '_eps_trend', lambda t: dict(eps_trend))
    monkeypatch.setattr(A, '_eps_revisions', lambda t: dict(eps_revisions))
    monkeypatch.setattr(A, '_growth_fwd', lambda t: 0.05)
    for bloc in ('_surprises', '_ratings_actions', '_holders', '_insider'):
        monkeypatch.setattr(A, bloc, lambda t: None)


def test_analyst_deep_ACCUMULE_au_lieu_d_ecraser(tmp_path, monkeypatch):
    """Le défaut : `cache[sym] = pack` détruisait l'instantané précédent."""
    from vertex.data_sources import analyst_deep as A
    monkeypatch.setattr(A, 'CACHE_PATH', str(tmp_path / 'analyst.json'))

    _brancher(monkeypatch, A, {'current': 5.32, 'revision_pct_90d': -0.2},
              {'net30': 0, 'trend': 'flat'})
    p1 = A.get('TEST', force=True)
    assert p1 is not None
    assert p1['revisions_observees'] == [], 'premier passage : rien a comparer'

    _brancher(monkeypatch, A, {'current': 5.10, 'revision_pct_90d': -4.3},
              {'net30': -3, 'trend': 'down'})
    p2 = A.get('TEST', force=True)
    champs = {x['champ'] for x in p2['revisions_observees']}
    assert 'eps_trend.current' in champs, p2['revisions_observees']
    assert 'eps_revisions.trend' in champs, p2['revisions_observees']
    assert p2['revisions_couverture']['entrees'] >= 2


def test_un_passage_SANS_changement_ne_gonfle_pas_l_historique(tmp_path, monkeypatch):
    """Contre-épreuve : un journal qui grossit à chaque rafraîchissement, même
    quand rien ne bouge, devient illisible et cesse d'être lu."""
    from vertex.data_sources import analyst_deep as A
    monkeypatch.setattr(A, 'CACHE_PATH', str(tmp_path / 'analyst.json'))
    _brancher(monkeypatch, A, {'current': 5.32, 'revision_pct_90d': -0.2},
              {'net30': 0, 'trend': 'flat'})
    A.get('TEST', force=True)
    _brancher(monkeypatch, A, {'current': 5.10, 'revision_pct_90d': -4.3},
              {'net30': -3, 'trend': 'down'})
    p2 = A.get('TEST', force=True)
    p3 = A.get('TEST', force=True)          # meme source, aucun mouvement
    assert len(p3['revisions_observees']) == len(p2['revisions_observees'])


def test_l_historique_SURVIT_au_rafraichissement(tmp_path, monkeypatch):
    """Le cœur du lot : la deuxième révision ne doit pas effacer la première."""
    from vertex.data_sources import analyst_deep as A
    monkeypatch.setattr(A, 'CACHE_PATH', str(tmp_path / 'analyst.json'))
    _brancher(monkeypatch, A, {'current': 5.32, 'revision_pct_90d': -0.2},
              {'net30': 0, 'trend': 'flat'})
    A.get('TEST', force=True)
    _brancher(monkeypatch, A, {'current': 5.10, 'revision_pct_90d': -4.3},
              {'net30': -3, 'trend': 'down'})
    n2 = len(A.get('TEST', force=True)['revisions_observees'])
    _brancher(monkeypatch, A, {'current': 4.80, 'revision_pct_90d': -9.8},
              {'net30': -6, 'trend': 'down'})
    h3 = A.get('TEST', force=True)['revisions_observees']
    assert len(h3) > n2, 'la seconde revision a efface la premiere'
    #  Le plus recent devant : un lecteur qui tronque lit ce qui vient d'arriver.
    assert h3[0]['apres'] in (4.80, -9.8, -6)


def test_le_producteur_passe_par_le_PROPRIETAIRE_unique():
    """Une seconde implantation de « ce qui a changé » divergerait du premier
    champ ajouté."""
    import inspect
    from vertex.data_sources import analyst_deep as A
    src = inspect.getsource(A)
    assert '_revisions.diff' in src and '_revisions.accumuler' in src
