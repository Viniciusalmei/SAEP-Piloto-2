from rest_framework import viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer, UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import serializers


class ProdutoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PermissoesPorPerfil(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'ADMIN':
                return True
            if request.user.is_superuser: 
                return True
            return False
        return True


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    pagination_class = ProdutoPagination
    permission_classes = [PermissoesPorPerfil]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']


class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [PermissoesPorPerfil]
    
    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']

       
        if tipo == 'S' and quantidade > produto.quantidade_estoque:
            mensagem = f"Saída não permitida: estoque insuficiente. Disponível {produto.quantidade_estoque}: Solicitado:{quantidade}"
            raise serializers.ValidationError(mensagem)

        
        if tipo == 'E':
            produto.quantidade_estoque += quantidade
        elif tipo == 'S':
            produto.quantidade_estoque -= quantidade
        
        produto.save()
        serializer.save(usuario=self.request.user)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]