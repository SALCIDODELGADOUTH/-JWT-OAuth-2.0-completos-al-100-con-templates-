from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import api_views
from . import oauth_views  # Importación correcta de tus vistas de OAuth

router = DefaultRouter()
router.register(r'libros', api_views.LibroViewSet, basename='libro')
router.register(r'autores', api_views.AutorViewSet, basename='autor')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'prestamos', api_views.PrestamoViewSet, basename='prestamo')

urlpatterns = [
    # ─────────────────────────────────
    # 🔐 AUTENTICACIÓN JWT (Tradicional)
    # ─────────────────────────────────
    path('auth/jwt/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ─────────────────────────────────
    # 🔑 AUTENTICACIÓN OAUTH 2.0 (GOOGLE)
    # ─────────────────────────────────
    # Esta es la que usa el botón de "Login con Google"
# En libros/api_urls.py
    path('auth/google/login/', oauth_views.google_oauth_redirect, name='google_login'),    
    # Esta es la URL que Google busca al terminar la autenticación
    path('auth/google/callback/', oauth_views.google_oauth_callback, name='google_callback'),
    
    # Este es el endpoint opcional que el servidor buscaba en tu error anterior
    path('auth/google/redirect/', oauth_views.google_oauth_redirect, name='google_redirect'),
    
    # ─────────────────────────────────
    # 📚 ENDPOINTS CRUD (Automáticos)
    # ─────────────────────────────────
    path('', include(router.urls)),
]