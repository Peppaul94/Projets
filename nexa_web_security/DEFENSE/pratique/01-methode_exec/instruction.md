### Instructions

1 .

Exécutez la commande terminal `node index.js` pour lancer une application Web qui utilise `exec` pour exécuter la commande bash `echo `pour imprimer le message dans la zone de texte. Vous devrez peut-être actualiser la fenêtre du navigateur intégré pour voir la page Web.

Essayez d'ajouter les chaînes suivantes correspondant à deux commandes bash en utilisant le caractère `;` :

* `"Hello\nWorld!"; ls`
* `"Hello\nWorld!"; cat example.txt`
* `"Hello\nWorld!"; rm example.txt`.

2 .

Sécurisez notre application en utilisant `execFile()`. En haut de **app.js** , importez la méthode `execFile` from `child_process` au lieu de `exec`.

3 .

Implémentons la méthode `execFile()`!

À la ligne 17, remplacez la méthode `exec` par `execFile` et supprimez son premier argument ``echo -e ${msg}``. Le premier argument de `execFile()`sera la commande `"echo"`. Le deuxième argument sera les drapeaux de commande sous forme de tableau de chaînes : `["-e", msg]`. Le troisième et dernier argument est la fonction de rappel qui peut être la même que la méthode `exec`.
