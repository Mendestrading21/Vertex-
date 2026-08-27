/* Vertex Options — contexte sous-jacent unique entre les sous-vues.
   Ce pont ne calcule rien : il transmet le symbole aux loaders existants et
   conserve le contrat READONLY. */
(function () {
  'use strict';
  var globalInput = document.getElementById('vx-options-symbol');
  var apply = document.getElementById('vx-options-apply');
  if (!globalInput || !apply) return;

  var label = document.querySelector('[data-page-label]');
  var view = ((label && label.dataset.pageLabel) || 'options:structure').split(':')[1];
  var targets = {
    structure: ['vx-os-sym', 'vx-os-go'],
    positioning: ['vx-gx-sym', 'vx-gx-go'],
    leaps: ['vx-lp-sym', 'vx-lp-go'],
    volatility: ['vx-opt-vol-sym', 'vx-opt-vol-go'],
    events: ['vx-opt-ev-sym', 'vx-opt-ev-go'],
    scenarios: ['vx-opt-sc-sym', 'vx-opt-sc-go'],
  };
  var target = targets[view];
  var context = globalInput.closest('.vx-options-context');
  if (!target && context) context.hidden = true;

  function valid(value) { return /^[A-Z.\-]{1,12}$/.test(value); }
  function normalize(value) { return String(value || '').trim().toUpperCase(); }
  function updateTabLinks(sym) {
    document.querySelectorAll('[data-view-tab]').forEach(function (link) {
      try {
        var url = new URL(link.href, location.origin);
        if (sym) url.searchParams.set('sym', sym); else url.searchParams.delete('sym');
        link.href = url.pathname + url.search;
      } catch (e) {}
    });
    updateChainLink(sym);
  }

  /* Le dossier par sous-jacent porte la chaine CALL / strike / PUT — « la table
     specialisee principale » du contrat. Son lien suit le symbole actif ; sans
     symbole il est DESACTIVE, parce qu'un lien qui menerait a une 404 est pire
     qu'un lien absent. */
  function updateChainLink(sym) {
    var lien = document.getElementById('vx-options-chain');
    if (!lien) return;
    if (sym) {
      lien.href = '/options/dossier/' + encodeURIComponent(sym);
      lien.removeAttribute('aria-disabled');
      lien.removeAttribute('tabindex');
      lien.textContent = 'Ouvrir la cha\u00eene de ' + sym + ' \u2192';
      lien.style.pointerEvents = '';
      lien.style.opacity = '';
    } else {
      lien.removeAttribute('href');
      lien.setAttribute('aria-disabled', 'true');
      lien.setAttribute('tabindex', '-1');
      lien.textContent = 'Choisir un sous-jacent pour ouvrir sa cha\u00eene';
      lien.style.pointerEvents = 'none';
      lien.style.opacity = '.45';
    }
  }
  function currentSymbol() {
    var query = '';
    try { query = new URLSearchParams(location.search).get('sym') || ''; } catch (e) {}
    var stored = '';
    try { stored = (window.VX && VX.store && VX.store.get('active_ticker')) || ''; } catch (e2) {}
    var local = target && document.getElementById(target[0]);
    return normalize(query || stored || (local && local.value));
  }
  function run() {
    var sym = normalize(globalInput.value);
    if (!valid(sym)) {
      if (window.VX && VX.toast) VX.toast('Symbole invalide', 'error');
      globalInput.focus(); return;
    }
    globalInput.value = sym;
    try { if (window.VX && VX.store) VX.store.set('active_ticker', sym); } catch (e) {}
    try {
      var page = new URL(location.href); page.searchParams.set('sym', sym);
      history.replaceState(history.state, '', page.pathname + page.search);
    } catch (e2) {}
    updateTabLinks(sym);
    if (!target) return;
    var local = document.getElementById(target[0]);
    var button = document.getElementById(target[1]);
    if (local) local.value = sym;
    if (button) button.click();
  }

  var initial = currentSymbol();
  if (initial && valid(initial)) globalInput.value = initial;
  updateTabLinks(initial);
  if (window.VX && VX.bus) VX.bus.on('vx:store-changed', function (payload) {
    if (!payload || payload.key !== 'active_ticker') return;
    var sym = normalize(payload.value); if (!valid(sym)) return;
    globalInput.value = sym; updateTabLinks(sym);
  });
  apply.addEventListener('click', run);
  globalInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') run();
  });
})();
