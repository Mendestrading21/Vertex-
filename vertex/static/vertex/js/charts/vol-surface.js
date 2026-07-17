/* vol-surface.js — surface strike × expiration (heatmap IV moteur). */
(function(){const C=window.VXCharts,VX=window.VX;
C.volSurfaceCard=function(host,surface,opts){
  const by=(surface&&surface.by_expiry)||{};
  const expiries=Object.keys(by);
  if(!expiries.length){const el=typeof host==='string'?document.getElementById(host):host;
    if(el)el.innerHTML=VX.states.empty('Surface de volatilité indisponible.');return;}
  const strikes=[...new Set(expiries.flatMap(e=>Object.keys(by[e].strikes||{})))].map(Number).sort((a,b)=>a-b);
  const rows=strikes.map(k=>({label:VX.fmt.price(k),
    cells:expiries.map(e=>{const iv=(by[e].strikes||{})[k];
      return{value:iv!=null?iv*100:null,label:iv!=null?(iv*100).toFixed(0)+'%':'—',
        title:`${e} · strike ${k}`};})}));
  C.heatmapCard(host,Object.assign({rows,columns:expiries.map(e=>e+' ('+(by[e].dte||'?')+'j)'),
    min:15,max:90,scale:'sequential'},opts||{}));};
})();
