"""
vertex/ui/vault.py — ARCHIVE VAULT (coffre-fort interne).

La bibliothèque de tout ce qui ne doit plus polluer les pages principales
mais mérite d'être gardé : anciens textes, prompts, analyses, versions de
modules, notes de dev, idées futures, décisions produit, historique des
refontes, brouillons.

Architecture (une fonction = un composant) :
  ArchiveVaultPage  → vaultRender()      — assemble la page
  ArchiveSearch     → vaultSearch()      — recherche plein texte en haut
  ArchiveFilters    → vaultFilters()     — chips type/statut/date/important
  ArchiveList       → vaultList()        — liste compacte (gauche)
  ArchiveItemCard   → vaultCard()        — une ligne d'item
  ArchiveDetail     → vaultDetail()      — lecture de l'item (droite)
  ArchiveEditor     → vaultEditor()      — création/édition

Données : localStorage `vxVault` (synchronisé entre appareils via /api/desk,
même contrat que le desk et le journal). Schéma d'un item :
  {id, title, type, content, tags[], createdAt, updatedAt, source,
   status: 'active'|'archived', priority: bool, linkedPage}

Au premier lancement, le coffre est amorcé avec l'historique RÉEL des
refontes et les idées futures notées pendant le développement — rien
d'inventé. Cette page ne touche à rien d'autre : elle ne peut pas casser
le produit. Analyse only, aucun ordre.
"""

CSS = r"""
#av{--acc:#ff7a18;--acc2:#ff9a3d;--good:#22c55e;--bad:#ef4444;--info:#b9683d;--warn:#f5b45b;--vio:#85609f;
 --ink:#eef2f8;--ink2:#aeb8c8;--mut:#8794ab;--faint:#4b5563;--surf:#101218;--bg2:#0b0d12;
 --hair:rgba(255,255,255,.07);--hair2:rgba(255,255,255,.12);
 --mono:ui-monospace,'SF Mono',Menlo,monospace;color:var(--ink);display:block}
#av .num{font-variant-numeric:tabular-nums}
#av .lbl{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
#av .top{display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
#av .search{flex:1;min-width:220px;display:flex;align-items:center;gap:9px;background:var(--bg2);border:1px solid var(--hair2);border-radius:12px;padding:10px 14px}
#av .search input{flex:1;background:none;border:0;outline:none;color:var(--ink);font-size:13.5px;font-family:inherit}
#av .chips{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px}
#av .chip{background:rgba(255,255,255,.035);border:1px solid var(--hair2);color:var(--ink2);border-radius:999px;font-size:11.5px;font-weight:700;padding:6px 13px;cursor:pointer;transition:all .13s}
#av .chip:hover{border-color:rgba(255,255,255,.25)}
#av .chip.on{background:rgba(255,122,24,.14);border-color:rgba(255,122,24,.5);color:var(--acc2)}
#av .layout{display:grid;grid-template-columns:minmax(330px,1fr) 1.5fr;gap:16px;align-items:start}
#av .list{display:flex;flex-direction:column;gap:7px;max-height:76vh;overflow-y:auto;padding-right:4px}
#av .item{background:var(--bg2);border:1px solid var(--hair);border-radius:12px;padding:10px 13px;cursor:pointer;transition:border-color .13s,transform .12s}
#av .item:hover{border-color:rgba(255,122,24,.35);transform:translateX(2px)}
#av .item.sel{border-color:rgba(255,122,24,.55);background:linear-gradient(165deg,#14161d,#0c0e13)}
#av .item.arch{opacity:.55}
#av .item .t{font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px}
#av .item .m{font-size:10.5px;color:var(--faint);margin-top:3px;display:flex;gap:8px;flex-wrap:wrap}
#av .tag{font-size:9.5px;font-weight:700;background:rgba(255,255,255,.05);border:1px solid var(--hair);border-radius:99px;padding:1px 8px;color:var(--mut)}
#av .type{font-size:9px;font-weight:800;padding:2px 8px;border-radius:8px;letter-spacing:.4px;white-space:nowrap}
#av .detail{background:linear-gradient(170deg,var(--surf),var(--bg2));border:1px solid var(--hair);border-radius:16px;padding:20px 22px;min-height:340px;position:sticky;top:12px}
#av .detail h3{font-size:19px;font-weight:800;margin:0}
#av .content{font-size:13.5px;line-height:1.7;color:var(--ink2);margin-top:14px;white-space:pre-wrap;word-break:break-word;
 background:#0a0c10;border:1px solid var(--hair);border-radius:12px;padding:15px 17px;max-height:52vh;overflow-y:auto;font-family:var(--mono);font-size:12.5px}
#av .meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:0;border:1px solid var(--hair);border-radius:12px;overflow:hidden;background:var(--bg2);margin-top:14px}
#av .meta>div{padding:9px 12px;border-right:1px solid var(--hair);font-size:12px}
#av .meta b{display:block;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);font-weight:800;margin-bottom:3px}
#av .acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;padding-top:14px;border-top:1px solid var(--hair)}
#av .ed{background:var(--bg2);border:1px solid var(--hair2);border-radius:14px;padding:16px;margin-bottom:14px;display:none}
#av .ed.on{display:block}
#av .ed .grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px}
#av .jf{width:100%;background:#0a0c10;border:1px solid var(--hair2);border-radius:10px;color:var(--ink);font-size:13px;padding:9px 11px;outline:none;font-family:inherit}
#av .jf:focus{border-color:rgba(255,122,24,.5)}
#av textarea.jf{min-height:110px;resize:vertical;font-family:var(--mono);font-size:12.5px}
#av .empty{padding:44px 20px;text-align:center;color:var(--mut);font-size:13px}
#av .imp{color:var(--warn)}
@media(max-width:960px){#av .layout{grid-template-columns:1fr}#av .detail{position:static}}
"""

BODY = (
  '<div id="av">'
  '<div class="vhead"><div><h1>🗄️ Archive Vault</h1>'
  '<div class="s" id="avHead">le coffre-fort interne — rien ne se perd, rien ne pollue</div></div>'
  '<div style="margin-left:auto;align-self:center;display:flex;gap:8px">'
  '<button class="vbtn pri" onclick="avNew()">➕ Ajouter</button>'
  '<button class="vbtn" onclick="avExport()">⬇ Export</button>'
  '<button class="vbtn" onclick="avImport()">⬆ Import</button></div></div>'
  '<div id="trkHost"></div>'
  '<div id="avRoot"></div>'
  '</div>')

JS = r"""
/* ═══ ArchiveVault — données (localStorage vxVault, sync desk) ═══ */
var AV_TYPES={prompt:['📜','Prompt','#85609f'],analyse:['🔬','Analyse','#b9683d'],idee:['💡','Idée','#f5b45b'],
 version:['🕰️','Ancienne version','#8794ab'],technote:['🔧','Note technique','#22c55e'],design:['🎨','Design','#ec4899'],
 bug:['🐛','Bug','#ef4444'],feature:['🚀','Feature future','#ff7a18'],texte:['📝','Texte libre','#aeb8c8']};
var AV={f:{q:'',type:'',status:'active',imp:false,period:''},sel:null,edit:null};
function avGet(){try{return JSON.parse(localStorage.getItem('vxVault')||'null')||avSeed();}catch(e){return avSeed();}}
function avSet(a){localStorage.setItem('vxVault',JSON.stringify(a));localStorage.setItem('deskTs',String(Date.now()));avPush();}
function avPush(){try{fetch('/api/desk').then(function(r){return r.json()}).then(function(d){var data=(d&&d.data)||{};
 data.vxVault=localStorage.getItem('vxVault');
 fetch('/api/desk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ts:Date.now(),data:data})});}).catch(function(){});}catch(e){}}
function avPull(cb){try{fetch('/api/desk').then(function(r){return r.json()}).then(function(d){
 if(d&&d.data&&d.data.vxVault){var lt=parseFloat(localStorage.getItem('deskTs')||'0');
  if((d.ts||0)>lt||!localStorage.getItem('vxVault'))localStorage.setItem('vxVault',d.data.vxVault);}
 if(cb)cb();}).catch(function(){if(cb)cb();});}catch(e){if(cb)cb();}}
function avSeed(){
 /* amorçage : l'historique RÉEL des refontes + les idées futures notées en cours de route */
 var now=Date.now(),d=function(off){return new Date(now-off*864e5).toISOString();};
 var mk=function(i,title,type,content,tags,src,linked,pri){return {id:now-i,title:title,type:type,content:content,
  tags:tags,createdAt:d(i),updatedAt:d(i),source:src,status:'active',priority:!!pri,linkedPage:linked};};
 var seed=[
  mk(1,'Refonte Options Lab — 12 chapitres','version',
   'La page /options est passée du rapport unique au Research Center en 12 chapitres :\n① cockpit marché ② option du jour + horizons + dauphines ③ analyse 10 dimensions (lue au sens du trade) ④ plan de trading ⑤ visualisations (payoff, cône, distribution, thêta, radar, heatmap) ⑥ 16 stratégies notées en contexte ⑦ 13 listes TOP ⑧ comparateur 8 véhicules ⑨ comité ⑩ matrice de risques ⑪ timeline ⑫ lectures IA.\nMoteur pur : vertex/engines/options_lab.py · API : /api/options-lab.',
   ['options','refonte','2026-07'],'refonte 2026-07-08','/options'),
  mk(2,'Refonte Trade Journal 2.0 — le cerveau','version',
   'Le journal est passé du formulaire au système vivant : 19 stats (Sharpe, Sortino, drawdown, streaks), Coach Vertex (niveau, XP, badges, diagnostic), dashboard (équité, drawdown, win rate glissant), calendrier-heatmap 6 mois, analyses par dimension, base de connaissances des erreurs avec solutions IA, fiche par trade (score /100 expliqué + 5 similaires), saisie minimale (auto-journalisation du Desk conservée).\nModule : vertex/ui/journal.py.',
   ['journal','refonte','2026-07'],'refonte 2026-07-08','/journal'),
  mk(3,'Décision produit — nav épurée à 8 entrées','version',
   'Watchlist (/suivi) et Market Intelligence (/bordel) retirés de la sidebar — routes conservées, accessibles par URL. La watchlist vit dans le Desk (Trading Track). Source unique de la nav : vertex/ui/nav.py.',
   ['nav','décision produit'],'décision 2026-07-08',''),
  mk(4,'Idée — max pain & GEX réels sur Options Lab','feature',
   'Brancher le net GEX / call wall / put wall / gamma flip (options_pack les calcule déjà par titre, réseau) dans le cockpit du Research Center + une jauge de positionnement dealers. Question : coût réseau par titre — à faire à la demande, pas en masse.',
   ['options','gex','à faire'],'idée notée pendant la refonte options','/options',true),
  mk(5,'Idée — sparkline & P&L par position sur le Desk','feature',
   'Chaque carte de position pourrait porter : mini-courbe du sous-jacent (detail.series existe déjà), historique du P&L latent de la position, et un stop suiveur suggéré (ATR).',
   ['desk','positions','à faire'],'idée notée pendant la refonte desk','/strategie',true),
  mk(6,'Idée — comparateur interactif d\'options','feature',
   'Dans le Research Center : choisir 2 véhicules dans le comparateur et les opposer (payoffs superposés, mêmes axes, différence de POP/coût/BE).',
   ['options','comparateur','à faire'],'idée notée','/options'),
  mk(7,'Note technique — apostrophes françaises dans les chaînes JS','technote',
   'Deux SyntaxError silencieuses ont vécu dans PAGE_DAILY parce que « aujourd\'hui » cassait des chaînes JS simples. Règle : dans les chaînes JS simples de terminal.py, TOUJOURS échapper les apostrophes françaises (aujourd\\\'hui) — ou utiliser des template literals. Le crawler d\'audit (scratchpad/audit.py) attrape ce genre de bug.',
   ['js','piège','qualité'],'incident corrigé le 2026-07-08','/'),
  mk(8,'Note technique — repli de cotation hors IBKR','technote',
   'Quand TWS est absent, les positions du Desk estiment le P&L : actions = prix du scan ; options = intrinsèque + valeur temps d\'entrée, étiqueté « ≈ estimé ». Le live remplace l\'estimation dès que la cotation arrive. Implémenté dans le builder de positions (_DESK_COCKPIT_JS).',
   ['desk','ibkr','fallback'],'refonte desk 2026-07-08','/strategie'),
  mk(9,'Historique — Production Baseline (nettoyage)','version',
   '17 fichiers hérités supprimés après preuve de non-référence (ère bot : bot_cockpit, paper_bot, paper_live_bot, dashboard, gex_dashboard, mnq_backtest, stock_backtest, daily_opportunities, _daily_check + launchers + notion + VERTEX_1.0.md). Conservés : ib_reader/test_connection (IBKR live), moteurs quant complets (migrés depuis l'ancien package), chart.umd, company_cache. Tag local : vertex-vnext-baseline.',
   ['baseline','nettoyage','2026-07'],'baseline 2026-07-08',''),
  mk(10,'Idée — appliquer l\'ambiance aux pages hors menu','design',
   'Les pages hors sidebar (suivi, bordel, heatmap, equipe, compare, ma-page) sont encore dans l\'ancien style. À harmoniser avec l\'ambiance salle de marché si elles reviennent dans le produit — sinon candidates à l\'archivage définitif.',
   ['design','harmonisation','à trier'],'audit production 2026-07-08',''),
 ];
 localStorage.setItem('vxVault',JSON.stringify(seed));
 return seed;}

/* ═══ helpers ═══ */
function avEsc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}
function avDate(iso){return (iso||'').slice(0,10);}
function avType(t){return AV_TYPES[t]||['📄',t||'?','#8794ab'];}

/* ═══ ArchiveSearch ═══ */
function vaultSearch(){return '<div class="top"><div class="search">🔎<input id="avQ" placeholder="Rechercher dans le coffre (titre, contenu, tags)…" value="'+avEsc(AV.f.q)+'" oninput="avQ(this.value)"></div></div>';}
window.avQ=function(v){AV.f.q=(v||'').toLowerCase();avRefreshList();};

/* ═══ ArchiveFilters ═══ */
function vaultFilters(counts){var c=function(l,on,fn){return '<span class="chip'+(on?' on':'')+'" onclick="'+fn+'">'+l+'</span>';};
 var h=c('Actifs · '+counts.active,AV.f.status==='active',"avF('status','active')")
  +c('Archivés · '+counts.archived,AV.f.status==='archived',"avF('status','archived')")
  +c('Tous',AV.f.status==='',"avF('status','')")
  +c('⭐ Importants',AV.f.imp,"avF('imp',!AV.f.imp)")
  +'<span style="width:10px"></span>';
 Object.keys(AV_TYPES).forEach(function(t){var n=counts.types[t]||0;if(!n&&AV.f.type!==t)return;
  var T=avType(t);h+=c(T[0]+' '+T[1]+' · '+n,AV.f.type===t,"avF('type','"+t+"')");});
 h+='<span style="width:10px"></span>'
  +c('7 jours',AV.f.period==='7',"avF('period','7')")
  +c('30 jours',AV.f.period==='30',"avF('period','30')");
 return '<div class="chips">'+h+'</div>';}
window.avF=function(k,v){if(k==='type'&&AV.f.type===v)v='';if(k==='period'&&AV.f.period===v)v='';AV.f[k]=v;avRefreshList();};

/* ═══ filtrage ═══ */
function avFiltered(){var a=avGet();
 return a.filter(function(x){
  if(AV.f.status&&x.status!==AV.f.status)return false;
  if(AV.f.type&&x.type!==AV.f.type)return false;
  if(AV.f.imp&&!x.priority)return false;
  if(AV.f.period){var lim=Date.now()-(+AV.f.period)*864e5;if(new Date(x.updatedAt||x.createdAt).getTime()<lim)return false;}
  if(AV.f.q){var hay=(x.title+' '+x.content+' '+(x.tags||[]).join(' ')).toLowerCase();if(hay.indexOf(AV.f.q)<0)return false;}
  return true;}).sort(function(a,b){return (b.priority?1:0)-(a.priority?1:0)||new Date(b.updatedAt)-new Date(a.updatedAt);});}

/* ═══ ArchiveItemCard ═══ */
function vaultCard(x){var T=avType(x.type);
 return '<div class="item'+(AV.sel===x.id?' sel':'')+(x.status==='archived'?' arch':'')+'" onclick="avSel('+x.id+')">'
  +'<div class="t">'+(x.priority?'<span class="imp">⭐</span>':'')+'<span class="type" style="background:'+T[2]+'1a;color:'+T[2]+'">'+T[0]+' '+T[1]+'</span> '+avEsc(x.title)+'</div>'
  +'<div class="m"><span class="num">'+avDate(x.updatedAt||x.createdAt)+'</span>'
  +(x.tags||[]).slice(0,4).map(function(t){return '<span class="tag">'+avEsc(t)+'</span>';}).join('')
  +(x.linkedPage?'<span class="tag" style="color:var(--info)">'+avEsc(x.linkedPage)+'</span>':'')+'</div></div>';}

/* ═══ ArchiveList ═══ */
function vaultList(){var f=avFiltered();
 if(!f.length)return '<div class="empty">Rien dans ce filtre.<br><span style="font-size:11.5px;color:var(--faint)">Élargis la recherche ou ajoute un élément (➕).</span></div>';
 return '<div class="list">'+f.map(vaultCard).join('')+'</div>';}

/* ═══ ArchiveDetail ═══ */
function vaultDetail(){var a=avGet();var x=a.filter(function(i){return i.id===AV.sel;})[0];
 if(!x)return '<div class="detail"><div class="empty">Sélectionne un élément à gauche —<br>ou ➕ ajoute une note, un prompt, une idée.</div></div>';
 var T=avType(x.type);
 return '<div class="detail">'
  +'<div style="display:flex;align-items:flex-start;gap:10px;flex-wrap:wrap">'
  +'<span class="type" style="background:'+T[2]+'1a;color:'+T[2]+';font-size:10px;padding:4px 10px;margin-top:4px">'+T[0]+' '+T[1]+'</span>'
  +'<h3 style="flex:1;min-width:200px">'+(x.priority?'⭐ ':'')+avEsc(x.title)+'</h3></div>'
  +'<div class="content">'+avEsc(x.content)+'</div>'
  +'<div class="meta">'
  +'<div><b>Créé</b><span class="num">'+avDate(x.createdAt)+'</span></div>'
  +'<div><b>Modifié</b><span class="num">'+avDate(x.updatedAt)+'</span></div>'
  +'<div><b>Source</b>'+avEsc(x.source||'—')+'</div>'
  +'<div><b>Statut</b>'+(x.status==='archived'?'🗃️ archivé':'● actif')+'</div>'
  +(x.linkedPage?'<div><b>Page liée</b><a href="'+avEsc(x.linkedPage)+'" style="color:var(--info);text-decoration:none">'+avEsc(x.linkedPage)+' →</a></div>':'')
  +'</div>'
  +((x.tags||[]).length?'<div style="margin-top:12px">'+(x.tags||[]).map(function(t){return '<span class="tag" style="margin-right:6px;font-size:11px;padding:3px 11px">'+avEsc(t)+'</span>';}).join('')+'</div>':'')
  +'<div class="acts">'
  +'<button class="vbtn" onclick="avEdit('+x.id+')">✏️ Modifier</button>'
  +'<button class="vbtn" onclick="avImp('+x.id+')">'+(x.priority?'☆ Retirer l\'étoile':'⭐ Important')+'</button>'
  +(x.status==='archived'
    ?'<button class="vbtn" onclick="avRestore('+x.id+')">↩︎ Restaurer</button>'
    :'<button class="vbtn" onclick="avArchive('+x.id+')">🗃️ Archiver</button>')
  +'<button class="vbtn dng" onclick="avDel('+x.id+')">🗑 Supprimer</button>'
  +'</div></div>';}

/* ═══ ArchiveEditor ═══ */
function vaultEditor(){var x=AV.edit!=null?(avGet().filter(function(i){return i.id===AV.edit;})[0]||{}):{};
 var opts=Object.keys(AV_TYPES).map(function(t){var T=avType(t);
  return '<option value="'+t+'"'+((x.type||'texte')===t?' selected':'')+'>'+T[0]+' '+T[1]+'</option>';}).join('');
 return '<div class="ed'+(AV.editorOpen?' on':'')+'" id="avEd">'
  +'<div class="lbl" style="margin-bottom:10px;color:var(--acc)">'+(AV.edit!=null?'✏️ Modifier':'➕ Nouvel élément')+'</div>'
  +'<div class="grid">'
  +'<div><label class="lbl">Titre</label><input id="aeT" class="jf" value="'+avEsc(x.title||'')+'" placeholder="ex. Prompt de refonte du journal"></div>'
  +'<div><label class="lbl">Type</label><select id="aeK" class="jf">'+opts+'</select></div>'
  +'<div><label class="lbl">Page liée</label><input id="aeL" class="jf" value="'+avEsc(x.linkedPage||'')+'" placeholder="/options"></div></div>'
  +'<div style="margin-top:10px"><label class="lbl">Contenu</label><textarea id="aeC" class="jf" placeholder="Le texte, le prompt, l\'analyse, l\'idée…">'+avEsc(x.content||'')+'</textarea></div>'
  +'<div class="grid" style="margin-top:10px;grid-template-columns:1fr 1fr">'
  +'<div><label class="lbl">Tags (séparés par des virgules)</label><input id="aeG" class="jf" value="'+avEsc((x.tags||[]).join(', '))+'" placeholder="options, refonte, à faire"></div>'
  +'<div><label class="lbl">Source</label><input id="aeS" class="jf" value="'+avEsc(x.source||'')+'" placeholder="ex. refonte 2026-07, brainstorm"></div></div>'
  +'<div style="display:flex;gap:8px;margin-top:12px"><button class="vbtn pri" onclick="avSave()">💾 Enregistrer</button>'
  +'<button class="vbtn" onclick="avCancel()">Annuler</button></div></div>';}
window.avNew=function(){AV.edit=null;AV.editorOpen=true;avRender();var t=document.getElementById('aeT');if(t)t.focus();};
window.avEdit=function(id){AV.edit=id;AV.editorOpen=true;avRender();};
window.avCancel=function(){AV.editorOpen=false;AV.edit=null;avRender();};
window.avSave=function(){var g=function(id){var e=document.getElementById(id);return e?(e.value||'').trim():'';};
 var title=g('aeT');if(!title){alert('Un titre au minimum.');return;}
 var a=avGet(),now=new Date().toISOString();
 var payload={title:title,type:g('aeK')||'texte',content:g('aeC'),linkedPage:g('aeL'),source:g('aeS'),
  tags:g('aeG')?g('aeG').split(',').map(function(t){return t.trim();}).filter(Boolean):[]};
 if(AV.edit!=null){for(var i=0;i<a.length;i++){if(a[i].id===AV.edit){for(var k in payload)a[i][k]=payload[k];a[i].updatedAt=now;AV.sel=a[i].id;}}}
 else{var it={id:Date.now(),createdAt:now,updatedAt:now,status:'active',priority:false};for(var k2 in payload)it[k2]=payload[k2];a.unshift(it);AV.sel=it.id;}
 avSet(a);AV.editorOpen=false;AV.edit=null;avRender();};

/* ═══ actions ═══ */
window.avSel=function(id){AV.sel=(AV.sel===id?null:id);avRender();};
window.avImp=function(id){var a=avGet();a.forEach(function(x){if(x.id===id)x.priority=!x.priority;});avSet(a);avRender();};
window.avArchive=function(id){var a=avGet();a.forEach(function(x){if(x.id===id){x.status='archived';x.updatedAt=new Date().toISOString();}});avSet(a);avRender();};
window.avRestore=function(id){var a=avGet();a.forEach(function(x){if(x.id===id){x.status='active';x.updatedAt=new Date().toISOString();}});avSet(a);avRender();};
window.avDel=function(id){var x=avGet().filter(function(i){return i.id===id;})[0];
 if(!confirm('Supprimer DÉFINITIVEMENT « '+(x?x.title:'')+' » ?\nCette action est irréversible (contrairement à Archiver).'))return;
 avSet(avGet().filter(function(i){return i.id!==id;}));if(AV.sel===id)AV.sel=null;avRender();};
window.avExport=function(){var blob=new Blob([JSON.stringify(avGet(),null,2)],{type:'application/json'});
 var u=URL.createObjectURL(blob);var a=document.createElement('a');a.href=u;a.download='vertex-vault.json';a.click();URL.revokeObjectURL(u);};
window.avImport=function(){var i=document.createElement('input');i.type='file';i.accept='.json';
 i.onchange=function(){var f=i.files[0];if(!f)return;var r=new FileReader();
  r.onload=function(){try{var d=JSON.parse(r.result);if(Array.isArray(d)){avSet(d);avRender();}}catch(e){alert('Fichier invalide.');}};
  r.readAsText(f);};i.click();};

/* ═══ ArchiveVaultPage ═══ */
function avRefreshList(){var el=document.getElementById('avListHost');if(el)el.innerHTML=vaultList();
 var fh=document.getElementById('avFiltHost');if(fh)fh.innerHTML=vaultFilters(avCounts());}
function avCounts(){var a=avGet(),c={active:0,archived:0,types:{}};
 a.forEach(function(x){c[x.status==='archived'?'archived':'active']++;
  if(!AV.f.status||x.status===AV.f.status)c.types[x.type]=(c.types[x.type]||0)+1;});return c;}
function avRender(){var a=avGet(),c=avCounts();
 document.getElementById('avHead').innerHTML='<b style="color:#C9D2E0">'+a.length+'</b> éléments · '
  +c.active+' actifs · '+c.archived+' archivés · ☁️ synchronisé — rien ne se perd, rien ne pollue';
 document.getElementById('avRoot').innerHTML=vaultSearch()+vaultEditor()
  +'<div id="avFiltHost">'+vaultFilters(c)+'</div>'
  +'<div class="layout"><div id="avListHost">'+vaultList()+'</div>'+vaultDetail()+'</div>'
  +'<div style="margin-top:30px;padding-top:12px;border-top:1px solid var(--hair);font-size:11px;color:var(--faint)">🗄️ <b style="color:var(--mut)">Coffre interne</b> — sert à nettoyer les pages principales sans perdre les bonnes idées · Archiver = réversible, Supprimer = définitif (confirmation) · privé, synchronisé via ton desk.</div>';
 var q=document.getElementById('avQ');if(q&&AV.f.q){q.focus();q.setSelectionRange(q.value.length,q.value.length);}}
avPull(function(){avRender();});

/* ═══ 📓 TRACK RECORD — le moteur se note lui-même (/api/track-record) ═══ */
function trkCell(v,unit,good){if(v==null)return '<td style="color:#5c6577">n/d</td>';
 var col=good===undefined?'#eef2f8':(v>=(good||0)?'#22c55e':'#ef4444');
 return '<td class="num" style="color:'+col+';font-weight:700">'+v+(unit||'')+'</td>';}
function trkTable(title,obj){var keys=Object.keys(obj||{});if(!keys.length)return '';
 keys.sort(function(a,b){return (obj[b].n||0)-(obj[a].n||0);});
 return '<div style="margin-top:14px"><div style="font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8794ab;margin-bottom:6px">'+title+'</div>'
  +'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:12.5px">'
  +'<thead><tr>'+['','N','Réussite 1j','Réussite 5j','Réussite 20j','Moy. 1j','Moy. 5j','Moy. 20j','TP1 avant stop'].map(function(h){return '<th style="text-align:left;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:#8794ab;padding:7px 10px;border-bottom:1px solid rgba(255,255,255,.12)">'+h+'</th>';}).join('')+'</tr></thead><tbody>'
  +keys.map(function(k){var b=obj[k];return '<tr style="border-bottom:1px solid rgba(255,255,255,.05)"><td style="padding:8px 10px;font-weight:700">'+(window.VX?VX.verdictBadge(k):k)+'</td>'
   +'<td class="num" style="color:#aeb8c8">'+b.n+'</td>'
   +trkCell(b.win_1j,'%',50)+trkCell(b.win_5j,'%',50)+trkCell(b.win_20j,'%',50)
   +trkCell(b.avg_1j,'%',0)+trkCell(b.avg_5j,'%',0)+trkCell(b.avg_20j,'%',0)
   +trkCell(b.tp1_rate,b.tp1_rate!=null?('% ('+b.tp1_resolved+')'):'',50)+'</tr>';}).join('')
  +'</tbody></table></div></div>';}
function trkLoad(){var host=document.getElementById('trkHost');if(!host)return;
 fetch('/api/track-record').then(function(r){return r.json();}).then(function(d){
  if(!d||!d.entries){host.innerHTML='';return;}
  var thin=d.resolved<30;
  host.innerHTML='<div style="background:linear-gradient(170deg,#101218,#0b0d12);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:20px 22px;margin-bottom:22px">'
   +'<div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap"><h2 style="font-size:19px;font-weight:800;margin:0">📓 Track record du moteur</h2>'
   +'<span style="font-size:11.5px;color:#8794ab">'+d.entries+' verdicts journalisés · '+d.resolved+' résolus · '+d.days+' jours de collecte · MAJ '+(d.as_of||'—')+'</span></div>'
   +'<div style="font-size:12px;color:#aeb8c8;margin-top:6px">Vertex mesure ses PROPRES verdicts contre les prix réels — aucune promesse, que du constaté.'
   +(thin?' <b style="color:#f5b45b">Échantillon encore mince — les stats se densifient chaque jour de collecte.</b>':'')+'</div>'
   +trkTable('Par verdict',d.by_verdict)+trkTable('Par grade',d.by_grade)+trkTable('Par régime de marché',d.by_regime)
   +'<div style="font-size:10px;color:#5c6577;margin-top:12px">⚠️ '+(d.note||'')+'</div></div>';
 }).catch(function(){});}
trkLoad();
"""

__all__ = ['CSS', 'BODY', 'JS']
