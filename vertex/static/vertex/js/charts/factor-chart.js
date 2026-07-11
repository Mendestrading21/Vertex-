/* factor-chart.js — exposition factorielle (barres horizontales). */
(function(){const C=window.VXCharts;
C.factorCard=function(host,opts){
  return C.barCard(host,Object.assign({horizontal:true},opts));};
})();
