from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/', include('routes.urls')),  # Redireciona para as URLs da app routes
]
