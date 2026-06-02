from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, MovimentacaoViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, MovimentacaoViewSet, UserCreateView

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'movimentacoes', MovimentacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registo/', UserCreateView.as_view(), name='user-register'), 
]


