/* sparkline.js — mini-courbes KPI/positions/watchlist (wrapper chart-core). */
(function(){const C=window.VXCharts;
C.sparklineInto=function(hostEl,values,opts){
  if(!hostEl)return null;
  hostEl.innerHTML='<canvas height="28" class="vx-sparkline" aria-hidden="true"></canvas>';
  return C.sparkline(hostEl.querySelector('canvas'),values,opts||{});};
})();
