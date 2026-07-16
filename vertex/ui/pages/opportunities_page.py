"""vertex.ui.pages.opportunities_page — le SCREENER complet (§24+).

Question : « Quelles opportunités méritent réellement une analyse ? »
La page passe de 515 titres scannés à UNE décision : filtres globaux
(verdict, secteur, score, proba de gain, gain/risque, volume relatif,
véhicule), graphiques qui montrent le POURQUOI (scatter avantage × proba,
distribution live, secteurs des résultats), top cartes, table triable.
Sous-vues : screener · options · portefeuille · anomalies · calendrier.
Données réelles uniquement — « — » honnête si absent.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell

_VIEWS = (('screener', 'Screener'), ('options', 'Options'),
          ('portfolio', 'Portefeuille'), ('anomalies', 'Anomalies'),
          ('calendar', 'Calendrier'))

# Anciennes vues → nouvelles (liens internes historiques : radar/stocks)
_VIEW_ALIASES = {'radar': 'screener', 'stocks': 'screener'}


def _tabs(view: str) -> str:
    return ('<div class="vx-tabs" role="tablist">'
            + ''.join(f'<a class="vx-tab" role="tab" aria-selected='
                      f'"{"true" if v == view else "false"}" '
                      f'href="/opportunities?view={v}">{label}</a>'
                      for v, label in _VIEWS) + '</div>')


_CONTENT = """
<div class="vx-page-header"><div><h1>Opportunités</h1>
<div class="vx-sub">Quelles opportunités méritent réellement une analyse ?</div></div>
<div class="vx-actions"><button class="vx-btn vx-btn-sm"
  onclick="VXEntities.openAddModal()">+ Ajouter</button></div></div>
%%TABS%%
<style>
  /* Barre de filtres du screener : collante, lisible, réactive */
  .vx-screenbar{position:sticky;top:calc(var(--vx-topbar-h) + 2px);z-index:14;
    display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;padding:10px 12px;
    margin-top:12px;border:1px solid var(--vx-border,#26221e);border-radius:12px;
    background:color-mix(in srgb,var(--vx-surface-1,#141513) 92%,transparent);
    backdrop-filter:blur(6px)}
  .vx-screenbar .vx-chip[aria-pressed="true"]{border-color:var(--vx-brand);color:var(--vx-brand-strong,#a3ca42)}
  .vx-screenbar label.rng{display:flex;align-items:center;gap:6px;font-size:11px;
    color:var(--vx-text-dim,#817d77)}
  .vx-screenbar label.rng input[type=range]{width:86px;accent-color:var(--vx-brand,#84aa31)}
  .vx-screenbar label.rng b{font-variant-numeric:tabular-nums;min-width:30px;color:var(--vx-text-secondary)}
  /* KPI du screener */
  .vx-scr-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:12px}
  .vx-scr-kpis .k{padding:11px 13px;border-radius:11px;background:var(--vx-surface-0,#0d100e);
    border:1px solid var(--vx-border,#26221e)}
  .vx-scr-kpis .k b{display:block;font:800 21px/1.15 var(--vx-font-mono,monospace);color:var(--vx-text-primary,#f2f5f1)}
  .vx-scr-kpis .k span{font-size:10.5px;color:var(--vx-text-dim,#817d77);text-transform:uppercase;letter-spacing:.05em}
  /* Table triable */
  th[data-sort]{cursor:pointer;user-select:none;white-space:nowrap}
  th[data-sort]:hover{color:var(--vx-brand,#84aa31)}
  th[data-sort][data-dir="desc"]::after{content:" ↓";color:var(--vx-brand)}
  th[data-sort][data-dir="asc"]::after{content:" ↑";color:var(--vx-brand)}
  /* Rail 52 semaines dans la table */
  .vx-rail52{display:inline-block;width:56px;height:5px;border-radius:99px;
    background:var(--vx-surface-0);position:relative;vertical-align:middle}
  .vx-rail52 i{position:absolute;top:-2px;width:8px;height:8px;margin-left:-4px;
    border-radius:99px;background:var(--vx-beige,#c0b79f)}
  /* Mobile : la barre de filtres (haute une fois empilée) ne reste pas collante */
  @media (max-width:760px){.vx-screenbar{position:static}}
</style>
<div id="op-body" class="vx-mt3">%%LOADING%%</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/timeline-chart.js" defer></script>
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
<script src="/static/vertex/js/charts/option-payoff.js" defer></script>
<script src="/static/vertex/js/charts/option-scenarios.js" defer></script>
<script src="/static/vertex/js/charts/option-theta.js" defer></script>
<script src="/static/vertex/js/charts/option-iv-sensitivity.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script src="/static/vertex/js/charts/sector-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW=%%VIEW%%;const PARAMS=%%PARAMS%%;
const $=(id)=>document.getElementById(id);
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function pbText(r){const p=r&&r.playbook;
  const s=(p&&typeof p==='object')?(p.name||p.desc||''):(typeof p==='string'?p:'');
  return s||(r&&typeof r.profile==='string'?r.profile:'');}
function pbIcon(r){const p=r&&r.playbook;return (p&&typeof p==='object'&&p.ic)?p.ic:'';}
function verdictDir(v){return (v==='BUY'||v==='ACHETER')?'up':(v==='AVOID'||v==='ÉVITER')?'down':'flat';}
function verdictWord(v){return (v==='BUY'||v==='ACHETER')?'Achat':(v==='AVOID'||v==='ÉVITER')?'Éviter':'Suivi';}
const VERD_FR={BUY:'ACHAT',WATCH:'SURVEILLER',WAIT:'ATTENDRE',AVOID:'ÉVITER'};
function heatCell(val,opts){
  opts=opts||{};
  if(val===null||val===undefined||val===''||isNaN(val))return `<td class="vx-num" data-label="${opts.label||''}">—</td>`;
  const max=opts.max||100;const w=Math.max(4,Math.min(100,Math.abs(val)/max*100));
  const col=(opts.good!=null)?(val>=opts.good?'var(--vx-positive)':val>=(opts.mid||0)?'var(--vx-warning)':'var(--vx-negative)'):'var(--vx-brand)';
  const disp=opts.fmt?opts.fmt(val):VX.fmt.num(val,0);
  return `<td class="vx-num" data-label="${opts.label||''}"><span style="display:inline-flex;align-items:center;gap:7px;justify-content:flex-end">`
    +`<span style="flex:0 0 40px;height:6px;border-radius:99px;background:var(--vx-surface-0);position:relative;overflow:hidden">`
    +`<i style="position:absolute;left:0;top:0;bottom:0;width:${w}%;background:${col};border-radius:99px"></i></span>`
    +`<b class="vx-mono" style="min-width:26px;font-weight:600">${disp}</b></span></td>`;
}
const OUT=['Actionnable','Proche','À surveiller','Radar','Rejetée'];
function bucketOf(r){
  if(r.verdict==='AVOID'||r.verdict==='ÉVITER')return'Rejetée';
  if((r.rr_ok&&r.score>=72&&(r.verdict==='BUY'||r.verdict==='ACHETER')))return'Actionnable';
  if(r.score>=66)return'Proche';
  if(r.score>=56)return'À surveiller';
  return'Radar';
}
function metaMode(scan){return scan&&scan.data_source==='demo'?'fallback':'delayed';}
function demoBanner(scan){return scan&&scan.data_source==='demo'?
  '<div class="vx-stale-banner">Mode DÉMO — données synthétiques, clairement identifiées.</div>':'';}
function rowActions(sym){return `<div class="vx-row-actions">
  <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${sym}">Analyse</button>
  <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${sym}" aria-label="Actions ${sym}">⋯</button></div>`;}
function sparkMini(closes){
  const v=(closes||[]).filter(x=>x!=null&&isFinite(x)).slice(-60);
  if(v.length<8)return '';
  const w=120,h=26,mn=Math.min.apply(null,v),mx=Math.max.apply(null,v),rng=(mx-mn)||1;
  const pts=v.map((x,i)=>(i/(v.length-1)*w).toFixed(1)+','+(h-1-((x-mn)/rng)*(h-2)).toFixed(1)).join(' ');
  const up=v[v.length-1]>=v[0];
  const col=up?'var(--vx-positive)':'var(--vx-negative)';
  return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" width="100%" height="26" style="display:block;margin-top:6px" aria-hidden="true">
    <polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/></svg>`;
}
function dimStrip(r){
  const dims=[['C','Conviction',r.st_conf,0],['M','Momentum',r.st_mom,0],['T','Technique',r.st_tech,0],
              ['F','Fondamental',r.st_fund,0],['R','Risque',r.st_risk,1]];
  if(!dims.some(d=>d[2]!=null))return '';
  return `<div style="display:flex;gap:5px;align-items:flex-end;margin-top:8px" role="img" aria-label="dimensions du score">`
    +dims.map(d=>{const v=d[2];
      const lvl=v==null?null:(d[3]?100-v:v);
      const col=lvl==null?'var(--vx-surface-4)':lvl>=67?'var(--vx-positive)':lvl>=40?'var(--vx-warning)':'var(--vx-negative)';
      const hh=v==null?4:Math.max(4,Math.round(v/100*24));
      return `<span title="${d[1]} : ${v==null?'n/d':Math.round(v)}" style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px">
        <span style="display:flex;align-items:flex-end;height:24px;width:100%"><i style="display:block;width:100%;height:${hh}px;border-radius:3px 3px 1px 1px;background:${col};opacity:${v==null?.35:.95}"></i></span>
        <b style="font:600 8.5px/1 var(--vx-font);color:var(--vx-text-faint)">${d[0]}</b></span>`;}).join('')+'</div>';
}
function rail52(v){
  if(v==null||isNaN(v))return '—';
  const p=Math.max(0,Math.min(100,v));
  return `<span class="vx-rail52" title="position dans la fourchette 52 semaines : ${Math.round(p)} %"><i style="left:${p}%"></i></span>`;
}

/* ═════════ SCREENER (vue par défaut) — de 515 titres à UNE décision ═════════ */
async function renderScreener(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>r.score!==undefined);
  if(!rows.length){$('op-body').innerHTML=VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
  const detail=scan.detail||{};
  const sectors=[...new Set(rows.map(r=>r.sector).filter(Boolean))].sort();

  /* État des filtres : URL (liens entrants) > localStorage > défauts. */
  let saved={};try{saved=JSON.parse(localStorage.getItem('vxScreenFilters')||'{}')}catch(e){}
  const state=Object.assign({bucket:'',sector:'',vehicle:'',setup:'',minScore:0,minPwin:0,minRR:0,minRvol:0},
    saved,{bucket:PARAMS.decision||saved.bucket||'',sector:PARAMS.sector||saved.sector||'',
           setup:(PARAMS.setup||saved.setup||'').toUpperCase()});
  function persist(){try{localStorage.setItem('vxScreenFilters',JSON.stringify(state))}catch(e){}}
  function filtered(){
    let f=rows;
    if(state.bucket)f=f.filter(r=>bucketOf(r)===state.bucket);
    if(state.sector)f=f.filter(r=>r.sector===state.sector);
    if(state.vehicle)f=f.filter(r=>String(r.vehicle||'').toUpperCase().includes(state.vehicle));
    if(state.setup)f=f.filter(r=>(pbText(r)||'').toUpperCase().includes(state.setup));
    if(state.minScore)f=f.filter(r=>(r.score||0)>=state.minScore);
    if(state.minPwin)f=f.filter(r=>((r.vx_pwin||0)*100)>=state.minPwin);
    if(state.minRR)f=f.filter(r=>(r.rr||0)>=state.minRR);
    if(state.minRvol)f=f.filter(r=>(r.rvol||0)>=state.minRvol);
    return f;
  }

  /* ── Squelette de la vue ── */
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-screenbar" role="group" aria-label="Filtres du screener">
      ${OUT.map(b=>`<button class="vx-chip" data-fk="bucket" data-fv="${b}" aria-pressed="${state.bucket===b}">${b}</button>`).join('')}
      <select class="vx-select" data-fk="sector" style="width:auto" aria-label="Secteur">
        <option value="">Tous secteurs</option>${sectors.map(s=>`<option ${state.sector===s?'selected':''}>${s}</option>`).join('')}</select>
      <select class="vx-select" data-fk="vehicle" style="width:auto" aria-label="Véhicule">
        <option value="">Action & option</option>
        <option value="ACTION" ${state.vehicle==='ACTION'?'selected':''}>Plutôt action</option>
        <option value="OPTION" ${state.vehicle==='OPTION'?'selected':''}>Plutôt option</option></select>
      <label class="rng">score ≥ <input type="range" data-fk="minScore" min="0" max="90" step="5" value="${state.minScore}"><b>${state.minScore||'0'}</b></label>
      <label class="rng">proba gain ≥ <input type="range" data-fk="minPwin" min="0" max="90" step="5" value="${state.minPwin}"><b>${state.minPwin||'0'}%</b></label>
      <label class="rng">gain/risque ≥ <input type="range" data-fk="minRR" min="0" max="4" step="0.5" value="${state.minRR}"><b>${state.minRR||'0'}×</b></label>
      <label class="rng">volume ≥ <input type="range" data-fk="minRvol" min="0" max="3" step="0.5" value="${state.minRvol}"><b>×${state.minRvol||'0'}</b></label>
      <input class="vx-input" data-fk="setup" style="width:130px" placeholder="setup (BREAKOUT…)" value="${esc(state.setup)}" aria-label="Setup">
      <button class="vx-btn vx-btn-sm vx-btn-ghost" id="op-reset">Réinitialiser</button>
      <span class="vx-meta vx-right" id="op-count"></span>
    </div>
    <div class="vx-scr-kpis" id="op-kpis" aria-label="Résumé des résultats"></div>
    <div class="vx-grid vx-mt4">
      <div class="vx-col-8" id="op-scatter"></div>
      <div class="vx-col-4">
        <div class="vx-card" id="op-sel-card"><div class="vx-card-header"><span class="vx-card-title">Sélection</span></div>
          <div id="op-radar-sel">${'<div class="vx-meta">Clique un point du nuage pour ouvrir son dossier express.</div>'}</div></div>
        <div id="op-funnel" class="vx-mt3"></div>
      </div>
    </div>
    <div class="vx-grid vx-mt4">
      <section class="vx-card vx-col-6" id="op-dist-card"><div class="vx-card-header">
        <span class="vx-card-title">Scores des résultats</span>
        <span class="vx-chart-question">Le filtre isole-t-il vraiment le haut du panier ?</span></div>
        <div id="op-dist"></div>
        <div class="vx-card-foot"><span class="vx-meta" id="op-dist-meta"></span></div></section>
      <div class="vx-col-6" id="op-sectors"></div>
    </div>
    <div id="op-topcards" class="vx-mt4"></div>
    <div class="vx-card vx-mt4"><div class="vx-card-header"><span class="vx-card-title">Tous les résultats</span>
      <span class="vx-chart-question">Trier par n’importe quelle colonne — cliquer une ligne ouvre la fiche.</span></div>
      <div class="vx-table-wrap vx-table-cards" id="op-table"></div>
      <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.source,metaMode(scan))}
        · <span id="op-table-count"></span> · tri : <span id="op-sort-label">score</span></div></div>`;

  /* ── KPI live ── */
  function paintKpis(f){
    const buys=f.filter(r=>r.verdict==='BUY'||r.verdict==='ACHETER').length;
    const avg=(arr)=>arr.length?arr.reduce((a,b)=>a+b,0)/arr.length:null;
    const avgScore=avg(f.map(r=>r.score).filter(x=>x!=null));
    const pwins=f.map(r=>r.vx_pwin).filter(x=>x!=null).map(x=>x*100);
    const avgPwin=avg(pwins);
    const bySec={};f.forEach(r=>{if(r.sector){(bySec[r.sector]=bySec[r.sector]||[]).push(r.score||0);}});
    const bestSec=Object.entries(bySec).map(([s,v])=>[s,avg(v)]).sort((a,b)=>b[1]-a[1])[0];
    $('op-kpis').innerHTML=
      `<div class="k"><b>${f.length}</b><span>titres retenus</span></div>`
      +`<div class="k"><b style="color:var(--vx-positive)">${buys}</b><span>signaux d’achat</span></div>`
      +`<div class="k"><b>${avgScore!=null?Math.round(avgScore):'—'}</b><span>score moyen</span></div>`
      +`<div class="k"><b>${avgPwin!=null?Math.round(avgPwin)+' %':'—'}</b><span>proba gain moyenne</span></div>`
      +`<div class="k"><b style="font-size:15px;line-height:1.4">${bestSec?esc(bestSec[0]):'—'}</b><span>secteur le mieux noté</span></div>`;
    $('op-count').textContent=f.length+' / '+rows.length+' titres';
  }

  /* ── Nuage POURQUOI : avantage statistique × proba de gain ── */
  let scatterChart=null;
  function paintScatter(f){
    const cc=VXCharts.colors;
    const pts=f.filter(r=>r.vx_edge!=null&&r.vx_pwin!=null).map(r=>({
      x:r.vx_edge,y:r.vx_pwin*100,sym:r.symbol,v:r.verdict,sector:r.sector||'',
      price:r.price,rr:r.rr,score:r.score,conv:r.st_conf,setup:pbText(r),
      r:4+Math.min(9,Math.max(0,(r.st_conf||50)-40)/6)}));
    const host=$('op-scatter');
    if(!pts.length){host.innerHTML='<div class="vx-card">'+VX.states.empty('Aucun titre du filtre ne porte à la fois un avantage (edge) et une proba de gain — élargis les filtres.')+'</div>';scatterChart=null;return;}
    const elite=pts.filter(p=>p.x>=60&&p.y>=60).length;
    VXCharts.card('op-scatter',{
      title:'Le POURQUOI en un regard — avantage × proba de gain',
      question:'Quels titres combinent un vrai avantage statistique ET une bonne proba de réussite ?',
      conclusion:elite+' titre(s) en zone ÉLITE (avantage ≥ 60 et proba ≥ 60 %)',
      height:320,source:scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
      limits:'avantage (edge 0-100) et proba de gain : moteur Vertex Monte-Carlo · taille de point = conviction',
      explain:{shows:'Chaque point est un titre filtré, placé par son avantage statistique (edge) et sa probabilité de gain simulée.',
        why:'Un bon dossier combine un avantage réel ET une proba favorable — l’un sans l’autre ne suffit pas.',
        confirm:'Un point qui migre vers le haut-droit en gardant sa conviction.',
        invalidate:'Proba qui retombe sous 50 % — le dossier perd son espérance.'},
      render:(cv)=>{scatterChart=VXCharts.mount(cv,{type:'scatter',
        data:{datasets:[{data:pts,
          pointRadius:(ctx)=>ctx.raw?ctx.raw.r:4,pointHoverRadius:(ctx)=>ctx.raw?ctx.raw.r+3:8,
          pointBackgroundColor:(ctx)=>{const v=ctx.raw&&ctx.raw.v;
            return v==='BUY'||v==='ACHETER'?cc.positive:(v==='AVOID'||v==='ÉVITER'?cc.negative:cc.neutral);},
          pointBorderColor:'rgba(255,255,255,.22)',pointBorderWidth:1}]},
        options:{scales:{
          x:{title:{display:true,text:'Avantage statistique (edge) →'},min:0,max:100,grid:{color:'rgba(255,255,255,.05)'}},
          y:{title:{display:true,text:'Proba de gain % ↑'},min:0,max:100,grid:{color:'rgba(255,255,255,.05)'}}},
          plugins:{tooltip:{callbacks:{label:(ctx)=>`${ctx.raw.sym} · avantage ${Math.round(ctx.raw.x)} · proba ${Math.round(ctx.raw.y)} % · score ${VX.fmt.nd(ctx.raw.score)}`}}},
          onClick:(evt,els,chart)=>{const p=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
            if(p.length)selectSym(chart.data.datasets[0].data[p[0].index]);}},
        plugins:[{id:'opZones',beforeDatasetsDraw(chart){
          const a=chart.chartArea,sx=chart.scales.x,sy=chart.scales.y,g=chart.ctx;
          const x60=sx.getPixelForValue(60),y60=sy.getPixelForValue(60),y50=sy.getPixelForValue(50);
          g.save();
          g.fillStyle='rgba(54,200,137,.055)';g.fillRect(x60,a.top,a.right-x60,y60-a.top);
          g.fillStyle='rgba(237,101,92,.045)';g.fillRect(a.left,y50,a.right-a.left,a.bottom-y50);
          g.strokeStyle='rgba(255,255,255,.10)';g.setLineDash([4,4]);g.beginPath();
          g.moveTo(x60,a.top);g.lineTo(x60,a.bottom);g.moveTo(a.left,y60);g.lineTo(a.right,y60);g.stroke();g.setLineDash([]);
          g.font='10px sans-serif';g.fillStyle='rgba(54,200,137,.55)';g.fillText('ZONE ÉLITE',a.right-70,a.top+14);
          g.fillStyle='rgba(237,101,92,.5)';g.fillText('proba défavorable',a.left+6,a.bottom-8);
          g.restore();}}]});return scatterChart;}});
  }
  function selectSym(d){
    $('op-radar-sel').innerHTML=
      `<div class="vx-flex"><span class="vx-ticker" style="font-size:16px">${esc(d.sym)}</span>${window.VXEntities?VXEntities.badges(d.sym):''}
         <span class="vx-badge vx-badge-decision vx-right" data-decision="${esc(d.v||'')}">${esc(VERD_FR[d.v]||d.v||'n/d')}</span></div>
       <div class="vx-kv vx-mt2"><span class="k">Avantage (edge)</span><span class="v vx-mono">${VX.fmt.nd(Math.round(d.x))} / 100</span></div>
       <div class="vx-kv"><span class="k">Proba de gain</span><span class="v vx-mono">${VX.fmt.nd(Math.round(d.y))} %</span></div>
       <div class="vx-kv"><span class="k">Score</span><span class="v vx-mono">${VX.fmt.nd(d.score)}</span></div>
       <div class="vx-kv"><span class="k">Cours</span><span class="v vx-mono">${d.price!=null?VX.fmt.price(d.price):'n/d'}</span></div>
       <div class="vx-kv"><span class="k">Gain/risque</span><span class="v vx-mono">${d.rr!=null?VX.fmt.num(d.rr,1)+'×':'n/d'}</span></div>
       ${d.setup?`<div class="vx-kv"><span class="k">Setup</span><span class="v">${esc(d.setup)}</span></div>`:''}
       ${d.sector?`<div class="vx-kv"><span class="k">Secteur</span><span class="v">${esc(d.sector)}</span></div>`:''}
       <div class="vx-flex vx-wrap vx-mt2" style="gap:.3rem">
         <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${esc(d.sym)}">Analyse</button>
         <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${esc(d.sym)}','follow')">Suivre</button>
         <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${esc(d.sym)}','alert')">Alerte</button>
         <a class="vx-btn vx-btn-sm" href="/options/${esc(d.sym)}">Options</a></div>`;
  }

  /* ── Distribution des scores (résultats filtrés) ── */
  function paintDist(f){
    const el=$('op-dist');if(!el)return;
    const dist=Array.from({length:10},()=>0);
    f.forEach(r=>{const sIdx=Math.max(0,Math.min(9,Math.floor((r.score||0)/10)));dist[sIdx]++;});
    const tot=f.length;
    if(!tot){el.innerHTML=VX.states.empty('Aucun résultat avec ces filtres.');$('op-dist-meta').textContent='';return;}
    const maxN=Math.max(1,...dist);
    el.innerHTML='<div style="display:flex;gap:4px;align-items:flex-end;padding:8px 2px">'+dist.map((n,i)=>{
      const hh=Math.round(n/maxN*100);
      const col=i>=7?'var(--vx-positive)':i<=2?'var(--vx-negative)':'var(--vx-warning)';
      return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px" role="img" aria-label="score ${i*10}-${i*10+10} : ${n} titres" title="${n} titre(s) entre ${i*10} et ${i*10+10}">
        <span style="font-size:9.5px;color:var(--vx-text-dim)">${n||''}</span>
        <span style="width:100%;height:110px;display:flex;align-items:flex-end"><span style="width:100%;height:${hh}%;background:${col};border-radius:3px 3px 0 0;min-height:2px;opacity:.85"></span></span>
        <span style="font-size:9px;color:var(--vx-text-muted);font-variant-numeric:tabular-nums">${i*10}</span></div>`;}).join('')+'</div>';
    const avg=Math.round(f.reduce((a,r)=>a+(r.score||0),0)/tot);
    $('op-dist-meta').textContent='score moyen des résultats : '+avg+' / 100 · '+tot+' titres';
  }

  /* ── Secteurs des résultats (score moyen par secteur, filtré) ── */
  function paintSectors(f){
    const host=$('op-sectors');if(!host)return;
    const by={};f.forEach(r=>{if(r.sector){(by[r.sector]=by[r.sector]||[]).push(r.score||0);}});
    const entries=Object.entries(by).map(([s,v])=>[s,Math.round(v.reduce((a,b)=>a+b,0)/v.length),v.length])
      .sort((a,b)=>b[1]-a[1]).slice(0,9);
    if(!entries.length){host.innerHTML='<div class="vx-card">'+VX.states.empty('Aucun secteur dans les résultats filtrés.')+'</div>';return;}
    VXCharts.sectorCard('op-sectors',{
      title:'Secteurs des résultats',question:'Où se concentrent les titres retenus par TES filtres ?',
      conclusion:entries[0][0]+' en tête ('+entries[0][1]+' de score moyen · '+entries[0][2]+' titres)',
      labels:entries.map(e=>e[0]+' ('+e[2]+')'),values:entries.map(e=>e[1]),height:240,
      source:scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
      onSector:(name)=>{state.sector=name.replace(/ \(\d+\)$/,'');persist();syncBar();applyAll();},
      explain:{shows:'Le score moyen par secteur, calculé UNIQUEMENT sur les titres qui passent tes filtres.',
        why:'Concentrer l’attention là où les résultats filtrés sont les plus forts.',
        confirm:'Un secteur qui reste en tête quand tu durcis les filtres.',invalidate:'Un leadership qui dépend d’un seul titre.'}});
  }

  /* ── Top cartes des résultats ── */
  function paintTopCards(f){
    const el=$('op-topcards');if(!el)return;
    const prio=(r)=>bucketOf(r)==='Actionnable'?0:bucketOf(r)==='Proche'?1:bucketOf(r)==='À surveiller'?2:3;
    const ranked=f.filter(r=>r.verdict!=='AVOID'&&r.verdict!=='ÉVITER')
      .slice().sort((a,b)=>prio(a)-prio(b)||(b.score||0)-(a.score||0)).slice(0,6);
    if(!ranked.length){el.innerHTML='';return;}
    el.innerHTML='<div class="vx-card-header" style="padding:0 0 8px"><span class="vx-card-title">Top des résultats — pourquoi eux</span>'
      +'<span class="vx-chart-question">Les 6 meilleurs candidats de TON filtre, avec leurs raisons.</span></div>'
      +'<div class="vx-grid vx-mb2">'+ranked.map(function(r){const dec=r.verdict||'';
      const gauge=(window.VXCharts&&VXCharts.confidenceGaugeSVG&&r.score!=null)
        ?VXCharts.confidenceGaugeSVG(r.score,verdictDir(dec),{size:78,stroke:7,dirLabel:verdictWord(dec)}):'';
      const pb=pbText(r);const ic=pbIcon(r);
      const ser=detail[r.symbol]&&detail[r.symbol].series;
      const spark=sparkMini(ser&&ser.close);
      const chips=[];
      if(r.vx_pwin!=null)chips.push(`<span class="vx-badge" style="color:var(--vx-positive)">proba. gain ${Math.round(r.vx_pwin*100)} %</span>`);
      if(r.vx_edge!=null)chips.push(`<span class="vx-badge">avantage ${Math.round(r.vx_edge)}</span>`);
      if(r.rr!=null)chips.push(`<span class="vx-badge">gain/risque ${VX.fmt.num(r.rr,1)}×</span>`);
      if(r.rvol!=null&&r.rvol>=1.5)chips.push(`<span class="vx-badge" style="color:var(--vx-warning)">volume ×${VX.fmt.num(r.rvol,1)}</span>`);
      return `<div class="vx-card vx-col-4 vx-card--premium" style="grid-column:span 4" aria-label="${r.symbol}">
        <div class="vx-flex" style="align-items:flex-start;gap:.6rem">
          <div style="min-width:0;flex:1">
            <div class="vx-flex" style="gap:.4rem"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" style="font-size:16px;padding-left:0" data-open-analysis="${r.symbol}">${r.symbol}</button>
              <span class="vx-badge">${bucketOf(r)}</span></div>
            <div class="vx-mono vx-mt1" style="font-size:18px;font-weight:700;color:var(--vx-text-primary,#f4f1ec)">${r.price!=null?'$'+VX.fmt.price(r.price):'—'}</div>
            ${spark}
          </div>
          <div style="flex:0 0 auto">${gauge}</div>
        </div>
        ${dimStrip(r)}
        <div class="vx-flex vx-wrap vx-mt1" style="gap:.3rem">${chips.join('')}</div>
        ${pb?`<div class="vx-meta vx-mt1" style="white-space:normal;line-height:1.45">${ic?esc(ic)+' ':''}<b>Pourquoi :</b> ${esc(pb)}</div>`:''}
        <div class="vx-flex vx-wrap vx-mt2" style="gap:.3rem">
          <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${r.symbol}">Analyser</button>
          <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${r.symbol}','follow')">Suivre</button>
          <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${r.symbol}','alert')">Alerte</button>
          <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/options/${r.symbol}">Options</a>
        </div></div>`;}).join('')+'</div>';
  }

  /* ── Table triable ── */
  const SORTS={score:{k:r=>r.score||0,label:'score'},pwin:{k:r=>(r.vx_pwin||0),label:'proba de gain'},
    edge:{k:r=>(r.vx_edge||0),label:'avantage'},rr:{k:r=>(r.rr||0),label:'gain/risque'},
    rvol:{k:r=>(r.rvol||0),label:'volume relatif'},chg:{k:r=>(r.change||0),label:'variation'},
    perfw:{k:r=>(r.perf_w||0),label:'perf. semaine'},pos52:{k:r=>(r.pos52||0),label:'position 52 sem.'}};
  let sortKey='score',sortDir=-1;
  function paintTable(f){
    const s=SORTS[sortKey]||SORTS.score;
    const sorted=f.slice().sort((a,b)=>(s.k(b)-s.k(a))*(-sortDir));
    $('op-sort-label').textContent=s.label+(sortDir<0?' ↓':' ↑');
    $('op-table-count').textContent=Math.min(sorted.length,100)+' affichés sur '+f.length;
    $('op-table').innerHTML=sorted.length?`<table class="vx-table"><thead><tr>
      <th>Titre</th><th>Statut</th><th>Verdict</th>
      <th class="vx-num" data-sort="score">Score</th>
      <th class="vx-num" data-sort="pwin">Proba gain</th>
      <th class="vx-num" data-sort="edge">Avantage</th>
      <th class="vx-num" data-sort="rr">Gain/risque</th>
      <th class="vx-num" data-sort="rvol">Vol. rel.</th>
      <th class="vx-num" data-sort="chg">Var. jour</th>
      <th class="vx-num" data-sort="perfw">Perf. sem.</th>
      <th data-sort="pos52">52 sem.</th>
      <th>Setup</th><th>Secteur</th><th></th></tr></thead><tbody>
      ${sorted.slice(0,100).map(r=>`<tr data-clickable data-open-analysis="${r.symbol}">
        <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span></td>
        <td data-label="Statut"><span class="vx-badge">${bucketOf(r)}</span></td>
        <td data-label="Verdict"><span class="vx-badge vx-badge-decision" data-decision="${esc(r.verdict||'')}">${esc(VERD_FR[r.verdict]||r.verdict||'')}</span></td>
        ${heatCell(r.score,{label:'Score',good:72,mid:56})}
        ${heatCell(r.vx_pwin!=null?r.vx_pwin*100:null,{label:'Proba',good:60,mid:45,fmt:v=>Math.round(v)+'%'})}
        ${heatCell(r.vx_edge,{label:'Avantage',good:60,mid:40})}
        ${heatCell(r.rr,{label:'G/R',max:3,good:2,mid:1,fmt:v=>VX.fmt.num(v,1)+'×'})}
        <td data-label="Vol." class="vx-num">${r.rvol!=null?'×'+VX.fmt.num(r.rvol,1):'—'}</td>
        <td data-label="Var." class="vx-num ${r.change>0?'vx-pos':r.change<0?'vx-neg':''}">${r.change!=null?VX.fmt.pct(r.change,1):'—'}</td>
        <td data-label="Sem." class="vx-num ${r.perf_w>0?'vx-pos':r.perf_w<0?'vx-neg':''}">${r.perf_w!=null?VX.fmt.pct(r.perf_w,1):'—'}</td>
        <td data-label="52s">${rail52(r.pos52)}</td>
        <td data-label="Setup" class="vx-truncate" style="max-width:130px">${esc(pbText(r)||'—')}</td>
        <td data-label="Secteur" class="vx-truncate" style="max-width:110px">${esc(r.sector||'—')}</td>
        <td>${rowActions(r.symbol)}</td></tr>`).join('')}</tbody></table>`
      :VX.states.empty('Aucun titre ne correspond aux filtres.','<button class="vx-btn vx-btn-sm" id="op-clear2">Effacer les filtres</button>');
    document.getElementById('op-clear2')?.addEventListener('click',resetFilters);
    document.querySelectorAll('#op-table th[data-sort]').forEach(th=>{
      if(th.dataset.sort===sortKey)th.dataset.dir=sortDir<0?'desc':'asc';
      th.addEventListener('click',()=>{
        if(sortKey===th.dataset.sort)sortDir=-sortDir;else{sortKey=th.dataset.sort;sortDir=-1;}
        paintTable(filtered());});
    });
  }

  /* ── Entonnoir CLIQUABLE : chaque étage applique le filtre correspondant ── */
  async function paintFunnel(){
    const el=$('op-funnel');if(!el)return;
    let fn;try{fn=await VX.fetch('/api/opportunities/funnel',{ttl:60000});}catch(e){return;}
    if(!fn||!fn.stages||!fn.stages.length)return;
    el.innerHTML='<div class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Entonnoir</span>'
      +'<span class="vx-chart-question">Cliquer un étage filtre le screener.</span></div>'
      +'<div id="op-funnel-viz"></div>'
      +(fn.actionable_symbols&&fn.actionable_symbols.length?'<div class="vx-dim vx-mt2" style="font-size:12px">Actionnables : '
        +fn.actionable_symbols.map(s=>'<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="'+esc(s)+'" style="padding:0 4px;color:var(--vx-positive)">'+esc(s)+'</button>').join(' ')+'</div>':'')
      +'</div>';
    if(window.VXCharts&&VXCharts.funnel){
      VXCharts.funnel('op-funnel-viz',{stages:fn.stages.map(s=>({label:s.label,value:s.count})),
        fmt:v=>VX.fmt.nd(v),ariaLabel:'Entonnoir de sélection'});
      /* étages cliquables → mappe l'étage vers un filtre bucket approché */
      const map={'Actionnable':'Actionnable','Proche':'Proche','À surveiller':'À surveiller'};
      el.querySelectorAll('#op-funnel-viz [role="img"], #op-funnel-viz svg, #op-funnel-viz div').forEach(()=>{});
      el.querySelector('#op-funnel-viz').addEventListener('click',(ev)=>{
        const t=(ev.target.textContent||'').trim();
        const k=Object.keys(map).find(x=>t.includes(x));
        if(k){state.bucket=state.bucket===map[k]?'':map[k];persist();syncBar();applyAll();}});
    }
  }

  /* ── Application globale des filtres ── */
  function applyAll(){
    const f=filtered();
    paintKpis(f);paintScatter(f);paintDist(f);paintSectors(f);paintTopCards(f);paintTable(f);
  }
  function syncBar(){
    document.querySelectorAll('[data-fk="bucket"]').forEach(c=>
      c.setAttribute('aria-pressed',String(c.dataset.fv===state.bucket)));
    const sec=document.querySelector('select[data-fk="sector"]');if(sec)sec.value=state.sector;
  }
  function resetFilters(){
    Object.assign(state,{bucket:'',sector:'',vehicle:'',setup:'',minScore:0,minPwin:0,minRR:0,minRvol:0});
    persist();
    document.querySelectorAll('.vx-screenbar input[type=range]').forEach(r=>{r.value=0;r.closest('label').querySelector('b').textContent='0'+(r.dataset.fk==='minPwin'?'%':r.dataset.fk==='minRR'?'×':r.dataset.fk==='minRvol'?'':'');});
    const inp=document.querySelector('input[data-fk="setup"]');if(inp)inp.value='';
    const veh=document.querySelector('select[data-fk="vehicle"]');if(veh)veh.value='';
    syncBar();applyAll();
  }
  /* Écouteurs de la barre */
  document.querySelectorAll('[data-fk="bucket"]').forEach(c=>c.addEventListener('click',()=>{
    state.bucket=state.bucket===c.dataset.fv?'':c.dataset.fv;persist();syncBar();applyAll();}));
  document.querySelector('select[data-fk="sector"]').addEventListener('change',function(){state.sector=this.value;persist();applyAll();});
  document.querySelector('select[data-fk="vehicle"]').addEventListener('change',function(){state.vehicle=this.value;persist();applyAll();});
  document.querySelectorAll('.vx-screenbar input[type=range]').forEach(r=>r.addEventListener('input',function(){
    state[this.dataset.fk]=+this.value;
    this.closest('label').querySelector('b').textContent=this.value+(this.dataset.fk==='minPwin'?'%':this.dataset.fk==='minRR'?'×':'');
    persist();applyAll();}));
  document.querySelector('input[data-fk="setup"]').addEventListener('input',function(){state.setup=this.value.toUpperCase();persist();applyAll();});
  document.getElementById('op-reset').addEventListener('click',resetFilters);

  paintFunnel();
  applyAll();
  VX.context.restoreIfReturning();
}

/* ═════════ OPTIONS : screener du board réel ═════════ */
async function renderOptions(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const board=(scan.options_board||[]);
  window.__opCompare=function(symWanted){
    const catOf2=(c)=>{const d=Math.abs(c.delta||0);
      if(d>=0.40&&d<=0.60)return'BALANCED';if(d>=0.28&&d<0.45)return'DYNAMIC';
      if(d>=0.18&&d<0.30)return'ULTRA_CONVEX';return'AUTRE';};
    let pool=board;
    if(symWanted)pool=pool.filter(c=>c.sym===symWanted);
    const pick=(cat)=>pool.filter(c=>catOf2(c)===cat)
      .sort((a,b)=>(b.quality||0)-(a.quality||0))[0]||null;
    const trio=[['Défensif (Balanced)',pick('BALANCED')],
                ['PRINCIPAL (Dynamic)',pick('DYNAMIC')],
                ['Explosif (Ultra convex)',pick('ULTRA_CONVEX')]];
    const avail=trio.filter(([,c])=>c);
    if(!avail.length){VX.toast('Aucun contrat comparable sur ce filtre','warning');return;}
    const row=(label,c)=>c?`<tr>
      <td><b>${label}</b><br><span class="vx-mono vx-meta">${c.sym} ${VX.fmt.nd(c.strike)} ${c.exp||''}</span></td>
      <td class="vx-num">${VX.fmt.nd(c.delta)}</td><td class="vx-num">${VX.fmt.nd(c.dte)}</td>
      <td class="vx-num">${c.iv!=null?(c.iv).toFixed(0)+'%':'—'}</td>
      <td class="vx-num">${VX.fmt.nd(c.cost)}</td>
      <td class="vx-num">${c.spread!=null?c.spread+'%':'—'}</td>
      <td class="vx-num">${VX.fmt.nd(c.oi)}</td>
      <td class="vx-num"><b>${VX.fmt.nd(c.quality)}</b></td></tr>`:'';
    const main=avail.find(([l])=>l.startsWith('PRINCIPAL'))||avail[0];
    const others=avail.filter(x=>x!==main);
    const why=others.map(([l,c])=>{
      const m=main[1];const wins=[];
      if((c.delta||0)>(m.delta||0))wins.push('delta plus élevé (plus défensif)');
      if((c.cost||1e9)<(m.cost||1e9))wins.push('prime plus faible (plus convexe)');
      if((c.oi||0)>(m.oi||0))wins.push('OI supérieur');
      return `<li><b>${l}</b> : ${wins.length?('gagne sur '+wins.join(', ')):'ne domine sur aucune dimension clé'} — qualité globale ${VX.fmt.nd(c.quality)} vs ${VX.fmt.nd(m[1]?m[1].quality:'')}.</li>`;
    }).join('');
    VX.shell.openDrawer('Comparateur de contrats'+(symWanted?' — '+symWanted:''),
      `<div class="vx-table-wrap"><table class="vx-table"><thead><tr>
        <th>Contrat</th><th class="vx-num">Δ</th><th class="vx-num">DTE</th><th class="vx-num">IV</th>
        <th class="vx-num">Prime</th><th class="vx-num">Spread</th><th class="vx-num">OI</th>
        <th class="vx-num">Qualité</th></tr></thead>
        <tbody>${avail.map(([l,c])=>row(l,c)).join('')}</tbody></table></div>
       <div class="vx-insight vx-mt3"><b>Pourquoi ${main[0]} domine</b>
         <div class="vx-mt1" style="font-size:12.5px">Le contrat principal offre le meilleur score composite
         (R:R simulé × liquidité × coût du temps). Les alternatives gagnent chacune sur UNE dimension :</div>
         <ul class="vx-mt1" style="margin:0;padding-left:18px;font-size:12.5px">${why||'<li>aucune alternative disponible</li>'}</ul></div>
       <div class="vx-help vx-mt2">Analyse uniquement — copier le contrat pour le consulter chez le broker.</div>`);
  };
  const symFilter=(PARAMS.sym||'').toUpperCase();
  const state={type:'',bucket:'',danger:'',minQ:0,minPop:0,sym:symFilter};
  function filtered(){
    let f=board;
    if(state.sym)f=f.filter(c=>c.sym===state.sym);
    if(state.type)f=f.filter(c=>c.type===state.type);
    if(state.bucket)f=f.filter(c=>c.bucket===state.bucket);
    if(state.danger)f=f.filter(c=>c.danger===state.danger);
    if(state.minQ)f=f.filter(c=>(c.quality||0)>=state.minQ);
    if(state.minPop)f=f.filter(c=>(c.pop||0)>=state.minPop);
    return f;
  }
  const dangers=[...new Set(board.map(c=>c.danger).filter(Boolean))];
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-screenbar" role="group" aria-label="Filtres options">
      ${['CALL','PUT'].map(t=>`<button class="vx-chip" data-fk="type" data-fv="${t}" aria-pressed="false"
        style="${t==='PUT'?'color:var(--vx-violet)':''}">${t}</button>`).join('')}
      ${['court','moyen','long'].map(b=>`<button class="vx-chip" data-fk="bucket" data-fv="${b}" aria-pressed="false">${b} terme</button>`).join('')}
      <select class="vx-select" data-fk="danger" style="width:auto" aria-label="Danger">
        <option value="">Tout danger</option>${dangers.map(d=>`<option>${esc(d)}</option>`).join('')}</select>
      <label class="rng">qualité ≥ <input type="range" data-fk="minQ" min="0" max="80" step="5" value="0"><b>0</b></label>
      <label class="rng">proba profit ≥ <input type="range" data-fk="minPop" min="0" max="70" step="5" value="0"><b>0%</b></label>
      <input class="vx-input" data-fk="sym" style="width:110px;text-transform:uppercase" placeholder="Ticker" value="${esc(state.sym)}">
      <button class="vx-btn vx-btn-sm vx-btn-soft" onclick="window.__opCompare&&window.__opCompare(document.querySelector('[data-fk=sym]').value.toUpperCase())">Comparer 3 contrats</button>
      <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/options">Desk options →</a>
      <span class="vx-meta vx-right" id="op-opt-count"></span>
    </div>
    <div class="vx-scr-kpis" id="op-opt-kpis"></div>
    <div class="vx-grid vx-mt4">
      <div class="vx-col-8" id="op-opt-scatter"></div>
      <div class="vx-col-4"><div class="vx-card" id="op-opt-sel-card">
        <div class="vx-card-header"><span class="vx-card-title">Contrat sélectionné</span></div>
        <div id="op-opt-sel"><div class="vx-meta">Clique un point du nuage ou une ligne de la table pour simuler le contrat.</div></div></div></div>
    </div>
    <div class="vx-card vx-mt4"><div class="vx-card-header"><span class="vx-card-title">Contrats du board</span>
      <span class="vx-chart-question">Cliquer une ligne simule le contrat (payoff, scénarios, décote temps).</span></div>
      <div class="vx-table-wrap vx-table-cards" id="op-opt-table"></div>
      <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.options_source||scan.source,metaMode(scan))}</div></div>
    <div class="vx-grid vx-mt4" id="op-contract" hidden>
      <div class="vx-col-6" id="op-payoff"></div>
      <div class="vx-col-6" id="op-scenarios"></div>
      <div class="vx-col-6" id="op-theta"></div>
      <div class="vx-col-6" id="op-iv"></div>
    </div>`;
  function paintKpis(f){
    const calls=f.filter(c=>c.type==='CALL').length;
    const qmax=f.length?Math.max(...f.map(c=>c.quality||0)):null;
    const pmax=f.length?Math.max(...f.map(c=>c.pop||0)):null;
    const ivs=f.map(c=>c.iv).filter(x=>x!=null).sort((a,b)=>a-b);
    const ivMed=ivs.length?ivs[Math.floor(ivs.length/2)]:null;
    const stale=f.filter(c=>c.stale).length;
    $('op-opt-kpis').innerHTML=
      `<div class="k"><b>${f.length}</b><span>contrats</span></div>`
      +`<div class="k"><b>${calls} / ${f.length-calls}</b><span>calls / puts</span></div>`
      +`<div class="k"><b>${qmax!=null?Math.round(qmax):'—'}</b><span>meilleure qualité</span></div>`
      +`<div class="k"><b>${pmax!=null?Math.round(pmax)+' %':'—'}</b><span>meilleure proba profit</span></div>`
      +`<div class="k"><b>${ivMed!=null?Math.round(ivMed)+' %':'—'}</b><span>IV médiane</span></div>`
      +`<div class="k"><b>${stale}</b><span>hors séance (indicatif)</span></div>`;
    $('op-opt-count').textContent=f.length+' / '+board.length+' contrats';
  }
  function paintScatter(f){
    const host=$('op-opt-scatter');if(!host)return;
    const cc=VXCharts.colors;
    const pts=f.filter(c=>c.quality!=null&&c.pop!=null).map(c=>({
      x:c.quality,y:c.pop,sym:c.sym,type:c.type,strike:c.strike,exp:c.exp,dte:c.dte,
      cost:c.cost,danger:c.danger,idx:board.indexOf(c),
      r:4+Math.min(8,Math.sqrt((c.cost||100)/220))}));
    if(!pts.length){host.innerHTML='<div class="vx-card">'+VX.states.empty('Aucun contrat avec qualité et proba dans ce filtre.')+'</div>';return;}
    const dangerCol={'Faible':cc.positive,'Modéré':cc.warning,'Élevé':cc.negative,'Extrême':'#b13a33'};
    VXCharts.card('op-opt-scatter',{
      title:'Qualité × proba de profit — où sont les bons contrats ?',
      question:'Quels contrats combinent qualité (liquidité, spread, théta) et proba de finir gagnants ?',
      conclusion:pts.filter(p=>p.x>=55&&p.y>=45).length+' contrat(s) en zone favorable (qualité ≥ 55 · proba ≥ 45 %)',
      height:320,source:scan.options_source||scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
      limits:'taille de point = prime engagée · couleur = danger (théta, proba, échéance)',
      explain:{shows:'Chaque point est un contrat du board, placé par sa qualité composite et sa probabilité de profit à l’échéance.',
        why:'Une prime pas chère ne vaut rien si le contrat est illiquide ou brûle trop vite — la qualité le mesure.',
        confirm:'Contrat en haut-droit avec danger Faible/Modéré.',
        invalidate:'Danger Élevé/Extrême : le théta ou l’échéance jouent contre toi.'},
      render:(cv)=>VXCharts.mount(cv,{type:'scatter',
        data:{datasets:[{data:pts,
          pointRadius:(ctx)=>ctx.raw?ctx.raw.r:4,pointHoverRadius:(ctx)=>ctx.raw?ctx.raw.r+3:8,
          pointBackgroundColor:(ctx)=>dangerCol[ctx.raw&&ctx.raw.danger]||cc.neutral,
          pointBorderColor:'rgba(255,255,255,.2)',pointBorderWidth:1}]},
        options:{scales:{
          x:{title:{display:true,text:'Qualité du contrat →'},min:0,max:100,grid:{color:'rgba(255,255,255,.05)'}},
          y:{title:{display:true,text:'Proba de profit % ↑'},min:0,max:100,grid:{color:'rgba(255,255,255,.05)'}}},
          plugins:{tooltip:{callbacks:{label:(ctx)=>`${ctx.raw.sym} ${ctx.raw.type} ${ctx.raw.strike} (${ctx.raw.dte} j) · qualité ${Math.round(ctx.raw.x)} · proba ${Math.round(ctx.raw.y)} % · danger ${ctx.raw.danger||'n/d'}`}}},
          onClick:(evt,els,chart)=>{const p=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
            if(p.length){const d=chart.data.datasets[0].data[p[0].index];openContract(board[d.idx]);}}}})});
  }
  function paintTable(f){
    const sorted=f.slice().sort((a,b)=>(b.quality||0)-(a.quality||0));
    $('op-opt-table').innerHTML=sorted.length?`<table class="vx-table"><thead><tr>
      <th>Sous-jacent</th><th>Type</th><th>Terme</th><th class="vx-num">Strike</th><th>Échéance</th>
      <th class="vx-num">DTE</th><th class="vx-num">Delta</th><th class="vx-num">IV</th>
      <th class="vx-num">Prime $</th><th class="vx-num">Théta/j</th><th class="vx-num">Proba profit</th>
      <th class="vx-num">Qualité</th><th>Danger</th><th></th></tr></thead>
      <tbody>${sorted.slice(0,60).map(c=>`<tr data-clickable data-ct="${board.indexOf(c)}" tabindex="0" role="button" aria-label="Simuler ${esc(c.sym)} ${VX.fmt.nd(c.strike)}">
        <td data-label="Sous-jacent"><span class="vx-ticker">${c.sym}</span></td>
        <td data-label="Type"><span class="vx-badge" style="color:${c.type==='PUT'?'var(--vx-violet)':'var(--vx-positive)'}">${c.type}</span></td>
        <td data-label="Terme">${esc(c.bucket||'—')}</td>
        <td data-label="Strike" class="vx-num">${VX.fmt.nd(c.strike)}</td>
        <td data-label="Échéance" class="vx-mono">${esc(String(c.exp||'').slice(0,10))}</td>
        <td data-label="DTE" class="vx-num">${VX.fmt.nd(c.dte)}</td>
        <td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
        <td data-label="IV" class="vx-num">${c.iv!=null?Math.round(c.iv)+'%':'—'}</td>
        <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.cost)}</td>
        <td data-label="Théta" class="vx-num">${c.theta_burn!=null?VX.fmt.num(c.theta_burn,1)+'%':'—'}</td>
        ${heatCell(c.pop,{label:'Proba',good:55,mid:40,fmt:v=>Math.round(v)+'%'})}
        ${heatCell(c.quality,{label:'Qualité',good:60,mid:45})}
        <td data-label="Danger"><span class="vx-badge" style="color:${{'Faible':'var(--vx-positive)','Modéré':'var(--vx-warning)','Élevé':'var(--vx-negative)','Extrême':'var(--vx-negative)'}[c.danger]||'var(--vx-text-dim)'}">${esc(c.danger||'—')}</span></td>
        <td>${rowActions(c.sym)}</td></tr>`).join('')}</tbody></table>`
      :VX.states.empty(state.sym?'Aucun contrat pour '+state.sym+' dans ce filtre.':'Board options vide — le sélecteur ne force jamais une idée.',
        '<a class="vx-btn vx-btn-sm" href="/system?view=data">Vérifier les données</a>');
    document.querySelectorAll('[data-ct]').forEach(tr=>{
      const open=(e)=>{if(e.target.closest('[data-open-analysis],[data-entity-menu]'))return;openContract(board[+tr.dataset.ct]);};
      tr.addEventListener('click',open);
      tr.addEventListener('keydown',(e)=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(e);}});});
  }
  function applyAll(){const f=filtered();paintKpis(f);paintScatter(f);paintTable(f);}
  document.querySelectorAll('.vx-screenbar [data-fk="type"],.vx-screenbar [data-fk="bucket"]').forEach(c=>c.addEventListener('click',()=>{
    const k=c.dataset.fk;state[k]=state[k]===c.dataset.fv?'':c.dataset.fv;
    document.querySelectorAll(`.vx-screenbar [data-fk="${k}"]`).forEach(x=>
      x.setAttribute('aria-pressed',String(x.dataset.fv===state[k])));applyAll();}));
  document.querySelector('select[data-fk="danger"]').addEventListener('change',function(){state.danger=this.value;applyAll();});
  document.querySelectorAll('.vx-screenbar input[type=range]').forEach(r=>r.addEventListener('input',function(){
    state[this.dataset.fk]=+this.value;
    this.closest('label').querySelector('b').textContent=this.value+(this.dataset.fk==='minPop'?'%':'');
    applyAll();}));
  document.querySelector('input[data-fk="sym"]').addEventListener('input',function(){state.sym=this.value.toUpperCase();applyAll();});
  async function openContract(c){
    if(!c)return;
    /* Les contrats du board ne portent pas toujours le spot : on le prend du
       scan (prix réel du sous-jacent) — sans spot, payoff vide honnête. */
    const spot=(c.spot!=null&&isFinite(c.spot))?c.spot:(((scan.detail||{})[c.sym]||{}).price);
    $('op-opt-sel').innerHTML=
      `<div class="vx-flex"><span class="vx-ticker" style="font-size:15px">${esc(c.sym)}</span>
        <span class="vx-badge" style="color:${c.type==='PUT'?'var(--vx-violet)':'var(--vx-positive)'}">${c.type}</span>
        <span class="vx-badge vx-right">${esc(c.bucket||'')}</span></div>
       <div class="vx-kv vx-mt2"><span class="k">Strike · échéance</span><span class="v vx-mono">${VX.fmt.nd(c.strike)} · ${esc(String(c.exp||'').slice(0,10))}</span></div>
       <div class="vx-kv"><span class="k">Prime</span><span class="v vx-mono">${VX.fmt.nd(c.cost)} $</span></div>
       <div class="vx-kv"><span class="k">Proba profit</span><span class="v vx-mono">${c.pop!=null?Math.round(c.pop)+' %':'n/d'}</span></div>
       <div class="vx-kv"><span class="k">Qualité</span><span class="v vx-mono">${VX.fmt.nd(c.quality)}</span></div>
       <div class="vx-kv"><span class="k">Danger</span><span class="v">${esc(c.danger||'n/d')}</span></div>
       <div class="vx-kv"><span class="k">Décote temps</span><span class="v vx-mono">${c.theta_burn!=null?VX.fmt.num(c.theta_burn,2)+' % / jour':'n/d'}</span></div>
       <div class="vx-flex vx-wrap vx-mt2" style="gap:.3rem">
         <a class="vx-btn vx-btn-sm vx-btn-primary" href="/options/${esc(c.sym)}">Dossier options</a>
         <button class="vx-btn vx-btn-sm" data-open-analysis="${esc(c.sym)}">Fiche action</button></div>`;
    $('op-contract').hidden=false;
    $('op-contract').scrollIntoView({behavior:'smooth',block:'nearest'});
    VXCharts.payoffCard('op-payoff',{title:`${c.sym} ${c.strike} ${c.type} ${c.exp}`,
      question:'Que rapporte/coûte ce contrat à l’échéance ?',
      conclusion:`Breakeven ${VX.fmt.nd(c.be)} · prime ${VX.fmt.nd(c.cost)}`,
      spot:spot,strike:c.strike,premium:c.cost,right:c.type==='PUT'?'P':'C',breakeven:c.be,height:210,
      source:'board options',timestamp:Date.now(),mode:'delayed',
      explain:{shows:'Le P&L du contrat à l’échéance selon le prix du sous-jacent (arithmétique du contrat).',
        why:'Visualiser breakeven et asymétrie avant d’engager la prime.',
        confirm:'Sous-jacent au-delà du breakeven avant l’échéance.',
        invalidate:'Stop sous-jacent touché — on ne « garde pas en espérant ».'}});
    try{
      const q=new URLSearchParams({sym:c.sym,strike:c.strike,dte:c.dte,mid:c.cost,
        iv:c.iv||'',right:c.type==='PUT'?'P':'C',exp:c.exp,spot:spot||''});
      const s=await VX.fetch('/api/options/simulate?'+q.toString(),{ttl:120000});
      VXCharts.scenarioMatrix('op-scenarios',s.sim,{title:'Scénarios (moteur)',
        question:'Que vaut le contrat selon le spot et le temps ?',
        conclusion:`R:R simulé ${VX.fmt.nd(s.sim.reward_risk)} · perte planifiée ${VX.fmt.nd(s.sim.worst_planned_loss_pct)} %`,
        source:'scenario_pricer',timestamp:Date.now(),mode:'delayed'});
      VXCharts.thetaCard('op-theta',s.sim,{title:'Décomposition temps',
        question:'Combien coûte chaque jour d’attente ?',
        conclusion:'Réévaluer après 5-8 séances sans mouvement',
        height:190,source:'scenario_pricer',timestamp:Date.now(),mode:'delayed'});
      VXCharts.ivSensitivityCard('op-iv',s.sim,{title:'Sensibilité IV',
        question:'Que se passe-t-il si la volatilité implicite bouge ?',
        conclusion:'IV -20 % à +20 % au scénario BASE',height:190,
        source:'scenario_pricer',timestamp:Date.now(),mode:'delayed'});
    }catch(e){
      $('op-scenarios').innerHTML='<div class="vx-card">'+VX.states.error('Simulation moteur indisponible : '+e.message)+'</div>';
      $('op-theta').innerHTML='';$('op-iv').innerHTML='';
    }
  }
  applyAll();
}

/* ═════════ PORTEFEUILLE : mes positions × le moteur + candidats ═════════ */
async function renderPortfolio(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]);
  const byId={};rows.forEach(r=>{byId[r.symbol]=r;});
  const pos=(window.VXEntities?VXEntities.positions():[])||[];
  if(!pos.length){
    $('op-body').innerHTML=VX.states.empty('Aucune position déclarée — le comparateur portefeuille × moteur s’active dès ta première position.',
      '<button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>');
    return;
  }
  const held=pos.map(p=>{
    const r=byId[String(p.sym).toUpperCase()]||null;
    const status=!r?'hors scan':(r.verdict==='AVOID'||r.verdict==='ÉVITER')?'à revoir'
      :(r.verdict==='BUY'||r.verdict==='ACHETER')?'confirmée':'neutre';
    return {p,r,status};
  });
  const toReview=held.filter(h=>h.status==='à revoir');
  const secOfHeld=[...new Set(held.map(h=>h.r&&h.r.sector).filter(Boolean))];
  /* Candidats de remplacement : meilleurs titres NON détenus, priorité aux secteurs du portefeuille */
  const heldSyms=new Set(pos.map(p=>String(p.sym).toUpperCase()));
  const candidates=rows.filter(r=>!heldSyms.has(r.symbol)&&(r.verdict==='BUY'||r.verdict==='ACHETER'))
    .slice().sort((a,b)=>(secOfHeld.includes(b.sector)?1:0)-(secOfHeld.includes(a.sector)?1:0)||(b.score||0)-(a.score||0))
    .slice(0,6);
  const statusBadge={confirmée:'<span class="vx-badge" style="color:var(--vx-positive)">CONFIRMÉE par le moteur</span>',
    'à revoir':'<span class="vx-badge" style="color:var(--vx-negative)">À REVOIR — verdict ÉVITER</span>',
    neutre:'<span class="vx-badge" style="color:var(--vx-warning)">NEUTRE — surveiller</span>',
    'hors scan':'<span class="vx-badge">hors de l’univers scanné</span>'};
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-scr-kpis">
      <div class="k"><b>${pos.length}</b><span>positions déclarées</span></div>
      <div class="k"><b style="color:var(--vx-positive)">${held.filter(h=>h.status==='confirmée').length}</b><span>confirmées par le moteur</span></div>
      <div class="k"><b style="color:var(--vx-negative)">${toReview.length}</b><span>à revoir (verdict ÉVITER)</span></div>
      <div class="k"><b>${candidates.length}</b><span>candidats d’achat non détenus</span></div>
    </div>
    ${toReview.length?`<div class="vx-insight vx-mt3" data-tone="risk"><b>⚠ ${toReview.length} position(s) contredite(s) par le moteur :</b>
      ${toReview.map(h=>`<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(h.p.sym)}">${esc(h.p.sym)}</button>`).join(' ')}
      — vérifier le dossier avant de décider (jamais de vente automatique).</div>`:''}
    <div class="vx-card vx-mt3"><div class="vx-card-header"><span class="vx-card-title">Mes positions × le moteur</span>
      <span class="vx-chart-question">Le moteur confirme-t-il encore chacune de mes lignes ?</span></div>
      <div class="vx-table-wrap vx-table-cards" id="op-pf-table"></div>
      <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.source,metaMode(scan))}
        · verdicts du moteur — analyse uniquement, aucune vente automatique</div></div>
    <div id="op-pf-cands" class="vx-mt4"></div>`;
  $('op-pf-table').innerHTML=`<table class="vx-table"><thead><tr>
    <th>Position</th><th>Type</th><th>Statut moteur</th><th class="vx-num">Score</th>
    <th class="vx-num">Proba gain</th><th class="vx-num">Var. jour</th><th>52 sem.</th><th>Setup</th><th></th></tr></thead><tbody>
    ${held.map(h=>{const r=h.r||{};return `<tr data-clickable data-open-analysis="${esc(h.p.sym)}">
      <td data-label="Position"><span class="vx-ticker">${esc(h.p.sym)}</span></td>
      <td data-label="Type"><span class="vx-badge" ${h.p.type!=='STK'?'style="color:var(--vx-violet)"':''}>${esc(h.p.type||'STK')}${h.p.strike?' '+esc(h.p.strike):''}</span></td>
      <td data-label="Statut">${statusBadge[h.status]||''}</td>
      ${heatCell(r.score,{label:'Score',good:72,mid:56})}
      ${heatCell(r.vx_pwin!=null?r.vx_pwin*100:null,{label:'Proba',good:60,mid:45,fmt:v=>Math.round(v)+'%'})}
      <td data-label="Var." class="vx-num ${r.change>0?'vx-pos':r.change<0?'vx-neg':''}">${r.change!=null?VX.fmt.pct(r.change,1):'—'}</td>
      <td data-label="52s">${rail52(r.pos52)}</td>
      <td data-label="Setup" class="vx-truncate" style="max-width:150px">${esc(pbText(r)||'—')}</td>
      <td>${rowActions(h.p.sym)}</td></tr>`;}).join('')}</tbody></table>`;
  const cd=$('op-pf-cands');
  cd.innerHTML='<div class="vx-card-header" style="padding:0 0 8px"><span class="vx-card-title">Candidats non détenus — signaux d’achat du moteur</span>'
    +'<span class="vx-chart-question">Qui mériterait une place, priorité aux secteurs déjà en portefeuille ?</span></div>'
    +(candidates.length?'<div class="vx-grid">'+candidates.map(r=>`
      <div class="vx-card vx-col-4" style="grid-column:span 4;border-left:3px solid var(--vx-positive)">
        <div class="vx-flex"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" style="font-size:15px;padding-left:0" data-open-analysis="${r.symbol}">${r.symbol}</button>
          <span class="vx-badge vx-badge-decision vx-right" data-decision="${esc(r.verdict)}">${esc(VERD_FR[r.verdict]||r.verdict)}</span></div>
        <div class="vx-flex vx-wrap vx-mt1" style="gap:.3rem">
          <span class="vx-badge">score ${VX.fmt.nd(r.score)}</span>
          ${r.vx_pwin!=null?`<span class="vx-badge" style="color:var(--vx-positive)">proba ${Math.round(r.vx_pwin*100)} %</span>`:''}
          ${r.sector?`<span class="vx-badge">${esc(r.sector)}${secOfHeld.includes(r.sector)?' · déjà en portefeuille':''}</span>`:''}</div>
        ${pbText(r)?`<div class="vx-meta vx-mt1" style="white-space:normal">${esc(pbText(r))}</div>`:''}
        <div class="vx-flex vx-mt2" style="gap:.3rem">
          <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${r.symbol}">Analyser</button>
          <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${r.symbol}','follow')">Suivre</button></div>
      </div>`).join('')+'</div>'
    :VX.states.empty('Aucun candidat d’achat non détenu dans le scan courant.'));
}

/* ═════════ ANOMALIES ═════════ */
async function renderAnomalies(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>(r.anomalies||[]).length);
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar">${['Actions','Données']
      .map((g,i)=>`<button class="vx-chip" aria-pressed="${i===0}" data-ag="${g}">${g}</button>`).join('')}</div>
    <div id="op-anom"></div>`;
  function paint(group){
    if(group==='Actions'){
      $('op-anom').innerHTML=rows.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Anomalies</th><th class="vx-num">Intensité</th><th class="vx-num">Score</th><th></th></tr></thead><tbody>
        ${rows.slice(0,60).map(r=>`<tr data-clickable data-open-analysis="${r.symbol}">
          <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span></td>
          <td data-label="Anomalies">${(r.anomalies||[]).slice(0,4).map(a=>`<span class="vx-badge">${esc(typeof a==='string'?a:(a.code||''))}</span>`).join(' ')}</td>
          <td data-label="Intensité" class="vx-num">${VX.fmt.nd(r.anomaly_score)}</td>
          <td data-label="Score" class="vx-num">${VX.fmt.nd(r.score)}</td>
          <td>${rowActions(r.symbol)}</td></tr>`).join('')}</tbody></table></div>`
        :VX.states.empty('Aucune anomalie action détectée sur le scan courant.');
    }else{
      VX.fetch('/api/data-quality',{ttl:60000}).then(dq=>{
        $('op-anom').innerHTML=`<div class="vx-card">${Object.entries(dq.by_quality||{}).map(([k,v])=>
          `<div class="vx-kv"><span class="k">${k}</span><span class="v">${v}</span></div>`).join('')}
          <div class="vx-meta vx-mt2">${esc(dq.note||'')}</div></div>`;
      }).catch(()=>{$('op-anom').innerHTML=VX.states.error('Qualité de données indisponible');});
    }
  }
  document.querySelectorAll('[data-ag]').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('[data-ag]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    paint(b.dataset.ag);}));
  paint('Actions');
}

/* ═════════ CALENDRIER ═════════ */
async function renderCalendar(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const positions=(window.VXEntities?window.VXEntities.positions():[]).map(p=>p.sym);
    const items=[...(cal.macro||[]).map(m=>({when:m.date,kind:m.kind,label:esc(m.label)+(m.note?' — '+esc(m.note):'')+(m.approx?' (approx.)':'')})),
      ...(cal.items||[]).map(it=>({when:it.date,kind:'Résultats',sym:it.sym,
        label:`résultats dans ${it.dte} j · verdict moteur ${esc(VERD_FR[it.verdict]||it.verdict||'n/d')}`
          +(positions.includes(it.sym)?' · <b class="vx-warn">position exposée</b>':'')}))]
      .sort((a,b)=>String(a.when).localeCompare(String(b.when)));
    $('op-body').innerHTML='<div id="op-cal"></div>';
    VXCharts.timelineCard('op-cal',{title:'Calendrier des catalyseurs',
      question:'Quels événements peuvent faire bouger les dossiers ?',
      items:items.slice(0,30),source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun événement identifié sur l’horizon.'});
  }catch(e){$('op-body').innerHTML=VX.states.error('Calendrier indisponible');}
}

const RENDER={screener:renderScreener,options:renderOptions,portfolio:renderPortfolio,
  anomalies:renderAnomalies,calendar:renderCalendar};
function boot(){(RENDER[VIEW]||renderScreener)().catch(e=>{
  $('op-body').innerHTML=VX.states.error('Chargement impossible : '+e.message);});}
if(window.VXCharts&&window.Chart)boot();else window.addEventListener('load',boot,{once:true});
})();
</script>
"""


def render(view: str = 'screener', params=None) -> str:
    view = _VIEW_ALIASES.get(view, view)
    view = view if view in dict(_VIEWS) else 'screener'
    p = {k: v for k, v in (params or {}).items() if k in
         ('sym', 'sector', 'setup', 'decision')}
    content = (_CONTENT.replace('%%TABS%%', _tabs(view))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:120px"></div>'))
    js = (_JS.replace('%%VIEW%%', json.dumps(view))
          .replace('%%PARAMS%%', json.dumps(p)))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Opportunités · {label}', active='opportunities',
                        space_label='Opportunités', sub_label=label,
                        content=content, page_js=js,
                        page_label=f'Opportunités {label}')
