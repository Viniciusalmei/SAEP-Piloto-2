from rest_framework import serializers
from .models import Produto, Movimentacao, UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['tipo']

class UserSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source='perfil.tipo', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        UserProfile.objects.create(user=user, tipo='operador')
        return user

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