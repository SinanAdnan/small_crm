from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list, name='list'),
    path('create/', views.create_offer, name='create'),
    path('<int:pk>/', views.offer_detail, name='detail'),
]