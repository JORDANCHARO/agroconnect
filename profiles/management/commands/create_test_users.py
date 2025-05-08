from django.core.management.base import BaseCommand
from users.models import CustomUser
from profiles.models import ProducerProfile, ProcessorProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'Crée des utilisateurs de test pour l\'application'

    def handle(self, *args, **kwargs):
        # Liste des utilisateurs à créer
        users_data = [
            # Producteurs
            {
                'username': 'producteur1',
                'email': 'producteur1@example.com',
                'password': 'test1234',
                'user_type': 'producer',
                'profile_data': {
                    'farm_name': 'Ferme du Soleil Levant',
                    'farm_description': 'Ferme familiale spécialisée dans la culture du maïs et du manioc',
                    'location': 'Douala, Cameroun',
                    'latitude': 4.0511,
                    'longitude': 9.7679
                }
            },
            {
                'username': 'producteur2',
                'email': 'producteur2@example.com',
                'password': 'test1234',
                'user_type': 'producer',
                'profile_data': {
                    'farm_name': 'Ferme des Trois Saisons',
                    'farm_description': 'Exploitation agricole diversifiée avec cultures maraîchères',
                    'location': 'Yaoundé, Cameroun',
                    'latitude': 3.8480,
                    'longitude': 11.5021
                }
            },
            # Transformateurs
            {
                'username': 'transformateur1',
                'email': 'transformateur1@example.com',
                'password': 'test1234',
                'user_type': 'processor',
                'profile_data': {
                    'company_name': 'AgroTrans SA',
                    'company_description': 'Entreprise de transformation de produits agricoles',
                    'location': 'Douala, Cameroun'
                }
            },
            {
                'username': 'transformateur2',
                'email': 'transformateur2@example.com',
                'password': 'test1234',
                'user_type': 'processor',
                'profile_data': {
                    'company_name': 'FoodPro Cameroun',
                    'company_description': 'Unité de transformation alimentaire moderne',
                    'location': 'Yaoundé, Cameroun'
                }
            }
        ]

        with transaction.atomic():
            for user_data in users_data:
                try:
                    # Vérifier si l'utilisateur existe déjà
                    if CustomUser.objects.filter(username=user_data['username']).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'L\'utilisateur {user_data["username"]} existe déjà'
                            )
                        )
                        continue

                    # Créer l'utilisateur
                    user = CustomUser.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        user_type=user_data['user_type']
                    )

                    # Créer le profil correspondant
                    if user_data['user_type'] == 'producer':
                        ProducerProfile.objects.create(
                            user=user,
                            **user_data['profile_data']
                        )
                    else:
                        ProcessorProfile.objects.create(
                            user=user,
                            **user_data['profile_data']
                        )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Utilisateur créé avec succès : {user_data["username"]}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Erreur lors de la création de l\'utilisateur {user_data["username"]}: {str(e)}'
                        )
                    ) 