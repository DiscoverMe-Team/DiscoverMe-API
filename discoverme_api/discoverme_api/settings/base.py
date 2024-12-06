from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers  # type: ignore
import os

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = 'django-insecure-)wwhqs#_(zf=qnm0l-^r^8b@0tv3cc+wq8xsazde$85uu38ks)'
DEBUG = False

ALLOWED_HOSTS = ['discovermeapp.com']

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'base',
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'discoverme_api.urls'

# Template Settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI Application
WSGI_APPLICATION = 'discoverme_api.wsgi.application'

# Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Set your minimum password length
        }
    },
]


# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['Authorization', 'Content-Type']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

# AWS SES
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_PORT = 587
AWS_SES_REGION_NAME = 'us-east-1'  # Replace with your region
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = 'no-reply@discovermeapp.com'
EMAIL_USE_TLS = True