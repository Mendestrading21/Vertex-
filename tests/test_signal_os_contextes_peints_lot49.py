"""SIGNAL OS · LOT 49 — TROIS MOTEURS CALCULÉS, ENVOYÉS, JAMAIS PEINTS.

La fusion de `main` a apporté 34 moteurs neufs (+8 056 lignes). Mesuré ensuite :
**aucune** de leurs sorties n'était lue par l'interface — 23 clés cherchées dans
`vertex/ui/**` et `vertex/static/**/js/`, 23 fois zéro.

Trois d'entre eux atteignaient pourtant déjà la réponse de `/api/skyler/<sym>`,
sous `decision.regime_break`, `.sector_coherence` et `.instrument_profile`.
C'est le motif du dossier 454, en toutes lettres : *une conséquence CALCULÉE,
SÉRIALISÉE et ENVOYÉE n'est toujours pas AFFICHÉE*.

Ce gardien tient les deux moitiés du contrat :

1. **la chaîne existe** — les trois clés sont bien dans la réponse servie ;
2. **elle est peinte** — la page lit les trois, et le dit descriptif.

Sans la première, la seconde pourrait passer sur une page qui affiche trois
lignes vides. Sans la seconde, on retomberait dans le défaut du 454.
"""
import re

import pytest

CLES = ('regime_break', 'sector_coherence', 'instrument_profile')


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('ctx49'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.mark.parametrize('cle', CLES)
def test_le_moteur_atteint_bien_la_reponse_servie(client, cle):
    """PREMIÈRE MOITIÉ : la donnée arrive. Sans elle, peindre ne sert à rien."""
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    sauve = detail.get('CTX49')
    detail['CTX49'] = {'price': 100.0, 'closes': [90.0 + i for i in range(120)],
                       'series': {'closes': [90.0 + i for i in range(120)]}}
    try:
        rep = client.get('/api/skyler/CTX49').get_json() or {}
    finally:
        if sauve is None:
            detail.pop('CTX49', None)
        else:
            detail['CTX49'] = sauve
    decision = rep.get('decision') or {}
    assert cle in decision, (
        '%s n\'atteint plus la reponse de /api/skyler : la page qui le peint '
        'affichera une ligne vide' % cle)


@pytest.mark.parametrize('cle', CLES)
def test_la_fiche_lit_le_moteur(client, cle):
    """SECONDE MOITIÉ : la page le lit. C'est ce qui manquait."""
    corps = client.get('/analysis/CTX49').get_data(as_text=True)
    assert cle in corps, (
        'la fiche Analyse ne lit plus %s — le moteur redevient calcule, '
        'serialise, envoye et jamais peint (motif du dossier 454)' % cle)


def test_le_bloc_de_contexte_est_APPELE_et_pas_seulement_present(client):
    """LE TEST QUI MANQUAIT, ET J'AI FAILLI NE PAS LE VOIR.

    Première version de ce gardien : il vérifiait que la chaîne `regime_break`
    est servie. Elle l'est — dans le CORPS de la fonction `contextes()`, servie
    qu'elle soit appelée ou non. Contre-épreuve : j'ai retiré `+contextes(d)`
    du rendu, c'est-à-dire le câblage lui-même, et **les huit tests sont restés
    verts**. Le gardien mesurait la présence d'un texte, pas l'existence d'un
    appel — exactement la faute que cette série corrige depuis le lot 35.

    Ici on exige le SITE D'APPEL dans le rendu."""
    corps = client.get('/analysis/CTX49').get_data(as_text=True)
    sans_espaces = corps.replace(' ', '').replace('\n', '')
    assert '+contextes(d)' in sans_espaces, (
        'le bloc de contexte n\'est plus APPELE par le rendu de la decision : '
        'sa fonction est encore servie, donc les clés apparaissent dans les '
        'octets, mais l\'ecran ne montre rien')


def test_les_contextes_sont_annonces_descriptifs(client):
    """Les trois moteurs portent `does_not_change_decision` / « ne modifie ni le
    score ni le verdict ». La page doit le DIRE : trois lignes chiffrées sous un
    verdict se lisent sinon comme un second verdict."""
    corps = client.get('/analysis/CTX49').get_data(as_text=True)
    assert 'ne modifie ni le score ni le verdict' in corps, (
        'la mention descriptive a disparu — les contextes peuvent etre lus '
        'comme un verdict concurrent')


def test_l_etat_indisponible_montre_la_raison_du_moteur(client):
    """ÉTAT HONNÊTE. Quand un moteur dit `available: false`, la page montre sa
    RAISON — jamais un tiret muet, jamais un chiffre de remplissage."""
    corps = client.get('/analysis/CTX49').get_data(as_text=True)
    #  Les trois branches d'indisponibilité lisent le champ du moteur.
    for motif in (r'rb\.reason', r'sc\.reason', r'ip\.classification_source'):
        assert re.search(motif, corps), (
            'la branche indisponible de %s ne lit plus la raison du moteur' % motif)


#  ─── LOT 50 : trois moteurs de plus, trouvés en re-mesurant ────────────────
#  Mon premier sondage les avait déclarés absents de la réponse. Il utilisait
#  un titre trop pauvre — clôtures plates, aucune date. Avec un historique
#  réaliste, `multi_asset_guard`, `opportunity_attribution` et
#  `opportunity_reliability` ressortent. Le sondage mesurait la pauvreté de
#  mon jeu d'essai, pas le produit.
CLES_50 = ('multi_asset_guard', 'opportunity_attribution', 'opportunity_reliability')


@pytest.mark.parametrize('cle', CLES_50)
def test_le_moteur_de_fiabilite_atteint_la_reponse(client, cle):
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    sauve = detail.get('CTX50')
    closes = [100.0 + i * 0.4 for i in range(200)]
    detail['CTX50'] = {'price': closes[-1], 'closes': closes, 'sector': 'Technology',
                       'series': {'closes': closes}}
    try:
        rep = client.get('/api/skyler/CTX50').get_json() or {}
    finally:
        if sauve is None:
            detail.pop('CTX50', None)
        else:
            detail['CTX50'] = sauve
    assert cle in (rep.get('decision') or {}), (
        '%s n\'atteint plus la reponse servie' % cle)


@pytest.mark.parametrize('cle', CLES_50)
def test_la_fiche_lit_le_moteur_de_fiabilite(client, cle):
    corps = client.get('/analysis/CTX50').get_data(as_text=True)
    assert cle in corps, 'la fiche ne lit plus %s' % cle


def test_le_bloc_de_fiabilite_est_APPELE(client):
    """Même exigence qu'au lot 49 : le SITE D'APPEL, pas la simple présence du
    corps de la fonction. C'est la mutation du 49 qui a montré la différence."""
    corps = client.get('/analysis/CTX50').get_data(as_text=True)
    assert '+fiabilite(d)' in corps.replace(' ', '').replace('\n', ''), (
        'le bloc de fiabilite n\'est plus appele par le rendu de la decision')


def test_ce_qui_manque_au_score_est_annonce(client):
    """Ce bloc est celui qui transforme un « 12/40 » opaque en actionnable."""
    corps = client.get('/analysis/CTX50').get_data(as_text=True)
    assert 'Ce qui manque au score' in corps
    #  On cherche un fragment NON COUPÉ. Le libellé est bâti par concaténation
    #  dans la source (`'… explique le '+'verdict, ne le remplace pas'`) : la
    #  phrase entière n'existe qu'après évaluation, pas dans les octets servis.
    #  Chercher la phrase complète, c'était tester ma mise en page, pas la règle.
    assert 'ne le remplace pas' in corps, (
        'la clause descriptive a disparu — la fiabilite peut se lire comme un '
        'second verdict')
