from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'phone_number', 'address',
                 'identity_document', 'land_title', 'business_registration', 'tax_registration')
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'identity_document': forms.FileInput(attrs={'class': 'form-control'}),
            'land_title': forms.FileInput(attrs={'class': 'form-control'}),
            'business_registration': forms.FileInput(attrs={'class': 'form-control'}),
            'tax_registration': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre les champs de documents obligatoires
        self.fields['identity_document'].required = True
        self.fields['identity_document'].help_text = "Document d'identité (CNI, passeport, etc.)"
        
        # Ajouter des validations personnalisées
        self.fields['identity_document'].validators = [
            self.validate_file_extension
        ]
        
        # Rendre les champs spécifiques obligatoires selon le type d'utilisateur
        if 'user_type' in self.data:
            if self.data['user_type'] == 'producer':
                self.fields['land_title'].required = True
                self.fields['land_title'].help_text = "Titre foncier ou document prouvant la propriété/exploitation des terres"
            elif self.data['user_type'] == 'processor':
                self.fields['business_registration'].required = True
                self.fields['tax_registration'].required = True
                self.fields['business_registration'].help_text = "Extrait Kbis ou document d'enregistrement de l'entreprise"
                self.fields['tax_registration'].help_text = "Numéro d'identification fiscale"

    def validate_file_extension(self, value):
        """Valide l'extension des fichiers uploadés"""
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        if ext.lower() not in valid_extensions:
            raise forms.ValidationError('Format de fichier non supporté. Formats acceptés : PDF, JPG, JPEG, PNG')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'producer':
            if not cleaned_data.get('land_title'):
                self.add_error('land_title', 'Ce champ est obligatoire pour les producteurs.')
        elif user_type == 'processor':
            if not cleaned_data.get('business_registration'):
                self.add_error('business_registration', 'Ce champ est obligatoire pour les transformateurs.')
            if not cleaned_data.get('tax_registration'):
                self.add_error('tax_registration', 'Ce champ est obligatoire pour les transformateurs.')
        
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    password = None
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'address', 'profile_photo')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("L'image ne doit pas dépasser 2MB")
            if not photo.content_type.startswith('image/'):
                raise forms.ValidationError("Le fichier doit être une image")
        return photo 