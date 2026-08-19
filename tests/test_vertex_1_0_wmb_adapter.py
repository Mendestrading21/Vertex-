"""Vertex 1.0 · #780 — L'ADAPTER WMB, ET L'INTERDIT RENDU EXÉCUTABLE.

`PRODUCT_CONTRACT.md` fixe trois bornes à WMB : provenance obligatoire, jamais
un prix canonique, jamais un contournement de hard gate.

La deuxième est celle qui se perd le plus facilement. Un commentaire qui dit
« WMB ne fournit pas de prix » n'empêche rien : six mois plus tard un champ
`spx_close` apparaît dans une charge, quelqu'un le lit « en attendant », et la
règle est morte sans que rien n'ait échoué. Ce fichier vérifie qu'elle est une
**propriété du code**.
"""
import datetime as _dt

import pytest

from vertex.market import wmb


def _t(h=0):
    return _dt.datetime(2026, 8, 18, 12, 0, tzinfo=_dt.timezone.utc) + _dt.timedelta(hours=h)


def test_un_champ_de_prix_est_mis_en_quarantaine_et_non_avale():
    """LE CŒUR DE #780.

    On n'exige pas seulement que le prix soit absent du contenu : on exige
    qu'il soit **tracé**. Un champ jeté en silence masquerait une source qui
    essaie de fournir des prix, et rendrait incompréhensible un brief qui
    semble incomplet."""
    brief = wmb.ingest({
        'publie': _t(-1).isoformat(),
        'sources': ['Fed'],
        'regime': {'label': 'risk-on', 'price': 5432.10},
        'enonces': [{'texte': 'La Fed maintient ses taux.', 'sources': ['Fed']}],
    }, maintenant=_t())

    assert 'price' not in (brief['contenu']['regime'] or {}), (
        'un champ de prix a survecu dans le contenu : WMB deviendrait une '
        'source de prix, ce que le contrat produit interdit')
    champs = [q['champ'] for q in brief['quarantaine']]
    assert 'regime.price' in champs, (
        'le champ de prix a ete jete en SILENCE : la tentative doit rester '
        'visible, sinon un brief ampute parait simplement incomplet')


@pytest.mark.parametrize('champ', ['price', 'bid', 'ask', 'delta', 'iv', 'strike',
                                   'premium', 'open_interest', 'greeks'])
def test_toute_la_famille_des_donnees_de_marche_est_refusee(champ):
    """La borne vise une FAMILLE, pas un nom. Prix, primes, Greeks, IV, strike,
    OI : tout ce qui ferait de WMB une source de marché canonique."""
    brief = wmb.ingest({'publie': _t(-1).isoformat(),
                        'secteurs': {'tech': {champ: 1.0}}}, maintenant=_t())
    assert brief['quarantaine'], 'le champ « %s » est passe' % champ


def test_un_mot_de_langage_courant_n_est_pas_confondu_avec_un_champ():
    """LE FAUX POSITIF QU'IL FAUT ÉVITER.

    « price » dans une phrase d'analyse est parfaitement légitime — c'est un
    CHAMP nommé `price` qui ne l'est pas. Une règle qui censure le vocabulaire
    rendrait le brief inutilisable et pousserait à la contourner."""
    brief = wmb.ingest({
        'publie': _t(-1).isoformat(),
        'enonces': [{'texte': 'Le price action reste hesitant sur le SPX.',
                     'sources': ['WMB']}],
    }, maintenant=_t())
    assert brief['quarantaine'] == [], (
        'un mot du langage courant a ete pris pour un champ de marche')
    assert brief['contenu']['enonces'][0]['texte'].startswith('Le price action')


def test_une_affirmation_sans_source_reste_non_verifiee():
    """`PRODUCT_CONTRACT.md` : « une affirmation non reliée à une source reste
    UNVERIFIED ». C'est ce qui empêche un brief bien écrit de peser autant
    qu'un fait sourcé."""
    brief = wmb.ingest({
        'publie': _t(-1).isoformat(),
        'enonces': [
            {'texte': 'Inflation a 2,4 % en juillet.', 'sources': ['BLS']},
            {'texte': 'Le marche anticipe deux baisses.'},
        ],
    }, maintenant=_t())
    statuts = {e['texte']: e['statut'] for e in brief['contenu']['enonces']}
    assert statuts['Inflation a 2,4 % en juillet.'] == 'VERIFIED'
    assert statuts['Le marche anticipe deux baisses.'] == 'UNVERIFIED'
    assert brief['verification'] == {'enonces': 2, 'verifies': 1, 'non_verifies': 1}
    assert brief['confiance_sourcage'] == 0.5, (
        'la confiance doit etre CALCULEE depuis la part de sourcage, jamais saisie')


def test_la_fraicheur_suit_l_age_et_n_invente_jamais_de_date():
    """Une date absente donne `MISSING`, jamais « maintenant » : substituer
    l'heure courante serait le zéro silencieux que le Quality Standard interdit.
    Un brief daté du FUTUR est douteux, pas « très frais »."""
    assert wmb.ingest({'publie': _t(-2).isoformat()}, maintenant=_t())['fraicheur'] == 'LIVE'
    assert wmb.ingest({'publie': _t(-30).isoformat()}, maintenant=_t())['fraicheur'] == 'DELAYED'
    assert wmb.ingest({'publie': _t(-100).isoformat()}, maintenant=_t())['fraicheur'] == 'STALE'
    assert wmb.ingest({}, maintenant=_t())['fraicheur'] == 'MISSING'
    assert wmb.ingest({'publie': 'pas une date'}, maintenant=_t())['fraicheur'] == 'MISSING'
    assert wmb.ingest({'publie': _t(+5).isoformat()}, maintenant=_t())['fraicheur'] == 'MISSING'
    assert wmb.ingest({'publie': _t(-2).isoformat()}, demo=True,
                      maintenant=_t())['fraicheur'] == 'DEMO'


def test_le_hash_porte_sur_le_contenu_normalise_et_non_sur_la_forme():
    """Sinon chaque relecture du même brief serait signalée comme une
    « correction », et l'historique des corrections deviendrait du bruit."""
    a = wmb.ingest({'publie': _t(-1).isoformat(),
                    'enonces': [{'texte': 'Fed stable.', 'sources': ['Fed']}]},
                   maintenant=_t())
    b = wmb.ingest({'publie': _t(-1).isoformat(),
                    'enonces': [{'texte': '  Fed stable.  ', 'sources': ['Fed']}]},
                   maintenant=_t(1))
    assert a['hash'] == b['hash'], (
        'un espace en plus change le hash : chaque relecture passerait pour '
        'une correction')


def test_une_correction_reelle_est_conservee_et_non_ecrasee():
    """Un brief qui se corrige est une information. L'écraser reviendrait à
    laisser l'IA réécrire l'historique — ce que #783 interdit explicitement."""
    v1 = wmb.ingest({'publie': _t(-1).isoformat(),
                     'enonces': [{'texte': 'Inflation a 2,4 %.', 'sources': ['BLS']}]},
                    maintenant=_t())
    v2 = wmb.ingest({'publie': _t(-1).isoformat(),
                     'enonces': [{'texte': 'Inflation revisee a 2,6 %.', 'sources': ['BLS']}]},
                    maintenant=_t(2), precedent=v1)
    assert v2['hash'] != v1['hash']
    assert len(v2['corrections']) == 1
    assert v2['corrections'][0]['hash'] == v1['hash'], (
        'la version precedente a disparu : l\'historique des corrections est perdu')


def test_la_deduplication_reutilise_le_moteur_existant():
    """Deux algorithmes de déduplication divergent au premier ajustement. Le
    prompt maître demande de chercher les doublons AVANT d'ajouter du code :
    on réutilise `vertex.market.news_dedup`.

    CE QUE LE MOTEUR FAIT VRAIMENT — mesuré, et mon premier test se trompait.
    `_key` compare des **ensembles de tokens exacts** : il fusionne donc des
    RÉORDONNANCEMENTS des mêmes mots, pas des paraphrases. « La Fed maintient
    ses taux » et « Taux maintenus par la Fed » ne fusionnent PAS
    (« maintient » ≠ « maintenus »). J'avais écrit un test qui postulait une
    capacité inexistante ; c'est le test qui avait tort, pas le code."""
    brief = wmb.ingest({
        'publie': _t(-1).isoformat(),
        'enonces': [
            {'texte': 'La Fed maintient ses taux directeurs.', 'sources': ['Fed']},
            {'texte': 'Ses taux directeurs : la Fed maintient.',
             'sources': ['Reuters']},
        ],
    }, maintenant=_t())
    enonces = brief['contenu']['enonces']
    assert len(enonces) == 1, (
        'deux enonces aux memes tokens significatifs n\'ont pas fusionne : '
        'la deduplication ne passe plus par news_dedup')
    assert enonces[0]['sources'] == ['Fed', 'Reuters'], (
        'la fusion doit REUNIR les sources : perdre une source affaiblirait '
        'la tracabilite au lieu de la renforcer')


def test_la_limite_de_la_deduplication_est_connue_et_assumee():
    """LA LIMITE RÉELLE, ÉCRITE PLUTÔT QUE DÉCOUVERTE PLUS TARD.

    Le moteur ne fusionne pas les paraphrases : deux dépêches racontant le même
    fait avec des mots différents restent deux énoncés. Ce n'est pas un défaut
    de l'adapter — c'est le contrat de `news_dedup`, réutilisé sciemment. Le
    durcir changerait le comportement de la déduplication d'actualités
    existante, ce qui demande une preuve de parité et n'appartient pas à #780.

    Ce test EXISTE pour que la limite tombe le jour où le moteur s'améliore,
    plutôt que de rester une surprise."""
    brief = wmb.ingest({
        'publie': _t(-1).isoformat(),
        'enonces': [
            {'texte': 'La Fed maintient ses taux directeurs.', 'sources': ['Fed']},
            {'texte': 'Taux directeurs maintenus par la Fed.', 'sources': ['Reuters']},
        ],
    }, maintenant=_t())
    assert len(brief['contenu']['enonces']) == 2, (
        'la deduplication fusionne desormais les PARAPHRASES : bonne nouvelle, '
        'mais verifier l\'impact sur vertex/market/news_dedup et ses '
        'consommateurs d\'actualites avant de retirer ce test')


def test_le_mandat_est_porte_par_l_objet_et_pas_seulement_par_la_doc():
    """Un consommateur peut lire ces bornes ; un test peut les vérifier."""
    brief = wmb.ingest({'publie': _t(-1).isoformat()}, maintenant=_t())
    assert brief['mandat'] == {'fournit_prix_canonique': False,
                               'peut_contourner_hard_gate': False,
                               'role': 'macro_context'}
    assert brief['schema_version'] == wmb.SCHEMA_VERSION
    assert brief['source_name'] == 'WMB Brief'


def test_un_brief_rassis_reste_affichable_mais_pas_exploitable():
    """L'honnêteté ne diminue pas avec la fraîcheur : un brief périmé s'affiche.
    Mais il ne doit pas nourrir un contexte présenté comme celui du jour."""
    assert wmb.est_exploitable(wmb.ingest({'publie': _t(-2).isoformat()}, maintenant=_t()))
    assert not wmb.est_exploitable(wmb.ingest({'publie': _t(-100).isoformat()},
                                              maintenant=_t()))
    assert not wmb.est_exploitable(wmb.ingest({}, maintenant=_t()))
    assert not wmb.est_exploitable(None)


def test_une_charge_absurde_ne_fait_pas_tomber_l_adapter():
    """Le brief vient d'une source externe : il n'a aucune obligation d'être
    bien formé. Un adapter qui lève sur une charge inattendue ferait tomber
    Aujourd'hui avec lui."""
    for charge in (None, {}, {'enonces': 'pas une liste'},
                   {'enonces': [None, 42, {'texte': ''}]}):
        brief = wmb.ingest(charge, maintenant=_t())
        assert brief['schema_version'] == wmb.SCHEMA_VERSION
        assert isinstance(brief['contenu']['enonces'], list)
