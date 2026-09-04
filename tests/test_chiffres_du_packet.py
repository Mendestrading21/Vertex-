"""Vertex Test 1.0 — L'IA POUVAIT ÉNONCER UN PRIX QUI N'EXISTAIT NULLE PART.

`CLAUDE.md`, interdit absolu n°1 pour l'IA :

> inventer prix/prime/Greek/probabilité/source

`VERTEX-INTELLIGENCE-2.0` Phase 4, critère d'acceptation : « aucune synthèse IA
sans citations internes du packet ».

## Le défaut, mesuré le 26 août 2026

Le prompt système interdit à l'IA de **calculer**. `response_validator`
interdisait le langage de certitude, les clés d'ordre et les tentatives de
recalcul de score. **Rien** n'empêchait le modèle d'**énoncer** un chiffre
absent du packet.

Sur un packet réel `{price: 309.90, score: 82, plan: {stop: 290.0, tp1: 330.0}}`
et une réponse qui invente :

```text
"AAPL cote 412,50 $ et affiche un P/E de 19,4. Objectif 480 $."
"La probabilite de hausse est de 87 %, avec un delta de 0,73."

validate_analysis -> valide ? True     erreurs : AUCUNE
```

Un prix, un P/E, un objectif, une probabilité et un Greek — **cinq chiffres
inventés, tous acceptés**. Une règle que rien n'applique est une intention, et
celle-ci était l'interdit numéro un.

## La ligne entre donnée et prose

Exiger que **tout** nombre figure dans le packet rendrait le garde-fou
inutilisable : « les **3** scénarios », « d'ici **2027** » sont de la prose. Un
garde-fou qui refuse la prose est désactivé au premier usage — D-088.

Un nombre doit être sourcé quand il **se présente comme une donnée** : unité
(`$`, `%`, `€`), partie décimale, ou valeur au-delà de 31. Les années restent
de la prose.

Et un **arrondi d'affichage n'est pas une invention** : le packet porte
`309.90`, écrire « 310 $ » est fidèle. Un facteur 100 non plus : `0.0226` dans
le packet s'écrit « 2,26 % » dans une phrase.

## Ce que ce lot ne garantit pas

Il ne vérifie pas que la phrase est **vraie**, seulement que ses chiffres
viennent du packet. Un modèle peut citer le bon prix dans une phrase fausse.
Le dire évite de faire passer ce garde-fou pour une garantie de véracité.
"""
from __future__ import annotations

import pytest

from vertex.ai.chiffres import non_sourcees, nombres_du_packet
from vertex.ai.response_validator import validate_analysis

PACKET = {'price': 309.90, 'score': 82, 'verdict': 'ACHETER',
          'plan': {'stop': 290.0, 'tp1': 330.0, 'tp2': 350.0},
          'div': 0.0226, 'greeks': {'delta': 0.58, 'theta': -2.23},
          'scenarios': [{'nom': 'BASE', 'gain_pct': 105.6}]}


def _valeurs(texte):
    return [x['valeur'] for x in non_sourcees(texte, PACKET)]


#  ═══════════  1. les chiffres inventés sont ATTRAPÉS  ════════════════════════

@pytest.mark.parametrize('texte,attendu', [
    ('AAPL cote 412,50 $', 412.5),
    ('affiche un P/E de 19,4', 19.4),
    ("Objectif 480 $ d'ici mars", 480.0),
    ('La probabilite de hausse est de 87 %', 87.0),
    ('avec un delta de 0,73', 0.73),
])
def test_un_chiffre_ABSENT_du_packet_est_signale(texte, attendu):
    """Les cinq chiffres exacts de la mesure du 26 août 2026."""
    assert attendu in _valeurs(texte), texte


def test_un_chiffre_invente_dans_une_CONTRADICTION_est_attrape():
    """`contradictions` est une liste : ne regarder que les chaînes de premier
    niveau laisserait passer un chiffre inventé là où le lecteur cherche
    précisément un fait."""
    ok, err = validate_analysis({
        'summary': 'RAS', 'bull_case': 'RAS', 'bear_case': 'RAS',
        'contradictions': ['Le moteur A donne 45 % quand B donne 12 %.'],
        'anomaly_reading': 'RAS', 'confidence_comment': 'RAS'}, packet=PACKET)
    assert ok is False
    assert any('45' in e for e in err) and any('12' in e for e in err)


def test_le_rejet_NOMME_le_champ_et_l_extrait():
    """« Invalide » n'aide personne à corriger. Le champ et la phrase, si."""
    _, err = validate_analysis({
        'summary': 'AAPL cote 412,50 $', 'bull_case': 'x', 'bear_case': 'x',
        'contradictions': [], 'anomaly_reading': 'x',
        'confidence_comment': 'x'}, packet=PACKET)
    assert any('summary' in e and '412.5' in e and 'cote' in e for e in err), err


#  ═══════════  2. le fidèle et la prose PASSENT  ══════════════════════════════

@pytest.mark.parametrize('texte', [
    'AAPL cote 309,90 $',                      # exact
    'AAPL cote 310 $',                         # arrondi d'affichage
    'stop a 290 $, cible 330 $',               # champs imbriques du plan
    'score de 82',
    'delta de 0,58',                           # greek du packet
    'theta de -2,23',
    'rendement de 2,26 %',                     # 0.0226 exprime en pourcent
    'gain de base 105,6 %',                    # valeur dans une liste
    'les 3 scenarios et 2 contradictions',     # prose : petits comptes
    "d'ici 2027, la these tient",              # prose : annee
    'Le titre reste bien oriente.',            # aucun chiffre
])
def test_un_texte_FIDELE_ou_de_la_prose_ne_declenche_rien(texte):
    """Contre-épreuve indispensable : un garde-fou qui refuse la prose ou les
    arrondis serait désactivé au premier usage (D-088)."""
    assert _valeurs(texte) == [], texte


def test_une_reponse_entierement_fidele_reste_VALIDE():
    ok, err = validate_analysis({
        'summary': 'AAPL cote 309,90 $, stop a 290 $.',
        'bull_case': 'Cible 330 $ puis 350 $.',
        'bear_case': 'Sous 290 $ la these tombe.',
        'contradictions': [], 'anomaly_reading': 'Score de 82.',
        'confidence_comment': 'Les 3 scenarios tiennent.'}, packet=PACKET)
    assert ok is True, err


#  ═══════════  2 bis. le signe négatif, défaut trouvé en écrivant ce lot  ════

def test_un_THETA_negatif_du_packet_n_est_pas_accuse():
    """Défaut de ma première version : le signe n'était pas lu, donc `-2,23`
    était comparé à `2,23`. Le packet portant `-2.23`, **tout theta** — qui est
    toujours négatif — aurait été signalé comme inventé. Un garde-fou qui crie
    sur chaque theta est retiré dans la semaine."""
    assert _valeurs('theta de -2,23') == []


def test_un_theta_negatif_INVENTE_reste_attrape():
    """Contre-épreuve : corriger le signe ne doit pas rendre le contrôle aveugle
    aux valeurs négatives."""
    assert -9.99 in _valeurs('theta de -9,99')


def test_un_INTERVALLE_n_est_pas_lu_comme_un_negatif():
    """« 290-330 $ » : le tiret sépare deux bornes, il ne rend pas la seconde
    négative. Le lire comme un signe inventerait un `-330` absent du packet."""
    assert _valeurs('fourchette 290-330 $') == []


#  ═══════════  3. le packet est parcouru EN ENTIER  ═══════════════════════════

def test_le_parcours_atteint_les_valeurs_IMBRIQUEES():
    """Un garde-fou qui n'inspecterait que `price` et `score` accuserait le
    modèle d'inventer une valeur qui figure ailleurs dans le dossier."""
    connues = nombres_du_packet(PACKET)
    for attendu in (309.90, 82, 290.0, 330.0, 0.58, -2.23, 105.6):
        assert attendu in connues, attendu


def test_un_nombre_ECRIT_dans_une_chaine_du_packet_compte():
    """Le packet porte aussi du texte — un chiffre qui y figure n'est pas
    inventé pour autant."""
    p = {'note': 'objectif consensus 412,50 $'}
    assert non_sourcees('la cible consensus est 412,50 $', p) == []


def test_un_BOOLEEN_du_packet_n_est_pas_lu_comme_un_nombre():
    """`True` vaut 1 en Python. Le laisser entrer sourcerait « 1 % » depuis un
    simple drapeau."""
    assert 1.0 not in nombres_du_packet({'demo': True, 'ok': False})


def test_un_packet_VIDE_ne_fait_pas_tomber_le_controle():
    for vide in ({}, None, [], ''):
        assert isinstance(non_sourcees('cote 412,50 $', vide), list)


#  ═══════════  4. la compatibilité est préservée  ═════════════════════════════

def test_SANS_packet_le_comportement_est_celui_d_avant():
    """`packet` reste optionnel : un appelant qui ne l'a pas ne doit pas voir
    le contrôle se transformer en panne."""
    invente = {'summary': 'AAPL cote 412,50 $', 'bull_case': 'x', 'bear_case': 'x',
               'contradictions': [], 'anomaly_reading': 'x', 'confidence_comment': 'x'}
    assert validate_analysis(invente)[0] is True


def test_les_controles_HISTORIQUES_tiennent_toujours():
    """Le langage de certitude et les clés interdites restent refusés."""
    ok, err = validate_analysis({
        'summary': "c'est garanti", 'bull_case': 'x', 'bear_case': 'x',
        'contradictions': [], 'anomaly_reading': 'x', 'confidence_comment': 'x',
        'order': 'BUY'}, packet=PACKET)
    assert ok is False
    assert any('certitude' in e for e in err)
    assert any('order' in e for e in err)


#  ═══════════  5. l'agent passe bien le packet  ═══════════════════════════════

def test_l_agent_PASSE_le_packet_au_validateur():
    """Sans cela, la correction ne quitte pas le banc."""
    import inspect
    from vertex.ai import investment_agent
    src = inspect.getsource(investment_agent)
    assert 'validate_analysis(raw, packet=request.packet)' in src


def test_une_reponse_qui_invente_BASCULE_sur_le_repli_deterministe():
    """La conséquence attendue : Vertex continue sans IA plutôt que de servir
    un chiffre inventé."""
    from vertex.ai.investment_agent import InvestmentAgent
    from vertex.ai.models import AnalysisRequest

    class _Menteur:
        model = 'faux'

        def available(self):
            return True

        def analyze(self, systeme, utilisateur):
            return {'summary': 'AAPL cote 412,50 $', 'bull_case': 'x',
                    'bear_case': 'x', 'contradictions': [],
                    'anomaly_reading': 'x', 'confidence_comment': 'x'}

    agent = InvestmentAgent(provider=_Menteur())
    res = agent.analyze(AnalysisRequest(symbol='AAPL', packet=PACKET))
    assert res.source != 'claude', 'une reponse inventee a ete servie'
    assert any('412.5' in e for e in (res.errors or [])), res.errors
