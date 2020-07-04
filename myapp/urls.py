from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'^revendedores/$', views.RevendedorList.as_view(), name='revendedores-list'),
    url(r'^revendedor/(?P<pk>[0-9]+)/$', views.RevendedorDetail.as_view(), name='revendedor-detail'),
    url(r'^faixas-cashback/$', views.FaixaCashBackList.as_view(), name='faixascasback-list'),
    url(r'^compras/$', views.ComprasList.as_view(), name='compras-list'),
    url(r'^compras-revendedor/$', views.ComprasDetailList.as_view({'get': 'list'}), name='compras-detail'),
    url(r'^validate-login/$', views.ValidatePasswordList.as_view({'get': 'list'}), name='validate-login-list'),
    url(r'^cashback/$', views.CashBackList.as_view({'get': 'list'}), name='compras-list'),
    url(r'^user/', views.UserList.as_view({'post': 'post'}), name='revendedores-list'),
    url(r'^token/', obtain_jwt_token, name='token_obtain_pair')
]