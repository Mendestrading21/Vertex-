/* Vertex Signal OS — sémantique visuelle.
   Aucun calcul, aucune donnée financière, aucun appel réseau.
   La couche LIT le DOM et y pose des attributs sémantiques ; elle n'invente
   aucun texte et n'en remplace aucun.

   LA TABLE DE MICRO-COPY EST FERMÉE.

   Cette couche portait une `Map` de 45 libellés qu'elle réécrivait dans le DOM
   après le rendu : le serveur envoyait « VIX — volatilité implicite du marché »,
   l'écran affichait « VIX ». Deux vérités pour un même libellé — et tout gardien
   qui lit les octets servis gardait l'ancienne, pendant que la nouvelle n'était
   gardée par rien.

   Vidée page par page, chaque libellé écrit à sa source :
     shell + Aujourd'hui (7) · Marchés (15) · Opportunités (5) · le reste (7).

   HUIT ENTRÉES NE POUVAIENT DÉJÀ PLUS RIEN RÉÉCRIRE. « Rechercher un titre pour
   ouvrir sa fiche canonique. », « Ce que révèle une fiche », « Que s'est-il
   passé après ? — évidence historique » et « Cette structure offre-t-elle une
   asymétrie suffisante ? » (présente DEUX fois) ne sont produites par aucune
   page ; « Skyler — décision canonique » n'existe que dans un commentaire ;
   « Où est la meilleure convexité… » que dans une docstring ; « Ajouter » avait
   été écrit à la source au lot Shell.
   **Une table de réécriture ne peut pas savoir qu'elle est périmée** : elle
   échoue en silence, ce qui est exactement sa nature.

   Ce qui reste ici est d'une autre espèce. `normalizeGrades` et
   `normalizeDecisionCards` ne changent aucun texte : elles LISENT une valeur
   déjà présente (« S+ », « pessimiste ») et posent l'attribut qui permet au CSS
   de la colorer. Le serveur reste la seule source du contenu. */
(function(){
'use strict';

let scheduled = false;

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
  /* L'observateur reste NÉCESSAIRE : les grades arrivent avec les données, donc
     après le premier rendu, et la navigation persistante remplace le contenu
     sans recharger la page. Il ne relance plus que deux passes qui lisent des
     attributs — la passe de réécriture, qui balayait sept sélecteurs sur tout
     le sous-arbre à chaque mutation, a disparu avec la table. */
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
