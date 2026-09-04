"""Vertex Test 1.0 — UNE DATE INDICATIVE NE SE FAIT JAMAIS PASSER POUR UN FAIT.

L'audit du 24 août classe P0 le calendrier macro « partiellement fabriqué par
règle » : les dates FOMC sont publiées par la Fed, mais le NFP est déduit du
« premier vendredi » et le CPI **placé au 13** avec `approx=True`.

## Ce qui a été mesuré avant d'écrire ce banc

Deux choses, et la seconde nuance la première.

1. **Aucun des treize hard gates V4 ne consomme les événements macro.** Le pire
   cas décrit par l'audit — « une date approximative lève un hard gate » — n'est
   donc pas actif aujourd'hui. Le dire compte : un correctif qui prétendrait
   fermer une brèche ouverte exagérerait son propre mérite.

2. **Le drapeau `approx` était perdu en route.** `events.build()` construisait
   l'événement macro avec `category='fact'` et `confidence='DECLARED'` — le CPI
   du 13 septembre, inventé par une règle, sortait *identique* à la décision
   FOMC du 16, publiée par la Fed. Il atteint ainsi la proximité d'événements,
   le recouvrement avec les options, et l'écran.

Le lot traite le second point, et pose la garde qui empêchera le premier de
s'ouvrir : le jour où quelqu'un écrira un gate de fenêtre d'événement, il ne
pourra pas accepter en silence une date que personne n'a publiée.
"""
from __future__ import annotations

import pytest

from vertex.data import macro_calendar as M
from vertex.engines import events as E


def _macro(ev):
    return [e for e in ev["events"] if e["kind"] == "macro"]


#  ═════════════  1. la fiabilité de la date traverse la chaîne  ═══════════════

def test_une_date_PUBLIEE_et_une_date_INDICATIVE_ne_se_ressemblent_plus():
    """Le défaut mesuré : le CPI placé au 13 par règle sortait `fact` /
    `DECLARED`, comme la décision FOMC publiée par la Fed."""
    ev = E.build("AAPL", macro=[
        {"kind": "FOMC", "label": "Décision Fed (FOMC)", "date": "2026-09-16",
         "dte": 20, "importance": "haute", "approx": False},
        {"kind": "CPI", "label": "Inflation US (CPI)", "date": "2026-09-13",
         "dte": 17, "importance": "haute", "approx": True},
    ])
    fomc = [e for e in _macro(ev) if e["impact_hint"] == "FOMC"][0]
    cpi = [e for e in _macro(ev) if e["impact_hint"] == "CPI"][0]

    assert fomc["date_fiabilite"] == E.DATE_PUBLIEE
    assert cpi["date_fiabilite"] == E.DATE_INDICATIVE
    assert fomc["category"] == "fact"
    assert cpi["category"] != "fact", (
        "une date que personne n'a publiée n'est pas un fait")
    assert cpi["confidence"] != fomc["confidence"]


def test_le_calendrier_reel_produit_bien_les_deux_natures():
    """Contre-épreuve sur la vraie source, pas sur une fixture : si le
    calendrier cessait de marquer `approx`, ce banc le verrait."""
    ev = E.build("AAPL", macro=M.events(horizon_days=90))
    macro = _macro(ev)
    assert macro, "le calendrier doit produire des événements"
    fiabilites = {e["date_fiabilite"] for e in macro}
    assert E.DATE_PUBLIEE in fiabilites, "FOMC et NFP ont des dates de règle officielle"
    assert E.DATE_INDICATIVE in fiabilites, "le CPI est placé au 13, par convention"


def test_un_evenement_sans_information_de_fiabilite_est_traite_en_INDICATIF():
    """Le sens du doute : une source qui ne dit pas si sa date est publiée ne
    doit pas être crue sur parole. Supposer « publiée » par défaut ferait
    entrer n'importe quelle estimation comme un fait."""
    ev = E.build("AAPL", macro=[
        {"kind": "CPI", "label": "Inflation US", "date": "2026-09-13", "dte": 17},
    ])
    assert _macro(ev)[0]["date_fiabilite"] == E.DATE_INDICATIVE


#  ══════════  2. la garde : une date indicative ne fonde pas un gate  ═════════

def test_une_date_indicative_ne_peut_PAS_fonder_un_hard_gate():
    """La garde que ce lot pose pour l'avenir. Aucun gate V4 ne consomme les
    événements aujourd'hui ; le jour où l'un le fera, il ne pourra pas accepter
    en silence une date que personne n'a publiée."""
    ev = E.build("AAPL", macro=[
        {"kind": "CPI", "label": "CPI", "date": "2026-09-13", "dte": 17,
         "approx": True},
        {"kind": "FOMC", "label": "FOMC", "date": "2026-09-16", "dte": 20,
         "approx": False},
    ])
    cpi, fomc = _macro(ev)[0], _macro(ev)[1]
    assert E.peut_fonder_un_gate(cpi) is False
    assert E.peut_fonder_un_gate(fomc) is True


def test_la_garde_refuse_aussi_ce_qui_n_a_AUCUNE_date():
    """Un événement sans date ne peut pas fonder une fenêtre temporelle : il
    n'y a rien à comparer."""
    assert E.peut_fonder_un_gate(
        {"date": None, "date_fiabilite": E.DATE_PUBLIEE}) is False
    assert E.peut_fonder_un_gate({}) is False


def test_la_garde_n_est_pas_un_refus_generalise():
    """Contre-épreuve : une garde qui refuse tout serait contournée au premier
    besoin réel."""
    assert E.peut_fonder_un_gate(
        {"date": "2026-09-16", "date_fiabilite": E.DATE_PUBLIEE}) is True


#  ═══════════  3. ce que le lot NE prétend pas avoir corrigé  ═════════════════

def test_aucun_hard_gate_V4_ne_consomme_encore_les_evenements():
    """Consigné comme MESURE, pas comme promesse. Si un futur lot branche un
    gate sur les événements, ce test tombera et rappellera qu'il doit passer
    par `peut_fonder_un_gate`."""
    import json
    from pathlib import Path
    profil = json.loads(
        (Path(__file__).resolve().parents[1] / "vertex" / "strategy"
         / "release_profiles" / "vertex_strategy_v4.json").read_text(encoding="utf-8"))
    gates = set(profil.get("hard_gates") or [])
    lies_aux_evenements = {g for g in gates
                           if "EVENT" in g or "EARNINGS_WINDOW" in g}
    assert lies_aux_evenements == set(), (
        "un gate consomme désormais des événements : il DOIT filtrer par "
        "`events.peut_fonder_un_gate`, sinon une date indicative pourrait le "
        "déclencher ou le lever — %s" % sorted(lies_aux_evenements))


def test_le_module_dit_ce_qu_il_ne_corrige_pas():
    """Un correctif qui tait sa portée se lit comme un correctif complet."""
    from pathlib import Path
    src = Path(E.__file__).read_text(encoding="utf-8")
    assert "peut_fonder_un_gate" in src
    assert "indicative" in src.lower()
