import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from .models import Revendedor, FaixaCashBack, Compras
from rest_framework.test import (APIClient)

class RevendedorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Revendedor.objects.create(Nome="Teste 0", CPF="32132132123", Email="teste@teste.com", Senha="12345", Super=True)

    def test_revendedor_login(self):
        revendedor = Revendedor.objects.get(Email="teste@teste.com")
        self.assertEqual(revendedor.Senha, '12345')
    
    def test_revendedor_endpoint(self):
        url = "/token/"
        u = User.objects.create_user('user','user@user.com','12345')
        resp = self.client.post(url, {'username':'user', 'password':'12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        data = {
            "Nome": "Teste 1",
            "CPF": "32112332112",
            "Email": "teste1@teste.com",
            "Senha": "12345",
            "Super": False
        }

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        resp = self.client.post("/revendedores/", data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

class ComprasTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Revendedor.objects.create(Nome="Teste 1", CPF="32132132123", Email="teste@teste.com", Senha="12345", Super=True)
        FaixaCashBack.objects.create(Descricao="Faixa 1", Porcentagem=10, FaixaTop=1000, FaixaIni=0)
        FaixaCashBack.objects.create(Descricao="Faixa 2", Porcentagem=15, FaixaTop=1500, FaixaIni=1000.1)
        FaixaCashBack.objects.create(Descricao="Faixa 3", Porcentagem=20, FaixaTop=500, FaixaIni=1500.1)
        
    def test_compra(self):
        faixacash = FaixaCashBack.objects.get(id=1)
        revendedor = Revendedor.objects.get(id=1)
        Compras.objects.create(FaixaCashBack=faixacash, Revendedor=revendedor, Data=datetime.date.today(), ValorCompra=600, Status="Em Analise")
        compra = Compras.objects.get(Revendedor=1)
        self.assertEqual(compra.Data, datetime.date.today())

    def check_faixa_cash(self):
        faixacash = FaixaCashBack.objects.get(id=1)
        compra = Compras.objects.get(Revendedor=1)
        self.assertEqual(compra.FaixaCashBack, faixacash)

    def test_compras_endpoint(self):
        url = "/token/"
        u = User.objects.create_user('user','user@user.com','12345')
        resp = self.client.post(url, {'username':'user', 'password':'12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        data = {
            "Revendedor": 1,
            "ValorCompra": 400.0,
            "Data": "2020-06-29",
            "Status": "Em Validacao"
        }
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        resp = self.client.post("/compras/", data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    

    def test_token(self):
        url = "/token/"
        u = User.objects.create_user('user','user@user.com','12345')
        u.is_active = False
        u.save()

        resp = self.client.post(url, {'email':'user@user.com', 'password':'1234'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        resp = self.client.post(url, {'username':'user', 'password':'12345'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = self.client.get('/compras/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        resp = self.client.get('/compras/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)