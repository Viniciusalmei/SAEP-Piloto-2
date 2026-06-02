from django.db import transaction
from .models import Produto

def registrar_movimentacao(produto_id, quantidade, tipo, usuario):
    with transaction.atomic():
        produto = Produto.objects.select_for_update().get(id=produto_id)

        if tipo == 'S':  
            if quantidade > produto.quantidade_estoque:
                raise ValueError(
                    f"Saída não permitida: estoque insuficiente. "
                    f"Disponível: {produto.quantidade_estoque}. Solicitado: {quantidade}."
                )
            produto.quantidade_estoque -= quantidade
        else:  
            produto.quantidade_estoque += quantidade

        produto.save()