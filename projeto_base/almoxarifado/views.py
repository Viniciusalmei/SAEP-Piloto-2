from rest_framework import viewsets, filters, permissions, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer

class PermisoRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT', 'PATCH']:
            return request.user.is_authenticated
        if request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_superuser
        return False

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [PermisoRoles]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [PermisoRoles]

    def perform_create(self, serializer):
        # ATENÇÃO ALUNO! Implemente a logica de estoque aqui 
        producto = serializer.validated_data['produto']
        cantidad = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']

        if tipo == 'S' and cantidad > producto.quantidade_estoque:
            raise ValidationError(
                f"Saída não permitida: estoque insuficiente. Disponível: {producto.quantidade_estoque}. Solicitado: {cantidad}"
            )

        if tipo == 'E':
            producto.quantidade_estoque += cantidad
        elif tipo == 'S':
            producto.quantidade_estoque -= cantidad
        
        producto.save()
        serializer.save(usuario=self.request.user)
    

    