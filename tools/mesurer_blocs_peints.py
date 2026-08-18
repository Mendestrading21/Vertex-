"""tools/mesurer_blocs_peints.py — LE PIXEL, PAS L'OCTET.

Le rapport SIGNAL-OS-49 §5.2 porte une réserve que j'ai écrite moi-même :

> **Le rendu n'est pas vérifié au navigateur dans ce lot** : le gardien prouve
> que le câblage existe et que la donnée arrive, pas que le pixel s'affiche.

C'est exact, et ce n'est pas une nuance de langage. Les gardiens des lots 49-51
lisent les **octets servis** : ils voient le site d'appel `+contextes(d)` et ils
voient la clé dans la réponse de l'API. Aucun des deux ne prouve qu'un humain
voit quoi que ce soit. Trois défauts très ordinaires passent sous eux :

- le bloc rend une chaîne vide (toutes ses gardes `if` retombent) ;
- il est rendu dans un conteneur `display:none` ou de hauteur nulle ;
- une exception JS plus haut dans `loadSkyler` interrompt le rendu avant lui.

Cet outil mesure la seule chose qui compte : **le texte que la page affiche**.

## Les trois pièges de montage, et pourquoi ils ne sont pas évitables « au flair »

1. **`<details>` replié — et il y en a DEUX, pas un.** J'avais prévu celui des
   contextes. Le premier jet a donc rendu 2 (aveugle) sur un témoin absent,
   et la mesure a montré pourquoi : `#an-skyler` porte 2 426 caractères de
   `textContent` pour **zéro** de `innerText`, dans une chaîne d'ancêtres tous
   `display:block` et `visibility:visible`. La cause n'est pas un masquage CSS
   mais un `<details id="an-deep-analysis">` **fermé** — 86 px de haut pour un
   contenu de 1 529 px. C'est un choix assumé, écrit dans la source : *«
   Expertise à la demande : les moteurs continuent tous de charger, mais leurs
   sorties secondaires ne concurrencent plus le verdict canonique. »* Les trois
   blocs vivent donc **deux disclosures en profondeur**.

   Deux leçons, et la seconde m'aurait coûté cher : Chromium **exclut de
   `innerText` le contenu d'un `<details>` fermé** — c'est justement ce qui en
   fait le bon instrument ici, `textContent` aurait déclaré « peint » un
   contenu que personne ne voit. Et une sonde qui n'ouvre pas les deux niveaux
   conclurait « jamais peint » sur un produit correct.

2. **Le chemin, pas l'attribut.** Les deux `<details>` sont ouverts par un
   **clic sur leur `<summary>`**, comme un humain, et non par un `open=true`
   posé à la main : c'est la règle du lot 48 — reproduire l'état que le produit
   peut réellement atteindre.

3. **Le service worker.** Bloqué, comme au lot 48 : sinon il sert une copie de
   cache assemblée à une visite antérieure et je mesure le cache, pas la page.

## Anti-vacuité

Un relevé « les trois blocs sont peints » ne vaut rien si la fiche ne s'est pas
chargée. L'outil exige donc un **témoin** : le verdict Skyler lui-même, dont on
sait qu'il est peint depuis longtemps. Sans lui, la sonde est aveugle et rend 2
plutôt qu'un satisfecit.

Et un témoin de plus, côté API : le titre choisi doit réellement porter les six
moteurs. Un titre pauvre ferait retomber les gardes `if` et les blocs rendraient
une chaîne vide — je conclurais « pas peint » en mesurant la pauvreté de mon jeu
d'essai. C'est la faute du lot 38, déjà payée trois fois dans cette série.

Usage : python tools/mesurer_blocs_peints.py [--base http://127.0.0.1:5002]
        [--sym ACN]
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#  Consigne de session : ces routes ne sont JAMAIS appelées, réseau ou pas.
_INTERDITS = ('**/api/ticker/**', '**/api/analyst/**', '**/api/correlations/**',
              '**/api/options-for/**', '**/options/*', '**/desc/**')

#  Ce que chaque bloc doit faire APPARAÎTRE à l'écran. On vise le libellé que
#  le bloc écrit lui-même — pas une phrase reconstruite par moi, qui testerait
#  ma mise en page au lieu du produit (faute mesurée au lot 50).
#
#  CHAQUE LIGNE EST CHERCHÉE DANS LE BLOC, PAS DANS LA PAGE, et la contre-
#  épreuve a montré pourquoi : bloc 51 supprimé, la sonde annonçait quand même
#  « lignes 3/3 ». « Technique », « Catalyseurs » et « Marché » sont des mots
#  courants — ils vivent aussi dans les cartes de dimensions et dans le détail
#  du score. Je mesurais des occurrences voisines, exactement le piège qui
#  m'avait déjà eu deux fois en écrivant le gardien du lot 51.
#
#  D'où l'ancre : un sélecteur qui isole le bloc. `ancre_texte` sert à le
#  reconnaître dans la page, `ancre_dom` à en extraire le sous-arbre.
BLOCS = (
    ('contextes (lot 49)', 'ne modifie ni le score ni le verdict',
     ('Rupture de régime', 'Cohérence sectorielle', 'Profil d’instrument')),
    ('fiabilité (lot 50)', 'explique le verdict, ne le remplace pas',
     ('Fiabilité des preuves', 'Ce qui manque au score', 'Garde-fou multi-actifs')),
    ('contextes du dossier (lot 51)', 'Contextes du dossier',
     ('Technique', 'Catalyseurs', 'Marché')),
)

#  Isole le sous-arbre de chaque bloc à partir de son ancre. On rend son
#  `innerText` — donc, encore une fois, ce qui est MONTRÉ et pas ce qui est écrit.
#
#  UN PAS DE PLUS QU'IL N'Y PARAÎT, et la contre-épreuve l'a montré. Ma première
#  version prenait « le plus petit élément portant l'ancre ». Elle rendait 0/3
#  sur un bloc pourtant intact : l'ancre est un libellé (`<div
#  class="vx-kpi-label">`) qui est le FRÈRE des lignes, pas leur parent. Le
#  conteneur du bloc est donc son parent — un pas, borné, jamais au-dessus de
#  `#an-skyler`. Ce n'est pas « remonter jusqu'à trouver ce que je cherche »,
#  qui finirait toujours par réussir et ne prouverait rien.
_PORTEE = """(ancre) => {
  const racine = document.getElementById('an-skyler');
  if (!racine) return null;
  const tous = Array.from(racine.querySelectorAll('*'))
    .filter(e => (e.innerText || '').includes(ancre));
  if (!tous.length) return null;
  let choix = tous[0], prof = -1;
  for (const e of tous) {
    let p = 0, n = e;
    while (n) { p++; n = n.parentElement; }
    if (p > prof) { prof = p; choix = e; }
  }
  //  Cas `<details>` : l'ancre est dans le `<summary>`. On prend le `<details>`
  //  entier, sinon on ne mesurerait que son titre.
  const det = choix.closest('details');
  if (det && det.querySelector('summary')
      && (det.querySelector('summary').innerText || '').includes(ancre)) {
    return det.innerText || '';
  }
  //  Cas libellé + lignes : le bloc est le parent du libellé.
  const cible = (choix.parentElement && choix.parentElement !== racine
                 && racine.contains(choix.parentElement))
                ? choix.parentElement : choix;
  return cible.innerText || '';
}"""

#  TÉMOIN — et le choisir a demandé une correction. J'avais pris « Score
#  Skyler », un libellé que j'ai supposé au lieu de le lire : il n'existe pas.
#  Un témoin doit être une chaîne que le produit peint VRAIMENT, et il doit
#  prouver la bonne chose. Le titre statique « Diagnostic moteurs » ne
#  conviendrait pas : il est dans le HTML servi et resterait à l'écran même si
#  `loadSkyler` échouait — un témoin qui survit à la panne qu'il doit détecter
#  ne témoigne de rien. « Objection : » est la DERNIÈRE chose que `loadSkyler`
#  écrit avant les trois blocs de cette série : le voir, c'est savoir que la
#  fonction est allée jusqu'au bout, et il est antérieur aux lots 49-51.
TEMOIN = 'Objection'


def _chromium(pw):
    """Chemin explicite : la version épinglée par le paquet n'est pas celle
    installée dans l'image. Mesuré — un `launch()` nu échoue."""
    import glob
    for motif in ('/opt/pw-browsers/chromium-*/chrome-linux/chrome',
                  '/opt/pw-browsers/chromium'):
        trouves = sorted(glob.glob(motif))
        if trouves:
            return pw.chromium.launch(executable_path=trouves[-1],
                                      args=['--no-sandbox'])
    return pw.chromium.launch(args=['--no-sandbox'])


def temoin_api(base, sym):
    """Le titre porte-t-il vraiment les six moteurs ? Sinon les blocs rendent
    une chaîne vide À BON DROIT et « pas peint » serait une accusation fausse."""
    try:
        with urllib.request.urlopen('%s/api/skyler/%s' % (base, sym), timeout=40) as r:
            rep = json.loads(r.read().decode())
    except Exception as exc:                       # pragma: no cover - diagnostic
        return None, 'API injoignable : %s' % exc
    dec = rep.get('decision') or {}
    ctx = ((rep.get('packet') or {}).get('contexts') or {})
    absents = [k for k in ('regime_break', 'sector_coherence', 'instrument_profile',
                           'opportunity_reliability', 'opportunity_attribution',
                           'multi_asset_guard') if k not in dec]
    if absents:
        return None, 'le titre %s ne porte pas %s' % (sym, ', '.join(absents))
    if len(ctx) < 15:
        return None, 'le titre %s ne publie que %d contextes' % (sym, len(ctx))
    return {'moteurs': 6, 'contextes': len(ctx)}, None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    sym = 'ACN'
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    if '--sym' in argv:
        sym = argv[argv.index('--sym') + 1]

    faits, souci = temoin_api(base, sym)
    if souci:
        print('AVEUGLE — %s.\nMesurer « pas peint » sur un dossier pauvre, c\'est '
              'mesurer mon jeu d\'essai.' % souci)
        return 2
    print('temoin API : %d moteurs · %d contextes sur %s'
          % (faits['moteurs'], faits['contextes'], sym))

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('AVEUGLE — Playwright absent. Refus de conclure.')
        return 2

    with sync_playwright() as pw:
        nav = _chromium(pw)
        #  SW bloqué : sinon je mesure une copie de cache (leçon du lot 48).
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        page = ctx.new_page()
        for motif in _INTERDITS:
            page.route(motif, lambda r: r.abort())
        erreurs = []
        page.on('pageerror', lambda e: erreurs.append(str(e)))
        page.goto('%s/analysis/%s' % (base, sym), wait_until='domcontentloaded',
                  timeout=45000)
        #  Attente sur une CONDITION, pas sur une durée : le lot 48 a montré
        #  qu'un délai fixe transforme une course en tirage au sort. On attend
        #  ici le `textContent` — le contenu est écrit AVANT d'être révélé.
        try:
            page.wait_for_function(
                "() => {const h=document.getElementById('an-skyler');"
                "return h && h.textContent.trim().length > 200;}", timeout=30000)
        except Exception:
            pass

        #  LE CHEMIN DU PRODUIT : deux disclosures, ouvertes au clic, dans
        #  l'ordre où un humain les rencontre.
        ouverts = []
        for libelle in ('Analyse approfondie', 'Contextes du dossier'):
            vu = False
            for som in page.query_selector_all('details > summary'):
                if libelle in (som.inner_text() or ''):
                    som.click()
                    page.wait_for_timeout(500)
                    vu = True
                    break
            ouverts.append((libelle, vu))

        texte = page.evaluate('() => document.body.innerText')
        if TEMOIN not in texte:
            nav.close()
            print('AVEUGLE — le temoin « %s » n\'est pas a l\'ecran meme apres '
                  'avoir suivi le chemin du produit : aucun verdict de peinture '
                  'n\'est recevable.' % TEMOIN)
            for libelle, vu in ouverts:
                print('   %-24s %s' % (libelle, 'ouvert' if vu else 'INTROUVABLE'))
            return 2
        print('temoin ecran : « %s » peint' % TEMOIN)
        ouvert = all(vu for _, vu in ouverts)
        for libelle, vu in ouverts:
            print('  disclosure %-24s %s' % (libelle, 'ouverte au clic' if vu
                                             else 'INTROUVABLE'))

        #  Peint = visible. Un texte présent dans un conteneur de hauteur nulle
        #  ne compte pas : on exige aussi une boite non degeneree. C'est ce
        #  controle qui separe « ecrit dans le DOM » de « montre a l'ecran ».
        boites = page.evaluate(
            "() => Array.from(document.querySelectorAll('#an-skyler *'))"
            ".filter(e => e.getBoundingClientRect().height > 0).length")
        ecrit = page.evaluate(
            "() => document.getElementById('an-skyler').textContent.trim().length")
        montre = page.evaluate(
            "() => document.getElementById('an-skyler').innerText.trim().length")
        #  Le texte de CHAQUE bloc, isolé — cf. la note sur BLOCS.
        portees = {nom: page.evaluate(_PORTEE, ancre)
                   for nom, ancre, _ in BLOCS}
        nav.close()

    print('#an-skyler : %d caracteres ecrits · %d montres · %d elements de '
          'hauteur non nulle' % (ecrit, montre, boites))
    print()

    manquants = []
    for nom, ancre, lignes in BLOCS:
        vu_ancre = ancre in texte
        #  Les lignes sont cherchées DANS LE BLOC. Hors du bloc, elles ne
        #  comptent pas : « Catalyseurs » existe ailleurs sur la page.
        portee = portees.get(nom) or ''
        vues = [t for t in lignes if t in portee]
        etat = 'PEINT' if vu_ancre and vues else 'ABSENT'
        print('%-32s %-7s ancre=%s · lignes %d/%d dans le bloc %s'
              % (nom, etat, 'oui' if vu_ancre else 'NON', len(vues), len(lignes),
                 '(' + ', '.join(vues) + ')' if vues else ''))
        if etat == 'ABSENT':
            manquants.append(nom)

    if erreurs:
        print('\nERREURS JS (%d) :' % len(erreurs))
        for e in erreurs[:5]:
            print('  %s' % e[:160])

    if manquants:
        print('\nNON PEINT : %s' % ', '.join(manquants))
        return 1
    if not ouvert:
        print('\nUne disclosure du chemin n\'a pas pu etre ouverte : le contenu '
              'qu\'elle porte n\'est pas mesure.')
        return 1
    print('\nLES TROIS BLOCS SONT PEINTS. La reserve du SIGNAL-OS-49 §5.2 est payee.')
    return 0 if not erreurs else 1


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
