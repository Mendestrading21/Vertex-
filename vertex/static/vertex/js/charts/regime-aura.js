/* regime-aura.js — REGIME AURA (widget officiel W01, réalisé en live).
   Le régime de marché comme une atmosphère : halo coloré par l'état, couronne
   de confiance SEGMENTÉE, grammaire boursière (SPX vs MM200 · breadth · VIX)
   et conclusion « risque neuf autorisé / bloqué » + invalidation.
   L'UI ne calcule rien : elle trace ce que renvoient les moteurs (régime,
   confiance, new_risk_allowed, invalidation). Donnée absente → état honnête.

   LOT 629 — refonte du dessin après rejet de la version en arc plein.
   Ce qui a changé et POURQUOI :

   1. L'échelle est visible. L'arc plein en dégradé continu (.18 → .95) était
      peint sur TOUTE la course quelle que soit la confiance : rien ne disait où
      s'arrêtait la mesure. La couronne segmentée montre les crans éteints — la
      confiance se COMPTE (62 % = 19 crans allumés sur 30), elle ne se devine
      plus.
   2. Le fond est calme. Deux ellipses floutées + un dégradé radial plein cadre
      se superposaient derrière le texte : un halo unique, borné, les remplace.
   3. Pas de fausse précision. Un cran est allumé quand son MILIEU est atteint —
      arrondi honnête, jamais un demi-cran allumé qui suggère le centième.
   4. Le verdict ne se répète plus (voir `_sansRedite`).
*/
(function () {
  'use strict';
  const VX = window.VX;
  const C = window.VXCharts = window.VXCharts || {};

  /* Tonalité dérivée UNIQUEMENT des données moteur (aucune couleur décorative). */
  function toneOf(o) {
    if (o.newRisk === true) return 'go';
    if (o.newRisk === false) return 'risk';
    return 'wait';
  }
  const TONE_COLOR = { go: 'var(--vx-positive)', risk: 'var(--vx-negative)', wait: 'var(--vx-warning)' };
  const ETEINT = 'var(--vx-border-default)';
  const ENCRE = 'var(--vx-text,#F8F5F3)';

  function arc(cx, cy, r, d0, d1) {
    const a0 = d0 * Math.PI / 180, a1 = d1 * Math.PI / 180;
    const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
    const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
    const large = Math.abs(d1 - d0) > 180 ? 1 : 0;
    return `M${x0.toFixed(1)},${y0.toFixed(1)} A${r},${r} 0 ${large} 1 ${x1.toFixed(1)},${y1.toFixed(1)}`;
  }

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  /* Clé de SENS : minuscules, accents retirés, ponctuation réduite à l'espace.
     Sert uniquement à comparer deux phrases, jamais à en afficher une. */
  const cle = (s) => String(s == null ? '' : s).toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ').trim();

  /* LOT 629 — la ligne de verdict disait deux fois la même chose :
       « Risque neuf BLOQUÉ · Régime UNKNOWN — risque neuf bloqué »
     Le verdict vient de `new_risk_allowed`, l'invalidation d'un texte éditorial
     qui le reformule souvent. On garde le verdict (il est structuré, donc sûr)
     et on ne conserve de l'invalidation que les fragments qui AJOUTENT quelque
     chose. Comparaison sur la clé de sens : « BLOQUÉ » et « bloqué » sont le
     même mot, la casse et l'accent ne doivent pas faire passer une redite. */
  function _sansRedite(invalidation, verdict) {
    const brut = String(invalidation == null ? '' : invalidation).trim();
    if (!brut) return '';
    const kv = cle(verdict);
    if (!kv) return brut;
    const morceaux = brut.split(/\s*[—–·]\s*|\s+-\s+/)
      .map((p) => p.trim())
      .filter((p) => {
        const kp = cle(p);
        return kp && kp !== kv && kp.indexOf(kv) < 0 && kv.indexOf(kp) < 0;
      });
    return morceaux.join(' — ');
  }

  C.regimeAura = function (host, opts) {
    const el = typeof host === 'string' ? document.getElementById(host) : host;
    if (!el) return null;
    const o = opts || {};

    /* État honnête : régime indéterminé → pas d'objet, message assumé.
       LOT 629 — `!o.regime` ne suffisait PAS. Le moteur ne rend pas une valeur
       vide quand il ne tranche pas : il rend la CHAÎNE 'UNKNOWN', qui est
       truthy. Le garde ne se déclenchait donc jamais, et Vertex dessinait une
       jauge complète — repère à zéro, arc corail — pour un régime qu'il n'a PAS
       mesuré. Deux mensonges dans un seul objet : une absence présentée comme
       une lecture, et une indétermination peinte dans la couleur qui, par la
       charte, signifie « perte / risque RÉEL ».
       La confiance nulle, elle, N'entre PAS dans ce garde : un régime mesuré
       avec 0 % de confiance reste une lecture. C'est la couronne éteinte qui le
       dit, pas la disparition de l'objet. */
    const indetermine = !o.regime
      || /^(unknown|inconnu|n\/?d|nd|none|null)$/i.test(String(o.regime).trim());
    if (o.state === 'empty' || indetermine) {
      el.innerHTML = VX.states.empty(o.stateMessage || 'Régime indéterminé — Vertex ne tranche pas.');
      return null;
    }
    if (o.state === 'error') {
      el.innerHTML = VX.states.error(o.stateMessage || 'Régime indisponible.');
      return null;
    }

    const tone = toneOf(o);
    const col = TONE_COLOR[tone];
    const conf = (o.confidence == null || isNaN(o.confidence)) ? null : Math.max(0, Math.min(100, o.confidence));
    const uid = 'ra' + Math.round((o.confidence || 0) + (o.regime || '').length * 7);
    const W = 320, H = 150, cx = W / 2, cy = 98, R = 64;
    const A0 = 152, COURSE = 236, CRANS = 30;

    /* COURONNE SEGMENTÉE — un cran est allumé quand son MILIEU est atteint.
       Les crans allumés s'épaississent et gagnent en densité vers le repère :
       la direction de lecture est donnée par la matière, pas par une flèche.
       Confiance absente → couronne entièrement éteinte, et rien d'autre : une
       couronne vide se lit « je ne sais pas », un arc rempli à 0 % se lirait
       « minimum mesuré ».

       BOUTS DROITS, ET C'EST MESURÉ. Première version en `stroke-linecap:round`
       (capture 1440 px) : un bout rond ajoute la MOITIÉ de l'épaisseur à chaque
       extrémité, soit 3,25 unités sur un rayon de 64 — 2,9° de chaque côté pour
       un intervalle de 7,87° et un cran dessiné de 4,88°. Les crans allumés
       (épais) se rejoignaient donc et redonnaient l'arc plein que ce lot vient
       de retirer, pendant que les crans éteints (fins) restaient séparés. Le
       défaut se voyait UNIQUEMENT sur la partie allumée : la seule qu'on lit. */
    let couronne = '';
    const pas = COURSE / CRANS, lame = pas * 0.6;
    for (let i = 0; i < CRANS; i++) {
      const part = (i + 0.5) / CRANS * 100;
      const on = conf != null && part <= conf;
      const d = arc(cx, cy, R, A0 + i * pas, A0 + i * pas + lame);
      couronne += `<path d="${d}" fill="none" stroke="${on ? col : ETEINT}"`
        + ` stroke-width="${on ? '7' : '3'}" stroke-linecap="butt"`
        + ` opacity="${on ? (0.62 + 0.38 * part / 100).toFixed(2) : '.9'}"/>`;
    }

    /* Repère : trait court POSÉ À L'EXTÉRIEUR de la couronne. Il ne recouvre
       aucun cran — la mesure reste lisible sous lui. */
    let repere = '';
    if (conf != null) {
      const a = (A0 + conf / 100 * COURSE) * Math.PI / 180;
      const pt = (rr) => [cx + rr * Math.cos(a), cy + rr * Math.sin(a)];
      const [x0, y0] = pt(R + 7), [x1, y1] = pt(R + 15);
      repere = `<line x1="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}"`
        + ` stroke="${ENCRE}" stroke-width="2.6" stroke-linecap="round" opacity=".95"/>`;
    }

    const g = o.grammar || {};
    const chip = (label, value) =>
      `<span class="vx-ra-chip"><span class="k">${label}</span><span class="v">${value}</span></span>`;
    const chips = [];
    if (g.roro) chips.push(chip('Marché', esc(g.roro)));
    if (g.breadth != null) chips.push(chip('Breadth &gt;MM200', VX.fmt.nd(g.breadth) + ' %'));
    if (g.vix != null) chips.push(chip('VIX', VX.fmt.nd(g.vix)));

    const confTxt = conf == null ? 'confiance n/d' : Math.round(conf) + ' % confiance';
    const verdict = o.newRisk === true ? 'Risque neuf autorisé'
      : o.newRisk === false ? 'Risque neuf BLOQUÉ' : 'Régime à confirmer';
    const reste = _sansRedite(o.invalidation, verdict);
    const inval = reste ? (' · ' + reste) : '';
    const regime = String(o.regime).trim();
    const aria = `Régime ${regime}, ${confTxt}. ${verdict}${inval}`;

    el.innerHTML =
      `<div class="vx-regime-aura" role="img" aria-label="${esc(aria)}">
        <svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:0 auto">
          <defs>
            <radialGradient id="${uid}h" cx="50%" cy="50%" r="50%">
              <stop offset="0" stop-color="${col}" stop-opacity=".30"/>
              <stop offset="58%" stop-color="${col}" stop-opacity=".07"/>
              <stop offset="100%" stop-color="${col}" stop-opacity="0"/></radialGradient>
          </defs>
          <ellipse cx="${cx}" cy="${cy - 6}" rx="106" ry="54" fill="url(#${uid}h)"/>
          <circle cx="${cx}" cy="${cy - 4}" r="44" fill="var(--vx-surface)" fill-opacity=".5"/>
          ${couronne}
          ${repere}
          <text x="${cx}" y="${cy - 6}" text-anchor="middle" fill="${ENCRE}" font-size="18" font-weight="800" letter-spacing=".5">${esc(regime)}</text>
          <text x="${cx}" y="${cy + 13}" text-anchor="middle" fill="${conf == null ? 'var(--vx-text-muted,#989092)' : col}" font-size="10.5" font-weight="${conf == null ? '400' : '800'}">${confTxt}</text>
        </svg>
        ${chips.length ? `<div class="vx-ra-grammar">${chips.join('')}</div>` : ''}
        <div class="vx-ra-verdict" data-tone="${tone}">▸ ${esc(verdict)}${esc(inval)}</div>
      </div>` +
      `<div class="vx-chart-foot">${VX.updateIndicator(o.timestamp, o.source || 'Moteur de régimes', o.mode || 'delayed')}</div>`;
    return el;
  };
})();
