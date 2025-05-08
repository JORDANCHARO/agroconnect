from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from users.models import CustomUser
from users.admin import CustomUserAdmin
from profiles.models import ProducerProfile, ProcessorProfile, Product, ProductionEvent
from messaging.models import Message, PartnershipRequest

class AgroConnectAdminSite(AdminSite):
    site_header = 'AgroConnect Administration'
    site_title = 'AgroConnect Admin'
    index_title = 'Tableau de bord AgroConnect'

    def get_app_list(self, request, app_label=None):
        """
        Retourne une liste triée des applications disponibles pour l'utilisateur.
        """
        app_list = super().get_app_list(request)
        
        # Ajouter les statistiques
        stats = {
            'users': {
                'total': CustomUser.objects.count(),
                'producers': CustomUser.objects.filter(user_type='producer').count(),
                'processors': CustomUser.objects.filter(user_type='processor').count(),
                'verified': CustomUser.objects.filter(is_verified=True).count(),
            },
            'profiles': {
                'total': ProducerProfile.objects.count() + ProcessorProfile.objects.count(),
                'producers': ProducerProfile.objects.count(),
                'processors': ProcessorProfile.objects.count(),
            },
            'products': {
                'total': Product.objects.count(),
                'available': Product.objects.filter(is_available=True).count(),
            },
            'messages': {
                'total': Message.objects.count(),
                'unread': Message.objects.filter(is_read=False).count(),
            }
        }
        
        # Ajouter les statistiques à chaque application
        for app in app_list:
            if app['app_label'] == 'users':
                app['stats'] = {
                    'Utilisateurs': stats['users']['total'],
                    'Producteurs': stats['users']['producers'],
                    'Transformateurs': stats['users']['processors'],
                    'Vérifiés': stats['users']['verified']
                }
            elif app['app_label'] == 'profiles':
                app['stats'] = {
                    'Profils': stats['profiles']['total'],
                    'Producteurs': stats['profiles']['producers'],
                    'Transformateurs': stats['profiles']['processors']
                }
            elif app['app_label'] == 'products':
                app['stats'] = {
                    'Produits': stats['products']['total'],
                    'Disponibles': stats['products']['available']
                }
            elif app['app_label'] == 'messaging':
                app['stats'] = {
                    'Messages': stats['messages']['total'],
                    'Non lus': stats['messages']['unread']
                }
        
        return app_list

admin_site = AgroConnectAdminSite(name='admin')

# Enregistrement des modèles avec des interfaces personnalisées
admin_site.register(CustomUser, CustomUserAdmin)

@admin.register(ProducerProfile, site=admin_site)
class ProducerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'location', 'created_at')
    list_filter = ('location',)
    search_fields = ('farm_name', 'user__username', 'location', 'farm_description')
    raw_id_fields = ('user',)
    
    fieldsets = (
        (None, {'fields': ('user', 'farm_name')}),
        ('Informations de la ferme', {
            'fields': ('farm_description', 'location', 'latitude', 'longitude')
        }),
        ('Documents', {'fields': ('certification_documents', 'farm_photos')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProcessorProfile, site=admin_site)
class ProcessorProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location', 'transformation_capacity', 'transformed_products', 'created_at')
    search_fields = ('company_name', 'user__username', 'location', 'company_description', 'transformed_products')
    raw_id_fields = ('user',)
    
    fieldsets = (
        (None, {'fields': ('user', 'company_name')}),
        ('Informations de l\'entreprise', {
            'fields': ('company_description', 'location')
        }),
        ('Capacités et Produits', {
            'fields': ('transformation_capacity', 'transformed_products'),
            'description': 'Informations sur la capacité de transformation et les produits transformés'
        }),
        ('Documents', {
            'fields': ('certification_documents',),
            'description': 'Documents de certification de l\'entreprise'
        }),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'producer', 'quantity', 'unit', 'price_per_unit', 'is_available')
    list_filter = ('is_available', 'unit')
    search_fields = ('name', 'producer__farm_name', 'description')
    raw_id_fields = ('producer',)

@admin.register(ProductionEvent, site=admin_site)
class ProductionEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'event_type', 'start_date', 'end_date')
    list_filter = ('event_type', 'start_date')
    search_fields = ('title', 'producer__farm_name', 'description')
    raw_id_fields = ('producer',)

@admin.register(Message, site=admin_site)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'receiver__username')
    raw_id_fields = ('sender', 'receiver')

@admin.register(PartnershipRequest, site=admin_site)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    raw_id_fields = ('sender', 'receiver')
