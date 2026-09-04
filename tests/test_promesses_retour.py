"""
LOT 375 — LES DOCSTRINGS DE FONCTIONS QUI PROMETTENT UNE FORME DE RETOUR.

Le gardien du lot 366 ne couvrait que les identifiants CAPS_SNAKE des docstrings
de **modules** de moteurs. Ici on descend aux **fonctions**, sur la promesse la
plus objectivement vérifiable qui soit : `Retourne {a, b, c}`.

**Verdict : sain, prouvé.** Six fonctions portent une telle promesse ; sur
**toutes** leurs branches `return {littéral}`, **aucune clé annoncée ne manque**.

Deux mesures étaient nécessaires, car un appel unique ne couvre qu'une branche :
on collecte donc les clés de **chaque** `return {…}` de la fonction. C'est plus
fort qu'un test d'exécution, qui n'aurait prouvé qu'un chemin.

Ce que le gardien n'exige PAS, délibérément : l'égalité exacte. `assess` renvoie
`spread_pct` en plus sur son chemin normal (mais pas sur sa sortie anticipée),
et `add` renvoie `entry` quand le signal est accepté. Ce sont des
**enrichissements optionnels**, pas des promesses fausses : rien de ce qui est
annoncé ne manque. Exiger l'égalité rendrait le gardien intenable dès qu'une
branche d'erreur renvoie le socle minimal — et un gardien qui crie au loup finit
désactivé (leçon du lot 374).

Note de méthode : ma première passe utilisait `ast.walk`, qui **descend dans les
fonctions imbriquées**. Le `return` de `pack()` — le constructeur de suggestions,
13 clés — était comparé à la promesse de `options_for_position`, qui en annonce
4 : une « violation » de 3 clés manquantes, entièrement imaginaire. Corrigé en
n'explorant que les nœuds appartenant à la fonction auditée. **10ᵉ fois** de la
boucle qu'un doute sur l'outil change le résultat, et **troisième d'affilée** où
c'est mon détecteur qui accusait du code sain.

Divergence réelle mais mineure, observée et NON corrigée : la docstring de
`options_for_position` énumère 12 clés de suggestion, `pack()` en renvoie 13
(`delta` non déclaré). Sous-déclaration, pas promesse fausse — même famille que
les deux ci-dessus. Vérifier les formes IMBRIQUÉES demanderait un analyseur d'un
autre ordre ; c'est déclaré ici plutôt que tu.

**Ce que ce lot NE peut PAS trancher** : les promesses en un seul mot majuscule
(`BALANCED`, `EXTREME`). Mesuré : 359 mots majuscules distincts cités dans des
docstrings de fonctions, tous « trouvés » dans le paquet — mais l'échantillon
(`ACHETER`, `ATTENDRE`, `ATTAQUE`, `ARBITRAIRE`) montre que le filet attrape
surtout des mots français mis en majuscules pour l'emphase. Sans underscore, rien
ne distingue un identifiant d'une emphase : la question n'est pas décidable ainsi,
et un « 0 problème » y serait un faux vert. Piste close par la mesure.
"""
import ast
import os

import pytest

RACINE = 'vertex'


def _fichiers():
    out = []
    for rac, _d, noms in os.walk(RACINE):
        for nom in sorted(noms):
            if nom.endswith('.py'):
                out.append(os.path.join(rac, nom).replace(os.sep, '/'))
    return out


def _promesses(doc):
    """Clés de premier niveau annoncées par `Retourne {...}`."""
    import re
    m = re.search(r'Retourne\s*\{(.*)', doc or '', re.S)
    if not m:
        return set()
    out, prof, courant = set(), 0, ''
    for ch in m.group(1):
        if ch in '{[':
            prof += 1
        elif ch in '}]':
            if prof == 0:
                break
            prof -= 1
        elif prof == 0 and ch == ',':
            out.add(courant); courant = ''; continue
        elif prof == 0 and ch == ':':
            out.add(courant); courant = None; continue
        if prof == 0 and courant is not None:
            courant += ch
    if courant:
        out.add(courant)
    return {re.sub(r'[^a-z_]', '', c.strip().strip('\'"')) for c in out
            if c and re.sub(r'[^a-z_]', '', c.strip().strip('\'"'))}


def _retours_propres(fn):
    """Clés de chaque `return {littéral}` de `fn` — SANS descendre dans les
    fonctions imbriquées (l'erreur de ma première passe : le `return` de
    `pack()` était attribué à `options_for_position`)."""
    out, pile = [], list(fn.body)
    while pile:
        n = pile.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                          ast.ClassDef)):
            continue
        if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict):
            cles = {k.value for k in n.value.keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)}
            if cles:
                out.append((n.lineno, cles))
        pile.extend(ast.iter_child_nodes(n))
    return out


def _fonctions_avec_promesse():
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for fn in [n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)]:
            prom = _promesses(ast.get_docstring(fn) or '')
            if prom:
                out.append((chemin, fn, prom))
    return out


# ── 1. Anti-vide et périmètre ───────────────────────────────────────────────

def test_le_perimetre_couvre_bien_les_moteurs():
    """Leçon du lot 373 : un balayage qui rate un dossier ment en silence."""
    fichiers = _fichiers()
    assert any(f.endswith('engines/recommendation.py') for f in fichiers), (
        'périmètre incomplet : les moteurs ne sont pas balayés')
    assert len(fichiers) >= 100, 'seulement %d fichiers balayés' % len(fichiers)


def test_le_detecteur_trouve_bien_des_promesses():
    trouvees = _fonctions_avec_promesse()
    assert len(trouvees) >= 3, (
        'seulement %d promesse(s) `Retourne {...}` trouvée(s) — le détecteur '
        'est cassé, le test suivant passerait à vide' % len(trouvees))


def test_chaque_promesse_a_bien_des_branches_a_verifier():
    """Sans branche `return {littéral}`, la vérification serait creuse."""
    sans = [(c, fn.name) for c, fn, _p in _fonctions_avec_promesse()
            if not _retours_propres(fn)]
    # `select_calls` construit son dict puis renvoie la variable : légitime.
    assert len(sans) <= 2, (
        'trop de promesses invérifiables statiquement : %s' % sans)


# ── 2. LA propriété : aucune clé annoncée ne manque ─────────────────────────

def test_aucune_promesse_de_forme_de_retour_n_est_trahie():
    fautes = []
    for chemin, fn, prom in _fonctions_avec_promesse():
        for lig, cles in _retours_propres(fn):
            manque = prom - cles
            if manque:
                fautes.append('%s::%s L%d manque %s'
                              % (chemin, fn.name, lig, ', '.join(sorted(manque))))
    assert not fautes, (
        'docstring qui annonce une clé que la fonction ne renvoie pas : %s'
        % ' | '.join(fautes))


def test_le_gardien_tolere_les_cles_supplementaires():
    """Gardien PAS TROP STRICT (leçon du lot 374). Deux fonctions enrichissent
    leur chemin normal — `spread_pct`, `entry` — sans que la promesse soit
    fausse. Si ce test échoue, c'est que ces enrichissements ont disparu et que
    la tolérance n'a plus d'objet : la revoir plutôt que de la garder à vide."""
    extras = 0
    for _c, fn, prom in _fonctions_avec_promesse():
        for _lig, cles in _retours_propres(fn):
            if cles - prom:
                extras += 1
    assert extras >= 1, (
        'plus aucune clé supplémentaire : la tolérance de ce gardien est '
        'devenue sans objet, la retirer ou resserrer le contrat')


# ── 3. Le détecteur ne doit pas ré-attribuer les `return` imbriqués ─────────

def test_les_returns_imbriques_ne_sont_pas_attribues_a_la_fonction_parente():
    """La faute exacte de ma première passe, verrouillée : `ast.walk` descendait
    dans `pack()` et attribuait ses 13 clés à `options_for_position`."""
    src = ast.parse(open('vertex/engines/recommendation.py', encoding='utf-8').read())
    cible = next((n for n in ast.walk(src) if isinstance(n, ast.FunctionDef)
                  and n.name == 'options_for_position'), None)
    assert cible is not None, 'options_for_position introuvable — gardien à revoir'
    imbriquees = [n.name for n in ast.walk(cible)
                  if isinstance(n, ast.FunctionDef) and n is not cible]
    assert imbriquees, (
        'plus aucune fonction imbriquée : ce gardien ne teste plus rien, '
        'le choisir ailleurs ou le retirer')
    for _lig, cles in _retours_propres(cible):
        assert len(cles) <= 6, (
            'un `return` de %d clés est attribué à options_for_position — le '
            'détecteur redescend dans les fonctions imbriquées %s'
            % (len(cles), imbriquees))


# ── 4. Les contrats survivants, nommément ──────────────────────────────────────────

@pytest.mark.parametrize('chemin,nom,attendues', [
    ('vertex/engines/recommendation.py', 'position_decision',
     {'verdict', 'label', 'tone', 'cls', 'reason', 'risk', 'action', 'confidence'}),
    ('vertex/data_sources/tradingview_signal_store.py', 'add',
     {'accepted', 'reason'}),
])
def test_le_contrat_annonce_est_bien_celui_qu_on_croit(chemin, nom, attendues):
    """Anti-dérive : si une docstring est réécrite, on veut le savoir ici plutôt
    que de voir le test générique continuer à passer sur une promesse amoindrie."""
    arbre = ast.parse(open(chemin, encoding='utf-8').read())
    fn = next((n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)
               and n.name == nom), None)
    assert fn is not None, '%s::%s introuvable' % (chemin, nom)
    assert _promesses(ast.get_docstring(fn) or '') == attendues, (
        '%s::%s : la promesse de docstring a changé' % (chemin, nom))
