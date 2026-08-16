"""SIGNAL OS · ANALYSE — le huitième espace, audité sans appeler ce qui est interdit.

## Le constat que je répétais depuis le lot 12 était faux deux fois

Je déclarais `/analysis/<sym>` « non mesurable » parce que l'ouvrir déclenche
`/api/ticker/<sym>`, appel sortant interdit dans cet environnement.

1. **`/analysis` — l'index — ne consulte que `/api/names`.** Il était mesurable
   depuis le début. Personne ne l'avait ouvert : la page portait le même nom que
   la fiche, et j'ai étendu l'interdiction de l'une à l'autre sans vérifier.
2. **La fiche est mesurable en AVORTANT les points d'entrée interdits au
   navigateur.** La requête ne part jamais, donc le serveur ne sort jamais. La
   mesure est **partielle** — elle prouve la structure, la mise en page et les
   erreurs de page, pas le rendu des données bloquées — et elle est dite comme
   telle.

> « Non mesurable » était un raccourci confortable : il transformait une mesure
> plus difficile en mesure impossible.

## Le défaut trouvé, et sa cause est déjà connue

Le **radar de scorecard** était tracé **sans question ni conclusion**.

C'est la **troisième** occurrence de la même cause structurelle, après le donut
« Secteurs » du Portefeuille (lot 12) : ce ne sont pas les graphiques qui
oublient la règle de `CHARTS.md`, ce sont **ceux qui n'entrent pas par le
gabarit `VXCharts.card`**. Trois fois le même mécanisme fait une règle, pas un
accident : *un graphique monté dans une carte bâtie à la main n'a personne pour
lui imposer sa question.*

## Ce que je n'ai PAS accusé

Le fil d'Ariane est rogné à 390 px (« Analyse » → 28 px coupés). Ce **n'est pas**
un défaut : il porte `text-overflow:ellipsis`, donc le rognage est **signalé**.
L'instrument du lot 13 l'exclut explicitement ; ma sonde ad-hoc, elle, ne le
faisait pas et l'accusait — onzième fois qu'une portée d'instrument me trompe,
cette fois par excès.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _src(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


def _bloc_radar():
    """Le bloc du radar SEUL.

    Portée : `an-scorecard` apparaît aussi dans une note de bas de carte
    (`an-scorecard-note`) située ailleurs. Chercher dans tout le fichier
    laissait passer le retrait de la question — dixième-et-unième variante du
    même piège de portée dans cette refonte.
    """
    src = _src('vertex', 'ui', 'pages', 'analysis_page.py')
    i = src.index("$('an-scores').innerHTML")
    # La borne de fin est le `}else if(...)`, PAS la première occurrence de
    # `missingAxes.length){` : celle-ci est le `if(...!missingAxes.length){`
    # qui OUVRE la branche, donc découper là tronquait le bloc avant la
    # dérivation qu'on vient y vérifier. Le test échouait sur du code présent.
    j = src.index('}else if(missingAxes.length){', i)
    return src[i:j]


def test_le_radar_de_scorecard_porte_sa_question():
    """`CHARTS.md` : « aucun graphique sans question ni conclusion ». Le radar
    était le troisième graphique du produit monté hors gabarit, donc le
    troisième sans personne pour la lui imposer."""
    bloc = _bloc_radar()
    assert 'vx-chart-question' in bloc, (
        'le radar de scorecard a reperdu sa question : c\'est un graphique '
        'monté dans une carte bâtie à la main, donc rien d\'autre ne la lui '
        'impose.')
    assert 'Quel axe de la décision est le plus faible' in bloc, (
        'la question du radar a changé — vérifier qu\'elle porte toujours sur '
        'une lecture, pas sur la description du graphique.')


def test_la_conclusion_du_radar_est_derivee_des_axes_traces():
    """CONTRE-EXEMPLE du test précédent, et c'est celui qui compte. Une phrase
    générique aurait satisfait « il y a une conclusion » tout en étant pire
    qu'une absence : elle aurait eu l'air d'une mesure.

    On exige donc que la conclusion NOMME un axe et SA VALEUR, calculés depuis
    les axes réellement tracés.
    """
    bloc = _bloc_radar()
    assert "scAxes.slice().sort(" in bloc, (
        'la conclusion du radar n\'est plus dérivée des axes tracés : si elle '
        'est devenue une phrase fixe, elle affirme sans mesurer.')
    assert "'Axe le plus faible : '+faible[0]+' ('+faible[1]+'/100).'" in bloc, (
        'la conclusion ne nomme plus l\'axe ET sa valeur.')
    # L'HÔTE, pas son lecteur. `'an-scorecard-ccl' in bloc` restait VERT quand
    # on supprimait le `<p>` : la ligne qui l'interroge, `$('an-scorecard-ccl')`,
    # contient elle aussi l'identifiant. Le test était satisfait par le code
    # qui LIT l'élément, pas par l'élément. Douzième portée trop large de cette
    # refonte, et la mutation l'a attrapée — pas la relecture.
    assert '<p class="vx-chart-conclusion" id="an-scorecard-ccl"></p>' in bloc, (
        'l\'hôte de la conclusion du radar a disparu : la dérivation calcule '
        'une phrase que plus rien n\'affiche.')


def test_l_etat_honnete_du_radar_survit():
    """Quand un axe manque, le radar n'est PAS tracé et le dit en nommant les
    axes absents. Ajouter question et conclusion ne devait pas écraser cet
    état : un radar tracé sur des axes partiels serait un chiffre inventé."""
    src = _src('vertex', 'ui', 'pages', 'analysis_page.py')
    assert 'Radar non tracé — axes n/d' in src, (
        'l\'état honnête du radar a disparu : des axes manquants risquent '
        'd\'être tracés comme des axes mesurés.')
    assert 'missingAxes' in src


def test_l_instrument_de_rognage_couvre_enfin_la_fiche():
    """La fiche était le seul écran du produit qu'AUCUN instrument ne balayait,
    et la raison — « points d'entrée interdits » — était contournable.

    Portée : on vérifie la ROUTE dans PAGES **et** le mécanisme d'avortement.
    Vérifier seulement la première laisserait un instrument qui visite la fiche
    en déclenchant ce qu'il ne doit pas déclencher.
    """
    src = _src('tools', 'mesurer_rognage_silencieux.py')
    assert "('/analysis/ACN', [''])" in src, (
        'l\'instrument ne balaie plus la fiche : elle redevient le seul écran '
        'du produit que personne ne mesure.')
    assert 'INTERDITS' in src and "'**/api/ticker/**'" in src, (
        'la liste des points d\'entrée interdits a disparu de l\'instrument.')
    assert 'pg.route(_motif, lambda r: r.abort())' in src, (
        'l\'instrument ne fait plus AVORTER les points d\'entrée interdits : '
        'il les appellerait vraiment en visitant la fiche.')


def test_les_onze_rangs_de_la_fiche_ont_chacun_leur_hote():
    """`PAGES.md` §4. Mesuré au navigateur : 11 sur 11 présents. On tient ici
    les hôtes, pour qu'une suppression se voie sans navigateur."""
    src = _src('vertex', 'ui', 'pages', 'analysis_page.py')
    manquants = [h for h in (
        'an-verdict', 'an-scenarios', 'an-chart', 'an-catalysts',
        'an-fundamental', 'an-technical', 'an-sentiment', 'an-rail-risks',
        'an-options', 'an-history') if ('id="%s"' % h) not in src]
    assert not manquants, (
        'des rangs de PAGES.md §4 ont perdu leur hôte : %s' % manquants)
