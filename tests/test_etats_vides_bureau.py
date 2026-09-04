"""LOT 608 — UN ÉTAT VIDE QUI VIENT DU BUREAU SAIT LE DIRE ; LES AUTRES SE TAISENT.

Le 607 a posé `VX.store.desk_sync` et affiche un **toast** — transitoire, global.
Ce lot met la mention **dans la zone** où l'utilisateur forme sa conviction :
« Aucune position déclarée » restait écrit tel quel alors que la lecture du
bureau avait échoué et que le serveur avait peut-être les positions.

**Le danger était de corriger trop large.** Sur les états vides du produit, la
grande majorité vient d'un **moteur serveur** et n'a rien à voir avec le bureau
(« Secteurs non calculés par le dernier scan », « Registre de jobs vide »…). Y
coller « bureau non synchronisé » serait un mensonge d'un autre genre — la faute
corrigée depuis le 602, commise à l'envers.

D'où deux états distincts, et ce gardien qui tient **les deux moitiés** :
  · `VX.states.emptyDesk` existe, consulte `desk_sync`, et n'ajoute rien quand la
    synchro va bien ;
  · les zones qui lisent le bureau l'emploient ; celles qui lisent un moteur
    gardent `VX.states.empty`.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CORE = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'vx-core.js')

# Zones dont le vide vient du BUREAU (localStorage synchronisé) — lues une par
# une au lot 608. La clé est un fragment du message, stable et parlant.
_ZONES_BUREAU = [
    ('vertex/ui/pages/briefing.py',         'Aucune alerte active.'),
    ('vertex/ui/pages/briefing.py',         'Aucune position déclarée.'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucune position déclarée — le portefeuille'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucune position urgente'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucune position déclarée.'),
    ('vertex/ui/pages/portfolio_page.py',   'Watchlist vide'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucun suivi actif'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucune position option'),
    ('vertex/ui/pages/portfolio_page.py',   'Aucune position déclarée — le risque'),
    ('vertex/ui/pages/analysis_page.py',    'Aucune thèse enregistrée sur ce titre.'),
    ('vertex/ui/pages/analysis_page.py',    'Aucune entrée de journal sur ce titre.'),
    ('vertex/ui/pages/performance_page.py', 'Aucune hypothèse journalisée'),
    ('vertex/ui/pages/performance_page.py', 'Aucune erreur déclarée'),
    ('vertex/ui/pages/performance_page.py', 'Aucune leçon consignée'),
    ('vertex/ui/pages/performance_page.py', 'Aucune erreur récurrente déclarée'),
    ('vertex/ui/pages/performance_page.py', 'Aucun état émotionnel déclaré'),
    ('vertex/ui/pages/performance_page.py', 'Aucun trade réel déclaré avec résultat'),
]

# Zones dont le vide vient d'un MOTEUR — la mention y serait un mensonge.
_ZONES_MOTEUR = [
    ('vertex/ui/pages/markets_page.py',     'Secteurs non calculés par le dernier scan.'),
    ('vertex/ui/pages/markets_page.py',     'VIX non fourni par le dernier scan.'),
    ('vertex/ui/pages/system_page.py',      'Registre de jobs vide.'),
    ('vertex/ui/pages/system_page.py',      'Liste des moteurs indisponible.'),
    ('vertex/ui/pages/performance_page.py', 'il en faut 5 par verdict pour publier une fiabilité'),
    ('vertex/ui/pages/analysis_page.py',    'Série de prix indisponible pour ce titre.'),
    ('vertex/ui/pages/opportunities_page.py', 'Aucun titre scoré dans le scan courant'),
]


def _lire(rel):
    return io.open(os.path.join(_ROOT, rel), encoding='utf-8').read()


def _appel_avant(src, fragment):
    """Le nom de l'état (`empty` / `emptyDesk`) qui précède ce fragment.

    VERTEX 2.0 — deux mécanismes coexistent, et ce gardien tient les deux.
    Les zones historiques passent par `VX.states.empty*`. Les zones refondues
    écrivent directement un bloc `vx2-state` avec son `data-kind`, parce
    qu'elles portent en plus une CAUSE et une action sûre, que `VX.states.empty`
    ne sait pas rendre.

    Ce qui est gardé est inchangé : une zone alimentée par un MOTEUR ne doit
    jamais imputer son vide au bureau. `data-kind="empty"` vaut donc `empty`,
    et un bloc 2.0 qui parlerait de synchro du bureau ressortirait comme tel.
    """
    i = src.index(fragment)
    amont = src[max(0, i - 700):i]
    m = None
    for m in re.finditer(r'VX\.states\.(emptyDesk|empty)\(', amont):
        pass
    if m is not None:
        return m.group(1)
    m2 = None
    for m2 in re.finditer(r'data-kind="(empty|missing|error|stale|partial)"', amont):
        pass
    assert m2 is not None, (
        'ni VX.states.empty*, ni bloc vx2-state en amont de : ' + fragment[:40])
    #  Un bloc 2.0 qui mentionnerait le bureau serait la faute que ce banc
    #  surveille : on la fait ressortir sous le nom attendu.
    if 'bureau' in amont.lower() or 'synchronis' in amont.lower():
        return 'emptyDesk'
    return 'empty' 


# ── 1. L'état existe et se tait quand tout va bien ──────────────────────────

def test_l_etat_bureau_existe():
    assert 'emptyDesk(reason, action, opts)' in _lire(
        'vertex/static/vertex/js/vx-core.js')


def test_il_ne_dit_rien_quand_la_synchro_va_bien():
    """Sans cette porte, la mention s'afficherait en permanence — et un
    avertissement permanent ne veut plus rien dire."""
    src = _lire('vertex/static/vertex/js/vx-core.js')
    i = src.index('emptyDesk(reason, action, opts)')
    corps = src[i:i + 1400]
    assert re.search(r"if\s*\(\s*!\s*sync\s*\|\|\s*sync\s*===\s*'ok'\s*\)\s*return\s+base", corps), (
        "emptyDesk doit rendre l'état vide NU quand `desk_sync` vaut 'ok' ou "
        "n'est pas encore connu")


def test_il_lit_l_etat_pose_par_le_lot_607():
    src = _lire('vertex/static/vertex/js/vx-core.js')
    i = src.index('emptyDesk(reason, action, opts)')
    assert "get('desk_sync')" in src[i:i + 1400], (
        "emptyDesk doit lire `desk_sync` — l'état posé par le lot 607")


# ── 2. Les deux familles sont du bon côté ───────────────────────────────────

def test_les_zones_du_bureau_disent_la_desynchro():
    manquants = []
    for rel, frag in _ZONES_BUREAU:
        if _appel_avant(_lire(rel), frag) != 'emptyDesk':
            manquants.append('%s : %s' % (rel.split('/')[-1], frag))
    assert not manquants, (
        "Ces zones lisent le BUREAU : leur vide peut venir d'une synchro ratée, "
        "elles doivent employer `VX.states.emptyDesk`.\n" + '\n'.join(manquants))


def test_les_zones_du_moteur_ne_mentent_pas():
    fautifs = []
    for rel, frag in _ZONES_MOTEUR:
        if _appel_avant(_lire(rel), frag) != 'empty':
            fautifs.append('%s : %s' % (rel.split('/')[-1], frag))
    assert not fautifs, (
        "Ces zones lisent un MOTEUR SERVEUR : leur vide n'a rien à voir avec le "
        "bureau. Y afficher « bureau non synchronisé » serait un mensonge d'un "
        "autre genre.\n" + '\n'.join(fautifs))


# ── 3. Garde-fou de volume (591-C) ──────────────────────────────────────────

def test_les_deux_familles_restent_peuplees():
    """Si l'une des deux listes se vidait, les tests ci-dessus passeraient en ne
    vérifiant plus rien."""
    assert len(_ZONES_BUREAU) >= 15, 'la famille BUREAU a maigri'
    assert len(_ZONES_MOTEUR) >= 5, 'la famille MOTEUR a maigri'
    n = sum(_lire(r).count('VX.states.emptyDesk(')
            for r in sorted({rel for rel, _ in _ZONES_BUREAU}))
    assert n >= 15, 'attendu ≥15 appels à emptyDesk dans les pages, mesuré %d' % n
