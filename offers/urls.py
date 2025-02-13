from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list, name='list'),
    path('create/', views.create_offer, name='create'),
    path('ajax/load-contacts/', views.load_contacts, name='load_contacts'),
    path('<int:pk>/', views.offer_detail, name='offer_detail'),
    path('<int:pk>/edit/', views.edit_offer, name='edit_offer'),
    path('<int:pk>/delete/', views.delete_offer, name='delete_offer'),
    path('initialize_counter/', views.initialize_counter, name='initialize_counter'),
    path('delivery-methods/', views.delivery_method_list, name='delivery_method_list'),
    path('delivery-methods/create/', views.create_delivery_method, name='create_delivery_method'),
    path('stages/', views.stage_list, name='stage_list'), 
    path('stages/create/', views.create_stage, name='create_stage'),  # Create stage
    path('stages/edit/<int:pk>/', views.edit_stage, name='edit_stage'),  # Edit stage
    path('stages/delete/<int:pk>/', views.delete_stage, name='delete_stage'),  # Delete stage
    path('offer-stages/', views.offer_stage, name='offer_stage'), #Offer stage page
    path('<int:offer_id>/add-product/', views.add_offer_product, name='add_offer_product'),  # Add product to offer
    path('<int:offer_id>/edit-product/<int:offer_product_id>/', views.edit_offer_product, name='edit_offer_product'),  # Edit product in offer
    path('<int:offer_id>/delete-product/<int:offer_product_id>/', views.delete_offer_product, name='delete_offer_product'),  # Delete product from offer
    
]