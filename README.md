# Azure_storage

https://damienplantin.github.io/Azure_storage/

- Créer un compte de StorageV2 (v2 à usage général) dans le groupe de ressources brief blob 1 
   options de sécurité appropriées : privé
   
- pip install azure-storage-blob

1) Configuration du fichier config.ini

- ouvrir le fichier config.ini 
- restoredir= Mettre le chemin du document "download" exemple : C:\Users\utilisateur\Desktop\download
account= Mettre le compte de stockage  
container= Mettre le nom de votre container
key= rentrer la clef qui se trouve acceuil> compte> clef d'accès> Afficher les clefs



Pour envoyer un blob dans le container : 

Ouvrir le terminal : 

python main.py upload "chemin + nom du fichier à upload" 
exemple : python main.py upload "C:\Users\utilisateur\Desktop\hello.txt"

Pour récupérer un blob du container : python .\main.py download "nom du fichier à downolad"  
exemple : python main.py download hello.txt  


Création du requiremets.txt :
pip install virtualenv
python -m virtualenv venv dans le dossier du script (venv nom donné par convention)
.\venv\Scripts\activate
python main.py pour voir quelles librairie il manque pour exécuter le script.
pip freeze > requirements.txt pour mettre directement les librairie dans le fichier requirements.txt
"deactivate" pour désactiver l'env
