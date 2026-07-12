"""vertex/ui/strategy_os.py — hub Vertex Strategy OS (§36).

Page autonome (aucune dépendance au shell du monolithe) : constitution,
décision exécutive, régime de marché, anomalies, équipe, diagnostics,
qualité de données, alertes, signaux TradingView. Donnée absente = « — »,
jamais un chiffre inventé.
"""
from __future__ import annotations


def render_page() -> str:
    return """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vertex Strategy OS</title>
<style>
:root{--bg:#080A0E;--card:#111827;--line:#1f2937;--tx:#e5e7eb;--dim:#9ca3af;
--pos:#34d399;--neg:#f87171;--warn:#fbbf24;--acc:#85609f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);
font:14px/1.5 -apple-system,'Segoe UI',Roboto,sans-serif;padding:18px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:15px;margin:0 0 10px;color:var(--acc)}
.sub{color:var(--dim);margin-bottom:18px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.kv{display:flex;justify-content:space-between;gap:10px;padding:3px 0;
border-bottom:1px dashed #1f2937}.kv:last-child{border:none}
.kv b{font-weight:600}.dim{color:var(--dim)}.pos{color:var(--pos)}
.neg{color:var(--neg)}.warn{color:var(--warn)}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:11px;
background:#1f2937;margin:2px 4px 2px 0}
input{background:#0b1220;color:var(--tx);border:1px solid var(--line);
border-radius:8px;padding:7px 10px;width:130px}
button{background:var(--acc);color:#0b1220;border:none;border-radius:8px;
padding:7px 14px;font-weight:700;cursor:pointer}
pre{white-space:pre-wrap;word-break:break-word;font-size:12px;color:var(--dim);
max-height:260px;overflow:auto;background:#0b1220;border-radius:8px;padding:10px}
a{color:var(--acc)}</style></head><body>
<h1>Vertex Strategy OS</h1>
<div class="sub">Stratégie Vertex · lecture seule — aucun ordre, jamais ·
donnée absente = « — »</div>
<div class="grid">
 <div class="card"><h2>Constitution</h2><div id="profile" class="dim">chargement…</div></div>
 <div class="card"><h2>Régime de marché</h2><div id="regime" class="dim">chargement…</div></div>
 <div class="card"><h2>Décision exécutive (moteur unique)</h2>
  <div style="margin-bottom:8px"><input id="sym" placeholder="Symbole ex. NVDA">
  <button onclick="loadDecision()">Analyser</button></div>
  <div id="decision" class="dim">entrer un symbole du scan…</div></div>
 <div class="card"><h2>Anomalies</h2>
  <div style="margin-bottom:8px"><input id="anosym" placeholder="Symbole">
  <button onclick="loadAnomalies()">Détecter</button></div>
  <div id="anomalies" class="dim">—</div></div>
 <div class="card"><h2>Équipe Vertex</h2><div id="team" class="dim">
  Le risque se calcule sur les positions réelles/simulées explicites
  (POST /api/portfolio/team). Aucun panier de scanner affiché comme portefeuille.</div></div>
 <div class="card"><h2>Alertes</h2><div id="alerts" class="dim">chargement…</div></div>
 <div class="card"><h2>Signaux TradingView</h2><div id="tv" class="dim">chargement…</div></div>
 <div class="card"><h2>Qualité des données</h2><div id="dq" class="dim">chargement…</div></div>
 <div class="card"><h2>Diagnostics système</h2><div id="diag" class="dim">chargement…</div></div>
</div>
<script>
const $=id=>document.getElementById(id);
const nd=v=>(v===null||v===undefined||v==='')?'—':v;
async function j(u,opt){try{const r=await fetch(u,opt);return await r.json()}catch(e){return null}}
function kv(k,v,cls){return '<div class="kv"><span class="dim">'+k+'</span><b class="'+(cls||'')+'">'+nd(v)+'</b></div>'}
(async()=>{
 const p=await j('/api/strategy/profile');
 $('profile').innerHTML=p?[
  kv('Stratégie',p.display_name),kv('Identifiant',p.strategy_id),
  kv('Version',p.version),kv('Style',(p.profile||{}).style),
  kv('Positions cibles',((p.profile||{}).portfolio_target_positions||{}).minimum+'–'+((p.profile||{}).portfolio_target_positions||{}).maximum),
  kv('Drawdown max',(p.profile||{}).portfolio_max_drawdown_pct+' %'),
  kv('Options simultanées max',(p.profile||{}).max_simultaneous_options),
  kv('Décisions','ACHETER · RENFORCER · ATTENDRE · REDUIRE · REFUSER')
 ].join(''):'API indisponible';
 const r=await j('/api/market/regime');
 $('regime').innerHTML=r?[
  kv('Régime',r.regime,r.regime==='PANIC'?'neg':(r.regime||'').includes('UP')?'pos':''),
  kv('Confiance',r.confidence),kv('Dimensions',(r.dimensions_used||[]).length),
  kv('Nouveau risque',(r.adjustments||{}).new_risk_allowed?'autorisé':'BLOQUÉ',
     (r.adjustments||{}).new_risk_allowed?'pos':'neg'),
  kv('Priorité setups',(r.adjustments||{}).setup_priority)
 ].join(''):'API indisponible';
 const a=await j('/api/alerts/active');
 $('alerts').innerHTML=a?((a.active||[]).length?
  a.active.map(x=>'<span class="badge">'+x.symbol+' · '+x.level+'</span>').join(''):
  'aucune alerte active')+kv('Émises',(a.status||{}).metrics?a.status.metrics.emitted:'—'):'—';
 const tv=await j('/api/tradingview/signals');
 $('tv').innerHTML=tv?((tv.signals||[]).slice(-6).map(s=>'<span class="badge">'+
  s.symbol+' · '+s.signal+'</span>').join('')||'aucun signal reçu')+
  kv('Stockés',(tv.status||{}).stored):'webhook non configuré';
 const dq=await j('/api/data-quality');
 $('dq').innerHTML=dq?[kv('Symboles',dq.total),kv('Source scan',dq.scan_source),
  ...Object.entries(dq.by_quality||{}).map(([k,v])=>kv(k,v,
   k==='FRESH'||k==='RECENT'?'pos':'warn'))].join(''):'—';
 const d=await j('/api/system/diagnostics');
 $('diag').innerHTML=d?'<pre>'+JSON.stringify(d,null,1).slice(0,2200)+'</pre>':'—';
})();
async function loadDecision(){
 const s=($('sym').value||'').trim().toUpperCase();if(!s)return;
 $('decision').textContent='analyse…';
 const d=await j('/api/strategy/decision/'+s);
 if(!d){$('decision').textContent='API indisponible';return}
 if(d.error){$('decision').innerHTML=kv('Erreur',d.error,'warn');return}
 const sc=d.scores||{};
 $('decision').innerHTML=[
  kv('Décision finale',d.final_decision,
     d.final_decision==='ACHETER'||d.final_decision==='RENFORCER'?'pos':
     d.final_decision==='REFUSER'||d.final_decision==='REDUIRE'?'neg':'warn'),
  kv('Conviction',sc.conviction),kv('Asymétrie',sc.asymmetry),
  kv('Timing',sc.timing),kv('Qualité données',sc.data_quality),
  kv('Règles bloquantes',(d.blocking_rules||[]).join(', ')||'aucune'),
  '<pre>'+(d.audit_trail||[]).join('\\n')+'</pre>'].join('');
}
async function loadAnomalies(){
 const s=($('anosym').value||'').trim().toUpperCase();if(!s)return;
 $('anomalies').textContent='détection…';
 const d=await j('/api/anomalies/'+s);
 if(!d){$('anomalies').textContent='API indisponible';return}
 $('anomalies').innerHTML=((d.anomalies||[]).map(a=>'<span class="badge">'+
  a.code+'</span>').join('')||'aucune anomalie détectée')+
  '<div class="dim" style="margin-top:6px;font-size:12px">'+nd(d.note)+'</div>';
}
</script></body></html>"""
