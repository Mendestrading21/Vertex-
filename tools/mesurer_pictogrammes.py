"""tools/mesurer_pictogrammes.py — QUELS PICTOGRAMMES SONT VRAIMENT PEINTS ?

`VISUAL_SYSTEM.md` : « une seule famille outline », « pas d'icônes
multicolores ». `COPY.md` : « emoji comme ponctuation de produit » est un
interdit. Des lots précédents ont retiré des pictogrammes ; il en reste, et la
question honnête n'est pas « en trouve-t-on dans le code ? » mais **« l'écran
en montre-t-il ? »**.

## Pourquoi un navigateur, et pas un `grep`

Mesuré sur les huit pages : les octets servis contiennent 🔴, 🟠, ✅, 🔒 — et
**aucun n'est peint**. Ils vivent dans des commentaires JS servis et dans une
comparaison de chaîne (`sev === '🔴'`). Un `grep` sur la source, ou même sur le
HTML servi, aurait accusé quatre pictogrammes fantômes ; c'est exactement la
faute que la série corrige depuis le lot 35 : *comparer par le texte ce qu'il
faut comparer par la structure*.

L'outil sépare donc deux populations, et ne les confond jamais :

- **PEINT** — présent dans le texte rendu (`innerText`) ou dans un attribut
  lisible par l'utilisateur (`aria-label`, `title`, `alt`). C'est ce que
  l'interface montre ou annonce.
- **SERVI SEULEMENT** — présent dans les octets, absent de l'écran. Du poids,
  parfois une fragilité (une égalité de chaîne sur un pictogramme casse en
  silence si un sélecteur de variante s'ajoute), mais pas une faute visuelle.

## Anti-vacuité

Un détecteur qui ne trouve rien ne prouve rien. Avant de conclure, l'outil
**injecte** un pictogramme témoin dans la page et exige de le revoir dans son
relevé. S'il ne le revoit pas, il rend 2 (aveugle) plutôt qu'un faux vert.

Usage : python tools/mesurer_pictogrammes.py [--base http://127.0.0.1:5002]
"""
import re
import sys
import unicodedata

#  Plages de pictogrammes. Les chiffres, lettres et ponctuation ordinaire n'y
#  sont pas : on cherche des DESSINS, pas du texte.
_PLAGES = (
    (0x2190, 0x21FF),    # flèches
    (0x2300, 0x23FF),    # technique divers (⌘, ⏩…)
    (0x2500, 0x257F),    # filets de tableau
    (0x2580, 0x259F),    # pavés
    (0x25A0, 0x25FF),    # formes géométriques
    (0x2600, 0x26FF),    # symboles divers (⚠, ★…)
    (0x2700, 0x27BF),    # casseau (✕, ✓…)
    (0x2B00, 0x2BFF),    # flèches et formes supplémentaires
    (0x1F300, 0x1FAFF),  # emoji
)

#  Emoji au sens strict : ceux que `COPY.md` interdit comme ponctuation, et que
#  `VISUAL_SYSTEM.md` interdit comme icône (ils sont multicolores par nature —
#  aucun token ne peut les repeindre).
def est_emoji(ch):
    cp = ord(ch)
    return cp >= 0x1F300 or ch in '✅❌⚠️🔴🟠🟡🟢'


def est_pictogramme(ch):
    cp = ord(ch)
    return any(a <= cp <= b for a, b in _PLAGES)


def _nom(ch):
    try:
        return unicodedata.name(ch)
    except ValueError:
        return '?'


SONDE = r"""() => {
  const vus = {};
  const ajoute = (t, ou) => {
    if (!t) return;
    for (const ch of String(t)) {
      const cp = ch.codePointAt(0);
      if (cp < 0x2190) continue;
      (vus[ch] = vus[ch] || {n: 0, ou: []}).n++;
      if (vus[ch].ou.length < 3) vus[ch].ou.push(ou);
    }
  };
  ajoute(document.body.innerText, 'texte');
  for (const e of document.querySelectorAll('[aria-label],[title],[alt]')) {
    ajoute(e.getAttribute('aria-label'), 'aria-label');
    ajoute(e.getAttribute('title'), 'title');
    ajoute(e.getAttribute('alt'), 'alt');
  }
  /*  LES PSEUDO-ELEMENTS, angle mort declare du lot 41.
      `innerText` ne les voit pas : un pictogramme pose par CSS
      (`::before { content: "…" }`) est PEINT a l'ecran et absent du texte.
      Le produit s'en sert (chevrons, puces), donc l'angle mort n'etait pas
      theorique. On lit la propriete calculee, et on ignore `none`/`normal`
      ainsi que les valeurs non litterales (`attr()`, `counter()`), qui ne
      portent pas de glyphe par elles-memes.  */
  for (const e of document.querySelectorAll('*')) {
    for (const pseudo of ['::before', '::after']) {
      let c;
      try { c = getComputedStyle(e, pseudo).content; } catch (_) { continue; }
      if (!c || c === 'none' || c === 'normal') continue;
      const m = c.match(/^"(.*)"$/s) || c.match(/^'(.*)'$/s);
      if (m) ajoute(m[1], pseudo);
    }
  }
  return vus;
}"""

PAGES = ('/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system')

#  LES ÉTATS QUE LA PAGE D'ACCUEIL NE MONTRE PAS, et c'est tout le lot.
#  Les huit pages ci-dessus ne peignaient que deux signes ; deux EMOJI vivaient
#  pourtant sur `/analysis/<sym>`, dans une branche qui ne s'ouvre que si la
#  donnée remplit la condition. Balayer les seuls écrans d'accueil, c'était
#  mesurer l'état le plus pauvre du produit et appeler ça une couverture.
#
#  Les symboles ne sont PAS inventés : ils sont choisis dans le scan pour la
#  branche qu'ils ouvrent (`_symboles_conditionnels`). Si le jeu de données
#  change et qu'aucun symbole n'ouvre la branche, l'outil le DIT au lieu de
#  balayer une page morte.
BRANCHES = (
    ('ttm_squeeze', '/analysis/%s', 'compression Bollinger/Keltner'),
    ('ttm_fired', '/analysis/%s', 'sortie de compression'),
)

TEMOIN = '\U0001F984'      # licorne : n'existe nulle part dans le produit


def _symboles_conditionnels(base):
    """Un symbole par branche, LU dans le scan servi — jamais choisi d'avance.

    Rend [(url, description)] et la liste des branches restées sans symbole :
    une branche qu'aucune donnée n'ouvre n'est pas « propre », elle est
    NON MESURÉE, et le rapport doit le dire."""
    import json
    import urllib.request
    with urllib.request.urlopen(base + '/scan', timeout=30) as r:
        detail = (json.loads(r.read().decode('utf-8')) or {}).get('detail') or {}
    urls, absentes = [], []
    for champ, gabarit, quoi in BRANCHES:
        sym = next((s for s, d in sorted(detail.items())
                    if isinstance(d, dict) and d.get(champ)), None)
        if sym is None:
            absentes.append('%s (%s)' % (champ, quoi))
        else:
            urls.append((gabarit % sym, '%s — %s' % (champ, quoi)))
    return urls, absentes


def _chromium():
    """Le Chromium réellement présent, ou None (Playwright choisira)."""
    import glob
    import os
    for motif in ('/opt/pw-browsers/chromium-*/chrome-linux/chrome',
                  '/opt/pw-browsers/chromium/chrome'):
        for c in sorted(glob.glob(motif)):
            if os.path.exists(c):
                return c
    return None


def _releve(nav, url, injecter=None):
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900})
    page = ctx.new_page()
    try:
        #  PAS `networkidle` : les pages tiennent un flux SSE (`/api/live/events`)
        #  qui, par conception, ne se termine jamais — le réseau n'est jamais
        #  « au repos » et l'attente expire. Même famille de piège que le
        #  balayage bloqué du lot 33. On attend le DOM, puis l'hydratation.
        page.goto(url, wait_until='domcontentloaded', timeout=45000)
        page.wait_for_timeout(3500)
        if injecter:
            #  DEUX témoins, parce que la sonde a deux organes et qu'un seul
            #  témoin n'en éprouve qu'un. Le nœud de texte éprouve `innerText` ;
            #  la règle CSS éprouve la lecture des pseudo-éléments — celle-là
            #  était l'angle mort déclaré du lot 41, et un angle mort qu'on
            #  ferme sans le vérifier reste un angle mort.
            page.evaluate(
                "t => {"
                " const d = document.createElement('div');"
                " d.textContent = t; d.id = 'vx-temoin-texte';"
                " document.body.appendChild(d);"
                " const s = document.createElement('style');"
                " s.textContent = '#vx-temoin-css::before{content:\"' + t + '\"}';"
                " document.head.appendChild(s);"
                " const p = document.createElement('span');"
                " p.id = 'vx-temoin-css'; document.body.appendChild(p);"
                "}", injecter)
            page.wait_for_timeout(150)
        return page.evaluate(SONDE), page.content()
    finally:
        ctx.close()


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    base = 'http://127.0.0.1:5002'
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]

    from playwright.sync_api import sync_playwright   # import PARESSEUX : la CI
    #  n'installe pas Playwright, et un import au niveau du module rendrait
    #  toute la suite incollectable (mesuré au lot 35).

    peints, servis = {}, {}
    with sync_playwright() as pw:
        #  Chemin EXPLICITE : l'environnement embarque un Chromium, et la
        #  version que Playwright réclame par défaut n'est pas toujours celle
        #  qui est là. Sans ce chemin, l'outil demande une installation que la
        #  consigne interdit (aucun téléchargement).
        nav = pw.chromium.launch(executable_path=_chromium(),
                                 args=['--no-sandbox'])
        try:
            #  Le témoin d'abord : si la sonde ne le revoit pas, tout le reste
            #  du relevé est sans valeur.
            vus, _ = _releve(nav, base + '/', injecter=TEMOIN)
            ou = set((vus.get(TEMOIN) or {}).get('ou') or [])
            manque = [o for o in ('texte', '::before') if o not in ou]
            if manque:
                print('AVEUGLE — le temoin n\'est pas revu par : %s. '
                      'La sonde a deux organes ; un seul qui repond ne prouve '
                      'que celui-la.' % ', '.join(manque))
                return 2
            print('temoin : revu dans le TEXTE et dans un PSEUDO-ELEMENT — '
                  'les deux organes de la sonde repondent')

            conditionnelles, absentes = _symboles_conditionnels(base)
            for u, quoi in conditionnelles:
                print('  branche ouverte : %-28s %s' % (u, quoi))
            for a in absentes:
                print('  BRANCHE NON MESUREE — aucun symbole ne l\'ouvre : %s' % a)

            for p in PAGES + tuple(u for u, _ in conditionnelles):
                vus, html = _releve(nav, base + p)
                for ch, info in vus.items():
                    if not est_pictogramme(ch):
                        continue
                    e = peints.setdefault(ch, {'n': 0, 'pages': set(), 'ou': set()})
                    e['n'] += info['n']
                    e['pages'].add(p)
                    e['ou'].update(info['ou'])
                for ch in set(html):
                    if est_pictogramme(ch) and ch not in vus:
                        servis.setdefault(ch, set()).add(p)
                print('  %-16s peints %2d distincts' % (p, len(
                    [c for c in vus if est_pictogramme(c)])))
        finally:
            nav.close()

    print('\nPEINTS A L\'ECRAN — %d pictogrammes distincts' % len(peints))
    for ch, e in sorted(peints.items(), key=lambda x: -x[1]['n']):
        print('  %s U+%04X ×%-4d %-9s %-28s %s'
              % (ch, ord(ch), e['n'], 'EMOJI' if est_emoji(ch) else 'signe',
                 _nom(ch)[:28], ' '.join(sorted(e['pages']))))

    print('\nSERVIS MAIS JAMAIS PEINTS — %d' % len(servis))
    for ch, pg in sorted(servis.items()):
        print('  %s U+%04X  %s' % (ch, ord(ch), ' '.join(sorted(pg))))

    fautes = {c: e for c, e in peints.items() if est_emoji(c)}
    if fautes:
        print('\n%d EMOJI PEINT(S) — interdit par COPY.md et VISUAL_SYSTEM.md :'
              % len(fautes))
        for ch, e in fautes.items():
            print('  %s ×%d  %s' % (ch, e['n'], ' '.join(sorted(e['pages']))))
        return 1
    print('\nAUCUN EMOJI PEINT.')
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
