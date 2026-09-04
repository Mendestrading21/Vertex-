"""Vertex Test 1.0 · #779 — PARITÉ DE L'API ENTREPRISE EXTRAITE DU MONOLITHE.

Trois routes — `/api/company/<sym>`, `/api/analyst/<sym>`, `/api/names` —
étaient décorées directement sur `app` dans `terminal.py`. Leur propriétaire est
désormais `vertex/app/routes/company_api.py`.

## Pourquoi celles-ci, et pourquoi seulement celles-ci

Les dépendances des quatorze routes LEGACY ont été mesurées à l'AST. Ces trois
sont, avec `/api/track-record`, les seules à ne dépendre de **rien d'autre que
`app`** — ni état local, ni verrou, ni fonction privée du monolithe. Elles se
déplacent donc **sans injection**, ce qui en fait la plus petite convergence
prouvable.

`/api/track-record` reste dans `terminal.py` : elle appelle l'auto-évaluation du
moteur, qui relève de la mémoire et de la calibration (#783). La ranger dans
`tracking_api`, qui gère des suivis *hypothétiques*, aurait été un mensonge de
nommage — le genre de rangement qui fait gagner un chiffre et perdre du sens.

## Ce que ce fichier garde

L'extraction déplace la **propriété**, pas le **comportement**. Le test appelle
donc les trois routes sur l'application canonique et vérifie qu'elles répondent
avec la même forme qu'avant — statut 200 et corps JSON —, plus le fait que
`terminal.py` ne les définit plus (sans quoi on aurait deux propriétaires et un
conflit d'enregistrement Flask).
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def client():
    from vertex.runtime import app
    app.config['TESTING'] = True
    return app.test_client()


def test_les_trois_routes_repondent_par_l_application_canonique(client):
    """Le contrat vu du dehors : mêmes chemins, même forme de réponse.

    En mode démonstration `/api/analyst` répond `{'demo': True}` — c'est le
    comportement d'origine, conservé mot pour mot, et c'est justement ce qu'il
    faut garder : une extraction qui « améliorerait » au passage rendrait la
    parité invérifiable."""
    for chemin in ('/api/company/ACN', '/api/analyst/ACN', '/api/names'):
        rep = client.get(chemin)
        assert rep.status_code == 200, (
            '%s ne repond plus 200 apres extraction (%d)' % (chemin, rep.status_code))
        assert rep.is_json, '%s ne rend plus du JSON' % chemin


def test_le_blueprint_est_le_proprietaire_declare():
    """Une extraction n'est finie que si le nouveau propriétaire est enregistré :
    un module créé mais jamais branché laisserait les routes absentes."""
    from vertex.runtime import app
    from vertex.app.routes import company_api
    assert company_api.bp.name == 'company_api'
    points = {r.endpoint for r in app.url_map.iter_rules()}
    for vue in ('company_api.api_company', 'company_api.api_analyst',
                'company_api.api_names'):
        assert vue in points, (
            'la vue « %s » n\'est pas servie : le blueprint n\'est pas '
            'enregistre sur l\'application canonique' % vue)


def test_le_monolithe_ne_definit_plus_ces_vues():
    """LA PREUVE QUE L'EXTRACTION A RETIRÉ, ET PAS SEULEMENT AJOUTÉ.

    Deux définitions du même chemin feraient lever Flask à l'enregistrement —
    mais surtout, un monolithe qui garde une copie n'a rien cédé du tout."""
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    for vue in ('def api_company(', 'def api_analyst(', 'def api_names('):
        assert vue not in src, (
            '`terminal.py` redefinit « %s » : le monolithe n\'a pas cede la '
            'propriete, il l\'a dupliquee' % vue)
    for chemin in ("'/api/company/<sym>'", "'/api/analyst/<sym>'", "'/api/names'"):
        assert ('@app.route(%s)' % chemin) not in src, (
            'le monolithe redecore %s sur `app`' % chemin)


def test_l_extraction_a_fait_baisser_le_compte_legacy():
    """La métrique d'avancement de #779, lue par l'instrument et non écrite.

    Le seuil est volontairement large : il ne fige pas un chiffre, il interdit
    la RÉGRESSION. Un lot suivant qui ferait remonter LEGACY au-dessus de 11
    aurait rendu une responsabilité au monolithe."""
    from tools.mesures.inventaire_runtime import inventorier
    t = inventorier()['totaux']
    assert t['routes_legacy'] <= 11, (
        'les routes LEGACY sont remontees a %d : le monolithe a repris une '
        'responsabilite au lieu d\'en ceder' % t['routes_legacy'])
    assert t['routes_canoniques'] >= 143, (
        'des routes canoniques ont disparu (%d) : verifier qu\'un blueprint '
        'n\'a pas cesse d\'etre enregistre' % t['routes_canoniques'])


def test_l_api_entreprise_ne_porte_aucun_chemin_d_ordre():
    """Invariant produit, revérifié sur chaque surface nouvellement créée."""
    src = pathlib.Path(
        RACINE / 'vertex' / 'app' / 'routes' / 'company_api.py'
    ).read_text(encoding='utf-8').lower()
    for mot in ('placeorder', 'transmit', 'submit_order', 'buy(', 'sell('):
        assert mot not in src, (
            'la nouvelle surface mentionne « %s »' % mot)
