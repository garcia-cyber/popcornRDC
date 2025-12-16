"""
Django settings for conf project, adapted for production deployment on Render.
"""

from pathlib import Path
import os
import dj_database_url # Nécessite 'pip install dj-database-url psycopg2-binary'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. SECURITY AND DEBUGGING (PRODUCTION CONFIG) ---
# La Clé Secrète DOIT être chargée depuis les variables d'environnement sur Render.
# Assurez-vous de définir SECRET_KEY sur la plateforme Render.
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG DOIT être False en production. On le charge via une variable d'environnement.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS DOIT lister les domaines de Render (chargés via ENV VAR).
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Trusted origins pour la protection CSRF (Render URL)
CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_TRUSTED_ORIGINS')]


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


# --- 2. DATABASE CONFIG (POSTGRESQL FOR RENDER) ---

# Par défaut (pour le développement local si DEBUG=True)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si DEBUG est False (production), on configure la connexion PostgreSQL
# en utilisant la variable d'environnement DATABASE_URL fournie par Render.
if not DEBUG:
    # Utilisez dj_database_url pour analyser la chaîne de connexion
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, 
        ssl_require=True # Exigé par Render pour les connexions sécurisées
    )


# Password validation
# (Reste inchangé)
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- 3. STATIC FILES (WHITENOISE CONFIG) ---
# WhiteNoise gérera ces fichiers en production.
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   
STATICFILES_DIRS = [
        BASE_DIR / 'static'  
]  


# Configuration de WhiteNoise pour la gestion des statiques en production.
# Cela permet de compresser et d'ajouter un hash aux noms de fichiers (cache-busting).
if not DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


# Auth URLs (Reste inchangé)
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/home/' 


# Media files (Fichiers utilisateurs)
# Ces fichiers DOIVENT être stockés sur un service cloud (ex: AWS S3) en prod.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'