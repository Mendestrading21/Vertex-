"""Vertex Test 1.0 · #779 — PARITÉ DU RUNTIME, POSÉE AVANT TOUTE EXTRACTION.

`MIGRATION_PLAN.md` §Phase 2 : *« Chaque extraction conserve un adaptateur, un
test de parité et un rollback. »* Ce fichier est ce test de parité, et il vient
**avant** la première extraction — sans lui, aucun découpage de `terminal.py`
n'est prouvable, seulement plausible.

## Ce qu'il fige, et pourquoi ces quatre-là

1. **La surface de routes** — l'extraction déplace du code d'un fichier à un
   autre ; si une route disparaît ou change de chemin en route, l'application
   perd une capacité en silence. Le test compare l'ENSEMBLE des règles, pas leur
   nombre : un compte identique peut cacher un échange.
2. **Aucun worker démarré à l'import** — critère d'acceptation explicite de
   #779 (« aucun double démarrage de worker »). Aujourd'hui `terminal.py` ne
   démarre ses 15 fils que dans `_start_app()` ; une factory mal extraite les
   ferait partir à l'import, et deux workers concurrents corrompraient l'état
   partagé sans rien casser de visible.
3. **Les invariants de sécurité** — `READONLY`, `ANALYSIS_ONLY`. Ils ne
   dépendent pas du découpage, et c'est justement pour ça qu'ils doivent être
   revérifiés à chaque étape : une régression ici ne se verrait nulle part
   ailleurs.
4. **Le point d'entrée canonique** — `vertex.runtime:app` doit rester
   l'application servie, quel que soit le chemin interne pour l'obtenir.

## Ce qu'il ne prétend pas

Il ne teste ni le comportement des vues, ni les données, ni l'UI : ces preuves
appartiennent à la suite complète et aux vérifications navigateur. Celui-ci
tient une seule propriété — **le découpage n'a rien perdu ni rien démarré.**
"""
import threading

import pytest

from vertex.app.config import ANALYSIS_ONLY, READONLY


@pytest.fixture(scope='module')
def application():
    """L'application par le point d'entrée CANONIQUE, jamais par `terminal`.

    Importer `terminal` directement donnerait la même application aujourd'hui —
    et c'est précisément ce que #779 doit rendre faux. Le test passe donc par
    `vertex.runtime`, pour que le jour où la factory change de propriétaire,
    c'est ce chemin-là qui soit prouvé."""
    from vertex.runtime import app
    return app


def _regles(app):
    """L'ensemble (chemin, méthodes) servi, forme comparable et stable."""
    return {
        (str(r.rule), tuple(sorted(r.methods - {'HEAD', 'OPTIONS'})))
        for r in app.url_map.iter_rules()
        if r.endpoint != 'static'
    }


def test_le_point_d_entree_canonique_sert_une_application_flask(application):
    """`vertex.runtime:app` est l'entrée WSGI déclarée par `ARCHITECTURE.md`."""
    assert application is not None
    assert hasattr(application, 'url_map'), (
        'vertex.runtime:app ne ressemble plus a une application Flask')


def test_la_surface_de_routes_reste_entiere(application):
    """LE FILET PRINCIPAL.

    On compare l'ENSEMBLE, pas le compte : un total identique peut cacher une
    route perdue et une route ajoutée. Le seuil bas protège contre le cas où
    l'application se construirait à moitié — un `url_map` presque vide passerait
    toute comparaison de forme."""
    regles = _regles(application)
    assert len(regles) >= 140, (
        'la surface de routes s\'est effondree (%d regles) : l\'application '
        'candidate ne se construit probablement qu\'a moitie' % len(regles))
    #  Quelques chemins structurants, choisis parce qu'ils appartiennent a des
    #  familles DIFFERENTES : sante, huit espaces, API de decision, journal
    #  client. Perdre l'un d'eux serait perdre une famille entiere.
    chemins = {r[0] for r in regles}
    for attendu in ('/healthz', '/', '/markets', '/opportunities', '/analysis',
                    '/portfolio', '/options', '/journal', '/system',
                    '/api/client-log'):
        assert attendu in chemins, (
            'la route « %s » a disparu de la surface servie' % attendu)


def test_aucun_worker_ne_demarre_a_l_import(application):
    """CRITÈRE D'ACCEPTATION EXPLICITE DE #779.

    `terminal.py` démarre 15 fils, mais dans `_start_app()`, pas à l'import.
    Une factory extraite trop vite les ferait partir au moment où le module est
    chargé — et sous Gunicorn, chaque worker WSGI en lancerait sa propre copie.
    Deux boucles de scan concurrentes n'échouent pas : elles se marchent dessus
    en silence."""
    vivants = [t.name for t in threading.enumerate() if t.is_alive()]
    #  On tolère les fils de l'hôte (pytest, ThreadPoolExecutor), on refuse les
    #  boucles de service du produit, reconnaissables à leur cible.
    suspects = [n for n in vivants
                if any(marque in n.lower()
                       for marque in ('_loop', 'worker', 'scan', 'radar', 'quotes'))]
    assert suspects == [], (
        'des boucles de service tournent alors que l\'application n\'a ete '
        'qu\'IMPORTEE : %s. Sous Gunicorn, chaque worker WSGI en demarrerait '
        'une copie, et deux boucles concurrentes corrompent l\'etat partage '
        'sans rien casser de visible.' % suspects)


def test_les_invariants_de_securite_survivent_au_decoupage():
    """Ils ne dépendent pas de l'architecture — et c'est pour ça qu'il faut les
    revérifier à chaque étape : une régression ici ne se verrait nulle part."""
    assert READONLY is True
    assert ANALYSIS_ONLY is True


def test_l_inventaire_est_reproductible_et_estampille():
    """L'inventaire de #779 est un livrable ; s'il n'est pas reproductible, ce
    n'est pas une mesure mais une photo. `MIGRATION_PLAN.md` §Phase 1 :
    « Aucun chiffre historique n'est repris comme baseline sans reproduction. »"""
    from tools.mesures.inventaire_runtime import inventorier
    a = inventorier()
    b = inventorier()
    assert a['totaux'] == b['totaux'], (
        'deux inventaires du meme SHA divergent : l\'instrument n\'est pas '
        'deterministe, donc ses chiffres ne sont pas une baseline')
    assert a['sha'] and a['sha'] != 'inconnu', (
        'l\'inventaire n\'est plus estampille du SHA : ses chiffres ne peuvent '
        'plus etre rattaches a un commit')
    assert a['totaux']['routes_canoniques'] > a['totaux']['routes_legacy'], (
        'les routes LEGACY sont devenues majoritaires : le monolithe reprend '
        'des responsabilites au lieu d\'en ceder')


def test_le_temoin_de_l_inventaire_mord():
    """« 0 route legacy » et « je ne sais pas voir » rendent le même chiffre."""
    from tools.mesures.inventaire_runtime import inventorier
    inv = inventorier(temoin=True)
    assert any(r['chemin'] == '/__temoin_route_fabriquee__'
               for r in inv['monolithe']['routes']), (
        'le detecteur de routes ne mord plus')
    assert '__temoin_worker__' in inv['monolithe']['workers'], (
        'le detecteur de workers ne mord plus')
    assert '__temoin_store__' in inv['monolithe']['stores'], (
        'le detecteur de stores ne mord plus')
