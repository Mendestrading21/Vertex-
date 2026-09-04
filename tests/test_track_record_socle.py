"""Vertex Test 1.0 · #783/G3 — LE MOTEUR NE SE NOTAIT PAS.

`RELEASE_GATES.md` G3 : *« … et la mémoire des résultats est exploitable sans
look-ahead »*. La seconde moitié n'a de sens que si la première tient : encore
faut-il que la mémoire produise **quelque chose**.

## Le défaut, mesuré

`track_record._fwd` cherchait un libellé `'%m-%d'` dans `series['dates']`, qui
contient des dates **ISO**. `'05-15' in ['2026-05-15', …]` est toujours faux :
`.index()` levait `ValueError` sur **chaque** entrée, et `evaluate()` rendait
`resolved: 0` quoi qu'il arrive.

```text
avant : 8 entrées, +1 / +5 / +20 tous échus  ->  0 résolue
après : 8 entrées, mêmes horizons            ->  8 résolues
```

`vertex/engines/analysis.py` fournit **les deux** formats — `dates` en ISO et
`date_labels` en `%m-%d` — avec un commentaire qui dit pourquoi : « afin de ne
jamais réinterpréter les années ». La fonction lisait le mauvais champ.

## Pourquoi il a survécu : un test vert au-dessus

`tests/test_track_record.py` fournissait `dates = ['08-01', …]`. Ce format
n'est **produit nulle part** dans le produit. Le test validait donc un chemin
qui n'existe pas en production, et il passait — ce qui rendait le défaut
invisible à la suite entière. Sa fixture reproduit désormais le format réel.

C'est la leçon la plus transférable de ce lot : **une fixture qui ne ressemble
pas à la production ne teste pas la production**, et un test vert au-dessus d'un
défaut est pire que pas de test — il en interdit la découverte.

## Ce que l'écran disait pendant ce temps

« Pas encore assez de verdicts résolus … **Le registre se remplit à chaque
scan** » — c'est-à-dire « patience ». Pour une condition qui ne pouvait jamais
se résoudre. `evaluate()` détaille désormais **pourquoi** chaque entrée n'est
pas notée, et l'écran sert ce détail.

## La restriction aux survivants, maintenant dite

Une entrée n'est notée que si son titre est **encore dans le scan du jour** :
c'est de là que viennent les séries de prix. Un verdict sur un titre sorti de
l'univers n'est jamais compté. La fiabilité affichée porte donc sur les
**survivants** — ce n'est pas corrigeable sans historique de prix pour les
titres sortis, mais c'est disable, et c'est désormais dans la note servie.
"""
import datetime
import pathlib
import sys

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from tools.mesures import mesurer_track_record as _mes  # noqa: E402

from vertex.engines import track_record as tr  # noqa: E402


@pytest.fixture(scope='module')
def mesure():
    return _mes.mesurer()


def test_le_moteur_se_note_vraiment(mesure):
    """LE CŒUR DU LOT. 8 entrées dont tous les horizons sont échus doivent
    produire 8 résolutions — pas 0."""
    e = mesure['horizons_echus']
    assert e['resolus'] == e['attendu'], (
        'le moteur ne se note pas : %d entrees resolues sur %d dont +1, +5 et '
        '+20 sont TOUS echus. Verifier que `_fwd` compare bien des dates ISO.'
        % (e['resolus'], e['attendu']))
    assert e['verdicts'], 'aucun bucket de verdict publie malgre n >= 5'


def test_aucun_look_ahead(mesure):
    """LA PROPRIÉTÉ DE G3. Une entrée dont aucun horizon n'est échu ne doit
    jamais être notée — sinon la fiabilité affichée serait celle des seuls
    verdicts assez vieux pour avoir eu raison."""
    t = mesure['horizons_non_echus']
    assert t['resolus'] == 0, (
        '%d entrees notees alors qu\'aucun horizon n\'est echu : la fiabilite '
        'servie est gonflee par du look-ahead' % t['resolus'])


def test_le_look_ahead_est_refuse_HORIZON_PAR_HORIZON():
    """Plus précis que le test ci-dessus, et c'est ce qui compte : `+1` peut
    être échu quand `+20` ne l'est pas. Chaque horizon doit être refusé
    séparément, pas en bloc."""
    serie = _mes._serie(datetime.date(2026, 5, 1))
    closes, dates = serie['close'], serie['dates']
    dernier = len(dates) - 1

    #  À J-3 de la fin : +1 est échu, +5 et +20 ne le sont pas.
    jour = dates[dernier - 3]
    f1, _ = tr._fwd(closes, dates, jour, 1)
    f5, _ = tr._fwd(closes, dates, jour, 5)
    f20, _ = tr._fwd(closes, dates, jour, 20)
    assert f1 is not None, '+1 seance echue et pourtant non calculee'
    assert f5 is None and f20 is None, (
        'un horizon NON echu a rendu une valeur : %s / %s' % (f5, f20))

    #  Sur la dernière séance, même +1 est hors d'atteinte.
    f1, i = tr._fwd(closes, dates, dates[dernier], 1)
    assert f1 is None and i == dernier, (
        'la derniere seance rend un rendement futur : %s' % f1)


def test_une_seance_absente_se_distingue_d_un_horizon_non_echu():
    """`(None, None)` = séance introuvable ; `(None, i)` = horizon pas encore
    échu. Confondre les deux, c'est perdre la cause exacte — et c'est justement
    ce qui a permis à `resolved: 0` de passer pour un manque d'historique."""
    serie = _mes._serie(datetime.date(2026, 5, 1))
    absent, i = tr._fwd(serie['close'], serie['dates'], '1999-01-04', 1)
    assert absent is None and i is None
    #  Et le format court, celui d'AVANT, doit rester introuvable : le champ
    #  `date_labels` existe pour l'affichage, jamais pour la jointure.
    court, j = tr._fwd(serie['close'], serie['dates'], serie['date_labels'][10], 1)
    assert court is None and j is None, (
        'la jointure accepte de nouveau un libelle court : l\'annee redevient '
        'ambigue, et deux annees se confondraient sur la meme date')


def test_evaluate_dit_POURQUOI_une_entree_n_est_pas_notee():
    """Sans cette ventilation, `resolved: 0` se lit « pas assez d'historique »
    quelle que soit la cause réelle."""
    non_echu = _mes._evaluer(_mes.SEANCES - 1)
    assert non_echu['ignores']['horizon_non_echu'] == _mes.ENTREES
    assert non_echu['ignores']['sans_serie'] == 0

    hors_univers = _mes._evaluer(10, symbole_serie='BBB')
    assert hors_univers['ignores']['sans_serie'] == _mes.ENTREES, (
        'un verdict sur un titre qui a quitte l\'univers n\'est plus compte '
        'comme tel : la cause du vide redevient indiscernable')

    normal = _mes._evaluer(10)
    assert sum(normal['ignores'].values()) == 0


def test_la_note_avoue_la_restriction_aux_survivants():
    """La fiabilité ne porte que sur les titres encore suivis. Ne pas le dire
    laisserait croire à une mesure sur l'ensemble des verdicts émis."""
    note = _mes._evaluer(10)['note']
    assert 'survivants' in note.lower(), (
        'la note servie ne dit plus que la fiabilite porte sur les seuls '
        'titres encore suivis : %r' % note)
    assert 'CLÔTURES' in note, 'la methode approximative n\'est plus dite'


def test_l_ecran_n_invite_plus_a_patienter_sans_raison():
    """L'ancien message promettait que « le registre se remplit à chaque scan ».
    Il l'a promis pendant que la jointure était cassée."""
    src = RACINE.joinpath('vertex/ui/pages/performance_page.py').read_text(
        encoding='utf-8')
    assert 'Le registre se remplit à chaque scan' not in src, (
        'l\'ecran invite de nouveau a patienter, sans savoir si la condition '
        'peut seulement se resoudre')
    assert 'tr.ignores' in src, (
        'l\'ecran ne sert plus le detail des entrees non notees')


def test_la_fixture_historique_ressemble_a_la_production():
    """Le test qui couvrait ce code fournissait des dates `'08-01'`, format que
    `analysis.py` ne produit jamais. Un test vert au-dessus d'un défaut en
    interdit la découverte."""
    src = RACINE.joinpath('tests/test_track_record.py').read_text(
        encoding='utf-8')
    assert "dates = ['08-01'" not in src, (
        'la fixture est revenue au format court : elle testerait de nouveau un '
        'chemin qui n\'existe pas en production')
    src_analyse = RACINE.joinpath('vertex/engines/analysis.py').read_text(
        encoding='utf-8')
    assert "'dates': [d.date().isoformat() for d in cc.index]" in src_analyse, (
        'le producteur des series a change de format : la jointure du track '
        'record doit suivre')


def test_les_temoins_de_l_instrument_mordent(mesure):
    """Un détecteur qui ne trouve rien ne prouve rien. Le témoin négatif de cet
    instrument avait « passé » pendant tout le temps où la jointure était
    cassée : rien ne se résolvait, donc rien ne pouvait se résoudre à tort."""
    assert _mes._temoins(mesure) == []


def test_aucun_chemin_d_ordre():
    src = RACINE.joinpath('vertex/engines/track_record.py').read_text(encoding='utf-8')
    for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit'):
        assert verbe not in src
