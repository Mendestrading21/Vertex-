"""
LOT 386 — LES 38 `except: pass` DE `terminal.py`, LUS UN PAR UN.

Le lot 379 avait fait ce travail pour les 46 de `vertex/`. Le lot 385 a montré
que le recensement s'arrêtait à cette frontière : `terminal.py` en porte 38 que
personne n'avait jamais ouverts. Ce lot les ouvre.

## Classement par ce que le `try` ENTOURE

```
nettoyage / fermeture        6   ← cancelMktData, disconnect, reqMarketDataType
journal / persistance       10   ← beats du scheduler, caches, track_record
import / config optionnel    2   ← dotenv, provider JSON
infra thread                 2   ← boucle asyncio, événement de re-scan
absence honnête             16   ← une donnée externe manque → clé/élément OMIS
examinés de près             2   ← L621 et L1342
```

Les 36 premiers sont sans danger pour l'invariant n°4 : un échec y produit une
**absence**, jamais une valeur inventée. Deux méritaient mieux qu'un coup d'œil.

## L621 — l'overlay IBKR : honnête au moteur, muet au produit

`_apply_ibkr_indices()` écrase les indices différés yfinance par les valeurs
IBKR **temps réel**, et marque chaque entrée touchée `src = 'ibkr'` — le
commentaire dit explicitement « provenance temps réel (honnêteté §4) ». Si
l'overlay échoue, les entrées restent **non marquées** : le mécanisme est
complet et correct côté moteur.

**Mais le marqueur n'atteint aucune surface servie.** Mesuré : les pages
servies (`markets_page.py`, `briefing.py`) lisent `.price`, `.change`, `.spark`
— jamais `.src`. Le seul endroit du dépôt qui rend « TEMPS RÉEL IBKR » vs
« yfinance différé » est `PAGE_ME` (L4741-5189), **l'une des 7 constantes
`PAGE_* mortes` du lot 374**, jamais renvoyée par une route. `indices_live`
part bien au client (`/scan` sérialise `{**scan_state}`) mais **aucun code
client ne le lit**.

Ce n'est pas une malhonnêteté — un cours différé reste un cours réel. C'est la
catégorie du lot 382 : **un énoncé du code plus large que ce que le produit
délivre.** Verdict : rien à corriger ici, mais la pièce fragile est la
**fenêtre de fraîcheur de 75 s** — si elle grandissait, des valeurs IBKR
périmées seraient présentées comme du temps réel. C'est elle que ce gardien
verrouille, avec le marqueur lui-même, pour qu'un affichage futur ait quelque
chose de vrai à lire.

## L1342 — `bret = 0.0` : mesuré, pas excusé

Dans `edge_backtest`, l'échec du calcul du rendement de référence laisse
`bret = 0.0`, qui part dans `analyse(sub, bret)`. J'ai failli l'excuser en
disant que 0 est neutre. **La mesure dit le contraire** : dans
`analysis.py:54`, `rs = clip(50 + (sym_ret − bench_ret) × 200, 0, 100)`.

```
sym +0.10  bench réel +0.15 → rs 40    |  bench 0.0 → rs 70
sym −0.05  bench réel +0.12 → rs 16    |  bench 0.0 → rs 40
sym +0.20  bench réel +0.20 → rs 50    |  bench 0.0 → rs 90
```

La force relative devient une performance absolue. **Ce n'est donc PAS un
neutre** — exactement le piège du lot 378 avec `entry_quality`.

Trois faits l'empêchent d'être une faute : (1) `0.0` est le défaut **déclaré**
de la fonction, atteint aussi sans exception quand `bi <= 63` ; (2) le chemin
de scan **vivant** (L395) passe un `bench_ret` réel — le repli est confiné au
backtest ; (3) `scan_state['edge']` part au client via `/scan` mais **aucune
page servie ne le lit**.

**Caractérisation, pas correction** — jumelle du dossier `context()` du lot 379.
Le test ci-dessous fige la sensibilité mesurée pour qu'on ne puisse plus
l'innocenter par un raisonnement élégant.
"""
import ast
import time

import pytest

FICHIER = 'terminal.py'

# Recensement GELÉ des 38 handlers, par famille. Une dérive réclame un examen.
FAMILLES = {
    'nettoyage/fermeture': 6,
    'journal/persistance': 10,
    'import/config optionnel': 2,
    'infra thread': 2,
    'absence honnête': 16,
    'examinés de près': 2,
}
TOTAL_PASS = 38

# Fenêtre de fraîcheur de l'overlay IBKR. Au-delà, une valeur périmée serait
# présentée comme du temps réel : c'est la borne d'honnêteté du mécanisme.
FENETRE_FRAICHEUR_S = 75


def _pass_secs():
    arbre = ast.parse(open(FICHIER, encoding='utf-8').read())
    return [h.lineno for n in ast.walk(arbre) if isinstance(n, ast.Try)
            for h in n.handlers if all(isinstance(x, ast.Pass) for x in h.body)]


# ── 1. Le dénominateur ──────────────────────────────────────────────────────

def test_le_detecteur_voit_bien_les_trente_huit():
    """Sans dénominateur, la lecture « un par un » ne prouverait rien : si le
    détecteur cassait, le recensement passerait pour complet en couvrant zéro
    handler (leçon des lots 375-377)."""
    n = len(_pass_secs())
    assert n == TOTAL_PASS, (
        '%d `except: pass` dans terminal.py, %d recensés au lot 386 — la '
        'population a changé : reclasser les nouveaux cas par ce que leur '
        '`try` ENTOURE avant de mettre ce chiffre à jour' % (n, TOTAL_PASS))


def test_le_recensement_par_famille_est_complet():
    assert sum(FAMILLES.values()) == TOTAL_PASS, (
        'le classement par famille (%d) ne couvre plus les %d handlers'
        % (sum(FAMILLES.values()), TOTAL_PASS))


# ── 2. L'overlay IBKR : le mécanisme d'honnêteté doit survivre ──────────────

def _seed(monkeypatch, terminal, age_s):
    monkeypatch.setitem(terminal.scan_state, 'indices',
                        [{'name': 'S&P 500', 'price': 100.0, 'change': 0.5}])
    monkeypatch.setitem(terminal.scan_state, 'indices_live', None)
    monkeypatch.setattr(terminal, '_IDX_IBKR', {
        'S&P 500': {'price': 4321.0, 'change': 1.25, 'ts': time.time() - age_s}})


def test_l_overlay_marque_la_provenance_des_valeurs_temps_reel(monkeypatch):
    """Le marqueur `src='ibkr'` est la SEULE trace qui distingue une valeur
    IBKR temps réel d'un cours yfinance différé. Aucune page ne la lit encore
    (mesuré au lot 386), mais la supprimer rendrait la distinction
    définitivement impossible à afficher."""
    import terminal
    _seed(monkeypatch, terminal, age_s=1)
    terminal._apply_ibkr_indices()
    e = terminal.scan_state['indices'][0]
    assert e['price'] == 4321.0, 'la valeur temps réel n\'a pas été appliquée'
    assert e.get('src') == 'ibkr', (
        'marqueur de provenance perdu : plus rien ne distingue le temps réel '
        'IBKR du différé yfinance (invariant n°4)')
    live = terminal.scan_state.get('indices_live')
    assert isinstance(live, dict) and live.get('source') == 'ibkr'


def test_une_valeur_ibkr_perimee_n_est_pas_presentee_comme_temps_reel(monkeypatch):
    """LA propriété d'honnêteté du mécanisme. Si la fenêtre de fraîcheur
    grandissait, un cours vieux de plusieurs minutes serait servi comme du
    temps réel, sans que rien ne le signale."""
    import terminal
    _seed(monkeypatch, terminal, age_s=FENETRE_FRAICHEUR_S + 5)
    terminal._apply_ibkr_indices()
    e = terminal.scan_state['indices'][0]
    assert e['price'] == 100.0, (
        'une valeur IBKR périmée (> %d s) a écrasé le cours différé : elle '
        'serait servie comme du temps réel' % FENETRE_FRAICHEUR_S)
    assert 'src' not in e, 'une valeur périmée a été marquée temps réel'


def test_la_fenetre_de_fraicheur_ne_s_elargit_pas():
    """Anti-dérive de la borne elle-même.

    Première version : `'< 75' in src`. **Creuse** — la preuve ROUGE l'a
    démasquée : la chaîne apparaît 4 fois dans `terminal.py` (deux autres
    fraîcheurs `_live_meta`, plus la docstring), donc élargir la fenêtre de
    l'overlay laissait le test vert. On lit désormais la constante DANS le
    corps de la fonction, par AST.
    """
    arbre = ast.parse(open(FICHIER, encoding='utf-8').read())
    fn = next(n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef) and n.name == '_apply_ibkr_indices')
    bornes = [c.value for n in ast.walk(fn) if isinstance(n, ast.Compare)
              for c in n.comparators
              if isinstance(c, ast.Constant) and isinstance(c.value, (int, float))
              and not isinstance(c.value, bool)]
    assert FENETRE_FRAICHEUR_S in bornes, (
        'la fenêtre de fraîcheur de %d s a disparu du corps de '
        '_apply_ibkr_indices (bornes trouvées : %s) — l\'élargir revient à '
        'présenter des valeurs périmées comme du temps réel'
        % (FENETRE_FRAICHEUR_S, bornes))


def test_l_overlay_ne_reassigne_pas_l_etat_partage():
    """`scan_state` est muté EN PLACE, jamais réassigné (règle d'architecture).
    L'overlay est l'un des rares écrivains directs."""
    arbre = ast.parse(open(FICHIER, encoding='utf-8').read())
    fn = next(n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef) and n.name == '_apply_ibkr_indices')
    for n in ast.walk(fn):
        if isinstance(n, ast.Assign):
            for c in n.targets:
                assert not (isinstance(c, ast.Name) and c.id == 'scan_state'), (
                    'scan_state réassigné dans _apply_ibkr_indices (L%d)' % n.lineno)


# ── 3. `bret = 0.0` : la sensibilité mesurée, figée ─────────────────────────

def test_le_repli_du_rendement_de_reference_n_est_pas_neutre():
    """Fige la mesure qui interdit d'innocenter ce repli par le raisonnement.
    `rs` est une force RELATIVE ; avec `bench_ret = 0`, elle devient une
    performance ABSOLUE — un score très différent, pas un milieu d'échelle.
    """
    import numpy as np

    def rs(sym_ret, bench_ret):
        return float(np.clip(50 + (sym_ret - bench_ret) * 200, 0, 100))

    assert rs(0.10, 0.15) == 40.0 and rs(0.10, 0.0) == 70.0
    assert rs(-0.05, 0.12) == 16.0 and rs(-0.05, 0.0) == 40.0
    ecarts = [abs(rs(s, b) - rs(s, 0.0)) for s, b in
              ((0.10, 0.15), (-0.05, 0.12), (0.20, 0.20))]
    assert min(ecarts) >= 20, (
        'le repli bench_ret=0 serait devenu indolore (écarts %s) — si la '
        'formule de force relative a changé, refaire la caractérisation'
        % ecarts)


def test_la_formule_de_force_relative_est_bien_celle_mesuree():
    """Anti-péremption : la caractérisation ci-dessus ne vaut que tant que la
    formule est celle-là. Si elle change, le lot 386 doit être rejoué."""
    src = open('vertex/engines/analysis.py', encoding='utf-8').read()
    assert '(sym_ret - bench_ret) * 200' in src, (
        'la formule de force relative a changé : la caractérisation du repli '
        'bench_ret=0 (lot 386) doit être refaite sur la nouvelle formule')


def test_le_chemin_de_scan_vivant_passe_un_rendement_reel():
    """Ce qui confine le repli au backtest. Si le scan vivant se mettait à
    appeler `analyse` sans rendement de référence réel, la distorsion mesurée
    ci-dessus atteindrait les scores SERVIS."""
    src = open(FICHIER, encoding='utf-8').read()
    assert 'analyse(df, bench_ret' in src, (
        'le chemin de scan vivant n\'appelle plus analyse() avec un rendement '
        'de référence réel : la distorsion du repli 0.0 atteindrait les '
        'scores servis')


@pytest.mark.parametrize('cle', ['edge', 'indices_live'])
def test_les_cles_non_lues_partent_quand_meme_au_client(cle):
    """Constat figé, pas un reproche : `/scan` sérialise `{**scan_state}`, donc
    ces clés voyagent. Aucune page servie ne les lit (mesuré au lot 386) — si
    l'une gagnait un lecteur, sa caractérisation ci-dessus deviendrait un
    enjeu d'affichage et devrait être revue."""
    src = open(FICHIER, encoding='utf-8').read()
    assert '{**scan_state' in src, (
        '/scan ne sérialise plus scan_state en bloc : revoir ce que la clé '
        '« %s » atteint désormais' % cle)
