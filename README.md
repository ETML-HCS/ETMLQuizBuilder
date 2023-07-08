# ETMLQuizBuilder

Auteur: Helder Costa Lopes
Date: juillet 2023

## Description

Ce code Python utilise Flask pour créer un module de quiz interactif. Il permet de charger un quiz depuis un fichier CSV, de générer le formulaire HTML, de gérer les réponses en temps réel et d'afficher les résultats. Le module simplifie également l'ajout des fichiers CSS et JavaScript nécessaires au fonctionnement.

## Utilisation

1. Assurez-vous d'avoir installé Python et Flask sur votre système.
   
3. Placez votre fichier de quiz au format CSV dans le même répertoire que ce script.
   
4. Suivez les instructions à l'écran pour créer le module de quiz.

5. Une fois le module créé, vous pouvez l'utiliser en exécutant le fichier `serverQuiz.py` généré. Assurez-vous d'exécuter le fichier dans le même répertoire que le module de quiz.

6. Accédez à l'URL `http://localhost:8000/` dans votre navigateur pour accéder au quiz.

7. Les étudiants peuvent soumettre leurs réponses au quiz. Les réponses seront enregistrées dans un fichier CSV et les résultats seront affichés en temps réel.

8. Pour afficher les résultats du quiz, accédez à l'URL `http://localhost:8000/results`.

9. Vous pouvez personnaliser le style du quiz en modifiant le fichier `styles.css` dans le répertoire `static/css`.

10. Pour modifier les questions du quiz, modifiez le fichier CSV correspondant et recréez le module de quiz en exécutant à nouveau le script.

11. Pour permettre l'accès au quiz à partir d'autres appareils sur le même réseau local, utilisez l'option `--host="0.0.0.0"` lors de l'exécution du fichier `serverQuiz.py`. Par exemple :
 ```
 python serverQuiz.py --host="0.0.0.0"
 ```

12. Assurez-vous d'arrêter le serveur en appuyant sur `Ctrl+C` dans la fenêtre du terminal lorsque vous avez terminé d'utiliser le module de quiz.

Pour plus d'informations et de détails sur l'utilisation du module de quiz, consultez la documentation du code.

