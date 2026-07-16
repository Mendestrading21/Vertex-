/* sector-chart.js — rotation sectorielle (barres horizontales cliquables). */
(function(){const C=window.VXCharts;
C.sectorCard=function(host,opts){
  return C.card(host,Object.assign({},opts,{render:(cv)=>{
    /* Valeurs = SCORES moyens (0-100), pas des % de variation. Couleur graduée
       par force : émeraude fort · ambre moyen · gris faible. */
    const cols=opts.values.map(v=>v>=60?C.colors.positive:(v>=45?C.colors.warning:C.colors.neutral));
    const chart=C.bars(cv,opts.labels,opts.values,{horizontal:true,colors:cols,yFmt:(v)=>v});
    if(opts.onSector)cv.onclick=(evt)=>{const pts=chart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
      if(pts.length)opts.onSector(opts.labels[pts[0].index]);};
    return chart;}}));};
})();
