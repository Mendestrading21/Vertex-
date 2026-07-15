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
    dims = ''.join(
        f'<div class="an-dim"><span class="an-dim-n">{n}</span>'
        f'<span class="an-dim-l">{lab}</span></div>'
        for n, lab in [
            ('1', 'Fondamental — qualité, croissance, valorisation'),
            ('2', 'Catalyseurs — résultats, événements datés'),
            ('3', 'Timing technique — tendance, niveaux, R:R'),
            ('4', 'Sentiment & positionnement'),
            ('·', 'Anomalies & signaux TradingView'),
            ('·', 'Scénarios Bull / Base / Bear'),
            ('·', 'Options associées — convexité, IV, DTE'),
            ('★', 'Décision finale & plan de niveaux'),
        ])
    content = """
<div class="vx-page-header"><div><h1>Analyse</h1>
<div class="vx-sub">Rechercher un titre pour ouvrir sa fiche canonique.</div></div></div>
<style id="an-index-css">
.an-dim{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--vx-border-soft)}
.an-dim:last-child{border-bottom:none}
.an-dim-n{flex:0 0 26px;height:26px;display:grid;place-items:center;border-radius:8px;
 background:var(--vx-brand-soft);color:var(--vx-copper-light);font:700 12px/1 var(--vx-font-mono,monospace);
 border:1px solid rgba(185,104,61,.28)}
.an-dim-l{font-size:13px;color:var(--vx-text-secondary)}
.an-shortcut{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;
 border-bottom:1px dashed var(--vx-border-soft);font-size:13px;color:var(--vx-text-secondary)}
.an-shortcut:last-child{border-bottom:none}
.an-kbd{font:600 11px/1 var(--vx-font-mono,monospace);color:var(--vx-text-primary);
 background:var(--vx-graphite-800);border:1px solid var(--vx-border-default);border-radius:6px;padding:4px 7px}
</style>
<div class="vx-grid">
  <div class="vx-col-7">
    <div class="vx-card">
      <div class="vx-field"><label for="an-search">Ticker ou entreprise</label>
      <input class="vx-input" id="an-search" placeholder="ex. NVDA, Microsoft…" autocomplete="off"
        style="font-size:16px;padding:12px" /></div>
      <div id="an-results" class="vx-flex-col"></div>
      <div class="vx-help vx-mt2">Astuce : ⌘K / Ctrl+K depuis n’importe quelle page.</div>
    </div>
    <section class="vx-card vx-mt4" aria-label="Titres récents">
      <div class="vx-card-header"><span class="vx-card-title">Titres récents</span></div>
      <div class="vx-card-body vx-flex vx-wrap" id="an-recent"><span class="vx-skeleton" style="width:120px;height:26px"></span></div>
    </section>
    <section class="vx-card vx-mt4" aria-label="Favoris">
      <div class="vx-card-header"><span class="vx-card-title">Favoris</span>
        <span class="vx-dim" style="font-size:12px">titres marqués ★</span></div>
      <div class="vx-card-body vx-flex vx-wrap" id="an-favs"></div>
    </section>
  </div>
  <aside class="vx-col-5">
    <section class="vx-card vx-accent" aria-label="Contenu d'une fiche">
      <div class="vx-card-header"><span class="vx-card-title">Ce que révèle une fiche</span></div>
      <div class="vx-card-body">""" + dims + """</div>
    </section>
    <section class="vx-card vx-mt4" aria-label="Raccourcis">
      <div class="vx-card-header"><span class="vx-card-title">Raccourcis</span></div>
      <div class="vx-card-body">
        <div class="an-shortcut"><span>Recherche globale</span><span class="an-kbd">⌘K</span></div>
        <div class="an-shortcut"><span>Scanner d’opportunités</span><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities">Ouvrir →</a></div>
        <div class="an-shortcut"><span>Portefeuille & positions</span><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">Ouvrir →</a></div>
      </div>
    </section>
  </aside>
</div>
"""
    js = r"""
<script>
(function(){
const $=(id)=>document.getElementById(id);
$('an-recent').innerHTML=VX.recentTickers.get().map(s=>
  `<button class="vx-btn vx-ticker" data-open-analysis="${s}">${s}</button>`).join('')
  ||'<span class="vx-muted">Aucun titre consulté récemment.</span>';
let favs=[];try{favs=JSON.parse(localStorage.getItem('myFavs')||'[]');}catch(e){favs=[];}
$('an-favs').innerHTML=(Array.isArray(favs)&&favs.length?favs:[]).map(s=>
  `<button class="vx-btn vx-ticker" data-open-analysis="${s}">${s}</button>`).join('')
  ||'<span class="vx-muted">Aucun favori — marque un titre avec ★ depuis sa fiche.</span>';
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
      <button class="vx-btn vx-btn-sm vx-btn-soft" id="an-follow"
        onclick="VXEntities.followStock('%%SYM%%',{decision:(document.getElementById('an-decision')||{}).dataset&&document.getElementById('an-decision').dataset.decision});location.href='/tracking';"
        title="Suivre : mesure la performance hypothétique depuis maintenant">Suivre →</button>
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

<!-- Workspace (§22) : colonne principale + rail sticky décisionnel -->
<div class="vx-grid vx-mt4" id="an-workspace">
<div class="vx-col-8">

<!-- 3. Graphique principal -->
<div id="an-chart"></div>

<!-- 3-bis. Valorisation vs secteur (radar) + Financials — fondamentaux réels -->
<div class="vx-grid vx-mt4">
  <div class="vx-col-5" id="an-valuation"></div>
  <section class="vx-card vx-col-7 vx-card--premium" id="an-financials">
    <div class="vx-card-header"><span class="vx-card-title">Financials — fondamentaux</span>
      <span class="vx-actions"><span class="vx-badge" id="an-fin-src">—</span></span></div>
    <div data-body>%%LOADING%%</div>
  </section>
</div>

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

<!-- 9. Scénarios -->
<section class="vx-card vx-mt4" id="an-scenarios"><div class="vx-card-header">
  <span class="vx-card-title">Scénarios Bull / Base / Bear</span></div><div data-body>%%LOADING%%</div></section>

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

</div>
<aside class="vx-col-4" id="an-rail">
<div style="position:sticky;top:calc(var(--vx-topbar-h) + 88px);display:flex;flex-direction:column;gap:var(--vx-s3)">
  <section class="vx-card vx-card--hero" id="an-rail-decision"><div class="vx-card-header">
    <span class="vx-card-title">Décision finale</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card" id="an-plan"><div class="vx-card-header">
    <span class="vx-card-title">Plan & niveaux clés</span></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-card--compact" id="an-rail-risks"><div class="vx-card-header">
    <span class="vx-card-title">Risques identifiés</span></div><div data-body>—</div></section>
</div>
</aside>
</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/price-chart.js" defer></script>
<script src="/static/vertex/js/charts/candlestick-chart.js" defer></script>
<script src="/static/vertex/js/vendor/lightweight-charts.standalone.production.js" defer></script>
<script src="/static/vertex/js/charts/candlestick-lwc.js" defer></script>
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

/* Cellule de métrique premium color-codée. m:{k,val,unit,cmp,tone,bar} — tone∈
   pos/neg/warn/opt/'' ; bar∈[0..100] (position vs médiane, repère à 50). Une
   valeur nulle rend « — » (aucun chiffre inventé). */
function metric(m){
  const v=(m.val===null||m.val===undefined||m.val==='')?'—':m.val;
  const tone=v==='—'?'':(m.tone||'');
  const bar=(m.bar!=null&&v!=='—')?
    `<div class="vx-metric-bar"><i style="width:${Math.max(3,Math.min(100,m.bar))}%"></i><b style="left:50%"></b></div>`:'';
  const cmp=(m.cmp&&v!=='—')?`<div class="vx-metric-cmp">${m.cmp}</div>`:'';
  return `<div class="vx-metric" data-tone="${tone}">`
    +`<span class="vx-metric-k" title="${esc(m.k)}">${esc(m.k)}</span>`
    +`<span class="vx-metric-v">${v}${m.unit?`<span class="vx-metric-u">${m.unit}</span>`:''}</span>`
    +cmp+bar+`</div>`;
}
function metricGrid(cells){return `<div class="vx-metricgrid">${cells.join('')}</div>`;}
/* score radial 0..100 (50=médiane) pour la mini-barre, aligné sur le radar. */
function vsMed(value,median,better){
  if(value==null||median==null||!median)return null;
  const r=better==='low'?(median/value):(value/median);
  return Math.max(6,Math.min(100,r*50));
}

/* Barre de fourchette des objectifs analystes (bas · médian · haut · prix courant).
   Données réelles company.analysts — jamais inventées ; le prix courant n'est
   superposé que s'il existe (souvent absent hors flux live). */
function analystRangeBar(an,price){
  const lo=an.target_low,hi=an.target_high,mid=an.target_median??an.target_mean;
  if(lo==null||hi==null||hi<=lo)return '';
  const pts=[lo,hi];if(mid!=null)pts.push(mid);if(price!=null)pts.push(price);
  const dmin=Math.min.apply(null,pts),dmax=Math.max.apply(null,pts),span=(dmax-dmin)||1;
  const pad=span*0.06,a=dmin-pad,b=dmax+pad,rng=(b-a)||1;
  const pos=(x)=>((x-a)/rng*100).toFixed(1);
  const fillL=pos(lo),fillR=pos(hi);
  const P=(v)=>'$'+VX.fmt.price(v);
  let ticks=`<i class="rb-tick" style="left:${pos(lo)}%"></i><i class="rb-tick" style="left:${pos(hi)}%"></i>`
    +`<span class="rb-lab" style="left:${pos(lo)}%">${P(lo)}<span class="rb-lab-sub">bas</span></span>`
    +`<span class="rb-lab" style="left:${pos(hi)}%">${P(hi)}<span class="rb-lab-sub">haut</span></span>`;
  if(mid!=null)ticks+=`<i class="rb-tick" data-kind="mean" style="left:${pos(mid)}%"></i>`
    +`<span class="rb-lab" data-kind="mean" style="left:${pos(mid)}%">${P(mid)}<span class="rb-lab-sub">objectif</span></span>`;
  if(price!=null)ticks+=`<i class="rb-tick" data-kind="price" style="left:${pos(price)}%"></i>`
    +`<span class="rb-lab" data-kind="price" style="left:${pos(price)}%">${P(price)}<span class="rb-lab-sub">cours</span></span>`;
  return `<div class="vx-rangebar" role="img" aria-label="Fourchette d'objectifs ${P(lo)} à ${P(hi)}">`
    +`<span class="rb-fill" style="left:${fillL}%;right:${(100-fillR)}%"></span>${ticks}</div>`;
}

/* Barres comparatives titre vs pairs sur une métrique (P/E par défaut).
   rows réels (company.fundamentals + peers_data) ; médiane sectorielle en repère. */
function peersCompareBars(cf,peers,sm,opt){
  opt=opt||{};const key=opt.key||'pe';const med=opt.median;
  const self={sym:SYM,val:cf[key],self:1};
  const others=(peers||[]).filter(p=>p&&p.symbol!==SYM&&p[key]!=null&&isFinite(p[key]))
    .map(p=>({sym:p.symbol,val:+p[key]}));
  const all=[self].concat(others).filter(r=>r.val!=null&&isFinite(r.val));
  if(all.length<2)return '';
  const mx=Math.max.apply(null,all.map(r=>Math.abs(r.val)),med?[Math.abs(med)]:[])||1;
  const fmtV=opt.fmt||(v=>(+v).toFixed(1));
  const bars=all.sort((x,y)=>y.val-x.val).map(r=>
    `<div class="vx-cmpbar" data-self="${r.self?1:0}">
       <span class="cb-name">${esc(r.sym)}</span>
       <span class="cb-track"><i style="width:${Math.max(4,Math.min(100,Math.abs(r.val)/mx*100)).toFixed(0)}%"></i></span>
       <span class="cb-val">${fmtV(r.val)}</span></div>`).join('');
  return `<div class="vx-cmpbars">${bars}</div>`
    +(med!=null?`<div class="vx-meta vx-mt1">Médiane secteur : <b class="vx-mono">${fmtV(med)}</b></div>`:'');
}

/* Valorisation vs secteur (radar) + Financials premium — données company réelles
   (cache serveur), jamais inventées. Le prix live peut manquer ; les
   fondamentaux/médianes sectorielles sont servis même sans flux temps réel. */
function paintValuation(t,cf){
  cf=cf||{};
  const sm=(t&&t.sector_median)||{};
  const demo=!!(window.__vxStatus&&window.__vxStatus.demo);
  /* pourcentages : cf.* en fraction (0.27) · sm.median_* déjà en % (18.03) */
  const revG=cf.rev_growth!=null?cf.rev_growth*100:null;
  const marg=cf.margin!=null?cf.margin*100:null;
  const roe=cf.roe!=null?cf.roe*100:null;
  /* ── Radar (via kit premium) ── */
  if(window.VXCharts&&VXCharts.valuationRadar){
    VXCharts.valuationRadar('an-valuation',{
      title:'Valorisation vs secteur',sym:SYM,sectorLabel:'Médiane secteur',
      question:'Le titre se paie-t-il cher ou bon marché face à ses pairs ?',
      axes:[
        {label:'Valorisation',value:cf.pe,median:sm.median_pe,better:'low',fmt:v=>'×'+(+v).toFixed(1)},
        {label:'Valo. fwd',value:cf.forward_pe,median:sm.median_fwd_pe,better:'low',fmt:v=>'×'+(+v).toFixed(1)},
        {label:'Croissance',value:revG,median:sm.median_growth,better:'high',fmt:v=>(+v).toFixed(1)+'%'},
        {label:'Marge',value:marg,median:sm.median_margin,better:'high',fmt:v=>(+v).toFixed(1)+'%'},
        {label:'Rentab.',value:roe,median:sm.median_roe,better:'high',fmt:v=>(+v).toFixed(0)+'%'},
      ],
      source:demo?'company (DÉMO)':'company (cache)',timestamp:Date.now(),mode:demo?'fallback':'delayed',
    });
  }
  /* ── Grille Financials premium ── */
  const B=(x)=>{if(x==null||!isFinite(x))return '—';const a=Math.abs(x),s=x<0?'-':'';
    if(a>=1e12)return s+(a/1e12).toFixed(2)+' T$';if(a>=1e9)return s+(a/1e9).toFixed(1)+' Md$';
    if(a>=1e6)return s+(a/1e6).toFixed(0)+' M$';return s+a.toFixed(0)+' $';};
  const cells=[
    metric({k:'P/E',val:cf.pe!=null?'×'+(+cf.pe).toFixed(1):null,
      tone:cf.pe!=null&&sm.median_pe?(cf.pe<sm.median_pe?'pos':'neg'):'',
      cmp:sm.median_pe?`méd ×${(+sm.median_pe).toFixed(1)}`:'',bar:vsMed(cf.pe,sm.median_pe,'low')}),
    metric({k:'P/E anticipé',val:cf.forward_pe!=null?'×'+(+cf.forward_pe).toFixed(1):null,
      tone:cf.forward_pe!=null&&sm.median_fwd_pe?(cf.forward_pe<sm.median_fwd_pe?'pos':'neg'):'',
      cmp:sm.median_fwd_pe?`méd ×${(+sm.median_fwd_pe).toFixed(1)}`:'',bar:vsMed(cf.forward_pe,sm.median_fwd_pe,'low')}),
    metric({k:'PEG',val:cf.peg!=null?(+cf.peg).toFixed(2):null,
      tone:cf.peg!=null?(cf.peg<1?'pos':cf.peg>2?'warn':''):''}),
    metric({k:'Croissance CA',val:revG!=null?(revG>=0?'+':'')+revG.toFixed(1):null,unit:'%',
      tone:revG!=null&&sm.median_growth?(revG>sm.median_growth?'pos':'neg'):'',
      cmp:sm.median_growth?`méd ${(+sm.median_growth).toFixed(1)}%`:'',bar:vsMed(revG,sm.median_growth,'high')}),
    metric({k:'Croissance BPA',val:cf.eps_growth!=null?((cf.eps_growth*100>=0?'+':'')+(cf.eps_growth*100).toFixed(1)):null,unit:'%',
      tone:cf.eps_growth!=null?(cf.eps_growth>0?'pos':'neg'):''}),
    metric({k:'Marge nette',val:marg!=null?marg.toFixed(1):null,unit:'%',
      tone:marg!=null&&sm.median_margin?(marg>sm.median_margin?'pos':'neg'):'',
      cmp:sm.median_margin?`méd ${(+sm.median_margin).toFixed(1)}%`:'',bar:vsMed(marg,sm.median_margin,'high')}),
    metric({k:'ROE',val:roe!=null?roe.toFixed(0):null,unit:'%',
      tone:roe!=null&&sm.median_roe?(roe>sm.median_roe?'pos':'neg'):'',
      cmp:sm.median_roe?`méd ${(+sm.median_roe).toFixed(0)}%`:'',bar:vsMed(roe,sm.median_roe,'high')}),
    metric({k:'Free cash flow',val:B(cf.fcf),tone:cf.fcf>0?'pos':cf.fcf<0?'neg':''}),
    metric({k:'Capitalisation',val:B(cf.mcap)}),
    metric({k:'Trésorerie',val:B(cf.cash),tone:'pos'}),
    metric({k:'Dette',val:B(cf.debt),tone:cf.debt>cf.cash?'warn':''}),
    metric({k:'Dividende',val:cf.dividend!=null?(+cf.dividend).toFixed(2):null,unit:cf.dividend?'$':''}),
  ];
  /* Comparaison P/E vs pairs (réel : company.fundamentals + peers_data) */
  const peers=(t&&t.peers_data)||[];
  const cmp=peersCompareBars(cf,peers,sm,{key:'pe',median:sm.median_pe,fmt:v=>'×'+(+v).toFixed(1)});
  const cmpBlock=cmp?`<div class="vx-mt3"><div class="vx-metric-k" style="margin-bottom:6px">P/E — ${SYM} vs pairs</div>${cmp}</div>`:'';
  body('an-financials',metricGrid(cells)+cmpBlock);
  const srcEl=$('an-fin-src');if(srcEl)srcEl.textContent=demo?'DÉMO':'cache';
}

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
  /* Rail décisionnel sticky */
  const railD=$('an-rail-decision')&&$('an-rail-decision').querySelector('[data-body]');
  if(railD){
    const audit=(exec&&exec.audit_trail)||[];
    railD.innerHTML=`<div class="vx-kpi vx-mb2">
        <span class="vx-kpi-value" style="font-size:24px"><span class="vx-badge vx-badge-decision" data-decision="${decision.replace('É','E')}" style="font-size:14px;padding:5px 14px">${decision}</span></span>
        <span class="vx-kpi-delta vx-muted">${exec&&exec.reason?esc(exec.reason):'moteur exécutif unique'}</span></div>`
      +(audit.length?`<details class="vx-mt1"><summary class="vx-meta" style="cursor:pointer">Audit trail (${audit.length})</summary>
        <ul style="margin:6px 0 0;padding-left:16px;font-size:11.5px" class="vx-dim">${audit.slice(0,8).map(a=>`<li>${esc(typeof a==='string'?a:JSON.stringify(a))}</li>`).join('')}</ul></details>`:'')
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'ExecutiveEngine',demo?'fallback':'delayed')}</div>`;
  }
  const railR=$('an-rail-risks')&&$('an-rail-risks').querySelector('[data-body]');
  if(railR){
    const blocking=(exec&&exec.blocking_anomalies)||(exec&&exec.blocking)||[];
    const warns=(exec&&exec.warnings)||[];
    const all=[...blocking.map(b=>({t:'bloquant',v:b})),...warns.map(w=>({t:'attention',v:w}))];
    let html=all.length?all.slice(0,6).map(r=>
      `<div class="vx-insight" data-tone="risk" style="font-size:12px"><b>${r.t}</b> — ${esc(typeof r.v==='string'?r.v:JSON.stringify(r.v))}</div>`).join('')
      :'<span class="vx-meta">Aucun risque bloquant remonté par les moteurs.</span>';
    /* Carte des risques d'entreprise (§24) — fondamentaux réels. */
    const rm=t&&t.risk_map;
    if(rm&&rm.risks){
      const col={'ÉLEVÉ':'var(--vx-negative,#dc6254)','MODÉRÉ':'var(--vx-warning,#cc892c)',
        'FAIBLE':'var(--vx-positive,#39b879)','INCONNU':'var(--vx-text-dim,#817d77)'};
      html+='<div class="vx-mt3" style="font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--vx-text-dim,#817d77)">Carte des risques ('
        +esc(rm.known_count)+'/'+esc(rm.total_count)+' mesurés)</div>'
        +rm.risks.map(r=>`<div style="display:flex;justify-content:space-between;gap:.5rem;padding:.3rem 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:12px">`
          +`<span>${esc(r.category)}</span><span style="color:${col[r.level]||'#888'};font-weight:600">${esc(r.level)}</span></div>`
          +`<div class="vx-meta" style="font-size:11px;margin-bottom:.2rem">${esc(r.note||'')}</div>`).join('');
    }
    railR.innerHTML=html;
  }
  const sc=(exec&&exec.scores)||{};
  const scAxes=[['Conviction',sc.conviction],['Risque',sc.risk],['Timing',sc.timing],
    ['Asymétrie',sc.asymmetry],['Qualité',sc.data_quality]];
  $('an-scores').innerHTML=scAxes.map(([k,v])=>
    `<span class="vx-badge" title="${k}">${k} <b class="vx-mono">${VX.fmt.nd(v)}</b></span>`).join('')
    +(demo?'<span class="vx-badge" style="color:var(--vx-warning)">DÉMO</span>':'')
    +'<div id="an-scorecard-radar" style="flex:1 0 100%;max-width:240px;margin:8px auto 0"></div>';
  if(window.VXCharts&&VXCharts.radar&&scAxes.some(a=>a[1]!==null&&a[1]!==undefined)){
    VXCharts.radar('an-scorecard-radar',{axes:scAxes.map(a=>({label:a[0],value:a[1]||0})),
      max:100,ariaLabel:'Scorecard '+SYM,color:VXCharts.colors.brand,width:240,height:190});
  }

  /* 3. Graphique principal — Trading Workspace (chandeliers réels + overlays MM) */
  const S=d.series||{};
  const closes=S.close||[];
  const plan=d.plan||{};
  const tfN={'1m':21,'3m':63,'6m':126,'1y':252,'2y':504}[TF]||126;
  const cut=closes.slice(-tfN);
  const tail=(arr)=>Array.isArray(arr)?arr.slice(-tfN):null;
  /* Bougies RÉELLES seulement si OHLC complet fourni par le moteur (jamais inventé). */
  const O=tail(S.open),H=tail(S.high),L=tail(S.low);
  const bars=(O&&H&&L&&O.length===cut.length)?cut.map((c,i)=>({o:O[i],h:H[i],l:L[i],c:c})):[];
  const VC=window.VXCharts||{cols:{}};
  const cc=(n,f)=>(VC.colors&&VC.colors[n])||f;
  /* Overlays = moyennes mobiles RÉELLES calculées côté serveur (ema20/sma50/sma200). */
  const overlays=[
    {label:'MM20',color:cc('amber','#ce8a29'),data:tail(S.ema20),dash:[]},
    {label:'MM50',color:cc('beige','#c8ad8d'),data:tail(S.sma50),dash:[5,3]},
    {label:'MM200',color:cc('neutral','#8f8a83'),data:tail(S.sma200),dash:[2,3]},
  ].filter(o=>o.data&&o.data.some(x=>x!=null));
  const events=[];
  if(d.earnings_dte!==null&&d.earnings_dte!==undefined&&d.earnings_dte>=0&&d.earnings_dte<=cut.length)
    events.push({index:cut.length-1,label:'E-'+d.earnings_dte+'j'});
  if(cut.length>10){
    /* Chandeliers PRO (TradingView LWC) si OHLC daté dispo ; repli auto sur le
       candlestick Chart.js sinon. Même contrat de carte (contrôles TF, explain…). */
    const drawChart=(window.VXCharts&&VXCharts.lwCandlestickCard)||VXCharts.candlestickCard;
    drawChart('an-chart',{
      title:SYM+' — graphique principal',timeframe:TF,
      question:'Le timing est-il exploitable maintenant ?',
      conclusion:(d.verdict?('Verdict technique moteur : '+d.verdict):'—')
        +(plan.rr?` · R:R structurel ${plan.rr}`:''),
      controlsHtml:['1m','3m','6m','1y','2y'].map(tf=>
        `<button class="vx-chip" data-tf="${tf}" aria-pressed="${tf===TF}">${tf}</button>`).join(''),
      labels:cut.map((_,i)=>i-cut.length),bars:bars,closes:cut,overlays:overlays,plan:plan,events,
      dates:tail(S.dates),volume:tail(S.volume),
      height:Math.round(Math.min(460,Math.max(340,(window.innerWidth||1200)*0.30))),
      source:(window.__vxStatus&&window.__vxStatus.demo)?'scan (DÉMO)':'scan',
      timestamp:(t&&t.detail&&t.detail.updated)||Date.now(),mode:demo?'fallback':'delayed',
      limits:(bars.length?'bougies OHLC quotidiennes':'clôtures quotidiennes')+' du scan · MM = moyennes serveur · niveaux = plan moteur',
      explain:{shows:'Chandeliers (ou clôtures) du titre, moyennes mobiles 20/50/200 et niveaux du plan moteur : entrée, stop (invalidation), objectifs.',
        why:'Le plan chiffré discipline l’exécution : l’invalidation est définie AVANT d’engager du capital ; les MM situent la tendance.',
        confirm:'Cours au-dessus des MM, cassure de la résistance avec volume, breadth favorable.',
        invalidate:`Clôture sous le stop ${VX.fmt.nd(plan.stop)} — la thèse est invalidée, pas « en retard ».`}});
    document.querySelectorAll('[data-tf]').forEach(b=>b.addEventListener('click',()=>{TF=b.dataset.tf;loadDossier();}));
    const chartEl=document.querySelector('#an-chart .vx-lwc')||document.querySelector('#an-chart canvas');
    if(chartEl)chartEl.addEventListener('dblclick',()=>VXCharts.alertFromLevel(SYM,plan.entry||d.price));
  }else{
    $('an-chart').innerHTML='<div class="vx-card">'+VX.states.empty('Série de prix indisponible pour ce titre.')+'</div>';
  }

  /* 4. Fondamental */
  const f=(exec&&exec.fundamental)||{};
  const peers=(t&&t.peers_data)||[];
  /* Le titre analysé n'est JAMAIS dans sa propre liste de pairs → on part de ses
     fondamentaux propres (company.fundamentals) puis on superpose l'entrée pairs
     si elle existe. Sans ce socle, P/E / marge / croissance / ROE restaient vides. */
  const cf=(t&&t.company&&t.company.fundamentals)||{};
  const me=Object.assign({pe:cf.pe,margin:cf.margin,rev_growth:cf.rev_growth,roe:cf.roe},
                         peers.find(p=>p.symbol===SYM)||{});
  body('an-fundamental',
    kv('Score fondamental moteur',d.st_fund??f.score)
    +kv('Croissance CA',me.rev_growth!==undefined?VX.fmt.pct(me.rev_growth*100,0):null)
    +kv('Marge',me.margin!==undefined?VX.fmt.pct(me.margin*100,0):null)
    +kv('P/E',me.pe!=null?(+me.pe).toFixed(1):null)+kv('ROE',me.roe!==undefined&&me.roe!==null?VX.fmt.pct(me.roe*100,0):null)
    +kv('Médiane sectorielle P/E',t&&t.sector_median&&(t.sector_median.median_pe??t.sector_median))
    +(peers.length>1?`<div class="vx-meta vx-mt2">Pairs : ${peers.filter(p=>p.symbol!==SYM).slice(0,4).map(p=>
      `<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${p.symbol}">${p.symbol}</button>`).join('')}</div>`:''));

  /* 4-bis. Valorisation vs secteur (radar) + Financials premium — vraie donnée cachée */
  paintValuation(t,cf);

  /* 5. Catalyseurs */
  body('an-catalysts',
    kv('Prochains résultats',d.earnings_dte!==null&&d.earnings_dte!==undefined?('dans '+d.earnings_dte+' j'):null,
       d.earnings_dte!==null&&d.earnings_dte<=10?'vx-warn':'')
    +kv('Politique par défaut','sortie avant annonce (hold-through = dossier complet exigé)')
    +`<div class="vx-meta vx-mt2"><a href="/opportunities?view=calendar">Calendrier complet →</a></div>`);

  /* 6. Technique */
  const ttm=(d.ttm_fired?'🚀 sortie de compression':(d.ttm_squeeze?'🔒 en compression (BB dans Keltner)':null));
  const ttmDir=d.ttm_dir==='up'?' · momentum haussier':d.ttm_dir==='down'?' · momentum baissier':'';
  function perfBars(d){
    const rows=[['1 sem.',d.perf_w],['1 mois',d.perf_m],['1 trim.',d.perf_q],['1 an',d.perf_y]].filter(r=>r[1]!=null&&!isNaN(r[1]));
    if(!rows.length)return '';
    const maxAbs=Math.max(5,...rows.map(r=>Math.abs(r[1])));
    return '<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#26221e);padding-top:8px">'
      +'<div class="vx-meta vx-mb1" style="text-transform:uppercase;letter-spacing:.04em">Performance multi-horizons</div>'
      +rows.map(function(r){const v=r[1];const neg=v<0;const w=Math.min(50,Math.abs(v)/maxAbs*50);
        return '<div style="display:flex;align-items:center;gap:6px;margin:2px 0" role="img" aria-label="'+r[0]+' '+(v>=0?'+':'')+v+' %">'
          +'<span style="width:52px;font-size:10.5px;color:var(--vx-text-muted,#817d77)">'+r[0]+'</span>'
          +'<span style="flex:1;height:10px;position:relative;background:var(--vx-surface-3,#17191c);border-radius:3px;overflow:hidden">'
            +'<span style="position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(255,255,255,.16)"></span>'
            +'<span style="position:absolute;top:0;bottom:0;'+(neg?('right:50%;width:'+w.toFixed(1)+'%'):('left:50%;width:'+w.toFixed(1)+'%'))+';background:'+(neg?'var(--vx-negative,#dc6255)':'var(--vx-positive,#39b878)')+'"></span></span>'
          +'<span style="width:54px;text-align:right;font-size:10.5px;font-variant-numeric:tabular-nums" class="'+(neg?'vx-neg':'vx-pos')+'">'+(v>=0?'+':'')+VX.fmt.num(v,1)+'%</span></div>';
      }).join('')+'</div>';
  }
  body('an-technical',
    kv('Score',d.score)+kv('Verdict technique (métadonnée)',d.verdict)
    +kv('Force relative',d.rs)+kv('RSI',d.rsi)
    +kv('Position 52 semaines',d.pos52!==undefined?d.pos52+' %':null)
    +kv('Extension vs ATR',d.ext_atr,(d.ext_atr>=2.5?'vx-warn':''))
    +(ttm?kv('TTM Squeeze',ttm+ttmDir,(d.ttm_fired&&d.ttm_dir==='up'?'vx-pos':d.ttm_fired&&d.ttm_dir==='down'?'vx-neg':'')):'')
    +perfBars(d)
    +`<div class="vx-meta vx-mt2">La décision finale unique reste ${decision} — les verdicts techniques sont des entrées du moteur exécutif.</div>`);

  /* 7. Sentiment + consensus analystes (données company déjà chargées → objectif de cours + potentiel) */
  const an=(t&&t.company&&t.company.analysts)||{};
  const _px=d.price, _tgt=an.target_mean;
  const _up=(_tgt&&_px)?((_tgt/_px-1)*100):null;
  const _rl={strong_buy:'Achat fort',buy:'Achat',outperform:'Surperformance',hold:'Conserver',underperform:'Sous-performance',sell:'Vente'}[an.rating]||an.rating;
  const consensus=(an.rating||_tgt)?(
    `<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#26221e);padding-top:8px">`
    +(an.rating?`<div class="vx-kv"><span class="k">Consensus analystes</span><span class="v">${esc(_rl||'—')}${an.rating_mean!=null?` (${(+an.rating_mean).toFixed(1)}/5)`:''}${an.n_analysts?` · ${an.n_analysts} analystes`:''}</span></div>`:'')
    +(_tgt?`<div class="vx-kv"><span class="k">Objectif moyen</span><span class="v">${VX.fmt.price(_tgt)}${_up!=null?` <span class="${_up>=0?'vx-pos':'vx-neg'}">(${_up>=0?'+':''}${_up.toFixed(1)}%)</span>`:''}</span></div>`:'')
    +analystRangeBar(an,_px)
    +`</div>`):'';
  body('an-sentiment',
    kv('Force relative vs univers',d.rs)
    +kv('Régime marché',(exec&&exec.technical&&exec.technical.regime)||null)
    +consensus
    +`<div class="vx-meta vx-mt2">Positionnement institutionnel : proxies uniquement — jamais présentés comme des flux certains. Consensus analystes = données publiques (peut dater).</div>`);

  /* 8. Anomalies */
  try{
    const a=await VX.fetch('/api/anomalies/'+SYM,{ttl:120000});
    body('an-anomalies',(a.anomalies&&a.anomalies.length)?
      a.anomalies.map(x=>`<span class="vx-badge" title="${esc(x.impact||'')}" style="margin:2px">${x.code}</span>`).join('')
      +`<div class="vx-meta vx-mt2">${esc(a.note||'')}</div>`
      :VX.states.empty('Aucune anomalie détectée sur la série disponible.'));
  }catch(e){body('an-anomalies',VX.states.error('Moteur d’anomalies injoignable'));}

  /* TradingView (§30) + confluence vs verdict moteur (miroir de tv_confluence.py) */
  try{
    const TV_BULL=['SUPPORT_RECLAIM','BREAKOUT_CONFIRMED','BREAKOUT_RETEST','MOMENTUM_ACCELERATION','VOLUME_EXPANSION','TREND_ALIGNMENT'];
    const TV_BEAR=['FAILED_BREAKOUT','THESIS_INVALIDATION'];
    const vDn=/AVOID|ÉVITER|EVITER|ALL[ÉE]GER|SORTIR|R[ÉE]DUIRE|NO_NEW_RISK|VENDRE|REFUS|REJET/i.test(d.verdict||'');
    const vUp=/ACHETER|BUY|RENFORCER|ACCUMULER/i.test(d.verdict||'');
    /* baissier d'abord (miroir de tv_confluence.verdict_stance) — jamais un faux CONFIRME */
    const vStance=vDn?'BEARISH':(vUp?'BULLISH':'NEUTRAL');
    function confl(sig){
      const sd=TV_BULL.indexOf(sig)>=0?'BULLISH':(TV_BEAR.indexOf(sig)>=0?'BEARISH':'NEUTRAL');
      if(sd==='NEUTRAL'||vStance==='NEUTRAL')return ['NEUTRE','vx-dim','·'];
      if(sd===vStance)return ['CONFIRME','vx-pos','✓'];
      return ['CONTREDIT','vx-neg','✗'];
    }
    const tv=await VX.fetch('/api/tradingview/signals?symbol='+SYM,{ttl:60000});
    const sigs=(tv.signals||[]).slice(-4).reverse();
    let confirms=0,contradicts=0;
    sigs.forEach(s=>{const c=confl(s.signal);if(c[0]==='CONFIRME')confirms++;else if(c[0]==='CONTREDIT')contradicts++;});
    const overall=contradicts&&!confirms?['CONTREDIT le verdict','vx-neg']
      :confirms&&!contradicts?['CONFIRME le verdict','vx-pos']
      :(confirms||contradicts)?['signaux MIXTES','vx-dim']:['—','vx-dim'];
    body('an-tv',(sigs.length?
      (d.verdict?`<div class="vx-kv"><span class="k">Confluence</span><span class="v ${overall[1]}"><b>${overall[0]}</b> <span class="vx-meta">(vs ${esc(d.verdict)})</span></span></div>`:'')
      +sigs.map(s=>{
      const fresh=(s.fresh!==undefined)?s.fresh:((Date.now()/1000-(s.received_ts||0))<=6*3600);
      const c=confl(s.signal);
      return `<div class="vx-kv"><span class="k">${s.signal}</span>
        <span class="v"><span class="vx-badge ${c[1]}" title="confluence">${c[2]} ${c[0]}</span>
        ${fresh?'':'<span class="vx-badge">rassis</span>'}
        <span class="vx-meta">${VX.fmt.ago((s.received_ts||0)*1000)}</span></span></div>`;}).join('')
      +'<div class="vx-meta vx-mt2">Un signal TradingView déclenche une réévaluation — jamais un ACHETER direct. La confluence est une lecture de cohérence, pas une décision.</div>'
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

  /* 10. Plan — échelle Risk/Reward (§24.5) : niveaux du plan proportionnels au prix */
  function rrLadder(px,plan){
    const VC=window.VXCharts||{colors:{}};const col=(n,f)=>(VC.colors&&VC.colors[n])||f;
    const lv=[];
    if(plan.stop!=null)lv.push({k:'Stop',v:plan.stop,c:col('negative','#dc5f52')});
    const e=(plan.entry!=null?plan.entry:px);
    if(e!=null)lv.push({k:'Entrée',v:e,c:col('info','#b9683d')});
    [plan.tp1,plan.tp2,plan.tp3].forEach(function(t,i){if(t!=null)lv.push({k:'TP'+(i+1),v:t,c:col('positive','#38b879')});});
    if(lv.length<2)return '';
    const vals=lv.map(function(l){return l.v;});
    const min=Math.min.apply(null,vals),max=Math.max.apply(null,vals),rng=(max-min)||1;
    const W=280,H=16+lv.length*26,padT=12,padB=12,plotH=H-padT-padB,axX=70;
    const y=function(v){return padT+(max-v)/rng*plotH;};
    let bands='';
    if(plan.stop!=null&&e!=null)bands+='<rect x="'+(axX-4)+'" y="'+Math.min(y(e),y(plan.stop)).toFixed(1)+'" width="8" height="'+Math.abs(y(plan.stop)-y(e)).toFixed(1)+'" fill="'+col('negative','#dc5f52')+'" fill-opacity=".18"/>';
    const tps=[plan.tp1,plan.tp2,plan.tp3].filter(function(t){return t!=null;});
    const topTp=tps.length?Math.max.apply(null,tps):null;
    if(topTp!=null&&e!=null)bands+='<rect x="'+(axX-4)+'" y="'+Math.min(y(e),y(topTp)).toFixed(1)+'" width="8" height="'+Math.abs(y(topTp)-y(e)).toFixed(1)+'" fill="'+col('positive','#38b879')+'" fill-opacity=".16"/>';
    const rows=lv.map(function(l){const yy=y(l.v);const pct=(px&&l.v)?((l.v/px-1)*100):null;
      return '<line x1="'+axX+'" y1="'+yy.toFixed(1)+'" x2="'+(axX+8)+'" y2="'+yy.toFixed(1)+'" stroke="'+l.c+'" stroke-width="2"/>'
        +'<circle cx="'+axX+'" cy="'+yy.toFixed(1)+'" r="3" fill="'+l.c+'"/>'
        +'<text x="'+(axX-8)+'" y="'+(yy+3).toFixed(1)+'" text-anchor="end" font-size="10" fill="var(--vx-text-secondary,#b7b2aa)">'+l.k+'</text>'
        +'<text x="'+(axX+14)+'" y="'+(yy+3).toFixed(1)+'" font-size="10.5" fill="'+l.c+'" style="font-variant-numeric:tabular-nums">'+VX.fmt.nd(l.v)+(pct!=null?' ('+(pct>=0?'+':'')+pct.toFixed(1)+'%)':'')+'</text>';}).join('');
    const aria='Échelle risque/récompense : '+lv.map(function(l){return l.k+' '+VX.fmt.nd(l.v);}).join(', ')+(plan.rr?', R:R '+plan.rr:'');
    return '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-width:'+W+'px;display:block;margin:0 auto 10px" role="img" aria-label="'+aria.replace(/"/g,'&quot;')+'">'
      +'<line x1="'+axX+'" y1="'+padT+'" x2="'+axX+'" y2="'+(H-padB)+'" stroke="rgba(255,255,255,.12)"/>'+bands+rows+'</svg>';
  }
  body('an-plan',
    rrLadder(d.price,plan)
    +kv('Entrée',plan.entry)+kv('Stop (invalidation sous-jacent)',plan.stop,'vx-neg')
    +kv('TP1',plan.tp1,'vx-pos')+kv('TP2',plan.tp2,'vx-pos')+kv('TP3',plan.tp3,'vx-pos')
    +kv('R:R structurel',plan.rr)
    +`<div class="vx-flex vx-mt3" style="flex-wrap:wrap;gap:.4rem">
      <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${SYM}','follow')">Créer un suivi</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" onclick="VXCharts.alertFromLevel('${SYM}',${JSON.stringify(plan.entry??null)})">Alerte sur l’entrée</button>
      <button class="vx-btn vx-btn-sm vx-btn-soft" onclick="window.__prepOrder&&window.__prepOrder('${SYM}')">Préparer l’ordre (copier IBKR)</button>
    </div>
    <div id="an-order-ticket" class="vx-mt2"></div>`);
  window.__prepOrder=function(sym){
    const host=document.getElementById('an-order-ticket');if(!host)return;
    const av=Number(localStorage.getItem('vxAccountValue')||'')||null;
    host.innerHTML=`<div class="vx-card" style="border-color:rgba(207,97,40,.35)">
      <div class="vx-card-header"><span class="vx-card-title">Préparation d’ordre — READONLY</span></div>
      <div class="vx-card-body vx-flex" style="gap:.5rem;flex-wrap:wrap;align-items:end">
        <label class="vx-field" style="max-width:170px"><span>Valeur du compte ($)</span>
          <input id="ot-av" class="vx-input" type="number" step="any" value="${av||''}" placeholder="ex. 100000"></label>
        <label class="vx-field" style="max-width:130px"><span>Risque par trade (%)</span>
          <input id="ot-rp" class="vx-input" type="number" step="any" value="1"></label>
        <button class="vx-btn vx-btn-sm" id="ot-go">Calculer le ticket</button>
      </div>
      <div id="ot-out"></div></div>`;
    document.getElementById('ot-go').addEventListener('click',function(){
      const avv=Number(document.getElementById('ot-av').value)||null;
      const rp=Number(document.getElementById('ot-rp').value)||null;
      if(avv)localStorage.setItem('vxAccountValue',String(avv));
      fetch('/api/planning/ticket',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({symbol:sym,account_value:avv,risk_pct:rp})})
        .then(r=>r.json()).then(function(t){
          const out=document.getElementById('ot-out');if(!out)return;
          const s=t.sizing||{};
          const warn=(t.blockers||[]).concat(t.warnings||[]);
          out.innerHTML='<div class="vx-mt2">'
            +'<div class="vx-stats-row" style="display:flex;gap:1.2rem;flex-wrap:wrap">'
            +'<div><div class="vx-meta">Quantité</div><b style="font-size:18px">'+(t.qty!=null?t.qty:'—')+'</b></div>'
            +'<div><div class="vx-meta">Capital à risque</div><b>'+(s.capital_at_risk!=null?'$'+s.capital_at_risk:'—')+'</b></div>'
            +'<div><div class="vx-meta">Capital engagé</div><b>'+(s.capital_deployed!=null?'$'+s.capital_deployed:'—')+'</b></div>'
            +'<div><div class="vx-meta">Poids projeté</div><b>'+(s.weight_pct!=null?s.weight_pct+' %':'—')+'</b></div>'
            +'<div><div class="vx-meta">R:R</div><b>'+(t.reward_risk!=null?t.reward_risk:'—')+'</b></div></div>'
            +(t.blocked?'<div class="vx-stale-banner vx-mt2">⛔ Préparation bloquée par la stratégie : '+warn.map(esc).join(' · ')+'</div>'
              :(warn.length?'<div class="vx-meta vx-mt2" style="color:var(--vx-warning)">'+warn.map(esc).join(' · ')+'</div>':''))
            +'<pre id="ot-pre" style="white-space:pre-wrap;background:var(--vx-surface-2,#1d1f22);padding:.7rem;border-radius:8px;margin-top:.7rem;font-size:12px">'+esc(t.copy_text||'')+'</pre>'
            +'<button class="vx-btn vx-btn-sm vx-btn-ghost" id="ot-copy">Copier le ticket</button>'
            +'<div class="vx-meta vx-mt1">'+esc(t.disclaimer||'')+'</div></div>';
          const cp=document.getElementById('ot-copy');
          if(cp)cp.addEventListener('click',function(){
            const pre=document.getElementById('ot-pre');
            if(pre&&navigator.clipboard)navigator.clipboard.writeText(pre.textContent);
            VX.toast('Ticket copié — à saisir manuellement dans IBKR','success');});
        }).catch(function(e){document.getElementById('ot-out').innerHTML='<div class="vx-error-banner">'+esc(e.message)+'</div>';});
    });
  };

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
  try{loadAnalyst();}catch(e){}
}

/* Analystes PROFONDS (à la demande) : révisions BPA, surprises, notes, détention, initiés.
   Enrichit Catalyseurs + Sentiment sans bloquer le dossier principal. */
async function loadAnalyst(){
  let a=null;
  try{a=await VX.fetch('/api/analyst/'+SYM,{ttl:600000});}catch(e){}
  if(!a||a.demo||a.error)return;
  const $b=id=>document.querySelector('#'+id+' [data-body]');
  const price=(TICKER&&TICKER.detail&&TICKER.detail.price)||null;
  /* Catalyseurs : révisions BPA + surprises + notes datées */
  const er=a.eps_revisions, su=a.surprises, sm=su&&su.summary, ra=a.ratings_actions, et=a.eps_trend;
  let cat='';
  if(su&&su.next)cat+=kv('Prochains résultats (est.)',su.next);
  if(sm)cat+=kv('Surprises BPA',`battu ${sm.beats}/${sm.total} trim.`+(sm.avg!=null?` · moy. ${sm.avg>=0?'+':''}${sm.avg}%`:''),(sm.beats>=sm.total*0.7?'vx-pos':sm.beats<=sm.total*0.4?'vx-neg':''));
  if(er&&er.net30!=null)cat+=kv('Révisions BPA (30j)',`${er.up30||0} ↑ / ${er.down30||0} ↓`+(et&&et.revision_pct_90d!=null?` · estim. ${et.revision_pct_90d>=0?'+':''}${et.revision_pct_90d}% /90j`:''),(er.trend==='up'?'vx-pos':er.trend==='down'?'vx-neg':''));
  if(a.growth_fwd!=null)cat+=kv('Croissance BPA attendue',`${a.growth_fwd>=0?'+':''}${a.growth_fwd}%`);
  if(ra&&ra.length){
    cat+=`<div class="vx-meta vx-mt2" style="text-transform:uppercase;letter-spacing:.04em">Notes récentes</div>`;
    cat+=ra.slice(0,4).map(function(r){
      const s=(r.pt_action||'')+' '+(r.to||'');
      const dir=/rais|upgrade|overweight|\bbuy\b|outperform/i.test(s)?'vx-pos':/low|cut|downgrade|underweight|\bsell\b|reduce/i.test(s)?'vx-neg':'';
      const tgt=r.target?` → ${VX.fmt.price(r.target)}`+(r.prior&&r.prior!==r.target?` (av. ${VX.fmt.price(r.prior)})`:''):'';
      return `<div class="vx-kv"><span class="k">${esc(r.date)} · ${esc(r.firm)}</span><span class="v ${dir}">${esc(r.to||r.pt_action||r.action)}${tgt}</span></div>`;
    }).join('');
  }
  if(cat){const el=$b('an-catalysts');if(el)el.innerHTML+=`<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#26221e);padding-top:8px">${cat}</div>`;}
  /* Sentiment : détention institutionnelle (13F) + initiés */
  let sen='';
  if(a.holders&&a.holders.length){
    sen+=`<div class="vx-meta vx-mt2" style="text-transform:uppercase;letter-spacing:.04em">Top détenteurs (13F)</div>`;
    sen+=a.holders.slice(0,5).map(function(h){
      return `<div class="vx-kv"><span class="k">${esc(h.holder)}</span><span class="v">${h.pct!=null?(h.pct*100).toFixed(1)+' %':'—'}${h.change?` <span class="${h.change>0?'vx-pos':'vx-neg'}">(${h.change>0?'+':''}${(h.change*100).toFixed(0)}%)</span>`:''}</span></div>`;
    }).join('');
  }
  if(a.insider){const ib=a.insider;
    sen+=kv('Initiés (récent)',`${ib.buys} achat(s) / ${ib.sells} vente(s)`,(ib.bias==='buy'?'vx-pos':ib.bias==='sell'?'vx-neg':''));
  }
  if(sen){const el=$b('an-sentiment');if(el)el.innerHTML+=`<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#26221e);padding-top:8px">${sen}</div>`;}
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
