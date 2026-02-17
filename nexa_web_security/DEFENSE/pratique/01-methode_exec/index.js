// Importation des modules nécessaires
import { exec } from "child_process"; // Méthode potentiellement dangereuse
import fs from "fs"; // Module pour la manipulation de fichiers
import http from "http"; // Module pour créer un serveur HTTP
import path, { dirname } from "path"; // Module pour la manipulation de chemins de fichiers
import { fileURLToPath } from 'url'; // Méthode pour convertir une URL de fichier en chemin de fichier

// Récupération du chemin du répertoire actuel dans un module ES6
const __filename = fileURLToPath(import.meta.url); // Récupération du nom du fichier à partir de l'URL du module
//Pourquoi on utilise fileURLToPath et dirname ? Car dans les modules ES6, __dirname et __filename ne sont pas définis par défaut comme dans les modules CommonJS. 
// fileURLToPath est utilisé pour convertir l'URL du module en un chemin de fichier, et dirname est utilisé pour obtenir le nom du répertoire à partir de ce chemin de fichier.
const __dirname = dirname(__filename); // Récupération du nom du répertoire à partir du chemin du fichier

// Configuration du serveur
const hostname = "localhost";
const port = process.env.PORT || 4001; // Utilisation du port défini dans les variables d'environnement ou du port 4001 par défaut 

// Création du serveur
const server = http.createServer((req, res) => {
  // Construction de l'URL de base à partir de l'hôte de la requête
  const baseURL = "http://" + req.headers.host + "/"; // Construction de l'URL complète de la requête en utilisant l'URL de base et le chemin de la requête
  const reqUrl = new URL(req.url, baseURL); // Création d'un objet URL à partir de l'URL de la requête

  // Récupération du paramètre "message" de l'URL
  const msg = reqUrl.searchParams.get("message"); // Récupération de la valeur du paramètre "message" à partir de l'URL
  let content = "";

  // Si l'URL de la requête se termine par ".css"
  if (req.url.endsWith(".css")) {
    // Définition de l'en-tête "Content-Type" pour indiquer que la réponse est un fichier CSS
    res.setHeader("Content-Type", "text/css"); // Définition de l'en-tête "Content-Type" pour indiquer que la réponse est un fichier CSS
    try {
      // Lecture du fichier CSS correspondant et envoi de son contenu
      // Lire le fichier en tant que Buffer pour préserver l'encodage original
      content = fs.readFileSync(path.join(__dirname, req.url));
      res.statusCode = 200;
      res.end(content);
    } catch (e) {
      // Si une erreur se produit lors de la lecture du fichier, envoi d'une réponse "Not Found"
      res.statusCode = 404; // Envoi d'une réponse "Not Found" si le fichier CSS n'est pas trouvé
      res.end("Not Found");
      console.log("Error:", e.stack);
    }
  } else if (msg) {
    // Si un message est présent dans l'URL, exécution de la commande "echo" avec ce message
    res.setHeader("Content-Type", "text/html");
    exec(`echo ${msg}`, { shell: 'cmd.exe' },(error, stdout, stderr) => { // Exécution de la commande "echo" avec le message fourni dans l'URL. Voici un exemple d'injection du code: Test& whoami (note: on est dans un cmd windows)
      if (error) {
        // Si une erreur se produit lors de l'exécution de la commande, envoi d'une réponse "ERROR"
        res.statusCode = 500; // Envoi d'une réponse d'erreur si la commande génère une erreur
        res.end("ERROR");
        console.log(`error: ${error.message}`);
        return;
      }
      if (stderr) { 
        // Si la commande produit une sortie d'erreur, envoi d'une réponse "ERROR"
        res.statusCode = 500; // Envoi d'une réponse d'erreur si la commande génère une sortie d'erreur
        res.end("ERROR");
        console.log(`stderr: ${stderr}`);
        return;
      }
      // Envoi de la sortie de la commande comme réponse
      res.statusCode = 200;
      res.end(stdout);
      console.log(`stdout: ${stdout}`);
    });
  } else {
    // Si aucune des conditions précédentes n'est pas remplie, envoi du contenu du fichier "web_page.html"
    res.statusCode = 200;
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    try {
      // Lire le fichier HTML en tant que Buffer pour éviter les problèmes d'encodage
      content = fs.readFileSync(path.join(__dirname, "web_page2.html"));
    } catch (e) {
      console.log("Error:", e.stack);
    }
    res.end(content);
  }
});

// Démarrage du serveur
server.listen(port, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
