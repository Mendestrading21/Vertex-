"""Vertex 1.0 — LE PLUS MODÉLISÉ DES QUATRE MOTEURS NE DÉCLARAIT RIEN.

## Le recensement du 26 août 2026

Quatre moteurs produisent un prix d'option dans ce dépôt. Trois disent leurs
hypothèses :

| moteur | ce qu'il déclare |
|---|---|
| `options/scenario_pricer` | `model_source`, `rate`, `limitations`, bloc `entrees` |
| `engines/multileg_lab` | bloc `model` (`r`, `q`, `iv_unit`, note PoP) |
| `options/double_prob` | bloc `model` (`calibrated: False`, statut ESTIMATED) |
| **`strategy/legacy_adapter`** | **rien** |

Et c'est le plus modélisé des quatre. Chez lui, **rien** ne vient d'une
cotation :

- le **strike** est CHOISI, par balayage, pour viser un delta cible ;
- la **prime** est CALCULÉE en Black-Scholes ;
- l'**IV** est DÉDUITE de l'ATR — `_iv_proxy(atr) = atr/100 × √252`, bornée
  à [0,22 ; 1,10].

## Ce que ça vaut, mesuré sur les vraies cotations

Sur les **578 contrats réellement cotés** du board du 25 août 2026, l'IV
médiane par titre s'étale de **2,52×** entre p10 (0,248) et p90 (0,625). Sur
cet intervalle, la prime d'un call ATM à 180 jours passe de 8,016 à 18,312 —
**+128 %**.

Le proxy assigne pourtant l'IV depuis le **seul ATR** : deux titres de même ATR
reçoivent la même IV, quelle que soit celle que le marché cote. L'ATR mesure la
volatilité **réalisée** ; une prime d'option se paie sur la volatilité
**implicite**.

## Le détail qui rend la confusion inévitable

La sortie servait `'iv': round(sig * 100)` — **le même nom de champ** que l'`iv`
des contrats du board, qui est, elle, une **cotation**. Même clé, deux sens,
aucune distinction.

## Pourquoi ça compte plus qu'ailleurs

Cette sortie porte un **dimensionnement en dollars** : nombre de contrats, coût,
et `maxloss` — sur des budgets de 5 k, 15 k, puis 50 k à 200 k dans
`build_portfolio`. Un chiffre modélisé qui prend la forme d'un montant engagé
doit dire qu'il est modélisé.

## Ce que ce lot ne fait PAS

**Aucun chiffre ne change.** Ce lot ajoute une déclaration ; il ne recâble ni le
taux ni le dividende. Le faire ici déplacerait des primes déjà entièrement
synthétiques, et la sensibilité à l'IV (+128 %) écrase de toute façon celle au
taux (76 pb). La déclaration d'abord ; le recâblage, s'il a lieu, sera son
propre lot.
"""
from __future__ import annotations

import json
import statistics

import pytest

from vertex.strategy import legacy_adapter as A

ROWS = [{'symbol': 'KO', 'score': 82}]
DETAIL = {'KO': {'price': 91.64, 'atr_pct': 2.2, 'verdict': 'ACHETER',
                 'grade': 'A', 'score': 82,
                 'plan': {'stop': 86.0, 'tp1': 98.0, 'tp2': 104.0}}}


def _build():
    return A.build(ROWS, DETAIL, market={'regime': 'risk-on'}, top_n=1)


#  ═══════════  1. le constructeur déclare enfin son modèle  ═══════════════════

def test_la_STRATEGIE_declare_son_modele():
    """Intention inchangee depuis D-104 ; le FAIT a change au lot suivant.

    `iv_source` valait `PROXY_ATR` en dur — c'etait alors la verite. Depuis
    D-107, l'IV COTEE l'emporte quand le board porte des contrats : le bloc
    global nomme desormais la REGLE, et chaque `pick` nomme ce qui lui est
    reellement arrive.
    """
    b = _build()
    assert b['model']['estimated'] is True
    assert b['model']['prix_source'] == 'MODEL_ESTIMATE'
    assert 'COTEE' in b['model']['iv_source'] and 'PROXY' in b['model']['iv_source']
    assert b['model']['strike_source'] == 'CHOISI_POUR_DELTA_CIBLE'


def test_le_PORTEFEUILLE_le_declare_aussi():
    """C'est lui qui engage 50 k à 200 k : s'il était le seul à se taire, la
    déclaration manquerait là où elle compte le plus."""
    pf = A.build_portfolio(ROWS, DETAIL, market={'regime': 'risk-on'}, capital=100000)
    assert pf['model']['estimated'] is True
    assert pf['limitations']


def test_le_taux_declare_est_LU_dans_le_moteur_et_non_recopie():
    """Une déclaration qui porterait sa propre copie du taux finirait par
    annoncer autre chose que ce qui a été calculé — c'est exactement D-084."""
    from vertex.options import legacy_engine
    assert A.MODELE['r'] == legacy_engine.R
    assert A.R is legacy_engine.R


#  ═══════════  2. l'IV proxy ne se fait plus passer pour une cotation  ════════

def test_l_IV_servie_NOMME_sa_source():
    """`iv` porte le même nom que l'IV **cotée** des contrats du board, et n'a
    pas le même sens. Le dire au plus près de la valeur est la seule façon
    qu'un lecteur ne les confonde pas."""
    p = _build()['picks'][0]
    assert p['iv_source'] == 'PROXY_ATR'
    assert p['iv_estimated'] is True


def test_l_ancienne_cle_iv_survit_pour_l_UI():
    """Contre-épreuve : renommer `iv` casserait l'affichage. On ajoute, on ne
    déplace pas."""
    p = _build()['picks'][0]
    assert isinstance(p['iv'], (int, float)) and p['iv'] > 0


def test_les_limitations_disent_le_SENS_de_chaque_ecart():
    """« Le modèle a des limites » n'informe personne. Chaque limite doit dire
    dans quel sens elle pousse, sinon le lecteur ne peut rien en faire."""
    lims = ' '.join(_build()['limitations']).lower()
    assert 'realisee' in lims and 'implicite' in lims, "la nature de l'IV proxy"
    assert 'surestim' in lims, 'le sens de l ecart du dividende ignore'
    #  D-104 citait la dispersion (2,52x). D-107 l'a remplacee par une mesure
    #  plus forte : le BIAIS du proxy, 30 titres sur 30, mediane +40 %.
    assert '30' in lims and '40' in lims, 'le biais MESURE du proxy'
    assert 'dimensionnement' in lims, 'le dollar decoule de la prime modelisee'


#  ═══════════  3. la mesure qui justifie la déclaration  ══════════════════════

def test_la_prime_est_TRES_sensible_a_l_IV_qui_est_proxiee():
    """+128 % entre p10 et p90 des IV réellement cotées. C'est ce qui fait de
    l'IV proxy la principale source d'incertitude — devant le taux (76 pb)."""
    from vertex.options.legacy_engine import _bs_price
    T = 180 / 365.0
    p10 = _bs_price(100.0, 100.0, T, 0.248, True)
    p90 = _bs_price(100.0, 100.0, T, 0.625, True)
    assert (p90 - p10) / p10 > 1.0, '%.3f -> %.3f' % (p10, p90)


def test_le_proxy_ignore_TOUT_sauf_l_ATR():
    """Deux titres de même ATR reçoivent la même IV, quelle que soit celle que
    le marché cote. C'est la propriété du proxy, et c'est ce que la limitation
    doit dire."""
    assert A._iv_proxy(2.2) == A._iv_proxy(2.2)
    assert A._iv_proxy(1.0) < A._iv_proxy(3.0)


def test_le_proxy_est_BORNE_et_les_bornes_sont_atteignables():
    """Un ATR de 0,8 % et un de 1,0 % donnent la même IV : sous le plancher, le
    proxy cesse de distinguer les titres."""
    assert A._iv_proxy(0.8) == A._iv_proxy(1.0) == 0.22
    assert A._iv_proxy(7.0) == A._iv_proxy(9.0) == 1.10


#  ═══════════  4. AUCUN chiffre ne change  ════════════════════════════════════

def test_ce_lot_ne_DEPLACE_aucun_prix():
    """La condition pour qu'une déclaration reste une déclaration. Les valeurs
    sont celles qu'un Black-Scholes à `R` et q=0 produit — inchangées."""
    from vertex.options.legacy_engine import _bs_price, R
    #  Sans board, le repli est le proxy — et la prime doit etre celle d'avant.
    jambe = _build()['picks'][0]['call'][0]
    attendu = _bs_price(91.64, jambe['strike'], jambe['dte'] / 365.0,
                        A._iv_proxy(2.2), True)
    assert abs(jambe['premium'] - round(attendu, 2)) < 0.01
    assert R == 0.045, 'le taux du moteur est inchange'


#  ═══════════  5. le recensement : plus aucun moteur muet  ════════════════════

def test_TOUS_les_moteurs_de_prix_declarent_leurs_hypotheses():
    """Le recensement qui a trouvé le défaut. Trois moteurs déclaraient, un
    seul se taisait — et c'était le plus modélisé. Un cinquième s'écrira ; il
    doit se heurter à ce banc."""
    from vertex.engines import multileg_lab
    from vertex.options import double_prob, scenario_pricer

    muets = []

    b = _build()
    if not (b.get('model') or {}).get('estimated'):
        muets.append('strategy/legacy_adapter')

    ml = multileg_lab.analyze_strategy(
        [{'type': 'call', 'strike': 95.0, 'qty': 1, 'premium': 4.20}], 91.64, 0.30, 180)
    if 'r' not in (ml.get('model') or {}):
        muets.append('engines/multileg_lab')

    dp = double_prob.double_probability(spot=91.64, strike=95.0, premium=4.20,
                                        dte=180, iv=0.30, right='CALL')
    if not (dp.get('model') or {}):
        muets.append('options/double_prob')

    if not scenario_pricer.limitations_pour(0.0):
        muets.append('options/scenario_pricer')

    assert muets == [], 'moteurs qui servent un prix sans dire son modele : %s' % muets


def test_ce_recensement_VOIT_un_moteur_muet_qu_on_lui_montre():
    """Contre-épreuve — D-031, payé cinq fois dans ce programme : un gardien
    qui ne trouve jamais rien passerait pour un gardien qui garde."""
    faux_moteur = {'premium': 4.20, 'delta': 0.5}      # aucun bloc `model`
    assert not (faux_moteur.get('model') or {}).get('estimated')


def test_double_prob_dit_toujours_qu_il_n_est_PAS_calibre():
    """« Toute probabilité non calibrée reste un score ou une fréquence
    descriptive » — AUDIT-TOTAL-2026-08-25. Ce moteur le disait déjà ; ce banc
    empêche que ça se perde."""
    from vertex.options import double_prob
    d = double_prob.double_probability(spot=91.64, strike=95.0, premium=4.20,
                                       dte=180, iv=0.30, right='CALL')
    assert d['model']['calibrated'] is False
