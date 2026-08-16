"""vertex.ui.pages.opportunities_page — découverte actions & options (§24).

Question : « Quelles opportunités méritent réellement une analyse ? »
Sous-vues : radar, stocks, options, anomalies, calendar.
"""
from __future__ import annotations


from vertex.ui.shell import json_for_script, render_shell

_VIEWS = (('radar', 'Radar'), ('stocks', 'Actions'), ('options', 'Options'),
          ('anomalies', 'Anomalies'), ('calendar', 'Calendrier'))


def _tabs(view: str) -> str:
    return ('<div class="vx-tabs" role="tablist">'
            + ''.join(f'<a class="vx-tab" role="tab" aria-selected='
                      f'"{"true" if v == view else "false"}" '
                      f'href="/opportunities?view={v}">{label}</a>'
                      for v, label in _VIEWS) + '</div>')


_CONTENT = """
<div class="vx-page-header vx-page-lead"><div><h1>Opportunités</h1>
<div class="vx-sub">Les dossiers qui méritent ton attention.</div></div>
<div class="vx-actions vx-toolbar"><span id="op-fresh" style="align-self:center"></span><button class="vx-btn vx-btn-sm"
  onclick="VXEntities.openAddModal()">+ Ajouter</button></div></div>
%%TABS%%
<div id="op-body" class="vx-mt4 vx-section-stack">%%LOADING%%</div>
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
function esc(s){return String(s??'').replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));}
const OUT=['Rejetée','Radar','À surveiller','Proche','Actionnable','Invalidée'];
function bucketOf(r){
  if(r.verdict==='AVOID'||r.verdict==='ÉVITER')return'Rejetée';
  if((r.rr_ok&&r.score>=72&&(r.verdict==='BUY'||r.verdict==='ACHETER')))return'Actionnable';
  if(r.score>=66)return'Proche';
  if(r.score>=56)return'À surveiller';
  return'Radar';
}
/* verdict → classe sémantique (buy/achat=vert, attente/surveille=jaune, évite/refus=rouge) */
function vCls(v){var s=String(v||'').toLowerCase();
  if(!s)return'';
  if(/(buy|achet|renforc|accumul|acheter|long\b|s\+)/.test(s))return'vx-pos';
  if(/(avoid|évit|evit|refus|réduir|reduir|sell|vendre|rejet|short)/.test(s))return'vx-neg';
  if(/(hold|attend|neutre|patience|surveil|proche|watch|radar)/.test(s))return'vx-warn';
  return'';}
/* bucket de statut → classe sémantique (actionnable=vert, proche/surveille=jaune, rejetée=rouge) */
function bucketCls(b){var s=String(b||'').toLowerCase();
  if(/actionnable/.test(s))return'vx-pos';
  if(/(rejet|invalid)/.test(s))return'vx-neg';
  if(/(proche|surveil|attente)/.test(s))return'vx-warn';
  return'';}
/* playbook peut être une chaîne OU un objet moteur → toujours une chaîne sûre */
function pbStr(pb){return (pb&&typeof pb==='object')?(pb.name||pb.label||pb.key||pb.type||''):(pb||'');}
function metaMode(scan){return scan&&scan.data_source==='demo'?'fallback':'delayed';}
function demoBanner(scan){return scan&&scan.data_source==='demo'?
  '<div class="vx-stale-banner">Mode DÉMO — données synthétiques, clairement identifiées.</div>':'';}
function rowActions(sym){return `<div class="vx-row-actions">
  <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${sym}">Analyse</button>
  <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${sym}" aria-label="Actions ${sym}">${VX.icon('more')}</button></div>`;}

/* ── Champs réels par ligne (jamais inventés) ── */
function opGrade(r){const g=(r.grade||'').toString().trim();
  if(g&&g!=='—')return g;return tierOf(r);}  /* moteur d'abord, sinon dérivé des buckets */
function opActive(rows){return (rows||[]).filter(r=>r.verdict!=='AVOID'&&r.verdict!=='ÉVITER');}
function opRanked(rows){const prio=(r)=>{const b=bucketOf(r);return b==='Actionnable'?0:b==='Proche'?1:b==='À surveiller'?2:3;};
  return opActive(rows).slice().sort((a,b)=>prio(a)-prio(b)||(b.score||0)-(a.score||0));}
function pctv(v){return (v==null||isNaN(v))?null:(v<=1?Math.round(v*100):Math.round(v));}
/* Momentum multi-horizon (perf_w/m/q/y RÉELS) → mini-barres d'intensité */
function momBars(r){
  const H=[['1S',r.perf_w],['1M',r.perf_m],['1T',r.perf_q],['1A',r.perf_y]].filter(x=>x[1]!=null&&!isNaN(x[1]));
  if(!H.length)return '';
  const mx=Math.max(6,...H.map(x=>Math.abs(x[1])));
  return '<div class="vx-op-mom" aria-label="momentum 1S/1M/1T/1A">'+H.map(function(x){
    const h=Math.max(10,Math.round(Math.abs(x[1])/mx*100));const col=x[1]>=0?'var(--vx-positive)':'var(--vx-negative)';
    return '<span class="b" title="'+x[0]+' '+VX.fmt.pct(x[1],1)+'"><i style="height:'+h+'%;background:'+col+'"></i><span>'+x[0]+'</span></span>';
  }).join('')+'</div>';
}
/* ── CARTE OPPORTUNITÉ DOMINANTE (distincte, signature) ── */
function renderDominant(rows,scan,catBySym){
  const el=$('op-dominant');if(!el)return;
  const best=opRanked(rows)[0];
  if(!best){el.innerHTML='';return;}
  const g=opGrade(best);const asym=best.vx_asym,pwin=pctv(best.vx_pwin),rr=best.vx_rr,edge=best.vx_edge;
  const cat=catBySym&&catBySym[best.symbol];
  const inval=(best.vx_stopfirst!=null)?('probabilité que le stop parte en premier : '+pctv(best.vx_stopfirst)+' % — stop structurel défini dans le dossier')
    :'stop structurel défini dans le dossier (Analyse)';
  const metric=(k,v,hot)=>`<div class="vx-op-metric${hot?' hot':''}"><span class="k">${k}</span><span class="v">${v}</span></div>`;
  el.innerHTML=
    `<div class="vx-op-dominant" aria-label="Opportunité dominante ${esc(best.symbol)}">
      <div class="vx-op-dom-l">
        <span class="vx-op-dom-badge">Opportunité dominante</span>
        <div class="vx-op-dom-tk"><span class="sym vx-ticker" style="cursor:pointer" role="button" tabindex="0" data-open-analysis="${esc(best.symbol)}">${esc(best.symbol)}</span>
          <span class="vx-op-grade" data-g="${esc(g)}">${esc(g)}</span></div>
        <div class="vx-op-dom-sub">${esc(best.sector||best.industry||'secteur n/d')} · ${best.price!=null?VX.fmt.price(best.price):'cours n/d'}
          ${best.verdict?' · <b class="'+vCls(best.verdict)+'">'+esc(best.verdict)+'</b>':''}</div>
        <div class="vx-op-dom-score"><span class="n">${VX.fmt.nd(best.score)}</span><span class="u">/100 · score Vertex</span></div>
        ${momBars(best)?'<div style="margin-top:4px"><div class="vx-meta" style="margin-bottom:4px">Momentum 1S · 1M · 1T · 1A</div>'+momBars(best)+'</div>':''}
      </div>
      <div class="vx-op-dom-r">
        <div class="vx-op-metrics vx-kpi-strip">
          ${metric('Asymétrie',asym!=null?VX.fmt.nd(asym):'n/d',asym!=null&&asym>=25)}
          ${metric('Probabilité de gain',pwin!=null?pwin+' %':'n/d',pwin!=null&&pwin>=55)}
          ${metric('R:R visé',rr!=null?VX.fmt.nd(rr):'n/d')}
          ${metric('Qualité données',best.vx_tq!=null?VX.fmt.nd(best.vx_tq)+'/100':'n/d')}
        </div>
        <div class="vx-op-lines">
          <div class="row"><span class="k">Catalyseur</span><span class="v">${cat?esc(cat):'aucun catalyseur daté à l’horizon du calendrier'}</span></div>
          <div class="row"><span class="k">Invalidation</span><span class="v risk">${esc(inval)}</span></div>
          <div class="row"><span class="k">Edge composite</span><span class="v">${edge!=null?VX.fmt.nd(edge)+'/100':'n/d'}</span></div>
          <div class="row"><span class="k">Profil</span><span class="v">${esc((best.profile||'')+(best.profile_hint?' — '+best.profile_hint:''))||'n/d'}</span></div>
        </div>
        <div class="vx-flex vx-wrap" style="gap:.4rem;margin-top:auto">
          <button class="vx-btn vx-btn-primary" data-open-analysis="${esc(best.symbol)}">Ouvrir le dossier ${esc(best.symbol)} →</button>
          <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${esc(best.symbol)}','alert')">Alerte</button>
          <span class="vx-grow"></span>
          <span class="vx-meta">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',metaMode(scan))}</span>
        </div>
      </div>
    </div>`;
}
/* ── SHORTLIST : 3 cartes ticker secondaires (identité, densité variable) ── */
function renderShortlist(rows,scan,catBySym){
  const el=$('op-shortlist');if(!el)return;
  const list=opRanked(rows).slice(1,4);  /* après la dominante */
  if(!list.length){el.innerHTML='';return;}
  el.innerHTML='<div class="vx-col-12 vx-op-sectitle">Shortlist</div>'
    +list.map(function(r){const g=opGrade(r);const cat=catBySym&&catBySym[r.symbol];
    return `<div class="vx-col-4"><div class="vx-op-tk" aria-label="${esc(r.symbol)}">
      <div class="vx-op-tk-top">
        <span class="vx-op-mono">${esc(r.symbol).slice(0,4)}</span>
        <span class="vx-op-tk-name"><span class="sym vx-ticker" style="cursor:pointer" role="button" tabindex="0" data-open-analysis="${esc(r.symbol)}">${esc(r.symbol)}</span>
          <span class="sec">${esc(r.sector||r.industry||'')}</span></span>
        <span class="vx-op-tk-grade" data-g="${esc(g)}">${esc(g)}</span>
      </div>
      <div class="vx-op-tk-row"><span class="vx-op-tk-score">${VX.fmt.nd(r.score)}<span class="vx-meta" style="font-size:11px;font-weight:600"> /100</span></span>
        <span class="vx-op-tk-asym">asym. ${r.vx_asym!=null?VX.fmt.nd(r.vx_asym):'n/d'} · R:R ${r.vx_rr!=null?VX.fmt.nd(r.vx_rr):'n/d'}${r.vx_pwin!=null?' · p '+pctv(r.vx_pwin)+'%':''}</span></div>
      <div class="vx-meta vx-truncate" title="${esc(cat||'')}">${cat?esc(cat):(r.profile_hint?esc(r.profile_hint):'—')}</div>
      ${momBars(r)}
      <div class="vx-op-tk-foot"><button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${esc(r.symbol)}">Analyser →</button>
        <span class="${vCls(r.verdict)}">${esc(r.verdict||'')}</span></div>
    </div></div>`;}).join('');
}
/* ── MATRICE DE COMPARAISON (2-4 meilleurs candidats, barres/rails, meilleur mis en avant) ── */
function renderCompare(rows){
  const el=$('op-compare');if(!el)return;
  const cand=opRanked(rows).slice(0,4);
  const disclosure=el.closest('details');
  if(cand.length<2){el.innerHTML='';if(disclosure)disclosure.hidden=true;return;}
  if(disclosure)disclosure.hidden=false;
  /* métriques réelles : (clé, label, accessor, max pour le rail, higherIsBetter) */
  const M=[
    ['score','Score',r=>r.score,100,true],
    ['asym','Asymétrie',r=>r.vx_asym,50,true],
    ['pwin','Prob. gain %',r=>pctv(r.vx_pwin),100,true],
    ['rr','R:R visé',r=>r.vx_rr,8,true],
    ['edge','Edge',r=>r.vx_edge,100,true],
    ['mom','Momentum 1M %',r=>r.perf_m,20,true],
    ['tq','Qualité données',r=>r.vx_tq,100,true],
  ];
  const head='<tr><th>Critère</th>'+cand.map((r,i)=>`<th class="sym${i===0?' best':''}">${esc(r.symbol)}${i===0?'<span class="vx-sr-only"> — meilleur candidat</span>':''}</th>`).join('')+'</tr>';
  const body=M.map(function(m){
    const vals=cand.map(m[2]);
    const nums=vals.map(v=>(v==null||isNaN(v))?null:v);
    const valid=nums.filter(v=>v!=null);
    const best=valid.length?(m[4]?Math.max.apply(null,valid):Math.min.apply(null,valid)):null;
    const cells=cand.map(function(r,i){const v=nums[i];
      const w=v==null?0:Math.max(6,Math.min(100,Math.abs(v)/m[3]*100));
      const win=(v!=null&&best!=null&&v===best);
      return `<td class="${i===0?'bestcol':''}"><div class="vx-op-cmp-cell${win?' win':''}">
        <span class="rail"><i style="width:${w.toFixed(0)}%"></i></span>
        <span class="n">${v==null?'n/d':VX.fmt.nd(v)}</span></div></td>`;}).join('');
    return `<tr><td class="metric">${m[1]}</td>${cells}</tr>`;}).join('');
  el.innerHTML='<div class="vx-card"><div class="vx-chart-head"><span class="vx-chart-title">Comparaison</span>'
    +'<span class="vx-chart-question">Lequel offre le meilleur couple asymétrie × probabilité ?</span></div>'
    +'<div class="vx-table-wrap"><table class="vx-op-cmp">'+'<thead>'+head+'</thead><tbody>'+body+'</tbody></table></div>'
    +'<div class="vx-card-foot"><span class="vx-meta">Barres = intensité relative par critère ; orange = meilleur du critère. Champs moteur réels (score, asymétrie vx_asym, prob. gain vx_pwin, R:R vx_rr, edge, momentum, qualité) — aucune valeur inventée. ★ = tête de shortlist.</span></div></div>';
}

/* ── ENTONNOIR D'OPPORTUNITÉS (§11-12) : univers → … → actionnable ── */
async function renderFunnel(){
  const el=$('op-funnel');if(!el)return;
  /* LOT 602 (dossier 531-A) : un echec ne laisse plus la colonne vide et muette.
     Invariant produit : donnee absente -> mention honnete, jamais du silence. */
  let f;try{f=await VX.fetch('/api/opportunities/funnel',{ttl:60000});}
  catch(e){el.innerHTML=VX.states.error('Entonnoir indisponible');return;}
  if(!f||!f.stages||!f.stages.length){
    el.innerHTML=VX.states.empty('Entonnoir vide — aucun etage retourne par le moteur.');return;}
  const roleColor={'ATTAQUE':'var(--vx-positive,#2BBE90)','MILIEU':'var(--vx-beige,#c8bfae)',
    'DÉFENSE':'var(--vx-neutral-chart,#BABABA)','RÉSERVE':'var(--vx-text-muted,#989092)'};
  const roles=(f.roles||[]).map(function(r){
    return '<span class="vx-chip" style="border:1px solid '+ (roleColor[r.role]||'#555')
      +';color:'+(roleColor[r.role]||'#aaa')+'">'+esc(r.role)+' '+esc(r.count)+'</span>';
  }).join(' ');
  /* Conclusion : plus forte déperdition entre deux étages (donnée réelle). */
  let concl='';const st=f.stages;
  if(st.length>=2){let bi=0,bd=0;for(let i=1;i<st.length;i++){const d=(st[i-1].count||0)-(st[i].count||0);if(d>bd){bd=d;bi=i;}}
    concl=bd>0?('Plus forte déperdition : '+esc(st[bi-1].label)+' → '+esc(st[bi].label)+' (−'+bd+').')
      :'Entonnoir plat — peu de déperdition entre étages.';}
  el.innerHTML='<section class="vx-card vx-card--compact" aria-label="Entonnoir de sélection"><div class="vx-card-header"><span class="vx-card-title">Sélection</span>'
    +'<span class="vx-chart-question">Que reste-t-il après filtrage ?</span></div>'
    +'<div class="vx-flex vx-wrap" style="gap:.35rem;margin-bottom:.4rem">'+roles+'</div>'
    +'<div id="op-funnel-viz"></div>'
    +(concl?'<div class="vx-op-sectitle" style="margin:.6rem 2px 0;text-transform:none;letter-spacing:0;font-weight:600;color:var(--vx-text-secondary)">'+concl+'</div>':'')
    +(f.note?'<div class="vx-dim" style="font-size:12px;margin-top:.4rem">'+esc(f.note)+'</div>':'')
    +(f.actionable_symbols&&f.actionable_symbols.length?'<div class="vx-dim" style="font-size:12px;margin-top:.4rem">Actionnables : '
      +f.actionable_symbols.map(function(s){return '<b style="color:var(--vx-positive)">'+esc(s)+'</b>';}).join(' · ')+'</div>':'')
    +'</section>';
  /* Vrai entonnoir décroissant (trapèzes + % par étage) au lieu des colonnes texte —
     donnée réelle /api/opportunities/funnel, jamais inventée ; le composant gère
     lui-même le repli si < 2 étages. */
  if(window.VXCharts&&VXCharts.funnel){
    VXCharts.funnel('op-funnel-viz',{stages:f.stages.map(function(s){return {label:s.label,value:s.count};}),
      fmt:function(v){return VX.fmt.nd(v);},ariaLabel:'Entonnoir d\'opportunités : univers vers actionnables'});
  }
}

/* ── RADAR (§24) : X qualité stratégique · Y timing · taille intensité ── */
/* Catalyseurs datés RÉELS (résultats à venir) indexés par symbole, depuis le
   calendrier moteur — jamais inventés ; absence → pas de catalyseur affiché. */
async function opCatalysts(){
  const by={};try{const cal=await VX.fetch('/cal-feed',{ttl:300000});
    (cal.items||[]).forEach(it=>{if(it&&it.sym&&it.dte!=null)by[it.sym]='Résultats dans '+it.dte+' j'
      +(it.verdict?' · '+it.verdict:'');});}catch(e){}
  return by;
}
async function renderRadar(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>r.score!==undefined);
  if(!rows.length){$('op-body').innerHTML=VX.states.empty('Aucun titre scanné — lancer un scan depuis Système.');return;}
  const catBySym=await opCatalysts();
  const best=opRanked(rows)[0];
  $('op-body').innerHTML=demoBanner(scan)
    +'<div id="op-hero"></div>'
    +'<div class="vx-grid vx-mt4" id="op-shortlist"></div>'
    +'<div class="vx-grid vx-hero-grid vx-mt4">'
      +'<div class="vx-col-8"><div id="op-scatter"></div>'
        +'<div id="op-scatter-missing" class="vx-meta vx-mt2"></div>'
        +'<section class="vx-card vx-mt3" id="op-scatter-sel-card"><div class="vx-card-header"><span class="vx-card-title">Point sélectionné</span>'
          +'<span class="vx-chart-question">Inspecte un titre du scatter</span></div>'
          +'<div id="op-scatter-sel" class="vx-op-scatter-sel"><div class="vx-help">Clique un point du scatter pour l’inspecter'
          +(best?', ou ouvre directement la meilleure opportunité : <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="'+esc(best.symbol)+'">Ouvrir '+esc(best.symbol)+' →</button>':'')+'.</div></div></section></div>'
      +'<aside class="vx-col-4 vx-insight-rail" id="op-funnel"></aside></div>'
    +'<details class="vx-disclosure vx-mt4" id="op-compare-disclosure"><summary>Comparer les candidats sous forme de matrice</summary>'
      +'<div id="op-compare" class="vx-mt3"></div></details>';
  renderHero(rows,scan,best,catBySym);
  renderDominant(rows,scan,catBySym);
  renderFunnel();
  renderShortlist(rows,scan,catBySym);
  renderCompare(rows);
  const bestSym=best?best.symbol:null;
  /* Un point n'existe que si SES DEUX axes sont présents. Les titres dont le
     timing ou la qualité manque restent explicitement hors du nuage : jamais
     de repli visuel à 50, qui fabriquerait une position neutre. */
  const axisNum=(v)=>v===null||v===undefined||v===''?null:Number(v);
  const axisOk=(v)=>v!==null&&Number.isFinite(v)&&v>=0&&v<=100;
  const scatterRows=rows.map(function(r){
    const x=axisNum(r.strat_score??r.score),y=axisNum(r.st_tech??r.rs);
    return {r:r,x:x,y:y,ok:axisOk(x)&&axisOk(y)};
  });
  const plotted=scatterRows.filter(p=>p.ok),missing=scatterRows.filter(p=>!p.ok);
  const missingHost=$('op-scatter-missing');
  if(missingHost)missingHost.innerHTML=missing.length
    ?'<b>'+missing.length+' titre(s) hors nuage :</b> axe qualité ou timing n/d / hors plage 0–100 — '
      +missing.slice(0,8).map(p=>esc(p.r.symbol)).join(' · ')+(missing.length>8?' · …':'')
    :'Tous les titres affichés disposent des deux axes.';
  VXCharts.card('op-scatter',{
    title:'Qualité × timing',
    question:'Où se trouvent les meilleurs couples qualité × timing ?',
    conclusion:(function(){const a=plotted.filter(p=>bucketOf(p.r)==='Actionnable').length;
      return a?(a+' candidat(s) en zone actionnable (haut-droit)'):'Aucun candidat en zone actionnable — attendre reste valide';})(),
    height:360,unit:'score 0-100',source:scan.source,timestamp:scan.scan_ts||scan.updated,mode:metaMode(scan),
    summary:'Nuage de points des titres disposant de deux scores : qualité stratégique en X, timing en Y ; les données incomplètes sont listées hors du graphique.',
    explain:{shows:'Chaque point est un titre scanné, placé par les scores moteur (qualité en X, timing en Y).',
      why:'La stratégie n’engage que lorsque qualité ET timing convergent (coin haut-droit).',
      confirm:'Un point qui migre vers le haut-droit avec volume.',
      invalidate:'Retour sous 55 en qualité stratégique.'},
    render:(cv)=>VXCharts.mount(cv,{type:'scatter',
      data:{datasets:[{data:plotted.map(p=>{const r=p.r;return {x:p.x,y:p.y,tOk:true,sym:r.symbol,
          v:r.verdict,setup:(r.profile||'')+(r.profile_hint?' — '+r.profile_hint:''),sector:r.sector||'',price:r.price,rr:r.vx_rr,asym:r.vx_asym,pwin:r.vx_pwin,score:r.score,
          best:r.symbol===bestSym,r:5+Math.min(8,(r.anomaly_score||r.sigcount||0))};}),
        pointRadius:(ctx)=>ctx.raw?ctx.raw.r:4,pointHoverRadius:(ctx)=>ctx.raw?ctx.raw.r+3:7,
        pointBackgroundColor:(ctx)=>{const raw=ctx.raw;if(raw&&raw.best)return VXCharts.colors.brand;const v=raw&&raw.v;const cc=VXCharts.colors;
          return v==='BUY'||v==='ACHETER'?cc.positive:(v==='AVOID'||v==='ÉVITER'?cc.negative:cc.neutral);},
        pointBorderColor:(ctx)=>ctx.raw&&ctx.raw.best?VXCharts.colors.brand:%%DEMO_BORDER%%,
        pointBorderWidth:(ctx)=>ctx.raw&&ctx.raw.best?2:1}]},
      options:{scales:{x:{min:0,max:100,title:{display:true,text:'Qualité stratégique →'},grid:{color:'rgba(255,255,255,.06)'}},
        y:{min:0,max:100,title:{display:true,text:'Qualité du timing ↑'},grid:{color:'rgba(255,255,255,.06)'}}},
        onClick:(evt,els,chart)=>{const pts=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
          if(pts.length){const d=chart.data.datasets[0].data[pts[0].index];
            document.getElementById('op-scatter-sel').innerHTML=
              `<div class="vx-flex"><span class="vx-ticker" style="font-size:18px" role="button" tabindex="0" data-open-analysis="${d.sym}">${d.sym}</span>${window.VXEntities.badges(d.sym)}
                 <span class="vx-badge vx-badge-decision vx-right" data-decision="${d.v||''}">${d.v||'n/d'}</span></div>
               <div class="vx-op-metrics vx-mt2">
                 <div class="vx-op-metric"><span class="k">Qualité strat.</span><span class="v">${VX.fmt.nd(d.x)}</span></div>
                 <div class="vx-op-metric"><span class="k">Timing</span><span class="v">${d.tOk?VX.fmt.nd(d.y):'n/d'}</span></div>
                 <div class="vx-op-metric"><span class="k">Asymétrie</span><span class="v">${VX.fmt.nd(d.asym)}</span></div>
                 <div class="vx-op-metric"><span class="k">R:R visé</span><span class="v">${VX.fmt.nd(d.rr)}</span></div></div>
               <div class="vx-kv vx-mt2"><span class="k">Cours</span><span class="v vx-mono">${d.price!==undefined&&d.price!==null?VX.fmt.price(d.price):'n/d'}</span></div>
               ${d.sector?`<div class="vx-kv"><span class="k">Secteur</span><span class="v">${esc(d.sector)}</span></div>`:''}
               <div class="vx-flex vx-wrap vx-mt2">
                 <button class="vx-btn vx-btn-sm vx-btn-primary" data-open-analysis="${d.sym}">Ouvrir le dossier</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${d.sym}','watchlist')">Watchlist</button>
                 <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${d.sym}','alert')">Alerte</button>
                 <a class="vx-btn vx-btn-sm" href="/opportunities?view=options&sym=${d.sym}">Options</a></div>`;}},
        plugins:{tooltip:{callbacks:{label:(ctx)=>`${ctx.raw.sym} · qualité ${VX.fmt.nd(ctx.raw.x)} · timing ${ctx.raw.tOk?VX.fmt.nd(ctx.raw.y):'n/d'} · asym ${VX.fmt.nd(ctx.raw.asym)}`}}}},
      plugins:[{id:'opQuad',afterDatasetsDraw(chart){const a=chart.chartArea,sx=chart.scales.x,sy=chart.scales.y;
        const xc=sx.getPixelForValue(55),yc=sy.getPixelForValue(55);const g=chart.ctx;g.save();
        /* LOT 121 : la zone actionnable (haut-droit) est TEINTÉE d'un dégradé
           positif très léger — on voit la cible avant de lire les axes. */
        if(xc<a.right&&yc>a.top){const gz=g.createLinearGradient(xc,yc,a.right,a.top);
          gz.addColorStop(0,VXCharts.colors.positive+'00');gz.addColorStop(1,VXCharts.colors.positive+'22');
          g.fillStyle=gz;g.fillRect(xc,a.top,a.right-xc,yc-a.top);}
        g.strokeStyle='rgba(255,255,255,.12)';g.setLineDash([4,4]);g.beginPath();
        if(xc>a.left&&xc<a.right){g.moveTo(xc,a.top);g.lineTo(xc,a.bottom);}
        if(yc>a.top&&yc<a.bottom){g.moveTo(a.left,yc);g.lineTo(a.right,yc);}g.stroke();g.setLineDash([]);
        g.font='700 10px sans-serif';g.fillStyle='rgba(255,255,255,.30)';
        g.fillText('À ÉTUDIER',a.right-64,a.top+14);g.fillText('TIMING SEUL',a.left+6,a.top+14);
        g.fillText('QUALITÉ SEULE',a.right-82,a.bottom-8);g.fillText('À ÉVITER',a.left+6,a.bottom-8);
        /* Étiquettes directes sur les meilleurs candidats (haut-droit) */
        const ds=chart.getDatasetMeta(0).data,raw=chart.data.datasets[0].data;
        const idx=raw.map((d,i)=>[d,i]).filter(x=>x[0].x>=55&&x[0].tOk&&x[0].y>=55)
          .sort((p,q)=>(q[0].score||0)-(p[0].score||0)).slice(0,4);
        g.font='700 11px sans-serif';
        idx.forEach(([d,i])=>{const m=ds[i];if(!m)return;g.fillStyle=d.best?VXCharts.colors.brand:'rgba(248,245,243,.92)';
          g.fillText(d.sym,Math.min(m.x+8,a.right-30),m.y-6);});
        g.restore();}}]})});
}

/* ── HERO ÉDITORIAL : combien d'asymétries, laquelle domine, honnêteté ── */
function tierOf(r){
  /* Niveaux dérivés des seuils moteur existants (bucketOf) → langage S+/S/A/B.
     Aucun score inventé : mappe les buckets réels. */
  const b=bucketOf(r);
  if(b==='Actionnable'&&(r.score||0)>=80)return 'S+';
  if(b==='Actionnable')return 'S';
  if(b==='Proche')return 'A';
  if(b==='À surveiller')return 'B';
  return b==='Rejetée'?'ÉVITER':'—';
}
/* ── HERO éditorial COMPACT : compte S+/S/A, meilleure, asymétrie, catalyseur,
      qualité des données, conclusion — jamais 40 % de vide, jamais inventé. ── */
function renderHero(rows,scan,best,catBySym){
  const el=$('op-hero');if(!el)return;
  const active=opActive(rows);
  const cnt={'S+':0,'S':0,'A':0,'B':0};active.forEach(r=>{const t=opGrade(r);if(cnt[t]!=null)cnt[t]++;});
  const m=metaMode(scan);const dq=m==='fallback'?'Démo':m==='live'?'Temps réel':'Différé';
  /* Message éditorial — UNIQUEMENT à partir des données réelles. */
  let msg,tone;
  if(cnt['S+']){msg=cnt['S+']+' opportunité(s) S+ exceptionnelle(s) détectée(s).';tone='go';}
  else if(cnt['S']){msg='Aucune opportunité S+ aujourd’hui. '+cnt['S']+' dossier(s) S méritent une analyse.';tone='go';}
  else if(cnt['A']){msg='Aucune asymétrie exceptionnelle. '+cnt['A']+' dossier(s) A à surveiller.';tone='wait';}
  else {msg='Aucune asymétrie exceptionnelle détectée. Attendre est une décision valide.';tone='wait';}
  const rankBadges='<div class="vx-toolbar vx-mt2" aria-label="Niveaux de la sélection">'
    +'<span class="vx-badge">S+ · '+cnt['S+']+'</span>'
    +'<span class="vx-badge">S · '+cnt['S']+'</span>'
    +'<span class="vx-badge">A · '+cnt['A']+'</span>'
    +'<span class="vx-badge">Données · '+dq+'</span></div>';
  /* Le message éditorial et la meilleure opportunité partagent désormais UNE
     seule carte hero. Les quatre métriques décisionnelles vivent dans la
     dominante ; les volumes S+/S/A restent de simples badges de contexte. */
  el.innerHTML='<section class="vx-card vx-card--hero" aria-label="Réponse du radar">'
    +'<div class="vx-card-header"><span class="vx-card-title">Priorités</span>'
    +'<span class="vx-actions"><span class="vx-freshness" data-live="'+(m==='fallback'?'fallback':'delayed')+'"><span class="vx-live-dot"></span>'+dq+'</span></span></div>'
    +'<div class="vx-grid vx-hero-grid"><div class="vx-col-5 vx-page-lead">'
      +'<div class="vx-op-hero-lead"><span class="tag" data-tone="'+tone+'">'+(cnt['S+']||cnt['S']?'À étudier':'Patience')+'</span>'
        +'<span class="txt">'+msg+'</span></div>'+rankBadges+'</div>'
      +'<div class="vx-col-7 vx-insight-rail" id="op-dominant"></div></div>'
    +'</section>';
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
    if(state.setup)f=f.filter(r=>(pbStr(r.playbook)||r.profile||'').toUpperCase().includes(state.setup));
    if(state.minScore)f=f.filter(r=>(r.score||0)>=state.minScore);
    f=f.slice().sort((a,b)=>(b.score||0)-(a.score||0));
    /* LOT 135 : le score n'est plus un chiffre nu — mini-barre de verre
       graduée 0-100 (>=70 positive, 40-69 warning, <40 negative ; dégradé
       doux → dense via color-mix sur tokens). L'œil classe le scan. */
    const scoreBar=(v)=>{const n=Number(v);if(!isFinite(n))return VX.fmt.nd(v);
      const tok=n>=70?'var(--vx-positive,#2BBE90)':n>=40?'var(--vx-warning,#D9BE3C)':'var(--vx-negative,#E9555F)';
      return '<span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">'
        +'<span style="width:56px;height:8px;background:var(--vx-surface-3,#121214);border-radius:3px;overflow:hidden;display:inline-block">'
        +'<span style="display:block;height:100%;width:'+Math.max(3,Math.min(100,n)).toFixed(0)+'%;background:linear-gradient(90deg,color-mix(in srgb,'+tok+' 35%,transparent),'+tok+');border-radius:3px"></span></span>'
        +'<span style="font-variant-numeric:tabular-nums">'+VX.fmt.nd(n)+'</span></span>';};
    const decisionCell=(r)=>`<span class="vx-badge ${bucketCls(bucketOf(r))}">${bucketOf(r)}</span>`
      +(r.verdict?`<span class="vx-meta ${vCls(r.verdict)}">${esc(r.verdict)}</span>`:'');
    const essentialRow=(r)=>`<tr data-clickable data-open-analysis="${r.symbol}">
      <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span><span class="vx-meta">${esc(r.sector||'secteur n/d')}</span></td>
      <td data-label="Décision">${decisionCell(r)}</td>
      <td data-label="Score" class="vx-num">${scoreBar(r.score)}</td>
      <td data-label="Cours" class="vx-num">${VX.fmt.nd(r.price!==undefined?VX.fmt.price(r.price):null)}</td>
      <td data-label="R:R" class="vx-num">${VX.fmt.nd(r.rr)}</td>
      <td data-label="Action">${rowActions(r.symbol)}</td></tr>`;
    const technicalRow=(r)=>`<tr data-clickable data-open-analysis="${r.symbol}">
      <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span></td>
      <td data-label="Décision">${decisionCell(r)}</td>
      <td data-label="Score" class="vx-num">${scoreBar(r.score)}</td>
      <td data-label="Cours" class="vx-num">${VX.fmt.nd(r.price!==undefined?VX.fmt.price(r.price):null)}</td>
      <td data-label="R:R" class="vx-num">${VX.fmt.nd(r.rr)}</td>
      <td data-label="Setup" class="vx-truncate" title="${esc(pbStr(r.playbook)||r.profile||'—')}">${esc(pbStr(r.playbook)||r.profile||'—')}</td>
      <td data-label="Secteur">${esc(r.sector||'—')}</td>
      <td data-label="Action">${rowActions(r.symbol)}</td></tr>`;
    $('op-table').innerHTML=f.length?`<section class="vx-card" aria-label="Meilleures actions du scan">
      <div class="vx-card-header"><span class="vx-card-title">Dossiers à étudier</span>
        <span class="vx-meta vx-right">Top ${Math.min(10,f.length)} sur ${f.length}</span></div>
      <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Décision</th><th class="vx-num" data-sortable>Score</th>
        <th class="vx-num">Cours</th><th class="vx-num">R:R</th><th>Action</th></tr></thead>
        <tbody>${f.slice(0,10).map(essentialRow).join('')}</tbody></table></div></section>
      <details class="vx-disclosure vx-mt3" id="op-stocks-full"><summary>Voir les ${f.length} titres et les détails techniques</summary>
        <div class="vx-table-wrap vx-table-cards vx-mt2"><table class="vx-table"><thead><tr>
          <th>Titre</th><th>Décision</th><th class="vx-num">Score</th><th class="vx-num">Cours</th>
          <th class="vx-num">R:R</th><th>Setup</th><th>Secteur</th><th>Action</th></tr></thead>
          <tbody>${f.map(technicalRow).join('')}</tbody></table></div></details>`
      :VX.states.empty('Aucun titre ne correspond aux filtres.','<button class="vx-btn vx-btn-sm" id="op-clear">Effacer les filtres</button>');
    document.getElementById('op-clear')?.addEventListener('click',()=>{Object.keys(state).forEach(k=>state[k]='');paint();});
  }
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar vx-toolbar" role="group" aria-label="Filtres">
      ${OUT.map(b=>`<button class="vx-chip" data-filter-key="decision" data-filter-value="${b}"
        aria-pressed="${state.bucket===b}">${b}</button>`).join('')}
      <select class="vx-select" data-filter-key="sector" style="width:auto" aria-label="Secteur">
        <option value="">Tous secteurs</option>${sectors.map(s=>`<option ${state.sector===s?'selected':''}>${s}</option>`).join('')}</select>
      <input class="vx-input" data-filter-key="setup" style="width:150px" placeholder="setup (BREAKOUT…)" value="${esc(state.setup)}" aria-label="Setup">
    </div>
    <div id="op-table"></div>
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
    const optRow=(c,compact)=>`<tr data-clickable data-ct="${board.indexOf(c)}" tabindex="0" role="button" aria-label="Simuler ${esc(c.sym)} ${VX.fmt.nd(c.strike)}">
        <td data-label="Contrat"><span class="vx-ticker">${c.sym}</span><span class="vx-meta">${VX.fmt.nd(c.strike)} · ${VX.fmt.nd(c.exp)}${c.dte!=null?' · '+VX.fmt.nd(c.dte)+' j':''}</span></td>
        <td data-label="Profil"><span class="vx-badge" style="color:var(--vx-violet)">${catOf(c)}</span></td>
        ${compact?`<td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
        <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.cost)}</td>
        <td data-label="Spread" class="vx-num">${c.spread_pct!=null?c.spread_pct+'%':'—'}</td>
        <td data-label="Qualité" class="vx-num"><b>${VX.fmt.nd(c.quality)}</b></td>
        <td data-label="Action">${rowActions(c.sym)}</td>`:`
        <td data-label="Strike" class="vx-num">${VX.fmt.nd(c.strike)}</td>
        <td data-label="Échéance" class="vx-mono">${VX.fmt.nd(c.exp)}</td>
        <td data-label="DTE" class="vx-num">${VX.fmt.nd(c.dte)}</td>
        <td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
        <td data-label="IV" class="vx-num" style="color:var(--vx-option)">${c.iv!=null?(c.iv*100).toFixed(0)+'%':'—'}</td>
        <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.cost)}</td>
        <td data-label="Spread" class="vx-num">${c.spread_pct!=null?c.spread_pct+'%':'—'}</td>
        <td data-label="Volume" class="vx-num">${VX.fmt.nd(c.vol)}</td>
        <td data-label="OI" class="vx-num">${VX.fmt.nd(c.oi)}</td>
        <td data-label="Breakeven" class="vx-num">${VX.fmt.nd(c.be)}</td>
        <td data-label="R:R" class="vx-num">${VX.fmt.nd(c.p_tgt)}</td>
        <td data-label="Action">${rowActions(c.sym)}</td>`}</tr>`;
    const shortlist=f.slice().sort((a,b)=>{
      const qa=Number(a.quality),qb=Number(b.quality);
      return (Number.isFinite(qb)?qb:-Infinity)-(Number.isFinite(qa)?qa:-Infinity);
    }).slice(0,3);
    $('op-opt-table').innerHTML=f.length?`<section class="vx-card" aria-label="Shortlist options">
      <div class="vx-card-header"><span class="vx-card-title">Shortlist options</span>
        <span class="vx-meta vx-right">${shortlist.length} contrat(s) sur ${f.length}</span></div>
      <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Contrat</th><th>Profil</th><th class="vx-num">Delta</th><th class="vx-num">Prime</th>
        <th class="vx-num">Spread</th><th class="vx-num">Qualité</th><th>Action</th></tr></thead>
        <tbody>${shortlist.map(c=>optRow(c,true)).join('')}</tbody></table></div>
      <div class="vx-card-footer">Sélection analytique uniquement · ouvrir Options pour valider liquidité, payoff et Greeks.</div></section>
      <details class="vx-disclosure vx-mt3" id="op-options-full"><summary>Voir le board complet et les métriques techniques</summary>
        <div class="vx-table-wrap vx-table-cards vx-mt2"><table class="vx-table"><thead><tr>
          <th>Contrat</th><th>Profil</th><th class="vx-num">Strike</th><th>Échéance</th>
          <th class="vx-num">DTE</th><th class="vx-num">Delta</th><th class="vx-num">IV</th>
          <th class="vx-num">Prime</th><th class="vx-num">Spread</th><th class="vx-num">Volume</th>
          <th class="vx-num">OI</th><th class="vx-num">Breakeven</th><th class="vx-num">R:R cible</th><th>Action</th></tr></thead>
          <tbody>${f.map(c=>optRow(c,false)).join('')}</tbody></table></div></details>`
      :VX.states.empty(state.sym?'Aucun contrat pour '+state.sym+' dans le board courant.':'Board options vide — le sélecteur ne force jamais une idée.',
        '<a class="vx-btn vx-btn-sm" href="/system?view=data">Vérifier les données</a>');
    document.querySelectorAll('[data-ct]').forEach(tr=>{
      const open=(e)=>{if(e.target.closest('[data-open-analysis],[data-entity-menu]'))return;openContract(board[+tr.dataset.ct]);};
      tr.addEventListener('click',open);
      tr.addEventListener('keydown',(e)=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(e);}});});
  }
  $('op-body').innerHTML=demoBanner(scan)+`
    <div class="vx-filterbar vx-toolbar">
      ${['BALANCED','DYNAMIC','ULTRA_CONVEX'].map(c=>`<button class="vx-chip" data-filter-key="setup"
        data-filter-value="${c}" aria-pressed="${state.cat===c}">${c}</button>`).join('')}
      <input class="vx-input" data-filter-key="sym" style="width:120px;text-transform:uppercase"
        placeholder="Ticker" value="${esc(state.sym)}" aria-label="Filtrer par ticker">
      <span class="vx-meta">Greeks complets (gamma/theta/vega) : disponibles à la simulation du contrat — le board legacy n'expose que le delta.</span>
    </div>
    <div class="vx-flex vx-toolbar vx-mb2" style="gap:.5rem;flex-wrap:wrap"><button class="vx-btn vx-btn-sm vx-btn-soft" id="op-compare"
      onclick="window.__opCompare&&window.__opCompare((new URLSearchParams(location.search)).get('sym')||'')">
      Comparer 3 contrats (défensif · principal · explosif)</button>
      <a class="vx-btn vx-btn-sm" href="/options">Options Intelligence →</a></div>
    <div id="op-opt-table"></div>
    <div class="vx-card-footer">${VX.updateIndicator(scan.scan_ts||scan.updated,scan.options_source||scan.source,metaMode(scan))}</div>
    <details class="vx-disclosure vx-mt4" id="op-contract" hidden><summary>Simulation détaillée du contrat sélectionné</summary>
      <div class="vx-grid vx-mt3">
        <div class="vx-col-6" id="op-payoff"></div>
        <div class="vx-col-6" id="op-scenarios"></div>
        <div class="vx-col-6" id="op-theta"></div>
        <div class="vx-col-6" id="op-iv"></div>
      </div></details>`;
  document.querySelectorAll('[data-filter-key="setup"]').forEach(c=>c.addEventListener('click',()=>{
    state.cat=state.cat===c.dataset.filterValue?'':c.dataset.filterValue;
    document.querySelectorAll('[data-filter-key="setup"]').forEach(x=>
      x.setAttribute('aria-pressed',String(x.dataset.filterValue===state.cat)));paint();}));
  document.querySelector('[data-filter-key="sym"]').addEventListener('input',function(){state.sym=this.value.toUpperCase();paint();});
  paint();
  async function openContract(c){
    $('op-contract').hidden=false;
    $('op-contract').open=true;
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
      $('op-scenarios').innerHTML='<div class="vx-card">'+VX.states.error('Simulation indisponible.')+'</div>';
      $('op-theta').innerHTML='';$('op-iv').innerHTML='';
    }
  }
}

/* ── ANOMALIES ── */
async function renderAnomalies(){
  const scan=await VX.fetch('/scan',{ttl:120000});
  const rows=(scan.rows||[]).filter(r=>(r.anomalies||[]).length);
  const groupMeta={Actions:'scan courant',Données:'/api/data-quality',Options:'non agrégé ici',
    Volatilité:'non agrégée ici',Portefeuille:'non agrégé ici',Modèles:'non agrégé ici'};
  $('op-body').innerHTML=demoBanner(scan)+`
    <!-- Cette vue portait 879 px de contenu et AUCUN titre : son seul intitule
         etait un <b> nu, la ou les 25 autres vues du produit ouvrent sur un
         titre. Mesure au navigateur — le releve de structure ne trouvait rien
         du tout sur cet onglet, ce qui a d'abord ressemble a une vue vide.
         Meme grammaire d'en-tete que partout ailleurs : titre + orientation. -->
    <div class="vx-page-lead vx-mb3"><h2>Anomalies par source</h2>
      <div class="vx-sub">Une catégorie sans flux consolidé est dite indisponible ; elle n’est jamais déduite depuis une autre métrique.</div></div>
    <div class="vx-filterbar vx-toolbar">${['Actions','Données','Options','Volatilité','Portefeuille','Modèles']
      .map((g,i)=>`<button class="vx-chip" aria-pressed="${i===0}" data-ag="${g}">${g} · ${groupMeta[g]}</button>`).join('')}</div>
    <div id="op-anom"></div>`;
  function paint(group){
    if(group==='Actions'){
      /* LOT 132 : l'intensité n'est plus un chiffre nu — mini-barre de VERRE
         (dégradé warning doux → dense via color-mix, aucun littéral) à côté
         de la valeur ; l'œil classe les anomalies sans lire chaque nombre. */
      const maxI=Math.max.apply(null,[1].concat(rows.map(r=>Number(r.anomaly_score)||0)));
      const ibar=(v)=>{const n=Number(v);if(!isFinite(n))return VX.fmt.nd(v);
        const w=Math.max(4,Math.min(100,n/maxI*100));
        return '<span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">'
          +'<span style="width:64px;height:8px;background:var(--vx-surface-3,#121214);border-radius:3px;overflow:hidden;display:inline-block">'
          +'<span style="display:block;height:100%;width:'+w.toFixed(0)+'%;background:linear-gradient(90deg,color-mix(in srgb,var(--vx-warning,#D9BE3C) 35%,transparent),var(--vx-warning,#D9BE3C));border-radius:3px"></span></span>'
          +'<span style="font-variant-numeric:tabular-nums">'+VX.fmt.nd(n)+'</span></span>';};
      $('op-anom').innerHTML=rows.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Anomalies</th><th class="vx-num">Intensité</th><th class="vx-num">Score</th><th></th></tr></thead><tbody>
        ${rows.slice(0,60).map(r=>`<tr data-clickable data-open-analysis="${r.symbol}">
          <td data-label="Titre"><span class="vx-ticker">${r.symbol}</span></td>
          <td data-label="Anomalies">${(r.anomalies||[]).slice(0,4).map(a=>`<span class="vx-badge vx-warn">${esc(typeof a==='string'?a:(a.code||''))}</span>`).join(' ')}</td>
          <td data-label="Intensité" class="vx-num">${ibar(r.anomaly_score)}</td>
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
      const href=group==='Options'?'/options':group==='Volatilité'?'/options?view=volatility':group==='Portefeuille'?'/portfolio?view=risk':'/system';
      $('op-anom').innerHTML=VX.states.empty(`Aucun flux agrégé « ${group} » n’est fourni à cette vue. Aucun résultat n’est déduit ou inventé.`,
        '<a class="vx-btn vx-btn-sm" href="'+href+'">Ouvrir l’espace source</a>');
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
    /* LOT 132 : imminence — les événements à ≤ 7 jours sont marqués urgent
       (liseré + date warning via timelineCard) ; dte réel pour les earnings,
       écart de dates pour la macro. Aucune donnée inventée. */
    const soonMacro=(dt)=>{const d=(new Date(dt+'T00:00:00')-Date.now())/864e5;return isFinite(d)&&d>=0&&d<=7;};
    const items=[...(cal.macro||[]).map(m=>({when:m.date,kind:m.kind,urgent:soonMacro(m.date),label:esc(m.label)+(m.note?' — '+esc(m.note):'')+(m.approx?' (approx.)':'')})),
      ...(cal.items||[]).map(it=>({when:it.date,kind:'Earnings',sym:it.sym,urgent:it.dte!=null&&it.dte<=7,
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

/* Classement Skyler (X1) : le moteur canonique sur TOUT l'univers scanné.
   Gate plafonnante visible par ligne — jamais masquée. Idempotent (re-boots). */
async function loadSkylerRank(){
  /* LOT 602 (dossier 531-A) : un echec de sweep ne disparait plus en silence —
     la section s affiche avec un etat honnete plutot que de ne pas exister. */
  let d=null,err=null;
  try{d=await VX.fetch('/api/skyler/sweep',{ttl:120000});}catch(e){err=e;}
  document.querySelectorAll('[aria-label="Classement Skyler"]').forEach(n=>n.remove());
  const host=document.createElement('details');
  host.className='vx-disclosure vx-mt3';host.setAttribute('aria-label','Classement Skyler');
  host.id='vx-skyler-rank';
  if(err||!d){
    host.innerHTML='<summary>Expertise avancée · Classement Skyler /40</summary><div class="vx-card vx-mt2">'
      +'<div class="vx-card-header"><span class="vx-card-title">Classement Skyler (/40)</span></div>'
      +VX.states.error('Classement Skyler indisponible')+'</div>';
    $('op-body').appendChild(host);return;}
  if(!d.n){
    host.innerHTML=`<summary>Expertise avancée · Classement Skyler /40</summary><div class="vx-card vx-mt2">
      <div class="vx-card-header"><span class="vx-card-title">Classement Skyler (/40)</span></div>
      ${VX.states.empty(esc((d.reason||'classement indisponible')+'.'))}</div>`;
  }else{
    const tone=x=>x==='ACHETER'||x==='RENFORCER'?'pos':x==='REFUSER'||x==='REDUIRE'?'neg':'neutral';
    /* LOT 136 : le score canonique /40 gagne sa mini-barre de verre graduee
       (patron lot 135) — >= 28 positive, 16-27 warning, < 16 negative. */
    const skBar=(v)=>{const n=Number(v);if(!isFinite(n))return '<b>—</b>/40';
      const tok=n>=28?'var(--vx-positive,#2BBE90)':n>=16?'var(--vx-warning,#D9BE3C)':'var(--vx-negative,#E9555F)';
      return '<span style="display:inline-flex;align-items:center;gap:6px">'
        +'<span style="width:48px;height:7px;background:var(--vx-surface-3,#121214);border-radius:3px;overflow:hidden;display:inline-block">'
        +'<span style="display:block;height:100%;width:'+Math.max(4,Math.min(100,n/40*100)).toFixed(0)+'%;background:linear-gradient(90deg,color-mix(in srgb,'+tok+' 35%,transparent),'+tok+');border-radius:3px"></span></span>'
        +'<span><b>'+n+'</b>/40</span></span>';};
    const rows=(d.rows||[]).map(r=>`<tr>
      <td data-label="Titre"><button class="vx-link" data-open-analysis="${esc(r.symbol)}"><b>${esc(r.symbol)}</b></button></td>
      <td data-label="Décision"><span class="vx-badge" data-tone="${tone(r.decision)}">${esc(r.decision||'—')}</span></td>
      <td data-label="Score" class="vx-num">${skBar(r.score_total)}</td>
      <td data-label="Niveau">${esc(r.level||'—')}</td>
      <td data-label="Gate">${r.capped_by_gate?'<span class="vx-neg" title="décision plafonnée par cette porte">'+VX.icon('close',13)+' '+esc(r.capped_by_gate)+'</span>':'<span class="vx-muted">—</span>'}</td>
      <td data-label="Catalyseur">${esc(r.catalyst||'—')}</td>
      <td data-label="Invalidation" class="vx-num">${r.invalidation!=null?VX.fmt.num(r.invalidation,2):'—'}</td>
    </tr>`).join('');
    host.innerHTML=`<summary>Expertise avancée · Classement Skyler /40</summary><div class="vx-card vx-mt2">
      <div class="vx-card-header"><span class="vx-card-title">Classement Skyler (/40)</span>
      <span class="vx-chart-question">Régime marché partagé : ${esc(d.market_regime||'n/d')} · gates visibles · un score ne déclenche jamais un ordre.</span></div>
      <div class="vx-table-wrap"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Décision</th><th>Score</th><th>Niveau</th><th>Gate</th><th>Catalyseur</th><th>Invalidation</th>
      </tr></thead><tbody>${rows}</tbody></table></div>
      <div class="vx-meta" style="margin-top:.3rem">${d.n} titre(s) · ${esc(d.note||'')}${d.demo?' · DÉMO':''}</div></div>`;
  }
  $('op-body').appendChild(host);
}
const RENDER={radar:async function(){await renderRadar();await loadSkylerRank();},
  stocks:renderStocks,options:renderOptions,
  anomalies:renderAnomalies,calendar:renderCalendar};
async function opFresh(){try{
  const el=document.getElementById('op-fresh');if(!el||!window.VX||!VX.freshness)return;
  let pk=VX.fetch.peek('/api/session/manifest');
  if(!pk){try{await VX.fetch('/api/session/manifest',{ttl:30000});pk=VX.fetch.peek('/api/session/manifest');}catch(e){}}
  const live=!(window.__vxStatus&&window.__vxStatus.demo);
  /* Âge HONNÊTE = ancienneté réelle de la session (manifest.age_s), pas l'âge de
     l'entrée de cache : un manifest resservi doit refléter l'âge de la DONNÉE. */
  const a=(pk&&pk.data&&typeof pk.data.age_s==='number')?pk.data.age_s*1000:null;
  el.innerHTML=VX.freshness.chip(VX.freshness.assess({ageMs:a,live:live}));
}catch(e){}}
function boot(){opFresh();(RENDER[VIEW]||renderRadar)().catch(e=>{
  $('op-body').innerHTML=VX.states.error('Impossible de charger les opportunités.');});}
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
    # `p` ne filtre que les CLÉS : les VALEURS viennent brutes de l'URL et
    # entrent dans un bloc <script>. `json_for_script` interdit la sortie de
    # balise (faille du lot 372).
    js = (_JS.replace('%%VIEW%%', json_for_script(view))
          .replace('%%PARAMS%%', json_for_script(p))
          .replace('%%DEMO_BORDER%%',
                   "(window.__vxStatus&&window.__vxStatus.demo)?VXCharts.colors.warning:'rgba(255,255,255,.25)'"))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Opportunités · {label}', active='opportunities',
                        space_label='Opportunités', sub_label=label,
                        content=content, page_js=js,
                        page_label=f'Opportunités {label}')
