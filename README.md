# Développez un programme logiciel en Python

Quatrième projet de la formation diplômante
Développeur Python sur Openclassrooms

## FAQ

#### Comment exécuter le programme ?

Après s'être placé dans le répertoire du projet depuis le terminal,
procéder aux étapes suivates :
- Exécuter la commande suivante pour créer votre environnement virtuel :
  - python -m venv env
- Exécuter la commande suivante pour activer votre environnement virtuel :
  - call env/Scripts/activate.bat (depuis Windows)
  - en cas de non-fonctionnent, exécuter Powershell en tant qu'administrateur
    - rentrer la commande _Set-ExecutionPolicy RemoteSigned_
    - revenir au terminal, et rentrer la commande _env/Scripts/activate_
  - source env/bin/activate (depuis autre OS)
- Exécuter la commande suivante pour installer les paquets requis
  - pip install -r requirements.txt
- Exécuter la commande suivante pour lancer le programme
  - python main.py

#### Comment utiliser le programme ?

Le programme est conçu sous l'architecture modèle-vue-contrôleur.
Après le lancement du programme, 
l'accès aux différentes fonctions du programme est explicitement indiqué, notamment pour :
- Créer un tournoi
- Créer des joueurs dans le tournoi (nombre de 8 requis)
- Créer des rounds dans le tournoi (7 rounds pour faire tous les affrontements)
- Modifier un tournoi

#### Comment générer un rapport flake8-html ?

- Depuis le terminal, entrer la commande suivante :
  - _flake8 --format=html --htmldir=flake-report_
- Lancer le fichier _index.html_ depuis le dossier _flake-report_
- Accéder à la liste des erreurs PEP8 en parcourant la page web