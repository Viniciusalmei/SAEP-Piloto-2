from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer, UserSerializer

# 1. Cadastro de Utilizadores
class CadastroUsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# 2. Paginação exigida (5 itens por página)
class PaginacaoCustomizada(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

# 3. Permissões (Administrador vs Operador)
class PermissaoRotasSAEP(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True # Administrador pode tudo
            
        if request.method == 'DELETE':
            return False # Operador não pode apagar
            
        return request.method in ['GET', 'POST', 'PUT']

# 4. View de Produtos
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('nome')
    serializer_class = ProdutoSerializer
    permission_classes = [PermissaoRotasSAEP]
    pagination_class = PaginacaoCustomizada
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']

# 5. View de Movimentações (com validação de stock)
class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all().order_by('-data_hora')
    serializer_class = MovimentacaoSerializer
    permission_classes = [PermissaoRotasSAEP] 
    
    def create(self, request, *args, **kwargs):
        id_produto = request.data.get('produto')
        quantidade_solicitada = int(request.data.get('quantidade', 0))
        tipo_movimentacao = request.data.get('tipo') 

        try:
            produto = Produto.objects.get(pk=id_produto)
        except Produto.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Regra de Stock do documento SAEP
        if tipo_movimentacao == 'S': 
            if quantidade_solicitada > produto.quantidade_estoque:
                return Response(
                    {"error": f"Saída não permitida: estoque insuficiente. Disponível {produto.quantidade_estoque}: Solicitado:{quantidade_solicitada}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            produto.quantidade_estoque -= quantidade_solicitada
        
        elif tipo_movimentacao == 'E': 
            produto.quantidade_estoque += quantidade_solicitada

        produto.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=self.request.user) # Salva o utilizador atual
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)