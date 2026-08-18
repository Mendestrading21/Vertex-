"""SIGNAL OS · LOT 56 — DIX QUESTIONS HOSTILES, ENFIN AFFICHÉES.

`red_team_review` est une clé de **premier niveau** de la réponse de
`/api/skyler/<sym>` : dix questions adversariales sur le dossier — « qu'est-ce
qui est déjà dans le prix ? », « quel chiffre peut être trompeur ? » — chacune
répondue avec les seules données présentes et assortie de son niveau de preuve.
Personne ne la lisait. C'est l'instrument du lot 55 qui l'a trouvée : le premier
à remonter la chaîne *appelant → clé → route → écran* au lieu de chercher des
noms de modules dans du JSON.

## Le point qui décide de l'honnêteté de ce bloc

Le moteur émet **deux** états, et le second compte plus que le premier :

- `ANSWERED` → `answer` + `evidence_level` ;
- `UNANSWERED` → une `reason`, et **rien d'autre**.

Le moteur le dit lui-même : *« les objections sans preuve restent ouvertes et ne
valident jamais le dossier »*. Une revue qui afficherait les réponses en taisant
les questions ouvertes transformerait une revue incomplète en satisfecit — le
mensonge exact que cette série traque depuis le lot 35. Les questions ouvertes
sont donc rendues **en premier** et comptées à part dans le résumé.

Deux des tests ci-dessous ne servent qu'à cela, et ils fabriquent une question
ouverte au lieu d'attendre qu'il en existe une : le jeu de démonstration répond
aux dix, donc l'état qui compte n'apparaîtrait jamais spontanément.
"""
import pytest


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('rt56'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.fixture(scope='module')
def reponse(client):
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    closes = [100.0 + i * 0.27 for i in range(240)]
    detail['RT56'] = {'price': closes[-1], 'closes': closes, 'sector': 'Technology',
                      'series': {'closes': closes}, 'volume': 1500000,
                      'avg_volume': 1000000}
    try:
        return client.get('/api/skyler/RT56').get_json() or {}
    finally:
        detail.pop('RT56', None)


def test_la_revue_atteint_la_reponse_avec_ses_dix_questions(reponse):
    """PREMIÈRE MOITIÉ : la donnée arrive, et elle est riche."""
    rt = reponse.get('red_team_review') or {}
    qs = rt.get('questions') or []
    assert len(qs) >= 10, (
        'la revue red-team ne publie plus que %d question(s) : le bloc perd sa '
        'matiere' % len(qs))
    assert all(q.get('id') and q.get('question') for q in qs), (
        'une question sans identifiant ou sans enonce : le rendu afficherait '
        'une ligne muette')


def test_la_fiche_lit_la_revue_ET_appelle_le_bloc(client):
    """SECONDE MOITIÉ : la page la lit — et le bloc est APPELÉ. L'exigence du
    site d'appel vient du lot 49, où retirer le câblage laissait huit tests
    verts parce que le CORPS d'une fonction est servi qu'elle soit appelée ou
    non."""
    corps = client.get('/analysis/RT56').get_data(as_text=True)
    assert 'red_team_review' in corps, 'la fiche ne lit plus `red_team_review`'
    assert '+revueAdversariale(r)' in corps.replace(' ', '').replace('\n', ''), (
        'le bloc de revue adversariale n\'est plus APPELE par le rendu : sa '
        'fonction reste servie, donc la cle apparait dans les octets, mais '
        'l\'ecran ne montre rien')


def test_une_question_ouverte_est_rendue_comme_ouverte():
    """L'ÉTAT QUI COMPTE, FABRIQUÉ PARCE QU'IL N'ARRIVE PAS TOUT SEUL.

    Le jeu de démonstration répond aux dix questions. Attendre qu'une reste
    ouverte, c'est ne jamais tester la branche qui empêche un satisfecit. On
    appelle donc le moteur sur un packet vide : ses questions sortent
    `UNANSWERED`, avec une raison et sans réponse."""
    from vertex.engines import red_team
    revue = red_team.review({}, {})
    ouvertes = [q for q in revue['questions'] if q['status'] != 'ANSWERED']
    assert ouvertes, (
        'un packet vide ne produit plus aucune question ouverte : le moteur '
        'comblerait donc les absences, ce qu\'il s\'interdit')
    for q in ouvertes:
        assert q.get('reason'), (
            'la question ouverte %s ne dit pas POURQUOI elle l\'est : la fiche '
            'ne pourrait afficher qu\'un blanc' % q['id'])
        assert 'answer' not in q, (
            'la question ouverte %s porte une reponse : une objection sans '
            'preuve serait presentee comme traitee' % q['id'])
    assert revue['complete'] is False


def test_le_rendu_distingue_les_deux_etats_et_compte_les_ouvertes(client):
    """LE GARDIEN DU MENSONGE POSSIBLE. On vise l'expression exacte qui trie les
    questions ouvertes, et la mention qui les compte à part — pas une occurrence
    voisine, faute déjà commise trois fois dans cette série."""
    compact = client.get('/analysis/RT56').get_data(as_text=True) \
        .replace(' ', '').replace('\n', '')
    assert "q.status!=='ANSWERED'" in compact, (
        'le rendu ne separe plus les questions ouvertes des questions '
        'repondues : une revue incomplete se lirait comme complete')
    assert 'ouverte(s),jamaiscomblée(s)' in compact, (
        'le resume ne compte plus les questions ouvertes a part')


def test_la_revue_est_annoncee_descriptive(client):
    """Dix questions sous un verdict se liraient comme un second verdict si
    rien ne disait qu'elles sont descriptives."""
    corps = client.get('/analysis/RT56').get_data(as_text=True)
    assert 'descriptive, lecture seule' in corps, (
        'la mention descriptive a disparu — la revue peut etre lue comme un '
        'verdict concurrent')
