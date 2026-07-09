"""
vertex/ui/options_lab.py — OPTIONS RESEARCH CENTER (page).

La page Options Lab refondue : 12 grands chapitres éditoriaux, servis par
/api/options-lab (payload consolidé côté serveur — plus de /scan géant).

Principes : une information n'est jamais une carte isolée ; un sujet = une
grande section ; listes premium, tableaux de synthèse, heatmaps, timelines ;
chaque graphique répond à une question ; l'IA (les lectures Vertex) explique
chaque chapitre. Rendu paresseux des graphiques (IntersectionObserver),
canvas haute densité (devicePixelRatio), responsive.

⛔ Analyse uniquement — aucune de ces vues ne passe d'ordre.
"""

CSS = r"""
#olab{--acc:#ff7a18;--acc2:#ff9a3d;--good:#22c55e;--bad:#ef4444;--info:#38bdf8;--warn:#f5b45b;--vio:#a78bfa;
 --ink:#eef2f8;--ink2:#aeb8c8;--mut:#8794ab;--faint:#4b5563;--surf:#101218;--bg2:#0b0d12;
 --hair:rgba(255,255,255,.07);--hair2:rgba(255,255,255,.12);
 --mono:ui-monospace,'SF Mono','JetBrains Mono',Menlo,monospace;
 --sp:clamp(46px,6vw,76px);color:var(--ink);display:block}
#olab .num{font-variant-numeric:tabular-nums lining-nums}
#olab .up{color:var(--good)}#olab .dn{color:var(--bad)}
#olab section{padding:var(--sp) 0 0}
#olab .eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:12px}
#olab .eyebrow .rn{font-family:var(--mono);color:var(--faint);letter-spacing:0}
#olab .eyebrow::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,rgba(255,122,24,.35),transparent)}
#olab h2{font-size:clamp(21px,2.6vw,28px);font-weight:800;letter-spacing:-.02em;margin:0 0 6px}
#olab .sub{color:var(--mut);font-size:13px;max-width:70ch;margin-bottom:22px}
#olab .panel{background:linear-gradient(170deg,var(--surf),var(--bg2));border:1px solid var(--hair);border-radius:20px;padding:22px 24px}
#olab .aiq{display:flex;gap:12px;align-items:flex-start;margin-top:18px;padding:14px 17px;background:linear-gradient(120deg,rgba(255,122,24,.09),rgba(255,122,24,.02));border:1px solid rgba(255,122,24,.16);border-left:2.5px solid var(--acc);border-radius:14px;font-size:13.5px;line-height:1.6;color:var(--ink2)}
#olab .aiq b{color:var(--ink)}
#olab .aiq .ico{flex:none;width:22px;height:22px;border-radius:7px;background:rgba(255,122,24,.16);display:grid;place-items:center;font-size:12px;margin-top:1px}
#olab .lbl{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
#olab .pill{display:inline-flex;align-items:center;gap:6px;font-size:10.5px;font-weight:800;padding:3px 10px;border-radius:999px;letter-spacing:.4px}
#olab .p-good{background:rgba(34,197,94,.13);color:var(--good)}
#olab .p-bad{background:rgba(239,68,68,.13);color:var(--bad)}
#olab .p-warn{background:rgba(245,180,91,.13);color:var(--warn)}
#olab .p-info{background:rgba(56,189,248,.13);color:var(--info)}
#olab .p-mut{background:rgba(255,255,255,.06);color:var(--mut)}
/* cockpit */
#olab .met{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:0;border:1px solid var(--hair);border-radius:18px;overflow:hidden;background:var(--bg2)}
#olab .met>div{padding:16px 18px;border-right:1px solid var(--hair);border-bottom:1px solid var(--hair)}
#olab .met .v{font-size:22px;font-weight:800;margin-top:5px;font-variant-numeric:tabular-nums}
#olab .met .s{font-size:10px;color:var(--faint);margin-top:3px}
/* fiche recherche */
#olab .hero{display:grid;grid-template-columns:1.5fr 1fr;gap:24px}
#olab .hero .id .tk{font-size:clamp(38px,5vw,54px);font-weight:900;letter-spacing:-.03em;line-height:1}
#olab .hero .id .ln{font-size:13px;color:var(--mut);margin-top:8px}
#olab .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:0;margin-top:22px;border-top:1px solid var(--hair)}
#olab .kpis>div{padding:13px 14px 12px;border-right:1px solid var(--hair);border-top:1px solid transparent}
#olab .kpis .v{font-size:17px;font-weight:800;margin-top:3px;font-variant-numeric:tabular-nums}
#olab .kpis .s{font-size:9.5px;color:var(--faint);margin-top:2px}
#olab .verdict{border-radius:16px;padding:18px;border:1px solid var(--hair);display:flex;flex-direction:column;gap:8px;justify-content:center}
#olab .verdict .v{font-size:26px;font-weight:900;letter-spacing:.02em}
#olab .verdict .w{font-size:12.5px;color:var(--ink2);line-height:1.55}
#olab .thesis{margin-top:22px;border-top:1px solid var(--hair)}
#olab .thesis>div{display:flex;gap:14px;padding:13px 2px;border-bottom:1px solid var(--hair);font-size:13.5px;line-height:1.6;color:var(--ink2)}
#olab .thesis .n{flex:none;font-family:var(--mono);color:var(--acc);font-weight:700;font-size:12px;padding-top:2px}
#olab .thesis b{color:var(--ink)}
/* analyse complète — liste premium */
#olab .arow{display:grid;grid-template-columns:210px 130px 1fr 230px;gap:18px;align-items:start;padding:17px 2px;border-bottom:1px solid var(--hair)}
#olab .arow:last-child{border-bottom:0}
#olab .arow .h{display:flex;gap:9px;align-items:center;font-weight:700;font-size:13.5px}
#olab .arow .imp{margin-top:6px}
#olab .arow .txt{font-size:12.8px;color:var(--ink2);line-height:1.6}
#olab .arow .rec{font-size:12px;color:var(--ink2);line-height:1.5;padding-left:12px;border-left:2px solid rgba(255,122,24,.4)}
#olab .arow .rec b{color:var(--acc2);font-weight:800;font-size:10px;letter-spacing:.8px}
#olab .sbar{height:5px;border-radius:99px;background:rgba(255,255,255,.06);margin-top:8px;overflow:hidden}
#olab .sbar i{display:block;height:100%;border-radius:99px}
#olab .snum{font-family:var(--mono);font-size:11px;color:var(--mut);margin-top:5px}
/* plan — timeline verticale */
#olab .tl{position:relative;padding-left:30px}
#olab .tl::before{content:"";position:absolute;left:9px;top:8px;bottom:8px;width:2px;background:linear-gradient(180deg,rgba(255,122,24,.5),rgba(255,255,255,.06))}
#olab .tl>div{position:relative;padding:0 0 22px}
#olab .tl .dot{position:absolute;left:-27px;top:3px;width:16px;height:16px;border-radius:99px;display:grid;place-items:center;font-size:9px;background:#16181f;border:2px solid var(--faint)}
#olab .tl .t{font-weight:800;font-size:13.5px}
#olab .tl .x{font-size:12.5px;color:var(--ink2);line-height:1.55;margin-top:3px;max-width:74ch}
#olab .two{display:grid;grid-template-columns:1.4fr 1fr;gap:22px}
#olab .vgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
#olab .chart{background:var(--bg2);border:1px solid var(--hair);border-radius:16px;padding:16px 16px 10px}
#olab .chart .q{font-size:12.5px;font-weight:700}
#olab .chart .a{font-size:11px;color:var(--mut);margin:3px 0 8px;line-height:1.45}
#olab canvas{width:100%;height:190px;display:block}
/* tableaux */
#olab table{width:100%;border-collapse:collapse;font-size:12.6px}
#olab th{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);font-weight:800;padding:9px 10px;border-bottom:1px solid var(--hair2);white-space:nowrap}
#olab td{padding:11px 10px;border-bottom:1px solid var(--hair);vertical-align:top}
#olab tr:last-child td{border-bottom:0}
#olab tbody tr{transition:background .12s}
#olab tbody tr:hover{background:rgba(255,255,255,.025)}
#olab .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
#olab .cellbar{min-width:64px}
/* tops */
#olab .topgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
#olab .toplist{background:var(--bg2);border:1px solid var(--hair);border-radius:16px;padding:14px 16px 6px}
#olab .toplist .h{font-size:13px;font-weight:800;padding-bottom:8px;border-bottom:1px solid var(--hair2)}
#olab .toplist .r{display:grid;grid-template-columns:1fr auto;gap:4px 12px;padding:10px 0;border-bottom:1px solid var(--hair)}
#olab .toplist .r:last-child{border-bottom:0}
#olab .toplist .l1{font-size:12.8px;font-weight:700}
#olab .toplist .l2{font-size:11px;color:var(--mut);line-height:1.45;grid-column:1/-1}
#olab .toplist .kv{font-family:var(--mono);font-size:11px;color:var(--ink2);white-space:nowrap;text-align:right}
/* heatmap */
#olab .heat td{padding:7px 8px;font-family:var(--mono);font-size:11.5px;text-align:center;border-bottom:1px solid rgba(255,255,255,.04)}
#olab .heat td:first-child{text-align:left;font-family:Inter;font-weight:700;font-size:12px}
#olab .hcell{border-radius:6px;padding:4px 0;display:block}
/* stratégies */
#olab .strow{display:grid;grid-template-columns:230px 90px 1fr;gap:18px;padding:15px 2px;border-bottom:1px solid var(--hair);align-items:start}
#olab .strow:last-child{border-bottom:0}
#olab .strow .nm{font-weight:800;font-size:13.5px}
#olab .strow .kd{font-size:10px;color:var(--mut);margin-top:4px;text-transform:uppercase;letter-spacing:.6px}
#olab .strow .cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;font-size:11.8px;color:var(--ink2);line-height:1.5}
#olab .strow .cols b{display:block;font-size:9px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px}
#olab .strow .cols .w b{color:var(--good)}#olab .strow .cols .av b{color:var(--bad)}#olab .strow .cols .cx b{color:var(--info)}
/* timeline horizontale (échéancier) */
#olab .htl{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;border:1px solid var(--hair);border-radius:16px;overflow:hidden;background:var(--bg2)}
#olab .htl>div{padding:15px 15px 13px;border-right:1px solid var(--hair);position:relative}
#olab .htl .w{font-family:var(--mono);font-size:10px;color:var(--faint)}
#olab .htl .t{font-weight:800;font-size:12.5px;margin:5px 0 4px}
#olab .htl .x{font-size:11px;color:var(--mut);line-height:1.45}
#olab .gaugerow{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:18px}
@media(max-width:1000px){#olab .arow{grid-template-columns:170px 1fr;grid-auto-rows:auto}#olab .arow .txt,#olab .arow .rec{grid-column:1/-1}
 #olab .strow{grid-template-columns:1fr}#olab .strow .cols{grid-template-columns:1fr}}
@media(max-width:860px){#olab .hero,#olab .two,#olab .vgrid,#olab .topgrid,#olab .gaugerow{grid-template-columns:1fr}}
#olab .foot{margin-top:44px;padding-top:14px;border-top:1px solid var(--hair);font-size:11px;color:var(--faint);line-height:1.6}
#olab .foot b{color:var(--mut)}
#olab .skel{padding:60px 0;text-align:center;color:var(--mut);font-size:13px}
"""

BODY = (
  '<div id="olab">'
  '<div data-vx-crumb></div>'
  '<div class="vhead"><div><h1>💎 Options Lab</h1>'
  '<div class="s" id="olabHead">chargement du board…</div></div>'
  '<div style="margin-left:auto;align-self:center"><button class="vbtn" onclick="olabLoad(true)">⟳ Actualiser</button></div></div>'
  '<div id="olabSym"></div>'
  '<div id="olabRoot"><div class="skel">Vertex analyse le marché des options…</div></div>'
  '</div>')

JS = r"""
var OL=null, OLDRAWN={};
function $h(s){return String(s==null?'—':s);}
function $n(x,d){return x==null?'—':Number(x).toLocaleString('fr-FR',{maximumFractionDigits:d==null?0:d});}
function $usd(x){return x==null?'—':'$'+$n(x,Math.abs(x)<10?2:0);}
function tone(t){return t==='good'?'var(--good)':t==='bad'?'var(--bad)':t==='warn'?'var(--warn)':t==='info'?'var(--info)':'var(--mut)';}
function scol(v){return v==null?'#4b5563':v>=65?'#22c55e':v>=45?'#f5b45b':'#ef4444';}
function heatbg(v,inv){if(v==null)return 'transparent';var x=Math.max(0,Math.min(100,inv?100-v:v));
 return x>=65?'rgba(34,197,94,'+(0.10+x/100*.22)+')':x>=45?'rgba(245,180,91,.16)':'rgba(239,68,68,'+(0.10+(100-x)/100*.16)+')';}
function bar(v,w){return '<div class="sbar" style="'+(w?'width:'+w:'')+'"><i style="width:'+(v==null?0:Math.max(2,Math.min(100,v)))+'%;background:'+scol(v)+'"></i></div>';}
function eyebrow(n,t){return '<div class="eyebrow"><span class="rn">'+n+'</span>'+t+'</div>';}
function ai(txt,label){return txt?'<div class="aiq"><div class="ico">▲</div><div><b>'+(label||'Lecture Vertex')+' — </b>'+txt+'</div></div>':'';}
function sec(n,ttl,sub,inner){return '<section>'+eyebrow(n,ttl.toUpperCase())+'<h2>'+ttl+'</h2><div class="sub">'+sub+'</div>'+inner+'</section>';}

/* ───────── canvas haute densité + rendu paresseux ───────── */
function cnv(id,h){return '<canvas id="'+id+'" style="height:'+(h||190)+'px"></canvas>';}
function ctx2d(id){var c=document.getElementById(id);if(!c)return null;var r=c.getBoundingClientRect(),d=window.devicePixelRatio||1;
 c.width=r.width*d;c.height=r.height*d;var x=c.getContext('2d');x.scale(d,d);x.W=r.width;x.H=r.height;
 x.font='10px ui-monospace,Menlo,monospace';return x;}
function chart(id,q,a,h){return '<div class="chart"><div class="q">'+q+'</div><div class="a">'+a+'</div>'+cnv(id,h)+'</div>';}
function lazyDraw(){var els=document.querySelectorAll('#olab canvas[id]');if(!('IntersectionObserver' in window)){els.forEach(function(c){drawOne(c.id);});return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){drawOne(e.target.id);io.unobserve(e.target);}});},{rootMargin:'160px'});
 els.forEach(function(c){io.observe(c);});}
function axes(x,pad,ymin,ymax,fmt){x.strokeStyle='rgba(255,255,255,.06)';x.fillStyle='#6b7480';x.textAlign='left';
 for(var i=0;i<=3;i++){var yy=pad.t+(x.H-pad.t-pad.b)*i/3;x.beginPath();x.moveTo(pad.l,yy);x.lineTo(x.W-pad.r,yy);x.stroke();
  var v=ymax-(ymax-ymin)*i/3;x.fillText(fmt?fmt(v):Math.round(v),4,yy+3);}}
function line(x,pts,pad,ymin,ymax,xmin,xmax,color,fill){var X=function(v){return pad.l+(x.W-pad.l-pad.r)*(v-xmin)/((xmax-xmin)||1);},
 Y=function(v){return pad.t+(x.H-pad.t-pad.b)*(1-(v-ymin)/((ymax-ymin)||1));};
 x.beginPath();pts.forEach(function(p,i){i?x.lineTo(X(p[0]),Y(p[1])):x.moveTo(X(p[0]),Y(p[1]));});
 if(fill){x.save();x.lineTo(X(pts[pts.length-1][0]),Y(ymin));x.lineTo(X(pts[0][0]),Y(ymin));x.closePath();x.fillStyle=fill;x.fill();x.restore();
  x.beginPath();pts.forEach(function(p,i){i?x.lineTo(X(p[0]),Y(p[1])):x.moveTo(X(p[0]),Y(p[1]));});}
 x.strokeStyle=color;x.lineWidth=1.8;x.stroke();return {X:X,Y:Y};}
function vline(x,map,vx,ymin,ymax,color,label){x.save();x.setLineDash([4,4]);x.strokeStyle=color;x.beginPath();
 x.moveTo(map.X(vx),map.Y(ymax));x.lineTo(map.X(vx),map.Y(ymin));x.stroke();x.setLineDash([]);
 if(label){x.fillStyle=color;x.textAlign='center';x.fillText(label,map.X(vx),map.Y(ymax)-4);}x.restore();}

/* ───────── graphiques ───────── */
function drawOne(id){if(OLDRAWN[id]||!OL)return;OLDRAWN[id]=1;var v=OL.viz||{};
 try{
 if(id==='cPayoff'&&v.payoff){var x=ctx2d(id);if(!x)return;var P=v.payoff.points.map(function(p){return [p.x,p.y];});
  var ys=P.map(function(p){return p[1];}),xs=P.map(function(p){return p[0];});
  var ymin=Math.min.apply(0,ys),ymax=Math.max.apply(0,ys),pad={l:44,r:8,t:14,b:6};
  axes(x,pad,ymin,ymax,function(y){return '$'+Math.round(y);});
  var m=line(x,P,pad,ymin,ymax,Math.min.apply(0,xs),Math.max.apply(0,xs),'#22c55e');
  // zone de perte sous 0
  x.save();x.globalAlpha=.9;x.strokeStyle='rgba(255,255,255,.18)';x.beginPath();x.moveTo(pad.l,m.Y(0));x.lineTo(x.W-pad.r,m.Y(0));x.stroke();x.restore();
  vline(x,m,v.payoff.spot,ymin,ymax,'#8794ab','titre '+$usd(v.payoff.spot));
  vline(x,m,v.payoff.be,ymin,ymax,'#f5b45b','seuil '+$usd(v.payoff.be));
  if(v.payoff.target)vline(x,m,v.payoff.target,ymin,ymax,'#38bdf8','cible');}
 if(id==='cCone'&&v.cone){var x=ctx2d(id);if(!x)return;var C=v.cone,pad={l:44,r:8,t:14,b:14};
  var lo=Math.min.apply(0,C.map(function(r){return r.p5;})),hi=Math.max.apply(0,C.map(function(r){return r.p95;}));
  axes(x,pad,lo,hi,function(y){return '$'+Math.round(y);});
  var xmax=C[C.length-1].d,m;
  [['p95','rgba(56,189,248,.10)'],['p75','rgba(56,189,248,.16)']].forEach(function(band){
   var up=C.map(function(r){return [r.d,r[band[0]]];}),dn=C.slice().reverse().map(function(r){return [r.d,r[band[0]==='p95'?'p5':'p25']];});
   x.beginPath();up.concat(dn).forEach(function(p,i){var X=pad.l+(x.W-pad.l-pad.r)*p[0]/xmax,Y=pad.t+(x.H-pad.t-pad.b)*(1-(p[1]-lo)/(hi-lo));i?x.lineTo(X,Y):x.moveTo(X,Y);});
   x.closePath();x.fillStyle=band[1];x.fill();});
  m=line(x,C.map(function(r){return [r.d,r.p50];}),pad,lo,hi,0,xmax,'#38bdf8');
  var be=(v.dist||{}).be;if(be){x.save();x.setLineDash([4,4]);x.strokeStyle='#f5b45b';x.beginPath();x.moveTo(pad.l,m.Y(be));x.lineTo(x.W-pad.r,m.Y(be));x.stroke();x.restore();
   x.fillStyle='#f5b45b';x.textAlign='right';x.fillText('seuil '+$usd(be),x.W-10,m.Y(be)-4);}
  x.fillStyle='#6b7480';x.textAlign='center';x.fillText('jours →',x.W/2,x.H-2);}
 if(id==='cDist'&&v.dist){var x=ctx2d(id);if(!x)return;var P=v.dist.points.map(function(p){return [p.x,p.y];});
  var ymax=Math.max.apply(0,P.map(function(p){return p[1];})),xs=P.map(function(p){return p[0];});
  var xmin=Math.min.apply(0,xs),xmax=Math.max.apply(0,xs),pad={l:10,r:8,t:12,b:14},be=v.dist.be,sgn=(OL.research||{}).type==='PUT'?-1:1;
  // aire de profit
  x.beginPath();var started=false;P.forEach(function(p){var ok=sgn>0?p[0]>=be:p[0]<=be;if(!ok)return;
   var X=pad.l+(x.W-pad.l-pad.r)*(p[0]-xmin)/(xmax-xmin),Y=pad.t+(x.H-pad.t-pad.b)*(1-p[1]/ymax);
   started?x.lineTo(X,Y):x.moveTo(X,pad.t+(x.H-pad.t-pad.b));if(!started){x.lineTo(X,Y);started=true;}});
  if(started){x.lineTo(sgn>0?x.W-pad.r:pad.l+(x.W-pad.l-pad.r)*(be-xmin)/(xmax-xmin),pad.t+(x.H-pad.t-pad.b));x.closePath();x.fillStyle='rgba(34,197,94,.18)';x.fill();}
  var m=line(x,P,pad,0,ymax,xmin,xmax,'#a78bfa');
  vline(x,m,v.dist.spot,0,ymax,'#8794ab','titre');vline(x,m,be,0,ymax,'#f5b45b','seuil');
  x.fillStyle='#22c55e';x.textAlign=sgn>0?'right':'left';x.fillText('P(profit) '+$n(v.dist.p_be,1)+'%',sgn>0?x.W-12:12,pad.t+10);}
 if(id==='cTheta'&&v.theta){var x=ctx2d(id);if(!x)return;var P=v.theta.map(function(p){return [p.d,p.v];});
  var ys=P.map(function(p){return p[1];}),ymax=Math.max.apply(0,ys),pad={l:44,r:8,t:12,b:14};
  axes(x,pad,0,ymax,function(y){return '$'+Math.round(y);});
  line(x,P,pad,0,ymax,Math.max.apply(0,P.map(function(p){return p[0];})),0,'#ef4444','rgba(239,68,68,.10)');
  x.fillStyle='#6b7480';x.textAlign='center';x.fillText('← jours restants',x.W/2,x.H-2);}
 if(id==='cTerm'&&v.term){var x=ctx2d(id);if(!x)return;var T=v.term,pad={l:44,r:8,t:16,b:18};
  var vals=[];T.forEach(function(t){if(t.sym_iv!=null)vals.push(t.sym_iv);if(t.board_iv!=null)vals.push(t.board_iv);});
  var ymax=Math.max.apply(0,vals)*1.15||60;axes(x,pad,0,ymax,function(y){return Math.round(y)+'%';});
  var bw=(x.W-pad.l-pad.r)/T.length;
  T.forEach(function(t,i){var cx=pad.l+bw*i+bw/2,W=Math.min(34,bw/3);
   [[t.sym_iv,'#ff7a18',-W-3],[t.board_iv,'rgba(255,255,255,.28)',3]].forEach(function(b){if(b[0]==null)return;
    var h=(x.H-pad.t-pad.b)*b[0]/ymax;x.fillStyle=b[1];x.fillRect(cx+b[2],x.H-pad.b-h,W,h);});
   x.fillStyle='#8794ab';x.textAlign='center';x.fillText(t.bucket,cx,x.H-4);});
  x.fillStyle='#ff7a18';x.textAlign='left';x.fillText('■ titre',pad.l,10);x.fillStyle='#8794ab';x.fillText('■ board',pad.l+50,10);}
 if(id==='cRadar'&&v.radar){var x=ctx2d(id);if(!x)return;var ks=Object.keys(v.radar),n=ks.length,
  cx=x.W/2,cy=x.H/2+4,R=Math.min(x.W,x.H)/2-26;
  x.strokeStyle='rgba(255,255,255,.08)';[.33,.66,1].forEach(function(f){x.beginPath();
   for(var i=0;i<=n;i++){var a=-Math.PI/2+i*2*Math.PI/n,X=cx+Math.cos(a)*R*f,Y=cy+Math.sin(a)*R*f;i?x.lineTo(X,Y):x.moveTo(X,Y);}x.stroke();});
  x.beginPath();ks.forEach(function(k,i){var a=-Math.PI/2+i*2*Math.PI/n,f=(v.radar[k]||0)/100,
   X=cx+Math.cos(a)*R*f,Y=cy+Math.sin(a)*R*f;i?x.lineTo(X,Y):x.moveTo(X,Y);});x.closePath();
  x.fillStyle='rgba(255,122,24,.18)';x.fill();x.strokeStyle='#ff7a18';x.lineWidth=1.6;x.stroke();
  x.fillStyle='#aeb8c8';ks.forEach(function(k,i){var a=-Math.PI/2+i*2*Math.PI/n;x.textAlign=Math.cos(a)>.3?'left':Math.cos(a)<-.3?'right':'center';
   x.fillText(k,cx+Math.cos(a)*(R+11),cy+Math.sin(a)*(R+11)+3);});}
 if((id==='gPop'||id==='gConv')&&v.gauges){var x=ctx2d(id);if(!x)return;
  var val=id==='gPop'?v.gauges.pop:v.gauges.conviction,cx=x.W/2,cy=x.H-16,R=Math.min(x.W/2-14,x.H-34);
  x.lineWidth=11;x.lineCap='round';x.strokeStyle='rgba(255,255,255,.07)';x.beginPath();x.arc(cx,cy,R,Math.PI,2*Math.PI);x.stroke();
  x.strokeStyle=scol(val);x.beginPath();x.arc(cx,cy,R,Math.PI,Math.PI*(1+Math.max(0,Math.min(100,val||0))/100));x.stroke();
  x.fillStyle='#eef2f8';x.font='800 24px Inter';x.textAlign='center';x.fillText($n(val)+(id==='gPop'?'%':''),cx,cy-8);
  x.font='10px ui-monospace,Menlo,monospace';x.fillStyle='#8794ab';x.fillText(id==='gPop'?'probabilité de profit':'conviction /100',cx,cy+12);}
 }catch(e){}}

/* ───────── chapitres ───────── */
function s01(o){var m=[['Contrats',$n(o.contracts),'analysés'],['Entreprises',$n(o.tickers),'sous-jacents'],
 ['CALL',$n(o.calls),'haussiers'],['PUT',$n(o.puts),'baissiers / hedge'],['LEAPS',$n(o.leaps),'≥ 300 j'],
 ['Put/Call',$n(o.pcr,2),'équilibre du board'],['Volume total',$n(o.vol_total),'contrats échangés'],
 ['Open Interest',$n(o.oi_total),'positions ouvertes'],['IV moyenne',$n(o.iv_avg,1)+'%','prix de l\'incertitude'],
 ['POP moyenne',$n(o.pop_avg)+'%','probabilité de profit'],['R:R moyen',$n(o.rr_avg,2),'asymétrie moyenne'],
 ['Score moyen',$n(o.score_avg)+'/100','qualité du board']];
 var flow=(o.hot_flow||[]).map(function(f){return '<span class="pill p-info num" style="margin:0 6px 6px 0">🐋 '+f.sym+' · z='+f.vol_z+'</span>';}).join('');
 return sec('01','Options Market Overview','L\'état du marché des options en un regard : profondeur du board, prix de la volatilité, équilibre haussier/baissier, flux anormaux.',
  '<div class="met">'+m.map(function(x){return '<div><div class="lbl">'+x[0]+'</div><div class="v num">'+x[1]+'</div><div class="s">'+x[2]+'</div></div>';}).join('')+'</div>'
  +(flow?'<div style="margin-top:16px"><div class="lbl" style="margin-bottom:8px">Flux inhabituels (volume anormal du sous-jacent)</div>'+flow+'</div>':'')
  +ai(o.ai,'Comment se comporte le marché des options aujourd\'hui'));}

function s02(r){if(!r)return '';
 var kp=[['Score Vertex',$n(r.score)+'/100'],['Confiance',$n(r.confidence)+'%'],['POP',$n(r.pop)+'%'],
  ['Risk/Reward',$n(r.rr,2)],['Rendement attendu','+'+$n(r.expected_return)+'%'],['Prime',$usd(r.premium)],
  ['Prix actuel',$usd(r.spot)],['Break even',$usd(r.be)+' ('+($n(r.move_needed_pct,1))+'%)'],
  ['IV',$n(r.iv,1)+'%'],['Delta',$n(r.delta,2)],['Thêta/j',$n(r.theta_burn,2)+'%'],
  ['Open Interest',$n(r.oi)],['Volume',$n(r.vol)],['Spread',$n(r.spread_pct,1)+'%'],
  ['Durée estimée',$h(r.hold)],['Échéance',$h((r.exp||'').slice(0,10))+' · '+$n(r.dte)+'j']];
 var caps=(r.capital||[]).map(function(s){return '<span class="pill p-mut num" style="margin:8px 8px 0 0">'+s.label+' → '+s.contracts+' contrats ($'+$n(s.cost)+')</span>';}).join('');
 var th=(r.thesis||[]).map(function(t,i){return '<div><span class="n">0'+(i+1)+'</span><span>'+t.replace(/^(Pourquoi[^—]*—)/,'<b>$1</b>')+'</span></div>';}).join('');
 var dv=r.decision||{};
 var hz=(r.by_horizon||[]).map(function(h){return '<span class="pill p-mut num" style="margin:0 8px 8px 0;padding:6px 13px">'+h.sym+' '+h.type+' $'+$n(h.strike,1)+' · <b style="color:var(--ink)">'+h.bucket+'</b> · '+$n(h.score)+'</span>';}).join('');
 var run=(r.runners||[]).map(function(x,i){return '<div style="flex:1;min-width:200px;background:var(--bg2);border:1px solid var(--hair);border-radius:14px;padding:13px 15px">'
  +'<div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:15px">'+(i+2)+'ᵉ · '+x.sym+' <span style="font-size:10px;font-weight:800;color:'+(x.type==='PUT'?'var(--bad)':'var(--good)')+'">'+x.type+'</span></b>'
  +'<b class="num" style="font-size:16px;color:'+scol(x.score)+'">'+$n(x.score)+'</b></div>'
  +'<div style="font-size:11px;color:var(--mut);margin-top:4px" class="num">$'+$n(x.strike,1)+' · '+x.exp+' · POP '+$n(x.pop)+'% · coût '+$usd(x.cost)+' · si scénario → <b style="color:var(--good)">+'+$n(x.pot)+'%</b></div></div>';}).join('');
 return sec('02','Option Research','La meilleure opportunité parmi les contrats analysés — la fiche qui répond à tout : quoi, pourquoi, combien, jusqu\'à quand.',
  '<div class="panel" style="border-color:rgba(255,122,24,.28);box-shadow:0 0 60px -38px rgba(255,122,24,.55)">'
  +'<div style="display:flex;align-items:center;gap:10px;margin-bottom:16px"><span class="pill" style="background:linear-gradient(135deg,rgba(255,122,24,.22),rgba(255,122,24,.08));color:var(--acc2);font-size:11px;padding:6px 14px">💎 L\'OPTION DU JOUR</span><span style="font-size:11px;color:var(--mut)">la plus asymétrique des '+$n((OL.overview||{}).contracts)+' analysées</span></div>'
  +'<div class="hero"><div class="id">'
  +'<span class="pill '+(r.type==='PUT'?'p-bad':'p-good')+'">'+r.type+'</span> <span class="pill p-mut">'+$h(r.sector)+'</span>'
  +'<div class="tk">'+r.sym+' <span style="font-size:.4em;color:var(--mut);font-weight:700">$'+$n(r.strike,1)+' · '+$h((r.exp||'').slice(0,10))+'</span></div>'
  +'<div class="ln">'+$h(r.name||'')+(r.stock_verdict?' · titre : '+(window.VX?VX.verdictBadge(r.stock_verdict):$h(r.stock_verdict))+' ('+$n(r.stock_score)+'/100)':'')+'</div>'
  +(caps?'<div>'+caps+'</div>':'')+'</div>'
  +'<div class="verdict" style="background:linear-gradient(150deg,'+(dv.tone==='good'?'rgba(34,197,94,.10)':dv.tone==='warn'?'rgba(245,180,91,.09)':'rgba(239,68,68,.09)')+',transparent)">'
  +'<div class="lbl">Décision Vertex</div><div class="v" style="color:'+tone(dv.tone)+'">'+$h(dv.verdict)+'</div><div class="w">'+$h(dv.why)+'</div></div></div>'
  +'<div data-vx-chips="'+r.sym+'">'+(window.VX?VX.linkChips(r.sym):'')+'</div>'
  +(window.VX?VX.actionBar(r.sym,{}):'')
  +'<div class="kpis">'+kp.map(function(x){return '<div><div class="lbl">'+x[0]+'</div><div class="v num">'+x[1]+'</div></div>';}).join('')+'</div>'
  +'<div class="thesis"><div style="border:0;padding-top:18px" class="lbl">Thèse d\'investissement</div>'+th+'</div>'
  +ai(r.exec_summary,'Résumé exécutif')
  +(hz?'<div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--hair)"><div class="lbl" style="margin-bottom:10px">Aussi · la meilleure par horizon</div>'+hz+'</div>':'')
  +(run?'<div style="margin-top:14px"><div class="lbl" style="margin-bottom:10px">Les dauphines — juste derrière l\'option du jour</div><div style="display:flex;gap:12px;flex-wrap:wrap">'+run+'</div></div>':'')
  +'</div>');}

function s03(rows){if(!rows||!rows.length)return '';
 var h=rows.map(function(a){return '<div class="arow">'
  +'<div><div class="h">'+a.icon+' '+a.label+'</div>'+bar(a.score)+'<div class="snum">'+(a.score==null?'non couvert':a.score+'/100')+'</div></div>'
  +'<div><span class="pill '+(String(a.impact).match(/haussier|favorable|positif|soutient|porteur|accumulation|correcte|exécutable|équilibrés|temps/)?'p-good':String(a.impact).match(/baissier|défavorable|négatif|fragilise|essoufflé|distribution|chère|coûteuse|course/)?'p-bad':'p-mut')+'">'+a.impact+'</span>'
  +'<div class="imp lbl">importance '+a.importance+'</div></div>'
  +'<div class="txt">'+a.text+'</div>'
  +'<div class="rec"><b>RECOMMANDATION</b><br>'+a.reco+'</div></div>';}).join('');
 return sec('03','Analyse complète','Dix dimensions, une seule section : chaque ligne porte un score, un impact, une explication et une recommandation — lue dans le sens du trade.',
  '<div class="panel" style="padding-top:8px">'+h+'</div>');}

function s04(p){if(!p)return '';
 var steps=(p.steps||[]).map(function(s){return '<div><div class="dot" style="border-color:'+tone(s.tone)+'">'+'</div>'
  +'<div class="t">'+s.icon+' '+s.label+'</div><div class="x">'+s.text+'</div></div>';}).join('');
 var side='<div class="panel"><div class="lbl">Capital conseillé</div>'
  +((p.capital||[]).map(function(s){return '<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--hair);font-size:13px"><span>'+s.label+'</span><b class="num">'+s.contracts+' contrats · $'+$n(s.cost)+'</b></div>';}).join('')||'<div class="sub">—</div>')
  +(p.duration?'<div style="margin-top:14px"><div class="lbl">Durée</div><div style="font-size:14px;font-weight:700;margin-top:4px">'+p.duration+'</div></div>':'')
  +'<div style="margin-top:14px"><div class="lbl">Gestion</div><div style="font-size:12.5px;color:var(--ink2);line-height:1.6;margin-top:4px">'+$h(p.mgmt)+'</div></div></div>';
 return sec('04','Plan de trading','De l\'entrée à l\'expiration : chaque étape est écrite avant d\'engager le premier dollar.',
  '<div class="two"><div class="panel"><div class="tl" style="margin-top:6px">'+steps+'</div></div>'+side+'</div>'+ai(p.ai,'Conseil de gestion'));}

function s05(v){if(!v)return '';
 var heat='';
 if(v.heat&&v.heat.length){heat='<div class="chart" style="grid-column:1/-1"><div class="q">Heatmap du board — score · POP · R:R · IV · flux</div>'
  +'<div class="a">Où sont les meilleures combinaisons ? Vert = favorable (IV : vert = bon marché).</div><div class="tscroll"><table class="heat"><thead><tr><th>Titre</th><th>Score</th><th>POP</th><th>R:R</th><th>IV</th><th>Flux z</th></tr></thead><tbody>'
  +v.heat.map(function(r){return '<tr><td>'+r.sym+'</td>'
   +'<td><span class="hcell num" style="background:'+heatbg(r.score)+'">'+$n(r.score)+'</span></td>'
   +'<td><span class="hcell num" style="background:'+heatbg(r.pop==null?null:r.pop*1.6)+'">'+$n(r.pop)+'%</span></td>'
   +'<td><span class="hcell num" style="background:'+heatbg(r.rr==null?null:r.rr*80)+'">'+$n(r.rr,2)+'</span></td>'
   +'<td><span class="hcell num" style="background:'+heatbg(r.iv,true)+'">'+$n(r.iv,1)+'%</span></td>'
   +'<td><span class="hcell num" style="background:'+heatbg(r.flow==null?null:50+r.flow*25)+'">'+$n(r.flow,1)+'</span></td></tr>';}).join('')
  +'</tbody></table></div></div>';}
 var tiles='<div class="chart"><div class="q">Move attendu &amp; Kelly</div><div class="a">Quelle amplitude le marché price-t-il, et quelle taille est mathématiquement défendable ?</div>'
  +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:8px 0 14px">'
  +'<div><div class="lbl">Move attendu</div><div class="v num" style="font-size:24px;font-weight:800">±'+$n((v.em||{}).pct,1)+'%</div><div class="s" style="font-size:10.5px;color:var(--faint)">'+$usd((v.em||{}).lo)+' ↔ '+$usd((v.em||{}).hi)+'</div></div>'
  +'<div><div class="lbl">Fraction de Kelly</div><div class="v num" style="font-size:24px;font-weight:800">'+$n((v.kelly||{}).pct,1)+'%</div><div class="s" style="font-size:10.5px;color:var(--faint)">'+$h((v.kelly||{}).note)+'</div></div></div></div>';
 return sec('05','Visualisations','Aucun graphique décoratif : chacun répond à une question précise sur le trade vedette.',
  '<div class="gaugerow" style="margin-bottom:18px">'
  +'<div class="chart"><div class="q">Quelle chance de finir gagnant ?</div><div class="a">Jauge POP</div>'+cnv('gPop',120)+'</div>'
  +'<div class="chart"><div class="q">Quelle conviction du modèle ?</div><div class="a">Jauge de conviction</div>'+cnv('gConv',120)+'</div>'
  +'<div class="chart"><div class="q">Où sont les sensibilités ?</div><div class="a">Radar des greeks (normalisé)</div>'+cnv('cRadar',120)+'</div>'
  +'<div class="chart"><div class="q">L\'IV est-elle chère sur quelle échéance ?</div><div class="a">Structure par terme, titre vs board</div>'+cnv('cTerm',120)+'</div></div>'
  +'<div class="vgrid">'
  +chart('cPayoff','Combien gagne/perd ce contrat à l\'échéance ?','Payoff par contrat — seuil, prix actuel, cible technique.')
  +chart('cCone','Où le titre peut-il aller pendant la vie du contrat ?','Cône de probabilité log-normal (p5→p95) — le “Monte Carlo” exact, sans bruit.')
  +chart('cDist','Quelle probabilité de dépasser le seuil ?','Distribution du prix à l\'échéance ; l\'aire verte = zone de profit.')
  +chart('cTheta','Combien coûte chaque jour qui passe ?','Valeur théorique du contrat en fonction des jours restants (érosion thêta).')
  +tiles+heat+'</div>');}

function s06(st){if(!st||!st.items)return '';
 var rows=st.items.map(function(s){return '<div class="strow">'
  +'<div><div class="nm">'+s.name+' <span class="pill '+(s.fit==='recommandée'?'p-good':s.fit==='jouable'?'p-warn':'p-mut')+'" style="margin-left:6px">'+s.fit+'</span></div>'
  +'<div class="kd">'+s.kind+' · risque '+s.risk+' · potentiel '+s.potential+'</div></div>'
  +'<div>'+bar(s.score)+'<div class="snum">'+s.score+'/100</div></div>'
  +'<div class="cols"><div class="w"><b>Quand l\'utiliser</b>'+s.when+'</div><div class="av"><b>Quand l\'éviter</b>'+s.avoid+'</div><div class="cx"><b>Contexte idéal</b>'+s.context+'</div></div></div>';}).join('');
 return sec('06','Strategy Center','Seize structures notées contre le contexte du jour (régime, risk-on/off, cherté de l\'IV) — du covered call à l\'iron condor.',
  '<div class="panel" style="padding-top:8px">'+rows+'</div>'+ai(st.ai,'La structure du jour'));}

function s07(tops){if(!tops||!tops.length)return '';
 var g=tops.map(function(t){return '<div class="toplist"><div class="h">'+t.label+'</div>'
  +t.rows.map(function(r){return '<div class="r"><div class="l1">'+r.sym+' <span style="color:'+(r.type==='PUT'?'var(--bad)':'var(--good)')+';font-size:10px;font-weight:800">'+r.type+'</span> <span class="num" style="color:var(--mut);font-weight:600">$'+$n(r.strike,1)+' · '+r.exp+'</span></div>'
  +'<div class="kv">'+$n(r.score)+'/100 · POP '+$n(r.pop)+'% · R:R '+$n(r.rr,2)+'</div>'
  +'<div class="l2">'+r.note+'</div></div>';}).join('')+'</div>';}).join('');
 return sec('07','Top opportunités','Des listes, pas une grille : chaque classement répond à un style de trading différent.',
  '<div class="topgrid">'+g+'</div>');}

function s08(c){if(!c)return '';
 var rows=c.rows.map(function(r){return '<tr><td style="font-weight:700">'+r.name+'</td>'
  +'<td class="num">'+$usd(r.cost)+'</td><td class="num" style="color:var(--bad)">'+$usd(r.maxloss)+'</td>'
  +'<td class="num" style="color:var(--good)">'+(typeof r.maxgain==='string'?r.maxgain:$usd(r.maxgain))+'</td>'
  +'<td class="num cellbar">'+$n(r.pop)+'%'+bar(r.pop,'64px')+'</td><td class="num">'+$usd(r.be)+'</td>'
  +'<td style="color:var(--mut);font-size:11.5px">'+r.note+'</td></tr>';}).join('');
 return sec('08','Comparateur de véhicules','Action, CALL, PUT, LEAPS, covered call, cash-secured put, spreads : même thèse, huit façons de la jouer — sur '+c.sym+'.',
  '<div class="panel"><div class="tscroll"><table><thead><tr><th>Véhicule</th><th>Coût</th><th>Perte max</th><th>Gain max</th><th>POP est.</th><th>Break even</th><th>Lecture</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
  +'<div style="font-size:10.5px;color:var(--faint);margin-top:10px">'+$h(c.note)+'</div>'+ai(c.verdict,'Le véhicule préférable')+'</div>');}

function s09(rows){if(!rows||!rows.length)return '';
 var h=rows.map(function(r){return '<tr><td style="font-weight:700;white-space:nowrap">'+r.title+'</td>'
  +'<td style="font-weight:700;color:var(--acc2);white-space:nowrap">'+$h(r.winner)+'</td>'
  +'<td class="num" style="white-space:nowrap">'+$h(r.value)+'</td>'
  +'<td style="color:var(--ink2);font-size:12px">'+$h(r.why)+'</td></tr>';}).join('');
 return sec('09','Comité Vertex','Le grand tableau des « meilleurs » : une ligne = un titre de champion, son gagnant et la raison du verdict.',
  '<div class="panel"><div class="tscroll"><table><thead><tr><th>Catégorie</th><th>Gagnant</th><th>Valeur</th><th>Pourquoi</th></tr></thead><tbody>'+h+'</tbody></table></div></div>');}

function s10(rows){if(!rows||!rows.length)return '';
 var h=rows.map(function(r){var lv=r.level==='ÉLEVÉ'?'p-bad':r.level==='MOYEN'?'p-warn':'p-good';
  return '<tr><td style="font-weight:700">'+r.name+'</td><td><span class="pill '+lv+'">'+r.level+'</span></td>'
  +'<td style="color:var(--ink2);font-size:12px">'+r.impact+'</td><td style="color:var(--mut);font-size:12px">'+r.proba+'</td>'
  +'<td style="color:var(--ink2);font-size:12px;border-left:2px solid rgba(34,197,94,.35);padding-left:12px">'+r.fix+'</td></tr>';}).join('');
 return sec('10','Matrice des risques','Chaque risque est nommé, mesuré, et surtout : neutralisé par une règle concrète.',
  '<div class="panel"><div class="tscroll"><table><thead><tr><th>Risque</th><th>Niveau</th><th>Impact</th><th>Probabilité</th><th>Solution</th></tr></thead><tbody>'+h+'</tbody></table></div></div>');}

function s11(tl){if(!tl||!tl.length)return '';
 var h=tl.map(function(t){return '<div><div class="w">'+$h(t.when)+' · '+$h(t.date)+'</div>'
  +'<div class="t" style="color:'+tone(t.tone)+'">'+t.icon+' '+t.label+'</div><div class="x">'+t.text+'</div></div>';}).join('');
 return sec('11','Timeline','L\'échéancier concret du trade : checkpoints, fenêtres de sortie, dates à risque.',
  '<div class="htl">'+h+'</div>');}

/* ───────── assemblage ───────── */
function olabRender(){var d=OL;if(!d)return;
 var head=document.getElementById('olabHead');
 if(d.empty){document.getElementById('olabRoot').innerHTML='<div class="skel">Le board d\'options n\'est pas encore chargé — le scan tourne, recharge dans un instant.</div>';return;}
 var o=d.overview||{};
 head.innerHTML='<b>'+$n(o.contracts)+'</b> contrats · <b>'+$n(o.tickers)+'</b> entreprises · IV '+$n(o.iv_avg,1)+'% · '
  +(d.demo?'<span style="color:var(--vio)">🎭 DÉMO</span>':'chaînes réelles')+(d.as_of?' · MAJ '+d.as_of:'');
 document.getElementById('olabRoot').innerHTML=
  s01(o)+s02(d.research)+s03(d.analysis)+s04(d.plan)+s05(d.viz)+s06(d.strategies)
  +s07(d.tops)+s08(d.comparator)+s09(d.committee)+s10(d.risks)+s11(d.timeline)
  +'<div class="foot">⚠️ <b>Analyse éducative</b> — une option achetée peut perdre 100 % de sa prime · les probabilités sont des estimations de modèle, pas des promesses · '
  +'<b>aucun ordre n\'est passé ni passable depuis Vertex</b> · sources : '+$h(o.source)+'.</div>';
 OLDRAWN={};lazyDraw();if(window.VX)VX.init();}

async function olabLoad(force){try{
 if(force){var b=document.querySelector('#olab .vbtn');if(b){b.textContent='⟳ Analyse…';setTimeout(function(){b.textContent='⟳ Actualiser';},1500);}}
 var r=await fetch('/api/options-lab');if(r.status===401){location.href='/login?next=/options';return;}
 OL=await r.json();olabRender();
}catch(e){document.getElementById('olabRoot').innerHTML='<div class="skel">Erreur de chargement — nouvelle tentative dans 5 s…</div>';setTimeout(olabLoad,5000);}}
olabLoad();setInterval(function(){if(!document.hidden)olabLoad();},120000);

/* ═══ FOCUS TITRE (?t=SYM) — les boutons « 💎 Options » de toute l'app scoprent ici ═══ */
(function olabSymFocus(){
 var t=(new URLSearchParams(location.search).get('t')||'').toUpperCase();
 if(!/^[A-Z.\-]{1,8}$/.test(t))return;
 var host=document.getElementById('olabSym');if(!host)return;
 host.innerHTML='<div class="panel" style="margin:14px 0 6px;border-color:rgba(56,189,248,.3)">'
  +'<div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap"><h2 style="margin:0;font-size:20px">🎯 Options sur '+t+'</h2>'
  +'<a href="/titre/'+t+'" style="color:#38bdf8;font-size:12px;font-weight:700;text-decoration:none">📄 Fiche '+t+' →</a></div>'
  +'<div id="olabSymBody" class="sub" style="margin:10px 0 0">analyse du board pour '+t+'…</div>'
  +'<div data-vx-actions="'+t+'" data-hidejournal></div></div>';
 if(window.VX)VX.init();
 fetch('/api/options-for/'+t).then(function(r){return r.json();}).then(function(d){
  var b=document.getElementById('olabSymBody');if(!b)return;
  if(!d||!d.suggestions||!d.suggestions.length){b.innerHTML=(d&&d.note)||('Aucun contrat chargé pour '+t+' — le board se remplit au fil du scan (reviens dans ~5 min).');return;}
  b.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:4px">'
   +d.suggestions.map(function(x){var col=x.type==='PUT'?'#ef4444':'#22c55e';
    return '<div style="background:var(--bg2);border:1px solid var(--hair);border-radius:14px;padding:12px 14px">'
     +'<div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:12.5px">'+x.role_label+'</b><b class="num" style="color:'+scol(x.score)+'">'+$n(x.score)+'/100</b></div>'
     +'<div class="num" style="font-size:12px;color:var(--ink2);margin-top:5px"><span style="color:'+col+';font-weight:800">'+x.type+'</span> $'+$n(x.strike,1)+' · '+(x.exp||'—')+(x.dte!=null?' · '+x.dte+'j':'')+'</div>'
     +'<div class="num" style="font-size:11px;color:var(--mut);margin-top:3px">prime '+$usd(x.premium)+' · POP '+$n(x.pop)+'%'+(x.grade?' · '+x.grade:'')+'</div>'
     +'<div style="font-size:11px;color:var(--mut);margin-top:5px;line-height:1.45">'+(x.why||'')+'</div></div>';}).join('')+'</div>';
 }).catch(function(){});
})();
"""

__all__ = ['CSS', 'BODY', 'JS']
