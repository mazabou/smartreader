##Projet
### Télécharger les articles d'actualité à partir de plusieurs flux (Base de données)
1. Les principaux médias proposent des flux RSS:   
   RSS =<titre> + <description> de l'article + un <lien> vers le site concerné
   * Pas besoin de scrapping 
   * On peut se baser sur la <description> pour extrarire "les thèmes" de l'article
   * Dans un premier temps, on renvoie l'utilisateur vers le site  
   ##### Librairie: feedparser
2. Parsing de l'article
   * Plusieurs algos permettent d'extraire text + meta data

### Classification
* Extraction de caractéristique:  
  * Identifier un "pattern" d'utilisation récurrente de mots 
  * Taguer les articles  
* Utilisation du NLP


### Recommendations
* Attribuer des scores à chaque article (thème, style de rédaction, longueur de l'article ... à identifier)
* Déterminer les préférences de l'utilisateur en étudiant son utilisation
* Trouver des méthodes pour évaluer les poids à associer aux scores

### Application
* Programmer une application Android  
  * Interface à étudier plus tard
* Utiliser la Google Cloud Platform / App Engine pour les serveurs


## Plan
1. Algorithme de classification des articles
2. Algorithme de recommendation
3. Création de la base des données d'articles
4. Partie serveur
5. Développement de l'application Android