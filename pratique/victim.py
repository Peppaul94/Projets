from flask import Flask, request, session, redirect, url_for, render_template_string, abort
import secrets

app = Flask(__name__)
# Clé de session pour le labo (NE PAS utiliser en production)
app.secret_key = 'dev-secret-for-lab'
# Optionnel : montrer l'usage de SameSite (commenter/décommenter pour tester)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Page d'accueil informative
@app.route('/')
def index():
    return render_template_string('''
    <h1>Victim (application cible) — TP CSRF</h1>
    <ul>
      <li><a href="/login">/login</a> — simuler l'authentification et créer un token CSRF en session</li>
      <li><a href="/form">/form</a> — formulaire légitime (inclut token CSRF)</li>
      <li><a href="/perform-action-demo">/perform-action (démonstration vulnérable)</a></li>
      <li><a href="/perform-action-protected-demo">/perform-action-protected (démonstration protégée)</a></li>
      <li><a href="/status">/status</a> — afficher le contenu de la session (debug)</li>
      <li><a href="/logout">/logout</a></li>
    </ul>
    ''')

# Simuler un login : crée la session et un token CSRF
@app.route('/login', methods=['GET'])
def login():
    session['user'] = 'alice'
    session['csrf_token'] = secrets.token_hex(16)
    return render_template_string('''
    <p>Logged in as <strong>{{user}}</strong></p>
    <p>csrf_token (session) = <code>{{token}}</code></p>
    <p><a href="/form">Ouvrir le formulaire légitime</a></p>
    <p><a href="/">Retour</a></p>
    ''', user=session['user'], token=session['csrf_token'])

# Formulaire légitime qui inclut le token CSRF
@app.route('/form', methods=['GET'])
def form():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string('''
    <h2>Formulaire légitime</h2>
    <form method="POST" action="/perform-action-protected">
      <label>Action: <input name="action" value="delete"></label><br>
      <input type="hidden" name="target" value="important-data">
      <input type="hidden" name="csrf_token" value="{{csrf}}">
      <button type="submit">Envoyer (protégé)</button>
    </form>
    <p><a href="/">Retour</a></p>
    ''', csrf=session.get('csrf_token',''))

# Route vulnérable (ne vérifie pas le token)
@app.route('/perform-action-protected', methods=['POST'])
def perform_action():
    data = request.form.to_dict()
    app.logger.info('VULN ACTION received: %s', data)
    return f"Action performed (vuln): {data}"

# Route protégée qui vérifie le token CSRF en session
@app.route('/perform-action-protected', methods=['POST'])
def perform_action_protected():
    token = request.form.get('csrf_token')
    if not token or token != session.get('csrf_token'):
        app.logger.warning('CSRF check failed. got=%s expected=%s', token, session.get('csrf_token'))
        return ('Forbidden - CSRF token missing or invalid', 403)
    data = request.form.to_dict()
    app.logger.info('PROTECTED ACTION received: %s', data)
    return f"Protected action performed: {data}"


# Debug endpoints that return JSON to facilitate attacker XHR demonstrations
from flask import jsonify


@app.after_request
def add_cors_headers(response):
    # Allow CORS for localhost origins to demonstrate XHR with credentials in the lab
    origin = request.headers.get('Origin')
    if origin and origin.startswith('http://localhost'):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/perform-action-debug', methods=['POST', 'OPTIONS'])
def perform_action_debug():
    if request.method == 'OPTIONS':
        return ('', 204)
    # accept JSON or form data
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()
    app.logger.info('VULN ACTION (debug) received: %s', data)
    resp = {
        'status': 'vulnerable',
        'data': data,
        'session_user': session.get('user'),
        'session_csrf': session.get('csrf_token')
    }
    return jsonify(resp)


@app.route('/perform-action-protected-debug', methods=['POST', 'OPTIONS'])
def perform_action_protected_debug():
    if request.method == 'OPTIONS':
        return ('', 204)
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()
    token = data.get('csrf_token') or request.form.get('csrf_token')
    csrf_valid = bool(token and token == session.get('csrf_token'))
    if not csrf_valid:
        app.logger.warning('CSRF check failed (debug). got=%s expected=%s', token, session.get('csrf_token'))
    app.logger.info('PROTECTED ACTION (debug) received: %s valid=%s', data, csrf_valid)
    resp = {
        'status': 'protected',
        'csrf_valid': csrf_valid,
        'data': data,
        'session_user': session.get('user')
    }
    return jsonify(resp)

# Démos rapides (GET pour tester comportement sans POST)
@app.route('/perform-action-demo')
def perform_action_demo():
    return render_template_string('''
    <h3>Effectuer une action vulnérable (POST)</h3>
    <form method="POST" action="/perform-action">
      <input type="hidden" name="action" value="delete">
      <input type="hidden" name="target" value="important-data">
      <button type="submit">Submit vuln</button>
    </form>
    <p><a href="/">Retour</a></p>
    ''')

@app.route('/perform-action-protected-demo')
def perform_action_protected_demo():
    return render_template_string('''
    <h3>Effectuer une action protégée (POST)</h3>
    <form method="POST" action="/perform-action-protected">
      <input type="hidden" name="action" value="delete">
      <input type="hidden" name="target" value="important-data">
      <input type="hidden" name="csrf_token" value="{{csrf}}">
      <button type="submit">Submit protected</button>
    </form>
    <p><a href="/">Retour</a></p>
    ''', csrf=session.get('csrf_token',''))

# Afficher le contenu de la session (debug)
@app.route('/status')
def status():
    return {
        'session': {k: session.get(k) for k in session.keys()}
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
