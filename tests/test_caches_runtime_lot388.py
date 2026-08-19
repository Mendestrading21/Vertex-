"""
LOT 388 — LA SUITE ÉCRIVAIT UN POINT FABRIQUÉ PAR JOUR DANS L'HISTORIQUE GEX RÉEL.

Le lot 387 avait traité `desk_data.json`. Il n'avait regardé que celui-là. Ce lot
mesure **les vingt fichiers runtime** du dépôt, avant et après la suite complète.

## Mesure

```text
7 fichiers sur 20 touchés par la suite :
  ai_enrichment.json          horodatage seul (`as_of`)
  session_digest_cache.json   horodatage seul (`age_s`)
  weekly_snapshot.json        horodatage seul (`generated_at`)
  desk_data.json              connu (lot 387), `data` byte-identique
  desk_backup_20260809.json   CRÉÉ — la suite consomme le créneau du jour
  skyler_sessions.json        un point/jour sur les tickers SYNTHÉTIQUES SKYX/TSTQ
  gex_history_cache.json      un point/jour sur MSFT — un VRAI titre
```

La création de `desk_backup_<jour>.json` **confirme par la mesure** ce que le lot
387 n'avait qu'annoncé : lancer la suite consomme le snapshot quotidien du desk.

## La trouvaille

`test_options_gex_route_real_numbers` sème un board d'options **fabriqué**
(MSFT, strikes 460/420, gamma 0.05/0.03, spot 440) puis appelle
`/api/options/gex/MSFT`. La route **journalise le profil** via
`gex_history.record()` — dans le vrai `gex_history_cache.json`, la fixture
`client` ne redirigeant rien.

Résultat mesuré : l'historique GEX de MSFT portait **8 points strictement
identiques** (`net_gex` 36 784 000, `spot` 440.0, `zero_gamma` 429.6), un par
exécution de la suite. Les autres symboles du fichier — ACN, ADBE — portent des
valeurs variées et n'ont pas bougé.

```text
MSFT   avant 7 pts 2026-08-02..08  → après 8 pts   (ajouté : 2026-08-09)
ACN    avant 2 pts                 → après 2 pts   (—)
ADBE   avant 2 pts                 → après 2 pts   (—)
```

**Ce fichier est servi** : `vertex/app/routes/options_intel_api.py` le lit pour
`/api/options/gex-radar`. Des chiffres fabriqués par un test étaient donc rendus
à l'utilisateur comme un historique mesuré, sur un titre qu'il détient
réellement — invariant n°4, cette fois sur un VRAI symbole et non un ticker de
test.

Corrigé côté test (redirection `_BASE_DIR` vers un dossier temporaire, le
mécanisme déjà employé par `test_desk_routes.py`) : **aucune production
touchée**.

## Ce que ce lot ne corrige pas, et pourquoi

`skyler_sessions.json` accumule aussi un point par jour, mais sur **SKYX** et
**TSTQ** — des tickers synthétiques utilisés par 8 fichiers de test, non
confondables avec un titre réel, et bornés (`MAX_SESSIONS = 400`). Le dégât n'est
pas de même nature : rien de faux n'est attribué à un vrai symbole. Corriger 8
fichiers dépasse la piste calibrée de ce lot ; c'est versé aux dossiers.
"""
import ast
import os

import pytest

# Caches runtime écrits par la PRODUCTION via `persist.save_json`, recensés au
# lot 388. Un nouveau venu doit être examiné : quels tests l'atteignent, et
# redirigent-ils leur stockage ?
# Mesure : 12 sites, une fois le détecteur rendu explicite (voir `_nom_de_cache`).
#  12 -> 13 au lot #783/G2 : `desk.py::_snapshot_avant_perte` ecrit un
#  instantane `desk_avantperte_<date>-<heure>.json` au moment ou un push
#  menacerait des cles. LA QUESTION QUE POSE CE GARDIEN, POSEE : quels tests
#  l'atteignent, et redirigent-ils leur stockage ?
#    - tests/test_desk_perte_lot362.py : OUI (monkeypatch de persist.cache_path)
#    - tests/test_desk_cycle_lot84.py  : NON, il travaille exprès sur le desk
#      REEL — et la premiere execution sous le nouveau contrat a bien ecrit un
#      instantane a la racine. Son `finally` a ete corrige pour vider la cle
#      explicitement au lieu de l'omettre, ce qui supprime le declencheur.
#  Le motif est ajoute au .gitignore (donnees personnelles).
NB_CACHES_PRODUCTION = 13

# Le test qui exerce une route journalisante doit rediriger son stockage.
# Étendu au lot 389 : `/api/skyler/<sym>` journalise une séance dans
# `skyler_sessions.json`. Périmètre établi en rejouant les 8 fichiers candidats
# un par un — **2 seulement** écrivaient, les 6 autres ne faisaient que
# mentionner les tickers.
TESTS_A_REDIRIGER = {
    'tests/test_options_routes.py': ['test_options_gex_route_real_numbers'],
    'tests/test_skyler_core.py': ['test_skyler_route'],
    'tests/test_xss_exits_lot177.py': [
        'test_skyler_packet_ne_sert_jamais_le_payload_brut'],
}


def _redirections(fn):
    """{'_BASE_DIR', 'cache_path'} effectivement monkeypatchés dans `fn`."""
    out = set()
    for n in ast.walk(fn):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == 'setattr'):
            continue
        for a in n.args:
            if isinstance(a, ast.Constant) and a.value in ('_BASE_DIR', 'cache_path'):
                out.add(a.value)
    return out


def _nom_de_cache(noeud):
    """Nomme la cible d'un `save_json`, quelle que soit sa forme.

    Ma première version rendait « ? » pour tout ce qui n'était ni constante ni
    nom simple — elle masquait `_slog.SESSIONS_FILE`, précisément le fichier qui
    accumule les tickers synthétiques. Un recensement opaque ne recense rien.
    """
    if isinstance(noeud, ast.Constant):
        return str(noeud.value)
    if isinstance(noeud, ast.Name):
        return '<%s>' % noeud.id
    if isinstance(noeud, ast.Attribute):
        return '<%s>' % noeud.attr
    if isinstance(noeud, ast.BinOp):                 # 'nom_%s.json' % ...
        return _nom_de_cache(noeud.left) + ' %…'
    return '<expression>'


def _fonction(chemin, nom):
    arbre = ast.parse(open(chemin, encoding='utf-8').read())
    for n in ast.walk(arbre):
        if isinstance(n, ast.FunctionDef) and n.name == nom:
            return n
    return None


# ── 1. Anti-vide : la route journalise-t-elle encore ? ──────────────────────

def test_la_route_gex_journalise_toujours():
    """Sans cet ancrage, le test suivant passerait pour la MAUVAISE raison : si
    la route cessait d'écrire l'historique, exiger une redirection ne
    protégerait plus rien et personne ne le saurait."""
    src = open('vertex/app/routes/options_intel_api.py', encoding='utf-8').read()
    assert 'gex_history' in src, (
        '/api/options/* ne journalise plus l\'historique GEX — la redirection '
        'exigée au lot 388 n\'a plus d\'objet : revérifier ce que les tests '
        'écrivent réellement avant de retirer ce gardien')


def test_la_route_skyler_journalise_toujours_une_seance():
    """Anti-vide jumeau, ajouté au lot 389 : si les routes cessaient de
    journaliser une séance, exiger une redirection dans les deux tests
    concernés ne protégerait plus rien.

    Première version : `'SESSIONS_FILE' in src`. **Creuse** — la preuve ROUGE
    l'a démasquée : la chaîne apparaît **6 fois** dans le fichier alors qu'il
    n'y a que **2 sites d'écriture**, donc en retirer un laissait le test vert.
    C'est mot pour mot la faute que le lot 386 avait déjà corrigée ailleurs.
    On compte désormais les sites par AST.
    """
    arbre = ast.parse(open('vertex/app/routes/analysis_api.py', encoding='utf-8').read())
    sites = [n for n in ast.walk(arbre)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == 'save_json' and n.args
             and isinstance(n.args[0], ast.Attribute)
             and n.args[0].attr == 'SESSIONS_FILE']
    assert len(sites) == 2, (
        '%d sites de journalisation de séance dans analysis_api, 2 mesurés au '
        'lot 389 — si la journalisation disparaît, les redirections exigées '
        'n\'ont plus d\'objet ; si elle se multiplie, vérifier les nouveaux '
        'chemins' % len(sites))


def test_l_historique_des_seances_garde_sa_borne():
    """`MAX_SESSIONS` borne l'accumulation par symbole. Sans elle, un ticker
    semé chaque jour par un test croîtrait sans fin."""
    arbre = ast.parse(open('vertex/engines/session_log.py', encoding='utf-8').read())
    bornes = {n.targets[0].id: n.value.value
              for n in arbre.body
              if isinstance(n, ast.Assign) and len(n.targets) == 1
              and isinstance(n.targets[0], ast.Name)
              and isinstance(n.value, ast.Constant)
              and isinstance(n.value.value, int)}
    assert bornes.get('MAX_SESSIONS') == 400, \
        'borne des séances modifiée : %s' % bornes


def test_l_historique_gex_garde_ses_bornes_anti_croissance():
    """`_MAX_SYMBOLS` évince les symboles les plus anciens : un symbole
    réinjecté en boucle par un test resterait « récent » et pourrait chasser un
    vrai symbole. Les bornes doivent rester explicites."""
    arbre = ast.parse(open('vertex/options/gex_history.py', encoding='utf-8').read())
    bornes = {n.targets[0].id: n.value.value
              for n in arbre.body
              if isinstance(n, ast.Assign) and len(n.targets) == 1
              and isinstance(n.targets[0], ast.Name)
              and isinstance(n.value, ast.Constant)
              and isinstance(n.value.value, int)}
    assert bornes.get('_MAX_DAYS') == 120, 'borne de profondeur modifiée : %s' % bornes
    assert bornes.get('_MAX_SYMBOLS') == 80, 'borne de symboles modifiée : %s' % bornes


# ── 2. LA propriété : le test journalisant redirige son stockage ────────────

@pytest.mark.parametrize('chemin,nom', [
    (c, n) for c, noms in sorted(TESTS_A_REDIRIGER.items()) for n in noms])
def test_le_test_journalisant_redirige_son_stockage(chemin, nom):
    """Sans redirection, ce test écrivait un point FABRIQUÉ par jour dans
    l'historique GEX réel — servi ensuite par `/api/options/gex-radar` comme une
    mesure. Mesuré au lot 388 : 8 points MSFT strictement identiques."""
    fn = _fonction(chemin, nom)
    assert fn is not None, '%s::%s a disparu — recensement à mettre à jour' % (chemin, nom)
    red = _redirections(fn)
    assert red, (
        '%s::%s exerce une route qui JOURNALISE dans un cache runtime, sans '
        'rediriger `persist._BASE_DIR` ni `persist.cache_path` vers un dossier '
        'temporaire : il écrit des chiffres fabriqués dans des données que '
        'l\'application sert comme réelles (invariant n°4)' % (chemin, nom))


def test_le_recensement_des_tests_journalisants_ne_se_perime_pas():
    """Une entrée qui ne correspond plus à rien doit être retirée, sinon le
    recensement couvre un cas disparu (leçon des lots 373-387)."""
    for chemin, noms in sorted(TESTS_A_REDIRIGER.items()):
        assert os.path.exists(chemin), 'fichier recensé disparu : %s' % chemin
        for nom in noms:
            assert _fonction(chemin, nom) is not None, (
                '%s::%s n\'existe plus : retirer du recensement' % (chemin, nom))


# ── 3. Le recensement des caches écrits par la production ──────────────────

def test_aucun_nouveau_cache_journalise_sans_examen():
    """Rend visible l'apparition d'un cache runtime écrit par la production.
    Chaque nouveau venu pose la même question que le GEX : quels tests
    l'atteignent, et redirigent-ils leur stockage ?"""
    trouves = set()
    for rac, _d, noms in os.walk('vertex'):
        if '__pycache__' in rac:
            continue
        for n in sorted(noms):
            if not n.endswith('.py'):
                continue
            chemin = os.path.join(rac, n)
            try:
                arbre = ast.parse(open(chemin, encoding='utf-8').read())
            except SyntaxError:
                continue
            for x in ast.walk(arbre):
                if (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                        and x.func.attr == 'save_json' and x.args):
                    trouves.add((_nom_de_cache(x.args[0]), chemin))
    assert len(trouves) == NB_CACHES_PRODUCTION, (
        '%d écritures de cache runtime par la production, %d recensées au lot '
        '388 — pour chaque nouveau venu, vérifier quels tests l\'atteignent et '
        's\'ils redirigent leur stockage : %s'
        % (len(trouves), NB_CACHES_PRODUCTION, sorted(trouves)))
