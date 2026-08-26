/* breadth-chart.js — participation de marché. */
(function(){const C=window.VXCharts;
C.breadthCard=function(host,opts){
  if(!C.hasData(opts.values))return C.emptyCard(host,opts,opts.emptyReason||'Participation indisponible.');
  return C.barCard(host,Object.assign({},opts,{colors:opts.values.map(v=>v>=50?C.colors.positive:C.colors.negative)}));};
})();
