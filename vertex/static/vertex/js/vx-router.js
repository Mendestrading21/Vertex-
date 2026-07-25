/* Vertex Router — navigation client persistante (CONTINUITY LOT 2).

   Progressive-enhancement : les URL servent TOUJOURS le document complet (accès
   direct, deep link, refresh, nouvel onglet, sans-JS = inchangés). Ce routeur est
   une SURCOUCHE : il intercepte les clics de liens internes, récupère un FRAGMENT
   (`X-Vertex-Fragment: 1`) et ne remplace que #vx-content — le shell (sidebar,
   topbar, palette, overlays) n'est jamais reconstruit. history.pushState/popstate
   gardent l'historique, le retour et les URL partageables intacts.

   Sécurité de ré-exécution : les scripts INLINE de page sont des IIFE (ré-exécution
   idempotente en portée globale) ; les scripts EXTERNES sont chargés une seule fois
   (dédup). Une page dont tout le comportement vit dans des scripts externes
   auto-initialisés (aucun inline) n'est PAS pilotable ainsi → repli navigation dure.
   Toute erreur → repli navigation dure. Aucun ordre, lecture seule. */
(function () {
  'use strict';
  var VX = window.VX = window.VX || {};
  if (VX.router) return;

  /* Indice de navigation discret (respecte prefers-reduced-motion via CSS). */
  var style = document.createElement('style');
  style.textContent =
    '.vx-navigating #vx-content{opacity:.55;transition:opacity .12s ease}' +
    '#vx-content{transition:opacity .12s ease}';
  document.head.appendChild(style);
  function startBar() { document.documentElement.classList.add('vx-navigating'); }
  function endBar() { document.documentElement.classList.remove('vx-navigating'); }

  function contentEl() { return document.getElementById('vx-content'); }
  function hard(href) { window.location.href = href; }

  /* Un lien est-il « app interne » (candidat SPA) ? Sinon → comportement natif. */
  function internalURL(a) {
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return null;
    var raw = a.getAttribute('href') || '';
    if (!raw || raw.charAt(0) === '#' || /^(mailto:|tel:|javascript:)/i.test(raw)) return null;
    var url;
    try { url = new URL(a.href, location.href); } catch (e) { return null; }
    if (url.origin !== location.origin) return null;
    var p = url.pathname;
    if (p.indexOf('/static') === 0 || p.indexOf('/api') === 0) return null;
    if (p === '/sw.js' || p.indexOf('/widget-lab') === 0) return null;   // pas de shell
    return url;
  }

  function alreadyLoaded(absSrc) {
    var s = document.getElementsByTagName('script');
    for (var i = 0; i < s.length; i++) { if (s[i].src === absSrc) return true; }
    return false;
  }

  /* Exécute les scripts du fragment DANS L'ORDRE : externes (une fois) puis inline. */
  function runScripts(scripts, done) {
    var i = 0;
    function next() {
      if (i >= scripts.length) { done(); return; }
      var node = scripts[i++];
      var src = node.getAttribute('src');
      if (src) {
        var abs = new URL(src, location.href).href;
        if (alreadyLoaded(abs)) { next(); return; }        // dédup inter-navigations
        var s = document.createElement('script');
        s.src = src; s.async = false;
        if (node.defer) s.defer = true;
        s.onload = next; s.onerror = next;                  // ne bloque jamais la nav
        document.body.appendChild(s);
      } else {
        try {
          var inl = document.createElement('script');
          inl.textContent = node.textContent;               // IIFE → portée isolée
          document.body.appendChild(inl);
          inl.parentNode.removeChild(inl);                   // DOM propre
        } catch (e) { /* une page cassée ne casse pas la nav */ }
        next();
      }
    }
    next();
  }

  function updateCrumb(spaceLabel, subLabel) {
    var el = document.querySelector('.vx-breadcrumb'); if (!el) return;
    var h = '<span class="vx-crumb-root">Vertex</span><span aria-hidden="true">/</span><b></b>';
    el.innerHTML = h;
    el.querySelector('b').textContent = spaceLabel;
    if (subLabel) {
      var sep = document.createElement('span'); sep.setAttribute('aria-hidden', 'true'); sep.textContent = '/';
      var sub = document.createElement('span'); sub.textContent = subLabel;
      el.appendChild(sep); el.appendChild(sub);
    }
  }

  function updateActive(active) {
    document.querySelectorAll('.vx-sidebar .vx-nav-item[data-nav-id]').forEach(function (a) {
      if (a.getAttribute('data-nav-id') === active) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    var path = location.pathname;
    document.querySelectorAll('.vx-mobile-bar a[href]').forEach(function (a) {
      if (a.getAttribute('href') === path) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  function setTicker(href) {
    var m = href.match(/^\/analysis\/([A-Za-z.\-]{1,8})/);
    if (m && VX.store) VX.store.set('active_ticker', m[1].toUpperCase());
  }

  var seq = 0;
  function navigate(url, opts) {
    opts = opts || {};
    var href = url.pathname + url.search + url.hash;
    var myseq = ++seq;
    startBar();
    fetch(href, { headers: { 'X-Vertex-Fragment': '1' }, credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('http');
        return r.text().then(function (t) { return { t: t, url: r.url, redirected: r.redirected }; });
      })
      .then(function (res) {
        if (myseq !== seq) return;                          // navigation supplantée
        var doc = new DOMParser().parseFromString(res.t, 'text/html');
        var frag = doc.querySelector('.vx-fragment');
        var tpl = doc.querySelector('template.vx-frag-content');
        if (!frag || !tpl) throw new Error('not-fragment');  // page non-shell → dure
        var scripts = [];
        doc.querySelectorAll('script').forEach(function (s) { scripts.push(s); });
        var inlineN = 0;
        scripts.forEach(function (s) { if (!s.getAttribute('src')) inlineN++; });
        var externalN = scripts.length - inlineN;
        if (inlineN === 0 && externalN > 0) throw new Error('external-only'); // repli dur

        try { VX.page._teardown(); } catch (e) {}            // arrête page sortante

        var main = contentEl();
        main.innerHTML = tpl.innerHTML;
        main.setAttribute('data-space', frag.getAttribute('data-active') || '');
        main.setAttribute('data-page-label', frag.getAttribute('data-page-label') || '');
        document.title = (frag.getAttribute('data-title') || 'Vertex') + ' · Vertex';
        updateCrumb(frag.getAttribute('data-space-label') || '', frag.getAttribute('data-sub-label') || '');
        updateActive(frag.getAttribute('data-active') || '');

        var finalHref = href;
        if (res.redirected && res.url) { var u = new URL(res.url); finalHref = u.pathname + u.search; }
        if (opts.push !== false) history.pushState({ vx: 1 }, '', finalHref);
        if (VX.store) VX.store.pushNav(finalHref);
        setTicker(finalHref);

        if (opts.scrollY != null) window.scrollTo(0, opts.scrollY); else window.scrollTo(0, 0);

        runScripts(scripts, function () {
          if (myseq !== seq) return;
          endBar();
          VX.bus.emit('vx:navigated', { href: finalHref });
        });
      })
      .catch(function () { endBar(); hard(href); });
  }

  /* Interception des clics de liens internes (délégation globale). */
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var url = internalURL(a);
    if (!url) return;
    e.preventDefault();
    navigate(url, { push: true });
  });

  window.addEventListener('popstate', function () {
    navigate(new URL(location.href), { push: false });
  });

  /* API programmatique (utilisée par les navigations « location.href » migrables). */
  VX.router = {
    go: function (href) { try { navigate(new URL(href, location.href), { push: true }); } catch (e) { hard(href); } },
    navigate: navigate,
  };

  /* Ancre l'entrée d'historique initiale pour que popstate ait toujours un état. */
  try { history.replaceState({ vx: 1 }, '', location.pathname + location.search); } catch (e) {}
  if (VX.store) VX.store.pushNav(location.pathname + location.search);
})();
