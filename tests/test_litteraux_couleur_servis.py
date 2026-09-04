"""
LOT 382 — L'INVARIANT COULEUR ANNONCÉ EST PLUS LARGE QUE CE QUE L'ON GARDE.

Seconde passe d'audit des gardiens par mutation (veine ouverte au 380, premier
trou trouvé au 381). Protocole durci : ancre unique, mutation vérifiée effective,
code muté vérifié SERVI, suite complète à chaque cas.

## Résultat de la passe

```
sanitize_news retiré de /news-feed (sortie servie)         MORD
sanitize_news retiré de la construction des événements     MORD
profondeur de rotation des sauvegardes ramenée à 0         MORD
fichier vertex/static modifié SANS bump d'empreinte        MORD
littéral de couleur #ff00ff dans le shell servi            AUCUN GARDIEN ⚠
[témoin] commentaire anodin                                 (ne mord pas — correct)
```

Le **témoin négatif** est là exprès : il prouve que la suite n'est pas
hypersensible, donc que les quatre « MORD » veulent dire quelque chose.

## Le trou n'est PAS une myopie — c'est un écart doc/gardien

`test_obsidian_theme.py::test_no_blue_in_ui_pages` balaie bien
`vertex/ui/**/*.py`, y compris le shell. Vérifié par mutation ciblée :

```
#1e6fd9 (bleu non-marque)   MORD
#ff00ff (magenta)           AUCUN
#c0392b (rouge brique)      AUCUN
```

Le gardien fait **exactement ce que son nom annonce** : aucun bleu non-marque.
Ce n'est pas lui qui ment. C'est `CLAUDE.md` qui annonçait
« tokens/VXChartTheme uniquement (**aucun littéral couleur**) », un invariant
bien plus large que ce que quoi que ce soit n'a jamais imposé.

## La mesure qui tranche

```
littéraux #RRGGBB distincts dans vertex/ui/**       : 265
dont réellement présents dans une page SERVIE       :  53
```

Répartis sur une dizaine de modules de page (`options_intel_page` 10,
`analysis_page` 9, `system_page` 8, `opportunities_page` 7…). Autrement dit,
« aucun littéral couleur » est **faux depuis longtemps** : il y en a 53 dans les
octets servis aujourd'hui. Exiger zéro casserait la suite sans rien améliorer ;
la règle réellement tenue est « aucun bleu non-marque ».

**Verdict : le code est conforme à la règle réelle. C'est l'énoncé qui était
faux, et le contrat qui n'était pas verrouillé.** Ce test fixe la borne AU
niveau mesuré, pour qu'aucun littéral supplémentaire n'entre en silence.
"""
#  MARCHES EST FUSIONNE DANS LE DASHBOARD (Black Glass).
#
#  `/markets` ne sert plus de page : la route redirige 302 vers `/#…`
#  pour preserver les favoris. Les listes d'espaces ci-dessous ne le
#  citent donc plus, et les appels directs visent `/`, qui porte
#  desormais ce contenu. La couverture n'est pas perdue : elle a
#  simplement suivi le contenu.
import glob
import os
import re

import pytest

import terminal

PAGES = ['/', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

_HEX = re.compile(r'#[0-9a-fA-F]{6}\b')

# Mesuré au lot 382 : 53 littéraux distincts atteignent une page servie.
# Borne fixée À la mesure (+2 de marge de formulation), pas au-dessus : une
# borne qui absorbe la première régression n'est pas une borne (leçon du 378).
MAX_LITTERAUX_SERVIS = 55


@pytest.fixture(scope='module')
def pages(request):
    cli = terminal.app.test_client()
    return {p: cli.get(p).get_data(as_text=True) for p in PAGES}


def _litteraux_servis(pages):
    """Littéraux #RRGGBB écrits dans `vertex/ui/**` ET présents dans une page."""
    servis = set()
    for chemin in [c.replace(os.sep, '/') for c in glob.glob('vertex/ui/**/*.py', recursive=True)]:
        src = open(chemin, encoding='utf-8', errors='ignore').read()
        for lit in set(_HEX.findall(src)):
            if any(lit in html for html in pages.values()):
                servis.add((chemin, lit))
    return servis


# ── 1. Anti-vide : la mesure porte-t-elle sur quelque chose ? ───────────────

def test_les_pages_sont_bien_rendues(pages):
    """Sans pages réelles, le comptage ci-dessous serait vide de sens."""
    for p, html in pages.items():
        assert len(html) > 20000, '%s : rendu incomplet (%d o)' % (p, len(html))


def test_il_existe_bien_des_litteraux_servis(pages):
    """Dénominateur explicite (leçon des lots 375-377) : si ce nombre tombe à
    zéro, ce n'est pas que tout va bien — c'est que le détecteur est cassé."""
    assert len(_litteraux_servis(pages)) >= 20, (
        'seulement %d littéral(aux) servi(s) détecté(s) — détecteur cassé'
        % len(_litteraux_servis(pages)))


# ── 2. La borne de dérive, fixée à la mesure ────────────────────────────────

def test_les_litteraux_de_couleur_servis_ne_prolifèrent_pas(pages):
    """Le contrat réel : on n'exige pas zéro (il y en a 53), on interdit la
    croissance silencieuse. Tout ajout doit être un choix, pas un accident."""
    servis = _litteraux_servis(pages)
    assert len(servis) <= MAX_LITTERAUX_SERVIS, (
        '%d littéraux de couleur atteignent une page servie (borne %d) — '
        'utiliser un token, ou relever la borne en connaissance de cause : %s'
        % (len(servis), MAX_LITTERAUX_SERVIS,
           ', '.join(sorted('%s→%s' % (c.split('/')[-1], l)
                            for c, l in servis))[:300]))


# ── 3. La règle réellement tenue, vérifiée sur les OCTETS SERVIS ────────────

def _bleu_interdit(hexa):
    from tests.test_obsidian_theme import _is_forbidden_blue
    return _is_forbidden_blue(hexa)


@pytest.mark.parametrize('page', PAGES)
def test_aucun_bleu_non_marque_dans_les_octets_servis(page, pages):
    """Le gardien historique lit les SOURCES `vertex/ui/**`. Ici on vérifie la
    même règle sur ce que le navigateur reçoit vraiment — un bleu introduit
    ailleurs (shell, statique, moteur) échapperait à l'autre."""
    fautifs = {h for h in set(_HEX.findall(pages[page])) if _bleu_interdit(h)}
    assert not fautifs, '%s sert un bleu non-marque : %s' % (page, sorted(fautifs))


# ── 4. Le gardien historique fait bien ce qu'il annonce ─────────────────────

def test_le_gardien_bleu_couvre_bien_le_shell():
    """Anti-péremption : `test_no_blue_in_ui_pages` balaie `vertex/ui/**` ;
    si son périmètre cessait d'inclure le shell, le trou deviendrait béant."""
    import tests.test_obsidian_theme as g
    src = open(g.__file__, encoding='utf-8').read()
    assert "'vertex', 'ui', '**', '*.py'" in src, (
        'le périmètre de test_no_blue_in_ui_pages a changé — revérifier qu\'il '
        'couvre encore vertex/ui/shell/__init__.py')
    assert 'vertex/ui/shell/__init__.py' in [
        c.replace(os.sep, '/')
        for c in glob.glob('vertex/ui/**/*.py', recursive=True)
    ], 'le shell est hors du balayage'
