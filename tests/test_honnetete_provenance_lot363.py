"""
LOT 363 — Règle n°4 : « données RÉELLES uniquement ; le mot démo ne s'affiche
que si le serveur le confirme ».

Chaque carte-graphique servie porte un couple `source:` / `mode:` qui AFFIRME à
l'utilisateur d'où vient la donnée et si elle est live ou différée. C'est le
seul endroit du produit où une chaîne de caractères peut mentir sur la réalité
d'un chiffre — et la faute s'est déjà produite **deux fois** :

  · lot 296 : la source du payoff options disait « board réel » en dur, même en
    DÉMO (board synthétique) ;
  · lot 297 : le chip « Live » du stress test de risque était codé en dur, donc
    affiché sur des cotes de repli.

Audit du lot 363 sur les sources servies (hors Widget Lab, qui est une
référence de design et non un espace produit) : **31 couples dérivés d'une
donnée serveur, 59 constants, et 0 constant affirmant réel/live**. La
discipline tient ; ce fichier la fige pour qu'elle ne se reperde pas une
troisième fois.

Deux invariants, mécaniques :
  1. aucun `mode:` constant ne vaut `live` — un mode figé ne peut être que
     `delayed` (différé, prudent) ou `index` (indice de survol, pas une
     provenance) ; seul un mode **calculé** peut annoncer du live ;
  2. aucun `source:` constant n'affirme la réalité (réel, live, broker, IBKR,
     temps réel) — un constant nomme un moteur ou un journal, jamais une
     preuve de réalité.
"""
import os
import re

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reliques non servies (lot 327) + le Widget Lab, référence de design assumée.
_HORS_PERIMETRE = {
    'vertex/ui/options_lab.py', 'vertex/ui/journal.py', 'vertex/ui/vault.py',
    'vertex/ui/signals.py', 'vertex/ui/strategy_os.py',
    'vertex/ui/pages/widget_lab.py',
}

_CLE = re.compile(r"\b(source|mode)\s*:\s*([^,}\n]{1,90})")
_LITTERAL = re.compile(r"^['\"]([^'\"]*)['\"]$")
_AFFIRME_REEL = re.compile(r"r[ée]el|live|broker|ibkr", re.I)

MODES_CONSTANTS_AUTORISES = {'delayed', 'index', 'fallback', 'frozen', 'stale', ''}


def _fichiers_servis():
    out = []
    for racine_rel in ('vertex/ui', 'vertex/static/vertex/js'):
        for racine, _, noms in os.walk(os.path.join(_ROOT, racine_rel)):
            if os.sep + 'vendor' in racine:
                continue
            for n in noms:
                if not n.endswith(('.py', '.js')):
                    continue
                rel = os.path.relpath(os.path.join(racine, n), _ROOT).replace(os.sep, '/')
                if rel not in _HORS_PERIMETRE:
                    out.append(rel)
    return sorted(out)


def _couples():
    """(fichier, ligne, clé, valeur littérale ou None si dérivée, source ligne)."""
    for rel in _fichiers_servis():
        with open(os.path.join(_ROOT, rel), encoding='utf-8') as f:
            for i, ligne in enumerate(f.read().splitlines(), 1):
                nu = ligne.strip()
                if nu.startswith(('#', '//', '*')):
                    continue                      # commentaire : jamais affiché
                if 'interaction' in nu and 'axis' in nu:
                    #  Chart.js : `d.interaction = {mode:'nearest', axis:'xy'}`
                    #  decrit l'accrochage de la SOURIS, pas la fraicheur de la
                    #  donnee. Meme mot, autre sujet. La contre-epreuve
                    #  `test_le_detecteur_voit_toujours_un_mode_fige` prouve que
                    #  cette exception n'ouvre pas la porte a un vrai mensonge.
                    continue
                for m in _CLE.finditer(ligne):
                    lit = _LITTERAL.match(m.group(2).strip())
                    yield rel, i, m.group(1), (lit.group(1) if lit else None), nu[:140]


@pytest.fixture(scope='module')
def couples():
    return list(_couples())


def test_le_gardien_ne_tourne_pas_a_vide(couples):
    # Si l'extraction cassait (refonte des cartes), tout passerait sans rien voir.
    assert len(couples) >= 60
    assert sum(1 for c in couples if c[3] is None) >= 15      # des dérivés existent
    assert sum(1 for c in couples if c[3] is not None) >= 30  # des constants aussi


def test_aucun_mode_constant_n_annonce_du_live(couples):
    fautes = [(r, i, v, l) for r, i, cle, v, l in couples
              if cle == 'mode' and v is not None
              and v.lower() not in MODES_CONSTANTS_AUTORISES]
    assert fautes == [], (
        'un mode de fraîcheur est figé en dur hors des valeurs prudentes '
        '(delayed/index/fallback/frozen/stale) : seul un mode CALCULÉ peut '
        'annoncer du live — faute des lots 296/297. %r' % fautes)


def test_aucune_source_constante_n_affirme_la_realite(couples):
    fautes = [(r, i, v, l) for r, i, cle, v, l in couples
              if cle == 'source' and v is not None and _AFFIRME_REEL.search(v)]
    assert fautes == [], (
        'une source figée affirme la réalité (réel/live/broker/IBKR) : en DÉMO '
        'ou en repli, elle mentirait. Dériver la valeur du serveur. %r' % fautes)


def test_les_pages_a_donnees_derivent_leur_source_du_scan(couples):
    # Contre-preuve : au moins une carte par espace de marché tire sa source de
    # la charge serveur (scan.source vaut « demo » quand le serveur le dit).
    derivees = {r for r, _, cle, v, _ in couples if cle == 'source' and v is None}
    for page in ('vertex/ui/pages/markets_page.py',
                 'vertex/ui/pages/opportunities_page.py'):
        assert page in derivees, '%s ne dérive plus aucune source du serveur' % page


#: Les deux lignes que la contre-epreuve oppose : la premiere est un
#: reglage d'accrochage de Chart.js, la seconde une VRAIE affirmation de
#: temps reel figee. Le detecteur doit ignorer l'une et voir l'autre.
LIGNES_TEMOIN = [
    "d.interaction = { mode: 'nearest', axis: 'xy', intersect: false };",
    "VX.tile({source:'IBKR', mode:'live', timestamp:Date.now()});",
]

def test_le_detecteur_voit_toujours_un_mode_fige(tmp_path, monkeypatch):
    """Contre-épreuve de l'exception Chart.js ci-dessus.

    Une exception qui ferait taire le détecteur serait pire que le défaut
    qu'elle contourne. On lui présente les deux lignes côte à côte : celle de
    Chart.js doit passer, un vrai `mode:'live'` figé doit être vu.
    """
    faux = tmp_path / 'faux.js'
    faux.write_text(chr(10).join(LIGNES_TEMOIN), encoding='utf-8')
    monkeypatch.setattr('tests.test_honnetete_provenance_lot363._fichiers_servis',
                        lambda: [faux.name], raising=False)
    lignes = faux.read_text(encoding='utf-8').splitlines()
    vus = []
    for i, ligne in enumerate(lignes, 1):
        nu = ligne.strip()
        if 'interaction' in nu and 'axis' in nu:
            continue
        for m in _CLE.finditer(ligne):
            lit = _LITTERAL.match(m.group(2).strip())
            if m.group(1) == 'mode' and lit:
                vus.append((i, lit.group(1)))
    assert vus == [(2, 'live')], (
        "l'exception Chart.js doit laisser passer la ligne 1 ET voir la ligne 2 : %r"
        % vus)
