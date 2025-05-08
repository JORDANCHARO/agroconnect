from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'verification_badge', 'document_status', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_verified', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    actions = ['verify_selected_profiles', 'verify_selected_documents']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_photo')}),
        ('Type d\'utilisateur', {'fields': ('user_type',)}),
        ('Documents et vérification', {
            'fields': (
                ('identity_document', 'identity_document_verified', 'view_identity_document'),
                ('land_title', 'land_title_verified', 'view_land_title'),
                ('business_registration', 'business_registration_verified', 'view_business_registration'),
                ('tax_registration', 'tax_registration_verified', 'view_tax_registration'),
                'is_verified',
                'verification_date',
                'verification_notes'
            ),
            'classes': ('collapse',),
            'description': 'Documents requis pour la vérification du profil'
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = (
        'view_identity_document', 'view_land_title', 
        'view_business_registration', 'view_tax_registration'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

    def verification_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px;">'
                '✓ Vérifié</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 4px;">'
            '⏳ En attente</span>'
        )
    verification_badge.short_description = 'Statut de vérification'

    def document_status(self, obj):
        html = []
        
        # Document d'identité (toujours requis)
        if obj.identity_document_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✗</span>')
        
        # Documents spécifiques selon le type d'utilisateur
        if obj.user_type == 'producer':
            if obj.land_title_verified:
                html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Terrain ✓</span>')
            else:
                html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Terrain ✗</span>')
        elif obj.user_type == 'processor':
            if obj.business_registration_verified:
                html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Entreprise ✓</span>')
            else:
                html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Entreprise ✗</span>')
            if obj.tax_registration_verified:
                html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Fiscal ✓</span>')
            else:
                html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Fiscal ✗</span>')
        
        return format_html(''.join(html))
    document_status.short_description = 'Documents'

    def view_identity_document(self, obj):
        if obj.identity_document:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" class="button" style="display: inline-block; padding: 8px 15px; background-color: #417690; color: white; text-decoration: none; border-radius: 4px;">'
                '<i class="fas fa-id-card"></i> Voir le document d\'identité</a>'
                '</div>',
                obj.identity_document.url
            )
        return format_html(
            '<div style="margin: 10px 0; color: #999;">'
            '<i class="fas fa-times-circle"></i> Aucun document uploadé'
            '</div>'
        )
    view_identity_document.short_description = ""

    def view_land_title(self, obj):
        if obj.land_title:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" class="button" style="display: inline-block; padding: 8px 15px; background-color: #417690; color: white; text-decoration: none; border-radius: 4px;">'
                '<i class="fas fa-file-contract"></i> Voir le titre foncier</a>'
                '</div>',
                obj.land_title.url
            )
        return format_html(
            '<div style="margin: 10px 0; color: #999;">'
            '<i class="fas fa-times-circle"></i> Aucun document uploadé'
            '</div>'
        )
    view_land_title.short_description = ""

    def view_business_registration(self, obj):
        if obj.business_registration:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" class="button" style="display: inline-block; padding: 8px 15px; background-color: #417690; color: white; text-decoration: none; border-radius: 4px;">'
                '<i class="fas fa-building"></i> Voir l\'extrait Kbis</a>'
                '</div>',
                obj.business_registration.url
            )
        return format_html(
            '<div style="margin: 10px 0; color: #999;">'
            '<i class="fas fa-times-circle"></i> Aucun document uploadé'
            '</div>'
        )
    view_business_registration.short_description = ""

    def view_tax_registration(self, obj):
        if obj.tax_registration:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<a href="{}" target="_blank" class="button" style="display: inline-block; padding: 8px 15px; background-color: #417690; color: white; text-decoration: none; border-radius: 4px;">'
                '<i class="fas fa-file-invoice"></i> Voir le numéro fiscal</a>'
                '</div>',
                obj.tax_registration.url
            )
        return format_html(
            '<div style="margin: 10px 0; color: #999;">'
            '<i class="fas fa-times-circle"></i> Aucun document uploadé'
            '</div>'
        )
    view_tax_registration.short_description = ""

    def verify_selected_profiles(self, request, queryset):
        for user in queryset:
            if user.is_fully_verified():
                user.verify_profile("Validation par l'administrateur")
        self.message_user(request, f"{queryset.count()} profils ont été vérifiés.")
    verify_selected_profiles.short_description = "Vérifier les profils sélectionnés"

    def verify_selected_documents(self, request, queryset):
        for user in queryset:
            # Vérifier le document d'identité
            if user.identity_document and not user.identity_document_verified:
                user.verify_document('identity_document', "Validation par l'administrateur")
            
            # Vérifier les documents spécifiques
            if user.user_type == 'producer' and user.land_title and not user.land_title_verified:
                user.verify_document('land_title', "Validation par l'administrateur")
            elif user.user_type == 'processor':
                if user.business_registration and not user.business_registration_verified:
                    user.verify_document('business_registration', "Validation par l'administrateur")
                if user.tax_registration and not user.tax_registration_verified:
                    user.verify_document('tax_registration', "Validation par l'administrateur")
        
        self.message_user(request, f"Les documents de {queryset.count()} utilisateurs ont été vérifiés.")
    verify_selected_documents.short_description = "Vérifier les documents sélectionnés"

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',)
        }
