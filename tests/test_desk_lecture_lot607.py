"""LOT 607 — LA LECTURE DU BUREAU DIT SON ÉCHEC (les deux chemins, pas un seul).

Le lot 604 a corrigé les trois **écritures** de la synchro du bureau. Il n'a pas
regardé la **lecture**. `vx-entities.js::pull()` faisait :

    const r = await fetch('/api/desk'); const d = await r.json();
    …
    } catch (e) {}

**`r.ok` n'était jamais lu** — c'est `604-A` sur l'autre chemin — et le `catch`
était vide.

Ce que ça coûtait, mesuré en navigateur : sur un profil **neuf** dont le GET
échoue, le bureau s'affiche **vide**, et « aucun trade déclaré » devient
**indiscernable** de « bureau non synchronisé » — alors que le serveur, lui, a
les données. C'est l'invariant produit pris à l'envers : pas une donnée absente
présentée comme réelle, mais une donnée **réelle** présentée comme **absente**.

Ce gardien tient les DEUX chemins ensemble : corriger l'un en laissant l'autre
muet est précisément la faute que ce lot répare.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'vx-entities.js')


def _lire():
    return io.open(_SRC, encoding='utf-8').read()


def _bloc(nom):
    """Le corps d'une fonction de `vx-entities.js`, lu sur disque."""
    src = _lire()
    i = src.index(nom)
    n, debut = 0, src.index('{', i)
    for j in range(debut, len(src)):
        if src[j] == '{':
            n += 1
        elif src[j] == '}':
            n -= 1
            if n == 0:
                return src[debut:j + 1]
    raise AssertionError('bloc non refermé : ' + nom)


# ── Les deux chemins lisent `r.ok` ──────────────────────────────────────────

def test_la_lecture_verifie_le_code_http():
    corps = _bloc('async function pull()')
    assert re.search(r"if\s*\(\s*!\s*r\.ok\s*\)", corps), (
        "`pull()` doit lire `r.ok` : `fetch` NE REJETTE PAS sur 4xx/5xx (604-A), "
        "donc sans cette lecture un refus du serveur est invisible.")


def test_l_ecriture_verifie_toujours_le_code_http():
    """Garde-fou : le correctif du 604 ne doit pas se perdre en corrigeant 607."""
    corps = _bloc('function pushNow()')
    assert 'r.ok' in corps, "`pushNow()` doit continuer de lire `r.ok` (lot 604)"


# ── Les deux chemins DISENT leur échec ──────────────────────────────────────

def test_la_lecture_ne_se_tait_plus_sur_echec():
    """Le `catch` visé est celui qui ferme le try ENGLOBANT — pas les `catch`
    vides des écritures localStorage internes, qui sont du « au mieux »
    légitime (une écriture qui échoue par quota ne doit pas casser la lecture).

    On l'identifie par sa PROFONDEUR, pas par sa position : une première version
    de ce test prenait « le dernier `catch` du bloc » et tombait sur le
    `catch (e2) {}` interne de `VX.store.set`. Une heuristique positionnelle sur
    du code est fragile ; la profondeur, non."""
    corps = _bloc('async function pull()')
    queue, profondeur = None, 0
    for m in re.finditer(r"[{}]|catch\s*\([^)]*\)\s*\{", corps):
        t = m.group(0)
        if t.startswith('catch'):
            if profondeur == 1:          # immédiatement dans le corps de pull()
                queue = corps[m.start():]
            profondeur += 1
        elif t == '{':
            profondeur += 1
        else:
            profondeur -= 1
    assert queue is not None, "aucun `catch` englobant trouvé dans `pull()`"
    assert not re.match(r"catch\s*\([^)]*\)\s*\{\s*\}", queue), (
        "le `catch` englobant de `pull()` ne doit plus être vide")
    assert 'syncAlerte(' in queue, (
        "`pull()` doit prévenir l'utilisateur : un bureau vide et un bureau non "
        "synchronisé ne doivent pas se ressembler")


def test_l_etat_distingue_la_lecture_de_l_ecriture():
    """Les deux échecs n'ont pas la même conséquence : l'écriture retentera
    toute seule, la lecture laisse un écran potentiellement vide. L'état doit
    permettre de les distinguer."""
    corps = _bloc('async function pull()')
    assert "'read-error'" in corps, (
        "un échec de LECTURE doit porter son propre état, distinct de l'écriture")
    assert "'ok'" in corps, "une lecture réussie doit remettre l'état à 'ok'"


def test_la_lecture_reste_en_lecture():
    """Invariant de sûreté : un correctif du chemin de lecture ne doit JAMAIS
    introduire d'écriture destructrice. `pull()` n'écrit dans localStorage que
    la branche « serveur plus récent », déjà présente avant ce lot."""
    corps = _bloc('async function pull()')
    ecritures = re.findall(r"localStorage\.setItem\(([^,]+)", corps)
    assert len(ecritures) == 2, (
        'attendu exactement 2 écritures localStorage dans `pull()` '
        '(les clés du serveur + deskTs), mesuré %d : %s' % (len(ecritures), ecritures))
    assert not re.search(r"localStorage\.(removeItem|clear)\(", corps), (
        "`pull()` ne doit jamais supprimer de donnée locale")


# ── Le message est honnête sur ce qui se passe ──────────────────────────────

def test_le_message_ne_laisse_pas_croire_que_le_bureau_est_vide():
    corps = _bloc('async function pull()')
    assert 'vient de cet appareil' in corps, (
        "le message doit dire d'où vient ce qui s'affiche")
    assert 'conclus pas' in corps or 'pas que' in corps, (
        "le message doit avertir que le vide affiché n'est pas un constat")
