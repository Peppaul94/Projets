### Introduction

Javascript est sensible à toutes sortes de vulnérabilités, permettant à des acteurs malveillants d'insérer du code malveillant dans les applications et packages Node. La programmation défensive combat ces vulnérabilités, garantissant que les logiciels continuent de fonctionner dans des circonstances imprévues. Dans cette leçon, nous aborderons les vulnérabilités courantes du code Node.js, leurs risques et les techniques de codage défensif.

![1716464388052](image/introduction/1716464388052.png)

Nous couvrirons :

* Fonctions et méthodes à risque comme `eval()` et `exec()`
* Les dangers de l'utilisation du module `fs` (file system)
* Vulnérabilités des expressions régulières
* Conseils pour sécuriser votre code
