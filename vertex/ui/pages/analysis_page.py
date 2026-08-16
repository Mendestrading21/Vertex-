"""vertex.ui.pages.analysis_page — la fiche canonique (§26).

Question : « Cette entreprise et cette opportunité méritent-elles du capital
maintenant ? ». Ordre strict : résumé décisionnel → thèse → graphique →
fondamental → catalyseurs → technique → sentiment → anomalies → scénarios →
plan → options → compatibilité portefeuille → historique.
Tout ticker, partout dans l'app, ouvre CETTE fiche.
"""
from __future__ import annotations


from vertex.ui.shell import icon, json_for_script, render_shell


def render_index(view: str = '') -> str:
    dims = ''.join(
        f'<div class="an-dim"><span class="an-dim-n">{n}</span>'
        f'<span class="an-dim-l">{lab}</span></div>'
        for n, lab in [
            ('1', 'Décision — verdict, confiance et prochaine action'),
            ('2', 'Prix — tendance, invalidation et objectifs'),
            ('3', 'Scénarios — perte, cas central et potentiel'),
            ('4', 'Preuves — fondamentaux, catalyseurs et risques'),
        ])
    content = """
<div class="vx-page-header"><div><h1>Analyse</h1>
<div class="vx-sub">Une recherche, une décision lisible, les preuves ensuite.</div></div></div>
<style id="an-index-css">
.an-dim{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--vx-border-soft)}
.an-dim:last-child{border-bottom:none}
.an-dim-n{flex:0 0 26px;height:26px;display:grid;place-items:center;border-radius:8px;
 background:var(--vx-brand-soft);color:var(--vx-copper-light);font:700 12px/1 var(--vx-font-mono,monospace);
 border:1px solid var(--vx-border-accent)}
.an-dim-l{font-size:13px;color:var(--vx-text-secondary)}
.an-shortcut{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;
 border-bottom:1px dashed var(--vx-border-soft);font-size:13px;color:var(--vx-text-secondary)}
.an-shortcut:last-child{border-bottom:none}
.an-kbd{font:600 11px/1 var(--vx-font-mono,monospace);color:var(--vx-text-primary);
 background:var(--vx-graphite-800);border:1px solid var(--vx-border-default);border-radius:6px;padding:4px 7px}
</style>
<div class="vx-grid">
  <div class="vx-col-7">
    <div class="vx-card">
      <div class="vx-field"><label for="an-search">Ticker ou entreprise</label>
      <input class="vx-input" id="an-search" placeholder="ex. NVDA, Microsoft…" autocomplete="off"
        style="font-size:16px;padding:12px" /></div>
      <div id="an-results" class="vx-flex-col"></div>
      <div class="vx-help vx-mt2">Astuce : ⌘K / Ctrl+K depuis n’importe quelle page.</div>
    </div>
    <section class="vx-card vx-mt4" aria-label="Titres récents">
      <div class="vx-card-header"><span class="vx-card-title">Récents</span></div>
      <div class="vx-card-body vx-flex vx-wrap" id="an-recent"><span class="vx-skeleton" style="width:120px;height:26px"></span></div>
    </section>
    <section class="vx-card vx-mt4" aria-label="Favoris">
      <div class="vx-card-header"><span class="vx-card-title">Favoris</span>
        <span class="vx-dim" style="font-size:12px">titres mis en favori</span></div>
      <div class="vx-card-body vx-flex vx-wrap" id="an-favs"></div>
    </section>
  </div>
  <aside class="vx-col-5">
    <details class="vx-card an-disclosure" aria-label="Contenu d'une fiche">
      <summary><span>Comment lire une fiche</span><span class="vx-meta">4 repères</span></summary>
      <div class="vx-card-body" style="padding:var(--vx-s3)">""" + dims + """</div>
    </details>
    <section class="vx-card vx-mt4" aria-label="Raccourcis">
      <div class="vx-card-header"><span class="vx-card-title">Raccourcis</span></div>
      <div class="vx-card-body">
        <div class="an-shortcut"><span>Recherche</span><span class="an-kbd">⌘K</span></div>
        <div class="an-shortcut"><span>Opportunités</span><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities">Ouvrir →</a></div>
        <div class="an-shortcut"><span>Portefeuille</span><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">Ouvrir →</a></div>
      </div>
    </section>
  </aside>
</div>
"""
    js = r"""
<script>
(function(){
const $=(id)=>document.getElementById(id);
$('an-recent').innerHTML=VX.recentTickers.get().map(s=>
  `<button class="vx-btn vx-ticker" data-open-analysis="${s}">${s}</button>`).join('')
  ||'<span class="vx-muted">Aucun titre consulté récemment.</span>';
let favs=[];try{favs=JSON.parse(localStorage.getItem('myFavs')||'[]');}catch(e){favs=[];}
$('an-favs').innerHTML=(Array.isArray(favs)&&favs.length?favs:[]).map(s=>
  `<button class="vx-btn vx-ticker" data-open-analysis="${s}">${s}</button>`).join('')
  ||'<span class="vx-muted">Aucun favori — mets un titre en favori depuis sa fiche.</span>';
let names=null;
/* Échappement local (ce bloc est une IIFE distincte du esc() principal) : les libellés
   de /api/names sont rendus en innerHTML → on neutralise tout HTML/attribut. */
const escN=s=>String(s??'').replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));
$('an-search').addEventListener('input',async function(){
  const q=this.value.trim().toUpperCase();
  if(!q){$('an-results').innerHTML='';return}
  try{ if(!names){const d=await VX.fetch('/api/names',{ttl:600000});names=d.names||d;} }catch(e){names={};}
  const hits=Object.entries(names).filter(([s,n])=>s.startsWith(q)||String(n).toUpperCase().includes(q)).slice(0,8);
  $('an-results').innerHTML=(hits.length?hits:( /^[A-Z.]{1,6}$/.test(q)?[[q,'ouvrir la fiche']]:[]))
    .map(([s,n])=>`<button class="vx-btn" style="justify-content:flex-start" data-open-analysis="${escN(s)}">
      <span class="vx-ticker" style="min-width:64px">${escN(s)}</span><span class="vx-dim">${escN(n)}</span></button>`).join('')
    ||VX.states.empty('Aucun titre trouvé dans l’univers.');
});
$('an-search').focus();
})();
</script>
"""
    return render_shell(title='Analyse', active='analysis', space_label='Analyse',
                        content=content, page_js=js, page_label='Analyse')


_SECTIONS = """
<div id="an-stale"></div>
<!-- Identité compacte : le verdict canonique reste dans an-verdict, juste dessous. -->
<section class="vx-card vx-accent an-identity" id="an-hero" aria-labelledby="an-identity-title">
  <h2 class="vx-sr-only" id="an-identity-title">Identité et cours de %%SYM%%</h2>
  <div class="an-identity-main">
    <span class="vx-ticker" id="an-sym">%%SYM%%</span>
    <span class="vx-dim" id="an-name">—</span>
    <span class="vx-kpi-value" id="an-price">—</span>
    <span class="vx-mono" id="an-change">—</span>
    <span id="an-fresh"></span>
    <span id="an-badges"></span>
    <!-- Contrat interne du suivi, volontairement non visuel : le verdict affiché
         vit exclusivement dans la Carte-Verdict ci-dessous. -->
    <span class="vx-badge vx-badge-decision" id="an-decision" data-decision="" hidden>—</span>
  </div>
  <div class="an-identity-actions">
    <button class="vx-btn vx-btn-icon vx-btn-ghost" id="an-fav" aria-label="Ajouter aux favoris"
      aria-pressed="false" title="Favori">%%FAVICON%%</button>
    <button class="vx-btn vx-btn-sm vx-btn-soft" id="an-follow"
      onclick="VXEntities.followStock('%%SYM%%',{decision:(document.getElementById('an-decision')||{}).dataset&&document.getElementById('an-decision').dataset.decision});location.href='/tracking';"
      title="Suivre : mesure la performance hypothétique depuis maintenant">Suivre →</button>
    <button class="vx-btn vx-btn-sm" data-entity-menu="%%SYM%%">Actions %%CARET%%</button>
  </div>
</section>

<!-- Niveau 1 : une seule décision visible, puis ses trois scénarios dérivés. -->
<section class="an-decision-grid vx-mt4" aria-label="Décision et scénarios">
  <div id="an-verdict">%%LOADING%%</div>
  <div id="an-scenarios"></div>
</section>

<!-- Un événement futur ne doit jamais être ancré sur une bougie historique. -->
<div class="an-catalyst-strip vx-mt3" id="an-catalyst-strip" hidden></div>

<!-- Graphique principal immédiatement après la réponse. -->
<div id="an-chart" class="vx-mt4"></div>

<!-- Workspace : preuves principales + rail court (plan et risques seulement). -->
<div class="vx-grid vx-mt4" id="an-workspace">
<div class="vx-col-8 an-main-column">
  <section class="vx-card" id="an-thesis-card" aria-labelledby="an-thesis-title">
    <div class="vx-card-header"><h2 class="vx-card-title" id="an-thesis-title">Thèse</h2>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost"
        onclick="VXEntities.openAddModal('%%SYM%%','note')">Éditer</button></span></div>
    <div id="an-thesis" class="vx-dim">—</div>
  </section>

  <!-- Raisonnement du comité (intégré depuis Intelligence). -->
  <div id="an-committee" class="vx-mt4"></div>

  <!-- Dimensions dans l'ordre constitutionnel. -->
  <div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" id="an-fundamental"><div class="vx-card-header">
    <h3 class="vx-card-title">1 · Fondamental</h3></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-catalysts"><div class="vx-card-header">
    <h3 class="vx-card-title">2 · Catalyseurs</h3></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-technical"><div class="vx-card-header">
    <h3 class="vx-card-title">3 · Timing technique</h3></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-sentiment"><div class="vx-card-header">
    <h3 class="vx-card-title">4 · Sentiment & positionnement</h3></div><div data-body>%%LOADING%%</div></section>
  </div>

  <!-- Expertise à la demande : les moteurs continuent tous de charger, mais
       leurs sorties secondaires ne concurrencent plus le verdict canonique. -->
  <details class="vx-card an-disclosure vx-mt4" id="an-deep-analysis">
    <summary><span>Analyse approfondie</span><span class="vx-meta">scores, anomalies, évidence et signaux</span></summary>
    <div class="an-proof-grid">
      <section aria-labelledby="an-engine-title">
        <h3 id="an-engine-title">Diagnostic moteurs</h3>
        <p class="vx-meta">Score /40, règles bloquantes et audit. Ces diagnostics expliquent la décision sans la remplacer.</p>
        <div id="an-skyler">%%LOADING%%</div>
        <section id="an-rail-decision" aria-label="Sortie ExecutiveEngine">
          <h3 class="vx-sr-only">Sortie ExecutiveEngine</h3><div data-body>%%LOADING%%</div></section>
        <div class="vx-flex vx-wrap vx-mt3" id="an-scores" aria-label="Scores du moteur"></div>
        <p class="vx-meta an-scorecard-note">Marge risque : 100 = aucun garde-fou bloquant ; ce score ne mesure pas la volatilité.</p>
      </section>
      <section aria-labelledby="an-anomaly-title">
        <h3 id="an-anomaly-title">Scanner d’anomalies</h3>
        <p class="vx-meta">Spikes |z|≥2, régime de volatilité, séquences et extrêmes. Constat descriptif, pas une prévision.</p>
        <div id="an-anomaly">%%LOADING%%</div>
        <section id="an-anomalies" aria-label="Liste des anomalies"><div data-body>%%LOADING%%</div></section>
        <details class="an-disclosure an-disclosure--nested">
          <summary>Évidence historique</summary>
          <p class="vx-meta">Résultats observés après les spikes passés de la série disponible. In-sample, descriptif — pas un backtest.</p>
          <div id="an-evidence">%%LOADING%%</div>
        </details>
      </section>
      <section id="an-tv" aria-labelledby="an-tv-title">
        <h3 id="an-tv-title">Signaux TradingView</h3><div data-body>%%LOADING%%</div>
      </section>
    </div>
  </details>
</div>
<aside class="vx-col-4" id="an-rail">
<div class="an-rail-stack">
  <section class="vx-card" id="an-plan"><div class="vx-card-header">
    <h2 class="vx-card-title">Plan & niveaux clés</h2></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-card--compact" id="an-rail-risks"><div class="vx-card-header">
    <h2 class="vx-card-title">Risques identifiés</h2></div><div data-body>—</div></section>
</div>
</aside>
</div>

<!-- Outils séparés du rail et repliés : disponibles sans écraser la lecture. -->
<details class="vx-card an-disclosure vx-mt4" id="an-tools">
<summary><span>Outils d’analyse</span><span class="vx-meta">copilote et contrôles avant décision</span></summary>
<div class="an-tools-grid">
  <section class="vx-card" id="an-copilot" aria-labelledby="an-copilot-title">
    <div class="vx-card-header"><h2 class="vx-card-title" id="an-copilot-title">Copilote</h2></div>
    <p class="vx-chart-question">Question sur ce titre — réponse ancrée dans les chiffres disponibles.</p>
    <div data-body>
      <input id="an-cp-q" class="vx-input" aria-label="Question sur ce titre" placeholder="ex. Quel est le risque principal ici ?" maxlength="500" autocomplete="off" style="margin-bottom:.4rem" />
      <button class="vx-btn vx-btn-sm vx-btn-primary" id="an-cp-go">Demander</button>
      <div id="an-cp-out" class="vx-mt2" aria-live="polite"></div>
      <div class="vx-meta vx-mt1">Lecture seule — aucune exécution.</div>
    </div></section>
  <section class="vx-card" id="an-pretrade" aria-labelledby="an-pretrade-title">
    <div class="vx-card-header"><h2 class="vx-card-title" id="an-pretrade-title">Contrôles avant décision</h2></div>
    <p class="vx-chart-question">Sept contrôles descriptifs avant d’envisager ce titre — aucune exécution.</p>
    <div data-body>
      <input id="an-pt-amt" class="vx-input" type="number" min="1" step="any" aria-label="Montant envisag&eacute; en dollars" placeholder="Montant envisagé (ex. 2000)" style="margin-bottom:.4rem" />
      <button class="vx-btn vx-btn-sm vx-btn-primary" id="an-pt-go">Vérifier les garde-fous</button>
      <div id="an-pt-out" class="vx-mt2" aria-live="polite"></div>
    </div></section>
</div>
</details>

<!-- Options, compatibilité et historique : relais secondaires. -->
<section class="vx-card vx-mt4" id="an-options">
  <div class="vx-card-header"><h2 class="vx-card-title">Options associées</h2>
    <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost"
      href="/opportunities?view=options&sym=%%SYM%%">Ouvrir le desk options →</a></span></div>
  <div data-body>%%LOADING%%</div>
</section>
<div class="vx-grid vx-mt4">
  <section class="vx-card vx-col-6" id="an-portfolio-fit"><div class="vx-card-header">
    <h2 class="vx-card-title">Compatibilité portefeuille</h2></div><div data-body>%%LOADING%%</div></section>
  <section class="vx-card vx-col-6" id="an-history"><div class="vx-card-header">
    <h2 class="vx-card-title">Historique et suivis</h2></div><div data-body>%%LOADING%%</div></section>
</div>
"""

_JS = r"""
<!-- Moteur de chandeliers : ÉCHELLE DE REPLI, pas un chargement concurrent.
     Un SEUL moteur rend le graphique (cf. drawChart plus bas) :
       1. VXCharts.lwCandlestickCard  → CANONIQUE (TradingView Lightweight Charts,
          qualité pro : chandeliers nets, overlays MM + plan, zoom/pan natif).
       2. VXCharts.candlestickCard    → repli Canvas si la lib LWC échoue.
       3. VXCharts.priceCard          → repli ligne si les bougies sont invalides.
     Vérifié navigateur : #an-chart contient un unique .vx-lwc (LWC actif).
     Ne pas retirer les paliers 2-3 : ce sont les replis honnêtes, pas des doublons. -->
<script src="/static/vertex/js/charts/price-chart.js" defer></script>
<script src="/static/vertex/js/charts/candlestick-chart.js" defer></script>
<script src="/static/vertex/js/vendor/lightweight-charts.standalone.production.js" defer></script>
<script src="/static/vertex/js/charts/candlestick-lwc.js" defer></script>
<script src="/static/vertex/js/charts/annotations.js" defer></script>
<script src="/static/vertex/js/charts/anomaly-scan.js" defer></script>
<script>
(function(){
'use strict';
const SYM=%%SYM_JSON%%;
const $=(id)=>document.getElementById(id);
const E=()=>window.VXEntities;
function esc(s){return String(s??'').replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]));}
function body(id,html){const el=document.querySelector('#'+id+' [data-body]');if(el)el.innerHTML=html;}
function kv(k,v,cls){return `<div class="vx-kv"><span class="k">${k}</span><span class="v ${cls||''}">${VX.fmt.nd(v)}</span></div>`;}

VX.recentTickers.push(SYM);

/* Header : badges entités + favori */
function paintBadges(){
  $('an-badges').innerHTML=E()?E().badges(SYM):'';
  const fav=!!(E()&&E().isFavorite(SYM));
  $('an-fav').style.color=fav?'var(--vx-warning)':'var(--vx-text-muted)';
  $('an-fav').setAttribute('aria-pressed',String(fav));
  $('an-fav').setAttribute('aria-label',fav?'Retirer des favoris':'Ajouter aux favoris');
}
$('an-fav').addEventListener('click',()=>{E().toggleFavorite(SYM);paintBadges();});
['vx:favorites-changed','vx:watchlist-changed','vx:follow-changed','vx:position-changed','vx:alert-changed']
  .forEach(ev=>VX.bus.on(ev,paintBadges));

/* Thèse (note utilisateur) */
function paintThesis(){
  const note=E()&&E().note(SYM);
  $('an-thesis').innerHTML=note?esc(note).replace(/\n/g,'<br>'):
    VX.states.emptyDesk('Aucune thèse enregistrée sur ce titre.',
      `<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${SYM}','note')">Écrire la thèse</button>`);
}
VX.bus.on('vx:thesis-changed',paintThesis);

/* Dossier principal — /api/ticker + décision exécutive */
let TF='6m'; let TICKER=null;
async function loadDossier(){
  let t=null,exec=null,status=window.__vxStatus||null;
  /* Anti-course ticker (§CONTINUITY) : on fige la génération de page à l'entrée. Si
     l'utilisateur a navigué ailleurs pendant les fetch, _gen a changé → on abandonne
     AVANT de peindre, pour ne jamais afficher le dossier d'un titre sur une autre page. */
  const _g=(window.VX&&VX.page)?VX.page._gen:0;
  try{t=await VX.fetch('/api/ticker/'+SYM,{ttl:60000});}catch(e){}
  try{exec=await VX.fetch('/api/strategy/decision/'+SYM,{ttl:60000});}catch(e){}
  try{status=status||await VX.fetch('/api/live/status',{ttl:60000});}catch(e){}
  if(window.VX&&VX.page&&VX.page._gen!==_g)return;   // page supplantée → ne rien peindre
  TICKER=t;
  const d=(t&&t.detail)||{};
  /* Source de prix centrale (§9) : le prix de ce ticker devient cohérent partout
     (shell, Portefeuille, Options, listes). Prix invalide ignoré, jamais inventé. */
  try{ if(window.VX&&VX.prices&&d.price!=null){ VX.prices.setLive(SYM,d.price,d.change); VX.prices.setRef(SYM,d.price,(VX.store&&VX.store.get('active_session_id'))||null); } }catch(e){}
  const demo=!!(status&&status.demo);
  const priceDomain=status&&status.domains&&status.domains.prices;
  const scanTs=priceDomain&&priceDomain.ts;
  const scanMode=(status&&status.mode)||'delayed';
  const scanSource=(priceDomain&&priceDomain.source)||'scan';
  if(!t||!t.in_universe&&!d.price){
    $('an-stale').innerHTML='<div class="vx-error-banner">Titre hors du scan courant — dossier partiel. '
      +'<a class="vx-btn vx-btn-sm" href="/system?view=data">Vérifier les données</a></div>';
  }
  /* Hero */
  $('an-name').textContent=(t&&t.company&&(t.company.name||t.company.shortName))||'';
  $('an-price').textContent=VX.fmt.nd(d.price!==undefined?VX.fmt.price(d.price):null);
  const verdictPrice=$('an-verdict-price');
  if(verdictPrice)verdictPrice.textContent=d.price!=null?VX.fmt.price(d.price):'n/d';
  const chg=d.change;
  $('an-change').textContent=chg!==undefined?VX.fmt.pct(chg):'n/d';
  $('an-change').className='vx-mono '+(chg>0?'vx-pos':chg<0?'vx-neg':'vx-muted');
  /* Badge de fraîcheur du prix (§8) : Live / Analyse / À actualiser, honnête. */
  try{
    if($('an-fresh')&&window.VX&&VX.freshness){
      if(d.price==null){$('an-fresh').innerHTML='';}
      else{
        const ageMs=priceDomain&&typeof priceDomain.age_s==='number'?priceDomain.age_s*1000:null;
        if(demo){$('an-fresh').innerHTML='<span class="vx-fresh-chip" data-state="demo">DÉMO</span>';}
        else{$('an-fresh').innerHTML=VX.freshness.chip(VX.freshness.assess({ageMs:ageMs,live:scanMode==='live'}));}
      }
    }
  }catch(e){}
  const decision=(exec&&exec.final_decision)||'ATTENDRE';
  const db=$('an-decision');db.textContent=decision;db.dataset.decision=decision.replace('É','E');
  /* Rail décisionnel sticky */
  const railD=$('an-rail-decision')&&$('an-rail-decision').querySelector('[data-body]');
  if(railD){
    const audit=(exec&&exec.audit_trail)||[];
    railD.innerHTML=`<div class="vx-kpi vx-mb2">
        <span class="vx-kpi-value" style="font-size:24px"><span class="vx-badge vx-badge-decision" data-decision="${decision.replace('É','E')}" style="font-size:14px;padding:5px 14px">${decision}</span></span>
        <span class="vx-kpi-delta vx-muted">${exec&&exec.reason?esc(exec.reason):'moteur exécutif unique'}</span></div>`
      +(audit.length?`<details class="vx-mt1"><summary class="vx-meta" style="cursor:pointer">Audit trail (${audit.length})</summary>
        <ul style="margin:6px 0 0;padding-left:16px;font-size:11.5px" class="vx-dim">${audit.slice(0,8).map(a=>`<li>${esc(typeof a==='string'?a:JSON.stringify(a))}</li>`).join('')}</ul></details>`:'')
      +`<div class="vx-card-footer">${scanTs
        ?VX.updateIndicator(scanTs,'ExecutiveEngine',demo?'fallback':scanMode)
        :'<span class="vx-update" data-mode="fallback"><span class="vx-dot"></span>ExecutiveEngine · fraîcheur n/d</span>'}</div>`;
  }
  const railR=$('an-rail-risks')&&$('an-rail-risks').querySelector('[data-body]');
  if(railR){
    const blocking=(exec&&exec.blocking_anomalies)||(exec&&exec.blocking)||[];
    const warns=(exec&&exec.warnings)||[];
    const all=[...blocking.map(b=>({t:'bloquant',v:b})),...warns.map(w=>({t:'attention',v:w}))];
    let html=all.length?all.slice(0,6).map(r=>
      `<div class="vx-insight" data-tone="risk" style="font-size:12px"><b>${r.t}</b> — ${esc(typeof r.v==='string'?r.v:JSON.stringify(r.v))}</div>`).join('')
      :'<span class="vx-meta">Aucun risque bloquant remonté par les moteurs.</span>';
    /* Carte des risques d'entreprise (§24) — fondamentaux réels. */
    const rm=t&&t.risk_map;
    if(rm&&rm.risks){
      const col={'ÉLEVÉ':'var(--vx-negative,#E9555F)','MODÉRÉ':'var(--vx-warning,#D9BE3C)',
        'FAIBLE':'var(--vx-positive,#2BBE90)','INCONNU':'var(--vx-text-muted,#989092)'};
      html+='<div class="vx-mt3" style="font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--vx-text-muted,#989092)">Carte des risques ('
        +esc(rm.known_count)+'/'+esc(rm.total_count)+' mesurés)</div>'
        +rm.risks.map(r=>`<div style="display:flex;justify-content:space-between;gap:.5rem;padding:.3rem 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:12px">`
          +`<span>${esc(r.category)}</span><span style="color:${col[r.level]||'#888'};font-weight:600">${esc(r.level)}</span></div>`
          +`<div class="vx-meta" style="font-size:11px;margin-bottom:.2rem">${esc(r.note||'')}</div>`).join('');
    }
    railR.innerHTML=html;
  }
  const sc=(exec&&exec.scores)||{};
  const scoreValue=(v)=>v!==null&&v!==undefined&&v!==''&&Number.isFinite(Number(v))?Number(v):null;
  const scAxes=[['Conviction',scoreValue(sc.conviction)],['Marge risque',scoreValue(sc.risk)],
    ['Timing',scoreValue(sc.timing)],['Asymétrie',scoreValue(sc.asymmetry)],
    ['Qualité',scoreValue(sc.data_quality)]];
  const missingAxes=scAxes.filter(a=>a[1]===null).map(a=>a[0]);
  /* Le radar est monté dans une carte BÂTIE À LA MAIN, donc hors du gabarit
     VXCharts.card qui impose question et conclusion. C'est la même cause
     structurelle que le donut « Secteurs » du Portefeuille (lot 12) : ce ne
     sont pas les graphiques qui oublient la règle, ce sont ceux qui n'entrent
     pas par le gabarit. La question et la conclusion sont donc posées ici, à
     la main, et la conclusion est DÉRIVÉE des axes tracés — elle nomme l'axe
     le plus faible et sa valeur, jamais une phrase générique. */
  $('an-scores').innerHTML=scAxes.map(([k,v])=>
    `<span class="vx-badge" title="${k}">${k} <b class="vx-mono">${VX.fmt.nd(v)}</b></span>`).join('')
    +(demo?'<span class="vx-badge" style="color:var(--vx-warning)">DÉMO</span>':'')
    +'<div style="flex:1 0 100%;max-width:240px;margin:8px auto 0">'
    +'<p class="vx-chart-question">Quel axe de la décision est le plus faible ?</p>'
    +'<div id="an-scorecard-radar"></div>'
    +'<p class="vx-chart-conclusion" id="an-scorecard-ccl"></p></div>';
  if(window.VXCharts&&VXCharts.radar&&!missingAxes.length){
    VXCharts.radar('an-scorecard-radar',{axes:scAxes.map(a=>({label:a[0],value:a[1]})),
      max:100,ariaLabel:'Scorecard '+SYM,color:VXCharts.colors.brand,width:240,height:190});
    const faible=scAxes.slice().sort((a,b)=>a[1]-b[1])[0];
    const ccl=$('an-scorecard-ccl');
    if(ccl&&faible)ccl.textContent='Axe le plus faible : '+faible[0]+' ('+faible[1]+'/100).';
  }else if(missingAxes.length){
    $('an-scorecard-radar').innerHTML='<div class="vx-empty" data-state="empty">Radar non tracé — axes n/d : '
      +missingAxes.map(esc).join(', ')+'.</div>';
  }

  /* 3. Graphique principal — Trading Workspace (chandeliers réels + overlays MM) */
  const S=d.series||{};
  const closes=S.close||[];
  const plan=d.plan||{};
  const tfN={'1m':21,'3m':63,'6m':126,'1y':252,'2y':504}[TF]||126;
  const cut=closes.slice(-tfN);
  const tail=(arr)=>Array.isArray(arr)?arr.slice(-tfN):null;
  /* Bougies RÉELLES seulement si OHLC complet fourni par le moteur (jamais inventé). */
  const O=tail(S.open),H=tail(S.high),L=tail(S.low);
  const bars=(O&&H&&L&&O.length===cut.length)?cut.map((c,i)=>({o:O[i],h:H[i],l:L[i],c:c})):[];
  const VC=window.VXCharts||{cols:{}};
  const cc=(n,f)=>(VC.colors&&VC.colors[n])||f;
  /* Overlays = moyennes mobiles RÉELLES calculées côté serveur (ema20/sma50/sma200). */
  const overlays=[
    {label:'MM20',color:cc('amber','#ce8a29'),data:tail(S.ema20),dash:[]},
    {label:'MM50',color:cc('beige','#c8ad8d'),data:tail(S.sma50),dash:[5,3]},
    {label:'MM200',color:cc('neutral','#9d978e'),data:tail(S.sma200),dash:[2,3]},
  ].filter(o=>o.data&&o.data.some(x=>x!=null));
  const earningsDte=(d.earnings_dte!==null&&d.earnings_dte!==undefined&&d.earnings_dte!==''
    &&Number.isFinite(Number(d.earnings_dte))&&Number(d.earnings_dte)>=0)?Math.round(Number(d.earnings_dte)):null;
  const catalyst=$('an-catalyst-strip');
  if(catalyst){
    catalyst.hidden=earningsDte===null;
    catalyst.innerHTML=earningsDte===null?'':`<span class="vx-badge vx-warn">Résultats estimés · dans ${earningsDte} j</span>
      <span class="vx-meta">Événement futur, hors série historique.</span>`;
  }
  if(cut.length>10){
    /* Chandeliers PRO (TradingView LWC) si OHLC daté dispo ; repli auto sur le
       candlestick Chart.js sinon. Même contrat de carte (contrôles TF, explain…). */
    const drawChart=(window.VXCharts&&VXCharts.lwCandlestickCard)||VXCharts.candlestickCard;
    drawChart('an-chart',{
      title:SYM+' — graphique principal',timeframe:TF,
      question:'Le timing est-il exploitable maintenant ?',
      conclusion:(d.verdict?('Verdict technique moteur : '+d.verdict):'—')
        +(plan.rr?` · R:R structurel ${plan.rr}`:''),
      controlsHtml:['1m','3m','6m','1y','2y'].map(tf=>
        `<button class="vx-chip" data-tf="${tf}" aria-pressed="${tf===TF}">${tf}</button>`).join(''),
      labels:cut.map((_,i)=>i-cut.length),bars:bars,closes:cut,overlays:overlays,plan:plan,events:[],
      dates:tail(S.dates),volume:tail(S.volume),
      height:Math.round(Math.min(460,Math.max(340,(window.innerWidth||1200)*0.30))),
      source:scanSource,timestamp:scanTs||null,mode:demo?'demo':scanMode,
      limits:(bars.length?'bougies OHLC quotidiennes':'clôtures quotidiennes')+' du scan · MM = moyennes serveur · niveaux = plan moteur',
      explain:{shows:'Chandeliers (ou clôtures) du titre, moyennes mobiles 20/50/200 et niveaux du plan moteur : entrée, stop (invalidation), objectifs.',
        why:'Le plan chiffré discipline l’exécution : l’invalidation est définie AVANT d’engager du capital ; les MM situent la tendance.',
        confirm:'Cours au-dessus des MM, cassure de la résistance avec volume, breadth favorable.',
        invalidate:`Clôture sous le stop ${VX.fmt.nd(plan.stop)} — la thèse est invalidée, pas « en retard ».`}});
    document.querySelectorAll('[data-tf]').forEach(b=>b.addEventListener('click',()=>{TF=b.dataset.tf;loadDossier();}));
    const chartEl=document.querySelector('#an-chart .vx-lwc')||document.querySelector('#an-chart canvas');
    if(chartEl)chartEl.addEventListener('dblclick',()=>VXCharts.alertFromLevel(SYM,plan.entry||d.price));
  }else{
    $('an-chart').innerHTML='<div class="vx-card">'+VX.states.empty('Série de prix indisponible pour ce titre.')+'</div>';
  }

  /* 4. Fondamental */
  const f=(exec&&exec.fundamental)||{};
  const peers=(t&&t.peers_data)||[];
  /* Le titre analysé n'est JAMAIS dans sa propre liste de pairs → on part de ses
     fondamentaux propres (company.fundamentals) puis on superpose l'entrée pairs
     si elle existe. Sans ce socle, P/E / marge / croissance / ROE restaient vides. */
  const cf=(t&&t.company&&t.company.fundamentals)||{};
  const me=Object.assign({pe:cf.pe,margin:cf.margin,rev_growth:cf.rev_growth,roe:cf.roe},
                         peers.find(p=>p.symbol===SYM)||{});
  body('an-fundamental',
    kv('Score fondamental moteur',d.st_fund??f.score)
    +kv('Croissance CA',me.rev_growth!==undefined?VX.fmt.pct(me.rev_growth*100,0):null,me.rev_growth==null?'':me.rev_growth>0?'vx-pos':me.rev_growth<0?'vx-neg':'')
    +kv('Marge',me.margin!==undefined?VX.fmt.pct(me.margin*100,0):null)
    +kv('P/E',me.pe!=null?(+me.pe).toFixed(1):null)+kv('ROE',me.roe!==undefined&&me.roe!==null?VX.fmt.pct(me.roe*100,0):null)
    +kv('Médiane sectorielle P/E',t&&t.sector_median&&(t.sector_median.median_pe??t.sector_median))
    +(peers.length>1?`<div class="vx-meta vx-mt2">Pairs : ${peers.filter(p=>p.symbol!==SYM).slice(0,4).map(p=>
      `<button class="vx-btn vx-btn-sm vx-btn-ghost vx-ticker" data-open-analysis="${p.symbol}">${p.symbol}</button>`).join('')}</div>`:''));

  /* 5. Catalyseurs */
  body('an-catalysts',
    kv('Prochains résultats',earningsDte!==null?('dans '+earningsDte+' j'):null,
       earningsDte!==null&&earningsDte<=10?'vx-warn':'')
    +kv('Politique par défaut','sortie avant annonce (hold-through = dossier complet exigé)')
    +`<div class="vx-meta vx-mt2"><a href="/opportunities?view=calendar">Calendrier complet →</a></div>`);

  /* 6. Technique */
  const ttm=(d.ttm_fired?'🚀 sortie de compression':(d.ttm_squeeze?'🔒 en compression (BB dans Keltner)':null));
  const ttmDir=d.ttm_dir==='up'?' · momentum haussier':d.ttm_dir==='down'?' · momentum baissier':'';
  function perfBars(d){
    const rows=[['1 sem.',d.perf_w],['1 mois',d.perf_m],['1 trim.',d.perf_q],['1 an',d.perf_y]].filter(r=>r[1]!=null&&!isNaN(r[1]));
    if(!rows.length)return '';
    const maxAbs=Math.max(5,...rows.map(r=>Math.abs(r[1])));
    return '<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#30292B);padding-top:8px">'
      +'<div class="vx-meta vx-mb1" style="text-transform:uppercase;letter-spacing:.04em">Performance multi-horizons</div>'
      /* LOT 130 : matiere verre — la barre est un degrade de sa propre couleur,
         doux au centre (zero) et DENSE a l'extremite de la valeur (meme
         grammaire que C.bars), via color-mix sur les tokens (aucun litteral). */
      +rows.map(function(r){const v=r[1];const neg=v<0;const w=Math.min(50,Math.abs(v)/maxAbs*50);
        const tok=neg?'var(--vx-negative,#E9555F)':'var(--vx-positive,#2BBE90)';
        const grad='linear-gradient('+(neg?'270deg':'90deg')+',color-mix(in srgb,'+tok+' 35%,transparent),'+tok+')';
        return '<div style="display:flex;align-items:center;gap:6px;margin:2px 0" role="img" aria-label="'+r[0]+' '+(v>=0?'+':'')+v+' %">'
          +'<span style="width:52px;font-size:10.5px;color:var(--vx-text-muted,#989092)">'+r[0]+'</span>'
          +'<span style="flex:1;height:10px;position:relative;background:var(--vx-surface-3,#121214);border-radius:3px;overflow:hidden">'
            +'<span style="position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(255,255,255,.16)"></span>'
            +'<span style="position:absolute;top:0;bottom:0;'+(neg?('right:50%;width:'+w.toFixed(1)+'%'):('left:50%;width:'+w.toFixed(1)+'%'))+';background:'+grad+';border-radius:2px"></span></span>'
          +'<span style="width:54px;text-align:right;font-size:10.5px;font-variant-numeric:tabular-nums" class="'+(neg?'vx-neg':'vx-pos')+'">'+(v>=0?'+':'')+VX.fmt.num(v,1)+'%</span></div>';
      }).join('')+'</div>';
  }
  body('an-technical',
    kv('Score',d.score)+kv('Verdict technique (métadonnée)',d.verdict)
    +kv('Force relative',d.rs)+kv('RSI',d.rsi)
    +kv('Position 52 semaines',d.pos52!==undefined?d.pos52+' %':null)
    +kv('Extension vs ATR',d.ext_atr,(d.ext_atr>=2.5?'vx-warn':''))
    +(ttm?kv('TTM Squeeze',ttm+ttmDir,(d.ttm_fired&&d.ttm_dir==='up'?'vx-pos':d.ttm_fired&&d.ttm_dir==='down'?'vx-neg':'')):'')
    +perfBars(d)
    +`<div class="vx-meta vx-mt2">La décision finale unique reste ${decision} — les verdicts techniques sont des entrées du moteur exécutif.</div>`);

  /* 7. Sentiment + consensus analystes (données company déjà chargées → objectif de cours + potentiel) */
  const an=(t&&t.company&&t.company.analysts)||{};
  const _px=d.price, _tgt=an.target_mean;
  const _up=(_tgt&&_px)?((_tgt/_px-1)*100):null;
  const _rl={strong_buy:'Achat fort',buy:'Achat',outperform:'Surperformance',hold:'Conserver',underperform:'Sous-performance',sell:'Vente'}[an.rating]||an.rating;
  const consensus=(an.rating||_tgt)?(
    `<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#30292B);padding-top:8px">`
    +(an.rating?`<div class="vx-kv"><span class="k">Consensus analystes</span><span class="v">${esc(_rl||'—')}${an.rating_mean!=null?` (${(+an.rating_mean).toFixed(1)}/5)`:''}${an.n_analysts?` · ${an.n_analysts} analystes`:''}</span></div>`:'')
    +(_tgt?`<div class="vx-kv"><span class="k">Objectif moyen</span><span class="v">${VX.fmt.price(_tgt)}${_up!=null?` <span class="${_up>=0?'vx-pos':'vx-neg'}">(${_up>=0?'+':''}${_up.toFixed(1)}%)</span>`:''}</span></div>`:'')
    +((an.target_low&&an.target_high)?(function(){
      /* LOT 141 : la fourchette d'objectifs n'est plus du texte nu — RAIL de
         verre low -> high avec le COURS (cyan) et l'OBJECTIF MOYEN (warning)
         en reperes halotes : on voit ou le prix vit dans la fourchette des
         analystes. Reperes clampes aux bords (jamais inventes). */
      const lo=an.target_low,hi=an.target_high,span=(hi-lo)||1;
      const pos=(v)=>Math.max(2,Math.min(98,(v-lo)/span*100));
      const mk=(v,tok,lbl)=>v==null?'':'<span title="'+lbl+' '+VX.fmt.price(v)+'" style="position:absolute;left:'+pos(v).toFixed(1)+'%;top:-2px;bottom:-2px;width:2px;background:'+tok+';border-radius:1px;box-shadow:0 0 5px color-mix(in srgb,'+tok+' 55%,transparent)"></span>';
      return '<div class="vx-kv"><span class="k">Fourchette</span><span class="v" style="display:inline-flex;align-items:center;gap:8px;min-width:0">'
        +'<span class="vx-dim" style="font-size:11px">'+VX.fmt.price(lo)+'</span>'
        +'<span style="position:relative;flex:1;min-width:70px;height:7px;background:linear-gradient(90deg,color-mix(in srgb,var(--vx-brand,#9B7BFF) 12%,transparent),color-mix(in srgb,var(--vx-brand,#9B7BFF) 30%,transparent));border-radius:3px">'
        +mk(_px,'var(--vx-cyan,#45D6E8)','cours')
        +mk(_tgt,'var(--vx-warning,#D9BE3C)','objectif moyen')
        +'</span><span class="vx-dim" style="font-size:11px">'+VX.fmt.price(hi)+'</span></span></div>';
    })():'')
    +`</div>`):'';
  body('an-sentiment',
    kv('Force relative vs univers',d.rs)
    +kv('Régime marché',(exec&&exec.technical&&exec.technical.regime)||null)
    +consensus
    +`<div class="vx-meta vx-mt2">Positionnement institutionnel : proxies uniquement — jamais présentés comme des flux certains. Consensus analystes = données publiques (peut dater).</div>`);

  /* 8. Anomalies */
  try{
    const a=await VX.fetch('/api/anomalies/'+SYM,{ttl:120000});
    body('an-anomalies',(a.anomalies&&a.anomalies.length)?
      a.anomalies.map(x=>`<span class="vx-badge" title="${esc(x.impact||'')}" style="margin:2px">${x.code}</span>`).join('')
      +`<div class="vx-meta vx-mt2">${esc(a.note||'')}</div>`
      :VX.states.empty('Aucune anomalie détectée sur la série disponible.'));
  }catch(e){body('an-anomalies',VX.states.error('Moteur d’anomalies injoignable'));}

  /* TradingView (§30) + confluence vs verdict moteur (miroir de tv_confluence.py) */
  try{
    const TV_BULL=['SUPPORT_RECLAIM','BREAKOUT_CONFIRMED','BREAKOUT_RETEST','MOMENTUM_ACCELERATION','VOLUME_EXPANSION','TREND_ALIGNMENT'];
    const TV_BEAR=['FAILED_BREAKOUT','THESIS_INVALIDATION'];
    const vDn=/AVOID|ÉVITER|EVITER|ALL[ÉE]GER|SORTIR|R[ÉE]DUIRE|NO_NEW_RISK|VENDRE|REFUS|REJET/i.test(d.verdict||'');
    const vUp=/ACHETER|BUY|RENFORCER|ACCUMULER/i.test(d.verdict||'');
    /* baissier d'abord (miroir de tv_confluence.verdict_stance) — jamais un faux CONFIRME */
    const vStance=vDn?'BEARISH':(vUp?'BULLISH':'NEUTRAL');
    function confl(sig){
      const sd=TV_BULL.indexOf(sig)>=0?'BULLISH':(TV_BEAR.indexOf(sig)>=0?'BEARISH':'NEUTRAL');
      if(sd==='NEUTRAL'||vStance==='NEUTRAL')return ['NEUTRE','vx-dim','·'];
      if(sd===vStance)return ['CONFIRME','vx-pos','✓'];
      return ['CONTREDIT','vx-neg','✗'];
    }
    const tv=await VX.fetch('/api/tradingview/signals?symbol='+SYM,{ttl:60000});
    const sigs=(tv.signals||[]).slice(-4).reverse();
    let confirms=0,contradicts=0;
    sigs.forEach(s=>{const c=confl(s.signal);if(c[0]==='CONFIRME')confirms++;else if(c[0]==='CONTREDIT')contradicts++;});
    const overall=contradicts&&!confirms?['CONTREDIT le verdict','vx-neg']
      :confirms&&!contradicts?['CONFIRME le verdict','vx-pos']
      :(confirms||contradicts)?['signaux MIXTES','vx-dim']:['—','vx-dim'];
    body('an-tv',(sigs.length?
      (d.verdict?`<div class="vx-kv"><span class="k">Confluence</span><span class="v ${overall[1]}"><b>${overall[0]}</b> <span class="vx-meta">(vs ${esc(d.verdict)})</span></span></div>`:'')
      +sigs.map(s=>{
      const fresh=(s.fresh!==undefined)?s.fresh:((Date.now()/1000-(s.received_ts||0))<=6*3600);
      const c=confl(s.signal);
      return `<div class="vx-kv"><span class="k">${s.signal}</span>
        <span class="v"><span class="vx-badge ${c[1]}" title="confluence">${c[2]} ${c[0]}</span>
        ${fresh?'':'<span class="vx-badge">rassis</span>'}
        <span class="vx-meta">${VX.fmt.ago((s.received_ts||0)*1000)}</span></span></div>`;}).join('')
      +'<div class="vx-meta vx-mt2">Un signal TradingView déclenche une réévaluation — jamais un ACHETER direct. La confluence est une lecture de cohérence, pas une décision.</div>'
      :VX.states.empty('Aucun signal TradingView reçu pour ce titre.',
        '<span class="vx-meta">Webhook : /api/tradingview/webhook (voir tradingview/README.md)</span>'))
      +`<div class="vx-flex vx-mt2">
        <a class="vx-btn vx-btn-sm" target="_blank" rel="noopener" href="https://www.tradingview.com/chart/?symbol=${SYM}">Ouvrir dans TradingView ↗</a>
        <button class="vx-btn vx-btn-sm vx-btn-ghost" onclick="VXEntities.openAddModal('${SYM}','alert')">Créer une alerte</button></div>`);
  }catch(e){body('an-tv',VX.states.empty('Intégration TradingView non configurée — aucune donnée inventée.'));}

  /* 9. Scénarios : domicile unique = Carte-Scénario en tête (loadDecisionStack). */

  /* 10. Plan — échelle Risk/Reward (§24.5) : niveaux du plan proportionnels au prix */
  function rrLadder(px,plan){
    const VC=window.VXCharts||{colors:{}};const col=(n,f)=>(VC.colors&&VC.colors[n])||f;
    const lv=[];
    if(plan.stop!=null)lv.push({k:'Stop',v:plan.stop,c:col('negative','#E9555F')});
    const e=plan.entry;
    if(e!=null)lv.push({k:'Entrée',v:e,c:col('info','#45D6E8')});
    else if(px!=null)lv.push({k:'Cours',v:px,c:col('neutral','#8A8284')});
    [plan.tp1,plan.tp2,plan.tp3].forEach(function(t,i){if(t!=null)lv.push({k:'TP'+(i+1),v:t,c:col('positive','#2BBE90')});});
    if(lv.length<2)return '';
    const vals=lv.map(function(l){return l.v;});
    const min=Math.min.apply(null,vals),max=Math.max.apply(null,vals),rng=(max-min)||1;
    const W=280,H=16+lv.length*26,padT=12,padB=12,plotH=H-padT-padB,axX=70;
    const y=function(v){return padT+(max-v)/rng*plotH;};
    let bands='';
    if(plan.stop!=null&&e!=null)bands+='<rect x="'+(axX-4)+'" y="'+Math.min(y(e),y(plan.stop)).toFixed(1)+'" width="8" height="'+Math.abs(y(plan.stop)-y(e)).toFixed(1)+'" fill="'+col('negative','#dc5f52')+'" fill-opacity=".18"/>';
    const tps=[plan.tp1,plan.tp2,plan.tp3].filter(function(t){return t!=null;});
    const topTp=tps.length?Math.max.apply(null,tps):null;
    if(topTp!=null&&e!=null)bands+='<rect x="'+(axX-4)+'" y="'+Math.min(y(e),y(topTp)).toFixed(1)+'" width="8" height="'+Math.abs(y(topTp)-y(e)).toFixed(1)+'" fill="'+col('positive','#38b879')+'" fill-opacity=".16"/>';
    const rows=lv.map(function(l){const yy=y(l.v);const pct=(px&&l.v)?((l.v/px-1)*100):null;
      return '<line x1="'+axX+'" y1="'+yy.toFixed(1)+'" x2="'+(axX+8)+'" y2="'+yy.toFixed(1)+'" stroke="'+l.c+'" stroke-width="2"/>'
        +'<circle cx="'+axX+'" cy="'+yy.toFixed(1)+'" r="3" fill="'+l.c+'"/>'
        +'<text x="'+(axX-8)+'" y="'+(yy+3).toFixed(1)+'" text-anchor="end" font-size="10" fill="var(--vx-text-secondary,#BABABA)">'+l.k+'</text>'
        +'<text x="'+(axX+14)+'" y="'+(yy+3).toFixed(1)+'" font-size="10.5" fill="'+l.c+'" style="font-variant-numeric:tabular-nums">'+VX.fmt.nd(l.v)+(pct!=null?' ('+(pct>=0?'+':'')+pct.toFixed(1)+'%)':'')+'</text>';}).join('');
    const aria='Échelle risque/récompense : '+lv.map(function(l){return l.k+' '+VX.fmt.nd(l.v);}).join(', ')+(plan.rr?', R:R '+plan.rr:'');
    return '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-width:'+W+'px;display:block;margin:0 auto 10px" role="img" aria-label="'+aria.replace(/"/g,'&quot;')+'">'
      +'<line x1="'+axX+'" y1="'+padT+'" x2="'+axX+'" y2="'+(H-padB)+'" stroke="rgba(255,255,255,.12)"/>'+bands+rows+'</svg>';
  }
  body('an-plan',
    rrLadder(d.price,plan)
    +`<details class="an-disclosure an-disclosure--nested vx-mt3">
      <summary>Voir tous les niveaux</summary>
      <div class="vx-mt2">`
    +kv('Entrée',plan.entry)+kv('Stop (invalidation sous-jacent)',plan.stop,'vx-neg')
    +kv('TP1',plan.tp1,'vx-pos')+kv('TP2',plan.tp2,'vx-pos')+kv('TP3',plan.tp3,'vx-pos')
    +kv('R:R structurel',plan.rr)
    +`</div></details>
    <div class="vx-flex vx-mt3" style="flex-wrap:wrap;gap:.4rem">
      <button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal('${SYM}','follow')">Créer un suivi</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" onclick="VXCharts.alertFromLevel('${SYM}',${JSON.stringify(plan.entry??null)})">Alerte sur l’entrée</button>
      <button class="vx-btn vx-btn-sm vx-btn-soft" onclick="window.__prepOrder&&window.__prepOrder('${SYM}')">Calculer le dimensionnement</button>
    </div>
    <div id="an-order-ticket" class="vx-mt2"></div>`);
  window.__prepOrder=function(sym){
    const host=document.getElementById('an-order-ticket');if(!host)return;
    const av=Number(localStorage.getItem('vxAccountValue')||'')||null;
    host.innerHTML=`<div class="vx-card">
      <div class="vx-card-header"><span class="vx-card-title">Dimensionnement indicatif — aucune exécution</span></div>
      <div class="vx-card-body vx-flex" style="gap:.5rem;flex-wrap:wrap;align-items:end">
        <label class="vx-field" style="max-width:170px"><span>Valeur du compte ($)</span>
          <input id="ot-av" class="vx-input" type="number" step="any" value="${av||''}" placeholder="ex. 100000"></label>
        <label class="vx-field" style="max-width:130px"><span>Risque par trade (%)</span>
          <input id="ot-rp" class="vx-input" type="number" step="any" value="1"></label>
        <button class="vx-btn vx-btn-sm" id="ot-go">Calculer</button>
      </div>
      <div id="ot-out"></div></div>`;
    document.getElementById('ot-go').addEventListener('click',function(){
      const avv=Number(document.getElementById('ot-av').value)||null;
      const rp=Number(document.getElementById('ot-rp').value)||null;
      if(avv)localStorage.setItem('vxAccountValue',String(avv));
      fetch('/api/planning/ticket',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({symbol:sym,account_value:avv,risk_pct:rp})})
        .then(r=>r.json()).then(function(t){
          const out=document.getElementById('ot-out');if(!out)return;
          const s=t.sizing||{};
          const warn=(t.blockers||[]).concat(t.warnings||[]);
          out.innerHTML='<div class="vx-mt2">'
            +'<div class="vx-stats-row" style="display:flex;gap:1.2rem;flex-wrap:wrap">'
            +'<div><div class="vx-meta">Quantité</div><b style="font-size:18px">'+(t.qty!=null?t.qty:'—')+'</b></div>'
            +'<div><div class="vx-meta">Capital à risque</div><b>'+(s.capital_at_risk!=null?'$'+s.capital_at_risk:'—')+'</b></div>'
            +'<div><div class="vx-meta">Capital engagé</div><b>'+(s.capital_deployed!=null?'$'+s.capital_deployed:'—')+'</b></div>'
            +'<div><div class="vx-meta">Poids projeté</div><b>'+(s.weight_pct!=null?s.weight_pct+' %':'—')+'</b></div>'
            +'<div><div class="vx-meta">R:R</div><b>'+(t.reward_risk!=null?t.reward_risk:'—')+'</b></div></div>'
            +(t.blocked?'<div class="vx-stale-banner vx-mt2">Préparation bloquée par la stratégie : '+warn.map(esc).join(' · ')+'</div>'
              :(warn.length?'<div class="vx-meta vx-mt2" style="color:var(--vx-warning)">'+warn.map(esc).join(' · ')+'</div>':''))
            +'<pre id="ot-pre" style="white-space:pre-wrap;background:var(--vx-surface-2,#121214);padding:.7rem;border-radius:8px;margin-top:.7rem;font-size:12px">'+esc(t.copy_text||'')+'</pre>'
            +'<button class="vx-btn vx-btn-sm vx-btn-ghost" id="ot-copy">Copier l’analyse</button>'
            +'<div class="vx-meta vx-mt1">'+esc(t.disclaimer||'')+'</div></div>';
          const cp=document.getElementById('ot-copy');
          if(cp)cp.addEventListener('click',function(){
            const pre=document.getElementById('ot-pre');
            if(pre&&navigator.clipboard)navigator.clipboard.writeText(pre.textContent);
            VX.toast('Ticket d’analyse copié — aucune transmission','success');});
        }).catch(function(e){document.getElementById('ot-out').innerHTML='<div class="vx-error-banner">'+esc(e.message)+'</div>';});
    });
  };

  /* 11. Options */
  try{
    const ob=await VX.fetch('/api/options-for/'+SYM+'?type=CALL',{ttl:180000});
    const cs=(ob&&(ob.contracts||ob.list||ob.best))||ob||{};
    const arr=Array.isArray(cs)?cs:(cs.contracts||[]);
    body('an-options',arr.length?
      `<div class="vx-table-wrap vx-table-cards"><table class="vx-table"><thead><tr>
        <th>Contrat</th><th class="vx-num">Strike</th><th>Échéance</th><th class="vx-num">Delta</th>
        <th class="vx-num">Prime</th><th class="vx-num">OI</th><th></th></tr></thead><tbody>${
        arr.slice(0,3).map(c=>`<tr>
          <td data-label="Contrat"><span class="vx-badge" style="color:var(--vx-violet)">CALL</span></td>
          <td data-label="Strike" class="vx-num">${VX.fmt.nd(c.strike)}</td>
          <td data-label="Échéance" class="vx-mono">${VX.fmt.nd(c.exp||c.expiry)}</td>
          <td data-label="Delta" class="vx-num">${VX.fmt.nd(c.delta)}</td>
          <td data-label="Prime" class="vx-num">${VX.fmt.nd(c.mid??c.premium??c.cost)}</td>
          <td data-label="OI" class="vx-num">${VX.fmt.nd(c.oi??c.openInterest)}</td>
          <td><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=options&sym=${SYM}">Analyser →</a></td></tr>`).join('')}
      </tbody></table></div>`
      :VX.states.empty('Aucun contrat CALL exploitable retourné par le moteur.',
        `<a class="vx-btn vx-btn-sm" href="/opportunities?view=options&sym=${SYM}">Ouvrir le desk options</a>`));
  }catch(e){body('an-options',VX.states.empty('Chaîne d’options indisponible (IBKR hors ligne ou titre sans options).'));}

  /* 12. Compatibilité portefeuille */
  const positions=E()?E().positions():[];
  const held=positions.filter(p=>p.sym===SYM);
  const count=positions.length;
  body('an-portfolio-fit',
    kv('Positions déclarées',count+' / 10 max')
    +kv('Ce titre',held.length?('détenu ('+held.map(h=>h.type).join(', ')+')'):'non détenu')
    +kv('Règle',count>=10?'portefeuille plein — remplacement obligatoire':'place disponible',
        count>=10?'vx-warn':'vx-pos')
    +`<div class="vx-meta vx-mt2"><a href="/portfolio?view=risk">Risque complet (positions réelles) →</a></div>`);

  /* 13. Historique */
  const jr=(E()?E().journal():[]).filter(j=>j.ticker===SYM).slice(-5).reverse();
  const follows=(E()?E().follows():[]).filter(r=>r.sym===SYM);
  body('an-history',
    (follows.length?`<div class="vx-insight">Suivi actif depuis ${follows[0].followed}
      — stop ${VX.fmt.nd(follows[0].stop)}, objectif ${VX.fmt.nd(follows[0].tgt)}</div>`:'')
    +(jr.length?jr.map(j=>`<div class="vx-kv"><span class="k">${j.date} · ${esc(j.dir||'')}</span>
      <span class="v ${j.pnl>0?'vx-pos':j.pnl<0?'vx-neg':''}">${j.result||''} ${j.pnl!==undefined&&j.pnl!==''?VX.fmt.num(j.pnl):''}</span></div>`).join('')
      :VX.states.emptyDesk('Aucune entrée de journal sur ce titre.'))
    +`<div class="vx-meta vx-mt2"><a href="/journal?view=journal&sym=${SYM}">Journal complet →</a></div>`);
  paintBadges();paintThesis();
  try{loadAnalyst();}catch(e){}
}

/* Analystes PROFONDS (à la demande) : révisions BPA, surprises, notes, détention, initiés.
   Enrichit Catalyseurs + Sentiment sans bloquer le dossier principal. */
async function loadAnalyst(){
  let a=null;
  try{a=await VX.fetch('/api/analyst/'+SYM,{ttl:600000});}catch(e){}
  if(!a||a.demo||a.error)return;
  const $b=id=>document.querySelector('#'+id+' [data-body]');
  const price=(TICKER&&TICKER.detail&&TICKER.detail.price)||null;
  /* Catalyseurs : révisions BPA + surprises + notes datées */
  const er=a.eps_revisions, su=a.surprises, sm=su&&su.summary, ra=a.ratings_actions, et=a.eps_trend;
  let cat='';
  if(su&&su.next)cat+=kv('Prochains résultats (est.)',su.next);
  if(sm)cat+=kv('Surprises BPA',`battu ${sm.beats}/${sm.total} trim.`+(sm.avg!=null?` · moy. ${sm.avg>=0?'+':''}${sm.avg}%`:''),(sm.beats>=sm.total*0.7?'vx-pos':sm.beats<=sm.total*0.4?'vx-neg':''));
  if(er&&er.net30!=null)cat+=kv('Révisions BPA (30j)',`${er.up30||0} ↑ / ${er.down30||0} ↓`+(et&&et.revision_pct_90d!=null?` · estim. ${et.revision_pct_90d>=0?'+':''}${et.revision_pct_90d}% /90j`:''),(er.trend==='up'?'vx-pos':er.trend==='down'?'vx-neg':''));
  if(a.growth_fwd!=null)cat+=kv('Croissance BPA attendue',`${a.growth_fwd>=0?'+':''}${a.growth_fwd}%`);
  if(ra&&ra.length){
    cat+=`<div class="vx-meta vx-mt2" style="text-transform:uppercase;letter-spacing:.04em">Notes récentes</div>`;
    cat+=ra.slice(0,4).map(function(r){
      const s=(r.pt_action||'')+' '+(r.to||'');
      const dir=/rais|upgrade|overweight|\bbuy\b|outperform/i.test(s)?'vx-pos':/low|cut|downgrade|underweight|\bsell\b|reduce/i.test(s)?'vx-neg':'';
      const tgt=r.target?` → ${VX.fmt.price(r.target)}`+(r.prior&&r.prior!==r.target?` (av. ${VX.fmt.price(r.prior)})`:''):'';
      return `<div class="vx-kv"><span class="k">${esc(r.date)} · ${esc(r.firm)}</span><span class="v ${dir}">${esc(r.to||r.pt_action||r.action)}${tgt}</span></div>`;
    }).join('');
  }
  if(cat){const el=$b('an-catalysts');if(el)el.innerHTML+=`<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#30292B);padding-top:8px">${cat}</div>`;}
  /* Sentiment : détention institutionnelle (13F) + initiés */
  let sen='';
  if(a.holders&&a.holders.length){
    sen+=`<div class="vx-meta vx-mt2" style="text-transform:uppercase;letter-spacing:.04em">Top détenteurs (13F)</div>`;
    sen+=a.holders.slice(0,5).map(function(h){
      return `<div class="vx-kv"><span class="k">${esc(h.holder)}</span><span class="v">${h.pct!=null?(h.pct*100).toFixed(1)+' %':'—'}${h.change?` <span class="${h.change>0?'vx-pos':'vx-neg'}">(${h.change>0?'+':''}${(h.change*100).toFixed(0)}%)</span>`:''}</span></div>`;
    }).join('');
  }
  if(a.insider){const ib=a.insider;
    sen+=kv('Initiés (récent)',`${ib.buys} achat(s) / ${ib.sells} vente(s)`,(ib.bias==='buy'?'vx-pos':ib.bias==='sell'?'vx-neg':''));
  }
  if(sen){const el=$b('an-sentiment');if(el)el.innerHTML+=`<div class="vx-mt2" style="border-top:1px solid var(--vx-border,#30292B);padding-top:8px">${sen}</div>`;}
}
/* ── Carte-Verdict + Carte-Scénario + Raisonnement du comité (decision stack) ── */
function pctRet(entry,tgt){if(entry==null||tgt==null||!entry)return null;return (tgt-entry)/entry*100;}
async function loadDecisionStack(){
  let dec=null;
  try{dec=await VX.fetch('/api/decision/'+SYM,{ttl:60000});}catch(e){}
  const V=$('an-verdict'),SC=$('an-scenarios'),CO=$('an-committee');
  if(!dec){if(V)V.innerHTML='<div class="vx-card">'+VX.states.error('Décision indisponible')+'</div>';return;}
  /* DATA_INSUFFICIENT → état honnête, aucune conviction. */
  if(dec.final_decision==='DATA_INSUFFICIENT'){
    const miss=(dec.data_quality&&(dec.data_quality.missing_fields||[]).join(', '))||'données du titre absentes';
    if(V)V.innerHTML='<section class="vx-card vx-verdict-card" data-tone="gray">'
      +'<div class="vx-verdict-head"><span class="vx-verdict-label">Données insuffisantes</span>'
      +'<span class="vx-verdict-score">confiance 0</span></div>'
      +'<div class="vx-insufficient"><div class="vx-insufficient-icon">&mdash;</div>'
      +'<div><b>Vertex ne tranche pas '+esc(SYM)+'.</b>'
      +'<div class="vx-insufficient-why">Données insuffisantes ('+esc(miss)+'). Aucune conviction affichée tant que le dossier n\'est pas complet.</div></div></div>'
      +'<div class="vx-mt3"><a class="vx-btn vx-btn-soft" href="/system?view=data">Prochaine action : vérifier les données →</a></div></section>';
    if(SC)SC.innerHTML='';if(CO)CO.innerHTML='';
    return;
  }
  const tone=dec.decision_tone||'gray';
  const conf=(dec.confidence!=null)?dec.confidence:null;
  const entry=dec.entry,inval=dec.invalidation!=null?dec.invalidation:dec.stop;
  const tgts=dec.targets||{};
  const dq=(dec.data_quality&&dec.data_quality.grade)?('données '+dec.data_quality.grade):'';
  const cell=(k,v,id)=>'<div class="vx-verdict-cell"><span class="k">'+k+'</span><span class="v"'
    +(id?' id="'+id+'"':'')+'>'+v+'</span></div>';
  if(V)V.innerHTML='<section class="vx-card vx-verdict-card" data-tone="'+esc(tone)+'">'
    +'<div class="vx-verdict-head"><span class="vx-verdict-label">'+esc(dec.decision_label||dec.final_decision)+'</span>'
    +(dec.grade?'<span class="vx-badge">'+esc(dec.grade)+'</span>':'')
    +(conf!=null?'<span class="vx-verdict-score">confiance '+conf+'/100</span>':'')
    +'<span class="vx-actions">'+('<span class="vx-freshness" data-live="'+(demoState()?'fallback':'delayed')+'"><span class="vx-live-dot"></span>'+(demoState()?'Démo':'Différé')+'</span>')+'</span></div>'
    +'<div class="vx-verdict-grid">'
    +cell('Prix',(TICKER&&TICKER.detail&&TICKER.detail.price!=null)?VX.fmt.price(TICKER.detail.price):'n/d','an-verdict-price')
    +cell('Entrée',entry!=null?VX.fmt.price(entry):'—')
    +cell('Invalidation',inval!=null?VX.fmt.price(inval):'—')
    +cell('Conviction',dec.conviction!=null?dec.conviction:'—')
    +cell('Véhicule',esc(dec.vehicle||'—'))
    +(dq?cell('Qualité',esc(dq)):'')
    +'</div>'
    +'<div class="vx-mt3 vx-flex vx-wrap vx-gap2">'
    +'<a class="vx-btn vx-btn-primary" href="#an-scenarios">Voir les scénarios ↓</a>'
    +'<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\''+SYM+'\',\'alert\')">Alerte sur l\'invalidation</button>'
    +'<button class="vx-btn vx-btn-sm" onclick="VXEntities.openAddModal(\''+SYM+'\',\'note\')">Journaliser l\'hypothèse</button></div>'
    +'</section>';
  /* Carte-Scénario : pessimiste / probable / exceptionnel dérivés du plan réel
     (entrée → invalidation / cibles). Aucune probabilité inventée. */
  if(SC){
    const rDown=pctRet(entry,inval),rBase=pctRet(entry,tgts.tp1!=null?tgts.tp1:tgts.tp2),rUp=pctRet(entry,tgts.tp3!=null?tgts.tp3:tgts.tp2);
    const asym=(rDown!=null&&rUp!=null&&rDown!==0)?Math.abs(rUp/rDown):null;
    const scen=(kind,k,tgt,ret,note)=>'<div class="vx-scenario" data-kind="'+kind+'"><span class="vx-scenario-k">'+k+'</span>'
      +'<span class="vx-scenario-v">'+(ret!=null?(ret>0?'+':'')+ret.toFixed(1)+' %':'—')+'</span>'
      +'<span class="vx-scenario-note">'+(tgt!=null?'cible '+VX.fmt.price(tgt):'cible n/d')+(note?' · '+note:'')+'</span></div>';
    if(entry!=null&&(inval!=null||tgts.tp1!=null)){
      SC.innerHTML='<section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Scénarios</span>'
        +'<span class="vx-chart-question">Combien puis-je perdre, gagner probablement, gagner exceptionnellement ?</span></div>'
        +'<div class="vx-scenario-grid">'
        +scen('down','Pessimiste',inval,rDown,'invalidation')
        +scen('base','Probable',tgts.tp1!=null?tgts.tp1:tgts.tp2,rBase,'cible 1')
        +scen('up','Exceptionnel',tgts.tp3!=null?tgts.tp3:tgts.tp2,rUp,'cible étendue')
        +'</div>'
        +(asym!=null?'<div class="vx-kv vx-mt2"><span class="k">Asymétrie (gain exceptionnel / perte max)</span><span class="v vx-mono '+(asym>=2?'vx-pos':asym>=1?'':'vx-neg')+'">'+asym.toFixed(1)+'×</span></div>':'')
        +'<div class="vx-card-foot"><span class="vx-meta">Scénarios dérivés du plan de niveaux moteur (entrée/invalidation/cibles) — aucune probabilité inventée.</span></div></section>';
    }else{SC.innerHTML='<div class="vx-card">'+VX.states.empty('Plan de niveaux insuffisant pour construire les scénarios.')+'</div>';}
  }
  /* Raisonnement du comité (intégré depuis Intelligence) */
  if(CO){
    const com=dec.committee||{};
    const pros=(dec.pros||[]).slice(0,4),cons=(dec.cons||[]).slice(0,4),unk=(dec.unknowns||[]).slice(0,3);
    CO.innerHTML='<section class="vx-card"><div class="vx-card-header"><span class="vx-card-title">Raisonnement du comité</span>'
      +(com.agreement!=null?'<span class="vx-actions"><span class="vx-badge">accord '+com.agreement+'/100</span></span>':'')+'</div>'
      +(com.view?'<div class="vx-dim vx-mb2">Consensus : <b>'+esc(com.view)+'</b>'+(com.has_contradiction?' · <span class="vx-neg">contradictions internes exposées</span>':'')+'</div>':'')
      +'<div class="vx-grid">'
      +'<div class="vx-col-6"><div class="vx-meta vx-mb1">Facteurs positifs</div>'+(pros.length?pros.map(p=>'<div class="vx-pos" style="font-size:12px">+ '+esc(p)+'</div>').join(''):'<span class="vx-muted">—</span>')+'</div>'
      +'<div class="vx-col-6"><div class="vx-meta vx-mb1">Facteurs négatifs</div>'+(cons.length?cons.map(c=>'<div class="vx-neg" style="font-size:12px">− '+esc(c)+'</div>').join(''):'<span class="vx-muted">—</span>')+'</div>'
      +'</div>'
      +(com.devils_advocate?'<div class="vx-insight vx-mt2" data-tone="risk"><b>Avocat du diable</b><div class="vx-mt1">'+esc(com.devils_advocate)+'</div></div>':'')
      +(unk.length?'<div class="vx-kv vx-mt2"><span class="k">Ce que nous ne savons pas</span><span class="v vx-muted">'+unk.map(esc).join(' · ')+'</span></div>':'')
      +'<div class="vx-card-foot"><span class="vx-meta">Comité déterministe (decision stack) — l\'IA explique, ne décide jamais.</span></div></section>';
  }
}
function demoState(){return !!(window.__vxStatus&&window.__vxStatus.demo);}
/* Copilote du titre : question libre → /api/copilot/ask ancré sur SYM (chiffres réels). */
(function(){
  const go=$('an-cp-go'),q=$('an-cp-q'),out=$('an-cp-out');
  if(!go||!q||!out)return;
  function ask(){
    const question=(q.value||'').trim();
    if(!question){VX.toast&&VX.toast('Écris une question','warn');return;}
    out.innerHTML='<div class="vx-empty">Le copilote analyse '+SYM+'…</div>';
    fetch('/api/copilot/ask',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({question:question,symbol:SYM})})
      .then(r=>r.json()).then(d=>{
        if(!d.ok){out.innerHTML='<div class="vx-error-banner">'+esc(d.error||'réponse indisponible')+'</div>';return;}
        out.innerHTML='<div class="vx-insight" data-tone="action" style="white-space:pre-wrap;font-size:12.5px">'+esc(d.answer)+'</div>'
          +'<div class="vx-meta" style="margin-top:.3rem">'+esc(d.label||'')+'</div>';
      }).catch(e=>{out.innerHTML='<div class="vx-error-banner">Copilote injoignable : '+esc(e.message)+'</div>';});
  }
  go.addEventListener('click',ask);
  q.addEventListener('keydown',e=>{if(e.key==='Enter')ask();});
})();
/* Ticket pré-trade : montant envisagé → 7 contrôles réels via /api/pretrade/check. */
(function(){
  const go=$('an-pt-go'),amt=$('an-pt-amt'),out=$('an-pt-out');
  if(!go||!amt||!out)return;
  const ICON={ok:'✓',attention:'⚠',defavorable:'✕',inconnu:'·'};
  const CLS={ok:'vx-pos',attention:'vx-warn',defavorable:'vx-neg',inconnu:'vx-muted'};
  function run(){
    const a=Number(amt.value);
    if(!(a>0)){VX.toast&&VX.toast('Montant envisagé requis','warn');return;}
    out.innerHTML='<div class="vx-empty">Vérification de '+SYM+'…</div>';
    fetch('/api/pretrade/check',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({symbol:SYM,amount:a})})
      .then(r=>r.json()).then(d=>{
        const tone=d.tone==='ok'?'pos':d.tone==='ko'?'neg':'neutral';
        out.innerHTML='<div class="vx-flex vx-mb1" style="gap:.4rem;align-items:center">'
          +'<span class="vx-badge" data-tone="'+tone+'">'+esc(d.overall||'—')+'</span>'
          +'<span class="vx-meta">'+esc(d.symbol)+' · '+VX.fmt.num(d.amount,0)+'</span></div>'
          +'<ul style="margin:.2rem 0;padding-left:0;list-style:none;font-size:12.5px">'
          +(d.checks||[]).map(c=>'<li style="margin:.25rem 0"><span class="'+(CLS[c.status]||'vx-muted')+'" style="display:inline-block;width:16px">'+(ICON[c.status]||'·')+'</span><b>'+esc(c.label)+'</b> — '+esc(c.detail)+'</li>').join('')
          +'</ul><div class="vx-meta">'+esc(d.narrative||'')+'</div>';
      }).catch(e=>{out.innerHTML='<div class="vx-error-banner">Vérification impossible : '+esc(e.message)+'</div>';});
  }
  go.addEventListener('click',run);
  amt.addEventListener('keydown',e=>{if(e.key==='Enter')run();});
})();
async function loadAnomalies(){
  const host=$('an-anomaly');if(!host)return;
  try{
    const d=await VX.fetch('/api/anomalies/'+SYM,{ttl:120000});
    if(window.VXCharts&&VXCharts.anomalyScan)VXCharts.anomalyScan('an-anomaly',d);
    else host.innerHTML='<div class="vx-empty">Builder indisponible.</div>';
  }catch(e){host.innerHTML='<div class="vx-error-banner">Scanner injoignable : '+esc(e.message)+'</div>';}
}
/* Skyler — décision canonique : score /40 par blocs, hard gates, scénarios. */
async function loadSkyler(){
  const host=$('an-skyler');if(!host)return;
  try{
    const r=await VX.fetch('/api/skyler/'+SYM,{ttl:120000});
    const d=r&&r.decision;if(!d){host.innerHTML='<div class="vx-empty">Décision indisponible.</div>';return;}
    const tone=d.decision==='ACHETER'||d.decision==='RENFORCER'?'pos'
      :d.decision==='REFUSER'||d.decision==='REDUIRE'?'neg':'neutral';
    const sc=d.score||{},blocks=sc.blocks||{};
    const LBL={fundamentals_quality:'Fondamentaux',catalysts:'Catalyseurs',
      technical_timing:'Technique',institutions_flow_anomalies:'Flux/anomalies',
      market_regime_sector:'Régime',asymmetry_scenarios:'Asymétrie',
      options_quality:'Option',data_quality:'Données'};
    const chips=Object.keys(LBL).filter(k=>blocks[k]).map(k=>{
      const b=blocks[k];const cls=b.status==='INSUFFICIENT'?'vx-muted':(b.points>=b.max*0.66?'vx-pos':'vx-warn');
      return '<span class="vx-badge" data-tone="neutral" title="'+esc(b.basis||'')+'" style="margin:.12rem .2rem .12rem 0"><span class="'+cls+'">'+esc(LBL[k])+' '+b.points+'/'+b.max+'</span></span>';
    }).join('');
    const gates=(d.gates||[]).filter(g=>g.triggered===true);
    const unknown=(d.gates||[]).filter(g=>g.triggered===null).length;
    const sn=d.scenarios||{};
    const row=(s,lab)=>s?'<li style="margin:.2rem 0"><b>'+lab+'</b> — cible '+VX.fmt.num(s.target,2)
      +' ('+(s.return_pct>0?'+':'')+s.return_pct+' %) · probabilité : non calibrée</li>':'';
    host.innerHTML='<div class="vx-flex vx-mb1" style="gap:.45rem;align-items:center;flex-wrap:wrap">'
      +'<span class="vx-badge" data-tone="'+tone+'">'+esc(d.decision||'—')+'</span>'
      +'<b>'+(sc.total??'—')+'/40</b><span class="vx-meta">niveau '+esc(d.level||'—')
      +(d.capped_by_gate?' · plafonnée par '+esc(d.capped_by_gate):'')+'</span></div>'
      +'<div class="vx-mb1">'+chips+'</div>'
      +(gates.length?'<div class="vx-mb1">'+gates.map(g=>'<div class="vx-neg" style="font-size:12.5px">'+VX.icon('close',13)+' '+esc(g.id)+' — '+esc(g.reason)+'</div>').join('')+'</div>':'')
      +(sn.available?'<ul style="margin:.2rem 0;padding-left:0;list-style:none;font-size:12.5px">'
        +row(sn.bear,'Pessimiste')+row(sn.base,'Probable')+row(sn.bull,'Exceptionnel')+'</ul>':'')
      +'<div class="vx-meta" style="margin-top:.3rem">'
      +(d.catalyst?'Catalyseur : '+esc(d.catalyst)+' · ':'')
      +(d.invalidation!=null?'Invalidation : '+VX.fmt.num(d.invalidation,2)+' · ':'')
      +(d.max_risk_pct!=null?'Risque max : '+d.max_risk_pct+' % · ':'')
      +(unknown?unknown+' porte(s) non évaluable(s) · ':'')
      +'Objection : '+esc(d.strongest_objection||'—')+'</div>';
  }catch(e){host.innerHTML='<div class="vx-error-banner">Skyler injoignable : '+esc(e.message)+'</div>';}
}
/* Laboratoire d'évidence (X2) : stats ex post réelles après les spikes passés. */
async function loadEvidence(){
  const host=$('an-evidence');if(!host)return;
  try{
    const d=await VX.fetch('/api/evidence/'+SYM,{ttl:300000});
    if(!d||d.available===false){
      host.innerHTML='<div class="vx-empty">'+esc((d&&d.reason)||'évidence indisponible')+'.</div>';return;
    }
    if(!d.n_events){
      host.innerHTML='<div class="vx-empty">Aucun spike historique sur la fenêtre ('+d.points+' clôtures) — rien à mesurer, rien d\'inventé.</div>';return;
    }
    const fm=(v)=>v==null?'—':((v>0?'+':'')+v+' %');
    const cls=(v)=>v==null?'':v>0?'vx-pos':v<0?'vx-neg':'';
    const row=(lab,b)=>b.n_measured?'<tr><td data-label="Direction"><b>'+lab+'</b> <span class="vx-meta">×'+b.n_measured+'</span></td>'
      +'<td data-label="+1 barre" class="vx-num '+cls(b.median_fwd_1_pct)+'">'+fm(b.median_fwd_1_pct)+'</td>'
      +'<td data-label="+5 barres" class="vx-num '+cls(b.median_fwd_5_pct)+'">'+fm(b.median_fwd_5_pct)+'</td>'
      +'<td data-label="+10 barres" class="vx-num '+cls(b.median_fwd_10_pct)+'">'+fm(b.median_fwd_10_pct)+'</td>'
      +'<td data-label="MFE" class="vx-num vx-pos">'+fm(b.median_mfe_pct)+'</td>'
      +'<td data-label="MAE" class="vx-num vx-neg">'+fm(b.median_mae_pct)+'</td></tr>':'';
    host.innerHTML='<div class="vx-table-wrap"><table class="vx-table"><thead><tr>'
      +'<th>Après un spike…</th><th>+1 barre</th><th>+5 barres</th><th>+10 barres</th><th>MFE</th><th>MAE</th>'
      +'</tr></thead><tbody>'+row('haussier',d.up)+row('baissier',d.down)+'</tbody></table></div>'
      +'<div class="vx-meta" style="margin-top:.3rem">'+d.n_events+' spike(s) historique(s)'
      +(d.n_unmeasurable?' · '+d.n_unmeasurable+' trop récent(s) non mesurable(s)':'')
      +' · médianes exactes · '+esc(d.note||'')+'</div>';
  }catch(e){host.innerHTML='<div class="vx-error-banner">Évidence injoignable : '+esc(e.message)+'</div>';}
}
loadDossier();
loadDecisionStack();
loadAnomalies();
loadEvidence();
VX.refresh.register(loadEvidence,300000,'analysis-evidence');
loadSkyler();
VX.refresh.register(loadSkyler,300000,'analysis-skyler');
VX.refresh.register(loadAnomalies,300000,'analysis-anomaly');
VX.refresh.register(loadDossier,180000,'analysis');
VX.refresh.register(loadDecisionStack,180000,'analysis-decision');
})();
</script>
"""

# Barre d'actions de la fiche. Elle EMPRUNTE la fabrique d'icônes du shell,
# comme la barre mobile générique des huit espaces : cinq pictogrammes textuels
# (★ ◎ ! ◇ ⋯) y voisinaient les traits SVG du reste du produit —
# VISUAL_SYSTEM.md interdit de mélanger deux familles sur une même surface, et
# c'est ici la surface la plus dense en actions.
_MOBILE_BAR = f"""
<div class="vx-mobile-bar"><nav aria-label="Actions rapides">
  <button onclick="VXEntities.toggleFavorite('%%SYM%%')">{icon('star', 20)}<span>Favori</span></button>
  <button onclick="VXEntities.openAddModal('%%SYM%%','follow')">{icon('follow', 20)}<span>Suivre</span></button>
  <button onclick="VXEntities.openAddModal('%%SYM%%','alert')">{icon('alert', 20)}<span>Alerte</span></button>
  <button onclick="location.href='/opportunities?view=options&sym=%%SYM%%'">{icon('option', 20)}<span>Options</span></button>
  <button data-entity-menu="%%SYM%%">{icon('more', 20)}<span>Plus</span></button>
</nav></div>
"""


def render(sym: str) -> str:
    sym = sym.upper()[:8]
    safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')
    content = ('<div class="vx-page-header"><div><h1>' + safe + '</h1>'
               '<div class="vx-sub">La thèse mérite-t-elle du capital, et à quel '
               'risque.</div></div></div>'
               + _SECTIONS.replace('%%SYM%%', safe)
               .replace('%%FAVICON%%', icon('star'))
               .replace('%%CARET%%', icon('caret', 15))
               .replace('%%LOADING%%', '<div class="vx-skeleton" style="height:48px"></div>'))
    js = _JS.replace('%%SYM_JSON%%', json_for_script(safe))
    return render_shell(title=f'{safe} · Analyse', active='analysis',
                        space_label='Analyse', sub_label=safe, content=content,
                        page_js=js, page_label=f'Analyse {safe}',
                        mobile_actions=_MOBILE_BAR.replace('%%SYM%%', safe))
