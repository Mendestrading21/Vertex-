/* equity-chart.js — courbe d'équité (Performance). */
(function(){const C=window.VXCharts;
C.equityCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,opts.values,{color:C.colors.cyan,yFmt:opts.yFmt})}));};
})();
