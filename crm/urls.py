from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', TemplateView.as_view(template_name='home.html'), name='home'),  # Home page
    path('companies/', include('company.urls')),
    path('products/', include('products.urls', namespace='products')),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)