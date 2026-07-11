"""vertex.ui.pages.analysis_page — la fiche canonique (§26).

Question : « Cette entreprise et cette opportunité méritent-elles du capital
maintenant ? ». Ordre strict : résumé décisionnel → thèse → graphique →
fondamental → catalyseurs → technique → sentiment → anomalies → scénarios →
plan → options → compatibilité portefeuille → historique.
Tout ticker, partout dans l'app, ouvre CETTE fiche.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell


def render_index(view: str = '') -> str:
    content = """
<div class="vx-page-header"><div><h1>Analyse</h1>
<div class="vx-sub">Rechercher un titre pour ouvrir sa fiche canonique.</div></div></div>
<div class="vx-card" style="max-width:640px">
  <div class="vx-field"><label for="an-search">Ticker ou entreprise</label>
  <input class="vx-input" id="an-search" placeholder="ex. NVDA, Microsoft…" autocomplete="off"
    style="font-size:16px;padding:12px" /></div>
  <div id="an-results" class="vx-flex-col"></div>
  <div class="vx-help vx-mt2">Astuce : ⌘K / Ctrl+K depuis n’importe quelle page.</div>
</div>
<div class="vx-section-header"><h2>Titres récents</h2></div>
<div class="vx-flex vx-wrap" id="an-recent"></div>
"""
    js = r"""
<script>
(function(){
const $=(id)=>document.getElementById(id);
$('an-recent').innerHTML=VX.recentTickers.get().map(s=>
  `<button class="vx-btn vx-ticker" data-open-analysis="${s}">${s}</button>`).join('')
  ||'<span class="vx-muted">Aucun titre consulté récemment.</span>';
let names=null;
$('an-search').addEventListener('input',async function(){
  const q=this.value.trim().toUpperCase();
  if(!q){$('an-results').innerHTML='';return}
  try{ if(!names){const d=await VX.fetch('/api/names',{ttl:600000});names=d.names||d;} }catch(e){names={};}
  const hits=Object.entries(names).filter(([s,n])=>s.startsWith(q)||String(n).toUpperCase().includes(q)).slice(0,8);
  $('an-results').innerHTML=(hits.length?hits:( /^[A-Z.]{1,6}$/.test(q)?[[q,'ouvrir la fiche']]:[]))
    .map(([s,n])=>`<button class="vx-btn" style="justify-content:flex-start" data-open-analysis="${s}">
      <span class="vx-ticker" style="min-width:64px">${s}</span><span class="vx-dim">${n}</span></button>`).join('')
    ||VX.states.empty('Aucun titre trouvé dans l’univers.');
});
$('an-search').focus();
})();
</script>
"""
    return render_shell(title='Analyse', active='analysis', space_label='Analyse',
                        content=content, page_js=js, page_label='Analyse')


_SECTIONS = """
<div id="an-stale"></div>
<!-- 1. Résumé décisionnel (header sticky géré en CSS local) -->
<div class="vx-card vx-accent" id="an-hero" style="position:sticky;top:calc(var(--vx-topbar-h) + 8px);z-index:20">
  <div class="vx-flex vx-wrap">
    <span class="vx-ticker" style="font-size:22px" id="an-sym">%%SYM%%</span>
    <span class="vx-dim" id="an-name">—</span>
    <span class="vx-kpi-value" style="font-size:22px" id="an-price">—</span>
    <span class="vx-mono" id="an-change">—</span>
    <span class="vx-badge vx-badge-decision" id="an-decision" data-decision="">—</span>
    <span id="an-badges"></span>
    <span class="vx-right vx-flex">
      <button class="vx-btn vx-btn-icon vx-btn-ghost" id="an-fav" aria-label="Favori" title="Favori">★</button>
      <button class="vx-btn vx-btn-sm" data-entity-menu="%%SYM%%">Actions ▾</button>
    </span>
  </div>
  <div class="vx-flex vx-wrap vx-mt2" id="an-scores" aria-label="Scores"></div>
</div>

<!-- 2. Thèse -->
<section class="vx-card vx-mt4" id="an-thesis-card">
  <div class="vx-card-header"><span class="vx-card-title">Thèse</span>
    <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost"
      onclick="VXEntities.openAddModal('%%SYM%%','note')">Éditer</button></span></div>
  <div id="an-thesis" class="vx-dim">—</div>
</section>

<!-- 3. Graphique principal -->
<div class="vx-mt4" id="an-chart"></div>

<!-- 4-8. Dimensions dans l'ordre imposé -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" id="an-fundamental"><div class="vx-card-header">
    <span class="vx-card-title">1 · Fondamental</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-catalysts"><div class="vx-card-header">
    <span class="vx-card-title">2 · Catalyseurs</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-technical"><div class="vx-card-header">
    <span class="vx-card-title">3 · Timing technique</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-sentiment"><div class="vx-card-header">
    <span class="vx-card-title">4 · Sentiment & positionnement</span></div><div data-body>%%LOADING%%</div></section>
</div>

<!-- 8. Anomalies + signaux TradingView -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" id="an-anomalies"><div class="vx-card-header">
    <span class="vx-card-title">Anomalies</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-5" id="an-tv"><div class="vx-card-header">
    <span class="vx-card-title">Signaux TradingView</span></div><div data-body>%%LOADING%%</div></section>
</div>

<!-- 9-10. Scénarios + plan -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" id="an-scenarios"><div class="vx-card-header">
    <span class="vx-card-title">Scénarios Bull / Base / Bear</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-5" id="an-plan"><div class="vx-card-header">
    <span class="vx-card-title">Plan</span></div><div data-body>%%LOADING%%</div></section>
</div>

<!-- 11. Options -->
<section class="vx-card vx-mt4" id="an-options">
  <div class="vx-card-header"><span class="vx-card-title">Options — Vertex Dynamic Options</span>
    <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost"
      href="/opportunities?view=options&sym=%%SYM%%">Ouvrir le desk options →</a></span></div>
  <div data-body>%%LOADING%%</div>
</section>

<!-- 12-13. Portefeuille + historique -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" id="an-portfolio-fit"><div class="vx-card-header">
    <span class="vx-card-title">Compatibilité portefeuille</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-history"><div class="vx-card-header">
    <span class="vx-card-title">Historique (journal & suivis)</span></div><div data-body>%%LOADING%%</div></section>
</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/price-chart.js" defer></script>
<script src="/static/vertex/js/charts/candlestick-chart.js" defer></script>
<script src="/static/vertex/js/charts/annotations.js" defer></script>
<script>
(function(){
'use strict';
const SYM=%%SYM_JSON%%;
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function body(id,html){const el=document.querySelector('#'+id+' [data-body]');if(el)el.innerHTML=html;}
function kv(k,v,cls){return `<div class="vx-kv"><span class="k">${k}</span><span class="v ${cls||''}">${VX.fmt.nd(v)}</span></div>`;}

VX.recentTickers.push(SYM);

/* Header : badges entités + favori */
function paintBadges(){
  $('an-badges').innerHTML=E()?E().badges(SYM):'';
  $('an-fav').style.color=E()&&E().isFavorite(SYM)?'#FFD27A':'var(--vx-text-muted)';
}
$('an-fav').addEventListener('click',()=>{E().toggleFavorite(SYM);paintBadges();});
['vx:favorites-changed','vx:watchlist-changed','vx:follow-changed','vx:position-changed','vx:alert-changed']
  .forEach(ev=>VX.bus.on(ev,paintBadges));

/* Thèse (note utilisateur) */
function paintThesis(){
  const note=E()&&E().note(SYM);
  $('an-thesis').innerHTML=note?esc(note).replace(/\n/g,'<br>'):
    VX.states.empty('Aucune thèse enregistrée sur ce titre.',
      `<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${SYM}','note')">Écrire la thèse</button>`);
}
VX.bus.on('vx:thesis-changed',paintThesis);

/* Dossier principal — /api/ticker + décision exécutive */
let TF='6m'; let TICKER=null;
async function loadDossier(){
  let t=null,exec=null,stale=false;
  try{t=await VX.fetch('/api/ticker/'+SYM,{ttl:60000});}catch(e){}
  try{exec=await VX.fetch('/api/strategy/decision/'+SYM,{ttl:60000});}catch(e){}
  TICKER=t;
  const d=(t&&t.detail)||{};
  const demo=!!(window.__vxStatus&&window.__vxStatus.demo);
  if(!t||!t.in_universe&&!d.price){
    $('an-stale').innerHTML='<div class="vx-error-banner">Titre hors du scan courant — dossier partiel. '
      +'<a class="vx-btn vx-btn-sm" href="/system?view=data">Vérifier les données</a></div>';
  }
  /* Hero */
  $('an-name').textContent=(t&&t.company&&(t.company.name||t.company.shortName))||'';
  $('an-price').textContent=VX.fmt.nd(d.price!==undefined?VX.fmt.price(d.price):null);
  const chg=d.change;
  $('an-change').textContent=chg!==undefined?VX.fmt.pct(chg):'n/d';
  $('an-change').className='vx-mono '+(chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted');
  const decision=(exec&&exec.final_decision)||'ATTENDRE';
  const db=$('an-decision');db.textContent=decision;db.dataset.decision=decision.replace('É','E');
  const sc=(exec&&exec.scores)||{};
  $('an-scores').innerHTML=[['Conviction',sc.conviction],['Risque',sc.risk],['Timing',sc.timing],
    ['Asymétrie',sc.asymmetry],['Qualité données',sc.data_quality]].map(([k,v])=>
    `<span class="vx-badge" title="${k}">${k} <b class="vx-mono">${VX.fmt.nd(v)}</b></span>`).join('')
    +(demo?'<span class="vx-badge" style="color:var(--vx-warning)">DÉMO</span>':'');

  /* 3. Graphique principal */
  const closes=(d.series&&d.series.close)||[];
  const plan=d.plan||{};
  const tfN={'1m':21,'3m':63,'6m':126,'1y':252,'2y':504}[TF]||126;
  const cut=closes.slice(-tfN);
  const events=[];
  if(d.earnings_dte!==null&&d.earnings_dte!==undefined&&d.earnings_dte>=0&&d.earnings_dte<=cut.length)
    events.push({index:cut.length-1,label:'E-'+d.earnings_dte+'j'});
  if(cut.length>10){
    VXCharts.candlestickCard('an-chart',{
      title:SYM+' — graphique principal',timeframe:TF,
      question:'Le timing est-il exploitable maintenant ?',
      conclusion:(d.verdict?('Verdict technique moteur : '+d.verdict):'—')
        +(plan.rr?` · R:R structurel ${plan.rr}`:''),
      controlsHtml:['1m','3m','6m','1y','2y'].map(tf=>
        `<button class="vx-chip" data-tf="${tf}" aria-pressed="${tf===TF}">${tf}</button>`).join(''),
      labels:cut.map((_,i)=>i-cut.length),bars:[],closes:cut,plan:plan,events,height:290,
      source:(window.__vxStatus&&window.__vxStatus.demo)?'scan (DÉMO)':'scan',
      timestamp:(t&&t.detail&&t.detail.updated)||Date.now(),mode:demo?'fallback':'delayed',
      limits:'clôtures quotidiennes du scan — niveaux = plan moteur (jamais recalculés côté UI)',
      explain:{shows:'Les clôtures du titre avec les niveaux du plan moteur : entrée, stop (invalidation du sous-jacent), objectifs.',
        why:'Le plan chiffré discipline l’exécution : l’invalidation est définie AVANT d’engager du capital.',
        confirm:'Cassure de la résistance avec volume, breadth de marché favorable.',
        invalidate:`Clôture sous le stop ${VX.fmt.nd(plan.stop)} — la thèse est invalidée, pas « en retard ».`}});
    document.querySelectorAll('[data-tf]').forEach(b=>b.addEventListener('click',()=>{TF=b.dataset.tf;loadDossier();}));
    const chartEl=document.querySelector('#an-chart canvas');
    if(chartEl)chartEl.addEventListener('dblclick',()=>VXCharts.alertFromLevel(SYM,plan.entry||d.price));
  }else{
    $('an-chart').innerHTML='<div class="vx-card">'+VX.states.empty('Série de prix indisponible pour ce titre.')+'</div>';
  }

  /* 4. Fondamental */
  const f=(exec&&exec.fundamental)||{};
  const peers=(t&&t.peers_data)||[];
  const me=peers.find(p=>p.symbol===SYM)||{};
  body('an-fundamental',
    kv('Score fondamental moteur',d.st_fund??f.score)
    +kv('Croissance CA',me.rev_growth!==undefined?VX.fmt.pct(me.rev_growth*100,0):null)
    +kv('Marge',me.margin!==undefined?VX.fmt.pct(me.margin*100,0):null)
    +kv('P/E',me.pe)+kv('ROE',me.roe!==undefined?VX.fmt.pct(me.roe*100,0):null)
    +kv('Médiane sectorielle P/E',t&&t.sector_median&&(t.sector_median.median_pe??t.sector_median))
    +(peers.length>1?`<div class="vx-meta vx-mt2">Pairs : ${peers.filter(p=>p.symbol!==SYM).slice(0,4).map(p=>
      `<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${p.symbol}">${p.symbol}</button>`).join('')}</div>`:''));

  /* 5. Catalyseurs */
  body('an-catalysts',
    kv('Prochains résultats',d.earnings_dte!==null&&d.earnings_dte!==undefined?('dans '+d.earnings_dte+' j'):null,
       d.earnings_dte!==null&&d.earnings_dte<=10?'vx-warn':'')
    +kv('Politique par défaut','sortie avant annonce (hold-through = dossier complet exigé)')
    +`<div class="vx-meta vx-mt2"><a href="/opportunities?view=calendar">Calendrier complet →</a></div>`);

  /* 6. Technique */
  body('an-technical',
    kv('Score',d.score)+kv('Verdict technique (métadonnée)',d.verdict)
    +kv('Force relative',d.rs)+kv('RSI',d.rsi)
    +kv('Position 52 semaines',d.pos52!==undefined?d.pos52+' %':null)
    +kv('Extension vs ATR',d.ext_atr,(d.ext_atr>=2.5?'vx-warn':''))
    +`<div class="vx-meta vx-mt2">La décision finale unique reste ${decision} — les verdicts techniques sont des entrées du moteur exécutif.</div>`);

  /* 7. Sentiment */
  body('an-sentiment',
    kv('Force relative vs univers',d.rs)
    +kv('Régime marché',(exec&&exec.technical&&exec.technical.regime)||null)
    +`<div class="vx-meta vx-mt2">Positionnement institutionnel : proxies uniquement — jamais présentés comme des flux certains.</div>`);

  /* 8. Anomalies */
  try{
    const a=await VX.fetch('/api/anomalies/'+SYM,{ttl:120000});
    body('an-anomalies',(a.anomalies&&a.anomalies.length)?
      a.anomalies.map(x=>`<span class="vx-badge" title="${esc(x.impact||'')}" style="margin:2px">${x.code}</span>`).join('')
      +`<div class="vx-meta vx-mt2">${esc(a.note||'')}</div>`
      :VX.states.empty('Aucune anomalie détectée sur la série disponible.'));
  }catch(e){body('an-anomalies',VX.states.error('Moteur d’anomalies injoignable'));}

  /* TradingView (§30) */
  try{
    const tv=await VX.fetch('/api/tradingview/signals?symbol='+SYM,{ttl:60000});
    const sigs=(tv.signals||[]).slice(-4).reverse();
    body('an-tv',(sigs.length?sigs.map(s=>{
      const age=(Date.now()/1000-(s.received_ts||0));
      const expired=age>4*3600;
      return `<div class="vx-kv"><span class="k">${s.signal}</span>
        <span class="v">${expired?'<span class="vx-badge">expiré</span>':'<span class="vx-badge" style="color:var(--vx-cyan)">à confirmer</span>'}
        <span class="vx-meta">${VX.fmt.ago((s.received_ts||0)*1000)}</span></span></div>`;}).join('')
      +'<div class="vx-meta vx-mt2">Un signal TradingView déclenche une réévaluation — jamais un ACHETER direct. Confirmation par les données broker exigée.</div>'
      :VX.states.empty('Aucun signal TradingView reçu pour ce titre.',
        '<span class="vx-meta">Webhook : /api/tradingview/webhook (voir tradingview/README.md)</span>'))
      +`<div class="vx-flex vx-mt2">
        <a class="vx-btn vx-btn-sm" target="_blank" rel="noopener" href="https://www.tradingview.com/chart/?symbol=${SYM}">Ouvrir dans TradingView ↗</a>
        <button class="vx-btn vx-btn-sm vx-btn-ghost" onclick="VXEntities.openAddModal('${SYM}','alert')">Créer une alerte</button></div>`);
  }catch(e){body('an-tv',VX.states.empty('Intégration TradingView non configurée — aucune donnée inventée.'));}

  /* 9. Scénarios Bull/Base/Bear (plan moteur) */
  const px=d.price;
  if(plan.tp1||plan.stop){
    body('an-scenarios',
      `<div class="vx-grid" style="grid-template-columns:repeat(3,1fr);gap:10px">
        <div class="vx-card" style="border-color:rgba(34,199,122,.3)"><div class="vx-kpi">
          <span class="vx-kpi-label">Bull</span><span class="vx-kpi-value vx-pos" style="font-size:19px">${VX.fmt.nd(plan.tp2||plan.tp1)}</span>
          <span class="vx-meta">${px&&(plan.tp2||plan.tp1)?VX.fmt.pct(((plan.tp2||plan.tp1)/px-1)*100,1):''}</span></div></div>
        <div class="vx-card"><div class="vx-kpi">
          <span class="vx-kpi-label">Base</span><span class="vx-kpi-value" style="font-size:19px">${VX.fmt.nd(plan.tp1)}</span>
          <span class="vx-meta">${px&&plan.tp1?VX.fmt.pct((plan.tp1/px-1)*100,1):''}</span></div></div>
        <div class="vx-card" style="border-color:rgba(239,83,80,.3)"><div class="vx-kpi">
          <span class="vx-kpi-label">Bear</span><span class="vx-kpi-value vx-neg" style="font-size:19px">${VX.fmt.nd(plan.stop)}</span>
          <span class="vx-meta">${px&&plan.stop?VX.fmt.pct((plan.stop/px-1)*100,1):''}</span></div></div>
      </div>
      <div class="vx-meta vx-mt2">Niveaux du plan moteur (structure de marché) — variations arithmétiques vs cours actuel.</div>`);
  }else body('an-scenarios',VX.states.empty('Plan moteur indisponible — pas de scénarios chiffrés.'));

  /* 10. Plan */
  body('an-plan',
    kv('Entrée',plan.entry)+kv('Stop (invalidation sous-jacent)',plan.stop,'vx-neg')
    +kv('TP1',plan.tp1,'vx-pos')+kv('TP2',plan.tp2,'vx-pos')+kv('TP3',plan.tp3,'vx-pos')
    +kv('R:R structurel',plan.rr)
    +`<div class="vx-flex vx-mt3">
      <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${SYM}','follow')">Créer un suivi</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" onclick="VXCharts.alertFromLevel('${SYM}',${JSON.stringify(plan.entry??null)})">Alerte sur l’entrée</button>
    </div>`);

  /* 11. Options */
  try{
    const ob=await VX.fetch('/api/options-for/'+SYM+'?type=CALL',{ttl:180000});
    const cs=(ob&&(ob.contracts||ob.list||ob.best))||ob||{};
    const arr=Array.isArray(cs)?cs:(cs.contracts||[]);
    body('an-options',arr.length?
      `<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Contrat</th><th class="vx-num">Strike</th><th>Échéance</th><th class="vx-num">Delta</th>
        <th class="vx-num">Prime</th><th class="vx-num">OI</th><th></th></tr></thead><tbody>${
        arr.slice(0,3).map(c=>`<tr>
          <td data-label="Contrat"><span class="vx-badge" style="color:var(--vx-violet)">CALL</span></td>
          <td data-label="Strike" class="vx-num">${VX.fmt.nd(c.strike)}</td>
          <td data-label="Échéance" class="vx-mono">${VX.fmt.nd(c.exp||c.expiry)}</td>
          <td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
          <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.mid??c.premium??c.cost)}</td>
          <td data-label="OI" class="vx-num">${VX.fmt.nd(c.oi??c.openInterest)}</td>
          <td><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=options&sym=${SYM}">Analyser →</a></td></tr>`).join('')}
      </tbody></table></div>`
      :VX.states.empty('Aucun contrat CALL exploitable retourné par le moteur.',
        `<a class="vx-btn vx-btn-sm" href="/opportunities?view=options&sym=${SYM}">Ouvrir le desk options</a>`));
  }catch(e){body('an-options',VX.states.empty('Chaîne d’options indisponible (IBKR hors ligne ou titre sans options).'));}

  /* 12. Compatibilité portefeuille */
  const positions=E()?E().positions():[];
  const held=positions.filter(p=>p.sym===SYM);
  const count=positions.length;
  body('an-portfolio-fit',
    kv('Positions déclarées',count+' / 10 max')
    +kv('Ce titre',held.length?('détenu ('+held.map(h=>h.type).join(', ')+')'):'non détenu')
    +kv('Règle',count>=10?'portefeuille plein — remplacement obligatoire':'place disponible',
        count>=10?'vx-warn':'vx-pos')
    +`<div class="vx-meta vx-mt2"><a href="/portfolio?view=risk">Risque complet (positions réelles) →</a></div>`);

  /* 13. Historique */
  const jr=(E()?E().journal():[]).filter(j=>j.ticker===SYM).slice(-5).reverse();
  const follows=(E()?E().follows():[]).filter(r=>r.sym===SYM);
  body('an-history',
    (follows.length?`<div class="vx-insight">Suivi actif depuis ${follows[0].followed}
      — stop ${VX.fmt.nd(follows[0].stop)}, objectif ${VX.fmt.nd(follows[0].tgt)}</div>`:'')
    +(jr.length?jr.map(j=>`<div class="vx-kv"><span class="k">${j.date} · ${esc(j.dir||'')}</span>
      <span class="v ${j.pnl>0?'vx-pos':j.pnl<0?'vx-neg':''}">${j.result||''} ${j.pnl!==undefined&&j.pnl!==''?VX.fmt.num(j.pnl):''}</span></div>`).join('')
      :VX.states.empty('Aucune entrée de journal sur ce titre.'))
    +`<div class="vx-meta vx-mt2"><a href="/performance?view=journal&sym=${SYM}">Journal complet →</a></div>`);
  paintBadges();paintThesis();
}
loadDossier();
VX.refresh.register(loadDossier,180000,'analysis');
})();
</script>
"""

_MOBILE_BAR = """
<div class="vx-mobile-bar"><nav aria-label="Actions rapides">
  <button onclick="VXEntities.toggleFavorite('%%SYM%%')">★<span>Favori</span></button>
  <button onclick="VXEntities.openAddModal('%%SYM%%','follow')">◎<span>Suivre</span></button>
  <button onclick="VXEntities.openAddModal('%%SYM%%','alert')">!<span>Alerte</span></button>
  <button onclick="location.href='/opportunities?view=options&sym=%%SYM%%'">◇<span>Options</span></button>
  <button data-entity-menu="%%SYM%%">⋯<span>Plus</span></button>
</nav></div>
"""


def render(sym: str) -> str:
    sym = sym.upper()[:8]
    safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')
    content = ('<div class="vx-page-header"><div><h1>' + safe + '</h1>'
               '<div class="vx-sub">Cette entreprise et cette opportunité '
               'méritent-elles du capital maintenant ?</div></div></div>'
               + _SECTIONS.replace('%%SYM%%', safe)
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:48px"></div>'))
    js = _JS.replace('%%SYM_JSON%%', json.dumps(safe))
    return render_shell(title=f'{safe} · Analyse', active='analysis',
                        space_label='Analyse', sub_label=safe, content=content,
                        page_js=js, page_label=f'Analyse {safe}',
                        mobile_actions=_MOBILE_BAR.replace('%%SYM%%', safe))
