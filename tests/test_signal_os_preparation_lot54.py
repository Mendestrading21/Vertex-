"""SIGNAL OS · LOT 54 — `decision.readiness`, ET UN CINQUIÈME PIÈGE DE NOMMAGE.

`decision_readiness` était classé **« enfermé »** dans l'inventaire du lot 52.
C'était faux, et pour la **cinquième** fois de la même famille : mon balayage
cherchait le **nom du module** dans les corps de réponse. Or ce moteur publie
sous `decision.readiness`, et `walk_forward_validation` sert un corps entier qui
ne se nomme jamais. *Une sonde qui cherche des noms de fichiers dans du JSON
mesure ma convention de nommage, pas le produit.*

Re-mesuré, moteur par moteur, par son APPELANT et par sa CLÉ DE SORTIE :

| moteur | sortie | route | lu par l'UI avant ce lot |
| --- | --- | --- | --- |
| `decision_evidence` | `contexts.data_quality` / `.reconciliation` | `/api/skyler/<sym>` | oui (lot 51) |
| `decision_readiness` | `decision.readiness` | `/api/skyler/<sym>` | **non → ce lot** |
| `walk_forward_validation` | corps entier | `/api/skyler/validation` | non |
| `historical_stress` | `stress_test` | `/api/portfolio/context` | non |
| `option_cohort` | corps entier | `/api/tracking/options/cohort` | non |

**Aucun des cinq n'est enfermé.** Tous atteignent une route servie ; quatre
étaient simplement muets. Le travail restant est de **peindre**, pas
d'**exposer** — bien moins que je ne l'avais annoncé.

## READONLY

Le moteur nomme `actions` une liste d'actes **analytiques** : collecter un
contexte, évaluer une règle. Il porte lui-même `read_only: true` et « ne
constitue jamais une instruction d'exécution ». Un rendu qui laisserait planer
le doute serait un défaut grave dans un produit dont l'invariant est de ne
jamais passer d'ordre. Un test ci-dessous tient cette phrase à l'écran.
"""
import re

import pytest


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('prep54'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.fixture(scope='module')
def reponse(client):
    """Dossier riche : un titre pauvre ferait retomber le moteur et je mesurerais
    mon jeu d'essai (faute du lot 38, payée cinq fois dans cette série)."""
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    closes = [100.0 + i * 0.29 for i in range(240)]
    detail['PREP54'] = {'price': closes[-1], 'closes': closes, 'sector': 'Technology',
                        'series': {'closes': closes}, 'volume': 1500000,
                        'avg_volume': 1000000}
    try:
        return client.get('/api/skyler/PREP54').get_json() or {}
    finally:
        detail.pop('PREP54', None)


def test_readiness_atteint_la_reponse_servie(reponse):
    """PREMIÈRE MOITIÉ : la donnée arrive."""
    r = (reponse.get('decision') or {}).get('readiness')
    assert isinstance(r, dict) and r.get('status'), (
        '`decision.readiness` n\'atteint plus la reponse servie : le bloc '
        'Preparation affichera le vide')
    assert r.get('read_only') is True, (
        'readiness ne se declare plus `read_only` — la clause que la page '
        'affiche ne serait plus fondee sur le moteur')


def test_la_fiche_lit_readiness_ET_appelle_le_bloc(client):
    """SECONDE MOITIÉ : la page le lit — et le bloc est APPELÉ.

    L'exigence du site d'appel vient du lot 49 : retirer `+contextes(d)` du
    rendu y avait laissé huit tests verts, parce que le CORPS d'une fonction est
    servi qu'elle soit appelée ou non."""
    corps = client.get('/analysis/PREP54').get_data(as_text=True)
    assert 'd.readiness' in corps, 'la fiche ne lit plus `decision.readiness`'
    assert '+preparation(d)' in corps.replace(' ', '').replace('\n', ''), (
        'le bloc Preparation n\'est plus APPELE par le rendu : sa fonction est '
        'encore servie, donc les cles apparaissent dans les octets, mais '
        'l\'ecran ne montre rien')


def test_les_quatre_statuts_du_moteur_ont_tous_un_libelle(client):
    """LE TEST QUI ÉVITE UN JETON BRUT À L'ÉCRAN.

    Le rendu traduit `status` par une table. Si le moteur gagne un statut que la
    table ignore, la page affiche un jeton en majuscules — laid, et surtout
    incompréhensible. Les statuts sont LUS DANS LE MOTEUR, pas recopiés ici :
    une liste recopiée diverge dès le premier ajout."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parent.parent
           / 'vertex' / 'engines' / 'decision_readiness.py').read_text(encoding='utf-8')
    statuts = set(re.findall(r"status = '([A-Z_]+)'", src))
    assert statuts, 'aucun statut releve dans le moteur : la lecture a echoue'
    corps = client.get('/analysis/PREP54').get_data(as_text=True)
    absents = sorted(s for s in statuts if s not in corps)
    assert not absents, (
        'le moteur peut rendre %s, que la table de libelles de la fiche ne '
        'traduit pas : l\'ecran afficherait un jeton brut' % ', '.join(absents))


def test_le_bloc_se_declare_descriptif_et_jamais_executif(client):
    """READONLY. Le moteur dit « ne constitue jamais une instruction
    d'exécution » ; le mot « actions » ne doit pas pouvoir se lire comme un
    ordre dans un produit qui n'en passe aucun."""
    corps = client.get('/analysis/PREP54').get_data(as_text=True)
    assert 'jamais une instruction d’exécution' in corps, (
        'la clause qui distingue un diagnostic analytique d\'un ordre a disparu')
    #  Et le rendu ne fabrique aucun verbe d'ordre.
    for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit'):
        assert verbe not in corps, (
            'un verbe d\'ordre (%s) est apparu sur la fiche Analyse' % verbe)


def test_la_troncature_de_la_liste_est_annoncee(client):
    """Une liste coupée en silence ferait croire le dossier plus proche d'être
    complet qu'il n'est. On borne, et on DIT ce qu'on a borné."""
    corps = client.get('/analysis/PREP54').get_data(as_text=True)
    assert 'point(s) d’analyse' in corps, (
        'le compte total des points d\'analyse n\'est plus affiche')
    assert '5 affichés' in corps, (
        'la troncature de la liste n\'est plus annoncee : elle devient '
        'silencieuse, et le dossier parait plus complet qu\'il n\'est')
