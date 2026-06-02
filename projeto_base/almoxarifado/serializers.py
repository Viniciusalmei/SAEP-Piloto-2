from rest_framework import serializers
from .models import Produto, Movimentacao, Perfil
from django.contrib.auth.models import User

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['tipo']

class UserSerializer(serializers.ModelSerializer):
   
    perfil = PerfilSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil']

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

    def validate(self, data):
        tipo = data.get('tipo')
        quantidade = data.get('quantidade')
        produto = data.get('produto')

        # Bloqueio de operação e Mensagem erro
        if tipo == 'S' and quantidade > produto.quantidade_estoque:
            mensagem = f"Saída não permitida: estoque insuficiente. Disponível {produto.quantidade_estoque}: Solicitado:{quantidade}"
            raise serializers.ValidationError(mensagem)
        
        return data

    def create(self, validated_data):
        tipo = validated_data.get('tipo')
        quantidade = validated_data.get('quantidade')
        produto = validated_data.get('produto')

        # Lógica de atualização do estoque
        if tipo == 'E':
            produto.quantidade_estoque += quantidade
        elif tipo == 'S':
           
            produto.quantidade_estoque -= quantidade
        
        produto.save()

        
        return super().create(validated_data)