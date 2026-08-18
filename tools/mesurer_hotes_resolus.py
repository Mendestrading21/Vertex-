"""tools/mesurer_hotes_resolus.py — QUEL HÔTE RESTE UN SQUELETTE ?

Réserve SIGNAL-OS-52 §6.4, écrite de ma main :

> La sonde ne mesure que trois blocs. Les autres sorties de la fiche
> (`an-rail-decision`, `an-anomaly`, `an-evidence`, `an-tv`) vivent sous la même
> disclosure et n'ont jamais été vérifiées au pixel.

Le lot 52 a montré ce que cela coûte de ne pas regarder : `#an-skyler` portait
2 426 caractères que personne ne voyait, et aucun gardien d'octets ne pouvait
le dire. La fiche Analyse a **quinze** hôtes `%%LOADING%%`. Chacun est un
endroit où le produit peut échouer **en silence**.

## Ce que l'outil mesure, et le vocabulaire qu'il impose

Un hôte finit dans exactement un de ces états, et trois d'entre eux sont sains :

| état | ce que voit l'utilisateur | verdict |
| --- | --- | --- |
| **RÉSOLU** | du contenu | sain |
| **VIDE HONNÊTE** | « rien à montrer », avec la raison | sain — c'est la règle produit |
| **ERREUR DITE** | un bandeau qui nomme la panne | sain — mieux qu'un mensonge |
| **SQUELETTE** | une barre grise, pour toujours | **DÉFAUT** |

Le squelette perpétuel est le seul verdict d'échec, et c'est le pire des quatre :
il promet un contenu qui n'arrivera jamais. Un vide honnête dit la vérité ; un
squelette éternel ment par omission.

## Qu'est-ce qu'un « hôte » ? La première réponse était fausse, et de quatre sur cinq

Premier jet : « tout `[id^="an-"]` ou `[data-body]` sans texte est un hôte qui
n'aboutit pas ». Il a accusé cinq éléments. **Quatre étaient corrects**, et
chacun pour une raison différente :

| élément | pourquoi il est vide | ce que j'avais manqué |
| --- | --- | --- |
| `#an-catalyst-strip` | porte `hidden`, `display:none` | je ne testais que les `<details>` fermés |
| `#an-fav` | `<button>` à icône SVG, `aria-label` posé | un contrôle n'est pas un hôte |
| `#an-order-ticket` | rempli **à la demande**, au clic sur « Calculer le dimensionnement » | vide au repos par construction |
| `#an-name` | le nom de société est inconnu | vrai défaut, mais **pas celui-ci** — voir plus bas |

C'est la faute du lot 51 sous un nouveau visage : **j'ai pris l'absence de
contenu pour un défaut sans demander si le produit l'avait voulue.** Absence de
contenu n'est pas promesse rompue.

La bonne définition est celle que le titre de l'outil énonçait déjà, et que je
n'avais pas suivie : **un hôte est un élément qui a porté un squelette.** Lui
seul a promis du contenu ; lui seul peut manquer à sa promesse. Les quatre
ci-dessus n'en ont jamais porté. L'outil les marque donc **au premier instant**,
puis ne mesure que ceux-là.

## Anti-vacuité : le témoin doit voir un squelette AVANT de dire qu'il n'y en a plus

Une sonde qui compte zéro squelette parce que son sélecteur est faux rend le
même chiffre qu'une page parfaite. Le marquage initial **est** le témoin : s'il
ne marque rien, l'outil rend 2.

## Le chemin du produit

Les deux `<details>` sont ouverts **au clic**, comme au lot 52 : un hôte replié
n'est pas mesurable, et un `open=true` posé à la main ne serait pas le produit.

## Le mode qui vaut le déplacement : `--couper`

Nominal, tous les hôtes aboutissent — c'est la réponse attendue et elle
n'apprend rien. La question qui mord est l'autre : **quand la donnée ne vient
pas, chaque hôte le DIT-il ?** Un `try/catch` oublié laisse un squelette
éternel, et rien dans les octets servis ne le révèle.

`--couper` répond 500 à toutes les routes de données — même périmètre que
`mesurer_degradation.py`, et jamais le HTML/CSS/JS, sinon on mesurerait un
navigateur en panne au lieu d'un produit qui dégrade. Le service worker est
bloqué : sans cela il sert sa copie de cache et la panne n'atteint jamais la
page (leçon du lot 48).

## L'attente est une CONDITION, jamais un chronomètre — et je l'ai réappris ici

Premier verdict de ce mode : « trois hôtes restent squelettes pour toujours ».
**Faux.** J'attendais 9 secondes. En instrumentant le produit, le point d'arrêt
se déplaçait d'une exécution à l'autre — parfois avant le hero, parfois avant la
section 11 : ce n'était pas une panne, c'était **moi qui lisais en cours de
route**. Mesuré en suivant l'état dans le temps :

```text
t= 5s  squelettes=11   t=10s  squelettes=3   t=15s  squelettes=0
```

Sous coupure totale, la fiche dégrade **entièrement**, en une quinzaine de
secondes : chaque `fetch` en échec coûte ~1,8 s et ils s'enchaînent en série.
Lent, mais honnête — et ce n'est pas un défaut.

C'est la leçon du lot 48 (*une attente fixe transforme une course en tirage au
sort*) commise par moi dans le lot même qui la cite. L'outil attend donc que la
condition soit remplie — plus aucun squelette — jusqu'à un plafond franc, et
**rend le temps qu'il a fallu**. Ce n'est qu'au-delà du plafond qu'il accuse.

## Les HUIT espaces, pas un seul (lot 59)

Réserve SIGNAL-OS-53 §5.1, de ma main : *« Une seule page. Les sept autres
espaces ont leurs propres hôtes et ne sont pas balayés. »* L'instrument était
générique dès l'origine ; seule la liste des disclosures à ouvrir était propre à
la fiche Analyse. Elle est désormais **découverte** au lieu d'être écrite :
l'outil ouvre TOUT `<details>` fermé qu'il rencontre, en plusieurs passes —
ouvrir une disclosure en révèle parfois d'autres, imbriquées.

Écrire la liste à la main aurait reproduit la faute du lot 56, où l'ajout d'un
troisième bloc replié avait fait rendre « jamais peint » sur un produit correct.

Usage : python tools/mesurer_hotes_resolus.py [--base http://127.0.0.1:5002]
        [--sym ACN] [--couper] [--espace /markets | --tous]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mesurer_blocs_peints import _INTERDITS, _chromium  # noqa: E402


def espaces():
    """Les huit espaces, LUS DU REGISTRE et non recopiés : une liste écrite à
    la main diverge dès le premier ajout de page."""
    from vertex.ui.shell import PRIMARY_NAV
    return [(it['id'], it['href']) for it in PRIMARY_NAV]

#  MARQUAGE — et il doit être POSÉ AVANT que la page ne vive. Un hôte est le
#  parent d'un squelette : c'est lui qui a promis du contenu. On le marque pour
#  le retrouver après, car son squelette, lui, aura disparu.
#
#  Marquer depuis le test, après `domcontentloaded`, n'allait pas : mesuré, 12
#  hôtes marqués sur les 15 que sert la page. Les trois manquants sont les plus
#  RAPIDES — résolus avant que ma sonde n'ouvre l'œil. Une sonde qui perd les
#  hôtes rapides mesure la lenteur du produit, pas ses promesses. Le marquage
#  est donc injecté comme script d'initialisation et s'exécute à
#  `DOMContentLoaded`, avant toute réponse d'API.
_MARQUER_TOT = """
(() => {
  const poser = () => {
    let n = 0;
    for (const sq of document.querySelectorAll('.vx-skeleton')) {
      const hote = sq.parentElement;
      if (hote && !hote.hasAttribute('data-vx-hote')) {
        hote.setAttribute('data-vx-hote', '1');
        n++;
      }
    }
    window.__vxHotes = (window.__vxHotes || 0) + n;
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', poser);
  } else {
    poser();
  }
})();
"""

#  Chaque hôte est décrit par ce qu'il MONTRE, pas par son identifiant : la
#  moitié d'entre eux sont des `<div data-body>` anonymes.
_RELEVE = """() => {
  const demande = (e) => {
    //  Trois façons, pour le produit, de ne pas encore demander un hôte —
    //  et j'en connaissais UNE au premier jet. Un hôte non demandé n'a rien
    //  promis : ce n'est pas un défaut, c'est un autre état.
    let n = e;
    while (n && n !== document.documentElement) {
      if (n.tagName === 'DETAILS' && !n.open) return false;
      if (n.hasAttribute && n.hasAttribute('hidden')) return false;
      const cs = getComputedStyle(n);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      n = n.parentElement;
    }
    return true;
  };
  const titre = (e) => {
    if (e.id) return '#' + e.id;
    const s = e.closest('section, article, div.vx-card');
    const h = s && s.querySelector('h2, h3');
    return (h && h.textContent.trim().slice(0, 40)) || '(sans titre)';
  };
  return Array.from(document.querySelectorAll('[data-vx-hote]')).map(e => {
    const err = e.querySelector('.vx-error-banner');
    const vide = e.querySelector('.vx-empty');
    return {
      nom: titre(e),
      revele: demande(e),
      squelette: !!e.querySelector('.vx-skeleton'),
      erreur: err ? err.innerText.trim().slice(0, 90) : '',
      vide: vide ? vide.innerText.trim().slice(0, 90) : '',
      caracteres: (e.innerText || '').trim().length,
      ecrits: (e.textContent || '').trim().length,
    };
  });
}"""


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    base = 'http://127.0.0.1:5002'
    sym = 'ACN'
    couper = '--couper' in argv
    if '--base' in argv:
        base = argv[argv.index('--base') + 1]
    if '--sym' in argv:
        sym = argv[argv.index('--sym') + 1]

    #  BALAYAGE DES HUIT ESPACES. Un seul verdict pour tout le produit : le pire
    #  des huit. Rendre 0 parce que sept pages vont bien et taire la huitieme
    #  serait exactement le genre de moyenne qui cache un defaut.
    if '--tous' in argv:
        pire, resume = 0, []
        for ident, href in espaces():
            url = href if href != '/analysis' else '/analysis/%s' % sym
            print('\n' + '=' * 72)
            print('ESPACE %s  (%s)%s' % (ident.upper(), url,
                                         '  [DONNEES COUPEES]' if couper else ''))
            print('=' * 72)
            code = une_page(base, url, couper)
            resume.append((ident, url, code))
            pire = max(pire, code)
        print('\n' + '=' * 72)
        print('RESUME DES HUIT ESPACES%s' % ('  [DONNEES COUPEES]' if couper else ''))
        print('=' * 72)
        for ident, url, code in resume:
            etat = {0: 'OK', 1: 'DEFAUT', 2: 'AVEUGLE'}.get(code, '?')
            print('  %-14s %-24s %s' % (ident, url, etat))
        return pire

    url = '/analysis/%s' % sym
    if '--espace' in argv:
        url = argv[argv.index('--espace') + 1]
    return une_page(base, url, couper)


def une_page(base, url, couper):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('AVEUGLE — Playwright absent. Refus de conclure.')
        return 2

    with sync_playwright() as pw:
        nav = _chromium(pw)
        ctx = nav.new_context(viewport={'width': 1440, 'height': 900},
                              service_workers='block')
        page = ctx.new_page()
        page.add_init_script(_MARQUER_TOT)
        for motif in _INTERDITS:
            page.route(motif, lambda r: r.abort())
        if couper:
            #  Les DONNÉES seulement — jamais le HTML/CSS/JS, sinon on mesure
            #  un navigateur en panne et non un produit qui dégrade.
            page.route('**/{api,scan,cal-feed,news-feed}**', lambda r: r.fulfill(
                status=500, content_type='application/json',
                body='{"error":"panne simulee"}'))
        erreurs = []
        page.on('pageerror', lambda e: erreurs.append(str(e)))
        page.goto(base + url, wait_until='domcontentloaded', timeout=45000)

        #  TÉMOIN ET DÉFINITION EN UN SEUL GESTE : le marquage posé à
        #  `DOMContentLoaded`. S'il n'a rien marqué, c'est la sonde qui est morte.
        marques = page.evaluate('() => window.__vxHotes || 0')
        if not marques:
            nav.close()
            print('AVEUGLE — aucun squelette au premier instant : le selecteur '
                  '`.vx-skeleton` ne trouve rien, donc « zero squelette » a la '
                  'fin ne prouverait rien.')
            return 2
        print('temoin : %d hotes marques au premier instant (parents de '
              'squelette)' % marques)

        #  ON OUVRE TOUT CE QUI EST REPLIÉ, ET EN PLUSIEURS PASSES.
        #  Nommer les disclosures une par une était juste pour la fiche Analyse
        #  et faux partout ailleurs — et le lot 56 a montré le coût : un
        #  troisième bloc replié, non prévu, et la sonde rend « jamais peint »
        #  sur un produit correct. Une passe ne suffit pas : ouvrir une
        #  disclosure en révèle parfois d'autres, imbriquées.
        for _ in range(4):
            fermees = [d for d in page.query_selector_all('details')
                       if not d.get_attribute('open')]
            if not fermees:
                break
            for d in fermees:
                som = d.query_selector('summary')
                if not som:
                    continue
                try:
                    som.click(timeout=2000)
                except Exception:
                    pass
            page.wait_for_timeout(300)
        #  ATTENTE SUR CONDITION — plus aucun squelette parmi les hôtes marqués.
        #  Un délai fixe transformait la mesure en tirage au sort : voir la note
        #  d'en-tête. Le plafond est franc et le temps écoulé est rendu.
        page.wait_for_timeout(500)
        attendu, PLAFOND, PAS = 0.5, 45.0, 0.5
        while attendu < PLAFOND:
            reste = page.evaluate(
                "() => Array.from(document.querySelectorAll('[data-vx-hote]'))"
                ".filter(e => e.querySelector('.vx-skeleton')).length")
            if not reste:
                break
            page.wait_for_timeout(int(PAS * 1000))
            attendu += PAS
        hotes = page.evaluate(_RELEVE)
        nav.close()

    reveles = [h for h in hotes if h['revele']]
    caches = [h for h in hotes if not h['revele']]
    print('mode : %s' % ('DONNEES COUPEES' if couper else 'nominal'))
    print('hotes releves : %d (%d reveles · %d encore replies)'
          % (len(hotes), len(reveles), len(caches)))
    print('resolution complete en %.1f s%s'
          % (attendu, ' — PLAFOND ATTEINT' if attendu >= PLAFOND else ''))
    print()

    bloques = []
    for h in sorted(reveles, key=lambda x: x['nom']):
        if h['squelette']:
            etat, dit = 'SQUELETTE', 'promet un contenu qui n\'arrive pas'
            bloques.append(h['nom'])
        elif h['erreur']:
            etat, dit = 'ERREUR DITE', h['erreur']
        elif h['vide']:
            etat, dit = 'VIDE HONNETE', h['vide']
        elif h['caracteres']:
            etat, dit = 'RESOLU', '%d caracteres montres' % h['caracteres']
        else:
            #  Ni squelette, ni message, ni texte : l'hôte a été vidé sans rien
            #  dire. C'est le défaut le plus discret de tous.
            etat, dit = 'MUET', ('%d caracteres ecrits, 0 montre'
                                 % h['ecrits'] if h['ecrits'] else 'entierement vide')
            bloques.append(h['nom'])
        print('  %-34s %-13s %s' % (h['nom'][:34], etat, dit))

    if caches:
        print('\n  encore replies (non demandes, pas un defaut) : %s'
              % ', '.join(sorted(h['nom'] for h in caches)))
    if erreurs:
        print('\nERREURS JS (%d) :' % len(erreurs))
        for e in erreurs[:5]:
            print('  %s' % e[:160])

    if bloques:
        print('\nHOTES QUI N\'ABOUTISSENT PAS : %s' % ', '.join(bloques))
        return 1
    print('\nTOUS LES HOTES REVELES ABOUTISSENT — contenu, vide honnete ou '
          'erreur nommee. Aucun squelette perpetuel.')
    return 0 if not erreurs else 1


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
