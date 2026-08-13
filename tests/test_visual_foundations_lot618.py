"""LOT 618 — gardiens des fondations visuelles Obsidian Copper.

Ce fichier ne juge pas si l'interface est « belle ». Il verrouille les contrats
présentationnels qui peuvent régresser silencieusement entre les trois miroirs
de palette, les breakpoints et les builders JavaScript :

* le cuivre canonique CSS reste identique dans la palette Python, le thème JS
  et le repli du moteur de graphiques, sans devenir une couleur financière ;
* un couple de grille 4/8, 5/7 ou 3/9 ne produit jamais une ligne 12 + une carte
  orpheline à demi-largeur ;
* le Chart Shell ne propose « Détails » que lorsqu'une explication non vide
  existe ;
* un donut de plus de cinq catégories conserve son total via « Autres » ;
* les barres horizontales appliquent ``valueFmt`` à l'axe de valeurs, au
  tooltip et à la valeur dominante ;
* le texte d'une heatmap reste une encre stable et son échelle expose ses
  bornes ;
* une carte inerte n'hérite d'aucun hover global.

Les sondes JavaScript exécutent le code servi dans Node avec un DOM minimal.
Elles vérifient les objets de configuration produits, pas seulement la présence
d'une chaîne dans le fichier.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / 'vertex/static/vertex/css/tokens.css'
LAYOUT = ROOT / 'vertex/static/vertex/css/layout.css'
RESPONSIVE = ROOT / 'vertex/static/vertex/css/responsive.css'
CHARTS_CSS = ROOT / 'vertex/static/vertex/css/charts.css'
CORE = ROOT / 'vertex/static/vertex/js/charts/chart-core.js'
THEME = ROOT / 'vertex/static/vertex/js/charts/chart-theme-obsidian-copper.js'
HEATMAP = ROOT / 'vertex/static/vertex/js/charts/heatmap.js'


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def _literal_tokens() -> dict[str, str]:
    source = re.sub(r'/\*.*?\*/', '', _read(TOKENS), flags=re.S)
    return {
        match.group(1): match.group(2).lower()
        for match in re.finditer(
            r'(--vx-[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', source
        )
    }


def _token_values() -> dict[str, str]:
    """Résout les alias ``var(--vx-…)`` simples du registre canonique."""
    # Les commentaires citent parfois des noms de tokens : ils ne font pas
    # partie du registre et ne doivent jamais pouvoir gagner la compréhension.
    src = re.sub(r'/\*.*?\*/', '', _read(TOKENS), flags=re.S)
    raw = {
        match.group(1): match.group(2).strip()
        for match in re.finditer(r'(--vx-[a-z0-9-]+)\s*:\s*([^;]+);', src)
    }

    def resolve(name: str, trail: tuple[str, ...] = ()) -> str:
        assert name not in trail, 'cycle de tokens : %s' % ' → '.join(trail + (name,))
        value = raw.get(name, '')
        alias = re.fullmatch(r'var\((--vx-[a-z0-9-]+)\)', value)
        return resolve(alias.group(1), trail + (name,)) if alias else value.lower()

    return {name: resolve(name) for name in raw}


def _js_hex(source: str, key: str) -> str:
    match = re.search(r'\b%s\s*:\s*[\'\"](#[0-9a-fA-F]{6})[\'\"]' % re.escape(key), source)
    assert match, '%s introuvable dans le miroir JavaScript' % key
    return match.group(1).lower()


def _js_series(source: str) -> list[str]:
    match = re.search(r'\bseries\s*:\s*\[([^\]]+)\]', source, re.S)
    assert match, 'série graphique introuvable'
    return [value.lower() for value in re.findall(r'#[0-9a-fA-F]{6}', match.group(1))]


def _strip_css_comments(source: str) -> str:
    return re.sub(r'/\*.*?\*/', '', source, flags=re.S)


def _balanced_block(source: str, marker: str) -> str:
    """Renvoie le contenu du bloc qui suit ``marker`` (accolades imbriquées)."""
    start = source.index(marker)
    opening = source.index('{', start)
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == '{':
            depth += 1
        elif source[index] == '}':
            depth -= 1
            if depth == 0:
                return source[opening + 1:index]
    raise AssertionError('bloc CSS non fermé : %s' % marker)


def _grid_rules(source: str) -> list[tuple[set[int], int]]:
    rules = []
    for match in re.finditer(r'([^{}]+)\{([^{}]+)\}', source):
        span = re.search(r'grid-column\s*:\s*span\s*(\d+)', match.group(2))
        if not span:
            continue
        columns = {int(value) for value in re.findall(r'\.vx-col-(\d+)\b', match.group(1))}
        if columns:
            rules.append((columns, int(span.group(1))))
    return rules


def _effective_spans(width: int) -> dict[int, int]:
    base = {column: column for column in range(1, 13)}
    for columns, span in _grid_rules(_strip_css_comments(_read(LAYOUT))):
        for column in columns:
            base[column] = span

    responsive = _strip_css_comments(_read(RESPONSIVE))
    # Ordre du fichier = ordre de cascade. Les blocs plus étroits arrivent
    # après les plus larges et peuvent donc les corriger.
    for breakpoint in (1280, 1024, 768, 640):
        if width <= breakpoint:
            block = _balanced_block(responsive, '@media (max-width:%dpx)' % breakpoint)
            for columns, span in _grid_rules(block):
                for column in columns:
                    base[column] = span
    return base


_NODE_PRELUDE = r"""
const fs = require('fs');
const vm = require('vm');
global.window = global;
global.document = {
  documentElement: {},
  addEventListener() {},
  querySelectorAll() { return []; },
  createElement() { return {width:0,height:0,getContext(){return {};}}; },
};
global.getComputedStyle = () => ({getPropertyValue(){return '';}});
global.matchMedia = () => ({matches:false});
const drawerCalls = [];
window.VX = {
  fmt: {
    ago(value) { return value ? 'Il y a 1 min' : '—'; },
    num(value, digits) { return Number(value).toFixed(digits == null ? 1 : digits); },
    price(value) { return String(value); },
  },
  states: {
    loading() { return '<span>chargement</span>'; },
  },
  updateIndicator() { return '<span class="vx-update">source</span>'; },
  shell: {
    openDrawer(title, body) { drawerCalls.push({title, body}); },
  },
};
vm.runInThisContext(fs.readFileSync('vertex/static/vertex/js/charts/chart-core.js', 'utf8'),
                    {filename:'chart-core.js'});
"""


def _node_chart_probe(body: str, *, heatmap: bool = False) -> object:
    script = _NODE_PRELUDE
    if heatmap:
        script += "\nvm.runInThisContext(fs.readFileSync('vertex/static/vertex/js/charts/heatmap.js', 'utf8'), {filename:'heatmap.js'});\n"
    script += '\n' + body
    run = subprocess.run(
        ['node', '-e', script], cwd=ROOT, text=True, capture_output=True, check=False
    )
    assert run.returncode == 0, 'sonde Node en échec :\n%s' % run.stderr
    lines = [line for line in run.stdout.splitlines() if line.strip()]
    assert lines, 'sonde Node muette'
    return json.loads(lines[-1])


def _split_top_level_commas(selector_group: str) -> list[str]:
    """Sépare un groupe CSS sans couper les virgules internes de ``:is()``."""
    parts, current = [], []
    parens = brackets = 0
    quote = None
    for char in selector_group:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in "'\"":
            quote = char
        elif char == '(':
            parens += 1
        elif char == ')':
            parens = max(0, parens - 1)
        elif char == '[':
            brackets += 1
        elif char == ']':
            brackets = max(0, brackets - 1)
        elif char == ',' and not parens and not brackets:
            parts.append(''.join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append(''.join(current).strip())
    return parts


def test_identite_cuivre_canonique_et_miroirs_restent_alignes():
    from vertex.visualization import palette

    tokens = _token_values()
    literals = _literal_tokens()
    theme = _read(THEME)
    core = _read(CORE)

    assert literals['--vx-ember-500'] == '#d28a54'
    assert literals['--vx-ember-400'] == '#e1a06e'
    assert tokens['--vx-brand'] == literals['--vx-ember-500']
    assert tokens['--vx-brand-hover'] == literals['--vx-ember-400']

    canonical = tokens['--vx-brand']
    hover = tokens['--vx-brand-hover']
    assert palette.BRAND.lower() == canonical
    assert palette.BRAND_HOVER.lower() == hover
    assert palette.SERIES[0].lower() == canonical
    assert _js_hex(theme, 'brand') == canonical
    assert _js_hex(theme, 'brandHover') == hover
    assert _js_hex(core, 'brand') == canonical
    assert _js_hex(core, 'brandHover') == hover
    assert _js_series(theme)[0] == canonical
    assert _js_series(core)[0] == canonical

    # Le cuivre est une identité/référence, jamais une hausse ou une perte.
    assert canonical not in {palette.POSITIVE.lower(), palette.NEGATIVE.lower()}
    assert _js_hex(theme, 'positive') == palette.POSITIVE.lower()
    assert _js_hex(theme, 'negative') == palette.NEGATIVE.lower()
    # `COPPER` est un alias historique de la série acier : il ne doit pas être
    # entraîné par un changement de la marque.
    assert palette.COPPER.lower() == tokens['--vx-steel-3'] == '#8a8284'
    assert palette.COPPER.lower() != canonical


def test_les_couples_responsive_ne_creent_aucune_carte_orpheline():
    """Un couple peut garder son ratio, devenir 6/6, ou s'empiler 12/12.

    Toute autre combinaison (notamment 12/6) laisse une demi-ligne vide et
    sépare visuellement deux panneaux conçus comme un couple.
    """
    invalid = []
    for width in (1440, 1280, 1100, 1024, 768, 640, 390):
        spans = _effective_spans(width)
        for left, right in ((4, 8), (5, 7), (3, 9)):
            actual = (spans[left], spans[right])
            if not (sum(actual) == 12 or actual == (12, 12)):
                invalid.append('%d px · %d/%d → %d/%d' %
                               (width, left, right, actual[0], actual[1]))
    assert not invalid, (
        'couples de grille cassés (une carte tombe sur une demi-ligne) :\n  ' +
        '\n  '.join(invalid)
    )


def test_chart_shell_affiche_details_seulement_pour_une_explication_reelle():
    result = _node_chart_probe(r"""
function host() {
  return {
    html: '', listeners: {}, classList: {add() {}},
    set innerHTML(value) { this.html = value; },
    get innerHTML() { return this.html; },
    querySelector(selector) {
      if (selector === 'canvas') return this.html.includes('<canvas') ? {} : null;
      if (selector === '[data-explain]' && this.html.includes('data-explain=')) {
        return {addEventListener: (name, fn) => { this.listeners[name] = fn; }};
      }
      return null;
    },
  };
}
const absent = host();
VXCharts.card(absent, {title:'Sans objet explain'});
const vide = host();
VXCharts.card(vide, {title:'Objet vide', explain:{shows:'   ', why:null}});
const utile = host();
VXCharts.card(utile, {title:'Explication utile', explain:{why:'Ce signal change la décision.'}});
if (utile.listeners.click) utile.listeners.click();
console.log(JSON.stringify({
  absent: absent.html,
  vide: vide.html,
  utile: utile.html,
  drawer: drawerCalls[0] || null,
}));
""")

    assert 'data-explain=' not in result['absent'] and '>Détails<' not in result['absent']
    assert 'data-explain=' not in result['vide'] and '>Détails<' not in result['vide']
    assert result['utile'].count('data-explain=') == 1
    assert result['utile'].count('>Détails<') == 1
    assert result['drawer'] is not None
    assert result['drawer']['body'].count('<h3') == 1
    assert 'Pourquoi cela compte' in result['drawer']['body']
    assert 'Ce signal change la décision.' in result['drawer']['body']
    assert '—' not in result['drawer']['body']


def test_donut_agrege_la_queue_dans_autres_sans_perdre_le_total():
    result = _node_chart_probe(r"""
let captured = null;
VXCharts.mount = (_canvas, config) => { captured = config; return config; };
const labels = ['A','B','C','D','E','F','G'];
const values = [10,20,30,40,5,6,7];
const labelsBefore = labels.slice();
const valuesBefore = values.slice();
VXCharts.donut({}, labels, values, {});
console.log(JSON.stringify({
  labels: captured.data.labels,
  values: captured.data.datasets[0].data,
  colors: captured.data.datasets[0].backgroundColor,
  neutral: VXCharts.colors.neutral,
  labelsInput: labels,
  valuesInput: values,
  labelsBefore,
  valuesBefore,
}));
""")

    assert result['labels'] == ['A', 'B', 'C', 'D', 'Autres']
    assert result['values'] == [10, 20, 30, 40, 18]
    assert sum(result['values']) == sum(result['valuesInput']) == 118
    assert result['colors'][-1] == result['neutral']
    assert result['labelsInput'] == result['labelsBefore']
    assert result['valuesInput'] == result['valuesBefore']


def test_barres_horizontales_appliquent_valuefmt_sur_l_axe_et_les_valeurs():
    result = _node_chart_probe(r"""
VXCharts.mount = (_canvas, config) => config;
const fmt = value => '€' + Number(value).toFixed(1);
const config = VXCharts.bars({}, ['A','B'], [1.25,-2.5], {
  horizontal:true, valueFmt:fmt, xTitle:'Valeur', yTitle:'Catégorie'
});
const painted = [];
const ctx = {
  save(){}, restore(){}, beginPath(){}, roundRect(){}, fill(){},
  measureText(){ return {width:24}; }, fillText(text){ painted.push(text); },
};
config.plugins[0].afterDatasetsDraw({
  ctx,
  chartArea:{left:0,right:300,top:0,bottom:180},
  getDatasetMeta(){return {data:[{x:80,y:40},{x:120,y:90}]};},
});
console.log(JSON.stringify({
  indexAxis: config.options.indexAxis,
  xTick: config.options.scales.x.ticks.callback(1.25),
  yHasFormatter: typeof config.options.scales.y.ticks.callback === 'function',
  tooltip: config.options.plugins.tooltip.callbacks.label({parsed:{x:-2.5,y:999}}),
  painted,
  xTitle: config.options.scales.x.title,
  yTitle: config.options.scales.y.title,
}));
""")

    assert result['indexAxis'] == 'y'
    assert result['xTick'] == '€1.3'
    assert result['yHasFormatter'] is False
    assert result['tooltip'] == '€-2.5'
    assert '€-2.5' in result['painted']
    assert result['xTitle'] == {'display': True, 'text': 'Valeur'}
    assert result['yTitle'] == {'display': True, 'text': 'Catégorie'}


def test_heatmap_garde_une_encre_stable_et_expose_son_echelle():
    result = _node_chart_probe(r"""
const host = {
  html:'', classList:{add(){}},
  set innerHTML(value){this.html=value;}, get innerHTML(){return this.html;},
  querySelectorAll(){return [];},
};
VXCharts.heatmapCard(host, {
  title:'Stabilité', min:-2, max:2,
  fmt:value => Number(value).toFixed(1) + ' %',
  rows:[{label:'Ligne', cells:[
    {value:-2}, {value:0}, {value:2}, {value:null,label:'n/d'}
  ]}],
});
console.log(JSON.stringify({html:host.html}));
""", heatmap=True)

    html = result['html']
    assert html.count('color:var(--vx-text-primary)') == 3
    assert html.count('color:var(--vx-text-muted)') == 1
    assert 'color:rgba(' not in html
    assert 'class="vx-heatmap-scale"' in html
    assert 'aria-label="Échelle de couleur, de -2.0 % à 2.0 %"' in html
    for label in ('>-2.0 %<', '>0.0 %<', '>2.0 %<'):
        assert label in html

    css = _read(CHARTS_CSS)
    assert '.vx-heatmap-scale' in css
    assert 'linear-gradient(90deg,var(--vx-negative),var(--vx-surface-elevated))' in css
    assert 'linear-gradient(90deg,var(--vx-surface-elevated),var(--vx-positive))' in css


def test_aucun_hover_global_ne_fait_bouger_une_carte_inerte():
    offenders = []
    css_root = ROOT / 'vertex/static/vertex/css'
    for path in sorted(css_root.glob('*.css')):
        source = _strip_css_comments(_read(path))
        for match in re.finditer(r'([^{}]+)\{', source):
            for selector in _split_top_level_commas(match.group(1)):
                compact = re.sub(r'\s+', '', selector)
                # Le pseudo-état doit porter sur le même composé que la carte,
                # pas sur un enfant arbitraire situé plus loin dans le sélecteur.
                if not re.search(r'\.vx-(?:card(?:--[\w-]+)?|kpi)[^\s>+~]*:hover', compact):
                    continue
                interactive = (
                    ':is(a,button,[role="button"],[data-clickable])' in compact
                    or '[data-clickable]' in compact
                    or '.vx-interactive' in compact
                    or re.search(r'(?:^|[^\w-])(?:a|button)\.vx-card', compact)
                    or re.search(r'\.vx-card[^\s>+~]*\[role=[\'\"]button[\'\"]\]', compact)
                )
                if not interactive:
                    offenders.append('%s : %s' % (path.name, selector.strip()))

    assert not offenders, (
        'hover global appliqué à des cartes/KPI potentiellement inertes :\n  ' +
        '\n  '.join(offenders)
    )
