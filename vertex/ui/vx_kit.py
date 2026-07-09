"""
vertex/ui/vx_kit.py — VERTEX CONNECT KIT (tissu connectif de l'application).

Un seul module, injecté sur TOUTES les pages, qui expose `window.VX` :
- formatteurs communs (jamais undefined / null / NaN → « — »)
- lecture d'état partagée (positions / suivis / watchlist / alertes) depuis le Desk
- navigation inter-pages (fiche, options, journal, desk)
- barre d'actions contextuelle universelle (Suivre · Watchlist · Position · Alerte · Options · Fiche · Journal)
- modale réutilisable + formulaires (ajout position / alerte)
- toasts + liens contextuels (« vous détenez déjà … »)

Conventions respectées (ne rien casser côté Trading Desk) :
- positions  → localStorage `myTrades`  (schéma id/type/sym/exp/strike/right/qty/cost/added/entrySnap …)
- suivis ⭐  → localStorage `myRecos`   (via window.vxFollowStk quand présent)
- watchlist  → localStorage `myFavs`    (tableau de tickers)
- alertes    → localStorage `vxAlerts`  (nouveau — aucun système préexistant)
- sync serveur → `deskTs` + window.deskPush() quand présent
"""

CSS = r"""
.vx-abar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0}
.vx-btn{display:inline-flex;align-items:center;gap:7px;height:36px;padding:0 14px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.045);color:#dfe6f2;font:600 12.5px/1 ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;cursor:pointer;transition:background .14s,border-color .14s,transform .14s,filter .14s;white-space:nowrap}
.vx-btn .i{font-size:14px;line-height:1}
.vx-btn:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.26);transform:translateY(-1px)}
.vx-btn.pri{background:linear-gradient(180deg,#ff8a2b,#f56f0e);border-color:#ff7a18;color:#160d03;font-weight:800}
.vx-btn.pri:hover{filter:brightness(1.07)}
.vx-btn.on{background:rgba(34,197,94,.16);border-color:rgba(34,197,94,.5);color:#7ee2a4}
.vx-mini{display:inline-flex;gap:4px;align-items:center}
.vx-ic{width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center;border-radius:8px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.045);cursor:pointer;font-size:13px;transition:background .12s,border-color .12s,transform .12s;padding:0;line-height:1}
.vx-ic:hover{background:rgba(255,255,255,.1);transform:translateY(-1px)}
.vx-ic.on{background:rgba(34,197,94,.16);border-color:rgba(34,197,94,.5)}
.vx-chips{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0}
.vx-chip{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;font:600 11.5px/1.2 ui-sans-serif,system-ui,sans-serif;text-decoration:none;border:1px solid transparent}
.vx-chip.pos{background:rgba(255,122,24,.14);border-color:rgba(255,122,24,.4);color:#ffb774}
.vx-chip.fol{background:rgba(245,180,91,.13);border-color:rgba(245,180,91,.35);color:#f5c67f}
.vx-chip.wl{background:rgba(56,189,248,.12);border-color:rgba(56,189,248,.34);color:#7dd3fc}
.vx-chip.al{background:rgba(239,68,68,.12);border-color:rgba(239,68,68,.34);color:#fca5a5}
.vx-dash{color:#5c6577}
.vx-crumb{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:2px 0 14px}
.vx-back{display:inline-flex;align-items:center;gap:4px;height:32px;padding:0 13px;border-radius:9px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.045);color:#cbd4e2;font:600 12.5px/1 ui-sans-serif,system-ui,sans-serif;cursor:pointer;transition:background .13s,border-color .13s}
.vx-back:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.26)}
.vx-trail{display:flex;align-items:center;gap:8px;font:600 12px/1 ui-sans-serif,system-ui,sans-serif;flex-wrap:wrap}
.vx-trail a{color:#8794ab;text-decoration:none}
.vx-trail a:hover{color:#cbd4e2}
.vx-trail .sep{color:#4b5563}
.vx-trail .cur{color:#ff9a3d;font-weight:800}
.vx-toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(16px);background:#12151c;border:1px solid rgba(255,255,255,.16);color:#eef2f8;padding:11px 18px;border-radius:12px;font:600 13px/1.3 ui-sans-serif,system-ui,sans-serif;box-shadow:0 12px 40px rgba(0,0,0,.5);z-index:99999;opacity:0;pointer-events:none;transition:opacity .22s,transform .22s;max-width:min(92vw,420px)}
.vx-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.vx-toast.ok{border-color:rgba(34,197,94,.5)}
.vx-modal-ov{position:fixed;inset:0;background:rgba(4,6,10,.62);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;z-index:99998;padding:18px;animation:vxfade .16s ease}
@keyframes vxfade{from{opacity:0}to{opacity:1}}
.vx-modal{width:min(560px,96vw);max-height:90vh;overflow:auto;background:#0e1117;border:1px solid rgba(255,255,255,.14);border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.vx-modal-h{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid rgba(255,255,255,.08);font:800 15px/1.2 ui-sans-serif,system-ui,sans-serif;color:#f2f5fa}
.vx-x{background:none;border:none;color:#8794ab;font-size:16px;cursor:pointer;padding:4px 8px;border-radius:8px;line-height:1}
.vx-x:hover{background:rgba(255,255,255,.08);color:#fff}
.vx-modal-b{padding:18px 20px}
.vx-modal-f{display:flex;justify-content:flex-end;gap:10px;padding:14px 20px;border-top:1px solid rgba(255,255,255,.08)}
.vx-grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.vx-field{display:flex;flex-direction:column;gap:5px;margin-bottom:12px}
.vx-field>span{font:600 11px/1 ui-sans-serif,system-ui,sans-serif;color:#8794ab;letter-spacing:.4px;text-transform:uppercase}
.vx-field input,.vx-field select{height:38px;padding:0 12px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.03);color:#eef2f8;font:600 13.5px/1 ui-sans-serif,system-ui,sans-serif;outline:none;width:100%}
.vx-field input:focus,.vx-field select:focus{border-color:#ff7a18;background:rgba(255,122,24,.06)}
.vx-field input[readonly]{opacity:.7;cursor:not-allowed}
.vx-hint{font:600 12px/1.4 ui-sans-serif,system-ui,sans-serif;color:#8794ab;min-height:16px;margin-top:4px}
.vx-hint .bad{color:#ef4444}
@media(max-width:520px){.vx-grid2{grid-template-columns:1fr}.vx-abar .vx-btn{flex:1 1 auto;justify-content:center}}
"""

JS = r"""
(function(){
if(window.VX)return;
function jget(k,d){try{var v=JSON.parse(localStorage.getItem(k));return v==null?d:v;}catch(e){return d;}}
function jset(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
function touch(){try{localStorage.setItem('deskTs',String(Date.now()));if(typeof window.deskPush==='function')window.deskPush();}catch(e){}}
function up(s){return (s==null?'':String(s)).toUpperCase();}
function esc(s){return (s==null?'':String(s)).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}

/* ---------- formatage (jamais undefined / null / NaN / Infinity) ---------- */
function _n(v){if(v==null||v==='')return null;var n=typeof v==='number'?v:parseFloat(String(v).replace(',','.'));return isFinite(n)?n:null;}
var DASH='<span class="vx-dash" title="Donnee indisponible.">—</span>';
function fmtNum(v,dec){var n=_n(v);if(n==null)return DASH;return n.toLocaleString('fr-FR',{minimumFractionDigits:dec||0,maximumFractionDigits:(dec==null?2:dec)});}
function fmtPrice(v){var n=_n(v);if(n==null)return DASH;return '$'+n.toLocaleString('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2});}
function fmtPct(v,signed){var n=_n(v);if(n==null)return DASH;return (signed&&n>0?'+':'')+n.toLocaleString('fr-FR',{minimumFractionDigits:1,maximumFractionDigits:2})+'%';}
function fmtMoney(v,signed){var n=_n(v);if(n==null)return DASH;return (signed&&n>0?'+':'')+Math.round(n).toLocaleString('fr-FR')+' $';}
function fmtCap(v){var n=_n(v);if(n==null)return DASH;var a=Math.abs(n);if(a>=1e12)return '$'+(n/1e12).toFixed(2)+' T';if(a>=1e9)return '$'+(n/1e9).toFixed(1)+' Md';if(a>=1e6)return '$'+(n/1e6).toFixed(0)+' M';return '$'+Math.round(n).toLocaleString('fr-FR');}
function fmtDate(v){if(!v)return DASH;try{var d=new Date(v);if(isNaN(d.getTime()))return String(v);return d.toLocaleDateString('fr-FR',{day:'2-digit',month:'short',year:'numeric'});}catch(e){return String(v);}}

/* ---------- lecture d'etat (source de verite locale = Desk) ---------- */
function positions(){return jget('myTrades',[]);}
function follows(){return jget('myRecos',[]);}
function favs(){var a=jget('myFavs',[]);return a.map(function(x){return up(x);});}
function alerts(){return jget('vxAlerts',[]);}
function posFor(s){s=up(s);return positions().filter(function(p){return up(p.sym)===s;});}
function hasPosition(s){return posFor(s).length>0;}
function isFollowed(s){s=up(s);return follows().some(function(r){return r.kind==='STK'&&up(r.sym)===s;});}
function inWatch(s){return favs().indexOf(up(s))>=0;}
function alertsFor(s){s=up(s);return alerts().filter(function(a){return up(a.sym)===s;});}
function hasAlert(s){return alertsFor(s).length>0;}

/* ---------- navigation ---------- */
function goStock(s){location.href='/titre/'+encodeURIComponent(up(s));}
function goOptions(s){location.href='/options?t='+encodeURIComponent(up(s));}
function goJournal(s){location.href='/journal'+(s?('?t='+encodeURIComponent(up(s))):'');}
function goDesk(){location.href='/strategie';}

/* ---------- toast ---------- */
var _toastT;
function toast(msg,tone){var t=document.getElementById('vx-toast');if(!t){t=document.createElement('div');t.id='vx-toast';document.body.appendChild(t);}t.className='vx-toast '+(tone||'');t.innerHTML=msg;void t.offsetWidth;t.classList.add('show');clearTimeout(_toastT);_toastT=setTimeout(function(){t.classList.remove('show');},2600);}

/* ---------- modale reutilisable ---------- */
function closeModal(){var o=document.getElementById('vx-modal-ov');if(o&&o.parentNode)o.parentNode.removeChild(o);}
function modal(opts){
 closeModal();
 var ov=document.createElement('div');ov.id='vx-modal-ov';ov.className='vx-modal-ov';
 ov.innerHTML='<div class="vx-modal" role="dialog" aria-modal="true"><div class="vx-modal-h"><span>'+(opts.title||'')+'</span><button class="vx-x" aria-label="Fermer">✕</button></div><div class="vx-modal-b">'+(opts.body||'')+'</div><div class="vx-modal-f"><button class="vx-btn" data-x>Annuler</button><button class="vx-btn pri" data-ok>'+(opts.ok||'Valider')+'</button></div></div>';
 document.body.appendChild(ov);
 ov.addEventListener('click',function(e){if(e.target===ov)closeModal();});
 ov.querySelector('.vx-x').addEventListener('click',closeModal);
 ov.querySelector('[data-x]').addEventListener('click',closeModal);
 ov.querySelector('[data-ok]').addEventListener('click',function(){var form=ov.querySelector('.vx-modal-b');if(opts.onOk){if(opts.onOk(form)===false)return;}closeModal();});
 var f=ov.querySelector('input:not([readonly]),select,textarea');if(f)f.focus();
 return ov;
}
function val(form,name){var e=form.querySelector('[name="'+name+'"]');return e?e.value.trim():'';}
function field(label,name,v,type,ro){return '<label class="vx-field"><span>'+label+'</span><input name="'+name+'" type="'+(type||'text')+'" value="'+esc(v)+'"'+(ro?' readonly':'')+(type==='number'?' step="any"':'')+'></label>';}
function selField(label,name,opts,sel){var o=opts.map(function(x){return '<option value="'+x[0]+'"'+(x[0]===sel?' selected':'')+'>'+x[1]+'</option>';}).join('');return '<label class="vx-field"><span>'+label+'</span><select name="'+name+'">'+o+'</select></label>';}

/* ---------- journal d'evenements (myTradeLog) ---------- */
function logEvent(sym,ev,txt,tid){try{if(typeof window.tlAdd==='function'){window.tlAdd(sym,ev,txt,tid);return;}var a=jget('myTradeLog',[]);a.unshift({ts:Date.now(),d:new Date().toISOString().slice(0,10),sym:up(sym),ev:ev,txt:txt,tid:tid});jset('myTradeLog',a.slice(0,400));}catch(e){}}

/* ---------- actions ---------- */
function watch(s){s=up(s);var a=jget('myFavs',[]);var idx=-1;for(var i=0;i<a.length;i++){if(up(a[i])===s){idx=i;break;}}if(idx>=0){a.splice(idx,1);jset('myFavs',a);touch();toast('★ '+s+' retire de la watchlist');}else{a.push(s);jset('myFavs',a);touch();toast('★ '+s+' ajoute a la watchlist','ok');}refresh();}
function follow(s,spot,stop,tgt){s=up(s);if(typeof window.vxFollowStk==='function'){window.vxFollowStk(s,spot,stop,tgt);setTimeout(refresh,80);return;}var a=jget('myRecos',[]);for(var i=0;i<a.length;i++){if(a[i].kind==='STK'&&up(a[i].sym)===s){a.splice(i,1);jset('myRecos',a);touch();toast('⭐ '+s+' retire du suivi');refresh();return;}}a.push({id:Date.now(),kind:'STK',sym:s,entry_spot:spot||null,stop:stop||null,tgt:tgt||null,followed:new Date().toISOString().slice(0,10)});jset('myRecos',a);touch();toast('⭐ '+s+' suivi jusqu\'a la vente','ok');refresh();}

function addPosition(s,pre){s=up(s);pre=pre||{};
 var body='<div class="vx-grid2">'
 +field('Ticker','ticker',s,'text',true)
 +selField('Type','ptype',[['STK','Action'],['CALL','CALL'],['PUT','PUT']],pre.type||'STK')
 +field('Quantite','qty',pre.qty||'','number')
 +field("Prix d'entree",'price',pre.price!=null?pre.price:'','number')
 +field('Strike (option)','strike',pre.strike||'','number')
 +field('Echeance (option)','exp',pre.exp||'','text')
 +field('Stop','stop',pre.stop!=null?pre.stop:'','number')
 +field('Objectif','tgt',pre.tgt!=null?pre.tgt:'','number')
 +selField('Devise','ccy',[['USD','USD'],['EUR','EUR'],['CHF','CHF']],pre.ccy||'USD')
 +field('Frais','fees',pre.fees||'','number')
 +'</div>'
 +field('Strategie','strategy',pre.strategy||'','text')
 +field('Note','note',pre.note||'','text')
 +'<div class="vx-hint" id="vx-ph"></div>';
 modal({title:'➕ Ajouter une position — '+s,ok:'Ajouter',body:body,onOk:function(form){
   var type=val(form,'ptype');var qty=_n(val(form,'qty'));var price=_n(val(form,'price'));var ph=form.querySelector('#vx-ph');
   if(!qty||qty<=0){ph.innerHTML='<b class="bad">Quantite requise.</b>';return false;}
   if(price==null||price<=0){ph.innerHTML="<b class=\"bad\">Prix d'entree requis.</b>";return false;}
   var strike=_n(val(form,'strike')),exp=val(form,'exp')||null;
   if(type!=='STK'&&(!strike||!exp)){ph.innerHTML='<b class="bad">Strike et echeance requis pour une option.</b>';return false;}
   var cost=type==='STK'?qty*price:qty*price*100;
   var stop=_n(val(form,'stop')),tgt=_n(val(form,'tgt')),fees=_n(val(form,'fees'));
   var snap=(typeof window.tSnapOf==='function')?window.tSnapOf(s):{spot:price,stop:stop,tgt:tgt,date:new Date().toISOString().slice(0,10)};
   var id=Date.now();
   var entry={id:id,type:type,sym:s,exp:exp,strike:strike!=null?strike:null,right:type==='PUT'?'P':(type==='CALL'?'C':null),qty:qty,cost:cost,added:new Date().toISOString().slice(0,10),entrySnap:snap,entryPrice:price,myStop:stop,myTgt:tgt,target1:tgt,fees:fees,currency:val(form,'ccy')||'USD',strategy:val(form,'strategy')||null,note:val(form,'note')||''};
   var a=jget('myTrades',[]);a.push(entry);jset('myTrades',a);
   logEvent(s,'OPEN',(type==='STK'?'Action':type)+' '+s+(strike?' $'+strike:'')+' · '+qty+'x · investi $'+Math.round(cost),id);
   touch();toast('✓ Position '+s+' ajoutee','ok');refresh();
   if(typeof window.tRender==='function')try{window.tRender();window.tRefresh&&window.tRefresh();}catch(e){}
 }});
}

function addAlert(s,pre){s=up(s);pre=pre||{};
 var body=field('Ticker','ticker',s,'text',true)
 +'<div class="vx-grid2">'
 +selField('Condition','cond',[['above','Prix ≥'],['below','Prix ≤'],['stop','Stop touche'],['target','Objectif atteint']],pre.cond||'above')
 +field('Niveau de prix','level',pre.level!=null?pre.level:'','number')
 +'</div>'
 +field('Note','note',pre.note||'','text')
 +'<div class="vx-hint" id="vx-ah"></div>';
 modal({title:'🔔 Creer une alerte — '+s,ok:"Creer l'alerte",body:body,onOk:function(form){
   var cond=val(form,'cond');var level=_n(val(form,'level'));var ah=form.querySelector('#vx-ah');
   if(level==null||level<=0){ah.innerHTML='<b class="bad">Niveau de prix requis.</b>';return false;}
   var a=jget('vxAlerts',[]);a.push({id:Date.now(),sym:s,cond:cond,level:level,note:val(form,'note')||'',created:new Date().toISOString(),active:true});
   jset('vxAlerts',a);touch();toast('🔔 Alerte creee sur '+s,'ok');refresh();
 }});
}

/* ---------- barre d'actions contextuelle ---------- */
function btn(icon,label,onclick,cls){return '<button class="vx-btn'+(cls?' '+cls:'')+'" onclick="'+onclick+'"><span class="i">'+icon+'</span>'+label+'</button>';}
function actionBar(s,opt){s=up(s);opt=opt||{};var b=[];
 b.push(btn('⭐',isFollowed(s)?'Suivi ✓':'Suivre','VX.follow(\''+s+'\')',isFollowed(s)?'on':''));
 b.push(btn('★',inWatch(s)?'Watchlist ✓':'Watchlist','VX.watch(\''+s+'\')',inWatch(s)?'on':''));
 b.push(btn('➕',hasPosition(s)?'Position ✓':'Position','VX.addPosition(\''+s+'\')',hasPosition(s)?'on':''));
 b.push(btn('🔔',hasAlert(s)?'Alerte ✓':'Alerte','VX.addAlert(\''+s+'\')',hasAlert(s)?'on':''));
 b.push(btn('💎','Options','VX.goOptions(\''+s+'\')'));
 if(!opt.hideFiche)b.push(btn('📄','Fiche','VX.goStock(\''+s+'\')'));
 if(!opt.hideJournal)b.push(btn('📖','Journal','VX.goJournal(\''+s+'\')'));
 return '<div class="vx-abar" data-vx-sym="'+s+'"'+(opt.hideFiche?' data-hidefiche="1"':'')+(opt.hideJournal?' data-hidejournal="1"':'')+'>'+b.join('')+'</div>';
}
function miniBar(s){s=up(s);return '<span class="vx-mini" data-vx-sym="'+s+'">'
 +'<button class="vx-ic'+(isFollowed(s)?' on':'')+'" title="Suivre" onclick="event.stopPropagation();VX.follow(\''+s+'\')">⭐</button>'
 +'<button class="vx-ic'+(hasPosition(s)?' on':'')+'" title="Ajouter position" onclick="event.stopPropagation();VX.addPosition(\''+s+'\')">➕</button>'
 +'<button class="vx-ic" title="Options" onclick="event.stopPropagation();VX.goOptions(\''+s+'\')">💎</button>'
 +'<button class="vx-ic" title="Fiche" onclick="event.stopPropagation();VX.goStock(\''+s+'\')">📄</button>'
 +'</span>';}
function linkChips(s){s=up(s);var c=[];
 if(hasPosition(s)){var n=posFor(s).length;c.push('<a class="vx-chip pos" href="/strategie">📌 Vous detenez '+s+(n>1?(' ('+n+')'):'')+' — voir position</a>');}
 if(isFollowed(s))c.push('<span class="vx-chip fol">⭐ '+s+' suivi</span>');
 if(inWatch(s))c.push('<span class="vx-chip wl">★ dans la watchlist</span>');
 if(hasAlert(s))c.push('<span class="vx-chip al">🔔 '+alertsFor(s).length+' alerte(s)</span>');
 return c.length?('<div class="vx-chips">'+c.join('')+'</div>'):'';}

/* re-render des barres/chips presents apres une action */
function refresh(){var bars=document.querySelectorAll('.vx-abar[data-vx-sym]');for(var i=0;i<bars.length;i++){var el=bars[i];var s=el.getAttribute('data-vx-sym');el.outerHTML=actionBar(s,{hideFiche:el.getAttribute('data-hidefiche')==='1',hideJournal:el.getAttribute('data-hidejournal')==='1'});}
 var chips=document.querySelectorAll('[data-vx-chips]');for(var k=0;k<chips.length;k++){chips[k].innerHTML=linkChips(chips[k].getAttribute('data-vx-chips'));}}

/* ---------- fil d'ariane + retour intelligent (point 17) ---------- */
var CRUMB={'':'Accueil','titre':'Stock Info','company':'Stock Info','stocks':'Stock Info','options':'Options Lab','strategie':'Trading Desk','journal':'Trade Journal','suivi':'Suivi','sectors':'Market Rotation','catalysts':'Market Calendar','anomalies':'Market Signals','vault':'Archive Vault','settings':'Reglages','compare':'Comparateur'};
function goBack(){if(history.length>1&&document.referrer&&document.referrer.indexOf(location.host)>=0){history.back();}else{location.href='/';}}
function breadcrumb(host){var parts=location.pathname.split('/').filter(function(x){return x;});var seg=parts[0]||'';var label=CRUMB[seg]||(seg?seg.charAt(0).toUpperCase()+seg.slice(1):'Accueil');
 var sym=host&&host.getAttribute('data-sym');if(!sym&&parts.length>1&&/^[A-Z.\-]{1,8}$/i.test(parts[1]))sym=parts[1].toUpperCase();
 var h='<div class="vx-crumb"><button class="vx-back" onclick="VX.goBack()">‹ Retour</button><nav class="vx-trail"><a href="/">Accueil</a>';
 if(seg&&label!=='Accueil')h+='<span class="sep">›</span><a href="/'+seg+'">'+label+'</a>';
 if(sym)h+='<span class="sep">›</span><span class="cur">'+sym+'</span>';
 h+='</nav></div>';return h;}

/* auto-init : remplit les conteneurs declaratifs [data-vx-actions] / [data-vx-chips] */
function initAuto(){var hosts=document.querySelectorAll('[data-vx-actions]');for(var i=0;i<hosts.length;i++){var h=hosts[i];if(h.__vx)continue;h.__vx=1;h.innerHTML=actionBar(h.getAttribute('data-vx-actions'),{hideFiche:h.hasAttribute('data-hidefiche'),hideJournal:h.hasAttribute('data-hidejournal')});}
 var ch=document.querySelectorAll('[data-vx-chips]');for(var j=0;j<ch.length;j++){if(!ch[j].__vx){ch[j].__vx=1;ch[j].innerHTML=linkChips(ch[j].getAttribute('data-vx-chips'));}}
 var cb=document.querySelectorAll('[data-vx-crumb]');for(var m=0;m<cb.length;m++){if(!cb[m].__vx){cb[m].__vx=1;cb[m].innerHTML=breadcrumb(cb[m]);}}}
if(document.readyState!=='loading')initAuto();else document.addEventListener('DOMContentLoaded',initAuto);
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});

window.VX={fmtNum:fmtNum,fmtPrice:fmtPrice,fmtPct:fmtPct,fmtMoney:fmtMoney,fmtCap:fmtCap,fmtDate:fmtDate,DASH:DASH,
 positions:positions,follows:follows,favs:favs,alerts:alerts,hasPosition:hasPosition,isFollowed:isFollowed,inWatch:inWatch,hasAlert:hasAlert,posFor:posFor,alertsFor:alertsFor,
 goStock:goStock,goOptions:goOptions,goJournal:goJournal,goDesk:goDesk,
 toast:toast,modal:modal,closeModal:closeModal,
 watch:watch,follow:follow,addPosition:addPosition,addAlert:addAlert,logEvent:logEvent,
 actionBar:actionBar,miniBar:miniBar,linkChips:linkChips,breadcrumb:breadcrumb,goBack:goBack,refresh:refresh,init:initAuto};
})();
"""
