from django.contrib import admin
from django.utils.html import format_html
from .models import ProducerProfile, ProcessorProfile, ProcessorPhoto, ProducerPhoto

class ProcessorPhotoInline(admin.TabularInline):
    model = ProcessorPhoto
    extra = 1
    fields = ('image', 'description', 'photo_type', 'uploaded_at')

@admin.register(ProcessorProfile)
class ProcessorProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'verification_badge', 'document_status', 'created_at')
    search_fields = ('company_name', 'user__username', 'user__email')
    list_filter = ('created_at', 'user__is_verified')
    inlines = [ProcessorPhotoInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'company_name', 'description')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email', 'website')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'region')
        }),
        ('Capacités de transformation', {
            'fields': ('processing_capacity', 'processing_capabilities')
        }),
        ('Certifications', {
            'fields': ('certifications', 'certification_details')
        }),
    )

    def verification_badge(self, obj):
        if obj.user.is_verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px;">'
                '✓ Vérifié</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 4px;">'
            '⏳ En attente</span>'
        )
    verification_badge.short_description = "Statut de vérification"

    def document_status(self, obj):
        html = []
        user = obj.user
        
        # Document d'identité (toujours requis)
        if user.identity_document_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✗</span>')
        
        # Documents spécifiques pour les transformateurs
        if user.business_registration_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Entreprise ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Entreprise ✗</span>')
        if user.tax_registration_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Fiscal ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Fiscal ✗</span>')
        
        return format_html(''.join(html))
    document_status.short_description = "Documents"

@admin.register(ProducerProfile)
class ProducerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'verification_badge', 'document_status', 'created_at')
    search_fields = ('farm_name', 'user__username', 'user__email')
    list_filter = ('created_at', 'user__is_verified')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'farm_name', 'description')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'region')
        }),
        ('Exploitation', {
            'fields': ('farm_size', 'crops', 'farming_methods')
        }),
        ('Certifications', {
            'fields': ('certifications', 'certification_details')
        }),
    )

    def verification_badge(self, obj):
        if obj.user.is_verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px;">'
                '✓ Vérifié</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 4px;">'
            '⏳ En attente</span>'
        )
    verification_badge.short_description = "Statut de vérification"

    def document_status(self, obj):
        html = []
        user = obj.user
        
        # Document d'identité (toujours requis)
        if user.identity_document_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">ID ✗</span>')
        
        # Documents spécifiques pour les producteurs
        if user.land_title_verified:
            html.append('<span style="background-color: #28a745; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Terrain ✓</span>')
        else:
            html.append('<span style="background-color: #dc3545; color: white; margin-right: 5px; padding: 3px 8px; border-radius: 3px;">Terrain ✗</span>')
        
        return format_html(''.join(html))
    document_status.short_description = "Documents"
