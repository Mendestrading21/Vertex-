"""SIGNAL OS · LOT 55 — LA CHAÎNE MOTEUR → CLÉ → ROUTE → ÉCRAN, TENUE PAR SA STRUCTURE.

`tools/mesurer_moteurs_muets.py` m'a donné **trois inventaires faux d'affilée**
(lots 49, 52, 54). La cause n'était pas un réglage mais son principe : il
cherchait la chaîne `"nom_du_module"` dans le corps des réponses servies. Cela ne
dit la vérité que si un moteur publie sous une clé portant son nom de fichier.
Or `drawdown_context` publie `contexts.drawdown`, `decision_readiness` publie
`decision.readiness` — et surtout `walk_forward_validation` et `option_cohort`
**servent le corps entier** d'une route dédiée. *Un corps de réponse ne se nomme
jamais lui-même* : aucune recherche de nom ne pouvait les voir.

`tools/mesurer_moteurs_par_appelant.py` remonte la chaîne réelle : appelant
(AST) → clé reçue → route → écran. Sa moitié AST ne demande **aucun serveur** :
elle se tient donc ici, en intégration continue.

Ce que ces tests protègent n'est pas l'outil pour lui-même — c'est **le câblage
du produit**. Renommer `decision['readiness']` ou déplacer un moteur hors de sa
route casse un test avec un message qui dit lequel.
"""
import pytest

from tools.mesurer_moteurs_par_appelant import moteurs, relever

#  Câblages mesurés au lot 55, moteur → (route, ce qui reçoit l'appel).
#  Chacun a été confirmé sur le produit vivant avant d'être figé ici.
CABLAGES = {
    'decision_readiness': ('/api/skyler/<sym>', 'decision.readiness'),
    'opportunity_attribution': ('/api/skyler/<sym>', 'decision.opportunity_attribution'),
    'opportunity_reliability': ('/api/skyler/<sym>', 'decision.opportunity_reliability'),
    'regime_break': ('/api/skyler/<sym>', 'decision.regime_break'),
    'sector_coherence': ('/api/skyler/<sym>', 'decision.sector_coherence'),
    'multi_asset_guard': ('/api/skyler/<sym>', 'decision.multi_asset_guard'),
}

#  Les moteurs qui SERVENT LE CORPS ENTIER d'une route. C'est le cas que
#  l'ancienne méthode ne pouvait structurellement pas voir, et c'est donc celui
#  qu'il faut tenir le plus fermement.
CORPS_ENTIER = {
    'walk_forward_validation': '/api/skyler/validation',
    'evidence_lab': '/api/evidence/<sym>',
    'decision_stack': '/api/decision/<sym>',
}


@pytest.fixture(scope='module')
def releve():
    return relever()[1]


def test_l_outil_trouve_des_appelants(releve):
    """ANTI-VACUITÉ. Un relevé vide ferait passer tous les tests d'absence."""
    avec = [n for n, v in releve.items() if v]
    assert len(avec) >= 40, (
        'seuls %d moteurs ont un appelant identifie : l\'analyse AST des routes '
        'ne trouve plus grand-chose, tout verdict tire d\'elle serait creux'
        % len(avec))


@pytest.mark.parametrize('moteur,attendu', sorted(CABLAGES.items()))
def test_le_moteur_reste_cable_a_sa_route_et_a_sa_cle(releve, moteur, attendu):
    """Le câblage mesuré, figé. Renommer la clé servie casse ici — et c'est
    précisément la mutation qui, au lot 55, a fait basculer `decision_readiness`
    de PEINT à MUET dans l'inventaire."""
    route, etiquette = attendu
    usages = releve.get(moteur) or []
    assert usages, '%s n\'est plus appele depuis aucune route' % moteur
    trouve = [(u['route'], u['etiquette']) for u in usages]
    assert (route, etiquette) in trouve, (
        '%s ne sort plus en `%s` depuis `%s` — mesure : %s. Si le changement '
        'est voulu, mettre a jour CABLAGES **et** verifier que l\'interface lit '
        'la nouvelle cle, sinon le moteur devient muet en silence'
        % (moteur, etiquette, route, trouve))


@pytest.mark.parametrize('moteur,route', sorted(CORPS_ENTIER.items()))
def test_le_moteur_qui_sert_le_corps_entier_est_reconnu(releve, moteur, route):
    """LE CAS QUI A COÛTÉ TROIS INVENTAIRES.

    Ces moteurs remplissent la réponse entière : `out = moteur.assess(...)` puis
    `jsonify(out)`. Aucune clé ne porte leur nom, donc aucune recherche de nom
    ne peut les trouver. L'outil doit les reconnaître par la STRUCTURE."""
    usages = [u for u in (releve.get(moteur) or []) if u['route'] == route]
    assert usages, '%s n\'est plus appele depuis %s' % (moteur, route)
    assert any(u['corps_entier'] for u in usages), (
        '%s ne sert plus le corps entier de %s : soit le cablage a change, soit '
        'la detection `jsonify(<variable>)` de l\'outil ne le voit plus. Dans '
        'le second cas l\'outil redeviendrait aveugle a la famille de moteurs '
        'qui a produit trois inventaires faux' % (moteur, route))


def test_les_moteurs_vivent_dans_les_quatre_paquets_mesures():
    """Chercher tous les moteurs dans `vertex/engines/` était l'une des erreurs
    du lot 52 : `historical_stress` est dans `portfolio/`, `option_cohort` dans
    `tracking/`. Le relevé couvre les quatre paquets ou il ment."""
    connus = moteurs()
    for nom, chemin in (('historical_stress', 'vertex/portfolio'),
                        ('option_cohort', 'vertex/tracking'),
                        ('regime_break', 'vertex/market'),
                        ('decision_readiness', 'vertex/engines')):
        assert nom in connus, '%s n\'est plus releve comme moteur' % nom
        assert connus[nom].startswith(chemin), (
            '%s a change de paquet (%s) : le relevé du lot 55 est perime'
            % (nom, connus[nom]))


def test_l_ancien_outil_refuse_de_mesurer():
    """Un instrument dont la méthode est connue fausse ne doit pas pouvoir
    produire un quatrième inventaire crédible. Il rend 2 et nomme son
    remplaçant."""
    from tools import mesurer_moteurs_muets
    assert mesurer_moteurs_muets.main() == 2, (
        'l\'ancien outil mesure de nouveau : sa methode — chercher un nom de '
        'module dans un corps JSON — a produit trois inventaires faux')
