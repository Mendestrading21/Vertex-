"""
vertex/ui/signals.py — MARKET SIGNALS (page refondue).

Le sonar de Vertex : tous les comportements hors-norme détectés par le scan
(volume, cassures, squeezes, divergences…), organisés en chapitres :

① Le pouls — anneau haussiers/baissiers, familles de signaux, lecture Vertex
② Le radar — nuage qualité du titre × intensité du signal (SVG cliquable) :
   la zone d'or est en haut à droite
③ Meilleures opportunités — signal haussier × qualité du titre
④ Tous les signaux — filtres + table premium avec barres d'intensité

Données : /scan (anomalies, rows, detail). ⭐ suivre / 💎 option conservés.
Analyse uniquement — un signal n'est jamais un ordre.
"""

CSS = r"""
#sg{--acc:#ff7a18;--acc2:#ff9a3d;--good:#22c55e;--bad:#ef4444;--info:#38bdf8;--warn:#f5b45b;--vio:#a78bfa;
 --ink:#eef2f8;--ink2:#aeb8c8;--mut:#8794ab;--faint:#4b5563;--surf:#101218;--bg2:#0b0d12;
 --hair:rgba(255,255,255,.07);--hair2:rgba(255,255,255,.12);
 --mono:ui-monospace,'SF Mono',Menlo,monospace;--sp:clamp(40px,5vw,60px);color:var(--ink);display:block}
#sg .num{font-variant-numeric:tabular-nums}
#sg section{padding:var(--sp) 0 0}
#sg .eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:12px}
#sg .eyebrow .rn{font-family:var(--mono);color:#FF9A3D;background:linear-gradient(135deg,rgba(255,122,24,.16),rgba(255,122,24,.05));border:1px solid rgba(255,122,24,.35);padding:6px 9px;border-radius:9px;letter-spacing:1.5px}
#sg .eyebrow::after{content:"";flex:1;height:2px;background:linear-gradient(90deg,rgba(255,122,24,.4),transparent);border-radius:2px}
#sg h2{font-size:clamp(20px,2.4vw,26px);font-weight:800;letter-spacing:-.02em;margin:0 0 6px;
 background:linear-gradient(180deg,#f7fafc,#c7d0dd);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
#sg .sub{color:var(--mut);font-size:12.5px;max-width:70ch;margin-bottom:18px}
#sg .panel{background:linear-gradient(170deg,var(--surf),var(--bg2));border:1px solid var(--hair);border-radius:18px;padding:20px 22px}
#sg .aiq{display:flex;gap:12px;align-items:flex-start;margin-top:16px;padding:13px 16px;background:linear-gradient(120deg,rgba(255,122,24,.09),rgba(255,122,24,.02));border:1px solid rgba(255,122,24,.16);border-left:2.5px solid var(--acc);border-radius:13px;font-size:13px;line-height:1.6;color:var(--ink2)}
#sg .aiq b{color:var(--ink)}
#sg .aiq .ico{flex:none;width:22px;height:22px;border-radius:7px;background:rgba(255,122,24,.16);display:grid;place-items:center;font-size:12px}
#sg .lbl{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
#sg .pulse{display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center}
#sg .fam{display:flex;flex-direction:column;gap:9px}
#sg .fam>div{display:grid;grid-template-columns:150px 1fr 44px;gap:12px;align-items:center;font-size:12.5px}
#sg .fam .bar{height:7px;border-radius:99px;background:rgba(255,255,255,.05);overflow:hidden}
#sg .fam .bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--acc),var(--acc2))}
#sg .radar-wrap{position:relative}
#sg .radar-wrap svg{width:100%;height:380px;display:block}
#sg .dot{cursor:pointer;transition:r .12s}
#sg .dot:hover{stroke:#fff;stroke-width:1.5}
#sg .opp{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:13px}
#sg .oppc{background:var(--bg2);border:1px solid var(--hair);border-radius:15px;padding:13px 15px;cursor:pointer;transition:transform .15s,border-color .15s}
#sg .oppc:hover{transform:translateY(-2px);border-color:rgba(34,197,94,.45)}
#sg table{width:100%;border-collapse:collapse;font-size:12.6px}
#sg th{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);font-weight:800;padding:9px 10px;border-bottom:1px solid var(--hair2);white-space:nowrap}
#sg td{padding:10px;border-bottom:1px solid var(--hair);vertical-align:middle}
#sg tr:last-child td{border-bottom:0}
#sg tbody tr{cursor:pointer;transition:background .12s}
#sg tbody tr:hover{background:rgba(255,255,255,.03)}
#sg .ibar{width:70px;height:6px;border-radius:99px;background:rgba(255,255,255,.06);overflow:hidden;display:inline-block;vertical-align:middle}
#sg .ibar i{display:block;height:100%;border-radius:99px}
#sg .pill{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:800;padding:3px 9px;border-radius:999px;white-space:nowrap}
#sg .tscroll{overflow-x:auto}
@media(max-width:860px){#sg .pulse{grid-template-columns:1fr}#sg .fam>div{grid-template-columns:110px 1fr 40px}}
"""

BODY = (
  '<div id="sg">'
  '<div class="vhead"><div><h1>📡 Market Signals</h1>'
  '<div class="s" id="sgHead">le sonar écoute le marché…</div></div></div>'
  '<div id="sgRoot"><div style="padding:50px;text-align:center;color:#8794ab">Chargement des signaux…</div></div>'
  '</div>')

JS = r"""
var SG_ALL=[],SG_ROWS={},SG_DET={},SG_F='all';
function sgN(x,d){return x==null?'—':Number(x).toLocaleString('fr-FR',{maximumFractionDigits:d||0});}
function sgDirCol(d){return d==='UP'?'#22C55E':d==='DOWN'?'#EF4444':'#F5B45B';}
function sgScol(s){return s==null?'#8794ab':s>=72?'#22C55E':s>=55?'#F5B45B':'#EF4444';}
function sgEyebrow(n,t){return '<div class="eyebrow"><span class="rn">'+n+'</span>'+t+'</div>';}
function sgSec(n,t,sub,inner){return '<section>'+sgEyebrow(n,t.toUpperCase())+'<h2>'+t+'</h2><div class="sub">'+sub+'</div>'+inner+'</section>';}
function sgAi(txt,lab){return txt?'<div class="aiq"><div class="ico">▲</div><div><b>'+(lab||'Lecture Vertex')+' — </b>'+txt+'</div></div>':'';}
/* ⭐ suivre & 💎 option (comportement historique conservé) */
function vxFollowStk(sym,spot,stop,tgt){try{var a=JSON.parse(localStorage.getItem('myRecos')||'[]');
 for(var i=0;i<a.length;i++){if(a[i].kind==='STK'&&a[i].sym===sym){
   if(confirm('⭐ '+sym+' est déjà suivi — le RETIRER du suivi ?')){a.splice(i,1);localStorage.setItem('myRecos',JSON.stringify(a));localStorage.setItem('deskTs',String(Date.now()));alert(sym+' retiré du suivi ✓');}
   return;}}
 a.push({id:Date.now(),kind:'STK',sym:sym,entry_spot:spot||null,stop:stop||null,tgt:tgt||null,followed:new Date().toISOString().slice(0,10)});
 localStorage.setItem('myRecos',JSON.stringify(a));localStorage.setItem('deskTs',String(Date.now()));
 alert('⭐ Suivi : '+sym+' — retrouve-le sur le Trading Desk.');}catch(e){}}
function sgStar(sym){var r=SG_ROWS[sym]||{},pl=(SG_DET[sym]||{}).plan||{};
 return '<span title="Suivre jusqu\'à la vente" onclick="event.stopPropagation();vxFollowStk(\''+sym+'\','+(r.price!=null?r.price:'null')+','+(pl.stop!=null?pl.stop:'null')+','+(pl.tp2!=null?pl.tp2:'null')+')" style="cursor:pointer;color:#F5B45B">⭐</span>';}
function sgOptBtn(sym){return '<span title="Analyser en option" onclick="event.stopPropagation();location.href=\'/options?t='+sym+'\'" style="cursor:pointer;color:#A78BFA">💎</span>';}

/* ① le pouls */
function sgPulse(){var n=SG_ALL.length,up=SG_ALL.filter(function(x){return x.dir==='UP';}).length;
 var pct=n?Math.round(up/n*100):0,c=pct>=55?'#22C55E':pct>=40?'#F5B45B':'#EF4444';
 var r=52,C=2*Math.PI*r,off=C*(1-pct/100);
 var ring='<svg width="150" height="150" viewBox="0 0 130 130"><circle cx="65" cy="65" r="'+r+'" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="11"/>'
  +'<circle cx="65" cy="65" r="'+r+'" fill="none" stroke="'+c+'" stroke-width="11" stroke-linecap="round" stroke-dasharray="'+C.toFixed(1)+'" stroke-dashoffset="'+off.toFixed(1)+'" transform="rotate(-90 65 65)" style="filter:drop-shadow(0 0 8px '+c+'66)"/>'
  +'<text x="65" y="62" text-anchor="middle" font-size="24" font-weight="800" fill="#eef2f8">'+pct+'%</text>'
  +'<text x="65" y="80" text-anchor="middle" font-size="8.5" fill="#8794ab">HAUSSIERS</text></svg>';
 var by={};SG_ALL.forEach(function(x){var k=x.label||x.code;if(!by[k])by[k]={n:0,up:0};by[k].n++;if(x.dir==='UP')by[k].up++;});
 var fams=Object.keys(by).sort(function(a,b){return by[b].n-by[a].n;}).slice(0,7);
 var mx=fams.length?by[fams[0]].n:1;
 var rows=fams.map(function(k){var f=by[k];
  return '<div><span style="color:var(--ink2);font-weight:700">'+k+'</span>'
   +'<span class="bar"><i style="width:'+Math.round(f.n/mx*100)+'%"></i></span>'
   +'<b class="num" style="text-align:right">'+f.n+'</b></div>';}).join('');
 var ai=(n===0)?null:('Le sonar relève '+n+' comportements hors-norme : '+up+' haussiers, '+(n-up)+' baissiers ou avertissements ('+pct+'% de biais acheteur — '
  +(pct>=55?'le marché accumule, les cassures ont du carburant':pct>=40?'équilibre — trier signal par signal':'la distribution domine, prudence sur les achats de cassure')+'). '
  +'Famille dominante : '+(fams[0]||'—')+'.');
 return '<div class="panel"><div class="pulse"><div style="text-align:center">'+ring+'<div class="lbl" style="margin-top:4px">'+up+' 🟢 · '+(n-up)+' 🔴</div></div>'
  +'<div class="fam"><div class="lbl" style="margin-bottom:2px">Familles de signaux</div>'+rows+'</div></div>'+sgAi(ai)+'</div>';}

/* ② le radar (SVG cliquable) */
function sgRadar(){var pts=[];var seen={};
 SG_ALL.forEach(function(x){var r=SG_ROWS[x.symbol]||{};if(r.score==null||x.score_anom==null)return;
  var k=x.symbol;if(seen[k]&&seen[k].a>=x.score_anom)return;seen[k]={s:r.score,a:x.score_anom,d:x.dir,label:x.label,sym:x.symbol};});
 pts=Object.keys(seen).map(function(k){return seen[k];});
 if(pts.length<3)return '<div class="panel" style="text-align:center;color:var(--mut);padding:30px">Pas assez de signaux notés pour le radar.</div>';
 var W=980,H=360,padL=52,padB=34,padT=18,padR=16;
 var X=function(v){return padL+(W-padL-padR)*Math.max(0,Math.min(100,v))/100;};
 var Y=function(v){return padT+(H-padT-padB)*(1-Math.max(0,Math.min(100,v))/100);};
 var grid='';[0,25,50,75,100].forEach(function(v){
  grid+='<line x1="'+X(v)+'" y1="'+Y(0)+'" x2="'+X(v)+'" y2="'+Y(100)+'" stroke="rgba(255,255,255,.05)"/>'
   +'<line x1="'+X(0)+'" y1="'+Y(v)+'" x2="'+X(100)+'" y2="'+Y(v)+'" stroke="rgba(255,255,255,.05)"/>'
   +'<text x="'+X(v)+'" y="'+(H-14)+'" text-anchor="middle" font-size="9" fill="#5d6673">'+v+'</text>'
   +'<text x="'+(padL-8)+'" y="'+(Y(v)+3)+'" text-anchor="end" font-size="9" fill="#5d6673">'+v+'</text>';});
 var zone='<rect x="'+X(60)+'" y="'+Y(100)+'" width="'+(X(100)-X(60))+'" height="'+(Y(60)-Y(100))+'" fill="rgba(34,197,94,.05)" stroke="rgba(34,197,94,.25)" stroke-dasharray="5 5" rx="8"/>'
  +'<text x="'+(X(80))+'" y="'+(Y(97))+'" text-anchor="middle" font-size="10" font-weight="800" fill="#22C55E" opacity=".8">ZONE D\'OR — titre fort × signal fort</text>';
 var dots=pts.map(function(p){var c=sgDirCol(p.d);
  return '<circle class="dot" cx="'+X(p.s).toFixed(1)+'" cy="'+Y(p.a).toFixed(1)+'" r="'+(p.a>=70?8:6)+'" fill="'+c+'" fill-opacity=".72" stroke="'+c+'" onclick="location.href=\'/titre/'+p.sym+'\'"><title>'+p.sym+' — '+p.label+' · intensité '+p.a+' · score titre '+p.s+'</title></circle>'
   +((p.a>=62&&p.s>=60)?'<text x="'+X(p.s).toFixed(1)+'" y="'+(Y(p.a)-11).toFixed(1)+'" text-anchor="middle" font-size="10" font-weight="800" fill="#eef2f8">'+p.sym+'</text>':'');}).join('');
 return '<div class="panel radar-wrap"><svg viewBox="0 0 '+W+' '+H+'">'+grid+zone+dots
  +'<text x="'+((padL+W-padR)/2)+'" y="'+(H-2)+'" text-anchor="middle" font-size="9.5" fill="#8794ab">QUALITÉ DU TITRE (score Vertex) →</text>'
  +'<text x="12" y="'+((padT+H-padB)/2)+'" text-anchor="middle" font-size="9.5" fill="#8794ab" transform="rotate(-90 12 '+((padT+H-padB)/2)+')">INTENSITÉ DU SIGNAL →</text></svg>'
  +'<div style="display:flex;gap:16px;font-size:11px;color:var(--mut);margin-top:8px"><span>🟢 haussier</span><span>🔴 baissier</span><span>🟡 avertissement</span><span>· survole un point, clique → fiche</span></div></div>';}

/* ③ meilleures opportunités */
function sgOpps(){var seen={};
 SG_ALL.filter(function(x){return x.dir==='UP';}).forEach(function(x){var r=SG_ROWS[x.symbol]||{};var sc=r.score||0;
  var opp=Math.round((x.score_anom||0)*0.45+sc*0.55);
  if(!seen[x.symbol]||seen[x.symbol].opp<opp)seen[x.symbol]={x:x,sc:sc,opp:opp,verdict:r.verdict};});
 var list=Object.keys(seen).map(function(k){return seen[k];}).sort(function(a,b){return b.opp-a.opp;}).slice(0,6);
 if(!list.length)return '<div class="panel" style="text-align:center;color:var(--mut);padding:26px">Aucun signal haussier exploitable pour l\'instant.</div>';
 return '<div class="opp">'+list.map(function(o){
  return '<div class="oppc" onclick="location.href=\'/titre/'+o.x.symbol+'\'">'
   +'<div style="display:flex;align-items:center;gap:8px"><b style="font-size:16px">'+o.x.symbol+'</b>'
   +'<span class="pill" style="background:rgba(34,197,94,.13);color:#22C55E">'+o.x.label+'</span>'
   +'<span style="margin-left:auto;text-align:right"><span class="lbl">Opportunité</span><br><b class="num" style="font-size:19px;color:#22C55E">'+o.opp+'</b></span></div>'
   +'<div style="font-size:11.5px;color:var(--ink2);margin-top:8px;line-height:1.5">'+(o.x.note||'')+'</div>'
   +'<div style="display:flex;gap:10px;margin-top:9px;padding-top:8px;border-top:1px solid var(--hair);font-size:11px;color:var(--mut)">Score titre <b style="color:'+sgScol(o.sc)+'">'+o.sc+'</b>'+(o.verdict?'<span>· '+o.verdict+'</span>':'')+'<span style="margin-left:auto;display:flex;gap:8px">'+sgStar(o.x.symbol)+sgOptBtn(o.x.symbol)+'</span></div></div>';}).join('')+'</div>';}

/* ④ tous les signaux (table premium) */
function sgTable(){var by={};SG_ALL.forEach(function(x){by[x.code]=(by[x.code]||0)+1;});
 var lab={};SG_ALL.forEach(function(x){lab[x.code]=x.label;});
 var nUp=SG_ALL.filter(function(x){return x.dir==='UP';}).length,nRk=SG_ALL.length-nUp;
 var chip=function(l,on,f,c){return '<button class="vbtn'+(on?' pri':'')+'" '+(c?'style="border-color:'+c+'55;color:'+c+(on?';background:'+c+'22':'')+'"':'')+' onclick="sgSetF(\''+f+'\')">'+l+'</button>';};
 var pills='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:13px">'
  +chip('Tous · '+SG_ALL.length,SG_F==='all','all')
  +chip('🟢 Opportunités · '+nUp,SG_F==='up','up','#22C55E')
  +chip('🔴 Risques · '+nRk,SG_F==='risk','risk','#EF4444')
  +Object.keys(by).sort(function(a,b){return by[b]-by[a];}).map(function(c){return chip((lab[c]||c)+' · '+by[c],SG_F===c,c);}).join('')+'</div>';
 var list=SG_ALL.slice();
 if(SG_F==='up')list=list.filter(function(x){return x.dir==='UP';});
 else if(SG_F==='risk')list=list.filter(function(x){return x.dir!=='UP';});
 else if(SG_F!=='all')list=list.filter(function(x){return x.code===SG_F;});
 list.sort(function(a,b){return (b.score_anom||0)-(a.score_anom||0);});
 var rows=list.map(function(x){var c=sgDirCol(x.dir),r=SG_ROWS[x.symbol]||{};
  return '<tr onclick="location.href=\'/titre/'+x.symbol+'\'">'
   +'<td style="font-weight:800;font-size:13.5px">'+x.symbol+'</td>'
   +'<td><span class="pill" style="background:'+c+'1a;color:'+c+'">'+(x.dir==='UP'?'▲':x.dir==='DOWN'?'▼':'⚠')+' '+x.label+'</span></td>'
   +'<td class="num"><span class="ibar"><i style="width:'+Math.max(4,Math.min(100,x.score_anom||0))+'%;background:'+c+'"></i></span> <b style="color:'+c+'">'+(x.score_anom!=null?x.score_anom:'—')+'</b></td>'
   +'<td class="num" style="color:'+sgScol(r.score)+';font-weight:700">'+(r.score!=null?r.score:'—')+'</td>'
   +'<td style="color:var(--mut);font-size:11.8px;max-width:420px">'+(x.note||'')+'</td>'
   +'<td style="white-space:nowrap;font-size:13px">'+sgStar(x.symbol)+' '+sgOptBtn(x.symbol)+'</td></tr>';}).join('');
 return pills+'<div class="panel" style="padding:6px 16px"><div class="tscroll"><table><thead><tr><th>Titre</th><th>Signal</th><th>Intensité</th><th>Score titre</th><th>Lecture</th><th></th></tr></thead><tbody>'
  +(rows||'<tr><td colspan="6" style="text-align:center;color:var(--mut);padding:22px">Aucun signal dans ce filtre.</td></tr>')+'</tbody></table></div></div>';}

window.sgSetF=function(f){SG_F=f;var el=document.getElementById('sgTableSec');if(el)el.innerHTML=sgTable();};
function sgRender(){
 document.getElementById('sgHead').innerHTML='<b style="color:#C9D2E0">'+SG_ALL.length+'</b> signaux hors-norme détectés par le scan · MAJ continue';
 document.getElementById('sgRoot').innerHTML=
  sgSec('01','Le pouls','Combien de signaux, dans quel sens, et dans quelles familles — l\'humeur du sonar en un regard.',sgPulse())
  +sgSec('02','Le radar','Chaque point est un titre : à droite les titres de qualité, en haut les signaux intenses — la zone d\'or combine les deux.',sgRadar())
  +sgSec('03','Meilleures opportunités','Signal haussier × qualité du titre : ce que le sonar recommande d\'ouvrir en premier.',sgOpps())
  +sgSec('04','Tous les signaux','Filtre par famille ou par direction — chaque ligne mène à la fiche complète.','<div id="sgTableSec">'+sgTable()+'</div>')
  +'<div style="margin-top:40px;padding-top:13px;border-top:1px solid var(--hair);font-size:11px;color:var(--faint)">⚠️ Un signal est une <b style="color:var(--mut)">anomalie statistique</b>, pas une recommandation — croiser avec la fiche du titre · analyse uniquement, aucun ordre.</div>';}
function sgLoad(){fetch('/scan').then(function(r){return r.json();}).then(function(d){
 SG_ALL=d.anomalies||[];SG_ROWS={};(d.rows||[]).forEach(function(r){SG_ROWS[r.symbol]=r;});SG_DET=d.detail||{};
 sgRender();}).catch(function(){setTimeout(sgLoad,5000);});}
sgLoad();setInterval(function(){if(!document.hidden)sgLoad();},60000);
"""

__all__ = ['CSS', 'BODY', 'JS']
