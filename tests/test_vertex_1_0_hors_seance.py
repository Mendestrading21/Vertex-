"""Vertex 1.0 · G5 — hors séance, l'écran ne doit pas se vider.

Signalé en conditions réelles : TWS branché, et « plein de graphiques qui ne
s'affichent pas, comme si sur IBKR on n'avait rien trouvé ». Mesure de l'heure
au moment du signalement : **02:50 à New York, marché fermé**.

Deux défauts, tous deux vérifiables sans broker.

## 1. `reqMarketDataType(1)` ne bascule pas tout seul

Les commentaires du produit affirmaient « bascule auto en différé si pas
d'abonnement » et « repli auto différé si besoin ». **C'est faux** : le type 1
demande du temps réel et ne rend rien d'autre. Marché fermé ou abonnement
absent → aucun tick, donc aucun cours, donc des écrans vides.

Le chemin options le savait déjà : il retente les cotations manquantes en type 2
(clôture figée). Les deux autres flux — cotations de la watchlist et indices —
ne le savaient pas. Encore un désaccord entre sites qui font la même chose, la
même famille que les cinq ordres de ports.

## 2. Un prix RÉEL était jeté parce qu'un champ dérivé manquait

`_store_ticker` exigeait `last` **et** `close` :

```python
if last and close:      # <- sinon rien n'est range du tout
```

Hors séance, IBKR ne livre pas toujours la clôture. Un prix parfaitement réel
était alors jeté parce que la **variation** n'était pas calculable. C'est
l'inverse de la règle du produit : une donnée absente devient un `—` honnête,
elle ne fait pas disparaître ce qu'on sait par ailleurs.
"""
from __future__ import annotations

import math
import pathlib
import re

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]
TERMINAL = RACINE / 'terminal.py'
NAN = float('nan')


class _Contrat:
    def __init__(self, symbole):
        self.symbol = symbole


class _Ticker:
    """Assez de surface pour `_store_ticker`, et pas plus."""

    def __init__(self, symbole='AAPL', last=NAN, close=NAN, bid=NAN, ask=NAN,
                 marche=NAN, mdt=1):
        self.contract = _Contrat(symbole)
        self.last, self.close, self.bid, self.ask = last, close, bid, ask
        self._marche = marche
        self.marketDataType = mdt

    def marketPrice(self):
        return self._marche


@pytest.fixture()
def store():
    import terminal
    terminal._live_quotes.clear()
    yield terminal
    terminal._live_quotes.clear()


# ── Le prix survit à l'absence de clôture ─────────────────────────────────

def test_un_prix_reel_sans_cloture_est_CONSERVE(store):
    """LE défaut. Hors séance, IBKR livre souvent `last` sans `close`."""
    stocke, _ = store._store_ticker(_Ticker('AAPL', last=190.5, close=NAN))
    assert stocke, (
        'un prix réel a été jeté parce que la clôture manquait — la variation '
        'n\'est pas calculable, le PRIX l\'est.')
    q = store._live_quotes['AAPL']
    assert q['last'] == 190.5
    assert q['change'] is None, (
        'la variation doit être INCONNUE, jamais inventée : sans clôture, il '
        'n\'y a rien à quoi comparer.')


def test_la_variation_est_calculee_quand_la_cloture_existe(store):
    store._store_ticker(_Ticker('AAPL', last=110.0, close=100.0))
    assert store._live_quotes['AAPL']['change'] == 10.0


def test_le_prix_de_marche_sert_de_repli_avant_la_cloture(store):
    stocke, _ = store._store_ticker(_Ticker('AAPL', last=NAN, marche=201.3))
    assert stocke and store._live_quotes['AAPL']['last'] == 201.3


def test_la_cloture_seule_reste_exploitable(store):
    """Marché fermé depuis longtemps : seule la clôture arrive. C'est une
    donnée vraie, simplement datée d'hier — la montrer vaut mieux qu'un écran
    vide, à condition que la fraîcheur le dise (elle le dit)."""
    stocke, temps_reel = store._store_ticker(_Ticker('AAPL', last=NAN, close=99.0,
                                                     mdt=2))
    assert stocke and store._live_quotes['AAPL']['last'] == 99.0
    assert temps_reel is False


def test_un_ticker_entierement_vide_ne_fabrique_rien(store):
    stocke, temps_reel = store._store_ticker(_Ticker('AAPL'))
    assert (stocke, temps_reel) == (False, False)
    assert 'AAPL' not in store._live_quotes, (
        'un ticker sans aucun prix a produit une entrée : c\'est exactement la '
        'donnée fabriquée que le produit interdit.')


def test_bid_et_ask_absents_valent_None_et_ne_bloquent_pas_le_prix(store):
    store._store_ticker(_Ticker('AAPL', last=190.5, close=189.0))
    q = store._live_quotes['AAPL']
    assert q['bid'] is None and q['ask'] is None and q['last'] == 190.5


def test_le_temps_reel_est_lu_du_ticker_et_pas_suppose(store):
    _, reel = store._store_ticker(_Ticker('AAPL', last=1.0, close=1.0, mdt=1))
    assert reel is True
    _, fige = store._store_ticker(_Ticker('MSFT', last=1.0, close=1.0, mdt=2))
    assert fige is False, (
        'une cotation en clôture figée se déclarait temps réel — la puce '
        '« Live » aurait menti hors séance.')


def test_un_nan_n_est_jamais_un_prix(store):
    assert store._px_valide(NAN) is None
    assert store._px_valide(None) is None
    assert store._px_valide(0) is None, 'un prix nul n\'est pas un prix'
    assert store._px_valide(-3) is None
    assert store._px_valide('12.5') == 12.5
    assert not math.isnan(store._px_valide(3.0))


# ── Le repli vers la clôture figée existe sur les trois chemins ───────────

def _source() -> str:
    return TERMINAL.read_text(encoding='utf-8')


def _corps(nom: str) -> str:
    """Corps d\'une fonction de terminal.py, decoupe a l\'AST.

    Compter les occurrences dans TOUT le fichier ne dirait pas OU elles sont :
    trois replis dans le meme worker passeraient pour trois chemins couverts.
    """
    import ast
    src = _source()
    arbre = ast.parse(src)
    for n in ast.walk(arbre):
        if isinstance(n, ast.FunctionDef) and n.name == nom:
            return ast.get_source_segment(src, n) or ''
    raise AssertionError('fonction %s introuvable dans terminal.py' % nom)


def _peut_demander_le_type(nom: str, voulu: int) -> bool:
    """Le worker peut-il demander CE type de données ?

    Contrôle de COMPORTEMENT, pas de texte. La première version cherchait le
    littéral `reqMarketDataType(2)` : elle a échoué dès que le code s\'est
    AMÉLIORÉ (`cible = 2 if recus == 0 else 1`), en signalant un défaut qui
    n\'existait pas. Un gardien qui n\'accepte qu\'une écriture interdit de
    réécrire — et pousse à contourner plutôt qu\'à corriger.
    """
    import ast
    import textwrap
    arbre = ast.parse(textwrap.dedent(_corps(nom)))
    #  Noms auxquels la constante voulue est affectee, meme dans une
    #  expression conditionnelle.
    noms = set()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Assign):
            if any(isinstance(c, ast.Constant) and c.value == voulu
                   for c in ast.walk(n.value)):
                noms |= {t.id for t in n.targets if isinstance(t, ast.Name)}
    for n in ast.walk(arbre):
        if (isinstance(n, ast.Call)
                and getattr(n.func, 'attr', '') == 'reqMarketDataType' and n.args):
            a = n.args[0]
            if isinstance(a, ast.Constant) and a.value == voulu:
                return True
            if isinstance(a, ast.Name) and a.id in noms:
                return True
    return False


@pytest.mark.parametrize('worker', ['_ibkr_opt_worker', '_quotes_worker',
                                    '_indices_loop'])
def test_chaque_chemin_sait_replier_vers_la_cloture_figee(worker):
    """Le chemin options le savait déjà ; les deux autres non. Un produit qui
    fait trois fois la même chose de trois façons finit toujours par en avoir
    une qui ment — c\'est la même famille que les cinq ordres de ports."""
    assert _peut_demander_le_type(worker, 2), (
        '%s ne peut plus demander la clôture figée (type 2) : hors séance, ses '
        'écrans redeviendront vides sans que rien ne le dise.' % worker)


@pytest.mark.parametrize('worker', ['_quotes_worker', '_indices_loop'])
def test_chaque_chemin_sait_revenir_au_temps_reel(worker):
    """Le repli doit être réversible. Un flux coincé en clôture figée après
    l\'ouverture afficherait le cours d\'hier en se disant à jour."""
    assert _peut_demander_le_type(worker, 1), (
        '%s ne peut plus revenir au temps réel.' % worker)


def test_les_commentaires_ne_promettent_plus_une_bascule_qui_n_existe_pas():
    """Le défaut n'était pas seulement dans le code : deux commentaires
    AFFIRMAIENT un repli automatique qu'IBKR ne fait pas. Un commentaire faux
    est pire qu'aucun — il dissuade d'aller vérifier."""
    src = _source()
    for mensonge in ('bascule auto en différé', 'repli auto différé'):
        assert mensonge not in src, (
            'le commentaire « %s » décrit un comportement qu\'IBKR n\'a pas.'
            % mensonge)


def test_le_retour_au_temps_reel_est_atteignable():
    """Rester en clôture figée après l'ouverture ferait mentir l'écran. La
    première version posait `debut_frozen` à CHAQUE cycle, ce qui rendait la
    condition de retour structurellement inatteignable — le même motif que
    l'état « Périmé » jamais atteint des étiquettes écrites à la main."""
    bloc = _corps('_quotes_worker')
    assert 'debut_frozen = time.time()' in bloc
    assert re.search(r"debut_frozen\s*=\s*time\.time\(\)\s*if\s", bloc) is None, (
        '`debut_frozen` est repositionné à chaque cycle : le retour au temps '
        'réel ne se déclencherait jamais.')
    assert 'debut_frozen = 0' in bloc, (
        'le compteur n\'est pas remis à zéro au retour en temps réel : la '
        'bascule se rejouerait en boucle.')
