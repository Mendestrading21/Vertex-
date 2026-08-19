"""Vertex 1.0 · #779 — PARITÉ DU REGISTRE DE ROUTES (contribution à G1).

`RELEASE_GATES.md` G1 exige que **le registre de routes ait un propriétaire
modulaire, avec parité**. Avant `vertex/app/factory.py`, 22
`app.register_blueprint(...)` étaient dispersés dans `terminal.py` entre les
lignes 147 et 2456 : personne ne pouvait répondre à « quelles routes
l'application sert-elle ? » sans lire 2 300 lignes.

## La collision qui aurait cassé en silence

Deux blueprints déclarent **le même chemin** — `/api/anomalies/<sym>`, par
`analysis_api` (sans injection) et `strategy_os_api` (à injection). Werkzeug
garde les deux règles ; c'est le **dispatch** qui tranche.

Regrouper les enregistrements sans injection **après** `strategy_os_api` aurait
donc changé le handler servi, sans erreur, sans test rouge, sans trace. Le groupe
est placé avant, et ce fichier garde ce choix.

Mesuré des deux côtés : `analysis_api.api_anomalies` gagne **avant comme après**.

## Ce que ce fichier ne prétend pas

G1 demande quatre propriétaires modulaires — factory, routes, lifecycle/workers,
scheduler. Seul le deuxième est traité. `Flask(__name__)` et les hooks de latence
restent dans `terminal.py` : les extraire demanderait de déplacer aussi la
configuration et l'observabilité, ce que `MIGRATION_PLAN.md` interdit de faire
d'un bloc.
"""
import pytest

from vertex.app import factory


@pytest.fixture(scope='module')
def application():
    from vertex.runtime import app
    return app


def test_le_dispatch_de_la_route_en_collision_est_inchange(application):
    """LE POINT LE PLUS FRAGILE DE L'EXTRACTION.

    Un test sur le NOMBRE de règles ne l'aurait pas vu : les deux règles
    existent dans les deux cas. Seul le handler effectivement choisi le dit."""
    adaptateur = application.url_map.bind('localhost')
    point, _ = adaptateur.match('/api/anomalies/ACN')
    assert point == 'analysis_api.api_anomalies', (
        '/api/anomalies/<sym> est desormais servi par « %s » : le regroupement '
        'des blueprints a change le gagnant de la collision. Verifier que '
        '`register_blueprints(app)` reste appele AVANT `strategy_os_api`.'
        % point)


def test_les_deux_regles_en_collision_coexistent_toujours(application):
    """Werkzeug garde les deux ; en perdre une serait une autre régression —
    plus visible, mais tout aussi silencieuse côté utilisateur."""
    points = sorted(r.endpoint for r in application.url_map.iter_rules()
                    if r.rule == '/api/anomalies/<sym>')
    assert points == ['analysis_api.api_anomalies', 'strategy_os.anomalies_for'], (
        'la collision connue a change de forme : %s' % points)


def test_le_registre_declare_ce_qui_est_reellement_enregistre(application):
    """Une liste déclarative qui diverge du réel est pire qu'aucune liste : elle
    fait croire à un inventaire."""
    declares = {chemin.rsplit('.', 1)[-1] for chemin, _ in factory.BLUEPRINTS}
    servis = set(application.blueprints)
    manquants = sorted(d for d in declares if d not in servis and
                       d.replace('_api', '') not in servis)
    assert not manquants, (
        'ces blueprints sont declares dans le registre mais absents de '
        'l\'application : %s' % manquants)
    assert len(factory.BLUEPRINTS) == 15, (
        'le registre ne compte plus 15 entrees (%d) : si un blueprint a migre '
        'depuis le monolithe, mettre a jour A_INJECTION en meme temps'
        % len(factory.BLUEPRINTS))


def test_les_blueprints_a_injection_restent_documentes(application):
    """`A_INJECTION` n'est pas décoratif : il dit **pourquoi** sept blueprints
    n'ont pas pu déménager. Une entrée qui disparaît sans que le blueprint bouge
    ferait mentir la doc ; une entrée qui reste alors que le blueprint a migré
    laisserait croire à un couplage résolu."""
    assert set(factory.A_INJECTION) == {
        'auth', 'desk', 'tv_webhooks', 'strategy_os_api', 'redesign',
        'positions_api', 'decision_api'}, (
        'la liste des blueprints a injection a change : verifier qu\'un '
        'couplage a bien ete resolu, et pas seulement efface de la doc')
    for nom, raison in factory.A_INJECTION.items():
        assert raison and len(raison) > 10, (
            '%s ne dit plus POURQUOI il ne peut pas deménager' % nom)


def test_le_monolithe_n_enregistre_plus_les_blueprints_sans_injection():
    """La preuve que le regroupement a RETIRÉ, et pas seulement ajouté.

    Un enregistrement resté en place ferait lever Flask (nom déjà pris) — mais
    surtout, le registre déclaratif cesserait d'être la source unique."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1].joinpath(
        'terminal.py').read_text(encoding='utf-8')
    for bp in ('_feeds.bp', '_analysis_api.bp', '_command.bp', '_session_api.bp',
               '_options_lab_api.bp', '_options_intel_api.bp', '_tracking_api.bp',
               '_opportunities_api.bp', '_planning_api.bp', '_ai_api.bp',
               '_live_api.bp', '_system.bp', '_live_events.bp', '_content.bp',
               '_company_api.bp'):
        assert ('app.register_blueprint(%s)' % bp) not in src, (
            '`terminal.py` enregistre encore %s directement : le registre '
            'declaratif n\'est plus la source unique' % bp)
    assert '_factory.register_blueprints(app)' in src, (
        'le monolithe n\'appelle plus le registre canonique : les 15 '
        'blueprints ne sont plus servis du tout')


def test_le_registre_n_importe_rien_a_son_propre_import():
    """Un registre qui importerait 15 modules au chargement ferait payer son
    coût à tous les tests, y compris ceux qui ne servent aucune route."""
    import pathlib
    src = pathlib.Path(factory.__file__).read_text(encoding='utf-8')
    tete = src.split('def register_blueprints')[0]
    assert 'from vertex.app.routes' not in tete, (
        'le registre importe des blueprints au chargement du module')
    assert 'import_module' in src, (
        'l\'import differe a disparu : le registre redevient un cout fixe')
