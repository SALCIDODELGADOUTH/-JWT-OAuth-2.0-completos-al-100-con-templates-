from pathlib import Path
from datetime import timedelta 

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-y9se3_3ui!j$)lj(m#5@&&mtj5z2!5mb$_l(tf2c7$0i+t!)hf'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    

    # Third-party apps
    'django_extensions',
    'oauth2_provider',
    'rest_framework',
    'corsheaders', 
    'django_filters', 
    'rest_framework_simplejwt', 
    'allauth',          
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Tu aplicación
    'libros',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  
]

ROOT_URLCONF = 'biblioteca_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'biblioteca_project.wsgi.application'

# Database (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'biblioteca_uni4',
        'USER': 'root',
        'PASSWORD': '', 
        'HOST': 'localhost',
        'PORT': '3307',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Hermosillo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# REST FRAMEWORK CONFIG
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# SIMPLE JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ALLAUTH / GOOGLE
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': 'id_oculto',
            'secret': 'secreto_oculto',
            'key': ''
        }
    }
}

# =========================================================
# OAUTH 2.0 PROVIDER SETTINGS 
# =========================================================
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,       
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 7, 
    
    'SCOPES': {
        'read': 'Acceso de lectura',
        'write': 'Acceso de escritura',
    },
    
    # ¡CORREGIDO! Sin la palabra ".models."
    'ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
    
    'PKCE_REQUIRED': False,
}

# Variables globales para evitar errores extra
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
OAUTH2_PROVIDER_ID_TOKEN_MODEL = 'oauth2_provider.IDToken'

# =========================================================
# CORRECCIÓN DE ERROR "TOO MANY VALUES TO UNPACK"
# (Mantenemos estas variables globales que te salvaron la vida)
# =========================================================
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
OAUTH2_PROVIDER_ID_TOKEN_MODEL = 'oauth2_provider.IDToken'
# Ya no ponemos aquí AccessToken y RefreshToken porque ya están dentro del diccionario