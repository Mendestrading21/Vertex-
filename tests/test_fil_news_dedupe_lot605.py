"""LOT 605 — LE FIL DE NEWS DÉDUPLIQUE SUR LE TITRE COMPLET, PLUS SUR 60 CARACTÈRES.

Avant ce lot, `_news_loop` de terminal.py dédupliquait ainsi :

    k = (it.get('title') or '')[:60]
    if k and k not in seen:

Deux erreurs opposées, toutes deux réelles :

  FAUX POSITIF   deux dépêches DIFFÉRENTES partageant leurs 60 premiers
                 caractères — cas courant en finance, où les titres ouvrent par
                 une formule figée (« La Réserve fédérale maintient ses taux
                 directeurs inchangés et… ») — la seconde était JETÉE.
                 **De l'information réelle disparaissait du fil.**

  FAUX NÉGATIF   le même article, même lien, titre en casse ou ponctuation
                 différente selon le fournisseur, passait DEUX FOIS.

`news_plus.dedupe_news()` existait dans le dépôt depuis le lot 4, testé, et clé
sur le **titre normalisé complet + le lien**. Le fil ne l'appelait simplement
pas. Ce gardien vérifie les deux moitiés : que le fil l'appelle, et que la
différence de comportement est bien celle annoncée.
"""

import io
import os
import re

from vertex.services.news_plus import dedupe_news

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _boucle_news():
    """Le corps de `_news_loop`, lu sur disque — c'est le code SERVI."""
    src = io.open(os.path.join(_ROOT, 'terminal.py'), encoding='utf-8').read()
    i = src.index('def _news_loop():')
    j = src.index('\ndef ', i + 10)
    return src[i:j]


def _dedupe_prefixe(items, n=60):
    """La déduplication d'AVANT le lot 605, reproduite pour la comparaison."""
    out, seen = [], set()
    for it in items:
        k = (it.get('title') or '')[:n]
        if k and k not in seen:
            seen.add(k)
            out.append(it)
    return out


# ── 1. Le fil appelle bien le dédupeur canonique ────────────────────────────

def test_le_fil_de_news_appelle_le_dedupeur_canonique():
    corps = _boucle_news()
    assert '_news_plus.dedupe_news(feed)' in corps, (
        "Le fil de news doit passer par news_plus.dedupe_news() : c'est le seul "
        "dédupeur testé du dépôt (titre normalisé complet + lien).")


def test_le_fil_ne_deduplique_plus_sur_un_prefixe_de_titre():
    corps = _boucle_news()
    assert not re.search(r"title'\s*\)\s*or\s*''\s*\)\s*\[:\d+\]", corps), (
        "Le fil ne doit plus clé sur une TRONCATURE du titre : deux dépêches "
        "différentes partageant leur ouverture seraient confondues.")


def test_le_dedupe_precede_le_tri_donc_le_premier_arrive_gagne():
    """`dedupe_news` garde le PREMIER de la liste ; dédupliquer après le tri
    changerait silencieusement quel article survit."""
    corps = _boucle_news()
    assert 'dedupe_news(feed)' in corps and 'feed.sort(' in corps, (
        'le fil doit contenir la déduplication ET le tri')
    assert corps.index('dedupe_news(feed)') < corps.index('feed.sort('), (
        'la déduplication doit précéder le tri (le premier arrivé gagne)')


# ── 2. La différence de comportement est bien celle annoncée ────────────────

_DEUX_DEPECHES_DISTINCTES = [
    {'title': 'La Reserve federale maintient ses taux directeurs inchanges et '
              'signale une baisse en juin', 'link': 'https://exemple.test/1'},
    {'title': 'La Reserve federale maintient ses taux directeurs inchanges et '
              'ecarte toute baisse cette annee', 'link': 'https://exemple.test/2'},
]

_MEME_ARTICLE_DEUX_FORMES = [
    {'title': 'Nvidia beats on revenue, raises outlook', 'link': 'https://exemple.test/x'},
    {'title': 'NVIDIA BEATS ON REVENUE - RAISES OUTLOOK', 'link': 'https://exemple.test/x'},
]


def test_deux_depeches_distinctes_survivent_toutes_les_deux():
    """Le faux positif corrigé : de l'information réelle ne disparaît plus."""
    assert len(_dedupe_prefixe(_DEUX_DEPECHES_DISTINCTES)) == 1, (
        'le banc de comparaison ne reproduit plus le défaut — cas à revoir')
    assert len(dedupe_news(_DEUX_DEPECHES_DISTINCTES)) == 2


def test_le_meme_article_en_deux_casses_ne_passe_qu_une_fois():
    """Le faux négatif corrigé : plus de doublon servi."""
    assert len(_dedupe_prefixe(_MEME_ARTICLE_DEUX_FORMES)) == 2, (
        'le banc de comparaison ne reproduit plus le défaut — cas à revoir')
    assert len(dedupe_news(_MEME_ARTICLE_DEUX_FORMES)) == 1


def test_le_senti_reste_pose_sur_chaque_item():
    """Le lot ne touche PAS au sentiment : `senti` reste écrit avant l'ajout au
    fil, et `aggregate()` continue de le lire."""
    corps = _boucle_news()
    assert "it['senti'] = _news_plus.sentiment(" in corps
