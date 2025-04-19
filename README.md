# Simulation Financière ESN

Application de simulation financière pour un modèle SAS France / SARL Sénégal.

## Description

Cette application permet de simuler et visualiser les résultats financiers d'un modèle d'entreprise avec une SAS en France et une SARL au Sénégal. Elle permet de:

- Ajuster tous les paramètres de la simulation (taux d'imposition, salaires, tarifs, etc.)
- Visualiser les résultats sous forme de graphiques interactifs
- Comparer différents scénarios
- Télécharger les résultats pour une analyse plus approfondie

## Installation locale

1. Cloner le dépôt:
   ```
   git clone <url-du-depot>
   cd simulation_esn
   ```

2. Installer les dépendances:
   ```
   pip install -r requirements.txt
   ```

3. Lancer l'application:
   ```
   streamlit run app.py
   ```

## Déploiement

### Déploiement avec Docker

#### Utilisation du script d'aide

1. Exécuter le script d'aide:
   ```
   ./docker-run.sh
   ```

2. Accéder à l'application dans votre navigateur à l'adresse: http://localhost:8501

#### Manuellement

1. Construire l'image Docker:
   ```
   docker build -t simulation-esn .
   ```

2. Exécuter le conteneur:
   ```
   docker run -p 8501:8501 simulation-esn
   ```

3. Accéder à l'application dans votre navigateur à l'adresse: http://localhost:8501

### Déploiement avec Docker Compose

#### Utilisation du script d'aide

1. Afficher l'aide:
   ```
   ./docker-compose-run.sh help
   ```

2. Lancer en mode développement:
   ```
   ./docker-compose-run.sh dev
   ```

3. Lancer en mode production:
   ```
   ./docker-compose-run.sh prod
   ```

4. Arrêter l'application:
   ```
   ./docker-compose-run.sh stop-dev  # Pour le mode développement
   ./docker-compose-run.sh stop-prod # Pour le mode production
   ```

5. Voir les logs (mode production):
   ```
   ./docker-compose-run.sh logs
   ```

#### Manuellement

##### Pour le développement (avec volumes montés)

1. Lancer l'application avec Docker Compose:
   ```
   docker-compose up
   ```

2. Pour arrêter l'application:
   ```
   docker-compose down
   ```

##### Pour la production

1. Lancer l'application en mode production:
   ```
   docker-compose -f docker-compose-prod.yml up -d
   ```

2. Pour arrêter l'application:
   ```
   docker-compose -f docker-compose-prod.yml down
   ```

3. Pour voir les logs:
   ```
   docker-compose -f docker-compose-prod.yml logs -f
   ```

### Déploiement sur Streamlit Cloud

1. Créer un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. Connecter votre dépôt GitHub
3. Déployer l'application en sélectionnant le fichier `app.py`

### Déploiement sur Heroku

1. Créer un compte sur [Heroku](https://heroku.com)
2. Installer le CLI Heroku et se connecter:
   ```
   heroku login
   ```

3. Créer une nouvelle application:
   ```
   heroku create nom-de-votre-app
   ```

4. Déployer l'application:
   ```
   git push heroku main
   ```

### Déploiement sur un serveur Linux

1. Installer les dépendances:
   ```
   pip install -r requirements.txt
   ```

2. Lancer l'application avec Streamlit:
   ```
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```

## Structure du projet

- `app.py`: Application Streamlit principale
- `config/`: Configuration et paramètres
- `model/`: Logique métier et calculs
- `visualization/`: Fonctions de visualisation
- `utils/`: Utilitaires divers
- `Dockerfile`: Configuration pour construire l'image Docker
- `docker-compose.yml`: Configuration pour Docker Compose (développement)
- `docker-compose-prod.yml`: Configuration pour Docker Compose (production)
- `.dockerignore`: Fichiers à exclure du contexte de build Docker
- `docker-run.sh`: Script pour construire et exécuter rapidement l'application
- `docker-compose-run.sh`: Script d'aide pour gérer Docker Compose
- `.env`: Variables d'environnement pour Docker Compose
- `healthcheck.py`: Script de vérification de santé pour le conteneur Docker
