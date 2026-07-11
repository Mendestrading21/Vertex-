"""vertex.ui.pages.portfolio_page — Équipe Vertex (§25).

Question : « Que possède le portefeuille et comment doit-il évoluer ? »
Sous-vues : team, positions, risk, watchlist. Les positions sont le registre
DÉCLARATIF de l'utilisateur (myTrades) + IBKR lecture seule — jamais un ordre.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell

_VIEWS = (('team', 'Équipe'), ('positions', 'Positions'),
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
</div></div>
%%TABS%%
<div class="vx-grid vx-mt4" id="pf-summary" aria-label="Synthèse portefeuille"></div>
<div id="pf-body" class="vx-mt4">%%LOADING%%</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/donut-chart.js" defer></script>
<script src="/static/vertex/js/charts/sparkline.js" defer></script>
<script src="/static/vertex/js/charts/equity-chart.js" defer></script>
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
  return pos.map(t=>{
    const q=quotes[t.id]||{};const mark=q.mark??q.last??null;
    const mult=t.type==='STK'?1:100;
    const value=mark!==null?mark*t.qty*mult:null;
    const invested=(t.cost||0)*t.qty*mult;
    const pl=value!==null&&invested?((value-invested)/invested*100):null;
    return Object.assign({},t,{mark,value,invested,pl});
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
      opts.length>=3?'plafond atteint':'hors équipe — convexité ciblée',
      opts.length>=3?'vx-warn':'');
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
  $('pf-body').innerHTML=`<div class="vx-grid">
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
  $('pf-contrib-body').innerHTML=withPl.length?
    withPl.slice(0,3).map(t=>`<div class="vx-kv"><span class="k">▲ ${t.sym}</span><span class="v vx-pos">${VX.fmt.pct(t.pl,1)}</span></div>`).join('')
    +withPl.slice(-2).reverse().filter(t=>t.pl<0).map(t=>`<div class="vx-kv"><span class="k">▼ ${t.sym}</span><span class="v vx-neg">${VX.fmt.pct(t.pl,1)}</span></div>`).join('')
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
  const counts=Object.entries(roles).filter(([,l])=>l.length);
  if(counts.length)VXCharts.donutCard('pf-roles-donut',{
    title:'Répartition par rôle',question:'L’équipe est-elle équilibrée ?',
    conclusion:counts.map(([r,l])=>`${r.split(' ')[0]} ${l.length}`).join(' · '),
    labels:counts.map(([r])=>r.split(' ')[0]),values:counts.map(([,l])=>l.length),
    source:'positions déclarées',timestamp:Date.now(),mode:window.__pfLive?'live':'fallback',
    explain:{shows:'La répartition des positions déclarées entre les rôles de l’équipe.',
      why:'La constitution impose une structure Offensive/Noyau/Défense/Réserve.',
      confirm:'8-10 composantes réparties selon les cibles.',invalidate:'Plus de 3 attaquants ou zéro défense.'}});
}

/* ── POSITIONS ── */
async function renderPositions(){
  const pos=E().positions();
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  let ibkr=null;
  try{ibkr=await VX.fetch('/api/ibkr/positions',{ttl:120000});}catch(e){}
  const groups={Actions:rich.filter(t=>t.type==='STK'),Options:rich.filter(t=>t.type!=='STK')};
  $('pf-body').innerHTML=
    (ibkr&&ibkr.ok===false?'<div class="vx-stale-banner">IBKR hors ligne — marques desk/EOD utilisées (aucune valeur inventée).</div>':'')
    +Object.entries(groups).map(([g,list])=>`
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">${g}</span>
      <span class="vx-meta vx-right">${list.length}</span></div>
    ${list.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
      <th>Titre</th><th>Contrat</th><th class="vx-num">Qté</th><th class="vx-num">Coût</th>
      <th class="vx-num">Marque</th><th class="vx-num">P&L</th><th>Depuis</th><th></th></tr></thead><tbody>
      ${list.map(t=>`<tr>
        <td data-label="Titre"><span class="vx-ticker">${t.sym}</span> ${E().badges(t.sym)}</td>
        <td data-label="Contrat">${t.type}${t.strike?' '+t.strike+' '+(t.exp||''):''}</td>
        <td data-label="Qté" class="vx-num">${t.qty}</td>
        <td data-label="Coût" class="vx-num">${VX.fmt.price(t.cost)}</td>
        <td data-label="Marque" class="vx-num">${t.mark!==null?VX.fmt.price(t.mark):'n/d'}</td>
        <td data-label="P&L" class="vx-num ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}">${t.pl!==null?VX.fmt.pct(t.pl,1):'n/d'}</td>
        <td data-label="Depuis" class="vx-mono vx-meta">${t.added||'—'}</td>
        <td><div class="vx-row-actions">
          <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${t.sym}">Analyse</button>
          <button class="vx-btn vx-btn-sm" data-close-pos="${t.id}">Clôturer</button>
          <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Plus">⋯</button>
        </div></td></tr>`).join('')}</tbody></table></div>`
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
      E().closePosition(t.id,v,document.getElementById('pf-note').value);
      VX.shell.closeModal();renderPositions();});
  }));
}

/* ── RISQUE (positions réelles → moteur §26) ── */
async function renderRisk(){
  const pos=E().positions();
  if(!pos.length){$('pf-body').innerHTML=VX.states.empty('Aucune position déclarée — le risque se calcule sur les positions réelles, jamais sur les candidats du scanner.');return;}
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  let scan=null;try{scan=await VX.fetch('/scan',{ttl:300000});}catch(e){}
  const sectorOf=(sym)=>{const d=scan&&scan.detail&&scan.detail[sym];return(d&&d.sector)||'';};
  const payload={positions:rich.filter(t=>t.type==='STK').map(t=>({symbol:t.sym,quantity:t.qty,
      avg_cost:t.cost,last_price:t.mark??t.cost,sector:sectorOf(t.sym)})),
    cash:E().capital()||0,simulated:false};
  try{
    const r=await fetch('/api/portfolio/team',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const d=await r.json();
    const risk=d.risk||{},guard=d.guard||{},stress=(d.stress||{}).scenarios||{};
    const optGreeks={delta:risk.options_exposure&&risk.options_exposure.delta};
    $('pf-body').innerHTML=`<div class="vx-grid">
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Garde-fous</span></div>
        ${kv('Nouveau titre',guard.new_stock_allowed?'autorisé':'BLOQUÉ',guard.new_stock_allowed?'vx-pos':'vx-neg')}
        ${kv('Nouvelle option',guard.new_option_allowed?'autorisée':'BLOQUÉE',guard.new_option_allowed?'vx-pos':'vx-neg')}
        ${(guard.blocking_rules||[]).map(r=>`<div class="vx-insight" data-tone="risk">${r}</div>`).join('')}
        ${(guard.mandatory_reviews||[]).map(r=>`<div class="vx-meta">⚠ ${esc(r)}</div>`).join('')}</div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Concentration</span></div>
        ${kv('Drawdown portefeuille',risk.drawdown_pct!==null&&risk.drawdown_pct!==undefined?risk.drawdown_pct+' %':'n/d (pic non renseigné)')}
        ${kv('HHI',risk.hhi)}${kv('Bêta pondéré',risk.beta)}
        ${Object.entries(risk.sector_weights||{}).slice(0,5).map(([s,w])=>kv(s,w+' %')).join('')}</div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Greeks agrégés</span></div>
        ${kv('Delta global',risk.options_exposure&&risk.options_exposure.delta)}
        ${kv('Gamma global',risk.options_exposure&&risk.options_exposure.gamma)}
        ${kv('Theta global',risk.options_exposure&&risk.options_exposure.theta)}
        ${kv('Vega global',risk.options_exposure&&risk.options_exposure.vega)}
        <div class="vx-meta vx-mt2">Greeks broker requis — sans IBKR, non estimés (aucune invention).</div></div>
      <section class="vx-card vx-col-12"><div class="vx-card-header"><span class="vx-card-title">Stress tests (§26)</span></div>
        <div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Scénario</th>
        <th class="vx-num">Impact estimé</th><th>Note</th></tr></thead><tbody>
        ${Object.entries(stress).map(([k,v])=>`<tr><td>${k}</td>
          <td class="vx-num ${v.impact_pct<0?'vx-neg':''}">${v.impact_pct!==null&&v.impact_pct!==undefined?VX.fmt.pct(v.impact_pct,1):'non estimé'}</td>
          <td class="vx-meta">${esc(v.note||'')}</td></tr>`).join('')}</tbody></table></div>
        <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'risk_engine (positions réelles)','live')}
        ${(risk.warnings||[]).length?'· '+risk.warnings.length+' avertissement(s)':''}</div></section></div>`;
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

const RENDER={team:renderTeam,positions:renderPositions,risk:renderRisk,watchlist:renderWatchlist};
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
