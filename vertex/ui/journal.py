"""
vertex/ui/journal.py — TRADE JOURNAL 2.0 : le cerveau de Vertex.

Le journal n'est plus un formulaire : c'est un système vivant qui apprend de
chaque trade. Tout est calculé côté client depuis les entrées (localStorage
`vxJournal`, synchronisé entre appareils via /api/desk) :

• header de 18 statistiques animées (win rate, profit factor, expectancy,
  Sharpe, Sortino, drawdown, R moyen, streaks, période en cours…)
• Coach Vertex : forces, faiblesses, quoi arrêter/renforcer, objectifs,
  niveau global — recalculé après chaque trade
• dashboard : courbe d'équité, drawdown, win rate & profit factor glissants,
  P&L mensuel
• calendrier-heatmap cliquable (6 mois), analyses par jour/type/direction/
  émotion/ticker, base de connaissances des erreurs (occurrences, coût,
  solution IA), fiche détaillée par trade (score IA /100, timeline,
  trades similaires, recommandations), gamification (XP, niveau, badges,
  missions) et roadmap de progression.

La saisie reste minimale : les clôtures du Desk arrivent toutes seules ;
le trader ne complète que l'émotion, l'erreur et la leçon.

⛔ Analyse uniquement — le journal observe, il ne passe jamais d'ordre.
"""

CSS = r"""
#tj{--acc:#ff7a18;--acc2:#ff9a3d;--good:#22c55e;--bad:#ef4444;--info:#38bdf8;--warn:#f5b45b;--vio:#a78bfa;
 --ink:#eef2f8;--ink2:#aeb8c8;--mut:#8794ab;--faint:#4b5563;--surf:#101218;--bg2:#0b0d12;
 --hair:rgba(255,255,255,.07);--hair2:rgba(255,255,255,.12);
 --mono:ui-monospace,'SF Mono','JetBrains Mono',Menlo,monospace;
 --sp:clamp(40px,5vw,62px);color:var(--ink);display:block}
#tj .num{font-variant-numeric:tabular-nums lining-nums}
#tj .up{color:var(--good)}#tj .dn{color:var(--bad)}
#tj section{padding:var(--sp) 0 0}
#tj .eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:12px}
#tj .eyebrow .rn{font-family:var(--mono);color:var(--faint);letter-spacing:0}
#tj .eyebrow::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,rgba(255,122,24,.35),transparent)}
#tj h2{font-size:clamp(20px,2.4vw,26px);font-weight:800;letter-spacing:-.02em;margin:0 0 6px}
#tj .sub{color:var(--mut);font-size:13px;max-width:72ch;margin-bottom:20px}
#tj .panel{background:linear-gradient(170deg,var(--surf),var(--bg2));border:1px solid var(--hair);border-radius:18px;padding:20px 22px}
#tj .aiq{display:flex;gap:12px;align-items:flex-start;margin-top:16px;padding:13px 16px;background:linear-gradient(120deg,rgba(255,122,24,.09),rgba(255,122,24,.02));border:1px solid rgba(255,122,24,.16);border-left:2.5px solid var(--acc);border-radius:13px;font-size:13px;line-height:1.6;color:var(--ink2)}
#tj .aiq b{color:var(--ink)}
#tj .aiq .ico{flex:none;width:22px;height:22px;border-radius:7px;background:rgba(255,122,24,.16);display:grid;place-items:center;font-size:12px;margin-top:1px}
#tj .lbl{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
#tj .pill{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;font-weight:800;padding:3px 10px;border-radius:999px;letter-spacing:.3px}
#tj .p-good{background:rgba(34,197,94,.13);color:var(--good)}
#tj .p-bad{background:rgba(239,68,68,.13);color:var(--bad)}
#tj .p-warn{background:rgba(245,180,91,.13);color:var(--warn)}
#tj .p-info{background:rgba(56,189,248,.13);color:var(--info)}
#tj .p-vio{background:rgba(167,139,250,.14);color:var(--vio)}
#tj .p-mut{background:rgba(255,255,255,.06);color:var(--mut)}
/* header stats */
#tj .met{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:0;border:1px solid var(--hair);border-radius:16px;overflow:hidden;background:var(--bg2)}
#tj .met>div{padding:13px 15px;border-right:1px solid var(--hair);border-bottom:1px solid var(--hair)}
#tj .met .v{font-size:19px;font-weight:800;margin-top:4px;font-variant-numeric:tabular-nums}
#tj .met .s{font-size:9.5px;color:var(--faint);margin-top:2px}
/* coach */
#tj .coach{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:6px}
#tj .coach .c{background:var(--bg2);border:1px solid var(--hair);border-radius:14px;padding:14px 16px}
#tj .coach .c .t{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}
#tj .coach .c li{font-size:12.3px;color:var(--ink2);line-height:1.55;margin:0 0 6px 2px;list-style:none}
#tj .coach .c ul{margin:0;padding:0}
#tj .lvl{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
#tj .lvl .big{font-size:38px;font-weight:900;letter-spacing:-.02em}
#tj .xpbar{flex:1;min-width:160px;height:8px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden}
#tj .xpbar i{display:block;height:100%;background:linear-gradient(90deg,var(--acc),var(--acc2));border-radius:99px;transition:width .8s ease}
#tj .badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
#tj .badge{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;padding:6px 12px;border-radius:999px;background:var(--bg2);border:1px solid var(--hair2);color:var(--ink2)}
#tj .badge.off{opacity:.32;filter:grayscale(1)}
/* charts */
#tj .vgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
#tj .chart{background:var(--bg2);border:1px solid var(--hair);border-radius:15px;padding:14px 14px 8px}
#tj .chart .q{font-size:12.5px;font-weight:700}
#tj .chart .a{font-size:10.5px;color:var(--mut);margin:2px 0 8px}
#tj canvas{width:100%;height:170px;display:block}
/* calendrier */
#tj .cal{display:grid;grid-template-rows:repeat(7,14px);grid-auto-flow:column;grid-auto-columns:14px;gap:3px;overflow-x:auto;padding:4px 2px 8px}
#tj .cal i{border-radius:3.5px;background:rgba(255,255,255,.05);cursor:pointer;transition:transform .1s}
#tj .cal i:hover{transform:scale(1.35)}
/* tables */
#tj table{width:100%;border-collapse:collapse;font-size:12.4px}
#tj th{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);font-weight:800;padding:8px 9px;border-bottom:1px solid var(--hair2);white-space:nowrap}
#tj td{padding:9px 9px;border-bottom:1px solid var(--hair);vertical-align:top}
#tj tr:last-child td{border-bottom:0}
#tj tbody tr:hover{background:rgba(255,255,255,.025)}
#tj .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
#tj .angrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
#tj .sbar{height:5px;border-radius:99px;background:rgba(255,255,255,.06);overflow:hidden;min-width:46px}
#tj .sbar i{display:block;height:100%;border-radius:99px}
/* saisie */
#tj .form{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
#tj .jf{width:100%;background:#0b0c10;border:1px solid var(--hair2);border-radius:10px;color:var(--ink);font-size:13px;padding:9px 11px;outline:none;font-family:inherit}
#tj .jf:focus{border-color:rgba(255,122,24,.5)}
#tj textarea.jf{min-height:56px;resize:vertical}
#tj .jfield label{display:block;font-size:9.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin:0 0 5px}
#tj .jchip{background:rgba(255,255,255,.04);border:1px solid var(--hair2);color:var(--ink2);border-radius:999px;font-size:12px;font-weight:600;padding:6px 12px;cursor:pointer}
#tj .jchip.on{background:rgba(255,122,24,.15);border-color:rgba(255,122,24,.5);color:var(--acc2)}
#tj .tog{display:flex;gap:8px}
#tj .tog button{flex:1;background:rgba(255,255,255,.04);border:1px solid var(--hair2);color:var(--ink2);border-radius:10px;font-size:12.5px;font-weight:700;padding:9px;cursor:pointer}
#tj .tog .onL{background:rgba(34,197,94,.15);border-color:rgba(34,197,94,.5);color:var(--good)}
#tj .tog .onS{background:rgba(239,68,68,.15);border-color:rgba(239,68,68,.5);color:var(--bad)}
/* liste des trades */
#tj .trow{display:grid;grid-template-columns:auto 1fr auto;gap:6px 14px;padding:12px 14px;border:1px solid var(--hair);border-radius:13px;background:var(--bg2);margin-bottom:9px;cursor:pointer;transition:border-color .15s,transform .12s}
#tj .trow:hover{border-color:rgba(255,122,24,.4);transform:translateY(-1px)}
#tj .trow .tk{font-size:15px;font-weight:900}
#tj .trow .meta{font-size:11px;color:var(--mut)}
#tj .todo{border:1px dashed rgba(245,180,91,.5);border-radius:13px;padding:11px 14px;margin-bottom:9px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;background:rgba(245,180,91,.04)}
/* fiche (overlay) */
#tj .ovl{position:fixed;inset:0;background:rgba(4,5,8,.78);backdrop-filter:blur(6px);z-index:90;display:none;align-items:flex-start;justify-content:center;overflow-y:auto;padding:4vh 14px}
#tj .ovl.on{display:flex}
#tj .fiche{width:100%;max-width:860px;background:linear-gradient(175deg,#13151b,#0b0d12);border:1px solid var(--hair2);border-radius:20px;padding:24px 26px;margin-bottom:6vh}
#tj .fscore{font-size:42px;font-weight:900;line-height:1}
#tj .ftl{position:relative;padding-left:24px;margin-top:8px}
#tj .ftl::before{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:2px;background:linear-gradient(180deg,rgba(255,122,24,.5),rgba(255,255,255,.06))}
#tj .ftl>div{position:relative;padding-bottom:13px;font-size:12.5px;color:var(--ink2)}
#tj .ftl>div::before{content:"";position:absolute;left:-21px;top:4px;width:9px;height:9px;border-radius:99px;background:#16181f;border:2px solid var(--faint)}
#tj .simrow{display:grid;grid-template-columns:1fr auto auto auto;gap:10px;font-size:12px;padding:8px 0;border-bottom:1px solid var(--hair)}
/* roadmap */
#tj .road{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px}
#tj .road>div{background:var(--bg2);border:1px solid var(--hair);border-radius:12px;padding:11px 10px;text-align:center;transition:border-color .15s}
#tj .road>div:hover{border-color:rgba(255,122,24,.45)}
#tj .road .i{font-size:18px}
#tj .road .t{font-size:10.5px;font-weight:800;margin-top:5px}
#tj .road .s{font-size:9px;color:var(--faint);margin-top:2px}
#tj .missions{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:14px}
#tj .mission{background:var(--bg2);border:1px solid var(--hair);border-radius:13px;padding:12px 14px;font-size:12.3px;color:var(--ink2)}
#tj .mission b{color:var(--ink);display:block;margin-bottom:3px;font-size:12.5px}
#tj .foot{margin-top:40px;padding-top:13px;border-top:1px solid var(--hair);font-size:11px;color:var(--faint);line-height:1.6}
#tj .empty{padding:28px;text-align:center;color:var(--mut);font-size:13px;background:var(--bg2);border:1px dashed var(--hair2);border-radius:14px}
@media(max-width:900px){#tj .vgrid,#tj .form{grid-template-columns:1fr}}
"""

BODY = (
  '<div id="tj">'
  '<div class="vhead"><div><h1>📖 Trade Journal</h1>'
  '<div class="s">Le cerveau de Vertex — chaque trade nourrit les statistiques, le coach et ta progression · '
  '🤖 les clôtures du Desk arrivent toutes seules · ☁️ synchronisé</div></div>'
  '<div style="margin-left:auto;align-self:center;display:flex;gap:8px">'
  '<button class="vbtn" onclick="jExport()">⬇ Export</button>'
  '<button class="vbtn" onclick="jImport()">⬆ Import</button></div></div>'
  '<div id="tjRoot"></div>'
  '<div class="ovl" id="tjOvl" onclick="if(event.target===this)tjClose()"><div class="fiche" id="tjFiche"></div></div>'
  '</div>')

JS = r"""
/* ═══════════ données & sync (schéma vxJournal conservé) ═══════════ */
var EMO=[['😌','Calme'],['🎯','Concentré'],['😰','Stressé'],['🤑','Avide'],['😐','Neutre'],['😤','Revanche']];
var EMOIC={Calme:'😌',Concentré:'🎯',Stressé:'😰',Avide:'🤑',Neutre:'😐',Revanche:'😤'};
var FORM={dir:'',res:'',emo:''};var JF={res:'',q:'',day:''};
function jGet(){try{return JSON.parse(localStorage.getItem('vxJournal')||'[]')}catch(e){return[]}}
function jSet(a){localStorage.setItem('vxJournal',JSON.stringify(a));localStorage.setItem('deskTs',String(Date.now()));jvSyncPush();}
function jvSyncPush(){try{fetch('/api/desk').then(function(r){return r.json()}).then(function(d){var data=(d&&d.data)||{};data.vxJournal=localStorage.getItem('vxJournal');['myTrades','myTradesClosed','myTradesEquity','myRecos','myRecosClosed','myCapital','simCash','simStart','simTrades','simClosed','myFavs','myNotes','vxJournal','myTradeLog','vxVault'].forEach(function(k){var v=localStorage.getItem(k);if(v!=null)data[k]=v;});fetch('/api/desk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ts:Date.now(),data:data})});}).catch(function(){});}catch(e){}}
function jvSyncPull(cb){try{fetch('/api/desk').then(function(r){return r.json()}).then(function(d){if(d&&d.data&&d.data.vxJournal){var lt=parseFloat(localStorage.getItem('deskTs')||'0');if((d.ts||0)>lt||!jGet().length){localStorage.setItem('vxJournal',d.data.vxJournal);if(d.data.myTradeLog)localStorage.setItem('myTradeLog',d.data.myTradeLog);localStorage.setItem('deskTs',String(d.ts||Date.now()));}}if(cb)cb();}).catch(function(){if(cb)cb();});}catch(e){if(cb)cb();}}
function $n2(x,d){return x==null||isNaN(x)?'—':Number(x).toLocaleString('fr-FR',{maximumFractionDigits:d==null?0:d});}
function money(x){return x==null||isNaN(x)?'—':((x>=0?'+':'−')+'$'+Math.abs(x).toLocaleString('fr-FR',{maximumFractionDigits:0}));}
function scol2(v,a,b){return v==null?'#8794ab':v>=(a==null?60:a)?'#22c55e':v>=(b==null?40:b)?'#f5b45b':'#ef4444';}
function rMult(t){var e=+t.entry,s=+t.stop,x=+t.exit;if(!e||!s||!x||e===s)return null;var r=(t.dir==='SHORT')?(e-x)/(s-e):(x-e)/(e-s);return isFinite(r)?r:null;}
function pnlOf(t){var v=+t.pnl;return isNaN(v)?null:v;}
function closedOf(a){return a.filter(function(t){return t.result;});}

/* ═══════════ score IA d'un trade (/100, expliqué) ═══════════ */
function aiScore(t){var s=50,why=[];
 var hasPlan=t.entry&&t.stop&&t.tp;
 if(hasPlan){s+=12;why.push(['+12','plan complet écrit (entrée/stop/objectif)']);}else{why.push(['—','plan incomplet : pas de score d\'entrée possible']);s-=8;}
 var e=+t.entry,st=+t.stop,tp=+t.tp;var rrp=(e&&st&&tp&&e!==st)?Math.abs(tp-e)/Math.abs(e-st):null;
 if(rrp!=null){if(rrp>=2){s+=10;why.push(['+10','R:R planifié '+rrp.toFixed(1)+' ≥ 2']);}else if(rrp<1){s-=8;why.push(['−8','R:R planifié '+rrp.toFixed(1)+' < 1 — trade structurellement perdant']);}}
 var rm=rMult(t);
 if(rm!=null){if(rm>=1){s+=8;why.push(['+8','sortie à '+rm.toFixed(1)+'R — le plan a payé']);}else if(rm<=-1.2){s-=10;why.push(['−10','perte '+rm.toFixed(1)+'R — stop dépassé ou déplacé']);}}
 if(t.disc){var d=+t.disc;if(d>=7){s+=8;why.push(['+8','discipline '+d+'/10']);}else if(d<=4){s-=8;why.push(['−8','discipline '+d+'/10']);}}
 if(t.emo==='Calme'||t.emo==='Concentré'){s+=7;why.push(['+7','état émotionnel sain ('+t.emo+')']);}
 if(t.emo==='Revanche'||t.emo==='Avide'){s-=12;why.push(['−12','émotion toxique ('+t.emo+')']);}
 if(t.trigger){s-=7;why.push(['−7','déclencheur d\'erreur : '+t.trigger]);}
 if(t.lesson){s+=6;why.push(['+6','leçon consignée — le trade enrichit la base']);}
 if(t.mistake){why.push(['·','erreur identifiée : "'+t.mistake+'" (bien vu — c\'est comme ça qu\'on progresse)']);}
 if(t.result==='WIN')s+=4;
 return {score:Math.max(5,Math.min(98,Math.round(s))),why:why};}

/* ═══════════ métriques globales ═══════════ */
function stats(a){var c=closedOf(a),n=c.length;
 var wins=c.filter(function(t){return t.result==='WIN';}),losses=c.filter(function(t){return t.result==='LOSS';});
 var pnls=c.map(pnlOf).filter(function(v){return v!=null;});
 var sumW=wins.reduce(function(s,t){return s+(pnlOf(t)||0);},0),sumL=losses.reduce(function(s,t){return s+Math.abs(pnlOf(t)||0);},0);
 var pnl=pnls.reduce(function(s,v){return s+v;},0);
 var mean=pnls.length?pnl/pnls.length:0;
 var sd=pnls.length>1?Math.sqrt(pnls.reduce(function(s,v){return s+(v-mean)*(v-mean);},0)/(pnls.length-1)):0;
 var dneg=pnls.filter(function(v){return v<0;});
 var sdd=dneg.length?Math.sqrt(dneg.reduce(function(s,v){return s+v*v;},0)/dneg.length):0;
 var cum=0,pk=0,dd=0;c.slice().reverse().forEach(function(t){cum+=(pnlOf(t)||0);if(cum>pk)pk=cum;if(pk-cum>dd)dd=pk-cum;});
 var rs=c.map(rMult).filter(function(v){return v!=null;});
 var ds=a.map(function(t){return +t.disc;}).filter(function(v){return v>0;});
 var ais=a.map(function(t){return aiScore(t).score;});
 /* streaks */
 var cur=0,best=0,worst=0,run=0;c.slice().reverse().forEach(function(t){if(t.result==='WIN'){run=run>0?run+1:1;if(run>best)best=run;}else{run=run<0?run-1:-1;if(run<worst)worst=run;}});cur=run;
 /* périodes */
 var now=new Date(),iso=function(d){return d.toISOString().slice(0,10);},today=iso(now);
 var wk=new Date(now);wk.setDate(now.getDate()-((now.getDay()+6)%7));var mo=today.slice(0,7);
 var per=function(f){return c.filter(f).reduce(function(s,t){return s+(pnlOf(t)||0);},0);};
 /* durée de détention (auto trades : added→closed) */
 var holds=c.map(function(t){if(t.added&&t.date){var d=(new Date(t.date)-new Date(t.added))/86400000;return d>=0?d:null;}return null;}).filter(function(v){return v!=null;});
 return {total:a.length,n:n,nwin:wins.length,nloss:losses.length,
  wr:n?Math.round(wins.length/n*100):null,
  pf:sumL>0?sumW/sumL:(sumW>0?99:null),exp:n?pnl/n:null,pnl:pnl,
  sharpe:(sd>0&&pnls.length>4)?mean/sd*Math.sqrt(252/Math.max(pnls.length,1))*Math.sqrt(pnls.length/252):null,
  sharpeRaw:sd>0?mean/sd:null,sortino:sdd>0?mean/sdd:null,maxdd:dd,
  avgW:wins.length?sumW/wins.length:null,avgL:losses.length?sumL/losses.length:null,
  avgR:rs.length?rs.reduce(function(s,v){return s+v;},0)/rs.length:null,
  avgHold:holds.length?holds.reduce(function(s,v){return s+v;},0)/holds.length:null,
  disc:ds.length?ds.reduce(function(s,v){return s+v;},0)/ds.length:null,
  ai:ais.length?Math.round(ais.reduce(function(s,v){return s+v;},0)/ais.length):null,
  stCur:cur,stBest:best,stWorst:worst,
  pDay:per(function(t){return t.date===today;}),pWeek:per(function(t){return t.date>=iso(wk);}),pMonth:per(function(t){return (t.date||'').slice(0,7)===mo;})};}

/* ═══════════ groupements (analyses par dimension) ═══════════ */
function groupBy(a,keyf){var by={};closedOf(a).forEach(function(t){var k=keyf(t);if(!k)return;(by[k]=by[k]||[]).push(t);});
 return Object.keys(by).map(function(k){var g=by[k],w=g.filter(function(t){return t.result==='WIN';}).length,p=g.reduce(function(s,t){return s+(pnlOf(t)||0);},0);
  return {k:k,n:g.length,wr:Math.round(w/g.length*100),pnl:p,exp:p/g.length};}).sort(function(x,y){return y.pnl-x.pnl;});}
var DAYS=['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'];

/* ═══════════ base de connaissances des erreurs ═══════════ */
var FIXES=[[/stop/i,'Écris le stop AVANT l\'entrée et traite-le comme un contrat : le déplacer = clôturer immédiatement.'],
 [/fomo|chass|tard/i,'Règle des 2 minutes : si le mouvement est déjà parti, il repartira — attendre le repli vers la moyenne.'],
 [/revanche|revenge/i,'Après une perte : pause obligatoire de 30 min et taille divisée par 2 sur le trade suivant.'],
 [/taille|sizing|gros/i,'La taille EST le stop : risque fixe de 1 % du capital, calculé avant l\'entrée, jamais pendant.'],
 [/t[ôo]t|early|press/i,'Attendre la clôture de la bougie de signal — une entrée précoce est un pari, pas un setup.'],
 [/plan/i,'Pas de plan écrit = pas de trade. La checklist des 4 étapes prend 90 secondes.'],
 [/sur.?trad|over/i,'Quota dur : 3 trades/jour maximum. Le 4ᵉ est statistiquement ton pire.'],
 [/confian|euphor/i,'Après 3 gains d\'affilée, réduire la taille de moitié : l\'euphorie précède la donation.']];
function fixFor(txt){for(var i=0;i<FIXES.length;i++){if(FIXES[i][0].test(txt))return FIXES[i][1];}
 return 'Nomme le contexte exact de cette erreur dans la leçon — la répétition vit dans les détails.';}
function mistakes(a){var by={};a.forEach(function(t){var m=(t.mistake||t.trigger||'').trim();if(!m)return;var k=m.toLowerCase().slice(0,40);
 if(!by[k])by[k]={label:m,n:0,cost:0,costR:0,last:''};var e=by[k];e.n++;var p=pnlOf(t);if(p!=null&&p<0)e.cost+=p;var r=rMult(t);if(r!=null&&r<0)e.costR+=r;if((t.date||'')>e.last)e.last=t.date||'';});
 return Object.keys(by).map(function(k){return by[k];}).sort(function(x,y){return x.cost-y.cost;});}

/* ═══════════ gamification ═══════════ */
function gamify(a,m){var xp=0;
 xp+=a.length*10;xp+=a.filter(function(t){return t.lesson;}).length*15;xp+=a.filter(function(t){return t.mistake;}).length*10;
 xp+=(m.nwin||0)*5;xp+=Math.max(0,m.stBest)*8;if(m.disc>=7)xp+=40;
 var lvl=1,need=100,rest=xp;while(rest>=need){rest-=need;lvl++;need=Math.round(need*1.35);}
 var names=['Débutant','Apprenti','Régulier','Discipliné','Méthodique','Opérateur','Stratège','Quant','Maître du risque','Hedge fund'];
 var badges=[
  ['📓','Premier trade',a.length>=1],['🔟','10 trades journalisés',a.length>=10],['💯','30 trades journalisés',a.length>=30],
  ['💡','Première leçon',a.some(function(t){return t.lesson;})],['🧠','10 leçons',a.filter(function(t){return t.lesson;}).length>=10],
  ['🎯','3 gains d\'affilée',m.stBest>=3],['🔥','5 gains d\'affilée',m.stBest>=5],
  ['🧭','Discipline ≥ 7',(m.disc||0)>=7],['⚖️','Profit factor ≥ 1.5',(m.pf||0)>=1.5],
  ['🛡️','Aucune émotion toxique (10 derniers)',a.slice(0,10).length>=5&&!a.slice(0,10).some(function(t){return t.emo==='Revanche'||t.emo==='Avide';})],
  ['🤖','Auto-journalisation active',a.some(function(t){return t.auto;})],['📈','R moyen positif',(m.avgR||0)>0]];
 return {xp:xp,lvl:lvl,name:names[Math.min(lvl-1,names.length-1)],pct:Math.round(rest/need*100),badges:badges};}

/* ═══════════ Coach Vertex ═══════════ */
function coach(a,m){if(m.n<3)return null;
 var byE=groupBy(a,function(t){return t.emo;}),byT=groupBy(a,function(t){return t.ticker;}),byD=groupBy(a,function(t){return t.dir;});
 var mk=mistakes(a);
 var bestE=byE[0],worstE=byE[byE.length-1],bestT=byT[0],worstT=byT[byT.length-1];
 var forces=[],faibl=[],stop=[],renf=[];
 if((m.wr||0)>=50)forces.push('Win rate '+m.wr+'% — ta sélection de setups est saine.');
 if((m.avgR||0)>0)forces.push('R moyen +'+m.avgR.toFixed(2)+'R — tes gains paient tes pertes.');
 if(bestE&&bestE.pnl>0)forces.push('État "'+bestE.k+'" : '+money(bestE.pnl)+' — ton meilleur terrain mental.');
 if(bestT&&bestT.pnl>0)forces.push(bestT.k+' est ton titre le plus rentable ('+money(bestT.pnl)+' sur '+bestT.n+' trades).');
 if(!forces.length)forces.push('Encore trop peu de données — chaque trade journalisé affine ce diagnostic.');
 if((m.pf||0)<1&&m.n>=5)faibl.push('Profit factor '+(m.pf==null?'—':m.pf.toFixed(2))+' < 1 : les pertes dominent — coupe-les plus vite.');
 if((m.avgL||0)>(m.avgW||0)&&m.nloss>0)faibl.push('Perte moyenne ('+money(-m.avgL)+') > gain moyen ('+money(m.avgW)+') — asymétrie inversée.');
 if(worstE&&worstE.pnl<0)faibl.push('État "'+worstE.k+'" : '+money(worstE.pnl)+' — ton terrain le plus coûteux.');
 if(mk[0])faibl.push('Erreur dominante : « '+mk[0].label+' » ('+mk[0].n+'×, '+money(mk[0].cost)+').');
 if(!faibl.length)faibl.push('Aucune fuite majeure détectée sur l\'échantillon actuel.');
 if(mk[0])stop.push(fixFor(mk[0].label));
 if(worstE&&worstE.pnl<0&&(worstE.k==='Revanche'||worstE.k==='Avide'||worstE.k==='Stressé'))stop.push('Ne plus trader en état "'+worstE.k+'" — ça t\'a coûté '+money(worstE.pnl)+'.');
 if(!stop.length)stop.push('Rien d\'urgent à arrêter — maintiens la routine.');
 if(bestE)renf.push('Provoquer l\'état "'+bestE.k+'" avant chaque session (routine, checklist, pause).');
 if((m.avgR||0)>=0.5)renf.push('Laisser courir davantage : vise TP2 sur la moitié de la position.');
 renf.push('Journaliser la leçon À CHAUD — ta base d\'erreurs est ta vraie edge.');
 var goal_d='Demain : 1 seul setup A+, risque ≤ 1 %, plan écrit avant l\'entrée.';
 var goal_w='Cette semaine : zéro trade en émotion toxique'+(mk[0]?' et zéro « '+mk[0].label+' »':'')+'.';
 var lvl=(m.ai||50);
 return {forces:forces,faibl:faibl,stop:stop,renf:renf,goalD:goal_d,goalW:goal_w,
  bestSetup:bestE?('"'+bestE.k+'" · '+(bestT?bestT.k:'')):null,worstSetup:worstE?'"'+worstE.k+'"':null,
  err:mk[0]?mk[0].label:null,note:lvl,
  resume:'Sur '+m.n+' trades clôturés : win rate '+(m.wr==null?'—':m.wr+'%')+', profit factor '+(m.pf==null?'—':(m.pf>=99?'∞':m.pf.toFixed(2)))+', expectancy '+money(m.exp)+'/trade. '
   +((m.pf||0)>=1.5?'La machine tourne — protège le processus, pas le P&L.':(m.pf||0)>=1?'Le système est à l\'équilibre — la prochaine marche passe par la réduction de l\'erreur dominante.':'Priorité absolue : réduire la perte moyenne avant d\'augmenter la taille.')};}

/* ═══════════ helpers UI ═══════════ */
function eyebrow2(n,t){return '<div class="eyebrow"><span class="rn">'+n+'</span>'+t+'</div>';}
function sec2(n,ttl,sub,inner){return '<section>'+eyebrow2(n,ttl.toUpperCase())+'<h2>'+ttl+'</h2><div class="sub">'+sub+'</div>'+inner+'</section>';}
function aiq2(txt,label){return txt?'<div class="aiq"><div class="ico">▲</div><div><b>'+(label||'Coach Vertex')+' — </b>'+txt+'</div></div>':'';}
function ctx2(id){var c=document.getElementById(id);if(!c)return null;var r=c.getBoundingClientRect(),d=window.devicePixelRatio||1;
 c.width=r.width*d;c.height=r.height*d;var x=c.getContext('2d');x.scale(d,d);x.W=r.width;x.H=r.height;x.font='10px ui-monospace,Menlo,monospace';return x;}
function lineChart(id,pts,opts){var x=ctx2(id);if(!x||pts.length<2)return;opts=opts||{};
 var ys=pts.map(function(p){return p[1];}),mn=Math.min.apply(0,ys.concat([opts.zero!=null?0:ys[0]])),mx=Math.max.apply(0,ys.concat([opts.zero!=null?0:ys[0]]));
 if(mn===mx){mn-=1;mx+=1;}var pad={l:46,r:6,t:10,b:8};
 x.strokeStyle='rgba(255,255,255,.06)';x.fillStyle='#6b7480';
 for(var i=0;i<=3;i++){var yy=pad.t+(x.H-pad.t-pad.b)*i/3;x.beginPath();x.moveTo(pad.l,yy);x.lineTo(x.W-pad.r,yy);x.stroke();
  x.fillText((opts.fmt||function(v){return Math.round(v);})(mx-(mx-mn)*i/3),4,yy+3);}
 var X=function(i){return pad.l+(x.W-pad.l-pad.r)*i/(pts.length-1);},Y=function(v){return pad.t+(x.H-pad.t-pad.b)*(1-(v-mn)/(mx-mn));};
 var col=opts.color||((ys[ys.length-1]>=(opts.zero!=null?0:ys[0]))?'#22c55e':'#ef4444');
 if(opts.zero!=null&&0>=mn&&0<=mx){x.save();x.setLineDash([4,4]);x.strokeStyle='rgba(255,255,255,.18)';x.beginPath();x.moveTo(pad.l,Y(0));x.lineTo(x.W-pad.r,Y(0));x.stroke();x.restore();}
 x.beginPath();pts.forEach(function(p,i){i?x.lineTo(X(i),Y(p[1])):x.moveTo(X(i),Y(p[1]));});
 x.save();x.lineTo(X(pts.length-1),Y(mn));x.lineTo(X(0),Y(mn));x.closePath();
 var g=x.createLinearGradient(0,pad.t,0,x.H);g.addColorStop(0,col+'38');g.addColorStop(1,col+'00');x.fillStyle=g;x.fill();x.restore();
 x.beginPath();pts.forEach(function(p,i){i?x.lineTo(X(i),Y(p[1])):x.moveTo(X(i),Y(p[1]));});
 x.strokeStyle=col;x.lineWidth=2;x.stroke();}
function barChart(id,items,opts){var x=ctx2(id);if(!x||!items.length)return;opts=opts||{};
 var vs=items.map(function(i){return i[1];}),mx=Math.max.apply(0,vs.map(Math.abs))||1,pad={l:8,r:8,t:10,b:16};
 var bw=(x.W-pad.l-pad.r)/items.length,H=x.H-pad.t-pad.b,zero=pad.t+H*(Math.max.apply(0,vs)>0?Math.max.apply(0,vs)/(Math.max.apply(0,vs)+Math.max(0,-Math.min.apply(0,vs))):1);
 if(vs.every(function(v){return v>=0;}))zero=x.H-pad.b;
 items.forEach(function(it,i){var v=it[1],h=Math.abs(v)/mx*(H*0.82);var cx=pad.l+bw*i;
  x.fillStyle=v>=0?'#22c55e':'#ef4444';x.fillRect(cx+bw*0.18,v>=0?zero-h:zero,bw*0.64,Math.max(h,1));
  x.fillStyle='#8794ab';x.textAlign='center';x.fillText(String(it[0]).slice(0,7),cx+bw/2,x.H-4);});}

/* ═══════════ sections ═══════════ */
function sHeader(m){var f=function(l,v,c,s){return '<div><div class="lbl">'+l+'</div><div class="v num" style="color:'+(c||'var(--ink)')+'">'+v+'</div>'+(s?'<div class="s">'+s+'</div>':'')+'</div>';};
 var pf=m.pf==null?'—':(m.pf>=99?'∞':m.pf.toFixed(2));
 return '<div class="met" style="margin-top:6px">'
  +f('Trades',m.total,null,m.n+' clôturés')
  +f('Win rate',m.wr==null?'—':m.wr+'%',scol2(m.wr,50,40),m.nwin+'W · '+m.nloss+'L')
  +f('Profit factor',pf,scol2(m.pf==null?null:m.pf*40,60,40),'gains / pertes')
  +f('Expectancy',m.exp==null?'—':money(m.exp),m.exp>=0?'var(--good)':'var(--bad)','par trade')
  +f('Sharpe',m.sharpeRaw==null?'—':m.sharpeRaw.toFixed(2),scol2(m.sharpeRaw==null?null:50+m.sharpeRaw*40,60,40),'par trade')
  +f('Sortino',m.sortino==null?'—':m.sortino.toFixed(2),scol2(m.sortino==null?null:50+m.sortino*30,60,40),'downside seul')
  +f('Max drawdown',m.maxdd?('−$'+$n2(m.maxdd)):'—','var(--warn)','creux d\'équité')
  +f('Gain moyen',m.avgW==null?'—':money(m.avgW),'var(--good)','par gagnant')
  +f('Perte moyenne',m.avgL==null?'—':money(-m.avgL),'var(--bad)','par perdant')
  +f('R moyen',m.avgR==null?'—':(m.avgR>=0?'+':'')+m.avgR.toFixed(2)+'R',m.avgR>=0?'var(--good)':'var(--bad)','unités de risque')
  +f('Détention moy.',m.avgHold==null?'—':$n2(m.avgHold,1)+' j',null,'entrée → sortie')
  +f('Discipline',m.disc==null?'—':m.disc.toFixed(1)+'/10',scol2(m.disc==null?null:m.disc*10,70,50),'auto-évaluée')
  +f('Score IA',m.ai==null?'—':m.ai+'/100',scol2(m.ai),'qualité moyenne')
  +f('Série en cours',m.stCur>0?m.stCur+' ✓':m.stCur<0?(-m.stCur)+' ✕':'—',m.stCur>0?'var(--good)':m.stCur<0?'var(--bad)':null,'consécutifs')
  +f('Meilleure série',m.stBest||'—','var(--good)','gains d\'affilée')
  +f('Pire série',m.stWorst?-m.stWorst:'—','var(--bad)','pertes d\'affilée')
  +f('Aujourd\'hui',money(m.pDay),m.pDay>=0?'var(--good)':'var(--bad)','P&L du jour')
  +f('Cette semaine',money(m.pWeek),m.pWeek>=0?'var(--good)':'var(--bad)','P&L 7 j')
  +f('Ce mois',money(m.pMonth),m.pMonth>=0?'var(--good)':'var(--bad)','P&L mensuel')+'</div>';}

function sCoach(a,m){var c=coach(a,m);var g=gamify(a,m);
 var lvlBlock='<div class="panel" style="margin-bottom:16px"><div class="lvl">'
  +'<div><div class="lbl">Niveau '+g.lvl+'</div><div class="big">'+g.name+'</div></div>'
  +'<div style="flex:1;min-width:200px"><div style="display:flex;justify-content:space-between;font-size:10.5px;color:var(--mut);margin-bottom:5px"><span>'+g.xp+' XP</span><span>niveau '+(g.lvl+1)+' à '+g.pct+'%</span></div><div class="xpbar"><i style="width:'+g.pct+'%"></i></div></div></div>'
  +'<div class="badges">'+g.badges.map(function(b){return '<span class="badge'+(b[2]?'':' off')+'" title="'+b[1]+'">'+b[0]+' '+b[1]+'</span>';}).join('')+'</div></div>';
 if(!c)return lvlBlock+'<div class="empty">Le coach s\'active à partir de 3 trades clôturés — journalise tes premiers trades ci-dessous.</div>';
 var box=function(t,col,items){return '<div class="c"><div class="t" style="color:'+col+'">'+t+'</div><ul>'+items.map(function(i){return '<li>· '+i+'</li>';}).join('')+'</ul></div>';};
 return lvlBlock+'<div class="panel"><div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap"><span style="font-size:16px;font-weight:800">🧠 Coach Vertex</span>'
  +'<span class="pill p-mut">niveau global '+c.note+'/100</span>'
  +(c.bestSetup?'<span class="pill p-good">meilleur terrain : '+c.bestSetup+'</span>':'')
  +(c.worstSetup?'<span class="pill p-bad">pire terrain : '+c.worstSetup+'</span>':'')
  +(c.err?'<span class="pill p-warn">erreur n°1 : '+c.err+'</span>':'')+'</div>'
  +'<div class="coach">'+box('💪 Tes points forts','var(--good)',c.forces)+box('🩹 Tes points faibles','var(--bad)',c.faibl)
  +box('🛑 À arrêter','var(--warn)',c.stop)+box('📈 À renforcer','var(--info)',c.renf)+'</div>'
  +'<div class="missions"><div class="mission"><b>🎯 Objectif de demain</b>'+c.goalD+'</div><div class="mission"><b>📆 Objectif de la semaine</b>'+c.goalW+'</div></div>'
  +aiq2(c.resume,'Synthèse')+'</div>';}

function sDash(a){var c=closedOf(a);if(c.length<3)return '<div class="empty">Le dashboard s\'allume à partir de 3 trades clôturés.</div>';
 return '<div class="vgrid">'
  +'<div class="chart"><div class="q">Courbe d\'équité</div><div class="a">P&amp;L cumulé, trade après trade — la seule courbe qui dit la vérité.</div><canvas id="jcEq"></canvas></div>'
  +'<div class="chart"><div class="q">Drawdown</div><div class="a">Distance au sommet d\'équité — ta souffrance maximale.</div><canvas id="jcDd"></canvas></div>'
  +'<div class="chart"><div class="q">Win rate glissant (10 trades)</div><div class="a">Ta forme récente, pas ta moyenne historique.</div><canvas id="jcWr"></canvas></div>'
  +'<div class="chart"><div class="q">P&amp;L par mois</div><div class="a">La régularité compte plus que le pic.</div><canvas id="jcMo"></canvas></div></div>';}
function drawDash(a){var c=closedOf(a).slice().reverse();if(c.length<3)return;
 var cum=0,eq=[[0,0]];c.forEach(function(t,i){cum+=(pnlOf(t)||0);eq.push([i+1,cum]);});
 lineChart('jcEq',eq,{zero:0,fmt:function(v){return '$'+Math.round(v);}});
 var pk=0,dd=[[0,0]];cum=0;c.forEach(function(t,i){cum+=(pnlOf(t)||0);if(cum>pk)pk=cum;dd.push([i+1,-(pk-cum)]);});
 lineChart('jcDd',dd,{color:'#ef4444',fmt:function(v){return '$'+Math.round(v);}});
 var wr=[];for(var i=9;i<c.length;i++){var w=c.slice(i-9,i+1).filter(function(t){return t.result==='WIN';}).length;wr.push([i,w*10]);}
 if(wr.length>=2)lineChart('jcWr',wr,{color:'#38bdf8',fmt:function(v){return Math.round(v)+'%';}});
 var mo={};c.forEach(function(t){var k=(t.date||'').slice(0,7);if(k)mo[k]=(mo[k]||0)+(pnlOf(t)||0);});
 var items=Object.keys(mo).sort().slice(-8).map(function(k){return [k.slice(2),mo[k]];});
 barChart('jcMo',items);}

function sCal(a){var byd={};closedOf(a).forEach(function(t){if(t.date)byd[t.date]=(byd[t.date]||0)+(pnlOf(t)||0);});
 var out='',today=new Date();var start=new Date(today);start.setDate(today.getDate()-181);
 while(start.getDay()!==1)start.setDate(start.getDate()-1);
 var d=new Date(start),mx=1;Object.keys(byd).forEach(function(k){mx=Math.max(mx,Math.abs(byd[k]));});
 while(d<=today){var k=d.toISOString().slice(0,10),v=byd[k];
  var bg=v==null?'rgba(255,255,255,.05)':v>=0?'rgba(34,197,94,'+(0.25+Math.min(1,v/mx)*0.6)+')':'rgba(239,68,68,'+(0.25+Math.min(1,-v/mx)*0.6)+')';
  out+='<i style="background:'+bg+'" title="'+k+(v!=null?' · '+money(v):'')+'" onclick="tjDay(\''+k+'\')"></i>';
  d.setDate(d.getDate()+1);}
 var legend='<div style="display:flex;gap:14px;font-size:10.5px;color:var(--mut);margin-top:4px"><span>■ vert = journée gagnante</span><span>■ rouge = perdante</span><span>· intensité = ampleur · clic = filtrer les trades du jour</span>'+(JF.day?'<span class="pill p-warn" style="cursor:pointer" onclick="tjDay(\'\')">filtre : '+JF.day+' ✕</span>':'')+'</div>';
 return '<div class="panel"><div class="cal">'+out+'</div>'+legend+'</div>';}
window.tjDay=function(d){JF.day=(JF.day===d?'':d);renderAll();};

function tableOf(rows,unit){if(!rows.length)return '<div class="empty" style="padding:14px">pas encore de données</div>';
 return '<div class="tscroll"><table><thead><tr><th>'+(unit||'')+'</th><th>N</th><th>Win rate</th><th>P&amp;L</th><th>Expectancy</th></tr></thead><tbody>'
 +rows.map(function(r){return '<tr><td style="font-weight:700">'+r.k+'</td><td class="num">'+r.n+'</td>'
  +'<td class="num" style="min-width:110px"><div style="display:flex;gap:8px;align-items:center"><span style="color:'+scol2(r.wr,50,40)+'">'+r.wr+'%</span><div class="sbar" style="flex:1"><i style="width:'+r.wr+'%;background:'+scol2(r.wr,50,40)+'"></i></div></div></td>'
  +'<td class="num" style="color:'+(r.pnl>=0?'var(--good)':'var(--bad)')+'">'+money(r.pnl)+'</td>'
  +'<td class="num" style="color:'+(r.exp>=0?'var(--good)':'var(--bad)')+'">'+money(r.exp)+'</td></tr>';}).join('')+'</tbody></table></div>';}
function sAnalyses(a){if(closedOf(a).length<3)return '<div class="empty">Les analyses par dimension s\'activent à partir de 3 trades clôturés.</div>';
 var card=function(t,inner){return '<div class="panel" style="padding:14px 16px"><div style="font-size:12.5px;font-weight:800;margin-bottom:8px">'+t+'</div>'+inner+'</div>';};
 return '<div class="angrid">'
  +card('📅 Par jour de la semaine',tableOf(groupBy(a,function(t){return t.date?DAYS[new Date(t.date).getDay()]:null;}),'Jour'))
  +card('🧠 Par émotion',tableOf(groupBy(a,function(t){return t.emo?(EMOIC[t.emo]||'')+' '+t.emo:null;}),'État'))
  +card('🏷️ Par titre',tableOf(groupBy(a,function(t){return t.ticker;}).slice(0,7),'Ticker'))
  +card('🧾 Par instrument',tableOf(groupBy(a,function(t){return t.kind?(t.kind==='STK'?'Action':t.kind):'Manuel';}),'Type'))
  +card('↕️ Par direction',tableOf(groupBy(a,function(t){return t.dir||null;}),'Sens'))
  +card('⚠️ Par déclencheur',tableOf(groupBy(a,function(t){return t.trigger||null;}),'Déclencheur'))+'</div>';}

function sErrors(a){var mk=mistakes(a);
 if(!mk.length)return '<div class="empty">Aucune erreur consignée — remplis le champ « erreur à ne plus répéter » : chaque erreur nommée devient une statistique, puis une solution.</div>';
 return '<div class="panel"><div class="tscroll"><table><thead><tr><th>Erreur</th><th>Observée</th><th>Coût total</th><th>Coût en R</th><th>Dernière fois</th><th>Solution IA</th></tr></thead><tbody>'
  +mk.map(function(e){return '<tr><td style="font-weight:700;color:var(--bad)">'+e.label+'</td><td class="num">'+e.n+'×</td>'
   +'<td class="num" style="color:var(--bad)">'+money(e.cost)+'</td><td class="num">'+(e.costR?e.costR.toFixed(1)+'R':'—')+'</td>'
   +'<td class="num">'+(e.last||'—')+'</td><td style="font-size:12px;color:var(--ink2);border-left:2px solid rgba(34,197,94,.35);padding-left:11px">'+fixFor(e.label)+'</td></tr>';}).join('')
  +'</tbody></table></div></div>';}

/* ═══════════ saisie + liste ═══════════ */
function jmsg(t,c){var m=document.getElementById('jMsg');if(!m)return;m.textContent=t;m.style.color=c;setTimeout(function(){if(m.textContent===t)m.textContent='';},2600);}
window.setDir=function(d){FORM.dir=(FORM.dir===d?'':d);var L=document.getElementById('jDirL'),S=document.getElementById('jDirS');if(L)L.className=FORM.dir==='LONG'?'onL':'';if(S)S.className=FORM.dir==='SHORT'?'onS':'';};
window.setRes=function(r){FORM.res=(FORM.res===r?'':r);var W=document.getElementById('jResW'),X=document.getElementById('jResL');if(W)W.className=FORM.res==='WIN'?'onL':'';if(X)X.className=FORM.res==='LOSS'?'onS':'';};
window.setEmo=function(e){FORM.emo=(FORM.emo===e?'':e);buildEmo();};
function buildEmo(){var el=document.getElementById('jEmoChips');if(el)el.innerHTML=EMO.map(function(x){return '<button type="button" class="jchip'+(FORM.emo===x[1]?' on':'')+'" onclick="setEmo(\''+x[1]+'\')">'+x[0]+' '+x[1]+'</button>';}).join('');}
window.rr=function(){var e=+gv('jEntry'),s=+gv('jStop'),t=+gv('jTp');var el=document.getElementById('jRR');if(!el)return;
 if(e&&s&&t&&e!==s){var v=Math.abs(t-e)/Math.abs(e-s);el.textContent=v.toFixed(2)+' : 1';el.style.color=v>=2?'#22C55E':v>=1?'#F5B45B':'#EF4444';}else{el.textContent='—';el.style.color='#F5B45B';}};
function gv(id){var el=document.getElementById(id);return el?(el.value||'').trim():'';}
window.jSave=function(){var tk=gv('jTicker');if(!tk){jmsg('Renseigne au moins un ticker.','#EF4444');return;}
 var e={id:Date.now(),ticker:tk.toUpperCase(),tf:gv('jTf'),dir:FORM.dir,reason:gv('jReason'),entry:gv('jEntry'),stop:gv('jStop'),tp:gv('jTp'),risk:gv('jRisk'),emo:FORM.emo,conf:gv('jConf'),disc:gv('jDisc'),trigger:gv('jTrigger'),result:FORM.res,exit:gv('jExit'),pnl:gv('jPnl'),lesson:gv('jLesson'),mistake:gv('jMistake'),date:new Date().toISOString().slice(0,10)};
 var a=jGet();a.unshift(e);jSet(a);FORM={dir:'',res:'',emo:''};jmsg('✓ Trade enregistré.','#22C55E');renderAll();};
window.jDel=function(id){if(!confirm('Supprimer cette entrée du journal ?'))return;jSet(jGet().filter(function(t){return t.id!==id;}));renderAll();};
window.jExport=function(){var blob=new Blob([JSON.stringify(jGet(),null,2)],{type:'application/json'});var u=URL.createObjectURL(blob);var a=document.createElement('a');a.href=u;a.download='vertex-journal.json';a.click();URL.revokeObjectURL(u);};
window.jImport=function(){var i=document.createElement('input');i.type='file';i.accept='.json';i.onchange=function(){var f=i.files[0];if(!f)return;var r=new FileReader();r.onload=function(){try{var d=JSON.parse(r.result);if(Array.isArray(d)){jSet(d);renderAll();jmsg('✓ Journal importé.','#22C55E');}}catch(e){jmsg('Fichier invalide.','#EF4444');}};r.readAsText(f);};i.click();};
window.setJF=function(k,v){JF[k]=v;renderAll();};
window.jQuick=function(id){var a=jGet();var t=a.filter(function(x){return x.id===id;})[0];if(!t)return;
 var emo=prompt('État émotionnel pendant ce trade ? (Calme / Concentré / Stressé / Avide / Neutre / Revanche)',t.emo||'');if(emo!=null)t.emo=emo.trim();
 var mk=prompt('Erreur à ne plus répéter ? (vide si aucune)',t.mistake||'');if(mk!=null)t.mistake=mk.trim();
 var ls=prompt('Leçon apprise ?',t.lesson||'');if(ls!=null)t.lesson=ls.trim();
 jSet(a);renderAll();};

function sForm(){return '<div class="panel"><div class="form">'
 +'<div><div class="lbl" style="margin-bottom:10px;color:var(--acc)">① Setup</div>'
  +'<div class="jfield"><label>Actif / ticker</label><input id="jTicker" class="jf" placeholder="ex. NVDA · MNQ"></div>'
  +'<div class="jfield" style="margin-top:9px"><label>Timeframe</label><input id="jTf" class="jf" placeholder="ex. Daily · 15m"></div>'
  +'<div class="jfield" style="margin-top:9px"><label>Direction</label><div class="tog"><button type="button" id="jDirL" onclick="setDir(\'LONG\')">▲ Long</button><button type="button" id="jDirS" onclick="setDir(\'SHORT\')">▼ Short</button></div></div>'
  +'<div class="jfield" style="margin-top:9px"><label>Raison d\'entrée</label><input id="jReason" class="jf" placeholder="setup / signal"></div></div>'
 +'<div><div class="lbl" style="margin-bottom:10px;color:var(--acc)">② Risque &amp; psychologie</div>'
  +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">'
  +'<div class="jfield"><label>Entrée</label><input id="jEntry" class="jf" type="number" step="any" oninput="rr()"></div>'
  +'<div class="jfield"><label>Stop</label><input id="jStop" class="jf" type="number" step="any" oninput="rr()"></div>'
  +'<div class="jfield"><label>Objectif</label><input id="jTp" class="jf" type="number" step="any" oninput="rr()"></div>'
  +'<div class="jfield"><label>Risque %</label><input id="jRisk" class="jf" type="number" step="any" placeholder="% capital"></div></div>'
  +'<div style="font-size:11.5px;color:var(--mut);margin:7px 0 9px">R:R planifié : <b id="jRR" style="color:#F5B45B">—</b></div>'
  +'<div class="jfield"><label>État émotionnel</label><div id="jEmoChips" style="display:flex;gap:6px;flex-wrap:wrap"></div></div>'
  +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px">'
  +'<div class="jfield"><label>Confiance /10</label><input id="jConf" class="jf" type="number" min="1" max="10"></div>'
  +'<div class="jfield"><label>Discipline /10</label><input id="jDisc" class="jf" type="number" min="1" max="10"></div></div>'
  +'<div class="jfield" style="margin-top:9px"><label>Déclencheur d\'erreur</label><input id="jTrigger" class="jf" placeholder="FOMO · revanche · sur-trading"></div></div>'
 +'<div><div class="lbl" style="margin-bottom:10px;color:var(--acc)">③ Résultat &amp; apprentissage</div>'
  +'<div class="jfield"><label>Résultat</label><div class="tog"><button type="button" id="jResW" onclick="setRes(\'WIN\')">✓ Gagnant</button><button type="button" id="jResL" onclick="setRes(\'LOSS\')">✕ Perdant</button></div></div>'
  +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:9px">'
  +'<div class="jfield"><label>Sortie</label><input id="jExit" class="jf" type="number" step="any"></div>'
  +'<div class="jfield"><label>P&amp;L ($)</label><input id="jPnl" class="jf" type="number" step="any"></div></div>'
  +'<div class="jfield" style="margin-top:9px"><label>💡 Leçon apprise</label><textarea id="jLesson" class="jf" placeholder="Qu\'est-ce qui a marché ? Que retenir ?"></textarea></div>'
  +'<div class="jfield" style="margin-top:9px"><label>⚠️ Erreur à ne plus répéter</label><input id="jMistake" class="jf" placeholder="ex. stop bougé trop tôt"></div>'
  +'<button class="vbtn pri" style="width:100%;padding:11px;font-size:14px;border-radius:13px;margin-top:12px" onclick="jSave()">💾 Enregistrer</button>'
  +'<div id="jMsg" style="text-align:center;font-size:12px;margin-top:7px;min-height:14px;font-weight:700"></div></div>'
 +'</div></div>';}

function sList(a){var todo=a.filter(function(t){return t.auto&&(!t.emo||!t.lesson);}).slice(0,4);
 var chip=function(l,on,k,v){return '<button class="vbtn'+(on?' pri':'')+'" onclick="setJF(\''+k+'\',\''+v+'\')">'+l+'</button>';};
 var bar='<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">'
  +chip('Tous',!JF.res,'res','')+chip('✓ Gagnants',JF.res==='WIN','res','WIN')+chip('✕ Perdants',JF.res==='LOSS','res','LOSS')
  +'<input placeholder="🔎 ticker" value="'+(JF.q||'')+'" oninput="setJF(\'q\',this.value.toUpperCase().trim())" class="jf" style="width:130px;margin-left:auto">'
  +'</div>';
 var td=todo.map(function(t){return '<div class="todo"><span class="pill p-warn">🤖 à compléter</span>'
  +'<b>'+t.ticker+'</b><span style="font-size:11.5px;color:var(--mut)">'+(t.date||'')+' · P&amp;L '+money(pnlOf(t))+' — il manque '+(!t.emo?'l\'émotion':'')+(!t.emo&&!t.lesson?' et ':'')+(!t.lesson?'la leçon':'')+'</span>'
  +'<button class="vbtn" style="margin-left:auto" onclick="event.stopPropagation();jQuick('+t.id+')">✍️ Compléter (30 s)</button></div>';}).join('');
 var f=a.filter(function(t){return (!JF.res||t.result===JF.res)&&(!JF.q||(t.ticker||'').indexOf(JF.q)>=0)&&(!JF.day||t.date===JF.day);});
 var rows=f.slice(0,60).map(function(t){var p=pnlOf(t),sc=aiScore(t).score,rm=rMult(t);
  var rc=t.result==='WIN'?'var(--good)':t.result==='LOSS'?'var(--bad)':'var(--mut)';
  return '<div class="trow" onclick="tjOpen('+t.id+')">'
  +'<div style="display:flex;flex-direction:column;gap:2px;min-width:76px"><span class="tk">'+t.ticker+'</span>'
  +'<span style="font-size:10px;font-weight:800;color:'+(t.dir==='SHORT'?'var(--bad)':'var(--good)')+'">'+(t.dir||'')+(t.kind&&t.kind!=='STK'?' · '+t.kind:'')+'</span></div>'
  +'<div><div class="meta">'+(t.date||'')+(t.auto?' · 🤖 auto':'')+(t.emo?' · '+(EMOIC[t.emo]||'')+' '+t.emo:'')+(t.trigger?' · ⚠️ '+t.trigger:'')+'</div>'
  +(t.lesson?'<div style="font-size:12px;color:var(--ink2);margin-top:3px">💡 '+t.lesson+'</div>':(t.reason?'<div style="font-size:11.5px;color:var(--mut);margin-top:3px">'+t.reason.slice(0,110)+'</div>':''))+'</div>'
  +'<div style="text-align:right"><div class="num" style="font-size:15px;font-weight:800;color:'+rc+'">'+(p!=null?money(p):(t.result||'en cours'))+'</div>'
  +'<div class="meta num">'+(rm!=null?(rm>=0?'+':'')+rm.toFixed(1)+'R · ':'')+'IA '+sc+'/100</div></div></div>';}).join('');
 return bar+td+(rows||'<div class="empty">Ton journal est vide — note ton premier trade ci-dessus, ou clôture une position sur le Desk : elle arrivera ici toute seule.</div>')
  +(f.length>60?'<div style="text-align:center;font-size:11px;color:var(--mut);padding:8px">'+(f.length-60)+' trades plus anciens — affine avec les filtres</div>':'');}

/* ═══════════ fiche détaillée ═══════════ */
window.tjClose=function(){document.getElementById('tjOvl').className='ovl';};
window.tjOpen=function(id){var a=jGet();var t=a.filter(function(x){return x.id===id;})[0];if(!t)return;
 var sc=aiScore(t),rm=rMult(t),p=pnlOf(t);
 var sims=a.filter(function(x){return x.id!==id&&x.result&&(x.ticker===t.ticker||(x.emo&&x.emo===t.emo&&x.dir===t.dir));}).slice(0,5);
 var e=+t.entry,st=+t.stop,tp=+t.tp;var rrp=(e&&st&&tp&&e!==st)?Math.abs(tp-e)/Math.abs(e-st):null;
 var tl=[['📍 Entrée',(t.added||t.date||'')+(t.entry?' · $'+t.entry:'')+(t.reason?' — '+t.reason.slice(0,90):'')],
  st?['🛑 Stop posé','$'+t.stop+(rrp!=null?' → R:R planifié '+rrp.toFixed(1)+':1':'')]:null,
  tp?['🎯 Objectif','$'+t.tp]:null,
  ['🏁 Sortie',(t.date||'')+(t.exit?' · $'+t.exit:'')+(p!=null?' — '+money(p)+(rm!=null?' ('+(rm>=0?'+':'')+rm.toFixed(1)+'R)':''):'')],
  ['🧠 Analyse IA','score '+sc.score+'/100 — chaque trade journalisé affine ton coach']].filter(Boolean);
 var simr=sims.map(function(x){var xp=pnlOf(x);return '<div class="simrow"><span><b>'+x.ticker+'</b> '+(x.date||'')+(x.emo?' · '+x.emo:'')+'</span>'
  +'<span class="num">'+(rMult(x)!=null?(rMult(x)>=0?'+':'')+rMult(x).toFixed(1)+'R':'—')+'</span>'
  +'<span class="num" style="color:'+(xp>=0?'var(--good)':'var(--bad)')+'">'+money(xp)+'</span>'
  +'<span class="num">IA '+aiScore(x).score+'</span></div>';}).join('');
 document.getElementById('tjFiche').innerHTML=
  '<div style="display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap"><div>'
  +'<div style="display:flex;gap:8px;align-items:center"><span style="font-size:26px;font-weight:900">'+t.ticker+'</span>'
  +(t.dir?'<span class="pill '+(t.dir==='SHORT'?'p-bad':'p-good')+'">'+t.dir+'</span>':'')
  +(t.kind&&t.kind!=='STK'?'<span class="pill p-vio">'+t.kind+(t.strike?' $'+t.strike:'')+'</span>':'')
  +(t.auto?'<span class="pill p-warn">🤖 auto</span>':'')+'</div>'
  +'<div style="font-size:12px;color:var(--mut);margin-top:5px">'+(t.date||'')+(t.emo?' · '+(EMOIC[t.emo]||'')+' '+t.emo:'')+(t.conf?' · confiance '+t.conf+'/10':'')+(t.disc?' · discipline '+t.disc+'/10':'')+'</div></div>'
  +'<div style="margin-left:auto;text-align:right"><div class="lbl">Score IA du trade</div><div class="fscore num" style="color:'+scol2(sc.score)+'">'+sc.score+'<span style="font-size:16px;color:var(--faint)">/100</span></div></div>'
  +'<span onclick="tjClose()" style="cursor:pointer;color:var(--mut);font-size:20px;padding:2px 6px">✕</span></div>'
  +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:18px" class="fcols">'
  +'<div><div class="lbl" style="margin-bottom:8px">Timeline du trade</div><div class="ftl">'+tl.map(function(s){return '<div><b style="color:var(--ink)">'+s[0]+'</b><br>'+s[1]+'</div>';}).join('')+'</div>'
  +(t.lesson?'<div class="aiq" style="margin-top:10px"><div class="ico">💡</div><div><b>Leçon — </b>'+t.lesson+'</div></div>':'')
  +(t.mistake?'<div class="aiq" style="border-left-color:var(--bad);background:linear-gradient(120deg,rgba(239,68,68,.08),transparent);margin-top:10px"><div class="ico" style="background:rgba(239,68,68,.15)">⚠️</div><div><b>Erreur — </b>'+t.mistake+'<br><span style="font-size:12px">Solution : '+fixFor(t.mistake)+'</span></div></div>':'')+'</div>'
  +'<div><div class="lbl" style="margin-bottom:8px">Pourquoi ce score</div>'
  +sc.why.map(function(w){return '<div style="display:flex;gap:9px;font-size:12.3px;color:var(--ink2);padding:5px 0;border-bottom:1px solid var(--hair)"><b class="num" style="min-width:30px;color:'+(w[0].charAt(0)==='+'?'var(--good)':w[0].charAt(0)==='−'?'var(--bad)':'var(--mut)')+'">'+w[0]+'</b><span>'+w[1]+'</span></div>';}).join('')
  +(simr?'<div class="lbl" style="margin:16px 0 6px">'+sims.length+' trades similaires (même titre ou même état)</div>'+simr:'')
  +'</div></div>'
  +'<div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap"><button class="vbtn" onclick="jQuick('+t.id+');tjClose()">✍️ Compléter émotion/leçon</button>'
  +'<button class="vbtn dng" onclick="tjClose();jDel('+t.id+')">🗑 Supprimer</button></div>';
 document.getElementById('tjOvl').className='ovl on';};

function sRoad(){var steps=[['🧾','Trade','clôturé'],['🧠','Analyse IA','score /100'],['⚠️','Erreur','détectée'],['📚','Historique','comparé'],['💡','Leçon','générée'],['🛠️','Plan','d\'amélioration'],['✅','Application','trade suivant'],['📈','Progression','mesurée'],['📊','Stats','mises à jour'],['🏆','Niveau','supérieur']];
 return '<div class="road">'+steps.map(function(s,i){return '<div><div class="i">'+s[0]+'</div><div class="t">'+s[1]+'</div><div class="s">'+s[2]+'</div></div>'+(i<steps.length-1?'':'');}).join('')+'</div>';}

/* ═══════════ assemblage ═══════════ */
function renderAll(){var a=jGet(),m=stats(a);
 document.getElementById('tjRoot').innerHTML=
  sHeader(m)
  +sec2('01','Coach Vertex','Ton niveau, tes badges, et le diagnostic qui évolue après chaque trade.',sCoach(a,m))
  +sec2('02','Dashboard','Les courbes qui disent la vérité : équité, drawdown, forme récente, régularité mensuelle.',sDash(a))
  +sec2('03','Calendrier','Six mois de trading en un regard — clique une journée pour revoir ses trades.',sCal(a))
  +sec2('04','Analyses avancées','Où gagnes-tu vraiment ? Par jour, émotion, titre, instrument, direction, déclencheur.',sAnalyses(a))
  +sec2('05','Base de connaissances des erreurs','Chaque erreur nommée devient une statistique : occurrences, coût, et la solution pour l\'éteindre.',sErrors(a))
  +sec2('06','Nouvelle entrée','Les clôtures du Desk se journalisent toutes seules — ici, tu n\'ajoutes que l\'humain : émotion, erreur, leçon.',sForm())
  +sec2('07','Mes trades','Clique un trade pour ouvrir sa fiche complète : timeline, score IA expliqué, trades similaires.',sList(a))
  +sec2('08','Décisions du comité épinglées','Fige un verdict du comité, reviens dessus, apprends — le « verdict a posteriori » est un professeur.',
   '<div class="kpiband" id="djStats" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-bottom:10px"></div><div id="djList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px"></div>')
  +sec2('09','La boucle de progression','Le cycle complet — chaque étape est alimentée automatiquement par ton journal.',sRoad())
  +'<div class="foot">⚠️ <b>Journal privé</b> — stocké sur cet appareil et synchronisé via ton desk · les scores IA sont des heuristiques pédagogiques, pas des vérités · <b>analyse uniquement, aucun ordre</b>.</div>';
 buildEmo();rr();drawDash(a);
 if(window.djRender)try{djRender();}catch(e){}}
jvSyncPull(function(){renderAll();});
"""

__all__ = ['CSS', 'BODY', 'JS']
