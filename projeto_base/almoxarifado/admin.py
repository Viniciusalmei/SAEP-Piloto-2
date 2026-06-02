from django.contrib import admin
from .models import Produto, Movimentacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'quantidade_estoque', 'data_cadastro']
    search_fields = ['nome']

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'produto', 'tipo', 'quantidade', 'usuario_responsavel', 'data_hora']
    list_filter = ['tipo', 'data_hora']