/* Vertex Signal OS — micro-copy et sémantique visuelle globales.
   Aucun calcul, aucune donnée financière, aucun appel réseau.
   La couche ne modifie que des libellés statiques connus et ajoute des attributs
   visuels aux grades déjà présents dans le DOM. */
(function(){
'use strict';

const COPY = new Map([
  ["Dois-je agir aujourd’hui, et sur quoi ?","Les signaux qui méritent une action."],
  ["Dois-je agir aujourd'hui, et sur quoi ?","Les signaux qui méritent une action."],
  ["Brief Vertex","Signal du jour"],
  ["Depuis ta dernière visite","Ce qui a changé"],
  ["Meilleures opportunités","Top opportunités"],
  ["Alertes prioritaires","Alertes"],
  ["Portefeuille — ce qui a changé","Portefeuille"],
  ["Dans quel environnement la stratégie opère-t-elle ?","Régime, risque et leadership."],
  ["Vue d’ensemble","Vue globale"],
  ["Vue d'ensemble","Vue globale"],
  ["Régime de marché","Régime"],
  ["Leadership sectoriel","Leadership"],
  ["Top 10 — plus fortes hausses","Top hausses"],
  ["Flop 10 — plus fortes baisses","Top baisses"],
  ["Détail — au-dessus des moyennes","Au-dessus des moyennes"],
  ["VIX — volatilité implicite du marché","VIX"],
  ["Quelles opportunités méritent réellement une analyse ?","Les dossiers qui méritent ton attention."],
  ["Shortlist — méritent une analyse","Shortlist"],
  ["Rechercher un titre pour ouvrir sa fiche canonique.","Ouvre un dossier complet en quelques secondes."],
  ["Ce que révèle une fiche","Contenu du dossier"],
  ["Titres récents","Récents"],
  ["Scanner d’opportunités","Opportunités"],
  ["Scanner d'opportunités","Opportunités"],
  ["Portefeuille & positions","Portefeuille"],
  ["Où mon capital est-il exposé, et quelle position exige une décision ?","Exposition, risque et prochaine décision."],
  ["Watchlist","Surveillance"],
  ["Où est la meilleure convexité, à quel prix de volatilité, et quel événement la menace ?","Convexité, volatilité et risque événementiel."],
  ["Cette structure offre-t-elle une asymétrie suffisante ?","L’asymétrie est-elle suffisante ?"],
  ["Cette structure offre-t-elle une asymétrie suffisante ?","L’asymétrie est-elle suffisante ?"],
  ["Mes positions","Positions"],
  ["Événements","Catalyseurs"],
  ["Scanner d'anomalies — qu'est-ce qui sort de l'ordinaire ?","Anomalies"],
  ["Que s'est-il passé après ? — évidence historique","Évidence historique"],
  ["Skyler — décision canonique","Décision Skyler"],
  ["Risque du jour","Risque principal"],
  ["Participation du marché","Participation"],
  ["Limites des données","Qualité des données"],
  ["Leaders par secteur","Leaders"],
  ["Entonnoir de sélection","Sélection"],
  ["Composition de la santé du marché","Santé du marché"],
  ["Recherche globale","Recherche"],
  ["Ajouter","Analyser"]
]);

const COPY_SELECTOR = [
  '.vx-page-header .vx-sub',
  '.vx-card-title',
  '.vx-chart-title',
  '.vx-section-header h2',
  '.vx-tab',
  '.an-shortcut > span:first-child',
  '.vx-op-sectitle'
].join(',');

let scheduled = false;

function replaceStaticCopy(root){
  const scope = root && root.querySelectorAll ? root : document;
  scope.querySelectorAll(COPY_SELECTOR).forEach(function(el){
    if(el.childElementCount) return;
    const before = (el.textContent || '').trim();
    const after = COPY.get(before);
    if(after && after !== before){
      el.textContent = after;
      el.dataset.signalCopy = '1';
    }
  });

  const search = document.getElementById('vx-global-search');
  if(search){
    search.placeholder = 'Ticker, option ou page';
    search.setAttribute('aria-label','Rechercher un ticker, une option ou une page');
  }

  const add = document.getElementById('vx-add-btn');
  if(add){
    const label = add.querySelector('.vx-hide-mobile');
    if(label) label.textContent = 'Analyser';
    add.setAttribute('aria-label','Lancer une analyse');
    add.title = 'Lancer une analyse';
  }
}

function normalizeGrades(root){
  const scope = root && root.querySelectorAll ? root : document;
  scope.querySelectorAll('[data-g],.vx-op-grade,.vx-op-tk-grade,.vx-badge,.vx-chip').forEach(function(el){
    const raw = String(el.dataset.g || el.textContent || '').trim().toUpperCase();
    if(raw === 'S+' || raw === 'S' || raw === 'A' || raw === 'B'){
      el.dataset.grade = raw;
      if(!el.getAttribute('aria-label')) el.setAttribute('aria-label','Niveau '+raw);
    }
  });
}

function normalizeDecisionCards(root){
  const scope = root && root.querySelectorAll ? root : document;
  scope.querySelectorAll('.vx-scenario').forEach(function(card){
    const label = card.querySelector('.vx-scenario-k');
    const text = String(label && label.textContent || '').toLowerCase();
    if(!card.dataset.kind){
      if(/pessim|risque|perte|baisse/.test(text)) card.dataset.kind = 'down';
      else if(/exception|hausse|gain/.test(text)) card.dataset.kind = 'up';
      else card.dataset.kind = 'base';
    }
  });

  scope.querySelectorAll('.vx-verdict-card').forEach(function(card){
    card.dataset.signalCard = 'decision';
  });
}

function apply(root){
  document.documentElement.dataset.visual = 'signal-os';
  if(document.body){
    document.body.dataset.visual = 'signal-os';
    document.body.classList.add('vx-signal-os');
  }
  replaceStaticCopy(root);
  normalizeGrades(root);
  normalizeDecisionCards(root);
}

function schedule(root){
  if(scheduled) return;
  scheduled = true;
  requestAnimationFrame(function(){
    scheduled = false;
    apply(root || document);
  });
}

function boot(){
  apply(document);
  const target = document.getElementById('vx-content') || document.body;
  if(target && window.MutationObserver){
    new MutationObserver(function(mutations){
      let root = target;
      for(const mutation of mutations){
        const node = mutation.addedNodes && mutation.addedNodes[0];
        if(node && node.nodeType === 1){ root = node; break; }
      }
      schedule(root);
    }).observe(target,{childList:true,subtree:true});
  }
  window.addEventListener('popstate',function(){schedule(document)});
  document.addEventListener('vx:navigation-complete',function(){schedule(document)});
}

if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded',boot,{once:true});
else boot();
})();
