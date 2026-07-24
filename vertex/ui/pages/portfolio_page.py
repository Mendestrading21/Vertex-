"""vertex.ui.pages.portfolio_page — l'espace Portefeuille (§25, refonte PR n°5).

Mission unique : « Où mon capital est-il réellement exposé, et quelle position
exige une décision ? » — pas un inventaire, un instrument de décision.

Sous-vues (?view=) :
  team        → Synthèse (premier écran : Hero + 4 KPI + risque dominant + action)
  positions   → Tableau canonique (état de thèse, invalidation, catalyseur, action)
  performance → Performance de portefeuille (MIGRÉE depuis Journal — un seul domicile)
  risk        → Risque priorisé (moteur risk_engine — positions réelles)
  options     → Options command center (inchangé — refonte dédiée PR n°7)
  watchlist   → Surveillance active (watchlist + suivis + favoris)

INVARIANTS ABSOLUS (Constitution §17-22) :
  · IBKR strictement READONLY — AUCUN chemin d'exécution d'ordre, aucun bouton
    Acheter/Vendre/Renforcer. Toute « action » est ANALYTIQUE.
  · Jamais déduire « thèse cassée » d'une simple baisse de prix : seul le
    franchissement de l'invalidation (niveau pré-défini) casse une thèse (§18).
  · JAMAIS suggérer de renforcer une position perdante sans confirmation
    positive explicite du marché (§18) — garde-fou testé.
  · Les gagnants sont réévalués selon la thèse, jamais vendus par réflexe (§19).
  · Donnée absente → « n/d » honnête, jamais un zéro inventé. Source/unité/
    fraîcheur/état (live/delayed/stale/demo/offline) toujours affichés.
"""
from __future__ import annotations

import json

from vertex.ui.shell import render_shell

_VIEWS = (('team', 'Synthèse'), ('positions', 'Positions'),
          ('performance', 'Performance'), ('risk', 'Risque'),
          ('options', 'Options'), ('watchlist', 'Watchlist'))


def _tabs(view: str) -> str:
    return ('<div class="vx-tabs" role="tablist">'
            + ''.join(f'<a class="vx-tab" role="tab" aria-selected='
                      f'"{"true" if v == view else "false"}" '
                      f'href="/portfolio?view={v}">{label}</a>'
                      for v, label in _VIEWS) + '</div>')


_CONTENT = """
<div class="vx-page-header"><div><h1>Portefeuille</h1>
<div class="vx-sub">Où mon capital est-il exposé, et quelle position exige une décision ?</div></div>
<div class="vx-actions">
  <button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal('','position')">+ Position</button>
  <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('','watchlist')">+ Watchlist</button>
  <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/tracking">Suivis →</a>
</div></div>
%%TABS%%
<div class="vx-grid vx-mt4" id="pf-summary" aria-label="Synthèse portefeuille"></div>
<div id="pf-body" class="vx-mt4">%%LOADING%%</div>
"""

_JS = r"""
<script src="/static/vertex/js/charts/donut-chart.js" defer></script>
<script src="/static/vertex/js/charts/sparkline.js" defer></script>
<script src="/static/vertex/js/charts/equity-chart.js" defer></script>
<script src="/static/vertex/js/charts/drawdown-chart.js" defer></script>
<script src="/static/vertex/js/charts/heatmap.js" defer></script>
<script src="/static/vertex/js/charts/bar-chart.js" defer></script>
<script src="/static/vertex/js/charts/option-payoff.js" defer></script>
<script src="/static/vertex/js/charts/line-area-chart.js" defer></script>
<script>
(function(){
'use strict';
const VIEW=%%VIEW%%;
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));}
function kv(k,v,cls){return `<div class="vx-kv"><span class="k">${k}</span><span class="v ${cls||''}">${VX.fmt.nd(v)}</span></div>`;}
const toneCls=(t)=>({pos:'vx-pos',neg:'vx-neg',warn:'vx-warn',muted:'vx-muted'}[t]||'vx-muted');

async function quotesFor(pos){
  if(!pos.length)return{};
  try{
    /* Contrat serveur /api/pos-quotes : {positions:[{sym,exp,strike,right}]}
       → résultats indexés par clé composite 'SYM|exp|strike|RIGHT'. */
    const body=pos.map(t=>({sym:t.sym,exp:t.exp,strike:t.strike,right:t.right}));
    const r=await fetch('/api/pos-quotes',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({positions:body})});
    const d=await r.json();window.__pfLive=!!d.live;
    const res=d.results||{};const byId={};
    pos.forEach(t=>{const key=[String(t.sym).toUpperCase(),t.exp||'',
      (t.strike!==null&&t.strike!==undefined)?t.strike:'',
      (t.right||'').toUpperCase()].join('|');
      if(res[key])byId[t.id]=res[key];});
    return byId;
  }catch(e){return{};}
}
function enrich(pos,quotes){
  /* Schéma desk : t.cost = TOTAL investi. Cotes serveur : spot (actions,
     par action) · mark (options, PAR ACTION → ×100 par contrat). */
  return pos.map(t=>{
    const q=quotes[t.id]||{};
    const isOpt=t.type!=='STK';
    const mark=isOpt?(q.mark??q.last??null):(q.spot??q.mark??q.last??null);
    const underSpot=isOpt?(q.spot??null):null;
    const value=mark!==null?(isOpt?mark*100*t.qty:mark*t.qty):null;
    const invested=t.cost||0;
    const pl=value!==null&&invested?((value-invested)/invested*100):null;   /* P&L % */
    const plAbs=value!==null?(value-invested):null;                          /* P&L absolu */
    return Object.assign({},t,{mark,underSpot,value,invested,pl,plAbs});
  });
}
function roleOf(t){
  const snap=t.entrySnap||{};
  if(t.type!=='STK')return'Options tactiques';
  if((snap.score||0)>=78||(snap.verdict||'').includes('FORT'))return'Offensive';
  if(['XLU','XLP','BIL','SGOV','SHV','GLD'].includes(t.sym))return'Défense / gardien';
  return'Noyau';
}

/* ═══════════════════════════════════════════════════════════════════════
   MOTEUR ANALYTIQUE DE THÈSE (Constitution §18-19) — jamais un ordre.
   ══════════════════════════════════════════════════════════════════════ */

/* Validation positive du marché : SEULE justification d'un renforcement (§18).
   Elle doit venir d'un fait explicite du snapshot d'entrée (breakout, résultats
   confirmés, revalidation) — JAMAIS d'une baisse de prix ni d'un P&L négatif. */
function hasPositiveConfirmation(t){
  const s=t.entrySnap||{};
  return !!(s.validated||s.breakout||s.confirmed||s.revalidated||s.thesis_improved);
}

/* État de thèse — six états honnêtes. La franchise de l'invalidation (niveau
   pré-défini AVANT l'entrée) casse la thèse ; une simple baisse ne la casse
   jamais (§18). Sans marque → « données insuffisantes » (jamais un verdict). */
function thesisState(t){
  const s=t.entrySnap||{};
  const stop=Number(s.stop);
  const hasStop=isFinite(stop)&&stop>0;
  const mark=(t.type!=='STK')?t.underSpot:t.mark;   /* option : niveau du sous-jacent */
  if(mark==null||mark===undefined)
    return {key:'insuffisant',label:'Données insuffisantes',tone:'muted'};
  if(hasStop&&mark<=stop)
    return {key:'cassee',label:'Cassée — invalidation atteinte',tone:'neg'};
  if(hasStop&&mark<=stop*1.04)
    return {key:'fragilisee',label:'Fragilisée — proche invalidation',tone:'warn'};
  if(hasPositiveConfirmation(t)&&t.pl!=null&&t.pl>0)
    return {key:'renforcee',label:'Renforcée par les faits',tone:'pos'};
  if(t.pl!=null&&t.pl>=0)
    return {key:'intacte',label:'Intacte',tone:'pos'};
  return {key:'surveiller',label:'À surveiller',tone:'muted'};
}

/* Gestion des gagnants — RÈGLES INDICATIVES uniquement (§19). Jamais une sortie
   automatique : « laisser courir » est la règle par défaut d'une thèse qui tient. */
function winnerRule(pl){
  if(pl==null||pl<20)return null;
  if(pl>=100)return 'Gain ≥ +100 % : sécuriser 25-50 % et laisser courir le reste (règle indicative).';
  if(pl>=75) return 'Gain ≥ +75 % : envisager de sécuriser une fraction, laisser courir le reste.';
  if(pl>=50) return 'Gain ≥ +50 % : relever le stop sous le prix, réévaluer la thèse (jamais vendre par réflexe).';
  if(pl>=30) return 'Gain ≥ +30 % : verrouiller le risque (stop au-dessus du prix moyen).';
  return 'Gain ≥ +20 % : trade validé — laisser courir tant que la thèse tient.';
}

/* Prochaine action ANALYTIQUE (§17-19). GARDE-FOU PERDANTS : une position en
   perte ne reçoit JAMAIS « renforcer » sans confirmation positive explicite —
   sinon message d'interdiction. Aucune de ces actions n'exécute d'ordre. */
function nextAction(t){
  const st=thesisState(t);
  if(st.key==='cassee')
    return {label:'Réévaluer la sortie — invalidation atteinte',tone:'neg'};
  if(st.key==='fragilisee')
    return {label:'Surveiller de près — thèse proche de l’invalidation',tone:'warn'};
  if(t.pl!=null&&t.pl<0){
    /* Perte SANS confirmation → renforcement formellement interdit (§18). */
    if(!hasPositiveConfirmation(t))
      return {label:'Renforcement interdit : aucune confirmation positive détectée',tone:'neg'};
    return {label:'Confirmation détectée — renforcement possible seulement après revue',tone:'muted'};
  }
  const wr=winnerRule(t.pl);
  if(wr)return {label:wr,tone:'pos'};
  return {label:'Conserver — thèse intacte, laisser courir',tone:'muted'};
}

/* Niveau analytique S+/S/A/B et borne d'allocation indicative (SKILL). Repère,
   jamais un ordre. Dérivé du score du snapshot d'entrée (/40 si présent). */
function tierOf(t){
  const sc=Number((t.entrySnap||{}).score);
  if(!isFinite(sc))return null;
  const n=sc<=40?sc:Math.round(sc/2.5);   /* tolère un score /100 → /40 */
  if(n>=36)return {tier:'S+',max:15};
  if(n>=32)return {tier:'S',max:10};
  if(n>=28)return {tier:'A',max:5};
  return {tier:'B',max:2};
}

/* Métriques de synthèse (LOT A/E) — poids, concentration Top1/Top3, exposition.
   Poids calculés sur la valeur de marché (repli au coût), cash séparé. */
function computeMetrics(rich,cash){
  const stocks=rich.filter(t=>t.type==='STK'),opts=rich.filter(t=>t.type!=='STK');
  const invested=rich.reduce((s,t)=>s+t.invested,0);
  const allMarked=rich.length&&rich.every(t=>t.value!==null);
  const grossVal=rich.reduce((s,t)=>s+(t.value??t.invested??0),0);
  const plAbs=allMarked?rich.reduce((s,t)=>s+t.plAbs,0):null;
  const netValue=grossVal+(cash||0);
  const weights=rich.map(t=>({sym:t.sym,type:t.type,
    w:grossVal?((t.value??t.invested??0)/grossVal*100):null}))
    .filter(x=>x.w!=null).sort((a,b)=>b.w-a.w);
  const top1=weights.length?weights[0]:null;
  const top3=weights.slice(0,3).reduce((s,x)=>s+x.w,0);
  const optVal=opts.reduce((s,t)=>s+(t.value??t.invested??0),0);
  const stkVal=stocks.reduce((s,t)=>s+(t.value??t.invested??0),0);
  const denom=grossVal+(cash||0);
  return {stocks,opts,invested,allMarked,grossVal,plAbs,netValue,weights,top1,top3,
    optPct:denom?optVal/denom*100:null,stkPct:denom?stkVal/denom*100:null,
    cashPct:denom&&cash!=null?cash/denom*100:null,cash};
}

/* Risque dominant unique (LOT A/F) — priorité : invalidation atteinte >
   sur-concentration Top1 > option DTE court > sur-exposition options. */
function dominantRisk(rich,m){
  const broken=rich.filter(t=>thesisState(t).key==='cassee');
  if(broken.length)
    return {label:`${broken.length} position(s) sous invalidation`,
      detail:broken.map(t=>t.sym).join(' · '),tone:'neg'};
  if(m.top1&&m.top1.w>25)
    return {label:`Concentration élevée : ${m.top1.sym} = ${VX.fmt.num(m.top1.w,0)} % du portefeuille`,
      detail:'au-delà d’un repère prudent (~15 % pour un titre)',tone:'warn'};
  const shortDte=rich.filter(t=>t.type!=='STK'&&t.exp&&((new Date(t.exp)-Date.now())/86400000)<=7);
  if(shortDte.length)
    return {label:`${shortDte.length} option(s) à échéance ≤ 7 j`,
      detail:shortDte.map(t=>t.sym).join(' · '),tone:'warn'};
  if(m.optPct!=null&&m.optPct>25)
    return {label:`Exposition options élevée : ${VX.fmt.num(m.optPct,0)} %`,
      detail:'les options concentrent le risque de temps (theta)',tone:'warn'};
  return {label:'Aucun risque critique détecté',
    detail:'concentration et invalidations dans les repères',tone:'muted'};
}

/* Action prioritaire unique (LOT A) — la position qui exige une décision. */
function priorityAction(rich){
  const scored=rich.map(t=>{const st=thesisState(t);
    const rank={cassee:3,fragilisee:2,surveiller:0,insuffisant:0,intacte:0,renforcee:0}[st.key]||0;
    return {t,st,rank};}).filter(x=>x.rank>0).sort((a,b)=>b.rank-a.rank);
  if(scored.length){const x=scored[0];
    return {sym:x.t.sym,label:nextAction(x.t).label,tone:nextAction(x.t).tone};}
  const bigWin=rich.filter(t=>t.pl!=null&&t.pl>=50).sort((a,b)=>b.pl-a.pl)[0];
  if(bigWin)return {sym:bigWin.sym,label:winnerRule(bigWin.pl),tone:'pos'};
  return {sym:null,label:'Aucune décision urgente — laisser courir les thèses intactes',tone:'muted'};
}

/* Bande KPI de contexte (positions/options/risk) — jamais un chiffre inventé. */
function renderSummary(rich){
  const host=$('pf-summary');if(!host)return;
  if(!rich.length){host.innerHTML='';return;}
  const stocks=rich.filter(t=>t.type==='STK'),opts=rich.filter(t=>t.type!=='STK');
  const invested=rich.reduce((s,t)=>s+t.invested,0);
  const marked=rich.filter(t=>t.value!==null);
  const value=marked.length===rich.length?rich.reduce((s,t)=>s+t.value,0):null;
  const pl=value!==null&&invested?(value-invested):null;
  const cell=(label,val,delta,cls)=>`<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3">
    <span class="vx-kpi-label">${label}</span>
    <span class="vx-kpi-value" style="font-size:20px">${val}</span>
    ${delta?`<span class="vx-kpi-delta ${cls||'vx-muted'}">${delta}</span>`:''}</div>`;
  host.innerHTML=
    cell('Valeur',value!==null?VX.fmt.price(value):VX.fmt.price(invested),
      value!==null?'marques live/desk':'au coût (marques indisponibles)')
    +cell('P&L latent',pl!==null?VX.fmt.price(pl):'n/d',
      pl!==null?VX.fmt.pct(pl/invested*100,1):'IBKR hors ligne',
      pl>0?'vx-pos':pl<0?'vx-neg':'vx-muted')
    +cell('Actions',stocks.length+' / 10',
      stocks.length>=10?'complet — remplacement obligatoire':'places disponibles',
      stocks.length>=10?'vx-warn':'')
    +cell('Options tactiques',opts.length+' / 3',
      `CALLS ${opts.filter(t=>t.type==='CALL').length} · PUTS ${opts.filter(t=>t.type==='PUT').length} / 1 max`,
      (opts.length>=3||opts.filter(t=>t.type==='PUT').length>1)?'vx-warn':'');
}

/* Freshness honnête (LOT A/I) — état réel de la source, jamais « live » par défaut. */
function freshBadge(){
  const st=window.__pfLive?'live':'delayed';
  const map={live:['LIVE','vx-pos'],delayed:['DELAYED','vx-warn'],offline:['OFFLINE','vx-neg']};
  const has=E()&&E().positions().length;
  const s=has?st:'offline';const m=map[s]||map.delayed;
  return `<span class="vx-freshness" data-state="${s}"><span class="vx-live-dot" data-live="${s==='live'?'1':'0'}"></span>${m[0]}</span>`;
}

/* ═══ SYNTHÈSE — PREMIER ÉCRAN (LOT A + H) ═══ */
async function renderSynthese(){
  const pos=E().positions();
  $('pf-summary').innerHTML='';
  if(!pos.length){
    $('pf-body').innerHTML=VX.states.empty(
      'Aucune position déclarée — le portefeuille répond « où suis-je exposé ? » '
      +'dès la première position. Déclare une position ou importe depuis IBKR (lecture seule).',
      '<button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>'
      +' <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities">Chercher des candidats →</a>');
    return;
  }
  const rich=enrich(pos,await quotesFor(pos));
  const cash=E().capital();
  const m=computeMetrics(rich,cash);
  const risk=dominantRisk(rich,m);
  const act=priorityAction(rich);
  const demo=window.__pfLive===false;

  /* Hero éditorial — honnête (données réelles uniquement), ≤ 1 message. */
  const plLine=m.plAbs!=null
    ?`<b class="${m.plAbs>=0?'vx-pos':'vx-neg'}">${m.plAbs>=0?'+':''}${VX.fmt.price(m.plAbs)}</b> de P&L latent`
    :'P&L latent <b>indisponible</b> (marques IBKR hors ligne — aucun chiffre inventé)';
  const concLine=m.top1?`Ta plus grosse position pèse <b>${VX.fmt.num(m.top1.w,0)} %</b> (${m.top1.sym}) · Top 3 = <b>${VX.fmt.num(m.top3,0)} %</b>`:'';
  const hero=`<section class="vx-card vx-card--hero vx-mb3" aria-label="Synthèse du portefeuille">
    <div class="vx-flex vx-wrap" style="justify-content:space-between;align-items:flex-start;gap:10px">
      <div style="max-width:640px">
        <div class="vx-flex" style="gap:8px;align-items:center;margin-bottom:6px">
          <span class="vx-eyebrow">Synthèse</span>${freshBadge()}
          ${demo?'<span class="vx-badge-demo">DÉMO</span>':''}</div>
        <h2 style="margin:0 0 6px;font-size:22px;line-height:1.25">
          ${m.netValue!=null?VX.fmt.price(m.netValue):'n/d'} de valeur nette · ${plLine}</h2>
        <p class="vx-dim" style="margin:0;font-size:13.5px;line-height:1.5">${concLine}${concLine?' · ':''}${rich.length} position(s), ${m.opts.length} option(s).</p>
      </div>
      <div class="vx-flex" style="gap:8px;flex-wrap:wrap">
        <a class="vx-btn vx-btn-sm vx-btn-primary" href="/portfolio?view=positions">Voir le tableau des positions →</a>
        <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio?view=risk">Analyser le risque</a>
      </div>
    </div>
    <div class="vx-grid vx-mt3">
      <div class="vx-insight vx-col-6" data-tone="risk">
        <span class="vx-kpi-label">Risque dominant</span>
        <div class="${toneCls(risk.tone)}" style="font-weight:600;margin-top:3px">${esc(risk.label)}</div>
        <div class="vx-meta">${esc(risk.detail)}</div></div>
      <div class="vx-insight vx-col-6" data-tone="action">
        <span class="vx-kpi-label">Action prioritaire</span>
        <div class="${toneCls(act.tone)}" style="font-weight:600;margin-top:3px">${act.sym?'<span class="vx-ticker">'+esc(act.sym)+'</span> — ':''}${esc(act.label)}</div>
        <div class="vx-meta">analyse — aucune exécution d’ordre</div></div>
    </div></section>`;

  /* 4 KPI canoniques (LOT A) — valeur nette · P&L · concentration · exposition. */
  const kpi=(label,val,sub,cls)=>`<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3">
    <span class="vx-kpi-label">${label}</span><span class="vx-kpi-value" style="font-size:21px">${val}</span>
    <span class="vx-kpi-delta ${cls||'vx-muted'}">${sub}</span></div>`;
  const kpis=`<div class="vx-grid vx-mb3">
    ${kpi('Valeur nette',m.netValue!=null?VX.fmt.price(m.netValue):'n/d',
      m.cash!=null?('dont cash '+VX.fmt.price(m.cash)):'cash non renseigné',m.allMarked?'':'vx-warn')}
    ${kpi('P&L latent total',m.plAbs!=null?((m.plAbs>=0?'+':'')+VX.fmt.price(m.plAbs)):'n/d',
      m.plAbs!=null?(VX.fmt.pct(m.grossVal-m.plAbs?m.plAbs/(m.grossVal-m.plAbs)*100:0,1)+' · marques '+(window.__pfLive?'live':'desk')):'IBKR hors ligne',
      m.plAbs>0?'vx-pos':m.plAbs<0?'vx-neg':'vx-muted')}
    ${kpi('Concentration',m.top1?VX.fmt.num(m.top1.w,0)+' %':'n/d',
      m.top1?('Top 1 '+m.top1.sym+' · Top 3 '+VX.fmt.num(m.top3,0)+' %'):'poids indisponibles',
      (m.top1&&m.top1.w>25)?'vx-warn':'')}
    ${kpi('Exposition',m.optPct!=null?('options '+VX.fmt.num(m.optPct,0)+' %'):'n/d',
      m.cashPct!=null?('cash '+VX.fmt.num(m.cashPct,0)+' % · actions '+VX.fmt.num(m.stkPct,0)+' %'):'—',
      (m.optPct!=null&&m.optPct>25)?'vx-warn':'')}
  </div>`;

  $('pf-body').innerHTML=hero+kpis
    +'<div id="pf-diff" class="vx-mb3"></div>'
    +`<section class="vx-card vx-mb3" aria-label="Allocation et concentration">
        <div class="vx-chart-head"><span class="vx-chart-title">Allocation & concentration du capital</span>
          <span class="vx-chart-question">Où le capital est-il réellement concentré ?</span></div>
        <div id="pf-alloc-tree" style="height:260px"></div>
        <div class="vx-card-foot"><span class="vx-meta">Taille = poids (valeur de marché, repli au coût) · couleur = P&amp;L latent (émeraude gagnant / corail perdant / neutre sans marque). Positions déclarées — aucune valeur inventée.</span></div>
      </section>`
    +`<section class="vx-card" aria-label="Positions exigeant une décision"><div class="vx-card-header">
        <span class="vx-card-title">Positions exigeant une décision</span>
        <span class="vx-meta vx-right"><a href="/portfolio?view=positions">Tableau complet →</a></span></div>
        <div id="pf-decision-list"></div></section>`;

  renderDiff(m,rich);

  /* Treemap allocation/concentration (1 graphique majeur, avec conclusion). */
  if(window.VXCharts&&VXCharts.treemap){
    const cc=VXCharts.colors;const el=$('pf-alloc-tree');const w=(el&&el.clientWidth)||900;
    VXCharts.treemap(el,{width:w,height:260,
      items:rich.map(t=>({label:t.sym,value:Math.max(1,t.value??t.invested??0),
        sub:(t.pl!=null?((t.pl>=0?'+':'')+VX.fmt.num(t.pl,1)+'%'):(t.type!=='STK'?t.type:'')),
        color:(t.pl>0?cc.positive:t.pl<0?cc.negative:cc.neutral)})),
      fmt:(v)=>VX.fmt.price(v)});
  }

  /* Aperçu « positions à décision » — les plus urgentes (cassée/fragilisée/gagnants). */
  const urgent=rich.map(t=>({t,st:thesisState(t)}))
    .filter(x=>['cassee','fragilisee'].includes(x.st.key)||(x.t.pl!=null&&x.t.pl>=50))
    .slice(0,5);
  const dl=$('pf-decision-list');
  if(dl){
    if(!urgent.length){dl.innerHTML=VX.states.empty('Aucune position urgente — toutes les thèses sont intactes ou en surveillance normale.');}
    else{dl.innerHTML=urgent.map(x=>{const t=x.t,na=nextAction(t);
      return `<div class="vx-flex" style="padding:9px 0;border-bottom:1px dashed var(--vx-border-soft);gap:10px;align-items:center">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${t.sym}">${t.sym}</button>
        <span class="vx-badge ${toneCls(x.st.tone)}">${esc(x.st.label)}</span>
        <span class="vx-num vx-mono ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':'vx-muted'}">${t.pl!=null?VX.fmt.pct(t.pl,1):'n/d'}</span>
        <span class="vx-grow vx-truncate ${toneCls(na.tone)}" style="font-size:12.5px">${esc(na.label)}</span>
      </div>`;}).join('');}
  }
}

/* Diff « depuis ta dernière visite » (LOT H) — honnête, jamais fabriqué. */
function renderDiff(m,rich){
  const host=$('pf-diff');if(!host)return;
  let base=null;try{base=JSON.parse(localStorage.getItem('vxPortfolioBaseline')||'null');}catch(e){}
  const now=Date.now();
  const snapshot={ts:now,netValue:m.netValue,plAbs:m.plAbs,
    byPl:Object.fromEntries(rich.filter(t=>t.pl!=null).map(t=>[t.sym,t.pl]))};
  /* (Re)poser la référence : première fois, ou si > 12 h (une « visite » distincte),
     et uniquement avec des marques réelles pour éviter un delta trivial. */
  if(m.allMarked&&(!base||(now-(base.ts||0))>43200000)){
    try{localStorage.setItem('vxPortfolioBaseline',JSON.stringify(snapshot));}catch(e){}
  }
  if(!base||base.netValue==null){
    host.innerHTML=`<section class="vx-card vx-card--compact"><div class="vx-card-header">
      <span class="vx-card-title">Depuis ta dernière visite</span></div>
      <div class="vx-meta">Aucun historique de comparaison disponible — la référence se pose à cette visite.</div></section>`;
    return;
  }
  const dNet=(m.netValue!=null&&base.netValue!=null)?(m.netValue-base.netValue):null;
  const dPl=(m.plAbs!=null&&base.plAbs!=null)?(m.plAbs-base.plAbs):null;
  const movers=Object.keys(snapshot.byPl).filter(s=>base.byPl&&base.byPl[s]!=null)
    .map(s=>({s,d:snapshot.byPl[s]-base.byPl[s]})).filter(x=>Math.abs(x.d)>=0.5)
    .sort((a,b)=>Math.abs(b.d)-Math.abs(a.d)).slice(0,3);
  host.innerHTML=`<section class="vx-card vx-card--compact"><div class="vx-card-header">
    <span class="vx-card-title">Depuis ta dernière visite</span>
    <span class="vx-meta vx-right">réf. ${VX.fmt.ago(base.ts)}</span></div>
    <div class="vx-flex vx-wrap" style="gap:18px">
      <span>Valeur nette : <b class="${dNet>0?'vx-pos':dNet<0?'vx-neg':'vx-muted'}">${dNet!=null?((dNet>=0?'+':'')+VX.fmt.price(dNet)):'n/d'}</b></span>
      <span>P&L latent : <b class="${dPl>0?'vx-pos':dPl<0?'vx-neg':'vx-muted'}">${dPl!=null?((dPl>=0?'+':'')+VX.fmt.price(dPl)):'n/d'}</b></span>
      ${movers.length?'<span class="vx-meta">Bougé : '+movers.map(x=>esc(x.s)+' '+(x.d>=0?'+':'')+VX.fmt.num(x.d,1)+' pt').join(' · ')+'</span>':'<span class="vx-meta">Aucun mouvement notable</span>'}
    </div></section>`;
}

/* ═══ POSITIONS — TABLEAU CANONIQUE (LOT B/C/D) ═══ */
function actionListHtml(state){
  const pf=(state&&state.portfolio)||{};
  const rows=pf.positions_needing_action||[];
  if(!rows.length)return '';
  const pill=(pr)=>{const c={P0_CRITICAL:'var(--vx-negative)',P1_HIGH:'var(--vx-warning)'}[pr]||'var(--vx-text-muted)';
    return `<span class="vx-badge" style="color:${c}">${(pr||'').replace('_',' ')}</span>`;}
  return `<section class="vx-card vx-mb3"><div class="vx-card-header">
    <span class="vx-card-title">Priorités du moteur (Position Intelligence)</span>
    <span class="vx-meta vx-right">${rows.length} · P0 puis P1</span></div>
    <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
    <th>Priorité</th><th>Titre</th><th>Statut</th><th>Action analytique</th>
    <th>Verdict moteur</th><th class="vx-num">P&L</th></tr></thead><tbody>
    ${rows.map(r=>`<tr>
      <td data-label="Priorité">${pill(r.priority)}</td>
      <td data-label="Titre"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.symbol}">${r.symbol}</button></td>
      <td data-label="Statut">${esc((r.status||'').replace(/_/g,' '))}</td>
      <td data-label="Action"><b>${esc((r.action||'').replace(/_/g,' '))}</b></td>
      <td data-label="Verdict">${r.decision?`<span class="vx-badge vx-badge-decision" data-decision="${(r.decision||'').replace('É','E')}">${r.decision}</span>`:'—'}</td>
      <td data-label="P&L" class="vx-num ${r.pl_pct>0?'vx-pos':r.pl_pct<0?'vx-neg':''}">${r.pl_pct!=null?VX.fmt.pct(r.pl_pct,1):'n/d'}</td>
    </tr>`).join('')}</tbody></table></div>
    <div class="vx-card-footer">${VX.updateIndicator(state.updated_at,'Position Intelligence',state.live?'live':'fallback')}
    · verdicts moteur — aucune action n’exécute d’ordre</div></section>`;
}

async function renderPositions(){
  const pos=E().positions();
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  if(!pos.length){
    $('pf-body').innerHTML=VX.states.empty('Aucune position déclarée.',
      '<button class="vx-btn vx-btn-sm vx-btn-primary" onclick="VXEntities.openAddModal(\'\',\'position\')">Déclarer une position</button>');
    return;
  }
  let ibkr=null,posState=null;
  try{ibkr=await VX.fetch('/api/ibkr/positions',{ttl:120000});}catch(e){}
  try{posState=await VX.fetch('/api/positions/state',{ttl:30000});}catch(e){}
  const perShare=(t)=>t.qty?(t.type==='STK'?t.cost/t.qty:t.cost/(t.qty*100)):null;
  const total=rich.reduce((s,t)=>s+(t.value??t.invested??0),0);
  const stBadge=(st)=>`<span class="vx-badge ${toneCls(st.tone)}" title="État de thèse">${esc(st.label)}</span>`;
  const convOf=(t)=>{const s=t.entrySnap||{};const tr=tierOf(t);
    if(tr)return `${tr.tier} · ${VX.fmt.nd(s.score)}`;
    return s.verdict?esc(s.verdict):'—';};

  const rowHtml=(t)=>{const st=thesisState(t),na=nextAction(t),tr=tierOf(t);
    const s=t.entrySnap||{};
    const cat=s.catalyst||(s.earnings_dte!=null?('résultats ~'+s.earnings_dte+' j'):'');
    const wgt=total?( (t.value??t.invested??0)/total*100):null;
    return `<tr>
      <td data-label="Titre"><button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${t.sym}">${t.sym}</button> ${E().badges(t.sym)}</td>
      <td data-label="Instrument">${t.type}${t.strike?' '+t.strike:''}${t.exp?' '+t.exp:''}</td>
      <td data-label="Qté" class="vx-num">${t.qty}</td>
      <td data-label="Prix moyen" class="vx-num">${perShare(t)!=null?VX.fmt.price(perShare(t)):'—'}</td>
      <td data-label="Prix actuel" class="vx-num">${t.mark!=null?VX.fmt.price(t.mark):'n/d'}</td>
      <td data-label="Valeur marché" class="vx-num">${t.value!=null?VX.fmt.price(t.value):'n/d'}</td>
      <td data-label="P&L" class="vx-num ${t.plAbs>0?'vx-pos':t.plAbs<0?'vx-neg':''}">${t.plAbs!=null?((t.plAbs>=0?'+':'')+VX.fmt.price(t.plAbs)):'n/d'}</td>
      <td data-label="P&L %" class="vx-num ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}">${t.pl!=null?VX.fmt.pct(t.pl,1):'n/d'}</td>
      <td data-label="Poids" class="vx-num ${(wgt!=null&&tr&&wgt>tr.max*1.5)?'vx-warn':''}">${wgt!=null?VX.fmt.num(wgt,1)+' %':'—'}${tr?'<span class="vx-meta"> / '+tr.max+' %</span>':''}</td>
      <td data-label="Conviction">${convOf(t)}</td>
      <td data-label="État de thèse">${stBadge(st)}</td>
      <td data-label="Invalidation" class="vx-num vx-neg">${VX.fmt.nd(s.stop)}</td>
      <td data-label="Catalyseur" class="vx-truncate" style="max-width:150px">${cat?esc(cat):'—'}</td>
      <td data-label="Prochaine action" class="${toneCls(na.tone)}" style="max-width:230px;font-size:12px">${esc(na.label)}</td>
      <td data-label="Actions"><div class="vx-row-actions">
        <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${t.sym}">Analyse</button>
        <button class="vx-btn vx-btn-sm vx-btn-ghost" data-journal-pos="${t.sym}">Journaliser</button>
        <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Plus ${t.sym}">⋯</button>
      </div></td></tr>`;};

  const groups={Actions:rich.filter(t=>t.type==='STK'),Options:rich.filter(t=>t.type!=='STK')};
  $('pf-body').innerHTML=
    (posState?actionListHtml(posState):'')
    +`<div class="vx-insight vx-mb3" data-tone="risk"><b>Garde-fou perdants (Constitution §18).</b>
       Une position en perte ne reçoit jamais de suggestion « renforcer » sans confirmation positive
       explicite du marché. Une thèse n’est « cassée » que si l’invalidation pré-définie est franchie —
       jamais par une simple baisse de prix.</div>`
    +(ibkr&&ibkr.ok===false?'<div class="vx-stale-banner">IBKR hors ligne — marques desk/EOD utilisées (aucune valeur inventée).</div>':'')
    +Object.entries(groups).map(([g,list])=>`
      <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">${g}</span>
        <span class="vx-meta vx-right">${list.length}</span></div>
      ${list.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Instrument</th><th class="vx-num">Qté</th><th class="vx-num">Prix moyen</th>
        <th class="vx-num">Prix actuel</th><th class="vx-num">Valeur marché</th><th class="vx-num">P&L</th>
        <th class="vx-num">P&L %</th><th class="vx-num">Poids</th><th>Conviction</th><th>État de thèse</th>
        <th class="vx-num">Invalidation</th><th>Catalyseur</th><th>Prochaine action</th><th></th></tr></thead>
        <tbody>${list.map(rowHtml).join('')}</tbody></table></div>`
        :VX.states.empty('Aucune position '+g.toLowerCase()+'.')}
      </section>`).join('')
    +`<section class="vx-card vx-mb3" aria-label="Contribution au P&L"><div class="vx-card-header">
        <span class="vx-card-title">Contribution au P&L par position</span>
        <span class="vx-chart-question">Qui porte le résultat du portefeuille ?</span></div>
       <div id="pf-contrib-host"></div></section>`
    +`<div class="vx-card-footer">${VX.updateIndicator(Date.now(),window.__pfLive?'IBKR/desk':'desk (repli)',window.__pfLive?'live':'fallback')}
      · IBKR: ${ibkr&&ibkr.count!==undefined?ibkr.count+' position(s) broker (lecture seule)':'hors ligne'} · lecture seule — aucun ordre</div>`;

  /* Contribution au P&L (barres horizontales signées) — repli honnête sans marque. */
  const withAbs=rich.filter(t=>t.plAbs!=null).sort((a,b)=>b.plAbs-a.plAbs);
  const ch=$('pf-contrib-host');
  if(ch){
    if(!withAbs.length){ch.innerHTML='<div class="vx-meta">Marques indisponibles (IBKR hors ligne) — aucune contribution affichée plutôt qu’un chiffre inventé.</div>';}
    else if(window.VXCharts&&VXCharts.card&&VXCharts.bars){
      VXCharts.card('pf-contrib-host',{title:'Contribution au P&L par position',
        question:'Qui porte le résultat ?',
        conclusion:withAbs[0].sym+' contribue le plus ('+((withAbs[0].plAbs>=0?'+':'')+VX.fmt.price(withAbs[0].plAbs))+').',
        height:Math.max(120,Math.min(320,withAbs.length*30)),
        source:window.__pfLive?'IBKR/desk':'desk (repli)',timestamp:Date.now(),mode:window.__pfLive?'live':'fallback',
        limits:'P&L latent absolu (valeur − coût) sur positions déclarées',
        render:(cv)=>VXCharts.bars(cv,withAbs.map(t=>t.sym),withAbs.map(t=>Math.round(t.plAbs)),
          {horizontal:true,colors:withAbs.map(t=>t.plAbs>=0?VXCharts.colors.positive:VXCharts.colors.negative),
           yFmt:(v)=>VX.fmt.price(v)})});
    }
  }
  document.querySelectorAll('[data-journal-pos]').forEach(b=>b.addEventListener('click',()=>{
    const sym=b.dataset.journalPos;
    if(E().addJournalEntry){/* pré-remplissage journal — déclaratif, aucun ordre */
      window.location.href='/journal?view=journal&sym='+encodeURIComponent(sym);
    }else{window.location.href='/journal?view=journal';}
  }));
}

/* ═══ PERFORMANCE (LOT G — migrée depuis Journal, domicile unique) ═══ */
function pfTrades(){return (E()?E().journal():[]).filter(e=>(e.result==='WIN'||e.result==='LOSS')&&isFinite(Number(e.pnl)));}
async function renderPerformance(){
  const pos=E().positions();
  renderSummary(enrich(pos,await quotesFor(pos)));
  const eq=(E()?E().equity():[])||[];
  const closed=(E()?E().closedPositions():[])||[];
  $('pf-body').innerHTML=`
    <div class="vx-insight vx-mb3" role="note"><b>Performance de portefeuille — domicile unique.</b>
      Courbe cumulée, drawdown, contribution et saisonnalité vivent ici (migrées depuis Journal).
      Le Journal ne conserve que la méthode, la discipline, les erreurs et l’apprentissage.</div>
    <div class="vx-grid vx-mb3">
      <div class="vx-col-7" id="pf-perf-equity"></div>
      <div class="vx-col-5" id="pf-perf-drawdown"></div>
    </div>
    <div class="vx-grid">
      <div class="vx-col-7" id="pf-perf-monthly"></div>
      <div class="vx-col-5" id="pf-perf-contrib"></div>
    </div>`;
  const emptyCard=(host,reason,action)=>{const el=$(host);if(el)el.innerHTML='<div class="vx-card">'+VX.states.empty(reason,action||'')+'</div>';};
  const JOURNAL_ACTION='<a class="vx-btn vx-btn-sm" href="/journal?view=journal">Ouvrir le journal</a>';

  /* Courbe d'équité cumulée + drawdown (série des clôtures déclarées). */
  if(eq.length>=2&&window.VXCharts&&VXCharts.equityCard){
    const labels=eq.map(p=>p.d),values=eq.map(p=>Number(p.v));
    const up=values[values.length-1]>=values[0];
    VXCharts.equityCard('pf-perf-equity',{title:'Courbe d’équité (cumulée)',timeframe:eq.length+' points',
      question:'Le capital progresse-t-il régulièrement ?',
      conclusion:up?'Équité en progression sur la période.':'Équité en retrait sur la période.',
      labels,values,height:240,source:'clôtures déclarées (myTradesEquity)',timestamp:Date.now(),mode:'delayed',
      explain:{shows:'La série d’équité issue de tes clôtures de positions.',
        why:'Une méthode saine produit une pente régulière, pas des à-coups.',
        confirm:'Nouveaux plus hauts avec drawdowns contenus.',invalidate:'Série de plus bas d’équité.'}});
    VXCharts.drawdownCard('pf-perf-drawdown',{title:'Drawdown depuis les pics',
      question:'Les pertes de portefeuille restent-elles contrôlées ?',
      conclusion:'Dérivé arithmétiquement de la courbe d’équité.',
      labels,values,height:240,source:'clôtures déclarées (myTradesEquity)',timestamp:Date.now(),mode:'delayed',
      limits:'dérivé de la série déclarée — pas un indicateur de marché',
      explain:{shows:'L’écart en % entre l’équité et son dernier pic.',
        why:'La profondeur des drawdowns mesure la discipline de risque réelle.',
        confirm:'Drawdowns courts et peu profonds.',invalidate:'Drawdown qui s’aggrave.'}});
  }else{
    emptyCard('pf-perf-equity','Courbe d’équité indisponible — elle se construit au fil des clôtures de positions déclarées.',JOURNAL_ACTION);
    emptyCard('pf-perf-drawdown','Drawdown indisponible sans courbe d’équité.');
  }

  /* Saisonnalité mensuelle (période) — moyenne simple des % de clôture par mois. */
  const withPl=closed.filter(t=>t.pnl_pct!==undefined&&t.pnl_pct!==null&&t.closed);
  if(withPl.length>=3&&window.VXCharts&&VXCharts.heatmapCard){
    const byMonth={};
    withPl.forEach(t=>{const m2=String(t.closed).slice(0,7);(byMonth[m2]=byMonth[m2]||[]).push(Number(t.pnl_pct));});
    const months=Object.keys(byMonth).sort();
    const years=[...new Set(months.map(m2=>m2.slice(0,4)))];
    const MN=['01','02','03','04','05','06','07','08','09','10','11','12'];
    const ML=['J','F','M','A','M','J','J','A','S','O','N','D'];
    VXCharts.heatmapCard('pf-perf-monthly',{title:'P&L moyen par mois (clôtures)',
      question:'Y a-t-il des périodes de sur- ou sous-performance ?',
      conclusion:months.length+' mois avec clôtures · moyenne simple des % par trade.',columns:ML,
      rows:years.map(y=>({label:y,cells:MN.map(mm=>{const arr=byMonth[y+'-'+mm];
        return arr?{value:arr.reduce((a,b)=>a+b,0)/arr.length,title:arr.length+' clôture(s)'}:{value:null,label:'·'};})})),
      min:-8,max:8,fmt:(v)=>v===null?'·':VX.fmt.pct(v,1),
      source:'clôtures déclarées',timestamp:Date.now(),mode:'delayed',
      limits:'moyenne des % par trade — pas une performance composée'});
  }else{emptyCard('pf-perf-monthly','Saisonnalité disponible à partir de 3 clôtures datées.',JOURNAL_ACTION);}

  /* Contribution par position (positions ouvertes, P&L latent absolu). */
  const rich=enrich(pos,await quotesFor(pos));
  const withAbs=rich.filter(t=>t.plAbs!=null).sort((a,b)=>b.plAbs-a.plAbs);
  if(withAbs.length&&window.VXCharts&&VXCharts.card&&VXCharts.bars){
    VXCharts.card('pf-perf-contrib',{title:'Contribution au P&L (positions ouvertes)',
      question:'Qui porte le résultat latent ?',
      conclusion:withAbs[0].sym+' domine ('+((withAbs[0].plAbs>=0?'+':'')+VX.fmt.price(withAbs[0].plAbs))+').',
      height:Math.max(160,Math.min(300,withAbs.length*30)),source:window.__pfLive?'IBKR/desk':'desk (repli)',
      timestamp:Date.now(),mode:window.__pfLive?'live':'fallback',limits:'P&L latent absolu (valeur − coût)',
      render:(cv)=>VXCharts.bars(cv,withAbs.map(t=>t.sym),withAbs.map(t=>Math.round(t.plAbs)),
        {horizontal:true,colors:withAbs.map(t=>t.plAbs>=0?VXCharts.colors.positive:VXCharts.colors.negative),
         yFmt:(v)=>VX.fmt.price(v)})});
  }else{emptyCard('pf-perf-contrib','Contribution indisponible — aucune marque (IBKR hors ligne).');}
}

/* ═══ OPTIONS COMMAND CENTER (§19 — inchangé, refonte dédiée PR n°7) ═══ */
async function renderOptions(){
  const pos=E().positions();
  const opts=pos.filter(t=>t.type!=='STK');
  const rich=enrich(opts,await quotesFor(opts));
  renderSummary(enrich(pos,await quotesFor(pos)));
  if(!opts.length){
    $('pf-body').innerHTML=VX.states.empty(
      'Aucune position option — le sélecteur Vertex Dynamic Options privilégie les CALLS (max 3, dont 1 PUT tactique).',
      '<a class="vx-btn vx-btn-sm vx-btn-primary" href="/opportunities?view=options">Chercher un contrat</a>');
    return;
  }
  const calls=rich.filter(t=>t.type==='CALL'),puts=rich.filter(t=>t.type==='PUT');
  const engaged=rich.reduce((s2,t)=>s2+t.invested,0);
  const marked=rich.filter(t=>t.pl!==null);
  const plTot=marked.length===rich.length&&rich.length?rich.reduce((s2,t)=>s2+(t.value-t.invested),0):null;
  const dtes=rich.map(t=>t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null).filter(v=>v!==null);
  const dteAvg=dtes.length?Math.round(dtes.reduce((a,b)=>a+b,0)/dtes.length):null;
  const H=(l,v,d,cls)=>`<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3">
    <span class="vx-kpi-label">${l}</span><span class="vx-kpi-value" style="font-size:20px">${v}</span>
    ${d?`<span class="vx-kpi-delta ${cls||'vx-muted'}">${d}</span>`:''}</div>`;
  $('pf-body').innerHTML=
    `<div class="vx-grid vx-mb3">
      ${H('CALLS ouverts',calls.length,'direction principale (~90 %)')}
      ${H('PUTS tactiques',puts.length+' / 1',puts.length>1?'PLAFOND DÉPASSÉ':'rares, jamais « parce que ça baisse »',puts.length>1?'vx-neg':'')}
      ${H('Capital engagé',VX.fmt.price(engaged),'coût total déclaré')}
      ${H('P&L options',plTot!==null?VX.fmt.price(plTot):'n/d',plTot!==null?VX.fmt.pct(plTot/engaged*100,1):'marques indisponibles (IBKR hors ligne)',plTot>0?'vx-pos':plTot<0?'vx-neg':'vx-muted')}
    </div>
    <div class="vx-grid vx-mb3">
      ${H('DTE moyen',dteAvg!==null?dteAvg+' j':'n/d','constitution : 60-270, préf. 90-210')}
      ${H('Delta total','n/d','Greeks broker requis — jamais estimés sans IBKR')}
      ${H('Theta quotidien','n/d','IBKR hors ligne')}
      ${H('Risque événementiel',rich.some(t=>t.entrySnap&&t.entrySnap.earnings_dte!=null)?'à vérifier':'—','earnings par position ci-dessous')}
    </div>
    <section class="vx-card vx-mb3" aria-label="Allocation du capital options">
      <div class="vx-chart-head"><span class="vx-chart-title">Capital engagé par contrat</span>
        <span class="vx-chart-question">Où est concentré le capital options ?</span></div>
      <div id="pf-opt-tree" style="height:220px"></div>
      <div class="vx-card-foot"><span class="vx-meta">Taille = capital engagé (coût déclaré) · couleur = sens (CALL acier / PUT violet). Aucune valeur inventée.</span></div>
    </section>
    <div id="pf-opt-combined" class="vx-grid vx-mb3"></div>
    <section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Positions options</span>
      <span class="vx-meta vx-right">analyse complète par position — aucune exécution</span></div>
    <div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
      <th>Contrat</th><th class="vx-num">Qté</th><th class="vx-num">Coût</th><th class="vx-num">Marque</th>
      <th class="vx-num">P&L</th><th class="vx-num">DTE</th><th>Stop sous-jacent</th><th></th></tr></thead><tbody>
    ${rich.map(t=>{
      const dte=t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null;
      return `<tr>
      <td data-label="Contrat"><span class="vx-ticker">${t.sym}</span>
        <span class="vx-badge" style="color:var(--vx-option)">${t.type} ${t.strike??''} ${t.exp||''}</span></td>
      <td data-label="Qté" class="vx-num">${t.qty}</td>
      <td data-label="Coût" class="vx-num">${VX.fmt.price(t.cost)}</td>
      <td data-label="Marque" class="vx-num">${t.mark!==null?VX.fmt.price(t.mark):'n/d'}</td>
      <td data-label="P&L" class="vx-num ${t.pl>0?'vx-pos':t.pl<0?'vx-neg':''}">${t.pl!==null?VX.fmt.pct(t.pl,1):'n/d'}</td>
      <td data-label="DTE" class="vx-num ${dte!==null&&dte<=7?'vx-warn':''}">${dte!==null?dte+' j':'—'}</td>
      <td data-label="Stop">${VX.fmt.nd(t.entrySnap&&t.entrySnap.stop)}</td>
      <td><div class="vx-row-actions">
        <button class="vx-btn vx-btn-sm vx-btn-primary" data-opt-analyze="${t.id}">Analyser</button>
        <button class="vx-btn vx-btn-icon vx-btn-ghost" data-entity-menu="${t.sym}" aria-label="Plus">⋯</button>
      </div></td></tr>`;}).join('')}</tbody></table></div>
    <div class="vx-card-footer">${VX.updateIndicator(Date.now(),window.__pfLive?'IBKR/desk':'desk (repli)',window.__pfLive?'live':'fallback')}
      · Greeks agrégés affichés uniquement avec IBKR (jamais estimés en agrégat)</div></section>`;
  if(window.VXCharts&&VXCharts.treemap){
    const cc=VXCharts.colors;const el=document.getElementById('pf-opt-tree');const w=(el&&el.clientWidth)||900;
    VXCharts.treemap(el,{width:w,height:220,
      items:rich.map(t=>({label:t.sym+' '+(t.strike||''),value:Math.max(1,t.invested||0),
        sub:(t.type==='PUT'?'PUT':'CALL')+(t.exp?' '+t.exp:''),
        color:(t.type==='PUT'?(cc.violet||'#9c79d0'):(cc.neutral||'#9d978e'))})),
      fmt:(v)=>VX.fmt.price(v)});
  }
  document.querySelectorAll('[data-opt-analyze]').forEach(b=>
    b.addEventListener('click',()=>openOptionDrawer(rich.find(t=>String(t.id)===b.dataset.optAnalyze))));
  renderCombinedOptions(rich);
}

async function renderCombinedOptions(rich){
  const host=document.getElementById('pf-opt-combined'); if(!host)return;
  const by={};
  rich.forEach(t=>{ if(t.type==='CALL'||t.type==='PUT'){(by[t.sym]=by[t.sym]||[]).push(t);} });
  const syms=Object.keys(by);
  if(!syms.length){host.innerHTML='';return;}
  const results=await Promise.all(syms.map(async sym=>{
    const group=by[sym];
    const spot=group.map(t=>t.underSpot).find(s=>s!=null);
    if(spot==null)return null;
    const legs=group.map(t=>({type:(t.type||'').toLowerCase(),strike:t.strike,
      premium:(t.qty&&t.cost)?t.cost/(t.qty*100):null,qty:t.qty}));
    if(legs.some(l=>l.premium==null||l.strike==null))return null;
    const dtes=group.map(t=>t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null).filter(v=>v!=null);
    const days=dtes.length?Math.min.apply(null,dtes):null;
    try{
      const r=await fetch('/api/options/analyze',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({legs:legs,spot:spot,iv:null,days:days,name:sym})});
      const d=await r.json(); if(!d||!d.available)return null; return {sym:sym,spot:spot,group:group,d:d};
    }catch(e){return null;}
  }));
  const ok=results.filter(Boolean);
  if(!ok.length){host.innerHTML='';return;}
  host.innerHTML=ok.map((x,i)=>{
    const d=x.d;
    const mp=d.max_profit_unbounded?'illimité':(d.max_profit!=null?VX.fmt.price(d.max_profit):'—');
    const be=(d.breakevens&&d.breakevens.length)?d.breakevens.map(b=>VX.fmt.nd(b)).join(' · '):'—';
    return `<section class="vx-card vx-col-6">
      <div class="vx-card-header"><span class="vx-card-title">${esc(x.sym)} — structure combinée (${x.group.length} jambe${x.group.length>1?'s':''})</span>
        <span class="vx-badge" style="color:var(--vx-${d.is_credit?'positive':'option'})">${d.is_credit?'crédit ':'débit '}${VX.fmt.price(Math.abs(d.net_premium))}</span></div>
      <div id="pf-comb-pf-${i}" style="height:150px"></div>
      <div class="vx-grid vx-mt2" style="grid-template-columns:repeat(3,1fr);gap:6px">
        <div class="vx-kv"><span class="k">Gain max</span><span class="v vx-mono">${mp}</span></div>
        <div class="vx-kv"><span class="k">Perte max</span><span class="v vx-mono vx-neg">${d.max_loss!=null?VX.fmt.price(d.max_loss):'—'}</span></div>
        <div class="vx-kv"><span class="k">Breakevens</span><span class="v vx-mono">${be}</span></div>
      </div>
      <div class="vx-card-foot"><span class="vx-meta">Payoff à l’échéance depuis tes positions réelles (spot ${VX.fmt.nd(x.spot)}) · greeks/PoP requièrent l’IV.</span></div>
    </section>`;
  }).join('');
  ok.forEach((x,i)=>{
    const cont=document.getElementById('pf-comb-pf-'+i); const pts=x.d.payoff||[];
    if(!cont||!window.VXCharts||pts.length<2)return;
    cont.innerHTML='<canvas></canvas>';
    VXCharts.mount(cont.querySelector('canvas'),{type:'line',
      data:{labels:pts.map(p=>p.price),datasets:[{data:pts.map(p=>p.pnl),borderColor:VXCharts.colors.neutral,
        borderWidth:1.6,pointRadius:0,fill:false,tension:0,
        segment:{borderColor:(ctx)=>ctx.p1.parsed.y>=0?VXCharts.colors.positive:VXCharts.colors.negative}}]},
      options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:(ctx)=>'P&L '+VX.fmt.price(ctx.parsed.y)+' @ '+VX.fmt.nd(ctx.label)}}},
        scales:{x:{ticks:{maxTicksLimit:6},grid:{display:false}},y:{grid:{color:'rgba(255,255,255,.06)'},ticks:{callback:(v)=>VX.fmt.price(v)}}}}});
  });
}

async function openOptionDrawer(t){
  if(!t)return;
  const dte=t.exp?Math.round((new Date(t.exp)-Date.now())/86400000):null;
  const unit=t.qty?t.cost/(t.qty*100):null;
  const snap=t.entrySnap||{};
  const kvR=(k,v,cls)=>`<div class="vx-kv"><span class="k">${k}</span><span class="v vx-mono ${cls||''}">${VX.fmt.nd(v)}</span></div>`;
  VX.shell.openDrawer(`${t.sym} ${t.type} ${t.strike??''} ${t.exp||''}`,
    `<h3 class="vx-mb2">Identité</h3>
     ${kvR('Contrat',`${t.sym} ${t.type} ${t.strike??'—'} · ${t.exp||'—'}`)}
     ${kvR('DTE',dte!==null?dte+' j':'—',dte!==null&&dte<=7?'vx-warn':'')}
     ${kvR('Quantité × multiplicateur',t.qty+' × 100')}
     ${kvR('Coût moyen (prime/action)',unit!==null?VX.fmt.price(unit):'—')}
     ${kvR('Capital engagé',VX.fmt.price(t.cost))}
     <h3 class="vx-mt4 vx-mb2">Marché</h3><div id="od-market">${kvR('Marque',t.mark!==null?VX.fmt.price(t.mark):'n/d (IBKR hors ligne)')}
     ${kvR('P&L',t.pl!==null?VX.fmt.pct(t.pl,1):'n/d',t.pl>0?'vx-pos':t.pl<0?'vx-neg':'')}
     <div class="vx-meta">bid/ask/volume/OI/IV/Greeks : fournis par IBKR uniquement — jamais estimés ici.</div></div>
     <h3 class="vx-mt4 vx-mb2">Plan</h3>
     ${kvR('Invalidation (sous-jacent)',snap.stop,'vx-neg')}
     ${kvR('Objectif',snap.tgt,'vx-pos')}
     ${kvR('Objectif de gain typique','+50 % (jamais garanti)')}
     ${kvR('Time stop','réévaluer avant '+(dte!==null?Math.max(5,Math.round(dte/6))+' j':'—'))}
     <h3 class="vx-mt4 vx-mb2">Décision analytique</h3><div id="od-decision"><div class="vx-skeleton" style="height:40px"></div></div>
     <h3 class="vx-mt4 vx-mb2">Payoff à l'échéance</h3><div id="od-payoff" style="height:180px"><canvas></canvas></div>
     <h3 class="vx-mt4 vx-mb2">Scénarios (moteur)</h3><div id="od-scenarios"><div class="vx-skeleton" style="height:60px"></div></div>
     <div class="vx-help vx-mt3">⛔ Lecture seule : aucune action de cette analyse ne peut exécuter, clôturer ou modifier un ordre.</div>`);
  try{
    const q=new URLSearchParams({type:t.type,entry:unit??'',stop:snap.stop??'',tp:snap.tgt??'',
      current:t.mark??'',pl_pct:t.pl??'',dte:dte??''});
    const d=await VX.fetch('/api/position-decision/'+t.sym+'?'+q.toString(),{ttl:60000});
    const el=document.getElementById('od-decision');
    if(el)el.innerHTML=`<div class="vx-flex"><span class="vx-badge vx-badge-decision" data-decision="${(d.action||'').replace('É','E')}" style="font-size:13px;padding:4px 12px">${d.action||d.label||'n/d'}</span></div>
      <div class="vx-dim vx-mt2" style="font-size:12.5px">${(d.reasons||[]).map(r=>'· '+r).join('<br>')||d.note||''}</div>
      ${d.underlying&&d.underlying.decision?`<div class="vx-meta vx-mt2">Sous-jacent : ${d.underlying.decision}</div>`:''}`;
  }catch(e){const el=document.getElementById('od-decision');
    if(el)el.innerHTML='<span class="vx-meta">Moteur de gestion indisponible : '+esc(e.message)+'</span>';}
  try{
    if(window.VXCharts&&VXCharts.payoffCard&&t.strike&&unit){
      VXCharts.payoffCard('od-payoff',{title:'Payoff',spot:(t.underSpot!=null)?t.underSpot:t.strike,
        strike:t.strike,premium:unit,right:t.type==='PUT'?'P':'C',height:170,
        source:(t.underSpot!=null)?'position déclarée (centre = cours réel)':'position déclarée (centre = strike sans cote)',
        timestamp:Date.now(),mode:(t.underSpot!=null)?'delayed':'fallback'});
    }
  }catch(e){}
  try{
    const el=document.getElementById('od-scenarios');
    if(el)el.innerHTML='<div class="vx-meta">Simulation spot×temps×IV disponible depuis le desk options '
      +'(<a href="/opportunities?view=options&sym='+t.sym+'">ouvrir</a>) — elle exige IV et spot frais ; '
      +'sans IBKR, rien n\'est estimé ici.</div>';
  }catch(e){}
}

/* ═══ RISQUE PRIORISÉ (LOT F — moteur risk_engine, positions réelles §26) ═══ */
async function renderRisk(){
  const pos=E().positions();
  if(!pos.length){$('pf-body').innerHTML=VX.states.empty('Aucune position déclarée — le risque se calcule sur les positions réelles, jamais sur les candidats du scanner.');return;}
  const rich=enrich(pos,await quotesFor(pos));
  renderSummary(rich);
  let scan=null;try{scan=await VX.fetch('/scan',{ttl:300000});}catch(e){}
  const sectorOf=(sym)=>{const d=scan&&scan.detail&&scan.detail[sym];return(d&&d.sector)||'';};
  const payload={positions:rich.filter(t=>t.type==='STK').map(t=>{const per=t.qty?t.cost/t.qty:t.cost;
      return {symbol:t.sym,quantity:t.qty,avg_cost:per,last_price:(t.mark!=null?t.mark:per),sector:sectorOf(t.sym)};}),
    cash:E().capital()||0,simulated:false};
  try{
    const r=await fetch('/api/portfolio/team',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const d=await r.json();
    const risk=d.risk||{},guard=d.guard||{},stress=(d.stress||{}).scenarios||{};

    /* LOT F — hiérarchie des risques : critiques (garde-fous bloquants + invalidations)
       > importants (concentration/bêta/pire stress) > secondaires (secteurs/greeks).
       « Manquant/insuffisant » n'est jamais présenté comme zéro. */
    const broken=rich.filter(t=>thesisState(t).key==='cassee');
    const critiques=[];
    (guard.blocking_rules||[]).forEach(x=>critiques.push(esc(x)));
    if(broken.length)critiques.push(broken.length+' position(s) sous invalidation : '+broken.map(t=>t.sym).join(' · '));
    const importants=[];
    if(risk.hhi!=null&&risk.hhi>=0.66)importants.push('Concentration très élevée (HHI '+risk.hhi+')');
    const _wsv=Object.values(stress).map(v=>v&&v.impact_pct).filter(x=>typeof x==='number');
    const _worst=_wsv.length?Math.min.apply(null,_wsv):null;
    if(_worst!=null&&_worst<=-15)importants.push('Pire scénario de stress : '+VX.fmt.pct(_worst,1));
    if(risk.beta!=null&&risk.beta>=1.3)importants.push('Bêta pondéré élevé ('+risk.beta+')');
    const prioBlock=`<section class="vx-card vx-mb3" aria-label="Risques priorisés">
      <div class="vx-card-header"><span class="vx-card-title">Risques priorisés</span>
        <span class="vx-meta vx-right">critiques → importants → secondaires</span></div>
      <div class="vx-kpi-label">Critiques</div>
      ${critiques.length?critiques.map(x=>`<div class="vx-insight" data-tone="risk">${x}</div>`).join(''):'<div class="vx-meta">Aucun risque critique détecté.</div>'}
      <div class="vx-kpi-label vx-mt3">Importants</div>
      ${importants.length?importants.map(x=>`<div class="vx-meta">⚠ ${esc(x)}</div>`).join(''):'<div class="vx-meta">Aucun risque important au-dessus des repères.</div>'}
      <div class="vx-kpi-label vx-mt3">Secondaires</div>
      <div class="vx-meta">Exposition sectorielle et Greeks détaillés ci-dessous. Greeks agrégés : ${risk.options_exposure&&risk.options_exposure.delta!=null?'disponibles':'non estimés sans IBKR (jamais inventés)'}.</div>
    </section>`;

    $('pf-body').innerHTML=prioBlock+`<div class="vx-grid vx-mb3">
      <section class="vx-card vx-col-4" aria-label="Concentration du risque">
        <div class="vx-card-header"><span class="vx-card-title">Concentration du risque</span>
          <span class="vx-chart-question">Le capital est-il trop concentré ?</span></div>
        <div id="pf-risk-gauge"><div class="vx-skeleton" style="height:118px"></div></div>
        <div class="vx-card-footer"><span class="vx-meta">Indice HHI (0 = dispersé · 100 = tout sur un titre) — donnée réelle du moteur.</span></div>
      </section>
      <section class="vx-card vx-col-8" aria-label="Synthèse du risque">
        <div class="vx-card-header"><span class="vx-card-title">Synthèse du risque</span></div>
        <div class="vx-grid" id="pf-risk-kpis"></div>
      </section>
    </div>
    <div class="vx-grid">
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Garde-fous</span></div>
        ${kv('Nouveau titre',guard.new_stock_allowed?'autorisé':'BLOQUÉ',guard.new_stock_allowed?'vx-pos':'vx-neg')}
        ${kv('Nouvelle option',guard.new_option_allowed?'autorisée':'BLOQUÉE',guard.new_option_allowed?'vx-pos':'vx-neg')}
        ${(guard.mandatory_reviews||[]).map(rr=>`<div class="vx-meta">⚠ ${esc(rr)}</div>`).join('')}</div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Concentration</span></div>
        ${kv('Drawdown portefeuille',risk.drawdown_pct!==null&&risk.drawdown_pct!==undefined?risk.drawdown_pct+' %':'n/d (pic non renseigné)')}
        ${kv('HHI',risk.hhi)}${kv('Bêta pondéré',risk.beta)}
        <div id="pf-sector-donut" class="vx-mt2"><span class="vx-meta">Exposition sectorielle…</span></div></div>
      <div class="vx-card vx-col-4"><div class="vx-card-header"><span class="vx-card-title">Greeks agrégés</span></div>
        ${kv('Delta global',risk.options_exposure&&risk.options_exposure.delta)}
        ${kv('Gamma global',risk.options_exposure&&risk.options_exposure.gamma)}
        ${kv('Theta global',risk.options_exposure&&risk.options_exposure.theta)}
        ${kv('Vega global',risk.options_exposure&&risk.options_exposure.vega)}
        <div class="vx-meta vx-mt2">Greeks broker requis — sans IBKR, non estimés (aucune invention).</div></div>
      <section class="vx-card vx-col-12"><div class="vx-card-header"><span class="vx-card-title">Stress tests (§26)</span>
        <span class="vx-chart-question">Combien perd le portefeuille dans chaque scénario ?</span></div>
        ${(function(){const arr=Object.entries(stress).filter(([,v])=>v.impact_pct!=null);
          if(!arr.length)return '';
          const maxAbs=Math.max.apply(null,[1].concat(arr.map(([,v])=>Math.abs(v.impact_pct))));
          return '<div class="vx-mb3">'+arr.map(([k,v])=>{const neg=v.impact_pct<0;
            const w=Math.min(100,Math.abs(v.impact_pct)/maxAbs*100);
            return '<div style="display:flex;align-items:center;gap:8px;margin:3px 0" role="img" aria-label="'+esc(k)+' '+VX.fmt.pct(v.impact_pct,1)+'">'
              +'<span style="width:150px;font-size:11px;color:var(--vx-text-secondary,#b7b2aa);text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+esc(k)+'</span>'
              +'<span style="flex:1;height:13px;background:var(--vx-surface-3,#17191c);border-radius:4px;overflow:hidden"><span style="display:block;height:100%;width:'+w.toFixed(0)+'%;background:'+(neg?'var(--vx-negative,#dc6255)':'var(--vx-positive,#39b878)')+';border-radius:4px"></span></span>'
              +'<span style="width:58px;text-align:right;font-size:11px;font-variant-numeric:tabular-nums" class="'+(neg?'vx-neg':'vx-pos')+'">'+VX.fmt.pct(v.impact_pct,1)+'</span></div>';
          }).join('')+'</div>';})()}
        <div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Scénario</th>
        <th class="vx-num">Impact estimé</th><th>Note</th></tr></thead><tbody>
        ${Object.entries(stress).map(([k,v])=>`<tr><td>${k}</td>
          <td class="vx-num ${v.impact_pct<0?'vx-neg':''}">${v.impact_pct!==null&&v.impact_pct!==undefined?VX.fmt.pct(v.impact_pct,1):'non estimé'}</td>
          <td class="vx-meta">${esc(v.note||'')}</td></tr>`).join('')}</tbody></table></div>
        <div class="vx-card-footer">${VX.updateIndicator(Date.now(),'risk_engine (positions réelles)','live')}
        ${(risk.warnings||[]).length?'· '+risk.warnings.length+' avertissement(s)':''}</div></section></div>`;
    try{
      var _hhi=(risk.hhi!=null)?Math.round(risk.hhi*100):null;
      if(window.VXCharts&&VXCharts.gauge)VXCharts.gauge('pf-risk-gauge',{
        value:_hhi,min:0,max:100,unit:'',label:'Concentration',
        reading:_hhi==null?'donnée indisponible':(_hhi>=66?'très concentré':_hhi>=33?'concentration modérée':'bien dispersé'),
        bands:[{to:33,color:VXCharts.colors.positive},{to:66,color:VXCharts.colors.warning},{to:100,color:VXCharts.colors.negative}]});
      var _rk=function(l,v,dd,cls){return '<div class="vx-card vx-card--compact vx-kpi" style="grid-column:span 3"><span class="vx-kpi-label">'+l+'</span><span class="vx-kpi-value" style="font-size:22px">'+(v==null?'—':v)+'</span>'+(dd?'<span class="vx-kpi-delta '+(cls||'vx-muted')+'">'+dd+'</span>':'')+'</div>';};
      var _rh=$('pf-risk-kpis');
      if(_rh)_rh.innerHTML=
        _rk('HHI',risk.hhi!=null?risk.hhi:'—','indice',(_hhi!=null&&_hhi>=66)?'vx-neg':'')
        +_rk('Bêta',risk.beta!=null?risk.beta:'—','pondéré')
        +_rk('Drawdown',(risk.drawdown_pct!=null)?(risk.drawdown_pct+' %'):'n/d','pic')
        +_rk('Pire scénario',_worst!=null?VX.fmt.pct(_worst,1):'—','stress',(_worst!=null&&_worst<0)?'vx-neg':'');
      var _sw=risk.sector_weights||{};
      var _sh=document.getElementById('pf-sector-donut');
      if(_sh){
        var _se=Object.keys(_sw).map(function(k){return [k,+_sw[k]];}).filter(function(e){return isFinite(e[1])&&e[1]>0;}).sort(function(a,b){return b[1]-a[1];});
        if(!_se.length){_sh.innerHTML='<span class="vx-meta">Exposition sectorielle indisponible (aucune position action).</span>';}
        else if(window.VXCharts&&VXCharts.donut){
          var _lab,_val;
          if(_se.length<=5){_lab=_se.map(function(e){return e[0];});_val=_se.map(function(e){return e[1];});}
          else{var _t=_se.slice(0,4);_lab=_t.map(function(e){return e[0];});_val=_t.map(function(e){return e[1];});
            var _rest=_se.slice(4).reduce(function(s,e){return s+e[1];},0);_lab.push('Autres');_val.push(+_rest.toFixed(2));}
          _sh.innerHTML='<div class="vx-kpi-label vx-mb1">Exposition sectorielle</div><div style="height:150px"><canvas></canvas></div>';
          VXCharts.donut(_sh.querySelector('canvas'),_lab,_val,{});
        } else {_sh.innerHTML=_se.map(function(e){return kv(e[0],e[1]+' %');}).join('');}
      }
    }catch(e){}
  }catch(e){$('pf-body').innerHTML=VX.states.error('Moteur de risque injoignable : '+e.message);}
}

/* ═══ WATCHLIST (+ suivis + favoris §18) ═══ */
async function renderWatchlist(){
  const wl=E().watchlist(),follows=E().follows(),favs=E().favorites();
  const statuses=['idee','a_etudier','en_attente','proche','declenchee','invalidee','archivee'];
  const labels={idee:'Idée',a_etudier:'À étudier',en_attente:'En attente',proche:'Proche',
    declenchee:'Déclenchée',invalidee:'Invalidée',archivee:'Archivée'};
  $('pf-body').innerHTML=`
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">Watchlist (surveillance active)</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('','watchlist')">+ Ajouter</button></span></div>
      ${wl.length?`<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Titre</th><th>Priorité</th><th>Thèse</th><th>Zone</th><th>Catalyseur</th>
        <th>Statut</th><th>Ajouté</th><th></th></tr></thead><tbody>
        ${wl.map(w=>`<tr>
          <td data-label="Titre"><span class="vx-ticker">${w.sym}</span> ${E().badges(w.sym)}</td>
          <td data-label="Priorité"><span class="vx-badge">${esc(w.priority||'normale')}</span></td>
          <td data-label="Thèse" class="vx-truncate" style="max-width:200px">${esc(w.thesis||'—')}</td>
          <td data-label="Zone" class="vx-mono">${esc(w.zone||'—')}</td>
          <td data-label="Catalyseur">${esc(w.catalyst||'—')}</td>
          <td data-label="Statut"><select class="vx-select" data-wl-status="${w.sym}" style="width:auto;padding:3px 24px 3px 8px">
            ${statuses.map(s=>`<option value="${s}" ${w.status===s?'selected':''}>${labels[s]}</option>`).join('')}</select></td>
          <td data-label="Ajouté" class="vx-mono vx-meta">${w.added||'—'}</td>
          <td><div class="vx-row-actions">
            <button class="vx-btn vx-btn-sm vx-btn-ghost" data-open-analysis="${w.sym}">Analyse</button>
            <button class="vx-btn vx-btn-sm vx-btn-danger" data-wl-del="${w.sym}">Retirer</button>
          </div></td></tr>`).join('')}</tbody></table></div>`
        :VX.states.empty('Watchlist vide — ajoutez les titres à surveiller activement avec thèse et zone.',
          '<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\'\',\'watchlist\')">+ Ajouter</button>')}
    </section>
    <section class="vx-card vx-mb3"><div class="vx-card-header"><span class="vx-card-title">Suivis actifs (setups)</span></div>
      ${follows.length?follows.map(r=>`<div class="vx-flex" style="padding:7px 0;border-bottom:1px dashed var(--vx-border-soft)">
        <button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${r.sym}">${r.sym}</button>
        <span class="vx-badge vx-badge-entity" data-kind="follow">${r.kind}</span>
        <span class="vx-grow vx-mono vx-meta">entrée ${VX.fmt.nd(r.entry_spot)} · stop ${VX.fmt.nd(r.stop)} · objectif ${VX.fmt.nd(r.tgt)}</span>
        <span class="vx-meta">depuis ${r.followed||'—'}</span>
        <button class="vx-btn vx-btn-sm vx-btn-danger" data-unfollow="${r.sym}">Retirer</button></div>`).join('')
        :VX.states.empty('Aucun suivi actif — créez un suivi depuis une analyse (entrée/stop/objectif).')}
    </section>
    <section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Favoris (accès rapide)</span></div>
      <div class="vx-flex vx-wrap">${favs.length?favs.map(s=>
        `<button class="vx-btn vx-ticker" data-open-analysis="${s}">★ ${s}</button>`).join('')
        :'<span class="vx-muted">Aucun favori — l’étoile est disponible sur chaque titre.</span>'}</div>
    </section>`;
  document.querySelectorAll('[data-wl-del]').forEach(b=>b.addEventListener('click',()=>{E().removeFromWatchlist(b.dataset.wlDel);renderWatchlist();}));
  document.querySelectorAll('[data-unfollow]').forEach(b=>b.addEventListener('click',()=>{E().unfollow(b.dataset.unfollow);renderWatchlist();}));
  document.querySelectorAll('[data-wl-status]').forEach(sel=>sel.addEventListener('change',()=>{
    E().addToWatchlist(sel.dataset.wlStatus,Object.assign({},E().watchlist().find(w=>w.sym===sel.dataset.wlStatus),{status:sel.value}));}));
}

const RENDER={team:renderSynthese,positions:renderPositions,performance:renderPerformance,
  options:renderOptions,risk:renderRisk,watchlist:renderWatchlist};
function boot(){(RENDER[VIEW]||renderSynthese)().catch(e=>{$('pf-body').innerHTML=VX.states.error(e.message);});}
if(window.VXCharts&&window.Chart)boot();else window.addEventListener('load',boot,{once:true});
['vx:position-changed','vx:watchlist-changed','vx:follow-changed','vx:favorites-changed']
  .forEach(ev=>VX.bus.on(ev,(e)=>{if((e.detail||{}).source!=='sync')return boot();boot();}));
})();
</script>
"""


def render(view: str = 'team') -> str:
    view = view if view in dict(_VIEWS) else 'team'
    content = (_CONTENT.replace('%%TABS%%', _tabs(view))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:120px"></div>'))
    label = dict(_VIEWS)[view]
    return render_shell(title=f'Portefeuille · {label}', active='portfolio',
                        space_label='Portefeuille', sub_label=label,
                        content=content, page_js=_JS.replace('%%VIEW%%', json.dumps(view)),
                        page_label=f'Portefeuille {label}')
