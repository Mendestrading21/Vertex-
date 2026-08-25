"""Vertex 1.0 — UN P/E LU AUJOURD'HUI N'EST PAS UNE PREUVE SUR HIER.

`AUDIT-TOTAL-2026-08-25` P0.2 : « une partie des fondamentaux vient encore
d'états actuels Yahoo. Un backtest peut donc voir une révision qui n'était pas
disponible à la date étudiée. »

## Ce qui a été mesuré le 25 août 2026, avant correction

**Aucun horodatage par titre.** `fundamentals.build()` ne portait qu'un
`provenance.as_of` **au niveau du lot**, égal à `utc_now_iso()` — l'instant de
RÉCEPTION du paquet entier. Deux titres, l'un collecté il y a six heures et
l'autre à l'instant, partageaient la même date.

**Un dossier vide indiscernable d'un dossier absent.** `ZZZZ_INEXISTANT` — 404
chez Yahoo — ressortait avec les **quatorze champs à `null` et aucun marqueur
d'erreur**. Strictement identique à un titre réel dont les fondamentaux
manquent. `QUALITY_STANDARD` §1 exige « erreur ou raison de l'absence ».

**Une hypothèse réfutée en la mesurant** : je pensais qu'un symbole en échec
était silencieusement retiré du lot (`if v is not None`). C'est faux —
`yfinance.info` rend un dict même sur 404, donc rien n'est retiré. Le défaut
réel était l'inverse : un dossier bien présent, entièrement vide, et muet.

## La garde, posée AVANT la brèche

Recensement du même jour : **aucun** module d'évaluation historique
(`track_record`, `walk_forward_validation`, `evidence_lab`, `out_of_sample`,
`probability_calibration`) ne lit les fondamentaux. Le pire cas décrit par
l'audit n'est donc pas actif, et le dire évite de prétendre fermer une brèche
ouverte. `exiger_disponibilite()` vaut pour l'avenir : le jour où un score
historique voudra un P/E, il ne pourra pas l'obtenir en silence.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from vertex.storage.point_in_time import (DisponibiliteInconnue,
                                          exiger_disponibilite)

RACINE = Path(__file__).resolve().parents[1]


#  ═══════════  1. ce qu'on ignore reste ignoré  ═══════════════════════════════

def test_une_valeur_sans_date_de_DISPONIBILITE_est_refusee():
    """Le cœur de P0.2. Joindre un P/E courant à une date passée donnerait au
    rétrotest une information que le marché n'avait pas."""
    with pytest.raises(DisponibiliteInconnue):
        exiger_disponibilite({'pe': 31.2, 'available_at': None},
                             contexte='retrotest')


def test_une_valeur_AVEC_date_de_disponibilite_passe():
    """Contre-épreuve : un refus qui refuse tout n'autorise plus rien, et le
    socle point-in-time deviendrait inutilisable."""
    v = {'pe': 31.2, 'available_at': '2026-08-01T23:59:59+00:00'}
    assert exiger_disponibilite(v, contexte='retrotest') is v


def test_le_refus_DIT_que_la_valeur_reste_utilisable_au_PRESENT():
    """Sans cette phrase, un lecteur conclurait que la donnée est fausse. Elle
    ne l'est pas : elle décrit parfaitement le présent, et c'est son usage
    actuel dans la fiche d'un titre."""
    with pytest.raises(DisponibiliteInconnue) as e:
        exiger_disponibilite({'available_at': None}, contexte='x')
    assert 'present' in str(e.value).lower()


def test_le_refus_NOMME_le_contexte():
    """« Date inconnue » sans dire OÙ n'aide personne à corriger."""
    with pytest.raises(DisponibiliteInconnue) as e:
        exiger_disponibilite({'available_at': None},
                             contexte='calibration H20 sur AAPL')
    assert 'calibration H20 sur AAPL' in str(e.value)


#  ═══════════  2. chaque titre porte SA provenance  ═══════════════════════════

def _un(monkeypatch, info):
    from vertex.data_sources import fundamentals as F

    class _Faux:
        def __init__(self, _s):
            pass

        @property
        def info(self):
            if isinstance(info, Exception):
                raise info
            return info

    monkeypatch.setattr(F.yf, 'Ticker', _Faux)
    return F._one('TEST')[1]


def test_chaque_titre_porte_sa_propre_date_de_RECEPTION(monkeypatch):
    """Un `as_of` de lot ne dit rien d'un titre collecté six heures plus tôt."""
    v = _un(monkeypatch, {'trailingPE': 20.0, 'sector': 'Tech'})
    assert v['source'] == 'yfinance.info'
    assert re.match(r'^\d{4}-\d\d-\d\dT', v['recu_a'] or '')


def test_ce_que_la_source_IGNORE_reste_None(monkeypatch):
    """Remplir `observe_a`/`available_at` avec l'instant de réception — l'erreur
    naturelle, et celle que le `as_of` de lot commettait de fait — ferait croire
    qu'un P/E lu aujourd'hui était connaissable aujourd'hui."""
    v = _un(monkeypatch, {'trailingPE': 20.0})
    assert v['observe_a'] is None
    assert v['available_at'] is None


def test_un_fondamental_yfinance_est_donc_REFUSE_comme_preuve_historique(monkeypatch):
    """Les deux moitiés du lot se rejoignent ici."""
    v = _un(monkeypatch, {'trailingPE': 20.0})
    with pytest.raises(DisponibiliteInconnue):
        exiger_disponibilite(v, contexte='retrotest fondamental')


#  ═══════════  3. un dossier vide n'est pas un dossier absent  ════════════════

def test_un_symbole_INCONNU_de_la_source_est_NOMME(monkeypatch):
    """Le cas mesuré : `ZZZZ_INEXISTANT` rendait quatorze `null` et rien d'autre."""
    from vertex.data_sources import fundamentals as F
    monkeypatch.setattr(F, '_one', lambda s: (s, {
        'source': 'yfinance.info', 'recu_a': 'x', 'observe_a': None,
        'available_at': None, 'erreur': None,
        **{c: None for c in ('pe', 'fwd_pe', 'pb', 'peg', 'margin', 'growth',
                             'beta', 'mcap', 'div', 'roe', 'debt_eq', 'sector',
                             'industry', 'name')}}))
    r = F.build(['ZZZZ'])
    assert 'inconnu' in (r['by_sym']['ZZZZ']['erreur'] or '')


def test_un_titre_REEL_partiel_n_est_PAS_declare_inconnu(monkeypatch):
    """Contre-épreuve. Un titre dont seul le P/E manque est un titre réel :
    le déclarer « inconnu de la source » serait une seconde erreur."""
    from vertex.data_sources import fundamentals as F
    monkeypatch.setattr(F, '_one', lambda s: (s, {
        'source': 'yfinance.info', 'recu_a': 'x', 'observe_a': None,
        'available_at': None, 'erreur': None, 'name': 'Vrai Titre',
        'sector': 'Tech', 'pe': None, 'fwd_pe': None, 'pb': None, 'peg': None,
        'margin': None, 'growth': None, 'beta': None, 'mcap': None,
        'div': None, 'roe': None, 'debt_eq': None, 'industry': None}))
    r = F.build(['VRAI'])
    assert r['by_sym']['VRAI']['erreur'] is None


def test_une_collecte_EN_ECHEC_porte_son_motif(monkeypatch):
    v = _un(monkeypatch, RuntimeError('reseau coupe'))
    assert 'reseau coupe' in (v['erreur'] or '')
    assert v['recu_a'], "l instant de la TENTATIVE reste mesure"


#  ═══════════  4. une médiane dit sur quoi elle porte  ════════════════════════

def test_les_medianes_sectorielles_comptent_les_ECARTES(monkeypatch):
    """Une médiane calculée sur trois titres d'un secteur qui en compte
    quarante n'est pas la médiane du secteur. Sans ces comptes, un lot à
    moitié muet produit un repère qui a l'air aussi solide qu'un lot complet."""
    from vertex.data_sources import fundamentals as F
    base = {'source': 'y', 'recu_a': 'x', 'observe_a': None,
            'available_at': None, 'sector': 'Tech', 'fwd_pe': None,
            'margin': None, 'growth': None}
    lots = {'A': {**base, 'pe': 10.0, 'erreur': None},
            'B': {**base, 'pe': 20.0, 'erreur': None},
            'C': {**base, 'pe': None, 'erreur': 'symbole inconnu'}}
    monkeypatch.setattr(F, '_one', lambda s: (s, lots[s]))
    sec = F.build(['A', 'B', 'C'])['by_sector']['Tech']
    assert sec['n'] == 3
    assert sec['n_pe'] == 2, "la mediane ne porte que sur les P/E REELS"
    assert sec['n_ecartes'] == 1


#  ═══════════  5. la garde est posée AVANT la brèche  ═════════════════════════

#: Les modules qui évaluent le PASSÉ. Y lire un fondamental non daté serait le
#: look-ahead que P0.2 rend impossible.
_EVALUATEURS = (
    'vertex/engines/track_record.py',
    'vertex/engines/walk_forward_validation.py',
    'vertex/engines/evidence_lab.py',
    'vertex/validation/out_of_sample.py',
    'vertex/validation/probability_calibration.py',
)


def test_aucun_evaluateur_historique_ne_lit_les_fondamentaux():
    """Recensé le 25 août 2026 : aucun ne le fait. Le dire évite de prétendre
    fermer une brèche ouverte — et ce banc tombera le jour où l'un d'eux en
    branchera un sans passer par `exiger_disponibilite`."""
    coupables = []
    for rel in _EVALUATEURS:
        f = RACINE / rel
        assert f.is_file(), 'evaluateur introuvable : %s' % rel
        src = f.read_text(encoding='utf-8')
        if re.search(r'\bfundamentals\b', src) and 'exiger_disponibilite' not in src:
            coupables.append(rel)
    assert coupables == [], (
        "ces evaluateurs du PASSE lisent un fondamental sans exiger sa date de "
        "disponibilite : %s" % coupables)


def test_le_recensement_des_evaluateurs_n_est_pas_VIDE():
    """Sans ce contrôle, la garde ci-dessus passerait sur zéro fichier et
    n'aurait jamais rien gardé."""
    assert len(_EVALUATEURS) >= 5
    for rel in _EVALUATEURS:
        assert (RACINE / rel).is_file(), rel


def test_le_gardien_VOIT_un_evaluateur_fautif_qu_on_lui_montre():
    """Contre-épreuve. Un gardien qui ne trouve jamais rien passerait pour un
    gardien qui garde — D-031, déjà payé deux fois."""
    faux = "from vertex.data_sources import fundamentals\npe = fundamentals.build(['AAPL'])"
    assert re.search(r'\bfundamentals\b', faux)
    assert 'exiger_disponibilite' not in faux


def test_le_gardien_NE_signale_PAS_un_evaluateur_qui_EXIGE_la_date():
    """Contre-épreuve inverse : un gardien qui refuse aussi la correction est
    désactivé au premier commit pressé."""
    bon = ("from vertex.data_sources import fundamentals\n"
           "from vertex.storage.point_in_time import exiger_disponibilite\n"
           "exiger_disponibilite(v, contexte='calibration')")
    assert re.search(r'\bfundamentals\b', bon) and 'exiger_disponibilite' in bon
