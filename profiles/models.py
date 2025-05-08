from django.db import models
from django.conf import settings

class ProducerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=200)
    farm_description = models.TextField(default="Aucune description disponible")
    farm_photos = models.ManyToManyField('FarmPhoto', blank=True)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    crops = models.TextField(help_text="Liste des cultures produites", default="")
    production_capacity = models.CharField(max_length=200, help_text="Capacité de production (ex: 100 tonnes/an)", default="")
    certification_documents = models.FileField(upload_to='certifications/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ferme de {self.user.username}"

class FarmPhoto(models.Model):
    image = models.ImageField(upload_to='farm_photos/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description or f"Photo de ferme {self.id}"

class Product(models.Model):
    UNIT_CHOICES = (
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('l', 'Litre'),
        ('ml', 'Millilitre'),
        ('unite', 'Unité'),
    )

    producer = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.get_unit_display()}"

class ProductionEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('planting', 'Plantation'),
        ('harvesting', 'Récolte'),
        ('maintenance', 'Maintenance'),
        ('other', 'Autre'),
    )

    producer = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()}"

class ProcessorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processor_profile')
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    location = models.CharField(max_length=200)
    certification_documents = models.FileField(upload_to='certification_documents/', null=True, blank=True)
    transformation_capacity = models.CharField(max_length=200, help_text="Capacité de transformation (ex: 1000 tonnes/an)")
    transformed_products = models.TextField(help_text="Liste des produits transformés")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"

class FacilityPhoto(models.Model):
    processor = models.ForeignKey(ProcessorProfile, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='facility_photos/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo d'installation de {self.processor.company_name if self.processor else 'Non assigné'}"

class PlantationPhoto(models.Model):
    processor = models.ForeignKey(ProcessorProfile, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='plantation_photos/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de plantation de {self.processor.company_name if self.processor else 'Non assigné'}"

class ProducerPhoto(models.Model):
    producer = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='producer_photos/')
    description = models.CharField(max_length=255, blank=True)
    photo_type = models.CharField(max_length=20, choices=[
        ('plantation', 'Plantation'),
        ('crop', 'Culture'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.producer.farm_name} - {self.get_photo_type_display()}"

    class Meta:
        ordering = ['-uploaded_at']

class ProcessorPhoto(models.Model):
    processor = models.ForeignKey(ProcessorProfile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='processor_photos/')
    description = models.CharField(max_length=255, blank=True)
    photo_type = models.CharField(max_length=20, choices=[
        ('facility', 'Installation'),
        ('machine', 'Machine'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.processor.company_name} - {self.get_photo_type_display()}"

    class Meta:
        ordering = ['-uploaded_at']
