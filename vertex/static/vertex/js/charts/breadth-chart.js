/* breadth-chart.js — participation de marché. */
(function(){const C=window.VXCharts;
C.breadthCard=function(host,opts){
  return C.barCard(host,Object.assign({},opts,{colors:opts.values.map(v=>v>=50?C.colors.positive:C.colors.negative)}));};
})();
