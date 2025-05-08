from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message de {self.sender} à {self.receiver}: {self.subject}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']

class PartnershipRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de partenariat de {self.sender} à {self.receiver}"

    class Meta:
        verbose_name = 'Demande de partenariat'
        verbose_name_plural = 'Demandes de partenariat'
        ordering = ['-created_at']

class Partnership(models.Model):
    STATUS_CHOICES = (
        ('active', 'Actif'),
        ('suspended', 'Suspendu'),
        ('terminated', 'Terminé'),
    )

    producer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='producer_partnerships')
    processor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processor_partnerships')
    request = models.OneToOneField(PartnershipRequest, on_delete=models.SET_NULL, null=True, related_name='partnership')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    terms = models.TextField(blank=True, help_text="Conditions du partenariat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partenariat entre {self.producer.username} et {self.processor.username}"

    class Meta:
        verbose_name = 'Partenariat'
        verbose_name_plural = 'Partenariats'
        ordering = ['-created_at']
        unique_together = ['producer', 'processor']
