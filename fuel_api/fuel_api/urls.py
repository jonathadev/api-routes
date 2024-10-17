from django.contrib import admin
from django.urls import path, include  # Não esqueça de incluir o módulo include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/', include('routes.urls')),  # Substitua 'api_routes' pelo nome correto da sua app
]
