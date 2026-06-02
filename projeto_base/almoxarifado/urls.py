from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/movimentar/<int:produto_id>/', views.registrar_movimentacao, name='registrar_movimentacao'),
    path('produtos/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
]