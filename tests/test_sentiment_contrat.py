"""LOT 609 — LE CONTRAT DU SENTIMENT, TENU AUX DEUX BOUTS.

`news_plus.sentiment()` rend **exactement** `-1`, `0` ou `+1`. Deux
consommateurs de `news_impact.py` ont été écrits pour un score **continu** :

    score_importance :  abs(senti) >= 0.5      -> +5
    potential_impact :  senti > 0.15           -> POSITIF_POTENTIEL
                        confidence = min(0.7, abs(senti))

Sur le domaine réel, ces seuils ne séparent que le **signé** du **neutre**, et
la « confiance » ne prend qu'une valeur par direction : **un littéral déguisé en
calcul**. Mesuré au lot 609 par **énumération exhaustive** du domaine — ce n'est
pas un échantillon, il n'existe pas d'autre cas.

Le lot n'a **rien changé au comportement** : inventer une amplitude sur un
lexique de 22+22 mots serait de la fausse précision. Ce gardien existe pour que
le désaccord ne puisse pas s'aggraver en silence, et il est **rouge dans les
deux sens** (608-B) :

  · si le producteur devient continu sans que les seuils soient revus, il casse ;
  · si les seuils sont modifiés alors que le producteur est resté ternaire, il
    casse aussi.
"""

import io
import os

from vertex.market.news_impact import potential_impact, score_importance
from vertex.services.news_plus import sentiment

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Le domaine ENTIER du producteur. Trois valeurs, pas un échantillon.
_DOMAINE = (-1, 0, 1)

# Des textes de forme réaliste, choisis pour couvrir les cas de comptage.
_TEXTES = [
    ('aucun mot du lexique',      'La societe publie un communique de presse'),
    ('un seul positif',           'Le titre signe un record'),
    ('trois positifs',            'record, hausse et profit en forte croissance'),
    ('un seul negatif',           'Le titre plonge apres la seance'),
    ('trois negatifs',            'chute, perte et avertissement apres une enquete'),
    ('trois positifs deux negatifs', 'record hausse profit malgre une chute et une perte'),
    ('deux contre deux',          'record et hausse contre chute et perte'),
]


# ── 1. Le producteur ne rend que trois valeurs ──────────────────────────────

def test_le_producteur_est_ternaire():
    vus = {sentiment(t) for _, t in _TEXTES}
    assert vus <= set(_DOMAINE), 'valeurs hors contrat : %s' % (vus - set(_DOMAINE))
    assert vus == set(_DOMAINE), (
        'le banc doit exercer les trois valeurs, sinon il ne vérifie rien '
        '(591-C) — observé : %s' % sorted(vus))


def test_l_amplitude_n_existe_pas():
    """Trois mots positifs valent un seul : c'est le fait qui justifie de NE PAS
    ajouter de décimales."""
    assert sentiment('record, hausse et profit en forte croissance') == \
        sentiment('Le titre signe un record') == 1


def test_le_contrat_est_ecrit_dans_le_code():
    src = io.open(os.path.join(_ROOT, 'vertex', 'services', 'news_plus.py'),
                  encoding='utf-8').read()
    i = src.index('def sentiment(text):')
    doc = src[i:i + 1600]
    assert 'EXACTEMENT' in doc and '{-1, 0, +1}' in doc, (
        "le domaine doit être écrit dans la docstring — c'est ce qui manquait")


# ── 2. Les seuils du consommateur ne discriminent que signé / neutre ────────

def test_les_deux_seuils_partitionnent_le_domaine_a_l_identique():
    """`0.15` et `0.5` sont écrits comme des seuils d'intensité. Sur le domaine
    réel ils rendent la MÊME partition. Si un jour ce test échoue, c'est que le
    producteur est devenu continu — et alors ces seuils doivent être revus."""
    base = score_importance({'sentiment': None, 'entities': []}, [])
    par_seuil_05 = {s: score_importance({'sentiment': s, 'entities': []}, []) != base
                    for s in _DOMAINE}
    par_seuil_015 = {s: potential_impact({'sentiment': s})['direction'] != 'NEUTRE'
                     for s in _DOMAINE}
    assert par_seuil_05 == par_seuil_015, (
        'les deux seuils ne partitionnent plus le domaine à l’identique : %s vs %s'
        % (par_seuil_05, par_seuil_015))
    assert par_seuil_05 == {-1: True, 0: False, 1: True}


def test_la_confiance_est_constante_par_direction():
    """Elle a l'air calculée ; sur le domaine réel elle ne prend qu'une valeur
    par direction. Le jour où ce test échoue, `confidence` sera devenue une
    vraie mesure — et il faudra décider si on l'affiche."""
    par_direction = {}
    for s in _DOMAINE:
        r = potential_impact({'sentiment': s})
        par_direction.setdefault(r['direction'], set()).add(r['confidence'])
    assert all(len(v) == 1 for v in par_direction.values()), (
        'confiance devenue variable : %s' % par_direction)
    assert par_direction == {'NEGATIF_POTENTIEL': {0.7}, 'NEUTRE': {0.3},
                             'POSITIF_POTENTIEL': {0.7}}


def test_le_desaccord_est_ecrit_chez_le_consommateur():
    src = io.open(os.path.join(_ROOT, 'vertex', 'market', 'news_impact.py'),
                  encoding='utf-8').read()
    assert 'ne sépare PAS le fort du faible' in src, (
        "score_importance doit dire ce que son seuil discrimine vraiment")
    assert "littéral déguisé en calcul" in src, (
        "potential_impact doit dire que sa confiance n'est pas une mesure")


# ── 3. Le comportement n'a pas changé ───────────────────────────────────────

def test_le_lot_609_n_a_rien_change_au_comportement():
    """Valeurs figées AVANT le lot, pour qu'une « amélioration » silencieuse du
    sentiment se voie ici."""
    assert score_importance({'sentiment': 1, 'entities': [], 'category': 'MACRO'}, []) == 45
    assert score_importance({'sentiment': 0, 'entities': [], 'category': 'MACRO'}, []) == 40
    assert potential_impact({'sentiment': 1}) == {
        'direction': 'POSITIF_POTENTIEL', 'confidence': 0.7}
    assert potential_impact({'sentiment': None}) == {
        'direction': 'INCONNUE', 'confidence': 0.0}
