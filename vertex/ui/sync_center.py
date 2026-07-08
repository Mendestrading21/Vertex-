"""
vertex/ui/sync_center.py — VERTEX SYNC CENTER (global, toutes pages).

Le centre de contrôle du Live Engine, injecté dans le shell : un clic sur
« ⟳ Mettre à jour » dans le header ouvre le modal —

• mode global (Live / Delayed / Démo / Offline) + badge permanent header
• état par domaine : source, fraîcheur (« il y a X »), volume, état coloré
• boutons : Tout mettre à jour · Prix · Options · News · IA · Rapport
• LIVE MODE ON/OFF : re-scan automatique périodique + badge animé
• rapport de synchronisation après chaque refresh, erreurs expliquées

S'appuie uniquement sur /api/live/* — zéro donnée isolée, zéro duplication.
"""

JS = r"""
;(function(){
 if(window.__vxSync)return;window.__vxSync=1;
 var SC={open:false,st:null,timer:null};
 var CSS='#vxsc-ovl{position:fixed;inset:0;background:rgba(4,5,8,.78);backdrop-filter:blur(6px);z-index:200;display:none;align-items:flex-start;justify-content:center;overflow-y:auto;padding:5vh 14px}'
 +'#vxsc-ovl.on{display:flex}'
 +'#vxsc{width:100%;max-width:720px;background:linear-gradient(175deg,#13151b,#0b0d12);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:22px 24px;color:#eef2f8;font-family:Inter,system-ui,sans-serif;margin-bottom:5vh}'
 +'#vxsc h2{font-size:19px;font-weight:800;margin:0;display:flex;align-items:center;gap:10px}'
 +'#vxsc .mode{font-size:10.5px;font-weight:800;padding:4px 12px;border-radius:999px;letter-spacing:.5px}'
 +'#vxsc .row{display:grid;grid-template-columns:auto 1fr auto auto;gap:12px;align-items:center;padding:11px 2px;border-bottom:1px solid rgba(255,255,255,.06);font-size:13px}'
 +'#vxsc .row:last-child{border-bottom:0}'
 +'#vxsc .dl{font-weight:700}#vxsc .dd{font-size:10.5px;color:#8794ab;margin-top:2px}'
 +'#vxsc .fresh{font-size:11.5px;color:#aeb8c8;text-align:right;font-variant-numeric:tabular-nums}'
 +'#vxsc .st{width:9px;height:9px;border-radius:99px;justify-self:end}'
 +'#vxsc .btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,.08)}'
 +'#vxsc button{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);color:#e8edf5;border-radius:11px;font-size:12px;font-weight:700;padding:9px 14px;cursor:pointer;font-family:inherit}'
 +'#vxsc button:hover{border-color:rgba(255,122,24,.5)}'
 +'#vxsc button.pri{background:linear-gradient(135deg,#FF7A18,#FF9A3D);color:#0b0b0b;border:none;font-weight:800}'
 +'#vxsc .rep{margin-top:14px;background:#0a0c10;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:13px 15px;font-size:12.3px;line-height:1.65;color:#aeb8c8;display:none}'
 +'#vxsc .rep b{color:#eef2f8}'
 +'#vxsc .lm{display:flex;align-items:center;gap:10px;margin-left:auto;font-size:11.5px;color:#8794ab;cursor:pointer;user-select:none}'
 +'#vxsc .sw{width:38px;height:20px;border-radius:99px;background:rgba(255,255,255,.1);position:relative;transition:background .2s}'
 +'#vxsc .sw i{position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:99px;background:#8794ab;transition:left .2s,background .2s}'
 +'#vxsc .lm.on .sw{background:rgba(34,197,94,.35)}#vxsc .lm.on .sw i{left:20px;background:#22C55E}'
 +'.vx-livedot{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:800;letter-spacing:.5px;padding:3px 10px;border-radius:999px;margin-right:8px;cursor:pointer}'
 +'.vx-livedot i{width:7px;height:7px;border-radius:99px;display:inline-block}'
 +'@keyframes vxpulse{0%,100%{opacity:1}50%{opacity:.35}}.vx-livedot.live i{animation:vxpulse 1.6s infinite}';
 var el=document.createElement('style');el.textContent=CSS;document.head.appendChild(el);
 var ovl=document.createElement('div');ovl.id='vxsc-ovl';
 ovl.innerHTML='<div id="vxsc"></div>';
 ovl.addEventListener('click',function(e){if(e.target===ovl)vxSyncClose();});
 document.body.appendChild(ovl);

 var MODES={live:['LIVE','#22C55E','rgba(34,197,94,.15)'],delayed:['DELAYED ~15 min','#F5B45B','rgba(245,180,91,.15)'],
  demo:['🎭 DÉMO','#a78bfa','rgba(167,139,250,.15)'],offline:['OFFLINE','#EF4444','rgba(239,68,68,.15)']};
 var STC={ok:'#22C55E',stale:'#F5B45B',offline:'#EF4444'};

 function fmtTs(ts){if(!ts)return '—';var d=new Date(ts*1000);return d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'});}
 function liveOn(){return localStorage.getItem('vxLiveMode')==='1';}

 function render(){var s=SC.st;if(!s)return;var M=MODES[s.mode]||MODES.offline;
  var rows=Object.keys(s.domains).map(function(k){var d=s.domains[k];
   return '<div class="row"><span style="font-size:16px">'+d.icon+'</span>'
    +'<span><span class="dl">'+d.label+'</span>'+(d.count!=null?' <span style="color:#5d6673;font-size:11px">· '+d.count+'</span>':'')
    +'<div class="dd">'+d.source+' — '+d.detail+'</div></span>'
    +'<span class="fresh">'+d.freshness+'</span>'
    +'<span class="st" style="background:'+(STC[d.state]||'#8794ab')+'" title="'+d.state+'"></span></div>';}).join('');
  var errs=(s.errors||[]).map(function(e){return '<div style="color:#f0b0b0;font-size:12px;margin-top:8px">⚠️ <b>'+e.domain+'</b> : '+e.error+'</div>';}).join('');
  document.getElementById('vxsc').innerHTML=
   '<h2>🛰️ Vertex Sync Center <span class="mode" style="color:'+M[1]+';background:'+M[2]+'">'+M[0]+'</span>'
   +'<span class="lm'+(liveOn()?' on':'')+'" onclick="vxLiveToggle()" title="Re-scan automatique toutes les 2 min"><span>Live Mode</span><span class="sw"><i></i></span></span>'
   +'<span style="cursor:pointer;color:#8794ab;font-size:18px;padding:0 4px" onclick="vxSyncClose()">✕</span></h2>'
   +'<div style="font-size:11.5px;color:#8794ab;margin:6px 0 12px">Source de vérité unique — toutes les pages lisent ces domaines. Dernier refresh manuel : '+fmtTs(s.last_refresh)+'</div>'
   +rows+errs
   +'<div class="btns">'
   +'<button class="pri" onclick="vxRefresh()">⟳ Tout mettre à jour</button>'
   +'<button onclick="vxRefresh(\'prices,ai\')">📈 Prix & scores</button>'
   +'<button onclick="vxRefresh(\'options\')">💎 Options</button>'
   +'<button onclick="vxRefresh(\'news,calendar\')">📰 News & calendrier</button>'
   +'<button onclick="vxRefresh(\'ai\')">🧠 IA</button>'
   +'<button onclick="vxReport()">📋 Dernier rapport</button></div>'
   +'<div class="rep" id="vxscRep"></div>'
   +'<div style="margin-top:12px;font-size:10px;color:#4b5563">⛔ Lecture seule — le Live Engine rafraîchit des analyses, il ne transmet jamais d\'ordre. IBKR : '+(s.ibkr?'connecté (TWS)':'non connecté — repli '+(s.demo?'démo':'yfinance delayed'))+'.</div>';}

 function badge(){var s=SC.st;if(!s)return;var host=document.getElementById('gnav-fresh');if(!host)return;
  var M=MODES[s.mode]||MODES.offline;var pr=(s.domains||{}).prices||{};
  host.style.display='';host.innerHTML='<span class="vx-livedot'+(s.mode==='live'||liveOn()?' live':'')+'" onclick="vxSyncOpen()" title="Ouvrir le Sync Center" style="color:'+M[1]+';background:'+M[2]+'"><i style="background:'+M[1]+'"></i>'+M[0]+' · '+(pr.freshness||'—')+'</span>';}

 function load(cb){fetch('/api/live/status').then(function(r){return r.json();}).then(function(s){SC.st=s;badge();if(SC.open)render();if(cb)cb(s);}).catch(function(){});}

 window.vxSyncOpen=function(){SC.open=true;ovl.className='on';load();render();};
 window.vxSyncClose=function(){SC.open=false;ovl.className='';};
 window.vxRefresh=function(domains){var rep=document.getElementById('vxscRep');if(rep){rep.style.display='block';rep.innerHTML='⏳ Mise à jour lancée…';}
  fetch('/api/live/refresh'+(domains?'?domains='+domains:''),{method:'POST'}).then(function(r){return r.json();}).then(function(d){
   showReport(d.report);setTimeout(function(){load();},4000);setTimeout(function(){load();},15000);}).catch(function(){if(rep)rep.innerHTML='❌ Échec — API injoignable. Réessaie dans un instant.';});};
 window.vxReport=function(){fetch('/api/live/report').then(function(r){return r.json();}).then(showReport);};
 function showReport(rp){var rep=document.getElementById('vxscRep');if(!rep)return;rep.style.display='block';
  if(!rp||!rp.lines||!rp.lines.length){rep.innerHTML='Aucun rapport — lance une mise à jour.';return;}
  rep.innerHTML='<b>📋 Rapport de synchronisation</b> — '+fmtTs(rp.ts)+' · demandé : '+rp.requested.join(', ')
   +rp.lines.map(function(l){return '<div style="margin-top:6px">'+l.icon+' <b>'+l.label+'</b>'
    +(l.count!=null?' ('+l.count+' éléments)':'')+' — était « '+l.before+' » → '+l.action+'</div>';}).join('');}

 window.vxLiveToggle=function(){localStorage.setItem('vxLiveMode',liveOn()?'0':'1');armLive();if(SC.open)render();badge();};
 function armLive(){if(SC.timer){clearInterval(SC.timer);SC.timer=null;}
  if(liveOn()){SC.timer=setInterval(function(){if(!document.hidden)fetch('/api/live/refresh?domains=prices,ai',{method:'POST'}).catch(function(){});},120000);}}

 /* le bouton header ⟳ ouvre désormais le Sync Center (gnavRescan conservé en secours) */
 window.gnavRescan=function(){vxSyncOpen();};
 armLive();load();setInterval(function(){if(!document.hidden)load();},60000);
})();
"""

__all__ = ['JS']
