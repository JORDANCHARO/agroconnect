# AgroConnect - Plateforme de Connexion Agricole

Une plateforme web pour connecter les producteurs agricoles et les transformateurs au Cameroun.

## Fonctionnalités

- Authentification sécurisée avec JWT
- Profils personnalisés pour producteurs et transformateurs
- Système de messagerie interne
- Gestion des documents et certifications
- Interface d'administration complète
- Fonctionne en mode hors ligne
- Interface utilisateur moderne et intuitive

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd agroconnect
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## Structure du Projet

- `users/` - Gestion des utilisateurs et authentification
- `profiles/` - Profils des producteurs et transformateurs
- `messaging/` - Système de messagerie
- `admin/` - Interface d'administration personnalisée
- `core/` - Fonctionnalités principales et configurations

## Technologies Utilisées

- Backend: Django + Django REST Framework
- Frontend: Django Templates + Bootstrap 5
- Base de données: SQLite
- Authentification: JWT

## Contribution

Les contributions sont les bienvenues ! Veuillez lire les directives de contribution avant de soumettre une pull request.

## Licence

Ce projet est sous licence MIT. 