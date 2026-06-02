from rest_framework import viewsets, filters
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer

class PermissaoAlmoxarifado(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_superuser
            
        return True


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated, PermissaoAlmoxarifado]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']


class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [IsAuthenticated, PermissaoAlmoxarifado]
    
    def perform_create(self, serializer):
        dados_validados = serializer.validated_data
        produto = dados_validados['produto']
        tipo = dados_validados['tipo']  
        quantidade = dados_validados['quantidade']

        if tipo == 'S':
            if quantidade > produto.quantidade_estoque:
                raise ValidationError({
                    "error": f"Saída não permitida: estoque insuficiente. Disponível: {produto.quantidade_estoque}. Solicitado: {quantidade}."
                })
            
            produto.quantidade_estoque -= quantidade
            
        elif tipo == 'E':
            produto.quantidade_estoque += quantidade

        produto.save()

        serializer.save(usuario=self.request.user)