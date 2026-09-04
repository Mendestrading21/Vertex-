"""LOT 620 — grammaire institutionnelle du socle VXCharts.

Ces gardiens exécutent les builders dans Node avec un Chart.js minimal. Ils
verrouillent les contrats réellement produits : densités, interactions selon
le type, toucher, reduced-motion, axes mobiles, crosshair borné et heatmap
accessible. Ils ne testent ni un goût visuel ni les données financières.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / 'vertex/static/vertex/css/charts.css'
CORE = ROOT / 'vertex/static/vertex/js/charts/chart-core.js'
HEATMAP = ROOT / 'vertex/static/vertex/js/charts/heatmap.js'
THEME = ROOT / 'vertex/static/vertex/js/charts/chart-theme-black-glass.js'


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def _node(body: str, *, mobile: bool = False, reduced: bool = False,
          heatmap: bool = False) -> dict:
    prelude = r"""
const fs = require('fs');
const vm = require('vm');
global.window = global;
global.document = {
  documentElement: {},
  addEventListener() {},
  querySelectorAll() { return []; },
  createElement() { return {width:0,height:0,getContext(){return {};}}; },
};
global.getComputedStyle = () => ({getPropertyValue(token) {
  return token === '--vx-font-mono' ? 'JetBrains Mono' : 'Inter';
}});
const MOBILE = %s;
const REDUCED = %s;
global.matchMedia = query => ({matches:
  (REDUCED && query.includes('prefers-reduced-motion')) ||
  (MOBILE && (query.includes('max-width: 520px') || query.includes('max-width: 768px')))
});
const chartConfigs = [];
function Chart(_ctx, config) { this.config = config; this.destroy = () => {}; chartConfigs.push(config); }
Chart.defaults = {
  font: {}, plugins: {legend: {labels: {}}, tooltip: {}}, scale: {title: {}}, animation: {},
};
Chart.getChart = () => null;
global.Chart = Chart;
window.VX = {
  fmt: {
    ago(value) { return value ? 'Il y a 1 min' : '—'; },
    num(value, digits) { return Number(value).toFixed(digits == null ? 1 : digits); },
    price(value) { return String(value); },
  },
  states: {loading() { return '<span>chargement</span>'; }},
  updateIndicator(timestamp, source, mode) {
    return '<span class="vx-update">' + (source || 'source') + ' · ' + (mode || 'live') + '</span>';
  },
  shell: {openDrawer() {}},
};
vm.runInThisContext(fs.readFileSync('vertex/static/vertex/js/charts/chart-theme-black-glass.js', 'utf8'), {filename:'theme.js'});
vm.runInThisContext(fs.readFileSync('vertex/static/vertex/js/charts/chart-core.js', 'utf8'), {filename:'chart-core.js'});
""" % ('true' if mobile else 'false', 'true' if reduced else 'false')
    if heatmap:
        prelude += "\nvm.runInThisContext(fs.readFileSync('vertex/static/vertex/js/charts/heatmap.js', 'utf8'), {filename:'heatmap.js'});\n"
    run = subprocess.run(
        ['node', '-e', prelude + '\n' + body], cwd=ROOT,
        text=True, encoding='utf-8', capture_output=True, check=False,
    )
    assert run.returncode == 0, run.stderr
    lines = [line for line in run.stdout.splitlines() if line.strip()]
    assert lines, 'sonde Node muette'
    return json.loads(lines[-1])


def test_quatre_densites_ont_des_hauteurs_bornees_et_responsives():
    css = _read(CSS)
    core = _read(CORE)
    desktop = {'micro': 72, 'compact': 176, 'standard': 240, 'hero': 360}
    for name, height in desktop.items():
        assert re.search(
            r'\.vx-chart-card\.vx-chart-size-%s\{--vx-chart-height:%dpx\}' %
            (name, height), css
        )
    assert 'C.sizes = Object.freeze({ micro: 72, compact: 176, standard: 240, hero: 360 })' in core
    assert 'height:var(--vx-chart-height)' in css
    assert 'max-width:100%' in css
    assert 'overflow:hidden' in css
    assert 'touch-action:pan-y' in css
    # Sur mobile, le hero reste expressif mais ne monopolise pas l'écran.
    assert '.vx-chart-card.vx-chart-size-hero{--vx-chart-height:268px}' in css


def test_chart_shell_applique_la_variante_et_relations_accessibles():
    result = _node(r"""
const classes = [];
const attrs = {};
const host = {
  html: '', classList: {add(...values){classes.push(...values);}, remove(){}},
  setAttribute(name, value){attrs[name]=value;},
  set innerHTML(value){this.html=value;}, get innerHTML(){return this.html;},
  querySelector(selector){
    if (selector === 'canvas') return null;
    return null;
  },
};
VXCharts.card(host, {
  title:'Participation', conclusion:'La participation progresse.', summary:'Résumé <fiable>',
  variant:'hero', timeframe:'1 mois', unit:'%', freshness:'live',
  source:'Moteur marché', timestamp:'2026-08-12T08:00:00Z', mode:'live'
});
console.log(JSON.stringify({html:host.html, classes, attrs}));
""")
    assert 'vx-chart-size-hero' in result['classes']
    assert result['attrs']['data-chart-size'] == 'hero'
    html = result['html']
    # La hauteur de variante reste pilotée par CSS pour réagir aux breakpoints.
    assert '--vx-chart-height:' not in html
    assert '<h3 class="vx-chart-title"' in html
    assert 'aria-labelledby="vxch-' in html and 'aria-describedby="vxch-' in html
    assert 'Résumé &lt;fiable&gt;' in html
    assert 'vx-chart-provenance' in html and 'Moteur marché' in html


def test_interactions_sont_index_pour_lignes_nearest_pour_formes_et_tactiles():
    result = _node(r"""
const canvas = () => ({getContext(){return {};}});
const line = VXCharts.area(canvas(), ['J1','J2'], [1,2], {last:false,crosshair:false});
const bars = VXCharts.bars(canvas(), ['A','B'], [1,-1], {});
const donut = VXCharts.donut(canvas(), ['A','B'], [60,40], {});
console.log(JSON.stringify({
  line: line.config.options.interaction,
  bars: bars.config.options.interaction,
  donut: donut.config.options.interaction,
  lineEvents: line.config.options.events,
  defaults: {
    events: Chart.defaults.events,
    tooltipBackground: Chart.defaults.plugins.tooltip.backgroundColor,
    tooltipBorder: Chart.defaults.plugins.tooltip.borderColor,
    tooltipBodyFont: Chart.defaults.plugins.tooltip.bodyFont,
    normalized: Chart.defaults.normalized
  }
}));
""")
    assert result['line'] == {'mode': 'index', 'intersect': False, 'axis': 'x'}
    assert result['bars'] == {'mode': 'nearest', 'intersect': False}
    assert result['donut'] == {'mode': 'nearest', 'intersect': True}
    for events in (result['lineEvents'], result['defaults']['events']):
        assert 'touchstart' in events and 'touchmove' in events
    assert result['defaults']['tooltipBackground'] == '#141619'
    assert result['defaults']['tooltipBorder'] == 'rgba(200,194,188,.20)'
    assert result['defaults']['tooltipBodyFont']['family'] == 'JetBrains Mono'
    assert result['defaults']['normalized'] is True


def test_axes_mobiles_reduisent_les_ticks_sans_casser_le_contrat_des_titres():
    result = _node(r"""
const axes = VXCharts.axes({xTitle:'Période', yTitle:'Valeur'});
console.log(JSON.stringify({
  xTicks:axes.x.ticks.maxTicksLimit, yTicks:axes.y.ticks.maxTicksLimit,
  xGrid:axes.x.grid.display, yGrid:axes.y.grid.display,
  xTitle:axes.x.title, yTitle:axes.y.title,
  xBorder:axes.x.border.display, yBorder:axes.y.border.display
}));
""", mobile=True)
    assert result['xTicks'] == result['yTicks'] == 4
    assert result['xGrid'] is False and result['yGrid'] is True
    assert result['xTitle'] == {'display': True, 'text': 'Période'}
    assert result['yTitle'] == {'display': True, 'text': 'Valeur'}
    assert result['xBorder'] is False and result['yBorder'] is False


def test_crosshair_neutre_reste_borne_et_absent_sans_point_actif():
    result = _node(r"""
const moves=[], lines=[], dashes=[], strokes=[];
const ctx = {
  save(){}, restore(){}, beginPath(){}, rect(){}, clip(){}, arc(){}, fill(){},
  setLineDash(value){dashes.push(value);},
  moveTo(x,y){moves.push([x,y]);}, lineTo(x,y){lines.push([x,y]);},
  stroke(){strokes.push(this.strokeStyle);}
};
const plugin = VXCharts.crosshairPlugin(VXCharts.colors.brand);
const chart = {
  ctx, chartArea:{left:10,right:90,top:5,bottom:70},
  data:{datasets:[{borderColor:VXCharts.colors.brand}]},
  tooltip:{opacity:1,getActiveElements(){return [{datasetIndex:0,element:{x:50,y:30}}];}}
};
plugin.afterDatasetsDraw(chart);
chart.tooltip.getActiveElements=()=>[];
plugin.afterDatasetsDraw(chart);
console.log(JSON.stringify({moves,lines,dashes,strokes,crosshair:VXCharts.colors.crosshair}));
""")
    assert result['moves'] == [[50, 5]]
    assert result['lines'] == [[50, 70]]
    assert result['strokes'] == [result['crosshair']]
    assert result['dashes'][0] == [2, 3]


def test_traits_temporels_sont_exacts_et_les_remplissages_retenus():
    src = _read(CORE)
    spark = src[src.index('C.sparkline ='):src.index('C.glowPlugin =')]
    area = src[src.index('C.area ='):src.index('C.bars =')]
    multiline = src[src.index('C.multiLine ='):src.index('C.levelLines =')]
    assert 'tension: 0' in spark and 'tension: 0' in area and 'tension: 0' in multiline
    assert 'glow = false' in area
    assert "color + '59'" not in area
    assert "color + '2E'" in area and "color + '00'" in area
    bars = src[src.index('C.bars ='):src.index('C.donut =')]
    assert 'createLinearGradient' not in bars
    assert "c + 'B8'" in bars


def test_reduced_motion_coupe_chartjs_et_les_transitions_css():
    result = _node(r"""
const canvas = {getContext(){return {};}};
const chart = VXCharts.area(canvas, ['A','B'], [1,2], {last:false,crosshair:false});
console.log(JSON.stringify({defaults:Chart.defaults.animation, mounted:chart.config.options.animation}));
""", reduced=True)
    assert result == {'defaults': False, 'mounted': False}
    css = _read(CSS)
    assert '@media (prefers-reduced-motion:reduce)' in css
    assert 'animation:none!important' in css and 'transition:none!important' in css


def test_heatmap_est_scrollable_semantique_et_ne_transforme_pas_nd_en_zero():
    result = _node(r"""
const host = {
  html:'', classList:{add(){}},
  set innerHTML(value){this.html=value;}, get innerHTML(){return this.html;},
  querySelectorAll(){return [];},
};
VXCharts.heatmapCard(host, {
  title:'Corrélations', question:'Quels liens dominent ?', conclusion:'Une relation ressort.',
  columns:['AAPL','Vide','Booléen','<MSFT>'], min:-1, max:1, source:'Moteur corrélation', mode:'live',
  rows:[{label:'Tech & IA', cells:[
    {value:null}, {value:[]}, {value:false}, {value:0.84,onclick:'/analysis/MSFT'}
  ]}]
});
console.log(JSON.stringify({html:host.html}));
""", heatmap=True)
    html = result['html']
    assert 'class="vx-heatmap-scroll"' in html
    assert 'role="region"' in html and 'tabindex="0"' in html
    assert '<th scope="col">&lt;MSFT&gt;</th>' in html
    assert '<th scope="row">Tech &amp; IA</th>' in html
    assert 'class="vx-num vx-heatmap-cell"' in html
    assert html.count('>n/d</td>') == 3 and '>0.0</td>' not in html
    assert 'role="link" tabindex="0"' in html
    assert 'aria-label="Tech &amp; IA, AAPL : n/d"' in html
    assert '<caption class="vx-sr-only">Une relation ressort.</caption>' in html
    assert 'role="img" aria-label="Échelle de couleur, de -1.0 à 1.0"' in html
    assert 'vx-chart-provenance' in html and 'Moteur corrélation' in html
    assert 'linear-gradient(135deg' not in html


def test_theme_garde_palette_metier_et_infrastructure_neutre_separees():
    theme = _read(THEME)
    assert "crosshair: 'rgba(200,194,188,.30)'" in theme
    assert "backgroundColor: '#141619'" in theme
    assert "titleColor: '#F5F3F0'" in theme
    assert "bodyColor: '#C8C2BC'" in theme
    # Aucun effet infrastructurel ne rejoint le tableau des séries financières.
    series = re.search(r'series\s*:\s*\[([^\]]+)\]', theme, re.S)
    assert series and 'rgba(' not in series.group(1)
