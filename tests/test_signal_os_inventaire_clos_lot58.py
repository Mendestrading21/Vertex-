"""SIGNAL OS · LOT 58 — L'INVENTAIRE FERMÉ, ET TROIS VERDICTS PLUTÔT QUE TROIS CHANTIERS.

L'instrument du lot 55 laissait **30 moteurs « indéterminés »** : l'AST voyait
l'appel mais pas la clé sous laquelle le résultat ressort. Ce lot les résout par
deux sauts structurels, bornés, jamais devinés :

- la variable est passée en **argument nommé** (`build_packet(events=ev)`) → la
  clé est `events` ;
- la variable est posée dans un **littéral de dictionnaire** (`{'paths': paths}`)
  → la clé est `paths` ;
- et, quand l'appel n'est affecté à **rien**, la même règle s'applique au nœud
  d'appel lui-même : `jsonify(moteur.build(...))` → corps entier,
  `jsonify({'risque': moteur.f(...)})` → clé `risque`. C'était le cas de
  **quatorze** moteurs sur trente : je rangeais « indéterminé » ce que l'arbre
  disait tout haut.

Chaque candidat est ensuite confronté au **produit vivant**, et — correction qui
a levé deux angles morts d'un coup — à **sa propre route** : `build_packet(...)`
publie dans `packet.events`, pas dans `packet.contexts` que seul je regardais, et
`knowledge_graph` sort sur `/api/skyler/graph/<sym>`, que `/api/skyler/ACN` ne
pouvait évidemment pas contenir.

Résultat mesuré : **49 peints · 3 muets · 14 indéterminés · 11 indirects ·
10 sans appelant trouvé** (87 moteurs).

## Les trois muets ne sont pas trois chantiers

Mesuré un par un, aucun ne demande d'être peint tel quel — et c'est un résultat,
pas une dérobade :

| moteur | route | verdict mesuré |
| --- | --- | --- |
| `recommendation` | `/api/position-decision/<sym>` | recoupe la carte-verdict du Portefeuille |
| `legacy_basket_risk` | `/api/risk` | **superseded** : `hhi`, `correlations`, `sector_mix`, `in_bounds` vivent déjà dans `/api/portfolio/context` |
| `options_lab` | `/api/options-lab` | riche, mais sert **26 emoji** — le peindre violerait la règle des pictogrammes |

Les tests ci-dessous tiennent ces trois faits, pour qu'aucun ne soit peint par
mégarde en croyant combler un manque.
"""
import json

import pytest

#  Mesuré au lot 58 sur la réponse réelle : les figures de risque du panier ont
#  déjà un domicile canonique. Peindre `/api/risk` en créerait un second.
CLES_CANONIQUES = ('hhi', 'correlations', 'sector_mix', 'in_bounds', 'bounds')

MUETS = {
    'recommendation': '/api/position-decision/',
    'legacy_basket_risk': '/api/risk',
    'options_lab': '/api/options-lab',
}


@pytest.fixture(scope='module')
def client(tmp_path_factory):
    """LA REDIRECTION PASSE PAR `setattr`, ET CE N'EST PAS UN DÉTAIL DE STYLE.

    Ce fichier écrit `desk_data.json` (il sème trois positions pour atteindre un
    état que le produit peut réellement calculer). `tests/test_desk_ecritures_lot387.py`
    veille à ce qu'aucun test n'écrive dans le VRAI desk de l'utilisateur, et il
    reconnaît la redirection à la forme `setattr(persist, '_BASE_DIR', …)` —
    convention suivie par douze fichiers. Ma première version affectait
    directement l'attribut : redirection réelle, mais invisible au gardien, qui
    m'a donc accusé. Il avait raison de le faire : sa règle est une forme
    reconnaissable, et une forme que lui seul ne peut pas vérifier ne protège
    plus rien. On se conforme à la convention plutôt que d'élargir le gardien.
    """
    from vertex.services import persist
    sauve = persist._BASE_DIR
    setattr(persist, '_BASE_DIR', str(tmp_path_factory.mktemp('inv58')))
    import terminal
    yield terminal.app.test_client()
    setattr(persist, '_BASE_DIR', sauve)


def _chaines(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from _chaines(v)
    elif isinstance(o, list):
        for v in o:
            yield from _chaines(v)


def test_le_risque_de_panier_a_deja_son_domicile_canonique(client, tmp_path):
    """`legacy_basket_risk` est superseded, et ce test le prouve plutôt que de
    l'affirmer : les figures qu'il calcule sont servies par le contexte
    portefeuille, celui que la page Portefeuille lit réellement.

    IL FAUT DES POSITIONS. Première version : j'interrogeais la route sur un
    desk vide. Elle répondait — correctement — `available: false, « aucune
    position réelle déclarée »`, et aucune clé de risque. Je concluais à une
    régression alors que je mesurais un état sain. C'est la faute du lot 38 :
    *un instrument doit reproduire l'état que le produit peut réellement
    atteindre.* On sème donc trois positions réelles par la porte du produit."""
    import json as _json

    from vertex.services import persist
    blob = persist.load_json('desk_data.json', {}) or {}
    sauve = _json.dumps(blob)
    donnees = dict(blob.get('data') or {})
    donnees['myTrades'] = _json.dumps([
        {'sym': 'ACN', 'type': 'STK', 'qty': 10, 'price': 300.0, 'sector': 'Technology'},
        {'sym': 'MMM', 'type': 'STK', 'qty': 20, 'price': 100.0, 'sector': 'Industrials'},
        {'sym': 'AOS', 'type': 'STK', 'qty': 15, 'price': 80.0, 'sector': 'Industrials'},
    ])
    persist.save_json('desk_data.json', dict(blob, data=donnees))
    #  … ET DES COTES. Deuxieme etat inatteignable : avec les positions seules,
    #  la route repondait « valeur totale nulle — poids incalculables ». Les
    #  poids viennent de `scan_state['detail']`, pas du desk. Deux portes, pas
    #  une — le produit ne calcule un risque de panier que s'il connait les prix.
    from vertex.app.state import scan_state
    detail = scan_state.setdefault('detail', {})
    anciens = {s: detail.get(s) for s in ('ACN', 'MMM', 'AOS')}
    for s, px in (('ACN', 300.0), ('MMM', 100.0), ('AOS', 80.0)):
        detail[s] = dict(detail.get(s) or {}, price=px)
    try:
        pc = client.get('/api/portfolio/context').get_json() or {}
    finally:
        persist.save_json('desk_data.json', _json.loads(sauve))
        for s, v in anciens.items():
            if v is None:
                detail.pop(s, None)
            else:
                detail[s] = v
    assert pc.get('available') is not False, (
        'le contexte portefeuille reste indisponible malgre trois positions '
        'semees : %s' % str(pc.get('reason'))[:120])
    absentes = [k for k in CLES_CANONIQUES if k not in pc]
    assert not absentes, (
        '%s ne sont plus servies par /api/portfolio/context : le risque de '
        'panier perdrait son domicile canonique, et `/api/risk` (legacy) '
        'redeviendrait la seule source — a trancher avant de le laisser filer'
        % ', '.join(absentes))


def test_options_lab_sert_des_emoji_donc_ne_doit_pas_etre_peint_tel_quel(client):
    """LE PIÈGE POSÉ POUR PLUS TARD.

    `/api/options-lab` est riche — contexte marché, secteur, entreprise, plan,
    comparateur. Il porte aussi **des emoji du plan astral** dans ses champs
    `icon`. La règle mesurée aux lots 41/47/48 est *zéro emoji peint*. Tant que
    la route n'est pas consommée, aucune violation ; le jour où quelqu'un la
    peint sans filtrer, il en injecte des dizaines d'un coup.

    Ce test tient l'ALTERNATIVE, pas l'interdit : **ou bien** la route n'est pas
    demandée par l'interface, **ou bien** elle ne sert plus d'emoji.

    ON MESURE LA SOURCE, PAS LA CHARGE, et la contre-épreuve a dit pourquoi.
    Première version : je lisais les emoji dans la réponse du client de test. Il
    répond `empty: true` — aucune donnée de scan, donc **aucun emoji**. Le test
    passait même en simulant une page qui peint la route : cinquième gardien
    creux de la série. Les emoji sont des **littéraux du moteur** ; c'est un
    fait de structure, stable quel que soit l'état des données."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parent.parent
    ecran = ''
    for p in list((racine / 'vertex' / 'ui').rglob('*.py')) + \
            list((racine / 'vertex' / 'static' / 'vertex' / 'js').rglob('*.js')):
        ecran += p.read_text(encoding='utf-8', errors='replace')
    demandee = '/api/options-lab' in ecran

    source = (racine / 'vertex' / 'engines' / 'options_lab.py').read_text(encoding='utf-8')
    emoji = sorted({c for c in source if ord(c) >= 0x1F300})

    assert not (demandee and emoji), (
        '/api/options-lab est desormais demande par l\'interface ET sert encore '
        '%d emoji litteraux (%s). La regle mesuree aux lots 41/47/48 est zero '
        'emoji peint : filtrer les champs `icon` avant de rendre, ou ne pas '
        'rendre cette route' % (len(emoji), ' '.join(emoji[:8])))


@pytest.mark.parametrize('moteur,route', sorted(MUETS.items()))
def test_le_muet_reste_non_demande_ou_a_ete_tranche(moteur, route):
    """Les trois muets sont documentés (SIGNAL-OS-58 §2) avec un verdict chacun.
    Si l'un devient demandé par l'interface, c'est une décision de conception —
    elle doit être prise sciemment, pas subie : ce test la rend visible."""
    import pathlib
    racine = pathlib.Path(__file__).resolve().parent.parent
    ecran = ''
    for p in list((racine / 'vertex' / 'ui').rglob('*.py')) + \
            list((racine / 'vertex' / 'static' / 'vertex' / 'js').rglob('*.js')):
        ecran += p.read_text(encoding='utf-8', errors='replace')
    assert route not in ecran, (
        '%s (%s) est desormais demande par l\'interface. Ce n\'est pas une '
        'erreur en soi, mais SIGNAL-OS-58 §2 lui donne un verdict : le peindre '
        'demandait de trancher d\'abord (doublon de domicile, ou emoji a '
        'filtrer). Mettre a jour le rapport et ce test' % (moteur, route))


def test_l_instrument_resout_les_appels_non_affectes():
    """LA CAPACITÉ AJOUTÉE PAR CE LOT, TENUE PAR UN CAS RÉEL.

    Quatorze moteurs étaient « indéterminés » parce que leur appel n'était
    affecté à aucune variable. Si cette détection se casse, l'inventaire
    regonfle sans que rien ne le signale."""
    from tools.mesurer_moteurs_par_appelant import relever
    trace = relever()[1]
    non_affectes = [n for n, usages in trace.items()
                    if any(u['genre'] in ('cle', 'corps') and u['route']
                           for u in usages)]
    #  Borne fixée à la MESURE (26), pas à une intuition — ma première version
    #  exigeait 30 et échouait sur un produit sain.
    assert len(non_affectes) >= 26, (
        'seuls %d moteurs ont une cle ou un corps identifie : la resolution des '
        'appels non affectes ne fonctionne plus, et l\'inventaire va regonfler '
        'd\'indetermines' % len(non_affectes))
