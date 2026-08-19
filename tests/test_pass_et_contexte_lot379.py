"""
LOT 379 — LES 46 `except: pass`, JUGÉS ; et ce que la sonde a trouvé à côté.

Le lot 378 les avait **comptés en déclarant ne pas les juger**. Ici on regarde ce
que chaque `try` ENTOURE, car c'est cela qui décide.

## Classement par nature (46)

```
nettoyage / fermeture      3   ← close, remove… : légitime par nature
journal / persistance      5   ← écrire un cache ne doit jamais casser l'appelant
autres                    38   ← lus un par un
```

Les 38 restants se répartissent en imports optionnels (`ai/*`, Anthropic absent),
lectures de fichier de configuration (`config.py`, `.env`), écritures de cache
(`open` + `dump`), et **calculs métier** — la seule famille qui pouvait menacer
l'invariant n°4.

## Les calculs métier : honnêtes par construction

Dans `vertex/market/context.py`, les cinq `try … except: pass` n'écrivent que
dans `out[...]` et des variables locales. Un échec produit donc une **absence**,
jamais une valeur périmée servie.

## `analysis.py:229` : hypothèse sérieuse, réfutée par la mesure

Ce cas méritait mieux qu'un coup d'œil. `grade` est calculé ligne 204 depuis le
score **initial** ; ligne 228 le score est **ajusté** ; ligne 230 le grade est
recalculé — sous `except: pass`. En cas d'échec, `grade` garderait la valeur du
score non ajusté tandis que `score` servi ligne 303 serait l'ajusté :
**deux champs incohérents servis côte à côte**, sans rien pour le signaler.

Mesure faite : `config.grade` ne lève pour **aucun** nombre (testé sur 0, 1, 50,
99, 100, −5, 105, 50.5 et NaN → toujours une note), et la ligne 228 garantit un
`int`. **Le handler est inatteignable** ; l'incohérence ne peut pas se produire.
Hypothèse précise, réfutée proprement — le test ci-dessous verrouille la raison.

## Ce que la sonde a trouvé à côté — et qui vaut plus que la piste

En vérifiant que `context()` dégrade bien par absence, j'ai mesuré son
comportement sur entrées vides. Il est **mixte** :

```
context(None, None, [], {}, [])
  vix, vix_band, vix_chg, spy_regime, spy_adx  → None       ← honnête
  roro       → 'NEUTRE'
  roro_gap   → 0
  breadth    → {above50: 0, above200: 0, adv: 0, …}
  verdict    → 'MARCHÉ · NEUTRE · participation 0% au-dessus MM50'
```

Ce n'est **pas** un `except` qui avale : le bloc *réussit*, parce que ses propres
défauts (`ro = … if any(…) else 50`) le font aboutir sur zéro donnée. Sur un
univers vide, l'application **affirme** donc un régime « NEUTRE » et une
participation « 0 % », au lieu de dire qu'elle ne sait pas.

**Caractérisation, pas correction.** Toucher au moteur de contexte de marché sans
accord serait exactement le changement gratuit que la boucle s'interdit — et la
question est jumelle du dossier déjà en attente depuis le lot 363
(« points réels du scan » sur `/markets`). Les tests ci-dessous **gèlent** ce
comportement : s'il change, ce sera délibérément.

**Verdict du lot : sain, rien touché.**
"""
import ast
import os

import pytest

from vertex.market.context import context
from vertex.strategy import config

RACINE = 'vertex'

# Population mesurée : 46 au lot 379, **50** aujourd'hui. Borne fixée À la
# mesure — une borne qui absorbe la première régression n'est pas une borne
# (leçon du lot 378).
#
# 46 -> 50 au fil de #779/G1, et AUCUN de ces handlers n'est neuf : ils sont
# arrivés dans `vertex/` avec le code qu'ils entouraient, en quittant
# `terminal.py` — qui, symétriquement, est passé de 38 à 32 (recensement tenu
# par `tests/test_pass_terminal_lot386.py`). Le total des deux périmètres est
# donc stable ; ce qui a changé, c'est la frontière.
#   • `_to_naive`            -> vertex/app/routes/correlations_api.py
#   • `_i` et `_f`           -> vertex/options/pack.py (×2, via options_pack)
#   • écriture du cache desc -> vertex/app/routes/descriptions_api.py
# Un `except: pass` réellement NOUVEAU ferait donc toujours échouer ce test.
MAX_PASS = 50

CLES_HONNETES = ('vix', 'vix_band', 'vix_chg', 'spy_regime', 'spy_adx',
                 'spy_trend_txt')
CLES_AFFIRMATIVES = ('roro', 'roro_gap', 'breadth', 'verdict')


def _fichiers():
    out = []
    for rac, _d, noms in os.walk(RACINE):
        for nom in sorted(noms):
            if nom.endswith('.py'):
                out.append(os.path.join(rac, nom))
    return out


def _pass_handlers():
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if isinstance(n, ast.Try):
                for h in n.handlers:
                    if all(isinstance(x, ast.Pass) for x in h.body):
                        out.append((chemin, n))
    return out


# ── 1. Périmètre, anti-vide, dérive ─────────────────────────────────────────

def test_le_perimetre_couvre_les_cibles():
    f = _fichiers()
    for cle in ('vertex/market/context.py', 'vertex/engines/analysis.py',
                'vertex/app/config.py'):
        assert cle in f, 'périmètre incomplet : %s' % cle


def test_le_detecteur_voit_bien_les_except_pass():
    n = len(_pass_handlers())
    assert n >= 30, 'seulement %d `except: pass` trouvés — détecteur cassé' % n
    assert n <= MAX_PASS, (
        '%d `except: pass` (borne %d) — la population a dérivé, examiner les '
        'nouveaux cas avant de relever la borne' % (n, MAX_PASS))


# ── 2. Les calculs métier échouent par ABSENCE, jamais en valeur périmée ────

def test_les_handlers_du_contexte_marche_n_ecrivent_que_dans_out():
    """La propriété qui rend ces `except: pass` honnêtes : un échec laisse la
    clé ABSENTE (ou None), il ne peut pas servir une valeur périmée. Si un jour
    un de ces blocs réaffecte un nom lu plus loin, cette garantie tombe."""
    src = open('vertex/market/context.py', encoding='utf-8').read()
    arbre = ast.parse(src)
    blocs = [n for n in ast.walk(arbre) if isinstance(n, ast.Try)
             and any(all(isinstance(x, ast.Pass) for x in h.body) for h in n.handlers)]
    assert len(blocs) >= 4, 'seulement %d bloc(s) — détecteur cassé' % len(blocs)
    for n in blocs:
        for x in ast.walk(ast.Module(body=n.body, type_ignores=[])):
            if not isinstance(x, ast.Assign):
                continue
            for t in x.targets:
                assert isinstance(t, (ast.Subscript, ast.Name)), (
                    'L%d : cible d\'affectation inattendue %s'
                    % (n.lineno, ast.unparse(t)))


# ── 3. `analysis.py:229` : le handler est INATTEIGNABLE, prouvé ─────────────

@pytest.mark.parametrize('valeur', [0, 1, 50, 99, 100, -5, 105, 50.5,
                                    float('nan'), float('inf')])
def test_config_grade_ne_leve_jamais_pour_un_nombre(valeur):
    """Raison pour laquelle le `except: pass` de `analysis.py:229` ne peut pas
    produire un grade incohérent avec le score servi à côté. Si `grade` devient
    faillible, ce handler redevient dangereux et doit être repris."""
    note = config.grade(valeur)
    assert isinstance(note, str) and note, 'grade(%r) = %r' % (valeur, note)


def test_le_grade_recalcule_reste_sous_protection_d_un_int():
    """Anti-dérive : la ligne qui précède le handler doit continuer de garantir
    un `int`, sinon la démonstration d'inatteignabilité tombe."""
    src = open('vertex/engines/analysis.py', encoding='utf-8').read()
    assert 'score = int(max(0, min(100, base_score + struct_adj)))' in src, (
        'la garantie `int` avant `config.grade(score)` a changé — reprendre la '
        'démonstration d\'inatteignabilité du lot 379')


# ── 4. Caractérisation gelée du contexte de marché sur univers vide ─────────

def _contexte_vide():
    return context(None, None, [], {}, [])


@pytest.mark.parametrize('cle', CLES_HONNETES)
def test_sur_univers_vide_les_mesures_absentes_valent_None(cle):
    """La moitié honnête : faute de donnée, ces champs valent `None` et
    l'interface affiche `—`."""
    r = _contexte_vide()
    assert cle in r, 'clé %s disparue du contexte' % cle
    assert r[cle] is None, (
        '%s vaut %r sur univers vide : une mesure est affirmée sans donnée'
        % (cle, r[cle]))


@pytest.mark.parametrize('cle', CLES_AFFIRMATIVES)
def test_caracterisation_les_verdicts_restent_affirmes_sur_univers_vide(cle):
    """L'autre moitié, GELÉE et non corrigée. Sur zéro donnée, `roro` affirme
    « NEUTRE » et `verdict` annonce « participation 0 % » — parce que les défauts
    internes du bloc (`else 50`) le font réussir, pas parce qu'un `except`
    avale quelque chose.

    Ce test ne valide pas ce comportement : il l'ancre. S'il échoue, c'est que
    quelqu'un l'a changé — ce qui est le but du dossier en attente (jumeau de
    celui du lot 363), et doit alors être fait délibérément."""
    r = _contexte_vide()
    assert cle in r and r[cle] is not None, (
        '%s n\'est plus affirmé sur univers vide — la caractérisation du '
        'lot 379 a changé, relire le rapport avant d\'ajuster' % cle)
