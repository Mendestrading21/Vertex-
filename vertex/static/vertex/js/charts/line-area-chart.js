/* line-area-chart.js — courbes en aire (indices, portefeuille, volatilité). */
(function(){const C=window.VXCharts;
C.areaCard=function(host,opts){
  if(!C.hasData(opts.values))return C.emptyCard(host,opts,opts.emptyReason||'Aucune série à tracer.');
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,opts.values,{color:opts.color,yFmt:opts.yFmt})}));};
})();
