"""Instrument — LE ROGNAGE SILENCIEUX.

Dette signalée pendant six lots : rien dans Vertex ne détectait un texte coupé
par un `overflow:hidden` **sans ellipse ni défilement**. C'est le défaut du
lot 209 (quatre cartes d'indice coupées de 25 à 66 px), trouvé alors par hasard
sur une capture d'écran, et que deux instruments de débordement avaient déclaré
inexistant : ils mesuraient le débordement du VIEWPORT, pas celui d'une carte.

## Ce qu'il mesure

Un élément est rogné en silence quand `scrollWidth > clientWidth` (ou
`scrollHeight > clientHeight`), que son conteneur cache le débordement, et que
rien ne le signale — ni ellipse, ni défilement.

## Le faux positif qu'il faut exclure, et pourquoi

Premier jet : 21 à 24 signalements, **tous** sur `.vx-sr-only`. Un texte réservé
aux lecteurs d'écran est rogné DÉLIBÉRÉMENT (boîte de 1×1 px, `overflow:hidden`)
— c'est la technique standard. Sans cette exclusion, l'instrument accuse
précisément l'accessibilité et noie le signal réel.

## Usage

    DEMO=1 NO_IBKR=1 START_ON_IMPORT=1 VERTEX_PORT=5002 python terminal.py &
    python3 tools/mesurer_rognage_silencieux.py

**Vérifier la version servie AVANT de lire le résultat** : un serveur périmé
rend une mesure fausse et convaincante (leçon du lot 03).

## Résultat au lot 13

1440 px : 0 · 390 px : 0, après correction des deux mécanismes trouvés.
"""
import io
import os
import re

from playwright.sync_api import sync_playwright
# LES VUES SONT LUES DANS LA SOURCE, JAMAIS ECRITES A LA MAIN.
# La premiere version de cet outil portait une liste ecrite de memoire : trois
# pages sur huit avaient des noms de vues INEXISTANTS (`shortlist`, `compare`,
# `gex`, `vol`). Une vue inconnue retombe sur la vue par defaut — donc l'outil
# mesurait la meme page plusieurs fois en croyant en couvrir plusieurs, et ne
# visitait jamais `stocks`, `anomalies`, `calendar`, `positioning`… C'est la
# troisieme fois qu'une URL fabriquee me trompe dans cette refonte ; une liste
# derivee de la source ne peut plus diverger.
def _vues(fichier, symbole='_VIEWS'):
    src = io.open(os.path.join('vertex', 'ui', 'pages', fichier), encoding='utf-8').read()
    m = (re.search(symbole + r'\s*=\s*\((.*?)\n\)', src, re.S)
         or re.search(symbole + r'\s*=\s*\((.*?)\)\s*\n\n', src, re.S))
    return re.findall(r"\('([a-z0-9-]+)'\s*,", m.group(1)) if m else ['']


PAGES = [('/', ['']),
         ('/markets', _vues('markets_page.py')),
         ('/opportunities', _vues('opportunities_page.py')),
         ('/analysis', ['']),
         # LA FICHE, pas seulement l'index. Elle etait le seul ecran du produit
         # qu'aucun instrument ne balayait : l'ouvrir declenche des points
         # d'entree interdits dans cet environnement, et j'en avais conclu
         # qu'elle etait « non mesurable ». Elle l'est — en AVORTANT ces points
         # d'entree au navigateur (cf. INTERDITS) : la requete ne part pas,
         # donc le serveur ne sort pas. La mesure est PARTIELLE et le dit :
         # elle porte sur la mise en page, pas sur le rendu des donnees
         # bloquees. Une page a demi mesuree vaut mieux qu'une page declaree
         # hors de portee.
         ('/analysis/ACN', ['']),
         ('/portfolio', _vues('portfolio_page.py')),
         ('/options', _vues('options_intel_page.py')),
         ('/journal', _vues('performance_page.py')),
         ('/system', _vues('system_page.py', 'VIEWS'))]

# Points d'entree que cet environnement interdit d'appeler. Ils sont avortes
# AU NAVIGATEUR : aucune requete ne part, donc aucun appel sortant.
INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
             '**/api/options-for/**', '**/options/*', '**/desc/**')

# Un texte est ROGNE EN SILENCE si son conteneur cache le debordement SANS
# ellipse ni defilement : rien a l'ecran ne signale qu'un mot est coupe.
JS = """() => {
  const out=[];
  document.querySelectorAll('#vx-content *').forEach(e=>{
    const cs=getComputedStyle(e);
    const cacheX = cs.overflowX==='hidden' || cs.overflow==='hidden';
    const cacheY = cs.overflowY==='hidden' || cs.overflow==='hidden';
    const debX = e.scrollWidth  - e.clientWidth  > 1;
    const debY = e.scrollHeight - e.clientHeight > 1;
    if(!((cacheX&&debX)||(cacheY&&debY))) return;
    // `.vx-sr-only` est rogne DELIBEREMENT (1x1 px, overflow hidden) : c'est la
    // technique standard du texte reserve aux lecteurs d'ecran, pas un defaut.
    // Sans cette exclusion l'instrument rend 21 a 24 faux positifs et zero
    // signal — il accuserait precisement l'accessibilite.
    if(e.classList && e.classList.contains('vx-sr-only')) return;
    if(e.closest && e.closest('.vx-sr-only')) return;
    if(e.clientWidth===0 || e.clientHeight===0) return;
    // signale ? ellipse, ou defilement possible
    const ellipse = cs.textOverflow==='ellipsis';
    if(ellipse && debX && !debY) return;
    // element hors ecran / replie : on n'accuse pas
    let anc=e, cache=false;
    while(anc){ if(anc.tagName==='DETAILS'&&!anc.open){cache=true;break;}
      const c2=getComputedStyle(anc); if(c2.display==='none'||c2.visibility==='hidden'){cache=true;break;} anc=anc.parentElement; }
    if(cache) return;
    const txt=(e.textContent||'').trim();
    if(!txt) return;
    out.push({cls:(e.className||'').toString().slice(0,40), tag:e.tagName,
              dx: debX?e.scrollWidth-e.clientWidth:0, dy: debY?e.scrollHeight-e.clientHeight:0,
              txt:txt.slice(0,40)});
  });
  return out;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for w,h in ((1440,900),(390,844)):
        ctx=b.new_context(viewport={'width':w,'height':h}, service_workers='block'); pg=ctx.new_page()
        for _motif in INTERDITS:
            pg.route(_motif, lambda r: r.abort())
        tot=0; vus=set()
        for route,vues in PAGES:
            for v in vues:
                url='http://localhost:5002'+route+(('?view='+v) if v else '')
                pg.goto(url, wait_until='domcontentloaded'); pg.wait_for_timeout(3200)
                for r in pg.evaluate(JS):
                    k=(route,v,r['cls'],r['txt'])
                    if k in vus: continue
                    vus.add(k); tot+=1
                    if tot<=14: print('%4dpx %s?%-12s %-8s %-40s dx=%d dy=%d | %s'%(w,route,v,r['tag'],r['cls'],r['dx'],r['dy'],r['txt']))
        print('=== %dpx : %d element(s) rogne(s) en silence\n'%(w,tot))
        ctx.close()
    b.close()
