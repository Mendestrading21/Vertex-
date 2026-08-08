"""
LOT 383 — TROIS INVARIANTS CONFRONTÉS, TROIS RÉELLEMENT IMPOSÉS.

Troisième passe d'audit des gardiens par mutation. Les lots 381 et 382 avaient
trouvé un écart chacun ; **celui-ci n'en trouve aucun**, et c'est le résultat.

## Résultat de la passe

```
apostrophes déséchappées dans un bloc JS SERVI       MORD
nom personnel injecté dans une page servie           MORD
scan_state réassigné dans un CONSOMMATEUR            MORD
ENGINE_VERSION : recul 0.9.0 → 0.8.0                 MORD
ENGINE_VERSION : bond   0.9.0 → 1.4.0                passe (plancher, voir ci-dessous)
demo_mode masqué                                      mutation sans effet servi
[témoin] aucune modification                          ne mord pas — correct
```

## Deux mutations d'abord fautives — le protocole a fonctionné

**`scan_state`.** Ma première mutation réassignait `scan_state` **dans
`vertex/app/state.py`** — or ce fichier est le `HOME` déclaré du gardien
`test_scan_state_invariant_lot217`, **exclu du scan par conception** : c'est le
domicile légitime de l'affectation. Rejouée dans un **consommateur**
(`routes/system.py`), la violation est attrapée immédiatement.

**`demo_mode`.** Passer `demo_mode=DEMO_MODE` à `demo_mode=False` ne change
**aucun octet servi** : `/system` rend le même MD5 (`73e917c0f2d0`, 82 837 o)
avant et après. `DEMO_MODE` vaut pourtant bien `True` au runtime — la mutation
était effective dans la source, mais ce point d'appel n'atteint pas la page.
Aucune conclusion sur un gardien n'est donc possible ; c'est une mutation
invalide, pas un trou.

Deux fois sur trois, le « AUCUN GARDIEN » initial accusait à tort. La règle du
lot 379 continue de payer : **un cas qui ne mord pas accuse d'abord la
mutation**, puis le périmètre, et seulement ensuite le gardien.

## Le seul écart : un plancher, pas une égalité

« skyler_core 0.9.0 intact » suggère une égalité. Le gardien réel
(`test_catalyst_type_lot30::test_engine_version_bumped_prospective`) impose
`parts >= (0, 9, 0)` : un **recul** échoue, un **bond en avant** passe.

C'est un cas de **gardien plus étroit que l'énoncé** (la distinction du lot 382)
— mais ici, contrairement au 382, **la règle réelle est la bonne** : une montée
de version est légitime, une régression ne l'est pas. Rien à corriger ; c'est
l'énoncé qui gagne à être dit précisément, et ce test le fixe.

**Verdict : sain, rien touché.**
"""
import re

import pytest

import terminal
from vertex.engines import skyler_core

PAGES = ['/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

_INLINE = re.compile(r'<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>', re.S | re.I)


@pytest.fixture(scope='module')
def pages():
    cli = terminal.app.test_client()
    return {p: cli.get(p).get_data(as_text=True) for p in PAGES}


# ── 1. La version du cœur : un PLANCHER, dit explicitement ──────────────────

def test_la_version_du_coeur_ne_peut_que_monter():
    """Ce que le gardien historique impose vraiment : `>= (0, 9, 0)`. Un recul
    échoue (vérifié par mutation : 0.8.0 fait tomber la suite), une montée
    passe. L'énoncé « 0.9.0 intact » laissait croire à une égalité."""
    parts = tuple(int(x) for x in skyler_core.ENGINE_VERSION.split('.'))
    assert parts >= (0, 9, 0), (
        'régression de la version du cœur : %s' % skyler_core.ENGINE_VERSION)


def test_le_plancher_de_version_est_bien_un_plancher_et_non_une_egalite():
    """Anti-dérive de la caractérisation : si quelqu'un durcit un jour en
    égalité stricte, ce test le dira — et le rapport du lot 383 devra être relu
    avant d'accepter le changement."""
    import tests.test_catalyst_type_lot30 as g
    src = open(g.__file__, encoding='utf-8').read()
    assert 'parts >= (0, 9, 0)' in src, (
        'le gardien de version n\'impose plus un plancher — relire SKYLER-LOT-383')


# ── 2. Le JS servi : les apostrophes restent échappées ──────────────────────

def test_le_js_inline_servi_contient_bien_des_apostrophes_echappees(pages):
    """Anti-vide : si ce nombre tombe à zéro, la règle n°2 n'a plus de surface
    et le test suivant ne prouverait plus rien. Mesuré : 31 sur les 8 pages."""
    total = sum(b.count("\\'") for html in pages.values()
                for b in _INLINE.findall(html))
    assert total >= 20, (
        'seulement %d apostrophe(s) échappée(s) dans le JS inline servi — '
        'la règle n°2 a perdu sa surface, revoir ce gardien' % total)


def test_le_balayage_node_couvre_bien_les_pages_servies():
    """Ce qui protège réellement la règle n°2, c'est `node --check` sur chaque
    bloc inline (`test_js_syntax_sweep_lot182`) — un vrai parseur, pas une
    heuristique.

    Note de méthode : ce gardien comptait d'abord la parité des quotes simples
    hors échappement. Il criait au loup sur les 8 pages — les quotes vivent
    aussi dans des chaînes à guillemets doubles, des regex et des commentaires,
    où la parité ne veut rien dire. Un gardien qui accuse du code sain finit
    désactivé : remplacé par la vérification que le vrai parseur couvre encore
    les pages servies."""
    import tests.test_js_syntax_sweep_lot182 as g
    src = open(g.__file__, encoding='utf-8').read()
    assert 'node' in src and '--check' in src, (
        'le balayage JS n\'utilise plus un vrai parseur')
    manquantes = [p for p in PAGES if "'%s'" % p not in src]
    assert not manquantes, (
        'pages servies absentes du balayage `node --check` : %s' % manquantes)


# ── 3. Aucun nom personnel dans les octets servis ───────────────────────────

@pytest.mark.parametrize('page', PAGES)
def test_aucun_marqueur_de_nom_personnel_dans_les_octets_servis(page, pages):
    """Le gardien historique (`test_namespace_guards`) balaie l'arbre ; ici on
    vérifie la même règle sur ce que le navigateur reçoit vraiment."""
    html = pages[page]
    for marqueur in ('auteur:', 'author:', '@author'):
        assert marqueur not in html.lower(), (
            '%s sert un marqueur d\'auteur (%r)' % (page, marqueur))


def test_le_gardien_de_noms_couvre_encore_l_arbre_courant():
    """Anti-péremption : si `test_no_personal_name_in_current_tree` disparaît,
    la vérification sur les octets servis ci-dessus devient le seul filet."""
    import tests.test_namespace_guards as g
    assert hasattr(g, 'test_no_personal_name_in_current_tree'), (
        'le gardien de noms personnels a disparu — revoir le périmètre')


# ── 4. scan_state : le domicile est exclu, les consommateurs non ────────────

def test_le_gardien_scan_state_exclut_le_domicile_et_scanne_la_production():
    """Ma première mutation a échoué parce qu'elle visait le HOME, exclu par
    conception. Ce test fixe cette sémantique : si le HOME changeait de nom ou
    si le scan cessait de couvrir la production, la protection deviendrait
    vide sans que rien ne le signale."""
    import tests.test_scan_state_invariant_lot217 as g
    src = open(g.__file__, encoding='utf-8').read()
    assert "HOME = 'vertex/app/state.py'" in src, (
        'le domicile déclaré de scan_state a changé — revoir le gardien')
    assert "'vertex' / '**' / '*.py'" in src.replace('"', "'"), (
        'le scan ne couvre plus tout le paquet vertex — protection amoindrie')
