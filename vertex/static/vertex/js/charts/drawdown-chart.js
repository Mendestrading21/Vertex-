/* drawdown-chart.js — drawdown depuis les pics (valeurs fournies/derivées
   arithmétiquement de la série d'équité déclarée — pas un indicateur). */
(function(){const C=window.VXCharts;
C.drawdown=function(values){let peak=-Infinity;return values.map(v=>{peak=Math.max(peak,v);return peak>0?(v/peak-1)*100:0;});};
C.drawdownCard=function(host,opts){
  const dd=opts.drawdowns||C.drawdown(opts.values||[]);
  return C.card(host,Object.assign({},opts,{render:(cv)=>C.area(cv,opts.labels,dd,{color:C.colors.negative,yFmt:(v)=>v.toFixed(0)+' %'})}));};
})();
