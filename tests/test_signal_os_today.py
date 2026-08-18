"""SIGNAL OS · AUJOURD'HUI — la tuile qui affichait un zéro qu'elle n'avait pas.

Sur la capture du lot Shell, la première tuile KPI de l'accueil disait :

    Régime
    UNKNOWN  (0%)
    voir →

Trois choses fausses dans quatre lignes.

## 1. `(0%)` était fabriqué

`const conf = Math.round((reg.confidence || 0) * 100)` — et le libellé
concaténait `(conf + '%')` **sans condition**. Une confiance **absente** devenait
donc « 0% », indiscernable d'un zéro mesuré.

C'est **exactement** le défaut corrigé au lot 629 dans l'objet Regime Aura, à un
**second site d'appel** : le résumé. Le 629 avait corrigé `loadRegime` et laissé
`loadSummary` intact — la même page portait le correctif et le défaut.

## 2. `UNKNOWN` était présenté comme un nom de régime

Le moteur ne rend pas une valeur vide quand il ne tranche pas : il rend la
**chaîne `'UNKNOWN'`**. La tuile l'affichait telle quelle, en majuscules, à la
place où elle affiche `TREND` ou `RISK-OFF` — donc comme un régime parmi
d'autres. Le prédicat de `regime-aura.js` est repris ici, au même titre.

## 3. `voir →` occupait le troisième étage des quatre tuiles

`VISUAL_SYSTEM.md` donne la forme d'un KPI : `label → valeur → delta/contexte`.
Les quatre tuiles portaient la **même phrase**, qui ne disait rien que la tuile
ne dise déjà — elle est un lien en entier. `COPY.md` range `View more` dans les
libellés à éviter.

Le troisième étage porte désormais une donnée réelle : confiance du régime,
interprétation du breadth, bande de VIX, verdict du comité. Absente → `—`.

## Et la hiérarchie

Catalyseurs et portefeuille étaient dans un `<details>` **fermé**. `PAGES.md`
les classe **4ᵉ et 5ᵉ** des six rangs de la page. Un catalyseur à J-2 qu'il faut
déplier pour voir ne remplit pas son office. Voir
`test_total_rebuild_today_markets_lot621.py::test_today_keeps_one_regime_visual_and_shows_catalysts`.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BRIEF = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'briefing.py')
_COMPONENTS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'components.css')


def _src():
    return io.open(_BRIEF, encoding='utf-8').read()


def _sans_commentaires(src):
    """Un commentaire n'est pas du code. Sans ce filtre, l'explication d'un
    retrait compte comme le retour du défaut (même famille que 616-B)."""
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)      # blocs JS
    return re.sub(r'<!--.*?-->', '', src, flags=re.S)    # commentaires HTML


# ── 1. Le zéro fabriqué ──────────────────────────────────────────────────────

def test_la_confiance_absente_n_est_plus_transformee_en_zero():
    """`(reg.confidence||0)*100` : le `||` de commodité qui invente une mesure."""
    code = _sans_commentaires(_src())
    assert '(reg.confidence||0)' not in code.replace(' ', ''), (
        'le repli `||0` est revenu sur la confiance du résumé : une confiance '
        'ABSENTE redevient « 0 % », indiscernable d\'un zéro mesuré.')
    assert 'reg.confidence!=null' in code.replace(' ', ''), (
        'le résumé ne distingue plus une confiance absente d\'un zéro mesuré.')


def test_le_pourcentage_n_est_affiche_que_s_il_existe():
    """Le garde d'entrée ne suffit pas : le libellé concaténait le pourcentage
    SANS condition. C'est le point de rendu qui doit savoir se taire."""
    code = _sans_commentaires(_src())
    assert "'confiance n/d'" in code.replace('"', "'"), (
        'aucune formulation honnête pour une confiance absente : le rendu '
        'affiche donc forcément un nombre.')


# ── 2. 'UNKNOWN' n'est pas un régime ─────────────────────────────────────────

def test_le_resume_reconnait_la_chaine_d_indetermination():
    """Le prédicat de `regime-aura.js`, au même titre. Sans lui, la tuile
    affiche « UNKNOWN » là où elle affiche « TREND »."""
    code = _sans_commentaires(_src())
    assert 'function regimeIndetermine' in code, (
        'le résumé ne reconnaît plus la chaîne que le moteur rend quand il ne '
        'tranche pas : elle redevient un régime comme un autre.')
    assert 'unknown' in code.lower()
    assert 'Indéterminé' in code, (
        'plus de formulation honnête pour un régime non tranché.'
    )


# ── 3. Le troisième étage porte une donnée, pas une invitation ───────────────

def test_les_tuiles_ne_portent_plus_quatre_fois_la_meme_invitation():
    """`COPY.md` range `View more` dans les libellés à éviter, et
    `VISUAL_SYSTEM.md` réserve ce troisième étage au delta/contexte."""
    code = _sans_commentaires(_src())
    assert 'voir →' not in code, (
        '« voir → » est revenu dans les tuiles KPI : quatre fois la même phrase, '
        'à la place réservée au contexte de la valeur.')


def test_chaque_tuile_recoit_un_contexte_reel():
    """Les quatre appels passent un cinquième argument tiré des données."""
    code = _sans_commentaires(_src())
    for appel, contexte in (
            ("kpiTile('Régime'", 'regCtx'),
            ("kpiTile('Breadth'", 'brCtx'),
            ("kpiTile('VIX'", 'vix_band'),
            ("kpiTile('Meilleure opp.'", 'verdict')):
        i = code.index(appel)
        ligne = code[i:code.index('\n', i)]
        assert contexte in ligne, (
            'la tuile %s ne reçoit plus son contexte (%s attendu) : le 3ᵉ étage '
            'retombe sur « — » alors que la donnée existe.' % (appel, contexte))


def test_un_seul_seuil_de_breadth_dans_le_fichier():
    """La couleur encodait `>= 55` sans le dire ; le contexte le nomme. Deux
    écritures du seuil, et l'une dérive un jour sans l'autre."""
    code = _sans_commentaires(_src())
    assert code.count('>=55') <= 1, (
        'le seuil de participation est écrit %d fois : la couleur et le texte '
        'peuvent diverger.' % code.count('>=55'))


# ── 4. Plus de style en ligne dans le gabarit de tuile ───────────────────────

def test_la_tuile_kpi_ne_porte_plus_de_style_en_ligne():
    """`text-decoration`, `color:inherit` et `font-size:20px` étaient écrits en
    ligne dans le gabarit JS. Rien de dynamique, donc rien à justifier."""
    code = _sans_commentaires(_src())
    debut = code.index('function kpiTile')
    corps = code[debut:code.index('\n}', debut)]
    assert 'style="' not in corps, (
        'la tuile KPI réintroduit un style en ligne : %s'
        % corps[corps.index('style="'):][:60])
    css = io.open(_COMPONENTS, encoding='utf-8').read()
    assert 'a.vx-kpi-card{text-decoration:none' in css.replace(' ', ''), (
        'la règle CSS qui remplace le style en ligne a disparu : la tuile '
        'redevient un lien souligné et bleu.')
