# ▲ VERTEX — Démarrer ici

Terminal d'**analyse** de marché. **Lecture seule — ne passe jamais d'ordre.**

---

## 🚀 Lancer en 1 clic

### Sur Mac
1. Ouvre le dossier `IBKT-DASHBORD-`.
2. **Double-clic sur `Lancer_VERTEX.command`**.
   - *La 1ʳᵉ fois, macOS peut bloquer :* clic droit → **Ouvrir** → **Ouvrir**.
3. Le navigateur s'ouvre sur **http://localhost:5002**. C'est prêt.

### Sur Windows
1. Ouvre le dossier `IBKT-DASHBORD-`.
2. **Double-clic sur `Lancer_VERTEX.bat`**.
   - *Si SmartScreen s'affiche :* **Informations complémentaires** → **Exécuter quand même**.
3. Le navigateur s'ouvre sur **http://localhost:5002**. C'est prêt.

> **La 1ʳᵉ fois seulement**, l'installation prend 1 à 2 minutes (elle prépare tout automatiquement). Les fois suivantes, le démarrage est immédiat.

---

## 🎭 Juste pour voir tout de suite (mode DÉMO)

Pas envie d'attendre les données ni d'ouvrir TWS ? Lance **`Lancer_VERTEX_DEMO`**
(`.command` sur Mac, `.bat` sur Windows). Chiffres **synthétiques réalistes mais
fictifs**, marqués **🎭 DÉMO** dans l'interface. Idéal pour découvrir l'outil.

---

## 📡 Données LIVE via IBKR (recommandé au bureau)

VERTEX lit tes cours et positions IBKR **en lecture seule**. Pour l'activer :

1. Ouvre **TWS** ou **IB Gateway** et connecte-toi.
2. *Configuration globale → API → Settings* :
   - ☑ **Enable ActiveX and Socket Clients**
   - ☑ **Read-Only API** *(le verrou anti-ordre — indispensable)*
   - **Trusted IP** : `127.0.0.1`
   - Port : `7496` (réel) ou `7497` (paper) — Gateway : `4001` / `4002`
3. Lance `Lancer_VERTEX`. En haut à droite, le badge passe à **🟢 LIVE IBKR**.

> Sans TWS ouvert, VERTEX marche quand même : cours **différés** (~15 min) via
> le filet de secours. Le badge indique alors **🟡 DIFFÉRÉ**.

---

## 🔒 Protéger l'accès (optionnel)

Pour demander un code à l'ouverture (utile si tu ouvres VERTEX depuis ton iPhone
sur le même WiFi) :

1. Copie `.env.example` en **`.env`**.
2. Mets ton code : `VERTEX_CODE=TonCodeSecret`.
3. Relance. VERTEX demandera ce code. *(Le fichier `.env` reste privé, jamais publié.)*

Sur ton iPhone (même WiFi) : `http://<IP-de-ton-ordi>:5002`.

---

## 🧭 Ce que tu trouves dans VERTEX

| Espace | À quoi ça sert |
|--------|----------------|
| 📊 **Overview** | le marché du jour en un coup d'œil |
| 🌅 **Matinal** | le brief du comité : les meilleurs setups du jour |
| 🏛️ **Comité** | tout l'univers passé en revue, filtrable |
| 🔬 **Recherche** | tes hypothèses, questions ouvertes, notes |
| 📝 **Décisions** | fige un verdict, reviens dessus, apprends |
| 🩺 **Santé** | état des moteurs et fraîcheur des données |
| 📈 **Fiche titre** | la **Salle du Comité** : prisme marché → contexte → 9 analystes → avocat du diable → décomposition du score → scénarios ↔ invalidations |

---

## ❓ Si ça ne démarre pas

- **« Python n'est pas installé »** → installe-le : <https://www.python.org/downloads/>
  (sur Windows, coche **Add Python to PATH**). Puis relance.
- **La page ne s'ouvre pas** → attends 10 s puis va sur **http://localhost:5002**.
- **Le port 5002 est pris** → ferme l'autre VERTEX, ou lance avec un autre port :
  `PORT=5050` (Mac : `PORT=5050 ./Lancer_VERTEX.command`).
- **Réinstaller à neuf** → supprime le dossier `.venv` et relance.

---

## ⚖️ Rappel

VERTEX **transforme des données en raisonnement structuré, transparent et
explicable**. Il ne promet pas de battre le marché, ne donne pas de conseil
financier, et **ne passe aucun ordre**. Chaque verdict est **éducatif et
analytique**. Quand une donnée est incertaine ou rassie, l'interface le dit.
