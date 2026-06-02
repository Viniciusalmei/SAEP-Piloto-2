from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_estoque = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} (Qtd: {self.quantidade_estoque})"

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data_hora = models.DateTimeField(default=timezone.now)
    
    usuario_responsavel = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"

    def save(self, *args, **kwargs):
        
        if self.tipo == 'saida':
            if self.quantidade > self.produto.quantidade_estoque:
                raise ValidationError(
                    f"Saída não permitida: estoque insuficiente. "
                    f"Disponível: {self.produto.quantidade_estoque}. "
                    f"Solicitado: {self.quantidade}."
                )
            self.produto.quantidade_estoque -= self.quantidade
        elif self.tipo == 'entrada':
            self.produto.quantidade_estoque += self.quantidade
            
        self.produto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.produto.nome} ({self.quantidade})"