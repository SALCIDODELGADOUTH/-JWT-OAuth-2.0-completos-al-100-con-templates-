from django.shortcuts import render, redirect
from django.conf import settings


def home(request):
    """Página de inicio"""
    return render(request, 'home.html')


def oauth_login(request):
    """Página de login con OAuth que maneja el callback de Google"""
    user_data = request.session.get('user_data', None)
    context = {
        'user': user_data,
        'message': "¡Login exitoso con Google!" if user_data else "No se pudo iniciar sesión"
    }
    return render(request, 'oauth_login.html', context)


def jwt_login_page(request):
    """Página de login con JWT (tradicional)"""
    return render(request, 'jwt_login.html')