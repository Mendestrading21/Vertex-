"""Vertex Test 1.0 — LE PRODUIT OFFRAIT UNE ÉCHÉANCE DE 30 JOURS SANS DIRE QU'ELLE EST HORS DOCTRINE.

## Ce qui a été vu

`/api/strategie` sert six échéances, de **30 à 365 jours** :

```text
1 mois 30 · 2 mois 60 · 3 mois 90 · 6 mois 180 · 9 mois 270 · 12 mois 365
```

La constitution active (v4) déclare, elle : **bande préférée 120–240, cible
180**. Rien à l'écran ne reliait les deux. Un lecteur choisissait « 1 mois »
sans savoir qu'il se plaçait **150 jours** sous la cible que le reste du
produit applique.

## Ce qui n'est PAS le défaut

Offrir une échelle et en préférer un point sont deux choses différentes, et
retirer les autres échéances serait une perte. Le défaut était le **silence**.

## La correction

`horizons_annotes()` lit la bande dans `release.etat_actif()` **à chaque
appel** et pose sur chaque échéance : `dans_la_bande`, `est_la_cible`,
`ecart_a_la_cible`.

Dérivé, jamais recopié. Une copie de la bande dans l'adaptateur finirait par
annoncer autre chose que ce que les moteurs appliquent — le défaut de D-084,
et la raison pour laquelle `R` est importé du moteur plutôt que redéclaré.

## Le cas qui compte le plus

Sans constitution active — entrée directe par `terminal.py`, mode de repli —
`dans_la_bande` vaut **`None`**, jamais `False`. « Je ne sais pas » et
« déconseillé par la doctrine » sont deux affirmations différentes, et
confondre les deux est exactement ce que la règle n°4 interdit.

## Au passage

`SIZING` portait deux couleurs **en dur** : `#EF4444` et `#FFB23F` — ce
dernier appartenant à la palette Obsidian Copper abandonnée. Un moteur qui
impose une couleur impose une palette. Remplacées par un `ton` sémantique.
"""
from __future__ import annotations

import os

import pytest

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('START_ON_IMPORT', '0')

from vertex.strategy import legacy_adapter as A  # noqa: E402


#  ═══════════  1. chaque échéance se situe par rapport à la doctrine  ═════════

def test_chaque_echeance_dit_si_la_doctrine_la_recommande():
    r = A.horizons_annotes()
    assert len(r['horizons']) == len(A.HORIZONS)
    for h in r['horizons']:
        assert 'dans_la_bande' in h
        assert 'est_la_cible' in h
        assert 'ecart_a_la_cible' in h


def test_l_echelle_ENTIERE_est_conservee():
    """Contre-épreuve : annoter ne doit rien retirer. Un correctif qui
    amputerait l'échelle pour la rendre conforme serait pire que le silence
    qu'il corrige."""
    r = A.horizons_annotes()
    assert [h['dte'] for h in r['horizons']] == [h['dte'] for h in A.HORIZONS]
    assert [h['key'] for h in r['horizons']] == [h['key'] for h in A.HORIZONS]


def test_une_seule_echeance_est_LA_CIBLE(monkeypatch):
    _bande(monkeypatch, [120, 240], 180)
    cibles = [h for h in A.horizons_annotes()['horizons'] if h['est_la_cible']]
    assert len(cibles) == 1 and cibles[0]['dte'] == 180


def test_les_echeances_courtes_sont_dites_HORS_bande(monkeypatch):
    """Le cœur : 30 jours, c'est 150 jours sous la cible, et cela doit se
    lire."""
    _bande(monkeypatch, [120, 240], 180)
    par_dte = {h['dte']: h for h in A.horizons_annotes()['horizons']}
    assert par_dte[30]['dans_la_bande'] is False
    assert par_dte[30]['ecart_a_la_cible'] == -150
    assert par_dte[180]['dans_la_bande'] is True


def test_les_bornes_de_la_bande_sont_INCLUSES(monkeypatch):
    """Une borne exclue retirerait une échéance que la constitution accepte."""
    _bande(monkeypatch, [30, 365], 180)
    assert all(h['dans_la_bande'] for h in A.horizons_annotes()['horizons'])


#  ═══════════  2. la bande est DÉRIVÉE, jamais recopiée  ══════════════════════

def test_la_bande_suit_la_constitution_ACTIVE(monkeypatch):
    """Si l'adaptateur portait sa propre copie, changer de constitution ne
    changerait rien — et le produit annoncerait une doctrine qu'il n'applique
    pas (D-084)."""
    _bande(monkeypatch, [120, 240], 180)
    a = A.horizons_annotes()
    _bande(monkeypatch, [30, 90], 60)
    b = A.horizons_annotes()
    assert a['bande_preferee'] != b['bande_preferee']
    par_a = {h['dte']: h['dans_la_bande'] for h in a['horizons']}
    par_b = {h['dte']: h['dans_la_bande'] for h in b['horizons']}
    assert par_a[30] is False and par_b[30] is True, (
        'la bande est recopiee : elle ne suit pas la constitution')


def test_AUCUNE_bande_en_dur_dans_l_adaptateur():
    """Le recensement qui empêche la copie de revenir."""
    import inspect
    src = inspect.getsource(A.horizons_annotes)
    for littéral in ('120', '240', '180,', '[90, 180]'):
        assert littéral not in src.split('"""')[-1], (
            'une borne de la doctrine est ecrite en dur : %r' % littéral)


#  ═══════════  3. « je ne sais pas » n'est pas « déconseillé »  ═══════════════

def test_SANS_constitution_active_la_reponse_est_NONE(monkeypatch):
    """Le cas le plus important. `False` se lirait « la doctrine deconseille
    cette echeance » — une affirmation que rien ne soutient."""
    _bande(monkeypatch, None, None)
    for h in A.horizons_annotes()['horizons']:
        assert h['dans_la_bande'] is None, h
        assert h['est_la_cible'] is False
        assert h['ecart_a_la_cible'] is None


def test_un_profil_ILLISIBLE_est_nomme_et_non_avale(monkeypatch):
    """Une erreur de lecture du profil ne doit pas passer pour « aucune
    doctrine » : les deux se corrigent différemment."""
    def _tombe():
        raise RuntimeError('profil corrompu')
    monkeypatch.setattr('vertex.strategy.release.etat_actif', _tombe)
    r = A.horizons_annotes()
    assert r['erreur'] and 'profil corrompu' in r['erreur']
    assert all(h['dans_la_bande'] is None for h in r['horizons'])


def test_la_note_explique_le_NONE():
    """Une valeur nulle sans explication se lit comme un oubli."""
    r = A.horizons_annotes()
    assert r['note'] and 'None' in r['note']


#  ═══════════  4. plus aucune couleur en dur dans le moteur  ══════════════════

def test_le_sizing_ne_porte_plus_d_hex():
    """`#FFB23F` appartenait à la palette Obsidian Copper abandonnée. Un
    moteur qui impose une couleur impose une palette (règle de design n°3)."""
    for s in A.SIZING:
        assert 'color' not in s, 'couleur en dur : %r' % s
        assert s.get('ton'), 'le ton semantique manque : %r' % s
    #  Sur les lignes de CODE seulement : le commentaire qui explique le
    #  retrait cite forcément les deux hex, et l'interdire reviendrait à
    #  effacer la trace de ce qu'on a corrigé.
    code = [l for l in open(A.__file__, encoding='utf-8').read().splitlines()
            if not l.lstrip().startswith('#')]
    for hexa in ('#EF4444', '#FFB23F'):
        fautives = [l.strip()[:70] for l in code if hexa in l]
        assert fautives == [], 'hex moteur %s : %r' % (hexa, fautives)


def test_les_tons_sont_des_noms_SEMANTIQUES():
    """« risque » et « prudence » se mappent sur un jeton ; « rouge » et
    « orange » imposeraient la palette depuis le moteur."""
    tons = {s['ton'] for s in A.SIZING}
    assert tons == {'risque', 'prudence'}


#  ═══════════  outils  ════════════════════════════════════════════════════════

def _bande(monkeypatch, bande, cible):
    monkeypatch.setattr('vertex.strategy.release.etat_actif',
                        lambda: {'dte_prefere': bande, 'dte_cible': cible,
                                 'version': 4 if bande else None})
