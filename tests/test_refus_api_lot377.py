"""
LOT 377 — LES AUTRES CONVENTIONS DE REFUS : le gardien du lot 376 n'en voyait
qu'un tiers.

Prolongement direct du lot 376, qui verrouillait le contrat de refus honnête sur
`return {…'available': False…}` **littéral** — 13 cas. Ce lot mesure les autres
conventions avant de conclure quoi que ce soit.

## Volume par convention (paquet `vertex`, 1321 fonctions)

```
return None                242     ← absence de valeur ordinaire, PAS un refus
return []                   28     ← « rien trouvé » sur une liste : honnête
return {}                   13
return {available: False}   13     ← seuls cas vus par le lot 376
return {ok: False}           4
```

`return None` domine largement, mais ce n'est **pas** une convention de refus :
c'est le retour normal d'un utilitaire sans valeur à donner. La question n'y est
pas décidable, et on ne prétend pas la trancher.

## Le vrai défaut trouvé : le PÉRIMÈTRE du gardien précédent

Mon premier détecteur ne regardait que `return <Dict>`. Or la majorité des refus
d'API sont **enveloppés** : `return jsonify({...})`, souvent
`return jsonify({...}), 400`. Le nœud est alors un `Call` ou un `Tuple`, jamais
un `Dict` — ils étaient **tous** invisibles.

```
refus vus par le détecteur naïf (lot 376)   : 13
refus réels, enveloppes déballées           : 39
                                              → couverture du lot 376 : 33 %
```

Les 26 manquants sont précisément les plus exposés : **les refus servis en JSON
au navigateur**, ceux que l'interface montre à l'utilisateur. **12ᵉ fois de la
boucle que le périmètre de l'outil ment**, et la première où c'est un gardien
**déjà fusionné** qui se révèle myope.

## Le résultat, une fois le périmètre corrigé

**39 refus, 39 motivés, 0 muet.** Vérifié aussi sur les réponses réellement
servies :

```
/api/copilot/ask   HTTP 200  {'ok': False}  error='question vide'
/api/desk/restore  HTTP 400  {'ok': False}  err='nom invalide'
```

Note honnête sur un cas voisin : `/api/skyler/<sym>` répond 200 sans clé d'état
pour un symbole inconnu — mais il sert une décision complète avec un
`audit_trail` qui énumère ce qui manquait (`anomaly: false, fundamentals: false`
…). C'est la forme honnête sous un autre habillage : la traçabilité **est** le
motif. Pas un refus muet.

## La discipline des contrats, mesurée

Une fonction qui renvoie un dict riche dans une branche et un `{}` ou `None` nu
dans une autre offre à l'appelant un refus muet déguisé en valeur. Mesure :
**37 fonctions mixtes existent**, et **aucune** ne porte de clé d'état dans sa
branche riche. Le dénominateur est réel, donc le zéro l'est aussi.

**Verdict : sain, rien touché.** Ce que ce lot corrige, c'est la **couverture**
du gardien — un gardien myope est plus dangereux qu'une absence de gardien,
puisqu'il rassure.
"""
import ast
import os

import pytest

import terminal

RACINE = 'vertex'
ETATS = ('ok', 'available', 'success', 'valid', 'found')
MOTIFS = ('reason', 'why', 'note', 'message', 'error', 'err', 'raison', 'motif',
          'refusals', 'issues', 'status', 'detail', 'details')


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _fichiers():
    out = []
    for rac, _d, noms in os.walk(RACINE):
        for nom in sorted(noms):
            if nom.endswith('.py'):
                out.append(os.path.join(rac, nom))
    return out


def _deballe(v):
    """`jsonify({...})`, `jsonify({...}), 400`, `({...}), 200` → le dict.

    Sans ce déballage, les refus d'API sont TOUS invisibles : c'est la myopie
    du gardien du lot 376, corrigée ici."""
    if isinstance(v, ast.Tuple) and v.elts:
        return _deballe(v.elts[0])
    if isinstance(v, ast.Call) and v.args:
        f = v.func
        if (isinstance(f, ast.Name) and f.id in ('jsonify', 'dict')) or \
           (isinstance(f, ast.Attribute) and f.attr == 'jsonify'):
            return _deballe(v.args[0])
    return v if isinstance(v, ast.Dict) else None


def _kv(d):
    return {k.value: val for k, val in zip(d.keys, d.values)
            if isinstance(k, ast.Constant) and isinstance(k.value, str)}


def _vide(v):
    if isinstance(v, ast.Constant) and v.value in ('', None):
        return True
    if isinstance(v, ast.List) and not v.elts:
        return True
    if isinstance(v, ast.Dict) and not v.keys:
        return True
    return False


def _refus(deballer=True):
    """[(fichier, ligne, état, clés, motifs non vides)]."""
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if not isinstance(n, ast.Return) or n.value is None:
                continue
            d = _deballe(n.value) if deballer else (
                n.value if isinstance(n.value, ast.Dict) else None)
            if d is None or not d.keys:
                continue
            m = _kv(d)
            for e in ETATS:
                x = m.get(e)
                if isinstance(x, ast.Constant) and x.value is False:
                    utiles = [k for k in MOTIFS if k in m and not _vide(m[k])]
                    out.append((chemin, n.lineno, e, sorted(m), utiles))
                    break
    return out


# ── 1. Périmètre et anti-vide ───────────────────────────────────────────────

def test_le_perimetre_couvre_les_routes_api():
    f = _fichiers()
    for cle in ('vertex/app/routes/desk.py', 'vertex/app/routes/analysis_api.py',
                'vertex/ai/copilot.py'):
        assert cle in f, 'périmètre incomplet : %s absent' % cle


def test_le_detecteur_trouve_bien_des_refus():
    r = _refus()
    assert len(r) >= 30, (
        'seulement %d refus trouvés — le détecteur est cassé, les tests '
        'suivants passeraient à vide' % len(r))


def test_le_deballage_voit_strictement_plus_que_le_detecteur_naif():
    """LA leçon de ce lot, verrouillée. Sans déballer `jsonify(...)`, les refus
    d'API — les plus exposés — sont invisibles. Si cet écart tombe à zéro, c'est
    que le déballage a été cassé, pas que le code a changé."""
    naif, complet = len(_refus(deballer=False)), len(_refus(deballer=True))
    assert complet > naif, (
        'le déballage ne voit plus rien de plus que le détecteur naïf '
        '(%d vs %d) — le gardien est redevenu myope' % (complet, naif))
    assert complet - naif >= 10, (
        'seulement %d refus enveloppés détectés (%d vs %d) — vérifier que '
        '`_deballe` suit encore les formes réellement employées'
        % (complet - naif, complet, naif))


# ── 2. LA propriété : aucun refus n'est muet ────────────────────────────────

def test_aucun_refus_n_est_muet():
    muets = [(c, l, e, cles) for c, l, e, cles, u in _refus() if not u]
    assert not muets, (
        'refus sans motif — l\'interface afficherait un blanc que l\'utilisateur '
        'lirait « rien à signaler » au lieu de « je ne sais pas » : %s'
        % ' | '.join('%s L%d (%s: False, clés : %s)' % (c, l, e, ', '.join(k))
                     for c, l, e, k in muets))


# ── 3. Sur les réponses RÉELLEMENT servies ──────────────────────────────────

@pytest.mark.parametrize('nom,methode,url', [
    ('copilot sans question', 'post', '/api/copilot/ask'),
    ('restore sans nom', 'post', '/api/desk/restore'),
])
def test_un_refus_servi_porte_un_motif_lisible(client, nom, methode, url):
    r = getattr(client, methode)(url, json={})
    charge = r.get_json()
    assert isinstance(charge, dict), '%s : réponse non-JSON' % nom
    assert charge.get('ok') is False, '%s : la route n\'a pas refusé' % nom
    motifs = [charge[k] for k in MOTIFS
              if isinstance(charge.get(k), str) and charge[k].strip()]
    assert motifs, '%s : refus servi SANS motif (%s)' % (nom, sorted(charge))
    assert max(len(m) for m in motifs) >= 8, (
        '%s : motif trop court pour être lisible (%r)' % (nom, motifs))


# ── 4. La discipline des contrats à deux visages ────────────────────────────

def _retours(fn):
    """(riches, nus) — sans descendre dans les portées imbriquées (lot 375)."""
    riches, nus, pile = [], [], list(fn.body)
    while pile:
        n = pile.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                          ast.ClassDef)):
            continue
        if isinstance(n, ast.Return) and n.value is not None:
            v = n.value
            if isinstance(v, ast.Dict) and v.keys:
                cles = {k.value for k in v.keys
                        if isinstance(k, ast.Constant) and isinstance(k.value, str)}
                if cles:
                    riches.append(cles)
            elif (isinstance(v, ast.Dict) and not v.keys) or \
                 (isinstance(v, ast.Constant) and v.value is None):
                nus.append(n.lineno)
        pile.extend(ast.iter_child_nodes(n))
    return riches, nus


def _mixtes():
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for fn in [n for n in ast.walk(arbre) if isinstance(n, ast.FunctionDef)]:
            riches, nus = _retours(fn)
            if riches and nus:
                out.append((chemin, fn.name, fn.lineno, riches))
    return out


def test_il_existe_bien_des_fonctions_mixtes_a_examiner():
    """Dénominateur du test suivant : sans fonctions mixtes, son « 0 » ne
    prouverait rien (leçon des lots 375 et 376)."""
    assert len(_mixtes()) >= 10, (
        'seulement %d fonction(s) mixte(s) — le test suivant serait vide'
        % len(_mixtes()))


def test_une_fonction_qui_promet_un_etat_ne_retombe_jamais_sur_un_retour_nu():
    """Un dict riche portant `available`/`ok` dans une branche, et un `{}` ou
    `None` nu dans une autre : l'appelant qui lit `r.get('reason')` reçoit
    `None` sans savoir pourquoi. Refus muet déguisé en valeur."""
    fautes = [(c, n, l) for c, n, l, riches in _mixtes()
              if any(cles & set(ETATS) for cles in riches)]
    assert not fautes, (
        'contrat à deux visages : %s — la branche nue doit porter le même état '
        'et un motif' % ' | '.join('%s::%s L%d' % f for f in fautes))


# ── 5. Le gardien n'est pas trop strict ─────────────────────────────────────

def test_plusieurs_familles_de_motifs_restent_employees():
    """`note`, `err`, `error`, `reason`… sont tous légitimes. Si une seule
    famille subsiste, cette tolérance est sans objet : la resserrer plutôt que
    la garder à vide."""
    familles = set()
    for _c, _l, _e, _cles, u in _refus():
        familles.update(u)
    assert len(familles) >= 3, (
        'seulement %s employé(s) comme motif : resserrer MOTIFS' % sorted(familles))
