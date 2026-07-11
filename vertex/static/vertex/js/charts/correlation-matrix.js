/* correlation-matrix.js — corrélations (réutilise la heatmap). */
(function(){const C=window.VXCharts;
C.correlationCard=function(host,opts){
  return C.heatmapCard(host,Object.assign({min:-1,max:1,fmt:(v)=>(v===null?'—':v.toFixed(2))},opts));};
})();
