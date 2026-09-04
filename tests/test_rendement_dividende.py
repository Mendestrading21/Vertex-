"""Vertex Test 1.0 — 0,35 % ÉTAIT LU COMME 35 %, ET ÇA CHANGEAIT LA TAILLE DE POSITION.

## Mesuré le 26 août 2026, sur la vraie source

`yfinance 1.5.2`, appel réel :

```text
KO     dividendYield=2.3    trailingAnnualDividendYield=0.022611
MO     dividendYield=6.19   trailingAnnualDividendYield=0.061925
AAPL   dividendYield=0.35   trailingAnnualDividendYield=0.003383
GOOGL  dividendYield=0.25   trailingAnnualDividendYield=0.002442
```

`dividendYield` est un **pourcentage**. `trailingAnnualDividendYield` est une
**fraction**. Les deux unités coexistent dans la même charge : n'importe quel
relecteur peut vérifier « yfinance rend une fraction » et avoir raison — sur
l'autre champ. C'est ce qui rend le piège durable.

Or `fundamentals.py` publiait le champ ambigu brut, et `analysis.py` le testait
contre `0.02` — seuil écrit pour une fraction, « rendement ≥ 2 % ». Il devenait
« ≥ 0,02 % ».

## Ce que ça produisait

- AAPL (0,35 %) et GOOGL (0,25 %) touchaient le **bonus défensif maximal**, au
  même titre que MO à 6,19 %.
- La branche de repli `else (1 if _div else 0)` exigeait `0 < div < 0,02`, soit
  un rendement réel sous **0,02 %** : **branche morte**.
- Balayage de 3 780 configurations réalistes : **900 bascules de verdict**
  (24 %), dans les dix secteurs. Pour AAPL et GOOGL, **13 conditions de marché
  sur 25** donnent DÉFENSIF là où la règle voulait ÉQUILIBRÉ.

`profile` alimente `decision_stack` : gate d'une décision d'option, et
`_size_hint` — la **taille de position** affichée (`STRONG_BUY` : 5-8 % en
OFFENSIF contre 4-6 % en DÉFENSIF).

## Le second défaut : une phrase qui affirmait ce qui n'avait pas lieu

`scenario_pricer.LIMITATIONS` déclarait, dans **chaque** réponse servie :

> « dividendes intégrés via un rendement continu »

Aucun appelant de production ne renseigne `UnderlyingSetup.dividend_yield` :
les deux sites (`options_intel_api`, `redesign`) construisent le setup sans ce
champ, qui vaut donc `0.0`. Seuls des bancs le passaient. Le produit affirmait
intégrer un dividende qu'il n'appliquait jamais — **exactement D-084**, où
l'écran de sécurité promettait une restriction absente.

Mesuré, DTE 180 (la cible du mandat), ATM, IV 30 % : ignorer 3 % de rendement
surévalue le call de **8,9 %** ; 7 % le surévalue de **19,8 %**. L'écart va
dans le sens qui flatte une thèse d'achat.
"""
from __future__ import annotations

import math

from vertex.data_sources import rendement_dividende as R

#: Charges REELLES mesurees le 26 aout 2026 (yfinance 1.5.2), et la fraction
#: attendue. Ce ne sont pas des exemples inventes : ce sont les quatre appels.
_MESURES = [
    ('KO', {'dividendYield': 2.3, 'trailingAnnualDividendYield': 0.022611152,
            'dividendRate': 2.12, 'currentPrice': 91.64}, 0.0226),
    ('MO', {'dividendYield': 6.19, 'trailingAnnualDividendYield': 0.061924927,
            'dividendRate': 4.24, 'currentPrice': 68.07}, 0.0619),
    ('AAPL', {'dividendYield': 0.35, 'trailingAnnualDividendYield': 0.003383386,
              'dividendRate': 1.08, 'currentPrice': 309.9}, 0.0034),
    ('GOOGL', {'dividendYield': 0.25, 'trailingAnnualDividendYield': 0.0024421078,
               'dividendRate': 0.88, 'currentPrice': 346.96}, 0.0024),
]


#  ═══════════  1. l'unité, sur les charges réellement mesurées  ═══════════════

def test_les_quatre_charges_REELLES_rendent_la_bonne_fraction():
    for sym, info, attendu in _MESURES:
        r = R.rendement(info)
        assert abs(r['valeur'] - attendu) < 5e-4, '%s : %r' % (sym, r)
        assert r['unite'] == R.FRACTION


def test_le_champ_NON_AMBIGU_est_prefere_et_l_unite_n_est_pas_deduite():
    """Tant qu'un champ non ambigu accompagne la charge, rien n'est inféré —
    et c'est le cas des quatre titres mesurés."""
    for sym, info, _ in _MESURES:
        r = R.rendement(info)
        assert r['source'] == 'trailingAnnualDividendYield', sym
        assert r['unite_inferee'] is False, sym


def test_AAPL_ne_vaut_plus_35_pourcent():
    """Le défaut, dit dans son cas le plus net : 0,35 % lu comme 35 %."""
    valeur = R.valeur(dict(_MESURES[2][1]))
    assert valeur < 0.01, 'AAPL rendrait %.2f %% par an' % (valeur * 100)


#  ═══════════  2. la reconstruction, quand le champ sûr manque  ═══════════════

def test_sans_champ_sur_le_rendement_se_RECONSTRUIT_du_montant_et_du_prix():
    """Deux grandeurs dont l'unité ne se discute pas."""
    r = R.rendement({'dividendYield': 2.3, 'dividendRate': 2.12, 'currentPrice': 91.64})
    assert r['source'] == 'dividendRate/prix'
    assert r['unite_inferee'] is False
    assert abs(r['valeur'] - 2.12 / 91.64) < 1e-9


def test_le_champ_AMBIGU_SEUL_est_utilise_mais_se_DECLARE_infere():
    """Rien dans la charge ne tranche entre 35 % et 0,35 %. La lecture retenue
    est celle des versions observées — mais elle est étiquetée, jamais
    présentée comme mesurée."""
    r = R.rendement({'dividendYield': 0.35})
    assert r['unite_inferee'] is True
    assert r['motif'] and 'ambigu' in r['motif']
    assert abs(r['valeur'] - 0.0035) < 1e-9


def test_une_valeur_hors_de_tout_rendement_plausible_est_REFUSEE():
    """Convertir au hasard produirait un chiffre plausible et faux — la pire
    espèce. `None` avec un motif est préférable."""
    r = R.rendement({'dividendYield': 900.0})
    assert r['valeur'] is None
    assert r['motif'] and 'plausible' in r['motif']


#  ═══════════  3. zéro n'est pas l'inconnu  ═══════════════════════════════════

def test_un_titre_qui_ne_verse_RIEN_rend_zero_et_non_None():
    """Même distinction qu'en D-081 pour l'open interest : les confondre ferait
    passer « je ne sais pas » pour « il ne verse pas »."""
    r = R.rendement({'dividendYield': 0.0})
    assert r['valeur'] == 0.0
    assert r['unite_inferee'] is False


def test_une_charge_SANS_rendement_rend_None_avec_un_motif():
    r = R.rendement({})
    assert r['valeur'] is None
    assert r['motif']


def test_les_entrees_illisibles_ne_font_pas_tomber_le_module():
    for charge in (None, {'dividendYield': 'n/d'}, {'dividendYield': float('nan')},
                   {'dividendYield': -3.0}, {'trailingAnnualDividendYield': 'x'}):
        r = R.rendement(charge)
        assert r['valeur'] is None or (isinstance(r['valeur'], float)
                                       and math.isfinite(r['valeur']))


#  ═══════════  4. le producteur publie bien une fraction  ═════════════════════

def test_les_fondamentaux_publient_la_FRACTION_et_sa_provenance(monkeypatch):
    """Le champ `div` que consomme `analysis.py` doit être dans l'unité que son
    seuil suppose — c'est tout le défaut."""
    from vertex.data_sources import fundamentals as F

    class _Faux:
        info = {'dividendYield': 2.3, 'trailingAnnualDividendYield': 0.022611152,
                'sector': 'Consumer Defensive', 'shortName': 'Coca-Cola'}

    monkeypatch.setattr(F.yf, 'Ticker', lambda s: _Faux())
    _s, v = F._one('KO')
    assert abs(v['div'] - 0.0226) < 5e-4, 'div=%r (le seuil 0.02 vaut 2 %%)' % v['div']
    assert v['div_source'] == 'trailingAnnualDividendYield'
    assert v['div_unite_inferee'] is False


def test_le_producteur_ne_lit_PLUS_le_champ_ambigu_directement():
    """Route par route, le troisième producteur héritera du piège. Un seul
    propriétaire de l'unité, et les producteurs le lisent."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parents[1]
    for chemin in ('vertex/data_sources/fundamentals.py', 'vertex/data/company.py'):
        src = (racine / chemin).read_text(encoding='utf-8')
        assert "info.get('dividendYield')" not in src, (
            '%s lit le champ ambigu au lieu du proprietaire' % chemin)
        assert '_rdt' in src, '%s ne passe pas par le proprietaire' % chemin


#  ═══════════  5. le seuil de profil redevient celui qui était voulu  ═════════

def test_le_seuil_defensif_separe_de_nouveau_MO_de_GOOGL():
    """Le cœur de l'impact : `analysis.py` accorde le bonus défensif plein à
    partir de 2 %. Avec le champ brut, GOOGL (0,25 %) le touchait comme MO
    (6,19 %)."""
    mo = R.valeur(dict(_MESURES[1][1]))
    googl = R.valeur(dict(_MESURES[3][1]))
    assert mo >= 0.02, 'MO verse 6,19 %% : il DOIT avoir le bonus plein'
    assert 0 < googl < 0.02, 'GOOGL verse 0,25 %% : bonus partiel, pas plein'


def test_la_branche_de_repli_du_profil_est_de_nouveau_ATTEIGNABLE():
    """Elle exigeait `0 < div < 0.02`, soit un rendement réel sous 0,02 % :
    aucun titre n'y tombait. Une branche morte n'est pas une règle."""
    atteignent = [s for s, info, _ in _MESURES
                  if 0 < (R.valeur(dict(info)) or 0) < 0.02]
    assert atteignent, 'aucun titre reel n atteint la branche : elle est morte'
    assert 'AAPL' in atteignent and 'GOOGL' in atteignent


#  ═══════════  6. le simulateur ne promet plus ce qu'il ne fait pas  ══════════

def test_sans_dividende_le_simulateur_AVOUE_qu_il_n_en_applique_aucun():
    """Le défaut D-084 rejoué sur le pricing : la phrase était écrite d'avance,
    et affirmait ce qui n'avait pas lieu."""
    from vertex.options import scenario_pricer as S
    lignes = S.limitations_pour(0.0)
    assert any('NON pris en compte' in x for x in lignes)
    assert any('SURESTIM' in x for x in lignes), (
        "le sens de l'erreur doit etre dit : la prime d'un call est surevaluee")
    assert not any('dividende pris en compte' in x for x in lignes)


def test_avec_un_dividende_le_simulateur_le_dit_ET_donne_sa_valeur():
    """Contre-épreuve : une phrase qui n'annonce jamais rien ne renseigne pas
    davantage que celle qui annonçait toujours tout."""
    from vertex.options import scenario_pricer as S
    lignes = S.limitations_pour(0.03)
    assert any('dividende pris en compte' in x and '3.00' in x for x in lignes)
    assert not any('NON pris en compte' in x for x in lignes)


def test_la_simulation_REELLE_porte_l_aveu(monkeypatch):
    """Sur le produit, pas seulement sur la fonction : c'est la réponse servie
    qui portait la fausse promesse."""
    from vertex.options import scenario_pricer as S
    from vertex.options.models import UnderlyingSetup
    contrat = {'symbol': 'KO', 'right': 'C', 'strike': 95.0, 'dte': 180,
               'mid': 4.2, 'iv': 0.30, 'expiry': '2027-02-19'}
    sim = S.simulate(contrat, UnderlyingSetup(symbol='KO', spot=91.64))
    assert any('NON pris en compte' in x for x in sim['limitations'])


def test_le_refus_pour_DTE_absent_porte_la_MEME_verite():
    """Une réponse refusée qui décrirait un autre modèle que la réponse servie
    rendrait les deux illisibles."""
    from vertex.options import scenario_pricer as S
    from vertex.options.models import UnderlyingSetup
    sim = S.simulate({'symbol': 'KO', 'right': 'C', 'strike': 95.0, 'dte': None,
                      'mid': 4.2, 'iv': 0.30}, UnderlyingSetup(symbol='KO', spot=91.64))
    assert any('NON pris en compte' in x for x in sim['limitations'])


def test_la_phrase_n_est_plus_ecrite_d_avance():
    """La cause n'était pas le texte : c'est qu'il ne dérivait pas de l'état
    qu'il décrit. S'il retourne dans la constante, il rementira — D-085."""
    from vertex.options import scenario_pricer as S
    assert not any('dividende' in x.lower() for x in S.LIMITATIONS), (
        'la phrase est de nouveau figee dans LIMITATIONS')


#  ═══════════  7. l'écart que le silence cachait  ═════════════════════════════

def test_ignorer_le_dividende_SUREVALUE_un_call_et_la_mesure_le_montre():
    """Ce que la fausse promesse recouvrait. DTE 180 — la cible du mandat — est
    le pire cas : l'effet du rendement croît avec l'échéance."""
    from vertex.options import scenario_pricer as S
    T = 180 / 365.0
    sans = S.bs_price(100.0, 100.0, T, 0.30, 0.045, 'C', 0.0)
    avec = S.bs_price(100.0, 100.0, T, 0.30, 0.045, 'C', 0.03)
    ecart = (sans - avec) / avec
    assert ecart > 0.08, 'ecart mesure %.1f %%' % (ecart * 100)


def test_l_effet_du_dividende_CROIT_avec_l_echeance():
    """Ce qui rend le défaut le plus grave précisément sur l'horizon visé par
    le produit : DTE préféré 120–240, cible 180."""
    from vertex.options import scenario_pricer as S
    ecarts = []
    for dte in (30, 90, 180, 240):
        T = dte / 365.0
        sans = S.bs_price(100.0, 100.0, T, 0.30, 0.045, 'C', 0.0)
        avec = S.bs_price(100.0, 100.0, T, 0.30, 0.045, 'C', 0.03)
        ecarts.append((sans - avec) / avec)
    assert ecarts == sorted(ecarts), ecarts
