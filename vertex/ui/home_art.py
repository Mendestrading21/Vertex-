"""
vertex/ui/home_art.py — MARKET OVERVIEW · couche artistique (Ch. IV/XI).

Un habillage « salle de marché » appliqué PAR-DESSUS la page d'accueil,
sans toucher à ses données ni à ses rendus existants :

• ambiance : halos orange/bleu + grille fine en toile de fond (fixe)
• chapitres : numéro en jeton orange, titres plus grands, règle dégradée
• panneaux : hover premium (élévation + liseré), sélection, scrollbar
• « La séance en images » : un tableau de bord graphique injecté sous
  Le Marché — grand S&P 500, Nasdaq & Dow en aires, VIX (peur) — nourri
  par /api/market/summary (léger), canvas haute densité
• apparition douce des sections au défilement (progressive enhancement :
  tout reste visible si le JS ne tourne pas)

Analyse uniquement — cette couche ne fait que dessiner.
"""

ART_CSS = r"""
/* ── ambiance salle de marché ── */
body{background:
 radial-gradient(1100px 520px at 78% -160px,rgba(255,122,24,.075),transparent 60%),
 radial-gradient(900px 560px at -12% 34%,rgba(56,189,248,.05),transparent 55%),
 radial-gradient(700px 500px at 108% 78%,rgba(167,139,250,.04),transparent 55%),
 #0b0e14 !important}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
 background-image:linear-gradient(rgba(255,255,255,.022) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,255,255,.022) 1px,transparent 1px);
 background-size:56px 56px;
 -webkit-mask-image:radial-gradient(900px 460px at 60% 0,#000 30%,transparent 75%);
 mask-image:radial-gradient(900px 460px at 60% 0,#000 30%,transparent 75%)}
::selection{background:rgba(255,122,24,.32);color:#fff}
*{scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.14) transparent}
*::-webkit-scrollbar{width:9px;height:9px}
*::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:9px}
*::-webkit-scrollbar-thumb:hover{background:rgba(255,122,24,.35)}
/* ── chapitres éditoriaux ── */
.ovchap{margin:64px 2px 22px!important;align-items:center!important}
.ovchap .n{color:#FF9A3D!important;background:linear-gradient(135deg,rgba(255,122,24,.16),rgba(255,122,24,.05));
 border:1px solid rgba(255,122,24,.35);padding:7px 10px 6px!important;border-radius:10px;
 font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:11px!important;letter-spacing:1.5px!important;
 box-shadow:0 0 22px -8px rgba(255,122,24,.55)}
.ovchap .t{font-size:clamp(23px,2.5vw,29px)!important;letter-spacing:-.02em!important;
 background:linear-gradient(180deg,#f7fafc,#c7d0dd);-webkit-background-clip:text;background-clip:text;
 -webkit-text-fill-color:transparent}
.ovchap .s{font-size:10px!important;letter-spacing:.14em;text-transform:uppercase;color:#5d6673!important;margin-top:6px!important;font-weight:700}
.ovchap .ln{height:2px!important;background:linear-gradient(90deg,rgba(255,122,24,.45),rgba(255,255,255,.05) 55%,transparent)!important;border-radius:2px}
.ovsub{color:#FF9A3D!important;letter-spacing:.16em!important}
.ovsub::before{content:"— "}
/* ── panneaux premium ── */
.hero,.scard{border-radius:18px!important;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.hero:hover,.scard:hover{transform:translateY(-2px);border-color:rgba(255,122,24,.26)!important;
 box-shadow:0 22px 48px -30px rgba(0,0,0,.9),0 0 34px -20px rgba(255,122,24,.4)}
.hero{background:linear-gradient(160deg,#14161d,#0c0e13)!important;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;top:-70px;right:-60px;width:240px;height:240px;pointer-events:none;
 background:radial-gradient(closest-side,rgba(255,122,24,.13),transparent);border-radius:50%}
/* ── apparition douce (uniquement si le JS a ajouté .artjs) ── */
.artjs .ovchap,.artjs .ovc{opacity:0;transform:translateY(16px);transition:opacity .55s ease,transform .55s ease}
.artjs .ovchap.artin,.artjs .ovc.artin{opacity:1;transform:none}
/* ── La séance en images ── */
#artBoard{display:grid;grid-template-columns:1.7fr 1fr 1fr;gap:14px;margin:14px 0 6px}
#artBoard .ac{background:linear-gradient(168deg,#12141b,#0b0d12);border:1px solid rgba(255,255,255,.09);
 border-radius:16px;padding:14px 15px 8px;transition:border-color .18s}
#artBoard .ac:hover{border-color:rgba(255,122,24,.3)}
#artBoard .hd{display:flex;align-items:baseline;gap:9px}
#artBoard .hd .t{font-size:12px;font-weight:800;letter-spacing:.4px}
#artBoard .hd .v{margin-left:auto;font-size:16px;font-weight:800;font-variant-numeric:tabular-nums}
#artBoard .hd .c{font-size:11px;font-weight:800;font-variant-numeric:tabular-nums}
#artBoard canvas{width:100%;display:block}
#artBoard .big{height:168px}#artBoard .mini{height:64px}
#artBoard .sub{font-size:9.5px;color:#5d6673;letter-spacing:.1em;text-transform:uppercase;font-weight:800;margin:6px 0 2px}
@media(max-width:980px){#artBoard{grid-template-columns:1fr}}
"""

ART_JS = r"""
(function(){
 document.documentElement.classList.add('artjs');document.body.classList.add('artjs');
 /* apparition douce */
 try{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('artin');io.unobserve(e.target);}});},{rootMargin:'60px'});
  document.querySelectorAll('.ovchap,.ovc').forEach(function(el){io.observe(el);});
 }catch(e){document.querySelectorAll('.ovchap,.ovc').forEach(function(el){el.classList.add('artin');});}
 /* hôte du tableau graphique, sous Le Marché */
 var mk=document.getElementById('ovMarket');if(!mk)return;
 var host=document.createElement('div');host.id='artBoard';mk.parentNode.insertBefore(host,mk.nextSibling);
 function cnv(id,cls){return '<canvas id="'+id+'" class="'+cls+'"></canvas>';}
 function ctx(id){var c=document.getElementById(id);if(!c)return null;var r=c.getBoundingClientRect(),d=window.devicePixelRatio||1;
  if(!r.width)return null;c.width=r.width*d;c.height=r.height*d;var x=c.getContext('2d');x.scale(d,d);x.W=r.width;x.H=r.height;
  x.font='9.5px ui-monospace,Menlo,monospace';return x;}
 function area(id,arr,col,opts){var x=ctx(id);if(!x||!arr||arr.length<2)return;opts=opts||{};
  var mn=Math.min.apply(0,arr),mx=Math.max.apply(0,arr);if(mn===mx){mn-=1;mx+=1;}
  var pad={l:opts.axis?40:6,r:6,t:8,b:opts.axis?6:6};
  if(opts.axis){x.strokeStyle='rgba(255,255,255,.05)';x.fillStyle='#5d6673';
   for(var i=0;i<=2;i++){var yy=pad.t+(x.H-pad.t-pad.b)*i/2;x.beginPath();x.moveTo(pad.l,yy);x.lineTo(x.W-pad.r,yy);x.stroke();
    x.fillText(Math.round(mx-(mx-mn)*i/2).toLocaleString('fr-FR'),3,yy+3);}}
  var X=function(i){return pad.l+(x.W-pad.l-pad.r)*i/(arr.length-1);},Y=function(v){return pad.t+(x.H-pad.t-pad.b)*(1-(v-mn)/(mx-mn));};
  /* moyenne mobile 8 points (lecture de tendance) */
  if(opts.ma){x.beginPath();for(var i=7;i<arr.length;i++){var m=0;for(var k=i-7;k<=i;k++)m+=arr[k];m/=8;
   (i===7)?x.moveTo(X(i),Y(m)):x.lineTo(X(i),Y(m));}x.strokeStyle='rgba(255,255,255,.28)';x.setLineDash([4,4]);x.lineWidth=1;x.stroke();x.setLineDash([]);}
  x.beginPath();arr.forEach(function(v,i){i?x.lineTo(X(i),Y(v)):x.moveTo(X(i),Y(v));});
  x.save();x.lineTo(X(arr.length-1),x.H-pad.b);x.lineTo(X(0),x.H-pad.b);x.closePath();
  var g=x.createLinearGradient(0,pad.t,0,x.H);g.addColorStop(0,col+'44');g.addColorStop(1,col+'00');x.fillStyle=g;x.fill();x.restore();
  x.beginPath();arr.forEach(function(v,i){i?x.lineTo(X(i),Y(v)):x.moveTo(X(i),Y(v));});
  x.strokeStyle=col;x.lineWidth=opts.axis?2.1:1.6;x.stroke();
  /* point vivant */
  var lx=X(arr.length-1),ly=Y(arr[arr.length-1]);
  x.fillStyle=col;x.beginPath();x.arc(lx,ly,3,0,7);x.fill();
  x.fillStyle=col+'33';x.beginPath();x.arc(lx,ly,7,0,7);x.fill();}
 function chip(v){var c=v>=0?'#22C55E':'#EF4444';return '<span class="c" style="color:'+c+'">'+(v>=0?'+':'')+(v==null?'—':v.toFixed(2))+'%</span>';}
 function render(d){var idx=(d&&d.indices)||[];if(!idx.length){host.style.display='none';return;}
  var find=function(n){return idx.filter(function(i){return (i.name||'').indexOf(n)>=0;})[0];};
  var sp=find('S&P'),nd=find('Nasdaq')||find('NDX'),dw=find('Dow'),vx=idx.filter(function(i){return i.vix;})[0]||find('VIX');
  host.innerHTML=
   '<div class="ac"><div class="hd"><span class="t">📈 S&P 500 — la boussole</span>'
    +(sp?'<span class="v num">'+Number(sp.price).toLocaleString('fr-FR')+'</span>'+chip(sp.change):'')+'</div>'
    +'<div class="sub">'+((sp&&sp.spark)?sp.spark.length:0)+' dernières séances · pointillé = tendance (MM8)</div>'+cnv('artSpx','big')+'</div>'
   +'<div class="ac"><div class="hd"><span class="t">💻 Nasdaq</span>'+(nd?'<span class="v num">'+Number(nd.price).toLocaleString('fr-FR')+'</span>'+chip(nd.change):'')+'</div>'+cnv('artNdx','mini')
    +'<div class="sub" style="margin-top:10px">🏛 Dow Jones</div><div class="hd">'+(dw?'<span class="v num" style="margin-left:0">'+Number(dw.price).toLocaleString('fr-FR')+'</span>'+chip(dw.change):'')+'</div>'+cnv('artDow','mini')+'</div>'
   +'<div class="ac"><div class="hd"><span class="t">😱 VIX — la peur</span>'+(vx?'<span class="v num">'+Number(vx.price).toLocaleString('fr-FR')+'</span>'+chip(vx.change):'')+'</div>'
    +cnv('artVix','mini')
    +'<div class="sub" style="margin-top:10px">Lecture</div>'
    +'<div style="font-size:11.5px;color:#aeb8c8;line-height:1.55;padding-bottom:8px">'+(vx?(vx.price<=14?'VIX bas : marché serein, les couvertures sont bon marché.':vx.price>=22?'VIX élevé : stress — options chères, tailles réduites.':'VIX en zone neutre : ni euphorie, ni panique.'):'—')+'</div></div>';
  if(sp&&sp.spark)area('artSpx',sp.spark,(sp.change>=0?'#22C55E':'#EF4444'),{axis:true,ma:true});
  if(nd&&nd.spark)area('artNdx',nd.spark,(nd.change>=0?'#22C55E':'#EF4444'));
  if(dw&&dw.spark)area('artDow',dw.spark,(dw.change>=0?'#22C55E':'#EF4444'));
  if(vx&&vx.spark)area('artVix',vx.spark,'#F5B45B');}
 function load(){fetch('/api/market/summary').then(function(r){return r.json();}).then(render).catch(function(){});}
 load();setInterval(function(){if(!document.hidden)load();},90000);
})();
"""


def apply(page):
    """Applique la couche artistique à PAGE_DAILY (style + script avant </body>)."""
    return page.replace('</body>', '<style>' + ART_CSS + '</style><script>' + ART_JS + '</script></body>', 1)


__all__ = ['ART_CSS', 'ART_JS', 'apply']
