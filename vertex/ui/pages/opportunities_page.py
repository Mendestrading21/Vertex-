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

/* ── RADAR (§24) : X qualité stratégique · Y timing · taille intensité ── */
async function renderRadar(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>r.score!==undefined);
  if(!rows.length){$('op-body').innerHTML=VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
  $('op-body').innerHTML=demoBanner(scan)+'<div class="vx-grid"><div class="vx-col-8" id="op-radar"></div>'
    +'<div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Lecture</span></div>'
    +'<div class="vx-dim" style="font-size:12.5px">X : qualité stratégique (score composite moteur).<br>'
    +'Y : qualité du timing (timing technique moteur).<br>Taille : intensité du signal (anomalies).<br>'
    +'Couleur : direction du verdict.<br>Bordure orange : qualité de données dégradée.</div>'
    +'<div id="op-radar-sel" class="vx-mt3"></div></div></div>';
  VXCharts.card('op-radar',{
    title:'Radar des opportunités',question:'Où se trouvent les meilleurs couples stratégie × timing ?',
    conclusion:rows.filter(r=>bucketOf(r)==='Actionnable').length+' candidat(s) en zone actionnable',
    height:340,source:scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
    explain:{shows:'Chaque point est un titre scanné, placé par les scores moteur.',
      why:'La stratégie n’engage que lorsque qualité ET timing convergent (coin haut-droit).',
      confirm:'Un point qui migre vers le haut-droit avec volume.',
      invalidate:'Retour sous 55 en qualité stratégique.'},
    render:(cv)=>VXCharts.mount(cv,{type:'scatter',
      data:{datasets:[{data:rows.map(r=>({x:r.strat_score??r.score,y:r.st_tech??r.rs??50,sym:r.symbol,
          v:r.verdict,setup:r.playbook||r.profile||'',sector:r.sector||'',price:r.price,rr:r.rr,
          r:4+Math.min(8,(r.anomaly_score||r.sigcount||0))})),
        pointRadius:(ctx)=>ctx.raw?ctx.raw.r:4,
        pointBackgroundColor:(ctx)=>{const v=ctx.raw&&ctx.raw.v;const cc=VXCharts.colors;
          return v==='BUY'||v==='ACHETER'?cc.positive:(v==='AVOID'||v==='ÉVITER'?cc.negative:cc.info);},
        pointBorderColor:%%DEMO_BORDER%%,pointBorderWidth:1}]},
      options:{scales:{x:{title:{display:true,text:'Qualité stratégique'},grid:{color:'rgba(255,255,255,.06)'}},
        y:{title:{display:true,text:'Qualité du timing'},grid:{color:'rgba(255,255,255,.06)'}}},
        onClick:(evt,els,chart)=>{const pts=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
          if(pts.length){const d=chart.data.datasets[0].data[pts[0].index];
            document.getElementById('op-radar-sel').innerHTML=
              `<div class="vx-flex"><span class="vx-ticker" style="font-size:16px">${d.sym}</span>${window.VXEntities.badges(d.sym)}
                 <span class="vx-badge vx-badge-decision vx-right" data-decision="${d.v||''}">${d.v||'n/d'}</span></div>
               <div class="vx-kv vx-mt2"><span class="k">Score stratégique</span><span class="v vx-mono">${VX.fmt.nd(d.x)}</span></div>
               <div class="vx-kv"><span class="k">Timing</span><span class="v vx-mono">${VX.fmt.nd(d.y)}</span></div>
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
        plugins:{tooltip:{callbacks:{label:(ctx)=>`${ctx.raw.sym} · stratégie ${ctx.raw.x} · timing ${ctx.raw.y}`}}}}})});
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
        <td data-label="Score" class="vx-num">${VX.fmt.nd(r.score)}</td>
        <td data-label="Décision"><span class="vx-badge">${esc(r.verdict||'')}</span></td>
        <td data-label="Cours" class="vx-num">${VX.fmt.nd(r.price!==undefined?VX.fmt.price(r.price):null)}</td>
        <td data-label="R:R" class="vx-num">${VX.fmt.nd(r.rr)}</td>
        <td data-label="Setup" class="vx-truncate" style="max-width:130px">${esc(r.playbook||r.profile||'—')}</td>
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
      <tbody>${f.slice(0,50).map((c,i)=>`<tr data-clickable data-ct="${board.indexOf(c)}">
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
    document.querySelectorAll('[data-ct]').forEach(tr=>tr.addEventListener('click',(e)=>{
      if(e.target.closest('[data-open-analysis],[data-entity-menu]'))return;
      openContract(board[+tr.dataset.ct]);}));
  }
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar">
      ${['BALANCED','DYNAMIC','ULTRA_CONVEX'].map(c=>`<button class="vx-chip" data-filter-key="setup"
        data-filter-value="${c}" aria-pressed="${state.cat===c}">${c}</button>`).join('')}
      <input class="vx-input" data-filter-key="sym" style="width:120px;text-transform:uppercase"
        placeholder="Ticker" value="${esc(state.sym)}" aria-label="Filtrer par ticker">
      <span class="vx-meta">Greeks complets (gamma/theta/vega) : disponibles à la simulation du contrat — le board legacy n'expose que le delta.</span>
    </div>
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
                   "(window.__vxStatus&&window.__vxStatus.demo)?'#F59E42':'rgba(255,255,255,.25)'"))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Opportunités · {label}', active='opportunities',
                        space_label='Opportunités', sub_label=label,
                        content=content, page_js=js,
                        page_label=f'Opportunités {label}')
