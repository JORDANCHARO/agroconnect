from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('send/<int:receiver_id>/', views.send_message, name='send_message_to'),
    path('partnership-requests/', views.partnership_requests, name='partnership_requests'),
    path('send-partnership-request/<int:receiver_id>/', views.send_partnership_request, name='send_partnership_request'),
    path('respond-partnership-request/<int:pk>/<str:status>/', views.respond_to_partnership_request, name='respond_partnership_request'),
    path('partnership/<int:pk>/', views.partnership_detail, name='partnership_detail'),
] 