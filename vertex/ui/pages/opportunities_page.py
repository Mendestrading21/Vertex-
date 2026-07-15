"""vertex.ui.pages.opportunities_page — découverte actions & options (§24).

Question : « Quelles opportunités méritent réellement une analyse ? »
Sous-vues : radar, stocks, options, anomalies, calendar.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell

_VIEWS = (('radar', 'Radar'), ('stocks', 'Actions'), ('options', 'Options'),
          ('anomalies', 'Anomalies'), ('calendar', 'Calendrier'))


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
<div id="op-body" class="vx-mt4">%%LOADING%%</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/timeline-chart.js" defer></script>
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
<script src="/static/vertex/js/charts/option-payoff.js" defer></script>
<script src="/static/vertex/js/charts/option-scenarios.js" defer></script>
<script src="/static/vertex/js/charts/option-theta.js" defer></script>
<script src="/static/vertex/js/charts/option-iv-sensitivity.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW=%%VIEW%%;const PARAMS=%%PARAMS%%;
const $=(id)=>document.getElementById(id);
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
/* Libellé de playbook robuste : r.playbook peut être un OBJET {name,desc,ic}
   (→ « [object Object] » si passé brut à esc) ou une chaîne ; sinon r.profile. */
function pbText(r){const p=r&&r.playbook;
  const s=(p&&typeof p==='object')?(p.name||p.desc||''):(typeof p==='string'?p:'');
  return s||(r&&typeof r.profile==='string'?r.profile:'');}
function pbIcon(r){const p=r&&r.playbook;return (p&&typeof p==='object'&&p.ic)?p.ic:'';}
/* Direction du verdict → jauge de confiance (émeraude/corail/acier). */
function verdictDir(v){return (v==='BUY'||v==='ACHETER')?'up':(v==='AVOID'||v==='ÉVITER')?'down':'flat';}
function verdictWord(v){return (v==='BUY'||v==='ACHETER')?'Achat':(v==='AVOID'||v==='ÉVITER')?'Éviter':'Suivi';}
/* Cellule heat-bar : nombre + barre inline color-codée (score 0-100, R:R…).
   opts:{label,max,good,mid,fmt}. Repli « — » honnête. */
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
const OUT=['Rejetée','Radar','À surveiller','Proche','Actionnable','Invalidée'];
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

/* ── CLASSEMENT : décomposition du score (§19.3) — barres de sous-scores moteur ── */
function scoreBar(label,val,color){
  if(val===null||val===undefined||isNaN(val))return `<div style="display:flex;align-items:center;gap:6px;margin:2px 0">
    <span style="width:82px;font-size:10.5px;color:var(--vx-text-muted,#817d77)">${label}</span>
    <span class="vx-muted" style="flex:1;font-size:10.5px">n/d</span></div>`;
  const v=Math.max(0,Math.min(100,val));
  return `<div style="display:flex;align-items:center;gap:6px;margin:2px 0" role="img" aria-label="${label} ${Math.round(v)} sur 100">
    <span style="width:82px;font-size:10.5px;color:var(--vx-text-muted,#817d77)">${label}</span>
    <span style="flex:1;height:6px;background:var(--vx-surface-3,#17191c);border-radius:4px;overflow:hidden">
      <span style="display:block;height:100%;width:${v}%;background:${color};border-radius:4px"></span></span>
    <span style="width:26px;text-align:right;font-size:10.5px;font-variant-numeric:tabular-nums;color:var(--vx-text-secondary,#b7b2aa)">${Math.round(v)}</span></div>`;
}
/* Sparkline compacte (60 dernières clôtures réelles du scan) — vert si la série
   monte, corail si elle baisse ; rien si la série manque (aucune invention). */
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
/* Bande des 5 dimensions du scoring (mini-colonnes C·M·T·F·R) — couleur par
   niveau (risque inversé). Tooltip = nom + valeur. Rien si tout manque. */
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
/* Top Opportunities (§17) : cartes des meilleurs candidats — actionnables d'abord */
function renderTopCards(rows,detail){
  const el=$('op-topcards');if(!el)return;
  detail=detail||{};
  const prio=(r)=>bucketOf(r)==='Actionnable'?0:bucketOf(r)==='Proche'?1:bucketOf(r)==='À surveiller'?2:3;
  const ranked=(rows||[]).filter(r=>r.verdict!=='AVOID'&&r.verdict!=='ÉVITER')
    .slice().sort((a,b)=>prio(a)-prio(b)||(b.score||0)-(a.score||0)).slice(0,6);
  if(!ranked.length){el.innerHTML='';return;}
  el.innerHTML='<div class="vx-card-header" style="padding:0 0 8px"><span class="vx-card-title">Top opportunités — les mieux notées</span>'
    +'<span class="vx-chart-question">Lesquelles méritent ton attention en premier ?</span></div>'
    +'<div class="vx-grid vx-mb3">'+ranked.map(function(r){const dec=r.verdict||'';
    const gauge=(window.VXCharts&&VXCharts.confidenceGaugeSVG&&r.score!=null)
      ?VXCharts.confidenceGaugeSVG(r.score,verdictDir(dec),{size:78,stroke:7,dirLabel:verdictWord(dec)}):'';
    const pb=pbText(r);const ic=pbIcon(r);
    const ser=detail[r.symbol]&&detail[r.symbol].series;
    const spark=sparkMini(ser&&ser.close);
    return `<div class="vx-card vx-col-4 vx-card--premium" style="grid-column:span 4" aria-label="${r.symbol}">
      <div class="vx-flex" style="align-items:flex-start;gap:.6rem">
        <div style="min-width:0;flex:1">
          <div class="vx-flex" style="gap:.4rem"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" style="font-size:16px;padding-left:0" data-open-analysis="${r.symbol}">${r.symbol}</button>
            <span class="vx-badge">${bucketOf(r)}</span></div>
          <div class="vx-mono vx-mt1" style="font-size:18px;font-weight:700;color:var(--vx-text-primary,#f4f1ec)">${r.price!==null&&r.price!==undefined?'$'+VX.fmt.price(r.price):'—'}</div>
          ${spark}
        </div>
        <div style="flex:0 0 auto">${gauge}</div>
      </div>
      ${dimStrip(r)}
      <div class="vx-flex vx-wrap vx-mt1" style="gap:.3rem">
        ${dec?`<span class="vx-badge vx-badge-decision" data-decision="${esc(dec)}">${esc(dec)}</span>`:''}
        ${r.rr!==null&&r.rr!==undefined?`<span class="vx-meta">R:R ${VX.fmt.nd(r.rr)}</span>`:''}
        ${r.sector?`<span class="vx-meta vx-truncate" style="max-width:110px">${esc(r.sector)}</span>`:''}</div>
      ${pb?`<div class="vx-meta vx-truncate vx-mt1">${ic?esc(ic)+' ':''}${esc(pb)}</div>`:''}
      <div class="vx-flex vx-wrap vx-mt2" style="gap:.3rem">
        <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${r.symbol}">Analyser</button>
        <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${r.symbol}','follow')">Suivre</button>
        <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${r.symbol}','alert')">Alerte</button>
        <a class="vx-btn vx-btn-sm vx-btn-ghost" target="_blank" rel="noopener" href="https://www.tradingview.com/chart/?symbol=${r.symbol}">TV ↗</a>
      </div></div>`;}).join('')+'</div>';
}
function renderRanking(rows){
  const el=$('op-ranking');if(!el||!window.VXCharts)return;
  const cc=VXCharts.colors;
  const top=(rows||[]).filter(r=>r.st_fund!=null||r.st_tech!=null||r.st_mom!=null)
    .slice().sort((a,b)=>(b.score||0)-(a.score||0)).slice(0,6);
  if(!top.length){el.innerHTML='';return;}
  el.innerHTML='<div class="vx-card"><div class="vx-chart-head"><span class="vx-chart-title">Classement — décomposition du score</span>'
    +'<span class="vx-chart-question">Pourquoi ces titres sortent-ils du lot ?</span></div>'
    +top.map(function(r){return '<div style="padding:9px 0;border-bottom:1px dashed var(--vx-border-soft,rgba(255,255,255,.065))">'
      +'<div class="vx-flex"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="'+r.symbol+'">'+r.symbol+'</button>'
      +'<span class="vx-badge">'+esc(r.verdict||'')+'</span>'
      +(r.sector?'<span class="vx-meta vx-truncate" style="max-width:120px">'+esc(r.sector)+'</span>':'')
      +'<span class="vx-grow"></span><span class="vx-mono" style="font-size:16px;font-weight:800;color:var(--vx-text-primary,#f3f1ed)">'+VX.fmt.nd(r.score)+'</span></div>'
      +'<div class="vx-mt1">'
        +scoreBar('Fondamental',r.st_fund,cc.positive)
        +scoreBar('Technique',r.st_tech,cc.cyan)
        +scoreBar('Momentum',r.st_mom,cc.warning)
        +scoreBar('Risque',r.st_risk,cc.negative)
      +'</div></div>';}).join('')
    +'<div class="vx-card-foot"><span class="vx-meta">Sous-scores du moteur de scoring (technical/momentum/fundamental/risk) — aucune pondération inventée.</span></div></div>';
}

/* ── ENTONNOIR D'OPPORTUNITÉS (§11-12) : univers → … → actionnable ── */
async function renderFunnel(){
  const el=$('op-funnel');if(!el)return;
  let f;try{f=await VX.fetch('/api/opportunities/funnel',{ttl:60000});}catch(e){return;}
  if(!f||!f.stages||!f.stages.length)return;
  const roleColor={'ATTAQUE':'var(--vx-positive,#36c889)','MILIEU':'var(--vx-beige,#c8ad8d)',
    'DÉFENSE':'var(--vx-neutral,#8f8a83)','RÉSERVE':'var(--vx-text-dim,#817d77)'};
  const roles=(f.roles||[]).map(function(r){
    return '<span class="vx-chip" style="border:1px solid '+ (roleColor[r.role]||'#555')
      +';color:'+(roleColor[r.role]||'#aaa')+'">'+esc(r.role)+' '+esc(r.count)+'</span>';
  }).join(' ');
  el.innerHTML='<div class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Entonnoir d\'opportunités</span>'
    +'<span class="vx-actions" style="display:flex;gap:.4rem;flex-wrap:wrap">'+roles+'</span></div>'
    +'<div id="op-funnel-viz" style="margin-top:.4rem"></div>'
    +(f.note?'<div class="vx-dim" style="font-size:12px;margin-top:.5rem">'+esc(f.note)+'</div>':'')
    +(f.actionable_symbols&&f.actionable_symbols.length?'<div class="vx-dim" style="font-size:12px;margin-top:.5rem">Actionnables : '
      +f.actionable_symbols.map(function(s){return '<b style="color:var(--vx-positive,#36c889)">'+esc(s)+'</b>';}).join(' · ')+'</div>':'')
    +'</div>';
  /* Vrai entonnoir décroissant (trapèzes + % par étage) au lieu des colonnes texte —
     donnée réelle /api/opportunities/funnel, jamais inventée ; le composant gère
     lui-même le repli si < 2 étages. */
  if(window.VXCharts&&VXCharts.funnel){
    VXCharts.funnel('op-funnel-viz',{stages:f.stages.map(function(s){return {label:s.label,value:s.count};}),
      fmt:function(v){return VX.fmt.nd(v);},ariaLabel:'Entonnoir d\'opportunités : univers vers actionnables'});
  }
}

/* ── RADAR (§24) : X qualité stratégique · Y timing · taille intensité ── */
async function renderRadar(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>r.score!==undefined);
  if(!rows.length){$('op-body').innerHTML=VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
  $('op-body').innerHTML=demoBanner(scan)+'<div id="op-topcards"></div><div id="op-funnel" class="vx-mb3"></div><div class="vx-grid"><div class="vx-col-8" id="op-radar"></div>'
    +'<div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Lecture</span></div>'
    +'<div class="vx-dim" style="font-size:12.5px">X : qualité stratégique (score composite moteur).<br>'
    +'Y : qualité du timing (timing technique moteur).<br>Taille : intensité du signal (anomalies).<br>'
    +'Couleur : direction du verdict (émeraude = achat · corail = éviter · acier = neutre).<br>Bordure ambre : qualité de données dégradée (démo).</div>'
    +'<div id="op-radar-sel" class="vx-mt3"></div></div></div>'
    +'<div id="op-ranking" class="vx-mt4"></div>';
  renderTopCards(rows,scan.detail||{});
  renderFunnel();
  renderRanking(rows);
  VXCharts.card('op-radar',{
    title:'Radar des opportunités',question:'Où se trouvent les meilleurs couples stratégie × timing ?',
    conclusion:rows.filter(r=>bucketOf(r)==='Actionnable').length+' candidat(s) en zone actionnable',
    height:340,source:scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
    explain:{shows:'Chaque point est un titre scanné, placé par les scores moteur.',
      why:'La stratégie n’engage que lorsque qualité ET timing convergent (coin haut-droit).',
      confirm:'Un point qui migre vers le haut-droit avec volume.',
      invalidate:'Retour sous 55 en qualité stratégique.'},
    render:(cv)=>VXCharts.mount(cv,{type:'scatter',
      data:{datasets:[{data:rows.map(r=>{const _t=(r.st_tech??r.rs);return {x:r.strat_score??r.score,y:(_t??50),tOk:_t!=null,sym:r.symbol,
          v:r.verdict,setup:pbText(r),sector:r.sector||'',price:r.price,rr:r.rr,
          r:4+Math.min(8,(r.anomaly_score||r.sigcount||0))};}),
        pointRadius:(ctx)=>ctx.raw?ctx.raw.r:4,
        pointBackgroundColor:(ctx)=>{const v=ctx.raw&&ctx.raw.v;const cc=VXCharts.colors;
          return v==='BUY'||v==='ACHETER'?cc.positive:(v==='AVOID'||v==='ÉVITER'?cc.negative:cc.neutral);},
        pointBorderColor:%%DEMO_BORDER%%,pointBorderWidth:1}]},
      options:{scales:{x:{title:{display:true,text:'Qualité stratégique'},grid:{color:'rgba(255,255,255,.06)'}},
        y:{title:{display:true,text:'Qualité du timing'},grid:{color:'rgba(255,255,255,.06)'}}},
        onClick:(evt,els,chart)=>{const pts=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
          if(pts.length){const d=chart.data.datasets[0].data[pts[0].index];
            document.getElementById('op-radar-sel').innerHTML=
              `<div class="vx-flex"><span class="vx-ticker" style="font-size:16px">${d.sym}</span>${window.VXEntities.badges(d.sym)}
                 <span class="vx-badge vx-badge-decision vx-right" data-decision="${d.v||''}">${d.v||'n/d'}</span></div>
               <div class="vx-kv vx-mt2"><span class="k">Score stratégique</span><span class="v vx-mono">${VX.fmt.nd(d.x)}</span></div>
               <div class="vx-kv"><span class="k">Timing</span><span class="v vx-mono">${d.tOk?VX.fmt.nd(d.y):'n/d'}</span></div>
               <div class="vx-kv"><span class="k">Cours</span><span class="v vx-mono">${d.price!==undefined&&d.price!==null?VX.fmt.price(d.price):'n/d'}</span></div>
               <div class="vx-kv"><span class="k">R:R plan</span><span class="v vx-mono">${VX.fmt.nd(d.rr)}</span></div>
               ${d.setup?`<div class="vx-kv"><span class="k">Setup</span><span class="v">${d.setup}</span></div>`:''}
               ${d.sector?`<div class="vx-kv"><span class="k">Secteur</span><span class="v">${d.sector}</span></div>`:''}
               <div class="vx-flex vx-wrap vx-mt2">
                 <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${d.sym}">Analyse</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.toggleFavorite('${d.sym}')">★ Favori</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${d.sym}','watchlist')">Watchlist</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${d.sym}','follow')">Suivi</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${d.sym}','alert')">Alerte</button>
                 <a class="vx-btn vx-btn-sm" href="/opportunities?view=options&sym=${d.sym}">Options</a>
                 <button class="vx-btn vx-btn-sm vx-btn-ghost" data-entity-menu="${d.sym}">Plus ▾</button></div>`;}},
        plugins:{tooltip:{callbacks:{label:(ctx)=>`${ctx.raw.sym} · stratégie ${ctx.raw.x} · timing ${ctx.raw.tOk?ctx.raw.y:'n/d'}`}}}}})});
}

/* ── ACTIONS ── */
async function renderStocks(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  let rows=(scan.rows||[]);
  const sectors=[...new Set(rows.map(r=>r.sector).filter(Boolean))].sort();
  const state={bucket:PARAMS.decision||'',sector:PARAMS.sector||'',setup:PARAMS.setup||'',minScore:0};
  function paint(){
    let f=rows;
    if(state.sector)f=f.filter(r=>r.sector===state.sector);
    if(state.bucket)f=f.filter(r=>bucketOf(r)===state.bucket);
    if(state.setup)f=f.filter(r=>(r.playbook||r.profile||'').toUpperCase().includes(state.setup));
    if(state.minScore)f=f.filter(r=>(r.score||0)>=state.minScore);
    f=f.slice().sort((a,b)=>(b.score||0)-(a.score||0));
    $('op-table').innerHTML=f.length?`<table class="vx-table"><thead><tr>
      <th>Titre</th><th>Statut</th><th class="vx-num" data-sortable>Score</th><th>Décision moteur</th>
      <th class="vx-num">Cours</th><th class="vx-num">R:R</th><th>Setup</th><th>Secteur</th><th></th></tr></thead><tbody>
      ${f.slice(0,80).map(r=>`<tr data-clickable data-open-analysis="${r.symbol}">
        <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span></td>
        <td data-label="Statut"><span class="vx-badge">${bucketOf(r)}</span></td>
        ${heatCell(r.score,{label:'Score',good:72,mid:56})}
        <td data-label="Décision"><span class="vx-badge vx-badge-decision" data-decision="${esc(r.verdict||'')}">${esc(r.verdict||'')}</span></td>
        <td data-label="Cours" class="vx-num">${VX.fmt.nd(r.price!==undefined?VX.fmt.price(r.price):null)}</td>
        ${heatCell(r.rr,{label:'R:R',max:3,good:2,mid:1,fmt:v=>VX.fmt.num(v,1)})}
        <td data-label="Setup" class="vx-truncate" style="max-width:140px">${esc(pbText(r)||'—')}</td>
        <td data-label="Secteur">${esc(r.sector||'—')}</td>
        <td>${rowActions(r.symbol)}</td></tr>`).join('')}</tbody></table>`
      :VX.states.empty('Aucun titre ne correspond aux filtres.','<button class="vx-btn vx-btn-sm" id="op-clear">Effacer les filtres</button>');
    document.getElementById('op-clear')?.addEventListener('click',()=>{Object.keys(state).forEach(k=>state[k]='');paint();});
  }
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar" role="group" aria-label="Filtres">
      ${OUT.map(b=>`<button class="vx-chip" data-filter-key="decision" data-filter-value="${b}"
        aria-pressed="${state.bucket===b}">${b}</button>`).join('')}
      <select class="vx-select" data-filter-key="sector" style="width:auto" aria-label="Secteur">
        <option value="">Tous secteurs</option>${sectors.map(s=>`<option ${state.sector===s?'selected':''}>${s}</option>`).join('')}</select>
      <input class="vx-input" data-filter-key="setup" style="width:150px" placeholder="setup (BREAKOUT…)" value="${esc(state.setup)}" aria-label="Setup">
    </div>
    <div class="vx-table-wrap vx-table-cards" id="op-table"></div>
    <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.source,metaMode(scan))}
      · ${rows.length} titres scannés</div>`;
  document.querySelectorAll('[data-filter-key="decision"]').forEach(c=>c.addEventListener('click',()=>{
    state.bucket=state.bucket===c.dataset.filterValue?'':c.dataset.filterValue;
    document.querySelectorAll('[data-filter-key="decision"]').forEach(x=>
      x.setAttribute('aria-pressed',String(x.dataset.filterValue===state.bucket)));paint();}));
  document.querySelector('[data-filter-key="sector"]').addEventListener('change',function(){state.sector=this.value;paint();});
  document.querySelector('[data-filter-key="setup"]').addEventListener('input',function(){state.setup=this.value.toUpperCase();paint();});
  paint();
  VX.context.restoreIfReturning();
}

/* ── OPTIONS (§24/§35) ── */
async function renderOptions(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const board=(scan.options_board||[]);
  /* Comparateur §22 : 3 contrats max — défensif (BALANCED) / principal
     (DYNAMIC) / explosif (ULTRA_CONVEX) — dominance expliquée, jamais
     d'exécution. */
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
      <td class="vx-num">${c.spread_pct!=null?c.spread_pct+'%':'—'}</td>
      <td class="vx-num">${VX.fmt.nd(c.oi)}</td>
      <td class="vx-num"><b>${VX.fmt.nd(c.quality)}</b></td></tr>`:'';
    const main=avail.find(([l])=>l.startsWith('PRINCIPAL'))||avail[0];
    const others=avail.filter(x=>x!==main);
    const why=others.map(([l,c])=>{
      const m=main[1];const wins=[];
      if((c.delta||0)>(m.delta||0))wins.push('delta plus élevé (plus défensif)');
      if((c.cost||1e9)<(m.cost||1e9))wins.push('prime plus faible (plus convexe)');
      if((c.oi||0)>(m.oi||0))wins.push('OI supérieur');
      return `<li><b>${l}</b> : ${wins.length?('gagne sur '+wins.join(', ')):'ne domine sur aucune dimension clé'} — mais qualité globale ${VX.fmt.nd(c.quality)} vs ${VX.fmt.nd(m[1]?m[1].quality:m.quality??'')}.</li>`;
    }).join('');
    VX.shell.openDrawer('Comparateur de contrats'+(symWanted?' — '+symWanted:''),
      `<div class="vx-table-wrap"><table class="vx-table"><thead><tr>
        <th>Contrat</th><th class="vx-num">Δ</th><th class="vx-num">DTE</th><th class="vx-num">IV</th>
        <th class="vx-num">Prime</th><th class="vx-num">Spread</th><th class="vx-num">OI</th>
        <th class="vx-num">Qualité</th></tr></thead>
        <tbody>${avail.map(([l,c])=>row(l,c)).join('')}</tbody></table></div>
       <div class="vx-insight vx-mt3"><b>Pourquoi ${main[0]} domine</b>
         <div class="vx-mt1" style="font-size:12.5px">Frontière de Pareto : le contrat principal offre le meilleur
         score composite (R:R simulé × liquidité × coût du temps). Les alternatives gagnent chacune sur UNE
         dimension mais en sacrifient d'autres :</div>
         <ul class="vx-mt1" style="margin:0;padding-left:18px;font-size:12.5px">${why||'<li>aucune alternative disponible</li>'}</ul></div>
       <div class="vx-help vx-mt2">Analyse uniquement — copier le contrat pour le consulter chez le broker.</div>`);
  };
  const symFilter=(PARAMS.sym||'').toUpperCase();
  const state={cat:PARAMS.setup||'',sym:symFilter};
  function catOf(c){const d=Math.abs(c.delta||0);
    if(d>=0.40&&d<=0.60)return'BALANCED';if(d>=0.28&&d<0.45)return'DYNAMIC';
    if(d>=0.18&&d<0.30)return'ULTRA_CONVEX';return'AUTRE';}
  function paint(){
    let f=board;
    if(state.sym)f=f.filter(c=>c.sym===state.sym);
    if(state.cat)f=f.filter(c=>catOf(c)===state.cat);
    $('op-opt-table').innerHTML=f.length?`<table class="vx-table"><thead><tr>
      <th>Sous-jacent</th><th>Catégorie</th><th class="vx-num">Strike</th><th>Échéance</th>
      <th class="vx-num">DTE</th><th class="vx-num">Delta</th><th class="vx-num">IV</th>
      <th class="vx-num">Prime</th><th class="vx-num">Spread</th><th class="vx-num">Volume</th>
      <th class="vx-num">OI</th><th class="vx-num">Breakeven</th><th class="vx-num">R:R cible</th><th></th></tr></thead>
      <tbody>${f.slice(0,50).map((c,i)=>`<tr data-clickable data-ct="${board.indexOf(c)}" tabindex="0" role="button" aria-label="Simuler ${esc(c.sym)} ${VX.fmt.nd(c.strike)}">
        <td data-label="Sous-jacent"><span class="vx-ticker">${c.sym}</span></td>
        <td data-label="Catégorie"><span class="vx-badge" style="color:var(--vx-violet)">${catOf(c)}</span></td>
        <td data-label="Strike" class="vx-num">${VX.fmt.nd(c.strike)}</td>
        <td data-label="Échéance" class="vx-mono">${VX.fmt.nd(c.exp)}</td>
        <td data-label="DTE" class="vx-num">${VX.fmt.nd(c.dte)}</td>
        <td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
        <td data-label="IV" class="vx-num">${c.iv!=null?(c.iv*100).toFixed(0)+'%':'—'}</td>
        <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.cost)}</td>
        <td data-label="Spread" class="vx-num">${c.spread_pct!=null?c.spread_pct+'%':'—'}</td>
        <td data-label="Volume" class="vx-num">${VX.fmt.nd(c.vol)}</td>
        <td data-label="OI" class="vx-num">${VX.fmt.nd(c.oi)}</td>
        <td data-label="Breakeven" class="vx-num">${VX.fmt.nd(c.be)}</td>
        <td data-label="R:R" class="vx-num">${VX.fmt.nd(c.p_tgt)}</td>
        <td>${rowActions(c.sym)}</td></tr>`).join('')}</tbody></table>`
      :VX.states.empty(state.sym?'Aucun contrat pour '+state.sym+' dans le board courant.':'Board options vide — le sélecteur ne force jamais une idée.',
        '<a class="vx-btn vx-btn-sm" href="/system?view=data">Vérifier les données</a>');
    document.querySelectorAll('[data-ct]').forEach(tr=>{
      const open=(e)=>{if(e.target.closest('[data-open-analysis],[data-entity-menu]'))return;openContract(board[+tr.dataset.ct]);};
      tr.addEventListener('click',open);
      tr.addEventListener('keydown',(e)=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(e);}});});
  }
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar">
      ${['BALANCED','DYNAMIC','ULTRA_CONVEX'].map(c=>`<button class="vx-chip" data-filter-key="setup"
        data-filter-value="${c}" aria-pressed="${state.cat===c}">${c}</button>`).join('')}
      <input class="vx-input" data-filter-key="sym" style="width:120px;text-transform:uppercase"
        placeholder="Ticker" value="${esc(state.sym)}" aria-label="Filtrer par ticker">
      <span class="vx-meta">Greeks complets (gamma/theta/vega) : disponibles à la simulation du contrat — le board legacy n'expose que le delta.</span>
    </div>
    <div class="vx-flex vx-mb2" style="gap:.5rem;flex-wrap:wrap"><button class="vx-btn vx-btn-sm vx-btn-soft" id="op-compare"
      onclick="window.__opCompare&&window.__opCompare((new URLSearchParams(location.search)).get('sym')||'')">
      Comparer 3 contrats (défensif · principal · explosif)</button>
      <a class="vx-btn vx-btn-sm" href="/options">Options Intelligence →</a></div>
    <div class="vx-table-wrap vx-table-cards" id="op-opt-table"></div>
    <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.options_source||scan.source,metaMode(scan))}</div>
    <div class="vx-grid vx-mt4" id="op-contract" hidden>
      <div class="vx-col-6" id="op-payoff"></div>
      <div class="vx-col-6" id="op-scenarios"></div>
      <div class="vx-col-6" id="op-theta"></div>
      <div class="vx-col-6" id="op-iv"></div>
    </div>`;
  document.querySelectorAll('[data-filter-key="setup"]').forEach(c=>c.addEventListener('click',()=>{
    state.cat=state.cat===c.dataset.filterValue?'':c.dataset.filterValue;
    document.querySelectorAll('[data-filter-key="setup"]').forEach(x=>
      x.setAttribute('aria-pressed',String(x.dataset.filterValue===state.cat)));paint();}));
  document.querySelector('[data-filter-key="sym"]').addEventListener('input',function(){state.sym=this.value.toUpperCase();paint();});
  paint();
  async function openContract(c){
    $('op-contract').hidden=false;
    $('op-contract').scrollIntoView({behavior:'smooth',block:'nearest'});
    VXCharts.payoffCard('op-payoff',{title:`${c.sym} ${c.strike} CALL ${c.exp}`,
      question:'Que rapporte/coûte ce contrat à l’échéance ?',
      conclusion:`Breakeven ${VX.fmt.nd(c.be)} · prime ${VX.fmt.nd(c.cost)}`,
      spot:c.spot,strike:c.strike,premium:c.cost,right:'C',breakeven:c.be,height:210,
      source:'board options',timestamp:Date.now(),mode:'delayed',
      explain:{shows:'Le P&L du CALL à l’échéance selon le prix du sous-jacent (arithmétique du contrat).',
        why:'Visualiser breakeven et asymétrie avant d’engager la prime.',
        confirm:'Sous-jacent au-dessus du breakeven avant l’échéance.',
        invalidate:'Stop sous-jacent touché — on ne « garde pas en espérant ».'}});
    try{
      const q=new URLSearchParams({sym:c.sym,strike:c.strike,dte:c.dte,mid:c.cost,
        iv:c.iv||'',right:'C',exp:c.exp,spot:c.spot||''});
      const s=await VX.fetch('/api/options/simulate?'+q.toString(),{ttl:120000});
      VXCharts.scenarioMatrix('op-scenarios',s.sim,{title:'Scénarios (moteur)',
        question:'Que vaut le contrat selon le spot et le temps ?',
        conclusion:`R:R simulé ${VX.fmt.nd(s.sim.reward_risk)} · perte planifiée ${VX.fmt.nd(s.sim.worst_planned_loss_pct)} %`,
        source:'scenario_pricer',timestamp:Date.now(),mode:'delayed'});
      VXCharts.thetaCard('op-theta',s.sim,{title:'Décomposition temps',
        question:'Combien coûte chaque jour d’attente ?',
        conclusion:'Time stop conseillé : réévaluer après 5-8 séances sans mouvement',
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
}

/* ── ANOMALIES ── */
async function renderAnomalies(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>(r.anomalies||[]).length);
  const groups={Actions:rows};
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar">${['Actions','Options','Données','Volatilité','Portefeuille','Modèles']
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
    }else if(group==='Données'){
      VX.fetch('/api/data-quality',{ttl:60000}).then(dq=>{
        $('op-anom').innerHTML=`<div class="vx-card">${Object.entries(dq.by_quality||{}).map(([k,v])=>
          `<div class="vx-kv"><span class="k">${k}</span><span class="v">${v}</span></div>`).join('')}
          <div class="vx-meta vx-mt2">${esc(dq.note||'')}</div></div>`;
      }).catch(()=>{$('op-anom').innerHTML=VX.states.error('Qualité de données indisponible');});
    }else{
      $('op-anom').innerHTML=VX.states.empty(`Anomalies « ${group} » : détectées par symbole — ouvrir une analyse pour le détail (moteurs option_anomalies / vol_surface / portefeuille).`,
        '<button class="vx-btn vx-btn-sm" onclick="document.getElementById(\'vx-global-search\').click()">Chercher un titre</button>');
    }
  }
  document.querySelectorAll('[data-ag]').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('[data-ag]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    paint(b.dataset.ag);}));
  paint('Actions');
}

/* ── CALENDRIER ── */
async function renderCalendar(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const positions=(window.VXEntities?window.VXEntities.positions():[]).map(p=>p.sym);
    const items=[...(cal.macro||[]).map(m=>({when:m.date,kind:m.kind,label:esc(m.label)+(m.note?' — '+esc(m.note):'')+(m.approx?' (approx.)':'')})),
      ...(cal.items||[]).map(it=>({when:it.date,kind:'Earnings',sym:it.sym,
        label:`résultats dans ${it.dte} j · verdict moteur ${esc(it.verdict||'n/d')}`
          +(positions.includes(it.sym)?' · <b class="vx-warn">position exposée</b>':'')}))]
      .sort((a,b)=>String(a.when).localeCompare(String(b.when)));
    $('op-body').innerHTML='<div id="op-cal"></div>';
    VXCharts.timelineCard('op-cal',{title:'Calendrier des catalyseurs',
      question:'Quels événements peuvent faire bouger les dossiers ?',
      items:items.slice(0,30),source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun événement identifié sur l’horizon.'});
  }catch(e){$('op-body').innerHTML=VX.states.error('Calendrier indisponible');}
}

const RENDER={radar:renderRadar,stocks:renderStocks,options:renderOptions,
  anomalies:renderAnomalies,calendar:renderCalendar};
function boot(){(RENDER[VIEW]||renderRadar)().catch(e=>{
  $('op-body').innerHTML=VX.states.error('Chargement impossible : '+e.message);});}
if(window.VXCharts&&window.Chart)boot();else window.addEventListener('load',boot,{once:true});
})();
</script>
"""


def render(view: str = 'radar', params=None) -> str:
    view = view if view in dict(_VIEWS) else 'radar'
    p = {k: v for k, v in (params or {}).items() if k in
         ('sym', 'sector', 'setup', 'decision')}
    content = (_CONTENT.replace('%%TABS%%', _tabs(view))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:120px"></div>'))
    js = (_JS.replace('%%VIEW%%', json.dumps(view))
          .replace('%%PARAMS%%', json.dumps(p))
          .replace('%%DEMO_BORDER%%',
                   "(window.__vxStatus&&window.__vxStatus.demo)?'#dda23b':'rgba(255,255,255,.25)'"))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Opportunités · {label}', active='opportunities',
                        space_label='Opportunités', sub_label=label,
                        content=content, page_js=js,
                        page_label=f'Opportunités {label}')
