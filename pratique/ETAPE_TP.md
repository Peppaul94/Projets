# TP : Attaques CSRF (Cross-Site Request Forgery) — étude pratique

Objectifs

- Comprendre le mécanisme d'une attaque CSRF et pourquoi elle profite des cookies de session.
- Reproduire une attaque simple à l'aide des pages fournies (exemple1.html, exemple2.html).
- Mettre en place et vérifier des contre-mesures : jeton CSRF (CSRF token) et réauthentification.
- Rédiger des recommandations et preuves (captures, logs) montrant que la protection fonctionne.

Prérequis

- Python 3 installé (pour les démonstrations Flask décrites ci‑dessous).
- Navigateur web moderne.
- Un terminal (PowerShell / cmd / bash).

Contenu du dossier pratique

- exemple1.html  — page d'attaque qui soumet automatiquement un formulaire.
- exemple2.html  — page d'attaque qui envoie un XHR POST.
- parade.py      — exemple de parade (pseudocode) en Flask/WTF.
- attacker.js    — script d'attaque réutilisable (submitForm / sendXhr).
- exemple1_local.html, exemple2_local.html — versions prêtes à l'emploi qui pointent vers `http://localhost:5000`.

Étapes pas à pas

1) Préparer le répertoire

   Ouvrez un terminal et placez‑vous dans le dossier du TP :

   cd C:\dev_web\Web_Security_formation\OWASP\CSRF\pratique
2) Démarrer l'attaquant (serveur de pages statiques)

   Pour servir les pages d'attaque, lancez un serveur HTTP statique depuis ce dossier :

   python -m http.server 8000

   Accédez ensuite à :

   http://localhost:8000/exemple1.html
   http://localhost:8000/exemple2.html

   (ou utilisez les pages locales préconfigurées)
   http://localhost:8000/exemple1_local.html
   http://localhost:8000/exemple2_local.html
3) Démarrer la cible (application vulnérable)

   Pour simuler la cible (site légitime), créez un petit serveur Flask `victim.py` contenant :

   ```
   from flask import Flask, request, session
   import secretsapp = Flask(name)
   app.secret_key = 'dev-secret-for-lab'@app.route('/login', methods=['GET','POST'])
   def login():
   session['user'] = 'alice'
   session['csrf_token'] = secrets.token_hex(16)
   return f"Logged in. csrf_token={session['csrf_token']}\n"@app.route('/perform-action', methods=['POST'])
   def perform_action():
   data = request.form.to_dict()
   print('Action received:', data)
   return 'Action performed: ' + str(data)@app.route('/perform-action-protected', methods=['POST'])
   def perform_action_protected():
   token = request.form.get('csrf_token')
   if not token or token != session.get('csrf_token'):
   return ('Forbidden', 403)
   data = request.form.to_dict()
   print('Protected action received:', data)
   return 'Protected action performed: ' + str(data)if name == 'main':
   app.run(port=5000)
   ```

   Enregistrez puis lancez :

   python victim.py
4) Authentification simulée (initialiser cookie de session)

   Ouvrez dans le navigateur :

   http://localhost:5000/login

   Cela initialise la session et génère un `csrf_token` stocké côté serveur.
5) Vérifier la vulnérabilité (attaque sans protection)

   - Modifiez `exemple1.html` pour que le formulaire cible pointe sur:

     http://localhost:5000/perform-action
   - Ouvrez `http://localhost:8000/exemple1.html` dans un onglet différent. La page soumettra automatiquement le formulaire.
   - Vérifiez dans la sortie du serveur `victim.py` que la requête a bien été reçue. L'action a été exécutée avec la session "authentifiée".
6) Tester une attaque par XHR (exemple2)

   - Modifiez `exemple2.html` pour que la requête XHR cible `http://localhost:5000/perform-action`.
   - Ouvrez la page attaquante et observez la requête côté serveur.
7) Implémenter la protection par jeton CSRF (CSRF token)

   - Dans vos pages légitimes, incluez le token de session dans les formulaires sensibles :

     <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
   - Dans le serveur, vérifiez que le token transmis correspond au token stocké en session (voir la route `/perform-action-protected` dans l'exemple `victim.py`).
8) Tester la protection

   - Après avoir activé la vérification du token, relancez l'attaque depuis le site d'attaquant (les pages statiques) : la requête sans token doit être rejetée (HTTP 403) par la route protégée.
9) Contre‑mesures complémentaires

- Définir le cookie de session avec l'attribut SameSite (Lax/Strict) pour limiter l'envoi automatique des cookies depuis d'autres origines.
- Exiger une réauthentification (saisie du mot de passe) pour les opérations sensibles.
- Protéger l'application contre XSS (sinon un token CSRF peut être volé).

Points clés à inclure dans le rapport

- Pourquoi la requête malveillante fonctionne (le navigateur envoie les cookies de session automatiquement).
- Pourquoi un token CSRF protège (l'attaquant ne peut pas connaître le token stocké en session).
- Les limites et la nécessité de combiner mesures (SameSite, reauthentification, lutte contre XSS).

Exercices optionnels

- Implémenter SameSite pour le cookie de session et observer le changement de comportement.
- Modifier `parade.py` pour utiliser Flask-WTF et son système CSRF intégré.
- Automatiser les tests avec `curl` ou un script PowerShell afin de documenter les réponses (200 vs 403).

Livrables attendus

- Bref rapport (1 page) décrivant :
  - la procédure suivie,
  - les captures/logs montrant l'attaque et la protection,
  - les changements effectués et recommandations.



### Barème / Critères d'évaluation 

- 40% : Compréhension et démonstration pratique de la vulnérabilité (formulaire auto‑soumis)
- 30% : Mise en place et test du token CSRF (route protégée) — preuves (logs, captures)
- 20% : Explication des mécanismes avancés (SameSite, CORS, limites vis‑à‑vis XSS)
- 10% : Qualité du document rendu (clarté, captures, recommandations)
