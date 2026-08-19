"""vertex/app/factory.py — REGISTRE DE ROUTES CANONIQUE (#779, gate G1).

`RELEASE_GATES.md` G1 : *« PASS lorsque factory Flask, routes, lifecycle/workers
et scheduler ont un propriétaire modulaire, avec parité et sans double
démarrage. »*

Ce module prend la deuxième de ces quatre responsabilités : **le registre de
routes**. Avant lui, 22 `app.register_blueprint(...)` étaient dispersés dans
`terminal.py` entre les lignes 147 et 2456, mêlés aux définitions de vues et aux
fonctions utilitaires. Personne ne pouvait répondre à « quelles routes
l'application sert-elle ? » sans lire 2 300 lignes.

## Deux familles, et une seule peut déménager aujourd'hui

Mesuré, pas supposé :

- **15 blueprints sans injection** — un objet `bp` de module, rien d'autre. Leur
  enregistrement est une donnée, pas du code : il devient la liste déclarative
  `BLUEPRINTS`.
- **7 blueprints à injection** — `make_blueprint(...)` nourri par l'état local du
  monolithe (`scan_state`, `_opt_job`, `_on_tv_signal`, `VERTEX_CODE`…). Ils
  restent dans `terminal.py` **tant que cet état y vit**. Les déplacer ici
  n'aurait rien découplé : le registre importerait alors le monolithe, ce qui
  inverse la dépendance sans la réduire.

## L'ordre d'enregistrement est-il neutre ?

Question qu'il fallait poser avant de regrouper. Flask résout les règles par leur
chemin, pas par leur ordre — sauf si deux blueprints déclarent la **même** règle,
auquel cas le premier gagne. Le filet de parité compare l'**ensemble complet des
193 règles** avant/après : un échange silencieux tomberait.

Un cas mérite d'être nommé : `_auth` installe un `before_request`. Il appartient
à la famille à injection et **reste enregistré tôt** dans `terminal.py`, exactement
où il était. Le regroupement ne le déplace pas.

## Ce que ce module ne fait pas

Il ne crée pas l'application. `Flask(__name__)` reste dans `terminal.py` avec les
hooks de latence qui l'accompagnent : les extraire demanderait de déplacer aussi
la configuration et l'observabilité, et `MIGRATION_PLAN.md` interdit le big bang.
G1 n'est donc **pas** franchi par ce fichier — il y contribue.
"""
from __future__ import annotations

from typing import Any, List, Tuple

#: LE REGISTRE DÉCLARATIF. Chaque entrée est `(module, attribut)` : le module est
#: importé à l'enregistrement, jamais au chargement de ce fichier — un registre
#: qui importerait 15 modules à l'import ferait payer son coût même aux tests qui
#: ne servent aucune route.
#:
#: L'ordre reproduit celui qu'avait `terminal.py`, pour que la parité soit
#: comparable ligne à ligne si quelqu'un doute.
BLUEPRINTS: Tuple[Tuple[str, str], ...] = (
    ('vertex.app.routes.feeds', 'bp'),
    ('vertex.app.routes.company_api', 'bp'),
    ('vertex.app.routes.analysis_api', 'bp'),
    ('vertex.app.routes.command', 'bp'),
    ('vertex.app.routes.session_api', 'bp'),
    ('vertex.app.routes.options_lab_api', 'bp'),
    ('vertex.app.routes.options_intel_api', 'bp'),
    ('vertex.app.routes.tracking_api', 'bp'),
    ('vertex.app.routes.opportunities_api', 'bp'),
    ('vertex.app.routes.planning_api', 'bp'),
    ('vertex.app.routes.ai_api', 'bp'),
    ('vertex.app.routes.live_api', 'bp'),
    ('vertex.app.routes.system', 'bp'),
    ('vertex.app.routes.live_events', 'bp'),
    ('vertex.app.routes.content', 'bp'),
)

#: Les blueprints qui restent chez le monolithe, et POURQUOI. Cette liste n'est
#: pas décorative : `tests/test_vertex_1_0_factory_parity.py` vérifie qu'elle
#: correspond à ce que `terminal.py` enregistre encore. Une entrée qui disparaît
#: sans que le blueprint bouge ferait mentir la doc ; une entrée qui reste alors
#: que le blueprint a migré laisserait croire à un couplage résolu.
A_INJECTION = {
    'auth': 'code d\'accès (VERTEX_CODE) + before_request de garde, posé tôt',
    'desk': 'job options `_opt_job` et drapeau IBKR, tous deux locaux au monolithe',
    'tv_webhooks': 'callback `_on_tv_signal` défini dans le monolithe',
    'strategy_os_api': '`scan_state` passé en argument à la fabrique',
    'redesign': '`scan_state` passé en argument à la fabrique',
    'positions_api': 'accès à l\'inventaire de positions tenu par le monolithe',
    'decision_api': '`scan_state` plus le mode démonstration résolu au démarrage',
}


def register_blueprints(app: Any) -> List[str]:
    """Enregistre les blueprints sans injection. Rend les noms enregistrés.

    Le retour n'est pas cosmétique : il permet à l'appelant — et au test de
    parité — de constater *ce qui a réellement été branché*, plutôt que de
    supposer que la liste et la réalité coïncident."""
    from importlib import import_module

    enregistres: List[str] = []
    for chemin, attribut in BLUEPRINTS:
        module = import_module(chemin)
        bp = getattr(module, attribut)
        app.register_blueprint(bp)
        enregistres.append(bp.name)
    return enregistres


__all__ = ['BLUEPRINTS', 'A_INJECTION', 'register_blueprints']
