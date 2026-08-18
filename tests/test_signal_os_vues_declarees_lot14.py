"""SIGNAL OS · LES VUES SONT DÉCLARÉES DANS LA SOURCE, PAS DANS MA MÉMOIRE.

## Le défaut, et il est dans mes instruments, pas dans le produit

En auditant Opportunités, j'ai lu les vues **déclarées** et comparé à celles que
mes relevés visitaient depuis cinq lots :

| relevé | URL utilisée | existe ? |
| --- | --- | --- |
| Opportunités | `?view=shortlist`, `?view=compare` | **non** |
| Options | `?view=gex`, `?view=vol` | **non** |

Une vue inconnue retombe sur la vue par défaut (`view = view if view in
dict(_VIEWS) else 'radar'`). Mes relevés mesuraient donc **la même page
plusieurs fois** en croyant en couvrir plusieurs, et ne visitaient **jamais**
`stocks`, `anomalies`, `calendar`, `positioning`, ni les trois vues héritées
d'Options.

**Troisième fois** qu'une URL fabriquée me trompe : au lot 08, l'onglet
`engines` de Système que j'avais inventé puis pris pour un doublon.

### Ce que ça change au lot 12

« 12 graphiques rendus » était faux. Sur les vues réellement déclarées il y en a
**quatorze**, et deux de mes douze étaient le même graphique compté trois fois.
La **conclusion** tient — 0 graphique sans question ni conclusion — et elle tient
désormais sur un échantillon correct et plus grand.

## Le vrai défaut produit, trouvé une fois l'instrument réparé

La vue **Anomalies** — rang 5 de `PAGES.md` §3 — porte 879 px de contenu et
**aucun titre** : son seul intitulé était un `<b>` nu, là où les 25 autres vues
du produit ouvrent sur un titre.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES = os.path.join(_ROOT, 'vertex', 'ui', 'pages')


def _src(nom):
    return io.open(os.path.join(_PAGES, nom), encoding='utf-8').read()


def _vues(nom, symbole='_VIEWS'):
    src = _src(nom)
    m = (re.search(symbole + r'\s*=\s*\((.*?)\n\)', src, re.S)
         or re.search(symbole + r'\s*=\s*\((.*?)\)\s*\n\n', src, re.S))
    return re.findall(r"\('([a-z0-9-]+)'\s*,", m.group(1)) if m else []


# Recensement MESURÉ des vues déclarées. Ce n'est pas une cible : c'est l'état
# constaté, et il sert de contrat aux instruments qui balaient le produit.
_ATTENDU = {
    'markets_page.py': ['overview', 'macro', 'sectors', 'breadth', 'volatility'],
    'opportunities_page.py': ['radar', 'stocks', 'options', 'anomalies', 'calendar'],
    'portfolio_page.py': ['team', 'positions', 'performance', 'risk', 'options', 'watchlist'],
    'options_intel_page.py': ['structure', 'positioning', 'leaps', 'positions',
                              'volatility', 'events'],
    'performance_page.py': ['overview', 'journal', 'learnings', 'progression', 'track-record'],
}


def test_le_recensement_des_vues_ne_derive_pas_en_silence():
    """Une vue ajoutée qu'aucun instrument ne visite est une zone du produit
    que personne ne mesure — et une vue retirée fait retomber les relevés sur
    la vue par défaut **sans erreur**, donc sans que rien ne le signale."""
    ecarts = []
    for nom, attendu in _ATTENDU.items():
        reel = _vues(nom)
        if reel != attendu:
            ecarts.append('%s : %s attendu, %s mesuré' % (nom, attendu, reel))
    reel_sys = _vues('system_page.py', 'VIEWS')
    if reel_sys != ['connections', 'data', 'automations', 'settings', 'archive']:
        ecarts.append('system_page.py : %s' % reel_sys)
    assert not ecarts, (
        'les vues déclarées ont changé :\n  ' + '\n  '.join(ecarts) +
        '\nMettre à jour _ATTENDU **et** vérifier que les instruments de '
        'tools/ couvrent la nouvelle vue — une vue non balayée n\'est mesurée '
        'par personne.')


def test_une_vue_inconnue_retombe_sur_un_defaut_silencieux():
    """LE mécanisme qui a rendu mes URL fabriquées indétectables : elles ne
    produisaient ni 404 ni erreur, juste une autre page. C'est un choix de
    conception défendable — un lien périmé ne casse pas — mais il faut le
    connaître pour ne pas mesurer trois fois la même vue.

    On garde ici le fait que ce repli EXISTE, pour que quiconque écrit un
    instrument sache qu'une URL fausse lui rendra une page valide.
    """
    # DEUX idiomes coexistent, et ma première version n'en connaissait qu'un :
    # elle accusait Marchés à tort. Le repli s'y écrit `if view not in dict(...)`
    # sur deux lignes, pas en expression ternaire. Un gardien qui impose UNE
    # forme d'écriture n'a rien mesuré : il a exigé un style.
    formes = (r'view\s*=\s*view\s+if\s+view\s+in\s+dict\(',
              r'if\s+view\s+not\s+in\s+dict\(')
    for nom in ('opportunities_page.py', 'markets_page.py', 'system_page.py',
                'portfolio_page.py', 'performance_page.py'):
        src = _src(nom)
        assert any(re.search(f, src) for f in formes), (
            '%s ne retombe plus sur une vue par défaut — vérifier ce qu\'une '
            'URL inconnue y produit désormais.' % nom)


def test_la_vue_anomalies_a_un_titre_comme_les_autres():
    """Rang 5 de PAGES.md §3. Elle servait 879 px de contenu sous un `<b>` nu :
    le relevé de structure ne trouvait RIEN sur cet onglet, ce qui ressemblait
    d'abord à une vue vide."""
    src = _src('opportunities_page.py')
    i = src.index('Anomalies par source')
    bloc = src[max(0, i - 200):i + 200]
    assert '<h2>Anomalies par source</h2>' in bloc, (
        'la vue Anomalies a reperdu son titre : elle sert du contenu sous un '
        'intitulé qui n\'en est pas un.')
    assert 'vx-sub' in bloc, (
        'l\'orientation de la vue Anomalies n\'emploie plus la grammaire '
        'd\'en-tête des sept autres espaces.')


def test_l_instrument_de_rognage_derive_ses_vues_de_la_source():
    """Il portait la même liste fabriquée que mes relevés. Une liste écrite à
    la main dans un outil ne peut pas savoir qu'elle est périmée — c'est
    exactement la nature du défaut qu'elle cause."""
    outil = os.path.join(_ROOT, 'tools', 'mesurer_rognage_silencieux.py')
    src = io.open(outil, encoding='utf-8').read()
    assert 'def _vues(' in src, (
        'l\'instrument ne dérive plus ses vues de la source : il peut de '
        'nouveau visiter des URL inexistantes sans que rien ne le signale.')
    assert "_vues('opportunities_page.py')" in src, (
        'la liste des vues d\'Opportunités est redevenue littérale.')
    for invente in ("'shortlist'", "'compare'", "'gex'", "'vol'"):
        assert invente not in src, (
            'un nom de vue FABRIQUÉ est revenu dans l\'instrument : %s' % invente)
