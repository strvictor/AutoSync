from django.db import models
from secrets import token_hex
from datetime import datetime
from clientes.models import Cliente, Carro
from .categorias import ChoicesCategoriaManutencao
import locale


# class CategoriaManutencao(models.Model):
#     titulo = models.CharField(max_length=100, choices=ChoicesCategoriaManutencao.choices)
#     preco = models.DecimalField(max_digits=7, decimal_places=2)

#     def __str__(self):
#         return self.titulo

class CategoriaManutencao(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.titulo

class Servicos(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    carro = models.ForeignKey(Carro, on_delete=models.SET_NULL, null=True, blank=True)
    categoria_manutencao = models.ManyToManyField(
        CategoriaManutencao, through='ServicoCategoriaQuantidade'
    )

    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    notifica_cliente = models.CharField(max_length=4, default='True')
    protocolo = models.CharField(max_length=18, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.titulo} | {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime('%d%m%Y%H%M%S') + token_hex(2)
        super(Servicos, self).save(*args, **kwargs)

    def preco_total(self):

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        preco_total = 0.0
        for item in self.servicocategoriaquantidade_set.all():
            preco_total += float(item.categoria.preco) * item.quantidade
        return locale.currency(preco_total, grouping=True, symbol=False)


class ServicoCategoriaQuantidade(models.Model):
    servico = models.ForeignKey(Servicos, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaManutencao, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.servico.titulo} - {self.categoria.titulo} (Quantidade: {self.quantidade})"

