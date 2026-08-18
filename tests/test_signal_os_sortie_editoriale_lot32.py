"""SIGNAL OS · LOT 32 — LA QUATRIÈME SORTIE DE NEWS, QUE PERSONNE NE GARDAIT.

Le lot 31 a montré qu'un gardien critique peut avoir des trous. Même discipline
ici, par mutation, sur les deux invariants les plus coûteux qui restaient : la
sortie XSS (sécurité) et les clés de sync desk (perte de données).

Les clés de sync tiennent (6 mutations sur 6 mordent). La sortie XSS, non — et
la question « pourquoi ces mutations ne mordent-elles pas ? » a mis à jour plus
grave que les mutations elles-mêmes.

## Ce qui a été mesuré

`news_state['items']` est **brut** : la boucle d'actualités (`terminal.py`) y
dépose les titres yfinance/RSS tels quels, et c'est chaque SORTIE qui assainit.
Le gardien du lot 177 en nomme trois — `/news-feed`, `/api/events/<sym>`,
`/api/skyler/<sym>`. Il y en a une quatrième :

    /api/briefing/editorial
      → vertex/market/daily_brief.build_daily_brief  (news_pipeline.collect)
      → vertex/market/editorial.build_narrative      (news_state direct)

Mesuré avant correction, charge injectée dans `news_state` :

    .editorial.narrative      À la une : <script>alert(1)</script>Résultats…
    .daily.what_changed[0]    <img src=x onerror=alert(2)> (<b>Pub</b>)
    .daily.compact[3]         Actualité dominante : <img src=x onerror=…
    .daily.sections[3].text   <img src=x onerror=alert(2)> (<b>Pub</b>, …)
    .what_changed_today[0]    <img src=x onerror=alert(2)> (<b>Pub</b>)

Aucun de ces champs n'était rendu ; les deux seuls consommés (`sources` et
`main_risk`, dans `briefing.py`) passent par `esc()`. **Il n'y avait donc pas de
XSS exploitable** — il y avait une charge vivante à un pas d'un rendu, et rien,
ni test ni documentation, pour dire que ce pas était interdit.

Le commentaire du code affirmait même l'inverse de la mesure : `editorial.py`
étiquetait sa source « actualités (fil assaini) », et l'en-tête de
`news_pipeline` parlait du fil « déjà collecté et assaini ».

## Pourquoi retirer le BALISAGE et non `sanitize_news`

Règle n°5 du projet : deux familles de sorties, deux contrats. Celle-ci est de
la seconde — son rendu échappe. Y appliquer l'assainissement complet
double-échapperait des titres parfaitement légitimes : `AT&T` deviendrait
`AT&amp;T` à l'écran, `Barron's` deviendrait `Barron&#39;s`. Le test
`…n_echappe_pas_le_texte_legitime` interdit précisément cette « correction ».
"""
import json
import re

import pytest

import terminal
from vertex.app.state import news_state
from vertex.market import news_pipeline

MAL = {'sym': 'TSTQ', 'title': '<script>alert(1)</script>Résultats "record"',
       'fr': '<img src=x onerror=alert(2)>', 'publisher': '<b>Pub</b>',
       'link': 'javascript:alert(3)', 'time': '2026-08-17T10:00', 'senti': 1}

# `<` suivi d'une LETTRE ou d'un `/` : une balise. « P/E < 10 » n'en est pas une.
BALISE = re.compile(r'<\s*[A-Za-z/][^>]*>')


@pytest.fixture()
def client():
    sauve = news_state.get('items')
    yield terminal.app.test_client()
    news_state['items'] = sauve


def _textes(o, chemin=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _textes(v, chemin + '.' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _textes(v, chemin + '[%d]' % i)
    elif isinstance(o, str):
        yield chemin, o


# ── 1. La sortie elle-même ──────────────────────────────────────────────────

def test_le_brief_editorial_ne_sert_aucun_balisage(client):
    """La quatrième sortie de news. Elle n'appelle pas `sanitize_news` et ne le
    doit pas — mais elle ne doit jamais laisser passer de balisage."""
    news_state['items'] = [dict(MAL)]
    charge = client.get('/api/briefing/editorial').get_json()
    coupables = [(c, t[:70]) for c, t in _textes(charge) if BALISE.search(t)]
    assert not coupables, 'balisage servi par /api/briefing/editorial : %s' % coupables


def test_le_brief_editorial_ne_sert_aucun_schema_executable(client):
    news_state['items'] = [dict(MAL)]
    blob = json.dumps(client.get('/api/briefing/editorial').get_json(), ensure_ascii=False)
    assert 'javascript:' not in blob and 'onerror=' not in blob


def test_le_brief_editorial_n_echappe_pas_le_texte_legitime(client):
    """Le contre-poids : ce qui interdit de « corriger » avec `sanitize_news`.
    Ces trois formes existent dans de vrais titres financiers."""
    news_state['items'] = [{'title': "AT&T : Barron's voit un P/E < 10 \"solide\"",
                            'publisher': "Barron's", 'link': 'https://ex.com/a',
                            'time': '2026-08-17T10:00'}]
    charge = client.get('/api/briefing/editorial').get_json()
    narratif = (charge.get('editorial') or {}).get('narrative') or ''
    assert "AT&T : Barron's voit un P/E < 10 \"solide\"" in narratif, (
        'titre déformé par la sortie — %r' % narratif[-160:])
    blob = json.dumps(charge, ensure_ascii=False)
    for entite in ('&amp;', '&#39;', '&quot;', '&lt;'):
        assert entite not in blob, (
            '%s servi : la sortie échappe alors que son rendu échappe déjà — '
            'le lecteur verrait l\'entité brute' % entite)


# ── 2. Le point d'entrée du texte externe dans le narratif ──────────────────

def test_le_pipeline_retire_le_balisage_des_champs_texte():
    ev = news_pipeline.collect({'items': [dict(MAL)]})['events'][0]
    assert ev['title'] == 'alert(1)Résultats "record"'
    assert ev['title_fr'] is None          # entièrement fait de balisage → vidé
    assert ev['source'] == 'Pub'


def test_le_pipeline_supprime_un_lien_non_http():
    ev = news_pipeline.collect({'items': [dict(MAL)]})['events'][0]
    assert ev['link'] is None, 'schéma exécutable conservé dans un événement servi'
    ok = news_pipeline.collect({'items': [dict(MAL, link='https://ex.com/a?b="c"')]})
    assert ok['events'][0]['link'] == 'https://ex.com/a?b=%22c%22'


def test_un_titre_entierement_balise_est_rejete_et_compte():
    """Un titre qui n'est QUE du balisage n'est pas un titre. Il est rejeté —
    et le rejet est compté, jamais masqué (contrat du module)."""
    r = news_pipeline.collect({'items': [dict(MAL, title='<b></b>', fr='')]})
    assert r['events'] == [] and r['rejected'] == 1


# ── 3. Ce sur quoi la sûreté repose côté rendu ──────────────────────────────

def test_les_deux_champs_consommes_du_brief_sont_echappes_au_rendu():
    """Les seuls champs de `/api/briefing/editorial` réellement rendus. Leur
    sûreté ne tient à rien d'autre qu'à ces deux `esc()` : les perdre rouvrirait
    la porte que le lot referme côté serveur."""
    src = open('vertex/ui/pages/briefing.py', encoding='utf-8').read()
    assert "esc((b.sources||[]).join(', '))" in src, (
        'la liste des sources (nom d\'éditeur EXTERNE) n\'est plus échappée')
    assert "'<p class=\"vx-today-decision\" data-tone=\"'+tone+'\">'+esc(decision)+'</p>'" in src, (
        'la phrase de décision du hero n\'est plus échappée')
