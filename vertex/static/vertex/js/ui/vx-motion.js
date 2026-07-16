/* Vertex — vx-motion.js : micro-motion discret (compteur KPI).
   Anime les éléments [data-countup] de 0 → valeur affichée, en RESTAURANT
   exactement le texte final (aucune dérive, jamais de NaN). Respecte
   prefers-reduced-motion (valeur finale instantanée). Observe le contenu pour
   animer aussi les KPI injectés par le JS des pages (hydratation fetch).
   Aucun dialogue, aucune logique métier — pur habillage. Lecture seule. */
(function () {
  'use strict';
  var VX = window.VX = window.VX || {};
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  // Jeton numérique : signe + chiffres avec regroupement (espaces/nbsp/point) + décimales
  var NUM_RE = /-?\d[\d   .]*\d|-?\d/;

  function split(txt) {
    var m = txt.match(NUM_RE);
    if (!m) return null;
    return { pre: txt.slice(0, m.index), tok: m[0], suf: txt.slice(m.index + m[0].length) };
  }
  function toNumber(tok) {
    var t = tok.replace(/[\s  ]/g, '');
    if (t.indexOf(',') >= 0) { t = t.replace(/\./g, '').replace(',', '.'); }
    return parseFloat(t);
  }
  function decimalsOf(tok) {
    var t = tok.replace(/[\s  ]/g, '');
    var dm = t.match(/[.,](\d+)$/);
    return dm ? dm[1].length : 0;
  }

  function animate(el) {
    if (!el || el.dataset.countupDone) return;
    var finalText = el.textContent;
    var parts = split(finalText);
    if (!parts) { el.dataset.countupDone = '1'; return; }
    var target = toNumber(parts.tok);
    el.dataset.countupDone = '1';
    if (!isFinite(target)) return;                 // laisse le texte honnête tel quel
    if (reduce || Math.abs(target) < 1e-4) return; // pas d'animation → valeur finale conservée

    var dec = decimalsOf(parts.tok);
    var dur = 620, t0 = null;
    function fmt(v) {
      return parts.pre + v.toLocaleString('fr-FR',
        { minimumFractionDigits: dec, maximumFractionDigits: dec }) + parts.suf;
    }
    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      if (p >= 1) { el.textContent = finalText; return; }  // restaure l'exact final
      var eased = 1 - Math.pow(1 - p, 3);                  // easeOutCubic
      el.textContent = fmt(target * eased);
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function scan(root) {
    var nodes = (root || document).querySelectorAll('[data-countup]:not([data-countup-done])');
    for (var i = 0; i < nodes.length; i++) animate(nodes[i]);
  }
  VX.countUp = scan;

  if (document.readyState !== 'loading') scan(document);
  else document.addEventListener('DOMContentLoaded', function () { scan(document); });

  // KPI injectés après coup (les pages hydratent par fetch) → on les anime aussi
  try {
    var mo = new MutationObserver(function (muts) {
      for (var i = 0; i < muts.length; i++) {
        var added = muts[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if (n.matches && n.matches('[data-countup]')) animate(n);
          if (n.querySelectorAll) scan(n);
        }
      }
    });
    var t = document.getElementById('vx-content') || document.body;
    if (t) mo.observe(t, { childList: true, subtree: true });
  } catch (e) {}
})();
