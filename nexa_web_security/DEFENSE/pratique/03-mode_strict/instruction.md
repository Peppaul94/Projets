### Instructions

1 .

Dans l'espace de travail, nous avons du code dans un fichier nommé **main.js** . Sans mode strict, il ne devrait y avoir aucune erreur.

Exécutez `node main.js` sur le terminal et notez le résultat. 


2 .

Ajoutez le mode strict en haut de ce fichier 

3 .

Utilisez `node main.js` pour essayer d'exécuter le programme avec le mode strict activé ! Notez que le mode strict arrêtera l'exécution à la première erreur, nous verrons donc une erreur à la fois pendant que nous corrigeons.

Le mode strict a attrapé un `SyntaxError`! Il semble que ce soit mécontent que la fonction `printNames()` ait des paramètres en double. Il existe deux paramètres appelés tous deux `names`. Supprimons l'un d'eux dans la définition de la fonction. N'oubliez pas de modifier également les appels à cette fonction.


4 .

Exécutez à nouveau **main.js** avec `node main.js`. Le mode strict en a attrapé un autre `SyntaxError`! Celui-ci doit indiquer que les variables ne peuvent pas être nommées `arguments` ou `eval`. Remplacez le nom de la variable qui viole cette règle par `ourNames`. N'oubliez pas de modifier également toutes les références à cette variable.


5 .

lancez `node main.js` à nouveau.  `SyntaxError `avertit que les variables ou les fonctions ne peuvent pas être supprimées. Supprimons la ligne `delete printNames;` du code.


6 .

Lancer  `node main.js` une dernière fois vous donne un message `ReferenceError`indiquant que `companyName is not defined`. Les variables ne peuvent pas être affectées sans avoir été déclarées au préalable. Assurez-vous que chaque variable est d'abord déclarée avec `let`, `var` ou `const`.

Bon travail! J'espère que vous comprenez comment nous pouvons lire les erreurs pour déterminer ce qui doit être modifié. La sortie lors de l'exécution `node main.js`ne devrait plus générer d'erreurs, ce qui signifie que le code a passé le mode strict de JavaScript !
