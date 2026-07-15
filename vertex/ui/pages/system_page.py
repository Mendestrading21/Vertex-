"""vertex.ui.pages.system_page — l'espace Système (§29).

Question : « Le système est-il en bonne santé et branché sur du réel ? ».
Quatre sous-vues : connections (IBKR / TradingView / Claude / sync / stockage),
data (qualité + fraîcheur par domaine), settings (préférences locales +
export/import desk), archive (coffre vxVault).

Invariant produit affirmé partout : READONLY — aucun ordre possible
(disabled-by-design). Donnée absente → état vide honnête avec action.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

VIEWS = (
    ('connections', 'Connexions'),
    ('data', 'Données'),
    ('automations', 'Automatisations'),
    ('settings', 'Réglages'),
    ('archive', 'Archive'),
)
_DEFAULT_VIEW = 'connections'


def _tabs(active: str) -> str:
    tabs = ''.join(
        f'<a class="vx-tab" role="tab" href="?view={vid}" '
        f'aria-selected="{"true" if vid == active else "false"}">{label}</a>'
        for vid, label in VIEWS)
    # Référence visuelle (§50) — lien vers la page Design System, à droite.
    ds = ('<a class="vx-tab" href="/design-system" style="margin-left:auto;color:var(--vx-copper-light)" '
          'title="Référence visuelle OBSIDIAN COPPER">Design System</a>')
    return f'<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Système">{tabs}{ds}</nav>'


def _header(active: str) -> str:
    return f'''<div class="vx-page-header">
  <div><h1>Système</h1>
  <div class="vx-sub">Le système est-il en bonne santé et branché sur du réel ?</div></div>
</div>
<div class="vx-insight vx-mb3" data-tone="risk" id="vx-readonly-invariant">
  <b>READONLY — aucun ordre possible (disabled-by-design).</b>
  Vertex est un terminal d&#8217;analyse : il lit, il n&#8217;ex&eacute;cute jamais.
  <span id="vx-readonly-confirm" class="vx-meta"></span></div>
{_tabs(active)}'''


_VIEW_CONTENT = {
    'connections': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-4" aria-label="Santé du système">
    <div class="vx-card-header"><span class="vx-card-title">Santé — moteurs</span>
      <span class="vx-chart-question">Les moteurs tournent-ils ?</span></div>
    <div id="vx-sys-gauge"><div class="vx-skeleton" style="height:118px"></div></div>
    <div class="vx-card-footer"><span class="vx-meta">% de moteurs au statut « ok » — donnée réelle, aucun score inventé.</span></div>
  </section>
  <div class="vx-col-8"><div class="vx-grid" id="vx-sys-kpis"><div class="vx-skeleton" style="height:70px"></div></div></div>
</div>
<section class="vx-card vx-mt4" id="vx-conn-summary" aria-label="Canaux de connexion">
  <div class="vx-card-header"><span class="vx-card-title">Canaux — état honnête</span>
    <span class="vx-dim" style="font-size:12px">configuré ≠ connecté · jamais LIVE sans preuve</span></div>
  <div id="vx-conn-summary-body">%%LOADING%%</div>
</section>
<div class="vx-grid vx-mt4" id="vx-conn-grid">
  <section class="vx-card vx-col-4" aria-label="IBKR">
    <div class="vx-card-header"><span class="vx-card-title">IBKR</span>
      <span id="vx-conn-ibkr-badge"></span></div>
    <div id="vx-conn-ibkr">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" aria-label="TradingView">
    <div class="vx-card-header"><span class="vx-card-title">TradingView</span>
      <span id="vx-conn-tv-badge"></span></div>
    <div id="vx-conn-tv">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-4" aria-label="Claude (IA)">
    <div class="vx-card-header"><span class="vx-card-title">Claude (IA)</span>
      <span id="vx-conn-ai-badge"></span></div>
    <div id="vx-conn-ai">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Cerveau Claude — enrichissement web">
    <div class="vx-card-header">
      <span class="vx-card-title">Cerveau Claude &mdash; donn&eacute;es web &agrave; jour</span>
      <span class="vx-actions">
        <span id="vx-brain-badge"></span>
        <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-brain-refresh">Mettre &agrave; jour avec Claude</button></span></div>
    <div class="vx-help vx-mb2">Quand l&#8217;acc&egrave;s live manque, Claude va chercher les vraies donn&eacute;es du jour
      sur le web (cotations diff&eacute;r&eacute;es, actualit&eacute;s) &mdash; toujours <b>sourc&eacute;es</b> et &eacute;tiquet&eacute;es
      <span class="vx-badge" style="color:var(--vx-orange-500,#cf6128);border:1px solid var(--vx-orange-500,#cf6128)">via Claude · web · diff&eacute;r&eacute;</span>,
      jamais d&eacute;guis&eacute;es en donn&eacute;e broker r&eacute;elle. Aucun chiffre invent&eacute;.</div>
    <div id="vx-brain-body">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Synchronisation">
    <div class="vx-card-header"><span class="vx-card-title">Synchronisation</span>
      <span id="vx-conn-sync-badge"></span></div>
    <div id="vx-conn-sync">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Stockage">
    <div class="vx-card-header"><span class="vx-card-title">Stockage &amp; sant&eacute;</span>
      <span id="vx-conn-store-badge"></span></div>
    <div id="vx-conn-store">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Moteurs">
    <div class="vx-card-header"><span class="vx-card-title">Moteurs</span>
      <span class="vx-actions" id="vx-conn-meta"></span></div>
    <div id="vx-conn-engines">%%LOADING%%</div>
  </section>
</div>''',

    'data': '''
<div class="vx-grid vx-mt4">
  <div class="vx-col-5" id="vx-data-quality-chart"></div>
  <section class="vx-card vx-col-7" aria-label="Dernier scan">
    <div class="vx-card-header"><span class="vx-card-title">Dernier scan &amp; m&eacute;triques</span>
      <span class="vx-actions">
        <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-data-refresh">Actualiser</button></span></div>
    <div id="vx-data-scan">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Fra&icirc;cheur par domaine">
    <div class="vx-card-header"><span class="vx-card-title">Fra&icirc;cheur par domaine</span>
      <span class="vx-actions" id="vx-data-fresh-meta"></span></div>
    <div id="vx-data-fresh">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Titres d&eacute;grad&eacute;s">
    <div class="vx-card-header"><span class="vx-card-title">Titres en qualit&eacute; d&eacute;grad&eacute;e</span></div>
    <div id="vx-data-degraded">%%LOADING%%</div>
  </section>
</div>''',

    'automations': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="Jobs de fond">
    <div class="vx-card-header"><span class="vx-card-title">Automatisations (§24)</span>
      <span class="vx-meta vx-right">priorit&eacute; : positions &gt; stops &gt; options &gt; risques &gt; d&eacute;cisions &gt; univers</span></div>
    <div id="vx-auto-jobs">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-5" aria-label="Rapport de d&eacute;marrage">
    <div class="vx-card-header"><span class="vx-card-title">Startup report (§10)</span></div>
    <div id="vx-auto-startup">%%LOADING%%</div>
  </section>
</div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Configuration">
    <div class="vx-card-header"><span class="vx-card-title">Configuration (statuts — aucune valeur affich&eacute;e)</span></div>
    <div id="vx-auto-config">%%LOADING%%</div>
  </section>
</div>
''',
    'settings': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" aria-label="Affichage">
    <div class="vx-card-header"><span class="vx-card-title">Affichage</span></div>
    <div class="vx-kv"><span class="k">Densit&eacute;</span><span class="v">
      <span class="vx-segmented" role="group" aria-label="Densit&eacute;">
        <button data-density-btn="compact" aria-pressed="false">Compact</button>
        <button data-density-btn="confort" aria-pressed="true">Confort</button>
        <button data-density-btn="dense" aria-pressed="false">Dense</button>
      </span></span></div>
    <div class="vx-kv"><span class="k">Navigation lat&eacute;rale</span><span class="v">
      <span class="vx-segmented" role="group" aria-label="Sidebar">
        <button data-sidebar-btn="expanded" aria-pressed="false">D&eacute;ploy&eacute;e</button>
        <button data-sidebar-btn="collapsed" aria-pressed="false">R&eacute;duite</button>
      </span></span></div>
    <div class="vx-kv"><span class="k">Notifications push</span><span class="v">
      <span class="vx-segmented" role="group" aria-label="Notifications">
        <button data-notif-btn="1" aria-pressed="false">Activ&eacute;es</button>
        <button data-notif-btn="0" aria-pressed="false">Coup&eacute;es</button>
      </span></span></div>
    <div class="vx-kv"><span class="k">Langue</span>
      <span class="v">Fran&ccedil;ais <span class="vx-meta">(interface FR uniquement pour l&#8217;instant)</span></span></div>
    <div class="vx-help vx-mt2">Pr&eacute;f&eacute;rences purement locales (localStorage de ce navigateur) —
      elles ne touchent ni les moteurs ni les donn&eacute;es desk.</div>
  </section>
  <section class="vx-card vx-col-6" aria-label="Donn&eacute;es desk">
    <div class="vx-card-header"><span class="vx-card-title">Donn&eacute;es desk (export / import)</span></div>
    <div id="vx-settings-desk">%%LOADING%%</div>
    <div class="vx-flex vx-wrap vx-gap2 vx-mt3">
      <button class="vx-btn vx-btn-primary" id="vx-desk-export">Exporter (JSON)</button>
      <label class="vx-btn" for="vx-desk-import-file" style="cursor:pointer">Importer un JSON&hellip;</label>
      <input type="file" id="vx-desk-import-file" accept="application/json,.json" hidden />
    </div>
    <div class="vx-help vx-mt2">L&#8217;export t&eacute;l&eacute;charge vos cl&eacute;s desk telles quelles
      (positions, journal, alertes, coffre&hellip;). L&#8217;import demande confirmation avant
      toute &eacute;criture — aucune cl&eacute; n&#8217;est renomm&eacute;e, le protocole de sync reste intact.</div>
  </section>
</div>''',

    'archive': '''
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Coffre — archive">
    <div class="vx-card-header"><span class="vx-card-title">Coffre (archive interne)</span>
      <span class="vx-actions">
        <button class="vx-btn vx-btn-sm" id="vx-vault-new">Nouvelle entr&eacute;e</button>
        <button class="vx-btn vx-btn-sm vx-btn-ghost" id="vx-vault-export">Exporter (JSON)</button></span></div>
    <div class="vx-flex vx-wrap vx-gap2 vx-mb3">
      <input class="vx-input" id="vx-vault-search" type="search"
        placeholder="Recherche plein texte (titre, contenu, tags)"
        aria-label="Rechercher dans le coffre" style="max-width:340px"
        data-filter-key="q" />
      <span id="vx-vault-chips" role="group" aria-label="Filtrer par type"
        class="vx-flex vx-wrap vx-gap2"></span>
    </div>
    <div id="vx-vault-list">%%LOADING%%</div>
  </section>
</div>''',
}


_JS = r"""
<script src="/static/vertex/js/charts/donut-chart.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script>
(function(){
'use strict';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
const ROOT=document.getElementById('vx-system');
const VIEW=(ROOT&&ROOT.dataset.view)||'connections';
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function whenChartsReady(fn){
  if(window.VXCharts&&window.Chart)return fn();
  window.addEventListener('load',fn,{once:true});
}
function statusBadge(status,label){
  return `<span class="vx-badge vx-badge-status" data-status="${esc(status)}">${esc(label||status)}</span>`;
}
function kv(k,v){return `<div class="vx-kv"><span class="k">${k}</span><span class="v">${v}</span></div>`;}

/* Bandeau consolidé des canaux — /api/system/connections (statuts canoniques). */
async function loadConnSummary(){
  const el=document.getElementById('vx-conn-summary-body');if(!el)return;
  let d;try{d=await VX.fetch('/api/system/connections',{ttl:20000});}catch(e){el.innerHTML=VX.states.error('Connexions indisponibles');return;}
  const tone={LIVE:'pos',READY:'pos',DELAYED:'warn',DEGRADED:'warn',FALLBACK:'warn',STALE:'warn',
    OFFLINE:'neg',ERROR:'neg',BLOCKED:'neg',CONFIGURATION_MISSING:'neutral',NOT_IMPLEMENTED:'neutral',DEMO:'neutral',LOADING:'neutral'};
  const col={pos:'var(--vx-positive,#39b879)',warn:'var(--vx-warning,#cc892c)',neg:'var(--vx-negative,#dc6254)',neutral:'var(--vx-text-dim,#817d77)'};
  const rows=(d.connections||[]).map(function(c){
    const t=tone[c.status]||'neutral';
    return '<div style="display:grid;grid-template-columns:150px 130px 1fr;gap:.6rem;align-items:center;padding:.4rem 0;border-bottom:1px solid rgba(255,255,255,.05)">'
      +'<b>'+esc(c.name)+'</b>'
      +'<span class="vx-badge" style="color:'+col[t]+';border:1px solid '+col[t]+'">'+esc(c.status)+'</span>'
      +'<span class="vx-dim" style="font-size:12.5px">'+esc(c.detail||'')+(c.action?' <span style="color:var(--vx-orange-500,#cf6128)">→ '+esc(c.action)+'</span>':'')+'</span></div>';
  }).join('');
  el.innerHTML=rows||'<div class="vx-empty">Aucun canal.</div>';
}

/* Cerveau Claude+web — /api/ai/status + /api/ai/enrichment (provenance honnête). */
const BRAIN_TONE={OK:['live','à jour'],DEGRADED:['delayed','partiel'],
  MISSING:['frozen','indisponible'],EMPTY:['frozen','jamais lancé']};
function brainCitations(cits){
  if(!cits||!cits.length)return '';
  return '<div class="vx-flex vx-wrap vx-gap2" style="margin-top:.2rem">'
    +cits.slice(0,4).map(c=>`<a class="vx-badge vx-badge-ghost" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer"
       style="font-size:11px" title="${esc(c.url)}">↗ ${esc((c.title||c.url).slice(0,42))}</a>`).join('')+'</div>';
}
async function loadBrain(){
  const body=$('vx-brain-body');if(!body)return;
  let st,snap;
  try{
    [st,snap]=await Promise.all([
      VX.fetch('/api/ai/status',{ttl:8000}),
      VX.fetch('/api/ai/enrichment',{ttl:8000})]);
  }catch(e){body.innerHTML=VX.states.error('Cerveau Claude injoignable');return;}
  const status=(st&&st.status)||'EMPTY';
  const tn=BRAIN_TONE[status]||['frozen','—'];
  $('vx-brain-badge').innerHTML=statusBadge(tn[0],tn[1]);
  const quotes=(snap&&snap.surfaces&&snap.surfaces.quotes)||{};
  const news=(snap&&snap.surfaces&&snap.surfaces.news)||{};
  const found=st&&st.quotes_found!=null?st.quotes_found:0;
  let head=kv('&Eacute;tat',statusBadge(tn[0],status)+' <span class="vx-dim" style="font-size:12px">'+esc((st&&st.note)||'')+'</span>')
    +kv('Mod&egrave;le',esc((st&&st.model)||'—'))
    +kv('Derni&egrave;re analyse',(snap&&snap.as_of)?VX.fmt.ago(Date.parse(snap.as_of)):'&mdash;')
    +kv('Cotations trouv&eacute;es',VX.fmt.nd(found)+' / '+VX.fmt.nd((st&&st.symbols)||0)+' <span class="vx-dim" style="font-size:12px">(diff&eacute;r&eacute;es, sourc&eacute;es)</span>');
  const syms=Object.keys(quotes).filter(s=>quotes[s]&&quotes[s].value!=null).slice(0,12);
  /* Plus forts mouvements du jour (change_pct réel déjà servi) en barres signées — au-dessus
     du tableau texte. Émeraude/corail par signe (hex, Chart.js ne résout pas var(--x)). */
  const movers=Object.keys(quotes).filter(s=>quotes[s]&&quotes[s].change_pct!=null)
    .sort((a,b)=>Math.abs(quotes[b].change_pct)-Math.abs(quotes[a].change_pct)).slice(0,8);
  let table='';
  if(syms.length){
    table='<div class="vx-divider"></div><div style="overflow-x:auto"><table class="vx-table">'
      +'<thead><tr><th>Titre</th><th class="vx-num">Cours (diff&eacute;r&eacute;)</th><th>Provenance</th><th>Actualit&eacute;</th></tr></thead><tbody>'
      +syms.map(s=>{
        const q=quotes[s];const n=news[s]&&news[s].value&&news[s].value[0];
        const chg=q.change_pct!=null?(' <span class="'+(q.change_pct>=0?'vx-pos':'vx-neg')+'">'+(q.change_pct>=0?'+':'')+VX.fmt.num(q.change_pct,2)+'%</span>'):'';
        const impactCls=n?({HAUSSIER:'vx-pos',BAISSIER:'vx-neg',NEUTRE:'vx-dim'}[n.impact]||'vx-dim'):'';
        return '<tr><td><b>'+esc(s)+'</b></td>'
          +'<td class="vx-num vx-mono">'+VX.fmt.num(q.value,2)+' '+esc(q.currency||'')+chg+'</td>'
          +'<td><span class="vx-badge" style="color:var(--vx-warning,#dda23b);border:1px solid var(--vx-warning,#dda23b);font-size:11px">'+esc(q.source_label||'via Claude · web')+'</span>'+brainCitations(q.citations)+'</td>'
          +'<td class="'+impactCls+'" style="font-size:12px">'+(n?esc(n.impact)+' — '+esc((n.headline||'').slice(0,64)):'<span class="vx-dim">—</span>')+'</td></tr>';
      }).join('')+'</tbody></table></div>';
  }else if(status==='MISSING'){
    table='<div class="vx-insight vx-mt2" data-tone="neutral">Analyse Claude+web <b>indisponible</b> — ajoute '
      +'<span class="vx-mono">ANTHROPIC_API_KEY</span> dans <span class="vx-mono">.env</span> pour activer le cerveau. '
      +'En attendant, l&#8217;app sert les donn&eacute;es r&eacute;elles/moteur uniquement (aucun chiffre invent&eacute;).</div>';
  }else{
    table='<div class="vx-empty vx-mt2">Aucune cotation web pour l&#8217;instant. « Mettre &agrave; jour avec Claude » pour lancer une recherche.</div>';
  }
  body.innerHTML=head+(movers.length?'<div id="vx-brain-movers" class="vx-mt3"></div>':'')+table
    +'<div class="vx-card-footer">'+VX.updateIndicator((snap&&snap.as_of)?Date.parse(snap.as_of):Date.now(),'/api/ai/enrichment',status==='OK'?'delayed':'fallback')
    +' · rendements/prix 100% diff&eacute;r&eacute;s &mdash; jamais un ordre</div>';
  if(window.VXCharts&&VXCharts.barCard&&movers.length){
    VXCharts.barCard('vx-brain-movers',{title:'Plus forts mouvements du jour',
      labels:movers,values:movers.map(s=>quotes[s].change_pct),
      colors:movers.map(s=>quotes[s].change_pct>=0?'#36c889':'#ed655c'),
      horizontal:true,yFmt:(v)=>v+'%',source:'via Claude · web',
      timestamp:(snap&&snap.as_of)?Date.parse(snap.as_of):Date.now(),mode:'delayed'});
  }
}
async function refreshBrain(){
  const btn=$('vx-brain-refresh');
  if(btn){btn.disabled=true;btn.textContent='Recherche Claude…';}
  try{
    const r=await fetch('/api/ai/refresh',{method:'POST'});
    const d=await r.json().catch(()=>({}));
    VX.toast(d.note||'Enrichissement Claude lancé', r.ok?'success':'error');
  }catch(e){VX.toast('Mise à jour impossible : '+e.message,'error');}
  /* Laisse le temps à la tâche de fond, puis rafraîchit l'affichage. */
  setTimeout(()=>{ if(btn){btn.disabled=false;btn.textContent='Mettre à jour avec Claude';} loadBrain(); }, 3500);
}

/* TradingView — liste globale des signaux récents (tous titres) + aide setup. */
const TV_BULL2=['SUPPORT_RECLAIM','BREAKOUT_CONFIRMED','BREAKOUT_RETEST','MOMENTUM_ACCELERATION','VOLUME_EXPANSION','TREND_ALIGNMENT'];
const TV_BEAR2=['FAILED_BREAKOUT','THESIS_INVALIDATION'];
function tvDirBadge(sig){
  const up=TV_BULL2.indexOf(sig)>=0,dn=TV_BEAR2.indexOf(sig)>=0;
  const c=up?'vx-pos':(dn?'vx-neg':'vx-dim'),t=up?'haussier':(dn?'baissier':'contextuel');
  return '<span class="vx-badge '+c+'" style="font-size:11px">'+t+'</span>';
}
async function loadTvSignals(){
  const host=$('vx-tv-signals');if(!host)return;
  let d;try{d=await VX.fetch('/api/tradingview/signals',{ttl:15000});}catch(e){host.innerHTML='';return;}
  const sigs=(d.signals||[]).slice().reverse();   // plus récent d'abord
  if(!sigs.length){host.innerHTML='<div class="vx-empty" style="margin-top:.6rem">Aucun signal reçu pour l\'instant — la liste se remplira à la première alerte TradingView.</div>';return;}
  host.innerHTML='<div class="vx-divider"></div><div class="vx-meta vx-mb1">Signaux récents — tous titres (plus récent d\'abord)</div>'
    +'<div style="overflow-x:auto"><table class="vx-table"><thead><tr><th>Titre</th><th>Signal</th><th>Sens</th><th>Reçu</th><th></th></tr></thead><tbody>'
    +sigs.slice(0,20).map(function(s){
      return '<tr><td><b>'+esc(s.symbol)+'</b></td><td class="vx-mono" style="font-size:12px">'+esc(s.signal)+'</td>'
        +'<td>'+tvDirBadge(s.signal)+'</td>'
        +'<td class="vx-meta">'+VX.fmt.ago((s.received_ts||0)*1000)+(s.fresh===false?' <span class="vx-badge">rassis</span>':'')+'</td>'
        +'<td><a class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" href="/analysis/'+esc(s.symbol)+'">Analyser →</a></td></tr>';
    }).join('')+'</tbody></table></div>';
}
function openTvSetup(){
  const origin=location.origin;
  const url=origin+'/api/tradingview/webhook';
  const codes=['SUPPORT_RECLAIM','BREAKOUT_CONFIRMED','BREAKOUT_RETEST','MOMENTUM_ACCELERATION',
    'VOLUME_EXPANSION','VOLATILITY_COMPRESSION','VOLATILITY_EXPANSION','TREND_ALIGNMENT',
    'CORRECTION_DEEP','FAILED_BREAKOUT','THESIS_INVALIDATION'];
  const payload='{\n  "secret": "TON_SECRET",\n  "symbol": "{{ticker}}",\n  "signal": "BREAKOUT_CONFIRMED",\n  "timestamp": {{timenow}},\n  "price": {{close}}\n}';
  VX.shell.openDrawer('Configurer ton alerte TradingView',
    '<div class="vx-help">Une alerte TradingView pointée ici déclenche une <b>réévaluation</b> Vertex — <b>jamais un ordre</b>. Suis ces 4 étapes.</div>'
    +'<ol style="padding-left:1.1rem;line-height:1.9;font-size:13px">'
    +'<li>Dans <span class="vx-mono">.env</span>, définis <span class="vx-mono">TRADINGVIEW_WEBHOOK_SECRET</span> (un mot de passe à toi) puis relance Vertex.</li>'
    +'<li>Sur TradingView : <b>Créer une alerte</b> → onglet <b>Notifications</b> → coche <b>Webhook URL</b> et colle :</li></ol>'
    +'<div class="vx-kv"><span class="k">URL webhook</span><span class="v"><code class="vx-mono" style="font-size:12px">'+esc(url)+'</code> '
    +'<button class="vx-btn vx-btn-sm" id="vx-tv-copy-url">Copier</button></span></div>'
    +'<ol start="3" style="padding-left:1.1rem;line-height:1.9;font-size:13px">'
    +'<li>Dans le <b>message</b> de l\'alerte, colle ce corps JSON (remplace <span class="vx-mono">TON_SECRET</span> par ton secret) :</li></ol>'
    +'<pre class="vx-mono" style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:12px;overflow-x:auto;font-size:12px">'+esc(payload)+'</pre>'
    +'<button class="vx-btn vx-btn-sm vx-mb2" id="vx-tv-copy-payload">Copier le corps JSON</button>'
    +'<ol start="4" style="padding-left:1.1rem;line-height:1.9;font-size:13px">'
    +'<li>Change <span class="vx-mono">"signal"</span> selon ton alerte. Codes acceptés :</li></ol>'
    +'<div class="vx-flex vx-wrap vx-gap2">'+codes.map(function(c){return '<span class="vx-badge vx-mono" style="font-size:11px">'+c+'</span>';}).join('')+'</div>'
    +'<div class="vx-help vx-mt3">Astuce : le script Pine prêt à l\'emploi est dans <span class="vx-mono">tradingview/vertex_signals.pine</span> — il émet déjà ce JSON avec les bons codes.</div>');
  document.getElementById('vx-tv-copy-url')?.addEventListener('click',function(){navigator.clipboard&&navigator.clipboard.writeText(url);VX.toast('URL webhook copiée','success');});
  document.getElementById('vx-tv-copy-payload')?.addEventListener('click',function(){navigator.clipboard&&navigator.clipboard.writeText(payload);VX.toast('Corps JSON copié','success');});
}

/* ══ Vue CONNEXIONS ═════════════════════════════════════════════════ */
async function loadConnections(){
  loadConnSummary();
  loadBrain();
  const [stR,liveR,diagR,hzR]=await Promise.allSettled([
    VX.fetch('/api/system-status',{ttl:30000}),
    VX.fetch('/api/live/status',{ttl:30000}),
    VX.fetch('/api/system/diagnostics',{ttl:30000}),
    VX.fetch('/healthz',{ttl:30000})]);
  const st=stR.status==='fulfilled'?stR.value:null;
  const live=liveR.status==='fulfilled'?liveR.value:null;
  const diag=diagR.status==='fulfilled'?diagR.value:null;
  const hz=hzR.status==='fulfilled'?hzR.value:null;

  /* Hero santé (jauge % moteurs ok) + bande KPI command center — §41.
     Agrégations RÉELLES des payloads (statuts moteurs, fraîcheur, warnings,
     scan, IA) ; aucun chiffre inventé, jamais 0 pour une valeur absente. */
  try{
    var _eng=(st&&st.engines)||[];
    var _ok=_eng.filter(function(e){return e&&e.status==='ok';}).length;
    var _fr=(st&&st.freshness)||{}, _frK=Object.keys(_fr);
    var _frOk=_frK.filter(function(k){return _fr[k]&&_fr[k].state==='fresh';}).length;
    var _warn=((st&&st.warnings)||[]).length;
    var _sym=(st&&st.scan&&st.scan.symbols); if(_sym==null&&diag&&diag.scan)_sym=diag.scan.rows;
    var _ai=(diag&&diag.ai)||{};
    var _pct=_eng.length?Math.round(_ok/_eng.length*100):null;
    whenChartsReady(function(){ if(window.VXCharts&&VXCharts.gauge) VXCharts.gauge('vx-sys-gauge',{
      value:_pct,min:0,max:100,unit:'%',label:'Moteurs OK',
      reading:_eng.length?(_ok+'/'+_eng.length+' moteurs opérationnels'):'moteurs inconnus',
      bands:[{to:60,color:VXCharts.colors.negative},{to:85,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.positive}]}); });
    var _kp=function(l,v,d,cls){return '<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 4"><span class="vx-kpi-label">'+l+'</span><span class="vx-kpi-value" style="font-size:22px">'+v+'</span>'+(d?'<span class="vx-kpi-delta '+(cls||'vx-muted')+'">'+d+'</span>':'')+'</div>';};
    var _kh=$('vx-sys-kpis');
    if(_kh)_kh.innerHTML=
      _kp('Moteurs',_eng.length?(_ok+'/'+_eng.length):'—','opérationnels',(_eng.length&&_ok===_eng.length)?'vx-pos':'')
      +_kp('Données fraîches',_frK.length?(_frOk+'/'+_frK.length):'—','domaines')
      +_kp('Erreurs',_warn,_warn===0?'aucune':'à voir',_warn===0?'vx-pos':'vx-neg')
      +_kp('Scan',_sym!=null?_sym:'—','titres')
      +_kp('Appels IA',_ai.total!=null?(_ai.ok+'/'+_ai.total):'—',(_ai.fallbacks?(_ai.fallbacks+' repli'):'ok'))
      +_kp('Lecture seule',(st&&st.readonly)?'✓':'⚠',(st&&st.readonly)?'aucun ordre':'à vérifier',(st&&st.readonly)?'vx-pos':'vx-neg');
  }catch(e){}

  /* Invariant READONLY confirmé par le serveur */
  if(st)$('vx-readonly-confirm').textContent=st.readonly&&st.analysis_only
    ?' Confirmé par le serveur : ordres '+(st.order_execution||'disabled-by-design')+'.'
    :' ATTENTION : le serveur ne confirme pas le mode lecture seule.';

  /* IBKR — honnête : connecté-live / connecté-différé / activé-inactif / désactivé */
  if(st){
    const ib=String((st.data_sources||{}).ibkr||'inconnu');
    const map={'connected-live':['live','connecté · temps réel (lecture seule)'],
      'connected-delayed':['delayed','connecté · différé (lecture seule)'],
      'enabled-idle':['frozen','activé · aucune session TWS confirmée'],
      'disabled':['offline','désactivé']};
    const m=map[ib]||['offline','inconnu'];
    const proven=ib==='connected-live'||ib==='connected-delayed';
    $('vx-conn-ibkr-badge').innerHTML=statusBadge(m[0],m[1]);
    $('vx-conn-ibkr').innerHTML=
      kv('&Eacute;tat',esc(m[1]))
      +(ib==='enabled-idle'?'<div class="vx-help vx-mt1 vx-mb1">Config présente mais <b>aucune preuve de session</b> — jamais affiché « connecté » sans tick réel. Ouvre TWS/Gateway (lecture seule).</div>':'')
      +kv('Donn&eacute;es march&eacute;',esc((st.data_sources||{}).market_data||'—'))
      +kv('Mode global',esc(st.mode||'—'))
      +kv('Ex&eacute;cution d&#8217;ordres','<b class="vx-neg">'+esc(st.order_execution||'disabled-by-design')+'</b>')
      +`<div class="vx-card-footer">${VX.updateIndicator(st.ts||Date.now(),'/api/system-status',proven?(ib==='connected-live'?'live':'delayed'):'fallback')}</div>`;
  }else{
    $('vx-conn-ibkr').innerHTML=VX.states.error('&Eacute;tat syst&egrave;me indisponible');
    $('vx-conn-ibkr-badge').innerHTML=statusBadge('offline','inconnu');
  }

  /* TradingView — état honnête : désactivé ≠ configuré-en-attente ≠ actif */
  const tv=diag&&diag.tradingview;
  if(tv){
    const stored=tv.stored??tv.count??0;
    const fresh=tv.fresh??0;
    /* state serveur : DISABLED (pas de secret) / WAITING (configuré, 0 signal frais) / ACTIVE */
    const state=tv.state||(tv.configured?(fresh>0?'ACTIVE':'WAITING'):'DISABLED');
    const badge={ACTIVE:['live','actif · '+fresh+' frais'],
      WAITING:['frozen','configuré · en attente'],
      DISABLED:['offline','webhook désactivé']}[state]||['offline','n/d'];
    $('vx-conn-tv-badge').innerHTML=statusBadge(badge[0],badge[1]);
    $('vx-conn-tv').innerHTML=
      kv('&Eacute;tat',state==='DISABLED'
        ?'<span class="vx-dim">secret webhook absent — 503 honn&ecirc;te, aucun signal invent&eacute;</span>'
        :(state==='ACTIVE'?'<span class="vx-pos">signaux re&ccedil;us</span>':'<span class="vx-dim">webhook pr&ecirc;t, aucun signal r&eacute;cent</span>'))
      +kv('Signaux stock&eacute;s',VX.fmt.nd(stored)+(fresh?' <span class="vx-dim">('+fresh+' frais)</span>':''))
      +(tv.newest_age_s!=null?kv('Dernier signal',VX.fmt.ago(Date.now()-tv.newest_age_s*1000)):'')
      +kv('R&ocirc;le','webhooks d&#8217;alertes TradingView — <b>r&eacute;&eacute;valuation</b>, jamais un ordre')
      +(state==='DISABLED'?'<div class="vx-help vx-mt2">Active-le : d&eacute;finis <span class="vx-mono">TRADINGVIEW_WEBHOOK_SECRET</span> dans <span class="vx-mono">.env</span>.</div>':'')
      +'<div class="vx-flex vx-wrap vx-gap2 vx-mt2"><button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-tv-setup">Configurer mon alerte TradingView</button></div>'
      +'<div id="vx-tv-signals"></div>'
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'/api/system/diagnostics',state==='ACTIVE'?'live':'delayed')}
        <a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/opportunities?view=radar">Voir le radar des signaux →</a></div>`;
    document.getElementById('vx-tv-setup')?.addEventListener('click',openTvSetup);
    loadTvSignals();
  }else{
    $('vx-conn-tv').innerHTML=VX.states.empty('Aucun diagnostic TradingView disponible — le magasin de signaux n&#8217;a rien re&ccedil;u.',
      '<a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=radar">Voir le radar</a>');
    $('vx-conn-tv-badge').innerHTML=statusBadge('offline','n/d');
  }

  /* Claude / IA */
  const ai=diag&&diag.ai;
  const aiSrc=st&&(st.data_sources||{}).ai;
  if(ai||aiSrc!==undefined){
    const ok=ai?(ai.ok??0):null,total=ai?(ai.total??0):null,fb=ai?(ai.fallbacks??0):null;
    const aiOn=String(aiSrc||'').indexOf('on')===0||String(aiSrc||'')==='enabled'||(ok!==null&&ok>0);
    $('vx-conn-ai-badge').innerHTML=statusBadge(aiOn?'live':(fb?'fallback':'offline'),
      aiOn?'disponible':(fb?'mode secours':'indisponible'));
    $('vx-conn-ai').innerHTML=
      kv('Source IA',esc(aiSrc??'—'))
      +(ai?kv('Appels r&eacute;ussis',VX.fmt.nd(ok)+' / '+VX.fmt.nd(total))
          +kv('Replis d&eacute;terministes',VX.fmt.nd(fb)):'')
      +kv('R&ocirc;le','<span class="vx-dim">explique et reformule — ne d&eacute;cide jamais</span>')
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'/api/system/diagnostics',aiOn?'live':'fallback')}</div>`;
  }else{
    $('vx-conn-ai').innerHTML=VX.states.empty('Audit IA indisponible — la synth&egrave;se d&eacute;terministe des moteurs reste servie.');
    $('vx-conn-ai-badge').innerHTML=statusBadge('fallback','n/d');
  }

  /* Synchronisation (Live Engine) */
  if(live){
    const doms=live.domains||{};
    const names=Object.keys(doms);
    const freshCount=names.filter(k=>doms[k].fresh||doms[k].state==='fresh'||doms[k].state==='live').length;
    const errs=(live.errors||[]);
    $('vx-conn-sync-badge').innerHTML=statusBadge(
      errs.length?'delayed':(freshCount===names.length&&names.length?'live':'delayed'),
      freshCount+' / '+names.length+' domaines frais');
    $('vx-conn-sync').innerHTML=
      kv('Mode',esc(live.mode||'—'))
      +kv('Derni&egrave;re synchro',VX.fmt.ago(live.last_refresh))
      +kv('Domaines',names.map(esc).join(', ')||'—')
      +(errs.length?`<div class="vx-error-banner vx-mt2">⚠ ${errs.map(e=>esc(e.domain+' : '+e.error)).join('<br>')}</div>`:'')
      +`<div class="vx-card-footer">${VX.updateIndicator(live.generated?live.generated*1000:Date.now(),'/api/live/status','delayed')}
        <a class="vx-btn vx-btn-sm vx-btn-ghost vx-right" href="/system?view=data">D&eacute;tail par domaine →</a></div>`;
  }else{
    $('vx-conn-sync').innerHTML=VX.states.error('Live Engine injoignable');
    $('vx-conn-sync-badge').innerHTML=statusBadge('offline','hors ligne');
  }

  /* Stockage & santé */
  if(hz){
    const ok=hz.ok!==false&&(hz.status==='ok'||hz.ok===true||hz.status===undefined);
    $('vx-conn-store-badge').innerHTML=statusBadge(ok?'live':'offline',ok?'sain':'dégradé');
    $('vx-conn-store').innerHTML=
      kv('Sant&eacute; serveur',ok?'<span class="vx-pos">OK</span>':'<span class="vx-neg">d&eacute;grad&eacute;</span>')
      +(st?kv('Build',esc(st.build||'—')):'')
      +kv('Donn&eacute;es perso','localStorage navigateur &harr; blob desk_data.json (last-writer-wins)')
      +kv('Sauvegardes','backup quotidien desk_backup_* c&ocirc;t&eacute; serveur')
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'/healthz',ok?'live':'error')}</div>`;
  }else{
    $('vx-conn-store').innerHTML=VX.states.error('/healthz injoignable');
    $('vx-conn-store-badge').innerHTML=statusBadge('offline','hors ligne');
  }

  /* Moteurs */
  if(st&&Array.isArray(st.engines)&&st.engines.length){
    /* Moteurs en stat-tiles à halo (au lieu de badges plats) : nom + état
       color-codé. Jamais « prêt » si le moteur n'a aucune donnée exploitable. */
    $('vx-conn-engines').innerHTML='<div class="vx-statrow">'
      +st.engines.map(en=>{
        const loaded=en.status==='ok'||en.ok===true;
        const hasData=!!(en.last_success||en.last_run||en.fresh);
        const state=!loaded?['neg','KO','hors service']:(hasData?['pos','Prêt','opérationnel']:['','Chargé','sans données']);
        const dotc=state[0]==='pos'?'var(--vx-positive)':state[0]==='neg'?'var(--vx-negative)':'var(--vx-warning)';
        return `<div class="vx-stat" data-tone="${state[0]}" title="${esc(en.last_error||en.last_success||'')}">
          <div class="vx-stat-k">${esc(en.name||'moteur')}</div>
          <div class="vx-stat-v" style="font-size:15px;display:flex;align-items:center;gap:6px"><span style="width:8px;height:8px;border-radius:99px;background:${dotc};flex:0 0 auto"></span>${state[1]}</div>
          <div class="vx-stat-sub">${state[2]}</div></div>`;
      }).join('')+'</div>'
      +((st.warnings||[]).length?`<div class="vx-stale-banner vx-mt3">⏳ ${st.warnings.map(esc).join(' · ')}</div>`:'')
      +`<div class="vx-mt3"><button class="vx-btn vx-btn-sm vx-btn-ghost" id="vx-tech-endpoints">Détails techniques (endpoints) →</button></div>`;
    $('vx-conn-meta').innerHTML=VX.updateIndicator(st.ts||Date.now(),'/api/system-status','delayed');
    $('vx-tech-endpoints')?.addEventListener('click',()=>{
      VX.shell.openDrawer('Endpoints techniques',
        [['GET /healthz','santé serveur'],['GET /api/system-status','état institutionnel complet'],
         ['GET /api/live/status','mode + fraîcheur par domaine'],['GET /api/system/diagnostics','diagnostics moteurs'],
         ['GET /api/data-quality','rapport qualité données'],['GET /api/client-log','erreurs JS remontées'],
         ['GET /scan','dump du dernier scan'],['GET/POST /api/desk','sync données perso (17 clés)'],
         ['POST /api/live/refresh','déclencher une mise à jour'],['GET /api/desk/backups + POST /api/desk/restore','sauvegardes quotidiennes']]
        .map(([ep,d])=>`<div class="vx-kv"><span class="k vx-mono" style="font-size:11px">${ep}</span><span class="v vx-meta">${d}</span></div>`).join('')
        +'<div class="vx-help vx-mt3">Lecture seule — aucun de ces endpoints ne peut passer un ordre.</div>');});
  }else{
    $('vx-conn-engines').innerHTML=VX.states.empty('Liste des moteurs indisponible.');
  }
}

/* ══ Vue DONNÉES ════════════════════════════════════════════════════ */
async function loadData(){
  const [dqR,diagR,liveR]=await Promise.allSettled([
    VX.fetch('/api/data-quality',{ttl:30000}),
    VX.fetch('/api/system/diagnostics',{ttl:30000}),
    VX.fetch('/api/live/status',{ttl:30000})]);
  const dq=dqR.status==='fulfilled'?dqR.value:null;
  const diag=diagR.status==='fulfilled'?diagR.value:null;
  const live=liveR.status==='fulfilled'?liveR.value:null;
  const scan=diag&&diag.scan;

  /* Qualité (donut) */
  if(dq&&dq.total>0){
    const byQ=dq.by_quality||{};
    const labels=Object.keys(byQ);
    const values=labels.map(k=>byQ[k]);
    const colByQ={FRESH:VXCharts.colors.positive,RECENT:VXCharts.colors.cyan,
      STALE:VXCharts.colors.warning,EXPIRED:VXCharts.colors.negative,MISSING:VXCharts.colors.muted};
    const dominant=labels.slice().sort((a,b)=>byQ[b]-byQ[a])[0];
    whenChartsReady(()=>VXCharts.donutCard('vx-data-quality-chart',{
      title:'Qualit&eacute; des donn&eacute;es ('+dq.total+' titres)',
      question:'Les donn&eacute;es sont-elles utilisables pour d&eacute;cider ?',
      conclusion:'Dominante : '+dominant+' ('+byQ[dominant]+' / '+dq.total+') · source '+(dq.scan_source||'n/d'),
      labels,values,colors:labels.map(k=>colByQ[k]||VXCharts.colors.muted),height:200,
      source:'scan '+(dq.scan_source||'n/d'),timestamp:(scan&&scan.last_scan_ts)||Date.now(),
      mode:dq.scan_source==='demo'?'fallback':'delayed',
      limits:dq.note||'',
      explain:{shows:'La r&eacute;partition des titres scann&eacute;s par niveau de qualit&eacute; de donn&eacute;es.',
        why:'Une d&eacute;cision ACTIONABLE exige des donn&eacute;es fra&icirc;ches — la qualit&eacute; plafonne la d&eacute;cision.',
        confirm:'Une majorit&eacute; FRESH/RECENT issue d&#8217;une source r&eacute;elle.',
        invalidate:'Des paquets STALE/EXPIRED/MISSING ou une source d&eacute;mo.'}}));
  }else{
    $('vx-data-quality-chart').innerHTML='<div class="vx-card">'
      +VX.states.empty('Aucun titre scann&eacute; — la qualit&eacute; ne peut pas &ecirc;tre mesur&eacute;e.',
        '<button class="vx-btn vx-btn-sm" id="vx-data-refresh-empty">Actualiser maintenant</button>')+'</div>';
    document.getElementById('vx-data-refresh-empty')?.addEventListener('click',doRefresh);
  }

  /* Scan + métriques */
  if(scan){
    const metrics=diag.metrics||{};
    const mkeys=Object.keys(metrics).slice(0,8);
    $('vx-data-scan').innerHTML=
      kv('Lignes scann&eacute;es',VX.fmt.nd(scan.rows))
      +kv('Source scan',esc(scan.source||'aucune'))
      +kv('Source options',esc(scan.options_source||'—'))
      +kv('Dernier scan',VX.fmt.ago(scan.last_scan_ts))
      +(mkeys.length?'<div class="vx-divider"></div><div class="vx-meta vx-mb1">M&eacute;triques internes</div>'
        +mkeys.map(k=>kv(esc(k),'<span class="vx-mono">'+esc(JSON.stringify(metrics[k]))+'</span>')).join(''):'')
      +`<div class="vx-card-footer">${VX.updateIndicator(scan.last_scan_ts,'/api/system/diagnostics',
        scan.source&&scan.source!=='demo'?'delayed':'fallback')}</div>`;
  }else{
    $('vx-data-scan').innerHTML=VX.states.error('Diagnostics indisponibles');
  }

  /* Fraîcheur par domaine */
  if(live&&live.domains&&Object.keys(live.domains).length){
    const doms=live.domains;
    /* Heatmap de fraîcheur (§37) : une tuile/domaine, couleur = état, chiffre = âge. */
    const tile=(k)=>{const d=doms[k]||{};
      const fresh=d.fresh===true||d.state==='fresh'||d.state==='live';
      const off=d.state==='offline';
      const col=fresh?'--vx-positive':(off?'--vx-negative':'--vx-warning');
      const soft=fresh?'rgba(57,184,120,.13)':(off?'rgba(220,98,85,.13)':'rgba(204,137,44,.13)');
      const age=d.age_s===null||d.age_s===undefined?'—':(d.age_s<120?Math.round(d.age_s)+' s':Math.round(d.age_s/60)+' min');
      const lbl=fresh?'frais':(off?'hors ligne':'différé');
      return `<div role="img" aria-label="${esc(k)} ${lbl} ${age}" style="padding:10px 12px;border-radius:9px;display:flex;flex-direction:column;gap:1px;background:${soft};border:1px solid var(${col},#8f8a83)">
        <span style="font-size:11px;color:var(--vx-text-secondary,#b7b2aa);text-transform:capitalize;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(k)}</span>
        <span style="font-size:16px;font-weight:800;font-variant-numeric:tabular-nums;color:var(${col},#8f8a83)">${age}</span>
        <span style="font-size:9px;letter-spacing:.05em;text-transform:uppercase;color:var(--vx-text-muted,#817d77)">${lbl}</span></div>`;};
    const heat=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:8px;margin-bottom:14px" aria-label="Heatmap de fraîcheur des données">${Object.keys(doms).map(tile).join('')}</div>`;
    $('vx-data-fresh').innerHTML=heat+`<div style="overflow-x:auto"><table class="vx-table">
      <thead><tr><th>Domaine</th><th>&Eacute;tat</th><th class="vx-num">&Acirc;ge</th><th>D&eacute;tail</th></tr></thead><tbody>`
      +Object.keys(doms).map(k=>{
        const d=doms[k]||{};
        const fresh=d.fresh===true||d.state==='fresh'||d.state==='live';
        const status=fresh?'live':(d.state==='offline'?'offline':'delayed');
        const age=d.age_s===null||d.age_s===undefined?'—'
          :(d.age_s<120?Math.round(d.age_s)+' s':Math.round(d.age_s/60)+' min');
        return `<tr><td><b>${esc(k)}</b></td>
          <td>${statusBadge(status,fresh?'frais':(d.state||'rassis'))}</td>
          <td class="vx-num vx-mono">${age}</td>
          <td class="vx-dim" style="font-size:12px">${esc(d.detail||'—')}</td></tr>`;
      }).join('')+'</tbody></table></div>';
    $('vx-data-fresh-meta').innerHTML=VX.updateIndicator(
      live.generated?live.generated*1000:Date.now(),'Live Engine · mode '+(live.mode||'n/d'),'delayed');
  }else{
    $('vx-data-fresh').innerHTML=VX.states.empty('Aucun domaine suivi par le Live Engine pour l&#8217;instant.');
  }

  /* Titres dégradés */
  if(dq){
    const worst=dq.degraded||[];
    $('vx-data-degraded').innerHTML=worst.length
      ?'<div class="vx-flex vx-wrap vx-gap2">'+worst.map(w=>
        `<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(w.symbol)}"
          title="${esc((w.warnings||[]).join(' · '))}">${esc(w.symbol)}
          <span class="vx-badge vx-badge-status" data-status="delayed">${esc(w.quality)}</span></button>`).join('')+'</div>'
      :VX.states.empty('Aucun titre en qualit&eacute; d&eacute;grad&eacute;e — rien &agrave; signaler.');
  }else{
    $('vx-data-degraded').innerHTML=VX.states.error('Rapport de qualit&eacute; indisponible');
  }
}
async function doRefresh(){
  const btn=$('vx-data-refresh');
  if(btn){btn.disabled=true;btn.textContent='Actualisation…';}
  try{
    const r=await fetch('/api/live/refresh',{method:'POST'});
    if(!r.ok)throw new Error('HTTP '+r.status);
    VX.toast('Actualisation demandée au Live Engine','success');
    await VX.refresh.runAll();
  }catch(e){VX.toast('Actualisation impossible : '+e.message,'error');}
  if(btn){btn.disabled=false;btn.textContent='Actualiser';}
  loadData();
}

/* ══ Vue RÉGLAGES ═══════════════════════════════════════════════════ */
function initSettings(){
  /* Densité (vxDashboardLayout.density) */
  let layout={};try{layout=JSON.parse(localStorage.getItem('vxDashboardLayout')||'{}')}catch(e){}
  const density=layout.density||'confort';
  document.querySelectorAll('[data-density-btn]').forEach(b=>{
    b.setAttribute('aria-pressed',String(b.dataset.densityBtn===density));
    b.addEventListener('click',()=>{
      layout.density=b.dataset.densityBtn;
      try{localStorage.setItem('vxDashboardLayout',JSON.stringify(layout))}catch(e){}
      document.body.dataset.density=layout.density==='compact'?'compact':(layout.density==='dense'?'dense':'');
      document.querySelectorAll('[data-density-btn]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
      VX.toast('Densité enregistrée','success');
    });
  });
  /* Sidebar (vxSidebarState) */
  const sb=localStorage.getItem('vxSidebarState')||'expanded';
  document.querySelectorAll('[data-sidebar-btn]').forEach(b=>{
    b.setAttribute('aria-pressed',String(b.dataset.sidebarBtn===sb));
    b.addEventListener('click',()=>{
      try{localStorage.setItem('vxSidebarState',b.dataset.sidebarBtn)}catch(e){}
      const app=document.getElementById('vx-app');
      if(app)app.dataset.sidebar=b.dataset.sidebarBtn;
      document.querySelectorAll('[data-sidebar-btn]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    });
  });
  /* Notifications (vxNotificationPrefs {push:bool}) */
  let notif={push:false};try{notif=Object.assign(notif,JSON.parse(localStorage.getItem('vxNotificationPrefs')||'{}'))}catch(e){}
  document.querySelectorAll('[data-notif-btn]').forEach(b=>{
    b.setAttribute('aria-pressed',String((b.dataset.notifBtn==='1')===!!notif.push));
    b.addEventListener('click',()=>{
      notif.push=b.dataset.notifBtn==='1';
      try{localStorage.setItem('vxNotificationPrefs',JSON.stringify(notif))}catch(e){}
      document.querySelectorAll('[data-notif-btn]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
      VX.toast(notif.push?'Notifications push activées':'Notifications push coupées','success');
    });
  });
  renderDeskSummary();
  $('vx-desk-export').addEventListener('click',exportDesk);
  $('vx-desk-import-file').addEventListener('change',importDesk);
  VX.bus.on('vx:data-refreshed',renderDeskSummary);
}
function deskKeys(){
  return (E()&&E().DESK_KEYS)||['myTrades','myTradesClosed','myTradesEquity','myRecos',
    'myRecosClosed','myCapital','simCash','simStart','simTrades','simClosed',
    'myFavs','myNotes','vxJournal','myTradeLog','vxVault','vxAlerts','vxWatchlist'];
}
function renderDeskSummary(){
  const keys=deskKeys();
  let present=0,bytes=0;
  keys.forEach(k=>{const v=localStorage.getItem(k);if(v!=null){present++;bytes+=v.length;}});
  $('vx-settings-desk').innerHTML=
    kv('Cl&eacute;s synchronis&eacute;es',keys.length+' (contrat __DESK_KEYS — aucune cl&eacute; renomm&eacute;e)')
    +kv('Cl&eacute;s pr&eacute;sentes localement',String(present))
    +kv('Taille locale',VX.fmt.num(bytes/1024,1)+' Ko')
    +kv('Derni&egrave;re &eacute;criture locale',VX.fmt.ago(Number(localStorage.getItem('deskTs')||0)||null));
}
function exportDesk(){
  const keys=deskKeys();const data={};
  keys.forEach(k=>{const v=localStorage.getItem(k);if(v!=null)data[k]=v;});
  const payload={exported:new Date().toISOString(),ts:Number(localStorage.getItem('deskTs')||Date.now()),data};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='vertex-desk-'+new Date().toISOString().slice(0,10)+'.json';
  a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),3000);
  VX.toast('Export desk téléchargé','success');
}
function importDesk(ev){
  const file=ev.target.files&&ev.target.files[0];
  ev.target.value='';
  if(!file)return;
  const reader=new FileReader();
  reader.onload=()=>{
    let payload=null;
    try{payload=JSON.parse(String(reader.result));}catch(e){VX.toast('Fichier JSON invalide','error');return;}
    const data=payload&&payload.data?payload.data:payload;
    if(!data||typeof data!=='object'){VX.toast('Structure inattendue — export desk attendu','error');return;}
    const keys=deskKeys();
    const importable=Object.keys(data).filter(k=>keys.includes(k)&&typeof data[k]==='string');
    if(!importable.length){VX.toast('Aucune clé desk reconnue dans ce fichier','error');return;}
    VX.shell.openModal('Confirmer l’import',
      `<p>Ce fichier va <b>remplacer</b> ${importable.length} cl&eacute;(s) locale(s) :</p>
       <div class="vx-flex vx-wrap vx-gap2 vx-mt2">${importable.map(k=>`<span class="vx-badge">${esc(k)}</span>`).join('')}</div>
       <div class="vx-insight vx-mt3" data-tone="risk">L&#8217;&eacute;criture est suivie d&#8217;une synchronisation
       serveur (last-writer-wins). Les backups quotidiens desk_backup_* restent disponibles en cas d&#8217;erreur.</div>`,
      '<button class="vx-btn vx-btn-primary" id="vx-desk-import-confirm">Importer et synchroniser</button>');
    document.getElementById('vx-desk-import-confirm').addEventListener('click',()=>{
      importable.forEach(k=>{try{localStorage.setItem(k,data[k]);}catch(e){}});
      try{localStorage.setItem('deskTs',String(Date.now()));}catch(e){}
      const out={};keys.forEach(k=>{const v=localStorage.getItem(k);if(v!=null)out[k]=v;});
      fetch('/api/desk',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({ts:Number(localStorage.getItem('deskTs')||Date.now()),data:out})}).catch(()=>{});
      VX.shell.closeModal();
      VX.bus.emit('vx:data-refreshed',{reason:'desk-import'});
      VX.toast(importable.length+' clé(s) importée(s) et synchronisée(s)','success');
      renderDeskSummary();
    });
  };
  reader.readAsText(file);
}

/* ══ Vue ARCHIVE (vxVault) ══════════════════════════════════════════ */
let vaultTypeFilter='';
function vaultGet(){try{const v=JSON.parse(localStorage.getItem('vxVault')||'[]');return Array.isArray(v)?v:[];}catch(e){return[];}}
function vaultSet(list){
  try{
    localStorage.setItem('vxVault',JSON.stringify(list));
    localStorage.setItem('deskTs',String(Date.now()));
  }catch(e){VX.toast('Écriture locale impossible (quota ?)','error');return;}
  /* Push desk — même protocole que vx-entities.js (last-writer-wins). */
  try{
    const keys=deskKeys();const data={};
    keys.forEach(k=>{const v=localStorage.getItem(k);if(v!=null)data[k]=v;});
    fetch('/api/desk',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({ts:Number(localStorage.getItem('deskTs')||Date.now()),data})}).catch(()=>{});
  }catch(e){}
}
function initArchive(){
  renderVault();
  $('vx-vault-search').addEventListener('input',renderVault);
  $('vx-vault-new').addEventListener('click',()=>openVaultModal(null));
  $('vx-vault-export').addEventListener('click',()=>{
    const blob=new Blob([JSON.stringify(vaultGet(),null,2)],{type:'application/json'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download='vertex-vault-'+new Date().toISOString().slice(0,10)+'.json';
    a.click();
    setTimeout(()=>URL.revokeObjectURL(a.href),3000);
    VX.toast('Export du coffre téléchargé','success');
  });
  VX.bus.on('vx:data-refreshed',renderVault);
}
function renderVault(){
  const all=vaultGet();
  const types=[...new Set(all.map(e=>e.type).filter(Boolean))].sort();
  $('vx-vault-chips').innerHTML=[['','Tous ('+all.length+')']]
    .concat(types.map(t=>[t,t+' ('+all.filter(e=>e.type===t).length+')']))
    .map(([val,label])=>`<button class="vx-chip" data-filter-key="type" data-filter-value="${esc(val)}"
      aria-pressed="${String(val===vaultTypeFilter)}">${esc(label)}</button>`).join('');
  document.querySelectorAll('#vx-vault-chips .vx-chip').forEach(ch=>
    ch.addEventListener('click',()=>{vaultTypeFilter=ch.dataset.filterValue;renderVault();}));
  const q=($('vx-vault-search').value||'').trim().toLowerCase();
  const rows=all.filter(e=>{
    if(vaultTypeFilter&&e.type!==vaultTypeFilter)return false;
    if(!q)return true;
    return [e.title,e.content,(e.tags||[]).join(' '),e.type]
      .map(x=>String(x||'').toLowerCase()).some(x=>x.includes(q));
  }).sort((a,b)=>String(b.updatedAt||b.createdAt||'').localeCompare(String(a.updatedAt||a.createdAt||'')));
  if(!rows.length){
    $('vx-vault-list').innerHTML=VX.states.empty(
      all.length?'Aucune entr&eacute;e ne correspond &agrave; la recherche ou au filtre.'
      :'Le coffre est vide — archivez ici vos analyses, mod&egrave;les et documents de r&eacute;f&eacute;rence.',
      all.length?'':'<button class="vx-btn vx-btn-sm" id="vx-vault-new-empty">Cr&eacute;er la premi&egrave;re entr&eacute;e</button>');
    document.getElementById('vx-vault-new-empty')?.addEventListener('click',()=>openVaultModal(null));
    return;
  }
  $('vx-vault-list').innerHTML=`<div style="overflow-x:auto"><table class="vx-table">
    <thead><tr><th>Titre</th><th>Type</th><th>Tags</th><th class="vx-num">Mis &agrave; jour</th><th></th></tr></thead><tbody>`
    +rows.map(e=>`<tr>
      <td><button class="vx-btn vx-btn-sm vx-btn-ghost" data-vault-open="${esc(String(e.id))}"
        style="font-weight:600">${esc(e.title||'(sans titre)')}</button>
        <div class="vx-meta vx-truncate" style="max-width:420px">${esc(String(e.content||'').slice(0,120))}</div></td>
      <td><span class="vx-badge">${esc(e.type||'note')}</span>
        ${e.status?`<span class="vx-badge vx-muted">${esc(e.status)}</span>`:''}</td>
      <td class="vx-dim" style="font-size:12px">${(e.tags||[]).map(t=>'#'+esc(t)).join(' ')||'—'}</td>
      <td class="vx-num vx-meta">${VX.fmt.ago(e.updatedAt||e.createdAt)}</td>
      <td><button class="vx-btn vx-btn-sm" data-vault-edit="${esc(String(e.id))}">Modifier</button></td>
    </tr>`).join('')+'</tbody></table></div>'
    +`<div class="vx-card-footer">${rows.length} entr&eacute;e(s) affich&eacute;e(s) · coffre local synchronis&eacute; via /api/desk</div>`;
  document.querySelectorAll('[data-vault-open]').forEach(b=>
    b.addEventListener('click',()=>openVaultDrawer(b.dataset.vaultOpen)));
  document.querySelectorAll('[data-vault-edit]').forEach(b=>
    b.addEventListener('click',()=>openVaultModal(b.dataset.vaultEdit)));
}
function openVaultDrawer(id){
  const e=vaultGet().find(x=>String(x.id)===String(id));
  if(!e)return;
  VX.shell.openDrawer(e.title||'(sans titre)',
    `<div class="vx-flex vx-wrap vx-gap2 vx-mb3">
      <span class="vx-badge">${esc(e.type||'note')}</span>
      ${e.priority?`<span class="vx-badge">priorit&eacute; ${esc(e.priority)}</span>`:''}
      ${e.status?`<span class="vx-badge">${esc(e.status)}</span>`:''}</div>
    <div style="white-space:pre-wrap;font-size:13px;line-height:1.7">${esc(e.content||'')}</div>
    ${(e.tags||[]).length?`<div class="vx-mt3 vx-dim">${e.tags.map(t=>'#'+esc(t)).join(' ')}</div>`:''}
    <div class="vx-divider"></div>
    <div class="vx-meta">Cr&eacute;&eacute;e ${VX.fmt.ago(e.createdAt)} · mise &agrave; jour ${VX.fmt.ago(e.updatedAt||e.createdAt)}</div>
    <div class="vx-mt3"><button class="vx-btn vx-btn-sm" onclick="document.querySelector('[data-vault-edit=&quot;${esc(String(e.id))}&quot;]')?.click();VX.shell.closeDrawer()">Modifier</button></div>`);
}
function openVaultModal(id){
  const existing=id?vaultGet().find(x=>String(x.id)===String(id)):null;
  const e=existing||{title:'',type:'note',content:'',tags:[],priority:'normal',status:'active'};
  VX.shell.openModal(existing?'Modifier l’entrée':'Nouvelle entrée',
    `<div class="vx-field"><label for="vv-title">Titre</label>
      <input class="vx-input" id="vv-title" value="${esc(e.title)}" /></div>
    <div class="vx-form-row">
      <div class="vx-field"><label for="vv-type">Type</label>
        <select class="vx-select" id="vv-type">
          ${['note','analyse','modele','document','lien','regle'].map(t=>
            `<option value="${t}" ${e.type===t?'selected':''}>${t}</option>`).join('')}
        </select></div>
      <div class="vx-field"><label for="vv-priority">Priorit&eacute;</label>
        <select class="vx-select" id="vv-priority">
          ${['haute','normal','basse'].map(p=>
            `<option value="${p}" ${e.priority===p?'selected':''}>${p}</option>`).join('')}
        </select></div>
    </div>
    <div class="vx-field"><label for="vv-content">Contenu</label>
      <textarea class="vx-textarea" id="vv-content" rows="8">${esc(e.content)}</textarea></div>
    <div class="vx-field"><label for="vv-tags">Tags (s&eacute;par&eacute;s par des virgules)</label>
      <input class="vx-input" id="vv-tags" value="${esc((e.tags||[]).join(', '))}" /></div>`,
    `${existing?'<button class="vx-btn vx-btn-ghost" id="vv-delete">Supprimer</button>':''}
     <button class="vx-btn vx-btn-primary" id="vv-save">${existing?'Enregistrer':'Cr&eacute;er'}</button>`);
  document.getElementById('vv-save').addEventListener('click',()=>{
    const title=(document.getElementById('vv-title').value||'').trim();
    if(!title){VX.toast('Titre requis','error');return;}
    const now=new Date().toISOString();
    const entry={
      id:existing?existing.id:Date.now(),
      title,
      type:document.getElementById('vv-type').value,
      content:document.getElementById('vv-content').value,
      tags:(document.getElementById('vv-tags').value||'').split(',').map(s=>s.trim()).filter(Boolean),
      createdAt:existing?(existing.createdAt||now):now,
      updatedAt:now,
      status:existing?(existing.status||'active'):'active',
      priority:document.getElementById('vv-priority').value,
    };
    const list=vaultGet().filter(x=>String(x.id)!==String(entry.id));
    list.push(entry);
    vaultSet(list);
    VX.shell.closeModal();
    VX.toast(existing?'Entrée mise à jour':'Entrée créée','success');
    renderVault();
  });
  document.getElementById('vv-delete')?.addEventListener('click',()=>{
    vaultSet(vaultGet().filter(x=>String(x.id)!==String(id)));
    VX.shell.closeModal();
    VX.toast('Entrée supprimée');
    renderVault();
  });
}

/* ══ Vue AUTOMATISATIONS (§24) ══════════════════════════════════════ */
async function loadAutomations(){
  try{
    const d=await VX.fetch('/api/system/automations',{ttl:15000});
    const jobs=d.jobs||[];
    $('vx-auto-jobs').innerHTML=jobs.length?`<div class="vx-table-wrap"><table class="vx-table"><thead><tr>
      <th>Job</th><th>Statut</th><th class="vx-num">Exécutions</th><th>Dernière</th><th>Prochaine (est.)</th><th class="vx-num">Durée</th></tr></thead><tbody>
      ${jobs.map(j=>{
        const st=j.last_run===null?['frozen','jamais exécuté']:(j.last_ok?['live','OK']:['offline','erreur']);
        return `<tr><td><b>${esc(j.name)}</b><br><span class="vx-meta">${esc(j.description||'')}</span></td>
        <td><span class="vx-badge vx-badge-status" data-status="${st[0]}" title="${esc(j.last_error||'')}">${st[1]}</span></td>
        <td class="vx-num">${j.runs||0}</td>
        <td class="vx-mono vx-meta">${j.age_s!==null&&j.age_s!==undefined?VX.fmt.ago(Date.now()-j.age_s*1000):'—'}</td>
        <td class="vx-mono vx-meta">${j.next_run_eta_s!==null&&j.next_run_eta_s!==undefined?('dans ~'+Math.round(j.next_run_eta_s/60)+' min'):(j.interval_s?'—':'sur événement')}</td>
        <td class="vx-num">${j.last_duration_ms!==null&&j.last_duration_ms!==undefined?j.last_duration_ms+' ms':'—'}</td></tr>`;}).join('')}
      </tbody></table></div>
      <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'/api/system/automations','live')}
      · les jobs « jamais exécuté » dépendent d'intégrations absentes dans cet environnement (honnêteté avant tout)</div>`
      :VX.states.empty('Registre de jobs vide.');
  }catch(e){$('vx-auto-jobs').innerHTML=VX.states.error('Registre indisponible : '+esc(e.message));}
  try{
    const r=await VX.fetch('/api/system/startup-report',{ttl:60000});
    $('vx-auto-startup').innerHTML=(r.steps||[]).length?
      (r.steps.map(st2=>{
        const tone={CONNECTED:'live',READY:'live',CONFIGURED:'live',DEGRADED:'delayed',
          MISSING:'frozen',OFFLINE:'offline',ERROR:'offline'}[st2.status]||'frozen';
        return `<div class="vx-kv"><span class="k">${esc(st2.step)}</span>
          <span class="v"><span class="vx-badge vx-badge-status" data-status="${tone}">${esc(st2.status)}</span></span></div>
          <div class="vx-meta" style="margin:-4px 0 6px">${esc(st2.detail||'')}</div>`;}).join('')
       +`<div class="vx-kv"><span class="k">Exécution d'ordres</span><span class="v vx-pos">${esc(r.order_execution||'')}</span></div>`
       +`<div class="vx-card-footer">${VX.updateIndicator((r.ts||0)*1000,'séquence de démarrage','live')}</div>`)
      :VX.states.empty('Rapport non généré (serveur fraîchement démarré ?).');
  }catch(e){$('vx-auto-startup').innerHTML=VX.states.error('Rapport indisponible');}
  try{
    const c=await VX.fetch('/api/system/config',{ttl:60000});
    const rows=Object.entries(c).filter(([k])=>!k.startsWith('_'));
    $('vx-auto-config').innerHTML=`<div class="vx-flex vx-wrap vx-gap2">${rows.map(([k,v])=>{
      const tone={CONFIGURED:'live',MISSING:'frozen',INVALID:'offline'}[v.status]||'frozen';
      return `<span class="vx-badge vx-badge-status" data-status="${tone}"
        title="${esc(v.consequence||'')}">${esc(k)} · ${esc(v.status)}</span>`;}).join('')}</div>
      <div class="vx-help vx-mt2">Survoler un badge : conséquence exacte d'une variable absente. Aucune valeur n'est jamais affichée ni journalisée.</div>`;
  }catch(e){$('vx-auto-config').innerHTML=VX.states.error('Validation indisponible');}
}

/* ══ Orchestration ══════════════════════════════════════════════════ */
if(VIEW==='connections'){
  loadConnections();
  document.getElementById('vx-brain-refresh')?.addEventListener('click',refreshBrain);
  VX.refresh.register(loadConnections,60000,'connections');
}else if(VIEW==='data'){
  loadData();
  $('vx-data-refresh').addEventListener('click',doRefresh);
  VX.refresh.register(loadData,60000,'data');
}else if(VIEW==='automations'){
  loadAutomations();
  VX.refresh.register(loadAutomations,60000,'automations');
}else if(VIEW==='settings'){
  initSettings();
}else if(VIEW==='archive'){
  initArchive();
}
VX.context.restoreIfReturning();
})();
</script>
"""


def render(view: str = 'connections') -> str:
    view = view if view in dict(VIEWS) else _DEFAULT_VIEW
    body = _VIEW_CONTENT[view].replace(
        '%%LOADING%%', '<div class="vx-skeleton" style="height:60px"></div>')
    content = (_header(view)
               + f'<div id="vx-system" data-view="{view}">' + body + '</div>')
    sub = dict(VIEWS)[view]
    return render_shell(title='Système', active='system',
                        space_label='Système', sub_label=sub,
                        content=content, page_js=_JS,
                        page_label='Système — ' + sub)
