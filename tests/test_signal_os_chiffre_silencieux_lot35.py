"""SIGNAL OS · LOT 35 — LE CHIFFRE FAUX QUI NE SE DIT PAS.

Réserve du lot 30, laissée ouverte et documentée dans l'outil lui-même : sous
panne PARTIELLE, « un chiffre faux peut se glisser entre des chiffres justes
sans qu'aucun état d'erreur ne s'affiche ». Le lot 30 avait essayé trois
méthodes et refusé de conclure. Le lot 35 ferme la question.

Ce fichier garde la LOGIQUE de détection — la partie qu'on peut éprouver sans
navigateur. Le balayage lui-même vit dans `tools/mesurer_panne_partielle.py`
(33 vues × 10 sources, ~10 min : sa place n'est pas dans une suite de 40 s).

Ce que la mesure a rendu, serveur de démonstration, SW v233 :
  · 546 cellules chiffrées, 546 stables (clé par chemin DOM) ;
  · 10 sources en panne isolée → **0** chiffre faux silencieux ;
  · témoin concluant : une source qui répond 200 avec un corps ALTÉRÉ fait
    afficher « 3 % » au lieu de « 45 % » et « 20.47 » au lieu de « 12.7 »,
    sans qu'aucun état n'apparaisse — l'instrument les voit.

Et un faux positif que je n'ai pas gardé : une première version prenait UNE
référence globale puis éprouvait les dix sources ; vingt minutes plus tard,
« Il y a 5 min » était devenu « Il y a 8 min » et l'outil accusait quinze
chiffres. Aucun n'était causé par la panne. D'où la double référence immédiate,
à la même cadence que la mesure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import mesurer_panne_partielle as pp        # noqa: E402


def _vue(cellules, etats=0, mentions=0):
    return {'cellules': dict(cellules), 'etats': etats, 'mentions': mentions,
            'fuite': None}


# ── La logique de détection, éprouvée cas par cas ───────────────────────────

def test_un_chiffre_qui_change_sans_rien_dire_est_signale():
    """LE cas : la vue affiche un autre nombre et ne signale rien."""
    avant = _vue({'DIV:0>SPAN:1': '45 %'})
    apres = _vue({'DIV:0>SPAN:1': '3 %'})
    assert pp._silencieux(avant, apres) == ['« 45 % » -> « 3 % »']


def test_un_chiffre_qui_change_est_TU_si_la_vue_signale_son_manque():
    """Une vue qui dit « donnée indisponible » n'invente rien : elle prévient.
    Deux formes comptent — un état rendu, ou une mention honnête en toutes
    lettres ; les deux doivent suffire, sinon on accuserait un produit honnête."""
    avant = _vue({'A': '45 %'})
    assert pp._silencieux(avant, _vue({'A': '3 %'}, etats=1)) == []
    assert pp._silencieux(avant, _vue({'A': '3 %'}, mentions=1)) == []


def test_une_cellule_devenue_mention_honnete_ou_disparue_ne_compte_pas():
    """« — », « n/d », ou la cellule qui s'efface : c'est le comportement voulu."""
    avant = _vue({'A': '45 %', 'B': '12.7'})
    assert pp._silencieux(avant, _vue({'A': '—'})) == []


def test_le_detecteur_ne_se_limite_pas_aux_ZEROS():
    """Le lot 30 ne cherchait qu'un « 0 » substitué. Une moyenne sur cinq
    sources au lieu de six est plausible, et fausse — c'est même la forme la
    plus dangereuse, parce qu'elle ne se remarque pas."""
    trouve = pp._silencieux(_vue({'A': '12.7'}), _vue({'A': '10.6'}))
    assert trouve == ['« 12.7 » -> « 10.6 »'], (
        'un chiffre faux NON NUL doit etre vu : %s' % trouve)


def test_un_chiffre_inchange_ne_declenche_rien():
    assert pp._silencieux(_vue({'A': '45 %'}), _vue({'A': '45 %'})) == []


# ── La méthode, figée là où elle a été payée par un faux positif ────────────

def test_la_cle_est_le_chemin_dom_et_non_la_classe():
    """`e.className` vaut « [object SVGAnimatedString] » pour TOUT texte SVG :
    la clé du lot 30 mettait des valeurs sans rapport dans le même seau."""
    assert 'chemin(e)' in pp.JS and 'indexOf(n)' in pp.JS
    assert 'className' not in pp.JS.split('const cellules')[0].split('chemin')[1]


def test_la_mesure_est_ENCADREE_par_des_releves_sans_panne():
    """Le point qui a débloqué la mesure — atteint en deux erreurs.

    1. Une référence globale unique, prise vingt minutes plus tôt : l'outil
       accusait « Il y a 5 min » devenu « Il y a 8 min ».
    2. Deux références immédiates : mieux, mais insuffisant. Un libellé à la
       minute ne bouge pas en 2,4 s, puis tombe pile pendant la mesure — la
       course complète a rendu quatre chiffres, tous des horloges.

    La forme juste : deux références AVANT, un contrôle APRÈS, tous sans panne,
    et une cellule n'est jugée que si elle est identique dans les TROIS. Aucune
    liste de formats de durée : on demande à la cellule si elle bouge aussi
    quand rien n'est cassé."""
    src = open(pp.__file__, encoding='utf-8').read()
    corps = src.split('for url in concernees:')[1].split('print(')[0]
    assert corps.count('_releve(pgA, url)') == 3, (
        'la mesure n\'est plus encadree (2 references + 1 controle sans panne) '
        '— le detecteur va accuser les horloges')
    assert corps.count('_releve(pgB, url)') == 1
    assert ("a['cellules'].get(k) == v and d['cellules'].get(k) == v" in corps), (
        'la stabilite ne croise plus les TROIS releves sans panne')


def test_l_outil_porte_son_propre_temoin_et_le_dit_quand_il_est_aveugle():
    """Un « 0 » peut vouloir dire « produit honnête » ou « instrument aveugle ».
    L'outil tranche lui-même, et rend un code distinct s'il ne voit rien."""
    src = open(pp.__file__, encoding='utf-8').read()
    assert 'def _altere(' in src and 'status=200' in src, (
        'le temoin doit repondre 200 avec un corps FAUX — une panne 500 ferait '
        'crier la vue et ne prouverait rien')
    assert re.search(r"AVEUGLE[^\n]*\n\s*return 2", src), (
        'sans temoin concluant, l outil doit refuser de conclure')


def test_les_sources_eprouvees_couvrent_le_produit():
    """Plancher : un balayage qui n'eprouve plus que deux sources passerait."""
    assert len(pp.CIBLES) >= 8, pp.CIBLES
    for essentielle in ('/scan', '/api/pos-quotes', '/api/desk'):
        assert essentielle in pp.CIBLES
