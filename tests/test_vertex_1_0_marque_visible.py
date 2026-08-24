"""Vertex 1.0 — LA PROVENANCE DE LA MARQUE, LISIBLE À L'ÉCRAN.

Le lot précédent a rendu la provenance disponible dans l'API. Elle n'était
visible nulle part : la colonne « Prix actuel » affichait un chiffre sans
origine, alors que trois conventions coexistent chez le courtier lui-même.

Mesuré le 24 août 2026 sur URA 20270115 C 50, à deux instants de la même
séance :

| instant | marché | dernier échange | marque retenue |
|---|---|---:|---:|
| 13:32 UTC | 3,50 / 4,30 | 3,70 | 3,70 |
| plus tard | 3,50 / 3,80 | 3,90 | **3,90** |

Au second instant, le dernier échange est **au-dessus de l'ask** : Vertex
valorise donc la position plus haut que le prix auquel elle pourrait être
vendue. Ce n'est pas une erreur de calcul — c'est la convention « dernier
échange » sur un contrat peu liquide. Mais sans provenance affichée, rien ne
permet de le voir.

## Pourquoi ce banc passe par Node

`marqueNote` est du JavaScript servi dans la page. L'éprouver en Python
reviendrait à tester une copie ; on exécute donc le VRAI code extrait de la
page servie, avec un `VX.fmt` réduit à ce qu'il utilise.

## Limite honnête

Le tableau des positions lit le bureau DÉCLARÉ. Sur ce compte, il contient
AAPL et ADP — deux actions — et pas l'option URA réellement détenue. La note
de provenance ne concerne donc aucune ligne affichée aujourd'hui : ce banc
prouve qu'elle est correcte, pas qu'elle est visible sur ce desk-là.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
PAGE = RACINE / "vertex" / "ui" / "pages" / "portfolio_page.py"


def _node_dispo():
    return shutil.which("node") is not None


def _extraire(nom: str) -> str:
    """Le source d'une fonction de la page, accolades équilibrées."""
    src = PAGE.read_text(encoding="utf-8")
    i = src.index("function %s(" % nom)
    prof, j = 0, i
    while j < len(src):
        if src[j] == "{":
            prof += 1
        elif src[j] == "}":
            prof -= 1
            if prof == 0:
                return src[i:j + 1]
        j += 1
    raise AssertionError("fonction %s non refermée" % nom)


def _sonde(cas: list) -> list:
    """Exécute `marqueNote` sur des cas, dans Node, avec un VX minimal."""
    prelude = """
const VX = { fmt: { pct(v, dec = 2, signed = true) {
  if (v === null || v === undefined || !isFinite(v)) return '—';
  const s = signed && v > 0 ? '+' : '';
  return s + Number(v).toFixed(dec) + ' %';
} } };
"""
    consts = ""
    for ligne in PAGE.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("const MARQUE_LIB=") or ligne.startswith("const SPREAD_INCERTAIN="):
            consts += ligne + "\n"
        elif consts and ligne.strip().startswith("CLOTURE_VEILLE"):
            consts += ligne + "\n"
    assert "MARQUE_LIB" in consts and "SPREAD_INCERTAIN" in consts, consts

    script = (prelude + consts + _extraire("marqueNote")
              + "\nconsole.log(JSON.stringify(%s.map(marqueNote)));"
              % json.dumps(cas))
    run = subprocess.run(["node", "-e", script], capture_output=True,
                         text=True, encoding="utf-8", check=False)
    assert run.returncode == 0, run.stderr
    return json.loads(run.stdout.strip().splitlines()[-1])


pytestmark = pytest.mark.skipif(not _node_dispo(),
                                reason="node absent — la mesure porterait sur rien")


#  ═══════════════════  1. chaque convention est NOMMÉE  ═══════════════════════

def test_chaque_origine_de_marque_a_son_libelle():
    a, b, c = _sonde([
        {"mark": 3.9, "markSource": "DERNIER_ECHANGE", "spreadPct": 2.0},
        {"mark": 4.0, "markSource": "MILIEU_FOURCHETTE", "spreadPct": 2.0},
        {"mark": 3.88, "markSource": "CLOTURE_VEILLE", "spreadPct": 2.0},
    ])
    assert "dernier echange" in a
    assert "milieu" in b
    assert "cloture veille" in c


def test_un_marche_LARGE_est_signale_avec_son_ampleur():
    """20,5 % : dernier échange, milieu et marque du courtier s'écartent de
    plusieurs pour cent. Un prix au centime promettrait une précision absente."""
    (html,) = _sonde([{"mark": 3.7, "markSource": "DERNIER_ECHANGE",
                       "spreadPct": 20.5}])
    assert "marche large" in html
    #  Arrondi au point de pourcentage : un indicateur de largeur de marché n'a
    #  pas besoin de décimales, et en afficher promettrait une précision que la
    #  fourchette elle-même n'a pas.
    assert "21 %" in html, html
    assert "vx-warn" in html, "l'avertissement doit être visible, pas seulement écrit"
    assert "dernier echange" in html, "l'origine reste dite, même quand on alerte"


def test_un_marche_SERRE_n_est_pas_signale():
    """Contre-épreuve : un avertissement présent partout ne distingue plus rien."""
    (html,) = _sonde([{"mark": 4.0, "markSource": "MILIEU_FOURCHETTE",
                       "spreadPct": 1.0}])
    assert "marche large" not in html
    assert "vx-warn" not in html
    assert "milieu" in html


#  ═══════════  2. ce qui ne doit RIEN afficher n'affiche rien  ════════════════

def test_une_action_sans_provenance_n_ajoute_aucune_note():
    """Les actions n'ont pas de convention de marque : leur coller une note
    vide ajouterait du bruit sur chaque ligne du tableau."""
    (html,) = _sonde([{"mark": 283.69, "markSource": None, "spreadPct": None}])
    assert html == ""


def test_une_marque_ABSENTE_n_affiche_pas_de_provenance():
    """Sans prix, il n'y a pas d'origine à donner — la cellule dira « n/d »."""
    (html,) = _sonde([{"mark": None, "markSource": "ABSENTE", "spreadPct": 30.0}])
    assert html == ""


def test_un_spread_INCONNU_ne_declenche_aucun_avertissement():
    """Ne pas connaître la fourchette n'est pas la savoir étroite — mais ce
    n'est pas non plus une raison de crier."""
    (html,) = _sonde([{"mark": 3.7, "markSource": "DERNIER_ECHANGE",
                       "spreadPct": None}])
    assert "marche large" not in html
    assert "dernier echange" in html


#  ═══════════  3. la page appelle bien la note, et une seule fois  ════════════

def test_la_cellule_prix_actuel_appelle_la_note():
    src = PAGE.read_text(encoding="utf-8")
    assert 'data-label="Prix actuel"' in src
    i = src.index('data-label="Prix actuel"')
    assert "marqueNote(t)" in src[i:i + 260], (
        "la provenance doit être rendue AVEC le prix, pas ailleurs")


def test_la_provenance_vient_du_SERVEUR_et_n_est_pas_recalculee_au_client():
    """La recalculer côté client la ferait diverger au premier ajustement, et
    l'écran annoncerait une origine que le calcul ne pratique plus."""
    src = PAGE.read_text(encoding="utf-8")
    assert "q.mark_source" in src, "la page doit LIRE la provenance servie"
    assert not re.search(r"markSource\s*=\s*\(?\s*mark\s*===", src), (
        "aucune redérivation locale de la provenance")


#  ═══════  4. la ROUTE n'annote que ce qui a une marque a expliquer  ══════════

def _client_desk(quotes):
    from flask import Flask
    from vertex.app.routes import desk
    app = Flask(__name__)
    app.register_blueprint(desk.make_blueprint(
        opt_job=lambda kind, args, timeout: {p['key']: quotes for p in args[0]},
        ibkr_enabled=True))
    return app.test_client()


def _coter(quotes):
    c = _client_desk(quotes)
    j = c.post('/api/pos-quotes', json={'positions': [
        {'sym': 'URA', 'exp': '2027-01', 'strike': 50, 'right': 'C'}]}).get_json()
    return j['results']['URA|2027-01|50|C']


def test_une_option_cotee_recoit_sa_provenance_et_son_spread():
    """Le cas réel du 24 août, servi par la route que lit l'écran."""
    q = _coter({'mark': 3.9, 'last': 3.9, 'bid': 3.5, 'ask': 3.8})
    assert q['mark_source'] == "DERNIER_ECHANGE"
    assert q['mid'] == 3.65
    assert q['spread_pct'] == 8.22


def test_une_cotation_d_ACTION_reste_INTACTE():
    """Une action servie par le repli ne porte qu'un `px` : aucune convention
    de marque ne s'y applique. Lui coller « ABSENTE » serait doublement faux —
    le prix existe, et l'origine n'est pas manquante, elle est hors sujet.
    Témoin négatif : sans lui, la route salissait chaque ligne d'actions."""
    assert _coter({'px': 1.23}) == {'px': 1.23}


def test_une_option_SANS_marque_ni_fourchette_reste_intacte():
    """Rien à expliquer non plus quand il n'y a rien à marquer."""
    assert _coter({'iv': 0.42}) == {'iv': 0.42}
