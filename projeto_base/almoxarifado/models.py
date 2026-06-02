from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    OPERADOR = 'OPERADOR'
    ADMINISTRADOR = 'ADMINISTRADOR'
    TIPO_CHOICES = [
        (OPERADOR, 'Operador de Almoxarifado'),
        (ADMINISTRADOR, 'Administrador do Sistema'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=OPERADOR)

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
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"
