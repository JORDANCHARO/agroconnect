# AgroConnect 🌱

AgroConnect est une plateforme web innovante qui connecte les producteurs agricoles et les transformateurs au Cameroun. Notre mission est de faciliter les échanges et de promouvoir le développement de l'agriculture locale.

## 🌟 Fonctionnalités

- **Profils détaillés** pour les producteurs et transformateurs
- **Système de messagerie** intégré
- **Gestion des produits** et des événements de production
- **Système de partenariat** entre producteurs et transformateurs
- **Interface responsive** et moderne
- **Gestion des photos** de plantations et d'installations

## 🛠️ Technologies utilisées

- Python 3.x
- Django 5.0
- Bootstrap 5
- Font Awesome
- SQLite (développement) / PostgreSQL (production)

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/JORDANCHARO/agroconnect.git
cd agroconnect
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Effectuez les migrations :
```bash
python manage.py migrate
```

5. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancez le serveur de développement :
```bash
python manage.py runserver
```

## 📁 Structure du projet

```
agroconnect/
├── admin_custom/     # Personnalisation de l'interface admin
├── chat/            # Module de chat en temps réel
├── marketplace/     # Gestion du marché
├── messaging/       # Système de messagerie
├── profiles/        # Gestion des profils
├── users/           # Gestion des utilisateurs
└── templates/       # Templates HTML
```

## 👥 Rôles utilisateurs

- **Producteurs** : Gestion des plantations, produits et événements
- **Transformateurs** : Gestion des installations et capacités de transformation
- **Administrateurs** : Gestion globale de la plateforme

## 🔒 Sécurité

- Authentification sécurisée
- Protection CSRF
- Validation des données
- Gestion sécurisée des fichiers

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📧 Contact

Jordan Charo - [@JORDANCHARO](https://github.com/JORDANCHARO)

Lien du projet : [https://github.com/JORDANCHARO/agroconnect](https://github.com/JORDANCHARO/agroconnect) 