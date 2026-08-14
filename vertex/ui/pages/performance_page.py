"""vertex.ui.pages.performance_page — l'espace Journal (§27, refonte PR n°7).

Question unique : « Suis-je en train de devenir un meilleur investisseur ? »

Le Journal ne mesure PLUS la performance du portefeuille (courbe, drawdown,
contribution) : elle vit définitivement dans Portefeuille → Performance (§6, un
seul domicile, migration PR n°5). Le Journal est exclusivement le lieu de la
DISCIPLINE : qualité des décisions, respect de la méthode, erreurs, apprentissage,
revue des hypothèses, statistiques comportementales.

Sous-vues (?view=) : overview (Discipline) · journal (Chronologie) · learnings
(Apprentissage) · progression · track-record (Historique).

Le module Python ne fait AUCUN calcul financier : il assemble le squelette + le
script client. Les agrégations côté client portent uniquement sur les décisions
DÉCLARÉES par l'utilisateur (localStorage via VXEntities) — jamais des indicateurs
de marché. Donnée absente → état honnête (jamais un pourcentage inventé).
"""
from __future__ import annotations

import html
import re

from vertex.ui.shell import render_shell

_VIEWS = (
    ('overview', 'Discipline'),
    ('journal', 'Chronologie'),
    ('learnings', 'Apprentissage'),
    ('progression', 'Progression'),
    ('track-record', 'Historique'),
)


def _tabs(view: str) -> str:
    items = []
    for vid, label in _VIEWS:
        sel = 'true' if vid == view else 'false'
        items.append(f'<a class="vx-tab" role="tab" href="?view={vid}" '
                     f'aria-selected="{sel}" data-view-tab="{vid}">{label}</a>')
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Journal">'
            + ''.join(items) + '</nav>')


_HEADER = """
<div class="vx-page-header vx-page-lead">
  <div class="vx-page-lead__main"><h1>Journal</h1>
  <div class="vx-sub">Suis-je en train de devenir un meilleur investisseur ?</div></div>
</div>
%%TABS%%
"""

_VIEW_CONTENT = {
    'overview': """
<section class="vx-card vx-card--hero vx-page-lead vx-mt3" id="vx-pf-hero" aria-label="Verdict de discipline">
  <div class="vx-skeleton" style="height:64px"></div></section>
<div class="vx-kpi-strip vx-mt3" id="vx-pf-kpis" data-max-kpis="4" aria-label="Quatre indicateurs de discipline"><div class="vx-skeleton vx-skeleton-kpi"></div></div>
<div class="vx-hero-grid vx-mt4">
  <section class="vx-card" aria-label="Revue des hypothèses">
    <div class="vx-card-header"><span class="vx-card-title">Revue des hypothèses</span>
      <span class="vx-chart-question">Mes thèses se vérifient-elles ?</span></div>
    <div id="vx-pf-hypo"><div class="vx-skeleton" style="height:80px"></div></div>
  </section>
  <aside class="vx-insight-rail" aria-label="Prochain axe de travail">
    <div class="vx-insight" id="vx-pf-next-axis" data-tone="neutral"><div class="vx-skeleton" style="height:80px"></div></div>
  </aside>
</div>
<div class="vx-section-stack vx-mt4">
  <details class="vx-disclosure" id="vx-pf-results-disclosure">
    <summary>R&eacute;sultats d&eacute;clar&eacute;s &middot; P&amp;L, r&eacute;ussite et profit factor</summary>
    <div class="vx-disclosure__body">
      <div class="vx-page-lead vx-mb3"><b>Mesure descriptive du journal.</b>
        <span class="vx-meta">La performance de portefeuille reste dans <a href="/portfolio?view=performance">Portefeuille &rarr; Performance</a>.</span></div>
      <div class="vx-hero-grid">
        <section class="vx-card" aria-label="Post-mortem des trades clôturés">
          <div class="vx-card-header"><span class="vx-card-title">Post-mortem &mdash; que disent mes sorties&nbsp;?</span>
            <span class="vx-chart-question">Stats r&eacute;elles et drapeaux de discipline. Descriptif, pas un conseil.</span></div>
          <div id="vx-pf-postmortem">%%LOADING%%</div>
        </section>
        <div id="vx-pf-dist"></div>
      </div>
    </div>
  </details>
  <details class="vx-disclosure" id="vx-pf-history-disclosure">
    <summary>Avanc&eacute; &middot; calibration et m&eacute;moire du moteur</summary>
    <div class="vx-disclosure__body vx-section-stack">
      <div class="vx-toolbar">
        <span class="vx-meta">Historique technique, calibration et ledger immuable.</span>
        <a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=track-record">Ouvrir Historique &rarr;</a>
      </div>
      <section class="vx-card" aria-label="Calibration Skyler">
        <div class="vx-card-header"><span class="vx-card-title">Calibration Skyler</span>
          <span class="vx-chart-question">D&eacute;cisions canoniques et rendements r&eacute;els ; Brier indisponible tant qu&rsquo;il ne peut pas &ecirc;tre mesur&eacute;.</span></div>
        <div id="vx-pf-calibration">%%LOADING%%</div>
      </section>
      <section class="vx-card" aria-label="Mémoire décisionnelle">
        <div class="vx-card-header"><span class="vx-card-title">M&eacute;moire d&eacute;cisionnelle</span>
          <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/api/skyler/memory/export" download>Exporter &rarr;</a>
            <label class="vx-btn vx-btn-sm vx-btn-ghost" for="vx-mem-import-file" style="cursor:pointer">Importer &larr;</label>
            <input type="file" id="vx-mem-import-file" accept="application/json,.json" style="display:none"></span></div>
        <div id="vx-mem-import-result"></div>
        <div id="vx-pf-memory">%%LOADING%%</div>
      </section>
    </div>
  </details>
</div>
""",
    'journal': """
<div class="vx-page-lead vx-mt3">
  <div><h2>Chronologie des d&eacute;cisions</h2><div class="vx-sub">Retrouver une d&eacute;cision, sa raison et la le&ccedil;on d&eacute;clar&eacute;e.</div></div>
</div>
<div class="vx-toolbar vx-mt3" role="search" aria-label="Outils de la chronologie">
  <input class="vx-input" id="vx-pf-filter" data-filter-key="sym" placeholder="Filtrer par ticker"
    value="%%SYM%%" autocomplete="off" style="max-width:190px;text-transform:uppercase" aria-label="Filtrer par ticker" />
  <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-pf-add">Ajouter une entrée</button>
</div>
<div class="vx-hero-grid vx-mt3">
  <section class="vx-card" aria-label="Chronologie des décisions">
    <div class="vx-card-header"><span class="vx-card-title">D&eacute;cisions d&eacute;clar&eacute;es</span></div>
    <div id="vx-pf-journal">%%LOADING%%</div>
  </section>
  <aside class="vx-insight-rail" aria-label="Statistiques d'erreurs">
    <section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Erreurs déclarées</span></div>
      <div id="vx-pf-mistakes">%%LOADING%%</div></section>
  </aside>
</div>
""",
    'learnings': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-6" aria-label="Leçons du journal">
    <div class="vx-card-header"><span class="vx-card-title">Leçons apprises</span></div>
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
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-12" aria-label="Biais comportementaux">
    <div class="vx-card-header"><span class="vx-card-title">Biais comportementaux</span>
      <span class="vx-chart-question">Quel état émotionnel accompagne mes décisions ?</span></div>
    <div id="vx-pf-biais">%%LOADING%%</div>
  </section>
</div>
""",
    'progression': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Progression de la discipline">
    <div class="vx-card-header"><span class="vx-card-title">Ma progression</span>
      <span class="vx-chart-question">Est-ce que je m'améliore, décision après décision ?</span></div>
    <div id="vx-pf-prog">%%LOADING%%</div>
  </section>
</div>
""",
    'track-record': """
<div class="vx-page-lead vx-mt3" role="note">
  <div><h2>Historique</h2><div class="vx-sub">Deux sources s&eacute;par&eacute;es : mesure du moteur et journal d&eacute;clar&eacute;. Aucun chiffre ne passe de l&rsquo;une &agrave; l&rsquo;autre.</div></div>
</div>
<div class="vx-section-stack vx-mt4">
  <section class="vx-card" aria-label="Historique théorique du moteur" data-source-kind="engine">
    <div class="vx-card-header"><span class="vx-card-title">Moteur &middot; verdicts th&eacute;oriques</span>
      <span class="vx-badge">Source API moteur</span></div>
    <div id="vx-pf-track">%%LOADING%%</div>
  </section>
  <section class="vx-card" aria-label="Historique déclaré du journal" data-source-kind="declared">
    <div class="vx-card-header"><span class="vx-card-title">Journal &middot; trades d&eacute;clar&eacute;s</span>
      <span class="vx-badge" style="color:var(--vx-cyan,#45D6E8)">Tes d&eacute;clarations</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=journal">Ouvrir la chronologie &rarr;</a></span></div>
    <div id="vx-pf-real">%%LOADING%%</div>
  </section>
</div>
""",
}

_JS = r"""
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW='%%VIEW%%';
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));}
function trades(){/* entrées avec un résultat déclaré et un P&L numérique */
  return (E()?E().journal():[]).filter(e=>(e.result==='WIN'||e.result==='LOSS')&&isFinite(Number(e.pnl)));
}
function stats(list){
  const pnls=list.map(e=>Number(e.pnl));
  const wins=pnls.filter(p=>p>0),losses=pnls.filter(p=>p<0);
  const gains=wins.reduce((a,b)=>a+b,0),pertes=Math.abs(losses.reduce((a,b)=>a+b,0));
  return {n:list.length,total:pnls.reduce((a,b)=>a+b,0),
    winRate:list.length?100*list.filter(e=>e.result==='WIN').length/list.length:null,
    profitFactor:pertes>0?gains/pertes:(gains>0?Infinity:null),
    expectancy:pnls.length?pnls.reduce((a,b)=>a+b,0)/pnls.length:null};
}
const JOURNAL_ACTION='<a class="vx-btn vx-btn-sm" href="/journal?view=journal">Ouvrir la chronologie</a>';
function emptyCard(host,reason,action){const el=$(host);if(el)el.innerHTML='<div class="vx-card">'+VX.states.empty(reason,action||'')+'</div>';}

/* Statistiques COMPORTEMENTALES — agrégations honnêtes sur les décisions déclarées
   (jamais un indicateur de marché, jamais un pourcentage inventé). */
function behavioral(){
  const j=(E()?E().journal():[])||[];
  const closed=j.filter(e=>e.result==='WIN'||e.result==='LOSS');
  const num=(x)=>{const n=Number(x);return isFinite(n)?n:null;};
  const withPlan=j.filter(e=>e.reason&&num(e.stop)!=null);      /* raison + invalidation = plan */
  const withReason=j.filter(e=>e.reason);
  const closedWithLesson=closed.filter(e=>e.lesson);
  const lossWithStop=closed.filter(e=>e.result==='LOSS'&&num(e.stop)!=null&&num(e.exit)!=null);
  const respected=lossWithStop.filter(e=>num(e.exit)>=num(e.stop)*0.97); /* sortie ≈ stop, pas au-delà */
  return {n:j.length,closed:closed.length,
    wins:closed.filter(e=>e.result==='WIN').length,
    losses:closed.filter(e=>e.result==='LOSS').length,
    open:j.filter(e=>!e.result).length,
    respectMethod:j.length?Math.round(withPlan.length/j.length*100):null,
    entryQuality:j.length?Math.round(withReason.length/j.length*100):null,
    exitQuality:closed.length?Math.round(closedWithLesson.length/closed.length*100):null,
    invalRespect:lossWithStop.length?Math.round(respected.length/lossWithStop.length*100):null,
    mistakes:j.filter(e=>String(e.mistake||'').trim()).length,
    lessons:new Set(j.map(e=>String(e.lesson||'').trim()).filter(Boolean)).size};
}

/* ═══ DISCIPLINE (overview) — Hero éditorial honnête + KPI comportementaux ═══ */
function loadDiscipline(){
  const b=behavioral();
  const hero=$('vx-pf-hero');
  const next=$('vx-pf-next-axis');
  if(!b.n){
    if(hero)hero.innerHTML=`<div class="vx-flex" style="gap:8px;align-items:center;margin-bottom:6px">
        <span class="vx-eyebrow">Discipline</span></div>
      <h2 style="margin:0 0 6px;font-size:21px">Aucune décision journalisée pour l’instant.</h2>
      <p class="vx-dim" style="margin:0;font-size:13.5px;line-height:1.6">Le Journal mesure ta <b>méthode</b> — pas la performance du portefeuille (elle vit dans <a href="/portfolio?view=performance">Portefeuille → Performance</a>). Journalise tes décisions pour révéler ta discipline, tes erreurs récurrentes et tes progrès.</p>
      <div class="vx-flex vx-mt3" style="gap:.5rem;flex-wrap:wrap">
        <a class="vx-btn vx-btn-sm vx-btn-primary" href="/journal?view=journal">Journaliser une décision</a></div>`;
    $('vx-pf-kpis').innerHTML='';
    if(next)next.innerHTML='<span class="vx-eyebrow">Prochain axe</span><h3>Documenter une premi&egrave;re d&eacute;cision</h3>'
      +'<p class="vx-dim">Renseigne au minimum la raison, l&rsquo;invalidation et ce qui confirmerait la th&egrave;se.</p>'
      +'<a class="vx-btn vx-btn-sm vx-btn-primary" href="/journal?view=journal">Commencer &rarr;</a>';
    return;
  }
  /* Phrase éditoriale construite UNIQUEMENT sur des faits comptés. */
  const bits=[];
  if(b.respectMethod!=null)bits.push(`Tu as documenté un plan (raison + invalidation) sur <b>${b.respectMethod} %</b> de tes décisions.`);
  if(b.mistakes)bits.push(`<b>${b.mistakes}</b> erreur(s) déclarée(s).`);
  if(b.closed)bits.push(`<b>${b.wins}</b> hypothèse(s) validée(s) · <b>${b.losses}</b> invalidée(s).`);
  const tone=(b.respectMethod!=null&&b.respectMethod>=80)?'vx-pos':(b.respectMethod!=null&&b.respectMethod<50?'vx-warn':'vx-muted');
  if(hero)hero.innerHTML=`<div class="vx-flex" style="gap:8px;align-items:center;margin-bottom:6px">
      <span class="vx-eyebrow">Discipline</span>
      <span class="vx-badge ${tone}">${b.n} décision(s) journalisée(s)</span></div>
    <h2 style="margin:0 0 8px;font-size:20px;line-height:1.35" class="${tone}">${bits[0]||'Ta discipline se mesure ici.'}</h2>
    <p class="vx-dim" style="margin:0;font-size:13.5px;line-height:1.6">${bits.slice(1).join(' ')||''} Aucun pourcentage n’est inventé — tout est compté sur tes déclarations.</p>`;
  /* KPI comportementaux — « n/d » honnête quand la donnée n'existe pas. */
  const pct=(v)=>v==null?'n/d':v+' %';
  const cell=(label,val,sub,cls)=>`<div class="vx-card vx-kpi-card vx-kpi vx-card--compact" aria-label="${esc(label)}">
    <span class="vx-kpi-label">${label}</span><span class="vx-kpi-value ${cls||''}" style="font-size:20px">${val}</span>
    <span class="vx-meta">${sub}</span></div>`;
  $('vx-pf-kpis').innerHTML=
    cell('Respect de la méthode',pct(b.respectMethod),'décisions avec plan documenté',b.respectMethod>=80?'vx-pos':b.respectMethod!=null&&b.respectMethod<50?'vx-neg':'')
    +cell('Qualité des entrées',pct(b.entryQuality),'avec raison d’entrée',b.entryQuality>=80?'vx-pos':b.entryQuality!=null&&b.entryQuality<50?'vx-neg':'')
    +cell('Qualité des sorties',pct(b.exitQuality),'clôtures avec leçon',b.exitQuality>=80?'vx-pos':b.exitQuality!=null&&b.exitQuality<50?'vx-neg':'')
    +cell('Respect des invalidations',pct(b.invalRespect),'pertes sorties près du stop',b.invalRespect!=null&&b.invalRespect>=80?'vx-pos':b.invalRespect!=null&&b.invalRespect<50?'vx-neg':'');
  if(next){
    const axes=[
      {value:b.respectMethod,title:'Formaliser le plan',body:'Ajouter une raison et une invalidation avant de juger la décision.'},
      {value:b.entryQuality,title:'Expliquer l’entrée',body:'Rendre la raison d’entrée explicite et vérifiable.'},
      {value:b.exitQuality,title:'Consigner la leçon',body:'Compléter la leçon après chaque clôture.'},
      {value:b.invalRespect,title:'Respecter l’invalidation',body:'Comparer la sortie au niveau d’invalidation déclaré.'}
    ];
    const known=axes.filter(a=>a.value!=null).sort((a,b2)=>a.value-b2.value);
    const axis=known[0]||axes.find(a=>a.value==null)||axes[0];
    next.dataset.tone=axis.value!=null&&axis.value<50?'risk':'neutral';
    next.innerHTML='<span class="vx-eyebrow">Prochain axe</span><h3>'+esc(axis.title)+'</h3>'
      +'<p class="vx-dim">'+esc(axis.body)+'</p>'
      +(axis.value==null?'<span class="vx-badge">mesure n/d</span>':'<span class="vx-badge">'+axis.value+' % aujourd&rsquo;hui</span>')
      +'<div class="vx-mt3"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/journal?view=journal">Voir la chronologie &rarr;</a></div>';
  }
}

/* Revue des hypothèses — validées / invalidées / en cours (déclarations). */
function loadHypotheses(){
  const host=$('vx-pf-hypo');if(!host)return;
  const j=(E()?E().journal():[])||[];
  if(!j.length){host.innerHTML=VX.states.emptyDesk('Aucune hypothèse journalisée — chaque décision est une thèse à vérifier.',JOURNAL_ACTION);return;}
  const wins=j.filter(e=>e.result==='WIN'),losses=j.filter(e=>e.result==='LOSS'),open=j.filter(e=>!e.result);
  const chip=(label,n,cls)=>`<div class="vx-kpi vx-card vx-card--compact" style="grid-column:span 4">
    <span class="vx-kpi-label">${label}</span><span class="vx-kpi-value ${cls}" style="font-size:24px">${n}</span></div>`;
  const line=(e)=>`<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft);gap:10px;align-items:center">
    <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(e.ticker||'')}">${esc(e.ticker||'—')}</button>
    <span class="vx-badge ${e.result==='WIN'?'vx-pos':e.result==='LOSS'?'vx-neg':'vx-muted'}">${e.result||'en cours'}</span>
    <span class="vx-grow vx-truncate vx-dim" style="font-size:12.5px" title="${esc(e.reason||e.lesson||'—')}">${esc(e.reason||e.lesson||'—')}</span></div>`;
  host.innerHTML=`<div class="vx-grid vx-mb3">
      ${chip('Validées',wins.length,'vx-pos')}${chip('Invalidées',losses.length,'vx-neg')}${chip('En cours',open.length,'vx-muted')}</div>`
    +j.slice().sort((a,b2)=>String(b2.date||'').localeCompare(String(a.date||''))).slice(0,6).map(line).join('')
    +`<div class="vx-card-footer">${j.length} hypothèse(s) · une hypothèse invalidée n’est pas un échec si l’invalidation a été respectée</div>`;
}

/* Distribution des rendements par trade — mesure de DISCIPLINE (asymétrie). */
function loadDist(){
  const closed=(E()?E().closedPositions():[])||[];
  const withPl=closed.filter(t=>t.pnl_pct!==undefined&&t.pnl_pct!==null&&t.closed);
  if(withPl.length<3){emptyCard('vx-pf-dist','Distribution disponible à partir de 3 clôtures datées.',JOURNAL_ACTION);return;}
  const buckets=[[-1e9,-20],[-20,-10],[-10,-5],[-5,0],[0,5],[5,10],[10,20],[20,50],[50,1e9]];
  const labels=['<-20','-20/-10','-10/-5','-5/0','0/+5','+5/+10','+10/+20','+20/+50','>+50'];
  const counts=buckets.map(([a,b])=>withPl.filter(t=>t.pnl_pct>=a&&t.pnl_pct<b).length);
  VXCharts.card('vx-pf-dist',{title:'Distribution des rendements par trade',
    question:'Le profil est-il asymétrique (petites pertes, gains amples) ?',
    conclusion:withPl.length+' clôtures · l’asymétrie droite valide la gestion.',
    height:220,source:'journal local (clôtures)',timestamp:Date.now(),mode:'delayed',
    explain:{shows:'Le décompte de tes trades clôturés par tranche de rendement (%).',
      why:'La méthode vise des pertes tronquées (stops) et des gains étendus (TP échelonnés).',
      confirm:'Masse des pertes concentrée entre 0 et −10 %, queue droite étendue.',
      invalidate:'Queue gauche épaisse — les stops ne sont pas respectés.'},
    render:(cv)=>VXCharts.bars(cv,labels,counts,
      {colors:buckets.map(([a])=>a<0?VXCharts.colors.negative:VXCharts.colors.positive)})});
}

/* ═══ CHRONOLOGIE (journal) ═══ */
function currentFilter(){return ($('vx-pf-filter')?$('vx-pf-filter').value:'').trim().toUpperCase();}
function loadJournal(){
  const all=(E()?E().journal():[]).slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
  const f=currentFilter();
  const list=f?all.filter(e=>String(e.ticker||'').toUpperCase().includes(f)):all;
  if(!list.length){
    $('vx-pf-journal').innerHTML=VX.states.emptyDesk(
      f?('Aucune entrée pour « '+esc(f)+' ».'):'Chronologie vide — déclare tes décisions pour mesurer ton exécution.',
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
    :VX.states.emptyDesk('Aucune erreur déclarée — renseigne le champ « erreur » à chaque sortie perdante.');
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

/* ═══ APPRENTISSAGE (learnings) ═══ */
function loadLearnings(){
  const all=E()?E().journal():[];
  const lessons=[...new Set(all.map(e=>String(e.lesson||'').trim()).filter(Boolean))];
  $('vx-pf-lessons').innerHTML=lessons.length?
    '<ul style="margin:0;padding-left:18px;line-height:1.9">'+lessons.map(l=>`<li>${esc(l)}</li>`).join('')+'</ul>'
    :VX.states.emptyDesk('Aucune leçon consignée — renseigne le champ « leçon » à chaque sortie de trade.',JOURNAL_ACTION);
  const counts={};
  all.forEach(e=>{const m=String(e.mistake||'').trim();if(m)counts[m]=(counts[m]||0)+1;});
  const top=Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  $('vx-pf-recurrent').innerHTML=top.length?top.map(([m,n])=>
    `<div class="vx-kv"><span class="k">${esc(m)}</span><span class="v vx-mono">× ${n}</span></div>`).join('')
    :VX.states.emptyDesk('Aucune erreur récurrente déclarée pour l’instant.');
  /* Biais comportementaux — décompte des états émotionnels déclarés. */
  const emo={};
  all.forEach(e=>{const m=String(e.emo||'').trim().toLowerCase();if(m)emo[m]=(emo[m]||0)+1;});
  const rows=Object.entries(emo).sort((a,b)=>b[1]-a[1]);
  const bh=$('vx-pf-biais');
  if(bh){
    if(!rows.length){bh.innerHTML=VX.states.emptyDesk('Aucun état émotionnel déclaré — renseigne « état émotionnel » (calme, FOMO, peur…) pour révéler tes biais.');}
    else{
      const max=rows[0][1];
      bh.innerHTML='<div style="display:flex;flex-direction:column;gap:6px">'+rows.map(([m,n])=>
        `<div style="display:flex;align-items:center;gap:8px"><span style="width:140px;font-size:12.5px;text-transform:capitalize" class="vx-dim">${esc(m)}</span>
         <span style="flex:1;height:13px;background:var(--vx-surface-3,#121214);border-radius:4px;overflow:hidden"><span style="display:block;height:100%;width:${Math.round(n/max*100)}%;background:var(--vx-brand,#D28A54);border-radius:4px"></span></span>
         <span class="vx-mono" style="width:34px;text-align:right">× ${n}</span></div>`).join('')+'</div>'
        +'<div class="vx-card-footer"><span class="vx-meta">Décompte déclaratif — un biais nommé est un biais qu’on peut corriger.</span></div>';
    }
  }
}

/* ═══ PROGRESSION ═══ */
function loadProgression(){
  const host=$('vx-pf-prog');if(!host)return;
  const b=behavioral();
  const milestones=[[5,'P&L, taux de réussite, profit factor, espérance'],
    [10,'Distribution gains/pertes, meilleurs & pires trades'],
    [20,'Respect des invalidations, MAE/MFE, meilleurs setups'],
    [30,'Rolling win rate & discipline par régime']];
  const rows=milestones.map(m=>{const done=b.n>=m[0];
    return `<div class="vx-kv"><span class="k">${done?'✅':'🔒'} ${m[0]} décisions</span>
      <span class="v vx-dim" style="font-size:12px;text-align:right">${esc(m[1])}</span></div>`;}).join('');
  /* Erreurs par mois (déclarées) — la fréquence baisse-t-elle ? */
  const all=(E()?E().journal():[])||[];
  const byMonth={};
  all.forEach(e=>{const d=String(e.date||'').slice(0,7);if(!d)return;if(String(e.mistake||'').trim())byMonth[d]=(byMonth[d]||0)+1;});
  const months=Object.keys(byMonth).sort();
  let trend='';
  if(months.length>=2&&window.VXCharts&&VXCharts.card){
    host.innerHTML=`<div class="vx-grid"><div class="vx-col-5">${rows}</div>
      <div class="vx-col-7" id="vx-pf-prog-chart"></div></div>`;
    VXCharts.card('vx-pf-prog-chart',{title:'Erreurs déclarées par mois',
      question:'Mes erreurs récurrentes diminuent-elles ?',
      conclusion:byMonth[months[months.length-1]]<=byMonth[months[0]]?'Tendance à la baisse — la discipline progresse.':'Vigilance : les erreurs ne diminuent pas encore.',
      height:200,source:'journal local',timestamp:Date.now(),mode:'delayed',
      render:(cv)=>VXCharts.bars(cv,months,months.map(m=>byMonth[m]),
        {colors:months.map(()=>VXCharts.colors.warning),yFmt:(v)=>v})});
  }else{
    host.innerHTML=`<div class="vx-mb3">${rows}</div>`
      +`<div class="vx-meta">La courbe de progression (erreurs par période) apparaîtra avec au moins deux mois de décisions datées. `
      +`${b.n?('Actuellement '+b.n+' décision(s) journalisée(s).'):''} Aucune progression fabriquée avant d’avoir des faits.</div>`;
  }
}

/* ═══ HISTORIQUE DU MOTEUR ═══ */
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
        <td class="vx-num vx-mono ${s.win_5j==null?'':s.win_5j>=50?'vx-pos':'vx-neg'}">${s.win_5j===null||s.win_5j===undefined?'—':VX.fmt.num(s.win_5j,0)+' %'}</td>
        <td class="vx-num vx-mono">${s.tp1_rate===null||s.tp1_rate===undefined?'—':VX.fmt.num(s.tp1_rate,0)+' % ('+s.tp1_resolved+')'}</td>
      </tr>`).join('')+'</tbody></table>'
      +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),'historique moteur','delayed')}
        <span class="vx-meta">${esc(tr.note||'')}${tr.as_of?' · au '+esc(tr.as_of):''}</span></div>`;
    try{
      const _tl=rows.map(([v])=>v),_tv=rows.map(([,s])=>(s.avg_20j==null?null:s.avg_20j));
      if(window.VXCharts&&VXCharts.card&&VXCharts.bars&&_tv.some(x=>x!=null)){
        VXCharts.card('vx-pf-track-bar',{title:'Rendement moyen +20 séances par verdict',
          question:'Quels verdicts moteur ont le mieux tenu ?',height:200,
          source:'historique moteur',timestamp:Date.now(),mode:'delayed',
          limits:'moyenne réelle des verdicts résolus (n≥5) — mesure, pas une promesse',
          render:(cv)=>VXCharts.bars(cv,_tl,_tv,{colors:_tv.map(v=>v==null?VXCharts.colors.muted:(v>=0?VXCharts.colors.positive:VXCharts.colors.negative)),yFmt:(x)=>x+' %'})});
      }
    }catch(e){}
  }catch(e){$('vx-pf-track').innerHTML=VX.states.error('Historique moteur indisponible ('+esc(e.message)+')');}
}
function loadReal(){
  const list=trades();
  if(!list.length){
    $('vx-pf-real').innerHTML=VX.states.emptyDesk('Aucun trade réel déclaré avec résultat — le journal est la seule source de cette section.',JOURNAL_ACTION);
    return;
  }
  const s=stats(list);
  const pf=s.profitFactor===Infinity?'∞':(s.profitFactor===null?'—':VX.fmt.num(s.profitFactor,2));
  $('vx-pf-real').innerHTML=
    `<table class="vx-table"><thead><tr><th class="vx-num">Trades</th><th class="vx-num">Taux de réussite</th>
     <th class="vx-num">P&amp;L total</th><th class="vx-num">Profit factor</th><th class="vx-num">Espérance / trade</th></tr></thead>
     <tbody><tr>
       <td class="vx-num vx-mono">${s.n}</td>
       <td class="vx-num vx-mono ${s.winRate==null?'':s.winRate>=50?'vx-pos':'vx-neg'}">${VX.fmt.num(s.winRate,0)} %</td>
       <td class="vx-num vx-mono ${s.total>=0?'vx-pos':'vx-neg'}">${(s.total>=0?'+':'')+VX.fmt.num(s.total,0)} $</td>
       <td class="vx-num vx-mono">${pf}</td>
       <td class="vx-num vx-mono ${s.expectancy>=0?'vx-pos':'vx-neg'}">${(s.expectancy>=0?'+':'')+VX.fmt.num(s.expectancy,0)} $</td>
     </tr></tbody></table>
     <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'journal local (tes déclarations)','delayed')}
       <span class="vx-meta">agrégations arithmétiques sur tes trades déclarés — indépendant des signaux moteur</span></div>`;
}

/* ═══ Orchestration ═══ */
/* Calibration Skyler (LOT 8e) : journal des décisions + rendements ex post réels.
   Brier honnêtement indisponible tant que rien de calibré. */
async function loadCalibration(){
  const host=$('vx-pf-calibration');if(!host)return;
  try{
    const d=await VX.fetch('/api/skyler/calibration',{ttl:120000});
    if(!d||!d.n_decisions){
      host.innerHTML='<div class="vx-empty">Aucune décision enregistrée pour le moment — le journal se remplit à chaque fiche Analyse consultée.</div>';
      return;
    }
    const byDec=Object.entries(d.by_decision||{}).map(([k,v])=>'<span class="vx-badge" data-tone="neutral" style="margin-right:.25rem">'+esc(k)+' × '+v+'</span>').join('');
    const oc=d.outcomes||{};
    let rows='';
    if(oc.available&&(oc.rows||[]).length){
      rows='<div class="vx-table-wrap vx-mt1"><table class="vx-table"><thead><tr><th>Titre</th><th>Décision</th><th>Prix décision</th><th>Prix actuel</th><th>Rendement</th></tr></thead><tbody>'
        +oc.rows.slice(-12).map(r=>{
          const cls=r.return_pct>0?'vx-pos':r.return_pct<0?'vx-neg':'';
          return '<tr><td data-label="Titre"><b>'+esc(r.symbol)+'</b></td><td data-label="Décision">'+esc(r.decision)+'</td>'
            +'<td data-label="Prix décision" class="vx-num">'+VX.fmt.num(r.entry_price,2)+'</td>'
            +'<td data-label="Prix actuel" class="vx-num">'+VX.fmt.num(r.current_price,2)+'</td>'
            +'<td data-label="Rendement" class="vx-num '+cls+'">'+(r.return_pct>0?'+':'')+r.return_pct+' %</td></tr>';
        }).join('')+'</tbody></table></div>';
    }
    host.innerHTML='<div class="vx-flex vx-mb1" style="gap:.4rem;align-items:center;flex-wrap:wrap">'
      +'<b>'+d.n_decisions+'</b><span class="vx-meta">décision(s) journalisée(s)</span>'+byDec
      +(d.demo?'<span class="vx-badge" data-tone="neutral">DÉMO</span>':'')+'</div>'
      +rows
      +'<div class="vx-meta" style="margin-top:.35rem">'
      +(oc.available?oc.measured+' mesurée(s), '+(oc.unmeasured||0)+' non mesurée(s) (sans cote — jamais inventé) · ':'')
      +'Brier : '+esc((d.brier&&d.brier.reason)||'indisponible')+'</div>';
  }catch(e){host.innerHTML='<div class="vx-error-banner">Calibration injoignable : '+esc(e.message)+'</div>';}
}
/* Mémoire décisionnelle (LOT 16) : ledger immuable + biais + erreurs par version.
   Lecture seule de /api/skyler/memory — états vides honnêtes, rien inventé. */
async function loadMemory(){
  const host=$('vx-pf-memory');if(!host)return;
  try{
    const d=await VX.fetch('/api/skyler/memory',{ttl:120000});
    if(!d||!d.n_decisions){
      host.innerHTML='<div class="vx-empty">Aucune décision figée pour le moment — la mémoire se remplit à chaque fiche Analyse consultée.</div>';
      return;
    }
    const agg=(d.aggregates&&d.aggregates.by_engine_version)||{};
    const vRows=Object.entries(agg).map(([v,a])=>{
      const errs=Object.entries(a.error_classes||{}).map(([k,n])=>esc(k)+' × '+n).join(' · ')||'aucune erreur classée (résultats en attente)';
      const decs=Object.entries(a.by_decision||{}).map(([k,n])=>esc(k)+' × '+n).join(' · ');
      return '<tr><td data-label="Moteur" class="vx-mono">'+esc(v)+'</td>'
        +'<td data-label="Décisions" class="vx-num">'+a.n_decisions+'</td>'
        +'<td data-label="Répartition">'+decs+'</td>'
        +'<td data-label="Mesurées" class="vx-num">'+(a.measured||0)+'</td>'
        +'<td data-label="Erreurs classées">'+errs+'</td></tr>';
    }).join('');
    const tone={DETECTE:'risk',ABSENT:'positive',INSUFFISANT:'neutral'};
    const pats=(d.patterns||[]).map(p=>'<span class="vx-badge" data-tone="'+(tone[p.status]||'neutral')
      +'" title="'+esc(p.basis||'')+'" style="margin:.12rem .25rem .12rem 0">'
      +esc(String(p.pattern||'').replace(/_/g,' '))+' : '+esc(p.status)+'</span>').join('');
    const recs=(d.recommendations||[]).map(r=>'<div class="vx-insight" data-tone="warning">'
      +esc(r.proposal)+' <span class="vx-meta">(en attente de validation humaine)</span></div>').join('');
    host.innerHTML='<div class="vx-flex vx-mb1" style="gap:.4rem;align-items:center;flex-wrap:wrap">'
      +'<b>'+d.n_decisions+'</b><span class="vx-meta">décision(s) figée(s) · '+(d.n_outcomes||0)+' résultat(s) mesuré(s)</span>'
      +(d.demo?'<span class="vx-badge" data-tone="neutral">DÉMO</span>':'')
      +((d.ledger_health&&d.ledger_health.status==='ANOMALIES')
        ?'<span class="vx-badge" data-tone="negative" title="'+esc(d.ledger_health.basis||'')
          +'">LEDGER : ANOMALIES</span>':'')
      +(function(){
        const ds=d.decisions||[];
        if(!ds.length)return '<span class="vx-meta">· aucune décision figée</span>';
        const sd=(ds[ds.length-1]||{}).session_date||null;
        if(!sd)return '<span class="vx-meta">· dernière décision figée : n/d</span>';
        const now=new Date();
        const todayUTC=Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate());
        const days=Math.round((todayUTC-new Date(sd+'T00:00:00Z').getTime())/86400000);
        const age=(isFinite(days)&&days>=0)?' (J-'+days+')':'';
        return '<span class="vx-meta">· dernière décision figée : '+esc(sd)+age+'</span>';
      })()+'</div>'
      +'<div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Moteur</th><th>Décisions</th><th>Répartition</th><th>Mesurées</th><th>Erreurs classées</th></tr></thead><tbody>'
      +vRows+'</tbody></table></div>'
      +(function(){
        const cc=d.calibration_by_context||{};
        const cells=[];
        [['by_level','niveau'],['by_regime','régime'],['by_decision','décision'],
         ['by_catalyst','catalyseur'],['by_catalyst_type','type']].forEach(([k,lbl])=>{
          Object.entries(cc[k]||{}).forEach(([name,c])=>{
            cells.push('<a class="vx-badge" data-tone="'+(c.status==='MESURE'?'positive':'neutral')
              +'" href="/memory/cell/'+encodeURIComponent(k)+'/'+encodeURIComponent(name)
              +'" title="'+esc(c.basis||'')+' — clic : décisions mesurées de la cellule" style="margin:.12rem .25rem .12rem 0">'
              +esc(lbl)+'='+esc(name)+' : '+(c.status==='MESURE'?(c.value+' ('+c.n_measured+' mesures)'):'insuffisant ('+c.n_measured+')')+'</a>');
          });
        });
        return cells.length?('<div class="vx-kpi-label vx-mt2">Calibration par contexte (niveau → régime → global · catalyseur/type = observation, jamais consommés)</div><div>'+cells.join('')+'</div>'):'';
      })()
      +'<div class="vx-kpi-label vx-mt2">Biais surveillés</div><div>'+pats+'</div>'
      +(recs?'<div class="vx-kpi-label vx-mt2">Propositions</div>'+recs:'')
      +(function(){
        const last=(d.decisions||[]).slice(-5).reverse();
        if(!last.length)return '';
        return '<div class="vx-kpi-label vx-mt2">Dernières décisions figées</div>'
          +'<div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Titre</th><th>Décision</th><th>Moteur</th><th>Séance</th><th>Post-mortem</th></tr></thead><tbody>'
          +last.map(r=>'<tr><td data-label="Titre"><b>'+esc(r.symbol)+'</b></td>'
            +'<td data-label="Décision">'+esc(r.decision)+'</td>'
            +'<td data-label="Moteur" class="vx-mono">'+esc(r.engine_version||'n/d')+'</td>'
            +'<td data-label="Séance">'+esc(r.session_date||'n/d')+'</td>'
            +'<td data-label="Post-mortem"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/memory/'+encodeURIComponent(r.decision_id)+'">détail →</a></td></tr>').join('')
          +'</tbody></table></div>';
      })()
      +'<div class="vx-meta" style="margin-top:.35rem">Ledger immuable — les décisions historiques ne sont jamais réécrites ; résultats séparés par version de moteur ; biais inobservables sans trades réels dits INSUFFISANT.</div>';
  }catch(e){host.innerHTML='<div class="vx-error-banner">Mémoire injoignable : '+esc(e.message)+'</div>';}
}
async function loadPostmortem(){
  const host=$('vx-pf-postmortem');if(!host)return;
  let d=null;
  try{d=await VX.fetch('/api/journal/postmortem',{ttl:60000});}catch(e){
    host.innerHTML=VX.states.error('Post-mortem indisponible : '+e.message);return;}
  if(!d||d.empty){
    host.innerHTML=VX.states.empty(esc((d&&d.reason)||'Aucun trade clôturé pour l\'instant.'),
      '<span class="vx-meta">Le post-mortem se construit avec tes clôtures (Portefeuille → Gérer → Clôturer).</span>');
    return;}
  const kpi=(l,v,cls)=>'<div class="vx-stat"><span class="vx-stat-label">'+l+'</span><span class="vx-stat-value '+(cls||'')+'">'+v+'</span></div>';
  const money=(x)=>x==null?'n/d':((x>=0?'+':'')+VX.fmt.num(x,0));
  host.innerHTML=
    '<div class="vx-stats-row">'
    +kpi('Trades',d.trades_n)
    +kpi('Réussite',d.win_rate!=null?d.win_rate+' %':'n/d')
    +kpi('P&L cumulé',money(d.total_pnl),d.total_pnl>0?'vx-pos':d.total_pnl<0?'vx-neg':'')
    +kpi('Profit factor',d.profit_factor!=null?VX.fmt.num(d.profit_factor,2):'n/d',d.profit_factor>=1?'vx-pos':'vx-neg')
    +kpi('Espérance/trade',money(d.expectancy),d.expectancy>0?'vx-pos':'vx-neg')
    +kpi('Durée moy.',d.hold_days_avg!=null?d.hold_days_avg+' j':'n/d')
    +'</div>'
    +'<p class="vx-lead" style="font-size:14px">'+esc(d.narrative||'')+'</p>'
    +((d.flags||[]).length?'<div class="vx-insight" data-tone="risk"><b>Drapeaux de discipline.</b><ul style="margin:.3rem 0 0;padding-left:1.1rem">'
      +d.flags.map(f=>'<li>'+esc(f)+'</li>').join('')+'</ul></div>':'')
    +((d.mistakes||[]).length?'<div class="vx-mt2 vx-muted">Erreurs notées : '
      +d.mistakes.map(m=>esc((m.ticker||'')+' — '+m.mistake)).join(' · ')+'</div>':'')
    +'<div class="vx-card-footer">Post-mortem descriptif (moteur déterministe, trades réels du desk) — pas un conseil.</div>';
}
function wireMemoryImport(){
  const inp=$('vx-mem-import-file');const host=$('vx-mem-import-result');
  if(!inp||!host||inp.dataset.wired)return;
  inp.dataset.wired='1';
  inp.addEventListener('change',()=>{
    const f=inp.files&&inp.files[0];if(!f)return;
    host.innerHTML='<div class="vx-insight" data-tone="neutral">Restauration en cours…</div>';
    const rd=new FileReader();
    rd.onload=async()=>{
      let bundle=null;
      try{bundle=JSON.parse(rd.result);}catch(e){
        host.innerHTML='<div class="vx-insight" data-tone="negative">Fichier illisible : pas un JSON valide.</div>';
        inp.value='';return;
      }
      try{
        const r=await fetch('/api/skyler/memory/import',{method:'POST',
          headers:{'Content-Type':'application/json'},body:JSON.stringify(bundle)});
        const d=await r.json();
        if(!r.ok||!d.ok){
          // erreur serveur affichée TELLE QUELLE (empreinte invalide, etc.)
          host.innerHTML='<div class="vx-insight" data-tone="negative">Import refus&eacute; — '
            +esc(d.error||('HTTP '+r.status))+(d.note?' : '+esc(d.note):'')+'</div>';
        }else{
          const s=d.stats||{};const ses=s.sessions||{};const j=s.journal||{};
          host.innerHTML='<div class="vx-insight" data-tone="positive">Restauration termin&eacute;e — '
            +'d&eacute;cisions : '+(s.added_decisions||0)+' ajout&eacute;e(s), '+(s.skipped_decisions||0)+' d&eacute;j&agrave; pr&eacute;sente(s) (la donn&eacute;e locale gagne) · '
            +'s&eacute;ances : '+(ses.added_sessions||0)+' ajout&eacute;e(s) · '
            +'journal : '+(j.added_entries||0)+' ajout&eacute;e(s)'
            +(((s.corrupted_entries||0)+(ses.corrupted_entries||0)+(j.corrupted_entries||0))>0
              ?' · entr&eacute;es corrompues ignor&eacute;es : '+((s.corrupted_entries||0)+(ses.corrupted_entries||0)+(j.corrupted_entries||0)):'')
            +' — ledger : '+esc((d.ledger_health||{}).status||'n/d')+'</div>';
          loadMemory();
        }
      }catch(e){
        host.innerHTML='<div class="vx-insight" data-tone="negative">Import impossible : '+esc(String(e))+'</div>';
      }
      inp.value='';
    };
    rd.readAsText(f);
  });
}
function bindDisclosures(){
  document.querySelectorAll('details.vx-disclosure').forEach(d=>{
    if(d.dataset.vxBound)return;
    d.dataset.vxBound='1';
    d.addEventListener('toggle',()=>{if(d.open)window.dispatchEvent(new Event('resize'));});
  });
}
function boot(){
  bindDisclosures();
  if(VIEW==='overview'){loadDiscipline();loadHypotheses();loadDist();loadPostmortem();loadCalibration();loadMemory();wireMemoryImport();}
  else if(VIEW==='journal'){
    loadJournal();loadMistakes();
    $('vx-pf-add')?.addEventListener('click',openEntryModal);
    $('vx-pf-filter')?.addEventListener('input',loadJournal);
  }
  else if(VIEW==='learnings'){loadLearnings();}
  else if(VIEW==='progression'){loadProgression();}
  else if(VIEW==='track-record'){loadTrack();loadReal();}
}
function whenReady(fn){
  if(window.VXEntities&&(VIEW!=='overview'&&VIEW!=='progression'||(window.VXCharts&&window.Chart)))return fn();
  window.addEventListener('load',fn,{once:true});
}
whenReady(boot);
VX.bus.on('vx:data-refreshed',()=>whenReady(boot));
})();
</script>
"""


def render(view: str = 'overview', params: dict | None = None) -> str:
    """Assemble le Journal pour la sous-vue demandée (URL = état)."""
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
    return render_shell(title='Journal', active='journal',
                        space_label='Journal', sub_label=label,
                        content=content, page_js=page_js,
                        page_label='Journal')
