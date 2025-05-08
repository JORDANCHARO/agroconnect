from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import random
from decimal import Decimal
from profiles.models import ProducerProfile, ProcessorProfile, Product, ProductionEvent
from datetime import timedelta

fake = Faker('fr_FR')
User = get_user_model()

class Command(BaseCommand):
    help = 'Crée des utilisateurs fictifs avec des profils complets'

    def handle(self, *args, **kwargs):
        # Créer 10 producteurs
        for _ in range(10):
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                user_type='producer'
            )

            # Créer le profil producteur
            producer = ProducerProfile.objects.create(
                user=user,
                farm_name=f"Ferme {fake.company()}",
                farm_description=fake.text(max_nb_chars=500),
                location=fake.city(),
                latitude=Decimal(str(fake.latitude())),
                longitude=Decimal(str(fake.longitude())),
                certification_documents=None
            )

            # Créer quelques produits
            for _ in range(random.randint(2, 5)):
                Product.objects.create(
                    producer=producer,
                    name=fake.word().capitalize(),
                    description=fake.text(max_nb_chars=200),
                    quantity=Decimal(str(random.randint(100, 1000))),
                    unit=random.choice(['kg', 'l', 'unite']),
                    price_per_unit=Decimal(str(random.randint(100, 1000))),
                    is_available=random.choice([True, False])
                )

            # Créer quelques événements de production
            for _ in range(random.randint(1, 3)):
                start_date = fake.date_time_between(start_date='-30d', end_date='+30d')
                ProductionEvent.objects.create(
                    producer=producer,
                    title=fake.sentence(),
                    description=fake.text(max_nb_chars=200),
                    event_type=random.choice(['planting', 'harvesting', 'maintenance']),
                    start_date=start_date,
                    end_date=start_date + timedelta(days=random.randint(1, 5)),
                    location=producer.location
                )

        # Créer 10 transformateurs
        for _ in range(10):
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                user_type='processor'
            )

            # Créer le profil transformateur
            ProcessorProfile.objects.create(
                user=user,
                company_name=f"Entreprise {fake.company()}",
                company_description=fake.text(max_nb_chars=500),
                location=fake.city(),
                certification_documents=None,
                facility_photos=None,
                plantation_photos=None
            )

        self.stdout.write(self.style.SUCCESS('20 utilisateurs fictifs ont été créés avec succès !')) 