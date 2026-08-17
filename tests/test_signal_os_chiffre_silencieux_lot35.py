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
import ast
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
    assert corps.count('_releve_neuf(nav, url)') == 3, (
        'la mesure n\'est plus encadree (2 references + 1 controle sans panne) '
        '— le detecteur va accuser les horloges')
    assert corps.count('_releve_neuf(nav, url, panne=cible') == 1
    assert ("a['cellules'].get(k) == v and d['cellules'].get(k) == v" in corps), (
        'la stabilite ne croise plus les TROIS releves sans panne')


def test_les_deux_bras_ont_le_MEME_cache():
    """QUATRIÈME forme de la même erreur, et la plus coûteuse : j'ai comparé
    deux bras qui n'étaient pas comparables.

    Le bras de contrôle réutilisait UN contexte pour ses trois relevés, donc le
    cache client (`VX.fetch` garde 15 s) lui rendait la même valeur, tandis que
    le bras sous panne — contexte neuf — refetchait. Toute valeur vivante (un âge
    calculé par le serveur) différait alors systématiquement entre les bras, et
    l'outil l'imputait à la panne. J'en avais conclu que « la panne change
    vraiment la durée » : c'était mon montage.

    Un contexte neuf par relevé, des DEUX côtés — témoin compris."""
    src = open(pp.__file__, encoding='utf-8').read()
    assert 'def _releve_neuf(' in src and 'ctx.close()' in src, (
        'le contexte n\'est plus recree par releve : les bras redeviennent '
        'incomparables des qu\'une valeur vit')
    # Plus aucun releve ne doit reutiliser un contexte partage entre deux bras.
    corps = src.split('def main(')[1]
    assert 'pgA' not in corps and 'pgB' not in corps, (
        'un contexte partage est revenu dans la boucle de mesure')
    temoin = corps.split('=== TEMOIN')[0].split('# Meme regle pour le temoin')[-1]
    assert temoin.count('_releve_neuf(nav') >= 3, (
        'le temoin ne compare plus a contexte neuf : il heriterait du meme '
        'biais que la mesure')


def test_l_outil_porte_son_propre_temoin_et_le_dit_quand_il_est_aveugle():
    """Un « 0 » peut vouloir dire « produit honnête » ou « instrument aveugle ».
    L'outil tranche lui-même, et rend un code distinct s'il ne voit rien."""
    src = open(pp.__file__, encoding='utf-8').read()
    assert 'def _altere(' in src and 'status=200' in src, (
        'le temoin doit repondre 200 avec un corps FAUX — une panne 500 ferait '
        'crier la vue et ne prouverait rien')
    assert re.search(r"AVEUGLE[^\n]*\n\s*return 2", src), (
        'sans temoin concluant, l outil doit refuser de conclure')


def test_aucun_outil_importe_par_un_gardien_n_exige_un_navigateur_pour_etre_LU():
    """Piège payé par une CI rouge que mon poste ne pouvait pas montrer.

    Ce gardien importe le module de l'outil pour éprouver sa LOGIQUE. L'outil
    importait Playwright au chargement : en CI, qui n'a pas de navigateur, la
    collecte de TOUTE la suite échouait (`ModuleNotFoundError`). Localement,
    Playwright est installé — l'erreur était invisible ici.

    Ce que l'outil exige pour MESURER ne doit pas être exigé pour le LIRE. Ce
    test tient la règle pour les trois outils que les gardiens importent, pas
    seulement pour celui qui a saigné."""
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lourds = ('playwright', 'curl_cffi', 'ib_insync', 'yfinance')
    for nom in ('mesurer_panne_partielle', 'mesurer_sorties_news',
                'mesurer_surface_ibkr'):
        src = open(os.path.join(racine, 'tools', nom + '.py'), encoding='utf-8').read()
        # AU NIVEAU DU MODULE seulement : on lit `tree.body`, pas des lignes de
        # texte. Ma première version découpait la source avant `def main(` et
        # accusait un import PARESSEUX niché dans une fonction définie plus haut
        # — exactement ce qu'on veut autoriser. C'est une propriété de
        # structure ; une comparaison de chaînes ne peut pas la voir.
        for n in ast.parse(src).body:
            noms = []
            if isinstance(n, ast.Import):
                noms = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                noms = [n.module or '']
            for m in noms:
                racine_mod = m.split('.')[0]
                assert racine_mod not in lourds, (
                    '%s importe %s AU NIVEAU DU MODULE : la suite deviendra '
                    'incollectable partout ou la dependance manque (CI). '
                    'Deplacer l\'import dans la fonction qui en a besoin.'
                    % (nom, racine_mod))


def test_une_duree_est_classee_a_part_et_jamais_masquee():
    """Après l'encadrement, il RESTE quatre cas sur `/system?view=automations` :
    des libellés d'âge identiques dans les trois relevés sains et différents
    sous panne. La panne change donc bien la durée affichée — mais une durée
    plus ancienne n'est pas un chiffre INVENTÉ.

    L'outil les compte à part **et les affiche toujours**. Ce test tient les
    deux moitiés : la classification doit reconnaître une durée, et ne doit pas
    avaler un pourcentage ou un prix."""
    for duree in ('Il y a 25 min', 'dans ~1 min', '41 s', '3 h', 'depuis 2 j'):
        assert pp.est_duree(duree), duree
    for donnee in ('45 %', '12.7', '8/8', '1 234 $', '0', '-2,4 %'):
        assert not pp.est_duree(donnee), (
            '%s classe comme duree : un vrai chiffre serait masque' % donnee)
    src = open(pp.__file__, encoding='utf-8').read()
    assert 'libelles de DUREE modifies (comptes a part)' in src, (
        'les durees ne sont plus AFFICHEES : compter a part sans dire, c\'est '
        'masquer')
    assert "for d in durees[:6]:" in src, 'les cas de duree ne sont plus listes'


def _vue_g(graphes, etats=0, mentions=0):
    return {'cellules': {}, 'graphes': dict(graphes), 'etats': etats,
            'mentions': mentions, 'fuite': None}


# ── LOT 37 — la GÉOMÉTRIE des graphiques ────────────────────────────────────

def test_un_trace_qui_change_sans_rien_dire_est_signale():
    """Réserve du lot 35 : « un chiffre faux dans un graphique SVG sans texte
    n'est pas vu ». Vertex est un produit de graphiques — c'était le plus gros
    angle mort de l'instrument. Une courbe qui perd la moitié de ses sommets ne
    porte aucun texte, donc aucune cellule ne peut la trahir."""
    avant = _vue_g({'DIV:0>svg:0': '3|747:144,731:140'})
    apres = _vue_g({'DIV:0>svg:0': '3|366:72,350:68'})
    trouve = pp._graphes_muets(avant, apres)
    assert len(trouve) == 1 and '->' in trouve[0], trouve


def test_un_trace_est_TU_si_la_vue_signale_son_manque_ou_s_il_disparait():
    avant = _vue_g({'A': '3|747:144'})
    assert pp._graphes_muets(avant, _vue_g({'A': '3|366:72'}, etats=1)) == []
    assert pp._graphes_muets(avant, _vue_g({'A': '3|366:72'}, mentions=1)) == []
    assert pp._graphes_muets(avant, _vue_g({})) == [], (
        'un trace retire n\'est pas un trace faux — c\'est la vue qui renonce'
    )
    assert pp._graphes_muets(avant, _vue_g({'A': '3|747:144'})) == []


def test_l_outil_porte_un_temoin_de_TRACE_distinct_et_refuse_de_conclure_sans():
    """Un « 0 trace » ne vaut rien sans preuve que le détecteur voie une courbe
    fausse — et le témoin des CELLULES ne suffit pas : mesuré, altérer le VIX
    change deux cellules et AUCUN tracé.

    Deux cibles ont dû être corrigées avant que le témoin ne morde : le radar
    ne bougeait pas, et une troncature limitée à `rows` ne touchait l'entrée
    d'aucune courbe. La forme qui marche — `/markets?view=overview` avec `/scan`
    tronqué — fait passer deux aires de 144 à 72 sommets."""
    src = open(pp.__file__, encoding='utf-8').read()
    assert 'def _altere_scan(' in src and 'URL_G' in src, (
        'le temoin des traces a disparu')
    assert re.search(r"AUCUN trace[^\n]*\n(.*\n)?\s*return 2", src), (
        'sans temoin de trace concluant, l outil doit REFUSER de conclure')
    # La troncature doit etre RECURSIVE : « rows » seul ne bouge aucune courbe.
    tronque = src.split('def _altere_scan(')[1].split('def _releve(')[0]
    assert 'isinstance(o, dict)' in tronque and 'isinstance(o, list)' in tronque, (
        'la troncature n\'est plus recursive — elle ne touchera plus l\'entree '
        'des traces, et le temoin redeviendra muet')


def test_la_stabilite_des_traces_croise_aussi_les_trois_releves_sains():
    src = open(pp.__file__, encoding='utf-8').read()
    corps = src.split('for url in concernees:')[1].split('print(')[0]
    assert "a.get('graphes', {}).get(k) == v" in corps \
        and "d.get('graphes', {}).get(k) == v" in corps, (
        'les traces ne sont plus encadres : ils vont deriver comme les horloges')


def test_les_sources_eprouvees_couvrent_le_produit():
    """Plancher : un balayage qui n'eprouve plus que deux sources passerait."""
    assert len(pp.CIBLES) >= 8, pp.CIBLES
    for essentielle in ('/scan', '/api/pos-quotes', '/api/desk'):
        assert essentielle in pp.CIBLES
