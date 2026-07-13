"""vertex.ui.pages.briefing — le cockpit (§20-22).

Question : « Que dois-je comprendre et surveiller aujourd'hui ? »
Composition §20 : Brief Vertex (8) + Régime (4) · Market strip · graphique
marché (8) + breadth (4) · opportunités actions (6) + options (6) · rotation
(7) + alertes (5) · portefeuille (7) + calendrier (5).
"""
from __future__ import annotations

import time

from vertex.ui.shell import render_shell


# ── Brief Vertex éditorial (§21) — paquet structuré → ~10 lignes ────────
def build_editorial(scan_state: dict) -> dict:
    """Brief déterministe composé UNIQUEMENT depuis les données moteur.

    Si la couche IA est disponible elle peut reformuler ce même paquet ;
    sinon ce texte déterministe est servi tel quel. Jamais de texte générique
    sans rapport avec les données.
    """
    m = scan_state.get('market') or scan_state.get('market_ctx') or {}
    sectors = scan_state.get('sectors') or []
    committee = scan_state.get('committee') or {}
    counts = committee.get('counts') or {}
    rows = scan_state.get(' rows') or scan_state.get('rows') or []
    source = scan_state.get('source') or 'aucune'
    lines: list[str] = []
    missing: list[str] = []

    regime = m.get('spy_regime') or m.get('regime')
    roro = m.get('roro')
    if regime or roro:
        lines.append(f"Régime : {regime or 'n/d'}"
                     + (f" · {roro}" if roro else '') + '.')
    else:
        missing.append('régime')
    idx = scan_state.get('indices') or []
    by_name = {i.get('name'): i for i in idx if isinstance(i, dict)} \
        if isinstance(idx, list) else {}
    parts = []
    for name in ('S&P 500', 'Nasdaq'):
        entry = by_name.get(name) or {}
        if entry.get('change') is not None:
            parts.append(f"{name} {entry['change']:+.1f} %")
    if parts:
        lines.append('Indices : ' + ' · '.join(parts) + '.')
    vix = m.get('vix')
    if vix is not None:
        band = m.get('vix_band') or ''
        lines.append(f'Volatilité : VIX {vix}' + (f' ({band})' if band else '') + '.')
    else:
        missing.append('volatilité')
    breadth = m.get('breadth')
    if breadth is not None:
        lines.append(f'Breadth : {breadth} % des leaders au-dessus de leur moyenne — '
                     + ('participation saine.' if breadth >= 55 else
                        'participation étroite, sélectivité obligatoire.'))
    if sectors:
        top = sectors[0] if isinstance(sectors[0], dict) else None
        weak = sectors[-1] if len(sectors) > 1 and isinstance(sectors[-1], dict) else None
        if top:
            lines.append(f"Secteur leader : {top.get('sector', 'n/d')} "
                         f"(score {top.get('avg_score', 'n/d')}).")
        if weak and weak is not top:
            lines.append(f"Secteur faible : {weak.get('sector', 'n/d')}.")
    if counts:
        lines.append(f"Comité : {counts.get('ACHETER', 0)} achat(s) possibles, "
                     f"{counts.get('ATTENDRE', 0)} en attente, "
                     f"{counts.get('ÉVITER', counts.get('EVITER', 0))} à éviter.")
    decisions = committee.get('decisions') or []
    prio = next((d for d in decisions if d.get('verdict') in ('ACHETER', 'RENFORCER')), None)
    if prio:
        lines.append(f"Opportunité prioritaire : {prio.get('symbol')} — vérifier le dossier complet avant toute décision.")
    lines.append('Discipline du jour : aucune improvisation — fondamental avant '
                 'technique, décision finale unique, stops dérivés du sous-jacent.')

    changed = scan_state.get('daily_changes') or []
    return {
        'lines': lines[:12],
        'word_count': sum(len(l.split()) for l in lines[:12]),
        'changed_since_yesterday': changed[:3] if isinstance(changed, list) else [],
        'as_of': scan_state.get('updated') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'sources': [source],
        'generator': 'deterministic',
        'missing': missing,
        'demo': source == 'demo',
    }


_CONTENT = """
<div class="vx-page-header">
  <div><h1>Briefing</h1>
  <div class="vx-sub">Que dois-je comprendre et surveiller aujourd’hui ?</div></div>
  <div class="vx-actions">
    <button class="vx-btn vx-btn-sm vx-btn-ghost" id="vx-customize-btn">Personnaliser</button>
    <div class="vx-segmented" role="group" aria-label="Densité">
      <button data-density-btn="compact" aria-pressed="false">Compact</button>
      <button data-density-btn="confort" aria-pressed="true">Confort</button>
      <button data-density-btn="dense" aria-pressed="false">Dense</button>
    </div>
  </div>
</div>
<div id="vx-demo-banner"></div>

<!-- Rangée 1 (§18) : Brief Vertex hero (8) + Régime (4) -->
<div class="vx-grid">
  <section class="vx-card vx-card--hero vx-col-8" id="vx-brief" data-block="brief" aria-label="Brief Vertex">
    <div class="vx-card-header"><span class="vx-card-title">Brief Vertex</span>
      <span class="vx-actions" id="vx-brief-meta"></span></div>
    <div id="vx-brief-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" id="vx-regime" data-block="regime" aria-label="Régime de marché">
    <div class="vx-card-header"><span class="vx-card-title">Régime de marché</span></div>
    <div id="vx-regime-body">%%LOADING%%</div>
  </section>
</div>

<!-- Rangée 2 : indices & marchés -->
<div class="vx-grid vx-mt4" id="vx-market-strip" aria-label="Indices et marchés"></div>

<!-- Rangée 3 : marché (8) + breadth (4) -->
<div class="vx-grid vx-mt4" data-block="market">
  <div class="vx-col-8" id="vx-market-chart"></div>
  <div class="vx-col-4" id="vx-breadth-chart"></div>
</div>

<!-- Rangée 3b : Top 10 / Flop 10 de la séance -->
<div class="vx-grid vx-mt4" data-block="topflop">
  <section class="vx-card vx-col-6" aria-label="Top 10 de la séance">
    <div class="vx-card-header"><span class="vx-card-title">Top 10 de la séance</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=stocks">Univers →</a></span></div>
    <div id="vx-top10">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Flop 10 de la séance">
    <div class="vx-card-header"><span class="vx-card-title">Flop 10 de la séance</span>
      <span class="vx-actions"><span class="vx-meta">plus fortes baisses · univers scanné</span></span></div>
    <div id="vx-flop10">%%LOADING%%</div>
  </section>
</div>

<!-- Rangée 4 : opportunités actions (6) + options (6) -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" data-block="opportunities" aria-label="Opportunités actions">
    <div class="vx-card-header"><span class="vx-card-title">Opportunités actions</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=stocks">Tout voir →</a></span></div>
    <div id="vx-opp-stocks">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Opportunités options">
    <div class="vx-card-header"><span class="vx-card-title">Opportunités options</span>
      <span class="vx-badge" style="color:var(--vx-violet)">Vertex Dynamic Options</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=options">Tout voir →</a></span></div>
    <div id="vx-opp-options">%%LOADING%%</div>
  </section>
</div>

<!-- Rangée 5 : rotation (7) + alertes (5) -->
<div class="vx-grid vx-mt4" data-block="rotation">
  <div class="vx-col-7" id="vx-rotation"></div>
  <section class="vx-card vx-col-5" data-block="alerts" aria-label="Alertes prioritaires">
    <div class="vx-card-header"><span class="vx-card-title">Alertes prioritaires</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=radar">Radar →</a></span></div>
    <div id="vx-alerts">%%LOADING%%</div>
  </section>
</div>

<!-- Rangée 6 : portefeuille (7) + calendrier (5) -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" data-block="portfolio" aria-label="Portefeuille">
    <div class="vx-card-header"><span class="vx-card-title">Portefeuille — Équipe Vertex</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">Ouvrir →</a></span></div>
    <div id="vx-portfolio">%%LOADING%%</div>
  </section>
  <div class="vx-col-5" data-block="calendar" id="vx-calendar"></div>
</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/sparkline.js" defer></script>
<script src="/static/vertex/js/charts/line-area-chart.js" defer></script>
<script src="/static/vertex/js/charts/breadth-chart.js" defer></script>
<script src="/static/vertex/js/charts/sector-chart.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script src="/static/vertex/js/charts/timeline-chart.js" defer></script>
<script>
(function(){
'use strict';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}

/* Personnalisation contrôlée des blocs (§43 — vxDashboardLayout.hidden) */
const BLOCKS=[['brief','Brief Vertex'],['regime','Régime'],['market','Marchés (graphiques)'],
  ['topflop','Top 10 / Flop 10'],['opportunities','Opportunités'],['rotation','Rotation & alertes'],
  ['portfolio','Portefeuille'],['calendar','Calendrier'],['alerts','Alertes']];
function layoutGet(){try{return JSON.parse(localStorage.getItem('vxDashboardLayout')||'{}')}catch(e){return{}}}
function layoutSet(l){try{localStorage.setItem('vxDashboardLayout',JSON.stringify(l))}catch(e){}}
function applyBlocks(){
  const hidden=(layoutGet().hidden)||[];
  document.querySelectorAll('[data-block]').forEach(el=>{
    el.style.display=hidden.includes(el.dataset.block)?'none':'';});
}
applyBlocks();
document.getElementById('vx-customize-btn')?.addEventListener('click',()=>{
  const hidden=(layoutGet().hidden)||[];
  VX.shell.openModal('Personnaliser le Briefing',
    BLOCKS.map(([id,label])=>`<label class="vx-checkbox" style="padding:5px 0">
      <input type="checkbox" data-blk="${id}" ${hidden.includes(id)?'':'checked'}> ${label}</label>`).join('')
    +'<div class="vx-help vx-mt2">Grille contrôlée — l’ordre des rangées reste fixe. Synchronisé sur cet appareil.</div>',
    '<button class="vx-btn" id="vx-layout-reset">Réinitialiser</button>'
    +'<button class="vx-btn vx-btn-primary" id="vx-layout-save">Enregistrer</button>');
  document.getElementById('vx-layout-save').addEventListener('click',()=>{
    const l=layoutGet();
    l.hidden=[...document.querySelectorAll('[data-blk]')].filter(c=>!c.checked).map(c=>c.dataset.blk);
    layoutSet(l);applyBlocks();VX.shell.closeModal();VX.toast('Briefing personnalisé','success');});
  document.getElementById('vx-layout-reset').addEventListener('click',()=>{
    const l=layoutGet();delete l.hidden;layoutSet(l);applyBlocks();VX.shell.closeModal();
    VX.toast('Disposition réinitialisée');});
});

/* Densité (vxDashboardLayout §43) */
(function(){
  let layout={};try{layout=JSON.parse(localStorage.getItem('vxDashboardLayout')||'{}')}catch(e){}
  const mode=layout.density||'confort';
  if(mode!=='confort')document.body.dataset.density=mode==='compact'?'compact':'dense';
  document.querySelectorAll('[data-density-btn]').forEach(b=>{
    b.setAttribute('aria-pressed',String(b.dataset.densityBtn===mode));
    b.addEventListener('click',()=>{
      layout.density=b.dataset.densityBtn;
      try{localStorage.setItem('vxDashboardLayout',JSON.stringify(layout))}catch(e){}
      document.body.dataset.density=layout.density==='compact'?'compact':(layout.density==='dense'?'dense':'');
      document.querySelectorAll('[data-density-btn]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    });
  });
})();

/* ── Market strip (§22) ── */
const STRIP=[['S&P 500','sp'],['Nasdaq','ndx'],['Dow Jones','dow'],['Russell 2000','rut'],
  ['VIX','vix'],['Taux 10 ans','tnx']];
const CROSS=[['DXY','dxy'],['Pétrole','oil'],['Or','gold'],['Bitcoin','btc']];
async function loadStrip(){
  let sum=null,scan=null;
  try{sum=await VX.fetch('/api/market/summary',{ttl:60000});}catch(e){}
  try{scan=await VX.fetch('/scan',{ttl:120000});}catch(e){}
  const list=(scan&&Array.isArray(scan.indices))?scan.indices:[];
  const byName={};list.forEach(i=>{byName[i.name]=i;});
  const pick=(n)=>{const i=byName[n]||{};return{last:i.price,change:i.change,series:i.spark};};
  const bySlug={sp:pick('S&P 500'),ndx:pick('Nasdaq'),dow:pick('Dow Jones'),
    rut:pick('Russell 2000'),vix:byName['VIX']?pick('VIX'):{last:sum&&sum.vix,change:sum&&sum.vix_chg},
    tnx:pick('Taux 10 ans'),dxy:pick('DXY'),oil:pick('Pétrole'),gold:pick('Or'),btc:pick('Bitcoin')};
  const mode=(scan&&scan.data_source==='demo')?'fallback':(scan&&scan.source==='ibkr'?'live':'delayed');
  const crossRows=CROSS.map(([label,slug])=>{
    const d=bySlug[slug]||{};const val=d.last??null;const chg=d.change??null;
    return `<div class="vx-kv"><span class="k">${label}</span>
      <span class="v vx-mono ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}">${val!==null?VX.fmt.price(val):'n/d'}${chg!==null?' · '+VX.fmt.pct(chg):''}</span></div>`;
  }).join('');
  $('vx-market-strip').innerHTML=STRIP.map(([label,slug])=>{
    const d=bySlug[slug]||{};
    const val=d.last??d.price??d.close??null;const chg=d.change??null;
    const target=slug==='vix'?'/markets?view=volatility':(['tnx','dxy','oil','gold','btc'].includes(slug)?'/markets?view=macro':'/markets?view=overview');
    /* Grand chiffre coloré pour les indices actions (direction = hausse bonne) ;
       VIX/taux restent neutres — colorer leur niveau induirait en erreur. */
    const dirClass=(chg!==null&&!['vix','tnx'].includes(slug))?(chg>0?'vx-pos':chg<0?'vx-neg':''):'';
    return `<a class="vx-card vx-card--compact vx-kpi vx-strip-item" style="text-decoration:none;color:inherit" href="${target}" aria-label="${label}">
      <span class="vx-kpi-label">${label}</span>
      <span class="vx-kpi-value ${dirClass}" style="font-size:19px">${VX.fmt.nd(val!==null?VX.fmt.price(val):null)}</span>
      <span class="vx-kpi-delta ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}">${chg!==null?VX.fmt.pct(chg):'n/d'}</span>
      <span data-spark="${slug}"></span>
      ${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),scan&&scan.source,mode)}</a>`;
  }).join('')
  +`<div class="vx-card vx-card--compact vx-strip-item" aria-label="Cross-asset">
     <span class="vx-kpi-label">Cross-asset</span>${crossRows}
     <a class="vx-btn vx-btn-sm vx-btn-ghost vx-mt1" href="/markets?view=macro">Macro →</a></div>`;
  STRIP.forEach(([_,slug])=>{const d=bySlug[slug]||{};
    if(d.series&&window.VXCharts)VXCharts.sparklineInto(document.querySelector(`[data-spark="${slug}"]`),d.series);});
  if(scan&&scan.data_source==='demo')
    $('vx-demo-banner').innerHTML='<div class="vx-demo-banner"><span class="vx-badge-demo">Démo</span> Données synthétiques clairement identifiées — jamais présentées comme réelles.</div>';
  return scan;
}

/* ── Brief Vertex (§21) ── */
async function loadBrief(){
  try{
    const b=await VX.fetch('/api/briefing/editorial',{ttl:60000});
    const changed=(b.changed_since_yesterday||[]).map(c=>`<li>${esc(c)}</li>`).join('');
    const daily=b.daily||{};
    const kindLabel={PRE_MARKET:'Pré-marché',INTRADAY:'Intraday',CLOSE:'Clôture',WEEKLY:'Hebdo'}[daily.kind]||'';
    const news=(b.what_changed_today||[]).map(x=>`<li>${esc(x)}</li>`).join('');
    const domSec=(daily.sections||[]).find(x=>x.label==='Actualité dominante');
    const ed=b.editorial||{};
    const edBlock=ed.narrative?(
      '<p style="font-size:15.5px;line-height:1.8;color:var(--vx-text,#f1efeb);margin:0 0 .8rem">'+esc(ed.narrative)+'</p>'
      +(ed.prices_mainly?'<div class="vx-insight vx-mt1"><b>Aujourd’hui, le marché prixe principalement</b><div class="vx-mt1">'+esc(ed.prices_mainly)+'</div></div>':'')
      +((ed.calls_impact||ed.discipline)?'<div class="vx-flex vx-wrap vx-mt2" style="gap:.4rem">'
        +(ed.calls_impact?'<span class="vx-badge" style="color:var(--vx-option,#85609f)">Calls : '+esc(ed.calls_impact)+'</span>':'')
        +(ed.news_available===false?'<span class="vx-badge" style="color:var(--vx-text-dim,#817d77)">Actualités indisponibles — brief data-only</span>':'')
        +'</div>':'')
      +'<div class="vx-divider vx-mt2"></div>'):'';
    $('vx-brief-body').innerHTML= edBlock+
      '<div style="font-size:14px;line-height:1.75">'+b.lines.map(l=>esc(l)).join('<br>')+'</div>'
      +(domSec?`<div class="vx-insight vx-mt3"><b>Actualité dominante</b><div class="vx-mt1">${esc(domSec.text)}</div></div>`:'')
      +(news?`<div class="vx-insight vx-mt2"><b>Ce qui a changé (sourcé)</b><ul class="vx-mt1" style="margin:0;padding-left:18px">${news}</ul></div>`:'')
      +(changed?`<div class="vx-insight vx-mt2"><b>Ce qui a changé depuis hier (moteurs)</b><ul class="vx-mt1" style="margin:0;padding-left:18px">${changed}</ul></div>`:'')
      +((b.main_risk||b.main_opportunity)?`<div class="vx-flex vx-wrap vx-mt2">
         ${b.main_risk?`<span class="vx-badge" style="color:var(--vx-negative)">Risque : ${esc(b.main_risk)}</span>`:''}
         ${b.main_opportunity?`<span class="vx-badge" style="color:var(--vx-positive)">Opportunité : ${esc(b.main_opportunity)}</span>`:''}</div>`:'')
      +`<div class="vx-card-footer">
         ${VX.updateIndicator(b.as_of,(b.sources||[]).join(', '),b.demo?'fallback':'delayed')}
         <span class="vx-badge">${b.generator==='deterministic'?'Brief déterministe (moteurs)':'Brief IA validé'}</span>
         ${kindLabel?`<span class="vx-badge" style="color:var(--vx-amber)">${kindLabel}</span>`:''}
         <a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets">Voir les preuves →</a></div>`;
    $('vx-brief-meta').innerHTML=`<span class="vx-meta">${(daily.word_count||b.word_count)} mots</span>`;
  }catch(e){$('vx-brief-body').innerHTML=VX.states.error('Brief indisponible ('+e.message+')');}
}

/* ── Régime (§20) ── */
async function loadRegime(){
  try{
    const r=await VX.fetch('/api/market/regime',{ttl:120000});
    const adj=r.adjustments||{};
    const conf=Math.round((r.confidence||0)*100);
    $('vx-regime-body').innerHTML=
      `<div id="vx-regime-gauge" class="vx-mb2"></div>
      <div class="vx-kpi vx-mb3" style="text-align:center"><span class="vx-kpi-value" style="font-size:22px" data-regime="${r.regime}">${r.regime}</span>
       <span class="vx-kpi-delta vx-muted">${(r.dimensions_used||[]).length} dimensions évaluées</span></div>
      <div class="vx-kv"><span class="k">Nouveau risque</span><span class="v ${adj.new_risk_allowed?'vx-pos':'vx-neg'}">${adj.new_risk_allowed?'autorisé':'BLOQUÉ'}</span></div>
      <div class="vx-kv"><span class="k">Priorité setups</span><span class="v">${VX.fmt.nd(adj.setup_priority)}</span></div>
      <div class="vx-kv"><span class="k">Confirmations exigées</span><span class="v">${VX.fmt.nd(adj.confirmation_required)}</span></div>
      <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'Moteur de régimes','delayed')}
      <a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets">Marchés →</a></div>`;
    if(window.VXCharts&&VXCharts.gauge){
      const reading=conf>=70?'Signal net — régime lisible':conf>=40?'Signal modéré — confirmations utiles':'Signal faible — prudence accrue';
      VXCharts.gauge('vx-regime-gauge',{value:conf,min:0,max:100,unit:' %',label:'confiance',reading:reading,
        bands:[{to:40,color:VXCharts.colors.negative},{to:70,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.positive}]});
    }
  }catch(e){$('vx-regime-body').innerHTML=VX.states.error('Régime indisponible');}
}

/* ── Graphique marché + breadth (rangée 3) ── */
async function loadMarketCharts(scan){
  scan=scan||{};const det=(scan.detail||{});
  const spyd=det.SPY||det[Object.keys(det)[0]]||{};
  const closes=(spyd.series&&spyd.series.close)||[];
  const m=scan.market||scan.market_ctx||{};
  const mode=scan.data_source==='demo'?'fallback':'delayed';
  if(closes.length>10){
    VXCharts.areaCard('vx-market-chart',{
      title:'Marché US — série de référence',timeframe:closes.length+' séances',
      question:'La tendance de fond reste-t-elle exploitable ?',
      conclusion:(m.spy_regime==='TREND'?'Tendance intacte':'Régime '+(m.spy_regime||'n/d'))+(m.verdict?' — '+m.verdict:''),
      labels:closes.map((_,i)=>i-closes.length),values:closes,height:230,
      source:scan.source||'scan',timestamp:scan.scan_ts||scan.updated,mode,
      explain:{shows:'La série de clôtures de la référence marché calculée par le scan.',
        why:'La Stratégie Vertex n’attaque qu’en environnement porteur : le régime module seuils et tailles.',
        confirm:'Nouvelle clôture au-dessus des dernières résistances avec breadth > 55 %.',
        invalidate:'Cassure des supports avec expansion de volatilité.'}});
  }else{
    $('vx-market-chart').innerHTML='<div class="vx-card">'+VX.states.empty('Série marché indisponible — lancer un scan depuis Système.','<a class="vx-btn vx-btn-sm" href="/system?view=data">Système / Données</a>')+'</div>';
  }
  const breadth=m.breadth;
  if(breadth!==null&&breadth!==undefined){
    VXCharts.breadthCard('vx-breadth-chart',{
      title:'Breadth / participation',question:'La hausse est-elle partagée ?',
      conclusion:breadth>=55?'Participation saine.':'Participation étroite — sélectivité.',
      labels:['> moyenne'],values:[breadth],height:190,
      source:scan.source||'scan',timestamp:scan.scan_ts||scan.updated,mode,
      limits:'breadth calculée sur les leaders scannés (univers partiel)',
      explain:{shows:'Le pourcentage de titres au-dessus de leur moyenne (moteur de contexte marché).',
        why:'Une hausse portée par 3 titres est fragile ; la breadth qualifie le régime.',
        confirm:'Breadth > 60 % stable plusieurs séances.',invalidate:'Breadth < 40 % pendant que les indices montent.'}});
  }else{$('vx-breadth-chart').innerHTML='<div class="vx-card">'+VX.states.empty('Breadth non calculée par le dernier scan.')+'</div>';}
}

/* ── Top 10 / Flop 10 de la séance (rangée 3b) ── */
function moversHtml(rows,dir){
  const sorted=rows.filter(r=>r.change!==null&&r.change!==undefined).slice()
    .sort((a,b)=>dir==='top'?(b.change-a.change):(a.change-b.change)).slice(0,10);
  if(!sorted.length)return VX.states.empty('Aucune variation exploitable dans le dernier scan.');
  return sorted.map(function(r){const chg=r.change;
    return `<div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">
      <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.symbol}">${r.symbol}</button>
      <span class="vx-num vx-mono ${chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted'}" style="width:62px;text-align:right;font-weight:700">${VX.fmt.pct(chg,1)}</span>
      <span class="vx-grow vx-truncate vx-dim" style="font-size:11.5px">${esc(r.sector||'')}</span>
      <span class="vx-num vx-mono vx-meta" style="width:64px;text-align:right">${r.price!==null&&r.price!==undefined?VX.fmt.price(r.price):''}</span>
      ${r.score!==null&&r.score!==undefined?`<span class="vx-badge" title="Score Vertex">${VX.fmt.num(r.score,0)}</span>`:''}
      <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${r.symbol}" aria-label="Actions ${r.symbol}">⋯</button>
    </div>`;}).join('');
}
function loadTopFlop(scan){
  const rows=(scan&&scan.rows)||[];
  const t=$('vx-top10'),f=$('vx-flop10');
  const mode=(scan&&scan.data_source==='demo')?'fallback':(scan&&scan.source==='ibkr'?'live':'delayed');
  const foot=`<div class="vx-card-footer">${VX.updateIndicator(scan&&(scan.scan_ts||scan.updated),(scan&&scan.source)||'scan',mode)} · ${rows.length} titres scannés</div>`;
  if(t)t.innerHTML=moversHtml(rows,'top')+foot;
  if(f)f.innerHTML=moversHtml(rows,'flop')+foot;
}

/* ── Opportunités (rangée 4) ── */
async function loadOpportunities(){
  try{
    const c=await VX.fetch('/api/command',{ttl:60000});
    const stocks=(c.top_stocks||[]).slice(0,5);
    $('vx-opp-stocks').innerHTML=stocks.length?stocks.map(s=>`
      <div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${s.symbol}">${s.symbol}</button>
        <span class="vx-badge">${esc(s.verdict||'')}</span>
        <span class="vx-grow vx-truncate vx-dim" style="font-size:12px">${esc(s.note||'')}</span>
        <span class="vx-num vx-mono">${VX.fmt.nd(s.price)}</span>
        <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${s.symbol}" aria-label="Actions ${s.symbol}">⋯</button>
      </div>`).join(''):VX.states.empty('Aucune opportunité action retenue par le comité.');
    const opts=(c.top_options||[]).slice(0,5);
    $('vx-opp-options').innerHTML=opts.length?opts.map(o=>`
      <div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${o.symbol}">${o.symbol}</button>
        <span class="vx-badge" style="color:var(--vx-violet)">${esc(o.label||o.dir||'CALL')}</span>
        <span class="vx-grow vx-num vx-mono vx-dim">strike ${VX.fmt.nd(o.strike)} · prime ${VX.fmt.nd(o.premium)}</span>
        <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${o.symbol}" aria-label="Actions ${o.symbol}">⋯</button>
      </div>`).join(''):VX.states.empty('Aucun contrat retenu — le sélecteur ne force jamais une idée.');
  }catch(e){
    $('vx-opp-stocks').innerHTML=VX.states.error('Opportunités indisponibles');
    $('vx-opp-options').innerHTML=VX.states.error('Opportunités indisponibles');
  }
}

/* ── Rotation + alertes (rangée 5) ── */
async function loadRotation(scan){
  const sectors=(scan&&scan.sectors)||[];
  if(sectors.length){
    VXCharts.sectorCard('vx-rotation',{
      title:'Rotation sectorielle',question:'Où va le capital en ce moment ?',
      conclusion:'Leader : '+(sectors[0].sector||'n/d'),
      labels:sectors.slice(0,9).map(s=>s.sector),
      values:sectors.slice(0,9).map(s=>s.avg_score??s.score??0),height:230,
      source:scan.source,timestamp:scan.scan_ts||scan.updated,
      mode:scan.data_source==='demo'?'fallback':'delayed',
      onSector:(name)=>{VX.context.save();location.href='/opportunities?view=stocks&sector='+encodeURIComponent(name);},
      explain:{shows:'Score moyen par secteur (moteur de rotation).',
        why:'La stratégie suit les secteurs qui attirent le capital.',
        confirm:'Leadership stable sur plusieurs séances.',invalidate:'Rotation défensive brutale.'}});
  }else $('vx-rotation').innerHTML='<div class="vx-card">'+VX.states.empty('Secteurs non calculés par le dernier scan.')+'</div>';
}
async function loadAlerts(){
  try{
    const [mine,fired]=await Promise.all([
      Promise.resolve((E()&&E().alerts())||[]),
      VX.fetch('/api/alerts/status',{ttl:30000}).catch(()=>({fired:{}}))]);
    const firedMap=fired.fired||{};
    const rows=mine.filter(a=>a.active).slice(0,6).map(a=>{
      const hit=Object.values(firedMap).find(f=>f.id===a.id);
      return `<div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${a.sym}">${a.sym}</button>
        <span class="vx-grow vx-dim" style="font-size:12px">${a.cond==='above'?'franchit':'casse'} ${VX.fmt.price(a.level)} ${esc(a.note||'')}</span>
        ${hit?'<span class="vx-badge" style="color:var(--vx-warning)">déclenchée</span>':'<span class="vx-badge">armée</span>'}
      </div>`;}).join('');
    $('vx-alerts').innerHTML=rows||VX.states.empty('Aucune alerte active.',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'alert\')">Créer une alerte</button>');
  }catch(e){$('vx-alerts').innerHTML=VX.states.error('Alertes indisponibles');}
}

/* ── Portefeuille + calendrier (rangée 6) ── */
async function loadPortfolio(){
  const pos=(E()&&E().positions())||[];
  if(!pos.length){
    $('vx-portfolio').innerHTML=VX.states.empty('Aucune position déclarée.',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>');
    return;
  }
  let quotes={};
  try{
    /* Contrat serveur : {positions:[...]} → résultats par clé 'SYM|exp|strike|RIGHT'. */
    const body=pos.map(t=>({sym:t.sym,exp:t.exp,strike:t.strike,right:t.right}));
    const r=await fetch('/api/pos-quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({positions:body})});
    const res=(await r.json()).results||{};
    pos.forEach(t=>{const key=[String(t.sym).toUpperCase(),t.exp||'',
      (t.strike!==null&&t.strike!==undefined)?t.strike:'',
      (t.right||'').toUpperCase()].join('|');
      if(res[key])quotes[t.id]=res[key];});
  }catch(e){}
  $('vx-portfolio').innerHTML=pos.slice(0,6).map(t=>{
    const q=quotes[t.id]||{};const isOpt=t.type!=='STK';
    const mark=isOpt?(q.mark??q.last??null):(q.spot??q.mark??q.last??null);
    const value=mark!==null?(isOpt?mark*100*t.qty:mark*t.qty):null;
    const pl=value!==null&&t.cost?((value-t.cost)/t.cost*100):null;
    return `<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
      <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${t.sym}">${t.sym}</button>
      <span class="vx-badge" ${t.type!=='STK'?'style="color:var(--vx-violet)"':''}>${t.type}${t.strike?' '+t.strike:''}</span>
      <span class="vx-grow vx-mono vx-meta">${t.qty} × ${VX.fmt.price(t.cost)}${t.exp?' · '+t.exp:''}</span>
      <span class="vx-num vx-mono ${pl>0?'vx-pos':pl<0?'vx-neg':'vx-muted'}">${pl!==null?VX.fmt.pct(pl,1):'n/d'}</span>
      <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Actions ${t.sym}">⋯</button></div>`;
  }).join('')+`<div class="vx-card-footer">${pos.length} position(s) · marques ${Object.keys(quotes).length?'IBKR/desk':'indisponibles'}</div>`;
}
async function loadCalendar(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const items=[...(cal.macro||[]).map(m=>({when:m.date,kind:m.kind,label:m.label+(m.note?' — '+m.note:'')})),
      ...(cal.items||[]).slice(0,6).map(it=>({when:it.date,kind:'Earnings',label:`résultats dans ${it.dte} j`,sym:it.sym}))]
      .sort((a,b)=>String(a.when).localeCompare(String(b.when))).slice(0,8);
    VXCharts.timelineCard('vx-calendar',{title:'Calendrier',question:'Quels catalyseurs arrivent ?',
      items,source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun événement imminent identifié.'});
  }catch(e){$('vx-calendar').innerHTML='<div class="vx-card">'+VX.states.error('Calendrier indisponible')+'</div>';}
}

/* ── Orchestration ── */
async function boot(){
  loadBrief();loadRegime();loadOpportunities();loadAlerts();loadPortfolio();loadCalendar();
  const scan=await loadStrip();
  loadMarketCharts(scan);loadTopFlop(scan);loadRotation(scan);
}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}
whenChartsReady(boot);
VX.refresh.register(loadStrip,120000,'strip');
VX.refresh.register(loadAlerts,60000,'alerts');
VX.bus.on('vx:position-changed',loadPortfolio);
VX.bus.on('vx:alert-changed',loadAlerts);
VX.bus.on('vx:data-refreshed',()=>{loadBrief();loadRegime();});
})();
</script>
"""


def render(scan_state: dict | None = None) -> str:
    content = _CONTENT.replace('%%LOADING%%',
                               '<div class="vx-skeleton" style="height:60px"></div>')
    return render_shell(title='Briefing', active='briefing', space_label='Briefing',
                        sub_label='Marchés US', content=content, page_js=_JS,
                        page_label='Briefing')
