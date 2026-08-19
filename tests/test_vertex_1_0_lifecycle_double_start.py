"""Vertex 1.0 · #779 — LE DOUBLE DÉMARRAGE DES BOUCLES, FERMÉ (G1).

`RELEASE_GATES.md` G1 : *« … avec parité et sans double démarrage »*. Rien ne
tenait cette moitié-là.

## Le défaut, mesuré

`terminal.py` appelle `_start_workers()` à **deux** endroits — à l'import quand
`START_ON_IMPORT=1`, et depuis `_start_app()` — et la fonction n'avait **aucune
garde d'idempotence**. Mesure directe en `DEMO=1 NO_IBKR=1` :

```text
avant  · START_ON_IMPORT=1 : import → 4 fils, puis _start_workers() → 7  (+3)
après  · START_ON_IMPORT=1 : import → 4 fils, puis _start_workers() → 4  (+0)
```

`_loop`, `_alerts_loop` et `_cal_loop` tournaient donc en double : deux boucles
de scan mutant `scan_state` en même temps. **Rien ne plante** — elles s'écrasent
l'une l'autre au hasard de l'ordonnancement, et le symptôme est une donnée qui
change sans raison.

## Où il mordait

La **production n'était pas touchée** : `render.yaml` lance
`gunicorn vertex.runtime:app --workers 1`, qui importe le module sans jamais
appeler `_start_app()`.

Le **lancement local l'était** — et `START_ON_IMPORT=1` est la variable des
commandes documentées et des outils de mesure du dépôt. Toute mesure prise dans
ce mode l'a été avec deux boucles concurrentes.

## Pourquoi ignorer plutôt que lever

Lever casserait un démarrage qui « marche » aujourd'hui. Le second appel est
donc ignoré **et compté** : sans compteur, la garde travaillerait en silence et
personne ne saurait que le double appel existe toujours dans le code.
"""
import threading

import pytest

from vertex.app import lifecycle


@pytest.fixture(autouse=True)
def _etat_propre():
    lifecycle.reinitialiser()
    yield
    lifecycle.reinitialiser()


def test_le_second_appel_est_ignore():
    """LE CŒUR DE LA GARDE."""
    trace = []
    assert lifecycle.demarrer_une_seule_fois(lambda: trace.append(1)) is True
    assert lifecycle.demarrer_une_seule_fois(lambda: trace.append(2)) is False
    assert trace == [1], (
        'le second demarreur a tourne : les boucles partiraient en double')


def test_la_tentative_ignoree_reste_comptee():
    """Une garde qui travaille en silence laisse croire que le double appel a
    disparu du code. Il est toujours là ; il est simplement neutralisé."""
    lifecycle.demarrer_une_seule_fois(lambda: None)
    lifecycle.demarrer_une_seule_fois(lambda: None)
    lifecycle.demarrer_une_seule_fois(lambda: None)
    etat = lifecycle.statut()
    assert etat['demarre'] is True
    assert etat['appels'] == 3
    assert etat['ignores'] == 2, (
        'les tentatives neutralisees ne sont plus comptees : un diagnostic ne '
        'pourra plus constater qu\'un second appel a eu lieu')


def test_la_garde_tient_sous_appels_concurrents():
    """Le verrou couvre la LECTURE et l'écriture du drapeau.

    Sans lui, deux appels simultanés — l'import et le lancement peuvent se
    croiser sous un serveur à threads — verraient tous deux `demarre == False`
    et démarreraient chacun leurs boucles."""
    compte = []
    barriere = threading.Barrier(8)

    def tenter():
        barriere.wait()
        lifecycle.demarrer_une_seule_fois(lambda: compte.append(1))

    fils = [threading.Thread(target=tenter) for _ in range(8)]
    for f in fils:
        f.start()
    for f in fils:
        f.join(timeout=10)

    assert len(compte) == 1, (
        '%d demarrages concurrents sont passes : le verrou ne couvre pas la '
        'lecture du drapeau' % len(compte))
    assert lifecycle.statut()['ignores'] == 7


def test_le_demarreur_tourne_hors_du_verrou():
    """`demarreur` lance des threads et peut durer. Le tenir sous verrou
    bloquerait un second appelant au lieu de le laisser repartir immédiatement
    avec `False` — et un démarrage lent gèlerait le processus."""
    verrou_libre = []

    def demarreur_lent():
        #  Si le verrou etait tenu ici, cet appel imbrique se bloquerait.
        verrou_libre.append(lifecycle.demarrer_une_seule_fois(lambda: None))

    lifecycle.demarrer_une_seule_fois(demarreur_lent)
    assert verrou_libre == [False], (
        'un appel imbrique n\'a pas pu obtenir le verrou : le demarreur tourne '
        'sous verrou, ce qui peut geler le demarrage')


def test_le_monolithe_passe_bien_par_la_garde():
    """La garde ne vaut que si `terminal._start_workers` l'emprunte. Un appel
    direct à l'ancien corps la contournerait entièrement."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1].joinpath(
        'terminal.py').read_text(encoding='utf-8')
    assert '_lifecycle.demarrer_une_seule_fois(_demarrer_les_boucles' in src, (
        '`terminal._start_workers` ne passe plus par la garde : le double '
        'demarrage est de nouveau possible')
    #  Les DEUX sites d'appel historiques doivent toujours viser la facade
    #  gardee, pas le corps interne. ON VISE UN APPEL, PAS LE NOM : la chaine
    #  `_demarrer_les_boucles()` est une SOUS-CHAINE de sa propre definition
    #  `def _demarrer_les_boucles():` — la chercher telle quelle faisait echouer
    #  le test sur un fichier parfaitement correct.
    import re
    appels = re.findall(r'(?<!def )\b_demarrer_les_boucles\(\)', src)
    assert appels == [], (
        'le corps interne est appele directement (%d fois) : ce chemin '
        'contourne la garde' % len(appels))
    assert 'if os.environ.get(\'START_ON_IMPORT\') == \'1\':' in src, (
        'le demarrage a l\'import a disparu — verifier que le mode cloud '
        '(gunicorn, sans _start_app) demarre encore ses boucles')


def test_la_reinitialisation_est_reservee_aux_tests():
    """Aucun chemin de production n'a de raison de redémarrer les boucles :
    c'est exactement ce que la garde interdit."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    src = racine.joinpath('terminal.py').read_text(encoding='utf-8')
    assert 'reinitialiser()' not in src, (
        '`terminal.py` reinitialise le cycle de vie : la garde devient '
        'contournable depuis la production')
