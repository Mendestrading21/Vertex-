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
<div class="vx-page-header vx-page-lead vx-today-header">
  <div class="vx-page-lead__main"><h1>Aujourd&#8217;hui</h1>
  <div class="vx-sub">La réponse utile maintenant, puis les preuves à la demande.</div></div>
</div>
<div id="vx-demo-banner"></div>

<!-- Bandeau de fraîcheur compact. Le digest reste celui du serveur : cette vue
     ne recalcule ni le régime, ni les opportunités, ni la confiance. -->
<section class="vx-asess vx-toolbar vx-today-freshness" id="vx-asess"
         aria-label="Fraîcheur de la session d'analyse" aria-live="polite">%%LOADING%%</section>

<!-- NIVEAU 1 — une phrase décisionnelle et quatre KPI au maximum. -->
<section class="vx-card vx-card--hero vx-today-lead" id="vx-hero" aria-label="Réponse du jour">
  <div class="vx-card-header"><span class="vx-card-title">Décision du jour</span>
    <span class="vx-actions" id="vx-hero-fresh"></span></div>
  <div id="vx-brief-body" aria-live="polite">%%LOADING%%</div>
  <div class="vx-kpi-strip vx-mt3" id="vx-hero-kpis" data-max-kpis="4"
       aria-label="Quatre indicateurs clés, chacun relié à son domicile canonique"></div>
  <!-- L'AGE des quatre KPI. Mesuré : sans lui, ces quatre chiffres — les
       premiers que l'écran montre — ne portaient AUCUNE indication de date ;
       la seule marque de la carte était le badge « Démo », qui qualifie la
       NATURE de la donnée, pas son âge. Rempli par loadSummary depuis
       `scan_age` (le serveur le sert déjà), via VX.freshness — jamais un
       libellé écrit à la main. -->
  <div class="vx-meta vx-mt2" id="vx-hero-age"></div>
  <div class="vx-mt3" id="vx-hero-action"></div>
</section>

<!-- NIVEAU 2 — une seule visualisation de régime ; changelog court à droite. -->
<div class="vx-hero-grid vx-mt4 vx-today-context">
  <section class="vx-card vx-card--hero" aria-label="Régime de marché">
    <div class="vx-card-header"><span class="vx-card-title">Régime</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/markets">Marchés →</a></span></div>
    <div id="vx-regime-body">%%LOADING%%</div>
  </section>
  <aside class="vx-insight-rail" style="grid-template-columns:minmax(0,1fr)" aria-label="Changements depuis la dernière visite">
    <section class="vx-card">
      <div class="vx-card-header"><span class="vx-card-title">Ce qui a changé</span></div>
      <div id="vx-diff">%%LOADING%%</div>
      <div id="vx-mkt-diff" class="vx-mt2"></div>
    </section>
  </aside>
</div>

<!-- NIVEAU 2 — les éléments à surveiller restent visibles mais secondaires. -->
<div class="vx-section-stack vx-mt4">
  <div class="vx-hero-grid vx-today-secondary">
    <section class="vx-card" aria-label="Meilleures opportunités">
      <div class="vx-card-header"><span class="vx-card-title">Opportunités à étudier</span>
        <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities">Toutes →</a></span></div>
      <div id="vx-opp-stocks">%%LOADING%%</div>
    </section>
    <section class="vx-card" aria-label="Alertes prioritaires">
      <div class="vx-card-header"><span class="vx-card-title">Alertes prioritaires</span>
        <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=radar">Radar →</a></span></div>
      <div id="vx-alerts">%%LOADING%%</div>
    </section>
  </div>

  <!-- NIVEAU 3 — contrats conservés, détails repliés pour ne pas concurrencer
       la décision principale. Les hôtes restent montés et sourcés. -->
  <details class="vx-disclosure vx-today-details">
    <summary>Catalyseurs et portefeuille</summary>
    <div class="vx-disclosure__body">
      <div class="vx-hero-grid">
        <div id="vx-calendar"></div>
        <section class="vx-card" aria-label="Portefeuille — ce qui a changé">
          <div class="vx-card-header"><span class="vx-card-title">Portefeuille — ce qui a changé</span>
            <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">Ouvrir →</a></span></div>
          <div id="vx-portfolio">%%LOADING%%</div>
        </section>
      </div>
    </div>
  </details>
</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/regime-aura.js" defer></script>
<script src="/static/vertex/js/charts/catalyst-runway.js" defer></script>
<script>
(function(){
'use strict';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));}
function freshBadge(m){const map={live:['live','Live'],delayed:['delayed','Différé'],demo:['fallback','Démo'],stale:['frozen','Périmé'],offline:['offline','Hors ligne'],missing:['offline','Indisponible']};
  const x=map[m]||map.delayed;return '<span class="vx-freshness" data-live="'+x[0]+'"><span class="vx-live-dot"></span>'+x[1]+'</span>';}
function num(x){return (x!==null&&x!==undefined&&!isNaN(x))?Number(x):null;}
/* lot 66 : métrique CANONIQUE d'abord (above200 — celle de la grammaire de
   régime et de Marchés), repli above50 — et la tuile porte l'ÉTIQUETTE de la
   métrique réellement affichée (le même chiffre, nommé pareil, partout). */
function breadthOf(sb){if(sb==null)return null;
  if(typeof sb==='object'){
    const a=num(sb.above200);if(a!=null)return{v:a,lbl:'>MM200'};
    const b=num(sb.above50);if(b!=null)return{v:b,lbl:'>MM50'};
    return null;}
  const n=num(sb);return n==null?null:{v:n,lbl:''};}
/* verdict → classe sémantique (achat=vert, attente=jaune, évite=rouge) */
function vCls(v){var s=String(v||'').toLowerCase();if(!s)return'';
  if(/(buy|achet|renforc|accumul|long\b|s\+)/.test(s))return'vx-pos';
  if(/(avoid|évit|evit|refus|réduir|reduir|sell|vendre|rejet)/.test(s))return'vx-neg';
  if(/(hold|attend|neutre|patience|surveil|watch)/.test(s))return'vx-warn';return'';}

/* Tuile KPI résumé — cliquable, pointe vers son domicile canonique. */
function kpiTile(label,value,cls,href){
  return '<a class="vx-card vx-card--compact vx-kpi vx-kpi-card" style="text-decoration:none;color:inherit" href="'+href+'" aria-label="'+esc(label)+'">'
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
    const lines=b.lines||[];
    const risk=b.main_risk||ed.main_risk||'';
    const opportunity=b.main_opportunity||ed.main_opportunity||'';
    const priced=ed.prices_mainly?('Aujourd’hui, le marché price principalement '+ed.prices_mainly):'';
    const decision=risk||opportunity||priced||lines[0]||'Aucune conclusion décisionnelle disponible avec les données actuelles.';
    const tone=risk?'risk':opportunity?'go':'neutral';
    $('vx-brief-body').innerHTML=
      '<p class="vx-today-decision" data-tone="'+tone+'">'+esc(decision)+'</p>'
      +'<div class="vx-card-footer"><span class="vx-meta">'+(b.generator==='deterministic'?'Conclusion déterministe · moteurs':'Conclusion éditoriale validée')+'</span>'
      +'<a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets">Voir les preuves →</a></div>';
    if(b.demo)$('vx-demo-banner').innerHTML='<div class="vx-demo-banner"><span class="vx-badge-demo">Démo</span> Données synthétiques clairement identifiées — jamais présentées comme réelles.</div>';
  }catch(e){$('vx-brief-body').innerHTML=VX.states.error('Brief indisponible ('+e.message+')');}
}

/* ── 4 KPI résumé cliquables (régime, breadth, VIX, meilleure opportunité) ── */
async function loadSummary(){
  const paint=(sum,reg,cmd)=>{
    sum=sum||{};reg=reg||{};cmd=cmd||{};
    const conf=Math.round((reg.confidence||0)*100);
    const br=breadthOf(sum.breadth);
    let vix=num(sum.vix);
    const best=(cmd.top_stocks||[])[0]||null;
    const regHtml=reg.regime?esc(reg.regime):'n/d';
    const brHtml=br!=null?(br.v+' %'):'n/d';
    const brCls=br!=null?(br.v>=55?'vx-pos':'vx-warn'):'';
    const vixHtml=vix!=null?vix:'n/d';
    const bestHtml=best?esc(best.symbol):'—';
    const kpis=[
      kpiTile('Régime',regHtml+' <span class="vx-meta">('+conf+'%)</span>','','/markets'),
      kpiTile('Breadth'+(br&&br.lbl?' '+br.lbl:''),brHtml,brCls,'/markets?view=breadth'),
      kpiTile('VIX',vixHtml,'','/markets?view=volatility'),
      best?kpiTile('Meilleure opp.',bestHtml,'','/analysis/'+encodeURIComponent(best.symbol)):kpiTile('Meilleure opp.','—','','/opportunities'),
    ].join('');
    $('vx-hero-kpis').innerHTML=kpis;
    /* Âge des quatre KPI. `scan_age` est en secondes ; absent → assess rend
       « — », l'aveu honnête, jamais une valeur inventée. La puce porte son
       instant de référence et se ré-évalue seule (VX.freshness._retick) :
       sans réseau, elle passe à « À actualiser » d'elle-même. */
    const sa=num(sum.scan_age);
    $('vx-hero-age').innerHTML='Données du scan : '
      +VX.freshness.chip(VX.freshness.assess({ageMs:sa!=null?sa*1000:null}));
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
    renderDiff({regime:reg.regime||null,breadth:br?br.v:null,vix:vix,best:best?best.symbol:null,
      opp:(cmd.top_stocks||[]).length});
  };
  /* Stale-while-revalidate : peinture IMMÉDIATE depuis le cache (même périmé, ex.
     au retour sur Aujourd'hui) puis revalidation en fond — jamais d'écran vide. */
  const cs=VX.fetch.peek('/api/market/summary'),cr=VX.fetch.peek('/api/market/regime'),cc=VX.fetch.peek('/api/command');
  if(cs||cr||cc) paint(cs&&cs.data,cr&&cr.data,cc&&cc.data);
  let sum={},reg={},cmd={};
  try{sum=await VX.fetch('/api/market/summary',{ttl:60000})||{};}catch(e){}
  try{reg=await VX.fetch('/api/market/regime',{ttl:120000})||{};}catch(e){}
  try{cmd=await VX.fetch('/api/command',{ttl:60000})||{};}catch(e){}
  paint(sum,reg,cmd);
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
      ? '<ul style="margin:0;padding-left:18px;line-height:1.9;font-size:13px">'+rows.slice(0,3).map(r=>'<li>'+r+'</li>').join('')+'</ul>'
        +'<div class="vx-meta vx-mt2">Depuis '+esc(new Date(prev.ts).toLocaleString('fr-FR'))+'</div>'
      : '<div class="vx-state" data-state="empty"><div class="vx-state-icon">=</div><div><b>Rien de significatif n’a changé</b><br><span class="vx-meta">depuis '+esc(new Date(prev.ts).toLocaleString('fr-FR'))+'</span></div></div>';
  }
  host.insertAdjacentHTML('beforeend','<div class="vx-meta vx-mt2">Source : comparaison locale de cette session</div>');
  try{localStorage.setItem('vxTodayBaseline',JSON.stringify(Object.assign({},cur,{ts:Date.now()})));}catch(e){}
}

/* ── Régime : objet REGIME AURA (widget officiel W01) — atmosphère + confiance
   + grammaire (marché/breadth/VIX) + verdict risque neuf, câblé aux moteurs. ── */
async function loadRegime(){
  try{
    const [r,sum,ed]=await Promise.all([
      VX.fetch('/api/market/regime',{ttl:120000}),
      VX.fetch('/api/market/summary',{ttl:60000}).catch(()=>({})),
      VX.fetch('/api/briefing/editorial',{ttl:60000}).catch(()=>({}))]);
    const adj=(r&&r.adjustments)||{};
    const inval=(ed&&(ed.main_risk||(ed.daily&&ed.daily.main_risk)))||'';
    const grammar={roro:(sum&&sum.roro)||null,
      breadth:(sum&&sum.breadth&&num(sum.breadth.above200)),
      vix:num(sum&&sum.vix)};
    $('vx-regime-body').innerHTML=
      '<div id="vx-regime-object" class="vx-mb2"></div>'
      +'<div class="vx-kv"><span class="k">Confirmations exigées</span><span class="v">'+VX.fmt.nd(adj.confirmation_required)+'</span></div>'
      +'<div class="vx-card-footer"><a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/markets?view=breadth">Participation →</a></div>';
    if(window.VXCharts&&VXCharts.regimeAura){
      /* LOT 629 — `||0` transformait une confiance ABSENTE en « 0 % confiance »,
         un chiffre inventé affiché comme mesure. Absente → null, et l’objet
         affiche « confiance n/d » avec sa couronne éteinte. */
      VXCharts.regimeAura('vx-regime-object',{regime:r&&r.regime,
        confidence:(r&&r.confidence!=null&&!isNaN(r.confidence))?Math.round(r.confidence*100):null,
        newRisk:(adj.new_risk_allowed===undefined?null:!!adj.new_risk_allowed),
        invalidation:inval,grammar:grammar,
        source:'Moteur de régimes',timestamp:r&&(r.as_of||r.timestamp||r.updated)||null,mode:'delayed'});
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
      +'<span class="vx-badge '+vCls(s.verdict)+'">'+esc(s.verdict||'')+'</span>'
      +'<span class="vx-grow vx-truncate vx-dim" style="font-size:12px" title="'+esc(s.note||'')+'">'+esc(s.note||'')+'</span>'
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
      +'<span class="vx-badge vx-warn">armée</span></div>').join('');
    $('vx-alerts').innerHTML=(srv+rows)||VX.states.emptyDesk('Aucune alerte active.',
      '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'alert\')">Créer une alerte</button>');
  }catch(e){$('vx-alerts').innerHTML=VX.states.error('Alertes indisponibles');}
}

/* ── Catalyseurs : objet CATALYST RUNWAY (widget officiel W-CR) — piste DTE +
   impact, prochain catalyseur priorisé, câblé au calendrier moteur. ── */
async function loadCalendar(){
  try{
    const cal=await VX.fetch('/cal-feed',{ttl:300000});
    const events=[...(cal.macro||[]).map(m=>({label:m.label,dte:m.dte,
        impact:(m.importance==='haute')?'high':(m.importance==='moyenne'?'med':'low')})),
      ...(cal.items||[]).filter(it=>it&&it.dte!=null).slice(0,4).map(it=>({label:(it.sym||'Résultats'),dte:it.dte,impact:'high'}))]
      .filter(e=>e.dte!=null&&!isNaN(e.dte));
    VXCharts.catalystRunway('vx-calendar',{title:'Catalyseurs imminents',question:'Quels catalyseurs arrivent, et quand ?',
      events,source:'calendrier moteur',timestamp:cal.ts||Date.now(),mode:'delayed',
      emptyText:'Aucun catalyseur imminent identifié.'});
  }catch(e){$('vx-calendar').innerHTML='<div class="vx-card">'+VX.states.error('Calendrier indisponible')+'</div>';}
}

/* ── Portefeuille : ce qui a changé (compact) ── */
async function loadPortfolio(){
  const pos=(E()&&E().positions())||[];
  if(!pos.length){
    $('vx-portfolio').innerHTML=VX.states.emptyDesk('Aucune position déclarée.',
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

/* ── Session d'analyse : fraîcheur compacte, sans répéter les KPI du hero. ── */
function sessAge(s){if(s==null)return'';if(s<60)return'il y a '+s+' s';if(s<3600)return'il y a '+Math.round(s/60)+' min';return'il y a '+Math.round(s/3600)+' h';}
function sessRender(d){
  const el=$('vx-asess');if(!el)return;
  const st=d.state||'analyzing';
  const live=st==='ready';
  const stLabel=live?'Analyse à jour':st==='restored'?'Analyse restaurée · rafraîchissement…':'Analyse en cours…';
  const when=d.as_of?esc(String(d.as_of)):sessAge(d.age_s);
  const confidence=d.confidence!=null?('couverture '+esc(d.confidence)+' %'):'couverture n/d';
  el.innerHTML='<div class="vx-ss-card" data-state="'+st+'">'
    +'<div class="vx-ss-head"><span class="vx-ss-dot'+(live?' live':'')+'" aria-hidden="true"></span>'
    +'<span class="vx-ss-title">Fraîcheur de l’analyse</span>'
    +'<span class="vx-ss-state">'+stLabel+'</span>'
    +'<span class="vx-grow"></span>'
    +'<span class="vx-meta">'+when+' · '+confidence+(d.demo?' · démo':' · moteurs')+' · lecture seule</span></div></div>';
}
async function loadSession(){
  try{
    const r=await fetch('/api/session/digest',{cache:'no-store'});
    sessRender(await r.json());
  }catch(e){const el=$('vx-asess');if(el)el.innerHTML='';}
}

/* ── Orchestration ── */
function boot(){
  loadSession();
  loadBrief();loadSummary();loadRegime();loadOpportunities();loadAlerts();loadCalendar();loadPortfolio();loadMarketDiff();
}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}
whenChartsReady(boot);
/* Diff MARCHÉ serveur (SKYLER LOT 8b) : MarketContext — transition de régime,
   changements depuis la dernière session, conflits de sources. Vérité serveur,
   jamais inventé : sans session précédente, on le dit. */
async function loadMarketDiff(){
  const host=$('vx-mkt-diff');if(!host)return;
  try{
    const d=await VX.fetch('/api/market/context',{ttl:120000});
    const tr=(d.regime||{}).transition||{};
    const changes=(d.changes_since_prev||[]).slice(0,3);
    const conflicts=(d.conflicts||[]).slice(0,1);
    let html='<div class="vx-eyebrow" style="margin-bottom:.25rem">Marché (serveur)</div>';
    if(tr.changed===true){
      html+='<div class="vx-mb1"><span class="vx-badge" data-tone="neutral">Régime : '
        +esc(tr.from||'—')+' → '+esc(tr.to||'—')+'</span></div>';
    }
    if(changes.length){
      html+='<ul style="margin:.2rem 0;padding-left:0;list-style:none;font-size:12.5px">'
        +changes.map(c=>'<li style="margin:.2rem 0">· '+esc(c)+'</li>').join('')+'</ul>';
    }else if(tr.changed===null){
      html+='<div class="vx-muted" style="font-size:12.5px">Première session enregistrée — pas de comparaison disponible.</div>';
    }else{
      html+='<div class="vx-muted" style="font-size:12.5px">Aucun changement de marché depuis la dernière session.</div>';
    }
    if(conflicts.length){
      html+='<div class="vx-warn" style="font-size:12.5px;margin-top:.25rem">⚠ '
        +conflicts.map(c=>esc(c.dimension)+' : sources en désaccord ('+(c.values||[]).join(' vs ')+')').join(' · ')+'</div>';
    }
    html+='<div class="vx-meta" style="margin-top:.25rem">'+(d.as_of?('scan '+esc(d.as_of)+' · '):'')+'MarketContext déterministe</div>';
    host.innerHTML=html;
  }catch(e){host.innerHTML='<div class="vx-muted" style="font-size:12.5px">Diff marché injoignable.</div>';}
}
VX.refresh.register(loadMarketDiff,300000,'today-mkt-diff');
VX.refresh.register(loadSummary,120000,'today-summary');
VX.refresh.register(loadAlerts,60000,'alerts');
VX.refresh.register(loadSession,45000,'session-digest');
VX.bus.on('vx:position-changed',loadPortfolio);
VX.bus.on('vx:alert-changed',loadAlerts);
VX.bus.on('vx:data-refreshed',()=>{loadSession();loadBrief();loadSummary();loadRegime();});
})();
</script>
"""


def render(scan_state: dict | None = None) -> str:
    content = _CONTENT.replace('%%LOADING%%',
                               '<div class="vx-skeleton" style="height:60px"></div>')
    return render_shell(title="Aujourd'hui", active='briefing', space_label="Aujourd'hui",
                        sub_label='Résumé du jour', content=content, page_js=_JS,
                        page_label="Aujourd'hui")
