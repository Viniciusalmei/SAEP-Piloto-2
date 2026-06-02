from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from .models import Produto, Movimentacao
from .serializers import (
    ProdutoSerializer,
    MovimentacaoSerializer,
    CadastroSerializer
)
from .permissions import OperadorOuAdmin
from . import services


Usuario = get_user_model()


class CadastroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CadastroSerializer
    permission_classes = [AllowAny]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [OperadorOuAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['nome', 'data_cadastro']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro']


class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    permission_classes = [OperadorOuAdmin]

    def perform_create(self, serializer):
        produto_id = self.request.data.get('produto')
        quantidade = int(self.request.data.get('quantidade'))
        tipo = self.request.data.get('tipo')

        try:
            services.registrar_movimentacao(
                produto_id=produto_id,
                quantidade=quantidade,
                tipo=tipo,
                usuario=self.request.user
            )
        except ValueError as e:
            raise ValidationError({
                'mensagem': str(e)
            })

        serializer.save(usuario=self.request.user)