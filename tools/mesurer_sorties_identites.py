"""tools/mesurer_sorties_identites.py — LES NEUF ROUTES QUE LE BALAYAGE RATAIT.

Réserve n°2 de `SIGNAL-OS-38` §4, mesurée au lot 39 : sur les 176 règles GET,
neuf portent un **identifiant** — suivi, décision figée, cellule de calibration,
position, graphique. `mesurer_sorties_news.py` ne sait pas les remplir : aucun
id valide n'existe dans le jeu de démonstration, et en inventer un rend un 404
qui ne prouve rien. Elles sortaient donc du balayage, silencieusement.

Cet outil-ci fabrique les identités, puis balaie les neuf routes.

## La règle apprise au lot 38, appliquée AVANT d'accuser

> Un instrument doit reproduire l'état que le produit peut réellement atteindre.

Elle commande tout ici, et deux fois :

1. **Le poison est déposé comme la production le dépose**, pas comme il est
   commode de le déposer. `news_state['items']` reçoit le titre BRUT (c'est ce
   que fait la boucle d'actualités) ; `scan_state['detail'][sym]['news']` reçoit
   la forme ASSAINIE (ce store a un écrivain unique, `terminal.py`, qui assainit
   avant de déposer). Empoisonner `detail` brut avait fait accuser `/scan` à
   tort au lot 38 — l'erreur ne sera pas refaite dans l'autre sens.
2. **Les identités sont créées par les portes du produit**, jamais en écrivant
   un magasin à la main avec une forme devinée. Le `decision_id` vient d'un vrai
   `GET /api/skyler/TSTQ` (cette route gèle la décision dans la mémoire) ; le
   suivi vient de `tracking.repository.create` — l'appel exact que fait le
   gestionnaire POST ; la position vient d'un blob desk au schéma réel
   (`data.myTrades`, chaîne JSON, comme le navigateur le pousse).

## L'anti-vacuité, spécifique à ce lot

Une route à identifiant interrogée avec un id qui ne résout pas rend un 404
structuré — et un 404 ne prouve **rien**. L'outil exige donc que chaque route
RÉSOLVE son identité (corps sans marqueur d'échec connu), et **refuse de
conclure** sinon : code de sortie 2, « aveugle », jamais un vert.

GET uniquement pour le balayage. Les identités sont semées en processus, par
appel de fonction — aucune requête HTTP mutante, l'invariant READONLY n'est pas
frôlé.

Usage : python tools/mesurer_sorties_identites.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_sorties_news import (  # noqa: E402  (chemin ajouté ci-dessus)
    CHARGE, MARQUEURS, armer_l_alarme, couper_le_reseau,
    neutraliser_le_worker, prouver_la_coupure,
)

SYM = 'TSTQ'

#  Les neuf règles à identifiant, telles que le lot 39 les a mesurées. La liste
#  est aussi écrite dans le gardien du lot 33 : si une dixième apparaît, la suite
#  échoue là-bas, et c'est ici qu'il faudra savoir la remplir.
REGLES = (
    '/api/tracking/<tracking_id>',
    '/api/tracking/<tracking_id>/history',
    '/api/tracking/<tracking_id>/performance',
    '/api/skyler/memory/<decision_id>',
    '/memory/<decision_id>',
    '/api/skyler/memory/cell/<group>/<key>',
    '/memory/cell/<group>/<key>',
    '/api/positions/<position_id>/changes',
    '/api/charts/<path:chart_id>/interpretation',
)

#  Signatures d'échec des gestionnaires — leur présence veut dire « identité non
#  résolue », donc route NON couverte. Elles sont recopiées des gestionnaires
#  eux-mêmes ; un libellé qui changerait ferait basculer l'outil en aveugle
#  (sortie 2), pas en faux vert.
ECHECS = ('suivi introuvable', 'decision_inconnue', 'Décision inconnue',
          'cellule_inconnue', 'groupe_inconnu', 'position introuvable',
          'Graphique non reconnu', 'chart_id inconnu')


def semer(app):
    """Fabrique les identités par les portes du produit. Rend un dict de
    substitutions {nom de paramètre → valeur}, ou lève si une porte a changé."""
    from vertex.app.state import cal_state, scan_state, news_state
    from vertex.services import news_plus, persist

    #  1. Le poison, sous les DEUX formes que la production produit.
    news_state['items'] = [dict(CHARGE)]
    detail = scan_state.setdefault('detail', {})
    detail[SYM] = {
        'price': 100.0,
        'closes': [90.0 + i for i in range(60)],
        'news': news_plus.sanitize_news([dict(CHARGE)]),
    }
    #  Un résultat daté : sans événement daté, la décision n'a pas de catalyseur
    #  et la cellule `by_catalyst_type` reste vide.
    cal_state.setdefault('items', []).append(
        {'sym': SYM, 'date': '2026-09-01', 'dte': 15})
    #  Une cellule de calibration n'existe qu'à partir de MIN_CALIBRATION_SAMPLE
    #  décisions MESURÉES (20). Un seul titre ne peut donc pas la former : il en
    #  faut autant de distincts, car l'identité d'une décision est un hachage de
    #  (titre, as_of, décision, version, démo). Les titres d'appoint ne portent
    #  aucune actualité — seul TSTQ porte la charge, et c'est lui qu'on suit.
    from vertex.engines import decision_memory as dm
    appoints = ['TST%02d' % i for i in range(1, dm.MIN_CALIBRATION_SAMPLE + 5)]
    for s in appoints:
        detail[s] = {'price': 100.0, 'closes': [90.0 + i for i in range(60)]}

    sub = {}
    client = app.test_client()

    #  2. decision_id — la VRAIE porte : `/api/skyler/<sym>` gèle la décision.
    client.get('/api/skyler/%s' % SYM)
    mem = persist.load_json(dm.MEMORY_FILE, None) or dm.empty_memory()
    decisions = mem.get('decisions') or []
    if not decisions:
        raise RuntimeError('aucune décision figée par /api/skyler/%s — la porte '
                           'a changé, refuser de conclure' % SYM)
    sub['decision_id'] = decisions[-1]['decision_id']

    #  3. group/key — la cellule exige des décisions MESURÉES, donc un RÉSULTAT
    #  par décision. La forme du résultat n'est pas devinée : `_measured_class`
    #  lit `horizons[H5|H20|H60].status == 'MESURE'`, rien d'autre ne compte.
    for s in appoints:
        client.get('/api/skyler/%s' % s)
    mem = persist.load_json(dm.MEMORY_FILE, None) or dm.empty_memory()
    for r in mem.get('decisions') or []:
        mem = dm.append_outcome(mem, {
            'decision_id': r['decision_id'],
            'measured_at': '2026-08-17T10:00:00+00:00',
            'sessions_observed': 20,
            'horizons': {'H20': {'status': 'MESURE', 'return_pct': 4.0}}})
    persist.save_json(dm.MEMORY_FILE, mem)

    #  La clé n'est pas choisie d'avance : on prend celle que le moteur a
    #  réellement formée. Aucune cellule MESURÉE ⇒ on refuse de continuer plutôt
    #  que d'interroger une route avec une clé qui rendrait un 404.
    from vertex.engines import skyler_core as sk
    ctx = dm.calibration_by_context(mem, sk.ENGINE_VERSION)
    formee = [(g, k) for g in dm.CONTEXT_GROUPS
              for k, c in (ctx.get(g) or {}).items()
              if c.get('status') == 'MESURE']
    if not formee:
        raise RuntimeError(
            'aucune cellule de calibration MESUREE apres %d decisions — '
            'la regle d\'appartenance a change' % len(mem.get('decisions') or []))
    sub['group'], sub['key'] = formee[0]

    #  4. tracking_id — l'appel exact du gestionnaire POST, sans passer par HTTP.
    from vertex.tracking import repository as repo
    tid = 'trk_mesure_identites'
    if repo.get(tid) is None:
        repo.create(tracking_id=tid, entity_type='STOCK', symbol=SYM,
                    quote={'last': 100.0, 'price': 100.0, 'source': 'scan'},
                    started_at='2026-08-17T10:00:00+00:00', market_open=True,
                    benchmark_quote=None, decision='SURVEILLER', score=21)
    sub['tracking_id'] = tid

    #  5. position_id — blob desk au schéma RÉEL : `data.myTrades` est une chaîne
    #  JSON, exactement ce que le navigateur pousse.
    pid = 'pos_mesure_identites'
    persist.save_json('desk_data.json', {'data': {'myTrades': json.dumps(
        [{'id': pid, 'sym': SYM, 'type': 'STK', 'qty': 10, 'cost': 1000.0,
          'note': CHARGE['title'], 'date': '2026-08-01'}])}})
    sub['position_id'] = pid

    #  6. chart_id — pas un magasin : un VOCABULAIRE, lu dans le gestionnaire.
    sub['path:chart_id'] = 'options.overview_mix'
    return sub


def interroger_avec_statut(client, chemin, secondes=20):
    """Comme `interroger`, mais rend AUSSI le code HTTP.

    `interroger` replie tout échec sur `None` — 500, exception et flux
    interminable deviennent le même « injoignable ». C'est le bon compromis pour
    balayer 158 routes ; ici il en reste neuf, et confondre « le serveur a
    renvoyé 500 » avec « la route n'a pas répondu » ferait perdre l'information
    la plus utile du lot. Aucune de ces neuf routes n'est un flux : une lecture
    ordinaire suffit."""
    import signal
    signal.setitimer(signal.ITIMER_REAL, secondes, 2)
    try:
        rep = client.get(chemin)
        return rep.status_code, rep.get_data(as_text=True)
    except BaseException as e:
        return None, '%s: %s' % (type(e).__name__, e)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def remplir(regle, sub):
    chemin = regle
    for nom, val in sub.items():
        chemin = chemin.replace('<%s>' % nom, str(val))
    return chemin if '<' not in chemin else None


def temoin(client):
    """LE TÉMOIN. Sans lui, ce lot rendrait un zéro qui ne prouve rien.

    Les neuf routes ne servent pas la charge — mais l'atteignent-elles seulement ?
    On fabrique un DÉFAUT : un second suivi dont le champ libre `decision` porte
    le balisage brut. Ce champ ne peut pas contenir de texte externe en
    production (le moteur y écrit un verdict d'un vocabulaire fermé) ; c'est
    précisément ce qui en fait un bon témoin — il n'existe que pour prouver que
    la chaîne semis → magasin → route → détection est vivante.

    Rend la liste des marqueurs effectivement ressortis."""
    from vertex.tracking import repository as repo
    tid = 'trk_temoin_identites'
    if repo.get(tid) is None:
        repo.create(tracking_id=tid, entity_type='STOCK', symbol=SYM,
                    quote={'last': 100.0, 'price': 100.0, 'source': 'scan'},
                    started_at='2026-08-17T10:00:00+00:00', market_open=True,
                    benchmark_quote=None, decision=CHARGE['title'], score=21)
    _, corps = interroger_avec_statut(client, '/api/tracking/%s' % tid)
    return [m for m in MARQUEURS if m in (corps or '')]


def sans_courtier():
    """Fixe l'environnement AVANT le premier import du produit, et pourquoi.

    `IBKR_ENABLED` est lu à l'import de la configuration, et `opt_job` est
    CAPTURÉ dans la fermeture du blueprint des positions
    (`make_blueprint(..., opt_job=_opt_job)`). `neutraliser_le_worker` remplace
    les liaisons de MODULE par identité d'objet : une cellule de fermeture lui
    échappe. Mesuré ici — `/api/positions/<id>/changes` attendait le worker
    45 s (`RequestTimeout`, anti-blocage) et sortait en « pas de reponse ». Sans
    courtier déclaré, la fermeture ne l'appelle jamais : c'est un état que la
    production atteint tous les jours (poste sans TWS).

    C'est aussi, mesurée, la cause des 3 routes « injoignables » du balayage des
    sorties de news — jusqu'ici constatées sans être expliquées.

    Appelé depuis `main`, pas à l'import : un outil ne doit pas modifier
    l'environnement du seul fait qu'on le lit."""
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('DEMO', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')


def main(argv=None):
    sans_courtier()
    couper_le_reseau()
    ok, detail = prouver_la_coupure()
    print('coupure reseau : %s  (%s)' % ('PROUVEE' if ok else 'NON PROUVEE', detail))
    if not ok:
        return 2
    armer_l_alarme()

    import tempfile
    from vertex.services import persist
    persist._BASE_DIR = tempfile.mkdtemp(prefix='vx-identites-')
    print('persistance redirigee vers', persist._BASE_DIR)

    import terminal
    print('worker IBKR neutralise sur %d liaison(s)'
          % neutraliser_le_worker(terminal))

    sub = semer(terminal.app)
    print('identites semees :')
    for nom in sorted(sub):
        print('   %-14s %s' % (nom, sub[nom]))

    client = terminal.app.test_client()

    coupables, aveugles, couvertes = [], [], 0
    for regle in REGLES:
        chemin = remplir(regle, sub)
        if chemin is None:
            aveugles.append('%s → parametre non substitue' % regle)
            continue
        statut, corps = interroger_avec_statut(client, chemin)
        if statut is None:
            aveugles.append('%s → pas de reponse (%s)' % (chemin, corps[:120]))
            continue
        if statut >= 500:
            aveugles.append('%s → HTTP %d (erreur serveur)' % (chemin, statut))
            continue
        if statut == 404:
            aveugles.append('%s → HTTP 404 (identite non resolue)' % chemin)
            continue
        rate = [e for e in ECHECS if e in corps]
        if rate:
            aveugles.append('%s → identite NON resolue (%s)' % (chemin, rate[0]))
            continue
        couvertes += 1
        trouves = [m for m in MARQUEURS if m in corps]
        if trouves:
            coupables.append('%s → %s' % (chemin, ', '.join(trouves)))

    print('\nroutes a identifiant : %d · couvertes : %d · non concluantes : %d'
          % (len(REGLES), couvertes, len(aveugles)))
    for a in aveugles:
        print('  … %s' % a)

    #  Le témoin passe APRÈS le balayage, et pas par confort : il dépose du
    #  balisage brut dans le magasin des suivis. Le faire avant, ce serait
    #  risquer qu'une route agrégeante le ramasse et se fasse accuser pour un
    #  défaut que l'instrument a lui-même semé.
    vus = temoin(client)
    print('temoin : %d/%d marqueur(s) ressorti(s) %s'
          % (len(vus), len(MARQUEURS), vus or ''))
    if not vus:
        print('\nAVEUGLE — le temoin ne ressort pas : la chaine semis → magasin '
              '→ route → detection est morte. Un zero ne prouverait rien.')
        return 2

    if coupables:
        print('\n%d ROUTE(S) SERVENT DU BALISAGE EXTERNE :' % len(coupables))
        for c in coupables:
            print('  %s' % c)
        return 1
    if aveugles:
        print('\nAVEUGLE — au moins une route n\'a pas resolu son identite. '
              'Un 404 ne prouve rien : refus de conclure.')
        return 2
    print('\nLES NEUF ROUTES A IDENTIFIANT SONT COUVERTES — aucune ne sert la charge.')
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
