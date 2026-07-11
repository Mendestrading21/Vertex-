/* sector-chart.js — rotation sectorielle (barres horizontales cliquables). */
(function(){const C=window.VXCharts;
C.sectorCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>{
    const chart=C.bars(cv,opts.labels,opts.values,{horizontal:true,yFmt:(v)=>v+' %'});
    if(opts.onSector)cv.onclick=(evt)=>{const pts=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
      if(pts.length)opts.onSector(opts.labels[pts[0].index]);};
    return chart;}}));};
})();
