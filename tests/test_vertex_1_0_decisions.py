"""Vertex 1.0 — LE JOURNAL DES DÉCISIONS RESTE CITABLE.

`DECISIONS.md` est la source d'autorité n°3 de CLAUDE.md : le code, les
messages de commit et les dossiers de validation y renvoient par numéro. Un
renvoi n'a de valeur que s'il désigne **une** décision.

## Le défaut qui a motivé ce banc

Un lot a inséré D-028, D-029 et D-030 alors que la base les portait déjà.
Trois identifiants ont désigné chacun DEUX décisions pendant trois lots :

| numéro | décision A (base) | décision B (insérée) |
|---|---|---|
| D-028 | aucun score avant le point-in-time | une preuve live qui ne se rejoue pas |
| D-029 | le profil V4 n'est pas modifié en place | le type de marché est observé |
| D-030 | sources officielles avant agrégateurs | l'anonymisation n'est pas optionnelle |

Un message de commit citant « D-029 » renvoyait donc à deux textes. Personne
ne l'a vu — et personne ne le verrait : aucune relecture humaine ne compte
cinquante numéros à la main. C'est exactement ce qu'une garde fait mieux
qu'une intention.

## Ce que ce banc NE fait pas

Il ne juge pas le contenu d'une décision. Il vérifie que la table reste
navigable : numéros uniques, suite sans trou, aucun renvoi vers le vide.
"""
from __future__ import annotations

import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
JOURNAL = RACINE / "docs" / "vertex-1.0" / "DECISIONS.md"

_LIGNE = re.compile(r"^\|\s*(D-\d+)\s*\|", re.M)
_RENVOI = re.compile(r"D-\d+")


def _numeros() -> list[str]:
    return _LIGNE.findall(JOURNAL.read_text(encoding="utf-8"))


def test_le_journal_existe_et_n_est_pas_vide():
    """Un banc qui passe sur un fichier absent ne garde rien."""
    assert JOURNAL.is_file()
    assert len(_numeros()) >= 40, "table introuvable ou format changé"


def test_aucun_numero_de_decision_n_est_utilise_DEUX_fois():
    """Le défaut réel du 24 août 2026 : trois numéros pour six décisions."""
    nums = _numeros()
    doublons = sorted({n for n in nums if nums.count(n) > 1})
    assert doublons == [], (
        "chacun de ces numeros designe plusieurs decisions, donc tout renvoi "
        "vers eux est ambigu : %s" % doublons)


def test_la_suite_des_numeros_n_a_pas_de_TROU():
    """Un trou n'est pas anodin : soit une décision a été supprimée sans être
    marquée `retiree`, soit un lot a sauté un numéro et le prochain le
    réutilisera. Les deux fabriquent la collision de demain."""
    nums = sorted(int(n[2:]) for n in _numeros())
    attendus = list(range(nums[0], nums[-1] + 1))
    manquants = sorted(set(attendus) - set(nums))
    assert manquants == [], "numeros absents de la suite : %s" % manquants
    assert nums[0] == 1, "la suite doit commencer a D-001, pas D-%03d" % nums[0]


def test_aucune_decision_ne_RENVOIE_vers_un_numero_inexistant():
    """Une décision qui cite `D-099` inexistant se lit comme une justification
    fondée sur un texte que personne ne peut ouvrir."""
    connus = set(_numeros())
    cites = set(_RENVOI.findall(JOURNAL.read_text(encoding="utf-8")))
    assert cites <= connus, "renvois vers le vide : %s" % sorted(cites - connus)


def test_chaque_ligne_porte_un_ETAT_lisible():
    """`active` ou `retiree` : une décision sans état ne dit pas si elle
    s'applique encore, et une doctrine qu'on ne sait pas lire n'en est pas une."""
    muettes = []
    for ligne in JOURNAL.read_text(encoding="utf-8").splitlines():
        if not _LIGNE.match(ligne):
            continue
        etat = ligne.rstrip().rstrip("|").rsplit("|", 1)[-1].strip().lower()
        if etat not in ("active", "retiree", "retirée", "remplacee", "remplacée"):
            muettes.append((_LIGNE.match(ligne).group(1), etat[:30]))
    assert muettes == [], "etat illisible : %s" % muettes


#  ═══════════  le gardien voit-il vraiment le defaut ?  ═══════════════════════

def test_le_gardien_REPERE_une_collision_qu_on_lui_montre(tmp_path):
    """Contre-épreuve. Un gardien qui ne connaît qu'une orthographe du défaut
    certifie un fichier qu'il n'a pas lu — D-031, déjà payé une fois."""
    faux = tmp_path / "DECISIONS.md"
    faux.write_text("| D-001 | a | active |\n| D-001 | b | active |\n",
                    encoding="utf-8")
    nums = _LIGNE.findall(faux.read_text(encoding="utf-8"))
    assert sorted({n for n in nums if nums.count(n) > 1}) == ["D-001"]


def test_le_gardien_REPERE_un_trou_qu_on_lui_montre(tmp_path):
    faux = tmp_path / "DECISIONS.md"
    faux.write_text("| D-001 | a | active |\n| D-003 | b | active |\n",
                    encoding="utf-8")
    nums = sorted(int(n[2:]) for n in _LIGNE.findall(faux.read_text(encoding="utf-8")))
    assert sorted(set(range(nums[0], nums[-1] + 1)) - set(nums)) == [2]
