/* equity-chart.js — courbe d'équité (Performance). */
(function(){const C=window.VXCharts;
C.equityCard=function(host,opts){
  if(!C.hasData(opts.values))return C.emptyCard(host,opts,opts.emptyReason||'Courbe d’équité indisponible (aucun trade clôturé).');
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,opts.values,{color:C.colors.cyan,yFmt:opts.yFmt})}));};
})();
