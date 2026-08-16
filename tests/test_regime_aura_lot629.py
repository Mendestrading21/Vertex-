"""LOT 629 — UNE JAUGE COMPLÈTE POUR UN RÉGIME JAMAIS MESURÉ.

Capture d'écran utilisateur (refus du graphique) : la carte RÉGIME affichait
une jauge pleine, repère à zéro, arc corail, sous-titre « 0 % confiance », et
la ligne « Risque neuf BLOQUÉ · Régime UNKNOWN — risque neuf bloqué ».

Trois défauts RÉELS derrière le refus esthétique :

1. **Une absence présentée comme une lecture.** `regime-aura.js` avait bien un
   garde d'honnêteté — `if (o.state === 'empty' || !o.regime)`. Il ne s'est
   **jamais** déclenché : le moteur ne rend pas une valeur vide quand il ne
   tranche pas, il rend la **chaîne `'UNKNOWN'`**, qui est *truthy*. Le garde
   était donc décoratif depuis son écriture.

2. **Un chiffre inventé.** Le site d'appel écrivait
   `confidence: Math.round(((r && r.confidence) || 0) * 100)`. Une confiance
   **absente** devenait `0`, affichée « 0 % confiance » — indiscernable d'un
   zéro mesuré. C'est la règle « données réelles uniquement » prise à revers par
   un `||` de commodité.

3. **La couleur du risque réel pour une indétermination.** `newRisk === false`
   → tonalité `risk` → `--vx-negative`, que la charte réserve à « perte /
   risque RÉEL ». Vertex peignait en rouge le fait de ne pas savoir.

## Le dessin

Le refus portait sur le graphique, et le graphique méritait le refus pour une
raison mesurable : **l'arc plein en dégradé continu était peint sur toute la
course quelle que soit la confiance**. Rien ne montrait l'échelle, donc rien ne
disait où s'arrêtait la mesure. La couronne segmentée du 629 montre les crans
**éteints** : la confiance se compte.

## Mesure — le builder RÉELLEMENT exécuté

Ces gardiens n'inspectent pas la source à la recherche d'une chaîne (leçon du
lot 615 : compter un littéral dans les octets servis n'est pas mesurer un rendu).
Ils **exécutent** `regime-aura.js` dans Node avec un DOM minimal et lisent le
HTML produit. Sans Node, seuls les gardiens de source subsistent — ils sont
écrits pour tenir seuls.

| cas | attendu | mesuré |
| --- | --- | --- |
| `UNKNOWN`, conf 0 | état vide honnête | vide ✔, 0 cran |
| `TREND`, conf 62 | 19 crans allumés / 30 | 11 éteints ✔ |
| conf `null` | couronne éteinte, « confiance n/d », pas de repère | ✔ |
| `CHOP`, conf 0 | régime CONSERVÉ, 30 éteints, repère au départ | ✔ |
| invalidation redondante | fragment répété retiré | ✔ |

Le 4ᵉ cas est le contre-exemple qui borne le correctif : une confiance nulle
**mesurée** ne doit PAS faire disparaître l'objet. Confondre « 0 » et « absent »
dans l'autre sens serait le même défaut à l'envers.
"""

import json
import os
import shutil
import subprocess
import tempfile

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_AURA = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'charts', 'regime-aura.js')
_BRIEFING = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'briefing.py')

_NODE = shutil.which('node') or shutil.which('nodejs')

# Banc : le VRAI fichier servi, un DOM minimal, et on lit le HTML produit.
_BANC = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
const g = {
  VX: {
    states: { empty: (m) => '<!--EMPTY-->' + m, error: (m) => '<!--ERROR-->' + m },
    fmt: { nd: (v) => (v == null ? 'n/d' : String(v)) },
    updateIndicator: () => '<!--FOOT-->',
  },
  VXCharts: {},
};
const ctx = Object.assign({ document: { getElementById: () => null } }, g, { window: g });
vm.runInNewContext(src, ctx);
const out = JSON.parse(process.argv[3]).map((c) => {
  const h = { innerHTML: '' };
  g.VXCharts.regimeAura(h, c);
  const html = h.innerHTML;
  return {
    vide: html.indexOf('<!--EMPTY-->') >= 0,
    crans: (html.match(/<path d="M/g) || []).length,
    eteints: (html.match(/stroke="var\(--vx-border-default/g) || []).length,
    negatif: html.indexOf('--vx-negative') >= 0,
    repere: html.indexOf('stroke-width="2.6"') >= 0,
    verdict: (html.match(/class="vx-ra-verdict"[^>]*>([^<]*)</) || [null, ''])[1],
    conf: (html.match(/>(\d+ % confiance|confiance n\/d)</) || [null, ''])[1],
  };
});
process.stdout.write(JSON.stringify(out));
"""

_CAS = [
    # 0 — LE cas de la capture d'écran.
    {'regime': 'UNKNOWN', 'confidence': 0, 'newRisk': False,
     'invalidation': 'Régime UNKNOWN — risque neuf bloqué'},
    # 1 — régime mesuré, confiance mesurée.
    {'regime': 'TREND', 'confidence': 62, 'newRisk': True,
     'invalidation': 'Invalidation : SPX sous 5800 — risque neuf autorisé'},
    # 2 — régime mesuré, confiance ABSENTE.
    {'regime': 'RISK-OFF', 'confidence': None, 'newRisk': False,
     'invalidation': 'Risque neuf bloqué'},
    # 3 — CONTRE-EXEMPLE : confiance nulle MESURÉE, régime bien réel.
    {'regime': 'CHOP', 'confidence': 0, 'newRisk': None, 'invalidation': ''},
]

_SANS_NODE = pytest.mark.skipif(
    _NODE is None,
    reason='Node absent : les gardiens de source ci-dessous couvrent seuls le lot 629')


@pytest.fixture(scope='module')
def rendu():
    """HTML réellement produit par le builder, pour les 4 cas."""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False,
                                     encoding='utf-8') as f:
        f.write(_BANC)
        banc = f.name
    try:
        p = subprocess.run([_NODE, banc, _AURA, json.dumps(_CAS)],
                           capture_output=True, text=True, timeout=60)
        assert p.returncode == 0, 'le builder a levé une erreur :\n%s' % p.stderr
        return json.loads(p.stdout)
    finally:
        os.unlink(banc)


# ── 1. Le défaut de la capture : 'UNKNOWN' est une CHAÎNE ────────────────────

@_SANS_NODE
def test_un_regime_unknown_ne_dessine_aucune_jauge(rendu):
    """LE défaut. `!o.regime` laissait passer `'UNKNOWN'` (truthy) et Vertex
    dessinait une jauge complète pour un régime qu'il n'a pas mesuré."""
    r = rendu[0]
    assert r['vide'], (
        'un régime « UNKNOWN » produit encore un objet dessiné. Le garde '
        'd\'honnêteté ne reconnaît que l\'absence de valeur, pas la chaîne que '
        'le moteur rend quand il ne tranche pas.')
    assert r['crans'] == 0, 'des crans sont tracés sous l\'état vide'


@_SANS_NODE
def test_une_indetermination_n_emprunte_pas_la_couleur_du_risque_reel(rendu):
    """`--vx-negative` = « perte / risque RÉEL » par la charte. Ne pas savoir
    n'est pas une perte."""
    assert not rendu[0]['negatif'], (
        'l\'état indéterminé emploie encore --vx-negative : la couleur du '
        'risque réel pour une absence de mesure.')


# ── 2. Le contre-exemple qui borne le correctif ──────────────────────────────

@_SANS_NODE
def test_une_confiance_nulle_mesuree_ne_fait_pas_disparaitre_le_regime(rendu):
    """Symétrique du défaut : élargir le garde jusqu'à `confidence <= 0`
    supprimerait un régime RÉEL au motif qu'on y croit peu. `0` mesuré et
    `absent` sont deux choses, dans les deux sens."""
    r = rendu[3]
    assert not r['vide'], (
        'un régime CHOP mesuré à 0 % de confiance a disparu : le garde '
        'd\'indétermination mord au-delà de son objet.')
    assert r['conf'] == '0 % confiance'
    assert r['eteints'] == 30, 'la couronne devrait être entièrement éteinte'
    assert r['repere'], 'le repère marque la position mesurée, ici le départ'


# ── 3. L'échelle est visible — c'est ce que le dessin d'avant ne montrait pas ─

@_SANS_NODE
def test_la_couronne_montre_les_crans_eteints(rendu):
    """L'arc plein était peint sur TOUTE la course quelle que soit la
    confiance : rien ne disait où s'arrêtait la mesure. Un cran est allumé
    quand son MILIEU est atteint — 62 % ⇒ 19 allumés sur 30."""
    r = rendu[1]
    assert r['crans'] == 30, 'la couronne n\'a plus 30 crans (%d)' % r['crans']
    assert r['eteints'] == 11, (
        '62 %% de confiance devraient laisser 11 crans éteints (19 allumés, '
        'seuil au milieu du cran) ; mesuré : %d. Si la règle d\'allumage a '
        'changé, re-mesurer — un cran allumé de trop est un point de confiance '
        'inventé.' % r['eteints'])
    assert r['conf'] == '62 % confiance'


@_SANS_NODE
def test_une_confiance_absente_laisse_la_couronne_eteinte(rendu):
    """Une couronne vide se lit « je ne sais pas ». Un arc rempli à 0 % se
    lirait « minimum mesuré » — c'est exactement le contresens du 629."""
    r = rendu[2]
    assert r['conf'] == 'confiance n/d'
    assert r['eteints'] == 30
    assert not r['repere'], (
        'un repère est posé alors qu\'aucune confiance n\'a été mesurée : il '
        'désigne une position qui n\'existe pas.')


# ── 4. Le verdict ne se répète plus ──────────────────────────────────────────

@_SANS_NODE
def test_l_invalidation_ne_repete_plus_le_verdict(rendu):
    """« Risque neuf BLOQUÉ · Régime UNKNOWN — risque neuf bloqué ».
    Le verdict vient de `new_risk_allowed` (structuré) ; l'invalidation est un
    texte éditorial qui le reformule. On garde ce qui AJOUTE."""
    # Le préfixe « ▸ » qui figurait ici a été retiré du produit au lot 09 (2/n)
    # de Signal OS : c'était une puce décorative devant un texte déjà mis en
    # forme comme un verdict, et le seul pictogramme textuel encore RENDU sur
    # l'accueil. Il n'a jamais été le sujet de ce test — la propriété gardée est
    # que l'invalidation n'y répète pas le verdict, et elle est intacte.
    assert rendu[1]['verdict'] == 'Risque neuf autorisé · Invalidation : SPX sous 5800', (
        'fragment redondant conservé : %r' % rendu[1]['verdict'])
    assert rendu[2]['verdict'] == 'Risque neuf BLOQUÉ', (
        'une invalidation qui ne dit QUE le verdict devrait disparaître '
        'entièrement : %r' % rendu[2]['verdict'])


# ── 5. Gardiens de source — ils tiennent même sans Node ──────────────────────

def test_le_site_d_appel_ne_fabrique_plus_une_confiance_nulle():
    """`((r && r.confidence) || 0) * 100` : une confiance absente devenait un
    « 0 % confiance » affiché comme une mesure. C'est le site d'appel qui
    mentait, pas le builder."""
    src = open(_BRIEFING, encoding='utf-8').read()
    assert 'Math.round(((r&&r.confidence)||0)*100)' not in src, (
        'le `||0` est revenu dans briefing.py : une confiance absente est de '
        'nouveau affichée « 0 % confiance ».')
    assert 'r.confidence!=null' in src, (
        'le site d\'appel ne distingue plus une confiance absente d\'un zéro '
        'mesuré avant de la passer à regimeAura.')


def test_le_garde_reconnait_les_chaines_d_indetermination():
    """Anti-péremption du gardien exécuté : si le motif disparaissait de la
    source, les tests Node le verraient — mais pas sur une machine sans Node."""
    src = open(_AURA, encoding='utf-8').read()
    assert 'unknown' in src.lower(), (
        'plus aucune reconnaissance de « UNKNOWN » dans regime-aura.js : la '
        'chaîne que le moteur rend quand il ne tranche pas redevient un régime '
        'comme un autre.')
    assert 'VX.states.empty' in src
