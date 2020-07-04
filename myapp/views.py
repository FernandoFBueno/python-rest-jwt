import requests
import time
import logging
from django.contrib.auth.models import User
from django.shortcuts import render
from django_filters import rest_framework as filters
from django.http import Http404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Revendedor, FaixaCashBack, Compras
from .serializers import RevendedorSerializer, FaixaCashBackSerializer, ComprasSerializer, ValidatePasswordSerializer

MAX_RETRIES = 5
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', filename='logs.log', encoding='utf-8', level=logging.DEBUG)


class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', True),
            "message": args.get('message', 'success'),
            "revendedor": args.get('revendedor', []),
        }

class ResponseInfoCompras(object):
    def __init__(self, **args):
        self.response = {
            "message": args.get('message', 'success'),
            "compras": args.get('compras', []),
        }

class UserList(viewsets.ModelViewSet):
    http_method_names = ["post"]
    queryset = Revendedor.objects.all()
    serializer_class = RevendedorSerializer

    def post(self, request, *args, **kwargs):
        try:
            request._request.POST = request._request.POST.copy()
            self.create(request, *args, **kwargs)
            user = User.objects.create_user(request.data["CPF"],request.data["Email"],request.data["Senha"])
            logging.info('Usuario para o CPF %s criado.'%(str(request.data["CPF"])))
            return Response({"message": "Revendedor cadastrado com sucesso"}, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e
            logging.error('Error in field %s.'%(str(errorMessage)))
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)

class RevendedorList(generics.ListCreateAPIView):

    queryset = Revendedor.objects.all()
    serializer_class = RevendedorSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            request._request.POST = request._request.POST.copy()
            self.create(request, *args, **kwargs)
            user = User.objects.create_user(request.data["CPF"],request.data["Email"],request.data["Senha"])
            logging.info('Usuario para o CPF %s criado.'%(str(request.data["CPF"])))
            return Response({"message": "Revendedor cadastrado com sucesso"}, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e
            logging.error('Error in field %s.'%(str(errorMessage)))
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)


class RevendedorDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Revendedor.objects.all()
    serializer_class = RevendedorSerializer
    permission_classes = (IsAuthenticated,)


class FaixaCashBackList(generics.ListCreateAPIView):

    queryset = FaixaCashBack.objects.all()
    serializer_class = FaixaCashBackSerializer
    permission_classes = (IsAuthenticated,)


class ValidatePasswordList(viewsets.ModelViewSet):
    
    http_method_names = ["get"]
    queryset = Revendedor.objects.all()
    serializer_class = ValidatePasswordSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ValidatePasswordList, self).__init__(**kwargs)
    
    def list(self, request, *args, **kwargs):
        try:
            revendedor = Revendedor.objects.filter(Email=request.data["Email"], Senha=request.data["Senha"])
            if (revendedor.count() > 0):
                serializer = RevendedorSerializer(revendedor, many=True)
                self.response_format['revendedor'] = serializer.data
                self.response_format["status"] = True
                self.response_format["message"] = "Is valid password"
            else:
                self.response_format["message"] = "Not is valid password"
                self.response_format["status"] = False
            return Response(self.response_format)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)
            

class ComprasFilter(filters.FilterSet):

    Data_gte = filters.DateFilter(name="Data", lookup_expr='gte')
    Data_lte = filters.DateFilter(name="Data", lookup_expr='lte')

    class Meta:
        model = Compras
        fields = '__all__'

class ComprasList(generics.ListCreateAPIView):

    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ComprasFilter
    filter_fields = '__all__'
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            request._request.POST = request._request.POST.copy()

            faixacashback = FaixaCashBack.objects.filter(FaixaIni__lte=request.data["ValorCompra"], FaixaTop__gte=request.data["ValorCompra"])
            
            if (faixacashback.count() > 0):
                for fc in faixacashback:
                    request.data["FaixaCashBack"] = fc.id
            else:
                faixacashback = FaixaCashBack.objects.raw('Select Max(FaixaIni), * From faixa_cashback')
                for fc in faixacashback:
                    request.data["FaixaCashBack"] = fc.id

            revendedor = Revendedor.objects.filter(id=request.data["Revendedor"])
            revCPF = ''

            for rev in revendedor:
                request.data["Revendedor"] = rev.id
                revCPF = rev.CPF
                if(rev.Super):
                    request.data["Status"] = "Aprovado"
                else:
                    request.data["Status"] = "Em Validacao"

            logging.info('Compra para o CPF %s cadastrada.'%(str(revCPF)))
            return self.create(request, *args, **kwargs)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e

            logging.error('Error in field %s.'%(str(errorMessage)))
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)

class ComprasDetailList(viewsets.ModelViewSet):

    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfoCompras().response
        super(ComprasDetailList, self).__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        try:
            revendedor = Revendedor.objects.filter(CPF=request.data["cpf"])
            revID = 0

            for rev in revendedor:
                revID = rev.id
            
            compras = Compras.objects.filter(Revendedor=revID)

            if (compras.count() > 0):
                serializer = ComprasSerializer(compras, many=True)
                self.response_format["compras"] = serializer.data
            else:
                self.response_format["message"] = "Not found"
            
            return Response(self.response_format)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e

            logging.error('Error in field %s.'%(str(errorMessage)))
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)


class CashBackList(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        try:
            q = request.data["cpf"]
            url = "https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf=%s"%(str(q))

            if request.method == "GET":
                attempt_num = 0
                while attempt_num < MAX_RETRIES:
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        data = r.json()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        attempt_num += 1
                        time.sleep(5)
                return Response({"error": "Request failed"}, status=r.status_code)
            else:
                return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if hasattr(e, 'message'):
                errorMessage = e.message
            else:
                errorMessage = e
            
            logging.error('Error %s.'%(str(errorMessage)))
            return Response({"error": errorMessage}, status=status.HTTP_400_BAD_REQUEST)