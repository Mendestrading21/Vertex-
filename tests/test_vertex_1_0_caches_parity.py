"""Vertex 1.0 · #779 — PARITÉ DES CACHES EXTRAITS.

`QUALITY_STANDARD.md` §8 : *« Les caches ont un propriétaire et une politique de
fraîcheur. »* Les huit caches d'exécution vivaient au niveau module de
`terminal.py`, sans propriétaire déclaré ni politique écrite. Ils ont un
domicile : `vertex/app/caches.py`.

## Ce que ce fichier garde, et pourquoi c'est l'identité qui compte

L'extraction ne vaut que si l'objet est **le même des deux côtés**. Les huit
sont mutés en place — un écrivain fait `cache['x'] = ...`, jamais
`cache = {...}`. Tant que `terminal._live_quotes is caches._live_quotes`, tout
écrivain existant écrit là où les lecteurs lisent, et le déplacement est
invisible au comportement.

Le jour où quelqu'un **réassigne** l'un d'eux, l'identité se casse : les deux
noms désignent alors deux dictionnaires différents, les écritures partent d'un
côté et les lectures de l'autre, et **rien ne plante**. C'est exactement le
défaut que `CLAUDE.md` décrit pour `scan_state` (« ne JAMAIS réassigner »), et
c'est pour ça qu'un test d'identité vaut mieux qu'un test de contenu.

## La politique est testée, pas seulement écrite

Un commentaire se périme sans bruit. `POLITIQUE` est un dictionnaire : chaque
cache y déclare son propriétaire — **mesuré à l'AST**, jamais supposé — et sa
règle de fraîcheur. Le test exige que le registre couvre exactement les objets
exportés : ajouter un cache sans déclarer son propriétaire fait échouer la
suite.
"""
import pytest

from vertex.app import caches

#  Les objets partagés. `_STOOQ_TTL` est un entier : il est comparé par valeur,
#  pas par identité — un `int` n'a pas d'identité stable en Python.
_PARTAGES = (
    '_STOOQ_CACHE', '_SOURCE_BUDGET_STATE', '_CORR_BENCH', '_ibkr_cache',
    '_IDX_IBKR', '_IDX_META', '_live_quotes', '_live_meta',
    #  #779/G1 — neuvieme cache. Il est partage entre TROIS parties :
    #  `_opt_loop` (rotation de l'univers, dans le monolithe),
    #  `vertex.options.pack.options_pack` (fiche ouverte) et le chargement
    #  disque au demarrage. Le monolithe le REMPLIT (`.update(...)`) au lieu de
    #  le reassigner : une reassignation separerait la boucle de la route sans
    #  qu'aucune erreur ne soit levee.
    '_OPTALL_CACHE',
)


@pytest.fixture(scope='module')
def monolithe():
    import terminal
    return terminal


def test_les_caches_sont_le_meme_objet_des_deux_cotes(monolithe):
    """LE CŒUR DE L'EXTRACTION.

    Si l'identité se rompt, les écritures et les lectures se séparent en
    silence : aucune exception, aucune trace, des chiffres qui cessent de
    bouger."""
    for nom in _PARTAGES:
        a = getattr(monolithe, nom)
        b = getattr(caches, nom)
        assert a is b, (
            '`terminal.%s` et `caches.%s` ne sont plus le MEME objet : les '
            'ecrivains et les lecteurs se sont separes en silence. Chercher une '
            'REAFFECTATION (`%s = {...}`) — il faut muter en place.'
            % (nom, nom, nom))


def test_le_ttl_stooq_reste_partage_par_valeur(monolithe):
    """Un entier n'a pas d'identité stable : on compare la valeur, et on la
    compare quand même — deux TTL divergents feraient marteler un endpoint
    gratuit d'un côté et pas de l'autre."""
    assert monolithe._STOOQ_TTL == caches._STOOQ_TTL == 6 * 3600


def test_chaque_cache_declare_un_proprietaire_et_une_fraicheur():
    """Un commentaire se périme sans bruit ; ce registre est testé.

    Ajouter un cache sans déclarer qui l'écrit fait échouer la suite — c'est
    précisément l'exigence de `QUALITY_STANDARD.md` §8."""
    declares = set(caches.POLITIQUE)
    #  Deux familles, et le registre doit couvrir les DEUX :
    #  - les caches PARTAGES avec le monolithe, dont l'identite est gardee
    #    plus haut (une reaffectation separerait ecrivains et lecteurs) ;
    #  - les magasins qui n'ont qu'un proprietaire dans le paquet. Ils
    #    n'entrent pas dans le contrat de parite — il n'y a rien a comparer —
    #    mais `QUALITY_STANDARD` §8 exige quand meme proprietaire et politique.
    #    Les exclure du registre reviendrait a dire que la regle ne vaut que
    #    pour les caches historiques.
    magasins = {n for n in dir(caches)
                if n.startswith('_') and not n.startswith('__')
                and isinstance(getattr(caches, n), caches._Magasin)}
    assert magasins, (
        'le recensement des magasins ne trouve RIEN : sans lui, un magasin '
        'pourrait apparaitre sans proprietaire declare sans que ce banc bronche')
    exportes = set(_PARTAGES) | {'_STOOQ_CACHE'} | magasins
    manquants = exportes - declares
    assert not manquants, (
        'ces caches n\'ont ni proprietaire ni politique de fraicheur '
        'declares : %s' % sorted(manquants))
    orphelins = declares - exportes
    assert not orphelins, (
        'le registre declare des caches qui n\'existent plus : %s' % sorted(orphelins))
    for nom, regle in caches.POLITIQUE.items():
        assert regle.get('proprietaire'), '%s sans proprietaire' % nom
        assert regle.get('fraicheur'), '%s sans politique de fraicheur' % nom
        #  « cache-persiste » : un cache qui SURVIT au redemarrage. La nuance
        #  n'est pas cosmetique — un cache memoire perdu se reconstruit, un
        #  cache disque perime peut servir des chaines d'options d'hier.
        assert regle.get('nature') in ('cache', 'cache-persiste', 'live',
                                       'live-meta', 'sante-source'), (
            '%s porte une nature inconnue : %r' % (nom, regle.get('nature')))


def test_le_monolithe_ne_redefinit_plus_ces_caches():
    """La preuve que l'extraction a bien RETIRÉ, et pas seulement ajouté.

    Une définition qui revient dans `terminal.py` écraserait l'objet importé au
    chargement : deux propriétaires pour un cache, et le registre mentirait."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1].joinpath('terminal.py').read_text(encoding='utf-8')
    for nom in _PARTAGES:
        assert ('\n%s = ' % nom) not in src, (
            '`terminal.py` redefinit `%s` au niveau module : l\'objet importe '
            'depuis `vertex/app/caches.py` serait ecrase, et le registre de '
            'politique deviendrait faux' % nom)


def test_aucun_cache_ne_porte_de_capacite_d_ordre():
    """Invariant produit, revérifié là où de la donnée IBKR transite.

    `ANALYSIS_ONLY` est global, mais ces caches sont exactement l'endroit où un
    instantané de compte pourrait devenir un chemin d'exécution. Le test est
    bon marché ; l'omission ne le serait pas."""
    interdits = ('order', 'placeorder', 'transmit', 'submit', 'buy(', 'sell(')
    import pathlib
    src = pathlib.Path(caches.__file__).read_text(encoding='utf-8').lower()
    for mot in interdits:
        assert mot not in src, (
            'le module de caches mentionne « %s » : verifier qu\'aucun chemin '
            'd\'ordre ne s\'y installe' % mot)
