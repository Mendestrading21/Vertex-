/* bar-chart.js — histogrammes (volume, breadth, contribution, secteurs). */
(function(){const C=window.VXCharts;
C.barCard=function(host,opts){
  if(!C.hasData(opts.values))return C.emptyCard(host,opts,opts.emptyReason||'Aucune donnée à représenter.');
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.bars(cv,opts.labels,opts.values,{colors:opts.colors,horizontal:opts.horizontal,yFmt:opts.yFmt})}));};
})();
