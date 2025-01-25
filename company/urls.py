from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'company'


urlpatterns = [
    path('', views.company_list, name='company_list'),  # This should be present
    path('add/', views.add_company, name='add_company'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('<int:company_id>/add_contact/', views.add_contact, name='add_contact'),
    path('contact/<int:contact_id>/edit/', views.edit_contact, name='edit_contact'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    path('edit/<int:pk>/', views.edit_company, name='edit_company'),
    path('delete/<int:pk>/', views.delete_company, name='delete_company'),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
