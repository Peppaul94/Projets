
from flask import Flask, session, render_template, request, abort
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
@app.route('/login', methods=['POST'])
def login():
  # Générer un jeton CSRF et l'associer à la session de l'utilisateur
  session['csrf_token'] = generate_csrf_token()

@app.route('/perform-action', methods=['POST'])
def perform_action():
  # Vérifier que le jeton CSRF inclus dans la requête correspond au jeton CSRF de la session
  if request.form['action'] != session['csrf_token']:
    abort(403)

  # Effectuer l'action
  # ...

@app.route('/form')
def form():
  # Inclure le jeton CSRF comme un champ de formulaire caché
  return render_template('form.html', csrf_token=session['csrf_token'])