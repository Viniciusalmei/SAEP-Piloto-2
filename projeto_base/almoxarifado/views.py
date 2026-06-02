from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto, Movimentacao
from .serializers import ProdutoSerializer, MovimentacaoSerializer

class CustomAuthenticationPermission(permissions.BasePermission):
    """
    Regra do SAEP: 
    - Operador pode apenas consultar, inserir e atualizar (GET, POST, PUT, PATCH).
    - Administrador pode tudo, incluindo deletar (DELETE)[cite: 13, 69].
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            

        try:
            tipo_usuario = request.user.perfil.tipo
        except AttributeError:
            tipo_usuario = 'operador'
        if tipo_usuario == 'administrador':
            return True

        if tipo_usuario == 'operador' and request.method == 'DELETE':
            return False

        return True



class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [CustomAuthenticationPermission] 
    
   
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']



class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [CustomAuthenticationPermission] 
    
    def perform_create(self, serializer):
        dados = serializer.validated_data
        produto = dados['produto']
        quantidade_solicitada = dados['quantidade']
        tipo_movimentacao = dados['tipo'] 

     
        if tipo_movimentacao == 'S':
            estoque_disponivel = produto.quantidade_estoque

           
            if quantidade_solicitada > estoque_disponivel:
               
                mensagem_erro = f"Saída não permitida: estoque insuficiente. Disponível: {estoque_disponivel}. Solicitado: {quantidade_solicitada}."
                raise ValidationError({"detail": mensagem_erro})

            
            produto.quantidade_estoque -= quantidade_solicitada
            produto.save()

    
        elif tipo_movimentacao == 'E':
            produto.quantidade_estoque += quantidade_solicitada
            produto.save()

    
        serializer.save(usuario=self.request.user)