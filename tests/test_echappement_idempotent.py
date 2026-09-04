"""Vertex Test 1.0 — L'ÉCRAN AFFICHAIT `Today&#39;s Market`.

## Ce qui a été vu, le 27 août 2026, sur le desk réel

Trois dépêches de la première page du Dashboard :

```text
Micron, Sandisk, … Stocks That Explain Today&amp;#39;s Market -- Barrons.com
Dow Falls Ahead of &amp;#39;Economic D-Day&amp;#39; … -- IBD
CFA Technology : examen d&amp;#39;initié pour le week-end …
```

L'apostrophe était échappée **deux fois**.

## Pourquoi

Dow Jones et IBKR envoient des titres **déjà porteurs d'entités HTML** :
`Today&#39;s Market`. `_clean_text` échappait sans décoder, donc le `&` de
`&#39;` devenait `&amp;`, et le navigateur affichait littéralement `&#39;`.

Le défaut n'existait pas tant que le fil du scan n'était pas assaini — il est
apparu **avec** la fermeture de la faille XSS de ce fil. Fermer une brèche a
révélé un défaut d'affichage qu'elle masquait.

## La correction

Décoder d'abord, échapper ensuite. L'opération devient **idempotente** : un
texte déjà propre traverse sans être abîmé, et rien ne s'accumule si le texte
passe deux fois par le point de sortie.

## Pourquoi décoder n'ouvre pas de brèche

L'échappement final s'applique au texte **décodé** et reste le dernier mot.
Mieux : le retrait de balises voit désormais une balise écrite `&lt;script&gt;`,
qui passait auparavant pour du texte. La garde est plus forte, pas plus faible
— et les bancs ci-dessous le prouvent dans les deux sens.
"""
from __future__ import annotations

import pytest

from vertex.services.news_plus import _clean_text, sanitize_news


#  ═══════════  1. l'idempotence, le cœur du lot  ══════════════════════════════

@pytest.mark.parametrize('texte', [
    "Today&#39;s Market",                 # entite deja presente (Dow Jones)
    "L'apostrophe nue",                   # texte brut
    "a &amp; b",                          # esperluette deja encodee
    'Il a dit "bonjour"',                 # guillemets nus
    "&quot;deja encode&quot;",            # guillemets deja encodes
    "rien de special",
])
def test_assainir_DEUX_fois_ne_change_rien(texte):
    """Le défaut nu : chaque passage ajoutait une couche d'échappement."""
    une = _clean_text(texte)
    assert _clean_text(une) == une, (
        'echappement non idempotent : %r -> %r -> %r'
        % (texte, une, _clean_text(une)))


def test_le_cas_REEL_de_Dow_Jones():
    """Le titre exact vu sur le desk."""
    t = "Stocks That Explain Today&#39;s Market -- Barrons.com"
    assert '&amp;#39;' not in _clean_text(t)
    assert _clean_text(t) == "Stocks That Explain Today&#39;s Market -- Barrons.com"


def test_une_apostrophe_NUE_est_bien_echappee():
    """Contre-épreuve : rendre l'opération idempotente ne doit pas revenir à
    ne plus échapper."""
    assert _clean_text("L'apostrophe") == 'L&#39;apostrophe'


#  ═══════════  2. la garde est plus FORTE, pas plus faible  ═══════════════════

def test_une_balise_NUE_est_retiree():
    assert '<script' not in _clean_text('<script>alert(1)</script>')


def test_une_balise_ENCODEE_est_retiree_AUSSI():
    """Le gain du décodage préalable : `&lt;script&gt;` passait avant pour du
    texte et ressortait visible. Le retrait la voit désormais."""
    assert 'script' not in _clean_text('&lt;script&gt;alert(1)&lt;/script&gt;')


@pytest.mark.parametrize('charge', [
    '<img src=x onerror=alert(1)>',
    '&lt;img src=x onerror=alert(1)&gt;',
    '<svg/onload=alert(1)>',
    "</script><script>alert(1)</script>",
    '&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;',
])
def test_aucune_charge_hostile_ne_ressort_ACTIVE(charge):
    """Le contrôle qui compte : après passage, plus aucun chevron brut, donc
    rien qui puisse redevenir une balise dans innerHTML."""
    r = _clean_text(charge)
    assert '<' not in r and '>' not in r, r


def test_le_double_passage_ne_reactive_RIEN():
    """Une charge assainie deux fois ne doit pas se recomposer — c'est
    précisément le risque qu'un décodage introduirait s'il était mal placé."""
    charge = '&lt;script&gt;alert(1)&lt;/script&gt;'
    une = _clean_text(charge)
    assert '<' not in _clean_text(une) and '>' not in _clean_text(une)


#  ═══════════  3. le point de sortie complet  ═════════════════════════════════

def test_sanitize_news_est_idempotent_sur_un_item_reel():
    item = [{'title': "Dow Falls Ahead of &#39;Economic D-Day&#39; -- IBD",
             'pub': 'IBD', 'link': 'https://example.com/a', 'sym': 'SPY'}]
    une = sanitize_news(item)
    deux = sanitize_news(une)
    assert une == deux
    assert '&amp;#39;' not in une[0]['title']


def test_le_lien_reste_SUR_apres_deux_passages():
    """Contre-épreuve croisée : l'idempotence du texte ne doit pas relâcher le
    filtre de schéma."""
    hostile = [{'title': 'x', 'link': 'javascript:alert(1)'}]
    une = sanitize_news(hostile)
    assert not (une[0].get('link') or '').lower().startswith('javascript')
    assert sanitize_news(une)[0].get('link') == une[0].get('link')
