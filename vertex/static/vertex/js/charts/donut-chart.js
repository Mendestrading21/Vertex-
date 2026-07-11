/* donut-chart.js — répartitions (rôles, secteurs, états). Max ~5 catégories. */
(function(){const C=window.VXCharts;
C.donutCard=function(host,opts){
  return C.card(host,Object.assign({height:opts.height||170},opts,{render:(cv)=>C.donut(cv,opts.labels,opts.values,{colors:opts.colors})}));};
})();
