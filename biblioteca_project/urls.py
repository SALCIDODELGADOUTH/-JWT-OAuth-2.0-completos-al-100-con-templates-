from django.contrib import admin
from django.urls import path, include
from libros import web_views
from libros import oauth_views  # IMPORTANTE: Importar tus vistas de OAuth
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from libros.jwt_views import CustomTokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT personalizado (Configuración según tu guía)
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),

    # 1. URLs de la API (Para tus endpoints de libros, etc.)
    path('api/', include('libros.api_urls')),

    # 2. Endpoints de Autenticación Google (ESTOS SON CLAVE)
    # El botón en home.html debe apuntar a: /api/auth/google/login/
    path('api/auth/google/login/', oauth_views.google_oauth_redirect, name='google_login'),
    
    # Esta es la URL que Google busca al regresar (Callback)
    path('api/auth/google/callback/', oauth_views.google_oauth_callback, name='google_callback'),

    # 3. URLs de páginas web (Templates HTML)
    path('', web_views.home, name='home'),
    
    # Esta ruta es donde se renderizarán tus datos de usuario y el TOKEN JWT
    path('oauth/login/', web_views.oauth_login, name='oauth_login'),
    
    path('login/jwt/', web_views.jwt_login_page, name='jwt_login_page'),

    # 4. GraphQL (Con protección CSRF desactivada para pruebas en GraphiQL)
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]