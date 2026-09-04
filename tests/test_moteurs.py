"""Vertex 1.0 — AUDIT DES MOTEURS : CE QU'ILS CALCULENT SORT-IL ?

La mission demande un audit des moteurs de décision **avant** d'en créer un
nouveau. La question naturelle — « que calcule chaque moteur ? » — n'est pas la
plus utile ; celle qui l'est : *ce qu'il calcule sort-il quelque part ?*

Le lot précédent a montré pourquoi. `track_record.evaluate()` tournait, ne
plantait pas, et rendait `resolved: 0` sur toutes les entrées : un moteur
parfaitement vivant dont le résultat était vide, sous un test vert. Un moteur
qu'aucune surface n'atteint est le cas dégénéré du même problème.

## Le résultat

```text
59 moteurs · 58 atteints ET appelés · 1 atteint par rien d'autre que des tests
```

Le seul isolé est `performance_ledger` (124 lignes). Il implémente la séparation
stricte SIGNAL → ALERT → RECOMMENDATION → USER_DECISION → SIMULATED_POSITION →
REAL_POSITION — exactement la discipline que `PRODUCT_CONTRACT` demande — et
**aucun chemin de production ne le lit**. Trois fichiers de tests l'importent, ce
qui lui donne l'apparence d'un module vivant.

Il n'est **pas supprimé ici** : la mission interdit tout nettoyage destructif
sans preuve de non-usage, et la preuve existe désormais — mais la suppression
elle-même relève de `CLEANUP_POLICY.md` (#782) et d'une décision humaine.

## Trois fois où l'instrument était faux avant le produit

1. **Surfaces trop étroites.** La première version ne partait que de `routes/`
   et `pages/`. Elle rendait `analysis` — 336 lignes, producteur des séries de
   prix de tout le produit — « INATTEINT ». L'hypothèse « surface = route » avait
   été invalidée par le chantier #779 lui-même, qui a fait passer `terminal.py`
   de 14 routes à 0 : le monolithe a cessé de déclarer des routes **sans cesser
   d'être servi**, puisqu'il héberge les boucles qui remplissent `scan_state`.
2. **Liaisons d'attribut ignorées.** Le compteur d'appels ne voyait que
   `X.f(...)`, pas `f = X.f` suivi de `f(...)`. Cinq faux positifs, dont
   `analysis` à nouveau — et l'idiome en cause est celui que j'ai moi-même
   généralisé en #779 (`_sync_ibkr_state = _ibkr_state.sync`).
3. Le témoin négatif d'origine vérifiait seulement qu'un fichier fabriqué
   n'existe pas sur disque — ce qui n'éprouve rien. Il **injecte** désormais un
   moteur que personne n'importe dans le graphe et vérifie qu'il ressort isolé.

## Ce que cette mesure ne dit pas

Un chemin d'import prouve la **portée**, pas la **sortie**. Le compteur d'appels
s'en approche mais reste **borné par le bas** : un appel indirect (`getattr`,
fonction passée en argument) n'est pas vu. Zéro appel n'est donc pas une preuve
d'inutilité — c'est une raison de regarder. `INATTEINT`, en revanche, est un fait
solide : aucun chemin n'existe.
"""
import pathlib
import sys

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from tools.mesures import mesurer_moteurs as _mes  # noqa: E402

#: Recensement GELÉ des moteurs qu'aucune surface servie n'atteint. Toute
#: entrée nouvelle doit passer ici, avec sa justification — un moteur isolé qui
#: apparaît en silence est du code mort qui se donne l'air vivant.
#  `performance_ledger` était le seul isolé ; il a été supprimé avec le reste du
#  code injoignable. Le recensement est vide : tout moteur qui apparaîtrait ici
#  serait du code mort qui se donne l'air vivant.
ISOLES_CONNUS: set[str] = set()


@pytest.fixture(scope='module')
def mesure():
    return _mes.mesurer()


def test_les_temoins_de_l_instrument_mordent(mesure):
    """Un détecteur qui ne trouve rien ne prouve rien. Le témoin négatif
    **injecte** un moteur que personne n'importe et vérifie qu'il ressort
    isolé ; le témoin positif exige que `decision_stack` — que le guide nomme
    « vérité des verdicts » — soit atteint ET appelé."""
    assert _mes._temoins(mesure) == []


def test_aucun_moteur_isole_hors_recensement(mesure):
    """LA PROPRIÉTÉ. Un moteur qu'aucune surface n'atteint ne rend service à
    personne — et il coûte : il est lu, maintenu, et il donne au dépôt une
    apparence de richesse que l'écran ne reçoit pas."""
    isoles = {l['moteur'] for l in mesure['moteurs'] if l['statut'] == 'INATTEINT'}
    nouveaux = sorted(isoles - ISOLES_CONNUS)
    assert not nouveaux, (
        'ces moteurs ne sont atteints par AUCUNE surface servie et ne sont pas '
        'recenses : %s — les justifier ici, ou les brancher, ou les retirer '
        'selon CLEANUP_POLICY.md' % nouveaux)


def test_le_recensement_ne_se_perime_pas(mesure):
    """Une entrée qui ne correspond plus à rien doit être RETIRÉE : sinon la
    liste blanche pourrit et couvre des cas disparus."""
    isoles = {l['moteur'] for l in mesure['moteurs'] if l['statut'] == 'INATTEINT'}
    mortes = sorted(ISOLES_CONNUS - isoles)
    assert not mortes, (
        'ces moteurs ne sont plus isoles — les retirer du recensement : %s'
        % mortes)




def test_le_producteur_des_series_est_bien_vu_comme_servi(mesure):
    """LE CONTRE-EXEMPLE QUI A CORRIGÉ L'INSTRUMENT.

    `analysis` produit `series['close']` et `series['dates']`, que toutes les
    pages lisent. Le voir « INATTEINT » signalerait que les surfaces de départ
    ont de nouveau été réduites aux routes — alors que le scan tourne dans les
    boucles de `terminal.py`."""
    par_nom = {l['moteur']: l for l in mesure['moteurs']}
    a = par_nom['analysis']
    assert a['statut'] != 'INATTEINT', (
        'le producteur des series de prix ressort isole : les surfaces de '
        'depart excluent les boucles de fond')
    assert a['appels_production'] > 0, (
        '`analysis` ne compte aucun appel : le detecteur ignore de nouveau les '
        'liaisons d\'attribut (`analyse = _analysis.analyse`)')


def test_les_liaisons_d_attribut_sont_comptees():
    """L'idiome `f = Module.f` est employé partout, y compris par les façades
    posées au chantier #779. Un compteur qui ne voit que `Module.f(...)` a
    produit cinq faux positifs."""
    src = pathlib.Path(_mes.__file__).read_text(encoding='utf-8')
    assert 'isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute)' in src, (
        'le compteur d\'appels ne suit plus les liaisons d\'attribut')


def test_les_surfaces_incluent_les_boucles_de_fond():
    """« Servi » ne veut pas dire « déclare une route ». Depuis #779,
    `terminal.py` n'en déclare plus aucune — et reste la surface qui remplit
    `scan_state`."""
    assert 'terminal.py' in _mes.SURFACES, (
        'les boucles de fond ne sont plus une surface de depart : tout le '
        'pipeline de scan ressortirait isole')
    assert mesurer_surfaces() >= 40, 'la remontee part de trop peu de surfaces'


def mesurer_surfaces():
    return _mes.mesurer()['surfaces_de_depart']
