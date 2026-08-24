"""
vertex/app/routes/system.py — SANTÉ SYSTÈME & PWA (Blueprint, Ch. II).

Health-check, état système institutionnel (version, LECTURE SEULE, sources,
fraîcheur des caches, moteurs), et l'enveloppe PWA (favicon, manifeste, service
worker). Lit l'état partagé ; aucune donnée sensible ; jamais d'ordre.
"""

import time
from collections import deque

from flask import Blueprint, jsonify, Response, request

from vertex.ai import briefs as ai
from vertex.app.config import IBKR_ENABLED, DEMO_MODE
from vertex.app.state import scan_state
from vertex.data.universe import UNIVERSE
from vertex.data import constants as _vconst
from vertex.data.constants import BUILD
from vertex.services import status_service as _status_svc

bp = Blueprint('system', __name__)


@bp.route('/healthz')
@bp.route('/api/healthz')
def healthz():
    """Health check (Render) — toujours 200 si le process répond. Indique l'état
    du scan sans bloquer. Aucune donnée sensible, lecture seule."""
    return jsonify({
        'status': 'ok',
        'build': BUILD,
        'data_source': scan_state.get('source'),
        'ibkr_enabled': IBKR_ENABLED,
        'universe': len(UNIVERSE),
        'scanned': scan_state.get('scanned_n'),
        'last_scan': scan_state.get('updated'),
        'scan_age': round(time.time() - scan_state['scan_ts']) if scan_state.get('scan_ts') else None,
        'scan_error': scan_state.get('error'),
        'source_health': scan_state.get('source_health') or {'scan': 'UNKNOWN'},
        'vertex_ready': sum(1 for d in (scan_state.get('detail') or {}).values() if d.get('vertex')),
        'engines': ['scoring', 'pivots', 'committee', 'strategy', 'portfolio_risk',
                    'vertex', 'vertex_ml', 'validator'],
    }), 200


# ─── TÉLÉMÉTRIE D'ERREURS CLIENT (objectif 0-erreur : observer pour corriger) ───
# Les erreurs JS des navigateurs remontent ici (window.onerror du vx_kit).
# Borné (100 max, payloads tronqués) — aucune donnée sensible, lecture locale.
_CLIENT_ERRORS = deque(maxlen=100)


@bp.route('/api/client-log', methods=['POST'])
def client_log_post():
    b = request.get_json(force=True, silent=True) or {}
    _CLIENT_ERRORS.append({
        'ts': round(time.time()),
        'page': str(b.get('page') or '')[:120],
        'msg': str(b.get('msg') or '')[:300],
        'src': str(b.get('src') or '')[:160],
        'line': b.get('line') if isinstance(b.get('line'), int) else None,
    })
    return jsonify({'ok': True})


@bp.route('/api/client-log')
def client_log_get():
    """Journal des erreurs JS remontées par les navigateurs — diagnostic 0-erreur."""
    return jsonify({'count': len(_CLIENT_ERRORS), 'errors': list(_CLIENT_ERRORS)})


@bp.route('/api/system/startup-report')
def startup_report_ep():
    """Rapport de la séquence de démarrage (§10) — honnête, jamais « OK » sans preuve."""
    from vertex.services.startup import startup_report
    return jsonify(startup_report())


@bp.route('/api/system/config')
def config_validation_ep():
    """Statuts de configuration CONFIGURED/MISSING/INVALID — aucune valeur exposée."""
    from vertex.app.config_validation import validate_config
    return jsonify(validate_config())


@bp.route('/api/system/automations')
@bp.route('/api/system/jobs')
def automations_ep():
    """Registre des jobs de fond : statut, dernière exécution, cadence, erreurs.
    Alias canonique /api/system/jobs (§41)."""
    from vertex.scheduler import registry
    return jsonify({'jobs': registry.jobs()})


@bp.route('/api/system/connections')
def connections_ep():
    """État honnête des connexions (§41) — IBKR/TradingView/Claude/stockage/
    scheduler/live. Statuts canoniques, jamais plus favorables que la réalité ;
    aucun secret exposé."""
    from vertex.services import connections
    return jsonify(connections.snapshot(scan_state, ibkr_enabled=IBKR_ENABLED,
                                        demo_mode=DEMO_MODE))


@bp.route('/readyz')
def readyz():
    """Readiness (§41) — l'application est-elle prête à servir ? Distinct de
    /healthz (process vivant). 200 si prête, 503 sinon. Honnête : n'affirme
    READY que si les vérifications critiques passent."""
    checks = []

    def _chk(name, ok, detail=''):
        checks.append({'name': name, 'ok': bool(ok), 'detail': detail})
        return ok

    # 1. Configuration validable.
    try:
        from vertex.app.config_validation import validate_config
        cfg = validate_config()
        bad = [k for k, v in cfg.items() if isinstance(v, dict) and v.get('status') == 'INVALID']
        _chk('configuration', not bad, 'invalides: %s' % ','.join(bad) if bad else 'valide')
    except Exception:
        _chk('configuration', False, 'configuration_indisponible')

    # 2. Stratégie chargée (constitution canonique).
    try:
        from vertex.strategy import profile as _prof  # noqa: F401
        _chk('strategie', True, 'constitution disponible')
    except Exception:
        # tolérant : la stratégie peut vivre ailleurs — non bloquant.
        _chk('strategie', True, 'module stratégie optionnel')

    # 3. Stockage desk lisible.
    try:
        from vertex.services import persist
        persist.load_json('desk_data.json', {})
        _chk('stockage', True, 'desk lisible')
    except Exception:
        _chk('stockage', False, 'stockage_indisponible')

    # 4. READONLY effectif (invariant absolu).
    from vertex.app.config import READONLY
    _chk('readonly', bool(READONLY), 'lecture seule effective')

    ready = all(c['ok'] for c in checks)
    return jsonify({'ready': ready, 'readonly': True, 'checks': checks,
                    'build': BUILD}), (200 if ready else 503)


@bp.route('/api/system-status')
@bp.route('/api/system/status')
def system_status_ep():
    """État système institutionnel : version, LECTURE SEULE, sources, fraîcheur
    des caches, âge scan/options/fondamentaux/news, moteurs. Analyse uniquement."""
    detail = scan_state.get('detail') or {}
    ok = not scan_state.get('error') and bool(scan_state.get('rows'))
    last = scan_state.get('updated')
    engines = [
        _status_svc.engine_status('scanner', ok=ok, last_success=last, last_error=scan_state.get('error')),
        _status_svc.engine_status('scoring', ok=ok, last_success=last),
        _status_svc.engine_status('vertex', ok=any(d.get('vertex') for d in detail.values()), last_success=last),
        _status_svc.engine_status('physics', ok=any(d.get('physics') for d in detail.values()), last_success=last),
        _status_svc.engine_status('timeframe', ok=any(d.get('mtf') for d in detail.values()), last_success=last),
        _status_svc.engine_status('options', ok=bool(scan_state.get('options_board')), last_success=last),
        _status_svc.engine_status('committee', ok=bool(scan_state.get('committee')), last_success=last),
        _status_svc.engine_status('validator', ok=ok, last_success=last),
    ]
    thresholds = {'scan': _vconst.STALE_SCAN_SEC, 'options': _vconst.STALE_OPTIONS_SEC,
                  'fundamentals': 86400, 'news': 3600}
    return jsonify(_status_svc.build_system_status(
        scan_state, build=BUILD, readonly=True, ibkr_enabled=IBKR_ENABLED,
        demo_mode=DEMO_MODE, ai_on=ai.available(), thresholds=thresholds, engines=engines))


@bp.route('/favicon.ico')
@bp.route('/favicon.svg')
def favicon_ep():
    """Favicon Vertex : triangle cuivre sobre sur fond obsidienne, en SVG inline
    (aucune dépendance fichier → zéro 404 dans l'onglet du navigateur)."""
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
           "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
           "<stop offset='0' stop-color='#e1a06e'/><stop offset='1' stop-color='#b96d3c'/>"
           "</linearGradient></defs>"
           "<rect width='64' height='64' rx='14' fill='#0b0e14'/>"
           "<path d='M32 15 L49 45 L15 45 Z' fill='url(#g)'/>"
           "</svg>")
    return Response(svg, mimetype='image/svg+xml',
                    headers={'Cache-Control': 'public, max-age=86400'})


@bp.route('/manifest.webmanifest')
def manifest_ep():
    """Manifeste PWA → permet « Ajouter à l'écran d'accueil » sur iPhone/Android
    et l'ouverture en plein écran comme une vraie app."""
    return jsonify({
        'name': 'Vertex — Cockpit IBKR',
        'short_name': 'Vertex',
        'description': "Cockpit d'analyse trading (analyse only).",
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'orientation': 'portrait-primary',
        'background_color': '#0b0e14',
        'theme_color': '#0b0e14',
        'icons': [
            {'src': '/static/icon-180.png', 'sizes': '180x180', 'type': 'image/png', 'purpose': 'any maskable'},
        ],
    })


_SW_JS = r"""
const CACHE='td-shell-v213';  // v213 : 169 ecritures innerHTML NUES (hote pris par identifiant, sans verifier qu'il existe) passent a la forme gardee dans 11 fichiers, dont TROIS servis sous /static (vx-shell.js, pages/options-gex.js, pages/options-structure.js). Une requete en vol qui revient sur un DOM remplace rompait la promesse — « Cannot set properties of null » —, defaut intermittent corrige d'abord sur /markets SEULEMENT, et revenu le lendemain sur l'accueil : le motif etait produit-wide. Bump obligatoire, sinon un visiteur en cache garde les trois JS fautifs. // v212 : les correctifs 9555b9c5 / 4b1a5e1f / 48581f33 ont modifie TROIS fichiers servis sous /static (neon-glass.css, charts/regime-aura.js, vx-core.js) SANS bumper cette version. Le service worker met tout /static en cache comme repli hors-ligne : sans bump, un visiteur qui a deja l'app en cache garde l'ANCIENNE copie et ne voit jamais ces correctifs — y compris la cle morte de /api/market/regime qu'ils reparent. Le gardien d'empreinte l'a trouve des qu'il a pu tourner sur cette machine (il etait rouge par construction sous Windows avant la correction de portabilite). Aucun asset n'est change ICI : on enregistre l'etat servi et on le fait suivre. // v211 G4/hors-ligne : UN AGE AFFICHE EST VRAI A LA SECONDE OU IL EST PEINT, ET FAUX ENSUITE. Mesure en vrai Chromium, horloge de la page avancee de 2 h : sur Marches, 11 lignes de provenance sur 11 FIGEES — « Il y a 21 min » indefiniment, RESEAU VIVANT, parce que la page n'enregistre aucune tache VX.refresh et ne repeint donc jamais. Le calcul n'etait pas en cause (VX.fmt.ago rendait bien « Aujourd'hui a 14:49 » sous horloge decalee, et assess({ageMs:2h}) rendait bien « stale ») : c'est le RENDU qui n'etait jamais rejoue. Reseau coupe, PLUS AUCUNE page ne repeint, y compris celles qui rafraichissent d'habitude. Correctif : updateIndicator emet `data-ts` et isole l'age dans `.vx-update-age`, assess/chip conservent l'instant de reference (`data-at`), et une tache de shell re-date toutes les 30 s SANS AUCUNE REQUETE — les chiffres restent, ils cessent seulement de se presenter comme frais. Mesure apres : Marches 1 gel sur 11, et le restant affiche « — » (age inconnu, aveu honnete) ; Portefeuille passe de 3 chiffres « dates faux » a 3 chiffres dates, la puce basculant seule. Et sur Aujourd'hui les QUATRE KPI de tete ne portaient AUCUNE date — la seule marque de la carte etait le badge « Demo », qui qualifie la nature de la donnee, pas son age : ils recoivent l'age reel du scan (`scan_age`, deja servi) via VX.freshness. // v210 #781 : le fil d'Ariane etait illisible en mobile. (a) Son segment d'espace est un LIEN et mesurait 19,5 px de haut sur les HUIT espaces — sous le plancher de 32 px des actions secondaires, seule cible tactile du produit sous ce plancher ; `padding-block:7px` (et non `min-height`+`display:flex`, qui casserait l'ellipse du lot 222) porte a 33,5 px, topbar a hauteur fixe donc inchangee. (b) Le fil recevait 84 px pour 122-185 px de contenu sur SEPT espaces sur huit : TOUS les segments tronques, separateur compris reduit a 2 px, alors que c'est le seul repere de lieu quand la sidebar est hors-ecran. Le nom d'espace est masque car PROUVE redondant (le h1 le repete a l'identique sur les 8) ; le sous-libelle, qui n'existe nulle part ailleurs, recupere la place. `:not(:last-child)` : sur /analysis le fil n'a qu'un segment, le masquer sans condition laisserait un topbar sans repere. // v209 QA/G4 : la rangee d'en-tete des cartes d'indices (.vx-mk-idx-top) ne pouvait ni passer a la ligne ni retrecir — monogramme fige a 34 px, pastille en `white-space:nowrap`, nom sans `min-width:0` — et le `overflow-x:hidden` de la carte COUPAIT le surplus en silence. Mesure a 390 px : 198 px de contenu dans 143 px, « milieu de plage » tronque sans points de suspension ni barre de defilement (Nasdaq, Dow). `flex-wrap:wrap` + ellipse sur le nom. // v208 lot #783/G3 : LE MOTEUR NE SE NOTAIT PAS. `track_record._fwd` cherchait un libelle '%m-%d' dans `series['dates']`, qui contient des dates ISO — la recherche levait ValueError sur CHAQUE entree, et `evaluate()` rendait `resolved: 0` quoi qu'il arrive. Mesure : 8 entrees dont +1, +5 et +20 etaient TOUS echus -> 0 resolue. Le defaut a survecu sous un test VERT dont la fixture fournissait des dates au format '08-01', que analysis.py ne produit jamais (il emet l'ISO et garde les libelles courts dans `date_labels`, « afin de ne jamais reinterpreter les annees »). Jointure en ISO ; `evaluate` detaille desormais POURQUOI chaque entree n'est pas notee (horizon non echu / titre plus suivi / seance introuvable) ; la note servie avoue que la fiabilite ne porte que sur les SURVIVANTS ; et l'ecran ne dit plus « le registre se remplit a chaque scan » — il le disait pour une condition qui ne pouvait jamais se resoudre. // v207  // v207 lot G1/#779 : le registre de jobs declarait 27 automatisations dont 20 n'avaient AUCUN emetteur `beat` dans le code — mesure AST, pas supposition. La page Systeme les affichait toutes « jamais execute », le meme mot pour un job en panne et pour un job qui n'existe pas, et le pied de page EXPLIQUAIT ce silence par des « integrations absentes » : faux pour 18 lignes sur 27. NEWS_REFRESH, lui, tournait toutes les 60 s depuis toujours et se declarait a 900 s. Etats separes cote serveur (NON_IMPLEMENTE / EN_ATTENTE / ACTIF / ERREUR), deux emetteurs cables (NEWS_REFRESH, POSITION_REFRESH), cadences corrigees. // v206  // v206 lot 629 : REGIME AURA redessine, apres refus de la capture d'ecran. Le refus etait esthetique, les defauts etaient reels. (1) Le garde d'etat honnete testait `!o.regime`, mais le moteur rend la CHAINE 'UNKNOWN', qui est truthy : il ne s'est jamais declenche, et Vertex dessinait une jauge complete pour un regime qu'il n'a PAS mesure, peinte dans le corail que la charte reserve a « perte / risque REEL ». (2) Le site d'appel ecrivait `((r&&r.confidence)||0)*100` : une confiance ABSENTE devenait « 0 % confiance », un chiffre inventé affiche comme mesure — desormais null, couronne eteinte, « confiance n/d ». (3) L'arc plein en degrade continu etait peint sur TOUTE la course quelle que soit la confiance : rien ne montrait l'echelle. Couronne de 30 crans, cran allume quand son MILIEU est atteint (62 % = 19 allumes), crans eteints visibles, halo unique borne au lieu de deux ellipses floutees plein cadre. (4) Le verdict ne se repete plus (« Risque neuf BLOQUE · Regime UNKNOWN — risque neuf bloque »). CONTRE-EXEMPLE tenu par un gardien : une confiance nulle MESUREE ne fait PAS disparaitre le regime — 0 et absent restent deux choses, dans les deux sens. // v205  // v205 lot 628 : rythme vertical de l'accueil. Mesure sur un serveur DONT LE CODE A ETE VERIFIE : tuiles de decision a 415 px du haut, dont 74 px pour la barre de fraicheur (une seule ligne de metadonnees) et 51 px pour le bandeau demo. Padding et marges resserres, contenus intacts : 415 -> 387 px. Le bandeau demo reste visible, meme texte, meme contraste — c'est lui qui empeche de prendre une donnee synthetique pour une donnee reelle. // v204  // v204 lot 627 : en-tete de page resserre. Mesure sur les 8 pages a 1440 px : la premiere donnee etait a 247 px du haut en moyenne. Gain reel mesure : +15 px de moyenne (0 a 24 selon la page ; /analysis n'utilise pas .vx-page-lead). Le h1 est CONSERVE. // v203  // v203 lot 625 : les tuiles KPI du Portefeuille portaient un `grid-column:span 3` EN LIGNE, dimensionne pour la grille historique a 12 colonnes ; la bande `vx-kpi-strip` de la refonte n'en declare que 4, donc UNE tuile par rangee — mesure a 1440 px : 4 tuiles de 860 px empilees au lieu de 276 cote a cote. Corrige par la BANDE (le meme helper sert aussi des grilles a 12 colonnes ou span 3 est juste). Et la treemap d'allocation, dont la seule dimension de couleur etait le P&L — precisement ce qui manque quand IBKR est hors ligne — porte desormais la CONCENTRATION en repli, legende suivant le mode reel. // v202  // v202 lots 620-625 : refonte visuelle totale Obsidian Copper, systeme graphique responsive, huit espaces hierarchises et matrice mobile verifiee. // v201 lot 619 : fiche Analyse decision-first, preuves progressives, graphique principal honnete et responsive. // v200 lot 618 : fondations OBSIDIAN COPPER sobres, cartes analytiques stables, grilles tablette coherentes et shell graphique simplifie. // v199 lot 617 : `.vx-state{max-height:240px}` retire. Le piege ecrit d'avance — « un plafond sans regle overflow fait DEBORDER » — est REFUTE : dans une boite flex-column les enfants sont flexibles, donc le plafond ne rogne pas et ne fait pas deborder, il COMPRIME, et la compression est invisible a tout test de debordement (deux instruments ont repondu « aucun debordement » a tort avant que le troisieme ne trouve). Effet reel mesure a 390 px sur /journal?view=track-record : hauteur naturelle 249 px pour un plafond de 240, les 9 px absorbes ENTIEREMENT par l'icone fantome decorative (41 -> 31 px). Aucun texte perdu. L'en-tete du fichier, qui promettait « jamais un rectangle geant vide » sur la foi de ce plafond, est corrige avec lui. // v198 lot 615 : l'etiquette `td::before` du mode cartes — le seul texte qui NOMME chaque valeur sous 720 px — n'avait jamais ete rendue par aucun banc (tables vides, donc `.vx-table-cards td` inexistant) ; mesuree par injection DOM a 390 px, elle donnait EXACTEMENT 4,50 avec le #847a7c du lot 613, soit zero marge. Le 614 ayant remonte `muted`, `--vx-text-faint` passe a #8f8587 : marge +0,73 sur la pire surface servie, et `surface-selected` fermee au passage. // v197 lot 614 : `--vx-text-muted` tombait a 4,04:1 sous .vx-meta / .vx-kpi-label / .vx-card-footer / .vx-muted — sous le seuil WCAG AA sur 11 combinaisons page x largeur ; le lot 613 l'avait refuse (60 litteraux, decision de design), l'humain a tranche. Porte a #989092 (4,86, marge +0,36 ; le minimum strict #938a8c ne laissait que +0,01). Les 39 replis, palette.TEXT_MUTED et VXCharts.colors.muted suivent ; le ROLE SERIE ACIER (--vx-steel-3, palette.COPPER, derniere serie, lignes support/resistance) reste a #8A8284 — meme hexadecimal, deux roles, un sed aveugle aurait change la couleur d'une serie de donnees. // v196 lot 613 : `--vx-text-faint` valait #655d5f, soit 3,23:1 sur la surface la PLUS favorable du produit — ce palier ne pouvait atteindre le seuil WCAG AA (4,5:1) NULLE PART, alors qu'il porte du texte reel (.vx-help, .vx-mono, etiquettes de momentum a 8 px, en-tetes de table en mode cartes sous 768 px) ; porte a #847a7c, conforme sur les quatre surfaces ou ce texte est servi, hierarchie des paliers preservee. // v195 lot 612 : l'en-tete « Cibles tactiles >= 40px » annoncait un seuil deux lignes au-dessus d'un `.vx-btn-sm{min-height:32px}` — il decrivait une intention, pas le bloc ; mesure a 390 px : 40 boutons a 32 px, dont 20 hors bandeaux, donc une regle generale des actions secondaires et non un angle mort. Seuil inchange, description corrigee. // v194 lot 610 : un etat d echec ecrit en enfant direct d une .vx-grid tombait dans une colonne implicite — bandeau large de 22 px, contenu coupe de 102 px, A TOUTES LES LARGEURS (390 comme 1440) ; regle de famille : tout etat prend la grille entiere. // v193 lot 608 : les etats vides qui viennent du BUREAU (positions, alertes, suivis, watchlist, these, journal, equite) disent desormais quand le bureau n'a pas pu etre synchronise — le message du 607 etait un toast transitoire, celui-ci est DANS la zone ou l'utilisateur forme sa conviction ; les 39 etats vides qui viennent d'un moteur serveur ne le portent PAS (y coller la mention serait un mensonge d'un autre genre). // v192 lot 607 : la LECTURE du bureau echouait en silence (r.ok jamais lu, catch vide) — sur un navigateur neuf dont le GET /api/desk echoue, le bureau s'affiche VIDE et « aucun trade declare » devient indiscernable de « bureau non synchronise » ; le chemin de lecture dit desormais son echec. // v191 lot 606 (dossier 582, ferme) : la puce de fraicheur de /system portait `(man.age_s||0)*1000`, un REPLI sur un age — le serveur met deliberement age_s a null quand il ignore l anciennete, `null||0` vaut 0, donc « Analyse » au lieu du tiret honnete ; garde de type, comme les quatre autres puces. // v190 lot 604 : la synchro du bureau echouait EN SILENCE — `fetch('/api/desk',{POST}).catch(()=>{})` avalait l'echec reseau ET ne lisait jamais r.ok, donc un refus 4xx/5xx du serveur etait TOTALEMENT invisible sur les donnees PERSONNELLES de l'utilisateur ; les trois push (vx-entities.js + 2 inline de /system) disent desormais leur echec, sans dramatiser (rien n'est perdu, localStorage garde tout). // v189 lot 603 (dossier 531-A, suite) : trois sections de Portefeuille (dependances cachees, stress-scenarios, discipline) DISPARAISSAIENT sur echec reseau, et l'appetit pour le risque de Marches laissait sa zone vide et muette ; les quatre disent desormais leur etat. // v188 lot 602 (dossier 531-A) : deux zones d'Opportunites echouaient EN SILENCE — l'entonnoir laissait sa colonne vide et muette, le classement Skyler ne s'affichait pas du tout ; elles disent desormais leur etat (invariant : donnee absente -> mention honnete). // v187 lot 328 : honnêteté d'affichage — la page Système annonçait « contrat __DESK_KEYS », symbole disparu avec la purge É1 (lot 323) ; le contrat réel s'appelle DESK_KEYS (vx_kit + vx-entities) ; v186 lot 302 : clavier — le Tab traverse la recherche sans ouvrir la palette (elle s'ouvrait de force, boutons du topbar inatteignables) ; ouverture au clic/tap ou à la frappe ; v185 lot 299 : a11y — aria-label sur les 2 champs de la fiche Analyse (copilote + ticket pré-trade), seuls champs sans étiquette des 26 vues ; v184 lot 297 : honnêteté — le stress test du risque suit __pfLive (le chip « Live » était codé en dur, affiché même sur cotes de repli/DEMO) ; v183 lot 296 : honnêteté — la source du payoff options dit « board démo » en DEMO (l'étiquette « board réel » était codée en dur) ; v182 lot 295 : mobile — boutons tickers .vx-link (21px) et liens vx-dim (16px) portés à ≥40px ; v181 lot 294 : mobile — contrôles segmentés (réglages Système) portés à ≥40px (mesurés 26px) ; v180 lot 293 : mobile — liens d'approfondissement (vx-meta a) portés à ≥40px (mesurés 15px sur la fiche Analyse) ; v179 lot 291 : palette — le tap sur le fond ferme (aucune sortie tactile n'existait : Échap seulement) ; v178 lot 289 : mobile — champ de recherche (chemin tactile vers la palette) ≥40px + icône recentrée ; v177 lot 288 : mobile — pastille ⌘K masquée dans la recherche (affordance clavier mensongère au tactile ; le tap ouvre la palette) ; v176 lot 286 : carte Application — version publiée (serveur) + verdict à jour/mise à jour ; v175 lot 284 : carte Application (version shell + mise à jour forcée) ; v174 lot 283 : carte Verrou d'accès (Système)   // v173 (SKYLER LOT 232) : ligne de fraicheur/source (.vx-update) replie en mobile (un libelle long debordait de 201px sur /portfolio?view=risk) ; v172 (SKYLER LOT 222) : topbar mobile — crumb long et libellé du bouton retour tronquent en ellipse (ils passaient sous les boutons / hors ecran a 390px) ; v171 (SKYLER LOT 213) : texte des tuiles treemap → var(--vx-text-primary) ; gardien hex nu étendu aux builders JS ; v170 (SKYLER LOT 212) : étiquettes RRG (Marchés) + bordure démo (Opportunités) → tokens ; gardien « aucun hex nu dans les pages » ; v169 (SKYLER LOT 211) : movers Système — hex en dur remplacés par les tokens VXCharts.colors ; v168 (SKYLER LOT 209) : a11y — drawer/modal fermés aria-hidden + inert (bascule openDrawer/closeDrawer) ; v167 (SKYLER LOT 203) : cône de mouvement — bandes σ HACHURÉES (estimation) ; GEX — murs call/put dominants + valeur en chip ; v166 (SKYLER LOT 202) : niveaux du plan (levelLines) — chips pleine couleur au bord droit style échelle TV, anti-collision ; canonique LWC déjà natif TV ; v165 (SKYLER LOT 201) : radar TV — sommet dominant : anneau de focus + valeur en chip (C.radar) ; jauge environnement options ✔ héritage C.gauge ; v164 (SKYLER LOT 200) : série de référence Marchés — chips Max/Min sur les extrêmes réels (extremes de areaCard) ; discipline Journal ✔ héritage C.bars ; v163 (SKYLER LOT 199) : barres TV (C.bars partagé) — barre dominante en évidence : liseré appuyé + valeur en chip pleine couleur (IV sens., S+/S/A/B, leadership, movers héritent) ; v162 (SKYLER LOT 198) : rails TV (Marchés) — chip de valeur réelle sur le pointeur (Calme↔Stress : VIX ; Défense↔Attaque : confiance %) ; v161 (SKYLER LOT 197) : théta TV — remplissage hachuré (projection modèle) + chip Min (C.hatchPattern réutilisable, option hatch de C.area) ; v160 (SKYLER LOT 196) : fraîcheur TV (Système) — le domaine le plus rassis en dominante : tuile liserée + âge en chip pleine couleur ; v159 (SKYLER LOT 195) : équité/drawdown TV — chips Max/Min sur les extrêmes réels (tvExtremesPlugin) ; v158 (SKYLER LOT 194) : heatmap TV — texte des cellules coloré par intensité + cellule dominante en évidence ; treemap — part en chip pleine couleur ; v157 (SKYLER LOT 193) : catalystRunway TV — piste en dégradé continu, zone ≤5 j hachurée, chip J-x sur le prochain ; v156 (SKYLER LOT 192) : regimeAura aligné grammaire TV (arc dégradé + pointeur) + payoff hachuré GAIN/PERTE ; v155 (SKYLER LOT 191) : barres de consensus du comité (Intelligence) — style Note des analystes ; v154 (SKYLER LOT 190) : cône de projection du plan (fiche Analyse) — éventail TV chips de bord ; v153 (SKYLER LOT 189) : jauge TV — arc dégradé continu + aiguille blanche + état coloré (tournée graphique) ; v152 (SKYLER LOT 187) : hex du design-system dérivés de tokens.css (fin des étiquettes périmées)
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/manifest.webmanifest','/static/icon-180.png','/static/vertex/css/fonts.css','/static/vertex/fonts/inter-var.woff2','/static/vertex/fonts/jetbrains-mono-var.woff2']).catch(()=>{})));});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{const ks=await caches.keys();await Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener('fetch',e=>{
  const req=e.request; if(req.method!=='GET')return;
  const url=new URL(req.url); if(url.origin!==location.origin)return;
  const cacheable=(req.mode==='navigate'||url.pathname.startsWith('/static')||url.pathname==='/manifest.webmanifest');
  e.respondWith((async()=>{
    const cache=await caches.open(CACHE);
    try{
      // network-first : on prefere TOUJOURS le frais ; repli cache si reseau lent (cold start) ou hors-ligne
      const net=await Promise.race([fetch(req),new Promise((_,rej)=>setTimeout(()=>rej(new Error('to')),4500))]);
      if(net&&net.ok&&cacheable)cache.put(req,net.clone());
      return net;
    }catch(err){
      const c=(await cache.match(req))||(req.mode==='navigate'?await cache.match('/'):null);
      return c||fetch(req);
    }
  })());
});
"""


@bp.route('/sw.js')
def service_worker():
    """Service worker PWA (network-first + repli cache) — masque les cold starts
    Render. ⛔ Aucune donnee perso ici (favoris/notes restent en localStorage)."""
    return Response(_SW_JS, mimetype='application/javascript',
                    headers={'Service-Worker-Allowed': '/', 'Cache-Control': 'no-cache'})


__all__ = ['bp']
