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
""",
    'macro': """
<div class="vx-grid vx-mt3" id="vx-mk-macro-kpis" aria-label="Indicateurs macro"></div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-7" id="vx-mk-macro-cal"></div>
  <section class="vx-card vx-col-5" aria-label="Limites des données macro">
    <div class="vx-card-header"><span class="vx-card-title">Limites des données</span></div>
    <div class="vx-insight">La courbe des taux complète n’est pas fournie par les
    moteurs — seul le taux 10 ans est disponible via le scan. Aucune autre maturité
    n’est affichée plutôt que d’inventer des points de courbe.</div>
  </section>
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
""",
    'breadth': """
<div class="vx-grid vx-mt3">
  <div class="vx-col-7" id="vx-mk-breadth-chart"></div>
  <div class="vx-col-5" id="vx-mk-verdicts"></div>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Limites des données de breadth">
    <div class="vx-insight">Advance/decline et nouveaux hauts/bas ne sont pas fournis
    par les moteurs — non affichés. La breadth ci-dessus est calculée sur l’univers
    des leaders scannés (univers partiel).</div>
  </section>
</div>
""",
    'volatility': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-6" id="vx-mk-vix" aria-label="VIX">
    <div class="vx-card-header"><span class="vx-card-title">VIX — volatilité implicite du marché</span></div>
    <div id="vx-mk-vix-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Volatilité implicite par symbole">
    <div class="vx-card-header"><span class="vx-card-title">IV par symbole</span></div>
    <div class="vx-insight">La term structure de volatilité implicite par symbole est
    disponible dans la fiche analyse de chaque titre (onglet Options). Cette vue ne
    couvre que la volatilité de marché (VIX) fournie par le moteur de contexte.</div>
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
    $('vx-mk-regime-body').innerHTML=
      `<div class="vx-kpi vx-mb3"><span class="vx-kpi-value" style="font-size:24px" data-regime="${esc(r.regime)}">${esc(r.regime)}</span>
       <span class="vx-kpi-delta vx-muted">confiance ${VX.fmt.num((r.confidence||0)*100,0)} % · ${(r.dimensions_used||[]).length} dimensions</span></div>
      <div class="vx-kv"><span class="k">Nouveau risque</span><span class="v ${adj.new_risk_allowed?'vx-pos':'vx-neg'}">${adj.new_risk_allowed?'autorisé':'BLOQUÉ'}</span></div>
      <div class="vx-kv"><span class="k">Priorité setups</span><span class="v">${VX.fmt.nd(esc(adj.setup_priority))}</span></div>
      <div class="vx-kv"><span class="k">Confirmations exigées</span><span class="v">${VX.fmt.nd(esc(adj.confirmation_required))}</span></div>
      <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'Moteur de régimes','delayed')}</div>`;
  }catch(e){$('vx-mk-regime-body').innerHTML=VX.states.error('Régime indisponible');}
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
function kpiCell(label,d,scan,extraNote){
  const val=d&&(d.last??d.price??d.close);const chg=d?d.change:null;
  return `<div class="vx-card vx-kpi" style="grid-column:span 4" aria-label="${esc(label)}">
    <span class="vx-kpi-label">${esc(label)}</span>
    <span class="vx-kpi-value" style="font-size:19px">${(val===null||val===undefined)?'—':VX.fmt.price(val)}</span>
    <span class="vx-kpi-delta ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}">${(chg===null||chg===undefined)?'n/d':VX.fmt.pct(chg)}</span>
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
    return kpiCell(label,{last:i.price,change:i.change},scan).replace('grid-column:span 4','grid-column:span 3');
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
}

/* ═══ BREADTH ═══ */
function loadBreadth(scan){
  const m=mkt(scan);
  if(m.breadth!==null&&m.breadth!==undefined){
    VXCharts.breadthCard('vx-mk-breadth-chart',{
      title:'Breadth / participation',question:'La hausse est-elle partagée ?',
      conclusion:m.breadth>=55?'Participation saine.':'Participation étroite — sélectivité obligatoire.',
      labels:['> moyenne'],values:[m.breadth],height:200,
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
}

/* ═══ VOLATILITY ═══ */
async function loadVix(scan){
  const m=mkt(scan);
  let chg=null;
  try{const sum=await VX.fetch('/api/market/summary',{ttl:60000});if(sum&&sum.vix_chg!==undefined)chg=sum.vix_chg;}catch(e){}
  if(m.vix===null||m.vix===undefined){
    $('vx-mk-vix-body').innerHTML=VX.states.empty('VIX non fourni par le dernier scan.',SCAN_ACTION);return;
  }
  $('vx-mk-vix-body').innerHTML=
    `<div id="vx-mk-vix-gauge" class="vx-mb2"></div>`
    +(chg!==null&&chg!==undefined?`<div class="vx-kv"><span class="k">Variation</span><span class="v ${chg>0?'vx-neg':chg<0?'vx-pos':'vx-muted'}">${VX.fmt.pct(chg)} vs hier</span></div>`:'')
    +(m.vix_band?`<div class="vx-kv"><span class="k">Bande</span><span class="v">${esc(m.vix_band)}</span></div>`:'')
    +`<div class="vx-help vx-mt2">Un VIX bas comprime les primes d’options ; un VIX en expansion invalide les entrées agressives.</div>`
    +`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',modeOf(scan))}</div>`;
  if(window.VXCharts&&VXCharts.gauge){
    const reading=m.vix<15?'Volatilité comprimée — primes d’options bon marché':m.vix<25?'Volatilité élevée — prudence sur les entrées':'Stress — expansion de volatilité';
    VXCharts.gauge('vx-mk-vix-gauge',{value:m.vix,min:0,max:50,label:'VIX',reading:reading,
      bands:[{to:15,color:VXCharts.colors.positive},{to:25,color:VXCharts.colors.warning},{to:50,color:VXCharts.colors.negative}]});
  }
}

/* ═══ Orchestration ═══ */
async function boot(){
  const scan=await getScan();
  demoBanner(scan);
  if(VIEW==='overview'){loadRegime();loadLeader(scan||{});loadRisk(scan);loadStrip(scan);loadSpyChart(scan);loadMultiIndex(scan);}
  else if(VIEW==='macro'){loadMacroKpis(scan);loadMacroCal();}
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
