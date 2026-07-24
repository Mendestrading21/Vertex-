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
  <div><h1>Aujourd&#8217;hui</h1>
  <div class="vx-sub">Dois-je agir aujourd&#8217;hui, et sur quoi ?</div></div>
</div>
<div id="vx-demo-banner"></div>

<!-- NIVEAU 1 — Réponse immédiate : Hero éditorial (la réponse en 10 s).
     Aujourd'hui RÉSUME ; Marchés explique. Une donnée = un seul domicile. -->
<section class="vx-card vx-card--hero" id="vx-hero" aria-label="Réponse du jour">
  <div class="vx-card-header"><span class="vx-card-title">Brief Vertex</span>
    <span class="vx-actions" id="vx-hero-fresh"></span></div>
  <div id="vx-brief-body">%%LOADING%%</div>
  <div class="vx-grid vx-mt3" id="vx-hero-kpis" aria-label="Résumé cliquable (chaque tuile pointe vers son domicile canonique)"></div>
  <div class="vx-mt3" id="vx-hero-action"></div>
</section>

<!-- NIVEAU 2 — Justification (résumé, jamais la recopie de Marchés) -->
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Depuis la dernière visite">
    <div class="vx-card-header"><span class="vx-card-title">Depuis ta dernière visite</span></div>
    <div id="vx-diff">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Régime de marché">
    <div class="vx-card-header"><span class="vx-card-title">Régime</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/markets">Marchés →</a></span></div>
    <div id="vx-regime-body">%%LOADING%%</div>
  </section>
</div>

<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Meilleures opportunités">
    <div class="vx-card-header"><span class="vx-card-title">Meilleures opportunités</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities">Toutes →</a></span></div>
    <div id="vx-opp-stocks">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Alertes prioritaires">
    <div class="vx-card-header"><span class="vx-card-title">Alertes prioritaires</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=radar">Radar →</a></span></div>
    <div id="vx-alerts">%%LOADING%%</div>
  </section>
</div>

<div class="vx-grid vx-mt4">
  <div class="vx-col-6" id="vx-calendar"></div>
  <section class="vx-card vx-col-6" aria-label="Portefeuille — ce qui a changé">
    <div class="vx-card-header"><span class="vx-card-title">Portefeuille — ce qui a changé</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">Ouvrir →</a></span></div>
    <div id="vx-portfolio">%%LOADING%%</div>
  </section>
</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/timeline-chart.js" defer></script>
<script>
(function(){
'use strict';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function freshBadge(m){const map={live:['live','Live'],delayed:['delayed','Différé'],demo:['fallback','Démo'],stale:['frozen','Périmé'],offline:['offline','Hors ligne'],missing:['offline','Indisponible']};
  const x=map[m]||map.delayed;return '<span class="vx-freshness" data-live="'+x[0]+'"><span class="vx-live-dot"></span>'+x[1]+'</span>';}
function num(x){return (x!==null&&x!==undefined&&!isNaN(x))?Number(x):null;}
function breadthOf(sb){if(sb==null)return null;if(typeof sb==='object')return num(sb.above50)??num(sb.above200);return num(sb);}

/* Tuile KPI résumé — cliquable, pointe vers son domicile canonique. */
function kpiTile(label,value,cls,href){
  return '<a class="vx-card vx-card--compact vx-kpi vx-col-3" style="text-decoration:none;color:inherit" href="'+href+'" aria-label="'+esc(label)+'">'
    +'<span class="vx-kpi-label">'+esc(label)+'</span>'
    +'<span class="vx-kpi-value '+(cls||'')+'" style="font-size:20px">'+value+'</span>'
    +'<span class="vx-kpi-delta vx-muted">voir →</span></a>';
}

/* ── Hero éditorial : la réponse en 10 s ── */
async function loadBrief(){
  try{
    const b=await VX.fetch('/api/briefing/editorial',{ttl:60000});
    const m=b.demo?'demo':'delayed';
    $('vx-hero-fresh').innerHTML=freshBadge(m)+' <span class="vx-meta">'+esc((b.sources||[]).join(', '))+'</span>';
    const ed=b.editorial||{};
    const edBlock=ed.narrative?('<p style="font-size:15.5px;line-height:1.75;color:var(--vx-text);margin:0 0 .7rem">'+esc(ed.narrative)+'</p>'):'';
    $('vx-brief-body').innerHTML=edBlock
      +'<div style="font-size:14px;line-height:1.75">'+(b.lines||[]).map(l=>esc(l)).join('<br>')+'</div>'
      +((b.main_risk||b.main_opportunity)?'<div class="vx-flex vx-wrap vx-mt2">'
        +(b.main_risk?'<span class="vx-badge" style="color:var(--vx-negative)">Risque : '+esc(b.main_risk)+'</span>':'')
        +(b.main_opportunity?'<span class="vx-badge" style="color:var(--vx-positive)">Opportunité : '+esc(b.main_opportunity)+'</span>':'')+'</div>':'')
      +'<div class="vx-card-footer"><span class="vx-badge">'+(b.generator==='deterministic'?'Brief déterministe (moteurs)':'Brief IA validé')+'</span>'
      +'<a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets">Voir les preuves →</a></div>';
    if(b.demo)$('vx-demo-banner').innerHTML='<div class="vx-demo-banner"><span class="vx-badge-demo">Démo</span> Données synthétiques clairement identifiées — jamais présentées comme réelles.</div>';
  }catch(e){$('vx-brief-body').innerHTML=VX.states.error('Brief indisponible ('+e.message+')');}
}

/* ── 4 KPI résumé cliquables (régime, breadth, VIX, meilleure opportunité) ── */
async function loadSummary(){
  let sum={},reg={},cmd={};
  try{sum=await VX.fetch('/api/market/summary',{ttl:60000})||{};}catch(e){}
  try{reg=await VX.fetch('/api/market/regime',{ttl:120000})||{};}catch(e){}
  try{cmd=await VX.fetch('/api/command',{ttl:60000})||{};}catch(e){}
  const conf=Math.round((reg.confidence||0)*100);
  const br=breadthOf(sum.breadth);
  let vix=num(sum.vix);
  const best=(cmd.top_stocks||[])[0]||null;
  const regHtml=reg.regime?esc(reg.regime):'n/d';
  const brHtml=br!=null?(br+' %'):'n/d';
  const brCls=br!=null?(br>=55?'vx-pos':'vx-warn'):'';
  const vixHtml=vix!=null?vix:'n/d';
  const bestHtml=best?esc(best.symbol):'—';
  const kpis=[
    kpiTile('Régime',regHtml+' <span class="vx-meta">('+conf+'%)</span>','','/markets'),
    kpiTile('Breadth',brHtml,brCls,'/markets?view=breadth'),
    kpiTile('VIX',vixHtml,'','/markets?view=volatility'),
    best?kpiTile('Meilleure opp.',bestHtml,'','/analysis/'+encodeURIComponent(best.symbol)):kpiTile('Meilleure opp.','—','','/opportunities'),
  ].join('');
  $('vx-hero-kpis').innerHTML=kpis;
  /* Action prioritaire : dérivée uniquement des données réelles. */
  let action='';
  if(best&&best.symbol){
    action='<a class="vx-btn vx-btn-primary" data-open-analysis="'+esc(best.symbol)+'">Action : étudier le dossier '+esc(best.symbol)+' →</a>';
  }else if(reg.regime){
    action='<a class="vx-btn vx-btn-soft" href="/markets">Action : vérifier le régime dans Marchés →</a>';
  }else{
    action='<span class="vx-meta">Aucune action prioritaire dérivée des données disponibles.</span>';
  }
  $('vx-hero-action').innerHTML=action;
  /* Diff honnête depuis la dernière visite. */
  renderDiff({regime:reg.regime||null,breadth:br,vix:vix,best:best?best.symbol:null,
    opp:(cmd.top_stocks||[]).length});
}

/* ── Diff « depuis ta dernière visite » — honnête (baseline locale) ── */
function renderDiff(cur){
  const host=$('vx-diff');if(!host)return;
  let prev=null;try{prev=JSON.parse(localStorage.getItem('vxTodayBaseline')||'null');}catch(e){prev=null;}
  const rows=[];
  if(!prev||!prev.ts){
    host.innerHTML='<div class="vx-state" data-state="empty"><div class="vx-state-icon">—</div>'
      +'<div><b>Aucun historique de comparaison disponible.</b><br>'
      +'<span class="vx-meta">La référence de cette visite est enregistrée ; les changements apparaîtront à la prochaine.</span></div></div>';
  }else{
    const fmtDelta=(a,b,unit)=>{if(a==null||b==null)return null;const d=Math.round((a-b)*10)/10;if(d===0)return null;
      const cls=d>0?'vx-pos':'vx-neg';return '<span class="vx-mono '+cls+'">'+(d>0?'+':'')+d+(unit||'')+'</span>';};
    if(prev.regime&&cur.regime&&prev.regime!==cur.regime)
      rows.push('Régime : <b>'+esc(prev.regime)+'</b> → <b>'+esc(cur.regime)+'</b>');
    const bd=fmtDelta(cur.breadth,prev.breadth,' pts');if(bd)rows.push('Breadth '+bd);
    const vd=fmtDelta(cur.vix,prev.vix,'');if(vd)rows.push('VIX '+vd);
    if((cur.opp||0)!==(prev.opp||0))rows.push('Opportunités : '+prev.opp+' → '+cur.opp);
    if(cur.best&&prev.best&&cur.best!==prev.best)rows.push('Meilleure opp. : '+esc(prev.best)+' → '+esc(cur.best));
    host.innerHTML=rows.length
      ? '<ul style="margin:0;padding-left:18px;line-height:1.9;font-size:13px">'+rows.map(r=>'<li>'+r+'</li>').join('')+'</ul>'
        +'<div class="vx-meta vx-mt2">Depuis '+esc(new Date(prev.ts).toLocaleString('fr-FR'))+'</div>'
      : '<div class="vx-state" data-state="empty"><div class="vx-state-icon">=</div><div><b>Rien de significatif n’a changé</b><br><span class="vx-meta">depuis '+esc(new Date(prev.ts).toLocaleString('fr-FR'))+'</span></div></div>';
  }
  try{localStorage.setItem('vxTodayBaseline',JSON.stringify(Object.assign({},cur,{ts:Date.now()})));}catch(e){}
}

/* ── Régime : jauge de confiance (1 des 2 graphiques conservés) ── */
async function loadRegime(){
  try{
    const r=await VX.fetch('/api/market/regime',{ttl:120000});
    const adj=r.adjustments||{};
    const conf=Math.round((r.confidence||0)*100);
    $('vx-regime-body').innerHTML=
      '<div id="vx-regime-gauge" class="vx-mb2"></div>'
      +'<div class="vx-kv"><span class="k">Nouveau risque</span><span class="v '+(adj.new_risk_allowed?'vx-pos':'vx-neg')+'">'+(adj.new_risk_allowed?'autorisé':'BLOQUÉ')+'</span></div>'
      +'<div class="vx-kv"><span class="k">Confirmations exigées</span><span class="v">'+VX.fmt.nd(adj.confirmation_required)+'</span></div>'
      +'<div class="vx-card-footer">'+VX.updateIndicator(Date.now(),'Moteur de régimes','delayed')
      +'<a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets?view=breadth">Participation →</a></div>';
    if(window.VXCharts&&VXCharts.gauge){
      const CO=(window.VXCharts&&VXCharts.colors)||{};
      const reading=conf>=70?'Signal net — régime lisible':conf>=40?'Signal modéré — confirmations utiles':'Signal faible — prudence accrue';
      VXCharts.gauge('vx-regime-gauge',{value:conf,min:0,max:100,unit:' %',label:esc(r.regime||'confiance'),reading:reading,
        bands:[{to:40,color:CO.negative},{to:70,color:CO.warning},{to:100,color:CO.positive}]});
    }
  }catch(e){$('vx-regime-body').innerHTML=VX.states.error('Régime indisponible');}
}

/* ── Meilleures opportunités (top 3, résumé) ── */
async function loadOpportunities(){
  try{
    const c=await VX.fetch('/api/command',{ttl:60000});
    const stocks=(c.top_stocks||[]).slice(0,3);
    $('vx-opp-stocks').innerHTML=stocks.length?stocks.map(s=>
      '<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">'
      +'<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="'+esc(s.symbol)+'">'+esc(s.symbol)+'</button>'
      +'<span class="vx-badge">'+esc(s.verdict||'')+'</span>'
      +'<span class="vx-grow vx-truncate vx-dim" style="font-size:12px">'+esc(s.note||'')+'</span>'
      +'<span class="vx-num vx-mono">'+VX.fmt.nd(s.price)+'</span>'
      +'<button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="'+esc(s.symbol)+'" aria-label="Actions">⋯</button></div>').join('')
      :VX.states.empty('Aucune opportunité retenue par le comité.');
  }catch(e){$('vx-opp-stocks').innerHTML=VX.states.error('Opportunités indisponibles');}
}

/* ── Alertes prioritaires (top 3) ── */
async function loadAlerts(){
  try{
    const [mine,cmd]=await Promise.all([
      Promise.resolve((E()&&E().alerts())||[]),
      VX.fetch('/api/command',{ttl:30000}).catch(()=>({}))]);
    const srv=((cmd&&cmd.alerts)||[]).slice(0,3).map(a=>{
      const icon=a[0]||'⚠', danger=(icon==='🔴');
      return '<div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">'
        +'<span aria-hidden="true">'+esc(icon)+'</span>'
        +'<span class="vx-grow vx-dim" style="font-size:12px">'+esc(a[2]||a[1]||'')+'</span>'
        +'<span class="vx-badge" style="color:var(--vx-'+(danger?'negative':'warning')+')">'+esc(a[1]||'alerte')+'</span></div>';}).join('');
    const rows=mine.filter(a=>a.active).slice(0,3).map(a=>
      '<div class="vx-flex" style="padding:6px 0;border-bottom:1px dashed var(--vx-border-soft)">'
      +'<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="'+esc(a.sym)+'">'+esc(a.sym)+'</button>'
      +'<span class="vx-grow vx-dim" style="font-size:12px">'+(a.cond==='above'?'franchit':'casse')+' '+VX.fmt.price(a.level)+'</span>'
      +'<span class="vx-badge">armée</span></div>').join('');
    $('vx-alerts').innerHTML=(srv+rows)||VX.states.empty('Aucune alerte active.',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'alert\')">Créer une alerte</button>');
  }catch(e){$('vx-alerts').innerHTML=VX.states.error('Alertes indisponibles');}
}

/* ── Catalyseurs (timeline, 2e graphique conservé, ≤ 3) ── */
async function loadCalendar(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const items=[...(cal.macro||[]).map(m=>({when:m.date,kind:m.kind,label:m.label+(m.note?' — '+m.note:'')})),
      ...(cal.items||[]).slice(0,4).map(it=>({when:it.date,kind:'Earnings',label:'résultats dans '+it.dte+' j',sym:it.sym}))]
      .sort((a,b)=>String(a.when).localeCompare(String(b.when))).slice(0,3);
    VXCharts.timelineCard('vx-calendar',{title:'Catalyseurs imminents',question:'Quels catalyseurs arrivent ?',
      conclusion:items.length?('Prochain : '+esc(items[0].label)):'',
      items,source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun événement imminent identifié.'});
  }catch(e){$('vx-calendar').innerHTML='<div class="vx-card">'+VX.states.error('Calendrier indisponible')+'</div>';}
}

/* ── Portefeuille : ce qui a changé (compact) ── */
async function loadPortfolio(){
  const pos=(E()&&E().positions())||[];
  if(!pos.length){
    $('vx-portfolio').innerHTML=VX.states.empty('Aucune position déclarée.',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>');
    return;
  }
  let quotes={};
  try{
    const body=pos.map(t=>({sym:t.sym,exp:t.exp,strike:t.strike,right:t.right}));
    const r=await fetch('/api/pos-quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({positions:body})});
    const res=(await r.json()).results||{};
    pos.forEach(t=>{const key=[String(t.sym).toUpperCase(),t.exp||'',
      (t.strike!==null&&t.strike!==undefined)?t.strike:'',(t.right||'').toUpperCase()].join('|');
      if(res[key])quotes[t.id]=res[key];});
  }catch(e){}
  $('vx-portfolio').innerHTML=pos.slice(0,4).map(t=>{
    const q=quotes[t.id]||{};const isOpt=t.type!=='STK';
    const mark=isOpt?(q.mark??q.last??null):(q.spot??q.mark??q.last??null);
    const value=mark!==null?(isOpt?mark*100*t.qty:mark*t.qty):null;
    const pl=value!==null&&t.cost?((value-t.cost)/t.cost*100):null;
    return '<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">'
      +'<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="'+t.sym+'">'+t.sym+'</button>'
      +'<span class="vx-badge" '+(t.type!=='STK'?'style="color:var(--vx-violet)"':'')+'>'+t.type+(t.strike?' '+t.strike:'')+'</span>'
      +'<span class="vx-grow vx-mono vx-meta">'+t.qty+' × '+VX.fmt.price(t.cost)+'</span>'
      +'<span class="vx-num vx-mono '+(pl>0?'vx-pos':pl<0?'vx-neg':'vx-muted')+'">'+(pl!==null?VX.fmt.pct(pl,1):'n/d')+'</span></div>';
  }).join('')+'<div class="vx-card-footer">'+pos.length+' position(s) · marques '+(Object.keys(quotes).length?'IBKR/desk':'indisponibles')+'</div>';
}

/* ── Orchestration ── */
function boot(){
  loadBrief();loadSummary();loadRegime();loadOpportunities();loadAlerts();loadCalendar();loadPortfolio();
}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}
whenChartsReady(boot);
VX.refresh.register(loadSummary,120000,'today-summary');
VX.refresh.register(loadAlerts,60000,'alerts');
VX.bus.on('vx:position-changed',loadPortfolio);
VX.bus.on('vx:alert-changed',loadAlerts);
VX.bus.on('vx:data-refreshed',()=>{loadBrief();loadSummary();loadRegime();});
})();
</script>
"""


def render(scan_state: dict | None = None) -> str:
    content = _CONTENT.replace('%%LOADING%%',
                               '<div class="vx-skeleton" style="height:60px"></div>')
    return render_shell(title="Aujourd'hui", active='briefing', space_label="Aujourd'hui",
                        sub_label='Résumé du jour', content=content, page_js=_JS,
                        page_label="Aujourd'hui")
