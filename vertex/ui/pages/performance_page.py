"""vertex.ui.pages.performance_page — l'espace Journal (§27, refonte PR n°7).

Question unique : « Suis-je en train de devenir un meilleur investisseur ? »

Le Journal ne mesure PLUS la performance du portefeuille (courbe, drawdown,
contribution) : elle vit définitivement dans Portefeuille → Performance (§6, un
seul domicile, migration PR n°5). Le Journal est exclusivement le lieu de la
DISCIPLINE : qualité des décisions, respect de la méthode, erreurs, apprentissage,
revue des hypothèses, statistiques comportementales.

Sous-vues (?view=) : overview (Discipline) · journal (Timeline) · learnings
(Apprentissage) · progression · track-record.

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
    ('journal', 'Timeline'),
    ('learnings', 'Apprentissage'),
    ('progression', 'Progression'),
    ('track-record', 'Track record'),
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
<div class="vx-page-header">
  <div><h1>Journal</h1>
  <div class="vx-sub">Suis-je en train de devenir un meilleur investisseur ?</div></div>
</div>
%%TABS%%
"""

_VIEW_CONTENT = {
    'overview': """
<section class="vx-card vx-card--hero vx-mt3" id="vx-pf-hero" aria-label="Verdict de discipline">
  <div class="vx-skeleton" style="height:64px"></div></section>
<div class="vx-grid vx-mt3" id="vx-pf-kpis" aria-label="Indicateurs de discipline"><div class="vx-skeleton vx-skeleton-kpi vx-col-3" style="grid-column:span 3"></div></div>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-7" aria-label="Revue des hypothèses">
    <div class="vx-card-header"><span class="vx-card-title">Revue des hypothèses</span>
      <span class="vx-chart-question">Mes thèses se vérifient-elles ?</span></div>
    <div id="vx-pf-hypo"><div class="vx-skeleton" style="height:80px"></div></div>
  </section>
  <div class="vx-col-5" id="vx-pf-dist"></div>
</div>
""",
    'journal': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-8" aria-label="Timeline des décisions">
    <div class="vx-card-header"><span class="vx-card-title">Timeline des décisions</span>
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
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=journal">Ouvrir la timeline →</a></span></div>
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
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
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
const JOURNAL_ACTION='<a class="vx-btn vx-btn-sm" href="/journal?view=journal">Ouvrir la timeline</a>';
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
  if(!b.n){
    if(hero)hero.innerHTML=`<div class="vx-flex" style="gap:8px;align-items:center;margin-bottom:6px">
        <span class="vx-eyebrow">Discipline</span></div>
      <h2 style="margin:0 0 6px;font-size:21px">Aucune décision journalisée pour l’instant.</h2>
      <p class="vx-dim" style="margin:0;font-size:13.5px;line-height:1.6">Le Journal mesure ta <b>méthode</b> — pas la performance du portefeuille (elle vit dans <a href="/portfolio?view=performance">Portefeuille → Performance</a>). Journalise tes décisions pour révéler ta discipline, tes erreurs récurrentes et tes progrès.</p>
      <div class="vx-flex vx-mt3" style="gap:.5rem;flex-wrap:wrap">
        <a class="vx-btn vx-btn-sm vx-btn-primary" href="/journal?view=journal">Journaliser une décision</a></div>`;
    $('vx-pf-kpis').innerHTML='';
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
  const cell=(label,val,sub,cls)=>`<div class="vx-card vx-kpi vx-card--compact" style="grid-column:span 3" aria-label="${esc(label)}">
    <span class="vx-kpi-label">${label}</span><span class="vx-kpi-value ${cls||''}" style="font-size:20px">${val}</span>
    <span class="vx-meta">${sub}</span></div>`;
  $('vx-pf-kpis').innerHTML=
    cell('Respect de la méthode',pct(b.respectMethod),'décisions avec plan documenté',b.respectMethod>=80?'vx-pos':b.respectMethod!=null&&b.respectMethod<50?'vx-neg':'')
    +cell('Qualité des entrées',pct(b.entryQuality),'avec raison d’entrée')
    +cell('Qualité des sorties',pct(b.exitQuality),'clôtures avec leçon')
    +cell('Respect des invalidations',pct(b.invalRespect),'pertes sorties près du stop',b.invalRespect!=null&&b.invalRespect>=80?'vx-pos':b.invalRespect!=null&&b.invalRespect<50?'vx-neg':'');
}

/* Revue des hypothèses — validées / invalidées / en cours (déclarations). */
function loadHypotheses(){
  const host=$('vx-pf-hypo');if(!host)return;
  const j=(E()?E().journal():[])||[];
  if(!j.length){host.innerHTML=VX.states.empty('Aucune hypothèse journalisée — chaque décision est une thèse à vérifier.',JOURNAL_ACTION);return;}
  const wins=j.filter(e=>e.result==='WIN'),losses=j.filter(e=>e.result==='LOSS'),open=j.filter(e=>!e.result);
  const chip=(label,n,cls)=>`<div class="vx-kpi vx-card vx-card--compact" style="grid-column:span 4">
    <span class="vx-kpi-label">${label}</span><span class="vx-kpi-value ${cls}" style="font-size:24px">${n}</span></div>`;
  const line=(e)=>`<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft);gap:10px;align-items:center">
    <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${esc(e.ticker||'')}">${esc(e.ticker||'—')}</button>
    <span class="vx-badge ${e.result==='WIN'?'vx-pos':e.result==='LOSS'?'vx-neg':'vx-muted'}">${e.result||'en cours'}</span>
    <span class="vx-grow vx-truncate vx-dim" style="font-size:12.5px">${esc(e.reason||e.lesson||'—')}</span></div>`;
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
    explain:{shows:'Le décompte de vos trades clôturés par tranche de rendement (%).',
      why:'La méthode vise des pertes tronquées (stops) et des gains étendus (TP échelonnés).',
      confirm:'Masse des pertes concentrée entre 0 et −10 %, queue droite étendue.',
      invalidate:'Queue gauche épaisse — les stops ne sont pas respectés.'},
    render:(cv)=>VXCharts.bars(cv,labels,counts,
      {colors:buckets.map(([a])=>a<0?VXCharts.colors.negative:VXCharts.colors.positive)})});
}

/* ═══ TIMELINE (journal) ═══ */
function currentFilter(){return ($('vx-pf-filter')?$('vx-pf-filter').value:'').trim().toUpperCase();}
function loadJournal(){
  const all=(E()?E().journal():[]).slice().sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
  const f=currentFilter();
  const list=f?all.filter(e=>String(e.ticker||'').toUpperCase().includes(f)):all;
  if(!list.length){
    $('vx-pf-journal').innerHTML=VX.states.empty(
      f?('Aucune entrée pour « '+esc(f)+' ».'):'Timeline vide — déclarez vos décisions pour mesurer votre exécution.',
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
    :VX.states.empty('Aucune erreur déclarée — renseignez le champ « erreur » à chaque sortie perdante.');
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
    :VX.states.empty('Aucune leçon consignée — renseignez le champ « leçon » à chaque sortie de trade.',JOURNAL_ACTION);
  const counts={};
  all.forEach(e=>{const m=String(e.mistake||'').trim();if(m)counts[m]=(counts[m]||0)+1;});
  const top=Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  $('vx-pf-recurrent').innerHTML=top.length?top.map(([m,n])=>
    `<div class="vx-kv"><span class="k">${esc(m)}</span><span class="v vx-mono">× ${n}</span></div>`).join('')
    :VX.states.empty('Aucune erreur récurrente déclarée pour l’instant.');
  /* Biais comportementaux — décompte des états émotionnels déclarés. */
  const emo={};
  all.forEach(e=>{const m=String(e.emo||'').trim().toLowerCase();if(m)emo[m]=(emo[m]||0)+1;});
  const rows=Object.entries(emo).sort((a,b)=>b[1]-a[1]);
  const bh=$('vx-pf-biais');
  if(bh){
    if(!rows.length){bh.innerHTML=VX.states.empty('Aucun état émotionnel déclaré — renseignez « état émotionnel » (calme, FOMO, peur…) pour révéler vos biais.');}
    else{
      const max=rows[0][1];
      bh.innerHTML='<div style="display:flex;flex-direction:column;gap:6px">'+rows.map(([m,n])=>
        `<div style="display:flex;align-items:center;gap:8px"><span style="width:140px;font-size:12.5px;text-transform:capitalize" class="vx-dim">${esc(m)}</span>
         <span style="flex:1;height:13px;background:var(--vx-surface-3,#17191c);border-radius:4px;overflow:hidden"><span style="display:block;height:100%;width:${Math.round(n/max*100)}%;background:var(--vx-brand,#84aa31);border-radius:4px"></span></span>
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
    try{
      const _tl=rows.map(([v])=>v),_tv=rows.map(([,s])=>(s.avg_20j==null?null:s.avg_20j));
      if(window.VXCharts&&VXCharts.card&&VXCharts.bars&&_tv.some(x=>x!=null)){
        VXCharts.card('vx-pf-track-bar',{title:'Rendement moyen +20 séances par verdict',
          question:'Quels verdicts moteur ont le mieux tenu ?',height:200,
          source:'moteur track-record',timestamp:Date.now(),mode:'delayed',
          limits:'moyenne réelle des verdicts résolus (n≥5) — mesure, pas une promesse',
          render:(cv)=>VXCharts.bars(cv,_tl,_tv,{colors:_tv.map(v=>v==null?'#9d978e':(v>=0?'#36c889':'#ed655c')),yFmt:(x)=>x+' %'})});
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

/* ═══ Orchestration ═══ */
function boot(){
  if(VIEW==='overview'){loadDiscipline();loadHypotheses();loadDist();}
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
