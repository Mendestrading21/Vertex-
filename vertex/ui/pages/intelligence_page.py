"""vertex.ui.pages.intelligence_page — l'espace Intelligence (§28).

Question : « Comment Vertex raisonne-t-il et comment la stratégie
évolue-t-elle ? ». Cinq sous-vues : analyst (interroger l'analyste),
committee (matrice du comité), strategy (constitution), research
(validation hors échantillon), memory (thèses & mémoire stratégique).

Principes : l'UI consomme les moteurs, ne recalcule rien ; l'IA explique,
ne décide jamais ; donnée absente → état vide honnête avec action.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

VIEWS = (
    ('analyst', 'Analyste'),
    ('committee', 'Comité'),
    ('strategy', 'Stratégie'),
    ('impacts', 'Impacts'),
    ('research', 'Recherche'),
    ('memory', 'Mémoire'),
)
_DEFAULT_VIEW = 'analyst'


def _tabs(active: str) -> str:
    tabs = ''.join(
        f'<a class="vx-tab" role="tab" href="?view={vid}" '
        f'aria-selected="{"true" if vid == active else "false"}">{label}</a>'
        for vid, label in VIEWS)
    return f'<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Intelligence">{tabs}</nav>'


def _header(active: str) -> str:
    return f'''<div class="vx-page-header">
  <div><h1>Intelligence</h1>
  <div class="vx-sub">Comment Vertex raisonne-t-il et comment la stratégie évolue-t-elle ?</div></div>
</div>
{_tabs(active)}'''


_VIEW_CONTENT = {
    'analyst': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="Interroger l&#8217;analyste">
    <div class="vx-card-header"><span class="vx-card-title">Interroger l&#8217;analyste</span></div>
    <form id="vx-analyst-form" autocomplete="off">
      <div class="vx-form-row">
        <div class="vx-field"><label for="vx-analyst-sym">Ticker</label>
          <input class="vx-input" id="vx-analyst-sym" placeholder="ex. NVDA"
            style="text-transform:uppercase" maxlength="7" /></div>
        <div class="vx-field" style="flex:2"><label for="vx-analyst-q">Question (optionnelle)</label>
          <input class="vx-input" id="vx-analyst-q"
            placeholder="ex. la th&egrave;se tient-elle apr&egrave;s les r&eacute;sultats ?" /></div>
      </div>
      <button class="vx-btn vx-btn-primary" type="submit">Analyser</button>
    </form>
    <div class="vx-mt3" id="vx-analyst-suggestions"></div>
    <div class="vx-insight vx-mt3" data-tone="ai"><b>Claude explique, ne d&eacute;cide jamais.</b>
      La d&eacute;cision finale vient exclusivement des moteurs d&eacute;terministes (constitution
      + moteur ex&eacute;cutif). Si l&#8217;IA est indisponible, une synth&egrave;se d&eacute;terministe des
      moteurs est servie &agrave; la place — jamais de texte invent&eacute;.</div>
  </section>
  <section class="vx-card vx-col-5" aria-label="D&eacute;cision finale">
    <div class="vx-card-header"><span class="vx-card-title">D&eacute;cision finale</span>
      <span class="vx-actions" id="vx-analyst-meta"></span></div>
    <div id="vx-analyst-verdict">%%IDLE%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-5" id="vx-analyst-scores"></div>
  <section class="vx-card vx-col-7" aria-label="Raisonnement et garde-fous">
    <div class="vx-card-header"><span class="vx-card-title">Raisonnement (audit trail)</span></div>
    <div id="vx-analyst-audit">%%IDLE%%</div>
  </section>
</div>''',

    'committee': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-4" aria-label="Convergence du comit&eacute;">
    <div class="vx-card-header"><span class="vx-card-title">Convergence</span>
      <span class="vx-chart-question">Les moteurs sont-ils d&#8217;accord ?</span></div>
    <div id="vx-committee-gauge"><div class="vx-skeleton" style="height:118px"></div></div>
    <div class="vx-card-footer"><span class="vx-meta">Accord moyen des moteurs sur l&#8217;univers scann&eacute; (0-100).</span></div>
  </section>
  <section class="vx-card vx-col-8" aria-label="Synth&egrave;se du comit&eacute;">
    <div class="vx-card-header"><span class="vx-card-title">Verdicts du comit&eacute;</span>
      <span class="vx-chart-question">Comment se r&eacute;partissent les d&eacute;cisions ?</span></div>
    <div class="vx-grid" id="vx-committee-kpis"></div>
    <div id="vx-committee-tally" class="vx-mt3"></div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Matrice du comit&eacute;">
    <div class="vx-card-header"><span class="vx-card-title">Comit&eacute; — revue de l&#8217;univers scann&eacute;</span>
      <span class="vx-actions" id="vx-committee-meta"></span></div>
    <div class="vx-flex vx-wrap vx-gap2 vx-mb3" id="vx-committee-chips" role="group"
      aria-label="Filtrer par d&eacute;cision"></div>
    <div id="vx-committee-body">%%LOADING%%</div>
  </section>
</div>''',

    'strategy': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Constitution de la strat&eacute;gie">
    <div class="vx-card-header"><span class="vx-card-title">Constitution — Strat&eacute;gie Vertex</span>
      <span class="vx-actions" id="vx-strategy-meta"></span></div>
    <div id="vx-strategy-core">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Garde-fous">
    <div class="vx-card-header"><span class="vx-card-title">Garde-fous (hard gates)</span></div>
    <div id="vx-strategy-gates">%%LOADING%%</div>
    <div class="vx-insight vx-mt3" data-tone="risk"><b>R&egrave;gle de modification.</b>
      Toute modification de la constitution exige une nouvelle version explicite
      + une confirmation humaine. Rien ne change silencieusement.</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Cat&eacute;gories d&#8217;options">
    <div class="vx-card-header"><span class="vx-card-title">Cat&eacute;gories d&#8217;options autoris&eacute;es</span></div>
    <div id="vx-strategy-options">%%LOADING%%</div>
  </section>
</div>''',

    'research': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="Validation hors &eacute;chantillon">
    <div class="vx-card-header"><span class="vx-card-title">Validateur hors &eacute;chantillon</span>
      <span class="vx-actions" id="vx-research-meta"></span></div>
    <div id="vx-research-body">%%LOADING%%</div>
  </section>
  <div class="vx-col-5">
    <div id="vx-research-chart"></div>
    <section class="vx-card vx-mt4" aria-label="Cycle de recherche">
      <div class="vx-card-header"><span class="vx-card-title">Cycle de recherche</span></div>
      <div class="vx-insight" data-tone="ai"><b>IDEA &rarr; BACKTEST &rarr; VALIDATION &rarr; OBSERVATION &rarr; APPROVED.</b>
        Une id&eacute;e de r&egrave;gle traverse chaque &eacute;tape dans l&#8217;ordre : formulation,
        backtest, validation hors &eacute;chantillon (walk-forward, PSR, DSR, PBO),
        p&eacute;riode d&#8217;observation sur donn&eacute;es r&eacute;elles, puis approbation.
        Aucune r&egrave;gle n&#8217;entre dans la constitution sans franchir toutes les
        &eacute;tapes et sans confirmation humaine finale.</div>
    </section>
  </div>
</div>''',

    'impacts': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="&Eacute;v&eacute;nements en direct">
    <div class="vx-card-header"><span class="vx-card-title">&Eacute;v&eacute;nements syst&egrave;me (flux temps r&eacute;el)</span>
      <span class="vx-meta vx-right" id="vx-imp-status">connexion&hellip;</span></div>
    <div id="vx-imp-feed">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-5" aria-label="Cha&icirc;ne d&#8217;impact">
    <div class="vx-card-header"><span class="vx-card-title">Cha&icirc;ne d&#8217;impact (&sect;27)</span></div>
    <div id="vx-imp-flow" style="margin:2px 0 8px"></div>
    <div class="vx-insight vx-mt2" data-tone="risk"><b>Corr&eacute;lation &ne; causalit&eacute;.</b>
      Chaque impact affich&eacute; est POTENTIEL : source, cible, direction et confiance &mdash;
      le recalcul de d&eacute;cision passe toujours par le moteur ex&eacute;cutif unique.</div>
    <div id="vx-imp-counters" class="vx-mt3"></div>
  </section>
</div>
''',
    'memory': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="Th&egrave;ses par titre">
    <div class="vx-card-header"><span class="vx-card-title">Th&egrave;ses &amp; notes par titre</span>
      <span class="vx-actions">
        <button class="vx-btn vx-btn-sm" id="vx-memory-add">Nouvelle th&egrave;se</button></span></div>
    <div id="vx-memory-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-5" aria-label="M&eacute;moire strat&eacute;gique">
    <div class="vx-card-header"><span class="vx-card-title">R&egrave;gles propos&eacute;es / confirm&eacute;es</span></div>
    <div class="vx-insight" data-tone="ai"><b>M&eacute;moire strat&eacute;gique serveur.</b>
      Les r&eacute;gularit&eacute;s d&eacute;tect&eacute;es par les moteurs suivent les statuts
      <b>OBSERVED &rarr; PROPOSED &rarr; CONFIRMED</b>. Une r&egrave;gle n&#8217;est jamais active
      sans confirmation humaine explicite ; jusque-l&agrave; elle reste une simple
      observation journalis&eacute;e c&ocirc;t&eacute; serveur.</div>
    <div class="vx-help vx-mt3">Les th&egrave;ses ci-contre sont vos notes personnelles
      (localStorage, synchronis&eacute;es via le desk). La m&eacute;moire strat&eacute;gique des
      moteurs est g&eacute;r&eacute;e c&ocirc;t&eacute; serveur et versionn&eacute;e avec la constitution.</div>
  </section>
</div>''',
}


_JS = r"""
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script>
(function(){
'use strict';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
const ROOT=document.getElementById('vx-intel');
const VIEW=(ROOT&&ROOT.dataset.view)||'analyst';
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}

/* ══ Vue ANALYSTE ═══════════════════════════════════════════════════ */
function initAnalyst(){
  const idle=VX.states.empty('Aucune analyse lanc&eacute;e — saisissez un ticker ci-contre.','');
  $('vx-analyst-verdict').innerHTML=idle;
  $('vx-analyst-audit').innerHTML=idle;
  /* Suggestions : exemples + tickers récents + raccourcis — rien d'inventé */
(function(){
  const host=$('vx-analyst-suggestions');if(!host)return;
  const recents=(VX.recentTickers&&VX.recentTickers.get&&VX.recentTickers.get())||[];
  const favs=(window.VXEntities&&VXEntities.favorites())||[];
  const EX=['La thèse tient-elle après les résultats ?','Quels risques invalideraient le dossier ?',
    'Le timing est-il aligné avec le régime de marché ?','Que disent les anomalies récentes ?'];
  host.innerHTML=
    '<div class="vx-meta vx-mb1">Exemples de questions</div>'
    +'<div class="vx-flex vx-wrap vx-mb2">'+EX.map(q=>
      `<button type="button" class="vx-chip" data-exq="${q}">${q}</button>`).join('')+'</div>'
    +((recents.length||favs.length)?'<div class="vx-meta vx-mb1">Tickers récents & favoris</div>'
      +'<div class="vx-flex vx-wrap">'+[...new Set([...recents.slice(0,6),...favs.slice(0,4)])].map(t=>
      `<button type="button" class="vx-chip" data-ext="${t}">${t}</button>`).join('')+'</div>':'');
  host.querySelectorAll('[data-exq]').forEach(b=>b.addEventListener('click',()=>{$('vx-analyst-q').value=b.dataset.exq;$('vx-analyst-sym').focus();}));
  host.querySelectorAll('[data-ext]').forEach(b=>b.addEventListener('click',()=>{$('vx-analyst-sym').value=b.dataset.ext;$('vx-analyst-q').focus();}));
})();
$('vx-analyst-form').addEventListener('submit',(e)=>{
    e.preventDefault();
    const sym=($('vx-analyst-sym').value||'').trim().toUpperCase();
    if(!/^[A-Z.\-]{1,7}$/.test(sym)){VX.toast('Ticker invalide','error');return;}
    VX.recentTickers.push(sym);
    runAnalysis(sym,($('vx-analyst-q').value||'').trim());
  });
}
async function runAnalysis(sym,question){
  $('vx-analyst-verdict').innerHTML=VX.states.loading(4);
  $('vx-analyst-audit').innerHTML=VX.states.loading(5);
  $('vx-analyst-scores').innerHTML='';
  const [sd,dd]=await Promise.allSettled([
    VX.fetch('/api/strategy/decision/'+encodeURIComponent(sym),{ttl:15000}),
    VX.fetch('/api/decision/'+encodeURIComponent(sym),{ttl:15000})]);
  const strat=sd.status==='fulfilled'?sd.value:null;
  const deci=dd.status==='fulfilled'?dd.value:null;
  /* Honnêteté : le serveur renvoie 200 + available:false pour un ticker absent du
     scan (strategy_os_api). On NE fabrique PAS un verdict « ATTENDRE » : on affiche
     l'état vide honnête tant qu'aucun dossier réel n'existe. */
  if(!strat||strat.available===false){
    $('vx-analyst-verdict').innerHTML=VX.states.empty(
      sym+' est absent du scan courant — impossible de d&eacute;cider sans donn&eacute;es.',
      '<a class="vx-btn vx-btn-sm" href="/system?view=data">Lancer un scan (Syst&egrave;me)</a>');
    $('vx-analyst-audit').innerHTML=VX.states.empty('Aucun raisonnement disponible sans dossier.');
    return;
  }
  renderVerdict(sym,question,strat,deci);
  renderAudit(strat,deci);
  renderScores(sym,strat);
}
function renderVerdict(sym,question,strat,deci){
  /* Données insuffisantes → état honnête, calme, explicite. JAMAIS une
     apparence de conviction (pas de verdict coloré, pas de comité chiffré). */
  if(deci&&deci.final_decision==='DATA_INSUFFICIENT'){
    const miss=(deci.data_quality&&(deci.data_quality.missing_fields||[]).join(', '))||'données du titre absentes';
    $('vx-analyst-verdict').innerHTML=
      `<div class="vx-flex vx-mb3">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${sym}">${sym}</button>
        <span class="vx-badge" data-decision="INCONNU">Donn&eacute;es insuffisantes</span></div>
      <div class="vx-insufficient"><div class="vx-insufficient-icon">&mdash;</div>
        <div><b>Vertex ne tranche pas ce titre.</b>
        <div class="vx-insufficient-why">Donn&eacute;es insuffisantes (${esc(miss)}). Aucune conviction n&#8217;est affich&eacute;e tant que le dossier n&#8217;est pas complet.</div></div></div>
      ${question?`<div class="vx-help vx-mt2">Question : &laquo; ${esc(question)} &raquo;</div>`:''}
      <div class="vx-flex vx-wrap vx-gap2 vx-mt3">
        <button class="vx-btn vx-btn-sm" data-open-analysis="${sym}">Ouvrir l&#8217;analyse compl&egrave;te</button></div>
      <div class="vx-card-footer">${VX.updateIndicator((strat&&strat.as_of),'decision stack','delayed')}</div>`;
    $('vx-analyst-meta').innerHTML=`<span class="vx-meta">${esc(sym)}</span>`;
    return;
  }
  const decision=(strat&&strat.final_decision)||'ATTENDRE';
  const unknowns=(strat&&strat.unknowns)||[];
  const blocking=(strat&&strat.blocking_rules)||[];
  const lens=deci&&deci.market_lens;
  $('vx-analyst-verdict').innerHTML=
    `<div class="vx-flex vx-mb3">
      <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${sym}">${sym}</button>
      <span class="vx-badge vx-badge-decision" data-decision="${esc(decision)}">${esc(decision)}</span>
      ${E()?E().badges(sym):''}</div>
    ${question?`<div class="vx-help vx-mb2">Question : &laquo; ${esc(question)} &raquo; — r&eacute;ponse via le dossier complet ci-dessous.</div>`:''}
    ${deci&&(deci.decision_label||deci.headline)?`<div class="vx-dim vx-mb2" style="font-size:13px">${esc(deci.decision_label||deci.headline)}</div>`:''}
    ${lens&&lens.summary?`<div class="vx-kv"><span class="k">Prisme march&eacute;</span><span class="v">${esc(lens.summary)}</span></div>`:''}
    ${blocking.length?`<div class="vx-kv"><span class="k">R&egrave;gles bloquantes</span><span class="v vx-neg">${blocking.map(esc).join(' · ')}</span></div>`:''}
    ${unknowns.length?`<div class="vx-kv"><span class="k">Inconnues</span><span class="v vx-muted">${unknowns.map(esc).join(' · ')}</span></div>`
      :'<div class="vx-kv"><span class="k">Inconnues</span><span class="v vx-pos">aucune donn&eacute;e critique manquante</span></div>'}
    <div class="vx-flex vx-wrap vx-gap2 vx-mt3">
      <button class="vx-btn vx-btn-sm" data-open-analysis="${sym}">Ouvrir l&#8217;analyse compl&egrave;te</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" data-entity-menu="${sym}">Actions (suivi, alerte, note…)</button>
    </div>
    <div class="vx-card-footer">${VX.updateIndicator((strat&&strat.as_of),'moteur ex&eacute;cutif + decision stack','delayed')}</div>`;
  $('vx-analyst-meta').innerHTML=`<span class="vx-meta">${esc(sym)}</span>`;
}
function renderAudit(strat,deci){
  const audit=(strat&&strat.audit_trail)||[];
  const order=(strat&&strat.analysis_order)||[];
  const pros=(deci&&deci.pros)||[];const cons=(deci&&deci.cons)||[];
  let html='';
  if(order.length)html+=`<div class="vx-meta vx-mb2">Ordre d&#8217;analyse : ${order.map(esc).join(' &rarr; ')}</div>`;
  html+=audit.length
    ?'<ol style="margin:0;padding-left:20px;line-height:1.8;font-size:13px">'
      +audit.map(a=>`<li>${esc(a)}</li>`).join('')+'</ol>'
    :VX.states.empty('Aucune trace d&#8217;audit fournie par le moteur pour ce titre.');
  if(pros.length||cons.length){
    html+='<div class="vx-grid vx-mt3">'
      +`<div class="vx-col-6"><div class="vx-meta vx-mb1">Arguments pour</div>${pros.slice(0,3).map(p=>`<div class="vx-pos" style="font-size:12px">+ ${esc(p)}</div>`).join('')||'<span class="vx-muted">—</span>'}</div>`
      +`<div class="vx-col-6"><div class="vx-meta vx-mb1">Arguments contre</div>${cons.slice(0,3).map(c=>`<div class="vx-neg" style="font-size:12px">− ${esc(c)}</div>`).join('')||'<span class="vx-muted">—</span>'}</div></div>`;
  }
  $('vx-analyst-audit').innerHTML=html;
}
function renderScores(sym,strat){
  const s=strat&&strat.scores;
  const host=$('vx-analyst-scores');
  if(!s){host.innerHTML='<div class="vx-card">'
    +VX.states.empty('Scores indisponibles pour '+esc(sym)+' — dossier absent du moteur ex&eacute;cutif.')+'</div>';return;}
  const axes=[{label:'Conviction',value:s.conviction??0},{label:'Risque',value:s.risk??0},
    {label:'Timing',value:s.timing??0},{label:'Asym&eacute;trie',value:s.asymmetry??0},
    {label:'Donn&eacute;es',value:s.data_quality??0}];
  const capped=(strat.blocking_rules||[]).length;
  whenChartsReady(()=>{
    host.classList.add('vx-card');
    host.innerHTML='<div class="vx-chart-head"><span class="vx-chart-title">Scores du dossier '+esc(sym)+'</span>'
      +'<span class="vx-chart-question">O&ugrave; le dossier est-il fort, o&ugrave; est-il fragile ?</span></div>'
      +'<div id="vx-analyst-radar" class="vx-mb2"></div>'
      +axes.map(function(a){const v=a.value;const cls=v>=70?'vx-pos':v>=50?'vx-warn':'vx-neg';
        return '<div class="vx-kv"><span class="k">'+a.label+'</span><span class="v vx-mono '+cls+'">'+VX.fmt.num(v,0)+' / 100</span></div>';}).join('')
      +'<div class="vx-card-foot"><span class="vx-meta">Cinq scores du moteur ex&eacute;cutif d&eacute;terministe (0-100)'
      +(capped?' — conviction plafonn&eacute;e par une r&egrave;gle bloquante':'')+'.</span></div>';
    if(window.VXCharts&&VXCharts.radar)
      VXCharts.radar('vx-analyst-radar',{axes:axes,max:100,ariaLabel:'Scores dossier '+sym,color:VXCharts.colors.brand});
  });
}

/* ══ Vue COMITÉ ═════════════════════════════════════════════════════ */
const DECISION_GROUP={STRONG_BUY:'ACHETER',BUY:'ACHETER',BUY_PULLBACK:'ACHETER',
  WATCH_BREAKOUT:'ATTENDRE',WAIT:'ATTENDRE',TOO_LATE:'ATTENDRE',
  AVOID:'REFUSER',NO_NEW_RISK:'REFUSER'};
let committeeData=null,committeeFilter='';
async function initCommittee(){
  try{
    committeeData=await VX.fetch('/api/committee-review',{ttl:60000});
    renderCommittee();
  }catch(e){
    $('vx-committee-body').innerHTML=VX.states.error('Comit&eacute; indisponible ('+esc(e.message)+')');
  }
}
function renderCommittee(){
  const c=committeeData;const reviews=c.reviews||[];
  const tally=c.tally||{};
  /* Hero §40 : jauge de convergence (accord moyen) + KPI + répartition des verdicts.
     Agrégations RÉELLES des reviews ; aucune valeur inventée. */
  try{
    var _avg=function(k){var xs=reviews.map(function(r){return r[k];}).filter(function(v){return typeof v==='number';});return xs.length?Math.round(xs.reduce(function(a,b){return a+b;},0)/xs.length):null;};
    var _conv=_avg('agreement'),_convc=_avg('conviction'),_conf=_avg('confidence');
    var _contra=reviews.filter(function(r){return r&&r.has_contradiction;}).length;
    whenChartsReady(function(){ if(window.VXCharts&&VXCharts.gauge) VXCharts.gauge('vx-committee-gauge',{
      value:_conv,min:0,max:100,unit:'',label:'Accord moyen',
      reading:_conv==null?'donnée indisponible':(_conv>=70?'forte convergence':_conv>=40?'convergence modérée':'faible convergence'),
      bands:[{to:40,color:VXCharts.colors.negative},{to:70,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.positive}]}); });
    var _kp=function(l,v,d){return '<div class="vx-card vx-card--compact vx-kpi vx-col-3"><span class="vx-kpi-label">'+l+'</span><span class="vx-kpi-value" style="font-size:22px">'+(v==null?'—':v)+'</span>'+(d?'<span class="vx-kpi-delta vx-muted">'+d+'</span>':'')+'</div>';};
    var _kh=$('vx-committee-kpis');
    if(_kh){_kh.innerHTML=
      _kp('Univers scanné',c.universe_scanned!=null?c.universe_scanned:c.count,'dossiers')
      +_kp('Conviction moy.',_convc,'/100')
      +_kp('Confiance moy.',_conf,'/100')
      +_kp('Contradictions',_contra,_contra?'à arbitrer':'aucune');
      /* Contexte marché qui conditionne la revue du comité — servi par l'API mais
         jamais affiché jusqu'ici (RoRo / régime SPY / bande VIX). '—' honnête si null. */
      var _mk=c.market||{};
      if(_mk.roro||_mk.spy_regime||_mk.vix_band){
        _kh.innerHTML+='<div class="vx-card vx-card--compact" style="grid-column:span 12;display:flex;gap:20px;flex-wrap:wrap;align-items:center;margin-top:2px">'
          +'<span class="vx-kpi-label" style="letter-spacing:.04em">Contexte marché</span>'
          +'<span class="vx-kv"><span class="k">RoRo</span><span class="v">'+(_mk.roro?esc(_mk.roro):'—')+'</span></span>'
          +'<span class="vx-kv"><span class="k">Régime S&amp;P</span><span class="v">'+(_mk.spy_regime?esc(_mk.spy_regime):'—')+'</span></span>'
          +'<span class="vx-kv"><span class="k">Bande VIX</span><span class="v">'+(_mk.vix_band?esc(_mk.vix_band):'—')+'</span></span>'
          +'</div>';
      }
    }
    var _tone={AVOID:'var(--vx-negative)',WAIT:'var(--vx-warning)',WATCH_BREAKOUT:'var(--vx-brand)',ACHETER:'var(--vx-positive)',RENFORCER:'var(--vx-positive)',ATTENDRE:'var(--vx-warning)'};
    var _tk=Object.keys(tally),_tmax=Math.max.apply(null,[1].concat(_tk.map(function(k){return tally[k];})));
    var _th=$('vx-committee-tally');
    if(_th)_th.innerHTML='<div class="vx-kpi-label vx-mb2">Répartition des verdicts</div>'+_tk.sort(function(a,b){return tally[b]-tally[a];}).map(function(k){var w=Math.round(tally[k]/_tmax*100);
      return '<div style="display:flex;align-items:center;gap:10px;margin:5px 0"><span style="width:140px;font-size:12px;color:var(--vx-text-secondary)">'+esc(k)+'</span><span style="flex:1;height:12px;background:var(--vx-surface-3);border-radius:6px;overflow:hidden"><span style="display:block;height:100%;width:'+w+'%;background:'+(_tone[k]||'var(--vx-neutral-chart)')+';border-radius:6px"></span></span><span class="vx-mono" style="width:34px;text-align:right;font-size:12px">'+tally[k]+'</span></div>';}).join('');
  }catch(e){}
  $('vx-committee-meta').innerHTML=VX.updateIndicator(c.as_of,
    (c.data_source==='demo'?'d&eacute;mo':'scan')+' · '+(c.universe_scanned??reviews.length)+' titres pass&eacute;s en revue',
    c.data_source==='demo'?'fallback':'delayed');
  const chips=[['','Toutes ('+reviews.length+')']].concat(
    Object.keys(tally).sort().map(k=>[k,k+' ('+tally[k]+')']));
  $('vx-committee-chips').innerHTML=chips.map(([val,label])=>
    `<button class="vx-chip" data-filter-key="decision" data-filter-value="${esc(val)}"
      aria-pressed="${String(val===committeeFilter)}">${esc(label)}</button>`).join('');
  document.querySelectorAll('#vx-committee-chips .vx-chip').forEach(ch=>
    ch.addEventListener('click',()=>{committeeFilter=ch.dataset.filterValue;renderCommittee();}));
  const rows=reviews.filter(r=>!committeeFilter||r.decision===committeeFilter);
  if(!rows.length){
    $('vx-committee-body').innerHTML=VX.states.empty(
      reviews.length?'Aucun titre ne correspond &agrave; ce filtre.'
      :'Aucune revue disponible — le scan n&#8217;a pas encore tourn&eacute;.',
      reviews.length?'':'<a class="vx-btn vx-btn-sm" href="/system?view=data">Syst&egrave;me / Donn&eacute;es</a>');
    return;
  }
  $('vx-committee-body').innerHTML=`<div style="overflow-x:auto"><table class="vx-table">
    <thead><tr><th>Titre</th><th>D&eacute;cision</th><th class="vx-num">Conviction</th>
    <th class="vx-num">Accord</th><th class="vx-num">Prix</th><th><span class="vx-sr-only">D&eacute;tail</span></th><th><span class="vx-sr-only">Actions</span></th></tr></thead><tbody>`
    +rows.map((r,i)=>{
      const grp=DECISION_GROUP[r.decision]||'ATTENDRE';
      const agree=r.agreement===null||r.agreement===undefined?null
        :(r.agreement<=1?r.agreement*100:r.agreement);
      return `<tr>
        <td><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(r.symbol)}">${esc(r.symbol)}</button>
          ${r.has_contradiction?'<span class="vx-badge" style="color:var(--vx-warning)" title="Le comit&eacute; est divis&eacute; sur ce titre">contradiction</span>':''}</td>
        <td><span class="vx-badge vx-badge-decision" data-decision="${esc(grp)}" title="${esc(r.decision)}">${esc(r.label||r.decision)}</span></td>
        <td class="vx-num vx-mono">${VX.fmt.nd(r.conviction!==null&&r.conviction!==undefined?VX.fmt.num(r.conviction,0):null)}</td>
        <td class="vx-num vx-mono">${agree===null?'—':VX.fmt.num(agree,0)+' %'}</td>
        <td class="vx-num vx-mono">${r.price!==null&&r.price!==undefined?VX.fmt.price(r.price):'—'}</td>
        <td><button class="vx-btn vx-btn-sm vx-btn-ghost" data-committee-detail="${i}" aria-expanded="false">D&eacute;tail</button></td>
        <td><button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${esc(r.symbol)}" aria-label="Actions ${esc(r.symbol)}">⋯</button></td>
      </tr>
      <tr id="vx-cdetail-${i}" hidden><td colspan="7">
        <div class="vx-grid" style="padding:6px 4px">
          <div class="vx-col-4"><div class="vx-meta vx-mb1">Argument pour</div>
            <div class="vx-pos" style="font-size:12px">${esc(r.top_pro||'—')}</div></div>
          <div class="vx-col-4"><div class="vx-meta vx-mb1">Argument contre</div>
            <div class="vx-neg" style="font-size:12px">${esc(r.top_con||'—')}</div></div>
          <div class="vx-col-4"><div class="vx-meta vx-mb1">Avocat du diable</div>
            <div class="vx-dim" style="font-size:12px">${esc(r.devils_advocate||'aucune objection formulée')}</div></div>
        </div></td></tr>`;
    }).join('')+'</tbody></table></div>'
    +`<div class="vx-card-footer">Confiance et accord calcul&eacute;s par les moteurs — le comit&eacute; ne passe jamais un ordre.</div>`;
  document.querySelectorAll('[data-committee-detail]').forEach(b=>
    b.addEventListener('click',()=>{
      const row=$('vx-cdetail-'+b.dataset.committeeDetail);
      row.hidden=!row.hidden;
      b.setAttribute('aria-expanded',String(!row.hidden));
    }));
}

/* ══ Vue STRATÉGIE ══════════════════════════════════════════════════ */
async function initStrategy(){
  try{
    const p=await VX.fetch('/api/strategy/profile',{ttl:300000});
    const raw=p.profile||{};
    const kv=(k,v)=>`<div class="vx-kv"><span class="k">${k}</span><span class="v">${v}</span></div>`;
    const tgt=raw.portfolio_target_positions||{};
    const pref=raw.preferred_stock_weight_pct||[];
    $('vx-strategy-core').innerHTML=
      kv('Identifiant',esc(p.strategy_id||'—'))
      +kv('Version','v'+esc(p.version)+' · disponibles : '+((p.versions_available||[]).map(esc).join(', ')||'—'))
      +kv('Style',esc(p.style||'—'))
      +kv('Positions cibles',(tgt.minimum??'—')+' &agrave; '+(tgt.maximum??'—'))
      +kv('Poids par titre','max '+VX.fmt.nd(raw.max_stock_weight_pct)+' % · pr&eacute;f&eacute;r&eacute; '
        +(pref.length===2?pref[0]+'-'+pref[1]+' %':'—'))
      +kv('Drawdown max portefeuille',VX.fmt.nd(raw.portfolio_max_drawdown_pct)+' %')
      +kv('Drawdown max par titre',VX.fmt.nd(raw.stock_max_drawdown_pct)+' %')
      +kv('Options simultan&eacute;es max',VX.fmt.nd(raw.max_simultaneous_options))
      +kv('Ordre d&#8217;analyse',(raw.analysis_order||[]).map(esc).join(' &rarr; ')||'—')
      +kv('D&eacute;cisions autoris&eacute;es',(raw.allowed_final_decisions||[]).map(d=>
        `<span class="vx-badge vx-badge-decision" data-decision="${esc(d)}">${esc(d)}</span>`).join(' ')||'—')
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'constitution serveur v'+esc(p.version),'delayed')}</div>`;
    $('vx-strategy-meta').innerHTML=`<span class="vx-badge">v${esc(p.version)}</span>`;
    renderGates(raw);
    renderOptionCategories(raw.options_profile||{});
  }catch(e){
    const err=VX.states.error('Constitution indisponible ('+esc(e.message)+')');
    $('vx-strategy-core').innerHTML=err;
    $('vx-strategy-gates').innerHTML=err;
    $('vx-strategy-options').innerHTML=err;
  }
}
function renderGates(raw){
  const op=raw.options_profile||{};
  const gates=[];
  if(op.short_options===false)gates.push('Vente d&#8217;options interdite (jamais short premium)');
  if(op.naked_options===false)gates.push('Options nues interdites');
  if(op.credit_spreads===false)gates.push('Credit spreads interdits');
  if(op.automatic_execution===false)gates.push('Ex&eacute;cution automatique interdite — analyse uniquement');
  if(raw.portfolio_max_drawdown_pct!==undefined)
    gates.push('Drawdown portefeuille plafonn&eacute; &agrave; '+raw.portfolio_max_drawdown_pct+' %');
  if(raw.stock_max_drawdown_pct!==undefined)
    gates.push('Drawdown par titre plafonn&eacute; &agrave; '+raw.stock_max_drawdown_pct+' %');
  if(raw.max_stock_weight_pct!==undefined)
    gates.push('Poids max par titre : '+raw.max_stock_weight_pct+' %');
  if(op.max_simultaneous_bearish_positions!==undefined)
    gates.push('Positions baissi&egrave;res simultan&eacute;es : max '+op.max_simultaneous_bearish_positions);
  gates.push('READONLY produit : aucun ordre n&#8217;est jamais pass&eacute; (disabled-by-design)');
  $('vx-strategy-gates').innerHTML='<ul style="margin:0;padding-left:18px;line-height:1.9;font-size:13px">'
    +gates.map(g=>`<li>${g}</li>`).join('')+'</ul>';
}
function renderOptionCategories(op){
  const cats=op.categories||{};
  const names=Object.keys(cats);
  if(!names.length){
    $('vx-strategy-options').innerHTML=VX.states.empty('Aucune cat&eacute;gorie d&#8217;options d&eacute;finie dans la constitution.');
    return;
  }
  const band=(a)=>Array.isArray(a)&&a.length===2?a[0]+' &agrave; '+a[1]:'—';
  $('vx-strategy-options').innerHTML=
    `<div class="vx-meta vx-mb2">Direction principale : ${esc(op.primary_direction||'—')} ·
      DTE absolu ${VX.fmt.nd(op.dte&&op.dte.absolute_minimum)}-${VX.fmt.nd(op.dte&&op.dte.absolute_maximum)} j ·
      d&eacute;tention ${VX.fmt.nd(op.holding_period_days&&op.holding_period_days.minimum)}-${VX.fmt.nd(op.holding_period_days&&op.holding_period_days.maximum)} j</div>
    <div style="overflow-x:auto"><table class="vx-table">
    <thead><tr><th>Cat&eacute;gorie</th><th class="vx-num">Delta</th><th class="vx-num">DTE pr&eacute;f&eacute;r&eacute;</th>
    <th class="vx-num">Gain cible %</th><th class="vx-num">Perte planifi&eacute;e %</th><th>Notes</th></tr></thead><tbody>`
    +names.map(n=>{
      const c=cats[n]||{};
      const dmin=c.delta_min??c.delta_abs_min,dmax=c.delta_max??c.delta_abs_max;
      const notes=[c.primary?'principale':'',c.rare_setup_only?'setup rare uniquement':'',
        c.frequency?('fr&eacute;quence '+esc(c.frequency)):''].filter(Boolean).join(' · ');
      return `<tr><td><b>${esc(n)}</b></td>
        <td class="vx-num vx-mono">${VX.fmt.nd(dmin)} &agrave; ${VX.fmt.nd(dmax)}</td>
        <td class="vx-num vx-mono">${band(c.preferred_dte)} j</td>
        <td class="vx-num vx-mono">${band(c.target_gain_pct)}</td>
        <td class="vx-num vx-mono">${band(c.planned_loss_pct)}</td>
        <td class="vx-dim" style="font-size:12px">${notes||'—'}</td></tr>`;
    }).join('')+'</tbody></table></div>';
}

/* ══ Vue RECHERCHE ══════════════════════════════════════════════════ */
async function initResearch(){
  try{
    const v=await VX.fetch('/api/validator',{ttl:120000});
    if(!v.ok){
      $('vx-research-body').innerHTML=VX.states.empty(
        'Validation indisponible : '+esc(v.note||'historique insuffisant')+'. '
        +'Le validateur exige une courbe d&#8217;equity r&eacute;elle — rien n&#8217;est simul&eacute; pour combler.',
        '<a class="vx-btn vx-btn-sm" href="/performance">Ouvrir Performance</a>');
      $('vx-research-chart').innerHTML='';
      return;
    }
    const row=(k,val,hint)=>`<tr><td>${k}${hint?` <span class="vx-meta">${hint}</span>`:''}</td>
      <td class="vx-num vx-mono">${val}</td></tr>`;
    $('vx-research-meta').innerHTML=
      `<span class="vx-badge" style="color:${esc(v.color||'inherit')}">${esc(v.verdict||'—')}</span>`;
    $('vx-research-body').innerHTML=
      `<div style="overflow-x:auto"><table class="vx-table"><thead>
        <tr><th>M&eacute;trique</th><th class="vx-num">Valeur</th></tr></thead><tbody>`
      +row('Sharpe annualis&eacute;',VX.fmt.num(v.sharpe_ann,2))
      +row('PSR',VX.fmt.num(v.psr0,3),'probabilit&eacute; que le Sharpe r&eacute;el d&eacute;passe 0')
      +row('DSR',VX.fmt.num(v.dsr,3),'Sharpe d&eacute;flat&eacute; ('+VX.fmt.nd(v.n_trials)+' essais)')
      +row('Walk-forward positif',VX.fmt.num(v.folds_positive_pct,0)+' %','fen&ecirc;tres au Sharpe &gt; 0')
      +row('Sharpe in-sample',VX.fmt.num(v.sr_in_sample,2))
      +row('Sharpe out-of-sample',VX.fmt.num(v.sr_out_sample,2))
      +row('D&eacute;gradation IS &rarr; OOS',VX.fmt.num(v.degradation,2))
      +row('PBO (proxy)',VX.fmt.num(v.pbo_estimate,2),'probabilit&eacute; de sur-optimisation')
      +row('Skew / Kurtosis',VX.fmt.num(v.skew,2)+' / '+VX.fmt.num(v.kurtosis,2))
      +row('Observations',VX.fmt.nd(v.n))
      +'</tbody></table></div>'
      +`<div class="vx-insight vx-mt3" data-tone="${v.verdict==='FRAGILE'?'risk':'ai'}">${esc(v.note||'')}</div>`
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'validateur hors &eacute;chantillon (indicatif)','delayed')}</div>`;
    const folds=v.fold_sharpes||[];
    if(folds.length){
      whenChartsReady(()=>VXCharts.barCard('vx-research-chart',{
        title:'Sharpe par fen&ecirc;tre (walk-forward)',
        question:'L&#8217;edge tient-il fen&ecirc;tre apr&egrave;s fen&ecirc;tre ?',
        conclusion:VX.fmt.num(v.folds_positive_pct,0)+' % des fen&ecirc;tres positives — verdict '+(v.verdict||'n/d'),
        labels:folds.map((_,i)=>'F'+(i+1)),values:folds,height:190,
        source:'validateur hors &eacute;chantillon',timestamp:Date.now(),mode:'delayed',
        limits:'indicatif — d&eacute;pend de l&#8217;historique disponible',
        explain:{shows:'Le Sharpe annualis&eacute; recalcul&eacute; sur chaque fen&ecirc;tre temporelle disjointe.',
          why:'Un edge r&eacute;el survit hors de la fen&ecirc;tre o&ugrave; il a &eacute;t&eacute; d&eacute;couvert.',
          confirm:'Une large majorit&eacute; de fen&ecirc;tres positives avec DSR &eacute;lev&eacute;.',
          invalidate:'Des fen&ecirc;tres n&eacute;gatives r&eacute;p&eacute;t&eacute;es ou une forte d&eacute;gradation IS &rarr; OOS.'}}));
    }else $('vx-research-chart').innerHTML='';
  }catch(e){
    $('vx-research-body').innerHTML=VX.states.error('Validateur indisponible ('+esc(e.message)+')');
  }
}

/* ══ Vue MÉMOIRE ════════════════════════════════════════════════════ */
function initMemory(){
  renderMemory();
  $('vx-memory-add').addEventListener('click',()=>{
    if(E())E().openAddModal('','note');else VX.toast('Couche entités indisponible','error');
  });
  VX.bus.on('vx:thesis-changed',renderMemory);
  VX.bus.on('vx:data-refreshed',renderMemory);
}
function renderMemory(){
  const notes=(E()&&E().notes())||{};
  const syms=Object.keys(notes).sort();
  if(!syms.length){
    $('vx-memory-body').innerHTML=VX.states.empty(
      'Aucune th&egrave;se enregistr&eacute;e — vos notes par titre appara&icirc;tront ici (synchronis&eacute;es via le desk).',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'note\')">Cr&eacute;er une th&egrave;se</button>');
    return;
  }
  $('vx-memory-body').innerHTML=`<div style="overflow-x:auto"><table class="vx-table">
    <thead><tr><th>Titre</th><th>Th&egrave;se / note</th><th><span class="vx-sr-only">Modifier</span></th><th><span class="vx-sr-only">Actions</span></th></tr></thead><tbody>`
    +syms.map(sym=>`<tr>
      <td><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(sym)}">${esc(sym)}</button></td>
      <td class="vx-dim" style="font-size:13px;max-width:480px">${esc(String(notes[sym]).slice(0,220))}${String(notes[sym]).length>220?'…':''}</td>
      <td><button class="vx-btn vx-btn-sm" data-edit-note="${esc(sym)}">Modifier</button></td>
      <td><button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${esc(sym)}" aria-label="Actions ${esc(sym)}">⋯</button></td>
    </tr>`).join('')+'</tbody></table></div>'
    +`<div class="vx-card-footer">${syms.length} th&egrave;se(s) · stock&eacute;es en local, synchronis&eacute;es via /api/desk</div>`;
  document.querySelectorAll('[data-edit-note]').forEach(b=>
    b.addEventListener('click',()=>E()&&E().openAddModal(b.dataset.editNote,'note')));
}

/* ══ Orchestration ══════════════════════════════════════════════════ */
function initImpacts(){
  const feed=[];const MAX=40;
  const CHANNELS=['market','positions','options','portfolio','decisions','alerts','connections','jobs','system'];
  function paintStatus(){const el=$('vx-imp-status');
    if(el)el.textContent='flux '+((VX.liveStatus&&VX.liveStatus())||'—');}
  function paint(){
    const el=$('vx-imp-feed');if(!el)return;
    el.innerHTML=feed.length?feed.slice(0,MAX).map(ev=>`
      <div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <span class="vx-badge" style="color:var(--vx-info)">${esc(ev.channel)}</span>
        <span class="vx-grow vx-mono vx-meta" style="font-size:11.5px">${esc(JSON.stringify(ev.data||{}).slice(0,110))}</span>
        <span class="vx-meta">${VX.fmt.ago(ev.ts*1000)}</span></div>`).join('')
      :VX.states.empty('Aucun événement reçu pour l’instant — le flux se remplit au rythme des scans, alertes et jobs.',
        '<span class="vx-meta">SSE '+((VX.liveStatus&&VX.liveStatus())||'')+'</span>');
    const counts={};feed.forEach(e=>counts[e.channel]=(counts[e.channel]||0)+1);
    const c=$('vx-imp-counters');
    if(c)c.innerHTML=Object.entries(counts).map(([k,v])=>
      `<div class="vx-kv"><span class="k">${esc(k)}</span><span class="v vx-mono">${v}</span></div>`).join('')
      ||'<span class="vx-meta">Compteurs vides.</span>';
    /* Chaîne d'impact en flow diagram — compteurs live par nœud raccordé à un canal */
    if(window.VXCharts&&VXCharts.flow){
      const chain=[['Marché','market'],['Régime',null],['Secteur',null],['Entreprise',null],
        ['Opportunité',null],['Position','positions'],['Option','options'],['Portefeuille','portfolio'],
        ['Risque',null],['Décision','decisions']];
      VXCharts.flow('vx-imp-flow',{ariaLabel:'Chaîne d\'impact',
        nodes:chain.map(function(p){const cnt=p[1]?(counts[p[1]]||0):null;
          return {label:p[0],count:cnt,tone:(cnt>0?'active':'idle')};})});
    }
  }
  CHANNELS.forEach(ch=>VX.bus.on('vx:live:'+ch,(e)=>{
    feed.unshift({channel:ch,data:e.detail,ts:Date.now()/1000});
    if(feed.length>MAX)feed.pop();paint();}));
  VX.bus.on('vx:live-status',paintStatus);
  paintStatus();paint();
  whenChartsReady(paint);   /* re-render une fois chart-core.js (defer) chargé → flow diagram */
}
if(VIEW==='analyst')initAnalyst();
else if(VIEW==='committee'){initCommittee();VX.refresh.register(initCommittee,120000,'committee');}
else if(VIEW==='strategy')initStrategy();
else if(VIEW==='research')initResearch();
else if(VIEW==='impacts')initImpacts();
else if(VIEW==='memory')initMemory();
VX.context.restoreIfReturning();
})();
</script>
"""


def render(view: str = 'analyst') -> str:
    view = view if view in dict(VIEWS) else _DEFAULT_VIEW
    body = _VIEW_CONTENT[view].replace(
        '%%LOADING%%', '<div class="vx-skeleton" style="height:60px"></div>').replace(
        '%%IDLE%%', '<div class="vx-skeleton" style="height:40px"></div>')
    content = (_header(view)
               + f'<div id="vx-intel" data-view="{view}">' + body + '</div>')
    sub = dict(VIEWS)[view]
    return render_shell(title='Intelligence', active='intelligence',
                        space_label='Intelligence', sub_label=sub,
                        content=content, page_js=_JS,
                        page_label='Intelligence — ' + sub)
