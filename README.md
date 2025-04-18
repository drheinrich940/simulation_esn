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
