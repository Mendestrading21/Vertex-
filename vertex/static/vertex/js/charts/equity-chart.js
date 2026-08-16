/* equity-chart.js — courbe d'équité (Performance).
   LOT 195 (tournée TV) : chips Max/Min posés sur les extrêmes RÉELS de la
   série (plus haut / plus bas d'équité — les deux chiffres du drawdown). */
(function(){const C=window.VXCharts=window.VXCharts||{};
C.equityCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,opts.values,{color:C.colors.brand,yFmt:opts.yFmt,extremes:true})}));};
})();
