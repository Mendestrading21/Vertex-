"""vertex.ui.pages.portfolio_page — Équipe Vertex (§25).

Question : « Que possède le portefeuille et comment doit-il évoluer ? »
Sous-vues : team, positions, risk, watchlist. Les positions sont le registre
DÉCLARATIF de l'utilisateur (myTrades) + IBKR lecture seule — jamais un ordre.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell

_VIEWS = (('team', 'Équipe'), ('positions', 'Positions'), ('options', 'Options'),
          ('risk', 'Risque'), ('watchlist', 'Watchlist'))


def _tabs(view: str) -> str:
    return ('<div class="vx-tabs" role="tablist">'
            + ''.join(f'<a class="vx-tab" role="tab" aria-selected='
                      f'"{"true" if v == view else "false"}" '
                      f'href="/portfolio?view={v}">{label}</a>'
                      for v, label in _VIEWS) + '</div>')


_CONTENT = """
<div class="vx-page-header"><div><h1>Portefeuille</h1>
<div class="vx-sub">Que possède le portefeuille et comment doit-il évoluer ? · Vertex Team Portfolio</div></div>
<div class="vx-actions">
  <button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal('','position')">+ Position</button>
  <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('','watchlist')">+ Watchlist</button>
  <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/tracking">Suivis →</a>
</div></div>
%%TABS%%
<div class="vx-grid vx-mt4" id="pf-summary" aria-label="Synthèse portefeuille"></div>
<div id="pf-body" class="vx-mt4">%%LOADING%%</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/donut-chart.js" defer></script>
<script src="/static/vertex/js/charts/sparkline.js" defer></script>
<script src="/static/vertex/js/charts/equity-chart.js" defer></script>
<script src="/static/vertex/js/charts/option-payoff.js" defer></script>
<script src="/static/vertex/js/charts/line-area-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW=%%VIEW%%;
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function kv(k,v,cls){return `<div class="vx-kv"><span class="k">${k}</span><span class="v ${cls||''}">${VX.fmt.nd(v)}</span></div>`;}

async function quotesFor(pos){
  if(!pos.length)return{};
  try{
    /* Contrat serveur /api/pos-quotes : {positions:[{sym,exp,strike,right}]}
       → résultats indexés par clé composite 'SYM|exp|strike|RIGHT'. */
    const body=pos.map(t=>({sym:t.sym,exp:t.exp,strike:t.strike,right:t.right}));
    const r=await fetch('/api/pos-quotes',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({positions:body})});
    const d=await r.json();window.__pfLive=!!d.live;
    const res=d.results||{};const byId={};
    pos.forEach(t=>{const key=[String(t.sym).toUpperCase(),t.exp||'',
      (t.strike!==null&&t.strike!==undefined)?t.strike:'',
      (t.right||'').toUpperCase()].join('|');
      if(res[key])byId[t.id]=res[key];});
    return byId;
  }catch(e){return{};}
}
function enrich(pos,quotes){
  /* Schéma desk : t.cost = TOTAL investi. Cotes serveur : spot (actions,
     par action) · mark (options, PAR ACTION → ×100 par contrat). */
  return pos.map(t=>{
    const q=quotes[t.id]||{};
    const isOpt=t.type!=='STK';
    const mark=isOpt?(q.mark??q.last??null):(q.spot??q.mark??q.last??null);
    /* Spot du SOUS-JACENT (options) : fourni par /api/pos-quotes → centre honnête du
       payoff sur le vrai cours, plus sur le strike par défaut. Null si pas de cote. */
    const underSpot=isOpt?(q.spot??null):null;
    const value=mark!==null?(isOpt?mark*100*t.qty:mark*t.qty):null;
    const invested=t.cost||0;
    const pl=value!==null&&invested?((value-invested)/invested*100):null;
    return Object.assign({},t,{mark,underSpot,value,invested,pl});
  });
}
function roleOf(t){
  const snap=t.entrySnap||{};
  if(t.type!=='STK')return'Options tactiques';
  if((snap.score||0)>=78||(snap.verdict||'').includes('FORT'))return'Offensive';
  if(['XLU','XLP','BIL','SGOV','SHV','GLD'].includes(t.sym))return'Défense / gardien';
  return'Noyau';
}
/* Synthèse chiffrée : valeur au coût toujours calculable ; marques live si
   disponibles — jamais un chiffre inventé, l'étiquette dit ce qui est affiché. */
function renderSummary(rich){
  const host=$('pf-summary');if(!host)return;
  if(!rich.length){host.innerHTML='';return;}
  const stocks=rich.filter(t=>t.type==='STK'),opts=rich.filter(t=>t.type!=='STK');
  const invested=rich.reduce((s,t)=>s+t.invested,0);
  const marked=rich.filter(t=>t.value!==null);
  const value=marked.length===rich.length?rich.reduce((s,t)=>s+t.value,0):null;
  const pl=value!==null&&invested?(value-invested):null;
  const cell=(label,val,delta,cls)=>`<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3">
    <span class="vx-kpi-label">${label}</span>
    <span class="vx-kpi-value" style="font-size:20px">${val}</span>
    ${delta?`<span class="vx-kpi-delta ${cls||'vx-muted'}">${delta}</span>`:''}</div>`;
  host.innerHTML=
    cell('Valeur',value!==null?VX.fmt.price(value):VX.fmt.price(invested),
      value!==null?'marques live/desk':'au coût (marques indisponibles)')
    +cell('P&L latent',pl!==null?VX.fmt.price(pl):'n/d',
      pl!==null?VX.fmt.pct(pl/invested*100,1):'IBKR hors ligne',
      pl>0?'vx-pos':pl<0?'vx-neg':'vx-muted')
    +cell('Équipe actions',stocks.length+' / 10',
      stocks.length>=10?'complet — remplacement obligatoire':'places disponibles',
      stocks.length>=10?'vx-warn':'')
    +cell('Options tactiques',opts.length+' / 3',
      `CALLS ${opts.filter(t=>t.type==='CALL').length} · PUTS ${opts.filter(t=>t.type==='PUT').length} / 1 max`,
      (opts.length>=3||opts.filter(t=>t.type==='PUT').length>1)?'vx-warn':'');
}

/* ── ÉQUIPE ── */
async function renderTeam(){
  const pos=E().positions();
  if(!pos.length){
    $('pf-body').innerHTML=VX.states.empty(
      'Aucune position déclarée — l’Équipe Vertex vise 8 à 10 composantes '
      +'(Offensive 2-3 · Noyau 3-4 · Défense ~2 · Réserve).',
      '<button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>');
    return;
  }
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  const roles={'Offensive':[],'Noyau':[],'Défense / gardien':[],'Options tactiques':[]};
  rich.forEach(t=>roles[roleOf(t)].push(t));
  const totalValue=rich.reduce((s,t)=>s+(t.value??t.invested),0);
  const sub={'Offensive':'Attaquants','Noyau':'Milieux','Défense / gardien':'Défenseurs & gardien',
    'Options tactiques':'HORS équipe — jamais gardien (max 3)'};
  $('pf-body').innerHTML=`<section class="vx-card vx-mb3" aria-label="Allocation du portefeuille">
      <div class="vx-chart-head"><span class="vx-chart-title">Allocation du portefeuille</span>
        <span class="vx-chart-question">Où est concentré le capital, et qui gagne/perd ?</span></div>
      <div id="pf-alloc-tree" style="height:260px"></div>
      <div class="vx-card-foot"><span class="vx-meta">Taille = poids (valeur au marché ou au coût) · couleur = P&amp;L latent (vert gagnant / rouge perdant / gris sans marque). Positions déclarées, aucune valeur inventée.</span></div>
    </section>
    <div class="vx-grid">
    <div class="vx-col-8" id="pf-team-cols"></div>
    <div class="vx-col-4"><div id="pf-roles-donut"></div>
      <div class="vx-card vx-mt3"><div class="vx-card-header"><span class="vx-card-title">Places</span></div>
      ${kv('Composantes',rich.filter(t=>t.type==='STK').length+' / 10 max')}
      ${kv('Options ouvertes',rich.filter(t=>t.type!=='STK').length+' / 3 max',
        rich.filter(t=>t.type!=='STK').length>=3?'vx-warn':'')}
      ${kv('Règle','11e position = remplacement obligatoire')}
      <div class="vx-meta vx-mt2"><a href="/opportunities">Chercher des candidats →</a></div></div>
      <div class="vx-card vx-mt3" id="pf-contrib"><div class="vx-card-header"><span class="vx-card-title">Contributeurs</span></div>
      <div id="pf-contrib-body"></div></div></div></div>`;
  const withPl=rich.filter(t=>t.pl!==null).sort((a,b)=>b.pl-a.pl);
  /* Barre P&L par position (gagnants/perdants d'un coup d'œil) — coloration émeraude/
     corail auto par signe (C.bars). Repli honnête si aucune marque (jamais de faux 0). */
  $('pf-contrib-body').innerHTML=withPl.length
    ?'<div style="height:'+Math.max(90,Math.min(280,withPl.length*26))+'px"><canvas id="pf-contrib-cv"></canvas></div>'
    :'<div class="vx-meta">Marques indisponibles (IBKR hors ligne) — aucun P&L affiché plutôt qu’un chiffre inventé.</div>';
  if(withPl.length&&window.VXCharts&&VXCharts.bars){
    VXCharts.bars(document.getElementById('pf-contrib-cv'),withPl.map(t=>t.sym),withPl.map(t=>t.pl),
      {horizontal:true,yFmt:(v)=>v+' %'});
  }
  $('pf-team-cols').innerHTML=Object.entries(roles).map(([role,list])=>`
    <section class="vx-card vx-mb3" aria-label="${role}">
      <div class="vx-card-header"><span class="vx-card-title">${role}</span>
        <span class="vx-meta">${sub[role]}</span>
        <span class="vx-meta vx-right">${list.length} position(s)</span></div>
      ${list.length?list.map(t=>`
        <div class="vx-flex" style="padding:8px 0;border-bottom:1px dashed var(--vx-border-soft)">
          <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${t.sym}">${t.sym}</button>
          <span class="vx-badge" ${t.type!=='STK'?'style="color:var(--vx-violet)"':''}>${t.type}${t.strike?' '+t.strike:''}</span>
          <span class="vx-mono vx-meta">${totalValue?VX.fmt.num((t.value??t.invested)/totalValue*100,1)+' %':'—'}</span>
          <span class="vx-grow vx-truncate vx-dim" style="font-size:12px">${esc((t.entrySnap&&t.entrySnap.thesis)||t.note||'—')}</span>
          <span class="vx-num vx-mono ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':'vx-muted'}">${t.pl!==null?VX.fmt.pct(t.pl,1):'n/d'}</span>
          <span class="vx-mono vx-meta">stop ${VX.fmt.nd(t.entrySnap&&t.entrySnap.stop)}</span>
          <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Actions ${t.sym}">⋯</button>
        </div>`).join(''):'<div class="vx-meta">— vide —</div>'}
    </section>`).join('');
  /* Treemap d'allocation (§20 — remplace le donut seul) : taille = poids, couleur = P&L */
  if(window.VXCharts&&VXCharts.treemap){
    const cc=VXCharts.colors;
    const el=document.getElementById('pf-alloc-tree');
    const w=(el&&el.clientWidth)||900;
    VXCharts.treemap(el,{width:w,height:260,
      items:rich.map(t=>({label:t.sym,value:Math.max(1,t.value??t.invested??0),
        sub:(t.pl!=null?((t.pl>=0?'+':'')+VX.fmt.num(t.pl,1)+'%'):(t.type!=='STK'?t.type:'')),
        color:(t.pl>0?cc.positive:t.pl<0?cc.negative:cc.neutral)})),
      fmt:(v)=>VX.fmt.price(v)});
  }
  const counts=Object.entries(roles).filter(([,l])=>l.length);
  if(counts.length&&window.VXCharts&&VXCharts.donutCard)VXCharts.donutCard('pf-roles-donut',{
    title:'Répartition par rôle',question:'L’équipe est-elle équilibrée ?',
    conclusion:counts.map(([r,l])=>`${r.split(' ')[0]} ${l.length}`).join(' · '),
    labels:counts.map(([r])=>r.split(' ')[0]),values:counts.map(([,l])=>l.length),
    source:'positions déclarées',timestamp:Date.now(),mode:window.__pfLive?'live':'fallback',
    explain:{shows:'La répartition des positions déclarées entre les rôles de l’équipe.',
      why:'La constitution impose une structure Offensive/Noyau/Défense/Réserve.',
      confirm:'8-10 composantes réparties selon les cibles.',invalidate:'Plus de 3 attaquants ou zéro défense.'}});
}

/* ── POSITIONS ── */
/* Liste « Positions nécessitant une action » (§31) — moteur Position
   Intelligence (statut, priorité, verdict) — jamais une exécution. */
function actionListHtml(state){
  const pf=(state&&state.portfolio)||{};
  const rows=pf.positions_needing_action||[];
  if(!rows.length)return '<section class="vx-card vx-mb3"><div class="vx-card-header">'
    +'<span class="vx-card-title">Positions nécessitant une action</span></div>'
    +VX.states.empty('Aucune position prioritaire — toutes saines ou en surveillance normale.')+'</section>';
  const pill=(pr)=>{const c={P0_CRITICAL:'var(--vx-negative)',P1_HIGH:'var(--vx-warning)'}[pr]||'var(--vx-text-muted)';
    return `<span class="vx-badge" style="color:${c}">${(pr||'').replace('_',' ')}</span>`;}
  return `<section class="vx-card vx-mb3"><div class="vx-card-header">
    <span class="vx-card-title">Positions nécessitant une action</span>
    <span class="vx-meta vx-right">${rows.length} · priorité P0 puis P1</span></div>
    <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
    <th>Priorité</th><th>Titre</th><th>Actif</th><th>Statut</th><th>Action analytique</th>
    <th>Verdict moteur</th><th class="vx-num">P&L</th><th>MàJ</th></tr></thead><tbody>
    ${rows.map(r=>`<tr>
      <td data-label="Priorité">${pill(r.priority)}</td>
      <td data-label="Titre"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.symbol}">${r.symbol}</button></td>
      <td data-label="Actif">${r.asset_type==='OPTION'?'Option':'Action'}</td>
      <td data-label="Statut">${esc((r.status||'').replace(/_/g,' '))}</td>
      <td data-label="Action"><b>${esc((r.action||'').replace(/_/g,' '))}</b></td>
      <td data-label="Verdict">${r.decision?`<span class="vx-badge vx-badge-decision" data-decision="${(r.decision||'').replace('É','E')}">${r.decision}</span>`:'—'}</td>
      <td data-label="P&L" class="vx-num ${r.pl_pct>0?'vx-pos':r.pl_pct<0?'vx-neg':''}">${r.pl_pct!=null?VX.fmt.pct(r.pl_pct,1):'n/d'}</td>
      <td data-label="MàJ" class="vx-mono vx-meta">${VX.fmt.ago(r.updated_at)}</td>
    </tr>`).join('')}</tbody></table></div>
    <div class="vx-card-footer">${VX.updateIndicator(state.updated_at,'Position Intelligence',state.live?'live':'fallback')}
    · verdicts moteur unique — aucune action n'exécute d'ordre</div></section>`;
}
async function renderPositions(){
  const pos=E().positions();
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  let ibkr=null,posState=null;
  try{ibkr=await VX.fetch('/api/ibkr/positions',{ttl:120000});}catch(e){}
  try{posState=await VX.fetch('/api/positions/state',{ttl:30000});}catch(e){}
  const posById={};((posState&&posState.positions)||[]).forEach(p=>{posById[String(p.position_id)]=p;});
  const srcLabel=(s)=>({IBKR:'IBKR',MANUAL:'Manuelle',PAPER:'Paper',SIMULATED:'Simulation',IMPORTED:'Importée'}[s]||'Manuelle');
  const groups={Actions:rich.filter(t=>t.type==='STK'),Options:rich.filter(t=>t.type!=='STK')};
  $('pf-body').innerHTML=
    (posState?actionListHtml(posState):'')+
    (ibkr&&ibkr.ok===false?'<div class="vx-stale-banner">IBKR hors ligne — marques desk/EOD utilisées (aucune valeur inventée).</div>':'')
    +Object.entries(groups).map(([g,list])=>`
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">${g}</span>
      <span class="vx-meta vx-right">${list.length}</span></div>
    ${list.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
      <th>Titre</th><th>Source</th><th>Contrat</th><th class="vx-num">Qté</th><th class="vx-num">Coût</th>
      <th class="vx-num">Marque</th><th class="vx-num">P&L</th><th>Statut</th><th></th></tr></thead><tbody>
      ${list.map(t=>{const pi=posById[String(t.id)]||{};return `<tr>
        <td data-label="Titre"><span class="vx-ticker">${t.sym}</span> ${E().badges(t.sym)}</td>
        <td data-label="Source"><span class="vx-badge">${srcLabel(pi.source)}</span></td>
        <td data-label="Contrat">${t.type}${t.strike?' '+t.strike+' '+(t.exp||''):''}</td>
        <td data-label="Qté" class="vx-num">${t.qty}</td>
        <td data-label="Coût (total)" class="vx-num">${VX.fmt.price(t.cost)}</td>
        <td data-label="Marque" class="vx-num">${t.mark!==null?VX.fmt.price(t.mark):'n/d'}</td>
        <td data-label="P&L" class="vx-num ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}">${t.pl!==null?VX.fmt.pct(t.pl,1):'n/d'}</td>
        <td data-label="Statut" class="vx-meta">${pi.lifecycle_status?esc(pi.lifecycle_status.replace(/_/g,' ')):'—'}</td>
        <td><div class="vx-row-actions">
          <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${t.sym}">Analyse</button>
          <button class="vx-btn vx-btn-sm" data-close-pos="${t.id}">Clôturer</button>
          <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Plus">⋯</button>
        </div></td></tr>`;}).join('')}</tbody></table></div>`
      :VX.states.empty('Aucune position '+g.toLowerCase()+'.')}
    </section>`).join('')
    +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),window.__pfLive?'IBKR/desk':'desk (repli)',window.__pfLive?'live':'fallback')}
     · IBKR: ${ibkr&&ibkr.count!==undefined?ibkr.count+' position(s) broker (lecture seule)':'hors ligne'}</div>`;
  document.querySelectorAll('[data-close-pos]').forEach(b=>b.addEventListener('click',()=>{
    const t=E().positions().find(x=>x.id===+b.dataset.closePos);if(!t)return;
    VX.shell.openModal('Clôturer '+t.sym,
      `<div class="vx-field"><label>Montant récupéré (total)</label>
       <input class="vx-input" id="pf-exit" type="number" step="any" value="${t.mark!==undefined&&t.mark!==null?(t.mark*t.qty*(t.type==='STK'?1:100)).toFixed(2):''}"></div>
       <div class="vx-field"><label>Note</label><input class="vx-input" id="pf-note"></div>
       <div class="vx-help">La clôture est déclarative (journal auto) — aucun ordre n’est envoyé.</div>`,
      '<button class="vx-btn vx-btn-primary" id="pf-close-confirm">Clôturer</button>');
    document.getElementById('pf-close-confirm').addEventListener('click',()=>{
      const v=Number(document.getElementById('pf-exit').value);
      if(!isFinite(v)){VX.toast('Montant requis','error');return;}
      E().recordExit(t.id,v,document.getElementById('pf-note').value);
      VX.shell.closeModal();renderPositions();});
  }));
}

/* ── OPTIONS COMMAND CENTER (§19) ── */
async function renderOptions(){
  const pos=E().positions();
  const opts=pos.filter(t=>t.type!=='STK');
  const rich=enrich(opts,await quotesFor(opts));
  renderSummary(enrich(pos,await quotesFor(pos)));
  if(!opts.length){
    $('pf-body').innerHTML=VX.states.empty(
      'Aucune position option — le sélecteur Vertex Dynamic Options privilégie les CALLS (max 3, dont 1 PUT tactique).',
      '<a class="vx-btn vx-btn-sm vx-btn-primary" href="/opportunities?view=options">Chercher un contrat</a>');
    return;
  }
  const calls=rich.filter(t=>t.type==='CALL'),puts=rich.filter(t=>t.type==='PUT');
  const engaged=rich.reduce((s2,t)=>s2+t.invested,0);
  const marked=rich.filter(t=>t.pl!==null);
  const plTot=marked.length===rich.length&&rich.length?rich.reduce((s2,t)=>s2+(t.value-t.invested),0):null;
  const dtes=rich.map(t=>t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null).filter(v=>v!==null);
  const dteAvg=dtes.length?Math.round(dtes.reduce((a,b)=>a+b,0)/dtes.length):null;
  const H=(l,v,d,cls)=>`<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3">
    <span class="vx-kpi-label">${l}</span><span class="vx-kpi-value" style="font-size:20px">${v}</span>
    ${d?`<span class="vx-kpi-delta ${cls||'vx-muted'}">${d}</span>`:''}</div>`;
  $('pf-body').innerHTML=
    `<div class="vx-grid vx-mb3">
      ${H('CALLS ouverts',calls.length,'direction principale (~90 %)')}
      ${H('PUTS tactiques',puts.length+' / 1',puts.length>1?'PLAFOND DÉPASSÉ':'rares, jamais « parce que ça baisse »',puts.length>1?'vx-neg':'')}
      ${H('Capital engagé',VX.fmt.price(engaged),'coût total déclaré')}
      ${H('P&L options',plTot!==null?VX.fmt.price(plTot):'n/d',plTot!==null?VX.fmt.pct(plTot/engaged*100,1):'marques indisponibles (IBKR hors ligne)',plTot>0?'vx-pos':plTot<0?'vx-neg':'vx-muted')}
    </div>
    <div class="vx-grid vx-mb3">
      ${H('DTE moyen',dteAvg!==null?dteAvg+' j':'n/d','constitution : 60-270, préf. 90-210')}
      ${H('Delta total','n/d','Greeks broker requis — jamais estimés sans IBKR')}
      ${H('Theta quotidien','n/d','IBKR hors ligne')}
      ${H('Risque événementiel',rich.some(t=>t.entrySnap&&t.entrySnap.earnings_dte!=null)?'à vérifier':'—','earnings par position ci-dessous')}
    </div>
    <section class="vx-card vx-mb3" aria-label="Allocation du capital options">
      <div class="vx-chart-head"><span class="vx-chart-title">Capital engagé par contrat</span>
        <span class="vx-chart-question">Où est concentré le capital options ?</span></div>
      <div id="pf-opt-tree" style="height:220px"></div>
      <div class="vx-card-foot"><span class="vx-meta">Taille = capital engagé (coût déclaré) · couleur = sens (CALL acier / PUT violet). Aucune valeur inventée.</span></div>
    </section>
    <section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Positions options</span>
      <span class="vx-meta vx-right">analyse complète par position — aucune exécution</span></div>
    <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
      <th>Contrat</th><th class="vx-num">Qté</th><th class="vx-num">Coût</th><th class="vx-num">Marque</th>
      <th class="vx-num">P&L</th><th class="vx-num">DTE</th><th>Stop sous-jacent</th><th></th></tr></thead><tbody>
    ${rich.map(t=>{
      const dte=t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null;
      return `<tr>
      <td data-label="Contrat"><span class="vx-ticker">${t.sym}</span>
        <span class="vx-badge" style="color:var(--vx-option)">${t.type} ${t.strike??''} ${t.exp||''}</span></td>
      <td data-label="Qté" class="vx-num">${t.qty}</td>
      <td data-label="Coût" class="vx-num">${VX.fmt.price(t.cost)}</td>
      <td data-label="Marque" class="vx-num">${t.mark!==null?VX.fmt.price(t.mark):'n/d'}</td>
      <td data-label="P&L" class="vx-num ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}">${t.pl!==null?VX.fmt.pct(t.pl,1):'n/d'}</td>
      <td data-label="DTE" class="vx-num ${dte!==null&&dte<=7?'vx-warn':''}">${dte!==null?dte+' j':'—'}</td>
      <td data-label="Stop">${VX.fmt.nd(t.entrySnap&&t.entrySnap.stop)}</td>
      <td><div class="vx-row-actions">
        <button class="vx-btn vx-btn-sm vx-btn-primary" data-opt-analyze="${t.id}">Analyser</button>
        <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Plus">⋯</button>
      </div></td></tr>`;}).join('')}</tbody></table></div>
    <div class="vx-card-footer">${VX.updateIndicator(Date.now(),window.__pfLive?'IBKR/desk':'desk (repli)',window.__pfLive?'live':'fallback')}
      · Greeks agrégés affichés uniquement avec IBKR (jamais estimés en agrégat)</div></section>`;
  if(window.VXCharts&&VXCharts.treemap){
    const cc=VXCharts.colors;const el=document.getElementById('pf-opt-tree');const w=(el&&el.clientWidth)||900;
    VXCharts.treemap(el,{width:w,height:220,
      items:rich.map(t=>({label:t.sym+' '+(t.strike||''),value:Math.max(1,t.invested||0),
        sub:(t.type==='PUT'?'PUT':'CALL')+(t.exp?' '+t.exp:''),
        color:(t.type==='PUT'?(cc.violet||'#9c79d0'):(cc.neutral||'#8f8a83'))})),
      fmt:(v)=>VX.fmt.price(v)});
  }
  document.querySelectorAll('[data-opt-analyze]').forEach(b=>
    b.addEventListener('click',()=>openOptionDrawer(rich.find(t=>String(t.id)===b.dataset.optAnalyze))));
}

/* Drawer d'analyse COMPLET par position option (§20-21) — lecture seule. */
async function openOptionDrawer(t){
  if(!t)return;
  const dte=t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null;
  const unit=t.qty?t.cost/(t.qty*100):null;   /* prime par action dérivée du coût total */
  const snap=t.entrySnap||{};
  const kvR=(k,v,cls)=>`<div class="vx-kv"><span class="k">${k}</span><span class="v vx-mono ${cls||''}">${VX.fmt.nd(v)}</span></div>`;
  VX.shell.openDrawer(`${t.sym} ${t.type} ${t.strike??''} ${t.exp||''}`,
    `<h3 class="vx-mb2">Identité</h3>
     ${kvR('Contrat',`${t.sym} ${t.type} ${t.strike??'—'} · ${t.exp||'—'}`)}
     ${kvR('DTE',dte!==null?dte+' j':'—',dte!==null&&dte<=7?'vx-warn':'')}
     ${kvR('Quantité × multiplicateur',t.qty+' × 100')}
     ${kvR('Coût moyen (prime/action)',unit!==null?VX.fmt.price(unit):'—')}
     ${kvR('Capital engagé',VX.fmt.price(t.cost))}
     <h3 class="vx-mt4 vx-mb2">Marché</h3><div id="od-market">${kvR('Marque',t.mark!==null?VX.fmt.price(t.mark):'n/d (IBKR hors ligne)')}
     ${kvR('P&L',t.pl!==null?VX.fmt.pct(t.pl,1):'n/d',t.pl>0?'vx-pos':t.pl<0?'vx-neg':'')}
     <div class="vx-meta">bid/ask/volume/OI/IV/Greeks : fournis par IBKR uniquement — jamais estimés ici.</div></div>
     <h3 class="vx-mt4 vx-mb2">Plan</h3>
     ${kvR('Invalidation (sous-jacent)',snap.stop,'vx-neg')}
     ${kvR('Objectif',snap.tgt,'vx-pos')}
     ${kvR('Objectif de gain typique','+50 % (jamais garanti)')}
     ${kvR('Time stop','réévaluer avant '+(dte!==null?Math.max(5,Math.round(dte/6))+' j':'—'))}
     <h3 class="vx-mt4 vx-mb2">Décision analytique</h3><div id="od-decision"><div class="vx-skeleton" style="height:40px"></div></div>
     <h3 class="vx-mt4 vx-mb2">Payoff à l'échéance</h3><div id="od-payoff" style="height:180px"><canvas></canvas></div>
     <h3 class="vx-mt4 vx-mb2">Scénarios (moteur)</h3><div id="od-scenarios"><div class="vx-skeleton" style="height:60px"></div></div>
     <div class="vx-help vx-mt3">⛔ Lecture seule : aucune action de cette analyse ne peut exécuter, clôturer ou modifier un ordre.</div>`);
  /* Décision de gestion — moteur unique /api/position-decision */
  try{
    const q=new URLSearchParams({type:t.type,entry:unit??'',stop:snap.stop??'',tp:snap.tgt??'',
      current:t.mark??'',pl_pct:t.pl??'',dte:dte??''});
    const d=await VX.fetch('/api/position-decision/'+t.sym+'?'+q.toString(),{ttl:60000});
    const el=document.getElementById('od-decision');
    if(el)el.innerHTML=`<div class="vx-flex"><span class="vx-badge vx-badge-decision" data-decision="${(d.action||'').replace('É','E')}" style="font-size:13px;padding:4px 12px">${d.action||d.label||'n/d'}</span></div>
      <div class="vx-dim vx-mt2" style="font-size:12.5px">${(d.reasons||[]).map(r=>'· '+r).join('<br>')||d.note||''}</div>
      ${d.underlying&&d.underlying.decision?`<div class="vx-meta vx-mt2">Sous-jacent : ${d.underlying.decision}</div>`:''}`;
  }catch(e){const el=document.getElementById('od-decision');
    if(el)el.innerHTML='<span class="vx-meta">Moteur de gestion indisponible : '+esc(e.message)+'</span>';}
  /* Payoff : calculable du strike + prime (données déclarées, pas de marché) */
  try{
    if(window.VXCharts&&VXCharts.payoffCard&&t.strike&&unit){
      VXCharts.payoffCard('od-payoff',{title:'Payoff',spot:(t.underSpot!=null)?t.underSpot:t.strike,
        strike:t.strike,premium:unit,right:t.type==='PUT'?'P':'C',height:170,
        source:(t.underSpot!=null)?'position déclarée (centre = cours réel)':'position déclarée (centre = strike sans cote)',
        timestamp:Date.now(),mode:(t.underSpot!=null)?'delayed':'fallback'});
    }
  }catch(e){}
  /* Scénarios moteur : nécessite IV + spot — refus honnête sinon */
  try{
    const spot=(t.underSpot??null);
    const el=document.getElementById('od-scenarios');
    if(el)el.innerHTML='<div class="vx-meta">Simulation spot×temps×IV disponible depuis le desk options '
      +'(<a href="/opportunities?view=options&sym='+t.sym+'">ouvrir</a>) — elle exige IV et spot frais ; '
      +'sans IBKR, rien n\'est estimé ici.</div>';
  }catch(e){}
}

/* ── RISQUE (positions réelles → moteur §26) ── */
async function renderRisk(){
  const pos=E().positions();
  if(!pos.length){$('pf-body').innerHTML=VX.states.empty('Aucune position déclarée — le risque se calcule sur les positions réelles, jamais sur les candidats du scanner.');return;}
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  let scan=null;try{scan=await VX.fetch('/scan',{ttl:300000});}catch(e){}
  const sectorOf=(sym)=>{const d=scan&&scan.detail&&scan.detail[sym];return(d&&d.sector)||'';};
  /* risk_engine attend des unités PAR ACTION (pl=(last/avg-1), mv=qty*last). Or t.cost
     est le TOTAL investi → dériver le prix unitaire, sinon fausses alertes de stop ~-100 %
     et concentration/bêta/stress corrompus. */
  const payload={positions:rich.filter(t=>t.type==='STK').map(t=>{const per=t.qty?t.cost/t.qty:t.cost;
      return {symbol:t.sym,quantity:t.qty,avg_cost:per,last_price:(t.mark!=null?t.mark:per),sector:sectorOf(t.sym)};}),
    cash:E().capital()||0,simulated:false};
  try{
    const r=await fetch('/api/portfolio/team',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const d=await r.json();
    const risk=d.risk||{},guard=d.guard||{},stress=(d.stress||{}).scenarios||{};
    const optGreeks={delta:risk.options_exposure&&risk.options_exposure.delta};
    $('pf-body').innerHTML=`<div class="vx-grid vx-mb3">
      <section class="vx-card vx-col-4" aria-label="Concentration du risque">
        <div class="vx-card-header"><span class="vx-card-title">Concentration du risque</span>
          <span class="vx-chart-question">Le capital est-il trop concentré ?</span></div>
        <div id="pf-risk-gauge"><div class="vx-skeleton" style="height:118px"></div></div>
        <div class="vx-card-footer"><span class="vx-meta">Indice HHI (0 = dispersé · 100 = tout sur un titre) — donnée réelle du moteur.</span></div>
      </section>
      <section class="vx-card vx-col-8" aria-label="Synthèse du risque">
        <div class="vx-card-header"><span class="vx-card-title">Synthèse du risque</span></div>
        <div class="vx-grid" id="pf-risk-kpis"></div>
      </section>
    </div>
    <div class="vx-grid">
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Garde-fous</span></div>
        ${kv('Nouveau titre',guard.new_stock_allowed?'autorisé':'BLOQUÉ',guard.new_stock_allowed?'vx-pos':'vx-neg')}
        ${kv('Nouvelle option',guard.new_option_allowed?'autorisée':'BLOQUÉE',guard.new_option_allowed?'vx-pos':'vx-neg')}
        ${(guard.blocking_rules||[]).map(r=>`<div class="vx-insight" data-tone="risk">${r}</div>`).join('')}
        ${(guard.mandatory_reviews||[]).map(r=>`<div class="vx-meta">⚠ ${esc(r)}</div>`).join('')}</div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Concentration</span></div>
        ${kv('Drawdown portefeuille',risk.drawdown_pct!==null&&risk.drawdown_pct!==undefined?risk.drawdown_pct+' %':'n/d (pic non renseigné)')}
        ${kv('HHI',risk.hhi)}${kv('Bêta pondéré',risk.beta)}
        <div id="pf-sector-donut" class="vx-mt2"><span class="vx-meta">Exposition sectorielle…</span></div></div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Greeks agrégés</span></div>
        ${kv('Delta global',risk.options_exposure&&risk.options_exposure.delta)}
        ${kv('Gamma global',risk.options_exposure&&risk.options_exposure.gamma)}
        ${kv('Theta global',risk.options_exposure&&risk.options_exposure.theta)}
        ${kv('Vega global',risk.options_exposure&&risk.options_exposure.vega)}
        <div class="vx-meta vx-mt2">Greeks broker requis — sans IBKR, non estimés (aucune invention).</div></div>
      <section class="vx-card vx-col-12"><div class="vx-card-header"><span class="vx-card-title">Stress tests (§26)</span>
        <span class="vx-chart-question">Combien perd le portefeuille dans chaque scénario ?</span></div>
        ${(function(){const arr=Object.entries(stress).filter(([,v])=>v.impact_pct!=null);
          if(!arr.length)return '';
          const maxAbs=Math.max.apply(null,[1].concat(arr.map(([,v])=>Math.abs(v.impact_pct))));
          return '<div class="vx-mb3">'+arr.map(([k,v])=>{const neg=v.impact_pct<0;
            const w=Math.min(100,Math.abs(v.impact_pct)/maxAbs*100);
            return '<div style="display:flex;align-items:center;gap:8px;margin:3px 0" role="img" aria-label="'+esc(k)+' '+VX.fmt.pct(v.impact_pct,1)+'">'
              +'<span style="width:150px;font-size:11px;color:var(--vx-text-secondary,#b7b2aa);text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+esc(k)+'</span>'
              +'<span style="flex:1;height:13px;background:var(--vx-surface-3,#17191c);border-radius:4px;overflow:hidden"><span style="display:block;height:100%;width:'+w.toFixed(0)+'%;background:'+(neg?'var(--vx-negative,#dc6255)':'var(--vx-positive,#39b878)')+';border-radius:4px"></span></span>'
              +'<span style="width:58px;text-align:right;font-size:11px;font-variant-numeric:tabular-nums" class="'+(neg?'vx-neg':'vx-pos')+'">'+VX.fmt.pct(v.impact_pct,1)+'</span></div>';
          }).join('')+'</div>';})()}
        <div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Scénario</th>
        <th class="vx-num">Impact estimé</th><th>Note</th></tr></thead><tbody>
        ${Object.entries(stress).map(([k,v])=>`<tr><td>${k}</td>
          <td class="vx-num ${v.impact_pct<0?'vx-neg':''}">${v.impact_pct!==null&&v.impact_pct!==undefined?VX.fmt.pct(v.impact_pct,1):'non estimé'}</td>
          <td class="vx-meta">${esc(v.note||'')}</td></tr>`).join('')}</tbody></table></div>
        <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'risk_engine (positions réelles)','live')}
        ${(risk.warnings||[]).length?'· '+risk.warnings.length+' avertissement(s)':''}</div></section></div>`;
    /* Hero §31-32 : jauge de concentration (HHI×100) + bande KPI risque. Données
       réelles du moteur (risk.hhi/beta/drawdown, pire scénario stress). */
    try{
      var _hhi=(risk.hhi!=null)?Math.round(risk.hhi*100):null;
      if(window.VXCharts&&VXCharts.gauge)VXCharts.gauge('pf-risk-gauge',{
        value:_hhi,min:0,max:100,unit:'',label:'Concentration',
        reading:_hhi==null?'donnée indisponible':(_hhi>=66?'très concentré':_hhi>=33?'concentration modérée':'bien dispersé'),
        bands:[{to:33,color:VXCharts.colors.positive},{to:66,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.negative}]});
      var _ws=Object.values(stress).map(function(v){return v&&v.impact_pct;}).filter(function(x){return typeof x==='number';});
      var _worst=_ws.length?Math.min.apply(null,_ws):null;
      var _rk=function(l,v,d,cls){return '<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3"><span class="vx-kpi-label">'+l+'</span><span class="vx-kpi-value" style="font-size:22px">'+(v==null?'—':v)+'</span>'+(d?'<span class="vx-kpi-delta '+(cls||'vx-muted')+'">'+d+'</span>':'')+'</div>';};
      var _rh=$('pf-risk-kpis');
      if(_rh)_rh.innerHTML=
        _rk('HHI',risk.hhi!=null?risk.hhi:'—','indice',(_hhi!=null&&_hhi>=66)?'vx-neg':'')
        +_rk('Bêta',risk.beta!=null?risk.beta:'—','pondéré')
        +_rk('Drawdown',(risk.drawdown_pct!=null)?(risk.drawdown_pct+' %'):'n/d','pic')
        +_rk('Pire scénario',_worst!=null?VX.fmt.pct(_worst,1):'—','stress',(_worst!=null&&_worst<0)?'vx-neg':'');
      /* Exposition sectorielle : donut au lieu d'une liste tronquée à 5 ; le surplus
         est regroupé en « Autres » (aucune troncature silencieuse). '—' honnête si vide. */
      var _sw=risk.sector_weights||{};
      var _sh=document.getElementById('pf-sector-donut');
      if(_sh){
        var _se=Object.keys(_sw).map(function(k){return [k,+_sw[k]];}).filter(function(e){return isFinite(e[1])&&e[1]>0;}).sort(function(a,b){return b[1]-a[1];});
        if(!_se.length){_sh.innerHTML='<span class="vx-meta">Exposition sectorielle indisponible (aucune position action).</span>';}
        else if(window.VXCharts&&VXCharts.donut){
          var _lab,_val;
          if(_se.length<=5){_lab=_se.map(function(e){return e[0];});_val=_se.map(function(e){return e[1];});}
          else{var _t=_se.slice(0,4);_lab=_t.map(function(e){return e[0];});_val=_t.map(function(e){return e[1];});
            var _rest=_se.slice(4).reduce(function(s,e){return s+e[1];},0);_lab.push('Autres');_val.push(+_rest.toFixed(2));}
          _sh.innerHTML='<div class="vx-kpi-label vx-mb1">Exposition sectorielle</div><div style="height:150px"><canvas></canvas></div>';
          VXCharts.donut(_sh.querySelector('canvas'),_lab,_val,{});
        } else {_sh.innerHTML=_se.map(function(e){return kv(e[0],e[1]+' %');}).join('');}
      }
    }catch(e){}
  }catch(e){$('pf-body').innerHTML=VX.states.error('Moteur de risque injoignable : '+e.message);}
}

/* ── WATCHLIST (+ suivis + favoris §18) ── */
async function renderWatchlist(){
  const wl=E().watchlist(),follows=E().follows(),favs=E().favorites();
  const statuses=['idee','a_etudier','en_attente','proche','declenchee','invalidee','archivee'];
  const labels={idee:'Idée',a_etudier:'À étudier',en_attente:'En attente',proche:'Proche',
    declenchee:'Déclenchée',invalidee:'Invalidée',archivee:'Archivée'};
  $('pf-body').innerHTML=`
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">Watchlist (surveillance active)</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('','watchlist')">+ Ajouter</button></span></div>
      ${wl.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Priorité</th><th>Thèse</th><th>Zone</th><th>Catalyseur</th>
        <th>Statut</th><th>Ajouté</th><th></th></tr></thead><tbody>
        ${wl.map(w=>`<tr>
          <td data-label="Titre"><span class="vx-ticker">${w.sym}</span> ${E().badges(w.sym)}</td>
          <td data-label="Priorité"><span class="vx-badge">${esc(w.priority||'normale')}</span></td>
          <td data-label="Thèse" class="vx-truncate" style="max-width:200px">${esc(w.thesis||'—')}</td>
          <td data-label="Zone" class="vx-mono">${esc(w.zone||'—')}</td>
          <td data-label="Catalyseur">${esc(w.catalyst||'—')}</td>
          <td data-label="Statut"><select class="vx-select" data-wl-status="${w.sym}" style="width:auto;padding:3px 24px 3px 8px">
            ${statuses.map(s=>`<option value="${s}" ${w.status===s?'selected':''}>${labels[s]}</option>`).join('')}</select></td>
          <td data-label="Ajouté" class="vx-mono vx-meta">${w.added||'—'}</td>
          <td><div class="vx-row-actions">
            <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${w.sym}">Analyse</button>
            <button class="vx-btn vx-btn-sm vx-btn-danger" data-wl-del="${w.sym}">Retirer</button>
          </div></td></tr>`).join('')}</tbody></table></div>`
        :VX.states.empty('Watchlist vide — ajoutez les titres à surveiller activement avec thèse et zone.',
          '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'watchlist\')">+ Ajouter</button>')}
    </section>
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">Suivis actifs (setups)</span></div>
      ${follows.length?follows.map(r=>`<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.sym}">${r.sym}</button>
        <span class="vx-badge vx-badge-entity" data-kind="follow">${r.kind}</span>
        <span class="vx-grow vx-mono vx-meta">entrée ${VX.fmt.nd(r.entry_spot)} · stop ${VX.fmt.nd(r.stop)} · objectif ${VX.fmt.nd(r.tgt)}</span>
        <span class="vx-meta">depuis ${r.followed||'—'}</span>
        <button class="vx-btn vx-btn-sm vx-btn-danger" data-unfollow="${r.sym}">Retirer</button></div>`).join('')
        :VX.states.empty('Aucun suivi actif — créez un suivi depuis une analyse (entrée/stop/objectif).')}
    </section>
    <section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Favoris (accès rapide)</span></div>
      <div class="vx-flex vx-wrap">${favs.length?favs.map(s=>
        `<button class="vx-btn vx-ticker" data-open-analysis="${s}">★ ${s}</button>`).join('')
        :'<span class="vx-muted">Aucun favori — l’étoile est disponible sur chaque titre.</span>'}</div>
    </section>`;
  document.querySelectorAll('[data-wl-del]').forEach(b=>b.addEventListener('click',()=>{E().removeFromWatchlist(b.dataset.wlDel);renderWatchlist();}));
  document.querySelectorAll('[data-unfollow]').forEach(b=>b.addEventListener('click',()=>{E().unfollow(b.dataset.unfollow);renderWatchlist();}));
  document.querySelectorAll('[data-wl-status]').forEach(sel=>sel.addEventListener('change',()=>{
    E().addToWatchlist(sel.dataset.wlStatus,Object.assign({},E().watchlist().find(w=>w.sym===sel.dataset.wlStatus),{status:sel.value}));}));
}

const RENDER={team:renderTeam,positions:renderPositions,options:renderOptions,risk:renderRisk,watchlist:renderWatchlist};
function boot(){(RENDER[VIEW]||renderTeam)().catch(e=>{$('pf-body').innerHTML=VX.states.error(e.message);});}
if(window.VXCharts&&window.Chart)boot();else window.addEventListener('load',boot,{once:true});
['vx:position-changed','vx:watchlist-changed','vx:follow-changed','vx:favorites-changed']
  .forEach(ev=>VX.bus.on(ev,(e)=>{if((e.detail||{}).source!=='sync')return boot();boot();}));
})();
</script>
"""


def render(view: str = 'team') -> str:
    view = view if view in dict(_VIEWS) else 'team'
    content = (_CONTENT.replace('%%TABS%%', _tabs(view))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:120px"></div>'))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Portefeuille · {label}', active='portfolio',
                        space_label='Portefeuille', sub_label=label,
                        content=content, page_js=_JS.replace('%%VIEW%%', json.dumps(view)),
                        page_label=f'Portefeuille {label}')
