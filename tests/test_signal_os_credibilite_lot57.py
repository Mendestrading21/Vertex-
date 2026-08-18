"""SIGNAL OS · LOT 57 — LA CRÉDIBILITÉ DU MOTEUR, ET UNE SEPTIÈME CORRECTION.

## D'abord la correction, parce qu'elle change le chantier

L'instrument du lot 55 déclarait **onze moteurs muets**. Sept l'étaient à tort.
Il demandait « la clé est-elle lue par l'écran ? » à des moteurs qui **servent le
corps entier** d'une route et n'en publient donc aucune : la réponse était non
**par construction**. `anomaly`, `evidence_lab`, `decision_stack`,
`session_digest`, `skyler_journal`, `multileg_lab` et `performance` sont peints —
l'interface `fetch` leur route et en affiche le corps.

Septième fois que la même faute se présente dans cette série, et cette fois
**dans l'outil que je venais de livrer comme le fiable**. La bonne question, pour
un moteur sans clé, est : *l'écran demande-t-il cette route ?*

Muets réels : **trois**. Deux sont peints par ce lot.

## Ce que ce lot peint

`/api/skyler/validation` et `/api/skyler/monitor` répondent à la question qui
précède toute confiance dans un verdict : **ce moteur a-t-il été éprouvé, et
tient-il encore ?** Aucun fichier de l'interface ne demandait ces deux routes.

## Le point d'honnêteté, et c'est lui que ces tests gardent

Les deux répondent aujourd'hui `INSUFFICIENT_SAMPLE`, avec leur raison chiffrée
(« 60 séance(s) datée(s) requise(s) ; 0 disponible(s) »). Un échantillon
insuffisant n'est **ni** une validation **ni** un échec : c'est l'absence de
conclusion. L'afficher en vert se lirait « validé » ; en rouge, « le moteur est
cassé ». Ni l'un ni l'autre n'est vrai — d'où un état neutre et la raison
affichée telle que le moteur la donne.
"""
import pytest

ROUTES = ('/api/skyler/validation', '/api/skyler/monitor')

#  Les sept accusés à tort par l'inventaire du lot 55, avec la route que
#  l'interface demande réellement. Mesuré, puis figé : c'est ce qui empêche de
#  refaire le compte faux.
PEINTS_PAR_LEUR_ROUTE = {
    'anomaly': '/api/anomalies/',
    'evidence_lab': '/api/evidence/',
    'decision_stack': '/api/decision/',
    'session_digest': '/api/session/digest',
    'skyler_journal': '/api/skyler/calibration',
    'multileg_lab': '/api/options/strategies/',
}


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('cred57'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.mark.parametrize('route', ROUTES)
def test_le_diagnostic_est_servi_avec_son_contrat(client, route):
    """PREMIÈRE MOITIÉ : la donnée arrive, et elle porte de quoi se dire.

    On n'exige pas `available: true` — le produit a le droit de manquer
    d'échantillon. On exige qu'il DISE dans quel état il est."""
    d = client.get(route).get_json() or {}
    assert d.get('status'), '%s ne publie plus de `status`' % route
    assert d.get('read_only') is True, (
        '%s ne se declare plus en lecture seule' % route)
    assert d.get('reason') or d.get('note'), (
        '%s ne dit plus POURQUOI il est dans cet etat : la page ne pourrait '
        'afficher qu\'un jeton nu' % route)


def test_la_page_systeme_demande_les_deux_routes(client):
    """SECONDE MOITIÉ : la page les demande — et le bloc est APPELÉ.

    L'exigence du site d'appel vient du lot 49 : le CORPS d'une fonction est
    servi qu'elle soit appelée ou non."""
    corps = client.get('/system?view=connections').get_data(as_text=True)
    for route in ROUTES:
        assert route in corps, 'la page Systeme ne demande plus %s' % route
    #  ON VISE LE SITE D'APPEL AVEC SON VOISIN, ET LA MUTATION A DIT POURQUOI.
    #  Première version : `'loadCredibilite()' in corps`. Elle est restée verte
    #  après suppression de l'appel — parce que la chaîne est incluse dans la
    #  DÉFINITION elle-même, `async function loadCredibilite(){`. Quatrième
    #  gardien creux de la série, tous du même genre : une sous-chaîne qui
    #  existe ailleurs. On exige donc l'enchaînement réel des deux appels.
    compact = corps.replace(' ', '').replace('\n', '')
    assert 'loadConnections();loadCredibilite();' in compact, (
        'le bloc de credibilite n\'est plus APPELE au chargement de la vue : sa '
        'fonction reste servie, donc les routes apparaissent dans les octets, '
        'mais l\'ecran ne montre rien')


def test_un_echantillon_insuffisant_n_est_ni_vert_ni_rouge(client):
    """LE TEST QUI PORTE TOUT LE LOT.

    Le libellé de `INSUFFICIENT_SAMPLE` doit dire l'absence de conclusion, et sa
    classe doit être neutre. Le peindre en `vx-pos` le ferait lire « validé » ;
    en `vx-neg`, « cassé ». On vise l'expression exacte de la table — viser un
    fragment voisin a donné trois gardiens creux dans cette série."""
    compact = client.get('/system?view=connections').get_data(as_text=True) \
        .replace(' ', '').replace('\n', '')
    assert ("INSUFFICIENT_SAMPLE:['échantilloninsuffisant—aucuneconclusion',"
            "'vx-muted']") in compact, (
        'l\'etat « echantillon insuffisant » n\'est plus neutre ou ne dit plus '
        'l\'absence de conclusion : il se lira comme une validation ou comme '
        'une panne, et les deux seraient faux')


def test_la_raison_chiffree_du_moteur_est_affichee(client):
    """Un état sans son chiffre serait une opinion. Le moteur donne
    « 60 séance(s) requise(s) ; 0 disponible(s) » — la page le montre."""
    corps = client.get('/system?view=connections').get_data(as_text=True)
    assert 'd.reason||d.note' in corps.replace(' ', ''), (
        'la page n\'affiche plus la raison donnee par le moteur')
    #  La raison vient du serveur ; ce qui vit dans les octets servis, c'est le
    #  RATIO de progression. Le premier rendu affichait les deux et répétait les
    #  mêmes mots — vu à l'écran, corrigé : la raison dit la phrase, le ratio
    #  montre la distance au seuil.
    assert 'required_dated_sessions' in corps, (
        'la page ne lit plus le seuil de seances datees : l\'utilisateur ne '
        'saurait pas ce qui manque pour conclure')
    assert 'progression ' in corps, (
        'le ratio de progression vers le seuil n\'est plus affiche')


@pytest.mark.parametrize('moteur,route', sorted(PEINTS_PAR_LEUR_ROUTE.items()))
def test_le_moteur_sans_cle_est_peint_par_sa_route(moteur, route):
    """LA CORRECTION DU §1, FIGÉE.

    Ces sept moteurs servent le corps entier d'une route : ils n'ont pas de clé,
    donc « la cle est-elle lue ? » leur répondait non par construction. Ce test
    tient le fait qui les rend peints — l'interface demande leur route — pour
    qu'on ne refasse pas le compte faux."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parent.parent
    sources = ''
    for p in list((racine / 'vertex' / 'ui').rglob('*.py')) + \
            list((racine / 'vertex' / 'static' / 'vertex' / 'js').rglob('*.js')):
        sources += p.read_text(encoding='utf-8', errors='replace')
    assert route in sources, (
        '%s sert le corps entier de %s et plus rien ne demande cette route : '
        'il devient reellement muet' % (moteur, route))
