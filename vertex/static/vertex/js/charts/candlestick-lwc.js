/* candlestick-lwc.js — chandeliers PRO via TradingView Lightweight Charts
   (Apache-2.0, auto-hébergé, aucun appel réseau, aucune donnée inventée).
   Expose VXCharts.lwCandlestickCard(host, opts) : même contrat que candlestickCard
   (réutilise C.card → titre / question / conclusion / contrôles timeframe / légende /
   pied source-date / bouton « Comprendre ce graphique »), mais rend un vrai graphique
   chandeliers interactif (crosshair, zoom/pan) à la place du canvas Chart.js.
   Bougies : hausse = émeraude (positif), baisse = corail (négatif) — JAMAIS le vert
   marque (#84aa31 = identité, pas « ça monte »). Volume + moyennes serveur + niveaux
   du plan moteur superposés. Repli automatique sur candlestickCard si la lib ou les
   dates OHLC manquent. Attribution TradingView affichée (exigence de licence). */
(function () {
  var C = window.VXCharts; if (!C) return;

  /* Un seul graphique LWC vivant par hôte : on détruit le précédent au re-render
     (changement de timeframe) pour éviter les ResizeObserver orphelins. */
  var LIVE = (typeof WeakMap !== 'undefined') ? new WeakMap() : null;

  function num(v) { if (v === null || v === undefined || v === '') return null; var n = +v; return isFinite(n) ? n : null; }
  function cssv(v, f) { try { var s = getComputedStyle(document.documentElement).getPropertyValue(v).trim(); return s || f; } catch (e) { return f; } }

  /* Reconstruit 'yyyy-mm-dd' à partir des dates 'MM-DD' du moteur : la dernière
     bougie ≈ aujourd'hui ; on décrémente l'année à chaque passage de bornage
     (déc.→janv. en remontant le temps). */
  function inferDates(mmdd) {
    var now = new Date(), y = now.getFullYear(), out = new Array(mmdd.length);
    for (var i = mmdd.length - 1; i >= 0; i--) {
      var s = String(mmdd[i] || ''), mm = s.slice(0, 2), dd = s.slice(3, 5);
      if (i < mmdd.length - 1) {
        var nextMM = parseInt(String(mmdd[i + 1]).slice(0, 2), 10);
        if (parseInt(mm, 10) > nextMM) y--;
      }
      out[i] = y + '-' + mm + '-' + dd;
    }
    return out;
  }

  function shownOverlays(overlays) {
    return (overlays || []).filter(function (o) {
      return o && o.data && o.data.some(function (x) { return x != null; });
    });
  }

  C.lwCandlestickCard = function (host, opts) {
    opts = opts || {};
    var el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    var LWC = window.LightweightCharts;
    var bars = opts.bars || [], dates = opts.dates || [];
    var okBars = bars.length >= 2 && bars.every(function (b) {
      return b && b.o != null && b.h != null && b.l != null && b.c != null;
    });
    /* Repli honnête : pas de lib, ou pas d'OHLC daté aligné → candlestick Chart.js. */
    if (!LWC || !okBars || dates.length !== bars.length) {
      return C.candlestickCard ? C.candlestickCard(host, opts) : null;
    }

    var times = inferDates(dates);
    /* Bougies strictement croissantes et uniques par date (exigence LWC). */
    var candles = [], seen = {}, lastT = '';
    for (var i = 0; i < bars.length; i++) {
      var b = bars[i], o = num(b.o), h = num(b.h), l = num(b.l), c = num(b.c), t = times[i];
      if (o == null || h == null || l == null || c == null || !t || t <= lastT) continue;
      seen[t] = i; lastT = t;
      candles.push({ time: t, open: o, high: h, low: l, close: c });
    }
    if (candles.length < 2) { return C.candlestickCard ? C.candlestickCard(host, opts) : null; }

    /* Légende = overlays réellement traçables (parité candlestickCard). */
    var legend = (opts.legend || []).concat(shownOverlays(opts.overlays).map(function (o) {
      return { label: o.label, color: o.color };
    }));

    return C.card(host, Object.assign({}, opts, { legend: legend, render: function (canvas) {
      if (LIVE) { var old = LIVE.get(el); if (old) { try { old.remove(); } catch (e) {} LIVE.delete(el); } }
      /* On garde le <canvas> masqué (compat sélecteurs de la page) et on monte LWC
         dans un conteneur frère occupant tout le corps du ChartCard. */
      var body = canvas.parentNode;
      canvas.style.display = 'none';
      /* Hauteur EXPLICITE en px : le corps du ChartCard est un flex:1 à base
         indéfinie → un enfant en height:100% s'effondrerait à 0 (LWC a besoin
         d'une hauteur mesurable, contrairement au canvas Chart.js). */
      var H = (+opts.height) || body.clientHeight || 360;
      var cont = document.createElement('div');
      cont.className = 'vx-lwc';
      cont.style.cssText = 'position:relative;width:100%;height:' + H + 'px';
      body.appendChild(cont);

      var pos = cssv('--vx-positive', '#36c889'), neg = cssv('--vx-negative', '#ed655c');
      var grid = 'rgba(237,255,237,.045)', border = 'rgba(237,255,237,.09)';
      var chart = LWC.createChart(cont, {
        autoSize: true,
        layout: { background: { type: 'solid', color: 'transparent' }, textColor: cssv('--vx-text-muted', '#817d77'), fontFamily: cssv('--vx-font', 'Inter, ui-sans-serif, system-ui, sans-serif'), fontSize: 11 },
        grid: { vertLines: { color: grid }, horzLines: { color: grid } },
        rightPriceScale: { borderColor: border },
        timeScale: { borderColor: border, timeVisible: false, secondsVisible: false, rightOffset: 3 },
        crosshair: { mode: 1, vertLine: { color: 'rgba(237,255,237,.28)', width: 1, style: 3 }, horzLine: { color: 'rgba(237,255,237,.28)', width: 1, style: 3 } },
      });

      var cs = chart.addCandlestickSeries({ upColor: pos, downColor: neg, borderVisible: false, wickUpColor: pos, wickDownColor: neg });
      cs.setData(candles);

      /* Volume (histogramme, échelle séparée en bas) — données réelles alignées. */
      if (opts.volume && opts.volume.length === bars.length) {
        var vs = chart.addHistogramSeries({ priceFormat: { type: 'volume' }, priceScaleId: 'vol' });
        chart.priceScale('vol').applyOptions({ scaleMargins: { top: 0.84, bottom: 0 } });
        var vdata = [];
        for (var j = 0; j < bars.length; j++) {
          var vt = times[j], vv = num(opts.volume[j]);
          if (!vt || vv == null || seen[vt] !== j) continue;
          var up = num(bars[j].c) >= num(bars[j].o);
          vdata.push({ time: vt, value: vv, color: up ? 'rgba(54,200,137,.34)' : 'rgba(237,101,92,.34)' });
        }
        if (vdata.length) vs.setData(vdata);
      }

      /* Moyennes mobiles serveur (overlays) en lignes. */
      shownOverlays(opts.overlays).forEach(function (ov) {
        var d = [], lt = '';
        for (var k = 0; k < ov.data.length; k++) {
          var val = num(ov.data[k]), tk = times[k];
          if (val == null || !tk || seen[tk] !== k || tk <= lt) continue;
          lt = tk; d.push({ time: tk, value: val });
        }
        if (d.length < 2) return;
        var ls = chart.addLineSeries({ color: ov.color || cssv('--vx-steel-2', '#a6ada5'), lineWidth: ov.width || 1.4, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false, lineStyle: (ov.dash && ov.dash.length) ? 2 : 0 });
        ls.setData(d);
      });

      /* Niveaux du plan moteur en lignes de prix (entrée/stop/TP/résistance/support). */
      var plan = opts.plan || {};
      [['entry', 'Entrée', cssv('--vx-brand', '#84aa31')], ['stop', 'Stop', neg],
       ['tp1', 'TP1', pos], ['tp2', 'TP2', pos], ['tp3', 'TP3', pos],
       ['resistance', 'Résist.', cssv('--vx-steel-3', '#747d75')], ['support', 'Support', cssv('--vx-steel-3', '#747d75')]
      ].forEach(function (p) {
        var v = num(plan[p[0]]); if (v == null) return;
        cs.createPriceLine({ price: v, color: p[2], lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: p[1] });
      });

      try { chart.timeScale().fitContent(); } catch (e) {}

      /* Attribution TradingView (licence) ajoutée au pied du ChartCard. */
      var card = (body.closest && body.closest('.vx-chart-card')) || el;
      var foot = card && card.querySelector('.vx-chart-foot');
      if (foot && !foot.querySelector('.vx-tv-attr')) {
        var a = document.createElement('a');
        a.className = 'vx-meta vx-tv-attr';
        a.href = 'https://www.tradingview.com/'; a.target = '_blank'; a.rel = 'noopener';
        a.textContent = 'Charting by TradingView ↗';
        a.style.cssText = 'margin-left:auto;text-decoration:none';
        foot.appendChild(a);
      }

      if (LIVE) LIVE.set(el, chart);
      return chart;
    } }));
  };
})();
