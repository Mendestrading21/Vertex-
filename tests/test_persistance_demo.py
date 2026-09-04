"""
LOT 391 — UN SCAN EN MODE DÉMO ÉCRIT DANS L'HISTORIQUE BREADTH RÉEL, ET SERVI.

Piste ouverte par une observation du lot 390 : lancer le serveur DEMO modifie
~8 fichiers runtime. Mesurée ici.

## Ce que les données disaient déjà, avant toute manipulation

`breadth_history.json` portait **16 points strictement identiques** —
`a50 50 · a200 45 · net −4 · health 37` — du 2026-07-21 au 2026-08-08, un par
jour. La participation réelle d'un marché ne reste pas figée seize séances de
suite : c'est la signature exacte de la pollution GEX du lot 388.

## Le lien causal, prouvé

```text
avant scan DEMO : 16 points, dernier {"d": "2026-08-08", "a50": 50, …}
après scan DEMO : 17 points, dernier {"d": "2026-08-09", "a50": 50, …}
dates ajoutées  : ['2026-08-09']
```

Le site d'écriture (`terminal.py`, section « BAROMÈTRE / INTERNALS ») est
**inconditionnel** : aucun test de `DEMO_MODE`. Et il n'ajoute pas seulement —
`if _bh[-1]['d'] == _today: _bh[-1] = _snap` **écrase** le point du jour, donc un
scan de démo lancé après un scan réel remplace la mesure du jour.

## Pourquoi c'est un enjeu d'honnêteté

`internals['history']` part dans `/scan` (17 points servis, mesuré) et
`markets_page.py` le consomme pour « Tendance de participation » — le commentaire
du code dit lui-même « historique breadth **RÉEL** ».

Pendant une session de démo l'utilisateur est prévenu : `/markets` sert un
`vx-demo-banner` et `/scan` expose `source = 'demo'`. **Mais le point persisté ne
porte aucune provenance** : `{d, a50, a200, net, health}`. Lors d'une session
RÉELLE ultérieure — sans bannière, `source` réelle — les points de démo sont
servis au milieu des vrais, indistinguables.

Le contre-exemple est dans le dépôt : `market_context_last.json` **est** écrit
avec un champ `demo`. Le mécanisme honnête existe donc ; il n'est simplement pas
appliqué à l'historique breadth.

## Ce que ce lot NE fait pas, et pourquoi

**Aucun fichier de production n'est modifié.** Ajouter un garde `DEMO_MODE`
autour de la persistance serait une **décision de conception**, pas la réparation
d'une incohérence : mesuré, **aucune** persistance du dépôt ne garde ce mode. Et
trois issues sont défendables — ne pas persister en démo, marquer le point, ou
assumer que la démo peuple l'historique. Ce choix revient à l'utilisateur ; le
dossier part au **rang 1** du classement du lot 390.

La purge des 16 points déjà accumulés relève de la même décision : c'est une
donnée runtime, elle n'est pas supprimée d'office.

## Une part de cette pollution vient de la boucle elle-même

Les vérifications de tranche de l'agent lancent le serveur DEMO. Les points
antérieurs au 2026-08-08 en portent la trace. **Le rituel de copie de sûreté et
de restauration adopté aux lots 388-390 a arrêté cette contribution** — le point
du 2026-08-09 créé par la mesure de ce lot a été restauré à l'octet. Ce qui
demeure, c'est l'exposition générale : elle ne dépend pas de l'agent.

## Ce que ce gardien verrouille

Les **mécanismes de distinction qui existent aujourd'hui** — pas le défaut. Un
gardien qui figerait l'absence de marqueur accuserait la correction future ; ces
tests-là restent verts quelle que soit l'issue retenue.
"""
import ast

import pytest

TERMINAL = 'terminal.py'


def _arbre(chemin):
    return ast.parse(open(chemin, encoding='utf-8').read())


# ── 1. Anti-vide : la chaîne persistance → service existe toujours ──────────

def test_l_historique_breadth_est_bien_persiste():
    """Sans ce site d'écriture, tout ce qui suit est sans objet — et un gardien
    sans objet passe au vert pour la mauvaise raison."""
    sites = [n for n in ast.walk(_arbre(TERMINAL))
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == '_save_json' and n.args
             and isinstance(n.args[0], ast.Constant)
             and n.args[0].value == 'breadth_history.json']
    assert len(sites) == 1, (
        '%d sites d\'écriture de breadth_history.json, 1 mesuré au lot 391 — '
        'si la persistance a disparu ou s\'est multipliée, le dossier de '
        'provenance change de nature' % len(sites))


def test_l_historique_breadth_atteint_bien_la_page_servie():
    """La gravité du dossier tient à ce que l'historique est SERVI. Si
    `/markets` cessait de le lire, il n'y aurait plus d'enjeu d'affichage."""
    src = open('vertex/ui/pages/markets_page.py', encoding='utf-8').read()
    assert 'scan.internals.history' in src, (
        '/markets ne consomme plus `internals.history` : la « Tendance de '
        'participation » ne sert plus l\'historique breadth — revérifier le '
        'dossier de provenance du lot 391')
    src_t = open(TERMINAL, encoding='utf-8').read()
    assert "internals['history']" in src_t, \
        'l\'historique n\'est plus publié dans internals — chaîne rompue'


# ── 2. Les marqueurs de provenance qui EXISTENT ne doivent pas disparaître ──

def test_le_contexte_marche_reste_persiste_avec_sa_provenance():
    """`market_context_last.json` est le **contre-exemple honnête** du dépôt :
    il est écrit avec un champ `demo`. C'est le modèle que l'historique breadth
    n'applique pas ; s'il disparaissait, le dépôt perdrait sa seule persistance
    datée et marquée."""
    src = open('vertex/app/routes/feeds.py', encoding='utf-8').read()
    assert 'demo=_demo' in src, (
        'le contexte marché n\'est plus construit avec son drapeau de '
        'provenance : la seule persistance honnête du dépôt perd sa marque')
    assert "save_json('market_context_last.json'" in src, \
        'la persistance du contexte marché a disparu'


def test_le_scan_expose_sa_source():
    """`source = 'demo'` est le marqueur qui permet à l'utilisateur — et à
    l'interface — de savoir que la session en cours n'est pas réelle."""
    arbre = _arbre(TERMINAL)
    src = open(TERMINAL, encoding='utf-8').read()
    #  Lot 42 — le marquage n'est plus une écriture éparse mais une clé du bloc
    #  publié atomiquement : `{'source': 'demo'} if DEMO_MODE` dans _publier.
    #  Même invariant (une session démo se DIT démo), forme de publication saine.
    assert "'source': 'demo'" in src, (
        'le scan ne marque plus sa source en mode démo : plus rien ne '
        'distingue une session de démonstration d\'une session réelle')
    #  #779/G1 — `data_source` est SERVI par `/scan`, qui a quitte terminal.py
    #  pour `vertex/app/routes/scan_api.py`. Le marquage (`source = 'demo'`)
    #  reste dans le monolithe, la SORTIE est ailleurs : chercher les deux au
    #  meme endroit faisait echouer ce test sur une chaine intacte.
    sortie = _arbre('vertex/app/routes/scan_api.py')
    sert = [n for n in ast.walk(sortie)
            if isinstance(n, ast.Constant) and n.value == 'data_source']
    assert sert, 'la source n\'est plus exposée aux consommateurs'


@pytest.mark.parametrize('page', ['markets_page.py', 'briefing.py'])
def test_les_pages_gardent_leur_banniere_de_demo(page):
    """Pendant une session de démo, la bannière est le seul avertissement
    visible. Elle ne couvre pas l'historique persisté — mais la retirer
    aggraverait le dossier au lieu de le résoudre."""
    src = open('vertex/ui/pages/' + page, encoding='utf-8').read()
    assert 'vx-demo-banner' in src, (
        '%s ne sert plus de bannière de démo : une session de démonstration '
        'deviendrait indistinguable d\'une session réelle' % page)


# ── 3. La forme du point persisté, sans figer le défaut ─────────────────────

def test_le_point_persiste_garde_ses_champs_de_mesure():
    """On fige les champs de MESURE, pas l'absence de provenance : si le
    dossier est tranché en ajoutant un marqueur, ce test reste vert. Un gardien
    qui accuserait la correction serait pire qu'aucun gardien (leçon du 383).
    """
    src = open(TERMINAL, encoding='utf-8').read()
    for champ in ("'d': _today", "'a50'", "'a200'", "'net'", "'health'"):
        assert champ in src, (
            'le champ %s a disparu du point de breadth persisté : la '
            'caractérisation du lot 391 est à refaire' % champ)
