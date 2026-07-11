/* bar-chart.js — histogrammes (volume, breadth, contribution, secteurs). */
(function(){const C=window.VXCharts;
C.barCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.bars(cv,opts.labels,opts.values,{colors:opts.colors,horizontal:opts.horizontal,yFmt:opts.yFmt})}));};
})();
