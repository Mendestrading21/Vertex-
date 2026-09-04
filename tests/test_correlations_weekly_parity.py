"""Vertex Test 1.0 · #779/G1 — CORRÉLATIONS ET SÉLECTION HEBDO SORTENT.

Deux routes de plus, avec les petits groupes de helpers qui les retenaient :

- `/api/correlations/<sym>` — carte des références, normalisation des dates,
  cache des séries ;
- `/weekly-regen` — chemin du snapshot figé, carte des résultats à venir.

```text
routes LEGACY   5 → 3
```

## Ce que j'ai cassé en transcrivant, et comment je l'ai vu

La première version de `api_correlations` dans le nouveau module portait trois
écarts que je n'avais pas décidés : un `.dropna()` ajouté sur les rendements, un
seuil de points passé de **20 à 30**, et une garde de colonne en plus.

Aucun test n'aurait échoué : la route rend une liste, et une liste plus courte
reste une liste. Les **corrélations servies** auraient simplement changé, sans
que personne ne l'ait demandé. Une extraction qui retouche au passage n'est plus
une extraction.

Corrigé par comparaison ligne à ligne des deux corps, normalisés des seuls
renommages. Les tests ci-dessous verrouillent les deux valeurs.

## Le piège du chemin, encore — et il n'aurait rien levé

`terminal.py` calculait `WEEKLY_PATH` par
`os.path.join(os.path.dirname(__file__), 'weekly_snapshot.json')`. Recopier
cette formule dans `vertex/app/` la ferait pointer **à côté du code** : le
snapshot de la semaine serait écrit ailleurs, l'ancien ne serait plus jamais
relu, et la sélection repartirait de zéro un lundi — **sans erreur**. Même
famille que le `static_folder` de la fabrique.

Le chemin passe donc par `persist.cache_path`, qui rend exactement la même
valeur (vérifié par égalité, pas par lecture).

## Une limite observée, laissée telle quelle

Quand le réseau ne répond pas, `/api/correlations` rend `corr: []` **sans** clé
`error` : aucune exception n'est levée, la boucle ne trouve simplement rien.
« Impossible de mesurer » devient donc indiscernable de « mesuré, rien de
significatif ». C'est le comportement d'avant, préservé délibérément — le
corriger serait un changement de contrat, pas une extraction.
"""
import pathlib
import re

import pytest

from vertex.app import factory, weekly_selection
from vertex.app.routes import correlations_api

RACINE = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def application():
    from vertex.runtime import app
    return app


def test_les_deux_routes_repondent(application):
    client = application.test_client()
    corps = client.get('/api/correlations/AAPL').get_json()
    assert corps['sym'] == 'AAPL' and isinstance(corps['corr'], list)
    r = client.get('/weekly-regen')
    assert r.status_code == 200 and 'ok' in r.get_json()


def test_les_blueprints_sont_les_proprietaires_declares(application):
    adaptateur = application.url_map.bind('localhost')
    for chemin, point in (('/api/correlations/AAPL', 'correlations_api.api_correlations'),
                          ('/weekly-regen', 'weekly_api.weekly_regen_ep')):
        vu, _ = adaptateur.match(chemin)
        assert vu == point, '%s est servi par « %s »' % (chemin, vu)


def test_le_monolithe_ne_les_definit_plus():
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    for vue in ('api_correlations', 'weekly_regen_ep', '_to_naive',
                '_corr_benchmarks', '_earnings_map'):
        assert not re.search(r'^def %s\(' % vue, src, re.M), (
            '`terminal.py` redefinit %s' % vue)
    assert not re.search(r'^_CORR_MAP\s*=', src, re.M)


def test_le_calcul_de_correlation_n_a_PAS_ete_retouche():
    """LE TEST LE PLUS IMPORTANT DE CE LOT.

    Trois écarts s'étaient glissés dans la transcription : un `.dropna()` en
    plus, un seuil passé de 20 à 30, une garde de colonne ajoutée. Aucun test
    n'aurait échoué — la route rend une liste, et une liste plus courte reste
    une liste. Seules les **corrélations servies** auraient changé."""
    src = pathlib.Path(correlations_api.__file__).read_text(encoding='utf-8')
    corps = src[src.index('def api_correlations'):]
    assert 'rets = df.pct_change()\n' in corps, (
        'un `.dropna()` (ou autre) a ete ajoute au calcul des rendements : les '
        'correlations servies changent sans que personne l\'ait demande')
    assert 'if len(pair) < 20:' in corps, (
        'le seuil minimal de points appaires a change : moins de references '
        'seraient servies, sans qu\'aucun test ne le voie')


def test_le_chemin_du_snapshot_hebdo_n_a_pas_bouge():
    """Recopier `os.path.dirname(__file__)` dans `vertex/app/` ferait pointer le
    snapshot à côté du code : l'ancien ne serait plus jamais relu, et la
    sélection repartirait de zéro un lundi — **sans erreur**."""
    import terminal
    #  ON COMPARE A LA RACINE, PAS A `persist.cache_path`. Premiere version :
    #  elle appelait la fonction — qui est monkeypatchee vers un dossier
    #  temporaire par `tests/test_persist_lot392.py`. Le test passait seul et
    #  echouait dans la suite complete. Troisieme dependance a l'ordre des
    #  autres tests que je pose et corrige dans cette serie.
    #
    #  Ce que l'echec a RÉVÉLÉ, et qui vaut d'etre ecrit : `CHEMIN` est calcule
    #  UNE FOIS a l'import. Rediriger `cache_path` plus tard ne le deplace pas —
    #  c'etait deja vrai du `WEEKLY_PATH` du monolithe, et ca reste vrai ici.
    assert pathlib.Path(weekly_selection.CHEMIN) == RACINE / 'weekly_snapshot.json'
    assert terminal.WEEKLY_PATH == weekly_selection.CHEMIN, (
        'le monolithe et le paquet visent deux fichiers differents : la '
        'selection ecrite d\'un cote serait relue de l\'autre')
    #  Et la formule employee reste celle du depot, pas un dirname local.
    src = pathlib.Path(weekly_selection.__file__).read_text(encoding='utf-8')
    assert 'persist.cache_path(' in src, (
        'le chemin est de nouveau calcule a la main : `os.path.dirname(__file__)` '
        'dans vertex/app/ ferait ecrire le snapshot a cote du code')


def test_la_carte_des_resultats_ne_devine_rien():
    """`dte` absent ⇒ le titre n'est PAS écarté. Ne pas savoir quand tombent les
    résultats n'est pas savoir qu'ils tombent cette semaine."""
    from vertex.app.state import cal_state
    memoire = list(cal_state.get('items') or [])
    try:
        cal_state['items'] = [{'sym': 'AAA', 'dte': 3},
                              {'sym': 'BBB'},                 # dte inconnu
                              {'sym': 'CCC', 'dte': None},    # dte inconnu
                              {'dte': 5}]                     # sans symbole
        carte = weekly_selection.carte_resultats()
        assert carte == {'AAA': 3}, (
            'un titre au calendrier incomplet est traite comme mesure : %s' % carte)
    finally:
        cal_state['items'] = memoire


def test_le_cache_des_references_est_bien_le_cache_partage():
    """Un cache local au module coûterait un téléchargement des huit références
    par fiche ouverte — elles sont pourtant identiques pour tous les titres."""
    from vertex.app.caches import _CORR_BENCH
    src = pathlib.Path(correlations_api.__file__).read_text(encoding='utf-8')
    assert 'from vertex.app.caches import _CORR_BENCH' in src
    assert correlations_api.TTL_S == 3600
    assert set(_CORR_BENCH) == {'ts', 'df'}


def test_le_registre_declare_les_nouveaux_proprietaires():
    for chemin in ('vertex.app.routes.correlations_api', 'vertex.app.routes.weekly_api'):
        assert (chemin, 'bp') in factory.BLUEPRINTS, '%s absent du registre' % chemin


def test_aucun_chemin_d_ordre_dans_les_nouveaux_modules():
    for module in ('vertex/app/routes/correlations_api.py',
                   'vertex/app/routes/weekly_api.py',
                   'vertex/app/weekly_selection.py'):
        src = RACINE.joinpath(module).read_text(encoding='utf-8')
        for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit',
                      'bracketOrder', 'MarketOrder', 'LimitOrder'):
            assert verbe not in src, '%s contient %s' % (module, verbe)
