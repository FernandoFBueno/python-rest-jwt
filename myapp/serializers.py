from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import Revendedor, FaixaCashBack, Compras

class RevendedorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Revendedor
        fields = '__all__'


class ValidatePasswordSerializer(serializers.ModelSerializer):

    class Meta:

        model = Revendedor
        fields = ('Email', 'Senha')

class FaixaCashBackSerializer(serializers.ModelSerializer):

    class Meta:

        model = FaixaCashBack
        fields = '__all__'

class ComprasSerializer(serializers.ModelSerializer):

    RevendedorNome = serializers.CharField(read_only=True, source="Revendedor.Nome")
    PorcentagemCash = serializers.CharField(read_only=True, source="FaixaCashBack.Porcentagem")
    ValorCash = serializers.SerializerMethodField()

    class Meta:

        model = Compras
        fields = ('id', 'RevendedorNome', 'Revendedor', 'FaixaCashBack', 'ValorCompra', 'Data', 'PorcentagemCash', 'ValorCash', 'Status')

    def get_ValorCash(self, instance):
        return (instance.ValorCompra * instance.FaixaCashBack.Porcentagem) / 100

