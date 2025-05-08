from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import ProducerProfile, ProcessorProfile
from django.db import transaction

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Popule la base de données avec des données de test réalistes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Suppression des données existantes...')
        CustomUser.objects.filter(is_superuser=False).delete()
        
        self.stdout.write('Création des données de test...')
        
        # Création des transformateurs
        processors_data = [
            {
                'username': 'transfo_cafe',
                'email': 'contact@transfo-cafe.com',
                'password': 'testpass123',
                'first_name': 'Mohamed',
                'last_name': 'Diallo',
                'phone_number': '+225 0700000001',
                'address': 'Zone Industrielle, Abidjan',
                'company_name': 'Transformation Café CI',
                'company_description': 'Entreprise spécialisée dans la transformation du café arabica et robusta. Nous valorisons le café local et travaillons avec les producteurs locaux.',
                'location': 'Abidjan, Côte d\'Ivoire',
                'transformation_capacity': '5000 tonnes/an',
                'transformed_products': 'Café vert\nCafé torréfié\nCafé moulu\nCafé soluble'
            },
            {
                'username': 'cacao_plus',
                'email': 'info@cacao-plus.com',
                'password': 'testpass123',
                'first_name': 'Aminata',
                'last_name': 'Koné',
                'phone_number': '+225 0700000002',
                'address': 'Route de Dabou, Abidjan',
                'company_name': 'Cacao Plus Transformation',
                'company_description': 'Transformateur de cacao certifié, spécialisé dans la production de pâte de cacao et de beurre de cacao de haute qualité.',
                'location': 'Dabou, Côte d\'Ivoire',
                'transformation_capacity': '3000 tonnes/an',
                'transformed_products': 'Pâte de cacao\nBeurre de cacao\nPoudre de cacao\nChocolat artisanal'
            },
            {
                'username': 'agro_transform',
                'email': 'contact@agro-transform.com',
                'password': 'testpass123',
                'first_name': 'Kouamé',
                'last_name': 'Yao',
                'phone_number': '+225 0700000003',
                'address': 'Zone Industrielle, Yamoussoukro',
                'company_name': 'Agro Transformation SA',
                'company_description': 'Entreprise polyvalente spécialisée dans la transformation de produits agricoles locaux. Nous transformons une large gamme de produits.',
                'location': 'Yamoussoukro, Côte d\'Ivoire',
                'transformation_capacity': '10000 tonnes/an',
                'transformed_products': 'Huile de palme\nJus de fruits\nConfitures\nFruits séchés'
            }
        ]

        # Création des producteurs
        producers_data = [
            {
                'username': 'ferme_cafe',
                'email': 'contact@ferme-cafe.com',
                'password': 'testpass123',
                'first_name': 'Moussa',
                'last_name': 'Coulibaly',
                'phone_number': '+225 0700000004',
                'address': 'Man, Côte d\'Ivoire',
                'farm_name': 'Ferme Café de l\'Ouest',
                'farm_description': 'Exploitation familiale spécialisée dans la culture du café arabica. Nous pratiquons une agriculture durable et respectueuse de l\'environnement.',
                'location': 'Man, Côte d\'Ivoire',
                'latitude': 7.4041,
                'longitude': -7.5539,
                'crops': 'Café Arabica\nCafé Robusta\nBananes plantains',
                'production_capacity': '200 tonnes/an de café'
            },
            {
                'username': 'cacao_quality',
                'email': 'info@cacao-quality.com',
                'password': 'testpass123',
                'first_name': 'Fatou',
                'last_name': 'Traoré',
                'phone_number': '+225 0700000005',
                'address': 'Soubré, Côte d\'Ivoire',
                'farm_name': 'Cacao Quality Farm',
                'farm_description': 'Plantation de cacao certifiée, produisant du cacao de qualité supérieure. Nous mettons l\'accent sur la qualité et la traçabilité.',
                'location': 'Soubré, Côte d\'Ivoire',
                'latitude': 5.7847,
                'longitude': -6.6017,
                'crops': 'Cacao\nPalmier à huile\nHévéa',
                'production_capacity': '150 tonnes/an de cacao'
            },
            {
                'username': 'agro_divers',
                'email': 'contact@agro-divers.com',
                'password': 'testpass123',
                'first_name': 'Issouf',
                'last_name': 'Ouattara',
                'phone_number': '+225 0700000006',
                'address': 'Bouaké, Côte d\'Ivoire',
                'farm_name': 'Agro Diversité',
                'farm_description': 'Ferme diversifiée produisant une large gamme de cultures : maïs, riz, légumes et fruits. Nous pratiquons l\'agroécologie.',
                'location': 'Bouaké, Côte d\'Ivoire',
                'latitude': 7.6900,
                'longitude': -5.0300,
                'crops': 'Maïs\nRiz\nTomates\nPiments\nAubergines\nHaricots verts',
                'production_capacity': '500 tonnes/an de produits divers'
            }
        ]

        with transaction.atomic():
            # Création des transformateurs
            for data in processors_data:
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    phone_number=data['phone_number'],
                    address=data['address'],
                    user_type='processor'
                )
                ProcessorProfile.objects.create(
                    user=user,
                    company_name=data['company_name'],
                    company_description=data['company_description'],
                    location=data['location'],
                    transformation_capacity=data['transformation_capacity'],
                    transformed_products=data['transformed_products']
                )

            # Création des producteurs
            for data in producers_data:
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    phone_number=data['phone_number'],
                    address=data['address'],
                    user_type='producer'
                )
                ProducerProfile.objects.create(
                    user=user,
                    farm_name=data['farm_name'],
                    farm_description=data['farm_description'],
                    location=data['location'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    crops=data['crops'],
                    production_capacity=data['production_capacity']
                )

        self.stdout.write(self.style.SUCCESS('Données de test créées avec succès !')) 