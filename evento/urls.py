from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('cadastrar_evento_detail/<int:pk>/', views.cadastrar_evento_detail, name='cadastrar_evento_detail'),
    path('cadastrar_evento_inativacao/<int:pk>/', views.cadastrar_evento_inativacao, name='cadastrar_evento_inativacao'),
]
