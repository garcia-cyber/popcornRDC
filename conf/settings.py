"""
Django settings for conf project.

Adapté pour le déploiement sur Render, en utilisant SQLite (attention aux données éphémères).
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. SECURITY AND DEBUGGING (PRODUCTION CONFIGURATION) ---

# CRITIQUE : La SECRET_KEY est chargée depuis l'environnement. 
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG: Charger la valeur depuis l'environnement, avec une valeur par défaut 'False'.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Utilise la variable d'environnement en production, mais inclut 
# un fallback pour le développement local si DEBUG=True.
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'popcornrdc.onrender.com']
else:
    # Récupère tous les hôtes autorisés depuis la variable d'environnement (séparés par des virgules)
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# CSRF_TRUSTED_ORIGINS: Nécessaire pour la sécurité des formulaires en production.
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app' , 
]

MIDDLEWARE = [
    # WhiteNoise doit être placé juste après SecurityMiddleware.
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Pour servir les statiques en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# --- 2. DATABASE CONFIG (SQLITE FOR RENDER) ---
# ATTENTION : Les données seront perdues à chaque redéploiement sur Render !
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation (Inchangé)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization (Inchangé)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- 3. STATIC FILES (WHITENOISE CONFIG) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
   BASE_DIR / 'static' 
] 

# Configuration de WhiteNoise pour la gestion des statiques en production.
if not DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


# Auth URLs (Inchangé)
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/home/' 


# Media files (Fichiers utilisateurs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'