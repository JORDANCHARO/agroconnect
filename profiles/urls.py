from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_profile_detail(request):
    return redirect('profile_detail')

urlpatterns = [
    path('profile/', redirect_to_profile_detail, name='old_profile'),
    path('profile/detail/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    
    # URLs pour le tableau de bord du producteur
    path('producer/dashboard/', views.producer_dashboard, name='producer_dashboard'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('event/add/', views.add_event, name='add_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    
    # URLs pour le tableau de bord du transformateur
    path('processor/dashboard/', views.processor_dashboard, name='processor_dashboard'),
    path('profile/upload-facility-photo/', views.upload_facility_photo, name='upload_facility_photo'),
    path('profile/delete-facility-photo/<int:photo_id>/', views.delete_facility_photo, name='delete_facility_photo'),
    path('profile/upload-plantation-photo/', views.upload_plantation_photo, name='upload_plantation_photo'),
    path('profile/delete-plantation-photo/<int:photo_id>/', views.delete_plantation_photo, name='delete_plantation_photo'),
    path('profile/upload-producer-photo/', views.upload_producer_photo, name='upload_producer_photo'),
    path('profile/delete-producer-photo/<int:photo_id>/', views.delete_producer_photo, name='delete_producer_photo'),
    path('profile/upload-processor-photo/', views.upload_processor_photo, name='upload_processor_photo'),
    path('profile/delete-processor-photo/<int:photo_id>/', views.delete_processor_photo, name='delete_processor_photo'),
] 