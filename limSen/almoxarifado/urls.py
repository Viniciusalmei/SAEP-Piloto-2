from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, MovimentacaoViewSet


router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'movimentacoes', MovimentacaoViewSet, basename='movimentacao')

urlpatterns = [   
    path('', include(router.urls)),
]