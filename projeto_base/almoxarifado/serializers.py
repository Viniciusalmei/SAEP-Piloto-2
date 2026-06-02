from rest_framework import serializers
from .models import Produto, Movimentacao
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

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

    class Meta:
        model = Movimentacao
        fields = '__all__'
        read_only_fields = ['usuario', 'data_hora']

Usuario = get_user_model()

class CadastroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo']

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)