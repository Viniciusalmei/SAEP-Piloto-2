from django.db import models
from django.contrib.auth.models import User
from rest_framework import permissions

class IsAdminOrOperatorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 1. Garante o acesso privado (exige autenticação) 
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Restrição do método DELETE (Apenas para Administradores) 
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.is_superuser
            
       
        metodos_permitidos = ['GET', 'POST', 'PUT']
        if request.method in metodos_permitidos:
            return True
            
        return False

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    quantidade_estoque = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    data_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"
