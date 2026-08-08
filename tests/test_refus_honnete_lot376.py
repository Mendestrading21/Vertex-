"""
LOT 376 — LE CONTRAT DE REFUS HONNÊTE.

Ce lot partait de l'angle mort déclaré au lot 375 : les docstrings qui décrivent
leur retour **en prose** plutôt qu'en `Retourne {…}`. La consigne était de
**mesurer le volume avant de promettre un verdict**. Voici la mesure :

```
fonctions                                  1321
avec docstring                              674
dont la docstring parle de RETOUR            51
  · forme structurée `Retourne {…}` (l.375)   6
  · EN PROSE                                 45
    dont mécaniquement vérifiables            2  → et les DEUX sont de faux positifs
```

Les deux « candidats » citaient `premium`, `model`, `iv`, `cost` — qui sont des
**paramètres d'entrée** ou des champs du board, pas des clés de retour. **11ᵉ fois
de la boucle que l'outil est le premier suspect, 4ᵉ d'affilée où mon détecteur
accuse du code sain.** Une docstring en prose ne distingue pas ce qu'elle décrit ;
la piste n'est pas décidable ainsi, et elle est close par la mesure — comme le
volet 2 du lot 375.

**Mais la lecture de ces docstrings a exhibé un contrat autrement plus utile, et
lui parfaitement décidable.** `multileg_lab.analyze_strategy` promet :

    entrée insuffisante ou invalide => {'available': False, 'reason',
                                        'refusals': [{field, value, why}]}

C'est l'**invariant produit n°4 de Vertex sous sa forme code** : donnée absente →
motif honnête, jamais un blanc. Un `available: False` sans motif est un refus
**muet** — l'interface affiche un vide que l'utilisateur ne peut pas interpréter,
et qu'il risque de lire comme « rien à signaler » plutôt que « je ne sais pas ».

Mesure : **13 refus dans le paquet, 13 motivés, 0 muet.** Vérifié aussi sur
valeurs réelles (leçon du lot 374 : la propriété se prouve sur ce que la fonction
renvoie vraiment, pas sur la forme du littéral) :

```
jambes vides   available=False  reason='jambes ou cours sous-jacent manquants.'
prime absente  available=False  reason='prime manquante sur une jambe — pas de P&L inventé.'
board vide     available=False  reason='aucun contrat pour ce titre dans le board.'
```

**Verdict : sain, rien touché.** Ce que ce gardien ajoute, c'est l'invariant :
aucun refus futur ne pourra être muet.
"""
import ast
import os

import pytest

from vertex.engines import multileg_lab

RACINE = 'vertex'

# Clés acceptées comme portant un motif de refus.
MOTIFS = ('reason', 'why', 'note', 'message', 'error', 'raison', 'motif',
          'refusals', 'issues', 'status')


def _fichiers():
    out = []
    for rac, _d, noms in os.walk(RACINE):
        for nom in sorted(noms):
            if nom.endswith('.py'):
                out.append(os.path.join(rac, nom))
    return out


def _cles_et_valeurs(d):
    return {k.value: v for k, v in zip(d.keys, d.values)
            if isinstance(k, ast.Constant) and isinstance(k.value, str)}


def _vide(v):
    if isinstance(v, ast.Constant) and v.value in ('', None):
        return True
    if isinstance(v, ast.List) and not v.elts:
        return True
    if isinstance(v, ast.Dict) and not v.keys:
        return True
    return False


def _refus():
    """[(fichier, ligne, clés, motifs non vides)] pour chaque
    `return {…'available': False…}` du paquet."""
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if not (isinstance(n, ast.Return) and isinstance(n.value, ast.Dict)):
                continue
            kv = _cles_et_valeurs(n.value)
            av = kv.get('available')
            if not (isinstance(av, ast.Constant) and av.value is False):
                continue
            utiles = [m for m in MOTIFS if m in kv and not _vide(kv[m])]
            out.append((chemin, n.lineno, sorted(kv), utiles))
    return out


# ── 1. Périmètre et anti-vide ───────────────────────────────────────────────

def test_le_perimetre_couvre_les_moteurs():
    """Leçon du lot 373 : un balayage qui rate un dossier ment en silence."""
    f = _fichiers()
    assert any(x.endswith('engines/multileg_lab.py') for x in f), 'périmètre KO'
    assert len(f) >= 100, 'seulement %d fichiers balayés' % len(f)


def test_le_detecteur_trouve_bien_des_refus():
    """Sans dénominateur, un « 0 muet » ne prouverait rien (leçon du lot 375,
    où 359 mots « tous trouvés » ne prouvaient rien du tout)."""
    r = _refus()
    assert len(r) >= 8, (
        'seulement %d refus `available: False` trouvés — le détecteur est '
        'cassé, le test suivant passerait à vide' % len(r))


# ── 2. LA propriété : aucun refus n'est muet ────────────────────────────────

def test_aucun_refus_n_est_muet():
    muets = [(c, l, cles) for c, l, cles, utiles in _refus() if not utiles]
    assert not muets, (
        'refus sans motif — l\'interface afficherait un blanc que l\'utilisateur '
        'lirait comme « rien à signaler » au lieu de « je ne sais pas » : %s'
        % ' | '.join('%s L%d (clés : %s)' % (c, l, ', '.join(k)) for c, l, k in muets))


# ── 3. La propriété sur les VALEURS RÉELLES (leçon du lot 374) ──────────────

@pytest.mark.parametrize('nom,appel', [
    ('jambes vides', lambda: multileg_lab.analyze_strategy([], 100.0, 0.4, 30)),
    ('cours nul', lambda: multileg_lab.analyze_strategy(
        [{'type': 'call', 'qty': 1, 'strike': 100, 'premium': 2.0}], 0, 0.4, 30)),
    ('prime absente', lambda: multileg_lab.analyze_strategy(
        [{'type': 'call', 'qty': 1, 'strike': 100}], 100.0, 0.4, 30)),
    ('board vide', lambda: multileg_lab.strategies_for_symbol([], 'AAPL', 100.0)),
])
def test_un_refus_reel_porte_un_motif_lisible(nom, appel):
    r = appel()
    assert isinstance(r, dict), '%s : retour non-dict' % nom
    assert r.get('available') is False, '%s : la fonction n\'a pas refusé' % nom
    motif = r.get('reason')
    assert isinstance(motif, str) and len(motif.strip()) >= 12, (
        '%s : motif absent ou trop court (%r) — refus muet à l\'exécution'
        % (nom, motif))
    assert not motif.strip().isdigit(), '%s : motif purement numérique' % nom


def test_le_contrat_de_refus_reste_annonce_dans_la_docstring():
    """Anti-dérive : si la docstring cesse d'annoncer le contrat, on veut le
    savoir ici — c'est elle qui fait de ce comportement une promesse."""
    doc = multileg_lab.analyze_strategy.__doc__ or ''
    assert "'available': False" in doc and 'reason' in doc, (
        'analyze_strategy n\'annonce plus son contrat de refus honnête')


# ── 4. Le gardien n'est pas trop strict ─────────────────────────────────────

def test_un_refus_peut_motiver_autrement_que_par_reason():
    """`refusals`, `issues`, `note`… sont des motifs légitimes. Si plus aucun
    refus n'utilise autre chose que `reason`, cette tolérance est sans objet et
    doit être resserrée plutôt que gardée à vide."""
    autres = [(c, l) for c, l, _k, utiles in _refus()
              if utiles and set(utiles) - {'reason'}]
    assert autres, (
        'plus aucun refus ne motive autrement que par `reason` : resserrer '
        'MOTIFS ou retirer cette tolérance')
