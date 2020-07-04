from django.db import models

class Revendedor(models.Model):

    class Meta:

        db_table = 'revendedores'

    Nome = models.CharField(max_length=200)
    CPF = models.CharField(max_length=12)
    Email = models.CharField(max_length=200)
    Senha = models.CharField(max_length=6)
    Super = models.BooleanField(default=False)

    def __str__(self):
        return self.Nome


class FaixaCashBack(models.Model):

    class Meta:

        db_table = 'faixa_cashback'

    Descricao = models.CharField(max_length=200)
    Porcentagem = models.FloatField()
    FaixaTop = models.FloatField()
    FaixaIni = models.FloatField(default=0)

    def __str__(self):
        return self.Descricao


class Compras(models.Model):

    class Meta:

        db_table = 'compras'
        
    FaixaCashBack = models.ForeignKey('FaixaCashBack', related_name='faixacash')
    Revendedor = models.ForeignKey('Revendedor', related_name='revendedor')
    Data = models.DateField()
    ValorCompra = models.FloatField(blank=True, null=True)
    Status = models.CharField(max_length=12, default="Em Validacao", blank=True, null=True)

    def __str__(self):
        return self.Data