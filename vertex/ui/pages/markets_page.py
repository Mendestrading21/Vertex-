"""vertex.ui.pages.markets_page — l'espace Marchés (§7.2, D-005).

Question : « Dans quel environnement de marché suis-je aujourd'hui ? »
Sous-vues (param ?view=) : overview · sectors · breadth · volatility · macro.

Marchés redevient un espace EXPLICITE (9e de la navigation V4) en RÉUTILISANT
les vues et données existantes — AUCUN nouveau moteur, aucune nouvelle donnée.
Le module Python assemble le squelette HTML + le script client ; les données
viennent des APIs déjà servies : /scan, /api/market/summary, /api/market/regime,
/api/command. Lecture seule ; états vides honnêtes ; aucun chiffre inventé.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

_VIEWS = (
    ('overview', 'Vue d’ensemble'),
    ('sectors', 'Secteurs'),
    ('breadth', 'Participation'),
    ('volatility', 'Volatilité'),
    ('macro', 'Macro'),
)


def _tabs(view: str) -> str:
    items = []
    for vid, label in _VIEWS:
        sel = 'true' if vid == view else 'false'
        items.append(f'<a class="vx-tab" role="tab" href="?view={vid}" '
                     f'aria-selected="{sel}" data-view-tab="{vid}">{label}</a>')
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Marchés">'
            + ''.join(items) + '</nav>')


# Cartes de la page. `data-mkv` liste les sous-vues où la section est montrée.
_CONTENT = """
<div class="vx-page-header">
  <div>
    <h1 class="vx-page-title">Marchés</h1>
    <p class="vx-page-sub">Le climat de marché, sans jargon — régime, indices, secteurs, participation, volatilité.</p>
  </div>
</div>
<div id="vx-demo-banner"></div>
%%TABS%%

<section class="vx-card vx-card--hero vx-mt3" id="mk-hero" data-mkv="overview sectors breadth volatility macro"
         aria-label="Climat de marché">
  <div class="vx-card-title">Climat de marché <span class="vx-actions vx-meta" id="mk-hero-meta"></span></div>
  <div id="mk-hero-body">%%LOADING%%</div>
</section>

<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" id="mk-indices" data-mkv="overview breadth macro" aria-label="Indices">
    <div class="vx-card-title">Indices &amp; cross-asset</div>
    <div id="mk-indices-body">%%LOADING%%</div>
  </section>
</div>

<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-8" id="mk-chart" data-mkv="overview macro volatility" aria-label="Référence marché"></section>
  <section class="vx-card vx-col-4" id="mk-vol" data-mkv="overview volatility macro" aria-label="Volatilité">
    <div class="vx-card-title">Volatilité &amp; régime</div>
    <div id="mk-vol-body">%%LOADING%%</div>
  </section>
</div>

<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-7" id="mk-sectors" data-mkv="overview sectors" aria-label="Secteurs">
    <div class="vx-card-title">Rotation sectorielle</div>
    <div id="mk-sectors-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-5" id="mk-breadth" data-mkv="overview breadth" aria-label="Participation">
    <div class="vx-card-title">Participation (breadth)</div>
    <div id="mk-breadth-body">%%LOADING%%</div>
  </section>
</div>
"""

_JS = r"""
<script>
(function(){
  var VIEW='%%VIEW%%';
  function $(id){return document.getElementById(id);}
  function esc(s){return (window.VX&&VX.esc)?VX.esc(s):String(s==null?'':s);}
  function num(v,d){return (window.VX&&VX.fmt)?VX.fmt.num(v,d==null?2:d):(v==null?'—':v);}
  function pct(v,d){return (window.VX&&VX.fmt)?VX.fmt.pct(v,d==null?2:d):(v==null?'—':v+' %');}

  /* N'affiche que les sections pertinentes pour la sous-vue courante. */
  function applyView(){
    document.querySelectorAll('[data-mkv]').forEach(function(el){
      var views=(el.getAttribute('data-mkv')||'').split(/\s+/);
      el.style.display=(views.indexOf(VIEW)>=0)?'':'none';
    });
  }

  function tone(v){return v==null?'':(v>0?'pos':(v<0?'neg':''));}
  function sign(v){return v>0?'+':'';}
  /* /api/market/summary sert breadth soit en scalaire, soit en objet
     {above50, above200, adv, dec…} — on en tire un % de participation honnête. */
  function breadthPct(b){
    if(b==null) return null;
    if(typeof b==='number') return b;
    if(b.above50!=null) return b.above50;
    if(b.above200!=null) return b.above200;
    if(b.adv!=null&&b.dec!=null&&(b.adv+b.dec)>0) return Math.round(b.adv/(b.adv+b.dec)*100);
    return null;
  }

  function paintHero(sum,reg){
    var el=$('mk-hero-body'); if(!el) return;
    var s=sum||{}, r=reg||{};
    if(s.score==null && !s.regime && !r.regime){
      el.innerHTML=VX.states.empty('Contexte de marché indisponible — lancer un scan depuis Système.',
        '<a class="vx-btn vx-btn-sm" href="/system?view=data">Système / Données</a>'); return;
    }
    var verdict=s.verdict||s.market_verdict||r.regime||'—';
    var vtone=({FAVORABLE:'pos','RISK-ON':'pos',DANGEREUX:'neg','RISK-OFF':'neg',NEUTRE:''} )[String(verdict).toUpperCase()]||'';
    var regime=s.regime||r.regime||'n/d';
    var regMap={TREND:'tendance',NEUTRAL:'neutre',CHOP:'sans direction',DOWN:'baissier'};
    var cards=[
      ['Score de climat', s.score!=null?num(s.score,0)+' / 100':'—', 'santé agrégée du marché', tone((s.score||0)-50)],
      ['Régime', regMap[regime]||regime, s.roro!=null?('RoRo '+num(s.roro,0)):'orientation de fond', ''],
      ['VIX', s.vix!=null?num(s.vix,2):'—', (s.vix_band?esc(s.vix_band):'volatilité implicite')+(s.vix_chg!=null?' · '+sign(s.vix_chg)+num(s.vix_chg,2):''), tone(s.vix_chg==null?null:-s.vix_chg)],
      ['Participation', (function(){var bp=breadthPct(s.breadth);return bp!=null?num(bp,0)+' %':'—';})(), 'titres au-dessus de leur MM', tone((function(){var bp=breadthPct(s.breadth);return bp==null?null:bp-50;})())]
    ];
    var meta=$('mk-hero-meta');
    if(meta) meta.innerHTML='<span class="vx-badge vx-badge-decision" data-decision="'+esc(verdict)+'">'+esc(verdict)+'</span>';
    el.innerHTML='<div class="vx-grid-4 vx-mt2">'+cards.map(function(c){
      return '<div class="vx-stat" data-tone="'+c[3]+'"><div class="vx-stat-k">'+esc(c[0])+'</div>'
        +'<div class="vx-stat-v">'+esc(c[1])+'</div>'
        +'<div class="vx-stat-sub vx-dim">'+esc(c[2])+'</div></div>';
    }).join('')+'</div>'
    +(VX.updateIndicator?('<div class="vx-mt2">'+VX.updateIndicator(s.scan_age?Date.now()-s.scan_age*1000:null, s.source||'scan', 'delayed')+'</div>'):'');
  }

  function paintIndices(scan,sum){
    var el=$('mk-indices-body'); if(!el) return;
    var idx=(scan&&scan.indices)||(sum&&sum.indices)||[];
    if(!idx.length){ el.innerHTML=VX.states.empty('Indices indisponibles.'); return; }
    el.innerHTML='<div class="vx-grid-4 vx-mt2">'+idx.slice(0,12).map(function(i){
      var ch=i.change;
      return '<div class="vx-stat" data-tone="'+tone(ch)+'"><div class="vx-stat-k">'+esc(i.name||i.symbol||'—')+'</div>'
        +'<div class="vx-stat-v vx-mono">'+(i.price!=null?num(i.price, i.price>=1000?0:2):'—')+'</div>'
        +'<div class="vx-stat-sub vx-mono '+(ch>0?'vx-pos':ch<0?'vx-neg':'vx-dim')+'">'+(ch!=null?sign(ch)+num(ch,2)+' %':'n/d')+'</div></div>';
    }).join('')+'</div>';
  }

  function paintChart(scan){
    var host=$('mk-chart'); if(!host||!window.VXCharts) return;
    scan=scan||{};
    var det=scan.detail||{};
    function okSeries(k){return det[k]&&det[k].series&&Array.isArray(det[k].series.close)&&det[k].series.close.length>10;}
    var hasSpy=okSeries('SPY');
    var spx=((scan.indices)||[]).find(function(i){return i&&i.name==='S&P 500';});
    var hasIdx=!hasSpy&&spx&&Array.isArray(spx.series)&&spx.series.length>10;
    var key=hasSpy?'SPY':(hasIdx?'S&P 500':Object.keys(det).find(okSeries));
    if(!key){ host.innerHTML=VX.states.empty('Série marché indisponible — lancer un scan depuis Système.',
      '<a class="vx-btn vx-btn-sm" href="/system?view=data">Système / Données</a>'); return; }
    var S=hasIdx?{close:spx.series,dates:spx.dates,ema20:spx.ema20,sma50:spx.sma50,sma200:spx.sma200}:(det[key].series||{});
    var cc=(VXCharts.colors)||{};
    var closes=S.close||[];
    var dates=S.dates;
    var labels=(dates&&dates.length===closes.length)?dates.map(function(d){var x=String(d);return x.length>7?x.slice(5):x;}):closes.map(function(_,i){return i-closes.length;});
    var m=Object.assign({},scan.market||{},scan.market_ctx||{});
    function mm(data,label,color,dash){return (Array.isArray(data)&&data.some(function(x){return x!=null;}))?[{label:label,data:data,borderColor:color,borderWidth:1.2,borderDash:dash,pointRadius:0,tension:.2,fill:false}]:[];}
    VXCharts.card('mk-chart',{
      title:(hasSpy||hasIdx)?'S&P 500 — tendance & moyennes':'Marché — référence · '+key,
      timeframe:closes.length+' séances',
      question:'La tendance de fond reste-t-elle exploitable ?',
      conclusion:(spx&&spx.price!=null?('S&P 500 '+VX.fmt.price(spx.price)+' ('+sign(spx.change)+num(spx.change,2)+' %) · '):'')
        +(({TREND:'tendance intacte',NEUTRAL:'marché neutre',CHOP:'sans direction',DOWN:'tendance baissière'})[m.spy_regime]||('régime '+(m.spy_regime||'n/d'))),
      height:300, source:scan.source||'scan', timestamp:scan.scan_ts||scan.updated, mode:'delayed',
      legend:[{label:hasSpy?'SPY':key,color:cc.brand}]
        .concat((S.ema20&&S.ema20.some(function(x){return x!=null;}))?[{label:'MM20',color:cc.amber}]:[])
        .concat((S.sma50&&S.sma50.some(function(x){return x!=null;}))?[{label:'MM50',color:cc.beige}]:[])
        .concat((S.sma200&&S.sma200.some(function(x){return x!=null;}))?[{label:'MM200',color:cc.neutral}]:[]),
      explain:{shows:'Les clôtures de la référence marché et ses moyennes mobiles 20/50/200 (calculées par le scan).',
        why:'L’environnement porteur ou non module la prise de risque : le régime pilote seuils et tailles.',
        confirm:'Clôtures au-dessus de MM50/MM200 ascendantes avec participation > 55 %.',
        invalidate:'Cassure des moyennes avec expansion de la volatilité.'},
      render:function(cv){return VXCharts.mount(cv,{type:'line',
        data:{labels:labels,datasets:[
          {label:key,data:closes,borderColor:cc.brand,borderWidth:1.9,pointRadius:0,tension:.22,fill:true,
           backgroundColor:function(ctx){var g=ctx.chart.ctx.createLinearGradient(0,0,0,ctx.chart.height||300);
             g.addColorStop(0,(cc.brand||'#9a5cff')+'33');g.addColorStop(1,(cc.brand||'#9a5cff')+'00');return g;}},
          ].concat(mm(S.ema20,'MM20',cc.amber,[]),mm(S.sma50,'MM50',cc.beige,[5,3]),mm(S.sma200,'MM200',cc.neutral,[2,3]))},
        options:{scales:VXCharts.axes({yFmt:function(v){return VX.fmt.price(v);}}),interaction:{mode:'index',intersect:false},plugins:{legend:{display:false}}}});
      }});
  }

  function paintVol(sum,reg){
    var el=$('mk-vol-body'); if(!el) return;
    var s=sum||{}, r=reg||{};
    if(s.vix==null && !r.regime){ el.innerHTML=VX.states.empty('Volatilité indisponible.'); return; }
    var rows=[
      ['VIX', s.vix!=null?num(s.vix,2):'—', s.vix_band||''],
      ['Variation VIX', s.vix_chg!=null?sign(s.vix_chg)+num(s.vix_chg,2):'—', s.vix_chg!=null?(s.vix_chg>0?'tension':'détente'):''],
      ['Régime SPY', ({TREND:'tendance',NEUTRAL:'neutre',CHOP:'sans direction',DOWN:'baissier'})[s.regime]||s.regime||r.regime||'n/d', ''],
      ['Risk-on / off', s.roro!=null?num(s.roro,0):'—', s.roro_gap!=null?('écart '+num(s.roro_gap,0)):'']
    ];
    el.innerHTML='<div class="vx-mt2">'+rows.map(function(x){
      return '<div class="vx-kv"><span class="vx-kv-k">'+esc(x[0])+'</span>'
        +'<span class="vx-kv-v vx-mono">'+esc(x[1])+(x[2]?' <span class="vx-dim">'+esc(x[2])+'</span>':'')+'</span></div>';
    }).join('')+'</div>';
  }

  function paintSectors(scan){
    var el=$('mk-sectors-body'); if(!el) return;
    var secs=(scan&&scan.sectors)||[];
    if(!secs.length){ el.innerHTML=VX.states.empty('Secteurs indisponibles — lancer un scan.'); return; }
    var vals=secs.map(function(s){return s.perf!=null?s.perf:(s.change!=null?s.change:null);}).filter(function(v){return v!=null;});
    var mx=vals.length?Math.max.apply(null,vals.map(Math.abs)):1;
    el.innerHTML='<div class="vx-wbars vx-mt2">'+secs.slice(0,12).map(function(s){
      var v=s.perf!=null?s.perf:(s.change!=null?s.change:null);
      var w=v==null?0:Math.max(4,Math.min(100,Math.abs(v)/(mx||1)*100));
      return '<div class="vx-wbar"><span class="wb-name">'+esc(s.name||s.sector||'—')+'</span>'
        +'<span class="wb-track"><i style="width:'+w.toFixed(0)+'%" data-tone="'+tone(v)+'"></i></span>'
        +'<span class="wb-val vx-mono '+(v>0?'vx-pos':v<0?'vx-neg':'vx-dim')+'">'+(v!=null?sign(v)+num(v,2)+' %':'n/d')+'</span></div>';
    }).join('')+'</div>';
  }

  function paintBreadth(sum,scan){
    var el=$('mk-breadth-body'); if(!el) return;
    var s=sum||{};
    var b=breadthPct(s.breadth);
    var scanned=s.scanned||(scan&&scan.scanned_n), uni=s.universe;
    if(b==null){ el.innerHTML=VX.states.empty('Participation indisponible.'); return; }
    var t=tone(b-50);
    el.innerHTML='<div class="vx-mt2" style="text-align:center">'
      +'<div class="vx-stat-v" style="font-size:34px" data-tone="'+t+'">'+num(b,0)+' %</div>'
      +'<div class="vx-dim">titres au-dessus de leur moyenne mobile</div>'
      +'<div class="vx-meter vx-mt2"><i style="width:'+Math.max(0,Math.min(100,b)).toFixed(0)+'%;background:var(--vx-'+(b>=55?'positive':b>=45?'warning':'negative')+')"></i></div>'
      +'<div class="vx-meta vx-mt2">'+(scanned!=null?esc(scanned)+(uni?' / '+esc(uni):'')+' titres scannés':'')+'</div>'
      +'<div class="vx-meta vx-mt1 vx-dim">> 55 % = marché large · < 45 % = participation étroite</div></div>';
  }

  async function boot(){
    var scan={},sum={},reg={},cmd={};
    try{scan=await VX.fetch('/scan',{ttl:120000})||{};}catch(e){}
    try{sum=await VX.fetch('/api/market/summary',{ttl:60000})||{};}catch(e){}
    try{reg=await VX.fetch('/api/market/regime',{ttl:120000})||{};}catch(e){}
    applyView();
    if($('vx-demo-banner')&&scan&&(scan.source==='demo'||(sum&&sum.source==='demo')))
      $('vx-demo-banner').innerHTML='<div class="vx-demo-banner"><span class="vx-badge-demo">Démo</span> Données synthétiques clairement identifiées — jamais présentées comme réelles.</div>';
    try{paintHero(sum,reg);}catch(e){}
    try{paintIndices(scan,sum);}catch(e){}
    try{paintChart(scan);}catch(e){}
    try{paintVol(sum,reg);}catch(e){}
    try{paintSectors(scan);}catch(e){}
    try{paintBreadth(sum,scan);}catch(e){}
  }
  function whenReady(fn){ if(window.VX&&window.VX.fetch&&window.VXCharts){fn();} else setTimeout(function(){whenReady(fn);},80); }
  whenReady(boot);
  if(window.VX&&VX.bus)VX.bus.on('vx:data-refreshed',function(){whenReady(boot);});
})();
</script>
"""


def render(view: str = 'overview', params: dict | None = None) -> str:
    """Assemble l'espace Marchés pour la sous-vue demandée (URL = état)."""
    if view not in dict(_VIEWS):
        view = 'overview'
    label = dict(_VIEWS)[view]
    content = (_CONTENT.replace('%%TABS%%', _tabs(view))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:60px"></div>'))
    page_js = _JS.replace('%%VIEW%%', view)
    return render_shell(title='Marchés', active='markets',
                        space_label='Marchés', sub_label=label,
                        content=content, page_js=page_js, page_label='Marchés')
