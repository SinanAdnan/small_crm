from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list, name='list'),
    path('create/', views.create_offer, name='create'),
    path('ajax/load-contacts/', views.load_contacts, name='load_contacts'),
    path('<int:pk>/', views.offer_detail, name='detail'),
    path('initialize_counter/', views.initialize_counter, name='initialize_counter'),
    path('delivery-methods/', views.delivery_method_list, name='delivery_method_list'),
    path('delivery-methods/create/', views.create_delivery_method, name='create_delivery_method'),
]