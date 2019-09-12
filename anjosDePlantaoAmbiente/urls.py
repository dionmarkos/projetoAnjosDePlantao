from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicos, name='servicos'),
    path('cadastrar_pessoa/', views.cadastrar_pessoa, name='cadastrar_pessoa'),
    path('cadastrar_pessoa/<int:pk>/', views.cadastrar_pessoa_detail, name='cadastrar_pessoa_detail'),
    path('cadastrar_pessoa_inativacao/<int:pk>/', views.cadastrar_pessoa_inativacao, name='cadastrar_pessoa_inativacao'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('cadastrar_produto/<int:pk>/', views.cadastrar_produto_detail, name='cadastrar_produto_detail'),
    path('cadastrar_produto_delete/<int:pk>/', views.cadastrar_produto_delete, name='cadastrar_produto_delete'),
    path('caixa_geral/', views.caixa_geral, name='caixa_geral'),
    path('doacao_entrada/', views.doacao_entrada, name='doacao_entrada'),
    path('doacao_entrada_detail/<int:pk>/', views.doacao_entrada_detail, name='doacao_entrada_detail'),
    path('doacao_entrada_delete/<int:pk>/', views.doacao_entrada_delete, name='doacao_entrada_delete'),
    path('doacao_entrada_delete_produto/<int:pk>/', views.doacao_entrada_delete_produto, name='doacao_entrada_delete_produto'),
    path('doacao_saida/', views.doacao_saida, name='doacao_saida'),
    path('doacao_saida_detail/<int:pk>/', views.doacao_saida_detail, name='doacao_saida_detail'),
    path('doacao_saida_delete/<int:pk>/', views.doacao_saida_delete, name='doacao_saida_delete'),
    path('doacao_saida_delete_produto/<int:pk>/', views.doacao_saida_delete_produto, name='doacao_saida_delete_produto'),
    path('busca/', views.busca, name='busca'),
    path('busca/<int:pk>/', views.busca, name='busca'),
]
