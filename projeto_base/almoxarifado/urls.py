from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProdutoViewSet, MovimentacaoViewSet, CadastroUsuarioViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'movimentacoes', MovimentacaoViewSet)
router.register(r'usuarios', CadastroUsuarioViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Rotas para efetuar Login e obter Token JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]