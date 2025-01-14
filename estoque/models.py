from django.db import models
from servicos.models import CategoriaManutencao

class Estoque(models.Model):
    nome = models.OneToOneField(CategoriaManutencao, on_delete=models.SET_NULL, null=True)
    quantidade_em_estoque = models.IntegerField()
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome.titulo} - {self.quantidade_em_estoque} em estoque'
