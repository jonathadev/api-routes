from django.urls import path
from .views import get_route

from . import views  # Isso importa as views da aplicação

urlpatterns = [
    path('', views.calculate_route, name='calculate_route'),  # Mapeia a raiz da aplicação
    path('calculate/<str:start>/<str:end>/', views.calculate_route, name='calculate_route_with_params'),
]
