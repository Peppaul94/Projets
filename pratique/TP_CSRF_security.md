# TP CSRF : étapes détaillées et explications

Ce document décrit, pas à pas, toutes les manipulations à effectuer pour réaliser le TP CSRF dans le dossier `OWASP/CSRF/pratique`. Pour chaque étape vous trouverez la commande à taper (ou l'action à réaliser dans le navigateur) et une explication claire de ce que fait l'étape et pourquoi.

## Contexte rapide — quelle est la cible et qui est l'attaquant ?

- Application cible (victim) :

  - Serveur : le serveur Flask fourni dans ce TP, démarré via `python victim.py`.
  - URL / port : http://localhost:5000 (par défaut). C'est l'application « légitime » contenant les routes : `/login`, `/form`, `/perform-action` (vulnérable) et `/perform-action-protected` (avec vérification CSRF).
  - Rôle dans le TP : simule un site web où l'utilisateur est connecté (cookie de session) — c'est la cible des requêtes CSRF.
- Attaquant (origines malveillantes) :

  - Serveur attaquant local : un simple serveur de fichiers statiques démarré avec `python -m http.server 8000` depuis le dossier `pratique`.
  - URL / port : http://localhost:8000. Les pages `exemple1_local.html` et `exemple2_local.html` représentent des pages contrôlées par l'attaquant.
  - Rôle dans le TP : héberger des pages qui déclenchent des requêtes vers la cible (formulaire auto-submit ou XHR) depuis une origine différente.

Remarque : dans un scénario réel l'attaquant n'est pas forcément sur la même machine — l'important est que l'origine (scheme+host+port) de la page attaquante soit différente de celle de la cible.

## Prérequis

Avant de commencer le TP assurez‑vous d'avoir les éléments suivants installés et configurés sur votre poste :

- Python 3.9+ (ou 3.8+) : vérifiez avec `python -V` ou `python3 -V`. Si Python n'est pas installé, téléchargez‑le depuis https://www.python.org/downloads/ ou installez via le gestionnaire de paquets de votre OS.
- pip : fourni avec Python moderne; vérifiez `pip -V`.
- Virtualenv (fortement recommandé) : création d'un environnement isolé pour le TP. Commandes :

  Windows PowerShell :

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

  Windows (cmd) :

  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

  macOS / Linux :

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

- Navigateur moderne (Chrome, Firefox, Edge) avec les outils de développement (onglet Réseau) pour inspecter requêtes/cookies.
- (Optionnel) Pandoc + moteur PDF (MiKTeX / TeX Live) ou `wkhtmltopdf` si vous souhaitez exporter les documents Markdown en PDF. Pandoc n'est pas nécessaire pour exécuter le TP mais peut être utile pour générer des livrables.
- Ports libres : assurez‑vous que les ports `5000` (Flask) et `8000` (serveur statique) sont disponibles et non bloqués par un pare‑feu.

Si vous avez des restrictions d'installation (pas de droits admin), utilisez une distribution portable de Python ou demandez l'aide du responsable système. Une fois le virtualenv activé, toutes les commandes du TP fonctionneront dans cet environnement isolé.

1) Préparer l'environnement

- Objectif : s'assurer que vous travaillez dans le bon dossier et que Python/Flask sont disponibles.
- Commande :

```bash
cd C:\dev_web\Web_Security_formation\OWASP\CSRF\pratique
python -V
```

- Ce que fait la commande :

  - `cd` vous place dans le dossier du TP où se trouvent `exemple1.html`, `exemple2.html`, `victim.py`, etc.
  - `python -V` vérifie que Python est installé et affiche la version.

  Installation de Flask (si nécessaire)

  - Objectif : installer Flask dans l'environnement afin de pouvoir exécuter `victim.py`.
  - Recommandé : utiliser un environnement virtuel pour ne pas polluer l'installation globale.

  Commandes (Windows PowerShell) :

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install flask
  ```

  Commandes (Windows cmd) :

  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install flask
  ```

  Commandes (Linux / macOS) :

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  pip install flask
  ```

  Si vous prévoyez d'utiliser `parade.py` ou Flask-WTF :

  ```bash
  pip install Flask-WTF
  ```

  Vérifier l'installation :

  ```bash
  python -c "import flask; print('Flask', flask.__version__)"
  ```

  Fichier `requirements.txt` (option recommandé)

  Pour faciliter l'installation des dépendances sur une machine ou pour partager l'environnement du TP, créez un fichier `requirements.txt` dans le dossier `pratique` avec le contenu suivant :

  ```
  Flask
  Flask-WTF
  ```

  Puis installez toutes les dépendances d'un coup :

  ```bash
  pip install -r requirements.txt
  ```

  Vérifier Flask-WTF :

  ```bash
  python -c "import flask_wtf; print('Flask-WTF', flask_wtf.__version__)"
  ```

  Remarque : si vous utilisez un virtualenv (`.venv`), activez‑le avant d'installer les dépendances.

2) Préparer les pages d'attaque (optionnel)

- Objectif : avoir des pages d'attaque prêtes à l'emploi.
- Contexte : le dossier contient `exemple1.html` et `exemple2.html` (génériques) et des versions locales `exemple1_local.html`, `exemple2_local.html` qui pointent vers `http://localhost:5000`.
- Action : ouvrez les fichiers si vous souhaitez les adapter, sinon laissez les versions `*_local.html` telles quelles.

3) Démarrer le serveur attaquant (pages statiques)

- Objectif : servir les pages d'attaque depuis une origine différente de la cible.
- Commande :

```bash
# depuis le dossier pratique
python -m http.server 8000
```

- Ce que fait la commande :
  - `python -m http.server 8000` lance un serveur HTTP simple qui sert les fichiers du dossier sur le port 8000.
  - Les pages d'attaque seront accessibles sur `http://localhost:8000/`.

4) Démarrer la cible (serveur vulnérable) — `victim.py`

- Objectif : lancer l'application cible qui simule l'application légitime vulnérable et la version protégée.
- Commande :

```bash
python victim.py
```

- Ce que fait `victim.py` :
  - Démarre un serveur Flask sur `http://localhost:5000`.
  - Route `/login` : simule l'authentification, crée `session['user']` et génère `session['csrf_token']`.
  - Route `/perform-action` : exemple vulnérable — n'effectue aucune vérification CSRF.
  - Route `/perform-action-protected` : exemple protégé — vérifie que le champ `csrf_token` de la requête correspond au token stocké en session.
  - Routes `/form`, `/perform-action-demo`, `/perform-action-protected-demo` : pages pour tester facilement via navigateur.

5) Initialiser la session (login)

- Objectif : créer une session utilisateur côté serveur afin que les requêtes envoyées depuis le navigateur contiennent le cookie de session.
- Action (navigateur) :

Ouvrir `http://localhost:5000/login`

- Ce que cela fait :
  - La réponse du serveur initialise la session (cookie de session envoyé au navigateur) et crée un token CSRF unique stocké dans la session serveur.
  - Vous pouvez vérifier le token affiché sur la page pour référence.

6) Démonstration de la vulnérabilité (form POST)

- Objectif : montrer qu'une page externe peut forcer le navigateur à envoyer une requête authentifiée.
- Préparation : si vous utilisez l'original `exemple1.html`, modifiez son `action` pour pointer vers `http://localhost:5000/perform-action`.
- Ou utilisez `exemple1_local.html` qui fait déjà cela.
- Action (navigateur) :

Ouvrir `http://localhost:8000/exemple1_local.html`

- Ce que cela fait :
  - La page d'attaque crée et soumet automatiquement un formulaire POST vers `http://localhost:5000/perform-action`.
  - Le navigateur inclut automatiquement le cookie de session (si vous êtes connecté), donc la requête arrive comme si l'utilisateur l'avait initiée.
  - Sur le serveur Flask (`victim.py`) vous verrez la requête reçue et le log `VULN ACTION received`.

7) Démonstration de la vulnérabilité (XHR)

- Objectif : montrer qu'une requête JavaScript (XHR / fetch) peut être envoyée depuis une autre origine et inclure le cookie.
- Préparation : utilisez `exemple2_local.html` ou modifiez `exemple2.html` pour pointer vers `http://localhost:5000/perform-action`.
- Action (navigateur) :

Ouvrir `http://localhost:8000/exemple2_local.html`

- Ce que cela fait :
  - Le script appelle `attacker.sendXhr('http://localhost:5000/perform-action')` qui envoie une POST sans token.
  - La requête arrive au serveur cible avec le cookie de session (sauf si SameSite bloque) et l'action est exécutée si la route n'effectue pas de vérification CSRF.

8) Activer la protection par token CSRF et tester

- Objectif : montrer que l'ajout d'un token empêche les attaques classiques.
- Mise en place : dans l'application cible, utilisez la route protégée `/perform-action-protected` ou modifiez vos routes pour effectuer la vérification `if request.form.get('csrf_token') != session['csrf_token'] : 403`.
- Test :

  - Depuis `http://localhost:8000/exemple1_local.html`, soumettez vers `/perform-action-protected` (ou adaptez la page pour cela).
  - La requête sans champ `csrf_token` valide doit recevoir 403 (Forbidden).
- Ce que cela démontre :

  - L'attaquant ne peut pas connaître ou deviner le `csrf_token` stocké en session ; sans le token, la requête est rejetée.

9) Vérifier l'empreinte du cookie `SameSite`

- Objectif : comprendre l'impact de l'attribut `SameSite` sur l'envoi automatique des cookies.
- Test : dans `victim.py`, changez `app.config['SESSION_COOKIE_SAMESITE']` entre `None`, `'Lax'`, `'Strict'` et observez le comportement :

  - `None` : cookie envoyé normalement (vulnérable si pas de token).
  - `Lax` : cookies ne sont pas envoyés pour certaines requêtes cross-site (GET navigations), mais les POST cross-site peuvent toujours être envoyés selon le navigateur.
  - `Strict` : cookie n'est envoyé que pour les requêtes same-site (plus strict), ce qui réduit fortement la surface CSRF.

10) Considérations XSS

- Rappel critique : si l'application est vulnérable à XSS, un attaquant contrôlant la page peut lire le `csrf_token` et l'envoyer lui-même. Le jeton CSRF doit donc être complété par des protections contre le XSS (validation/échappement, CSP, etc.).

11) Journaux et preuve

- Pendant les tests, sauvegardez les logs du serveur Flask (console) et capturez des captures d'écran montrant :
  - la page `/login` affichant le token,
  - la requête malveillante déclenchée depuis le site attaquant,
  - la réponse 403 reçue lorsque la vérification CSRF est active.

12) Livrable attendu

- Un court document (1 page) contenant :
  - description de la configuration et des commandes utilisées,
  - captures d'écran / extraits de logs montrant la requête malveillante et la protection (avant/après),
  - recommandations finales (SameSite, réauthentification pour actions sensibles, lutte contre XSS).

Questions fréquentes et réponses rapides

- Q : Le token CSRF empêche-t-il toutes les attaques ?
- Q : Dois-je toujours utiliser la vérification CSRF si j'ai SameSite=Strict ?
