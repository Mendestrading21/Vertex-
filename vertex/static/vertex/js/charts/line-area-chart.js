/* line-area-chart.js — courbes en aire (indices, portefeuille, volatilité).
   LOT 200 (tournée TV) : passthrough `extremes` → chips Max/Min posés sur
   les extrêmes RÉELS de la série (C.tvExtremesPlugin, lot 195). */
(function(){const C=window.VXCharts=window.VXCharts||{};
C.areaCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,opts.values,{color:opts.color,yFmt:opts.yFmt,extremes:opts.extremes||false})}));};
})();
