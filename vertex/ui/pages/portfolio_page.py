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
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
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
/* Barres divergentes autour de 0 : attribution P&L par position (gagnants à droite,
   perdants à gauche). items:[{name,val}] où val = P&L en %. Données réelles. */
function divBars(items,opt){
  opt=opt||{};const fmt=opt.fmt||((v)=>VX.fmt.pct(v,1));
  const arr=(items||[]).filter(x=>x&&x.val!=null&&isFinite(x.val)).sort((a,b)=>b.val-a.val);
  if(!arr.length)return '';
  const mx=Math.max.apply(null,[1e-9].concat(arr.map(x=>Math.abs(x.val))));
  return '<div class="vx-divbars">'+arr.map(x=>{const pos=x.val>=0;const w=Math.max(2,Math.min(50,Math.abs(x.val)/mx*50));
    return `<div class="vx-divbar"><span class="db-name">${esc(x.name)}</span>`
      +`<span class="db-track"><i class="${pos?'pos':'neg'}" style="width:${w.toFixed(1)}%"></i></span>`
      +`<span class="db-val ${pos?'vx-pos':'vx-neg'}">${fmt(x.val)}</span></div>`;}).join('')+'</div>';
}
/* Greeks agrégés du portefeuille options : delta directionnel (émeraude/corail),
   theta = décroissance (corail si négatif). Note honnête si non estimés (IBKR requis). */
function greeksBlock(g){
  g=g||{};
  const has=g.delta!=null||g.gamma!=null||g.theta!=null||g.vega!=null;
  if(!has)return '<div class="vx-meta vx-mt2">Greeks broker requis — sans IBKR ni options ouvertes, non estimés (aucune invention).</div>';
  const row=(k,v,dec,tone)=>`<div class="vx-kv"><span class="k">${k} global</span><span class="v vx-mono ${tone||''}">${v==null?'—':VX.fmt.num(v,dec)}</span></div>`;
  return row('Delta',g.delta,3,g.delta>0?'vx-pos':g.delta<0?'vx-neg':'')
    +row('Gamma',g.gamma,4)
    +row('Theta',g.theta,3,g.theta<0?'vx-neg':'')
    +row('Vega',g.vega,3)
    +(g.open_options?`<div class="vx-meta vx-mt2">${g.open_options} option(s) ouverte(s)${g.greeks_partial?' · agrégat partiel (certaines jambes sans greeks)':''}</div>`:'');
}
/* Heatmap de corrélations du portefeuille (risk.correlations : pairs réels +
   symbols_covered). Couleur INVERSÉE vs défaut : haute corrélation = risque =
   corail ; décorrélé = émeraude. Vide honnête sans historique. */
function corrHeatmap(hostId,corr){
  const el=$(hostId);if(!el)return;
  const syms=(corr&&corr.symbols_covered)||[];const pairs=(corr&&corr.pairs)||{};
  if(syms.length<2||!Object.keys(pairs).length){
    el.className='vx-col-12';
    el.innerHTML='<div class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Corrélations du portefeuille</span></div>'
      +VX.states.empty('Corrélations indisponibles — nécessitent un historique de prix (≥ 30 séances par titre, disponible avec le flux live).')+'</div>';
    return;
  }
  const raw=(a,b)=>a===b?1:((pairs[a+'/'+b]!=null)?pairs[a+'/'+b]:(pairs[b+'/'+a]!=null?pairs[b+'/'+a]:null));
  const rows=syms.map(a=>({label:a,cells:syms.map(b=>{const v=raw(a,b);
    return {value:(a===b||v==null)?null:-v,   // négation : haute corrélation → corail
            label:(v==null?'—':(+v).toFixed(2)),title:a+' / '+b+' : '+(v==null?'n/d':(+v).toFixed(2))};})}));
  VXCharts.heatmapCard(hostId,{title:'Corrélations du portefeuille',
    question:'La diversification est-elle réelle ou illusoire ?',
    conclusion:(corr.average!=null?('corrélation moyenne '+(+corr.average).toFixed(2)):'')+(corr.warning?' — '+corr.warning:''),
    columns:syms,rows:rows,min:-1,max:1,source:'risk_engine · rendements réels',timestamp:Date.now(),mode:'live',
    limits:'corail = fortement corrélé (risque de concentration) · émeraude = décorrélé (diversification réelle)'});
}
/* Composition du capital : Actions / Options / Cash en barre empilée + légende.
   Valeur au marché si dispo, sinon au coût ; cash = capital déclaré. Réel. */
function compositionBar(rich){
  const stk=rich.filter(t=>t.type==='STK').reduce((s,t)=>s+(t.value??t.invested),0);
  const opt=rich.filter(t=>t.type!=='STK').reduce((s,t)=>s+(t.value??t.invested),0);
  const cash=E().capital()||0;const tot=stk+opt+cash;
  if(!tot)return '';
  const seg=(v,col)=>{const p=v/tot*100;return p>0?`<i style="width:${p.toFixed(1)}%;background:${col}"></i>`:'';};
  const leg=(l,v,col)=>`<span><i style="background:${col}"></i>${l} <b>${(v/tot*100).toFixed(0)}%</b> · ${VX.fmt.price(v)} $</span>`;
  const A='var(--vx-brand)',O='var(--vx-violet)',C='var(--vx-steel-3)';
  return `<div class="vx-mt3"><span class="vx-metric-k" style="display:block;margin-bottom:2px">Composition du capital</span>`
    +`<div class="vx-stackbar" role="img" aria-label="Actions ${(stk/tot*100).toFixed(0)}% Options ${(opt/tot*100).toFixed(0)}% Cash ${(cash/tot*100).toFixed(0)}%">`
    +seg(stk,A)+seg(opt,O)+seg(cash,C)+`</div>`
    +`<div class="vx-stackbar-legend">`+leg('Actions',stk,A)+leg('Options',opt,O)+leg('Cash',cash,C)+`</div></div>`;
}
/* Barres de poids par position (allocation réelle du moteur risk.weights) : cash
   inclus, surpondérations (risk.overweight) en ambre, repère au poids max. */
function weightBars(weights,overweight,maxW){
  maxW=maxW||15;
  const es=Object.keys(weights||{}).map(k=>({k:k==='_CASH'?'Cash':k,raw:k,v:+weights[k],
      cash:k==='_CASH',over:!!(overweight&&overweight[k]!=null)}))
    .filter(e=>isFinite(e.v)&&e.v>0).sort((a,b)=>b.v-a.v);
  if(!es.length)return '';
  const mx=Math.max.apply(null,[maxW*1.15].concat(es.map(e=>e.v)));
  return '<div class="vx-wbars">'+es.map(e=>`<div class="vx-wbar" data-tone="${e.cash?'cash':e.over?'over':''}">`
    +`<span class="wb-name">${esc(e.k)}${e.over?'<span class="wb-tag">surpondéré</span>':''}</span>`
    +`<span class="wb-track"><i style="width:${Math.max(2,Math.min(100,e.v/mx*100)).toFixed(0)}%"></i>`
    +`${e.cash?'':`<b style="left:${Math.min(100,maxW/mx*100).toFixed(0)}%"></b>`}</span>`
    +`<span class="wb-val">${e.v.toFixed(1)}%</span></div>`).join('')
    +`<div class="vx-meta vx-mt2">Repère corail = poids max ${maxW}% par position · Cash = liquidités.</div></div>`;
}
/* COCKPIT de synthèse : jauge « positions gagnantes » + gagnants/perdants +
   valeur/P&L/équipe/options en tuiles. Valeur au coût toujours calculable ;
   marques live si disponibles — jamais un chiffre inventé, l'étiquette dit
   ce qui est affiché ; jauge absente sans marques (honnête). */
function renderSummary(rich){
  const host=$('pf-summary');if(!host)return;
  if(!rich.length){host.innerHTML='';return;}
  const stocks=rich.filter(t=>t.type==='STK'),opts=rich.filter(t=>t.type!=='STK');
  const invested=rich.reduce((s,t)=>s+t.invested,0);
  const marked=rich.filter(t=>t.value!==null);
  const value=marked.length===rich.length?rich.reduce((s,t)=>s+t.value,0):null;
  const pl=value!==null&&invested?(value-invested):null;
  const winners=marked.filter(t=>t.pl>0).length,losers=marked.filter(t=>t.pl<0).length;
  const winPct=marked.length?Math.round(winners/marked.length*100):null;
  const gauge=(winPct!=null&&window.VXCharts&&VXCharts.scoreGaugeSVG)
    ?VXCharts.scoreGaugeSVG(winPct,{label:'positions gagnantes',size:92,stroke:8}):'';
  const wl=marked.length?`<div style="display:flex;height:9px;border-radius:99px;overflow:hidden;background:var(--vx-surface-0);margin-top:8px" role="img" aria-label="${winners} gagnantes contre ${losers} perdantes">
      <i style="width:${(winners/(marked.length||1)*100).toFixed(0)}%;background:var(--vx-positive)"></i>
      <i style="flex:1;background:var(--vx-negative)"></i></div>
    <div class="vx-meter-row" style="margin-top:5px"><span style="color:var(--vx-positive)">${winners} gagnante(s)</span><span style="color:var(--vx-negative)">${losers} perdante(s)</span></div>`:'';
  const tile=(label,val,sub,tone)=>`<div class="vx-stat" data-tone="${tone||''}">
    <div class="vx-stat-k">${label}</div><div class="vx-stat-v" style="font-size:19px">${val}</div>
    ${sub?`<div class="vx-stat-sub">${sub}</div>`:''}</div>`;
  host.innerHTML=`<div class="vx-card vx-col-12 vx-card--premium">
    <div class="vx-scorecard" style="grid-template-columns:auto minmax(0,1fr)">
      ${gauge?`<div class="vx-gaugecluster" style="flex-direction:column">${gauge}</div>`:''}
      <div class="vx-scorecard-side">
        <div class="vx-statrow">
          ${tile('Valeur',value!==null?VX.fmt.price(value):VX.fmt.price(invested),value!==null?'marques live/desk':'au coût (marques indisponibles)')}
          ${tile('P&L latent',pl!==null?((pl>=0?'+':'')+VX.fmt.price(pl)):'n/d',pl!==null?VX.fmt.pct(pl/invested*100,1):'IBKR hors ligne',pl>0?'pos':pl<0?'neg':'')}
          ${tile('Équipe actions',stocks.length+' / 10',stocks.length>=10?'complet — remplacement obligatoire':'places disponibles')}
          ${tile('Options tactiques',opts.length+' / 3','CALLS '+opts.filter(t=>t.type==='CALL').length+' · PUTS '+opts.filter(t=>t.type==='PUT').length+' / 1 max')}
        </div>
        ${wl}
      </div>
    </div></div>`;
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
      ${compositionBar(rich)}
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
  /* Attribution P&L par position en barres divergentes, en DOLLARS de contribution
     (value − investi) — « qui a bougé l'aiguille », pas le % qui exagère les petites
     lignes. Gagnants à droite, perdants à gauche. Repli honnête sans marque. */
  const withVal=rich.filter(t=>t.value!=null&&t.invested);
  const _pfx=(v)=>(v>=0?'+':'')+VX.fmt.price(v)+' $';
  $('pf-contrib-body').innerHTML=withVal.length
    ?divBars(withVal.map(t=>({name:(t.sym+(t.type!=='STK'?' '+t.type:'')),val:(t.value-t.invested)})),{fmt:_pfx})
    :'<div class="vx-meta">Marques indisponibles (IBKR hors ligne) — aucun P&L affiché plutôt qu’un chiffre inventé.</div>';
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
        <td data-label="P&L" class="vx-num">${t.pl!==null?`<span style="display:inline-flex;align-items:center;gap:7px;justify-content:flex-end"><span style="flex:0 0 38px;height:6px;border-radius:99px;background:var(--vx-surface-0);position:relative;overflow:hidden"><i style="position:absolute;left:0;top:0;bottom:0;width:${Math.max(4,Math.min(100,Math.abs(t.pl)*6)).toFixed(0)}%;background:${t.pl>0?'var(--vx-positive)':t.pl<0?'var(--vx-negative)':'var(--vx-steel-3)'};border-radius:99px"></i></span><b class="vx-mono ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}" style="min-width:44px">${VX.fmt.pct(t.pl,1)}</b></span>`:'<span class="vx-muted">n/d</span>'}</td>
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
    <div id="pf-opt-combined" class="vx-grid vx-mb3"></div>
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
  renderCombinedOptions(rich);
}

/* Structure combinée par sous-jacent : analyse TES positions options réelles comme une
   stratégie multi-jambes (payoff net, breakevens, gain/perte max) via le moteur
   multileg_lab. Greeks/PoP nécessitent l'IV (n/d sans IBKR) — jamais estimés. */
async function renderCombinedOptions(rich){
  const host=document.getElementById('pf-opt-combined'); if(!host)return;
  const by={};
  rich.forEach(t=>{ if(t.type==='CALL'||t.type==='PUT'){(by[t.sym]=by[t.sym]||[]).push(t);} });
  const syms=Object.keys(by);
  if(!syms.length){host.innerHTML='';return;}
  const results=await Promise.all(syms.map(async sym=>{
    const group=by[sym];
    const spot=group.map(t=>t.underSpot).find(s=>s!=null);
    if(spot==null)return null;   // pas de cote sous-jacent → pas de payoff honnête
    const legs=group.map(t=>({type:(t.type||'').toLowerCase(),strike:t.strike,
      premium:(t.qty&&t.cost)?t.cost/(t.qty*100):null,qty:t.qty}));
    if(legs.some(l=>l.premium==null||l.strike==null))return null;
    const dtes=group.map(t=>t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null).filter(v=>v!=null);
    const days=dtes.length?Math.min.apply(null,dtes):null;
    try{
      const r=await fetch('/api/options/analyze',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({legs:legs,spot:spot,iv:null,days:days,name:sym})});
      const d=await r.json(); if(!d||!d.available)return null; return {sym:sym,spot:spot,group:group,d:d};
    }catch(e){return null;}
  }));
  const ok=results.filter(Boolean);
  if(!ok.length){host.innerHTML='';return;}
  host.innerHTML=ok.map((x,i)=>{
    const d=x.d;
    const mp=d.max_profit_unbounded?'illimité':(d.max_profit!=null?VX.fmt.price(d.max_profit):'—');
    const be=(d.breakevens&&d.breakevens.length)?d.breakevens.map(b=>VX.fmt.nd(b)).join(' · '):'—';
    return `<section class="vx-card vx-col-6">
      <div class="vx-card-header"><span class="vx-card-title">${esc(x.sym)} — structure combinée (${x.group.length} jambe${x.group.length>1?'s':''})</span>
        <span class="vx-badge" style="color:var(--vx-${d.is_credit?'positive':'option'})">${d.is_credit?'crédit ':'débit '}${VX.fmt.price(Math.abs(d.net_premium))}</span></div>
      <div id="pf-comb-pf-${i}" style="height:150px"></div>
      <div class="vx-grid vx-mt2" style="grid-template-columns:repeat(3,1fr);gap:6px">
        <div class="vx-kv"><span class="k">Gain max</span><span class="v vx-mono">${mp}</span></div>
        <div class="vx-kv"><span class="k">Perte max</span><span class="v vx-mono vx-neg">${d.max_loss!=null?VX.fmt.price(d.max_loss):'—'}</span></div>
        <div class="vx-kv"><span class="k">Breakevens</span><span class="v vx-mono">${be}</span></div>
      </div>
      <div class="vx-card-foot"><span class="vx-meta">Payoff à l’échéance depuis tes positions réelles (spot ${VX.fmt.nd(x.spot)}) · greeks/PoP requièrent l’IV.</span></div>
    </section>`;
  }).join('');
  ok.forEach((x,i)=>{
    const cont=document.getElementById('pf-comb-pf-'+i); const pts=x.d.payoff||[];
    if(!cont||!window.VXCharts||pts.length<2)return;
    cont.innerHTML='<canvas></canvas>';
    VXCharts.mount(cont.querySelector('canvas'),{type:'line',
      data:{labels:pts.map(p=>p.price),datasets:[{data:pts.map(p=>p.pnl),borderColor:VXCharts.colors.neutral,
        borderWidth:1.6,pointRadius:0,fill:false,tension:0,
        segment:{borderColor:(ctx)=>ctx.p1.parsed.y>=0?VXCharts.colors.positive:VXCharts.colors.negative}}]},
      options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:(ctx)=>'P&L '+VX.fmt.price(ctx.parsed.y)+' @ '+VX.fmt.nd(ctx.label)}}},
        scales:{x:{ticks:{maxTicksLimit:6},grid:{display:false}},y:{grid:{color:'rgba(255,255,255,.06)'},ticks:{callback:(v)=>VX.fmt.price(v)}}}}});
  });
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
        <div class="vx-mt3"><span class="vx-metric-k" style="display:block;margin-bottom:2px">Poids par position</span>
          <div id="pf-weight-bars"><span class="vx-meta">Allocation…</span></div></div>
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
        ${greeksBlock(risk.options_exposure)}</div>
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
        ${(risk.warnings||[]).length?'· '+risk.warnings.length+' avertissement(s)':''}</div></section>
      <div class="vx-col-12" id="pf-corr-heatmap"></div></div>`;
    /* Heatmap de corrélations RÉELLES entre les positions (risk_engine · rendements) :
       rouge = fortement corrélé (diversification illusoire), vert = décorrélé. Vide
       honnête sans historique de prix (flux live requis). */
    corrHeatmap('pf-corr-heatmap',risk.correlations);
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
      /* Barres de poids par position (risk.weights réel + cash + surpondérations) —
         remplit la synthèse et rend la concentration lisible d'un coup d'œil. */
      var _wb=$('pf-weight-bars');
      if(_wb)_wb.innerHTML=weightBars(risk.weights,risk.overweight,15)||'<span class="vx-meta">Poids par position indisponibles.</span>';
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
/* Sparkline compacte pour les tuiles de watchlist (série réelle du scan). */
function sparkWl(closes,up){
  const v=(closes||[]).filter(x=>x!=null&&isFinite(x)).slice(-40);
  if(v.length<8)return '';
  const w=100,h=20,mn=Math.min.apply(null,v),mx=Math.max.apply(null,v),rng=(mx-mn)||1;
  const pts=v.map((x,i)=>(i/(v.length-1)*w).toFixed(1)+','+(h-1-((x-mn)/rng)*(h-2)).toFixed(1)).join(' ');
  return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" width="100%" height="20" style="display:block;margin:7px 0 2px;opacity:.9" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="${up?'var(--vx-positive)':'var(--vx-negative)'}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"/></svg>`;
}
async function renderWatchlist(){
  const wl=E().watchlist(),follows=E().follows(),favs=E().favorites();
  const statuses=['idee','a_etudier','en_attente','proche','declenchee','invalidee','archivee'];
  const labels={idee:'Idée',a_etudier:'À étudier',en_attente:'En attente',proche:'Proche',
    declenchee:'Déclenchée',invalidee:'Invalidée',archivee:'Archivée'};
  /* Jointure watchlist ↔ scan : score, variation, MTF et sparkline RÉELS quand le
     titre est scanné ; tuile sobre (sans enrichissement inventé) sinon. */
  let scan=null;try{scan=await VX.fetch('/scan',{ttl:120000});}catch(e){}
  const rowOf={};((scan&&scan.rows)||[]).forEach(r=>{if(r&&r.symbol)rowOf[r.symbol]=r;});
  const detOf=(scan&&scan.detail)||{};
  const wlTiles=wl.map(w=>{
    const r=rowOf[w.sym]||{};const det=detOf[w.sym]||{};
    const chg=r.change;const mtf=det.mtf||{};
    const mtfTone=/HAUSS/i.test(mtf.state||'')?'var(--vx-positive)':/BAISS/i.test(mtf.state||'')?'var(--vx-negative)':'var(--vx-warning)';
    const prio=(w.priority||'normale');
    return `<div class="vx-mover" style="cursor:default">
      <div class="vx-flex" style="justify-content:space-between;gap:6px">
        <span class="mv-sym">${esc(w.sym)}</span>
        <span class="vx-flex" style="gap:4px">
          ${prio!=='normale'?`<span class="vx-badge" style="color:var(--vx-warning)">${esc(prio)}</span>`:''}
          ${r.score!=null?`<span class="vx-badge" title="Score Vertex">${VX.fmt.num(r.score,0)}</span>`:''}</span></div>
      <div class="mv-chg ${chg>0?'vx-pos':chg<0?'vx-neg':''}" style="font-size:15px">
        ${chg!=null?VX.fmt.pct(chg,1):'<span class="vx-muted" style="font-size:12px">hors scan</span>'}
        ${r.price!=null?`<span class="vx-meta" style="font-weight:500"> · ${VX.fmt.price(r.price)}</span>`:''}</div>
      ${mtf.state?`<div class="mv-sub" style="color:${mtfTone};margin-top:4px">MTF ${esc(mtf.state)}</div>`:''}
      ${sparkWl(det.series&&det.series.close,chg==null?true:chg>=0)}
      ${w.thesis?`<div class="mv-sub" style="white-space:normal;line-height:1.4;max-height:2.9em;overflow:hidden" title="${esc(w.thesis)}">${esc(w.thesis)}</div>`:''}
      <div class="mv-sub" style="margin-top:5px">${w.zone?`zone <b>${esc(w.zone)}</b>`:''}${w.zone&&w.catalyst?' · ':''}${w.catalyst?esc(w.catalyst):''}</div>
      <div class="vx-flex vx-mt2" style="gap:.3rem;align-items:center">
        <select class="vx-select" data-wl-status="${w.sym}" style="width:auto;padding:3px 22px 3px 8px;font-size:11px">
          ${statuses.map(s=>`<option value="${s}" ${w.status===s?'selected':''}>${labels[s]}</option>`).join('')}</select>
        <span class="vx-grow"></span>
        <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${w.sym}">Analyser</button>
        <button class="vx-btn vx-btn-sm vx-btn-danger" data-wl-del="${w.sym}">✕</button>
      </div>
    </div>`;}).join('');
  $('pf-body').innerHTML=`
    <section class="vx-card vx-mb3 vx-card--premium"><div class="vx-card-header"><span class="vx-card-title">Watchlist (surveillance active)</span>
      <span class="vx-chart-question">Score, tendance et alignement en direct du scan</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('','watchlist')">+ Ajouter</button></span></div>
      ${wl.length?`<div class="vx-movergrid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))">${wlTiles}</div>`
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
