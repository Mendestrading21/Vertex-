"""SIGNAL OS · LOT 41 — AUCUN EMOJI DANS LE CODE VIVANT DES PAGES SERVIES.

`COPY.md` interdit « l'emoji comme ponctuation de produit » ; `VISUAL_SYSTEM.md`
impose « une seule famille outline » et proscrit les icônes multicolores — un
emoji l'est par nature, aucun token ne peut le repeindre.

## Ce que la mesure a trouvé, et pourquoi elle a failli le rater

Un relevé navigateur des huit pages d'accueil ne peignait que deux signes
(`→`, `⌘`) et **aucun emoji**. Conclusion tentante, et fausse : deux emoji
(🚀, 🔒) vivaient sur `/analysis/<sym>`, dans une branche qui ne s'ouvre que si
la donnée remplit la condition (compression Bollinger/Keltner). L'état
d'accueil est l'état le plus pauvre du produit ; le mesurer seul et appeler ça
une couverture, c'est la faute du lot 38 sous un nouveau déguisement.

Ce gardien n'a pas besoin d'un navigateur : il interroge les pages servies et
regarde le **code vivant**, commentaires retirés. Un emoji dans du code vivant
est soit peint, soit du code mort — les deux méritent d'échouer.

## Ce qu'il ne prétend pas

Il ne juge pas les commentaires servis : ils documentent précisément pourquoi
tel pictogramme a été retiré, et les effacer perdrait la raison. Il ne juge pas
non plus les signes de casseau (`⚠`, `✕`, `✓`, `→`) : ce ne sont pas des emoji,
ils sont monochromes et prennent la couleur du texte.
"""
import re

import pytest

#  Emoji au sens de la règle : plan astral (multicolore par nature) plus les
#  quelques caractères anciens qui reçoivent une présentation emoji.
_EMOJI = re.compile('[\U0001F300-\U0001FAFF✅❌⬛⬜]')

#  Les huit espaces, tels que `redesign.py` les route.
PAGES = ('/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system')

_BLOC = re.compile(r'/\*.*?\*/', re.S)


def sans_commentaires(html):
    """Retire les commentaires de bloc `/* … */` — c'est là que vivent les
    explications qui CITENT un pictogramme retiré, et elles ont le droit d'y
    vivre. Les `//` ne sont pas retirés : une URL en contient, et sur-filtrer
    rendrait le gardien aveugle bien au-delà de son objet."""
    return _BLOC.sub(' ', html)


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('picto'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.mark.parametrize('chemin', PAGES)
def test_aucun_emoji_dans_le_code_vivant_des_huit_espaces(client, chemin):
    corps = client.get(chemin).get_data(as_text=True)
    assert corps, 'page vide — test sans objet'
    trouves = sorted(set(_EMOJI.findall(sans_commentaires(corps))))
    assert not trouves, (
        '%s sert %d emoji dans du code vivant : %s — interdit par COPY.md '
        '(ponctuation) et VISUAL_SYSTEM.md (famille unique, pas de '
        'multicolore)' % (chemin, len(trouves), ' '.join(trouves)))


def test_la_fiche_d_un_titre_en_compression_ne_peint_plus_d_emoji(client):
    """LA BRANCHE QUI AVAIT ÉCHAPPÉ AU BALAYAGE.

    On ouvre la condition au lieu d'espérer qu'elle s'ouvre : sans cet état,
    le test passerait sans jamais atteindre la ligne qu'il garde."""
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    sauve = detail.get('PIC41')
    detail['PIC41'] = {'price': 100.0, 'ttm_squeeze': True, 'ttm_fired': False,
                       'ttm_dir': 'up', 'closes': [90.0 + i for i in range(60)]}
    try:
        corps = client.get('/analysis/PIC41').get_data(as_text=True)
    finally:
        if sauve is None:
            detail.pop('PIC41', None)
        else:
            detail['PIC41'] = sauve
    assert 'compression' in corps, (
        'la branche TTM ne se rend plus — le test ne garde plus rien')
    trouves = sorted(set(_EMOJI.findall(sans_commentaires(corps))))
    assert not trouves, (
        'la fiche d\'un titre en compression sert %s dans du code vivant'
        % ' '.join(trouves))


def test_la_severite_d_alerte_n_est_plus_comparee_a_un_pictogramme():
    """DÉFAUT RÉEL ÉVITÉ, pas seulement une question de style.

    Le serveur transporte la sévérité d'alerte comme un emoji. L'ancienne
    lecture comparait la chaîne entière ; un sélecteur de variante (U+FE0F)
    ajouté en amont aurait rendu l'égalité fausse EN SILENCE — une alerte de
    danger peinte en jaune. La comparaison porte désormais sur le point de
    code du caractère de base."""
    import pathlib
    src = pathlib.Path('vertex/ui/pages/briefing.py').read_text(encoding='utf-8')
    vivant = sans_commentaires(src)
    assert 'codePointAt(0)===ROUGE' in vivant.replace(' ', ''), (
        'la severite n\'est plus lue par point de code — verifier qu\'elle '
        'n\'est pas revenue a une egalite de chaine sur un emoji')
    assert not _EMOJI.search(vivant), (
        'un emoji est revenu dans le code vivant de la page Aujourd\'hui')
