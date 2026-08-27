/* Vertex Shell — interactions du squelette : sidebar, topbar, palette,
   drawers, modals, notifications, connexions, horloge, retour contextuel. */
(function () {
  'use strict';
  const VX = window.VX;
  const $ = (id) => document.getElementById(id);
  const app = $('vx-app');

  /* ── Sidebar (état persistant vxSidebarState) ────────────────────── */
  try {
    const saved = localStorage.getItem('vxSidebarState');
    if (saved === 'collapsed') app.dataset.sidebar = 'collapsed';
  } catch (e) {}
  $('vx-collapse-btn')?.addEventListener('click', () => {
    const next = app.dataset.sidebar === 'collapsed' ? 'expanded' : 'collapsed';
    app.dataset.sidebar = next;
    try { localStorage.setItem('vxSidebarState', next); } catch (e) {}
  });
  /* Mobile drawer nav */
  const mobileNavBtn = $('vx-mobile-nav-btn');
  if (window.matchMedia('(max-width:640px)').matches && mobileNavBtn) mobileNavBtn.style.display = 'inline-flex';
  mobileNavBtn?.addEventListener('click', () => {
    app.dataset.mobileNav = app.dataset.mobileNav === 'open' ? 'closed' : 'open';
    overlay(app.dataset.mobileNav === 'open');
  });
  $('vx-mobile-more')?.addEventListener('click', () => {
    /* Espaces ABSENTS de la barre mobile (briefing/opportunités/portefeuille/
       analyse/performance y sont déjà) — Marchés est fusionné dans le Dashboard. */
    VX.shell.openDrawer('Navigation', ['options', 'intelligence', 'system'].map(id => {
      const it = { options: ['Options', '/options'], intelligence: ['Intelligence', '/intelligence'], system: ['Système', '/system'] }[id];
      return `<a class="vx-nav-item" href="${it[1]}">${it[0]}</a>`;
    }).join(''));
  });

  /* ── Overlay / drawer / modal ────────────────────────────────────── */
  let lastFocus = null;
  function overlay(open) { $('vx-overlay').dataset.open = open ? '1' : '0'; }
  function focusable(container) {
    return Array.from(container.querySelectorAll(
      'button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'
    )).filter(el => !el.hidden && el.getAttribute('aria-hidden') !== 'true'
      && (!el.getClientRects || el.getClientRects().length));
  }
  function trapFocus(container) {
    const items = focusable(container);
    if (items.length) items[0].focus();
  }
  /* A11y (lot 209) : un panneau FERMÉ est invisible aux lecteurs d'écran et
     infocusable — aria-hidden + inert posés fermé, retirés à l'ouverture. */
  function panelOpen(el) { el.dataset.open = '1'; el.removeAttribute('aria-hidden'); el.removeAttribute('inert'); }
  function panelClose(el) { el.dataset.open = '0'; el.setAttribute('aria-hidden', 'true'); el.setAttribute('inert', ''); }
  const shell = VX.shell = {
    openDrawer(title, html, options) {
      const opts = options || {};
      const drawer = $('vx-drawer');
      lastFocus = document.activeElement;
      ($('vx-drawer-title')||{}).textContent = title;
      ($('vx-drawer-body')||{}).innerHTML = html;
      ($('vx-drawer-footer')||{}).innerHTML = opts.footerHtml || '';
      ($('vx-drawer-tabs')||{}).innerHTML = opts.tabsHtml || '';
      $('vx-drawer-tabs').hidden = !opts.tabsHtml;
      drawer.dataset.variant = opts.variant === 'summary' || opts.variant === 'detail'
        ? opts.variant : 'default';
      drawer.setAttribute('aria-label', title || 'Panneau contextuel');
      panelOpen(drawer); overlay(true);
      trapFocus(drawer);
    },
    closeDrawer() {
      const drawer = $('vx-drawer');
      panelClose(drawer); overlay(false);
      $('vx-drawer-tabs').hidden = true;
      lastFocus?.focus?.();
    },
    openModal(title, bodyHtml, footerHtml) {
      lastFocus = document.activeElement;
      ($('vx-modal-title')||{}).textContent = title;
      ($('vx-modal-body')||{}).innerHTML = bodyHtml;
      ($('vx-modal-footer')||{}).innerHTML = footerHtml || '';
      panelOpen($('vx-modal'));
      trapFocus($('vx-modal'));
    },
    closeModal() { panelClose($('vx-modal')); lastFocus?.focus?.(); },
    closeAll() {
      shell.closeDrawer(); shell.closeModal();
      $('vx-palette').dataset.open = '0';
      $('vx-context-menu').dataset.open = '0';
      app.dataset.mobileNav = 'closed'; overlay(false);
    },
  };
  document.querySelectorAll('[data-close-drawer]').forEach(b => b.addEventListener('click', shell.closeDrawer));
  document.querySelectorAll('[data-close-modal]').forEach(b => b.addEventListener('click', shell.closeModal));
  $('vx-overlay').addEventListener('click', shell.closeAll);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { shell.closeAll(); return; }
    if (e.key !== 'Tab') return;
    const panel = [$('vx-palette'), $('vx-modal'), $('vx-drawer')]
      .find(el => el && el.dataset.open === '1');
    if (!panel) return;
    const items = focusable(panel); if (!items.length) return;
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ── Retour contextuel (§15) ─────────────────────────────────────── */
  const backBtn = $('vx-back-btn');
  const ctx = VX.context.get();
  const SPACE_LABELS = { '/': 'au dashboard', '/opportunities': 'aux opportunités', '/portfolio': 'au portefeuille', '/analysis': 'à l’analyse', '/performance': 'à la performance', '/intelligence': 'à l’intelligence', '/system': 'au système' };
  if (ctx && ctx.from && ctx.from !== location.pathname && backBtn) {
    const label = ctx.view === 'watchlist' ? 'Retour à la watchlist' : ('Retour ' + (SPACE_LABELS[ctx.from] || 'à ' + (ctx.label || ctx.from)));
    backBtn.querySelector('span').textContent = label;
    backBtn.dataset.visible = '1';
    backBtn.addEventListener('click', () => {
      const url = new URL(ctx.from, location.origin);
      if (ctx.view) url.searchParams.set('view', ctx.view);
      location.href = url.pathname + url.search;
    });
  }
  VX.context.restoreIfReturning();

  /* ── Horloge & session marché (heure New York) + compte à rebours ──── */
  function untilNext(day, mins) {
    // Séance régulière NYSE 09:30–16:00 (570–960 min). Renvoie l'événement suivant
    // (ouverture/fermeture) et les minutes restantes — cohérent avec le marché réel.
    if (day >= 1 && day <= 5 && mins >= 570 && mins < 960) return { ev: 'ferme', u: 960 - mins };
    if (day >= 1 && day <= 5 && mins < 570) return { ev: 'ouvre', u: 570 - mins };
    // Après la clôture ou week-end → prochaine ouverture d'un jour ouvré à 09:30.
    let u = 1440 - mins, d = (day + 1) % 7;
    while (d === 0 || d === 6) { u += 1440; d = (d + 1) % 7; }
    return { ev: 'ouvre', u: u + 570 };
  }
  function tickClock() {
    const el = $('vx-session'); if (!el) return;
    try {
      const ny = new Date().toLocaleTimeString('fr-FR', { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit' });
      const nyDate = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/New_York' }));
      const day = nyDate.getDay(), mins = nyDate.getHours() * 60 + nyDate.getMinutes();
      const open = day >= 1 && day <= 5 && mins >= 570 && mins < 960;
      const pre = day >= 1 && day <= 5 && mins >= 240 && mins < 570;
      const label = open ? 'Marché ouvert' : (pre ? 'Pré-marché' : 'Marché fermé');
      const dotCol = open ? 'var(--vx-positive)' : (pre ? 'var(--vx-warning)' : 'var(--vx-text-faint)');
      const nx = untilNext(day, mins), h = Math.floor(nx.u / 60), m = nx.u % 60;
      const cd = (h >= 1 ? h + ' h ' : '') + (m < 10 ? '0' + m : m) + ' min';
      el.innerHTML = `<b><span class="vx-live-dot" style="display:inline-block;margin-right:5px;background:${dotCol}"></span>${label}</b>`
        + `<br><span class="vx-muted">New York ${ny} · ${nx.ev} dans ${cd}</span>`;
    } catch (e) { /* fuseaux non dispo */ }
  }
  tickClock(); setInterval(tickClock, 30000);

  /* ── État global (sidebar footer) + connexions ───────────────────── */
  /* ── Mode offline / dégradé (§13) : on ne montre JAMAIS un écran vide parce
     qu'une source est indisponible. Hors ligne → on marque l'état, on garde les
     dernières données (cache persistant LOT 3) et la navigation ; au retour, on
     revalide. Bascule online/offline via les événements réseau ET l'échec des
     requêtes de statut. ── */
  function setNet(state) {
    const prev = document.documentElement.getAttribute('data-net') || 'online';
    document.documentElement.setAttribute('data-net', state);
    if (VX.store) VX.store.set('connection_state', state);
    if (prev === state) return;
    const el = $('vx-global-status');
    if (state === 'offline') {
      if (el) {
        const d = el.querySelector('.vx-dot'), l = el.querySelector('.vx-status-label');
        if (d) d.style.background = 'var(--vx-negative)';
        if (l) l.textContent = 'Hors ligne';
      }
      try { VX.toast('Hors ligne — dernières données conservées', 'warn', 3200); } catch (e) {}
    } else {
      try { VX.toast('Reconnecté', 'success', 2000); } catch (e) {}
      VX.bus.emit('vx:data-refreshed', { reason: 'reconnect' });
    }
  }
  try { setNet(navigator.onLine === false ? 'offline' : 'online'); } catch (e) {}
  window.addEventListener('offline', function () { setNet('offline'); });
  window.addEventListener('online', function () { setNet('online'); loadStatus(); });

  async function loadStatus() {
    try {
      const st = await VX.fetch('/api/live/status', { ttl: 60000 });
      // HONNÊTETÉ réseau : le statut peut être servi du cache persistant pendant une
      // vraie coupure — ne JAMAIS annoncer « Reconnecté » si le navigateur est hors ligne.
      if (navigator.onLine !== false) setNet('online');
      const el = $('vx-global-status'); if (!el) return;
      const demo = !!st.demo;
      const dot = el.querySelector('.vx-dot'); const label = el.querySelector('.vx-status-label');
      dot.style.background = demo ? 'var(--vx-warning)' : 'var(--vx-positive)';
      label.textContent = demo ? 'Mode démo' : 'Données actives';
      window.__vxStatus = st;
      VX.bus.emit('vx:connection-changed', st);
    } catch (e) {
      if (navigator.onLine === false) setNet('offline');   // échec réseau réel → dégradé
    }
  }
  loadStatus(); VX.refresh.register(loadStatus, 90000, 'status', { persistent: true });

  /* ── Session d'analyse : détection de NOUVELLE session + bascule atomique ──
     (CONTINUITY LOT 5) On surveille le manifest ; quand le session_id change (un
     nouveau scan s'est publié), on bascule d'un coup : le store est mis à jour, le
     cache instantané (snapshot) est invalidé, une notification discrète paraît, et
     toutes les pages se rechargent via vx:data-refreshed. Aucun recalcul, lecture seule. */
  let _lastSessionNotify = 0;
  const SESSION_NOTIFY_THROTTLE = 600000;   // notification visible au plus toutes les 10 min
  async function watchSession() {
    let m;
    try { m = await VX.fetch('/api/session/manifest', { ttl: 0 }); } catch (e) { return; }
    if (!m || !m.session_id) return;                     // scan pas encore publié → on ré-essaiera
    VX.store.set('session_status', m.status);
    VX.store.set('active_session_id', m.session_id);     // base des badges de fraîcheur

    /* Le cache de données est ALIGNÉ sur la session courante (l'identifiant est
       persisté avec le cache en sessionStorage). Dès que la session observée diffère
       de celle du cache, on invalide et on recharge :
       - 1re publication APRÈS un démarrage à froid (le cache tenait un état vide/partiel) ;
       - nouveau scan (bascule 30 min).
       → on ne reste JAMAIS figé sur un écran de démarrage vide (régime UNKNOWN / n/d).
       Même session ⇒ on ne touche à rien ⇒ navigation instantanée. */
    let aligned = null;
    try { aligned = sessionStorage.getItem('vxCacheSession'); } catch (e) {}
    if (m.session_id === aligned) return;                // session inchangée → cache valide
    try { sessionStorage.setItem('vxCacheSession', m.session_id); } catch (e) {}
    VX.store.set('previous_session_id', aligned);
    // invalide le snapshot de scan ; garde le desk perso ET le manifest (toujours réseau)
    VX.fetch.invalidate((u) => u.indexOf('/api/desk') !== 0 && u.indexOf('/api/session/manifest') !== 0);
    VX.bus.emit('vx:session-changed', m);
    VX.bus.emit('vx:data-refreshed', { reason: aligned == null ? 'session-ready' : 'session-switch' });
    // Notification visible SEULEMENT pour une vraie bascule (pas le 1er alignement à froid),
    // throttlée (~10 min) pour ne pas spammer.
    if (aligned != null) {
      const now = Date.now();
      if (now - _lastSessionNotify >= SESSION_NOTIFY_THROTTLE) {
        _lastSessionNotify = now;
        const bits = ['Analyse mise à jour'];
        if (m.as_of) bits.push('Session ' + m.as_of);
        if (m.scanned) bits.push(m.scanned + ' sociétés');
        if (m.quality_pct != null) bits.push('qualité ' + m.quality_pct + ' %');
        try { VX.toast(bits.join(' · '), 'success', 4200); } catch (e) {}
      }
    }
  }
  watchSession(); VX.refresh.register(watchSession, 60000, 'session-watch', { persistent: true });

  $('vx-connections-btn')?.addEventListener('click', async () => {
    let st = window.__vxStatus, diag = null;
    try { diag = await VX.fetch('/api/system/diagnostics', { ttl: 30000 }); } catch (e) {}
    const ib = st && !st.demo ? (st.domains?.quotes?.fresh ? 'live' : 'delayed') : 'offline';
    const rows = [
      ['IBKR', ib === 'live' ? 'Live' : (ib === 'delayed' ? 'Différé' : 'Hors ligne'), ib],
      ['TradingView', diag?.tradingview ? `${diag.tradingview.stored} signaux stockés` : 'non configuré', diag?.tradingview?.stored ? 'live' : 'fallback'],
      ['Claude', diag?.ai ? `${diag.ai.ok}/${diag.ai.total} analyses OK` : 'non configuré', diag?.ai?.total ? 'live' : 'fallback'],
      ['Synchronisation', 'desk /api/desk (last-writer-wins)', 'live'],
      ['Qualité des données', st?.demo ? 'DÉMO (synthétique, jamais réel)' : 'voir Système / Données', st?.demo ? 'fallback' : 'live'],
    ].map(([name, detail, mode]) =>
      `<div class="vx-kv"><span class="k">${name}</span><span class="v"><span class="vx-badge vx-badge-status" data-status="${mode}"><span class="vx-dot"></span>${detail}</span></span></div>`
    ).join('');
    VX.shell.openDrawer('Connexions', rows +
      '<div class="vx-mt4"><a class="vx-btn" href="/system?view=connections">Ouvrir Système / Connexions</a></div>');
  });

  /* ── Notifications (§42) ─────────────────────────────────────────── */
  const notifs = VX.notifications = {
    _items: [],
    push(item) {
      this._items.unshift(Object.assign({ ts: Date.now(), status: 'unread', priority: 'normal' }, item));
      this._items = this._items.slice(0, 60); this._render();
    },
    markAllRead() { this._items.forEach(i => i.status = 'read'); this._render(); },
    _render() {
      const unread = this._items.filter(i => i.status === 'unread').length;
      const badge = $('vx-notif-badge');
      if (badge) { badge.hidden = !unread; badge.textContent = unread; }
    },
  };
  $('vx-notifs-btn')?.addEventListener('click', async () => {
    try {
      const a = await VX.fetch('/api/alerts/active', { ttl: 20000 });
      (a.active || []).forEach(al => {
        if (!notifs._items.some(n => n.key === al.symbol + al.level)) {
          notifs.push({ key: al.symbol + al.level, category: 'Alerte', title: `${al.symbol} · ${al.level}`, message: al.reason, ticker: al.symbol, priority: al.level === 'ACTIONABLE' ? 'high' : 'normal' });
        }
      });
    } catch (e) {}
    const html = notifs._items.length ? notifs._items.map(n =>
      `<div class="vx-notif-item" data-priority="${VX.esc(n.priority)}"><div class="vx-notif-body">
        <div class="vx-flex vx-between"><b>${VX.esc(n.title)}</b><span class="vx-meta">${VX.fmt.ago(n.ts)}</span></div>
        <div class="vx-dim">${VX.esc(n.message || '')}</div>
        <div class="vx-meta">${VX.esc(n.category || '')}</div></div>
        ${/^[A-Z0-9.\-]{1,10}$/.test(String(n.ticker || '')) ? `<button class="vx-btn vx-btn-sm" onclick="VX.openAnalysis('${n.ticker}')">Analyse</button>` : ''}</div>`
    ).join('') : VX.states.empty('Aucune notification pour le moment.', '');
    VX.shell.openDrawer('Notifications', html);
    notifs.markAllRead();
  });

  /* ── Actualiser ──────────────────────────────────────────────────── */
  $('vx-refresh-btn')?.addEventListener('click', function () { VX.refresh.runAll(this); });

  /* ── Command palette (§14) ───────────────────────────────────────── */
  /* VERTEX 2.0 — les DOUZE pages, dans l'ordre de la navigation, plus leurs
     approfondissements joignables. Une page absente d'ici est une page que la
     recherche globale ne trouve pas : le contrôle 028 de l'audit ne tolère
     aucun écart entre ce que la sidebar propose et ce que la palette atteint.
     Les entrées historiques (Journal, Suivis) restent listées sous leur nouveau
     nom : leurs URL répondent toujours, et quelqu'un peut encore les chercher
     par l'ancien mot. */
  const PAGES = [
    ['Aujourd\'hui', '/'], ['Aujourd\'hui · Marchés', '/#markets'],
    ['Aujourd\'hui · Secteurs', '/#sectors'],
    ['Aujourd\'hui · Pouls (volatilité & breadth)', '/#pulse'],
    ['Aujourd\'hui · Mouvements', '/#topflop'],
    ['Calendrier', '/calendar'], ['Calendrier · Semaine', '/calendar?view=week'],
    ['Calendrier · Agenda', '/calendar?view=agenda'],
    ['Calendrier · Macro', '/calendar?view=macro'],
    ['Calendrier · Portefeuille', '/calendar?view=portfolio'],
    ['Marchés', '/markets'], ['Marchés · Macro', '/markets?view=macro'],
    ['Marchés · Secteurs', '/markets?view=sectors'],
    ['Marchés · Volatilité', '/markets?view=volatility'],
    ['Opportunités', '/opportunities'], ['Opportunités · Options', '/opportunities?view=options'],
    ['Opportunités · Anomalies', '/opportunities?view=anomalies'],
    ['Opportunités · Calendrier', '/opportunities?view=calendar'],
    ['Analyse', '/analysis'], ['Analyse · Comité', '/intelligence?view=committee'],
    ['Options', '/options'], ['Options · Volatilité', '/options?view=volatility'],
    ['Simulateur', '/simulator'], ['Simulateur · Avancé', '/simulator?view=avance'],
    ['Simulateur · Comparer', '/simulator?view=comparer'],
    ['Portefeuille', '/portfolio'], ['Portefeuille · Watchlist', '/portfolio?view=watchlist'],
    ['Portefeuille · Risque', '/portfolio?view=risk'],
    ['Suivi', '/follow-up'], ['Suivi · Suivis (ancienne URL)', '/tracking'],
    ['Performance', '/performance'], ['Performance · Journal', '/performance?view=journal'],
    ['Performance · Track Record', '/performance?view=track-record'],
    ['Performance · Journal (ancienne URL)', '/journal'],
    ['Vertex IA', '/intelligence'],
    ['Système', '/system'], ['Système · Connexions', '/system?view=connections'],
    ['Système · Archive', '/system?view=archive'], ['Système · Design System', '/design-system'],
  ];
  const palette = $('vx-palette'), pInput = $('vx-palette-input'), pList = $('vx-palette-list');
  let pItems = [], pSel = 0, namesCache = null;
  function openPalette() {
    lastFocus = document.activeElement;
    palette.dataset.open = '1'; pInput.value = ''; renderPalette(''); pInput.focus();
  }
  async function tickerMatches(q) {
    if (!q || q.length < 1) return VX.recentTickers.get().slice(0, 5).map(s => ({ sym: s, name: 'récent' }));
    try {
      if (!namesCache) namesCache = (await VX.fetch('/api/names', { ttl: 600000 })) || {};
      const names = namesCache.names || namesCache;
      const qq = q.toUpperCase();
      return Object.entries(names)
        .filter(([sym, name]) => sym.startsWith(qq) || String(name).toUpperCase().includes(qq))
        .slice(0, 6).map(([sym, name]) => ({ sym, name }));
    } catch (e) {
      return /^[A-Za-z.]{1,6}$/.test(q) ? [{ sym: q.toUpperCase(), name: 'ouvrir l’analyse' }] : [];
    }
  }
  async function renderPalette(q) {
    const groups = [];
    const tickers = await tickerMatches(q);
    const ent = window.VXEntities;
    if (tickers.length) groups.push(['Titres', tickers.map(t => ({ label: t.name, mono: t.sym, run: () => VX.openAnalysis(t.sym) }))]);
    if (ent) {
      const qq = q.toUpperCase();
      const pos = ent.positions().filter(p => !qq || p.sym.includes(qq)).slice(0, 4);
      if (pos.length) groups.push(['Positions', pos.map(p => ({ label: `position · ${VX.fmt.nd(p.qty)} @ ${VX.fmt.nd(p.entry)}`, mono: p.sym, run: () => VX.openAnalysis(p.sym) }))]);
      const watch = ent.watchlist().filter(w => !qq || w.sym.includes(qq)).slice(0, 4);
      if (watch.length) groups.push(['Watchlist', watch.map(w => ({ label: w.thesis || 'surveillance', mono: w.sym, run: () => VX.openAnalysis(w.sym) }))]);
      const alerts = ent.alerts().filter(a => !qq || String(a.sym || '').includes(qq)).slice(0, 3);
      if (alerts.length) groups.push(['Alertes', alerts.map(a => ({ label: a.note || a.cond || 'alerte', mono: a.sym, run: () => VX.openAnalysis(a.sym) }))]);
    }
    const ql = q.toLowerCase();
    const pages = PAGES.filter(([label]) => !ql || label.toLowerCase().includes(ql)).slice(0, 7);
    if (pages.length) groups.push(['Pages', pages.map(([label, href]) => ({ label, mono: '→', run: () => location.href = href }))]);
    groups.push(['Actions', [
      { label: 'Ajouter (favori, watchlist, suivi, position, alerte, thèse)', mono: '+', run: () => { shell.closeAll(); window.VXEntities?.openAddModal(q.toUpperCase()); } },
      { label: 'Actualiser les données', mono: '↻', run: () => VX.refresh.runAll($('vx-refresh-btn')) },
    ].filter(a => !ql || a.label.toLowerCase().includes(ql))]);

    pItems = []; pSel = 0;
    pList.innerHTML = groups.filter(([, items]) => items.length).map(([g, items]) =>
      `<div class="vx-palette-group">${g}</div>` + items.map(it => {
        const idx = pItems.push(it) - 1;
        return `<div class="vx-palette-item" role="option" data-idx="${idx}" aria-selected="${idx === 0}">
          <span class="vx-mono">${it.mono || ''}</span><span class="vx-truncate">${it.label}</span></div>`;
      }).join('')).join('');
    pList.querySelectorAll('.vx-palette-item').forEach(el => {
      el.addEventListener('click', () => { pItems[+el.dataset.idx]?.run(); palette.dataset.open = '0'; });
      el.addEventListener('mousemove', () => selectPalette(+el.dataset.idx));
    });
  }
  function selectPalette(i) {
    pSel = Math.max(0, Math.min(pItems.length - 1, i));
    pList.querySelectorAll('.vx-palette-item').forEach(el =>
      el.setAttribute('aria-selected', String(+el.dataset.idx === pSel)));
    pList.querySelector(`[data-idx="${pSel}"]`)?.scrollIntoView({ block: 'nearest' });
  }
  pInput?.addEventListener('input', () => renderPalette(pInput.value.trim()));
  pInput?.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); selectPalette(pSel + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); selectPalette(pSel - 1); }
    else if (e.key === 'Enter') { e.preventDefault(); pItems[pSel]?.run(); palette.dataset.open = '0'; }
  });
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openPalette(); }
  });
  /* Lot 302 : ne JAMAIS ouvrir au focus — le Tab clavier traversait le champ
     et la palette s'ouvrait de force (les boutons du topbar devenaient
     inatteignables au clavier). Ouverture : clic/tap (inchangé) ou FRAPPE
     dans le champ (le caractère saisi amorce la recherche de la palette). */
  $('vx-global-search')?.addEventListener('click', openPalette);
  $('vx-global-search')?.addEventListener('keydown', (e) => {
    if (e.key === 'Tab' || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === 'Enter' || e.key === 'ArrowDown' || e.key.length === 1) {
      e.preventDefault(); openPalette();
      if (e.key.length === 1) { pInput.value = e.key; renderPalette(e.key); }
    }
  });
  /* Lot 291 : la palette est un fond plein écran sans Échap au tactile —
     le tap sur le fond (hors boîte) ferme, comme tout dialogue. */
  palette?.addEventListener('click', (e) => { if (e.target === palette) palette.dataset.open = '0'; });

  /* ── + Ajouter (§19) ─────────────────────────────────────────────── */
  $('vx-add-btn')?.addEventListener('click', () => window.VXEntities?.openAddModal());

  /* ── Sauvegarde du contexte avant de quitter la page ─────────────── */
  window.addEventListener('pagehide', () => {
    if (!location.pathname.startsWith('/analysis/')) VX.context.save();
  });

  /* ── Service worker : offline + précache (LOT 82) ──────────────────
     Le shell canonique n'enregistrait JAMAIS /sw.js (seules les pages
     legacy le faisaient) : aucun offline sur les 8 espaces. */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    });
  }
})();
