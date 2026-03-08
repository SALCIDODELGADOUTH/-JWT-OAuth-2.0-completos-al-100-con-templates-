import requests
from urllib.parse import urlencode
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import redirect

# --- CONFIGURACIÓN DE GOOGLE ---
google_config = {
    'client_id': 'id_oculto',
    'secret': 'secreto_oculto',
}

# La URI que te pide tu guía para la comunicación con Google
REDIRECT_URI = 'http://127.0.0.1:8000/api/auth/google/callback/'

# ¡CORRECCIÓN APLICADA AQUÍ! 
# Ahora apunta a la ruta de tu página morada según tu urls.py
FRONTEND_URL = 'http://127.0.0.1:8000/oauth/login/'


@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_redirect(request):
    """Paso 1: Redirige a Google"""
    scopes = ['openid', 'email', 'profile']
    params = {
        'client_id': google_config["client_id"],
        'redirect_uri': REDIRECT_URI,
        'scope': " ".join(scopes),
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}'
    return redirect(auth_url)


@api_view(['GET', 'POST'])
@authentication_classes([]) # <--- ¡AQUÍ ESTÁ LA MAGIA! Esto apaga el escudo CSRF de DRF
@permission_classes([AllowAny])
def google_oauth_callback(request):
    """Paso 2 y 3: Maneja el regreso de Google Y la petición del JavaScript"""
    
    # ==========================================================
    # CASO GET: Google te devuelve aquí.
    # Acción: Te redirigimos a tu PANTALLA MORADA pasándole el código.
    # ==========================================================
    if request.method == 'GET':
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'No se recibió código de Google'}, status=400)
        
        # ¡Esto evita que te quedes atascado en la pantalla blanca de DRF!
        return redirect(f'{FRONTEND_URL}?code={code}')

    # ==========================================================
    # CASO POST: El fetch de tu JavaScript (pantalla morada) pide los datos.
    # Acción: Validamos con Google y devolvemos JSON (tu foto, nombre, etc).
    # ==========================================================
    elif request.method == 'POST':
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Código no proporcionado'}, status=400)
        
        # Intercambiar código por Token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': google_config['client_id'],
            'client_secret': google_config['secret'],
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response({'error': 'Error en token', 'details': token_json}, status=400)

        # Obtener información real del usuario
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        user_info_response = requests.get(user_info_url, params={'access_token': access_token})
        user_data = user_info_response.json()

        # Devolvemos el JSON que tu HTML está esperando para pintar tu foto
        return Response({
            'message': 'Login exitoso con Google',
            'access': access_token,
            'refresh': 'dummy',
            'user': {
                'email': user_data.get('email'),
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', ''),
                'username': user_data.get('email', '').split('@')[0],
            },
            'google_data': {
                'picture': user_data.get('picture')
            }
        })