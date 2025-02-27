from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list, name='list'),
    path('initialize_counter/', views.initialize_counter, name='initialize_counter'),
    path('create/', views.create_offer, name='create'),
    path('<int:pk>/', views.offer_detail, name='offer_detail'),
    path('edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('delete/<int:pk>/', views.delete_offer, name='delete_offer'),
    path('load_contacts/', views.load_contacts, name='load_contacts'),
    path('delivery_methods/', views.delivery_method_list, name='delivery_method_list'),
    path('delivery_methods/create/', views.create_delivery_method, name='create_delivery_method'),
    path('stages/', views.stage_list, name='stage_list'),
    path('stages/create/', views.create_stage, name='create_stage'),
    path('stages/edit/<int:pk>/', views.edit_stage, name='edit_stage'),
    path('stages/delete/<int:pk>/', views.delete_stage, name='delete_stage'),
    path('offer_stage/', views.offer_stage, name='offer_stage'),
    path('add_offer_product/<int:offer_id>/', views.add_offer_product, name='add_offer_product'),
    path('edit_offer_product/<int:offer_id>/<int:offer_product_id>/', views.edit_offer_product, name='edit_offer_product'),
    path('delete_offer_product/<int:offer_id>/<int:offer_product_id>/', views.delete_offer_product, name='delete_offer_product'),
    path('update_stage_order/', views.update_stage_order, name='update_stage_order'),
]