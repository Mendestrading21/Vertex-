"""LOT 606 — LES CINQ PUCES DE FRAÎCHEUR GARDENT L'IGNORANCE (dossier 582 fermé).

Le serveur efface **délibérément** l'âge qu'il ne peut pas garantir :

    # vertex/engines/session_snapshot.py
    'age_s': (round(time.time() - ts) if isinstance(ts, (int, float)) … else None)

    # vertex/app/routes/session_api.py
    # HONNÊTETÉ : l'âge figé au build sous-estimerait la vraie ancienneté […]
    restored['age_s'] = None

Côté client, `VX.freshness.assess` rend le tiret honnête **si et seulement si**
`ageMs` arrive à `null` :

    const a = o.ageMs;
    if (a == null) return { state: 'unknown', label: '—', tone: 'muted' };

Un **repli** `(x || 0)` détruit cette entrée : `null || 0` vaut `0`, pas `null`.
`/system` était le seul des cinq sites à employer un repli plutôt qu'une garde
de type — mesuré au lot 582, corrigé au lot 606.

Ce gardien interdit le retour du repli **sur les cinq sites servis**, et non sur
le seul qui était fautif : la règle vaut pour la famille, pas pour le cas.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Les modules de page qui affichent une puce de fraîcheur.
_PAGES = [
    'vertex/ui/pages/analysis_page.py',
    'vertex/ui/pages/opportunities_page.py',
    'vertex/ui/pages/portfolio_page.py',
    'vertex/ui/pages/markets_page.py',
    'vertex/ui/pages/system_page.py',
]

# `ageMs:` suivi, quelque part avant la virgule/accolade, d'un repli `|| 0`.
_REPLI = re.compile(r"ageMs\s*:\s*[^,}\n]*\|\|\s*0")


def _lire(rel):
    return io.open(os.path.join(_ROOT, rel), encoding='utf-8').read()


def test_aucun_repli_zero_sur_un_age_dans_les_pages_servies():
    fautifs = []
    for rel in _PAGES:
        for m in _REPLI.finditer(_lire(rel)):
            fautifs.append('%s : %s' % (rel, m.group(0)))
    assert not fautifs, (
        "Un `|| 0` sur un âge rend la branche honnête `—` INATTEIGNABLE : "
        "le serveur envoie `null` quand il ignore l'âge, et `null || 0` vaut 0, "
        "donc « Analyse » — l'inverse exact du tiret.\n"
        "Employer la garde de type : `(typeof x === 'number') ? x*1000 : null`.\n"
        + '\n'.join(fautifs))


def test_les_cinq_sites_appellent_bien_assess():
    """Garde-fou de volume (591-C) : si les appels disparaissent, le test
    ci-dessus passerait en ne vérifiant plus rien."""
    n = sum(1 for rel in _PAGES if 'VX.freshness.assess(' in _lire(rel))
    assert n == 5, 'attendu 5 pages affichant une puce de fraîcheur, mesuré %d' % n


def test_system_emploie_desormais_la_garde_de_type():
    src = _lire('vertex/ui/pages/system_page.py')
    assert "typeof man.age_s==='number'" in src, (
        "/system doit garder l'ignorance comme les quatre autres sites")


def test_assess_rend_bien_le_tiret_sur_un_age_nul():
    """L'autre bout de la chaîne : si `assess` cessait de traiter `null`, la
    garde de type ne servirait plus à rien."""
    core = _lire('vertex/static/vertex/js/vx-core.js')
    i = core.index('assess(o) {')
    corps = core[i:i + 700]
    assert re.search(r"a\s*==\s*null[^\n]*state:\s*'unknown'", corps), (
        "`assess` doit rendre l'état `unknown` (libellé « — ») pour un âge nul")


def test_le_serveur_efface_bien_l_age_qu_il_ne_garantit_pas():
    """Le troisième bout : si le serveur se mettait à renvoyer 0 au lieu de
    None, la garde de type ne verrait jamais l'ignorance."""
    snap = _lire('vertex/engines/session_snapshot.py')
    assert re.search(r"'age_s':\s*\(round\(time\.time\(\) - ts\)", snap)
    assert 'else None' in snap, (
        "session_snapshot doit rendre None — jamais 0 — quand l'âge est inconnu")
