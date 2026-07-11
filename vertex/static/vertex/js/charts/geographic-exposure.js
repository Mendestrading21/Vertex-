/* geographic-exposure.js — exposition géographique (barres, pas de carte 3D).
   Ne s'affiche que si les moteurs fournissent une répartition réelle. */
(function(){const C=window.VXCharts,VX=window.VX;
C.geoCard=function(host,opts){
  if(!(opts.labels||[]).length){const el=typeof host==='string'?document.getElementById(host):host;
    if(el)el.innerHTML=VX.states.empty('Répartition géographique non fournie par les moteurs.');return null;}
  return C.barCard(host,Object.assign({horizontal:true},opts));};
})();
