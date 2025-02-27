# products/urls.py
from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
    path('api/product/<int:product_id>/', views.product_detail_api, name='product_detail_api'),
    path('', views.product_list, name='product_list'),
    path('new/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('data/<int:product_id>/', views.product_offer_data, name='product_offer_data'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('add-category/', views.add_category, name='add_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]
