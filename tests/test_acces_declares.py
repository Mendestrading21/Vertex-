"""UN ACCÈS QUI BLOQUE UNE SOURCE DOIT ÊTRE DÉCOUVRABLE.

## Le défaut mesuré

`vertex/data_sources/sec_edgar.py` **refuse** d'appeler la SEC sans
`SEC_USER_AGENT` — il lève `EntitlementManquant`, et il a raison : le
fair-access de la SEC exige un contact réel, que Vertex n'invente pas.

Mais cette variable n'était **ni dans `.env.example`, ni dans le tableau
`config_validation._SPEC`** qui alimente Système → Connexions. Un utilisateur
qui voulait les fondamentaux SEC recevait donc un refus, sans aucun moyen de
découvrir quoi poser : le modèle de configuration ne la mentionnait pas, et la
page des statuts ne la montrait pas manquante.

Une source rendue inaccessible par une variable invisible est une capacité
absente qui ne se déclare pas — exactement ce que l'invariant 8 interdit.

## Ce que ce banc garde

Toute variable d'environnement dont l'absence **empêche** une source de
fonctionner doit être :

1. déclarée dans `config_validation._SPEC`, pour que son statut soit visible ;
2. présente dans `.env.example`, pour être découvrable.

## Ce qu'il n'exige PAS

Les variables de réglage interne (`VERTEX_SCAN_WORKERS`, `VERTEX_YF_TTL`,
`START_ON_IMPORT`…) n'ont pas à être documentées : leur absence ne bloque rien,
elle laisse un défaut raisonnable. Confondre les deux remplirait le modèle de
bruit et noierait les trois variables qui comptent vraiment.
"""
from __future__ import annotations

import os
import re

import pytest

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Variables dont l'absence FAIT ÉCHOUER une source, relevées à la lecture du
#: code : chacune est lue puis suivie d'une levée d'exception ou d'un refus.
_BLOQUANTES = ('SEC_USER_AGENT',)


def _modele() -> str:
    with open(os.path.join(_RACINE, '.env.example'), encoding='utf-8') as f:
        return f.read()


def _spec_noms() -> set[str]:
    from vertex.app import config_validation as cv
    return {entree[0] for entree in cv._SPEC}


# ── 1. Anti-vide ────────────────────────────────────────────────────────────

def test_le_tableau_de_validation_n_est_pas_vide():
    """Sans tableau, les assertions suivantes seraient vraies pour rien."""
    noms = _spec_noms()
    assert len(noms) >= 10, 'seulement %d variables déclarées' % len(noms)


def test_le_modele_env_liste_bien_des_variables():
    trouvees = set(re.findall(r'^#?\s*([A-Z_]{3,})=', _modele(), re.M))
    assert len(trouvees) >= 10, 'modèle .env quasi vide : %s' % sorted(trouvees)


# ── 2. Le contrat ───────────────────────────────────────────────────────────

@pytest.mark.parametrize('variable', _BLOQUANTES)
def test_une_variable_BLOQUANTE_est_declaree_au_tableau(variable):
    """Déclarée → Système → Connexions la montre CONFIGURED / MISSING, avec sa
    conséquence. Non déclarée → l'utilisateur ne sait pas qu'elle existe."""
    assert variable in _spec_noms(), (
        '%s empêche une source de fonctionner mais n’apparaît pas dans '
        'config_validation._SPEC : son absence resterait invisible' % variable)


@pytest.mark.parametrize('variable', _BLOQUANTES)
def test_une_variable_BLOQUANTE_est_dans_le_modele_env(variable):
    assert re.search(r'^#?\s*%s=' % re.escape(variable), _modele(), re.M), (
        '%s n’est pas dans .env.example : elle n’est pas découvrable' % variable)


@pytest.mark.parametrize('variable', _BLOQUANTES)
def test_la_consequence_annoncee_n_est_pas_vide(variable):
    """« MISSING » sans conséquence ne dit pas ce qu'on perd."""
    from vertex.app import config_validation as cv
    for nom, _requis, _valide, consequence in cv._SPEC:
        if nom == variable:
            assert consequence and len(consequence) > 20, (
                '%s est déclarée sans conséquence lisible : %r'
                % (variable, consequence))
            return
    pytest.fail('%s absente du tableau' % variable)


# ── 3. Contre-épreuve : le refus existe bien ────────────────────────────────

def test_la_source_SEC_refuse_VRAIMENT_sans_user_agent(monkeypatch):
    """Si la source n'échouait pas sans la variable, ce banc garderait une
    règle imaginaire."""
    from vertex.data_sources import sec_edgar
    monkeypatch.delenv('SEC_USER_AGENT', raising=False)
    with pytest.raises(Exception) as capture:
        sec_edgar.user_agent()
    message = str(capture.value)
    assert 'SEC_USER_AGENT' in message, (
        'le refus ne nomme pas la variable à poser : %s' % message)


def test_le_refus_SEC_ne_fuit_aucune_exception_python(monkeypatch):
    """Le message doit nommer le remède, pas un type Python."""
    from vertex.data_sources import sec_edgar
    monkeypatch.delenv('SEC_USER_AGENT', raising=False)
    with pytest.raises(Exception) as capture:
        sec_edgar.user_agent()
    message = str(capture.value)
    for interdit in ('Traceback', 'IndexError', 'TypeError', 'KeyError'):
        assert interdit not in message, message


# ── 4. Le modèle ne promet pas ce que le code ignore ────────────────────────

def test_le_modele_env_n_invente_aucune_variable_ignoree():
    """Une variable listée dans `.env.example` mais lue NULLE PART est une
    promesse creuse : l'utilisateur la pose et rien ne se passe."""
    declarees = set(re.findall(r'^#?\s*([A-Z_]{3,})=', _modele(), re.M))
    lues = set(_spec_noms())
    for racine, dirs, noms in os.walk(os.path.join(_RACINE, 'vertex')):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for nom in noms:
            if not nom.endswith('.py'):
                continue
            with open(os.path.join(racine, nom), encoding='utf-8',
                      errors='ignore') as f:
                src = f.read()
            lues |= set(re.findall(r"""environ(?:\.get)?\(\s*['"]([A-Z_]{3,})['"]""", src))
            lues |= set(re.findall(r"""getenv\(\s*['"]([A-Z_]{3,})['"]""", src))
    with open(os.path.join(_RACINE, 'terminal.py'), encoding='utf-8',
              errors='ignore') as f:
        src = f.read()
    lues |= set(re.findall(r"""environ(?:\.get)?\(\s*['"]([A-Z_]{3,})['"]""", src))
    lues |= set(re.findall(r"""getenv\(\s*['"]([A-Z_]{3,})['"]""", src))

    orphelines = sorted(declarees - lues)
    assert orphelines == [], (
        'promises par .env.example et lues nulle part — l’utilisateur les pose '
        'et rien ne se passe : %s' % orphelines)
