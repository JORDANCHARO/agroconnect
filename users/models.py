from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('producer', 'Producteur'),
        ('processor', 'Transformateur'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Documents d'identité requis pour tous les utilisateurs
    identity_document = models.FileField(
        upload_to='identity_documents/',
        help_text="Document d'identité (CNI, passeport, etc.)",
        null=True,
        blank=True
    )
    identity_document_verified = models.BooleanField(default=False)
    
    # Documents spécifiques aux producteurs
    land_title = models.FileField(
        upload_to='land_titles/',
        help_text="Titre foncier ou document prouvant la propriété/exploitation des terres",
        null=True,
        blank=True
    )
    land_title_verified = models.BooleanField(default=False)
    
    # Documents spécifiques aux transformateurs
    business_registration = models.FileField(
        upload_to='business_registrations/',
        help_text="Extrait Kbis ou document d'enregistrement de l'entreprise",
        null=True,
        blank=True
    )
    business_registration_verified = models.BooleanField(default=False)
    tax_registration = models.FileField(
        upload_to='tax_registrations/',
        help_text="Numéro d'identification fiscale",
        null=True,
        blank=True
    )
    tax_registration_verified = models.BooleanField(default=False)
    
    # Statut de vérification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
    def get_user_type_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, self.user_type)
    
    def get_required_documents(self):
        """Retourne la liste des documents requis selon le type d'utilisateur"""
        required_docs = ['identity_document']
        if self.user_type == 'producer':
            required_docs.append('land_title')
        elif self.user_type == 'processor':
            required_docs.extend(['business_registration', 'tax_registration'])
        return required_docs
    
    def verify_document(self, document_type, notes=""):
        """Marque un document comme vérifié"""
        if document_type == 'identity_document':
            self.identity_document_verified = True
        elif document_type == 'land_title':
            self.land_title_verified = True
        elif document_type == 'business_registration':
            self.business_registration_verified = True
        elif document_type == 'tax_registration':
            self.tax_registration_verified = True
        
        # Ajouter la note avec la date
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.verification_notes:
            self.verification_notes += f"\n[{timestamp}] {notes}"
        else:
            self.verification_notes = f"[{timestamp}] {notes}"
        
        self.save()

    def verify_profile(self, notes=""):
        """Marque le profil comme vérifié si tous les documents requis sont vérifiés"""
        if self.is_fully_verified():
            self.is_verified = True
            self.verification_date = timezone.now()
            
            # Ajouter la note avec la date
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.verification_notes:
                self.verification_notes += f"\n[{timestamp}] {notes}"
            else:
                self.verification_notes = f"[{timestamp}] {notes}"
            
            self.save()

    def is_fully_verified(self):
        """Vérifie si tous les documents requis sont vérifiés selon le type d'utilisateur"""
        if not self.identity_document_verified:
            return False
        
        if self.user_type == 'producer':
            return self.land_title_verified
        elif self.user_type == 'processor':
            return self.business_registration_verified and self.tax_registration_verified
        
        return False

    def get_verification_status(self):
        """Retourne le statut de vérification des documents"""
        status = {
            'identity_document': self.identity_document_verified,
            'land_title': self.land_title_verified if self.user_type == 'producer' else None,
            'business_registration': self.business_registration_verified if self.user_type == 'processor' else None,
            'tax_registration': self.tax_registration_verified if self.user_type == 'processor' else None,
        }
        return status

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
