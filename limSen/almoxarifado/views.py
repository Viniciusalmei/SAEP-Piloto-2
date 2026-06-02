from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer
from .models import IsAdminOrOperatorReadOnly

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAdminOrOperatorReadOnly]  # Garante que rotas sejam privadas e controladas por perfil
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']  # Filtros por nome e data exigidos
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [IsAdminOrOperatorReadOnly] 
    
    def perform_create(self, serializer):
        # Captura os dados enviados na requisição
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']  # 'E' para Entrada, 'S' para Saída
        
        # Garante que não sejam enviadas quantidades negativas ou zeradas
        if quantidade <= 0:
            raise ValidationError({"detail": "A quantidade deve ser maior que zero."})

        # Bloquear tentativa de registrar saída maior que o saldo disponível
        if tipo == 'S':
            if produto.quantidade_estoque < quantidade:
                
                mensagem_erro = f"Saída não permitida: estoque insuficiente. Disponível {produto.quantidade_estoque}: Solicitado:{quantidade}"
                raise ValidationError({"detail": mensagem_erro})
            
           
            produto.quantidade_estoque -= quantidade
            
        elif tipo == 'E':
          
            produto.quantidade_estoque += quantidade
        
        # Salva a alteração física do saldo do produto no banco de dados
        produto.save()
        
        serializer.save(usuario=self.request.user)