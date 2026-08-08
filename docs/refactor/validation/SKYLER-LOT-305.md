# SKYLER LOT 305 — Round-trip desk prouvé de bout en bout ; campagne d'audits close

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-305` (base : lot 304 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — parcours transverse à ÉCRITURE LOCALE (dernier angle)

En navigateur réel, par le chemin RÉEL du store (`VXEntities`, jamais
desk_data.json à la main) :

1. `VXEntities.toggleFavorite('AAPL')` → `favorites()=["AAPL"]`,
   `myFavs` en localStorage ✓
2. Push débouncé automatique → **le serveur `/api/desk` porte
   `data.myFavs=["AAPL"]`**, les autres clés desk intactes (6) ✓
3. `localStorage.clear()` + rechargement → **le pull au démarrage
   RESTAURE le favori** (`favorites()=["AAPL"]`) ✓
4. Nettoyage par le même chemin → serveur revenu à `[]` ✓

0 erreur console sur tout le parcours. (2 imprécisions de MA sonde
corrigées en route : l'API est `toggleFavorite` — pas `toggleFav` — et
`/api/desk` enveloppe dans `{ts, data}`.)

**Verdict : SAIN de bout en bout** — écriture locale, push
last-writer-wins, pull de restauration : le contrat desk tient.

## Campagne d'audits close (lots 292-305)

Tous les angles balayés, tous SAINS après correctifs : tactile (3
défauts corrigés), honnêteté (2 mensonges corrigés + gardien), a11y
(2 champs), clavier (1 défaut corrigé), robustesse API, textes FR,
performance, écriture locale. 3 sondeurs outillés dans tools/.
→ Les prochains lots de développement reviennent aux améliorations
produit calibrées.

## Preuves

Suite complète : **2516 passed / 2 skipped** (référence maintenue).

## Décision SW

**Pas de bump** (`td-shell-v186`) : docs seulement.

## Suite

LOT 306 : purge É1 en PRIORITÉ dès déblocage ; sinon amélioration
produit calibrée (donnée moteur servie non affichée, domicile unique).
