from rest_framework import viewsets, filters, serializers
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer
from .permissions import RoleBasedAccessPermission

class ProdutoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [RoleBasedAccessPermission]
    pagination_class = ProdutoPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [RoleBasedAccessPermission]
    
    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']

        if tipo == 'S':
            if quantidade > produto.quantidade_estoque:
                raise serializers.ValidationError(
                    f"Saída não permitida: estoque insuficiente. Disponível: {produto.quantidade_estoque}. Solicitado: {quantidade}."
                )
            produto.quantidade_estoque -= quantidade
        elif tipo == 'E':
            produto.quantidade_estoque += quantidade
            
        produto.save()
        serializer.save(usuario=self.request.user)
