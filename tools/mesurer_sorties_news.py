"""tools/mesurer_sorties_news.py — QUELLES ROUTES SERVENT DU TEXTE EXTERNE ?

Réserve n°1 du lot 32 : l'énumération des sorties de news était MANUELLE — le
gardien du lot 177 en nommait trois, le lot 32 en a trouvé une quatrième par
hasard, en cherchant pourquoi une mutation ne mordait pas. Un gardien qui liste
des noms ne peut pas voir la sortie qu'on ajoutera demain.

Cet outil renverse la charge de la preuve : il empoisonne les états partagés,
puis interroge **toutes** les routes GET de l'application et regarde lesquelles
renvoient la charge. Aucune liste à tenir à jour.

Les fonctions publiques (`couper_le_reseau`, `prouver_la_coupure`,
`neutraliser_le_worker`, `armer_l_alarme`, `chemins_get`, `interroger`) sont
partagées avec le gardien `tests/test_signal_os_enumeration_sorties_lot33.py` —
une seule mécanique, pas deux à maintenir.

GET uniquement : rien n'est muté, et l'invariant READONLY n'est même pas frôlé.

Usage : python tools/mesurer_sorties_news.py
"""
import os
import re
import signal
import socket
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Marqueurs distinctifs : s'ils ressortent tels quels, la route sert du balisage
# externe vivant. Aucun n'apparaît dans un texte légitime du produit.
MARQUEURS = ('<script>alert(1)', '<img src=x onerror=', 'javascript:alert(3)',
             '<b>PubTest</b>')
CHARGE = {'sym': 'TSTQ', 'title': '<script>alert(1)</script>Résultats "record"',
          'fr': '<img src=x onerror=alert(2)>', 'publisher': '<b>PubTest</b>',
          'link': 'javascript:alert(3)', 'time': '2026-01-02T10:00', 'senti': 1}

_ETAT = {'tirs': 0}

# Points HORS LIMITES : consigne de session, jamais appelés — y compris avec le
# réseau coupé et prouvé. La coupure garantit que rien ne sort ; elle ne dispense
# pas de respecter une interdiction qui porte sur l'APPEL lui-même. Ces routes
# sont comptées à part, nommées, et leur cas est raisonné à la lecture du code.
HORS_LIMITES = ('/api/ticker/', '/api/analyst/', '/api/correlations/',
                '/api/options-for/', '/desc/', '/options/')


def hors_limites(chemin):
    return any(chemin.startswith(p) for p in HORS_LIMITES)


def couper_le_reseau():
    """Coupe la sortie réseau. Deux étages, parce qu'un seul ne tient pas — et
    je l'ai mesuré en le cassant :

    1. `socket.socket.connect` — couvre `requests`, `urllib`, tout client Python.
       On patche la MÉTHODE, pas la classe : `ssl.SSLSocket` dérive de
       `socket.socket`, remplacer le symbole casse l'import de `yfinance`.
    2. Les variables de proxy pointées sur un port mort local — `yfinance` passe
       par `curl_cffi`, donc par libcurl, qui ouvre ses sockets en C : aucun
       patch Python ne l'arrête. Première version de cet outil : `socket.socket`
       remplacé, et des requêtes sont quand même parties vers Yahoo (refusées
       403 par le proxy). Un garde-fou qu'on n'a pas éprouvé n'est pas un
       garde-fou — d'où `prouver_la_coupure()`.
    """
    for var in ('HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
                'ALL_PROXY', 'all_proxy'):
        os.environ[var] = 'http://127.0.0.1:9'      # discard : rien ne sort
    os.environ['NO_PROXY'] = os.environ['no_proxy'] = ''

    if getattr(socket.socket.connect, '_vertex_coupe', False):
        return
    _vrai_connect = socket.socket.connect

    def _connect(self, adresse, *a, **k):
        hote = adresse[0] if isinstance(adresse, tuple) else adresse
        if str(hote) not in ('127.0.0.1', '::1', 'localhost'):
            raise OSError('reseau coupe (mesurer_sorties_news) : %s' % (hote,))
        return _vrai_connect(self, adresse, *a, **k)

    _connect._vertex_coupe = True
    socket.socket.connect = _connect


def prouver_la_coupure():
    """Un client HTTP réel tente une sortie. Elle DOIT échouer sans qu'aucun
    paquet ne quitte la machine (le proxy est un port mort local, l'hôte visé
    est un TLD réservé qui ne résout jamais). Rend (ok, détail)."""
    try:
        from curl_cffi import requests as curl
    except Exception as e:
        return False, 'curl_cffi introuvable : %s' % e
    try:
        r = curl.get('https://exemple.invalid/', timeout=4)
        return False, 'REPONSE RECUE (%s) — la coupure ne tient pas' % r.status_code
    except Exception as e:
        return True, type(e).__name__ + ' : ' + str(e)[:90]


def neutraliser_le_worker(terminal):
    """Le worker IBKR n'est pas connecté ici : une route qui l'attend bloque 20
    à 45 s (`RequestTimeout=45`, anti-blocage — à ne pas retirer). On le fait
    échouer tout de suite ; la route reste exercée par son chemin d'erreur, et
    ne peut de toute façon pas servir de news sans worker.

    Patché PARTOUT où la fonction est liée, par IDENTITÉ d'objet — les
    blueprints gardent leur propre référence après `from terminal import …`, et
    une liste de modules serait le même défaut que celui que ce lot corrige.
    Rend le nombre de liaisons remplacées."""
    vrai = terminal._opt_job

    def _sans_worker(*a, **k):
        raise RuntimeError('worker IBKR indisponible (balayage)')

    n = 0
    for module in list(sys.modules.values()):
        if not hasattr(module, '__dict__'):
            continue
        for nom in list(vars(module)):
            try:
                if getattr(module, nom) is vrai:
                    setattr(module, nom, _sans_worker)
                    n += 1
            except Exception:
                pass
    return n


def armer_l_alarme():
    """ESCALADE. Une alarme ordinaire ne suffit pas : le produit enveloppe ses
    attentes dans des `except Exception` (`desk.py` reçoit même `opt_job` en
    PARAMÈTRE de fabrique — une variable de fermeture, qu'aucun patch d'attribut
    n'atteint), avale la `TimeoutError` et repart attendre. La seconde alarme
    lève donc une `BaseException`, que ces gardes ne captent pas."""
    def _trop_lente(*a):
        _ETAT['tirs'] += 1
        if _ETAT['tirs'] == 1:
            raise TimeoutError('route trop lente')
        raise KeyboardInterrupt('route trop lente (escalade)')
    signal.signal(signal.SIGALRM, _trop_lente)


#  Valeurs de paramètre qu'on sait remplir HONNÊTEMENT, c'est-à-dire par une
#  valeur que le moteur reconnaît — un paramètre deviné rend un 404 ou un
#  `available: false`, et une route qui ne s'exécute pas ne prouve rien.
#    · symbole  → le ticker piégé, présent dans `news_state` et dans `detail`.
#    · univers  → les univers du scanner d'options (`horizon_scanners`).
#  Restent NON remplis, et c'est le vrai trou du balayage : les identifiants
#  (`<tracking_id>`, `<decision_id>`, `<position_id>`, `<chart_id>`,
#  `<group>/<key>`), qu'aucun jeu de démonstration ne porte, et
#  `<path:filename>` qui ne sert que des fichiers statiques.
_SYMBOLE = re.compile(r'<[^>]*(sym|ticker|tk)[^>]*>')


def chemins_get(app):
    """Toutes les routes GET, paramètre rempli quand on sait le faire sans
    inventer : symbole → ticker piégé, univers → `LEAPS`. Le reste est écarté
    et NOMMÉ comme réserve (voir SIGNAL-OS-38 §4) plutôt que deviné."""
    out = set()
    for r in app.url_map.iter_rules():
        if 'GET' not in (r.methods or set()):
            continue
        chemin = str(r.rule)
        if '<' in chemin:
            if chemin.count('<') == 1 and _SYMBOLE.search(chemin):
                chemin = re.sub(r'<[^>]*>', 'TSTQ', chemin)
            elif '<universe>' in chemin:
                chemin = chemin.replace('<universe>', 'LEAPS')
            else:
                continue
        if hors_limites(chemin):
            continue
        out.add(chemin)
    return sorted(out)


def interroger(client, chemin, secondes=8, plafond=2_000_000):
    """Rend le corps servi (borné), ou None si la route n'aboutit pas — une
    route injoignable ne PROUVE rien et n'est jamais comptée comme propre.

    LECTURE BORNÉE, et ce n'est pas une optimisation. `/api/live/events` est un
    flux SSE : sa réponse ne se termine JAMAIS par conception, et un
    `client.get()` ordinaire la consomme indéfiniment. Mesuré : le balayage y
    restait bloqué, insensible même à l'escalade — non pas à cause d'un
    `except:` nu, comme je l'avais d'abord supposé, mais parce qu'il y avait
    toujours quelque chose de plus à lire. `buffered=False` + un plafond
    d'octets permet d'inspecter ce qu'un flux sert **sans attendre sa fin**."""
    _ETAT['tirs'] = 0
    signal.setitimer(signal.ITIMER_REAL, secondes, 2)
    morceaux, taille = [], 0
    try:
        rep = client.get(chemin, buffered=False)
        if rep.status_code >= 500:
            return None
        for bloc in rep.response:
            morceaux.append(bloc)
            taille += len(bloc)
            if taille >= plafond:
                break
    except BaseException:            # y compris l'escalade — voir armer_l_alarme
        return b''.join(morceaux).decode('utf-8', 'replace') or None
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        try:
            rep.close()
        except Exception:
            pass
    return b''.join(morceaux).decode('utf-8', 'replace')


def _option(argv, nom, defaut=None):
    if nom in argv:
        i = argv.index(nom)
        return argv[i + 1] if i + 1 < len(argv) else defaut
    return defaut


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    journal = _option(argv, '--journal')
    sauter = set(filter(None, (_option(argv, '--sauter') or '').split(',')))
    tmp = tempfile.mkdtemp(prefix='vx-sorties-')
    import terminal
    from vertex.app.state import news_state, scan_state
    from vertex.services import persist
    persist._BASE_DIR = tmp                      # aucune écriture dans le dépôt

    couper_le_reseau()
    ok, detail = prouver_la_coupure()
    print('coupure reseau : %s  (%s)' % ('PROUVEE' if ok else 'NON PROUVEE', detail))
    if not ok:
        print('\nBALAYAGE REFUSE — sans coupure prouvee, interroger toutes les '
              'routes ferait sortir de vraies requetes.')
        return 2
    print('worker IBKR neutralise sur %d liaison(s)' % neutraliser_le_worker(terminal))
    armer_l_alarme()

    # CHAQUE STORE EST REMPLI COMME EN PRODUCTION, et c'est decisif.
    #  · `news_state['items']` est BRUT : la boucle d'actualites y depose les
    #    titres tels quels, et chaque SORTIE assainit.
    #  · `scan_state['detail'][sym]['news']` est deja ASSAINI : ce store a un
    #    seul ecrivain, la boucle de scan, qui neutralise AVANT de deposer.
    # Ma premiere version empoisonnait les deux a l'identique, en brut. Elle
    # accusait alors `/scan` et `/api/ticker` — pour un etat que la production
    # ne produit jamais. Un instrument qui fabrique un etat impossible mesure
    # son propre montage. (Constat du lot 33, applique ici au lot 38.)
    from vertex.services import news_plus
    news_state['items'] = [dict(CHARGE)]
    scan_state.setdefault('detail', {})['TSTQ'] = {
        'price': 100.0, 'news': news_plus.sanitize_news([dict(CHARGE)])}
    client = terminal.app.test_client()

    coupables, injoignables, servies = [], [], 0
    for chemin in chemins_get(terminal.app):
        if chemin in sauter:
            print('  … %-38s SAUTEE (resiste a l\'interruption)' % chemin, flush=True)
            continue
        if journal:
            # La route est nommée AVANT d'être sondée : celle qui tue le
            # processus se dénonce elle-même. Certaines gardes du produit sont
            # des `except:` NUS — ils rattrapent jusqu'au KeyboardInterrupt, et
            # aucune escalade en Python ne les traverse. Le superviseur relance
            # en sautant la coupable : le balayage finit, et ce qu'il n'a pas
            # couvert est NOMMÉ au lieu d'être tu.
            with open(journal, 'a', encoding='utf-8') as f:
                f.write(chemin + '\n')
        corps = interroger(client, chemin)
        if corps is None:
            injoignables.append(chemin)
            print('  … %-38s injoignable' % chemin, flush=True)
            continue
        servies += 1
        trouves = [m for m in MARQUEURS if m in corps]
        if trouves:
            coupables.append((chemin, trouves))

    print('\nroutes GET servies : %d · injoignables : %d' % (servies, len(injoignables)))
    print('persistance redirigee vers %s' % tmp)
    if not coupables:
        print('\nAUCUNE SORTIE NE SERT LA CHARGE.')
        return 0
    print('\n%d ROUTE(S) SERVENT DU BALISAGE EXTERNE :' % len(coupables))
    for chemin, trouves in coupables:
        print('  %-38s %s' % (chemin, ', '.join(trouves)))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
