from rest_framework import viewsets, filters, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    
    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']

        if quantidade <= 0:
            raise ValidationError({"quantidade": "A quantidade informada deve ser maior que zero."})

        if tipo == 'E':
        
            produto.quantidade_estoque += quantidade
        elif tipo == 'S':
        
            if produto.quantidade_estoque < quantidade:
                raise ValidationError({"quantidade": f"Estoque insuficiente. O saldo atual é de {produto.quantidade_estoque} unidades."})
      
            produto.quantidade_estoque -= quantidade
        

        produto.save()
        
       
        serializer.save(usuario=self.request.user)