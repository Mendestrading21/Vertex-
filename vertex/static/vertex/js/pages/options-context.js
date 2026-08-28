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
    /*  Deux entrees vers la meme page : le bouton contextuel et, depuis le
        lot 25, l'onglet « Chaine » que le contrat range parmi les sous-vues.
        Les deux suivent le sous-jacent, et les deux sont DESACTIVES sans lui —
        un lien qui menerait a une 404 est pire qu'un lien absent. */
    var onglet = document.getElementById('vx-options-chain-tab');
    if (onglet) {
      if (sym) {
        onglet.href = '/options/dossier/' + encodeURIComponent(sym);
        onglet.removeAttribute('aria-disabled');
        onglet.removeAttribute('tabindex');
        onglet.title = 'Chaine CALL / strike / PUT de ' + sym;
        onglet.style.pointerEvents = '';
        onglet.style.opacity = '';
      } else {
        onglet.removeAttribute('href');
        onglet.setAttribute('aria-disabled', 'true');
        onglet.setAttribute('tabindex', '-1');
        onglet.title = 'Choisir un sous-jacent pour ouvrir sa chaine';
        onglet.style.pointerEvents = 'none';
        onglet.style.opacity = '.45';
      }
    }
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

  /* ── BARRE DE CONTEXTE ────────────────────────────────────────────────
     Deux emplacements de la barre 2.0 — le sous-jacent actif et la fraicheur
     — etaient DECLARES et remplis par personne : la barre annoncait « Aucun
     sous-jacent choisi » et « Lecture… » indefiniment, y compris apres une
     saisie. Meme classe de defaut que les emplacements morts d'Opportunites
     et de Suivi. Ce pont connait deja le symbole ; il le DIT.

     La fraicheur n'est pas devinee : elle vient du scan, seule source de
     contrats de cette page. Quand elle manque, on l'ecrit. */
  var _tsAffiche = null;
  function peindreContexte(sym) {
    var cible = document.getElementById('vx-opt-ctx-sym');
    if (cible) {
      cible.innerHTML = sym
        ? '<span class="vx2-badge" data-state="option">' + sym + '</span>'
        : '<span class="vx2-badge" data-state="missing">Aucun sous-jacent choisi</span>';
    }
    var frais = document.getElementById('vx-opt-ctx-fresh');
    if (!frais) return;
    var dire = function (texte, etat) {
      frais.innerHTML = '<span class="vx2-badge" data-state="' + etat + '">' + texte + '</span>';
    };
    /*  Priorite a l'horodatage de la donnee AFFICHEE (les graphiques de
        volatilite l'emettent). A defaut, l'age du scan, qui est la source des
        contrats. A defaut encore, on l'avoue.  */
    if (_tsAffiche != null && window.VX && VX.freshness) {
      var ageDonnee = VX.freshness._ms(_tsAffiche);
      if (ageDonnee != null) {
        frais.innerHTML = VX.freshness.chip(VX.freshness.assess({ ageMs: Date.now() - ageDonnee, live: false }));
        return;
      }
    }
    var pk = null;
    try { pk = window.VX && VX.fetch && VX.fetch.peek('/scan'); } catch (e) {}
    var scan = pk && pk.data;
    if (!scan) { dire('Aucune donn\u00e9e dat\u00e9e sur cette vue', 'missing'); return; }
    var age = (typeof scan.scan_age === 'number') ? scan.scan_age * 1000 : null;
    if (age == null) { dire('Scan non horodat\u00e9 \u2014 \u00e2ge inconnu', 'missing'); return; }
    if (window.VX && VX.freshness) {
      var etat = VX.freshness.assess({ ageMs: age, live: scan.data_source !== 'demo' });
      frais.innerHTML = VX.freshness.chip(etat);
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
    peindreContexte(sym);
    if (!target) return;
    var local = document.getElementById(target[0]);
    var button = document.getElementById(target[1]);
    if (local) local.value = sym;
    if (button) button.click();
  }

  var initial = currentSymbol();
  if (initial && valid(initial)) globalInput.value = initial;
  updateTabLinks(initial);
  peindreContexte(valid(initial) ? initial : '');
  /*  Le scan arrive apres ce script : la fraicheur se repeint quand il est la,
      plutot que de rester sur « non encore lu » pour toujours.  */
  if (window.VX && VX.bus) {
    VX.bus.on('vx:data-refreshed', function () {
      peindreContexte(normalize(globalInput.value));
    });
    /*  `VX.bus.emit(nom, detail)` envoie un CustomEvent : l'abonne recoit
        l'EVENEMENT, et la charge vit dans `e.detail`. Lire `payload.ts`
        directement rendait toujours `undefined`, et la barre affichait
        « aucune donnee datee » alors que la donnee etait datee.  */
    VX.bus.on('vx:options-fresh', function (e) {
      _tsAffiche = ((e && e.detail) || {}).ts || null;
      peindreContexte(normalize(globalInput.value));
    });
  }
  setTimeout(function () { peindreContexte(normalize(globalInput.value)); }, 2000);
  if (window.VX && VX.bus) VX.bus.on('vx:store-changed', function (payload) {
    if (!payload || payload.key !== 'active_ticker') return;
    var sym = normalize(payload.value); if (!valid(sym)) return;
    globalInput.value = sym; updateTabLinks(sym); peindreContexte(sym);
  });
  apply.addEventListener('click', run);
  globalInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') run();
  });
})();
