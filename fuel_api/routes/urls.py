from django.urls import path
from . import views  # Importa as views da aplicação


from .views import home, route_view

urlpatterns = [
    path('', views.home, name='home'),  # Rota para a página inicial
    path('get_route/', views.get_route, name='get_route'),  # Rota para obter a rota
     path('route/', route_view, name='route_view'),
]
