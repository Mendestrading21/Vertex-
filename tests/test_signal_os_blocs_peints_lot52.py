"""SIGNAL OS · LOT 52 — LE PIXEL, ET L'INVENTAIRE CORRIGÉ.

Ce lot paie une réserve que j'avais écrite moi-même dans SIGNAL-OS-49 §5.2 :

> Le rendu n'est pas vérifié au navigateur : le gardien prouve que le câblage
> existe et que la donnée arrive, **pas que le pixel s'affiche**.

La vérification au navigateur vit dans `tools/mesurer_blocs_peints.py` — elle
exige Chromium et un serveur, que l'intégration continue n'a pas. Ce fichier
tient donc ce qui se tient **sans navigateur**, et rien de plus : prétendre
autrement serait exactement le genre de gardien creux que cette série corrige
depuis le lot 35.

## Ce que la mesure au navigateur a trouvé, et que ces tests protègent

`#an-skyler` portait **2 426 caractères de `textContent` pour zéro de
`innerText`**, dans une chaîne d'ancêtres tous `display:block` et
`visibility:visible`. Rien n'était masqué : les trois blocs vivent **deux
`<details>` en profondeur** (`an-deep-analysis`, puis « Contextes du dossier »).
C'est un choix assumé — la source le dit : *« Expertise à la demande […] leurs
sorties secondaires ne concurrencent plus le verdict canonique »* — mais c'est
un fait de structure dont dépend tout le chemin de peinture. S'il change sans
qu'on le veuille, les blocs deviennent inatteignables sans qu'aucun test des
lots 49-51 ne bronche : eux lisent les octets servis, où le contenu est présent
qu'il soit révélé ou non.

## L'inventaire du §4, faux de quinze sur vingt

SIGNAL-OS-49 §4 nommait **vingt** moteurs « n'atteignant aucune réponse
servie ». Mesuré ici : **cinq**. Les douze premiers sortent dans
`packet.contexts` sous des clés plus courtes — `drawdown_context` publie
`contexts.drawdown` — et trois autres sortent dans `decision` (corrigés au
lot 50). C'est la **quatrième** fois dans cette série qu'une hypothèse de
nommage me trompe ; d'où un test qui fige la correspondance module → clé au
lieu de la laisser à ma mémoire.

Ce test a un second effet, plus utile que le premier : le bloc générique du
lot 51 lit `packet.contexts` **en entier**. Renommer une clé n'y casse rien
visiblement — la ligne disparaît, en silence. Nommer les douze, c'est rendre
cette disparition bruyante.
"""
import re

import pytest

#  Mesuré sur la réponse réelle, pas déduit du code : nom de module tel que le
#  §4 le nommait → clé réellement publiée par le packet.
CORRESPONDANCE = {
    'relative_volume_context': 'relative_volume',
    'relative_strength_context': 'relative_strength',
    'iv_skew_context': 'iv_skew',
    'iv_term_structure': 'iv_term_structure',
    'open_interest_concentration': 'open_interest_concentration',
    'earnings_proximity': 'earnings_proximity',
    'gap_risk_context': 'gap_risk',
    'drawdown_context': 'drawdown',
    'downside_volatility': 'downside_volatility',
    'fundamental_context': 'fundamentals',
    'anomaly_context': 'anomalies',
    'call_put_structure': 'call_put_structure',
}

#  Les seuls réellement enfermés — mesurés sur les **162 routes GET servies**,
#  témoin à l'appui (deux moteurs connus sortants retrouvés ; sans eux la sonde
#  aurait rendu « aveugle » plutôt qu'un inventaire flatteur).
#
#  Le CHEMIN est mesuré, pas deviné : ma première version cherchait ces modules
#  sous une liste de préfixes de mon cru et en manquait deux. Le fait qu'elle
#  révèle est plus intéressant que le test lui-même — `historical_stress` vit
#  dans `vertex/portfolio/` et `option_cohort` dans `vertex/tracking/`. Ce ne
#  sont pas des moteurs par titre : ils n'ont rien à faire sur
#  `/api/skyler/<sym>`, et les exposer demandera une route de portefeuille ou
#  de suivi, pas une ligne de plus sur la fiche Analyse.
ENFERMES = {
    'decision_evidence': 'vertex/engines/decision_evidence.py',
    'decision_readiness': 'vertex/engines/decision_readiness.py',
    'walk_forward_validation': 'vertex/engines/walk_forward_validation.py',
    'historical_stress': 'vertex/portfolio/historical_stress.py',
    'option_cohort': 'vertex/tracking/option_cohort.py',
}


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('peints52'))
    import terminal
    yield terminal.app.test_client()
    persist._BASE_DIR = sauve


@pytest.fixture(scope='module')
def contextes(client):
    """Un dossier RICHE. Un titre pauvre ferait retomber les moteurs et je
    mesurerais mon jeu d'essai — la faute du lot 38, déjà payée quatre fois."""
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    closes = [100.0 + i * 0.31 for i in range(240)]
    detail['PNT52'] = {'price': closes[-1], 'closes': closes, 'sector': 'Technology',
                       'series': {'closes': closes}, 'volume': 1500000,
                       'avg_volume': 1000000}
    try:
        rep = client.get('/api/skyler/PNT52').get_json() or {}
    finally:
        detail.pop('PNT52', None)
    return ((rep.get('packet') or {}).get('contexts') or {})


@pytest.mark.parametrize('module,cle', sorted(CORRESPONDANCE.items()))
def test_le_moteur_sort_bien_sous_sa_cle_de_packet(contextes, module, cle):
    """LA CORRESPONDANCE, FIGÉE. Le §4 déclarait ces douze « enfermés » parce
    que je les cherchais par nom de module. Ils sortent tous."""
    assert cle in contextes, (
        '%s ne publie plus `contexts.%s` : le bloc generique du lot 51 perd '
        'sa ligne EN SILENCE — il lit la table entiere, une cle absente ne '
        'lui arrache aucune erreur' % (module, cle))


def test_les_contextes_du_packet_ne_retrecissent_pas(contextes):
    """Borne mesurée. Le rendu générique vaut par sa matière."""
    assert len(contextes) >= 21, (
        'le packet ne publie plus que %d contextes (21 mesures au lot 52)'
        % len(contextes))


def test_les_blocs_vivent_derriere_la_disclosure_mesuree(client):
    """LE FAIT DE STRUCTURE QUE SEUL LE NAVIGATEUR A MONTRÉ.

    `#an-skyler` est dans `<details id="an-deep-analysis">`. Tant que c'est
    vrai, le chemin de peinture est : ouvrir « Analyse approfondie », puis
    « Contextes du dossier ». Les gardiens des lots 49-51 ne peuvent pas le
    voir — ils lisent les octets servis, où le contenu est present qu'il soit
    revele ou non. Si cette structure change, `tools/mesurer_blocs_peints.py`
    doit changer avec elle, sinon il rendra 2 (aveugle) sans qu'on sache
    pourquoi."""
    corps = client.get('/analysis/PNT52').get_data(as_text=True)
    ouverture = corps.find('<details class="vx-card an-disclosure vx-mt4" '
                           'id="an-deep-analysis">')
    assert ouverture > 0, (
        'la disclosure `an-deep-analysis` a change de forme : le chemin '
        'd\'ouverture mesure au lot 52 n\'est plus valide')
    hote = corps.find('id="an-skyler"')
    assert hote > ouverture, (
        '`#an-skyler` n\'est plus dans `an-deep-analysis` : le chemin de '
        'peinture a change')
    #  La disclosure ne doit pas être ouverte d'office : ce serait un autre
    #  produit (les sorties secondaires concurrenceraient le verdict).
    entete = corps[ouverture:ouverture + 200]
    assert not re.search(r'\bopen\b', entete), (
        'la disclosure est desormais ouverte par defaut — decision de produit, '
        'a assumer explicitement, pas a subir')


@pytest.mark.parametrize('nom,chemin', sorted(ENFERMES.items()))
def test_le_moteur_enferme_est_toujours_recense(nom, chemin):
    """Le reste du gisement, tenu par son chemin. Ce test ne demande pas que le
    moteur SORTE — il n'y est pas encore. Il demande qu'il soit encore LÀ, pour
    qu'on ne perde pas la trace des cinq derniers en croyant le chantier fini."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parent.parent
    assert (racine / chemin).is_file(), (
        '%s n\'est plus a %s : soit il a ete supprime, soit il a ete deplace. '
        'Dans les deux cas la liste des cinq moteurs restant a exposer '
        '(SIGNAL-OS-52 §3) est perimee' % (nom, chemin))
