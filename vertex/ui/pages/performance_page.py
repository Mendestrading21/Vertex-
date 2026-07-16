"""vertex.ui.pages.performance_page — l'espace Performance (§27).

Question : « La méthode fonctionne-t-elle et est-elle correctement exécutée ? »
Sous-vues (param ?view=) : overview · journal · track-record · learnings.

Le module Python ne fait AUCUN calcul financier : il assemble le squelette
HTML + le script client. Les seules opérations côté client sont des
agrégations arithmétiques simples (somme, moyenne, ratio) sur les trades
DÉCLARÉS par l'utilisateur (localStorage via VXEntities) — jamais des
indicateurs de marché. Les statistiques moteur viennent de /api/track-record
et restent visuellement séparées des trades réels (« jamais confondus »).
"""
from __future__ import annotations

import html
import re

from vertex.ui.shell import render_shell

_VIEWS = (
    ('overview', 'Vue d’ensemble'),
    ('journal', 'Journal'),
    ('track-record', 'Track record'),
    ('learnings', 'Enseignements'),
)


def _tabs(view: str) -> str:
    """Barre d'onglets — navigation par URL (?view=…), pas d'état JS."""
    items = []
    for vid, label in _VIEWS:
        sel = 'true' if vid == view else 'false'
        items.append(f'<a class="vx-tab" role="tab" href="?view={vid}" '
                     f'aria-selected="{sel}" data-view-tab="{vid}">{label}</a>')
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Performance">'
            + ''.join(items) + '</nav>')


_HEADER = """
<div class="vx-page-header">
  <div><h1>Performance</h1>
  <div class="vx-sub">La méthode fonctionne-t-elle et est-elle correctement exécutée ?</div></div>
</div>
%%TABS%%
"""

_VIEW_CONTENT = {
    'overview': """
<div class="vx-grid vx-mt3" id="vx-pf-kpis" aria-label="Indicateurs de performance"><div class="vx-skeleton vx-skeleton-kpi vx-col-3" style="grid-column:span 3"></div></div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-7" id="vx-pf-equity"></div>
  <div class="vx-col-5" id="vx-pf-drawdown"></div>
</div>
<div class="vx-grid vx-mt4">
  <div class="vx-col-7" id="vx-pf-monthly"></div>
  <div class="vx-col-5" id="vx-pf-dist"></div>
</div>
""",
    'journal': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-8" aria-label="Journal de trading">
    <div class="vx-card-header"><span class="vx-card-title">Journal de trading</span>
      <span class="vx-actions">
        <input class="vx-input" id="vx-pf-filter" data-filter-key="sym" placeholder="Filtrer par ticker"
          value="%%SYM%%" autocomplete="off" style="max-width:160px;text-transform:uppercase" aria-label="Filtrer par ticker" />
        <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-pf-add">Ajouter une entrée</button>
      </span></div>
    <div id="vx-pf-journal">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" aria-label="Statistiques d'erreurs">
    <div class="vx-card-header"><span class="vx-card-title">Erreurs déclarées</span></div>
    <div id="vx-pf-mistakes">%%LOADING%%</div>
  </section>
</div>
""",
    'track-record': """
<div class="vx-mt3 vx-insight" role="note"><b>Deux mondes, jamais confondus.</b>
« Signaux (théorique) » mesure la fiabilité des verdicts du moteur sur données de marché ;
« Trades réels (journal) » reflète uniquement ce que vous avez déclaré avoir exécuté.
Aucun chiffre de l’un n’alimente l’autre.</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Signaux théoriques du moteur">
    <div class="vx-card-header"><span class="vx-card-title">Signaux (théorique) — le moteur se note</span>
      <span class="vx-badge">API moteur</span></div>
    <div id="vx-pf-track">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Trades réels du journal">
    <div class="vx-card-header"><span class="vx-card-title">Trades réels (journal)</span>
      <span class="vx-badge" style="color:var(--vx-cyan,#c8ad8d)">Vos déclarations</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=journal">Ouvrir le journal →</a></span></div>
    <div id="vx-pf-real">%%LOADING%%</div>
  </section>
</div>
""",
    'learnings': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-6" aria-label="Leçons du journal">
    <div class="vx-card-header"><span class="vx-card-title">Leçons retenues</span></div>
    <div id="vx-pf-lessons">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Erreurs récurrentes">
    <div class="vx-card-header"><span class="vx-card-title">Erreurs récurrentes</span></div>
    <div id="vx-pf-recurrent">%%LOADING%%</div>
    <div class="vx-card-footer">
      <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/intelligence?view=memory">Règles proposées (Intelligence / Mémoire) →</a>
    </div>
  </section>
</div>
""",
}

_JS = r"""
<script src="/static/vertex/js/charts/equity-chart.js" defer></script>
<script src="/static/vertex/js/charts/drawdown-chart.js" defer></script>
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW='%%VIEW%%';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function trades(){/* entrées du journal avec un résultat déclaré et un P&L numérique */
  return (E()?E().journal():[]).filter(e=>(e.result==='WIN'||e.result==='LOSS')&&isFinite(Number(e.pnl)));
}
/* Agrégations arithmétiques simples sur les trades DÉCLARÉS (pas des indicateurs de marché). */
function stats(list){
  const pnls=list.map(e=>Number(e.pnl));
  const wins=pnls.filter(p=>p>0),losses=pnls.filter(p=>p<0);
  const gains=wins.reduce((a,b)=>a+b,0),pertes=Math.abs(losses.reduce((a,b)=>a+b,0));
  const avgWin=wins.length?gains/wins.length:null,avgLoss=losses.length?-(pertes/losses.length):null;
  /* Drawdown max chiffré : plus grand repli du cumul de P&L (ordre chronologique). */
  let maxDD=0;{let cum=0,peak=0;list.slice().sort((a,b)=>String(a.date||'').localeCompare(String(b.date||'')))
    .forEach(e=>{cum+=Number(e.pnl)||0;peak=Math.max(peak,cum);maxDD=Math.min(maxDD,cum-peak);});}
  return {n:list.length,
    total:pnls.reduce((a,b)=>a+b,0),
    winRate:list.length?100*list.filter(e=>e.result==='WIN').length/list.length:null,
    profitFactor:pertes>0?gains/pertes:(gains>0?Infinity:null),
    expectancy:pnls.length?pnls.reduce((a,b)=>a+b,0)/pnls.length:null,
    avgWin:avgWin,avgLoss:avgLoss,
    ratio:(avgWin!=null&&avgLoss)?avgWin/Math.abs(avgLoss):null,
    best:pnls.length?Math.max.apply(null,pnls):null,
    worst:pnls.length?Math.min.apply(null,pnls):null,
    maxDD:maxDD};
}
const JOURNAL_ACTION='<a class="vx-btn vx-btn-sm" href="/performance?view=journal">Ouvrir le journal</a>';
function emptyCard(host,reason,action){
  const el=$(host);if(el)el.innerHTML='<div class="vx-card">'+VX.states.empty(reason,action||'')+'</div>';
}

/* Anneau de progression (§39) — n/max trades clôturés. SVG pur, sur tokens. */
function progressRing(n,max){
  var frac=Math.max(0,Math.min(1,max?n/max:0)),R=46,C=2*Math.PI*R;
  var col=frac>=1?'var(--vx-positive)':'var(--vx-brand)';
  return '<svg viewBox="0 0 120 120" style="width:132px;height:132px" role="img" aria-label="'+n+' sur '+max+' trades clôturés">'
    +'<circle cx="60" cy="60" r="'+R+'" fill="none" stroke="var(--vx-surface-3)" stroke-width="10"/>'
    +'<circle cx="60" cy="60" r="'+R+'" fill="none" stroke="'+col+'" stroke-width="10" stroke-linecap="round" stroke-dasharray="'+(frac*C).toFixed(1)+' '+C.toFixed(1)+'" transform="rotate(-90 60 60)"/>'
    +'<text x="60" y="57" text-anchor="middle" font-size="32" font-weight="800" fill="var(--vx-text-primary)" style="font-variant-numeric:tabular-nums">'+n+'</text>'
    +'<text x="60" y="78" text-anchor="middle" font-size="12" fill="var(--vx-text-muted)">/ '+max+' trades</text></svg>';
}
/* Aperçu FANTÔME de la courbe d'équité (§39) — forme déterministe, AUCUN chiffre :
   fait sentir le produit à venir sans jamais afficher de fausse performance. */
function ghostEquity(){
  var pts='M0 95 L60 88 L120 92 L180 70 L240 74 L300 52 L360 58 L420 34';
  return '<div style="position:relative;margin-bottom:6px"><svg viewBox="0 0 420 120" preserveAspectRatio="none" style="width:100%;height:118px;opacity:.55" aria-hidden="true">'
    +'<defs><linearGradient id="pfghost" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--vx-brand)" stop-opacity=".22"/><stop offset="1" stop-color="var(--vx-brand)" stop-opacity="0"/></linearGradient></defs>'
    +'<path d="'+pts+' L420 120 L0 120 Z" fill="url(#pfghost)"/><path d="'+pts+'" fill="none" stroke="var(--vx-brand)" stroke-width="2" stroke-dasharray="4 5" stroke-linejoin="round"/></svg>'
    +'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><span class="vx-meta" style="background:var(--vx-surface-1);padding:4px 11px;border-radius:999px;border:1px solid var(--vx-border-soft)">Ta courbe d&#8217;équité apparaîtra ici</span></div></div>';
}

/* ═══ OVERVIEW ═══ */
function loadKpis(){
  const list=trades();
  if(list.length<5){
    const n=list.length;
    const milestones=[[5,'P&L, taux de réussite, profit factor, espérance'],
      [10,'Distribution gains/pertes, meilleurs & pires trades'],
      [20,'Courbe d’équité vs SPY, drawdown, MAE / MFE'],
      [30,'Rolling win rate & expectancy, perf par setup / régime']];
    const pct=Math.min(100,Math.round(n/5*100));
    const rows=milestones.map(function(m){const done=n>=m[0];
      return `<div class="vx-kv"><span class="k">${done?'✅':'🔒'} ${m[0]} trades</span>`
        +`<span class="v vx-dim" style="font-size:12px;text-align:right">${esc(m[1])}</span></div>`;}).join('');
    $('vx-pf-kpis').innerHTML=`<div class="vx-card vx-col-12">
      <div class="vx-card-header"><span class="vx-card-title">Construis ton track record</span>
        <span class="vx-meta vx-right">${n} / 5 trades pour débloquer les premières statistiques</span></div>
      <div class="vx-grid">
        <div class="vx-col-4" style="display:flex;align-items:center;justify-content:center;padding:6px 0">${progressRing(n,5)}</div>
        <div class="vx-col-8">${ghostEquity()}<div class="vx-mt1">${rows}</div></div>
      </div>
      <div class="vx-help vx-mt3">Chaque trade clôturé (WIN/LOSS + P&amp;L) débloque des analyses. Aucune fausse performance n’est affichée avant d’avoir des données réelles — la méthode se juge sur des faits, pas des estimations.</div>
      <div class="vx-flex vx-mt3" style="gap:.5rem;flex-wrap:wrap">
        <a class="vx-btn vx-btn-sm vx-btn-primary" href="/performance?view=journal">Ajouter une entrée au journal</a>
        <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio?view=positions">Voir mes positions</a></div>
    </div>`;
    return list;
  }
  const s=stats(list);
  const pf=s.profitFactor===Infinity?'∞':(s.profitFactor===null?'—':VX.fmt.num(s.profitFactor,2));
  const cells=[
    ['P&L total (déclaré)',(s.total>=0?'+':'')+VX.fmt.num(s.total,0)+' $',s.total>=0?'vx-pos':'vx-neg'],
    ['Taux de réussite',VX.fmt.num(s.winRate,0)+' %',s.winRate>=50?'vx-pos':'vx-neg'],
    ['Profit factor',pf,(s.profitFactor||0)>=1?'vx-pos':'vx-neg'],
    ['Espérance / trade',(s.expectancy>=0?'+':'')+VX.fmt.num(s.expectancy,0)+' $',s.expectancy>=0?'vx-pos':'vx-neg'],
    ['Gain moyen',s.avgWin!=null?'+'+VX.fmt.num(s.avgWin,0)+' $':'—','vx-pos'],
    ['Perte moyenne',s.avgLoss!=null?VX.fmt.num(s.avgLoss,0)+' $':'—','vx-neg'],
    ['Ratio gain/perte',s.ratio!=null?VX.fmt.num(s.ratio,2):'—',(s.ratio||0)>=1?'vx-pos':'vx-neg'],
    ['Drawdown max',s.maxDD<0?VX.fmt.num(s.maxDD,0)+' $':'—','vx-neg'],
    ['Meilleur / pire',(s.best!=null?((s.best>=0?'+':'')+VX.fmt.num(s.best,0)):'—')+' / '+(s.worst!=null?VX.fmt.num(s.worst,0):'—')+' $','vx-muted'],
    ['Trades déclarés',String(s.n),'vx-muted'],
  ];
  $('vx-pf-kpis').innerHTML=cells.map(([label,val,cls])=>{
    const tone=cls==='vx-pos'?'pos':cls==='vx-neg'?'neg':'';
    return `<div class="vx-stat" style="grid-column:span 2" data-tone="${tone}" aria-label="${esc(label)}">
      <div class="vx-stat-k">${label}</div>
      <div class="vx-stat-v">${val}</div>
      <div class="vx-stat-sub">journal local · vos déclarations</div></div>`;}).join('')
    +`<div class="vx-stat" style="grid-column:span 2">
      <div class="vx-stat-k">Source</div>
      <div class="vx-meta" style="font-size:11.5px;margin-top:5px;line-height:1.4">Calculs arithmétiques sur VOS trades déclarés — aucun indicateur de marché.</div></div>`;
  return list;
}
/* Équité DÉRIVÉE du cumul des P&L de clôture déclarés (le stock myTradesEquity
   n'est jamais alimenté par recordExit — s'y fier laissait la courbe vide). Base
   = capital déclaré si présent, sinon 0 (courbe de P&L cumulé). Réel, arithmétique. */
function derivedEquity(){
  const cl=trades().slice().filter(e=>e.date).sort((a,b)=>String(a.date).localeCompare(String(b.date)));
  if(cl.length<2)return [];
  const base=(E()&&E().capital&&E().capital())||0;
  let cum=base;const eq=[];
  cl.forEach(e=>{cum+=Number(e.pnl)||0;eq.push({d:e.date,v:Math.round(cum*100)/100});});
  return eq;
}
function loadEquity(){
  const eq=derivedEquity();
  if(eq.length>=2){
    /* equity-chart.js / drawdown-chart.js sont des scripts `defer` : garde-fou
       si loadEquity court avant leur enregistrement (évite « equityCard is not a
       function ») — on retente une fois tous les scripts chargés. */
    if(!(window.VXCharts&&VXCharts.equityCard&&VXCharts.drawdownCard)){
      window.addEventListener('load',loadEquity,{once:true});return;}
    const labels=eq.map(p=>p.d),values=eq.map(p=>Number(p.v));
    VXCharts.equityCard('vx-pf-equity',{
      title:'Courbe d’équité (déclarée)',timeframe:eq.length+' points',
      question:'Le capital déclaré progresse-t-il régulièrement ?',
      conclusion:values[values.length-1]>=values[0]?'Équité en progression sur la période.':'Équité en retrait sur la période.',
      labels,values,height:240,
      source:'journal local (cumul des clôtures)',timestamp:Date.now(),mode:'delayed',
      explain:{shows:'La série d’équité issue de vos clôtures de positions déclarées.',
        why:'Une méthode saine produit une pente régulière, pas des à-coups.',
        confirm:'Nouveaux plus hauts d’équité avec drawdowns contenus.',
        invalidate:'Série de plus bas d’équité — réduire la taille et revoir le process.'}});
    VXCharts.drawdownCard('vx-pf-drawdown',{
      title:'Drawdown depuis les pics',
      question:'Les pertes restent-elles contrôlées ?',
      conclusion:'Dérivé arithmétiquement de la courbe d’équité déclarée.',
      labels,values,height:240,
      source:'journal local (cumul des clôtures)',timestamp:Date.now(),mode:'delayed',
      limits:'dérivé de la série déclarée — pas un indicateur de marché',
      explain:{shows:'L’écart en % entre l’équité et son dernier pic.',
        why:'La profondeur des drawdowns mesure la discipline de risque réelle.',
        confirm:'Drawdowns courts et peu profonds.',invalidate:'Drawdown qui s’aggrave pendant que vous continuez à trader.'}});
  }else{
    emptyCard('vx-pf-equity','Courbe d’équité indisponible — elle se construit au fil des clôtures de positions déclarées.',JOURNAL_ACTION);
    emptyCard('vx-pf-drawdown','Drawdown indisponible sans courbe d’équité.');
  }
}
/* Heatmap mensuelle + distribution — agrégations arithmétiques sur VOS
   clôtures déclarées (jamais un indicateur de marché). */
function loadMonthlyAndDist(){
  /* Cartes issues de scripts `defer` (heatmap.js) : garde-fou tant qu'ils ne sont
     pas enregistrés (évite un TypeError si l'orchestration court trop tôt). */
  if(!(window.VXCharts&&VXCharts.heatmapCard&&VXCharts.card&&VXCharts.bars)){
    window.addEventListener('load',loadMonthlyAndDist,{once:true});return;}
  /* pnl_pct n'est jamais écrit par recordExit → le calculer depuis (exit−cost)/cost
     (données réelles des clôtures déclarées). Sinon le filtre restait toujours vide. */
  const closed=(E()?E().closedPositions():[])||[];
  const withPl=closed.filter(t=>t.closed&&t.cost).map(t=>Object.assign({},t,
    {pnl_pct:Math.round((t.exit-t.cost)/t.cost*1000)/10}));
  if(withPl.length<3){
    emptyCard('vx-pf-monthly','Heatmap mensuelle disponible à partir de 3 clôtures datées.',JOURNAL_ACTION);
    emptyCard('vx-pf-dist','Distribution disponible à partir de 3 clôtures.');
    return;
  }
  const byMonth={};
  withPl.forEach(t=>{const m=String(t.closed).slice(0,7);
    (byMonth[m]=byMonth[m]||[]).push(Number(t.pnl_pct));});
  const months=Object.keys(byMonth).sort();
  const years=[...new Set(months.map(m=>m.slice(0,4)))];
  const MN=['01','02','03','04','05','06','07','08','09','10','11','12'];
  const ML=['J','F','M','A','M','J','J','A','S','O','N','D'];
  VXCharts.heatmapCard('vx-pf-monthly',{
    title:'P&L moyen par mois (clôtures déclarées)',
    question:'Y a-t-il des périodes où la méthode sur- ou sous-performe ?',
    conclusion:months.length+' mois avec clôtures · moyenne simple des % par trade.',
    columns:ML,
    rows:years.map(y=>({label:y,cells:MN.map(mm=>{
      const arr=byMonth[y+'-'+mm];
      return arr?{value:arr.reduce((a,b)=>a+b,0)/arr.length,
        title:arr.length+' clôture(s)'}:{value:null,label:'·'};})})),
    min:-8,max:8,fmt:(v)=>v===null?'·':VX.fmt.pct(v,1),
    source:'journal local (clôtures)',timestamp:Date.now(),mode:'delayed',
    limits:'moyenne des % par trade — pas une performance composée'});
  const buckets=[[-1e9,-20],[-20,-10],[-10,-5],[-5,0],[0,5],[5,10],[10,20],[20,50],[50,1e9]];
  const labels=['<-20','-20/-10','-10/-5','-5/0','0/+5','+5/+10','+10/+20','+20/+50','>+50'];
  const counts=buckets.map(([a,b])=>withPl.filter(t=>t.pnl_pct>=a&&t.pnl_pct<b).length);
  VXCharts.card('vx-pf-dist',{
    title:'Distribution des rendements par trade',
    question:'Le profil est-il asymétrique (petites pertes, gains amples) ?',
    conclusion:withPl.length+' clôtures · l’asymétrie droite valide la gestion.',
    height:220,source:'journal local (clôtures)',timestamp:Date.now(),mode:'delayed',
    explain:{shows:'Le décompte de vos trades clôturés par tranche de rendement (%).',
      why:'La stratégie vise des pertes tronquées (stops) et des gains étendus (TP échelonnés).',
      confirm:'Masse des pertes concentrée entre 0 et −10 %, queue droite étendue.',
      invalidate:'Queue gauche épaisse — les stops ne sont pas respectés.'},
    render:(cv)=>VXCharts.bars(cv,labels,counts,
      {colors:buckets.map(([a])=>a<0?VXCharts.colors.negative:VXCharts.colors.positive)})});
}

/* ═══ JOURNAL ═══ */
function currentFilter(){return ($('vx-pf-filter')?$('vx-pf-filter').value:'').trim().toUpperCase();}
function loadJournal(){
  const all=(E()?E().journal():[]).slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
  const f=currentFilter();
  const list=f?all.filter(e=>String(e.ticker||'').toUpperCase().includes(f)):all;
  if(!list.length){
    $('vx-pf-journal').innerHTML=VX.states.empty(
      f?('Aucune entrée de journal pour « '+esc(f)+' ».'):'Journal vide — déclarez vos trades pour mesurer votre exécution.',
      '<button class="vx-btn vx-btn-sm" id="vx-pf-add-empty">Ajouter une entrée</button>');
    $('vx-pf-add-empty')?.addEventListener('click',openEntryModal);
    return;
  }
  $('vx-pf-journal').innerHTML=
    `<table class="vx-table"><thead><tr><th>Date</th><th>Ticker</th><th>Direction</th>
     <th>Résultat</th><th class="vx-num">P&amp;L</th><th>Leçon</th><th></th></tr></thead><tbody>`
    +list.map(e=>{
      const pnl=Number(e.pnl);
      return `<tr>
        <td class="vx-mono vx-meta">${esc(e.date||'—')}</td>
        <td><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(e.ticker||'')}">${esc(e.ticker||'—')}</button></td>
        <td>${esc(e.dir||'—')}${e.auto?' <span class="vx-badge">auto</span>':''}</td>
        <td>${e.result==='WIN'?'<span class="vx-badge vx-pos">WIN</span>':e.result==='LOSS'?'<span class="vx-badge vx-neg">LOSS</span>':'—'}</td>
        <td class="vx-num vx-mono ${pnl>0?'vx-pos':pnl<0?'vx-neg':'vx-muted'}">${isFinite(pnl)?(pnl>0?'+':'')+VX.fmt.num(pnl,0)+' $':'—'}</td>
        <td class="vx-dim" style="font-size:12px;max-width:260px">${esc(e.lesson||'')}</td>
        <td><button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${esc(e.ticker||'')}" aria-label="Actions ${esc(e.ticker||'')}">⋯</button></td>
      </tr>`;}).join('')+'</tbody></table>'
    +`<div class="vx-card-footer">${list.length} entrée(s)${f?' (filtre : '+esc(f)+')':''} · journal local synchronisé desk</div>`;
}
function loadMistakes(){
  const all=E()?E().journal():[];
  const counts={};
  all.forEach(e=>{const m=String(e.mistake||'').trim();if(m)counts[m]=(counts[m]||0)+1;});
  const top=Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  $('vx-pf-mistakes').innerHTML=top.length?top.map(([m,n])=>
    `<div class="vx-kv"><span class="k">${esc(m)}</span><span class="v vx-mono">× ${n}</span></div>`).join('')
    :VX.states.empty('Aucune erreur déclarée dans le journal — renseignez le champ « erreur » à chaque sortie perdante.');
}
function openEntryModal(){
  const field=(id,label,type,ph)=>`<div class="vx-field"><label for="${id}">${label}</label>
    <input class="vx-input" id="${id}" type="${type||'text'}" ${type==='number'?'step="any"':''} placeholder="${ph||''}" autocomplete="off" /></div>`;
  const body=`
    <div class="vx-form-row">${field('j-ticker','Ticker','text','ex. NVDA')}
      <div class="vx-field"><label for="j-dir">Direction</label>
        <select class="vx-select" id="j-dir"><option value="LONG">LONG</option><option value="SHORT">SHORT</option></select></div></div>
    <div class="vx-field"><label for="j-reason">Raison d’entrée</label>
      <input class="vx-input" id="j-reason" placeholder="setup, catalyseur…" autocomplete="off" /></div>
    <div class="vx-form-row">${field('j-entry','Entrée','number')}${field('j-stop','Stop','number')}</div>
    <div class="vx-form-row">${field('j-tp','Objectif (TP)','number')}
      <div class="vx-field"><label for="j-result">Résultat</label>
        <select class="vx-select" id="j-result"><option value="">— en cours —</option>
        <option value="WIN">WIN</option><option value="LOSS">LOSS</option></select></div></div>
    <div class="vx-form-row">${field('j-exit','Sortie','number')}${field('j-pnl','P&amp;L ($)','number')}</div>
    <div class="vx-field"><label for="j-lesson">Leçon</label>
      <input class="vx-input" id="j-lesson" placeholder="ce que ce trade enseigne" autocomplete="off" /></div>
    <div class="vx-form-row">${field('j-mistake','Erreur commise (si perte)','text','ex. entrée sans confirmation')}
      ${field('j-emo','État émotionnel','text','calme, FOMO…')}</div>
    <div class="vx-help">Registre déclaratif — Vertex n’envoie JAMAIS un ordre.</div>`;
  VX.shell.openModal('Ajouter une entrée de journal',body,
    '<button class="vx-btn vx-btn-primary" id="j-confirm">Enregistrer</button>');
  $('j-confirm')?.addEventListener('click',()=>{
    const v=(id)=>$(id)?.value?.trim()||'';
    const n=(id)=>{const x=v(id);return x===''?null:Number(x);};
    const ticker=v('j-ticker').toUpperCase();
    if(!/^[A-Z.\-]{1,7}$/.test(ticker)){VX.toast('Ticker invalide','error');return;}
    const result=v('j-result');
    if(result&&n('j-pnl')===null){VX.toast('P&L requis quand un résultat est déclaré','error');return;}
    E().addJournalEntry({ticker,dir:v('j-dir'),reason:v('j-reason'),
      entry:n('j-entry'),stop:n('j-stop'),tp:n('j-tp'),
      result:result||'',exit:n('j-exit'),pnl:n('j-pnl'),
      lesson:v('j-lesson'),mistake:v('j-mistake'),emo:v('j-emo')});
    VX.shell.closeModal();
    loadJournal();loadMistakes();
  });
  $('j-ticker')?.focus();
}

/* ═══ TRACK RECORD ═══ */
async function loadTrack(){
  try{
    const tr=await VX.fetch('/api/track-record',{ttl:120000});
    const by=tr.by_verdict||{};
    const rows=Object.entries(by);
    if(!rows.length){
      $('vx-pf-track').innerHTML=VX.states.empty(
        'Pas encore assez de verdicts résolus pour mesurer la fiabilité ('+(tr.entries||0)
        +' verdict(s) enregistré(s), '+(tr.resolved||0)+' résolu(s) — minimum 5 par verdict). Le registre se remplit à chaque scan.',
        '<a class="vx-btn vx-btn-sm" href="/system?view=data">Système / Données</a>');
      return;
    }
    $('vx-pf-track').innerHTML=
      `<div id="vx-pf-track-bar" class="vx-mb3"></div>`
      +`<table class="vx-table"><thead><tr><th>Verdict moteur</th><th class="vx-num">N</th>
       <th class="vx-num">Rdt +5 séances</th><th class="vx-num">Rdt +20 séances</th>
       <th class="vx-num">% gagnants +5 s</th><th class="vx-num">TP1 avant stop</th></tr></thead><tbody>`
      +rows.map(([verdict,s])=>`<tr>
        <td><b>${esc(verdict)}</b></td>
        <td class="vx-num vx-mono">${VX.fmt.nd(s.n)}</td>
        <td class="vx-num vx-mono ${s.avg_5j>0?'vx-pos':s.avg_5j<0?'vx-neg':'vx-muted'}">${s.avg_5j===null||s.avg_5j===undefined?'—':VX.fmt.pct(s.avg_5j)}</td>
        <td class="vx-num vx-mono ${s.avg_20j>0?'vx-pos':s.avg_20j<0?'vx-neg':'vx-muted'}">${s.avg_20j===null||s.avg_20j===undefined?'—':VX.fmt.pct(s.avg_20j)}</td>
        <td class="vx-num vx-mono">${s.win_5j===null||s.win_5j===undefined?'—':VX.fmt.num(s.win_5j,0)+' %'}</td>
        <td class="vx-num vx-mono">${s.tp1_rate===null||s.tp1_rate===undefined?'—':VX.fmt.num(s.tp1_rate,0)+' % ('+s.tp1_resolved+')'}</td>
      </tr>`).join('')+'</tbody></table>'
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'moteur track-record','delayed')}
        <span class="vx-meta">${esc(tr.note||'')}${tr.as_of?' · au '+esc(tr.as_of):''}</span></div>`;
    /* Aperçu graphique du rendement moyen +20 séances par verdict (au-dessus du tableau
       détaillé qui garde N, %gagnants, TP1). Données réelles du moteur — null exclu. */
    try{
      const _tl=rows.map(([v])=>v),_tv=rows.map(([,s])=>(s.avg_20j==null?null:s.avg_20j));
      if(window.VXCharts&&VXCharts.card&&VXCharts.bars&&_tv.some(x=>x!=null)){
        VXCharts.card('vx-pf-track-bar',{title:'Rendement moyen +20 séances par verdict',
          question:'Quels verdicts moteur ont le mieux tenu ?',height:200,
          source:'moteur track-record',timestamp:Date.now(),mode:'delayed',
          limits:'moyenne réelle des verdicts résolus (n≥5) — mesure, pas une promesse',
          render:(cv)=>VXCharts.bars(cv,_tl,_tv,{colors:_tv.map(v=>v==null?'#8f8a83':(v>=0?'#36c889':'#ed655c')),yFmt:(x)=>x+' %'})});
      }
    }catch(e){}
  }catch(e){$('vx-pf-track').innerHTML=VX.states.error('Track record moteur indisponible ('+esc(e.message)+')');}
}
function loadReal(){
  const list=trades();
  if(!list.length){
    $('vx-pf-real').innerHTML=VX.states.empty('Aucun trade réel déclaré avec résultat — le journal est la seule source de cette section.',JOURNAL_ACTION);
    return;
  }
  const s=stats(list);
  const pf=s.profitFactor===Infinity?'∞':(s.profitFactor===null?'—':VX.fmt.num(s.profitFactor,2));
  $('vx-pf-real').innerHTML=
    `<table class="vx-table"><thead><tr><th class="vx-num">Trades</th><th class="vx-num">Taux de réussite</th>
     <th class="vx-num">P&amp;L total</th><th class="vx-num">Profit factor</th><th class="vx-num">Espérance / trade</th></tr></thead>
     <tbody><tr>
       <td class="vx-num vx-mono">${s.n}</td>
       <td class="vx-num vx-mono">${VX.fmt.num(s.winRate,0)} %</td>
       <td class="vx-num vx-mono ${s.total>=0?'vx-pos':'vx-neg'}">${(s.total>=0?'+':'')+VX.fmt.num(s.total,0)} $</td>
       <td class="vx-num vx-mono">${pf}</td>
       <td class="vx-num vx-mono ${s.expectancy>=0?'vx-pos':'vx-neg'}">${(s.expectancy>=0?'+':'')+VX.fmt.num(s.expectancy,0)} $</td>
     </tr></tbody></table>
     <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'journal local (vos déclarations)','delayed')}
       <span class="vx-meta">agrégations arithmétiques sur vos trades déclarés — indépendant des signaux moteur</span></div>`;
}

/* ═══ LEARNINGS ═══ */
function loadLearnings(){
  const all=E()?E().journal():[];
  const lessons=[...new Set(all.map(e=>String(e.lesson||'').trim()).filter(Boolean))];
  $('vx-pf-lessons').innerHTML=lessons.length?
    '<ul style="margin:0;padding-left:18px;line-height:1.9">'+lessons.map(l=>`<li>${esc(l)}</li>`).join('')+'</ul>'
    :VX.states.empty('Aucune leçon consignée — renseignez le champ « leçon » à chaque sortie de trade.',JOURNAL_ACTION);
  const counts={};
  all.forEach(e=>{const m=String(e.mistake||'').trim();if(m)counts[m]=(counts[m]||0)+1;});
  const top=Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  $('vx-pf-recurrent').innerHTML=top.length?top.map(([m,n])=>
    `<div class="vx-kv"><span class="k">${esc(m)}</span><span class="v vx-mono">× ${n}</span></div>`).join('')
    :VX.states.empty('Aucune erreur récurrente déclarée pour l’instant.');
}

/* ═══ Orchestration ═══ */
function boot(){
  if(VIEW==='overview'){loadKpis();loadEquity();loadMonthlyAndDist();}
  else if(VIEW==='journal'){
    loadJournal();loadMistakes();
    $('vx-pf-add')?.addEventListener('click',openEntryModal);
    $('vx-pf-filter')?.addEventListener('input',loadJournal);
  }
  else if(VIEW==='track-record'){loadTrack();loadReal();}
  else if(VIEW==='learnings'){loadLearnings();}
}
function whenReady(fn){
  if(window.VXEntities&&(VIEW!=='overview'||(window.VXCharts&&window.Chart)))return fn();
  window.addEventListener('load',fn,{once:true});
}
whenReady(boot);
VX.bus.on('vx:data-refreshed',()=>whenReady(boot));
})();
</script>
"""


def render(view: str = 'overview', params: dict | None = None) -> str:
    """Assemble la page Performance pour la sous-vue demandée (URL = état).

    params : arguments d'URL (ex. request.args) — seul ``sym`` est utilisé,
    pour pré-appliquer le filtre du journal. Validé/échappé, jamais interprété.
    """
    if view not in dict(_VIEWS):
        view = 'overview'
    label = dict(_VIEWS)[view]
    sym = ''
    if params:
        raw = str(params.get('sym') or '').strip().upper()
        if re.fullmatch(r'[A-Z.\-]{1,7}', raw):
            sym = raw
    content = (_HEADER.replace('%%TABS%%', _tabs(view))
               + _VIEW_CONTENT[view])
    content = content.replace('%%SYM%%', html.escape(sym)).replace(
        '%%LOADING%%', '<div class="vx-skeleton" style="height:60px"></div>')
    page_js = _JS.replace('%%VIEW%%', view)
    return render_shell(title='Performance', active='performance',
                        space_label='Performance', sub_label=label,
                        content=content, page_js=page_js,
                        page_label='Performance')
