"""vertex.ui.pages.markets_page — l'espace Marchés (§23).

Question : « Dans quel environnement la stratégie opère-t-elle ? »
Sous-vues (param ?view=) : overview · macro · sectors · breadth · volatility.

Le module Python ne fait AUCUN calcul financier : il assemble le squelette
HTML + le script client ; toutes les données viennent des moteurs via
VX.fetch (/scan, /api/market/regime, /cal-feed, /api/market/summary).
Donnée absente → VX.states.empty honnête, jamais un chiffre inventé.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

# Sous-vues canoniques (ordre = ordre des onglets).
_VIEWS = (
    ('overview', 'Vue d’ensemble'),
    ('macro', 'Macro'),
    ('sectors', 'Secteurs'),
    ('breadth', 'Breadth'),
    ('volatility', 'Volatilité'),
)


def _tabs(view: str) -> str:
    """Barre d'onglets — navigation par URL (?view=…), pas d'état JS."""
    items = []
    for vid, label in _VIEWS:
        sel = 'true' if vid == view else 'false'
        items.append(f'<a class="vx-tab" role="tab" href="?view={vid}" '
                     f'aria-selected="{sel}" data-view-tab="{vid}">{label}</a>')
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Marchés">'
            + ''.join(items) + '</nav>')


_HEADER = """
<div class="vx-page-header">
  <div><h1>Marchés</h1>
  <div class="vx-sub">Dans quel environnement la stratégie opère-t-elle ?</div></div>
</div>
%%TABS%%
<div id="vx-demo-banner"></div>
"""

# ── Squelettes par sous-vue ──────────────────────────────────────────────
_VIEW_CONTENT = {
    'overview': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-4" id="vx-mk-regime" aria-label="Régime de marché">
    <div class="vx-card-header"><span class="vx-card-title">Régime de marché</span></div>
    <div id="vx-mk-regime-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" id="vx-mk-leader" aria-label="Leadership sectoriel">
    <div class="vx-card-header"><span class="vx-card-title">Leadership sectoriel</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=sectors">Secteurs →</a></span></div>
    <div id="vx-mk-leader-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" id="vx-mk-risk" aria-label="Risque du jour">
    <div class="vx-card-header"><span class="vx-card-title">Risque du jour</span></div>
    <div id="vx-mk-risk-body">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4" id="vx-mk-strip" aria-label="Indices et cross-asset"></div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-12" id="vx-mk-spy"></div>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-12" id="vx-mk-multi"></div>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Top 10 hausses">
    <div class="vx-card-header"><span class="vx-card-title">Top 10 — plus fortes hausses</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=stocks">Univers →</a></span></div>
    <div id="vx-mk-top"></div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Flop 10 baisses">
    <div class="vx-card-header"><span class="vx-card-title">Flop 10 — plus fortes baisses</span></div>
    <div id="vx-mk-flop"></div>
  </section>
</div>
""",
    'macro': """
<div class="vx-grid vx-mt3" id="vx-mk-macro-kpis" aria-label="Indicateurs macro"></div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-7" id="vx-mk-yield"></div>
  <section class="vx-card vx-col-5" aria-label="Limites des données macro">
    <div class="vx-card-header"><span class="vx-card-title">Limites des données</span></div>
    <div class="vx-insight">Courbe tracée sur les <b>4 maturités réelles</b> du scan
    (3M · 5A · 10A · 30A). Les maturités intermédiaires (2A/7A/20A) ne sont pas fournies
    par les moteurs — non affichées plutôt qu’inventées.</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-12" id="vx-mk-macro-cal"></div>
</div>
""",
    'sectors': """
<div class="vx-grid vx-mt3">
  <div class="vx-col-7" id="vx-mk-sectors-chart"></div>
  <section class="vx-card vx-col-5" aria-label="Leaders par secteur">
    <div class="vx-card-header"><span class="vx-card-title">Leaders par secteur</span></div>
    <div id="vx-mk-sectors-leaders">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-12" id="vx-mk-sectors-heat"></div>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-12" id="vx-mk-rotation"></div>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Poids et performance par secteur">
    <div class="vx-chart-head"><span class="vx-chart-title">Poids &amp; performance par secteur</span>
      <span class="vx-chart-question">Où se concentre l’univers, et qui performe ?</span></div>
    <div id="vx-mk-sectors-tree" style="height:300px"></div>
    <div class="vx-card-foot"><span class="vx-meta">Taille = nombre de titres scannés du secteur · couleur = variation moyenne du jour (vert entrant / rouge sortant).</span></div>
  </section>
</div>
""",
    'breadth': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-5 vx-card--accent" aria-label="Participation du marché">
    <div class="vx-card-header"><span class="vx-card-title">Participation du marché</span></div>
    <div id="vx-mk-breadth-gauge">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-7" aria-label="Détail de la participation">
    <div class="vx-card-header"><span class="vx-card-title">Détail — au-dessus des moyennes</span></div>
    <div id="vx-mk-breadth-detail">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-7" id="vx-mk-breadth-chart"></div>
  <div class="vx-col-5" id="vx-mk-verdicts"></div>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-5" id="vx-mk-internals-card" aria-label="Internals du marché" hidden>
    <div class="vx-card-header"><span class="vx-card-title">Internals — participation mesurée</span></div>
    <div id="vx-mk-internals"></div>
  </section>
  <section class="vx-card vx-col-7" id="vx-mk-dist-card" aria-label="Distribution des scores" hidden>
    <div class="vx-chart-head"><span class="vx-chart-title">Distribution des scores de l’univers</span>
      <span class="vx-chart-question">Le marché est-il globalement fort ou faible ?</span></div>
    <div id="vx-mk-dist"></div>
    <div class="vx-card-foot"><span class="vx-meta">Nombre de titres par tranche de score Vertex (0-100). Décalage à droite = univers globalement fort.</span></div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" id="vx-mk-health-card" aria-label="Composition de la santé du marché" hidden>
    <div class="vx-chart-head"><span class="vx-chart-title">Composition de la santé du marché</span>
      <span class="vx-chart-question">D’où vient le score de santé ?</span></div>
    <div id="vx-mk-health-wf" style="height:240px"></div>
    <div class="vx-card-foot"><span class="vx-meta">Santé = 30&nbsp;% (&gt;MM50) + 25&nbsp;% (&gt;MM200) + 25&nbsp;% (breadth) + 20&nbsp;% (avancées/déclins). Contributions pondérées du moteur d’internals — aucune pondération inventée.</span></div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Limites des données de breadth">
    <div class="vx-insight">Breadth, participation (&gt;MM50/MM200), avancées/déclins,
    nouveaux hauts/bas et distribution des scores sont calculés sur l’<b>univers des leaders
    scannés</b> (univers partiel, pas l’ensemble du NYSE). Advance/decline cumulés
    multi-séances ne sont pas fournis — non affichés plutôt qu’inventés.</div>
  </section>
</div>
""",
    'volatility': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-6 vx-card--accent" id="vx-mk-vix" aria-label="VIX">
    <div class="vx-card-header"><span class="vx-card-title">VIX — volatilité implicite du marché</span></div>
    <div id="vx-mk-vix-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6 vx-card--accent" aria-label="Contexte de volatilité">
    <div class="vx-card-header"><span class="vx-card-title">Contexte — régime &amp; participation</span></div>
    <div class="vx-flex vx-wrap" style="gap:1rem;align-items:flex-start">
      <div id="vx-mk-vol-regime" style="flex:1;min-width:150px">%%LOADING%%</div>
      <div id="vx-mk-vol-breadth" style="flex:1;min-width:150px"></div>
    </div>
    <div id="vx-mk-vol-rail" class="vx-mt3"></div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Volatilité implicite par symbole">
    <div class="vx-card-header"><span class="vx-card-title">IV par symbole</span></div>
    <div class="vx-insight">La term structure de volatilité implicite par symbole est
    disponible dans la fiche analyse de chaque titre (onglet Options). Cette vue
    couvre la volatilité de marché (VIX) et le contexte de régime fournis par le moteur.</div>
    <div class="vx-mt3"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/analysis">Ouvrir une fiche analyse →</a></div>
  </section>
</div>
""",
}

_JS = r"""
<script src="/static/vertex/js/charts/line-area-chart.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script src="/static/vertex/js/charts/breadth-chart.js" defer></script>
<script src="/static/vertex/js/charts/sector-chart.js" defer></script>
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
<script src="/static/vertex/js/charts/donut-chart.js" defer></script>
<script src="/static/vertex/js/charts/timeline-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW='%%VIEW%%';
const $=(id)=>document.getElementById(id);
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function modeOf(scan){return scan&&scan.data_source==='demo'?'fallback':(scan&&scan.source==='ibkr'?'live':'delayed');}
function mkt(scan){return (scan&&(scan.market||scan.market_ctx))||{};}
async function getScan(){try{return await VX.fetch('/scan',{ttl:120000});}catch(e){return null;}}
function demoBanner(scan){
  if(scan&&scan.data_source==='demo'&&$('vx-demo-banner'))
    $('vx-demo-banner').innerHTML='<div class="vx-demo-banner"><span class="vx-badge-demo">Démo</span> Données synthétiques clairement identifiées — jamais présentées comme réelles.</div>';
}
function emptyCard(host,reason,action){
  const el=$(host);if(el)el.innerHTML='<div class="vx-card">'+VX.states.empty(reason,action||'')+'</div>';
}
const SCAN_ACTION='<a class="vx-btn vx-btn-sm" href="/system?view=data">Système / Données</a>';

/* ═══ OVERVIEW ═══ */
async function loadRegime(){
  try{
    const r=await VX.fetch('/api/market/regime',{ttl:120000});
    const adj=r.adjustments||{};
    const conf=Math.round((r.confidence||0)*100);
    $('vx-mk-regime-body').innerHTML=
      `<div id="vx-mk-regime-gauge" class="vx-mb2"></div>
      <div class="vx-kpi vx-mb3" style="text-align:center"><span class="vx-kpi-value" style="font-size:22px" data-regime="${esc(r.regime)}">${esc(r.regime)}</span>
       <span class="vx-kpi-delta vx-muted">${(r.dimensions_used||[]).length} dimensions évaluées</span></div>
      <div class="vx-kv"><span class="k">Nouveau risque</span><span class="v ${adj.new_risk_allowed?'vx-pos':'vx-neg'}">${adj.new_risk_allowed?'autorisé':'BLOQUÉ'}</span></div>
      <div class="vx-kv"><span class="k">Priorité setups</span><span class="v">${VX.fmt.nd(esc(adj.setup_priority))}</span></div>
      <div class="vx-kv"><span class="k">Confirmations exigées</span><span class="v">${VX.fmt.nd(esc(adj.confirmation_required))}</span></div>
      <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'Moteur de régimes','delayed')}</div>`;
    if(window.VXCharts&&VXCharts.gauge){
      const reading=conf>=70?'Signal net — régime lisible':conf>=40?'Signal modéré — confirmations utiles':'Signal faible — prudence accrue';
      VXCharts.gauge('vx-mk-regime-gauge',{value:conf,min:0,max:100,unit:' %',label:'confiance',reading:reading,
        bands:[{to:40,color:VXCharts.colors.negative},{to:70,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.positive}]});
    }
  }catch(e){$('vx-mk-regime-body').innerHTML=VX.states.error('Régime indisponible');}
}
function moversRows(rows,dir){
  const sorted=(rows||[]).filter(r=>r.change!==null&&r.change!==undefined).slice()
    .sort((a,b)=>dir==='top'?(b.change-a.change):(a.change-b.change)).slice(0,10);
  if(!sorted.length)return VX.states.empty('Aucune variation exploitable dans le dernier scan.');
  return sorted.map(function(r){const chg=r.change;
    return `<div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">
      <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.symbol}">${r.symbol}</button>
      <span class="vx-num vx-mono ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}" style="width:62px;text-align:right;font-weight:700">${VX.fmt.pct(chg,1)}</span>
      <span class="vx-grow vx-truncate vx-dim" style="font-size:11.5px">${esc(r.sector||'')}</span>
      <span class="vx-num vx-mono vx-meta" style="width:64px;text-align:right">${r.price!==null&&r.price!==undefined?VX.fmt.price(r.price):''}</span>
      ${r.score!==null&&r.score!==undefined?`<span class="vx-badge" title="Score Vertex">${VX.fmt.num(r.score,0)}</span>`:''}
      <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${r.symbol}" aria-label="Actions ${r.symbol}">⋯</button></div>`;}).join('');
}
function loadMovers(scan){
  const rows=(scan&&scan.rows)||[];
  const t=$('vx-mk-top'),f=$('vx-mk-flop');
  const foot=`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))} · ${rows.length} titres scannés</div>`;
  if(t)t.innerHTML=moversRows(rows,'top')+foot;
  if(f)f.innerHTML=moversRows(rows,'flop')+foot;
}
function loadLeader(scan){
  const sectors=(scan&&scan.sectors)||[];
  if(!sectors.length||typeof sectors[0]!=='object'){
    $('vx-mk-leader-body').innerHTML=VX.states.empty('Secteurs non calculés par le dernier scan.',SCAN_ACTION);return;
  }
  const top=sectors[0];
  const topLeader=top.leader&&(top.leader.symbol||((typeof top.leader==='string')?top.leader:null));
  $('vx-mk-leader-body').innerHTML=
    `<div class="vx-kpi vx-mb3"><span class="vx-kpi-value" style="font-size:20px">${esc(top.sector||'n/d')}</span>
     <span class="vx-kpi-delta vx-muted">score moyen ${VX.fmt.nd(top.avg_score)}</span></div>`
    +(topLeader?`<div class="vx-kv"><span class="k">Titre leader</span><span class="v">
      <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(topLeader)}">${esc(topLeader)}</button>
      <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${esc(topLeader)}" aria-label="Actions ${esc(topLeader)}">⋯</button></span></div>`:'')
    +`<div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.source||'scan',modeOf(scan))}</div>`;
}
function loadRisk(scan){
  const m=mkt(scan);
  if(!m.verdict&&!m.roro){
    $('vx-mk-risk-body').innerHTML=VX.states.empty('Verdict marché non calculé — lancer un scan.',SCAN_ACTION);return;
  }
  $('vx-mk-risk-body').innerHTML=
    (m.verdict?`<div style="font-size:14px;line-height:1.7">${esc(m.verdict)}</div>`:'')
    +(m.roro?`<div class="vx-kv vx-mt2"><span class="k">Risk-on / risk-off</span><span class="v">${esc(m.roro)}</span></div>`:'')
    +(m.spy_regime?`<div class="vx-kv"><span class="k">Régime S&amp;P 500</span><span class="v">${esc(m.spy_regime)}</span></div>`:'')
    +`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))}</div>`;
}
const IDX=['S&P 500','Nasdaq','Dow Jones','Russell 2000','Taux 10 ans','DXY','Pétrole','Or','Bitcoin'];
function idxByName(scan){
  const list=(scan&&Array.isArray(scan.indices))?scan.indices:[];
  const by={};list.forEach(i=>{if(i&&i.name)by[i.name]=i;});return by;
}
function sparkSvg(vals,pos){
  if(!Array.isArray(vals)||vals.length<2)return '';
  const w=100,h=22,mn=Math.min.apply(null,vals),mx=Math.max.apply(null,vals),rng=(mx-mn)||1;
  const pts=vals.map((v,i)=>(i/(vals.length-1)*w).toFixed(1)+','+(h-((v-mn)/rng)*(h-2)-1).toFixed(1)).join(' ');
  const col=pos?'var(--vx-positive,#39b878)':'var(--vx-negative,#dc6255)';
  return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" width="100%" height="22" style="margin-top:5px;display:block" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/></svg>`;
}
function kpiCell(label,d,scan,extraNote){
  const val=d&&(d.last??d.price??d.close);const chg=d?d.change:null;
  return `<div class="vx-card vx-kpi" style="grid-column:span 4" aria-label="${esc(label)}">
    <span class="vx-kpi-label">${esc(label)}</span>
    <span class="vx-kpi-value" style="font-size:19px">${(val===null||val===undefined)?'—':VX.fmt.price(val)}</span>
    <span class="vx-kpi-delta ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}">${(chg===null||chg===undefined)?'n/d':VX.fmt.pct(chg)}</span>
    ${(d&&d.series)?sparkSvg(d.series,(chg==null?true:chg>=0)):''}
    ${extraNote?`<span class="vx-meta">${extraNote}</span>`:''}
    ${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))}</div>`;
}
function loadStrip(scan){
  const by=idxByName(scan);
  const known=IDX.filter(n=>by[n]&&(by[n].price!==null&&by[n].price!==undefined));
  if(!known.length){
    $('vx-mk-strip').innerHTML='<div class="vx-card vx-col-12">'+VX.states.empty('Indices indisponibles — lancer un scan depuis Système.',SCAN_ACTION)+'</div>';return;
  }
  $('vx-mk-strip').innerHTML=known.map(label=>{
    const i=by[label];
    return kpiCell(label,{last:i.price,change:i.change,series:i.spark},scan).replace('grid-column:span 4','grid-column:span 3');
  }).join('');
}
/* Comparaison multi-indices : chaque série rebasée à 0 % (transformation
   d'affichage des séries fournies — aucun point inventé). */
function loadMultiIndex(scan){
  const by=idxByName(scan);
  const wanted=['S&P 500','Nasdaq','Dow Jones','Russell 2000'];
  const sets=wanted.map(n=>({n,spark:(by[n]&&by[n].spark)||[]})).filter(x=>x.spark.length>5);
  if(!sets.length){emptyCard('vx-mk-multi','Séries indices indisponibles dans le dernier scan.',SCAN_ACTION);return;}
  const len=Math.min(...sets.map(x=>x.spark.length));
  const labels=Array.from({length:len},(_,i)=>i-len);
  window.VXCharts.card('vx-mk-multi',{
    title:'Indices — performance comparée',timeframe:len+' points',
    question:'Qui mène : large caps, tech ou small caps ?',
    conclusion:'Chaque indice rebasé à 0 % en début de fenêtre.',
    height:240,source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
    legend:wanted.map((n,i)=>({label:n,color:VXCharts.colors.series[i%6]})),
    explain:{shows:'Les mêmes séries d’indices que le bandeau, rebasées à 0 % pour comparer la force relative.',
      why:'Le leadership (tech vs small caps) qualifie l’appétit pour le risque.',
      confirm:'Small caps et tech au-dessus des large caps — appétit confirmé.',
      invalidate:'Défensives seules en tête — régime prudent.'},
    render:(cv)=>VXCharts.multiLine(cv,labels,
      sets.map(x=>({label:x.n,data:x.spark.slice(-len).map(v=>x.spark[x.spark.length-len]?(v/x.spark[x.spark.length-len]-1)*100:0)})),
      {yFmt:(v)=>v.toFixed(1)+' %'})});
}
function loadSpyChart(scan){
  const det=(scan&&scan.detail)||{};
  const closes=(det.SPY&&det.SPY.series&&det.SPY.series.close)||[];
  const m=mkt(scan);
  if(closes.length>10){
    VXCharts.areaCard('vx-mk-spy',{
      title:'S&P 500 (SPY) — série de référence',timeframe:closes.length+' séances',
      question:'La tendance de fond reste-t-elle exploitable ?',
      conclusion:(m.spy_regime==='TREND'?'Tendance intacte':'Régime '+(m.spy_regime||'n/d'))+(m.verdict?' — '+m.verdict:''),
      labels:closes.map((_,i)=>i-closes.length),values:closes,height:260,
      source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
      explain:{shows:'Les clôtures de SPY telles que fournies par le scan (aucun indicateur recalculé côté UI).',
        why:'La Stratégie Vertex n’attaque qu’en environnement porteur : le régime module seuils et tailles.',
        confirm:'Clôtures au-dessus des dernières résistances avec breadth > 55 %.',
        invalidate:'Cassure des supports avec expansion de volatilité.'}});
  }else{
    emptyCard('vx-mk-spy','Série SPY indisponible — lancer un scan depuis Système.',SCAN_ACTION);
  }
}

/* ═══ MACRO ═══ */
const MACRO_NAMES=['Taux 10 ans','DXY','Pétrole','Or','Bitcoin'];
function loadMacroKpis(scan){
  const by=idxByName(scan);
  const known=MACRO_NAMES.filter(n=>by[n]&&by[n].price!==null&&by[n].price!==undefined);
  if(!known.length){
    $('vx-mk-macro-kpis').innerHTML='<div class="vx-card vx-col-12">'+VX.states.empty('Données macro non fournies par le scan (VIX et indices actions seulement) — rien d’inventé.',SCAN_ACTION)+'</div>';return;
  }
  $('vx-mk-macro-kpis').innerHTML=known.map(n=>kpiCell(n,{last:by[n].price,change:by[n].change},scan)).join('');
}
/* Courbe des taux US — 4 maturités RÉELLES du scan (jamais interpolées) */
function loadYield(scan){
  const el=document.getElementById('vx-mk-yield');if(!el||!window.VXCharts)return;
  const macro=(scan&&scan.macro)||[];const byId={};macro.forEach(m=>{byId[m.id]=m;});
  const mats=[['^IRX','3M'],['^FVX','5A'],['^TNX','10A'],['^TYX','30A']];
  const pts=mats.filter(m=>byId[m[0]]&&byId[m[0]].value!=null);
  if(pts.length<2){emptyCard('vx-mk-yield','Courbe des taux indisponible — maturités non fournies par le scan.',SCAN_ACTION);return;}
  const labels=pts.map(m=>m[1]);
  const cur=pts.map(m=>byId[m[0]].value);
  const prev=pts.map(m=>byId[m[0]].prev!=null?byId[m[0]].prev:byId[m[0]].value);
  const t10=byId['^TNX'],t3=byId['^IRX'];
  const spread=(t10&&t3&&t10.value!=null&&t3.value!=null)?(t10.value-t3.value):null;
  const cc=VXCharts.colors;
  VXCharts.card('vx-mk-yield',{
    title:'Courbe des taux US',timeframe:'clôture',
    question:'La courbe est-elle normale ou inversée ?',
    conclusion:spread!=null?('Spread 10a-3m '+(spread>=0?'+':'')+spread.toFixed(2)+' pt — '+(spread<0?'INVERSÉE (signal de récession)':'pentue / normale')):'—',
    height:250,source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
    limits:'4 maturités réelles (3M/5A/10A/30A)',
    legend:[{label:'Actuelle',color:cc.brand},{label:'Séance préc.',color:cc.neutral}],
    explain:{shows:'Le rendement du Trésor US par maturité (points réels du scan, non interpolés).',
      why:'Une courbe inversée (court > long) précède souvent les récessions et module l’appétit pour le risque.',
      confirm:'Repentification : le spread 10a-3m remonte durablement.',invalidate:'Inversion qui s’aggrave.'},
    render:(cv)=>VXCharts.multiLine(cv,labels,[
      {label:'Actuelle',data:cur,borderColor:cc.brand,borderWidth:2.2,pointRadius:3,pointBackgroundColor:cc.brand,fill:false},
      {label:'Séance préc.',data:prev,borderColor:cc.neutral,borderWidth:1.4,borderDash:[4,3],pointRadius:0,fill:false}
    ],{yFmt:(v)=>v+' %'})});
}
async function loadMacroCal(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const items=(cal.macro||[]).map(m=>({when:m.date,kind:m.kind||'Macro',
      label:esc(m.label||'')+(m.note?' — '+esc(m.note):'')+(m.dte!==undefined&&m.dte!==null?` (J-${m.dte})`:'')}));
    VXCharts.timelineCard('vx-mk-macro-cal',{title:'Calendrier macro',
      question:'Quels événements macro peuvent changer le régime ?',
      items,source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun événement macro fourni par le calendrier moteur.'});
  }catch(e){emptyCard('vx-mk-macro-cal','Calendrier macro indisponible ('+esc(e.message)+').');}
}

/* ═══ SECTORS ═══ */
function loadSectors(scan){
  const sectors=(scan&&scan.sectors)||[];
  if(!sectors.length){
    emptyCard('vx-mk-sectors-chart','Secteurs non calculés par le dernier scan.',SCAN_ACTION);
    VXCharts.heatmapCard('vx-mk-sectors-heat',{
    title:'Performance et momentum par secteur',
    question:'Quels secteurs attirent le capital aujourd’hui ?',
    conclusion:'Vert = flux entrant, rouge = flux sortant (variation moyenne du jour).',
    columns:['Var. moyenne %','Score','RVOL','Titres'],
    rows:sectors.map(sec=>({label:esc(sec.sector||'n/d'),cells:[
      {value:sec.avg_change??null,onclick:'/opportunities?view=stocks&sector='+encodeURIComponent(sec.sector||'')},
      {value:sec.avg_score??null,label:VX.fmt.nd(sec.avg_score)},
      {value:null,label:VX.fmt.nd(sec.avg_rvol)},
      {value:null,label:String(sec.n??'—')}]})),
    min:-3,max:3,fmt:(v)=>v===null?'—':VX.fmt.pct(v),
    source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
    limits:'univers = leaders scannés'});
  $('vx-mk-sectors-leaders').innerHTML=VX.states.empty('Secteurs non calculés par le dernier scan.');
    return;
  }
  VXCharts.sectorCard('vx-mk-sectors-chart',{
    title:'Rotation sectorielle',question:'Où va le capital en ce moment ?',
    conclusion:'Leader : '+(sectors[0].sector||'n/d')+' · cliquer un secteur pour voir ses opportunités',
    labels:sectors.map(s=>s.sector),values:sectors.map(s=>s.avg_score??s.score??0),height:Math.max(230,sectors.length*30),
    source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
    onSector:(name)=>{VX.context.save();location.href='/opportunities?view=stocks&sector='+encodeURIComponent(name);},
    explain:{shows:'Le score moyen par secteur calculé par le moteur de rotation.',
      why:'La stratégie suit les secteurs qui attirent le capital.',
      confirm:'Leadership stable sur plusieurs séances.',invalidate:'Rotation défensive brutale.'}});
  VXCharts.heatmapCard('vx-mk-sectors-heat',{
    title:'Performance et momentum par secteur',
    question:'Quels secteurs attirent le capital aujourd’hui ?',
    conclusion:'Vert = flux entrant, rouge = flux sortant (variation moyenne du jour).',
    columns:['Var. moyenne %','Score','RVOL','Titres'],
    rows:sectors.map(sec=>({label:esc(sec.sector||'n/d'),cells:[
      {value:sec.avg_change??null,onclick:'/opportunities?view=stocks&sector='+encodeURIComponent(sec.sector||'')},
      {value:sec.avg_score??null,label:VX.fmt.nd(sec.avg_score)},
      {value:null,label:VX.fmt.nd(sec.avg_rvol)},
      {value:null,label:String(sec.n??'—')}]})),
    min:-3,max:3,fmt:(v)=>v===null?'—':VX.fmt.pct(v),
    source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
    limits:'univers = leaders scannés'});
  $('vx-mk-sectors-leaders').innerHTML=
    `<table class="vx-table"><thead><tr><th>Secteur</th><th class="vx-num">Score</th><th>Leader</th><th></th></tr></thead><tbody>`
    +sectors.map(s=>{
      const L=s.leader&&(s.leader.symbol||((typeof s.leader==='string')?s.leader:null));
      return `<tr>
      <td><a href="/opportunities?view=stocks&sector=${encodeURIComponent(s.sector||'')}" onclick="VX.context.save()">${esc(s.sector||'n/d')}</a></td>
      <td class="vx-num vx-mono">${VX.fmt.nd(s.avg_score)}</td>
      <td>${L?`<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(L)}">${esc(L)}</button>`:'—'}</td>
      <td>${L?`<button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${esc(L)}" aria-label="Actions ${esc(L)}">⋯</button>`:''}</td>
    </tr>`;}).join('')+'</tbody></table>'
    +`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))}</div>`;
  /* Treemap poids & performance par secteur (type réutilisable) */
  if(window.VXCharts&&VXCharts.treemap){
    const cc=VXCharts.colors;
    const col=(ch)=>ch==null?cc.neutral:(ch>=0.3?cc.positive:ch<=-0.3?cc.negative:cc.warning);
    const el=document.getElementById('vx-mk-sectors-tree');
    const w=(el&&el.clientWidth)||900;
    VXCharts.treemap(el,{width:w,height:300,
      items:sectors.map(s=>({label:s.sector||'n/d',value:(s.n||s.avg_score||1),
        sub:(s.avg_change!=null?((s.avg_change>=0?'+':'')+Number(s.avg_change).toFixed(1)+'%'):''),
        color:col(s.avg_change)})),
      fmt:(v)=>v+' titres'});
  }
  /* Rotation sectorielle en quadrant (RRG-like) : force relative × momentum */
  if(window.VXCharts&&sectors.length>=2){
    const cc2=VXCharts.colors;
    const pts=sectors.map(s=>({x:(s.avg_score!=null?s.avg_score:(s.score||50)),y:(s.avg_change!=null?s.avg_change:0),label:s.sector||''}));
    const quadCol=(x,y)=>x>=50?(y>=0?cc2.positive:cc2.warning):(y>=0?cc2.info:cc2.negative);
    VXCharts.card('vx-mk-rotation',{
      title:'Rotation sectorielle — force relative × momentum',
      question:'Quels secteurs mènent, lesquels s’essoufflent ?',
      conclusion:'Haut-droit = Leaders (force + momentum) · bas-gauche = Retardataires — cliquer un secteur',
      height:360,source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
      limits:'force = score moyen · momentum = variation moyenne du jour (univers scanné)',
      explain:{shows:'Chaque secteur placé par sa force relative (score moyen) et son momentum (variation moyenne du jour).',
        why:'La stratégie surpondère la zone « Leading » (haut-droit) et se méfie du « Lagging » (bas-gauche).',
        confirm:'Un secteur qui migre vers le haut-droit sur plusieurs séances.',invalidate:'Bascule vers le bas-gauche.'},
      render:(cv)=>VXCharts.mount(cv,{type:'scatter',
        data:{datasets:[{data:pts,pointRadius:7,pointHoverRadius:11,
          pointBackgroundColor:(ctx)=>ctx.raw?quadCol(ctx.raw.x,ctx.raw.y):cc2.neutral,
          pointBorderColor:'rgba(255,255,255,.22)',pointBorderWidth:1}]},
        options:{scales:{
          x:{title:{display:true,text:'Force relative (score moyen) →'},min:0,max:100,grid:{color:'rgba(255,255,255,.06)'}},
          y:{title:{display:true,text:'Momentum (var. moy. %) ↑'},grid:{color:'rgba(255,255,255,.06)'}}},
          plugins:{tooltip:{callbacks:{label:(ctx)=>ctx.raw.label+' · force '+VX.fmt.num(ctx.raw.x,0)+' · momentum '+VX.fmt.pct(ctx.raw.y,1)}}},
          onClick:(evt,els,chart)=>{const p=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
            if(p.length){const d=chart.data.datasets[0].data[p[0].index];VX.context.save();location.href='/opportunities?view=stocks&sector='+encodeURIComponent(d.label);}}},
        plugins:[{id:'vxQuad',afterDatasetsDraw(chart){const a=chart.chartArea,sx=chart.scales.x,sy=chart.scales.y;const xc=sx.getPixelForValue(50),y0=sy.getPixelForValue(0);const g=chart.ctx;
          g.save();g.strokeStyle='rgba(255,255,255,.12)';g.setLineDash([4,4]);g.beginPath();
          if(xc>a.left&&xc<a.right){g.moveTo(xc,a.top);g.lineTo(xc,a.bottom);}
          if(y0>a.top&&y0<a.bottom){g.moveTo(a.left,y0);g.lineTo(a.right,y0);}g.stroke();g.setLineDash([]);
          g.font='10px sans-serif';g.fillStyle='rgba(255,255,255,.32)';
          g.fillText('LEADING',a.right-58,a.top+14);g.fillText('IMPROVING',a.left+6,a.top+14);
          g.fillText('WEAKENING',a.right-66,a.bottom-8);g.fillText('LAGGING',a.left+6,a.bottom-8);
          g.fillStyle='#bab4ac';g.font='9px sans-serif';
          chart.data.datasets[0].data.forEach((d,i)=>{const m=chart.getDatasetMeta(0).data[i];if(m)g.fillText(String(d.label).slice(0,11),m.x+9,m.y+3);});
          g.restore();}}]})});
  }
}

/* ═══ BREADTH ═══ */
async function loadBreadth(scan){
  const G=window.VXCharts&&VXCharts.gauge;const CO=(window.VXCharts&&VXCharts.colors)||{};
  /* breadth réelle = /api/market/summary.breadth (objet), pas scan.market. */
  let sum={};try{sum=await VX.fetch('/api/market/summary',{ttl:60000})||{};}catch(e){}
  const sb=sum.breadth;let brNum=null,bo=null;
  if(sb!=null&&typeof sb==='object'){bo=sb;brNum=(sb.above50!=null)?Number(sb.above50):(sb.above200!=null?Number(sb.above200):null);}
  else if(sb!=null&&!isNaN(sb))brNum=Number(sb);
  /* Jauge de participation (au-dessus de la MM50) */
  if(G&&brNum!=null){VXCharts.gauge('vx-mk-breadth-gauge',{value:brNum,min:0,max:100,unit:' %',label:'> MM50',
    reading:brNum>=55?'Participation saine — hausse partagée':brNum>=45?'Participation moyenne':'Participation étroite — sélectivité',
    bands:[{to:40,color:CO.negative},{to:55,color:CO.warning},{to:100,color:CO.positive}]});}
  else emptyCard('vx-mk-breadth-gauge','Participation non calculée par le dernier scan.',SCAN_ACTION);
  /* Détail : au-dessus des moyennes, avancées/déclins, nouveaux hauts/bas */
  const dEl=$('vx-mk-breadth-detail');
  if(dEl){
    if(bo){
      const kv=(k,v,cls)=>`<div class="vx-kv"><span class="k">${k}</span><span class="v vx-mono ${cls||''}">${v}</span></div>`;
      const pc=(v)=>v>=55?'vx-pos':v<=45?'vx-neg':'';
      dEl.innerHTML=
        (bo.above50!=null?kv('Titres > MM50',Math.round(bo.above50)+' %',pc(bo.above50)):'')
        +(bo.above200!=null?kv('Titres > MM200',Math.round(bo.above200)+' %',pc(bo.above200)):'')
        +((bo.adv!=null&&bo.dec!=null)?kv('Avancées / Déclins',bo.adv+' / '+bo.dec,bo.adv>=bo.dec?'vx-pos':'vx-neg'):'')
        +((bo.nh!=null&&bo.nl!=null)?kv('Nouveaux hauts / bas',bo.nh+' / '+bo.nl,bo.nh>=bo.nl?'vx-pos':'vx-neg'):'')
        +(bo.buy!=null?kv('Signaux d’achat (univers)',bo.buy):'')
        +`<div class="vx-help vx-mt2">Calculé sur l’univers des leaders scannés (partiel, pas tout le NYSE). Advance/decline cumulés multi-séances non fournis — non affichés plutôt qu’inventés.</div>`;
    }else dEl.innerHTML=VX.states.empty('Détail de participation non fourni par le dernier scan.');
  }
  const m=mkt(scan);
  if(brNum!==null){
    VXCharts.breadthCard('vx-mk-breadth-chart',{
      title:'Breadth / participation',question:'La hausse est-elle partagée ?',
      conclusion:brNum>=55?'Participation saine.':'Participation étroite — sélectivité obligatoire.',
      labels:['> moyenne'],values:[brNum],height:200,
      source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
      limits:'breadth calculée sur les leaders scannés (univers partiel)',
      explain:{shows:'Le pourcentage de titres au-dessus de leur moyenne (moteur de contexte marché).',
        why:'Une hausse portée par 3 titres est fragile ; la breadth qualifie le régime.',
        confirm:'Breadth > 60 % stable plusieurs séances.',invalidate:'Breadth < 40 % pendant que les indices montent.'}});
  }else emptyCard('vx-mk-breadth-chart','Breadth non calculée par le dernier scan.',SCAN_ACTION);
  const rows=(scan&&scan.rows)||[];
  const counts={};
  rows.forEach(r=>{const v=r.verdict||r.decision;if(v)counts[v]=(counts[v]||0)+1;});
  const top=Object.entries(counts).sort((a,b)=>b[1]-a[1]).slice(0,5);
  if(top.length){
    VXCharts.donutCard('vx-mk-verdicts',{
      title:'Répartition des verdicts du scan',question:'Le moteur trouve-t-il des dossiers ?',
      conclusion:top[0][0]+' domine ('+top[0][1]+' titre(s) sur '+rows.length+')',
      labels:top.map(x=>x[0]),values:top.map(x=>x[1]),height:200,
      source:(scan&&scan.source)||'scan',timestamp:scan&&(scan.scan_ts||scan.updated),mode:modeOf(scan),
      explain:{shows:'Le décompte des verdicts moteur sur l’univers scanné (max 5 catégories).',
        why:'Beaucoup d’ÉVITER = environnement hostile même si les indices tiennent.',
        confirm:'Verdicts d’achat en hausse sur plusieurs scans.',invalidate:'Bascule massive vers ÉVITER.'}});
  }else emptyCard('vx-mk-verdicts','Aucun verdict dans le dernier scan.',SCAN_ACTION);
  /* Waterfall : composition de la santé du marché (contributions pondérées de l'internals) */
  const inter=(scan&&scan.internals)||{};
  const card=$('vx-mk-health-card');
  if(card&&window.VXCharts&&VXCharts.waterfall&&inter.health!=null&&inter.pct_a50!=null){
    card.hidden=false;
    VXCharts.waterfall('vx-mk-health-wf',{ariaLabel:'Composition de la santé du marché',
      items:[
        {label:'>MM50',value:0.30*(inter.pct_a50||0)},
        {label:'>MM200',value:0.25*(inter.pct_a200||0)},
        {label:'Breadth',value:0.25*(inter.breadth!=null?inter.breadth:(brNum||0))},
        {label:'Adv/Déc',value:0.20*(inter.advpct||0)},
        {label:'Santé',value:inter.health,isTotal:true}],
      fmt:(v)=>Math.round(v)});
  }else if(card){card.hidden=true;}
  loadBreadthInternals(scan);
}
function loadBreadthInternals(scan){
  const inter=(scan&&scan.internals)||{};
  const iCard=$('vx-mk-internals-card'),dCard=$('vx-mk-dist-card');
  if(!inter||inter.pct_a50===null||inter.pct_a50===undefined){if(iCard)iCard.hidden=true;if(dCard)dCard.hidden=true;return;}
  if(iCard)iCard.hidden=false;
  const kvr=(k,v,cls)=>`<div class="vx-kv"><span class="k">${k}</span><span class="v vx-mono ${cls||''}">${v}</span></div>`;
  const pos=(v)=>v>=55?'vx-pos':v<=45?'vx-neg':'';
  $('vx-mk-internals').innerHTML=
    kvr('% au-dessus MM50',inter.pct_a50+' %',pos(inter.pct_a50))
    +kvr('% au-dessus MM200',inter.pct_a200+' %',pos(inter.pct_a200))
    +kvr('Avancées / déclins',inter.advpct+' % en hausse',pos(inter.advpct))
    +kvr('Nouveaux plus-hauts (52s)',VX.fmt.nd(inter.nh),inter.nh>inter.nl?'vx-pos':'')
    +kvr('Nouveaux plus-bas (52s)',VX.fmt.nd(inter.nl),inter.nl>inter.nh?'vx-neg':'')
    +(inter.avg_rsi!==null&&inter.avg_rsi!==undefined?kvr('RSI moyen univers',inter.avg_rsi):'')
    +`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))} · univers scanné</div>`;
  const dist=inter.dist||[];
  if(dCard&&dist.length&&window.VXCharts){dCard.hidden=false;
    const maxN=Math.max(1,...dist);const cc=VXCharts.colors;
    const bar=(n,i)=>{const h=Math.round(n/maxN*100);
      const col=i>=7?cc.positive:i<=2?cc.negative:cc.warning;
      return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px" role="img" aria-label="score ${i*10} à ${i*10+10} : ${n} titres">
        <span style="width:100%;height:120px;display:flex;align-items:flex-end"><span style="width:100%;height:${h}%;background:${col};border-radius:3px 3px 0 0;min-height:2px"></span></span>
        <span style="font-size:9px;color:var(--vx-text-muted,#817b73);font-variant-numeric:tabular-nums">${i*10}</span></div>`;};
    $('vx-mk-dist').innerHTML='<div style="display:flex;gap:3px;align-items:flex-end;padding:6px 2px">'+dist.map(bar).join('')+'</div>';
  }else if(dCard){dCard.hidden=true;}
}

/* ═══ VOLATILITY ═══ (cockpit : jauge VIX + rail calme↔stress + régime/participation)
   Source RÉELLE = /api/market/summary (scan.market ne porte que la session). */
async function loadVix(scan){
  const G=window.VXCharts&&VXCharts.gauge;const CO=(window.VXCharts&&VXCharts.colors)||{};
  let sum={};try{sum=await VX.fetch('/api/market/summary',{ttl:60000})||{};}catch(e){}
  let vix=(sum.vix!=null&&!isNaN(sum.vix))?Number(sum.vix):null;
  if(vix==null){const vi=((scan&&scan.indices)||[]).find(i=>i&&i.name==='VIX');if(vi&&vi.price!=null)vix=Number(vi.price);}
  const chg=(sum.vix_chg!==undefined)?sum.vix_chg:null;
  const band=sum.vix_band||mkt(scan).vix_band;
  if(vix==null){
    $('vx-mk-vix-body').innerHTML=VX.states.empty('VIX non fourni par le dernier scan.',SCAN_ACTION);
  }else{
    $('vx-mk-vix-body').innerHTML=
      `<div id="vx-mk-vix-gauge" class="vx-mb2"></div>`
      +(chg!==null&&chg!==undefined?`<div class="vx-kv"><span class="k">Variation</span><span class="v ${chg>0?'vx-neg':chg<0?'vx-pos':'vx-muted'}">${VX.fmt.pct(chg)} vs hier</span></div>`:'')
      +(band?`<div class="vx-kv"><span class="k">Bande</span><span class="v">${esc(band)}</span></div>`:'')
      /* Rail calme ↔ stress : VIX 10→40 projeté sur 0→100 % */
      +`<div class="vx-stat-xl-label vx-mt3">Calme ↔ Stress</div>`
      +`<div class="vx-rail vx-rail--stress vx-mt2" style="--vx-rail-pos:${Math.max(0,Math.min(100,(vix-10)/30*100)).toFixed(0)}%"><span class="vx-rail-mark"></span></div>`
      +`<div class="vx-rail-scale"><span>10</span><span>25</span><span>40+</span></div>`
      +`<div class="vx-help vx-mt2">Un VIX bas comprime les primes d’options ; un VIX en expansion invalide les entrées agressives.</div>`
      +`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))}</div>`;
    if(G){
      const reading=vix<15?'Volatilité comprimée — primes d’options bon marché':vix<25?'Volatilité élevée — prudence sur les entrées':'Stress — expansion de volatilité';
      VXCharts.gauge('vx-mk-vix-gauge',{value:vix,min:0,max:50,label:'VIX',reading:reading,
        bands:[{to:15,color:CO.positive},{to:25,color:CO.warning},{to:50,color:CO.negative}]});
    }
  }
  /* Contexte : jauge participation (breadth) + jauge régime */
  let br=null;const sb=sum.breadth;
  if(sb!=null&&typeof sb==='object')br=(sb.above50!=null)?Number(sb.above50):(sb.above200!=null?Number(sb.above200):null);
  else if(sb!=null&&!isNaN(sb))br=Number(sb);
  if(G&&br!=null){VXCharts.gauge('vx-mk-vol-breadth',{value:br,min:0,max:100,unit:' %',label:'Breadth',
    reading:br>=55?'Participation saine':'Étroite',
    bands:[{to:40,color:CO.negative},{to:55,color:CO.warning},{to:100,color:CO.positive}]});}
  else if($('vx-mk-vol-breadth'))$('vx-mk-vol-breadth').innerHTML=VX.states.empty('Breadth non calculée.');
  try{
    const r=await VX.fetch('/api/market/regime',{ttl:120000});
    const conf=Math.round((r.confidence||0)*100);
    const allowed=r.adjustments&&r.adjustments.new_risk_allowed;
    if(G){VXCharts.gauge('vx-mk-vol-regime',{value:conf,min:0,max:100,unit:' %',label:esc(r.regime||'Régime'),
      reading:allowed?'Risque autorisé':'Risque bloqué',
      bands:[{to:40,color:CO.negative},{to:70,color:CO.warning},{to:100,color:CO.positive}]});}
    const pos=allowed?Math.max(55,conf):Math.min(45,100-conf);
    if($('vx-mk-vol-rail'))$('vx-mk-vol-rail').innerHTML=
      '<div class="vx-stat-xl-label">Positionnement — Défense ↔ Attaque</div>'
      +'<div class="vx-rail vx-mt2" style="--vx-rail-pos:'+pos+'%"><span class="vx-rail-mark"></span></div>'
      +'<div class="vx-rail-scale"><span>Défense</span><span>Neutre</span><span>Attaque</span></div>'
      +'<div class="vx-meta vx-mt2">Régime <b>'+esc(r.regime||'n/d')+'</b> · '
      +(allowed?'<span class="vx-pos">nouveau risque autorisé</span>':'<span class="vx-neg">nouveau risque BLOQUÉ</span>')+'</div>';
  }catch(e){if($('vx-mk-vol-regime'))$('vx-mk-vol-regime').innerHTML=VX.states.empty('Régime non calculé.');}
}

/* ═══ Orchestration ═══ */
async function boot(){
  const scan=await getScan();
  demoBanner(scan);
  if(VIEW==='overview'){loadRegime();loadLeader(scan||{});loadRisk(scan);loadStrip(scan);loadSpyChart(scan);loadMultiIndex(scan);loadMovers(scan);}
  else if(VIEW==='macro'){loadMacroKpis(scan);loadYield(scan);loadMacroCal();}
  else if(VIEW==='sectors'){loadSectors(scan);}
  else if(VIEW==='breadth'){loadBreadth(scan);}
  else if(VIEW==='volatility'){loadVix(scan);}
}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}
whenChartsReady(boot);
VX.bus.on('vx:data-refreshed',boot);
})();
</script>
"""


def render(view: str = 'overview') -> str:
    """Assemble la page Marchés pour la sous-vue demandée (URL = état)."""
    if view not in dict(_VIEWS):
        view = 'overview'
    label = dict(_VIEWS)[view]
    content = (_HEADER.replace('%%TABS%%', _tabs(view))
               + _VIEW_CONTENT[view]).replace(
        '%%LOADING%%', '<div class="vx-skeleton" style="height:60px"></div>')
    page_js = _JS.replace('%%VIEW%%', view)
    return render_shell(title='Marchés', active='markets', space_label='Marchés',
                        sub_label=label, content=content, page_js=page_js,
                        page_label='Marchés')
