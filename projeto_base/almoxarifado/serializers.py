from rest_framework import serializers
from .models import Produto, Movimentacao
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class MovimentacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.ReadOnlyField(source='usuario.username')
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    data_hora = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    
    estoque_anterior = serializers.SerializerMethodField()
    estoque_atual = serializers.SerializerMethodField()

    class Meta:
        model = Movimentacao
        fields = ['id', 'usuario', 'usuario_nome', 'produto', 'produto_nome',
                  'tipo', 'quantidade', 'estoque_anterior', 'estoque_atual',
                  'data_hora']
        read_only_fields = ['usuario', 'data_hora']

    def get_estoque_anterior(self, obj):
        if obj.tipo == 'E':
            return obj.produto.quantidade_estoque - obj.quantidade
        elif obj.tipo == 'S':
            return obj.produto.quantidade_estoque + obj.quantidade
        return obj.produto.quantidade_estoque

    def get_estoque_atual(self, obj):
        return obj.produto.quantidade_estoque
